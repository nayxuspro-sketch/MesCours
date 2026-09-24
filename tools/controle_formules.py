#!/usr/bin/env python3
"""controle_formules.py — Q3 de la porte §G.1, côté tableur.

Le module M03 enseigne Excel, qui ne s'exécute pas ici. Ce contrôleur fait le maximum
de ce qui est faisable : il **recalcule le classeur d'atelier** avec la bibliothèque
`formulas` (implémentation indépendante de la sémantique des fonctions Excel) et
confronte chaque valeur obtenue (a) à la valeur attendue écrite dans le classeur par
le générateur, qui la tient de `chiffres_cites.json`, et (b) à un calcul pandas fait
ici, sans lire le classeur. Un désaccord entre les trois moyens de calcul est une
erreur du manuel, pas de l'outil.

Usage :
    python3 tools/controle_formules.py            # M03 complet
    python3 tools/controle_formules.py --rapport  # détail ligne à ligne
"""
import argparse, datetime as dt, json, os, re, sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REF = os.path.join(ROOT, "01_socle_donnees", "data", "reference")
CLASSEUR = os.path.join(ROOT, "01_socle_donnees", "data", "projection", "m03_classeur_atelier.xlsx")
PIEGES = {"RECHERCHEV"}          # lignes volontairement en erreur, documentées comme telles

# Lignes de « Calculs » qui comptent ou somment la feuille de preuve. `formulas` convertit le texte
# numérique (« 1234 » stocké en chaîne) là où Excel et LibreOffice ne le convertissent pas : NB y rend
# 3 avec `formulas` et 0 dans Excel. C'est toute la leçon de C02 §5.1, donc le contrôleur ne doit pas
# se fier au moteur pour ces deux lignes : il relit les types réellement stockés dans le fichier.
FEUILLE_PREUVE = {"NB appliqué aux montants reçus": "compte",
                  "SOMME sur la feuille reçue": "somme"}
NUM = (int, float, np.integer, np.floating)


def valeur(sol, feuille, ref):
    """Le dictionnaire de `formulas` clé par cellule, au format "'[fichier]FEUILLE'!REF"
    — le nom de fichier garde sa casse d'origine, la feuille et la référence sont en capitales."""
    cible = "'[%s]%s'!%s" % (os.path.basename(CLASSEUR), feuille.upper(), ref.upper())
    for k, v in sol.items():
        if k == cible or k.replace("'", "").upper() == cible.replace("'", "").upper():
            try:
                return v.value[0, 0]
            except Exception:
                return getattr(v, "value", v)
    return None


def pareil(a, b, tol=0.51):
    if isinstance(a, NUM) and isinstance(b, NUM):
        return abs(float(a) - float(b)) <= tol
    return str(a).strip() == str(b).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapport", action="store_true")
    a = ap.parse_args()
    import warnings
    import formulas
    from openpyxl import load_workbook

    K = json.load(open(os.path.join(REF, "chiffres_cites.json"), encoding="utf-8"))["M03"]
    wb = load_workbook(CLASSEUR)
    t0 = __import__("time").time()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sol = formulas.ExcelModel().loads(CLASSEUR).finish().calculate()
    print("classeur recalculé en %.1f s" % (__import__("time").time() - t0))

    ok = ko = 0
    ecarts = []

    # ---------------------------------------------------------------- 1. feuille Calculs, auto-contrôle
    ws = wb["Calculs"]
    print("\n— Calculs : la valeur rendue par la formule contre la valeur attendue —")
    for r in range(2, ws.max_row + 1):
        nom = ws.cell(r, 2).value or ""
        att = ws.cell(r, 4).value
        obt = valeur(sol, "Calculs", "E%d" % r)
        if att is None and obt is None:
            continue
        if str(nom).strip() in FEUILLE_PREUVE:
            ce_qu = FEUILLE_PREUVE[str(nom).strip()]
            vue = wb["ventes_brutes"]
            numeriques = [vue.cell(r_, 13).value for r_ in range(2, vue.max_row + 1)
                          if isinstance(vue.cell(r_, 13).value, NUM)]
            vu = len(numeriques) if ce_qu == "compte" else sum(numeriques)
            bon = pareil(att, vu)
            ok, ko = ok + bon, ko + (not bon)
            note = "le moteur `formulas` rend %r, les types du fichier rendent %r — Excel et LibreOffice " \
                   "suivent le fichier" % (obt, vu)
            if a.rapport or not bon:
                print("  %-44s %s  attendu %r · types du fichier %r  (%s)"
                      % (nom[:44], "✔" if bon else "✘", att, vu, note))
            if not bon:
                ecarts.append((f"Calculs!E{r}", nom, att, vu))
            continue
        if any(p in str(nom).upper() for p in PIEGES):
            bon = isinstance(obt, str) and obt.startswith("#N/A")
            etat = "✔ (piège reproduit)" if bon else "✘ (piège non reproduit)"
            ok, ko = ok + bon, ko + (not bon)
            print("  %-44s %s  → %r" % (nom[:44], etat, obt))
            continue
        if isinstance(obt, str) and obt.startswith("#"):
            ko += 1
            ecarts.append((f"Calculs!E{r}", nom, att, obt))
            print("  %-44s ✘ erreur %s (attendu %r)" % (nom[:44], obt, att))
            continue
        # les pourcentages stockés en fraction se comparent avec une tolérance relative
        tol = 5e-4 if isinstance(att, NUM) and abs(float(att)) < 1 else 0.51
        bon = pareil(att, obt, tol)
        ok, ko = ok + bon, ko + (not bon)
        if a.rapport or not bon:
            print("  %-44s %s  attendu %r · rendu %r" % (nom[:44], "✔" if bon else "✘", att, obt))
        if not bon:
            ecarts.append((f"Calculs!E{r}", nom, att, obt))

    # ---------------------------------------------------------------- 2. TCD, contre pandas
    print("\n— TCD : le tableau croisé reconstitué par COUNTIFS/SUMIFS contre le calcul pandas —")
    p = pd.read_csv(os.path.join(REF, "ventes_magasin5_2025_ATTENDU.csv"), sep=";")
    ca_total = float(p["montant_ttc"].sum())
    ws = wb["TCD"]
    for r in range(2, ws.max_row + 1):
        cat = ws.cell(r, 1).value
        if not cat or cat == "Total" or valeur(sol, "TCD", "B%d" % r) is None:
            continue
        g = p[p["categorie"] == cat]
        attendu = [len(g), float(g["montant_ttc"].sum()), float(g["montant_ttc"].mean()),
                   float(g["montant_ttc"].sum()) / ca_total, int((g["remise"] > 0).sum())]
        rendu = [valeur(sol, "TCD", f"{c}{r}") for c in "BCDEF"]
        bons = [pareil(x, y, 5e-4 if i == 3 else 0.51) for i, (x, y) in enumerate(zip(attendu, rendu))]
        ok, ko = ok + sum(bons), ko + (5 - sum(bons))
        marque = "✔" if all(bons) else "✘"
        print("  %-16s %s  lignes %s · CA %s · part %s" % (
            cat, marque, rendu[0],
            f"{float(rendu[1]):,.0f}".replace(",", "\u202f") if isinstance(rendu[1], NUM) else rendu[1],
            f"{100*float(rendu[3]):.1f} %" if isinstance(rendu[3], NUM) else rendu[3]))
        if not all(bons):
            ecarts.append((f"TCD!B{r}:F{r}", cat, attendu, rendu))

    # ---------------------------------------------------------------- 3. Mensuel, contre pandas
    print("\n— Mensuel : CA et effectifs par mois, objectif, jours ouvrés —")
    obj = pd.read_csv(os.path.join(ROOT, "01_socle_donnees", "data", "brut", "objectifs_de_ca.csv"),
                      sep=";", encoding="cp1252")
    obj.columns = [c.strip() for c in obj.columns]
    d5 = obj[(obj["id_magasin"].astype(str) == "5") & (obj["annee"].astype(str) == "2025")]
    dates = pd.to_datetime(p["date"])
    ws = wb["Mensuel"]
    for i in range(1, 13):
        r = 1 + i
        sel = dates.dt.month == i
        m01 = dt.date(2025, i, 1)
        m1 = dt.date(2025, i + 1, 1) if i < 12 else dt.date(2026, 1, 1)
        objectif = float(pd.to_numeric(d5[d5["mois"].astype(str) == str(i)]["ca_objectif_ttc"], errors="coerce").sum())
        attendu = [float(p.loc[sel, "montant_ttc"].sum()), int(sel.sum()), objectif,
                   (float(p.loc[sel, "montant_ttc"].sum()) / objectif) if objectif else "objectif absent",
                   int(np.busday_count(m01, m1))]
        rendu = [valeur(sol, "Mensuel", f"{c}{r}") for c in "BCDEF"]
        if objectif == 0:
            attendu[4] = "objectif absent"
        bons = [pareil(x, y, 5e-4 if i == 4 else 0.51) if not isinstance(x, str) else str(x) == str(y).strip()
                for i, (x, y) in enumerate(zip(attendu, rendu))]
        ok, ko = ok + sum(bons), ko + (5 - sum(bons))
        print("  mois %2d  %s  CA %s · lignes %s · objectif %s · ratio %s" % (
            i, "✔" if all(bons) else "✘",
            f"{float(rendu[0]):,.0f}".replace(",", "\u202f") if isinstance(rendu[0], NUM) else rendu[0],
            rendu[1],
            f"{float(rendu[2]):,.0f}".replace(",", "\u202f") if isinstance(rendu[2], NUM) else rendu[2],
            f"{100*float(rendu[3]):.1f} %" if isinstance(rendu[3], NUM) else rendu[3]))
        if not all(bons):
            ecarts.append((f"Mensuel!B{r}:F{r}", i, attendu, rendu))

    # ---------------------------------------------------------------- 4. filets
    print("\n— Aucune cellule de contrôle ne doit être une erreur —")
    erreurs = []
    for feuille, zone in (("Calculs", "E2:E%d" % wb["Calculs"].max_row), ("TCD", "B2:F20"), ("Mensuel", "B2:F15")):
        for row in wb[feuille][zone]:
            for c in row:
                if c.data_type == "f":
                    v = valeur(sol, feuille, c.coordinate)
                    if isinstance(v, str) and v.startswith("#") and not any(
                            pi in str(wb["Calculs"].cell(c.row, 2).value or "").upper() for pi in PIEGES):
                        erreurs.append((feuille, c.coordinate, v))
    if erreurs:
        for e in erreurs[:10]:
            print("   ✘", e)
        ko += len(erreurs)
    else:
        print("   ✔ aucune #NAME?, #VALUE!, #REF! non documentée")

    print("\nTotal : %d contrôles conformes, %d écarts" % (ok, ko))
    if ecarts:
        print("\nDétail des écarts :")
        for f, nom, att, obt in ecarts[:20]:
            print("  %s %s\n      attendu %s\n      rendu   %s" % (f, nom, att, obt))
    return 1 if ko else 0


if __name__ == "__main__":
    sys.exit(main())
