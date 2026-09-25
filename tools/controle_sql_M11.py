#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""controle_sql_M11.py — les tests de non-regression du module M11 (chapitre C07).

Le module publie des chiffres. Ceux-ci vivent dans
`01_socle_donnees/data/reference/chiffres_cites.json`, ecrits par le socle python
(`chiffres_manuel.py M11`). Ce controleur rejoue **18 requetes SQL** sur le socle
`03_exercices/dossier_M11/socle_m11.sql` et compare chaque resultat a la valeur publiee.

C'est un test **croise** : les deux cotes du controle n'ont pas la meme origine —
d'un cote une requete DuckDB executee a l'instant, de l'autre un fichier JSON fige
plus tot, eventuellement sur une autre machine. Si les deux divergent, ce n'est pas
« le test qui a echoue » : c'est le socle, la requete ou le fichier publie qui a
change, et il faut savoir lequel avant de livrer un rapport.

Usage :
    python3 tools/controle_sql_M11.py            # les 18 controles
    python3 tools/controle_sql_M11.py --liste    # les noms des controles seuls
"""
from __future__ import annotations

import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = os.path.join(RACINE, "03_exercices", "dossier_M11")
SQL = os.path.join(DOSSIER, "socle_m11.sql")
REF = os.path.join(RACINE, "01_socle_donnees", "data", "reference", "chiffres_cites.json")

# (cle publiee, requete, type) — chaque requete repond a une question metier du module.
CONTROLES = [
    ("m11_lignes", "SELECT COUNT(*) FROM ventes", "int"),
    ("m11_lignes_hors_retours", "SELECT COUNT(*) FROM ventes WHERE NOT est_retour", "int"),
    ("m11_retours", "SELECT COUNT(*) FROM ventes WHERE est_retour", "int"),
    ("m11_tickets", "SELECT COUNT(DISTINCT id_ticket) FROM ventes WHERE NOT est_retour", "int"),
    ("m11_clients_vente", "SELECT COUNT(DISTINCT id_client) FROM ventes", "int"),
    ("m11_magasins", "SELECT COUNT(DISTINCT id_magasin) FROM ventes", "int"),
    ("m11_produits", "SELECT COUNT(DISTINCT id_produit) FROM ventes", "int"),
    ("m11_ca_2023",
     "SELECT ROUND(SUM(montant_ttc)) FROM ventes WHERE NOT est_retour "
     "AND YEAR(date_vente) = 2023", "int"),
    ("m11_ca_8_mois_2026",
     "SELECT ROUND(SUM(montant_ttc)) FROM ventes WHERE NOT est_retour "
     "AND YEAR(date_vente) = 2026 AND MONTH(date_vente) <= 8", "int"),
    ("m11_client0_lignes",
     "SELECT COUNT(*) FROM ventes WHERE NOT est_retour AND id_client = 0", "int"),
    ("m11_client0_ca",
     "SELECT ROUND(SUM(montant_ttc)) FROM ventes WHERE NOT est_retour AND id_client = 0", "int"),
    # la requete est rejouee A L'IDENTIQUE (ordre descendant compris) : un test qui
    # reecrit la requete teste autre chose — en ordre croissant, on lirait 23 497.
    ("m11_c02_max_rank",
     "WITH c AS (SELECT id_client, COUNT(DISTINCT id_ticket) t FROM ventes WHERE NOT est_retour "
     "GROUP BY 1), r AS (SELECT RANK() OVER (ORDER BY t DESC) rk FROM c) SELECT MAX(rk) FROM r", "int"),
    ("m11_c02_max_dense_rank",
     "WITH c AS (SELECT id_client, COUNT(DISTINCT id_ticket) t FROM ventes WHERE NOT est_retour "
     "GROUP BY 1), r AS (SELECT DENSE_RANK() OVER (ORDER BY t DESC) dr FROM c) "
     "SELECT MAX(dr) FROM r", "int"),
    ("m11_c03_ratio_saison",
     "WITH s AS (SELECT MONTH(date_vente) m, SUM(montant_ttc) / COUNT(DISTINCT date_trunc('month', "
     "date_vente)) ca FROM ventes WHERE NOT est_retour GROUP BY 1) "
     "SELECT ROUND(MAX(ca) / MIN(ca), 2) FROM s", "float"),
    ("m11_c04_rfm_blocs",
     "WITH c AS (SELECT id_client, MAX(date_vente) d FROM ventes WHERE NOT est_retour GROUP BY 1) "
     "SELECT COUNT(*) FILTER (WHERE r = 1) FROM (SELECT NTILE(3) OVER (ORDER BY d DESC, id_client) r "
     "FROM c)", "int"),
    ("m11_c04_oneshot",
     "SELECT COUNT(*) FROM (SELECT id_client, COUNT(DISTINCT date_trunc('month', date_vente)) nm "
     "FROM ventes WHERE NOT est_retour GROUP BY 1) WHERE nm = 1", "int"),
    ("m11_c05_grouping_sets_lignes",
     "WITH n AS (SELECT id_produit, CASE WHEN UPPER(TRIM(categorie)) IN ('MATERIAUX', 'MATÉRIAUX') "
     "THEN 'MATÉRIAUX' WHEN UPPER(TRIM(categorie)) IN ('PEINTURE', 'PEINTURES') THEN 'PEINTURE' "
     "WHEN UPPER(TRIM(categorie)) = 'ELECTRICITÉ' THEN 'ÉLECTRICITÉ' ELSE UPPER(TRIM(categorie)) END "
     "AS f FROM produit), b AS (SELECT ma.quartier q, n.f f FROM ventes v JOIN magasin ma "
     "USING (id_magasin) JOIN n USING (id_produit) WHERE NOT v.est_retour GROUP BY 1, 2) "
     "SELECT COUNT(*) FROM (SELECT 1 FROM b GROUP BY GROUPING SETS ((q), (f), (q, f)))", "int"),
    ("m11_calendrier_jours", "SELECT COUNT(*) FROM calendrier", "int"),
]


def nombre(valeur):
    """Extrait un nombre d'une valeur publiee : « 15 595 154 955 FCFA », « 38.1 » ou 23497."""
    if isinstance(valeur, (int, float)):
        return float(valeur)
    t = str(valeur).replace("\u202f", " ").replace(" ", "").replace("%", "")
    t = t.replace(",", ".")
    chiffres = ""
    for c in t:
        if c.isdigit() or c == ".":
            chiffres += c
        elif chiffres:
            break
    return float(chiffres) if chiffres else None


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    actifs = list(CONTROLES)
    if "--liste" in argv:
        for cle, _, _ in actifs:
            print(cle)
        return 0
    try:
        import duckdb
    except ImportError as e:
        raise SystemExit("duckdb indisponible (%s) : installer ou relancer dans l'atelier" % e)

    publie = json.load(open(REF, encoding="utf-8"))["M11"]
    os.chdir(RACINE)                      # les vues du socle sont relatives a la racine
    con = duckdb.connect()
    con.execute(open(SQL, encoding="utf-8").read())

    print("=== controle SQL M11 : %d requetes, une source par cote ===" % len(actifs))
    print("  cote SQL   : socle_m11.sql rejoue par DuckDB %s" % duckdb.__version__)
    print("  cote publie: chiffres_cites.json (%s cles M11)" % len(publie))
    print()
    print("  | # | controle | SQL | publie | verdict |")
    print("  |---|---|---|---|---|")
    echecs = []
    for i, (cle, requete, type_) in enumerate(actifs, 1):
        brut = con.execute(requete).fetchone()[0]
        attendu = publie.get(cle)
        if attendu is None:
            verdict, sql_v, pub_v = "cle absente", brut, "—"
        else:
            sql_v = float(brut)
            pub_v = nombre(attendu)
            if pub_v is None:
                verdict = "illisible"
            elif type_ == "int":
                verdict = "OK" if int(round(sql_v)) == int(round(pub_v)) else "ECART"
            else:
                verdict = "OK" if abs(sql_v - pub_v) <= 0.51 else "ECART"
            if verdict != "OK":
                echecs.append((i, cle, sql_v, pub_v, verdict))
        print("  | %d | %s | %s | %s | %s |" % (i, cle, brut, attendu, verdict))
    print()
    if echecs:
        print("  %d controle(s) en ecart — le fichier publie ne decrit plus le socle :" % len(echecs))
        for i, cle, a, b, v in echecs:
            print("    %d. %s : SQL %s / publie %s (%s)" % (i, cle, a, b, v))
        return 1
    print("  %d controles sur %d : OK — le socle et le fichier publie disent la meme chose."
          % (len(actifs), len(actifs)))
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
