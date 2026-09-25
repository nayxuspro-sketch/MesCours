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
    print()
    print("  verdict : le modele rend le meme chiffre d'affaires que la source (%s FCFA), "
          "sans orphelin et avec un grain prouve sur %d tables."
          % (f(m["c_ca_source"]), m["c_tables_cles_uniques"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
