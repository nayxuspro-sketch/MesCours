#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""connexion.py — ouvre le socle M11 de n'importe quel dossier de travail.

    import sys; sys.path.insert(0, "03_exercices/dossier_M11")
    from connexion import ouvrir

    con = ouvrir()                    # le socle, prêt à interroger (0,4 s)
    con = ouvrir(materialiser=True)   # + copies en mémoire `ventes_m`, `clients_m`
                                      #   pour tout ce qui parle de performance

Le socle est un SCRIPT, pas un fichier de base : cette fonction le rejoue en mémoire.
Les vues pointent vers des CSV par des chemins **relatifs à la racine du dépôt** :
la fonction s'y place avant d'ouvrir, sinon DuckDB ne trouve pas les fichiers.
C'est le premier réflexe de tout rapport M11.
"""
from __future__ import annotations

import os

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FICHIER_SQL = os.path.join(RACINE, "03_exercices", "dossier_M11", "socle_m11.sql")


def ouvrir(materialiser: bool = False):
    """Rend une connexion DuckDB en mémoire, socle chargé."""
    import duckdb
    os.chdir(RACINE)
    sql = open(FICHIER_SQL, encoding="utf-8").read()
    con = duckdb.connect()
    con.execute(sql)
    if materialiser:
        con.execute("CREATE OR REPLACE TABLE ventes_m AS SELECT * FROM ventes")
        con.execute("CREATE OR REPLACE TABLE clients_m AS SELECT * FROM clients")
    return con
