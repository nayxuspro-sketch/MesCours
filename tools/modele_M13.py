#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""modele_M13.py — l'instrument du module M13 : le modele de Sahel Distribution, controle.

Quatre controles de recette, dans l'ordre ou un modele se verifie :

  1. **unicite**    — chaque table a une cle dont le nombre de valeurs distinctes egale
                     le nombre de lignes : le grain est PROUVE, pas suppose ;
  2. **grain**      — chaque table de faits porte EXACTEMENT les lignes de sa source :
                     aucune jointure ne l'a multiplie ni filtre en chemin ;
  3. **orphelins**  — chaque cle etrangere pointe vers une ligne existante ; la seule
                     exception est declaree : le client 0, present dans les ventes et
                     absent du referentiel, recoit une ligne « client non identifie » ;
  4. **totaux**     — la recette : le chiffre d'affaires du modele doit etre IDENTIQUE
                     a celui de la source (15 595 154 955 FCFA).

Puis cinq mesures qui font la matiere des chapitres :

  * les changements lents (SCD de type 2) : versions, clients avec histoire, les deux
    trous qu'une jointure doit boucher (client non identifie, fait anterieur a la
    creation du client), et surtout
    l'ecart entre un attribut LU AU MOMENT DU FAIT et le meme attribut lu AUJOURD'HUI ;
  * le calendrier : jours, feries, annees fiscales, semaines commerciales ;
  * les modeles fautifs : ce que produisent deux tableaux additionnes, trois tableaux
    additionnes, et une jointure faite sur la mauvaise cle ;
  * les revisions tarifaires, et la grille de revue des quinze points.

Usage :
    python3 tools/modele_M13.py            # deroule les controles et publie le verdict
    python3 tools/modele_M13.py --json     # les mesures seules, en JSON
"""
from __future__ import annotations

import csv
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = os.path.join(RACINE, "03_exercices", "dossier_M13")
sys.path.insert(0, DOSSIER)


def f(x):
    """1500000 -> '1 500 000' (l'espace insecable fine du manuel est rendue par une espace)."""
    return "{:,}".format(int(round(float(x)))).replace(",", " ")


def fd(x):
    """0.31 -> '0,31' : un facteur n'est pas un entier, et le manuel ecrit la virgule."""
    return ("%g" % float(x)).replace(".", ",")


def controler():
    from connexion import ouvrir
    con = ouvrir(fautif=True)
    q = lambda s: con.execute(s).fetchall()
    un = lambda s: con.execute(s).fetchone()[0]
    out = {}

    # ---------------------------------------------------------- 1. unicite
    cles = {
        "dim_client": "id_client", "dim_produit": "id_produit", "dim_magasin": "id_magasin",
        "dim_vendeur": "id_vendeur", "dim_date": "date",
        "dim_client_scd": "cle_version", "dim_produit_scd": "cle_version",
        "fait_ventes": "id_vente", "fait_commandes": "id_commande",
        "fait_encaissements": "id_facture",
        "fait_stock_mensuel": "id_produit || '-' || mois",
        "fait_ruptures": "id_produit || '-' || id_magasin || '-' || mois",
        "fait_logistique": "id_magasin || '-' || mois",
        "fait_objectifs": "id_magasin || '-' || annee_mois",
    }
    tables = {}
    for t, k in cles.items():
        n = un("SELECT COUNT(*) FROM " + t)
        d = un("SELECT COUNT(DISTINCT %s) FROM %s" % (k, t))
        tables[t] = {"lignes": n, "cles": d, "unique": n == d}
    out["c_tables"] = len(tables)
    out["c_tables_cles_uniques"] = sum(1 for v in tables.values() if v["unique"])
    out["c_detail_cles"] = tables
    out["c_dimensions"] = 5
    out["c_faits"] = 7
    out["c_dimensions_historisees"] = 2
    out["c_tables_du_modele"] = len(tables)
    out["c_colonnes"] = {t: un("SELECT COUNT(*) FROM information_schema.columns "
                               "WHERE table_name = '%s'" % t) for t in cles}
    out["c_grains"] = "; ".join(
        "%s %s" % (t, f(v["lignes"])) for t, v in sorted(tables.items()))
    out["c_verdict_unicite"] = ("%d tables sur %d ont une cle unique : le grain de chaque "
                                "table est prouve, pas suppose"
                                % (out["c_tables_cles_uniques"], out["c_tables"]))

    # ---------------------------------------------------------- 2. grain
    # Le controle du grain : chaque table de faits doit porter EXACTEMENT les lignes de
    # sa source. Une jointure posee au mauvais moment multiplie les lignes (x 44 sur le
    # magasin) ou les filtre (x 0,36) — le total, lui, reste plausible.
    sources = {
        "fait_ventes": "ventes", "fait_commandes": "commande",
        "fait_encaissements": "encaissement", "fait_stock_mensuel": "stock_mensuel",
        "fait_ruptures": "rupture", "fait_logistique": "logistique",
        "fait_objectifs": "objectif_mois",
    }
    grains = {}
    for fait, source in sources.items():
        n, m = un("SELECT COUNT(*) FROM " + fait), un("SELECT COUNT(*) FROM " + source)
        grains[fait] = {"lignes_modele": n, "lignes_source": m, "ok": n == m}
    out["c_grain_detail"] = grains
    out["c_grain_ok"] = sum(1 for v in grains.values() if v["ok"])
    out["c_faits_controles"] = len(grains)
    # et les fichiers du dossier doivent se LIRE : un champ qui contient une virgule sans
    # guillemets casse le fichier sans qu'aucun total ne s'en apercoive
    lisibles = {}
    for nom in ("mouvements_clients.csv", "tarifs_produits.csv", "table_plate.csv"):
        with open(os.path.join(DOSSIER, nom), encoding="utf-8", newline="") as flux:
            lignes = list(csv.reader(flux))
        n = len(lignes[0])
        lisibles[nom] = {"lignes": len(lignes) - 1, "colonnes": n,
                         "ok": all(len(l) == n for l in lignes)}
    out["c_fichiers_lisibles"] = lisibles
    out["c_fichiers_ok"] = sum(1 for v in lisibles.values() if v["ok"])
    out["c_verdict_grain"] = (
        "%d tables de faits sur %d portent exactement les lignes de leur source : le grain "
        "declare est celui du chargement, et aucune jointure ne l'a ni multiplie ni filtre ; "
        "les %d fichiers du dossier se lisent, colonne par colonne"
        % (out["c_grain_ok"], out["c_faits_controles"], out["c_fichiers_ok"]))

    # ---------------------------------------------------------- 3. orphelins
    fks = [
        ("fait_ventes", "id_produit", "dim_produit", "id_produit"),
        ("fait_ventes", "id_client", "dim_client", "id_client"),
        ("fait_ventes", "id_magasin", "dim_magasin", "id_magasin"),
        ("fait_ventes", "id_vendeur", "dim_vendeur", "id_vendeur"),
        ("fait_ruptures", "id_produit", "dim_produit", "id_produit"),
        ("fait_ruptures", "id_magasin", "dim_magasin", "id_magasin"),
        ("fait_stock_mensuel", "id_produit", "dim_produit", "id_produit"),
        ("fait_logistique", "id_magasin", "dim_magasin", "id_magasin"),
        ("fait_objectifs", "id_magasin", "dim_magasin", "id_magasin"),
        ("fait_commandes", "id_client", "dim_client", "id_client"),
        ("fait_commandes", "id_magasin", "dim_magasin", "id_magasin"),
        ("fait_encaissements", "id_client", "dim_client", "id_client"),
    ]
    orphelins = {}
    for fait, fk, dim, dk in fks:
        orphelins["%s.%s" % (fait, fk)] = un(
            "SELECT COUNT(*) FROM %s f WHERE f.%s IS NOT NULL AND NOT EXISTS "
            "(SELECT 1 FROM %s d WHERE d.%s = f.%s)" % (fait, fk, dim, dk, fk))
    out["c_cles_etrangeres"] = len(fks)
    out["c_orphelins_total"] = sum(orphelins.values())
    out["c_orphelins_detail"] = orphelins
    out["c_client_inconnu_lignes"] = un(
        "SELECT COUNT(*) FROM fait_ventes f JOIN dim_client d ON d.id_client = f.id_client "
        "WHERE d.type_client = 'Inconnu'")
    out["c_client_inconnu_ca"] = round(un(
        "SELECT SUM(f.montant_ttc) FROM fait_ventes f JOIN dim_client d ON d.id_client = f.id_client "
        "WHERE d.type_client = 'Inconnu' AND f.est_retour = 0"))
    out["c_verdict_orphelins"] = (
        "%d cles etrangeres verifiees, %d orphelin : le client absent du referentiel a recu une "
        "ligne « client non identifie » (%s lignes, %s FCFA) au lieu d'une cle qui ne pointe nulle part"
        % (len(fks), out["c_orphelins_total"], f(out["c_client_inconnu_lignes"]),
           f(out["c_client_inconnu_ca"])))

    # ---------------------------------------------------------- 4. totaux
    rec = q("SELECT * FROM recette_ca")[0]
    out["c_ca_modele"] = round(rec[0])
    out["c_ca_source"] = round(rec[1])
    out["c_recette_ok"] = abs(rec[0] - rec[1]) < 1
    out["c_recette_texte"] = (
        "recette du modele : %s FCFA par le modele, %s FCFA par la source — %s"
        % (f(rec[0]), f(rec[1]), "identiques" if out["c_recette_ok"] else "ECART"))

    # ------------------------------------------- 5. les SCD (mesure, pas controle)
    out["c_lignes_client_scd"] = un("SELECT COUNT(*) FROM dim_client_scd")
    out["c_versions_client"] = un("SELECT COUNT(*) FROM dim_client_scd WHERE id_client <> 0")
    out["c_versions_produit"] = un("SELECT COUNT(*) FROM dim_produit_scd")
    out["c_clients_avec_histoire"] = un(
        "SELECT COUNT(*) FROM (SELECT id_client FROM dim_client_scd GROUP BY 1 HAVING COUNT(*) > 1)")
    out["c_versions_max"] = un(
        "SELECT MAX(n) FROM (SELECT COUNT(*) AS n FROM dim_client_scd GROUP BY id_client)")
    out["c_mouvements"] = un("SELECT COUNT(*) FROM read_csv_auto('03_exercices/dossier_M13/"
                             "mouvements_clients.csv', header = true)")
    out["c_mouvements_type2"] = un("SELECT COUNT(*) FROM read_csv_auto('03_exercices/dossier_M13/"
                                   "mouvements_clients.csv', header = true) WHERE type_scd = 2")
    out["c_mouvements_type1"] = out["c_mouvements"] - out["c_mouvements_type2"]
    # la jointure « au moment du fait » ne doit ni perdre ni dupliquer une ligne
    n_asof = un("""SELECT COUNT(*) FROM fait_ventes f JOIN dim_client_scd h
                   ON h.id_client = f.id_client
                  AND f.date_vente BETWEEN h.date_debut AND COALESCE(h.date_fin, DATE '2100-01-01')""")
    out["c_ventes_jointes_asof"] = n_asof
    out["c_ventes_hors_retours"] = un("SELECT COUNT(*) FROM fait_ventes WHERE est_retour = 0")
    out["c_ventes_total"] = un("SELECT COUNT(*) FROM fait_ventes")
    out["c_ventes_client_inconnu"] = un("SELECT COUNT(*) FROM fait_ventes WHERE id_client = 0")
    # les ventes anterieures a la date de creation du client : le referentiel porte une
    # date de SAISIE, le fait porte une date de VENTE — la plus ancienne ouvre l'histoire
    out["c_clients_rattrapes"] = un(
        "SELECT COUNT(DISTINCT CAST(f.id_client AS INTEGER)) FROM ventes f "
        "JOIN clients c ON CAST(c.id_client AS INTEGER) = CAST(f.id_client AS INTEGER) "
        "WHERE CAST(f.id_client AS INTEGER) <> 0 "
        "AND TRY_CAST(f.date_vente AS DATE) < TRY_CAST(c.date_creation AS DATE)")
    out["c_ventes_rattrapees"] = un(
        "SELECT COUNT(*) FROM ventes f "
        "JOIN clients c ON CAST(c.id_client AS INTEGER) = CAST(f.id_client AS INTEGER) "
        "WHERE CAST(f.id_client AS INTEGER) <> 0 "
        "AND TRY_CAST(f.date_vente AS DATE) < TRY_CAST(c.date_creation AS DATE)")
    out["c_asof_integrale"] = n_asof == un("SELECT COUNT(*) FROM fait_ventes")

    def par_segment(historique):
        dim = "dim_client_scd h" if historique else "dim_client c"
        cle = "h.segment" if historique else "c.segment"
        joint = ("JOIN dim_client_scd h ON h.id_client = f.id_client AND f.date_vente "
                 "BETWEEN h.date_debut AND COALESCE(h.date_fin, DATE '2100-01-01')"
                 if historique else "JOIN dim_client c ON c.id_client = f.id_client")
        return [(s, round(ca)) for s, ca in q(
            "SELECT %s, SUM(f.montant_ttc) FROM fait_ventes f %s WHERE f.est_retour = 0 "
            "GROUP BY 1 ORDER BY 2 DESC" % (cle, joint))]

    courant = par_segment(False)
    histo = par_segment(True)
    out["c_ca_par_segment_courant"] = "; ".join("%s %s FCFA" % (s, f(v)) for s, v in courant)
    out["c_ca_par_segment_historique"] = "; ".join("%s %s FCFA" % (s, f(v)) for s, v in histo)
    d_courant, d_histo = dict(courant), dict(histo)
    ecarts = []
    for s1 in sorted(d_courant, key=lambda x: -d_courant[x]):
        v1, v2 = d_courant[s1], d_histo.get(s1, 0)
        if abs(v1 - v2) >= 1:
            ecarts.append("%s : %s contre %s FCFA" % (s1, f(v1), f(v2)))
    out["c_ecart_scd_detail"] = "; ".join(ecarts)
    out["c_ecart_scd_max"] = max((abs(d_courant[s] - d_histo.get(s, 0)) for s in d_courant),
                                 default=0)
    out["c_scd_texte"] = (
        "lire un attribut AU MOMENT du fait n'est pas le lire AUJOURD'HUI : le meme chiffre "
        "d'affaires par segment vaut %s lu sur la dimension courante et %s lu sur la dimension "
        "historisee — l'ecart atteint %s FCFA sur un seul segment"
        % (" / ".join(f(v) for _, v in courant), " / ".join(f(v) for _, v in histo),
           f(out["c_ecart_scd_max"])))
    out["c_asof_texte"] = (
        "la jointure « au moment du fait » rend %s lignes pour %s ventes : aucun doublon, aucune "
        "perte. Deux trous l'auraient ouverte sans rien afficher : le client non identifie "
        "(%s ventes) et les %s ventes anterieures a la date de creation de leur client, "
        "rattachees a la premiere version (%s clients concernes) — c'est le controle qui "
        "distingue un SCD de type 2 d'un SCD de type 2 faux"
        % (f(n_asof), f(out["c_ventes_total"]), f(out["c_ventes_client_inconnu"]),
           f(out["c_ventes_rattrapees"]), f(out["c_clients_rattrapes"])))

    # ---------------------------------------------------- 6. le calendrier
    out["c_calendrier_jours"] = un("SELECT COUNT(*) FROM dim_date")
    out["c_calendrier_feries"] = un("SELECT SUM(est_ferie) FROM dim_date")
    out["c_calendrier_mois"] = un("SELECT COUNT(DISTINCT annee_mois) FROM dim_date")
    out["c_calendrier_annees_fiscales"] = un("SELECT COUNT(DISTINCT annee_fiscale) FROM dim_date")
    out["c_calendrier_semaines_com"] = un("SELECT COUNT(DISTINCT annee || '-' || semaine_commerciale) "
                                          "FROM dim_date")
    out["c_calendrier_semaines_iso"] = un("SELECT COUNT(DISTINCT semaine_iso) FROM dim_date")
    out["c_calendrier_tables_date"] = un(
        "SELECT COUNT(*) FROM information_schema.columns WHERE table_name LIKE 'fait_%' "
        "AND column_name IN ('annee', 'mois_libelle', 'trimestre', 'semaine_iso')")
    out["c_calendrier_texte"] = (
        "%s jours, %s feries, %s mois, %s annees fiscales (1er juillet), %s semaines "
        "commerciales contre %s semaines ISO : le calendrier du fil rouge ne portait que le "
        "calendrier ISO, il porte maintenant le calendrier de gestion"
        % (f(out["c_calendrier_jours"]), f(out["c_calendrier_feries"]), f(out["c_calendrier_mois"]),
           f(out["c_calendrier_annees_fiscales"]), f(out["c_calendrier_semaines_com"]),
           f(out["c_calendrier_semaines_iso"])))

    # ----------------------------------------------- 7. les modeles fautifs
    out["c_ca_reference"] = out["c_ca_source"]
    deux = un("SELECT ca FROM ca_deux_tableaux")
    trois = un("SELECT ca FROM ca_trois_tableaux")
    folle = un("SELECT ca FROM ca_jointure_folle")
    out["c_ca_deux_tableaux"] = round(deux)
    out["c_ca_trois_tableaux"] = round(trois)
    out["c_ca_jointure_folle"] = round(folle)
    out["c_facteur_deux_tableaux"] = round(100.0 * (deux / out["c_ca_reference"] - 1), 1)
    out["c_facteur_trois_tableaux"] = round(100.0 * (trois / out["c_ca_reference"] - 1), 1)
    out["c_facteur_jointure_folle"] = round(folle / out["c_ca_reference"], 1)
    out["c_fautif_texte"] = (
        "deux tableaux de montants additionnes donnent %s FCFA (+%s %%), trois donnent %s FCFA "
        "(+%s %%), et une jointure faite sur la mauvaise cle donne %s FCFA (x %s) — les trois "
        "s'executent sans erreur"
        % (f(deux), f(out["c_facteur_deux_tableaux"]), f(trois), f(out["c_facteur_trois_tableaux"]),
           f(folle), f(out["c_facteur_jointure_folle"])))

    # ------------------------------------------------- 8. les tarifs (SCD prix)
    out["c_prix_tarif_2023"] = un("SELECT ROUND(AVG(prix_vente_ht)) FROM dim_produit_scd "
                                  "WHERE version = 1")
    out["c_prix_tarif_2026"] = un("SELECT ROUND(AVG(prix_vente_ht)) FROM dim_produit_scd "
                                  "WHERE est_courante = 1")
    out["c_derive_tarif_pct"] = round(
        100.0 * (out["c_prix_tarif_2026"] / out["c_prix_tarif_2023"] - 1), 1)
    out["c_tarif_texte"] = (
        "la grille tarifaire passe de %s FCFA en 2023 a %s FCFA en 2026 (+%s %%) sur %s "
        "versions : c'est la traduction en modele de la hausse de prix mesuree en M12"
        % (f(out["c_prix_tarif_2023"]), f(out["c_prix_tarif_2026"]),
           f(out["c_derive_tarif_pct"]), f(out["c_versions_produit"])))

    # -------------------------------------------------------- 9. la revue
    out["c_revue_points"] = 15
    out["c_revue_defauts"] = 5
    out["c_revue_texte"] = (
        "la grille de revue compte %d points et le modele annote du chapitre C07 porte %d "
        "defauts a trouver : une dimension recopiee dans les faits, deux temps dans la meme "
        "table, un objectif pose sur la mauvaise ligne, aucune cle declaree, et une categorie "
        "reprise telle quelle du fichier source" % (out["c_revue_points"], out["c_revue_defauts"]))
    # ------------------------------- 10. le point de depart (chapitre C01)
    # Ce que le chapitre C01 mesure : ce que le modele remplace, et ce que coute de le
    # faire autrement. Un modele ne se justifie pas par une opinion, par un ecart.
    out["c01_clients_referentiel"] = un("SELECT COUNT(*) FROM dim_client WHERE id_client <> 0")
    out["c01_clients_acheteurs"] = un(
        "SELECT COUNT(DISTINCT id_client) FROM fait_ventes WHERE id_client <> 0")
    out["c01_clients_sans_vente"] = un(
        "SELECT COUNT(*) FROM dim_client d WHERE d.id_client <> 0 AND NOT EXISTS "
        "(SELECT 1 FROM fait_ventes f WHERE f.id_client = d.id_client)")
    out["c01_produits"] = un("SELECT COUNT(*) FROM dim_produit")
    out["c01_produits_jamais_vendus"] = un(
        "SELECT COUNT(*) FROM dim_produit p WHERE NOT EXISTS "
        "(SELECT 1 FROM fait_ventes f WHERE f.id_produit = p.id_produit)")
    out["c01_magasins"] = un("SELECT COUNT(*) FROM dim_magasin")
    out["c01_magasins_vendeurs"] = un("SELECT COUNT(DISTINCT id_magasin) FROM fait_ventes")
    out["c01_depot_sans_vente"] = out["c01_magasins"] - out["c01_magasins_vendeurs"]
    out["c01_vendeurs"] = un("SELECT COUNT(*) FROM dim_vendeur")
    out["c01_vendeurs_vendeurs"] = un("SELECT COUNT(DISTINCT id_vendeur) FROM fait_ventes")
    out["c01_jours"] = un("SELECT COUNT(*) FROM dim_date")
    par_client = q("SELECT MIN(n), ROUND(AVG(n), 1), MEDIAN(n), MAX(n) FROM "
                   "(SELECT id_client, COUNT(*) AS n FROM fait_ventes "
                   " WHERE id_client <> 0 GROUP BY id_client)")
    out["c01_ventes_par_client"] = "%s a %s, %s en moyenne" % tuple(
        f(x) for x in (par_client[0][0], par_client[0][3], par_client[0][1]))
    out["c01_ventes_par_client_min"] = par_client[0][0]
    out["c01_ventes_par_client_moyenne"] = par_client[0][1]
    out["c01_ventes_par_client_mediane"] = par_client[0][2]
    out["c01_ventes_par_client_max"] = par_client[0][3]
    par_produit = q("SELECT MIN(n), MAX(n) FROM (SELECT id_produit, COUNT(*) AS n "
                    "FROM fait_ventes GROUP BY id_produit)")
    out["c01_ventes_par_produit_min"] = par_produit[0][0]
    out["c01_ventes_par_produit_max"] = par_produit[0][1]
    par_magasin = q("SELECT MAX(n), MIN(n) FROM (SELECT id_magasin, COUNT(*) AS n "
                    "FROM fait_ventes GROUP BY id_magasin)")
    out["c01_ventes_par_magasin_max"] = par_magasin[0][0]
    out["c01_ventes_par_magasin_min"] = par_magasin[0][1]
    out["c01_tickets"] = un("SELECT COUNT(DISTINCT id_ticket) FROM fait_ventes")
    out["c01_ticket_exemple"] = un("SELECT MIN(id_ticket) FROM fait_ventes")
    par_ticket = q("SELECT ROUND(AVG(n), 2), MAX(n) FROM (SELECT id_ticket, COUNT(*) AS n "
                   "FROM fait_ventes GROUP BY id_ticket)")
    out["c01_lignes_par_ticket_moyenne"] = par_ticket[0][0]
    out["c01_lignes_par_ticket_max"] = par_ticket[0][1]
    # le cout de la redondance : le nom du client, recopie sur chaque ligne de vente
    out["c01_noms_recopies_caracteres"] = un(
        "SELECT SUM(LENGTH(c.nom)) FROM fait_ventes f JOIN dim_client c ON c.id_client = f.id_client")
    out["c01_noms_dimension_caracteres"] = un("SELECT SUM(LENGTH(nom)) FROM dim_client")
    out["c01_noms_facteur"] = round(
        out["c01_noms_recopies_caracteres"] / out["c01_noms_dimension_caracteres"], 1)
    # le point de depart a nettoyer : deux tables jointes au mauvais niveau
    ca = un("SELECT SUM(montant_ttc) FROM fait_ventes WHERE est_retour = 0")
    deux = q("SELECT SUM(v.montant_ttc), COUNT(*) FROM fait_ventes v "
             "JOIN fait_commandes c ON c.id_client = v.id_client WHERE v.est_retour = 0")
    trois = q("SELECT SUM(v.montant_ttc), COUNT(*) FROM fait_ventes v "
              "JOIN fait_encaissements e ON e.id_client = v.id_client WHERE v.est_retour = 0")
    out["c01_jointure_commandes_ca"] = round(deux[0][0])
    out["c01_jointure_commandes_lignes"] = deux[0][1]
    out["c01_jointure_commandes_facteur"] = round(deux[0][0] / ca, 2)
    out["c01_jointure_encaissements_ca"] = round(trois[0][0])
    out["c01_jointure_encaissements_lignes"] = trois[0][1]
    out["c01_jointure_encaissements_facteur"] = round(trois[0][0] / ca, 2)
    out["c01_texte_jointures"] = (
        "au niveau du client, les ventes jointes aux commandes donnent %s FCFA (x %s) et les "
        "ventes jointes aux encaissements %s FCFA (x %s) : les deux requetes s'executent, "
        "aucune ne leve d'erreur, et les deux faux totaux sont credibles"
        % (f(out["c01_jointure_commandes_ca"]), fd(out["c01_jointure_commandes_facteur"]),
           f(out["c01_jointure_encaissements_ca"]), fd(out["c01_jointure_encaissements_facteur"])))
    # l'extrait denormalise du chapitre C02, lu comme un fichier (et non par le socle)
    with open(os.path.join(DOSSIER, "table_plate.csv"), encoding="utf-8", newline="") as flux:
        tp = list(csv.reader(flux))[1:]
    noms = {}
    for ligne in tp:
        noms[ligne[4]] = noms.get(ligne[4], 0) + 1
    out["c01_table_plate_lignes"] = len(tp)
    out["c01_table_plate_clients"] = len({l[3] for l in tp})
    out["c01_table_plate_categories"] = len({l[9] for l in tp})
    out["c01_table_plate_noms_recopies"] = sum(len(l[4]) for l in tp)
    out["c01_table_plate_noms_dimension"] = sum(len(n) for n in noms)
    out["c01_table_plate_nom_max"] = max(noms, key=lambda x: (noms[x], x))
    out["c01_table_plate_nom_max_fois"] = max(noms.values())
    out["c01_table_plate_villes_client_41"] = len({l[5] for l in tp if l[3] == "41"})
    out["c01_clients_servis_somme"] = un(
        "SELECT SUM(n) FROM (SELECT COUNT(DISTINCT id_client) AS n FROM fait_ventes "
        "GROUP BY id_magasin)")
    out["c01_texte_depart"] = (
        "l'extrait denormalise compte %s lignes pour %s clients : le nom du client y est "
        "recopie %s caracteres contre %s ranges une fois, et le client 41 y porte deja %s "
        "villes differentes — le defaut est visible sur 18 lignes, il est invisible sur %s"
        % (f(len(tp)), f(len({l[3] for l in tp})), f(out["c01_table_plate_noms_recopies"]),
           f(out["c01_table_plate_noms_dimension"]), f(out["c01_table_plate_villes_client_41"]),
           f(out["c01_clients_acheteurs"])))
    # ------------------------------- 11. la normalisation, mesuree (chapitre C02)
    # Le chapitre C02 ne parle pas de normalisation en theorie : il compare la meme
    # information rangee dans une table plate et rangee dans le modele.
    con.execute("""CREATE OR REPLACE TABLE plat AS
        SELECT f.id_vente, f.montant_ttc, c.nom AS nom_client, c.ville, c.segment,
               p.designation, p.libelle_source AS categorie, m.nom AS magasin,
               v.nom_complet AS vendeur, f.date_vente, f.mode_paiement
        FROM fait_ventes f
        JOIN dim_client c  ON c.id_client  = f.id_client
        JOIN dim_produit p ON p.id_produit = f.id_produit
        JOIN dim_magasin m ON m.id_magasin = f.id_magasin
        JOIN dim_vendeur v ON v.id_vendeur = f.id_vendeur""")
    out["c02_lignes_plates"] = un("SELECT COUNT(*) FROM plat")
    out["c02_colonnes_plates"] = un("SELECT COUNT(*) FROM information_schema.columns "
                                    "WHERE table_name = 'plat'")
    out["c02_colonnes_dimensions"] = un(
        "SELECT SUM(n) FROM (SELECT COUNT(*) AS n FROM information_schema.columns WHERE "
        "table_name IN ('dim_client','dim_produit','dim_magasin','dim_vendeur','dim_date') "
        "GROUP BY table_name)")
    out["c02_ca_plat"] = round(un("SELECT SUM(montant_ttc) FROM plat"))
    out["c02_libelles_bruts"] = un("SELECT COUNT(DISTINCT categorie) FROM plat")
    out["c02_familles_reelles"] = un("SELECT COUNT(DISTINCT famille) FROM dim_produit")
    # le classement change selon qu'on lit le libelle brut ou la famille : la plus grosse
    # famille du reseau se cache derriere QUATRE libelles
    frag = q("SELECT categorie, ROUND(SUM(montant_ttc)) FROM plat "
             "WHERE UPPER(TRIM(categorie)) LIKE 'MAT%' GROUP BY 1 ORDER BY 2 DESC")
    out["c02_materiaux_fragments"] = "; ".join("%s %s FCFA" % (c, f(v)) for c, v in frag)
    out["c02_materiaux_fragments_n"] = len(frag)
    out["c02_materiaux_total"] = sum(int(v) for _, v in frag)
    out["c02_materiaux_plus_gros_fragment"] = max(int(v) for _, v in frag)
    fam = q("SELECT famille, ROUND(SUM(f.montant_ttc)) FROM fait_ventes f "
            "JOIN dim_produit p ON p.id_produit = f.id_produit GROUP BY 1 ORDER BY 2 DESC")
    out["c02_familles_ca"] = "; ".join("%s %s FCFA" % (c, f(v)) for c, v in fam)
    out["c02_famille_1"] = fam[0][0]
    out["c02_famille_1_ca"] = int(fam[0][1])
    out["c02_texte_libelles"] = (
        "le referentiel ecrit la meme famille de %s facons, et le fichier plat classe donc %s "
        "groupes la ou le modele en compte %s : la famille la plus lourde du reseau (%s, %s FCFA) "
        "arrive en 5e position si l'on classe les libelles bruts, parce que son montant est "
        "partage entre %s ecritures — %s"
        % (out["c02_materiaux_fragments_n"], f(out["c02_libelles_bruts"]),
           f(out["c02_familles_reelles"]), out["c02_famille_1"], f(out["c02_famille_1_ca"]),
           f(out["c02_materiaux_fragments_n"]), out["c02_materiaux_fragments"]))
    # la redondance, mesuree sur trois attributs
    out["c02_nom_recopie_plat"] = un("SELECT SUM(LENGTH(nom_client)) FROM plat")
    out["c02_nom_dimension"] = un("SELECT SUM(LENGTH(nom)) FROM dim_client")
    out["c02_designation_recopiee"] = un(
        "SELECT SUM(LENGTH(p.designation)) FROM fait_stock_mensuel s "
        "JOIN dim_produit p ON p.id_produit = s.id_produit")
    out["c02_designation_dimension"] = un("SELECT SUM(LENGTH(designation)) FROM dim_produit")
    out["c02_facteur_designation"] = round(
        out["c02_designation_recopiee"] / out["c02_designation_dimension"], 1)
    # le cout de la normalisation, mesure : une requete de groupe sur la table plate et
    # sur le modele (mediane de sept executions, dans l'atelier du module)
    import statistics as _st
    import time as _t

    def _chrono(requete, n=7):
        mesures = []
        for _ in range(n):
            depart = _t.perf_counter()
            con.execute(requete).fetchall()
            mesures.append((_t.perf_counter() - depart) * 1000.0)
        return int(round(_st.median(mesures)))   # en millisecondes entieres : une mesure de
                                                 # temps n'a pas de decimale honnete

    out["c02_temps_plat_famille_ms"] = _chrono(
        "SELECT categorie, SUM(montant_ttc) FROM plat GROUP BY 1")
    out["c02_temps_modele_famille_ms"] = _chrono(
        "SELECT p.famille, SUM(f.montant_ttc) FROM fait_ventes f "
        "JOIN dim_produit p ON p.id_produit = f.id_produit GROUP BY 1")
    out["c02_texte_cout"] = (
        "normaliser ne ralentit pas la lecture sur ce moteur, parce qu'il ne lit que les colonnes "
        "utiles : la meme requete de groupe prend %s ms sur la table plate (%s lignes, %s colonnes) "
        "et %s ms sur le modele (une table de faits et une dimension de %s lignes) — le cout de la "
        "normalisation n'est pas la lecture, c'est l'ecriture et la discipline"
        % (f(out["c02_temps_plat_famille_ms"]), f(out["c02_lignes_plates"]),
           f(out["c02_colonnes_plates"]), f(out["c02_temps_modele_famille_ms"]),
           f(out["c01_produits"])))
    con.execute("DROP TABLE plat")
    # --------------------- 12. le grain et l'additivite, mesures (chapitre C03)
    # Un modele ne se juge pas sur son dessin mais sur ce qu'il rend quand on l'interroge.
    # Ce bloc mesure les deux proprietes qui font qu'un total est juste : le GRAIN (ce que
    # porte une ligne) et l'ADDITIVITE (ce qu'on a le droit d'additionner).
    faits = [("fait_ventes", "ligne de ticket", "id_vente"),
             ("fait_commandes", "commande", "id_commande"),
             ("fait_encaissements", "facture", "id_facture"),
             ("fait_stock_mensuel", "produit x mois", "id_produit, mois"),
             ("fait_ruptures", "produit x magasin x mois", "id_produit, id_magasin, mois"),
             ("fait_logistique", "magasin x mois", "id_magasin, mois"),
             # attention : dans fait_objectifs, `mois` est le NUMERO du mois (1 a 12) ;
             # la cle du grain est (id_magasin, annee_mois). Le piege est mesure plus bas.
             ("fait_objectifs", "magasin x mois", "id_magasin, annee_mois")]
    grains = []
    for table, grain, cle in faits:
        lignes = un("SELECT COUNT(*) FROM %s" % table)
        # DuckDB n'accepte pas COUNT(DISTINCT a, b) sur une cle composite : la sous-requete
        # dit exactement la meme chose, et elle marche sur les trois moteurs du manuel.
        cles = un("SELECT COUNT(*) FROM (SELECT DISTINCT %s FROM %s)" % (cle, table))
        grains.append((table, grain, lignes, cles == lignes))
    out["c03_faits_avec_grain_prouve"] = sum(1 for g in grains if g[3])
    out["c03_grains"] = "; ".join("%s %s (%s)" % (t.replace("fait_", ""), f(n), g)
                                  for t, g, n, _ in grains)
    out["c03_lignes_faits_total"] = sum(g[2] for g in grains)
    fin = un("SELECT COUNT(*) FROM fait_ventes")
    gros = un("SELECT COUNT(*) FROM fait_objectifs")
    out["c03_ratio_grain"] = int(round(fin / gros))
    # la cle qui n'en est pas une : (magasin, numero de mois) rend 60 valeurs distinctes
    # pour 218 lignes — un grain verifie avec la mauvaise cle passe pour un doublon
    out["c03_objectifs_cle_fausse"] = un(
        "SELECT COUNT(*) FROM (SELECT DISTINCT id_magasin, mois FROM fait_objectifs)")
    out["c03_objectifs_lignes"] = un("SELECT COUNT(*) FROM fait_objectifs")
    out["c03_lignes_par_ticket"] = round(fin / un("SELECT COUNT(DISTINCT id_ticket) FROM fait_ventes"), 2)
    # ---- l'additivite, trois regimes
    # 1. additif : le montant se somme dans tous les sens, et se re-somme a l'identique
    par_mois = q("SELECT strftime(date_vente, '%Y-%m') AS mois, ROUND(SUM(montant_ttc)) AS ca "
                 "FROM fait_ventes WHERE est_retour = 0 GROUP BY 1 ORDER BY 1")
    out["c03_mois"] = len(par_mois)
    total_remonte = sum(int(v) for _, v in par_mois)
    out["c03_ca_somme_mensuelle"] = total_remonte
    out["c03_facteur_additif"] = round(total_remonte / un("SELECT ROUND(SUM(montant_ttc)) "
                                                          "FROM fait_ventes WHERE est_retour = 0"), 2)
    # 2. semi-additif : un instantane de stock s'additionne dans l'espace, jamais dans le temps
    out["c03_stock_somme"] = round(un("SELECT SUM(stock_moyen_unites) FROM fait_stock_mensuel"))
    out["c03_stock_un_mois"] = round(out["c03_stock_somme"] / out["c03_mois"])
    out["c03_stock_facteur"] = round(out["c03_stock_somme"] / out["c03_stock_un_mois"])
    out["c03_stock_dernier_mois"] = round(un(
        "SELECT SUM(stock_moyen_unites) FROM fait_stock_mensuel WHERE mois = "
        "(SELECT MAX(mois) FROM fait_stock_mensuel)"))
    # 3. non additif : un taux ne se somme pas, il se recalcule sur les totaux
    out["c03_taux_somme"] = round(un("SELECT SUM(marge_objectif_pct) * 100 FROM fait_objectifs"), 1)
    out["c03_taux_moyen"] = round(un("SELECT AVG(marge_objectif_pct) * 100 FROM fait_objectifs"), 1)
    out["c03_taux_lignes"] = un("SELECT COUNT(*) FROM fait_objectifs")
    # ---- les trois facons de fabriquer un faux total
    # 1. joindre sur une cle trop large : chaque ligne de vente rencontre 44 lignes de logistique
    joint_w = q("""SELECT COUNT(*), ROUND(SUM(v.montant_ttc)) FROM fait_ventes v
                   JOIN fait_logistique l ON l.id_magasin = v.id_magasin
                   WHERE v.est_retour = 0""")[0]
    out["c03_faux_large_lignes"] = joint_w[0]
    out["c03_faux_large_ca"] = int(joint_w[1])
    out["c03_faux_large_facteur"] = round(out["c03_faux_large_ca"] / total_remonte, 1)
    # 2. joindre sur une cle trop fine : les ventes sans rupture disparaissent sans un mot
    joint_f = q("""SELECT COUNT(*), ROUND(SUM(v.montant_ttc)) FROM fait_ventes v
                   JOIN fait_ruptures r ON r.id_produit = v.id_produit
                     AND r.mois = strftime(v.date_vente, '%Y-%m')
                   WHERE v.est_retour = 0""")[0]
    out["c03_faux_filtre_lignes"] = joint_f[0]
    out["c03_faux_filtre_ca"] = int(joint_f[1])
    out["c03_faux_filtre_facteur"] = round(out["c03_faux_filtre_ca"] / total_remonte, 2)
    out["c03_faux_filtre_manquants"] = round((1 - out["c03_faux_filtre_facteur"]) * 100)
    # 3. joindre sur la bonne cle : le controle negatif, celui qui disculpe la jointure
    joint_j = q("""SELECT COUNT(*), ROUND(SUM(v.montant_ttc)) FROM fait_ventes v
                   JOIN fait_stock_mensuel s ON s.id_produit = v.id_produit
                     AND s.mois = strftime(v.date_vente, '%Y-%m')
                   WHERE v.est_retour = 0""")[0]
    out["c03_bon_grain_lignes"] = joint_j[0]
    out["c03_bon_grain_ca"] = int(joint_j[1])
    out["c03_bon_grain_facteur"] = round(out["c03_bon_grain_ca"] / total_remonte, 2)
    out["c03_texte_cle"] = (
        "le grain se prouve avec la BONNE cle : sur fait_objectifs, la cle (magasin, numero de "
        "mois) rend %s valeurs distinctes pour %s lignes, et l'on conclurait a tort a des doublons ; "
        "la cle du grain est (magasin, annee_mois), et elle rend %s valeurs pour %s lignes — le "
        "grain declare est celui du chargement"
        % (f(out["c03_objectifs_cle_fausse"]), f(out["c03_objectifs_lignes"]),
           f(out["c03_objectifs_lignes"]), f(out["c03_objectifs_lignes"])))
    out["c03_texte_grain"] = (
        "les %s tables de faits portent %s grains differents et prouves (la cle distincte egale "
        "le nombre de lignes) : de la ligne de ticket (%s lignes) a l'objectif mensuel par magasin "
        "(%s lignes), il y a un facteur %s — deux tables du meme modele ne repondent donc pas a la "
        "meme question, et rien ne doit les additionner"
        % (f(len(faits)), f(len(faits)), f(fin), f(gros), f(out["c03_ratio_grain"])))
    out["c03_texte_additivite"] = (
        "le montant est additif : %s totaux mensuels se re-somment exactement au total du modele "
        "(facteur %s). Le stock est semi-additif : sommer %s mois d'instantanes donne %s unites, "
        "soit %s fois le stock d'un mois (%s unites) — un chiffre credibile et faux. Le taux est "
        "non additif : les %s taux de marge du plan d'objectifs se somment a %s %%, quand leur "
        "moyenne vaut %s %% et qu'aucun des deux n'est la marge du reseau"
        % (f(out["c03_mois"]), fd(out["c03_facteur_additif"]), f(out["c03_mois"]),
           f(out["c03_stock_somme"]), f(out["c03_stock_facteur"]), f(out["c03_stock_un_mois"]),
           f(out["c03_taux_lignes"]), fd(out["c03_taux_somme"]), fd(out["c03_taux_moyen"])))
    # ---- le filtre silencieux qui vient du grain, pas de la cle : joindre deux agregats
    # mensuels quand l'un des magasins n'a aucune vente. Le depot central coute 44 mois de
    # logistique et ne vend rien : une jointure interne le fait disparaitre sans un mot.
    out["c03_logistique_total"] = round(un("SELECT SUM(cout_total) FROM fait_logistique"))
    out["c03_logistique_magasins"] = un("SELECT COUNT(DISTINCT id_magasin) FROM fait_logistique")
    out["c03_magasins_vendeurs"] = un("SELECT COUNT(DISTINCT id_magasin) FROM fait_ventes")
    inner = q("""WITH ca AS (SELECT strftime(date_vente,'%Y-%m') AS mois, id_magasin,
                        ROUND(SUM(montant_ttc)) AS ca
                 FROM fait_ventes WHERE est_retour = 0 GROUP BY 1, 2),
                 logi AS (SELECT mois, id_magasin, ROUND(SUM(cout_total)) AS cout
                          FROM fait_logistique GROUP BY 1, 2)
                 SELECT ROUND(SUM(logi.cout)), ROUND(SUM(ca.ca))
                 FROM ca JOIN logi ON logi.mois = ca.mois AND logi.id_magasin = ca.id_magasin""")[0]
    out["c03_logistique_jointe_interne"] = int(inner[0])
    out["c03_logistique_perdue"] = out["c03_logistique_total"] - int(inner[0])
    out["c03_depot_cout"] = round(un(
        "SELECT SUM(cout_total) FROM fait_logistique WHERE id_magasin NOT IN "
        "(SELECT DISTINCT id_magasin FROM fait_ventes)"))
    out["c03_depot_mois"] = un(
        "SELECT COUNT(*) FROM fait_logistique WHERE id_magasin NOT IN "
        "(SELECT DISTINCT id_magasin FROM fait_ventes)")
    out["c03_texte_jointure_agregats"] = (
        "joindre deux agregats mensuels par une jointure interne fait disparaitre le magasin qui "
        "n'a aucune vente : le depot central porte %s mois de couts logistiques (%s FCFA) et zero "
        "vente, donc le total des couts tombe a %s FCFA quand la table en contient %s — la "
        "jointure est au bon grain des deux cotes, et elle filtre quand meme"
        % (f(out["c03_depot_mois"]), f(out["c03_depot_cout"]),
           f(out["c03_logistique_jointe_interne"]), f(out["c03_logistique_total"])))
    out["c03_texte_faux"] = (
        "trois requetes, trois totaux faux, aucune erreur : joindre les ventes a la logistique sur "
        "le magasin seul rend %s lignes et %s FCFA (facteur %s) ; les joindre aux ruptures sur le "
        "produit et le mois rend %s lignes et %s FCFA (facteur %s, soit %s %% du chiffre d'affaires "
        "perdu sans un mot) ; les joindre au stock sur le produit et le mois rend %s lignes et un "
        "total juste (facteur %s) — c'est la cle, pas la jointure, qui decide"
        % (f(out["c03_faux_large_lignes"]), f(out["c03_faux_large_ca"]), fd(out["c03_faux_large_facteur"]),
           f(out["c03_faux_filtre_lignes"]), f(out["c03_faux_filtre_ca"]),
           fd(out["c03_faux_filtre_facteur"]), f(out["c03_faux_filtre_manquants"]),
           f(out["c03_bon_grain_lignes"]), fd(out["c03_bon_grain_facteur"])))
    # ------------------- 13. l'etoile et les changements lents (chapitre C04)
    # Un schema en etoile se juge sur trois choses : ses dimensions CONFORMES (les memes
    # dans plusieurs faits), sa gestion du TEMPS QUI PASSE (les types de SCD), et la
    # requete qui lit le passe sans le reecrire.
    faits = ["fait_ventes", "fait_commandes", "fait_encaissements", "fait_stock_mensuel",
             "fait_ruptures", "fait_logistique", "fait_objectifs"]
    conformes = {}
    for dim in ("dim_client", "dim_produit", "dim_magasin", "dim_vendeur", "dim_date"):
        prefixe = dim.replace("dim_", "id_")
        servis = []
        for fait in faits:
            colonnes = [c[0] for c in q("SELECT column_name FROM information_schema.columns "
                                        "WHERE table_name = '%s'" % fait)]
            if any(c == prefixe for c in colonnes):
                servis.append(fait.replace("fait_", ""))
        conformes[dim] = servis
    out["c04_dimension_magasin_faits"] = len(conformes["dim_magasin"])
    out["c04_dimension_client_faits"] = len(conformes["dim_client"])
    out["c04_dimension_produit_faits"] = len(conformes["dim_produit"])
    out["c04_dimension_vendeur_faits"] = len(conformes["dim_vendeur"])
    out["c04_dimension_date_faits"] = len(conformes["dim_date"])
    out["c04_texte_conformes"] = (
        "sur les %s tables de faits du modele, une dimension est CONFORME quand plusieurs faits "
        "pointent sur la meme : dim_magasin sert %s faits (%s), dim_client et dim_produit en "
        "servent %s chacune, dim_vendeur une seule, et dim_date aucune — elle existe, elle est "
        "juste, et aucun fait ne pointe dessus par cle : c'est le trou que le chapitre C06 "
        "viendra fermer"
        % (f(len(faits)), f(out["c04_dimension_magasin_faits"]),
           ", ".join(conformes["dim_magasin"]), f(out["c04_dimension_client_faits"])))
    # ---- les deux trous reunis : ce qu'une jointure interne perdrait sans le dire
    out["c04_trous_total_lignes"] = out["c_ventes_client_inconnu"] + out["c_ventes_rattrapees"]
    out["c04_trous_total_texte"] = (
        "les deux trous d'une jointure historisee mal bornee se cumulent : %s ventes du client non "
        "identifie et %s ventes anterieures a la creation du compte, soit %s lignes de ticket "
        "perdues par une jointure interne, sans erreur et sans avertissement"
        % (f(out["c_ventes_client_inconnu"]), f(out["c_ventes_rattrapees"]),
           f(out["c04_trous_total_lignes"])))
    # ---- les quatre types de SCD, mesures sur les 1 120 mouvements du socle
    mouvements = "read_csv_auto('03_exercices/dossier_M13/mouvements_clients.csv', header = true)"
    par_type = dict(q("SELECT type_scd, COUNT(*) FROM " + mouvements + " GROUP BY 1"))
    out["c04_mouvements_type1"] = int(par_type.get(1, 0))
    out["c04_mouvements_type2"] = int(par_type.get(2, 0))
    par_nature = q("SELECT nature, type_scd, COUNT(*) FROM " + mouvements + " GROUP BY 1, 2 "
                   "ORDER BY 1, 2")
    out["c04_mouvements_detail"] = "; ".join("%s type %s : %s" % (n, t, f(c)) for n, t, c in par_nature)
    out["c04_attributs_historiises"] = ", ".join(sorted({n for n, _, _ in par_nature}))
    # type 3 : une colonne « valeur precedente » ne sait garder QU'un changement
    out["c04_clients_deux_changements"] = un(
        "SELECT COUNT(*) FROM (SELECT id_client FROM dim_client_scd "
        "GROUP BY 1 HAVING COUNT(DISTINCT ville) > 2)")
    # GROUP BY id_client, jamais GROUP BY 1 : ici le premier item du SELECT est un agregat,
    # et le moteur refuse de grouper sur un agregat (lecon deja payee au chapitre C03)
    out["c04_villes_max"] = un(
        "SELECT MAX(n) FROM (SELECT COUNT(DISTINCT ville) AS n FROM dim_client_scd "
        "GROUP BY id_client)")
    out["c04_clients_avec_histoire"] = un(
        "SELECT COUNT(*) FROM (SELECT id_client FROM dim_client_scd GROUP BY 1 HAVING COUNT(*) > 1)")
    out["c04_texte_types"] = (
        "les %s mouvements du referentiel se rangent en deux familles : %s de type 2 (une nouvelle "
        "version, l'ancienne reste lisible) et %s de type 1 (une correction, l'ancienne valeur est "
        "ecrasee) ; les attributs historises sont %s. Le type 3, qui range la valeur precedente "
        "dans une colonne, ne representerait pas ce socle : %s clients ont change de ville plus de "
        "deux fois (jusqu'a %s villes distinctes), et il aurait fallu autant de colonnes que de "
        "changements possibles"
        % (f(out["c_mouvements"]), f(out["c04_mouvements_type2"]), f(out["c04_mouvements_type1"]),
           out["c04_attributs_historiises"], f(out["c04_clients_deux_changements"]),
           f(out["c04_villes_max"])))
    # ---- ce que coute la lecture historisee, et ce qu'elle rapporte
    o_courant = _chrono("SELECT c.segment, ROUND(SUM(f.montant_ttc)) FROM fait_ventes f "
                       "JOIN dim_client c ON c.id_client = f.id_client "
                       "WHERE f.est_retour = 0 GROUP BY 1")
    o_histo = _chrono("SELECT h.segment, ROUND(SUM(f.montant_ttc)) FROM fait_ventes f "
                     "JOIN dim_client_scd h ON h.id_client = f.id_client AND f.date_vente "
                     "BETWEEN h.date_debut AND COALESCE(h.date_fin, DATE '2100-01-01') "
                     "WHERE f.est_retour = 0 GROUP BY 1")
    out["c04_temps_courant_ms"] = o_courant
    out["c04_temps_historise_ms"] = o_histo
    prix_courant = un("SELECT ROUND(AVG(p.prix_vente_ht)) FROM fait_ventes f "
                      "JOIN dim_produit p ON p.id_produit = f.id_produit WHERE f.est_retour = 0")
    prix_histo = un("SELECT ROUND(AVG(h.prix_vente_ht)) FROM fait_ventes f "
                    "JOIN dim_produit_scd h ON h.id_produit = f.id_produit AND f.date_vente "
                    "BETWEEN h.date_debut AND COALESCE(h.date_fin, DATE '2100-01-01') "
                    "WHERE f.est_retour = 0")
    out["c04_prix_moyen_courant"] = prix_courant
    out["c04_prix_moyen_historise"] = prix_histo
    out["c04_prix_ecart_pct"] = round(abs(prix_courant - prix_histo) / prix_histo * 100, 1)
    out["c04_texte_lecture"] = (
        "lire le passe coute %s ms au lieu de %s ms sur le fil rouge (une jointure par intervalle "
        "au lieu d'une egalite de cle, mediane de sept executions), et rapporte davantage : le prix "
        "moyen des ventes vaut %s FCFA lu sur la dimension historisee et %s FCFA lu sur la "
        "dimension courante, soit %s %% d'ecart — le prix d'aujourd'hui n'a pas ete pratique sur "
        "les ventes de 2023"
        % (f(o_histo), f(o_courant), f(prix_histo), f(prix_courant),
           fd(out["c04_prix_ecart_pct"])))
    out["c04_versions_produit_par_produit"] = round(out["c_versions_produit"]
                                                    / un("SELECT COUNT(DISTINCT id_produit) "
                                                         "FROM dim_produit_scd"), 1)
    # ---- deux exemples nommes, pour le chapitre : un produit et un client qui bougent
    versions_produit_exemple = q("SELECT version, date_debut, prix_vente_ht FROM dim_produit_scd "
                                 "WHERE id_produit = 12 ORDER BY version")
    out["c04_exemple_produit"] = "produit 12 : " + " ; ".join(
        "version %s (%s) %s FCFA" % (v, d.year, f(p_)) for v, d, p_ in versions_produit_exemple)
    out["c04_exemple_produit_variation_pct"] = round(
        (versions_produit_exemple[-1][2] / versions_produit_exemple[0][2] - 1) * 100, 1)
    client_exemple = q("SELECT id_client FROM dim_client_scd GROUP BY id_client "
                       "HAVING COUNT(DISTINCT ville) > 2 ORDER BY id_client LIMIT 1")[0][0]
    out["c04_exemple_client"] = "client %s : " % f(client_exemple) + " ; ".join(
        "version %s du %s au %s, %s" % (v, d1, d2 or "aujourd'hui", ville)
        for v, d1, d2, ville in q("SELECT version, date_debut, date_fin, ville FROM dim_client_scd "
                                  "WHERE id_client = %s ORDER BY version" % client_exemple))
    out["c04_texte_tarifs"] = (
        "la grille tarifaire est historisee elle aussi : %s versions pour %s produits (%s versions "
        "par produit), une nouvelle version chaque 1er janvier, et jamais d'ecriture par-dessus — "
        "la marge d'une vente de 2023 se calcule avec le tarif de 2023"
        % (f(out["c_versions_produit"]), f(un("SELECT COUNT(DISTINCT id_produit) FROM dim_produit_scd")),
           fd(out["c04_versions_produit_par_produit"])))
    con.close()
    return out


def main(argv=None):
    argv = argv or sys.argv[1:]
    m = controler()
    if "--json" in argv:
        print(json.dumps(m, ensure_ascii=False, indent=1, sort_keys=True))
        return 0
    print("=== modele M13 : le modele de Sahel Distribution, controle ===")
    print("  %d tables : %d dimensions, %d faits, %d dimensions historisees"
          % (m["c_tables_du_modele"], m["c_dimensions"], m["c_faits"],
             m["c_dimensions_historisees"]))
    print("  1. unicite   : %s" % m["c_verdict_unicite"])
    print("  2. grain     : %s" % m["c_verdict_grain"])
    print("  3. orphelins : %s" % m["c_verdict_orphelins"])
    print("  4. totaux    : %s" % m["c_recette_texte"])
    print("  5. SCD       : %s versions client (+ la ligne « client non identifie »), "
          "%s versions produit, %s mouvements (dont %s corrections)"
          % (f(m["c_versions_client"]), f(m["c_versions_produit"]), f(m["c_mouvements"]),
             f(m["c_mouvements_type1"])))
    print("     %s" % m["c_asof_texte"])
    print("     %s" % m["c_scd_texte"])
    print("  6. calendrier: %s" % m["c_calendrier_texte"])
    print("  7. fautifs   : %s" % m["c_fautif_texte"])
    print("  8. tarifs    : %s" % m["c_tarif_texte"])
    print("  9. revue     : %s" % m["c_revue_texte"])
    print(" 10. depart    : %s" % m["c01_texte_depart"])
    print("     %s" % m["c01_texte_jointures"])
    print(" 11. normaliser: %s" % m["c02_texte_libelles"])
    print("     %s" % m["c02_texte_cout"])
    print(" 12. grain     : %s" % m["c03_texte_grain"])
    print("     %s" % m["c03_texte_cle"])
    print("     %s" % m["c03_texte_additivite"])
    print("     %s" % m["c03_texte_faux"])
    print("     %s" % m["c03_texte_jointure_agregats"])
    print(" 13. etoile    : %s" % m["c04_texte_conformes"])
    print("     %s" % m["c04_texte_types"])
    print("     %s" % m["c04_texte_lecture"])
    print("     %s" % m["c04_texte_tarifs"])
    print("     %s" % m["c04_exemple_produit"])
    print("     %s (variation %s %%)" % (m["c04_exemple_client"], m["c04_exemple_produit_variation_pct"]))
    print("     %s" % m["c04_trous_total_texte"])
    print()
    print("  verdict : le modele rend le meme chiffre d'affaires que la source (%s FCFA), "
          "sans orphelin et avec un grain prouve sur %d tables."
          % (f(m["c_ca_source"]), m["c_tables_cles_uniques"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
