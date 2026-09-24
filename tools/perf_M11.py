#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""perf_M11.py — l'instrument de mesure du chapitre C06 (requêtes lentes et plans).

Il mesure, sur le socle M11, les quatre faits du chapitre :

  1. une **vue** (qui relit le CSV) contre une **table** (copiée en mémoire) ;
  2. le coût du `SELECT *` contre trois colonnes nommées — à l'horloge **et dans le plan** ;
  3. l'effet d'un **index**, sur une recherche par client et sur un agrégat ;
  4. ce que `EXPLAIN` annonce, étage par étage, avant toute exécution.

Chaque mesure d'horloge est la **médiane de 5 exécutions** : le premier appel paie la
lecture du fichier, les suivants non. Un temps machine n'est pas reproductible au bit
près — c'est pourquoi le protocole est publié, et pourquoi les valeurs retenues sont
**figées** par `--figer` dans `PERF_M11.json` (daté), que `chiffres_manuel.py` relit.
Deux relevés de `chiffres_manuel.py` restent donc identiques, même sur une machine
plus lente.

Usage :
    python3 tools/perf_M11.py            # mesure et affiche
    python3 tools/perf_M11.py --figer    # mesure et fige PERF_M11.json
"""
from __future__ import annotations

import json
import os
import statistics
import sys
import time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = os.path.join(RACINE, "03_exercices", "dossier_M11")
SQL = os.path.join(DOSSIER, "socle_m11.sql")
FICHIER = os.path.join(DOSSIER, "PERF_M11.json")
REPETITIONS = 5
OPERATEURS = ("HASH_GROUP_BY", "PROJECTION", "HASH_JOIN", "SEQ_SCAN", "TABLE_SCAN", "READ_CSV",
              "FILTER", "ORDER_BY", "UNGROUPED_AGGREGATE", "TOP_N", "PIVOT")


def median_ms(con, requete: str, repetitions: int = REPETITIONS) -> float:
    temps = []
    for _ in range(repetitions):
        t = time.perf_counter()
        con.execute(requete).fetchall()
        temps.append((time.perf_counter() - t) * 1000)
    return round(statistics.median(temps), 1)


def etages(plan: str) -> list:
    """Les opérateurs du plan, en lisant les cases du cadre dessiné par EXPLAIN."""
    trouves = []
    for ligne in plan.split("\n"):
        mot = ligne.strip("│ ┌┐└┘─ ").strip()
        if mot in OPERATEURS and (not trouves or trouves[-1] != mot):
            trouves.append(mot)
    return trouves


def colonnes_projetees(plan: str) -> int:
    """Nombre de colonnes listées sous « Projections: » dans un SEQ_SCAN."""
    lignes = plan.split("\n")
    for i, l in enumerate(lignes):
        if "Projections:" in l:
            n = 0
            for suite in lignes[i + 1:]:
                if not suite.strip("│ ").strip():
                    break
                n += 1
            return n
    return 0


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    try:
        import duckdb
    except ImportError as e:  # pragma: no cover
        raise SystemExit("duckdb indisponible (%s)" % e)

    os.chdir(RACINE)
    con = duckdb.connect()
    con.execute(open(SQL, encoding="utf-8").read())
    print("=== perf_M11 : mesures de C06 (médiane de %d exécutions) ===" % REPETITIONS)

    # 1. vue contre table
    vue_ms = median_ms(con, "SELECT COUNT(*) FROM ventes WHERE est_retour")
    con.execute("CREATE OR REPLACE TABLE ventes_m AS SELECT * FROM ventes")
    table_ms = median_ms(con, "SELECT COUNT(*) FROM ventes_m WHERE est_retour")
    print("  1. vue (relit le CSV)   %8.1f ms" % vue_ms)
    print("     table (en mémoire)   %8.1f ms   -> rapport x%.0f" % (table_ms, vue_ms / table_ms))

    # 2. SELECT * contre colonnes nommées, à l'horloge et dans le plan
    etoile_ms = median_ms(con, "SELECT * FROM ventes_m")
    trois_ms = median_ms(con, "SELECT date_vente, id_magasin, montant_ttc FROM ventes_m")
    vue_etoile_ms = median_ms(con, "SELECT * FROM ventes")
    vue_trois_ms = median_ms(con, "SELECT date_vente, id_magasin, montant_ttc FROM ventes")
    plan_etoile = con.execute("EXPLAIN SELECT * FROM ventes_m").fetchall()[0][1]
    plan_trois = con.execute(
        "EXPLAIN SELECT date_vente, id_magasin, montant_ttc FROM ventes_m").fetchall()[0][1]
    col_etoile = colonnes_projetees(plan_etoile)
    col_trois = colonnes_projetees(plan_trois)
    print("  2. table : SELECT *      %8.1f ms  (plan : %d colonnes lues)" % (etoile_ms, col_etoile))
    print("     table : 3 colonnes   %8.1f ms  (plan : %d colonnes lues) -> x%.1f"
          % (trois_ms, col_trois, etoile_ms / trois_ms))
    print("     vue   : SELECT *     %8.1f ms | 3 colonnes %8.1f ms -> x%.1f"
          % (vue_etoile_ms, vue_trois_ms, vue_etoile_ms / vue_trois_ms))

    # 3. index
    client = 15676
    point = "SELECT COUNT(*), SUM(montant_ttc) FROM ventes_m WHERE id_client = %d" % client
    avant = median_ms(con, point)
    con.execute("CREATE INDEX idx_m11_client ON ventes_m(id_client)")
    apres = median_ms(con, point)
    groupe = "SELECT id_magasin, SUM(montant_ttc) FROM ventes_m GROUP BY 1 ORDER BY 1"
    g_avant = median_ms(con, groupe)
    con.execute("CREATE INDEX idx_m11_magasin ON ventes_m(id_magasin)")
    g_apres = median_ms(con, groupe)
    plan_point = con.execute(
        "EXPLAIN SELECT COUNT(*), SUM(montant_ttc) FROM ventes_m WHERE id_client = %d" % client
    ).fetchall()[0][1]
    indice_utilise = "INDEX_SCAN" in plan_point
    print("  3. recherche client %d : sans index %6.1f ms | avec index %6.1f ms"
          % (client, avant, apres))
    print("     agrégat par magasin  : sans index %6.1f ms | avec index %6.1f ms"
          % (g_avant, g_apres))
    print("     le plan utilise-t-il l'index ? %s" % ("oui" if indice_utilise else "non (SEQ_SCAN)"))

    # 4. EXPLAIN
    plan = con.execute(
        "EXPLAIN SELECT m.nom, SUM(v.montant_ttc) FROM ventes_m v "
        "JOIN magasin m USING(id_magasin) GROUP BY 1").fetchall()[0][1]
    liste_etages = etages(plan)
    print("  4. EXPLAIN : %d étages -> %s" % (len(liste_etages), " | ".join(liste_etages)))

    figees = {
        "date": time.strftime("%d/%m/%Y"),
        "protocole": "mediane de %d executions, DuckDB %s, atelier" % (REPETITIONS, duckdb.__version__),
        "instrument": "tools/perf_M11.py",
        "vue_ms": int(round(vue_ms)),
        "table_ms": max(1, int(round(table_ms))),
        "select_etoile_ms": int(round(etoile_ms)),
        "select_trois_colonnes_ms": int(round(trois_ms)),
        "vue_select_etoile_ms": int(round(vue_etoile_ms)),
        "vue_select_trois_colonnes_ms": int(round(vue_trois_ms)),
        "index_client_sans_ms": round(avant, 1),
        "index_client_avec_ms": round(apres, 1),
        "index_agregat_sans_ms": round(g_avant, 1),
        "index_agregat_avec_ms": round(g_apres, 1),
        "index_utilise_par_le_plan": indice_utilise,
        "colonnes_plan_etoile": col_etoile,
        "colonnes_plan_trois": col_trois,
        "etages_plan": len(liste_etages),
        "etages_liste": liste_etages,
    }
    print("\n  | mesure | sans | avec | rapport |")
    print("  |---|---|---|---|")
    print("  | vue contre table | %d ms | %d ms | x%d |"
          % (vue_ms, figees["table_ms"], round(vue_ms / figees["table_ms"])))
    print("  | SELECT * contre 3 colonnes | %d ms | %d ms | x%.1f |"
          % (etoile_ms, trois_ms, etoile_ms / trois_ms))
    print("  | index, recherche client | %.1f ms | %.1f ms | %s |"
          % (avant, apres, "aucun effet"))
    print("  | index, agrégat magasin | %.1f ms | %.1f ms | %s |"
          % (g_avant, g_apres, "aucun effet"))
    print("  | colonnes lues dans le plan | %d | %d | x%.1f |"
          % (col_etoile, col_trois, col_etoile / col_trois if col_trois else 0))

    if "--figer" in argv:
        json.dump(figees, open(FICHIER, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print("\n  valeurs figées : %s" % os.path.relpath(FICHIER, RACINE))
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
