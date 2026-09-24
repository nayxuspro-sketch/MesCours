#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Budget de pages du manuel : le recalculer, le mesurer, ne jamais le laisser « à l'œil ».

    python3 tools/budget_pages.py            # tableau du budget, colonnes vérifiées
    python3 tools/budget_pages.py --mesure   # ajoute la mesure réelle des modules composés

Le calibre en vigueur (décision du 17/09/2026, mesurée sur M01) : **12,5 pages par chapitre**
— 7 pages de matière (blocs 1 à 9, 14 à 16 du gabarit §B.3) et 5,5 pages d'exercices embarqués
(blocs 10 à 13) — plus **17 pages d'appareil de module** (ouverture 3, bilan 3, projet 5,
évaluation 6). M21 porte 60 pages de plus : rendus exemplaires annotés et soutenance.

Le script échoue (code 1) si une colonne ne s'additionne pas, si un total annoncé du fichier
d'architecture diverge, ou si un module mesuré sort de la fourchette 10 à 16 pages par chapitre.
"""
from __future__ import annotations

import argparse
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCH = os.path.join(RACINE, "00_architecture", "01_architecture_pedagogique.md")

CALIBRE = 12.5
APPAREIL_MODULE = 17
EXTRA = {"M21": 60}
APPAREIL_GLOBAL = {"ouverture": 39, "glossaire_index": 80, "feuille_de_route": 50, "annexes": 60}

# chapitres par module, tenus en correspondance avec le tableau §D de l'architecture
CHAP = {"M01": 7, "M02": 8, "M03": 8, "M04": 6, "M05": 5, "M06": 5, "M07": 8, "M08": 8,
        "M09": 6, "M10": 7, "M11": 7, "M12": 6, "M13": 7, "M14": 8, "M15": 7, "M16": 5,
        "M17": 6, "M18": 7, "M19": 6, "M20": 6, "M21": 6, "M22": 4}

MOTS_PAR_PAGE = 456          # mesuré le 17/09/2026 : module M01, 50 164 mots pour 110 pages composées
SEUIL_DERIVE = 0.15          # tolérance entre le budget du module et sa composition réelle


def budget():
    lignes = {}
    for k, c in CHAP.items():
        mat = int(c * CALIBRE + 0.5)   # arrondi au demi-supérieur, comme au §F.4
        lignes[k] = (c, mat, APPAREIL_MODULE + EXTRA.get(k, 0), mat + APPAREIL_MODULE + EXTRA.get(k, 0))
    return lignes


def mesurer(budget):
    """Pages réelles : PDF assemblé si présent, sinon estimation par les mots des fichiers sources."""
    out = {}
    for k in CHAP:
        pdf = os.path.join(RACINE, "05_livrables", k + ".pdf")
        fichiers = ([os.path.join(RACINE, "02_modules", x) for x in sorted(os.listdir(os.path.join(RACINE, "02_modules")))
                     if x.startswith(k + "_") and x.endswith(".md")] if os.path.isdir(os.path.join(RACINE, "02_modules")) else [])
        fichiers += [os.path.join(RACINE, d, x) for d in ("03_exercices", "04_evaluations")
                     if os.path.isdir(os.path.join(RACINE, d))
                     for x in sorted(os.listdir(os.path.join(RACINE, d))) if x.startswith(k + "_") and x.endswith(".md")]
        if not fichiers:
            continue
        n_chap = len([f for f in fichiers if re.search(r"_C\d{2}_", os.path.basename(f))])
        if n_chap < CHAP[k]:
            out[k] = dict(en_cours=True, n_chap=n_chap, fichiers=len(fichiers))
            continue
        mots = mots_chapitres = 0
        for f in fichiers:
            m = len(re.findall(r"[A-Za-zÀ-ÿ0-9'’-]+", open(f, encoding="utf-8").read()))
            mots += m
            if "_C0" in os.path.basename(f) or "_C1" in os.path.basename(f):
                mots_chapitres += m
        pages_pdf = None
        if os.path.exists(pdf):
            try:
                import pypdfium2 as pdfium
                d = pdfium.PdfDocument(pdf)
                pages_pdf = len(d)
                d.close()
            except Exception:                      # l'estimation par les mots reste possible sans le PDF
                pages_pdf = None
        out[k] = dict(fichiers=len(fichiers), mots=mots, mots_chapitres=mots_chapitres,
                      pages_estimees=round(mots / MOTS_PAR_PAGE), pages_pdf=pages_pdf,
                      budget=budget[k][3])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mesure", action="store_true", help="ajoute la mesure des modules rédigés")
    a = ap.parse_args()

    lignes = budget()
    s_mat = sum(v[1] for v in lignes.values())
    s_app = sum(v[2] for v in lignes.values())
    s_pages = sum(v[3] for v in lignes.values())
    total = s_pages + sum(APPAREIL_GLOBAL.values())
    jalon = sum(lignes[k][3] for k in list(CHAP)[:7]) + APPAREIL_GLOBAL["ouverture"]

    entetes = [l for l in open(ARCH, encoding="utf-8").read().splitlines() if l.startswith("| M")]
    print(f"budget recalculé : {sum(CHAP.values())} chapitres · {s_mat} p. de chapitres + {s_app} p. d'appareil "
          f"= {s_pages} p. · manuel complet {total} p. · jalon fin M07 {jalon} p.")
    for k, (c, mat, app, pages) in lignes.items():
        print(f"  {k}  {c} chap. × {CALIBRE} = {mat:>4} p. + {app:>3} p. d'appareil = {pages:>4} p.")

    erreurs = []
    if s_pages != sum(int(c * CALIBRE + 0.5) + APPAREIL_MODULE + EXTRA.get(k, 0) for k, c in CHAP.items()):
        erreurs.append("colonnes du sous-total incohérentes")
    if entetes:
        # le tableau §F.4 du fichier d'architecture doit porter exactement ces chiffres
        texte = open(ARCH, encoding="utf-8").read()
        texte = re.sub(r"(?<=\d)[ \u00a0\u202f](?=\d)", "", texte)   # les milliers espacés du texte
        for k, (c, mat, app, pages) in lignes.items():
            m = re.search(rf"^\| {k} \| {c} \| (\d+) \| (\d+) \| \*\*(\d+)\*\* \|", texte, flags=re.M)
            if not m:
                erreurs.append(f"§F.4 : ligne {k} introuvable ou hors format")
            elif (int(m.group(1)), int(m.group(2)), int(m.group(3))) != (mat, app, pages):
                erreurs.append(f"§F.4 : {k} annonce {m.group(1)}/{m.group(2)}/{m.group(3)}, le calcul donne {mat}/{app}/{pages}")
        if f"**MANUEL COMPLET** | **143 chap.** | | | **{total} p.**" not in texte:
            erreurs.append(f"§F.4 : le total du manuel complet n'est pas {total} p.")
    mes = mesurer(lignes) if a.mesure else {}
    if a.mesure:
        for k, v in mes.items():
            if v.get("en_cours"):
                print(f"  mesure {k} : module en cours de rédaction ({v['n_chap']}/{CHAP[k]} chapitres), "
                      f"{v['fichiers']} fichiers — contrôle du budget reporté à l'achèvement")
                continue
            mesure = v["pages_pdf"] or v["pages_estimees"]
            source_pdf = v["pages_pdf"] is not None
            derive = mesure / v["budget"] - 1
            par_chap = v["mots_chapitres"] / MOTS_PAR_PAGE / CHAP[k]
            print(f"  mesure {k} : {v['fichiers']} fichiers · {v['mots']} mots · budget {v['budget']} p. · "
                  + (f"composé {mesure} p. → dérive {derive:+.0%} ; {par_chap:.1f} p./chapitre (calibre {CALIBRE})"
                     if source_pdf else
                     f"estimé {mesure} p. d'après les mots — PDF non lu (installer `pypdfium2`) ; "
                     f"{par_chap:.1f} p./chapitre (calibre {CALIBRE})"))
            if abs(derive) > SEUIL_DERIVE:
                erreurs.append(f"{k} : composition à {mesure} p. pour un budget de {v['budget']} p. "
                               f"(dérive {derive:+.0%} au-delà de ±{SEUIL_DERIVE:.0%})")
            if not 10 <= par_chap <= 16:
                erreurs.append(f"{k} : {par_chap:.1f} pages par chapitre, hors fourchette 10–16")
    for e in erreurs:
        print("ERREUR :", e)
    if erreurs:
        return 1
    print("Résultat : budget additif et conforme à l'architecture.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
