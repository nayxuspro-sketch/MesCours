#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""connexion.py — ouvrir le socle du module M13 (modelisation des donnees).

    import sys; sys.path.insert(0, '03_exercices/dossier_M13')
    from connexion import ouvrir
    con = ouvrir()

Le socle est un SCRIPT, pas un fichier de base : il rejoue trois fichiers SQL, dans
l'ordre — M11 (ventes et referentiels), M12 (les cinq sources operationnelles),
M13 (le modele en etoile). Aucun fichier `.duckdb` n'est versionne : le format a un
plancher d'environ 512 Ko, et l'atelier vit sous quota.

Le modele M13 ajoute DOUZE tables (5 dimensions + 7 faits) et DEUX dimensions
historisees (type 2) ; les modeles fautifs sont dans `modele_fautif.sql`.

Parametres :
    materialiser=False  (defaut) : les ventes restent des VUES ; le socle s'ouvre en
                        quelques dixiemes de seconde et ne pese rien en memoire.
    materialiser=True   : les ventes et les faits sont copies en table ; c'est le mode
                        des mesures de volume et de plan.
"""
from __future__ import annotations

import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def ouvrir(materialiser=False, fautif=False):
    import duckdb
    con = duckdb.connect()
    con.execute("SET enable_progress_bar = false;")
    for nom in ("dossier_M11/socle_m11.sql", "dossier_M12/socle_m12.sql",
                "dossier_M13/socle_m13.sql"):
        chemin = os.path.join(RACINE, "03_exercices", nom)
        with open(chemin, encoding="utf-8") as f:
            con.execute(f.read())
    if fautif:
        chemin = os.path.join(RACINE, "03_exercices", "dossier_M13", "modele_fautif.sql")
        with open(chemin, encoding="utf-8") as f:
            con.execute(f.read())
    if materialiser:
        for t in ("ventes", "fait_ventes", "fait_commandes", "fait_encaissements"):
            con.execute("CREATE OR REPLACE TABLE %s_m AS SELECT * FROM %s;" % (t, t))
    return con


if __name__ == "__main__":
    c = ouvrir(fautif=True)
    tables = c.execute("SELECT table_name FROM information_schema.tables "
                       "ORDER BY table_name").fetchall()
    print("tables du modele M13 :", ", ".join(t[0] for t in tables if t[0].startswith(("dim_", "fait_"))))
    print("fait_ventes    :", c.execute("SELECT COUNT(*) FROM fait_ventes").fetchone()[0], "lignes")
    print("dim_client_scd :", c.execute("SELECT COUNT(*) FROM dim_client_scd").fetchone()[0], "versions")
    rec = c.execute("SELECT * FROM recette_ca").fetchone()
    print("recette        : modele %s / source %s" % (rec[0], rec[1]))
    sys.exit(0)
