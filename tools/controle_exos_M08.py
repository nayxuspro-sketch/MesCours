#!/usr/bin/env python3
"""Auto-validation des 15 exercices de l'évaluation M08 (épreuve C).

Chaque exercice est un court bloc pandas exécuté sur le dossier du module
(`03_exercices/dossier_M08/`, les 8 CSV) et comparé à une valeur attendue
mesurée sur le socle (jamais déduite ; clés `m08_*` / `m08p_*` dans
`data/reference/chiffres_cites.json`). Le contrôleur rapporte chaque valeur
obtenue + le bilan.

Usage : python3 tools/controle_exos_M08.py
Sortie : une ligne par exercice (✔/✘ + valeur obtenue) + bilan.
"""
import pathlib

import pandas as pd

RACINE = pathlib.Path(__file__).resolve().parents[1]
DOSSIER = RACINE / "03_exercices" / "dossier_M08"

# (id, libellé, code, valeur attendue, tolérance absolue)
# Chaque code se termine par l'affectation `result = ...`
EXOS = [
    ("E01", "Nombre de ventes (lignes de vente.csv)",
     'result = len(v)', 50008, 0.5),
    ("E02", "CA brut total en centimes (FCFA)",
     'result = int((v["montant_ttc"] * 100).round().astype("int64").sum()) // 100',
     7908259732, 0.5),
    ("E03", "Ventes uniques (dedoublonnage 12 colonnes métier)",
     'result = v.drop_duplicates(subset=[c for c in v.columns if c != "id_vente"]).shape[0]',
     50000, 0.5),
    ("E04", "Retours en brut (est_retour = True)",
     'result = int(v["est_retour"].sum())', 208, 0.5),
    ("E05", "CA propre en centimes, retours exclus (FCFA)",
     'result = int((v[~v["est_retour"]]["montant_ttc"] * 100).round().astype("int64").sum()) // 100',
     7876320164, 0.5),
    ("E06", "Panier moyen, arrondi (FCFA)",
     'result = round(int((v["montant_ttc"] * 100).round().astype("int64").sum()) // 100 / len(v))',
     158140, 0.5),
    ("E07", "CA du top magasin (centimes, FCFA)",
     'result = int(((v["montant_ttc"] * 100).round().astype("int64"))'
     '.groupby(v["id_magasin"]).sum().max()) // 100',
     1596813264, 0.5),
    ("E08", "Ventes un dimanche (dayofweek == 6)",
     'result = int((pd.to_datetime(v["date_vente"]).dt.dayofweek == 6).sum())',
     7136, 0.5),
    ("E09", "Forme du merge avec objectif_magasin (tuple lignes × colonnes)",
     'result = v.merge(o, on="id_magasin", how="left").shape', (50008, 16), None),
    ("E10", "Cellules NaN de ca_objectif_ttc après le merge",
     'result = int(v.merge(o, on="id_magasin", how="left")["ca_objectif_ttc"].isna().sum())',
     50008, 0.5),
    ("E11", "Lignes de la vue mensuelle (sans retours, magasin × annee-mois)",
     'p = v[~v["est_retour"]]\n'
     'p = p.assign(mois=pd.to_datetime(p["date_vente"]).dt.to_period("M").astype(str))\n'
     'result = p.groupby(["id_magasin", "mois"]).ngroups', 120, 0.5),
    ("E12", "Plus gros mois de la vue (centimes, FCFA)",
     'p = v[~v["est_retour"]]\n'
     'p = p.assign(mois=pd.to_datetime(p["date_vente"]).dt.to_period("M").astype(str))\n'
     'ct = (p["montant_ttc"] * 100).round().astype("int64")\n'
     'result = int(ct.groupby([p["id_magasin"], p["mois"]]).sum().max()) // 100',
     78965529, 0.5),
    ("E13", "Ventes de 2025",
     'result = int(v["date_vente"].str.startswith("2025").sum())', 24920, 0.5),
    ("E14", "Ventes de 2026",
     'result = int(v["date_vente"].str.startswith("2026").sum())', 25088, 0.5),
    ("E15", "Ventes de 100 000 FCFA et plus (gros montants)",
     'result = int((v["montant_ttc"] > 100000).sum())', 28065, 0.5),
]


def main():
    v = pd.read_csv(DOSSIER / "vente.csv")
    o = pd.read_csv(DOSSIER / "objectif_magasin.csv")
    ok, ko = 0, 0
    for eid, lib, code, attendu, tol in EXOS:
        ns = {"v": v, "o": o, "pd": pd}
        try:
            exec(compile(code, "<exo " + eid + ">", "exec"), ns)
            obtenu = ns.get("result")
        except Exception as e:  # un exo qui lève une erreur est raté, pas le contrôleur
            obtenu = f"ERREUR {type(e).__name__}: {e}"
        if isinstance(attendu, tuple):
            bon = obtenu == attendu
        else:
            bon = proche(obtenu, attendu, tol)
        marque = "✔" if bon else "✘"
        if bon:
            ok += 1
        else:
            ko += 1
            marque += f" (attendu {attendu})"
        print(f"{marque} {eid} {lib} : {obtenu}")
    print(f"Bilan : {ok}/{len(EXOS)} réponses conformes" + (f" · {ko} à revoir" if ko else " · tout est vert"))
    return 0 if ko == 0 else 1


def proche(obtenu, attendu, tol):
    try:
        return abs(float(obtenu) - float(attendu)) <= tol
    except (TypeError, ValueError):
        return False


if __name__ == "__main__":
    raise SystemExit(main())
