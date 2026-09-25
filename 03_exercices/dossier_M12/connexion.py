#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""connexion.py — ouvrir le socle du module M12 (BI).

    import sys; sys.path.insert(0, '03_exercices/dossier_M12')
    from connexion import ouvrir
    con = ouvrir()

Le socle est un SCRIPT, pas un fichier de base : il rejoue deux fichiers SQL, dans
l'ordre — celui de M11 (ventes et référentiels) puis celui de M12 (les cinq tables
opérationnelles). Aucun fichier `.duckdb` n'est versionné : le format a un plancher
d'environ 512 Ko, et l'atelier vit sous quota.

Paramètres :
    materialiser=False  (défaut) : les ventes restent des VUES ; le socle s'ouvre en
                        quelques dixièmes de seconde et ne pèse rien en mémoire.
    materialiser=True   : les ventes sont copiées en table (`ventes_m`) ; c'est le
                        mode des mesures de volume et de plan, celui du chapitre C06
                        de M11 — et de toute mesure de performance.
"""
from __future__ import annotations

import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def ouvrir(materialiser=False):
    import duckdb
    con = duckdb.connect()
    con.execute("SET enable_progress_bar = false;")
    for nom in ("dossier_M11/socle_m11.sql", "dossier_M12/socle_m12.sql"):
        chemin = os.path.join(RACINE, "03_exercices", nom)
        with open(chemin, encoding="utf-8") as f:
            con.execute(f.read())
    if materialiser:
        con.execute("CREATE OR REPLACE TABLE ventes_m AS SELECT * FROM ventes;")
        con.execute("CREATE OR REPLACE TABLE clients_m AS SELECT * FROM clients;")
    return con


if __name__ == "__main__":
    c = ouvrir()
    tables = c.execute("SELECT table_name FROM information_schema.tables "
                       "ORDER BY table_name").fetchall()
    print("socle M12 :", ", ".join(t[0] for t in tables))
    print("ventes    :", c.execute("SELECT COUNT(*) FROM ventes").fetchone()[0], "lignes")
    sys.exit(0)
