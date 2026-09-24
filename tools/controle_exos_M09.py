#!/usr/bin/env python3
"""Auto-validation des 15 exercices de l'évaluation M09 (épreuve C).

Chaque exercice est un court bloc pandas exécuté sur le dossier du module
(`03_exercices/dossier_M09/`) et comparé à une valeur **mesurée** sur le socle
(jamais déduite des chapitres ; clés `m09p_*` / `m09v_*` dans
`data/reference/chiffres_cites.json`). Le contrôleur affiche, pour chaque
exercice, la valeur obtenue et le verdict.

Le dossier porte quatre jeux : quincaillerie (fil rouge), sante, scolaire,
projet (`fichier_inconnu.csv`). Les exercices E04 à E11 portent sur le
**variant 12 mois** du centre de santé (2025-07-01 → 2026-06-30), la fenêtre de
l'étude de cas de l'évaluation.

Usage : python3 tools/controle_exos_M09.py
Sortie : une ligne par exercice (✔/✘ + valeur obtenue) + bilan.
"""
import pathlib

import pandas as pd

RACINE = pathlib.Path(__file__).resolve().parents[1]
DOSSIER = RACINE / "03_exercices" / "dossier_M09"

# (id, libellé, code, valeur attendue, tolérance absolue)
# Le code s'appuie sur les DataFrames préparés dans main() et se termine par
# l'affectation `result = ...`.
EXOS = [
    ("E01", "Lignes de vente.csv (quincaillerie)",
     'result = len(v)', 50008, 0.5),
    ("E02", "Ventes distinctes (dédoublonnage 12 colonnes métier)",
     'result = v.drop_duplicates(subset=[c for c in v.columns if c != "id_vente"]).shape[0]',
     50000, 0.5),
    ("E03", "CA propre en centimes, retours exclus (FCFA)",
     'result = int((v[~v["est_retour"]]["montant_ttc"] * 100).round()'
     '.astype("int64").sum()) // 100', 7876320164, 0.5),
    ("E04", "Consultations du variant 12 mois (2025-07-01 → 2026-06-30)",
     'result = len(var)', 9450, 0.5),
    ("E05", "Jours distincts du variant",
     'result = var["date_consultation"].nunique()', 365, 0.5),
    ("E06", "Fréquentation moyenne par jour du variant (arrondie)",
     'result = round(len(var) / var["date_consultation"].nunique(), 2)', 25.89, 0.01),
    ("E07", "Pic mensuel du variant (consultations)",
     'result = int(var.groupby(var["date_consultation"].str[:7]).size().max())', 882, 0.5),
    ("E08", "Amplitude mensuelle du variant (pic - creux)",
     'p = var.groupby(var["date_consultation"].str[:7]).size()\n'
     'result = int(p.max() - p.min())', 204, 0.5),
    ("E09", "Moyenne mensuelle d'été du variant (juil.-sept., 1 décimale)",
     'p = var.groupby(var["date_consultation"].str[:7]).size()\n'
     'mois = pd.to_datetime(p.index).month\n'
     'result = round(float(p[mois.isin([7, 8, 9])].mean()), 1)', 857.3, 0.05),
    ("E10", "Écart-type des mois d'été du variant (2 décimales)",
     'p = var.groupby(var["date_consultation"].str[:7]).size()\n'
     'mois = pd.to_datetime(p.index).month\n'
     'result = round(float(p[mois.isin([7, 8, 9])].std()), 2)', 24.03, 0.01),
    ("E11", "Consultations du lundi (variant)",
     'result = int((pd.to_datetime(var["date_consultation"]).dt.dayofweek == 0).sum())',
     1899, 0.5),
    ("E12", "Consultations du dimanche (variant)",
     'result = int((pd.to_datetime(var["date_consultation"]).dt.dayofweek == 6).sum())',
     201, 0.5),
    ("E13", "Notes hors bornes (0 à 20) du jeu scolaire",
     'result = int(((no["note"] < 0) | (no["note"] > 20)).sum())', 6, 0.5),
    ("E14", "Doublons de tx_ref dans le fichier projet",
     'result = int(pj["tx_ref"].duplicated().sum())', 14, 0.5),
    ("E15", "Taux de succès du projet, après normalisation (%), 2 décimales",
     'd2 = pj.drop_duplicates(subset="tx_ref")\n'
     'OK = ["OK", "ok", "Reussie", "REUSSI"]\n'
     'result = round(100 * d2["statut"].isin(OK).mean(), 2)', 81.15, 0.01),
]


def proche(obtenu, attendu, tol):
    try:
        return abs(float(obtenu) - float(attendu)) <= tol
    except (TypeError, ValueError):
        return False


def main():
    v = pd.read_csv(DOSSIER / "quincaillerie" / "vente.csv")
    cons = pd.read_csv(DOSSIER / "sante" / "consultation.csv")
    var = cons[(cons["date_consultation"] >= "2025-07-01")
               & (cons["date_consultation"] <= "2026-06-30")]
    no = pd.read_csv(DOSSIER / "scolaire" / "note.csv")
    pj = pd.read_csv(DOSSIER / "projet" / "fichier_inconnu.csv")
    ok, ko = 0, 0
    for eid, lib, code, attendu, tol in EXOS:
        ns = {"v": v, "cons": cons, "var": var, "no": no, "pj": pj, "pd": pd}
        try:
            exec(compile(code, "<exo " + eid + ">", "exec"), ns)
            obtenu = ns.get("result")
        except Exception as e:                      # un exo qui lève est raté, pas le contrôleur
            obtenu = f"ERREUR {type(e).__name__}: {e}"
        bon = proche(obtenu, attendu, tol)
        marque = "✔" if bon else "✘"
        if bon:
            ok += 1
        else:
            ko += 1
            marque += f" (attendu {attendu})"
        print(f"{marque} {eid} {lib} : {obtenu}")
    print(f"Bilan : {ok}/{len(EXOS)} réponses conformes"
          + (f" · {ko} à revoir" if ko else " · tout est vert"))
    return 0 if ko == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
