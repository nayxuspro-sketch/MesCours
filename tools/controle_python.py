#!/usr/bin/env python3
"""Contrôle Q3 (porte §G.1) côté Python : les blocs ```python publiés sont exécutés.

Les blocs d'un même chapitre sont exécutés **dans le même espace de noms et dans
l'ordre de lecture**, parce que c'est ce que fait l'apprenant qui tape le chapitre :
un bloc qui s'appuie sur la variable définie deux pages plus haut est légitime. Un
bloc qui échoue pour une autre raison (nom inconnu, formule fausse, accroche
d'API) est un défaut du manuel.

Préambule injecté (il correspond au préambule enseigné en M01/M02) : pandas, numpy,
scipy.stats, `df` = extrait nettoyé du magasin 5 sur 2025, `pop` = ventes propres.

Usage : python3 tools/controle_python.py M02 [--max-erreurs 20]
"""
import argparse, contextlib, glob, io, pathlib, re, sys, traceback

RACINE = pathlib.Path(__file__).resolve().parents[1]
PREAMBULE = """
import numpy as np, pandas as pd
from scipy import stats
pd.set_option("display.width", 120)
df = pd.read_csv(RACINE / "01_socle_donnees/data/reference/ventes_magasin5_2025_ATTENDU.csv",
                 sep=";", encoding="utf-8-sig")
pop = pd.read_csv(RACINE / "01_socle_donnees/data/reference/ventes_propres.csv",
                  sep=";", encoding="utf-8-sig")
"""

def blocs(fichiers):
    for f in fichiers:
        lignes = pathlib.Path(f).read_text(encoding="utf-8").splitlines()
        i = 0
        while i < len(lignes):
            j = i
            if lignes[i].strip() in ("```python", "```py"):
                j = i + 1
                while j < len(lignes) and lignes[j].strip() != "```":
                    j += 1
                yield pathlib.Path(f).name, i + 1, "\n".join(lignes[i + 1:j])
            i = j + 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("module")
    ap.add_argument("--max-erreurs", type=int, default=20)
    a = ap.parse_args()
    fs = sorted(glob.glob(str(RACINE / "02_modules" / f"{a.module}_*.md")))
    ns = {"__name__": "__contrôle__", "RACINE": RACINE, "pd": None}
    exec(PREAMBULE, ns)
    ok = frag = ko = 0
    for nom, ligne, code in blocs(fs):
        entete = f"{nom}:{ligne}"
        if re.search(r"^\s*(#|→).*(attendu|sortie)", code, re.M) and not code.strip():
            continue
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(code, entete, "exec"), ns)
            ok += 1
            sortie = " ; ".join(x.strip() for x in buf.getvalue().splitlines() if x.strip())[:110]
            print(f"  ✔  {entete}  {sortie}")
        except NameError as e:
            frag += 1
            print(f"  ~  {entete}  fragment pédagogique ({e})")
        except Exception as e:
            ko += 1
            print(f"  ✘  {entete}  {type(e).__name__}: {str(e)[:180]}")
            if ko <= 3:
                print("     " + "\n     ".join(traceback.format_exc().splitlines()[-4:]))
            if ko > a.max_erreurs:
                print("  … arrêt, trop d'erreurs")
                break
    print(f"Python publié : {ok} bloc(s) exécuté(s), {frag} fragment(s) à nom non résolu, {ko} défaut(s)")
    return 1 if ko else 0

if __name__ == "__main__":
    sys.exit(main())
