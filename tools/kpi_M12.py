#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kpi_M12.py — les 10 indicateurs du module M12, mesurés sur le socle.

Un module qui apprend à écrire des définitions d'indicateurs doit les tenir
lui-même : chaque KPI de la carte de définition entregée au projet est calculé
ici, en SQL, sur le socle de M12 — jamais estimé à la main.

    python3 tools/kpi_M12.py            les 10 KPI, valeurs et définitions
    python3 tools/kpi_M12.py --json     la même chose, en JSON (pour chiffres_manuel)

Les **définitions** sont imprimées avec les valeurs : c'est le point du module.
Un chiffre sans définition n'est pas un indicateur, c'est une opinion.
"""
from __future__ import annotations

import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "03_exercices", "dossier_M12"))


def fmt(n):
    if n is None:
        return "—"
    if isinstance(n, float):
        entier = abs(n - round(n)) < 0.005
        if entier:
            n = round(n)
    if isinstance(n, int) or float(n).is_integer():
        return "{:,}".format(int(n)).replace(",", " ")
    return ("{:.2f}".format(n)).replace(".", ",")


def mesurer():
    from connexion import ouvrir
    con = ouvrir()
    q = lambda s: con.execute(s).fetchall()
    un = lambda s: con.execute(s).fetchone()[0]
    out = {}

    # ---------------------------------------------------------------- 1. CA net
    ca_net = un("SELECT ROUND(SUM(montant_ttc)) FROM ventes WHERE est_retour = 0")
    ca_brut = un("SELECT ROUND(SUM(montant_ttc)) FROM ventes")
    tickets = un("SELECT COUNT(DISTINCT id_ticket) FROM ventes WHERE est_retour = 0")
    lignes = un("SELECT COUNT(*) FROM ventes WHERE est_retour = 0")
    out["k01_ca_net_fcfa"] = ca_net
    out["k01_ca_avec_retours_fcfa"] = ca_brut
    out["k01_ecart_definitions_fcfa"] = ca_net - ca_brut
    out["k01_ecart_definitions_pct"] = round(100.0 * (ca_net - ca_brut) / ca_net, 2)

    # ------------------------------------------------------------ 2. marge brute
    mb = un("""SELECT ROUND(SUM(marge_fcfa)) FROM vente_marge WHERE est_retour = 0""")
    ht = un("""SELECT ROUND(SUM(montant_ht)) FROM vente_marge WHERE est_retour = 0""")
    out["k02_marge_brute_fcfa"] = mb
    out["k02_taux_marge_pct"] = round(100.0 * mb / ht, 2)
    # effet des deux prix manquants du référentiel (coût reconstitué au prix médian)
    mb_sans = un("""SELECT ROUND(SUM(marge_fcfa)) FROM vente_marge
                    WHERE est_retour = 0 AND id_produit NOT IN (62, 149)""")
    ht_sans = un("""SELECT ROUND(SUM(montant_ht)) FROM vente_marge
                    WHERE est_retour = 0 AND id_produit NOT IN (62, 149)""")
    out["k02_taux_marge_hors_deux_produits_pct"] = round(100.0 * mb_sans / ht_sans, 2)
    out["k02_effet_prix_manquants_pts"] = round(
        100.0 * mb / ht - 100.0 * mb_sans / ht_sans, 2)
    # Le taux realise (29 %) depasse la cible du referentiel (18 a 24 %) : les prix de
    # vente du socle montent avec les annees, alors que le referentiel porte un prix
    # unique. Un ecart d'indicateur a toujours une cause, et elle se mesure.
    derive = q("""SELECT year(v.date_vente), ROUND(AVG(v.prix_unitaire_ht)),
                         ROUND(AVG(p.prix_vente_ht)), COUNT(*)
                  FROM ventes v JOIN produit p ON p.id_produit = v.id_produit
                  WHERE v.est_retour = 0 GROUP BY 1 ORDER BY 1""")
    out["k02_prix_unitaire_par_an"] = [
        {"annee": int(a), "prix_vente_moyen": float(b), "prix_referentiel": float(c),
         "lignes": int(d)} for a, b, c, d in derive]
    out["k02_derive_prix_pct"] = round(
        100.0 * (out["k02_prix_unitaire_par_an"][-1]["prix_vente_moyen"]
                 / out["k02_prix_unitaire_par_an"][0]["prix_vente_moyen"] - 1), 1)
    out["k02_marge_definition"] = (
        "marge brute = ventes HT moins cout standard x quantite. Le taux mesure (%s %%) "
        "depasse la cible du referentiel (18 a 24 %%) parce que les prix de vente du socle "
        "montent de %s %% entre 2023 et 2026 alors que le referentiel porte un prix "
        "unique : publier le taux sans cette phrase fait croire a une performance"
        % (fmt(out["k02_taux_marge_pct"]), fmt(out["k02_derive_prix_pct"])))

    # ------------------------------------------------------------ 3. taux de rupture
    servis = un("""SELECT COUNT(*) FROM (SELECT DISTINCT id_produit, id_magasin,
                          strftime(date_vente, '%Y-%m') FROM ventes WHERE est_retour = 0)""")
    en_rupture = un("SELECT COUNT(*) FROM rupture")
    out["k03_couples_servis"] = servis
    out["k03_couples_en_rupture"] = en_rupture
    out["k03_taux_rupture_pct"] = round(100.0 * en_rupture / servis, 2)
    out["k03_jours_rupture"] = un("SELECT SUM(jours_rupture) FROM rupture")
    out["k03_ca_perdu_estime_fcfa"] = un("SELECT ROUND(SUM(ca_perdu_estime_fcfa)) FROM rupture")
    out["k03_rupture_definition"] = (
        "part des couples produit-magasin-mois servis qui ont connu au moins un jour "
        "de rupture : le dénominateur est ce que nous avons VENDU, pas ce que nous "
        "aurions pu vendre — un taux de rupture calculé sur le catalogue entier "
        "mesure l'assortiment, pas la disponibilité")

    # ------------------------------------------------------ 4. rotation de stock
    out["k04_entrees_unites"] = round(un("SELECT SUM(entrees_unites) FROM stock_mensuel"))
    ventes_12 = un("""SELECT SUM(v.quantite) FROM ventes v
                      WHERE v.est_retour = 0
                        AND v.date_vente >= DATE '2025-09-01'
                        AND v.date_vente < DATE '2026-09-01'""")
    # Le stock qui compte est la MOYENNE MENSUELLE du stock total, jamais la SOMME des
    # stocks mensuels : sommer douze mois de stock multiplie le denominateur par douze
    # et divise la rotation par douze (mesure du 24/09/2026 : 0,78 contre 9,4 tours).
    stock_moyen = un("""
        SELECT AVG(stock_du_mois) FROM (
          SELECT mois, SUM(stock_moyen_unites) AS stock_du_mois FROM stock_mensuel
          WHERE mois >= '2025-09' AND mois < '2026-09' GROUP BY 1)""")
    out["k04_ventes_12_mois_unites"] = round(ventes_12)
    out["k04_stock_moyen_mensuel_unites"] = round(stock_moyen)
    out["k04_rotation_annuelle"] = round(ventes_12 / stock_moyen, 2)
    out["k04_couverture_mois"] = round(stock_moyen / ventes_12 * 12, 2)
    out["k04_erreur_somme_stocks"] = round(ventes_12 / (
        un("""SELECT SUM(stock_moyen_unites) FROM stock_mensuel
              WHERE mois >= '2025-09' AND mois < '2026-09'""")), 2)
    out["k04_rotation_definition"] = (
        "quantités vendues sur 12 mois glissants divisées par le stock moyen de la "
        "même période : rotation et couverture sont l'inverse l'une de l'autre, et "
        "publier l'une sans l'autre laisse croire qu'un stock « tourne » alors qu'il "
        "dort (9 mois de couverture = 1,3 tour par an)")

    # ---------------------------------------------------------- 5. panier moyen
    out["k05_panier_moyen_ticket_fcfa"] = round(un(
        "SELECT SUM(montant_ttc) / COUNT(DISTINCT id_ticket) FROM ventes WHERE est_retour = 0"))
    out["k05_panier_median_fcfa"] = un("""
        SELECT ROUND(MEDIAN(panier)) FROM (
          SELECT id_ticket, SUM(montant_ttc) AS panier FROM ventes
          WHERE est_retour = 0 GROUP BY 1)""")
    out["k05_ligne_moyenne_fcfa"] = round(ca_net / lignes)
    out["k05_ecart_ticket_ligne_pct"] = round(
        100.0 * (out["k05_panier_moyen_ticket_fcfa"] - ca_net / lignes)
        / (out["k05_panier_moyen_ticket_fcfa"]), 1)

    # ----------------------------------------------------------- 6. taux de retour
    out["k06_lignes_retour"] = un("SELECT COUNT(*) FROM ventes WHERE est_retour = 1")
    out["k06_lignes_total"] = un("SELECT COUNT(*) FROM ventes")
    out["k06_taux_retour_lignes_pct"] = round(
        100.0 * out["k06_lignes_retour"] / out["k06_lignes_total"], 2)
    out["k06_tickets_avec_retour"] = un("""
        SELECT COUNT(*) FROM (SELECT id_ticket FROM ventes GROUP BY 1
                              HAVING MAX(CASE WHEN est_retour = 1 THEN 1 ELSE 0 END) = 1)""")
    out["k06_tickets_mixtes"] = un("""
        SELECT COUNT(*) FROM (SELECT id_ticket FROM ventes GROUP BY 1
                              HAVING MIN(CASE WHEN est_retour = 1 THEN 1 ELSE 0 END) = 0
                                 AND MAX(CASE WHEN est_retour = 1 THEN 1 ELSE 0 END) = 1)""")
    out["k06_tickets_retour_seul"] = un("""
        SELECT COUNT(*) FROM (SELECT id_ticket FROM ventes GROUP BY 1
                              HAVING MIN(CASE WHEN est_retour = 1 THEN 1 ELSE 0 END) = 1)""")
    out["k06_tickets_total"] = un("SELECT COUNT(DISTINCT id_ticket) FROM ventes")
    out["k06_taux_retour_tickets_pct"] = round(
        100.0 * out["k06_tickets_avec_retour"] / out["k06_tickets_total"], 2)
    out["k06_retour_definition"] = (
        "deux taux de retour coexistent : %s %% des lignes et %s %% des tickets — le "
        "premier mesure la logistique, le second le mécontentement client ; et parmi les "
        "%s tickets concernés, %s sont mixtes (une vente ET un retour sur le même ticket) "
        "alors que %s ne portent que des retours"
        % (fmt(out["k06_taux_retour_lignes_pct"]), fmt(out["k06_taux_retour_tickets_pct"]),
           fmt(out["k06_tickets_avec_retour"]), fmt(out["k06_tickets_mixtes"]),
           fmt(out["k06_tickets_retour_seul"])))

    # --------------------------------------------------------- 7. taux de service
    out["k07_commandes"] = un("SELECT COUNT(*) FROM commande")
    out["k07_livrees"] = un("SELECT COUNT(*) FROM commande WHERE statut = 'livree'")
    out["k07_annulees"] = un("SELECT COUNT(*) FROM commande WHERE statut = 'annulee'")
    out["k07_a_lheure"] = un("""SELECT COUNT(*) FROM commande
                                WHERE statut = 'livree' AND date_livraison <= date_promisee""")
    out["k07_taux_service_pct"] = round(
        100.0 * out["k07_a_lheure"] / out["k07_livrees"], 1)
    out["k07_taux_service_annulees_incluses_pct"] = round(
        100.0 * out["k07_a_lheure"] / out["k07_commandes"], 1)
    out["k07_retard_median_jours"] = un("""
        SELECT MEDIAN(date_diff('day', date_promisee, date_livraison)) FROM commande
        WHERE statut = 'livree' AND date_livraison > date_promisee""")
    out["k07_service_definition"] = (
        "part des commandes livrées au plus tard à la date promise : les commandes "
        "annulées sortent du dénominateur dans la première version et y entrent dans "
        "la seconde — 78,2 % ou 77,9 %, deux chiffres défendables, un seul à choisir")

    # ---------------------------------------------------- 8. taux de recouvrement
    out["k08_factures"] = un("SELECT COUNT(*) FROM encaissement")
    out["k08_a_echeance"] = un("""SELECT COUNT(*) FROM encaissement
                                  WHERE date_encaissement IS NOT NULL
                                    AND date_encaissement <= date_echeance""")
    out["k08_encaissees"] = un("SELECT COUNT(*) FROM encaissement WHERE date_encaissement IS NOT NULL")
    out["k08_ouvertes"] = un("SELECT COUNT(*) FROM encaissement WHERE date_encaissement IS NULL")
    out["k08_taux_recouvrement_pct"] = round(
        100.0 * out["k08_a_echeance"] / out["k08_factures"], 1)
    out["k08_montant_facture_fcfa"] = round(un("SELECT SUM(montant_ttc) FROM encaissement"))
    out["k08_montant_encaisse_fcfa"] = round(un("SELECT SUM(montant_encaisse) FROM encaissement"))
    out["k08_encours_ouvert_fcfa"] = round(un(
        "SELECT SUM(montant_ttc) FROM encaissement WHERE date_encaissement IS NULL"))
    out["k08_dso_jours"] = round(un("""
        SELECT AVG(date_diff('day', date_facture, date_encaissement)) FROM encaissement
        WHERE date_encaissement IS NOT NULL"""), 1)

    # ------------------------------------------------ 9. coût logistique unitaire
    out["k09_colis"] = round(un("SELECT SUM(colis) FROM logistique"))
    out["k09_cout_total_fcfa"] = round(un("SELECT SUM(cout_total_fcfa) FROM logistique"))
    out["k09_cout_unitaire_fcfa"] = round(
        out["k09_cout_total_fcfa"] / out["k09_colis"])
    out["k09_cout_au_kg_fcfa"] = round(
        out["k09_cout_total_fcfa"] / un("SELECT SUM(poids_kg) FROM logistique"))
    out["k09_part_carburant_pct"] = round(100.0 * un(
        "SELECT SUM(cout_carburant_fcfa) FROM logistique") / out["k09_cout_total_fcfa"], 1)
    # Le depot central n'a aucune vente : ses colis sont dans le total sans activite en face.
    out["k09_colis_magasins"] = round(un(
        "SELECT SUM(colis) FROM logistique WHERE id_magasin IN "
        "(SELECT DISTINCT id_magasin FROM ventes)"))
    out["k09_cout_unitaire_magasins_fcfa"] = round(un(
        "SELECT SUM(cout_total_fcfa) FROM logistique WHERE id_magasin IN "
        "(SELECT DISTINCT id_magasin FROM ventes)") / out["k09_colis_magasins"])

    # --------------------------------------------- 10. part de marché interne
    villes = q("""SELECT m.ville, m.nom, ROUND(SUM(v.montant_ttc)) AS ca
                  FROM ventes v JOIN magasin m ON m.id_magasin = v.id_magasin
                  WHERE v.est_retour = 0 GROUP BY 1, 2 ORDER BY 3 DESC""")
    total = sum(x[2] for x in villes)
    par_ville = {}
    for ville, nom, ca in villes:
        par_ville.setdefault(ville, []).append((nom, ca))
    parts = []
    for ville, liste in sorted(par_ville.items()):
        tot = sum(c for _, c in liste)
        for nom, ca in sorted(liste, key=lambda x: -x[1]):
            parts.append((nom, ville, ca, round(100.0 * ca / tot, 1), round(100.0 * ca / total, 1)))
    out["k10_parts_ville"] = [
        {"magasin": nom, "ville": ville, "ca_fcfa": ca, "part_ville_pct": pv,
         "part_reseau_pct": pr}
        for nom, ville, ca, pv, pr in parts]
    out["k10_definition"] = (
        "part de marché INTERNE : la part du chiffre d'affaires d'un magasin dans "
        "celui de sa ville. Ce n'est pas une part de marché : elle mesure notre "
        "réseau contre lui-même, et le seul chiffre honnête qu'on puisse en tirer est "
        "la part de chaque point de vente dans le total de l'enseigne")
    out["k10_depot_sans_vente"] = un(
        "SELECT COUNT(*) FROM magasin WHERE id_magasin NOT IN (SELECT DISTINCT id_magasin FROM ventes)")
    out["k10_colis_depot"] = round(un(
        "SELECT SUM(colis) FROM logistique WHERE id_magasin NOT IN (SELECT DISTINCT id_magasin FROM ventes)"))
    con.close()
    return out


def mesurer_grain():
    """Le vocabulaire exact (C03) : grain, dimensions, additivite — mesures, pas definitions.

    Quatre familles de mesures, toutes verifiees sur huit tables :

      1. **le grain** de chaque table : une cle distincte par ligne, ou des doublons ;
      2. **les dimensions** et leur cardinalite (combien de valeurs distinctes) ;
      3. **l'additivite** : ce qui se somme (montants, effectifs de lignes) et ce qui ne se
         somme pas (clientes distincts, taux, moyennes, clôtures de stock) ;
      4. **les pieges de cle** : la jointure qui multiplie les lignes quand une cle manque.
    """
    from connexion import ouvrir
    con = ouvrir()
    q = lambda s: con.execute(s).fetchall()
    un = lambda s: con.execute(s).fetchone()[0]
    out = {}

    # ------------------------------------------------------------- 1. le grain
    cles = {"ventes": "id_vente", "commande": "id_commande", "encaissement": "id_facture",
            "stock_mensuel": "id_produit || '-' || mois",
            "rupture": "id_produit || '-' || id_magasin || '-' || mois",
            "logistique": "id_magasin || '-' || mois", "produit": "id_produit",
            "magasin": "id_magasin"}
    grains = {}
    for t, k in cles.items():
        n = un("SELECT COUNT(*) FROM " + t)
        d = un("SELECT COUNT(*) FROM (SELECT DISTINCT %s FROM %s)" % (k, t))
        grains[t] = {"lignes": n, "cles": d, "unique": n == d}
    out["g_grains"] = grains
    out["g_tables"] = len(grains)
    out["g_tables_cles_uniques"] = sum(1 for v in grains.values() if v["unique"])

    # -------------------------------------------------------- 2. les dimensions
    dims = {
        "magasin": un("SELECT COUNT(DISTINCT id_magasin) FROM ventes"),
        "ville": un("SELECT COUNT(DISTINCT m.ville) FROM ventes v "
                    "JOIN magasin m ON m.id_magasin = v.id_magasin"),
        "quartier": un("SELECT COUNT(DISTINCT m.quartier) FROM ventes v "
                       "JOIN magasin m ON m.id_magasin = v.id_magasin"),
        "vendeur": un("SELECT COUNT(DISTINCT id_vendeur) FROM ventes"),
        "mode_paiement": un("SELECT COUNT(DISTINCT mode_paiement) FROM ventes"),
        "canal": un("SELECT COUNT(DISTINCT canal) FROM ventes"),
        "produit": un("SELECT COUNT(*) FROM produit"),
        "categorie_brute": un("SELECT COUNT(DISTINCT categorie) FROM produit"),
        "sous_categorie": un("SELECT COUNT(DISTINCT sous_categorie) FROM produit"),
        "client": un("SELECT COUNT(DISTINCT id_client) FROM ventes WHERE est_retour = 0"),
        "mois": un("SELECT COUNT(DISTINCT mois) FROM stock_mensuel"),
        "jour": un("SELECT COUNT(*) FROM calendrier"),
    }
    out["g_dimensions"] = dims
    out["g_couples_canal_mode"] = un(
        "SELECT COUNT(*) FROM (SELECT DISTINCT canal, mode_paiement FROM ventes)")

    # -------------------------------------------------------- 3. l'additivite
    total = un("SELECT SUM(montant_ttc) FROM ventes WHERE est_retour = 0")
    somme_mag = un("""SELECT SUM(ca) FROM (SELECT SUM(montant_ttc) AS ca FROM ventes
                      WHERE est_retour = 0 GROUP BY id_magasin)""")
    out["g_ca_total"] = round(total)
    out["g_ca_somme_magasins"] = round(somme_mag)
    out["g_ca_additif"] = abs(total - somme_mag) < 1

    clients_par_produit = un("""SELECT SUM(n) FROM (SELECT COUNT(DISTINCT id_client) AS n
                              FROM ventes WHERE est_retour = 0 GROUP BY id_produit)""")
    clients_par_magasin = un("""SELECT SUM(n) FROM (SELECT COUNT(DISTINCT id_client) AS n
                               FROM ventes WHERE est_retour = 0 GROUP BY id_magasin)""")
    clients_total = un("SELECT COUNT(DISTINCT id_client) FROM ventes WHERE est_retour = 0")
    out["g_clients_somme_par_produit"] = clients_par_produit
    out["g_clients_somme_par_magasin"] = clients_par_magasin
    out["g_clients_total"] = clients_total
    out["g_clients_ratio_produit"] = round(1.0 * clients_par_produit / clients_total, 2)
    out["g_clients_ratio_magasin"] = round(1.0 * clients_par_magasin / clients_total, 2)
    out["g_clients_non_additif"] = (
        "le nombre de clients distincts ne s'additionne pas : %s clients par produit s'ajoutent en "
        "%s, et par magasin en %s, pour %s clients reels — un client qui achete dans deux magasins se "
        "compte deux fois, et c'est ce que fait tout tableau croise qui somme des comptages distincts"
        % (fmt(clients_total), fmt(clients_par_produit), fmt(clients_par_magasin),
           fmt(clients_total)))

    paniers = q("""SELECT m.nom, AVG(panier) FROM (SELECT id_magasin, id_ticket,
                    SUM(montant_ttc) AS panier FROM ventes WHERE est_retour = 0 GROUP BY 1, 2) t
                   JOIN magasin m ON m.id_magasin = t.id_magasin GROUP BY 1 ORDER BY 2 DESC""")
    vraie = un("""SELECT AVG(panier) FROM (SELECT id_ticket, SUM(montant_ttc) AS panier
                  FROM ventes WHERE est_retour = 0 GROUP BY 1)""")
    moyenne_des_moyennes = sum(v for _, v in paniers) / len(paniers)
    out["g_paniers_par_magasin"] = [{"magasin": n, "panier_moyen_fcfa": round(v)}
                                    for n, v in paniers]
    out["g_panier_moyenne_des_moyennes"] = round(moyenne_des_moyennes)
    out["g_panier_vraie_moyenne"] = round(vraie)
    out["g_panier_ecart_fcfa"] = round(moyenne_des_moyennes - vraie)
    out["g_panier_ecart_pct"] = round(100 * (moyenne_des_moyennes / vraie - 1), 1)

    fin = un("SELECT ROUND(SUM(stock_moyen_unites)) FROM stock_mensuel WHERE mois = '2026-08'")
    tout = un("SELECT ROUND(SUM(stock_moyen_unites)) FROM stock_mensuel")
    out["g_stock_cloture"] = fin
    out["g_stock_somme_tous_mois"] = tout
    out["g_stock_ratio"] = round(1.0 * tout / fin, 1)

    # -------------------------------------------------- 4. les pieges de cle
    n1 = un("SELECT COUNT(*) FROM ventes v JOIN produit p ON p.id_produit = v.id_produit")
    n2 = un("""SELECT COUNT(*) FROM ventes v JOIN rupture r ON r.id_produit = v.id_produit""")
    ca2 = un("""SELECT ROUND(SUM(v.montant_ttc)) FROM ventes v
                JOIN rupture r ON r.id_produit = v.id_produit WHERE v.est_retour = 0""")
    out["g_jointure_produit_lignes"] = n1
    out["g_jointure_sans_mois_lignes"] = n2
    out["g_jointure_sans_mois_facteur"] = round(1.0 * n2 / 240000, 1)
    out["g_jointure_sans_mois_ca"] = ca2
    out["g_jointure_sans_mois_ca_facteur"] = round(1.0 * ca2 / total, 1)
    out["g_cle_piege"] = (
        "une jointure sur le produit seul, sans le mois, multiplie les lignes par %s (%s au lieu de "
        "240 000) et le chiffre d'affaires par %s (%s FCFA au lieu de %s) : la cle oubliee ne "
        "provoque aucune erreur, elle fabrique un total"
        % (fmt(out["g_jointure_sans_mois_facteur"]), fmt(n2),
           fmt(out["g_jointure_sans_mois_ca_facteur"]), fmt(int(ca2)), fmt(round(total))))

    # ---------------------------------- 5. les trois horizons de decision
    record = q("""SELECT date_vente, ROUND(SUM(montant_ttc)) FROM ventes WHERE est_retour = 0
                  GROUP BY 1 ORDER BY 2 DESC LIMIT 1""")[0]
    out["g_jour_record"] = str(record[0])
    out["g_jour_record_ca"] = record[1]
    out["g_jour_moyen_ca"] = un("""SELECT ROUND(SUM(montant_ttc) /
                                  COUNT(DISTINCT date_vente)) FROM ventes WHERE est_retour = 0""")
    out["g_jour_record_ratio"] = round(1.0 * record[1] / out["g_jour_moyen_ca"], 2)
    out["g_mois_record"] = q("""SELECT strftime(date_vente, '%Y-%m'), ROUND(SUM(montant_ttc))
                                FROM ventes WHERE est_retour = 0 GROUP BY 1 ORDER BY 2 DESC
                                LIMIT 1""")[0][0]
    annees = q("""SELECT year(date_vente), ROUND(SUM(montant_ttc)) FROM ventes
                  WHERE est_retour = 0 GROUP BY 1 ORDER BY 1""")
    out["g_annees"] = [{"annee": int(a), "ca": c} for a, c in annees]
    con.close()
    return out


def mesurer_regimes():
    """Les quatre régimes de question (C02), mesurés sur le socle.

    1. descriptif  (« quoi »)          : ce qui s'est passé, et en combien de tranches on peut le lire
    2. diagnostique (« pourquoi »)     : l'écart d'un indicateur et sa cause, mesurée
    3. prédictif   (« quoi demain »)   : trois projections simples, et leur erreur **constatée**
    4. prescriptif (« que faire »)     : la file d'action, triée, chiffrée, avec son seuil

    Le module tient à montrer le troisième régime **sans modèle** : une projection naïve
    déclarée est un acte de BI ; une projection non déclarée est une croyance.
    """
    from connexion import ouvrir
    con = ouvrir()
    q = lambda s: con.execute(s).fetchall()
    un = lambda s: con.execute(s).fetchone()[0]
    out = {}

    # ---------------------------------------------------- 1. descriptif
    serie = q("""SELECT strftime(date_vente, '%Y-%m') AS m, ROUND(SUM(montant_ttc))
                 FROM ventes WHERE est_retour = 0 GROUP BY 1 ORDER BY 1""")
    out["r1_mois"] = len(serie)
    out["r1_premier_mois"] = serie[0][0]
    out["r1_premier_ca"] = serie[0][1]
    out["r1_dernier_mois"] = serie[-1][0]
    out["r1_dernier_ca"] = serie[-1][1]
    out["r1_magasin_mois"] = un("""SELECT COUNT(DISTINCT id_magasin || '-' ||
                                   strftime(date_vente, '%Y-%m')) FROM ventes""")
    out["r1_cellules"] = un("""SELECT COUNT(*) FROM (SELECT DISTINCT v.id_magasin,
                               strftime(v.date_vente, '%Y-%m'), p.categorie
                               FROM ventes v JOIN produit p ON p.id_produit = v.id_produit
                               WHERE v.est_retour = 0)""")
    out["r1_produits_servis"] = un("SELECT COUNT(DISTINCT id_produit) FROM ventes WHERE est_retour = 0")
    jours = dict(q("""SELECT strftime(date_vente, '%w') AS j, ROUND(SUM(montant_ttc))
                      FROM ventes WHERE est_retour = 0 GROUP BY 1"""))
    out["r1_ca_lundi"] = jours["1"]
    out["r1_ca_dimanche"] = jours["0"]
    out["r1_ratio_lundi_dimanche"] = round(jours["1"] / jours["0"], 2)
    out["r1_part_fin_de_mois_pct"] = round(un("""
        SELECT SUM(CASE WHEN CAST(strftime(date_vente, '%d') AS INT) > 25
                        THEN montant_ttc ELSE 0 END) / SUM(montant_ttc) * 100
        FROM ventes WHERE est_retour = 0"""), 1)

    # ---------------------------------------------------- 2. diagnostique
    out["r2_marge_pct"] = un("""SELECT ROUND(SUM(marge_fcfa) / SUM(montant_ht) * 100, 2)
                                FROM vente_marge WHERE est_retour = 0""")
    out["r2_marge_cible_min_pct"] = 18.0
    out["r2_marge_cible_max_pct"] = 24.0
    out["r2_rupture_jours"] = un("SELECT SUM(jours_rupture) FROM rupture")
    out["r2_rupture_ca_estime"] = un("SELECT ROUND(SUM(ca_perdu_estime_fcfa)) FROM rupture")

    # ---------------------------------------------------- 3. predictif
    vals = [v for _, v in serie]
    mois = [m for m, _ in serie]
    d = dict(serie)
    erreurs = {"naive": [], "saisonniere": [], "moyenne": []}
    base = sum(vals[-24:-12]) / 12.0
    for i, m in enumerate(mois):
        if not m.startswith("2026"):
            continue
        reel = d[m]
        erreurs["naive"].append(abs(reel - vals[i - 1]) / reel)
        an_prec = d.get("%d-%s" % (int(m[:4]) - 1, m[5:]))
        if an_prec:
            erreurs["saisonniere"].append(abs(reel - an_prec) / reel)
        erreurs["moyenne"].append(abs(reel - base) / reel)
    out["r3_mois_evalues"] = len(erreurs["naive"])
    out["r3_mape_naive_pct"] = round(100 * sum(erreurs["naive"]) / len(erreurs["naive"]), 1)
    out["r3_mape_saisonniere_pct"] = round(
        100 * sum(erreurs["saisonniere"]) / len(erreurs["saisonniere"]), 1)
    out["r3_mape_moyenne_pct"] = round(
        100 * sum(erreurs["moyenne"]) / len(erreurs["moyenne"]), 1)
    out["r3_definition"] = (
        "trois projections du mois sont testées sur les %d mois de 2026 : reconduire le mois "
        "précédent se trompe de %s %% en moyenne, la même période de l'an dernier de %s %%, la "
        "moyenne des douze derniers mois de %s %% — la plus simple est la meilleure, et aucune ne "
        "descend sous 12 %% : c'est la mesure qui autorise (ou interdit) une promesse prédictive"
        % (out["r3_mois_evalues"], fmt(out["r3_mape_naive_pct"]),
           fmt(out["r3_mape_saisonniere_pct"]), fmt(out["r3_mape_moyenne_pct"])))

    # ---------------------------------------------------- 4. prescriptif
    tranches = q("""
        SELECT CASE WHEN date_diff('day', date_echeance, DATE '2026-08-31') <= 30 THEN '0-30 j'
                    WHEN date_diff('day', date_echeance, DATE '2026-08-31') <= 60 THEN '31-60 j'
                    WHEN date_diff('day', date_echeance, DATE '2026-08-31') <= 90 THEN '61-90 j'
                    ELSE 'plus de 90 j' END AS tranche,
               COUNT(*), ROUND(SUM(montant_ttc))
        FROM encaissement WHERE date_encaissement IS NULL GROUP BY 1 ORDER BY 1""")
    out["r4_balance_agee"] = [{"tranche": t, "factures": n, "montant_fcfa": m}
                              for t, n, m in tranches]
    total_ouvert = sum(x["montant_fcfa"] for x in out["r4_balance_agee"])
    plus90 = next(x for x in out["r4_balance_agee"] if x["tranche"] == "plus de 90 j")
    out["r4_encours_ouvert_fcfa"] = total_ouvert
    out["r4_part_plus_90_pct"] = round(100.0 * plus90["montant_fcfa"] / total_ouvert, 1)
    out["r4_file_relance"] = plus90["factures"]
    out["r4_file_relance_fcfa"] = plus90["montant_fcfa"]
    retard = q("""SELECT COUNT(*), MEDIAN(date_diff('day', date_echeance, date_encaissement))
                  FROM encaissement
                  WHERE date_encaissement IS NOT NULL
                    AND date_encaissement > date_echeance""")
    out["r4_payees_en_retard"] = retard[0][0]
    out["r4_retard_median_jours"] = retard[0][1]
    out["r4_definition"] = (
        "la prescription tient en une phrase : relancer les %s factures de plus de 90 jours, qui "
        "pèsent %s FCFA, soit %s %% de l'encours ouvert (%s FCFA) — le seuil existe, la file "
        "existe, le montant existe, et il ne manque que le nom du responsable"
        % (fmt(out["r4_file_relance"]), fmt(out["r4_file_relance_fcfa"]),
           fmt(out["r4_part_plus_90_pct"]), fmt(out["r4_encours_ouvert_fcfa"])))
    con.close()
    return out


def main():
    k = mesurer()
    if "--json" in sys.argv:
        print(json.dumps(k, ensure_ascii=False, indent=2, sort_keys=True))
        return
    print("=== les 10 indicateurs du module M12, mesures sur le socle ===")
    print()
    lignes = [
        ("1. CA net", "%s FCFA" % fmt(k["k01_ca_net_fcfa"]),
         "ventes nettes de retours, toutes lignes non retournees"),
        ("   CA brut (avec retours)", "%s FCFA" % fmt(k["k01_ca_avec_retours_fcfa"]),
         "deux definitions, %s FCFA d'ecart (%s %%)"
         % (fmt(abs(k["k01_ecart_definitions_fcfa"])), fmt(k["k01_ecart_definitions_pct"]))),
        ("2. Marge brute", "%s FCFA (taux %s %%)"
         % (fmt(k["k02_marge_brute_fcfa"]), fmt(k["k02_taux_marge_pct"])),
         "vente HT - cout standard x quantite ; %s %% hors des 2 produits a prix manquant ; "
         "prix de vente moyens %s -> %s FCFA quand le referentiel reste a %s"
         % (fmt(k["k02_taux_marge_hors_deux_produits_pct"]),
            fmt(k["k02_prix_unitaire_par_an"][0]["prix_vente_moyen"]),
            fmt(k["k02_prix_unitaire_par_an"][-1]["prix_vente_moyen"]),
            fmt(k["k02_prix_unitaire_par_an"][0]["prix_referentiel"]))),
        ("3. Taux de rupture", "%s %% (%s couples sur %s servis)"
         % (fmt(k["k03_taux_rupture_pct"]), fmt(k["k03_couples_en_rupture"]),
            fmt(k["k03_couples_servis"])),
         "%s jours de rupture, %s FCFA de CA perdu ESTIME"
         % (fmt(k["k03_jours_rupture"]), fmt(k["k03_ca_perdu_estime_fcfa"]))),
        ("4. Rotation de stock", "%s tours par an (couverture %s mois)"
         % (fmt(k["k04_rotation_annuelle"]), fmt(k["k04_couverture_mois"])),
         "12 mois glissants : %s unites vendues, stock moyen mensuel %s unites"
         % (fmt(k["k04_ventes_12_mois_unites"]), fmt(k["k04_stock_moyen_mensuel_unites"]))),
        ("5. Panier moyen", "%s FCFA par ticket, %s FCFA en mediane"
         % (fmt(k["k05_panier_moyen_ticket_fcfa"]), fmt(k["k05_panier_median_fcfa"])),
         "la ligne moyenne vaut %s FCFA : %s %% plus bas que le panier ticket"
         % (fmt(k["k05_ligne_moyenne_fcfa"]), fmt(k["k05_ecart_ticket_ligne_pct"]))),
        ("6. Taux de retour", "%s %% des lignes, %s %% des tickets"
         % (fmt(k["k06_taux_retour_lignes_pct"]), fmt(k["k06_taux_retour_tickets_pct"])),
         "%s lignes de retour sur %s ; %s tickets sur %s en portent un (%s mixtes, %s seuls)"
         % (fmt(k["k06_lignes_retour"]), fmt(k["k06_lignes_total"]),
            fmt(k["k06_tickets_avec_retour"]), fmt(k["k06_tickets_total"]),
            fmt(k["k06_tickets_mixtes"]), fmt(k["k06_tickets_retour_seul"]))),
        ("7. Taux de service", "%s %% des livrees, %s %% des commandes"
         % (fmt(k["k07_taux_service_pct"]), fmt(k["k07_taux_service_annulees_incluses_pct"])),
         "%s commandes a l'heure sur %s livrees (%s annulees), retard median %s jours"
         % (fmt(k["k07_a_lheure"]), fmt(k["k07_livrees"]), fmt(k["k07_annulees"]),
            fmt(k["k07_retard_median_jours"]))),
        ("8. Taux de recouvrement", "%s %% a echeance"
         % fmt(k["k08_taux_recouvrement_pct"]),
         "%s factures, %s ouvertes ; encours ouvert %s FCFA, DSO %s jours"
         % (fmt(k["k08_factures"]), fmt(k["k08_ouvertes"]),
            fmt(k["k08_encours_ouvert_fcfa"]), fmt(k["k08_dso_jours"]))),
        ("9. Cout logistique unitaire", "%s FCFA par colis, %s FCFA au kilo"
         % (fmt(k["k09_cout_unitaire_fcfa"]), fmt(k["k09_cout_au_kg_fcfa"])),
         "%s colis (%s hors depot), %s FCFA de cout, dont %s %% de carburant"
         % (fmt(k["k09_colis"]), fmt(k["k09_colis_magasins"]),
            fmt(k["k09_cout_total_fcfa"]), fmt(k["k09_part_carburant_pct"]))),
        ("10. Part de marche interne", "%d magasins classes"
         % len(k["k10_parts_ville"]),
         "premier point de vente : %s (%s %% de son reseau)"
         % (k["k10_parts_ville"][0]["magasin"], fmt(k["k10_parts_ville"][0]["part_reseau_pct"]))),
    ]
    for nom, valeur, note in lignes:
        print("  %-28s %s" % (nom, valeur))
        print("  %-28s   %s" % ("", note))
    print()
    print("  depot sans vente : %d magasin, %s colis factures a son nom"
          % (k["k10_depot_sans_vente"], fmt(k["k10_colis_depot"])))
    print("  juge de paix : un indicateur sans definition ecrite n'est pas un indicateur.")

    r = mesurer_regimes()
    print()
    print("=== les 4 regimes de question (C02), mesures ===")
    print("  1. descriptif   : %s mois (%s -> %s), %s cellules magasin-mois-famille,"
          % (fmt(r["r1_mois"]), r["r1_premier_mois"], r["r1_dernier_mois"], fmt(r["r1_cellules"])))
    print("                    lundi %s FCFA contre dimanche %s (x %s), %s %% du CA apres le 25"
          % (fmt(r["r1_ca_lundi"]), fmt(r["r1_ca_dimanche"]), fmt(r["r1_ratio_lundi_dimanche"]),
             fmt(r["r1_part_fin_de_mois_pct"])))
    print("  2. diagnostique : marge %s %% pour une cible de %s a %s %%, %s jours de rupture,"
          % (fmt(r["r2_marge_pct"]), fmt(r["r2_marge_cible_min_pct"]),
             fmt(r["r2_marge_cible_max_pct"]), fmt(r["r2_rupture_jours"])))
    print("                    soit %s FCFA ESTIMES" % fmt(r["r2_rupture_ca_estime"]))
    print("  3. predictif    : MAPE naive %s %%, saisonniere %s %%, moyenne %s %% sur %s mois"
          % (fmt(r["r3_mape_naive_pct"]), fmt(r["r3_mape_saisonniere_pct"]),
             fmt(r["r3_mape_moyenne_pct"]), fmt(r["r3_mois_evalues"])))
    print("  4. prescriptif  : %s factures de plus de 90 jours (%s FCFA), soit %s %% de l'encours"
          % (fmt(r["r4_file_relance"]), fmt(r["r4_file_relance_fcfa"]),
             fmt(r["r4_part_plus_90_pct"])))

    g = mesurer_grain()
    print()
    print("=== le vocabulaire exact (C03), mesure ===")
    print("  %d tables, %d a cle unique ; %d couples canal x mode"
          % (g["g_tables"], g["g_tables_cles_uniques"], g["g_couples_canal_mode"]))
    print("  additif    : CA = somme par magasin (%s FCFA)" % fmt(g["g_ca_total"]))
    print("  non additif: clients %s (par produit) / %s (par magasin) pour %s reels"
          % (fmt(g["g_clients_somme_par_produit"]), fmt(g["g_clients_somme_par_magasin"]),
             fmt(g["g_clients_total"])))
    print("  moyenne de moyennes : %s contre %s FCFA (%s %%)"
          % (fmt(g["g_panier_moyenne_des_moyennes"]), fmt(g["g_panier_vraie_moyenne"]),
             fmt(g["g_panier_ecart_pct"])))
    print("  clôture de stock : %s unites au dernier mois, %s si on somme les 44 mois (x %s)"
          % (fmt(g["g_stock_cloture"]), fmt(g["g_stock_somme_tous_mois"]), fmt(g["g_stock_ratio"])))
    print("  cle oubliee: x %s de lignes et x %s de CA (%s FCFA)"
          % (fmt(g["g_jointure_sans_mois_facteur"]), fmt(g["g_jointure_sans_mois_ca_facteur"]),
             fmt(int(g["g_jointure_sans_mois_ca"]))))


if __name__ == "__main__":
    main()
