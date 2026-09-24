#!/usr/bin/env python3
"""figures_M10.py — la recette des 7 planches du module M10 (Data visualization).

DIFFERENCE AVEC M01..M09. Dans les modules precedents, les planches etaient des SVG
dessines a la main (`figures_M0x.py` posait les coordonnees) : le script PRODUISAIT les
figures. Ici, les planches sont des graphiques **executes** : chacune est produite par le
script de son chapitre (`perception_M10.py`, `seize_graphiques_M10.py`, ...). Le role de ce
fichier est donc la **recette** : rejouer, comparer, mesurer, verifier la citation.

Pour chacune des 7 planches :
  1. rejouer le script du chapitre (il produit le SVG) ;
  2. verifier le DETERMINISME : deux executions, meme empreinte sha256 ;
  3. verifier la LARGEUR : <= 776 px (format du module, contrainte heritee de M08) ;
  4. verifier la CITATION : le chapitre cite le fichier, et sa legende renvoie a ../figures/ ;
  5. rapporter poids et dimensions.

Code de sortie : 0 si les 7 planches passent, 1 sinon.

Usage : python3 tools/figures_M10.py
"""
from __future__ import annotations

import hashlib
import io
import contextlib
import os
import re
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LARGEUR_MAX_PX = 776

CHAPITRES = {
    "C01": "M10_C01_ordre_perceptuel_comment_l_oeil_lit_un_graphique.md",
    "C02": "M10_C02_tableau_question_graphique_16_graphiques_carte_metriques.md",
    "C03": "M10_C03_couleurs_palettes_accessibilite_culture_locale.md",
    "C04": "M10_C04_ecrire_un_graphique_titres_axes_annotations.md",
    "C05": "M10_C05_les_10_erreurs_qui_tuent_la_credibilite.md",
    "C06": "M10_C06_storytelling_raconter_pour_decider.md",
    "C07": "M10_C07_matplotlib_excel_power_bi_support_export.md",
}

PLANCHES = [
    ("C01", "tools/perception_M10.py", "figures/M10_C01_cinq_encodages.svg"),
    ("C02", "tools/seize_graphiques_M10.py", "figures/M10_C02_seize_graphiques.svg"),
    ("C03", "tools/couleurs_M10.py", "figures/M10_C03_palette_testee.svg"),
    ("C04", "tools/ecriture_M10.py", "figures/M10_C04_ecriture_titre_axe_annotation.svg"),
    ("C05", "tools/erreurs_M10.py", "figures/M10_C05_mur_des_10_erreurs.svg"),
    ("C06", "tools/sequence_M10.py", "figures/M10_C06_sequence_trois_ecrans.svg"),
    ("C07", "tools/outils_M10.py", "figures/M10_C07_meme_graphique_trois_outils.svg"),
]


def empreinte(chemin):
    return hashlib.sha256(open(chemin, "rb").read()).hexdigest()


def dimensions(chemin):
    """Largeur et hauteur en pixels : les attributs sont en points (96/72)."""
    d = open(chemin, encoding="utf-8").read(700)
    m = re.search(r'width="([\d.]+)pt" height="([\d.]+)pt"', d)
    if m:
        return round(float(m.group(1)) * 96 / 72), round(float(m.group(2)) * 96 / 72)
    m = re.search(r'width="([\d.]+)" height="([\d.]+)"', d)
    return (round(float(m.group(1))), round(float(m.group(2)))) if m else (0, 0)


def rejouer(script):
    """Rejoue le script du chapitre : sortie, code de retour, duree."""
    r = subprocess.run([sys.executable, os.path.join(RACINE, script)],
                       capture_output=True, text=True, cwd=RACINE)
    return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()


def citation(chemin_svg, chapitre):
    """Le chapitre cite-t-il la planche, et par un chemin ../figures/... ?"""
    md = open(os.path.join(RACINE, "02_modules", chapitre), encoding="utf-8").read()
    nom = os.path.basename(chemin_svg)
    trouve = nom in md
    chemin_relatif = "](../figures/" + nom + ")" in md
    return trouve, chemin_relatif


def main():
    resultats, echecs = [], []
    print("=" * 92)
    print("RECETTE DES 7 PLANCHES — module M10 (Data visualization)")
    print("=" * 92)
    print(f"{'planche':10s} {'script':32s} {'px':>10s} {'Ko':>7s}  rejeu  determin.  citation")
    print("-" * 92)
    for chapitre, script, chemin in PLANCHES:
        svg = os.path.join(RACINE, chemin)
        if not os.path.exists(svg):
            echecs.append(f"{chapitre} : planche absente ({chemin})")
            continue
        avant = empreinte(svg)
        rc1, _, err1 = rejouer(script)
        rc2, _, err2 = rejouer(script)
        apres = empreinte(svg)
        l, h = dimensions(svg)
        ko = round(os.path.getsize(svg) / 1024, 1)
        deterministe = (avant == apres) and rc1 == 0 and rc2 == 0
        trouve, relatif = citation(chemin, CHAPITRES[chapitre])
        large = l <= LARGEUR_MAX_PX
        print(f"{chapitre:10s} {os.path.basename(script):32s} {str(l) + 'x' + str(h):>10s} "
              f"{ko:7.1f}  {'ok' if rc1 == 0 else 'KO':5s}  "
              f"{'ok' if deterministe else 'KO':9s}  "
              f"{'ok' if (trouve and relatif) else 'KO'}")
        if not large:
            echecs.append(f"{chapitre} : largeur {l} px > {LARGEUR_MAX_PX} px")
        if not deterministe:
            echecs.append(f"{chapitre} : non deterministe (rc={rc1}/{rc2}) {err1[:120]}")
        if not (trouve and relatif):
            echecs.append(f"{chapitre} : planche non citee par le chapitre "
                          f"({CHAPITRES[chapitre]})")
        resultats.append(dict(chapitre=chapitre, script=script, svg=chemin, largeur=l, hauteur=h,
                              ko=ko, deterministe=deterministe, citee=trouve and relatif,
                              empreinte=apres[:12]))
    print("-" * 92)
    largeur_max = max(r["largeur"] for r in resultats) if resultats else 0
    poids_total = round(sum(r["ko"] for r in resultats), 1)
    print(f"  planches : {len(resultats)} / 7   |   largeur maximale : {largeur_max} px "
          f"(limite {LARGEUR_MAX_PX})   |   poids total : {poids_total} Ko")
    print(f"  determinisme : {sum(r['deterministe'] for r in resultats)} / {len(resultats)}   |   "
          f"citation : {sum(r['citee'] for r in resultats)} / {len(resultats)}")
    print("-" * 92)
    for e in echecs:
        print("  ECHEC :", e)
    verdict = "OK" if not echecs else "ECHEC"
    print(f"  VERDICT : {verdict}")
    print("=" * 92)
    return 0 if not echecs else 1


if __name__ == "__main__":
    with contextlib.redirect_stdout(io.StringIO()) if False else contextlib.nullcontext():
        raise SystemExit(main())
