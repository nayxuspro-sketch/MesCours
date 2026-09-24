#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle qualité automatique d'un module rédigé.

Il vérifie ce que l'œil ne voit plus après trois relectures : la structure du gabarit,
l'origine de chaque chiffre cité, l'existence des figures et des fichiers cités, la présence
des corrigés, la cohérence arithmétique des énoncés.

    python3 01_socle_donnees/scripts/autovalide.py M01
    python3 01_socle_donnees/scripts/autovalide.py M01 --strict     # les avertissements comptent comme erreurs

Contrôles implémentés (les règles de production du README sont opposables) :
  R1  chaque chapitre contient les 16 blocs du gabarit, dans l'ordre
  R2  tout nombre de 4 chiffres ou plus cité dans un module existe dans chiffres_cites.json,
      dans les stats de génération, ou est un nombre de pages/lignes/colonnes vérifié sur disque
  R3  les figures .svg citées existent
  R4  les chemins de fichiers cités (`01_socle_donnees/...`) existent
  R5  chaque énoncé d'exercice a son corrigé (titre repris dans le bloc « Correction détaillée »)
  R6  le total des barèmes annoncés est cohérent (pts annoncés = somme des lignes du tableau)
  R7  aucun texte non-français parasite, aucun mot répété, aucun anglicisme sans son couple
      « français — English »
  R8  la fréquence des six encadrés pédagogiques respecte le §B.4 de l'architecture
      (4 à 8 « Définition », 2 à 4 « À retenir », 2 à 5 « Attention », 1 à 3 « Conseil
      professionnel », 1 à 2 « Dans les faits », 1 « Boîte à outils » par section-outil)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MOD = os.path.join(RACINE, "02_modules")
EXOS = os.path.join(RACINE, "03_exercices")
EVAL = os.path.join(RACINE, "04_evaluations")
DATA = os.path.join(RACINE, "01_socle_donnees", "data")
REF = os.path.join(DATA, "reference")

BLOCS = [
    "Objectifs du chapitre", "Pourquoi cette notion est importante", "Explication simple",
    "Vocabulaire essentiel", "Cours approfondi", "Exemple concret", "Démonstration pas à pas",
    "Erreurs fréquentes", "Bonnes pratiques professionnelles", "Exercice guidé", "Exercices autonomes",
    "Correction détaillée", "Mini-projet", "Résumé du chapitre", "À retenir", "Évaluation formative",
]

# Nombres structurels acceptés hors chiffres_cites : pages, lignes de code, années, identifiants courts
IGNORE_NOMBRES = set("""2023 2024 2025 2026 1934 1935 143 660 620 229 1705 1001 338 366 525 710 20260917 8601 1252
20250101 20250913 20251201 8859 18 480 489 13 316 316""".split())


def charger_source_chiffres():
    """Tous les nombres produits par le socle : ils sont seuls recevables dans un chapitre."""
    ch = json.load(open(os.path.join(REF, "chiffres_cites.json"), encoding="utf-8"))
    st = json.load(open(os.path.join(REF, "stats_generation.json"), encoding="utf-8"))
    valides = set()

    def ramasser(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if isinstance(k, str):
                    for n in re.findall(r"\d+", k.replace("_", " ")):
                        valides.add(n)
                ramasser(v)
        elif isinstance(x, (list, tuple)):
            for v in x:
                ramasser(v)
        elif isinstance(x, bool):
            pass
        elif isinstance(x, (int, float)):
            s = f"{int(x):,}".replace(",", " ")
            valides.add(str(int(x)))
            valides.add(s)
            if isinstance(x, float):
                valides.add(str(x).replace(".", ","))
        elif isinstance(x, str):
            for n in re.findall(r"\d[\d ]*", x):
                valides.add(n.strip().replace(" ", ""))
                for sub in re.findall(r"\d+", n):
                    valides.add(sub)

    ramasser(ch)
    ramasser(st)
    # nombres réellement présents dans les petits fichiers du socle (un prix, une quantité, un identifiant)
    for sous in ("brut", "reference", "projection"):
        d = os.path.join(DATA, sous)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".csv") and os.path.getsize(os.path.join(d, f)) < 3_000_000:
                with open(os.path.join(d, f), encoding="utf-8-sig", errors="replace") as fh:
                    for ligne in fh:
                        for n in re.findall(r"\d+", ligne):
                            valides.add(n.lstrip("0") or "0")
                            valides.add(n)
            if f.endswith((".json", ".md", ".txt")) and os.path.getsize(os.path.join(d, f)) < 300_000:
                with open(os.path.join(d, f), encoding="utf-8", errors="replace") as fh:
                    for n in re.findall(r"\d[\d ]*", fh.read()):
                        for sub in re.findall(r"\d+", n):
                            valides.add(sub)
    # volumes réels des fichiers livrés (contrôle R2 de second niveau)
    for sous in ("brut", "reference", "projection"):
        d = os.path.join(DATA, sous)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if not f.endswith((".csv", ".xlsx", ".md", ".json", ".txt")):
                continue
            p = os.path.join(d, f)
            if f.endswith(".csv") and os.path.getsize(p) < 60_000_000:
                with open(p, encoding="utf-8-sig", errors="replace") as fh:
                    n = sum(1 for _ in fh)
                valides.add(str(n))
                valides.add(str(n - 1))
                entete = fh = None
                with open(p, encoding="utf-8-sig", errors="replace") as fh:
                    l0 = fh.readline().rstrip("\n")
                for sep in (";", ",", "\t"):
                    if sep in l0:
                        valides.add(str(len(l0.split(sep))))
                        break
            valides.add(str(round(os.path.getsize(p) / 1e6, 1)))
            valides.add(str(round(os.path.getsize(p) / 1e6)))
    return valides


ANNEES = {str(a) for a in range(1900, 2130)}


def derives(valides):
    """Additions, soustractions et multiples simples des nombres du socle : un calcul de cours est licite."""
    noms = sorted({int(v) for v in valides if v.isdigit() and 1000 <= int(v) <= 10 ** 11})
    out = set(noms)
    petits = noms[:400]
    for a in petits:
        for k in range(2, 6):
            out.add(str(a * k))
        for b in petits:
            out.add(str(a + b))
            out.add(str(abs(a - b)))
    return out


def nombres_cites(txt):
    """Nombres « de résultat » : au moins 3 chiffres, ou un nombre suivi d'unité, ou un %."""
    out = []
    propre = re.sub(r"```.*?```", "", txt, flags=re.S)        # code exclu
    propre = re.sub(r"`[^`]*`", "", propre)                     # citations inline exclues
    propre = re.sub(r"^\s*\|.*$", "", propre, flags=re.M)       # tableaux : contrôlés à part
    for m in re.finditer(r"(?<![\d.])\d[\d ]{2,}(?:[,.]\d+)?", propre):
        s = m.group(0).strip()
        if re.fullmatch(r"\d[\d ]*", s):
            net = s.replace(" ", "")
            if len(net) >= 4:
                out.append(net)
    return out


def blocs_manquants(txt):
    vus, pos = [], -1
    for b in BLOCS:
        m = re.search(rf"^#{{2,3}}\s+\d+\.\s*{re.escape(b)}", txt, flags=re.M)
        if not m:
            yield f"bloc absent : « {b} »"
        else:
            if m.start() < pos:
                yield f"bloc hors ordre : « {b} »"
            pos = m.start()
            vus.append(b)


JARGON = ("dataframe", "pipeline", "dashboard", "dataset", "KPI", "self-service", "gouvernance de la donn")


def _tableau_bareme(bloc):
    """Renvoie (total_declare, somme_des_lignes) si le bloc est un barème, sinon None."""
    lignes = [l for l in bloc.strip().split("\n") if l.strip().startswith("|")]
    if len(lignes) < 3:
        return None
    entete = [c.strip(" *") for c in lignes[0].strip().strip("|").split("|")]
    col = next((k for k, c in enumerate(entete) if re.search(r"points|pts|bar\w*m", c, re.I)), None)
    if col is None:
        return None
    total, somme = None, 0.0
    for l in lignes[2:]:
        cel = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cel) <= col:
            return None
        m = re.fullmatch(r"[^|]*?(\d+(?:[.,]\d+)?)\s*(?:points?|pts)?[^|]*", " ".join([cel[col]]))
        if not m:
            continue
        val = float(m.group(1).replace(",", "."))
        if re.match(r"^(?:\*\*)?total", cel[0], re.I):
            total = val
        else:
            somme += val
    if total is None:
        return None
    return total, round(somme, 4)


def _eval_expr(s):
    """Évalue une suite de nombres reliés par + − × (les milliers espacés et la virgule décimale sont admis)."""
    s = re.sub(r"[\u00a0\u202f ]", "", s).replace(",", ".").replace("\u2212", "-").replace("\u00d7", "*").replace("x", "*")
    if not re.fullmatch(r"[\d.*+-]+", s):
        return None
    total, signe, i = 0.0, 1.0, 0
    while i < len(s):
        if s[i] == "+":
            signe, i = 1.0, i + 1
            continue
        if s[i] == "-":
            signe, i = -1.0, i + 1
            continue
        m = re.match(r"[\d.]+(?:\*[\d.]+)*", s[i:])
        if not m:
            return None
        val = 1.0
        for morceau in m.group(0).split("*"):
            if not re.fullmatch(r"\d*\.?\d+", morceau or "0"):
                return None
            val *= float(morceau or 0)
        total += signe * val
        i += len(m.group(0))
    return total


EQUATION = re.compile(r"((?:\d[\d \u00a0\u202f]{0,15}\s*[+\-\u00d7\u2212*x]\s*)+\d[\d \u00a0\u202f]{0,15})\s*=\s*(\d[\d \u00a0\u202f]{0,15})")


def _eqs_verifier(txt, nom):
    """Toute égalité arithmétique écrite dans le manuel doit être juste : le lecteur, lui, calcule."""
    out = []
    for m in EQUATION.finditer(txt):
        g = _eval_expr(m.group(1))
        d = _eval_expr(m.group(2))
        if g is None or d is None:
            continue
        if abs(g - d) > max(0.01, abs(d) * 0.001):
            out.append(f"{nom} : égalité fausse — « {m.group(0).strip()} » (le calcul donne {g:g})")
    return out


# Nombres d'exemple qui décrivent l'outil, non le jeu de données (numéro de série d'une date dans un tableur)
HORS_SOCLE = {"45669", "45670", "44927", "45292", "45264"}


def controler(module: str, strict: bool = False):
    erreurs, avertis = [], []
    fichiers = sorted(f for f in os.listdir(MOD) if f.startswith(module + "_") and f.endswith(".md")) if os.path.isdir(MOD) else []
    if not fichiers:
        return [f"aucun fichier de module trouvé pour {module} dans {MOD}"], avertis, []
    valides = charger_source_chiffres()
    DERIVES = derives(valides)
    GLOSSAIRE = "\n".join(open(os.path.join(MOD, f), encoding="utf-8").read() for f in fichiers)
    chiffres_md = os.path.join(REF, "chiffres_cites.md")
    if not os.path.exists(chiffres_md):
        erreurs.append("chiffres_cites.md absent : exécuter scripts/chiffres_manuel.py avant de rédiger")

    # périmètre contrôlé : chapitres + projet de module + évaluation (mêmes règles d'arithmétique et de sourçage)
    chemins = [os.path.join(MOD, f) for f in fichiers]
    for dossier in (EXOS, EVAL):
        if os.path.isdir(dossier):
            chemins += [os.path.join(dossier, f) for f in sorted(os.listdir(dossier))
                        if f.startswith(module + "_") and f.endswith(".md")]

    for p in chemins:
        f = os.path.basename(p)
        txt = open(p, encoding="utf-8").read()
        est_chapitre = p.startswith(MOD + os.sep) and re.match(rf"{module}_C\d{{2}}_", f) and "_C00_" not in f
        # R1 : gabarit (16 blocs, dans l'ordre)
        if est_chapitre:
            for msg in blocs_manquants(txt):
                erreurs.append(f"{f} : {msg}")
        # R2 : origine des nombres cités
        scenario = set()
        for num in (10, 11):
            m = re.search(rf"^#{{2,3}}\s+{num}\.[^\n]*\n(.*?)(?=^#{{2,3}}\s+\d+\.)", txt, flags=re.M | re.S)
            if m:
                scenario |= set(re.findall(r"\d+", m.group(1)))
        for n in sorted(set(nombres_cites(txt))):
            if (n in IGNORE_NOMBRES or n in valides or n in ANNEES or n in scenario
                    or n in DERIVES or n in HORS_SOCLE):
                continue
            avertis.append(f"{f} : nombre {n} introuvable dans les données du socle — à sourcer ou à retirer")
        # R3 : figures citées
        for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", txt):
            cible = os.path.normpath(os.path.join(os.path.dirname(p), m.group(1)))
            if not os.path.exists(cible):
                erreurs.append(f"{f} : figure absente {m.group(1)}")
        # R4 : chemins du socle cités en dur
        for m in re.finditer(r"`((?:0[1-9]_\w+/)?[\w./-]+\.(?:csv|xlsx|md|json|py|duckdb|sql|txt))`", txt):
            c = m.group(1)
            if c.startswith("01_socle_donnees"):
                cible = os.path.join(RACINE, c)
            elif c.startswith(("data/", "scripts/")):
                cible = os.path.join(RACINE, "01_socle_donnees", c)
            else:
                continue
            if not os.path.exists(cible):
                erreurs.append(f"{f} : fichier cité inexistant — {c}")
        # R5 : chaque énoncé d'exercice a sa reprise dans le corrigé
        bloc_corr = re.search(r"^#{2,3}\s+\d+\.\s*Correction détaillée(.*?)(?=^#{2,3}\s+\d+\.)", txt, flags=re.M | re.S)
        bloc_exos = re.search(r"^#{2,3}\s+\d+\.\s*Exercices autonomes(.*?)(?=^#{2,3}\s+\d+\.)", txt, flags=re.M | re.S)
        if bloc_exos:
            for e in re.findall(r"\*\*(Exercice\s+\d+\.\d+)", bloc_exos.group(1)):
                if bloc_corr is None or e not in bloc_corr.group(1):
                    erreurs.append(f"{f} : « {e} » n'a pas de reprise dans le corrigé")
        # R6 : arithmétique — total d'un barème et égalité écrites en clair
        for bloc in re.findall(r"(^\|.*\n\|[ -|:]+\n(?:^\|.*\n?)+)", txt, flags=re.M):
            res = _tableau_bareme(bloc)
            if res:
                total, somme = res
                if abs(total - somme) > 0.001:
                    erreurs.append(f"{f} : barème annoncé {total:g} pts, les lignes font {somme:g} pts")
        erreurs += _eqs_verifier(txt, f)
        # R7 : parasites et restes de rédaction
        for m in re.finditer(r"[，。、；：][^ ]|[一-鿿]", txt):
            erreurs.append(f"{f} : texte non français détecté — « {m.group(0)[:40]} »")
        for mot in ("TODO", "FIXME", "XXX", "lorem"):
            if mot.lower() in txt.lower():
                erreurs.append(f"{f} : reste « {mot} »")
        for m in re.finditer(r"\b(?!vous |nous |se |ce |cet |cette |me |te |le |la |les |on |il |elle )"
                             r"([A-Za-zÀ-ÿ]{3,})\s+\1\b", txt):
            erreurs.append(f"{f} : mot répété à la lecture — « {m.group(0)} »")
        # jargon : tout terme technique doit être apparié à son français quelque part dans le module
        for terme in JARGON:
            if not re.search(terme, txt, flags=re.I):
                continue
            if re.search(r"[A-Za-zàâçéèêëîïôûùüÿ'’-]{3,}[^|\n]{0,4}[—–][^|\n]{0,4}" + re.escape(terme), GLOSSAIRE, flags=re.I):
                continue
            m = re.search(terme, txt, flags=re.I)
            avertis.append(f"{f} : « {terme} » employé sans couple français — English (position {m.start()})")
        # R8 : fréquence des six encadrés pédagogiques (§B.4 de l'architecture)
        if est_chapitre:
            cibles = {"Définition": (4, 8), "À retenir": (2, 4), "Attention": (2, 5),
                      "Conseil professionnel": (1, 3), "Dans les faits": (1, 2)}
            for nom, (mini, maxi) in cibles.items():
                n = len(re.findall(r">\s*\*\*" + nom + r"\.", txt))
                if n < mini:
                    avertis.append(f"{f} : encadré « {nom} » ×{n} (< {mini} attendu par chapitre, §B.4)")
                elif n > maxi:
                    avertis.append(f"{f} : encadré « {nom} » ×{n} (> {maxi}, §B.4 : noyer le lecteur)")
            if re.search(r"^#{2,3}\s+[\d.]+\s*[^\n]*[Oo]util", txt, flags=re.M) and not re.search(r">\s*\*\*Boîte à outils\.", txt):
                avertis.append(f"{f} : sous-section « outil » sans encadré Boîte à outils (§B.4)")
        if strict:
            erreurs += [f"(strict) {a}" for a in avertis]
            avertis = []

    if strict:
        erreurs += [f"(strict) {a}" for a in avertis]
        avertis = []
    return erreurs, avertis, [os.path.basename(x) for x in chemins]


def main():
    ap = argparse.ArgumentParser(description="Contrôle qualité automatique d'un module rédigé.")
    ap.add_argument("module", nargs="?", default="M01", help="identifiant de module, ex. M01")
    ap.add_argument("--strict", action="store_true", help="les avertissements deviennent des erreurs")
    a = ap.parse_args()
    erreurs, avertis, fichiers = controler(a.module, a.strict)
    print(f"=== autovalidation {a.module} · {len(fichiers)} fichier(s) ===")
    for f in fichiers:
        print("  -", f)
    for e in erreurs:
        print("ERREUR     ", e)
    for w in avertis:
        print("avertissem.", w)
    nb_e, nb_a = len(erreurs), len(avertis)
    if nb_e or (a.strict and nb_a):
        print(f"Résultat : ÉCHEC ({nb_e} erreur(s), {nb_a} avertissement(s))")
        return 1
    print(f"Résultat : OK ({nb_a} avertissement(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
