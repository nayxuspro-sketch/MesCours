#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""connexion.py — ouvrir le socle depuis le dossier M14.

    import sys; sys.path.insert(0, '03_exercices/dossier_M14')
    from connexion import ouvrir
    con = ouvrir()

Le socle du module M14 est celui de M13 : M14 n'ajoute aucune table. Il n'ajoute qu'une
colonne, le cout d'achat, et cette colonne vit deja dans `cout_produit` (source M12) :
la FUSION de requetes de Power Query la fait entrer dans le referentiel produit.

Les fichiers d'import CSV ne sont pas versionnes (12 tables, 29,3 Mo) : ils se
regenere hors atelier par `python3 tools/mesures_M14.py --export`.
"""
from __future__ import annotations

import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def ouvrir(fautif=False):
    """Ouvre le socle M13 (donc M11, M12 et M13) et rend la connexion DuckDB."""
    sys.path.insert(0, os.path.join(RACINE, "03_exercices", "dossier_M13"))
    from connexion import ouvrir as ouvrir_m13
    return ouvrir_m13(fautif=fautif)


if __name__ == "__main__":
    c = ouvrir()
    print("modele M14 (celui de M13, plus le cout d'achat) :")
    print("  fait_ventes      :", c.execute("SELECT COUNT(*) FROM fait_ventes").fetchone()[0])
    print("  dim_produit      :", c.execute("SELECT COUNT(*) FROM dim_produit").fetchone()[0])
    print("  cout_produit     :", c.execute("SELECT COUNT(*) FROM cout_produit").fetchone()[0])
    sys.exit(0)
