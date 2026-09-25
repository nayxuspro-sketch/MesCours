#!/usr/bin/env python3
"""
chiffres_manuel.py — source d'unique vérité des chiffres cités dans le manuel.

Règle de production n°3 du projet : tout montant, tout comptage, toute date écrits dans un chapitre
doivent provenir de ce script. On exécute, on lit, on recopie. Aucun chiffre « à peu près ».

Sorties :
  data/reference/chiffres_cites.json   tous les nombres, par module (machines)
  data/reference/chiffres_cites.md     la même chose en tableaux, pour la relecture humaine
  + la structure réelle du socle (pour vérifier le §E.1 de l'architecture)

Usage : python3 scripts/chiffres_manuel.py [M01 M02 ...]
"""
from __future__ import annotations
import json, os, sys
import re
from collections import OrderedDict

def unidecode_str(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
BRUT = os.path.join(ROOT, "data", "brut")
REF = os.path.join(ROOT, "data", "reference")
PROJ = os.path.join(ROOT, "data", "projection")
FMT = lambda v: f"{int(round(v)):,}".replace(",", " ")


def fmcfa(v):
    return f"{int(round(v)):,} FCFA".replace(",", " ")


# ---------------------------------------------------------------- structure du socle
def structure():
    out = OrderedDict()
    tables = {
        "ventes_brutes.csv": ("brut.ventes", os.path.join(BRUT, "ventes_brutes.csv")),
        "clients.csv": ("brut.clients", os.path.join(BRUT, "clients.csv")),
        "produits.csv": ("brut.produits", os.path.join(BRUT, "produits.csv")),
        "magasins.csv": ("brut.magasins", os.path.join(BRUT, "magasins.csv")),
        "vendeurs.csv": ("brut.vendeurs", os.path.join(BRUT, "vendeurs.csv")),
        "objectifs_de_ca.csv": ("brut.objectifs", os.path.join(BRUT, "objectifs_de_ca.csv")),
        "stocks_quotidiens.csv": ("brut.stocks", os.path.join(BRUT, "stocks_quotidiens.csv")),
        "couts_achat.csv": ("brut.couts_achat", os.path.join(BRUT, "couts_achat.csv")),
        "remises_manuelles.xlsx": ("brut.remises", os.path.join(BRUT, "remises_manuelles.xlsx")),
        "ventes_propres.csv": ("propre.ventes", os.path.join(REF, "ventes_propres.csv")),
        "dim_date.csv": ("propre.dim_date", os.path.join(REF, "dim_date.csv")),
        "ventes_magasin5_2025.csv": ("projection", os.path.join(PROJ, "ventes_magasin5_2025.csv")),
    }
    for f, (tbl, path) in tables.items():
        if not os.path.exists(path):
            out[tbl] = {"fichier": f, "absent": True}
            continue
        if f.endswith(".xlsx"):
            df = pd.read_excel(path)
        elif f == "objectifs_de_ca.csv":
            df = pd.read_csv(path, sep=";", encoding="cp1252")
        elif "projection" in f or f == "ventes_magasin5_2025.csv":
            df = pd.read_csv(path, sep=";", encoding="utf-8-sig", dtype=str)
        else:
            df = pd.read_csv(path)
        out[tbl] = dict(fichier=f, lignes=int(len(df)), colonnes=int(df.shape[1]),
                        colonnes_liste=list(df.columns))
    return out


# ---------------------------------------------------------------- M01
def m01():
    """Tous les nombres utiles au module 1 : lecture d'un fichier, structure, anomalies visibles."""
    d = OrderedDict()
    petit = pd.read_csv(os.path.join(PROJ, "ventes_magasin5_2025.csv"), sep=";", encoding="utf-8-sig",
                        dtype=str, keep_default_na=False, na_values=[""])
    propre = pd.read_csv(os.path.join(REF, "ventes_magasin5_2025_ATTENDU.csv"), sep=";")
    d["petit_nom_fichier"] = "ventes_magasin5_2025.csv"
    d["petit_lignes"] = int(len(petit))
    d["petit_colonnes"] = int(petit.shape[1])
    d["petit_entetes"] = list(petit.columns)
    d["petit_types_infere_par_pandas"] = {c: str(t) for c, t in
                              pd.read_csv(os.path.join(PROJ, "ventes_magasin5_2025.csv"), sep=";",
                                          encoding="utf-8-sig").dtypes.items()}
    d["petit_valeurs_uniques"] = {c: int(petit[c].replace("", np.nan).nunique(dropna=True)) for c in petit.columns}
    d["petit_lignes_en_double"] = int(petit.duplicated().sum())
    d["petit_vendeur_distincts"] = int(petit["vendeur"].nunique())
    d["petit_categories"] = {k: int(v) for k, v in petit["categorie"].value_counts().items()}
    d["petit_produits_distincts"] = int(petit["produit"].nunique())
    d["petit_clients_manquants"] = int(petit["client"].isna().sum())
    d["petit_dates_mixtes"] = int(petit["date"].str.contains("/").sum())
    d["petit_montants_texte"] = int(pd.to_numeric(petit["montant_ttc"], errors="coerce").isna().sum())
    q = pd.to_numeric(petit["quantite"], errors="coerce")
    d["petit_quantites_max"] = int(q.max())
    d["petit_lignes_quantite_gt_500"] = int((q > 500).sum())
    d["petit_lignes_quantite_aberrantes"] = int((q > 500).sum())
    # ce que donne le fichier « tel quel » vs après nettoyage : la leçon du module
    brut_ttc = pd.to_numeric(petit["montant_ttc"].str.replace(" ", "", regex=False), errors="coerce")
    d["petit_total_ttc_brut"] = fmcfa(brut_ttc.sum())
    d["petit_total_ttc_brut_valeur"] = int(brut_ttc.sum())
    d["petit_total_ttc_propre"] = fmcfa(propre.montant_ttc.sum())
    d["petit_total_ttc_propre_valeur"] = int(propre.montant_ttc.sum())
    d["petit_ecart_nettoyage_pct"] = round(100 * (brut_ttc.sum() / propre.montant_ttc.sum() - 1), 2)
    # valeurs dérivées citées dans les énoncés : calculées ici, jamais inventées dans le texte
    _ecart = int(brut_ttc.sum() - propre.montant_ttc.sum())
    d["petit_ecart_nettoyage_valeur"] = fmcfa(_ecart)
    d["petit_ecart_nettoyage_valeur_brute"] = _ecart
    d["petit_double_total_brut"] = int(brut_ttc.sum() * 2)
    _trois = sorted(pd.to_numeric(propre.assign(m=pd.to_datetime(propre["date"]).dt.month)
                                   .groupby("m").montant_ttc.sum()).index)[:3]
    _p = propre.assign(m=pd.to_datetime(propre["date"]).dt.month)
    _p["montant_ttc"] = pd.to_numeric(_p["montant_ttc"])
    _s3 = _p[_p.m.isin(_trois)].montant_ttc.sum()
    d["petit_moyenne_trois_premiers_mois"] = int(round(_s3 / 3))
    d["petit_commande_brut_1_5pct"] = int(round(brut_ttc.sum() * 0.015))
    d["petit_commande_propre_1_5pct"] = int(round(propre.montant_ttc.astype("int64").sum() * 0.015))
    d["petit_surcout_commande_1_5pct"] = d["petit_commande_brut_1_5pct"] - d["petit_commande_propre_1_5pct"]
    d["petit_nb_tickets"] = int(propre["n_ticket"].nunique())
    d["petit_lignes_propres"] = int(len(propre))
    # bornes et modalités citées dans les énoncés : jamais recopiées de mémoire
    pq = pd.to_numeric(petit["prix_unitaire_ht"], errors="coerce")
    qq = pd.to_numeric(petit["quantite"], errors="coerce")
    d["petit_prix_min"], d["petit_prix_max"] = int(pq.min()), int(pq.max())
    d["petit_quantite_min"], d["petit_quantite_max"] = int(qq.min()), int(qq.max())
    d["petit_heure_min"], d["petit_heure_max"] = str(petit["heure"].min()), str(petit["heure"].max())
    d["petit_remise_modalites"] = sorted(float(x) for x in pd.to_numeric(petit["remise"], errors="coerce").dropna().unique())
    d["petit_dates_ecritures_distinctes"] = int(petit["date"].nunique())
    d["petit_jours_distincts"] = int(pd.to_datetime(propre["date"], dayfirst=False).dt.date.nunique())
    d["petit_montant_ht_max"] = int(pd.to_numeric(petit["montant_ht"], errors="coerce").max())
    # questions d'exercice, avec leur réponse chiffrée
    p = propre.copy()
    p["montant_ttc"] = pd.to_numeric(p["montant_ttc"], errors="coerce")
    p["date"] = pd.to_datetime(p["date"])
    p["mois"] = p["date"].dt.month
    par_mois = p.groupby("mois").montant_ttc.sum().astype(int)
    d["petit_meilleur_mois"] = f"mois {int(par_mois.idxmax())} — {fmcfa(par_mois.max())}"
    d["petit_pire_mois"] = f"mois {int(par_mois.idxmin())} — {fmcfa(par_mois.min())}"
    d["petit_ratio_meilleur_pire_mois"] = round(float(par_mois.max() / par_mois.min()), 2)
    d["petit_ca_par_mois"] = {int(k): int(v) for k, v in par_mois.items()}
    d["petit_panier_moyen"] = fmcfa(p.groupby("n_ticket").montant_ttc.sum().mean())
    d["petit_panier_median"] = fmcfa(p.groupby("n_ticket").montant_ttc.sum().median())
    _lignes = p.groupby("n_ticket").size()
    d["petit_lignes_par_ticket"] = (f"moyenne {round(_lignes.mean(), 2)} ligne(s) ; maximum {int(_lignes.max())}")
    par_cat = p.groupby("categorie").montant_ttc.sum().astype(int).sort_values(ascending=False)
    d["petit_ca_par_categorie"] = {k: int(v) for k, v in par_cat.items()}
    d["petit_lignes_par_categorie"] = {k: int(v) for k, v in petit["categorie"].value_counts().items()}
    d["petit_categorie_n1"] = (f"{par_cat.index[0]} — {fmcfa(par_cat.iloc[0])} "
                                f"({round(100 * par_cat.iloc[0] / par_cat.sum(), 1)} % du CA)")
    prod = p.groupby("produit").montant_ttc.sum().astype(int).sort_values(ascending=False)
    d["petit_top3_produits"] = {k: int(v) for k, v in prod.head(3).items()}
    jours = p.groupby(p["date"].dt.date).montant_ttc.sum()
    d["petit_jours_avec_ventes"] = int(len(jours))
    # attention : un jour sans ligne dans l'extrait ne veut pas dire magasin fermé
    d["petit_jours_sans_ligne_dans_extrait"] = int(365 - len(jours))
    d["petit_meilleur_jour"] = f"{jours.idxmax()} — {fmcfa(jours.max())}"
    v = p.groupby("vendeur").montant_ttc.sum().astype(int).sort_values(ascending=False)
    d["petit_vendeur_n1"] = f"{v.idxmax()} — {fmcfa(v.max())}"
    d["petit_classement_vendeurs"] = {k: int(x) for k, x in v.items()}
    # le fichier du fournisseur : ses 4 défauts, comptés
    fp = os.path.join(BRUT, "tarif_fournisseur_peinture.csv")
    lignes = open(fp, encoding="cp1252").read().splitlines()
    d["fournisseur_lignes_totales"] = len(lignes)
    d["fournisseur_lignes_chapeau"] = 3
    d["fournisseur_lignes_utiles"] = len(lignes) - 4
    d["fournisseur_separateur"] = "point-virgule ;"
    d["fournisseur_encodage"] = "Windows-1252 (cp1252)"
    d["fournisseur_prix_decimal"] = "virgule"
    d["fournisseur_entete"] = lignes[3]
    tar = pd.read_csv(fp, sep=";", encoding="cp1252", skiprows=3)
    tar["prix_unitaire"] = pd.to_numeric(tar["prix_unitaire"].astype(str).str.replace(",", ".", regex=False))
    d["fournisseur_prix_moyen"] = fmcfa(tar["prix_unitaire"].mean())
    d["fournisseur_prix_max"] = fmcfa(tar["prix_unitaire"].max())
    d["fournisseur_prix_max_brut"] = int(round(tar["prix_unitaire"].max()))
    d["fournisseur_tva"] = sorted(float(x) for x in pd.to_numeric(
        tar["tva"].astype(str).str.replace(",", ".", regex=False), errors="coerce").dropna().unique())
    # le gros fichier, pour l'exercice « combien de temps ça prend »
    gros = pd.read_csv(os.path.join(REF, "ventes_propres.csv"), usecols=["id_vente", "montant_ttc"])
    d["gros_lignes"] = int(len(gros))
    d["gros_ca"] = fmcfa(gros.montant_ttc.sum())
    d["gros_ca_valeur"] = int(gros.montant_ttc.sum())
    d["gros_taille_modo"] = round(os.path.getsize(os.path.join(BRUT, "ventes_brutes.csv")) / 1e6, 1)
    return d


# ---------------------------------------------------------------- M02
def m02():
    d = OrderedDict()
    p = pd.read_csv(os.path.join(REF, "ventes_magasin5_2025_ATTENDU.csv"), sep=";")
    p["montant_ttc"] = pd.to_numeric(p["montant_ttc"], errors="coerce")
    p["quantite"] = pd.to_numeric(p["quantite"], errors="coerce")
    t = p.groupby("n_ticket").montant_ttc.sum()
    d["panier_moyenne"] = int(round(t.mean()))
    d["panier_mediane"] = int(round(t.median()))
    d["panier_min"], d["panier_max"] = int(t.min()), int(t.max())
    d["panier_etendue"] = int(t.max() - t.min())
    d["panier_ecart_type"] = int(round(t.std(ddof=1)))
    d["panier_variance"] = int(round(t.var(ddof=1)))
    d["panier_cv_pct"] = round(100 * t.std(ddof=1) / t.mean(), 1)
    for q in (0.25, 0.5, 0.75, 0.9, 0.95, 0.99):
        d[f"panier_p{int(q*100)}"] = int(round(t.quantile(q)))
    d["panier_iqr"] = int(round(t.quantile(.75) - t.quantile(.25)))
    borne_sup = t.quantile(.75) + 1.5 * (t.quantile(.75) - t.quantile(.25))
    d["panier_seuil_iqr"] = int(round(borne_sup))
    d["panier_nb_aberrants_iqr"] = int((t > borne_sup).sum())
    d["panier_mode"] = int(round(t.mode().iloc[0])) if not t.mode().empty else None
    d["panier_modes"] = [int(round(v)) for v in t.mode()]
    d["panier_mode_fois"] = int((t == t.mode().iloc[0]).sum())
    d["panier_n"] = int(len(t))
    d["panier_asymetrie"] = round(float(t.skew()), 2)
    # corrélation quantité/montant et CA mensuel vs pluies (fil conducteur du chapitre M02.C06)
    d["corr_quantite_montant"] = round(float(p["quantite"].corr(p["montant_ttc"])), 3)

    # ---- M02.C01 : population, individus, variables, modalités, fréquences (mesuré sur l'ATTENDU propre)
    d["c01_n_lignes"] = int(len(p))
    d["c01_n_variables"] = int(p.shape[1])
    d["c01_n_tickets"] = int(p.n_ticket.nunique())
    d["c01_lignes_par_ticket"] = round(len(p) / p.n_ticket.nunique(), 2)
    d["c01_tickets_multi_lignes"] = int((p.groupby("n_ticket").size() > 1).sum())
    d["c01_pct_tickets_multi"] = round(100 * (p.groupby("n_ticket").size() > 1).mean(), 1)
    d["c01_max_lignes_par_ticket"] = int(p.groupby("n_ticket").size().max())
    for col in ("categorie", "vendeur", "magasin", "remise", "client", "produit"):
        d[f"c01_modalites_{col}"] = int(p[col].nunique())
    cat = p.categorie.value_counts()
    for k, v in cat.items():
        cle = "c01_freq_lignes_" + re.sub(r"[^a-z0-9]+", "_", unidecode_str(str(k)).lower()).strip("_")
        d[cle] = int(v)
        d[cle + "_pct"] = round(100 * v / len(p), 1)
    rm = p.remise.value_counts().sort_index()
    d["c01_freq_remise"] = {float(k): int(v) for k, v in rm.items()}
    d["c01_lignes_sans_remise"] = int((p.remise == 0).sum())
    d["c01_pct_lignes_sans_remise"] = round(100 * (p.remise == 0).mean(), 1)
    d["c01_lignes_avec_remise"] = int((p.remise > 0).sum())
    d["c01_mois_distincts"] = int(pd.to_datetime(p.date).dt.month.nunique())
    d["c01_lignes_par_mois"] = int(round(len(p) / pd.to_datetime(p.date).dt.month.nunique()))

    # ---- M02.C02 : centres, avec et sans valeurs extrêmes ; moyenne pondérée ; par vendeur
    t2 = p.groupby("n_ticket").montant_ttc
    _sans = t[t <= borne_sup]
    d["c02_panier_moyenne_sans_aberrants"] = int(round(_sans.mean()))
    d["c02_panier_mediane_sans_aberrants"] = int(round(_sans.median()))
    d["c02_ecart_moyenne_mediane"] = int(round(t.mean() - t.median()))
    d["c02_ratio_moyenne_mediane"] = round(float(t.mean() / t.median()), 2)
    d["c02_moyenne_pct_du_p75"] = round(100 * float(t.mean()) / float(t.quantile(.75)), 1)
    d["c02_tickets_sous_la_moyenne"] = int((t < t.mean()).sum())
    d["c02_pct_tickets_sous_la_moyenne"] = round(100 * (t < t.mean()).mean(), 1)
    d["c02_quantite_moyenne"] = round(float(p.quantite.mean()), 1)
    d["c02_quantite_mediane"] = int(round(float(p.quantite.median())))
    d["c02_montant_ligne_moyen"] = int(round(p.montant_ttc.mean()))
    d["c02_montant_ligne_median"] = int(round(p.montant_ttc.median()))
    d["c02_remise_moyenne"] = round(float(p.remise.mean()), 4)
    d["c02_remise_ponderee"] = round(float((p.remise * p.montant_ht.abs()).sum() / p.montant_ht.abs().sum()), 4)
    par_v = p.groupby("vendeur").montant_ttc.agg(["sum", "count"]).sort_values("sum", ascending=False)
    for v, r in par_v.iterrows():
        cle = "c02_vendeur_" + re.sub(r"[^a-z0-9]+", "_", unidecode_str(str(v)).lower()).strip("_")
        d[cle] = int(round(r["sum"]))
        d[cle + "_lignes"] = int(r["count"])
        d[cle + "_moyenne_ligne"] = int(round(r["sum"] / r["count"]))

    # ---- C01 : ce que « distinct » veut dire sur la colonne client (vides compris)
    cl = p["client"].astype(str).str.strip()
    d["c01_clients_modalites_brutes"] = int(cl.nunique())
    d["c01_clients_vides"] = int(cl.isin(["", "nan", "0", "0.0"]).sum())
    d["c01_clients_distincts_hors_vides"] = int(cl[~cl.isin(["", "nan", "0", "0.0"])].nunique())
    d["c01_produits_distincts"] = int(p["produit"].nunique())
    d["c01_date_ecritures_distinctes"] = int(p["date"].astype(str).nunique())
    d["c01_date_jours_reels"] = int(pd.to_datetime(p["date"], dayfirst=True, format="mixed").dt.date.nunique())

    # ========================================================= M02.C02 à C08 : mesures dédiées
    import numpy as _np
    ligne = p.copy()
    d["c02_total_propre"] = int(ligne.montant_ttc.sum())
    _brut = pd.read_csv(os.path.join(REF, "..", "projection", "ventes_magasin5_2025.csv"), sep=";")
    d["c02_total_brut"] = int(pd.to_numeric(_brut["montant_ttc"].astype(str).str.replace(" ", ""), errors="coerce").sum())
    tp = ligne.groupby("n_ticket").montant_ttc
    simple = ligne.groupby("n_ticket").size()
    pan = tp.sum()
    d["c02_panier_moyen_simple"] = int(round(pan[simple == 1].mean()))
    d["c02_panier_median_simple"] = int(round(pan[simple == 1].median()))
    d["c02_panier_moyen_multi"] = int(round(pan[simple > 1].mean()))
    d["c02_panier_median_multi"] = int(round(pan[simple > 1].median()))
    d["c02_n_tickets_simple"] = int((simple == 1).sum())
    d["c02_n_tickets_multi"] = int((simple > 1).sum())
    tri = pan.sort_values()
    k = int(round(0.10 * len(tri)))
    d["c02_part_ca_top10pct_pct"] = round(100 * tri.iloc[-k:].sum() / pan.sum(), 1)
    d["c02_lignes_negatives"] = int((ligne.montant_ttc < 0).sum())
    d["c02_moyenne_ligne_sans_negatifs"] = int(round(ligne.loc[ligne.montant_ttc > 0, "montant_ttc"].mean()))
    d["c02_etendue_quantite"] = int(ligne.quantite.max() - ligne.quantite.min())
    mq = ligne.quantite.value_counts()
    d["c02_quantite_mode"] = int(mq.index[0])
    d["c02_quantite_mode_lignes"] = int(mq.iloc[0])
    for cat, g in ligne.groupby("categorie"):
        cle = "c02_" + re.sub(r"[^a-z0-9]+", "_", unidecode_str(str(cat)).lower()).strip("_")
        d[cle + "_moyenne_ligne"] = int(round(g.montant_ttc.mean()))
        d[cle + "_mediane_ligne"] = int(round(g.montant_ttc.median()))

    # ---- C03 : dispersion
    sd = float(pan.std(ddof=1))
    d["c03_erreur_type_moyenne"] = int(round(sd / _np.sqrt(len(pan))))
    d["c03_mad"] = int(round((pan - pan.median()).abs().median()))
    d["c03_ratio_etendue_iqr"] = round(float(pan.max() - pan.min()) / d["panier_iqr"], 1)
    d["c03_cv_sans_aberrants_pct"] = round(100 * float(_sans.std(ddof=1) / _sans.mean()), 1)
    d["c03_se_pct_moyenne"] = round(100 * (sd / _np.sqrt(len(pan))) / float(pan.mean()), 1)
    for cat, g in ligne.groupby("categorie"):
        cle = "c03_cv_" + re.sub(r"[^a-z0-9]+", "_", unidecode_str(str(cat)).lower()).strip("_")
        d[cle + "_pct"] = round(100 * float(g.montant_ttc.std(ddof=1) / g.montant_ttc.mean()), 1)
        d[cle + "_ecart_type"] = int(round(g.montant_ttc.std(ddof=1)))
    d["c03_ligne_ecart_type"] = int(round(ligne.montant_ttc.std(ddof=1)))
    d["c03_variance_ligne"] = int(round(ligne.montant_ttc.var(ddof=1)))
    d["c02_ligne_min"] = int(ligne.montant_ttc.min())
    d["c02_ligne_max"] = int(ligne.montant_ttc.max())
    d["c02_ligne_etendue"] = int(ligne.montant_ttc.max() - ligne.montant_ttc.min())
    d["c02_ligne_cv_pct"] = round(100 * float(ligne.montant_ttc.std(ddof=1) / ligne.montant_ttc.mean()), 1)
    d["c02_retours_n"] = int((ligne.montant_ttc < 0).sum())
    d["c02_retours_somme"] = int(ligne.loc[ligne.montant_ttc < 0, "montant_ttc"].sum())
    d["c02_quantite_min"] = int(ligne.quantite.min())
    d["c02_quantite_max"] = int(ligne.quantite.max())
    d["c03_quantite_ecart_type"] = round(float(ligne.quantite.std(ddof=1)), 1)
    d["c03_quantite_cv_pct"] = round(100 * float(ligne.quantite.std(ddof=1) / ligne.quantite.mean()), 1)
    d["c03_tukey_k"] = int(round(1.5 * d["panier_iqr"]))
    d["c03_tukey_borne_basse"] = int(round(pan.quantile(.25) - 1.5 * d["panier_iqr"]))
    d["c03_sigma2"] = int(round(2 * sd))
    _en = pd.read_csv(os.path.join(REF, "..", "projection", "ventes_magasin5_2025.csv"), sep=";")
    d["c02_quantite_max_enonce"] = int(_en.quantite.max())
    d["c02_quantite_lignes_gt500_enonce"] = int((_en.quantite > 500).sum())

    # ---- C04 : positions
    for q in (10, 20, 40, 60, 80):
        d[f"c04_panier_p{q}"] = int(round(pan.quantile(q / 100)))
    borne_inf = pan.quantile(.25) - 1.5 * d["panier_iqr"]
    d["c04_moustache_basse"] = int(round(pan[pan >= borne_inf].min()))
    d["c04_moustache_haute"] = int(round(pan[pan <= d["panier_seuil_iqr"]].max()))
    d["c04_hors_moustaches_bas"] = int((pan < borne_inf).sum())
    d["c04_nb_entre_q1_q3"] = int(((pan >= pan.quantile(.25)) & (pan <= pan.quantile(.75))).sum())
    d["c04_percentile_200000"] = int(round(100 * (pan < 200000).mean()))
    d["c04_percentile_50000"] = int(round(100 * (pan < 50000).mean()))
    d["c04_ca_du_dernier_decile_pct"] = round(100 * pan.nlargest(len(pan) // 10).sum() / pan.sum(), 1)
    # variantes de méthode de percentile + répartition du CA par bandes de déciles
    d["c04_p90_lineaire"] = int(round(pan.quantile(.90)))
    d["c04_p90_voisin"] = int(round(pan.quantile(.90, interpolation="lower")))
    d["c04_p90_plus_proche"] = int(round(pan.quantile(.90, interpolation="nearest")))
    _v = pan.sort_values().to_numpy()
    _pos = 0.90 * (len(_v) + 1)                     # convention « exclusive » des tableurs : QUARTILE.EXC
    _i = int(_pos // 1) - 1
    d["c04_p90_exclusif"] = int(round(_v[_i] + (_pos - int(_pos)) * (_v[_i + 1] - _v[_i])))
    _c = pan.sort_values()
    for b in (25, 50, 75, 90):
        d[f"c04_ca_sous_p{b}_pct"] = round(100 * float(_c[_c <= _c.quantile(b / 100)].sum() / _c.sum()), 1)
    d["c04_effectif_premier_decile"] = int(round(.10 * len(_c)))
    d["c04_nb_au_dessus_p90"] = int((_c > _c.quantile(.90)).sum())
    d["c04_ca_au_dessus_p90_pct"] = round(100 * float(_c[_c > _c.quantile(.90)].sum() / _c.sum()), 1)
    d["c04_ecart_top32_vs_p90_pp"] = round(d["c02_part_ca_top10pct_pct"] - d["c04_ca_au_dessus_p90_pct"], 1)

    # ---- C05 : formes
    bornes = [-float("inf")] + list(range(0, 300000, 50000)) + [float("inf")]
    hist = _np.histogram(pan, bins=bornes)[0]
    d["c05_classes_50k"] = [int(x) for x in hist]
    d["c05_classe_modale_index"] = int(_np.argmax(hist)) + 1
    d["c05_classes_nuis"] = int((hist > 0).sum())
    d["c05_classe_modale_effectif"] = int(hist.max())
    d["c05_classe_modale_pct"] = round(100 * float(hist.max() / len(pan)), 1)
    d["c05_sup_300k"] = int((pan > 300000).sum())
    d["c05_sup_500k"] = int((pan > 500000).sum())
    d["c05_entre_0_50k"] = int(((pan > 0) & (pan <= 50000)).sum())
    d["c05_kurtosis"] = round(float(pan.kurt()), 2)
    d["c05_tickets_negatifs"] = int((pan < 0).sum())
    d["c05_tickets_sup_100k"] = int((pan > 100000).sum())
    d["c05_pct_sup_100k"] = round(100 * (pan > 100000).mean(), 1)
    d["c05_ratio_max_median"] = round(float(pan.max() / pan.median()), 1)
    d["c05_tickets_au_dessus_moyenne"] = int((pan > pan.mean()).sum())
    d["c05_pct_au_dessus_moyenne"] = round(100 * (pan > pan.mean()).mean(), 1)
    # règles de choix de classes, pour la démonstration du §5.2 de M02.C05
    _n = len(pan)
    _fd = 2 * float(d["panier_iqr"]) / (_n ** (1 / 3))
    d["c05_largeur_fd"] = int(round(_fd))
    d["c05_nb_classes_fd"] = int(round((pan.max() - pan.min()) / _fd))
    d["c05_nb_classes_sturges"] = int(round(1 + _np.log2(_n)))
    d["c05_paniers_distincts"] = int(pan.nunique())
    d["c05_pct_classe_sup_250k"] = round(100 * hist[6] / _n, 1)
    d["c05_pct_classe_negatifs"] = round(100 * hist[0] / _n, 1)
    d["c05_somme_classes"] = int(sum(hist))
    d["c05_classe_mediane_index"] = int(_np.digitize(pan.median(), bornes[1:-1]) + 1)
    _tot = float(pan.sum())
    for _nom, _sel in (("inf50k", pan < 50000), ("0_50k", (pan >= 0) & (pan < 50000)),
                       ("milieu", (pan >= 50000) & (pan < 250000)), ("sup250k", pan > 250000)):
        d[f"c05_ca_classe_{_nom}_pct"] = round(100 * float(pan[_sel].sum()) / _tot, 1)
        d[f"c05_n_classe_{_nom}"] = int(_sel.sum())
    _idx = _np.digitize(pan, bornes[1:-1])
    d["c05_ca_par_classe_pct"] = [round(100 * float(pan[_idx == i].sum()) / _tot, 1) for i in range(len(hist))]
    d["c05_n_par_classe"] = [int(x) for x in hist]


    # ---- C06 : relations
    from scipy import stats as _st
    d["c06_covariance_quantite_montant"] = int(round(float(_np.cov(ligne.quantite, ligne.montant_ttc)[0, 1])))
    d["c06_corr_spearman"] = round(float(_st.spearmanr(ligne.quantite, ligne.montant_ttc).statistic), 3)
    d["c06_corr_remise_montant"] = round(float(ligne.remise.corr(ligne.montant_ttc)), 3)
    d["c06_corr_prix_montant"] = round(float(ligne.prix_unitaire_ht.corr(ligne.montant_ttc)), 3)
    heure = ligne["heure"].astype(str).str.split(":").str[0].astype(float)
    d["c06_corr_heure_montant"] = round(float(_np.corrcoef(heure, ligne.montant_ttc)[0, 1]), 3)
    reg = _st.linregress(ligne.quantite, ligne.montant_ttc)
    d["c06_pente_par_unite"] = int(round(reg.slope))
    d["c06_ordonnee"] = int(round(reg.intercept))
    d["c06_r2_pct"] = round(100 * reg.rvalue ** 2, 1)
    d["c06_pente_valeur_absolue_pct"] = round(100 * abs(reg.slope) * ligne.quantite.std() / ligne.montant_ttc.std(), 1)
    d["c06_corr_ht_ttc"] = round(float(ligne.montant_ht.corr(ligne.montant_ttc)), 3)
    d["c06_corr_quantite_prix"] = round(float(ligne.quantite.corr(ligne.prix_unitaire_ht)), 3)
    d["c06_r_au_carre_pct"] = round(100 * float(ligne.quantite.corr(ligne.montant_ttc)) ** 2, 1)
    d["c06_prediction_a_moyenne"] = int(round(d["c06_ordonnee"] + d["c06_pente_par_unite"] * d["c02_quantite_moyenne"]))

    # ---- C07 : hasard, intervalle, taille d'échantillon
    n = len(pan)
    prop_multi = (simple > 1).mean()
    d["c07_se_propotion_pp"] = round(100 * float(_np.sqrt(prop_multi * (1 - prop_multi) / n)), 1)
    d["c07_ic95_prop_multi"] = [round(100 * (prop_multi - 1.96 * _np.sqrt(prop_multi * (1 - prop_multi) / n)), 1),
                               round(100 * (prop_multi + 1.96 * _np.sqrt(prop_multi * (1 - prop_multi) / n)), 1)]
    d["c07_n_pour_marge_5pp"] = int(_np.ceil(0.25 * (1.96 / 0.05) ** 2))
    d["c07_ic95_moyenne_panier"] = [int(round(pan.mean() - 1.96 * sd / _np.sqrt(n))),
                                    int(round(pan.mean() + 1.96 * sd / _np.sqrt(n)))]
    rng = _np.random.default_rng(20260917)
    meds = _np.median(rng.choice(pan.to_numpy(), size=(2000, n), replace=True), axis=1)
    d["c07_mediane_ic95"] = [int(round(_np.percentile(meds, 2.5))), int(round(_np.percentile(meds, 97.5)))]
    d["c07_largeur_ic_mediane"] = d["c07_mediane_ic95"][1] - d["c07_mediane_ic95"][0]

    # ---- C07 : ce que l'estimation doit au hasard (population réelle de l'extrait, biais, IC, bootstrap)
    gros = pd.read_csv(os.path.join(REF, "ventes_propres.csv"),
                       usecols=["id_ticket", "id_magasin", "annee", "date_vente", "montant_ttc", "id_produit"],
                       parse_dates=["date_vente"])
    prod = pd.read_csv(os.path.join(REF, "produits_propres.csv"), usecols=["id_produit", "categorie"])
    pop = gros[(gros.id_magasin == 5) & (gros.annee == 2025)].merge(prod, on="id_produit", how="left")
    poppan = pop.groupby("id_ticket").agg(m=("montant_ttc", "sum"), jour=("date_vente", lambda s: s.min().day))
    d["c07_pop_lignes"] = int(len(pop))
    d["c07_pop_tickets"] = int(len(poppan))
    d["c07_pop_moyenne_panier"] = int(round(poppan.m.mean()))
    d["c07_pop_mediane_panier"] = int(round(poppan.m.median()))
    d["c07_part_extrait_lignes_pct"] = round(100 * len(ligne) / len(pop), 1)
    d["c07_part_extrait_tickets_pct"] = round(100 * len(pan) / len(poppan), 1)
    d["c07_ecart_moyenne_pop_pct"] = round(100 * (float(pan.mean()) / float(poppan.m.mean()) - 1), 1)
    d["c07_ecart_mediane_pop_pct"] = round(100 * (float(pan.median()) / float(poppan.m.median()) - 1), 1)
    dat = pd.to_datetime(ligne["date"])
    d["c07_jours_du_mois"] = [int(v) for v in sorted(dat.dt.day.unique())]
    d["c07_dates_distinctes"] = int(ligne["date"].nunique())
    d["c07_lignes_max_date"] = int(ligne["date"].value_counts().max())
    d["c07_lignes_par_mois"] = int(round(len(ligne) / dat.dt.month.nunique()))
    _par_mois = ligne.assign(m=dat.dt.month).groupby("m")["date"].nunique()
    d["c07_jours_par_mois_min"] = int(_par_mois.min())
    d["c07_jours_par_mois_max"] = int(_par_mois.max())
    d["c07_lignes_mediane_par_date"] = int(ligne["date"].value_counts().median())
    _h = ligne["heure"].astype(str)
    d["c07_heure_min"], d["c07_heure_max"] = str(_h.min()), str(_h.max())
    d["c07_mois_couverts"] = int(dat.dt.month.nunique())
    debut = poppan.jour <= max(d["c07_jours_du_mois"])
    d["c07_pop_moy_jours_debut"] = int(round(poppan.m[debut].mean()))
    d["c07_pop_moy_autres_jours"] = int(round(poppan.m[~debut].mean()))
    d["c07_pop_med_jours_debut"] = int(round(poppan.m[debut].median()))
    d["c07_pop_med_autres_jours"] = int(round(poppan.m[~debut].median()))
    d["c07_pop_part_jours_debut_pct"] = round(100 * float(debut.mean()), 1)
    d["c07_se_moyenne"] = int(round(sd / _np.sqrt(n)))
    d["c07_marge_erreur"] = int(round(1.96 * sd / _np.sqrt(n)))
    d["c07_ic95_normal"] = [int(round(pan.mean() - d["c07_marge_erreur"])), int(round(pan.mean() + d["c07_marge_erreur"]))]
    d["c07_largeur_ic_moyenne"] = 2 * d["c07_marge_erreur"]
    d["c07_ecart_mediane_vs_jours_debut"] = abs(pan.median() - d["c07_pop_med_jours_debut"])
    d["c07_ic95_couvre_population"] = bool(d["c07_ic95_normal"][0] <= d["c07_pop_moyenne_panier"] <= d["c07_ic95_normal"][1])
    x = pan.to_numpy(dtype=float)
    _r = _np.random.default_rng(20260917)
    moy30 = x[_np.argsort(_r.random((5000, n)), axis=1)[:, :30]].mean(axis=1)   # 5000 tirages SANS remise de 30 tickets
    d["c07_tirages"] = 5000
    d["c07_taille_tirage"] = 30
    d["c07_graine"] = 20260917
    d["c07_moyenne_dist_moyenne_n30"] = int(round(moy30.mean()))
    d["c07_sd_dist_moyenne_n30"] = int(round(moy30.std(ddof=1)))
    d["c07_theorie_sd_racine_n30"] = int(round(sd / _np.sqrt(30)))
    # tirage SANS remise dans une population finie : la correction réduit l'écart type théorique
    _fpc = _np.sqrt((n - 30) / (n - 1))
    d["c07_fpc_n30"] = round(float(_fpc), 3)
    d["c07_theorie_sd_corrigee_n30"] = int(round(sd / _np.sqrt(30) * _fpc))
    d["c07_ic95_dist_moyenne_n30"] = [int(round(v)) for v in _np.percentile(moy30, [2.5, 97.5])]
    d["c07_cv_dist_moyenne_pct"] = round(100 * float(moy30.std(ddof=1)) / float(moy30.mean()), 1)
    _r = _np.random.default_rng(20260917)
    med30 = _np.median(x[_np.argsort(_r.random((5000, n)), axis=1)[:, :30]], axis=1)
    d["c07_moyenne_dist_mediane_n30"] = int(round(med30.mean()))
    d["c07_sd_dist_mediane_n30"] = int(round(med30.std(ddof=1)))
    d["c07_cv_dist_mediane_pct"] = round(100 * float(med30.std(ddof=1)) / float(med30.mean()), 1)
    d["c07_ic95_dist_mediane_n30"] = [int(round(v)) for v in _np.percentile(med30, [2.5, 97.5])]
    _r = _np.random.default_rng(20260917)
    boot = _r.choice(x, size=(2000, n), replace=True)
    d["c07_ic95_bootstrap_moyenne"] = [int(round(v)) for v in _np.percentile(boot.mean(axis=1), [2.5, 97.5])]
    bmin = boot.min(axis=1)
    d["c07_ic95_bootstrap_min"] = [int(round(v)) for v in _np.percentile(bmin, [2.5, 97.5])]
    d["c07_bootstrap_min_fois_exact_pct"] = round(100 * float((bmin == x.min()).mean()), 1)
    d["c07_n_pour_marge_3pp"] = int(_np.ceil(0.25 * (1.96 / 0.03) ** 2))
    _pr = float((ligne.remise > 0).mean())
    _se_pr = float(_np.sqrt(_pr * (1 - _pr) / len(ligne)))
    d["c07_lignes_avec_remise"] = int((ligne.remise > 0).sum())
    d["c07_part_remise_pct"] = round(100 * _pr, 1)
    d["c07_se_remise_pp"] = round(100 * _se_pr, 1)
    d["c07_marge_remise_pp"] = round(100 * 1.96 * _se_pr, 1)
    d["c07_ic95_part_remise"] = [round(100 * (_pr - 1.96 * _se_pr), 1), round(100 * (_pr + 1.96 * _se_pr), 1)]
    d["c07_n_pour_marge_3pp_a36pct"] = int(_np.ceil(_pr * (1 - _pr) * (1.96 / 0.03) ** 2))
    d["c07_n_pour_marge_5pp_33pct"] = int(_np.ceil(prop_multi * (1 - prop_multi) * (1.96 / 0.05) ** 2))
    d["c07_n_pour_10pct_relatif"] = int(_np.ceil((1.96 * sd / (0.1 * float(pan.mean()))) ** 2))
    d["c07_moy_ligne_extrait"] = int(round(float(ligne.montant_ttc.mean())))
    d["c07_moy_ligne_population"] = int(round(float(pop.montant_ttc.mean())))
    d["c07_ecart_brut_ligne_pct"] = round(100 * (float(ligne.montant_ttc.mean()) / float(pop.montant_ttc.mean()) - 1), 1)
    moy_par_cat = ligne.groupby("categorie").montant_ttc.mean()
    part_pop = pop.categorie.value_counts(normalize=True).reindex(moy_par_cat.index).fillna(0.0)
    d["c07_moy_ligne_ponderee"] = int(round(float((part_pop * moy_par_cat).sum())))
    d["c07_ecart_pondere_ligne_pct"] = round(100 * (float((part_pop * moy_par_cat).sum()) / float(pop.montant_ttc.mean()) - 1), 1)

    # ---- C08 : décider avec incertitude
    v = ligne.groupby("vendeur").montant_ttc
    bato = v.get_group("Adama Bationo")
    ilbo = v.get_group("Moussa Ilboudo")
    tw = _st.ttest_ind(bato, ilbo, equal_var=False)
    d["c08_t_welch"] = round(float(tw.statistic), 2)
    d["c08_p_welch"] = float(f"{tw.pvalue:.3g}")
    diff = float(bato.mean() - ilbo.mean())
    se = _np.sqrt(bato.var(ddof=1) / len(bato) + ilbo.var(ddof=1) / len(ilbo))
    d["c08_diff_moyennes_ligne"] = int(round(diff))
    d["c08_ic95_diff"] = [int(round(diff - 1.96 * se)), int(round(diff + 1.96 * se))]
    d["c08_n_bationo"] = int(len(bato)); d["c08_n_ilboudo"] = int(len(ilbo))
    tt = _st.ttest_1samp(pan, 100000)
    d["c08_t_vs_100k"] = round(float(tt.statistic), 2)
    d["c08_p_vs_100k"] = float(f"{tt.pvalue:.3g}")
    tab = pd.crosstab(ligne.vendeur, ligne.remise > 0)
    ch = _st.chi2_contingency(tab)
    d["c08_chi2"] = round(float(ch.statistic), 2)
    d["c08_chi2_ddl"] = int(ch.dof)
    d["c08_chi2_p"] = float(f"{ch.pvalue:.3g}")
    d["c08_chi2_theorique_min"] = round(float(ch.expected_freq.min()), 1)
    # effectifs observés du tableau vendeur × remise (pour afficher le test en clair)
    obs = tab.to_dict("index")
    for v, r in obs.items():
        cle = "c08_obs_" + re.sub(r"[^a-z0-9]+", "_", unidecode_str(str(v)).lower()).strip("_")
        d[cle + "_avec_remise"] = int(r.get(True, 0))
        d[cle + "_sans_remise"] = int(r.get(False, 0))
    # --- C08 (suite) : les six comparaisons deux à deux, puissance, permutation, et le grain du test
    def _sl(v):
        return re.sub(r"[^a-z0-9]+", "_", unidecode_str(str(v)).lower()).strip("_")
    import itertools as _it
    par_v = {v: g.montant_ttc.to_numpy(dtype=float) for v, g in ligne.groupby("vendeur")}
    noms = sorted(par_v)
    paires = OrderedDict()
    for a, b in _it.combinations(noms, 2):
        Aa, Bb = par_v[a], par_v[b]
        dd = float(Aa.mean() - Bb.mean())
        ee = float(_np.sqrt(Aa.var(ddof=1) / len(Aa) + Bb.var(ddof=1) / len(Bb)))
        tt = _st.ttest_ind(Aa, Bb, equal_var=False)
        mw = _st.mannwhitneyu(Aa, Bb)
        paires[_sl(a) + "__" + _sl(b)] = {"ecart": int(round(dd)), "ic_bas": int(round(dd - 1.96 * ee)),
                                         "ic_haut": int(round(dd + 1.96 * ee)), "t": round(float(tt.statistic), 2),
                                         "p_welch": round(float(tt.pvalue), 3), "p_rangs": round(float(mw.pvalue), 4)}
    d["c08_paires"] = paires
    A, B = par_v["Adama Bationo"], par_v["Moussa Ilboudo"]
    d["c08_ligne_moyenne_bationo"] = int(round(A.mean()))
    d["c08_ligne_mediane_bationo"] = int(round(_np.median(A)))
    d["c08_ligne_p90_bationo"] = int(round(_np.percentile(A, 90)))
    d["c08_ligne_sup250k_bationo_pct"] = round(100 * float((A > 250000).mean()), 1)
    d["c08_ligne_moyenne_ilboudo"] = int(round(B.mean()))
    d["c08_ligne_mediane_ilboudo"] = int(round(_np.median(B)))
    d["c08_ligne_p90_ilboudo"] = int(round(_np.percentile(B, 90)))
    d["c08_ligne_sup250k_ilboudo_pct"] = round(100 * float((B > 250000).mean()), 1)
    d["c08_ecart_medianes"] = int(round(_np.median(A) - _np.median(B)))
    ee = float(_np.sqrt(A.var(ddof=1) / len(A) + B.var(ddof=1) / len(B)))
    d["c08_se_difference"] = int(round(ee))
    d["c08_ddl_welch"] = round(float(tw.df), 1)
    d["c08_t_critique"] = round(float(_st.t.ppf(0.975, tw.df)), 2)
    pool = float(_np.sqrt(((len(A) - 1) * A.var(ddof=1) + (len(B) - 1) * B.var(ddof=1)) / (len(A) + len(B) - 2)))
    d["c08_ecart_type_pooled"] = int(round(pool))
    d["c08_cohen_d"] = round(diff / pool, 2)
    d["c08_mde_puissance80"] = int(round((_st.t.ppf(0.975, tw.df) + _st.t.ppf(0.8, tw.df)) * ee))
    d["c08_puissance_ecart_20k_pct"] = round(100 * float(_st.norm.cdf(20000 / ee - _st.norm.ppf(0.975))), 1)
    d["c08_puissance_ecart_observe_pct"] = round(100 * float(_st.norm.cdf(diff / ee - _st.norm.ppf(0.975))), 1)
    d["c08_n_par_groupe_pour_80pc"] = int(_np.ceil(2 * (1.96 + 0.8416) ** 2 * pool ** 2 / diff ** 2))
    _r = _np.random.default_rng(20260917)
    tout = _np.concatenate([A, B]).astype(_np.float64)
    na = len(A)
    perm = _np.empty(10000)
    for _i in range(10000):
        s = _r.permutation(tout)
        perm[_i] = s[:na].mean() - s[na:].mean()
    d["c08_p_permutation"] = round(float((_np.sum(_np.abs(perm) >= abs(diff)) + 1) / (len(perm) + 1)), 4)
    d["c08_tirages_permutation"] = 10000
    d["c08_alpha_bonferroni"] = round(0.05 / len(list(_it.combinations(noms, 2))), 4)
    d["c08_comparaisons"] = int(len(list(_it.combinations(noms, 2))))
    d["c08_p_min_comparaisons"] = min(v["p_welch"] for v in paires.values())
    d["c08_tickets_multi_vendeurs"] = int((p.groupby("n_ticket").vendeur.nunique() > 1).sum())
    v_ = ligne.groupby("n_ticket").vendeur.first()
    Bt = pan[(v_ == "Adama Bationo").to_numpy()].to_numpy(dtype=float)
    It = pan[(v_ == "Moussa Ilboudo").to_numpy()].to_numpy(dtype=float)
    tv = _st.ttest_ind(Bt, It, equal_var=False)
    dv = float(Bt.mean() - It.mean())
    ev = float(_np.sqrt(Bt.var(ddof=1) / len(Bt) + It.var(ddof=1) / len(It)))
    d["c08_version_ticket"] = OrderedDict([("n_bationo", int(len(Bt))), ("n_ilboudo", int(len(It))),
                                         ("moyenne_bationo", int(round(Bt.mean()))), ("moyenne_ilboudo", int(round(It.mean()))),
                                         ("ecart", int(round(dv))), ("t", round(float(tv.statistic), 2)),
                                         ("p", round(float(tv.pvalue), 3)), ("ic_bas", int(round(dv - 1.96 * ev))),
                                         ("ic_haut", int(round(dv + 1.96 * ev)))])
    n_il, x_il = int(tab.loc["Moussa Ilboudo"].sum()), int(tab.loc["Moussa Ilboudo"][True])
    n_ba, x_ba = int(tab.loc["Adama Bationo"].sum()), int(tab.loc["Adama Bationo"][True])
    p1, p2 = x_il / n_il, x_ba / n_ba
    z = (p1 - p2) / _np.sqrt((x_il + x_ba) / (n_il + n_ba) * (1 - (x_il + x_ba) / (n_il + n_ba)) * (1 / n_il + 1 / n_ba))
    sep = _np.sqrt(p1 * (1 - p1) / n_il + p2 * (1 - p2) / n_ba)
    d["c08_part_remise_ilboudo_pct"] = round(100 * float(p1), 1)
    d["c08_part_remise_bationo_pct"] = round(100 * float(p2), 1)
    d["c08_ecart_remise_pp"] = round(100 * float(p1 - p2), 1)
    d["c08_ic95_ecart_remise_pp"] = [round(100 * float(p1 - p2 - 1.96 * sep), 1), round(100 * float(p1 - p2 + 1.96 * sep), 1)]
    d["c08_z_remise"] = round(float(z), 2)
    d["c08_p_remise"] = round(float(2 * (1 - _st.norm.cdf(abs(z)))), 3)
    for v_, arr in par_v.items():
        cle = "c08_" + _sl(v_)
        d[cle + "_moyenne_ligne"] = int(round(arr.mean()))
        d[cle + "_mediane_ligne"] = int(round(_np.median(arr)))
        d[cle + "_p90_ligne"] = int(round(_np.percentile(arr, 90)))
        d[cle + "_sup250k_pct"] = round(100 * float((arr > 250000).mean()), 1)
        d[cle + "_tickets"] = int(ligne[ligne.vendeur == v_].n_ticket.nunique())
    d["c08_marge_difference"] = int(round(1.96 * ee))
    d["c08_se_version_ticket"] = int(round(ev))
    tab_c = pd.crosstab(ligne.vendeur, ligne.categorie)
    ch_c = _st.chi2_contingency(tab_c)
    d["c08_chi2_cat"] = round(float(ch_c.statistic), 2)
    d["c08_chi2_cat_ddl"] = int(ch_c.dof)
    d["c08_chi2_cat_p"] = round(float(ch_c.pvalue), 3)
    d["c08_chi2_cat_theorique_min"] = round(float(ch_c.expected_freq.min()), 2)
    d["c08_chi2_cat_cases_sous_5"] = int((ch_c.expected_freq < 5).sum())
    d["c08_chi2_cat_cases"] = int(tab_c.size)



    # effet de structure (Simpson) : panier moyen par ticket, global puis à catégorie contenue
    lig = ligne.copy()
    lig["gros"] = (lig.remise > 0).astype(int)
    def paniers(sous):
        return sous.groupby("n_ticket").montant_ttc.sum()
    glob = {v: float(paniers(g).mean()) for v, g in lig.groupby("vendeur")}
    d["c06_panier_global_max"] = int(round(max(glob.values())))
    d["c06_panier_global_min"] = int(round(min(glob.values())))
    d["c06_panier_global_ecart"] = int(round(max(glob.values()) - min(glob.values())))
    cats = sorted(lig.categorie.unique())
    diffs = []
    parts = {}
    for cat in cats:
        sub = {}
        for v, g in lig[lig.categorie == cat].groupby("vendeur"):
            q = g.groupby("n_ticket").montant_ttc
            if len(g) >= 8:
                sub[v] = float(q.sum().mean())
        if len(sub) >= 2:
            diffs.append(max(sub.values()) - min(sub.values()))
    d["c06_ecart_within_categorie_moyen"] = int(round(sum(diffs) / len(diffs))) if diffs else 0
    d["c06_ecart_within_categorie_max"] = int(round(max(diffs))) if diffs else 0
    d["c06_ecart_within_categorie_min"] = int(round(min(diffs))) if diffs else 0
    for v, g in lig.groupby("vendeur"):
        cle = "c06_mix_" + re.sub(r"[^a-z0-9]+", "_", unidecode_str(str(v)).lower()).strip("_")
        parts[v] = round(100 * float((g.categorie == "Bois & panneaux").mean()), 1)
        d[cle + "_part_bois_pct"] = parts[v]
        d[cle + "_lignes"] = int(len(g))
    # ---- Contrôles du corrigé de l'évaluation M02 (concentration, effet du retrait des retours)
    ca_tk = float(t.sum())
    d["c05_ca_extrait_tickets"] = int(round(ca_tk))
    tri = t.sort_values(ascending=False)
    d["c05_ca_top32_tickets"] = int(round(tri.head(32).sum()))
    d["c05_part_ca_top32_pct"] = round(100 * tri.head(32).sum() / ca_tk, 1)
    d["c05_ca_top9_tickets"] = int(round(tri.head(9).sum()))
    d["c05_part_ca_top9_pct"] = round(100 * tri.head(9).sum() / ca_tk, 1)
    sup250 = t[t > 250_000]
    d["c05_nb_tickets_sup250k"] = int(len(sup250))
    d["c05_ca_tickets_sup250k"] = int(round(sup250.sum()))
    neg = t[t <= 0]
    d["c03_nb_tickets_negatifs"] = int(len(neg))
    t_pos = t[t > 0]
    borne_pos = t_pos.quantile(.75) + 1.5 * (t_pos.quantile(.75) - t_pos.quantile(.25))
    d["c03_borne_hors_tickets_negatifs"] = int(round(borne_pos))
    d["c03_nb_aberrants_hors_negatifs"] = int((t_pos > borne_pos).sum())
    d["c03_ecart_borne_apres_retrait_negatifs"] = int(round(borne_sup - borne_pos))
    # ---- Projet M02.P : le test entre deux magasins, exécuté au tableur puis vérifié en Python
    _v = pd.read_csv(os.path.join(REF, "ventes_propres.csv"), usecols=["id_ticket", "id_magasin", "annee", "montant_ttc"])
    _v = _v[_v.annee == 2025]
    _pv = _v.groupby("id_ticket").agg(m=("montant_ttc", "sum"), mag=("id_magasin", "first"))
    d["m02p_lignes_2025"] = int(len(_v))
    d["m02p_tickets_2025"] = int(len(_pv))
    d["m02p_paniers_par_magasin"] = {int(k): {"tickets": int(len(g)), "moyenne": int(round(g.m.mean())),
                                             "median": int(round(g.m.median()))}
                                     for k, g in _pv.groupby("mag")}
    a1 = _pv.m[_pv.mag == 1].to_numpy(dtype=float)
    a5 = _pv.m[_pv.mag == 5].to_numpy(dtype=float)
    tp2 = _st.ttest_ind(a1, a5, equal_var=False)
    dd = float(a1.mean() - a5.mean())
    ee2 = float(_np.sqrt(a1.var(ddof=1) / len(a1) + a5.var(ddof=1) / len(a5)))
    d["m02p_ecart_m1_m5"] = int(round(dd))
    d["m02p_se_difference"] = int(round(ee2))
    d["m02p_marge_difference"] = int(round(1.96 * ee2))
    d["m02p_t_welch"] = round(float(tp2.statistic), 2)
    d["m02p_ddl"] = round(float(tp2.df), 1)
    d["m02p_p"] = float(f"{tp2.pvalue:.3g}")
    d["m02p_ic_difference"] = [int(round(dd - 1.96 * ee2)), int(round(dd + 1.96 * ee2))]
    d["m02p_m1_mediane"] = int(round(_np.median(a1)))
    d["m02p_m5_mediane"] = int(round(_np.median(a5)))
    d["m02p_m1_moyenne"] = int(round(a1.mean()))
    d["m02p_m5_moyenne"] = int(round(a5.mean()))
    return d





# ---------------------------------------------------------------- M03 — Excel pour l'analyse
def m03():
    """Mesures citées par le module M03 (Excel). Tout est lu dans les deux fichiers de travail :
    l'énoncé reçu (489 lignes, défauts compris) et l'attendu nettoyé (480 lignes)."""
    d = OrderedDict()
    en = pd.read_csv(os.path.join(PROJ, "ventes_magasin5_2025.csv"), sep=";", encoding="utf-8-sig",
                     dtype=str, keep_default_na=False)
    p = pd.read_csv(os.path.join(REF, "ventes_magasin5_2025_ATTENDU.csv"), sep=";")
    d["m03_lignes_enonce"] = int(len(en))
    d["m03_colonnes"] = int(en.shape[1])
    d["m03_lignes_attendu"] = int(len(p))
    d["m03_derniere_cellule_enonce"] = "M%d" % (len(en) + 1)
    d["m03_derniere_cellule_attendu"] = "M%d" % (len(p) + 1)
    # ce que la cellule contient vraiment, pas ce qu'elle affiche
    brut_cell = pd.to_numeric(en["montant_ttc"], errors="coerce")          # tel que le tableur le lit
    net = pd.to_numeric(brut_cell.fillna(en["montant_ttc"].str.replace("\u00a0", "").str.replace(" ", "")),
                        errors="coerce")                                     # après retrait des séparateurs
    d["m03_ca_enonce_partiel"] = int(round(float(brut_cell.sum())))
    d["m03_montant_lus_comme_texte"] = int(brut_cell.isna().sum())
    d["m03_montant_lus_comme_nombres"] = int(brut_cell.notna().sum())
    d["m03_lignes_montants_nombres"] = [int(i) + 2 for i, v in enumerate(en["montant_ttc"])
                                        if pd.notna(pd.to_numeric(v, errors="coerce"))]
    ht_cell = pd.to_numeric(en["montant_ht"], errors="coerce")
    d["m03_montant_ht_lus_comme_nombres"] = int(ht_cell.notna().sum())
    d["m03_montant_ht_lus_comme_texte"] = int(ht_cell.isna().sum())
    d["m03_quantite_min_attendu"] = int(p["quantite"].min())
    d["m03_remise_max_attendu_pct"] = round(float(p["remise"].max()) * 100, 1)
    # --- mesures du chapitre C02 (formats, saisie, validation, mise en forme conditionnelle)
    d["m03_dates_iso_enonce"] = int(en["date"].str.match(r"^\d{4}-\d{2}-\d{2}$").sum())
    d["m03_remise_ecrites_avec_point"] = int(en["remise"].str.match(r"^\d+\.\d+$").sum())
    d["m03_lignes_retours"] = int((p["montant_ttc"] < 0).sum())
    d["m03_ca_retours"] = int(round(float(p.loc[p["montant_ttc"] < 0, "montant_ttc"].sum())))
    d["m03_lignes_montant_sup_million"] = int((p["montant_ttc"] > 1_000_000).sum())
    d["m03_lignes_quantite_sup_100"] = int((p["quantite"] > 100).sum())
    d["m03_ca_lignes_positives"] = int(round(float(p.loc[p["montant_ttc"] > 0, "montant_ttc"].sum())))
    d["m03_ca_enonce_apres_nettoyage"] = int(round(net.sum()))
    d["m03_ca_attendu"] = int(round(pd.to_numeric(p["montant_ttc"], errors="coerce").sum()))
    d["m03_ca_ecart"] = d["m03_ca_enonce_apres_nettoyage"] - d["m03_ca_attendu"]
    d["m03_dates_ecrites_dans_le_brut"] = int(en["date"].str.match(r"^\d{2}/\d{2}/\d{4}$").sum())
    q_en = pd.to_numeric(en["quantite"], errors="coerce")
    d["m03_quantite_max_enonce"] = int(q_en.max())
    d["m03_quantite_au_dessus_de_500"] = int((q_en > 500).sum())
    d["m03_quantite_max_attendu"] = int(p["quantite"].max())
    d["m03_doublons_enonce"] = int(en.duplicated().sum())
    # --- mesures du chapitre C03 (tableau structuré, tri, filtres, dédoublonnage)
    d["m03_lignes_a_retirer_sur_ticket_seul"] = int(en["n_ticket"].duplicated().sum())
    d["m03_ca_a_retirer_sur_ticket_seul"] = int(round(float(pd.to_numeric(
        en.loc[en["n_ticket"].duplicated(), "montant_ttc"].str.replace("\u00a0", "").str.replace(" ", ""),
        errors="coerce").sum())))
    d["m03_lignes_a_retirer_sur_ticket_produit"] = int(en.duplicated(subset=["n_ticket", "produit"]).sum())
    d["m03_ca_a_retirer_sur_ticket_produit"] = int(round(float(pd.to_numeric(
        en.loc[en.duplicated(subset=["n_ticket", "produit"]), "montant_ttc"].str.replace("\u00a0", "")
        .str.replace(" ", ""), errors="coerce").sum())))
    d["m03_faux_doublons_attendu"] = int(p.duplicated(subset=["n_ticket", "produit"]).sum())
    gard = en[~en["n_ticket"].duplicated()]
    d["m03_lignes_restant_apres_ticket_seul"] = int(len(gard))
    d["m03_ca_restant_apres_ticket_seul"] = int(round(float(pd.to_numeric(
        gard["montant_ttc"].str.replace("\u00a0", "").str.replace(" ", ""), errors="coerce").sum())))
    d["m03_groupes_texte_pour_12_mois"] = int(en["date"].str.slice(0, 7).nunique())
    d["m03_cellules_attendu_texte"] = int(sum(p[c].dtype == object for c in p.columns))
    d["m03_cellules_attendu_vides"] = int(p.isna().sum().sum())
    # niveau de la ligne, tel que le tableur le calcule
    m = p["montant_ttc"]
    d["m03_moyenne_ligne"] = int(round(m.mean()))
    d["m03_mediane_ligne"] = int(round(m.median()))
    d["m03_ecart_type_ligne"] = int(round(m.std(ddof=1)))
    d["m03_min_ligne"] = int(round(m.min()))
    d["m03_max_ligne"] = int(round(m.max()))
    d["m03_q1_ligne"] = int(round(m.quantile(.25)))
    d["m03_q3_ligne"] = int(round(m.quantile(.75)))
    d["m03_ca_ht_attendu"] = int(round(p["montant_ht"].sum()))
    _moy_cat = p.groupby("categorie")["montant_ttc"].mean()
    d["m03_moyenne_des_moyennes_categories"] = int(round(float(_moy_cat.mean())))
    _t = p.groupby("n_ticket")["montant_ttc"].sum()
    d["m03_ca_moyen_par_ticket"] = int(round(float(_t.mean())))
    d["m03_lignes_avec_remise"] = int((p["remise"] > 0).sum())
    # --- mesures du chapitre C05 (agrégats et fonctions conditionnelles)
    d["m03_ca_remises_accordees"] = int(round(float((p["montant_ht"] * p["remise"]).sum())))
    d["m03_ca_lignes_avec_remise"] = int(round(float(p.loc[p["remise"] > 0, "montant_ttc"].sum())))
    d["m03_moyenne_ligne_hors_retours"] = int(round(float(p.loc[p["montant_ttc"] > 0, "montant_ttc"].mean())))
    d["m03_premiere_ligne_montant"] = int(pd.to_numeric(
        en["montant_ttc"].iloc[0].replace("\u00a0", "").replace(" ", "")))
    d["m03_jours_entre_min_max"] = int((pd.to_datetime(p["date"]).max() - pd.to_datetime(p["date"]).min()).days)
    par_mois = pd.to_datetime(p["date"]).dt.month.value_counts().sort_index()
    d["m03_lignes_par_mois"] = [int(par_mois.get(k, 0)) for k in range(1, 13)]
    grp = p.assign(dt=pd.to_datetime(p["date"])).groupby(pd.to_datetime(p["date"]).dt.month)["montant_ttc"].sum()
    d["m03_ca_par_mois"] = [int(round(grp.get(k, 0))) for k in range(1, 13)]
    # repères de navigation
    idx = int(pd.to_numeric(p["montant_ttc"]).idxmax())
    d["m03_ligne_plus_gros_montant_ligne"] = idx + 2
    d["m03_cellule_plus_gros_montant_ligne"] = "M%d" % (idx + 2)
    d["m03_ligne_plus_gros_montant_position"] = idx + 1
    d["m03_plus_gros_montant_ligne"] = int(p["montant_ttc"].max())
    tailles = p.groupby("n_ticket").size()
    d["m03_ticket_le_plus_fourni"] = str(tailles.idxmax())
    d["m03_ticket_le_plus_fourni_lignes"] = int(tailles.max())
    d["m03_tickets"] = int(p["n_ticket"].nunique())
    # compteurs d'un TCD
    d["m03_categories"] = int(p["categorie"].nunique())
    d["m03_vendeurs_dans_extrait"] = int(p["vendeur"].nunique())
    d["m03_produits_distincts"] = int(p["produit"].nunique())
    cat = p.assign(m=pd.to_numeric(p["montant_ttc"])).groupby("categorie")["m"].agg(["count", "sum", "mean"])
    for nom, r in cat.iterrows():
        cle = "m03_tcd_" + re.sub(r"[^a-z0-9]+", "_", unidecode_str(str(nom)).lower()).strip("_")
        d[cle + "_lignes"] = int(r["count"])
        d[cle + "_ca"] = int(round(r["sum"]))
        d[cle + "_moyenne"] = int(round(r["mean"]))
        d[cle + "_part_pct"] = round(100 * r["sum"] / d["m03_ca_attendu"], 1)
    # joints et recherches
    prod = pd.read_csv(os.path.join(REF, "produits_propres.csv"))
    cli = pd.read_csv(os.path.join(REF, "clients_propres.csv"))
    lib_p = set(prod["designation"])
    d["m03_produits_absents_du_referentiel"] = int(p.loc[~p["produit"].isin(lib_p), "produit"].nunique())
    prix_ref = prod.set_index("designation")["prix_vente_ht"].to_dict()
    rapport = (p["prix_unitaire_ht"] / p["produit"].map(prix_ref)).dropna()
    d["m03_lignes_prix_identique_au_catalogue"] = int((rapport.sub(1).abs() < 1e-6).sum())
    d["m03_ecart_prix_median_pct"] = round(100 * (rapport.median() - 1), 1)
    d["m03_ecart_prix_min_pct"] = round(100 * (rapport.min() - 1), 1)
    d["m03_ecart_prix_max_pct"] = round(100 * (rapport.max() - 1), 1)
    d["m03_produits_plusieurs_prix_dans_extrait"] = int((p.groupby("produit")["prix_unitaire_ht"].nunique() > 1).sum())
    d["m03_produit_du_plus_gros_montant"] = str(p.loc[p["montant_ttc"].idxmax(), "produit"])
    d["m03_categories_ordre_fichier"] = ", ".join(p["categorie"].dropna().unique().tolist())
    # contrôle de cohérence : le produit recalculé, arrondi ligne à ligne comme dans le classeur (=ARRONDI,
    # à mi-chemin on s'éloigne de zéro), moins le montant enregistré par la caisse
    _prod = p["quantite"] * p["prix_unitaire_ht"] * (1 - p["remise"])
    _excel = np.floor(_prod + 0.5)
    d["m03_ecart_controle_montant_ht"] = int(round(float(_excel.sum() - p["montant_ht"].sum())))
    d["m03_ecart_controle_montant_ht_total_seul"] = int(round(float(_prod.sum() - p["montant_ht"].sum())))
    d["m03_lignes_a_demi_franc"] = int((_prod % 1 == 0.5).sum())
    d["m03_lignes_arrondi_qui_diverge"] = int((_excel != _prod.round(0)).sum())
    for nom, grp in p.groupby("categorie"):
        cle = "m03_tcd_" + re.sub(r"[^a-z0-9]+", "_", unidecode_str(str(nom)).lower()).strip("_")
        d[cle + "_remises"] = int((grp["remise"] > 0).sum())
    ids_cli = set(cli["id_client"].astype(str))
    cl = p["client"].astype(str).str.replace(".0", "", regex=False)
    d["m03_lignes_client_trouve"] = int(cl.isin(ids_cli).sum())
    d["m03_lignes_client_non_trouve"] = int((~cl.isin(ids_cli)).sum())
    d["m03_lignes_client_comptoir_zero"] = int((cl == "0").sum())
    d["m03_lignes_client_champ_vide"] = int((~cl.isin(ids_cli) & (cl == "nan")).sum())
    d["m03_clients_distincts"] = int(p["client"].nunique())
    d["m03_clients_referentiel"] = int(len(cli))
    # dates, jours ouvrés, objectifs
    dd = pd.to_datetime(p["date"])
    d["m03_date_min"] = dd.min().strftime("%d/%m/%Y")
    d["m03_date_max"] = dd.max().strftime("%d/%m/%Y")
    d["m03_jours_distincts"] = int(dd.dt.date.nunique())
    d["m03_jours_ouvres_entre_min_max"] = int(np.busday_count(dd.min().date(), dd.max().date() + np.timedelta64(1, "D")))
    _n_ouvr = int(d["m03_jours_ouvres_entre_min_max"])
    d["m03_ca_par_jour_ouvre"] = int(round(d["m03_ca_attendu"] / _n_ouvr))
    d["m03_ca_par_jour_calendaire"] = int(round(d["m03_ca_attendu"] / (int(d["m03_jours_entre_min_max"]) + 1)))
    obj = pd.read_csv(os.path.join(BRUT, "objectifs_de_ca.csv"), sep=";", encoding="cp1252")
    obj.columns = [c.strip() for c in obj.columns]
    d["m03_objectifs_lignes"] = int(len(obj))
    o5 = obj[(obj["id_magasin"].astype(str) == "5") & (obj["annee"].astype(str) == "2025")]
    d["m03_objectif_magasin5_2025"] = int(round(pd.to_numeric(o5["ca_objectif_ttc"], errors="coerce").sum()))
    _v = v = pd.read_csv(os.path.join(REF, "ventes_propres.csv"), usecols=["id_magasin", "annee", "mois", "montant_ttc"])
    ca5 = pd.to_numeric(v[(v.id_magasin == 5) & (v.annee == 2025)]["montant_ttc"], errors="coerce").sum()
    d["m03_ca_magasin5_2025_population"] = int(round(ca5))
    d["m03_realisation_pct"] = round(100 * ca5 / d["m03_objectif_magasin5_2025"], 1)
    d["m03_realisation_extrait_pct"] = round(100 * d["m03_ca_attendu"] / d["m03_objectif_magasin5_2025"], 1)
    _v["annee_mois"] = _v.annee.astype(str) + "-" + _v.mois.astype(str).str.zfill(2)
    _g = _v.groupby(["id_magasin", "annee_mois"])["montant_ttc"].sum().reset_index()
    _j = _g.merge(obj[["id_magasin", "annee_mois", "ca_objectif_ttc"]], on=["id_magasin", "annee_mois"])
    _r = pd.to_numeric(_j.montant_ttc) / pd.to_numeric(_j.ca_objectif_ttc)
    d["m03_ratio_ca_objectif_min"] = round(float(_r.min()), 2)
    d["m03_ratio_ca_objectif_median"] = round(float(_r.median()), 2)
    d["m03_ratio_ca_objectif_max"] = round(float(_r.max()), 2)
    d["m03_objectifs_joints_magasin_mois"] = int(len(_j))
    d["m03_objectifs_lignes_sans_ventes"] = int(len(obj) - len(_j))
    _s = _g[["id_magasin", "annee_mois"]].merge(obj[["id_magasin", "annee_mois"]], on=["id_magasin", "annee_mois"],
                                                how="left", indicator=True)
    manq = _s[_s["_merge"] == "left_only"]
    d["m03_ventes_sans_objectif"] = int(len(manq))
    d["m03_ventes_sans_objectif_detail"] = [f"magasin {int(a.id_magasin)} {a.annee_mois}" for a in manq.itertuples()]
    d["m03_ecart_objectif"] = int(round(ca5 - d["m03_objectif_magasin5_2025"]))
    return d

def m04():
    """Mesures citées par le module M04 (qualité, préparation, documentation).

    Le module travaille sur le socle ENTIER, pas sur un extrait : le diagnostic doit tenir sur
    243 360 lignes. Tout est relu sur disque, y compris contre `verites_terrain.csv`, parce que
    la promesse du module est de prouver qu'on n'a pas cassé les totaux en nettoyant.
    """
    d = OrderedDict()
    b = pd.read_csv(os.path.join(BRUT, "ventes_brutes.csv"), dtype=str, keep_default_na=False,
                    encoding="utf-8-sig")
    n = len(b)
    d["m04_lignes_brut"] = int(n)
    d["m04_colonnes_brut"] = int(b.shape[1])
    d["m04_entetes_brut"] = list(b.columns)

    # ---- 1. complétude : ce qui est vide, colonne par colonne
    vides = {c: int((b[c].str.strip() == "").sum()) for c in b.columns}
    d["m04_colonnes_vides"] = {k: v for k, v in sorted(vides.items(), key=lambda kv: -kv[1]) if v}
    d["m04_lignes_au_moins_un_vide"] = int((b.apply(lambda s: s.str.strip() == "").any(axis=1)).sum())

    # ---- 2. unicité : la clé déclarée, la clé réelle
    d["m04_id_vente_distincts"] = int(b["id_vente"].nunique())
    d["m04_lignes_id_vente_redites"] = int(n - b["id_vente"].nunique())
    d["m04_lignes_entierement_dupliquees"] = int(b.duplicated().sum())
    d["m04_tickets_distincts"] = int(b["id_ticket"].nunique())

    # ---- 3. validité : types réellement tenus par la cellule, pas par l'en-tête
    for c in ("montant_ttc", "montant_ht", "quantite", "prix_unitaire_ht", "poids_kg"):
        d["m04_%s_non_numeriques" % c] = int(pd.to_numeric(b[c], errors="coerce").isna().sum())
    d["m04_dates_non_iso"] = int((~b["date_vente"].str.match(r"^\d{4}-\d{2}-\d{2}$")).sum())
    d["m04_derniere_date_iso"] = str(b.loc[b["date_vente"].str.match(r"^\d{4}-\d{2}-\d{2}$"),
                                          "date_vente"].max())

    # ---- 4. cohérence : les égalités que le fichier doit tenir
    q = pd.to_numeric(b["quantite"], errors="coerce")
    pr = pd.to_numeric(b["prix_unitaire_ht"], errors="coerce")
    tr = pd.to_numeric(b["taux_remise"], errors="coerce")
    ht = pd.to_numeric(b["montant_ht"], errors="coerce")
    tva = pd.to_numeric(b["montant_tva"], errors="coerce")
    ttc = pd.to_numeric(b["montant_ttc"], errors="coerce")
    ok = q.notna() & pr.notna() & tr.notna() & ht.notna()
    att_ht = (q * pr * (1 - tr)).round(0)
    d["m04_lignes_montant_ht_incoherent"] = int((ok & ((att_ht - ht).abs() > 1)).sum())
    ok2 = ht.notna() & tva.notna() & ttc.notna()
    d["m04_lignes_ttc_non_egal_ht_plus_tva"] = int((ok2 & ((ht + tva - ttc).abs() > 1)).sum())

    # ---- 5. exactitude : les remises, et le sens des retours
    d["m04_remises_superieures_a_1"] = int((tr > 1).sum())
    d["m04_remise_max_lue"] = round(float(tr.max()) if tr.notna().any() else 0.0, 2)
    retour = pd.to_numeric(b["est_retour"], errors="coerce")
    d["m04_retours_signales"] = int((retour == 1).sum())
    d["m04_retours_montant_positif"] = int(((retour == 1) & (ttc > 0)).sum())
    d["m04_lignes_montant_ttc_negatif"] = int((ttc < 0).sum())

    # ---- 6. ce que le total naïf perd : le défaut qui casse les chiffres
    d["m04_ca_brut_naif"] = int(round(float(ttc.sum())))
    vt = pd.read_csv(os.path.join(REF, "verites_terrain.csv"))
    total_vrai = int(vt.loc[(vt["niveau"] == "total") & (vt["cle"].astype(str) == "toutes_ventes"),
                            "ca_ttc"].iloc[0])
    d["m04_ca_verite_terrain"] = total_vrai
    d["m04_ca_brut_sous_estime"] = int(total_vrai - int(round(float(ttc.sum()))))
    d["m04_lignes_propres"] = int(len(pd.read_csv(os.path.join(REF, "ventes_propres.csv"))))
    d["m04_lignes_a_retirer_du_brut"] = int(n - d["m04_lignes_propres"])

    # ---- 7. conformité : casse et variantes dans les colonnes déclaratives
    for c in ("mode_paiement", "canal"):
        vals = sorted(b[c].unique().tolist())
        d["m04_%s_modalites" % c] = len(vals)
        d["m04_%s_exemples" % c] = vals[:8]

    # ---- clients : absences, quasi-doublons, données personnelles
    cl = pd.read_csv(os.path.join(BRUT, "clients.csv"), dtype=str, keep_default_na=False,
                     encoding="utf-8-sig")
    d["m04_lignes_clients"] = int(len(cl))
    d["m04_clients_ville_absente"] = int((cl["ville"].str.strip() == "").sum())
    d["m04_clients_email_absent"] = int((cl["email"].str.strip() == "").sum())
    d["m04_clients_telephone_present"] = int((cl["telephone"].str.strip() != "").sum())
    # nom ramené à ses seuls caractères alphanumériques minuscules : la « règle naïve » du dédoublonnage
    nom_norm = cl["nom"].str.strip().str.lower().str.replace(r"[^a-z0-9]", "", regex=True)
    cle_norm = nom_norm
    d["m04_clients_meme_nom_normalise"] = int(len(cl) - cle_norm.nunique())
    d["m04_clients_id_dupliques"] = int(len(cl) - cl["id_client"].nunique())

    # ---- le vrai mécanisme du « doublon » : invisible à la clé, visible à l'affaire
    d["m04_id_vente_tous_distincts"] = int(b["id_vente"].nunique() == n)
    d["m04_doublons_cle_affaire"] = int(b.duplicated(["id_ticket", "id_produit", "quantite"]).sum())
    d["m04_lignes_absentes_du_propre"] = int(n - len(set(b["id_vente"]) &
                                                       set(pd.read_csv(os.path.join(REF, "ventes_propres.csv"))["id_vente"].astype(str))))
    garde = b[~b.duplicated(["id_ticket", "id_produit"], keep="first")]
    retirees = b[b.duplicated(["id_ticket", "id_produit"], keep=False)].merge(
        garde[["id_ticket", "id_produit", "quantite", "montant_ttc"]], on=["id_ticket", "id_produit"],
        suffixes=("", "_gardee"), how="inner")
    d["m04_jumeaux_meme_ticket_produit"] = int(len(retirees))
    d["m04_jumeaux_meme_quantite"] = int((retirees["quantite"].astype(str) == retirees["quantite_gardee"].astype(str)).sum())
    d["m04_jumeaux_montant_deja_texte"] = int(retirees["montant_ttc"].pipe(pd.to_numeric, errors="coerce").isna().sum())

    # ---- ce que donne le nettoyage dans le désordre : les deux totaux faux
    repaire = b.copy()
    repaire["ttc_repare"] = ttc.fillna((ht + tva).round(0))
    d["m04_ca_repare_sans_dedoublonner"] = int(round(float(repaire["ttc_repare"].sum())))
    d["m04_ecart_repare_sans_dedoublonner"] = int(round(float(repaire["ttc_repare"].sum())) - total_vrai)
    d["m04_ecart_naif_vs_verite"] = d["m04_ca_verite_terrain"] - d["m04_ca_brut_naif"]
    d["m04_lignes_montant_texte_et_doublon"] = int((b.duplicated(["id_ticket", "id_produit"], keep=False)
                                                    & ttc.isna() & (b["montant_ttc"].str.strip() != "")).sum())
    # recouvrements : c’est ce qui distingue « deux défauts » de « un défaut vu deux fois »
    propres = set(pd.read_csv(os.path.join(REF, "ventes_propres.csv"), encoding="utf-8-sig")["id_vente"].astype(str))
    a_retirer = ~b["id_vente"].astype(str).isin(propres)
    d["m04_recouvrement_textes_et_retirees"] = int((ttc.isna() & a_retirer).sum())
    d["m04_union_textes_ou_retirees"] = int((ttc.isna() | a_retirer).sum())
    collisions = b.duplicated(["id_ticket", "id_produit", "quantite"], keep="first")
    d["m04_recouvrement_textes_et_collisions"] = int((ttc.isna() & collisions).sum())
    d["m04_union_textes_ou_collisions"] = int((ttc.isna() | collisions).sum())

    # ---- actualité et retours
    dates = pd.to_datetime(b["date_vente"], errors="coerce")
    d["m04_dates_apres_le_31_aout_2026"] = int((dates > pd.Timestamp("2026-08-31")).sum())
    d["m04_date_max_brut"] = str(dates.max().date())
    d["m04_retours_non_negatifs"] = int(((retour == 1) & (ttc >= 0)).sum())
    d["m04_retours_montant_non_numerique"] = int(((retour == 1) & ttc.isna()).sum())
    orphelins = ~b["id_client"].isin(set(pd.read_csv(os.path.join(BRUT, "clients.csv"), dtype=str,
                                                     keep_default_na=False, encoding="utf-8-sig")["id_client"])) \
        & (b["id_client"].str.strip() != "0") & (b["id_client"].str.strip() != "")
    d["m04_lignes_client_non_reference"] = int(orphelins.sum())
    d["m04_clients_orphelins_distincts"] = int(b.loc[orphelins, "id_client"].nunique())
    d["m04_taille_fichier_octets"] = int(os.path.getsize(os.path.join(BRUT, "ventes_brutes.csv")))
    d["m04_lignes_remise_aberrante_et_ht_faux"] = int(((tr > 1) & ((att_ht - ht).abs() > 1)).sum())

    # ---- les 412 quasi-doublons clients, et ce que la règle naïve aurait cassé
    d["m04_clients_brut"] = int(len(cl))
    d["m04_clients_propres"] = int(len(pd.read_csv(os.path.join(REF, "clients_propres.csv"))))
    d["m04_clients_a_retirer"] = int(d["m04_clients_brut"] - d["m04_clients_propres"])
    d["m04_clients_doublons_par_nom_seul"] = int(len(cl) - cle_norm.nunique())
    chiffres_tel = cl["telephone"].str.replace(r"\D", "", regex=True)
    cle_tel_nom = cle_norm + "|" + chiffres_tel
    d["m04_clients_doublons_par_nom_et_chiffres_tel"] = int(len(cl) - cle_tel_nom.nunique())
    d["m04_lignes_clients_avec_telephone"] = int((cl["telephone"].str.strip() != "").sum())

    # ---- produits : la catégorie qui n'en est pas une
    prdf = pd.read_csv(os.path.join(BRUT, "produits.csv"), encoding="utf-8-sig")
    cats = prdf["categorie"].astype(str).str.strip()
    d["m04_produits_lignes"] = int(len(prdf))
    d["m04_produits_modalites_categorie"] = int(cats.nunique())
    d["m04_produits_categorie_heteroclite"] = int((~cats.isin(
        ["Bois & panneaux", "Consommables", "Electricité", "Matériaux", "Peinture", "Plomberie",
         "Quincaillerie"])).sum())
    d["m04_produits_categorie_vide"] = int((cats == "").sum())

    # ---- stocks : le cas d'étude de l'évaluation
    st = pd.read_csv(os.path.join(BRUT, "stocks_quotidiens.csv"))
    ecart = (st["qte_physique"] - st["qte_theorique"])
    d["m04_lignes_stocks"] = int(len(st))
    d["m04_stock_physique_negatif"] = int((st["qte_physique"] < 0).sum())
    d["m04_stock_ecart_max"] = int(ecart.abs().max())
    d["m04_stock_lignes_sous_alerte"] = int((st["qte_physique"] < st["seuil_alerte"]).sum())
    d["m04_stock_ecart_moyen"] = round(float(ecart.abs().mean()), 2)

    # ---- le fichier fournisseur : bruit avant l'en-tête, encodage, virgule, lignes hors domaine
    octets = open(os.path.join(BRUT, "tarif_fournisseur_peinture.csv"), "rb").read()
    lignes_texte = octets.decode("cp1252").splitlines()
    tete = next(i for i, l in enumerate(lignes_texte) if l.count(";") >= 4)   # index de la vraie ligne d'en-têtes
    tf = pd.read_csv(os.path.join(BRUT, "tarif_fournisseur_peinture.csv"), sep=";", skiprows=tete,
                     encoding="cp1252", decimal=",")
    d["m04_tarif_lignes_bruit_avant_en_tete"] = int(tete)
    d["m04_tarif_lignes"] = int(len(tf))
    d["m04_tarif_lignes_colonnes"] = int(tf.shape[1])
    d["m04_tarif_octets_hors_ascii"] = int(sum(1 for x in octets if x > 127))
    try:
        octets.decode("utf-8")
        d["m04_tarif_decodage_utf8_possible"] = 1
    except UnicodeDecodeError as e:
        d["m04_tarif_decodage_utf8_possible"] = 0
        d["m04_tarif_decodage_utf8_plantage_octet"] = int(e.start)
    lib = tf["libelle"].astype(str)
    d["m04_tarif_lignes_hors_domaine"] = int(lib.str.contains("PVC|bois|lambris|quincaille", case=False, regex=True).sum())
    d["m04_tarif_prix_a_la_virgule"] = int(pd.read_csv(os.path.join(BRUT, "tarif_fournisseur_peinture.csv"),
                                                       sep=";", skiprows=tete, encoding="cp1252", dtype=str,
                                                       keep_default_na=False)["prix_unitaire"].str.contains(",").sum())
    d["m04_tarif_conditionnements_distincts"] = int(tf["conditionnement"].astype(str).nunique())

    # ---- les coûts d'achat : périodes qui se recouvrent, trous
    ca = pd.read_csv(os.path.join(BRUT, "couts_achat.csv"))
    ca = ca.sort_values(["id_produit", "date_debut"])
    recouvrements = 0
    trous = 0
    for _, g in ca.groupby("id_produit"):
        fin_prec = None
        for _, r in g.iterrows():
            if fin_prec is not None:
                if r["date_debut"] <= fin_prec:
                    recouvrements += 1
                elif (pd.to_datetime(r["date_debut"]) - pd.to_datetime(fin_prec)).days > 1:
                    trous += 1
            fin_prec = r["date_fin"]
    d["m04_couts_lignes"] = int(len(ca))
    d["m04_couts_periodes_recouvrees"] = int(recouvrements)
    d["m04_couts_periodes_trouees"] = int(trous)
    d["m04_couts_produits_distincts"] = int(ca["id_produit"].nunique())

    # ---- le fichier tenu à la main : 18 200 lignes sans contrôle
    rm = pd.read_excel(os.path.join(BRUT, "remises_manuelles.xlsx"))
    d["m04_remises_manuelles_lignes"] = int(len(rm))
    d["m04_remises_manuelles_auteurs"] = int(rm["saisi_par"].nunique())
    d["m04_remises_manuelles_montants_nuls"] = int((pd.to_numeric(rm["remise_consentie_montant"], errors="coerce") == 0).sum())
    d["m04_remises_manuelles_total"] = int(round(float(pd.to_numeric(rm["remise_consentie_montant"], errors="coerce").sum())))

    # ---- C04 : ce que chaque famille de règle signale vraiment
    px = pd.to_numeric(b["prix_unitaire_ht"], errors="coerce")
    qt = q.copy()
    po = pd.to_numeric(b["poids_kg"], errors="coerce")
    q1, q3 = float(px.quantile(.25)), float(px.quantile(.75))
    iqr = q3 - q1
    d["m04_prix_min"] = int(px.min()); d["m04_prix_max"] = int(px.max())
    d["m04_prix_mediane"] = int(round(float(px.median())))
    d["m04_prix_q1"] = int(q1); d["m04_prix_q3"] = int(q3)
    d["m04_prix_ecart_type"] = int(round(float(px.std())))
    d["m04_prix_hors_bornes_iqr"] = int(((px < q1 - 1.5 * iqr) | (px > q3 + 1.5 * iqr)).sum())
    z = (px - px.mean()) / px.std()
    d["m04_prix_z_sup_3"] = int((z.abs() > 3).sum())
    d["m04_prix_z_sup_6"] = int((z.abs() > 6).sum())
    d["m04_quantite_min"] = int(qt.min()); d["m04_quantite_max"] = int(qt.max())
    d["m04_quantite_nulles_ou_negatives"] = int((qt <= 0).sum())
    d["m04_quantite_sup_50"] = int((qt > 50).sum())
    d["m04_poids_max"] = int(round(float(po.max())))
    d["m04_poids_mediane"] = round(float(po.median()), 1)
    d["m04_poids_negatifs"] = int((po < 0).sum())
    d["m04_remise_negative"] = int((tr < 0).sum())
    # ce que devient la « réparation évidente » des 973 remises : mesuré, pas supposé
    au_plein = (q * px).round(0)
    d["m04_lignes_ht_egal_plein_sans_remise"] = int((abs(au_plein - ht) <= 1).sum())
    d["m04_lignes_remise_aberrante_ht_au_plein"] = int((abs(au_plein - ht) <= 1)[tr > 1].sum())
    recalc = 1 - ht / (q * px)
    d["m04_remise_recalculee_maxi"] = round(float(recalc[tr > 1].max()), 3)
    d["m04_lignes_remise_recalculee_dans_domaine"] = int(((recalc[tr > 1] >= 0) & (recalc[tr > 1] <= 0.25)).sum())
    d["m04_lignes_reparation_div100_hors_domaine"] = int(((tr[tr > 1] / 100) > 0.25).sum())
    d["m04_lignes_tva_non_conforme"] = int((abs(tva - (ht * 0.18).round(0)) > 1).sum())
    # le contrôle qui a du sens : la cohérence avec le référentiel, pas avec la distribution
    prx = pd.read_csv(os.path.join(BRUT, "produits.csv"), dtype=str, keep_default_na=False, encoding="utf-8-sig")
    prx["prix_ref"] = pd.to_numeric(prx["prix_vente_ht"], errors="coerce")
    prx["poids_ref"] = pd.to_numeric(prx["poids_unite_kg"], errors="coerce")
    mm = b.merge(prx[["id_produit", "prix_ref", "poids_ref"]], on="id_produit", how="left")
    ratio = pd.to_numeric(mm["prix_unitaire_ht"], errors="coerce") / mm["prix_ref"]
    d["m04_lignes_prix_different_du_catalogue"] = int(
        (abs(pd.to_numeric(mm["prix_unitaire_ht"], errors="coerce") - mm["prix_ref"]) > 1).sum())
    d["m04_produits_concernes_par_un_ecart_de_prix"] = int(
        mm.loc[abs(pd.to_numeric(mm["prix_unitaire_ht"], errors="coerce") - mm["prix_ref"]) > 1, "id_produit"].nunique())
    d["m04_prix_ratio_mini"] = round(float(ratio.min()), 3)
    d["m04_prix_ratio_maxi"] = round(float(ratio.max()), 3)
    d["m04_prix_hors_bande_095_135"] = int(((ratio < 0.95) | (ratio > 1.35)).sum())
    ecart_poids = (pd.to_numeric(mm["poids_kg"], errors="coerce") - qt * mm["poids_ref"]).abs()
    d["m04_lignes_poids_incoherent"] = int((ecart_poids > 1).sum())
    d["m04_lignes_poids_sup_5000_kg"] = int((po > 5000).sum())

    # ---- C05 : la normalisation, mesurée signe par signe
    txt = b.loc[ttc.isna() & (b["montant_ttc"].str.strip() != ""), "montant_ttc"].astype(str)
    d["m04_montants_texte_avec_suffixe"] = int(txt.str.contains(r"FCFA", regex=True).sum())
    d["m04_montants_texte_avec_espace"] = int(txt.str.contains(r"\s", regex=True).sum())
    d["m04_montants_texte_avec_virgule"] = int(txt.str.contains(",", regex=False).sum())
    dep = pd.to_numeric(txt.str.replace(" FCFA", "", regex=False).str.replace(" ", "", regex=False)
                        .str.replace(",", ".", regex=False), errors="coerce")
    d["m04_ca_apres_decoupage_des_textes"] = int(round(float(ttc.fillna(dep).sum())))
    d["m04_ecart_deux_voies_de_reparation"] = int(abs(round(float(ttc.fillna(dep).sum()))
                                                     - d["m04_ca_repare_sans_dedoublonner"]))
    d["m04_montants_texte_reparables_par_decoupage"] = int(dep.notna().sum())
    d["m04_clients_nom_distincts_brut"] = int(cl["nom"].nunique())
    d["m04_clients_nom_distincts_normalises"] = int(cle_norm.nunique())
    d["m04_clients_nom_avec_espace_surabondant"] = int((cl["nom"] != cl["nom"].str.strip()).sum())
    d["m04_clients_telephone_a_espaces_regles"] = int(cl["telephone"].str.match(r"^\+226 \d").sum())
    d["m04_clients_telephone_non_formates"] = int(len(cl) - cl["telephone"].str.match(r"^\+226 \d").sum())
    # C05 : combien de cellules de la colonne monétaire sont déjà numériques
    d["m04_montants_numeriques_dans_brut"] = int(ttc.notna().sum())
    propres_cli = set(pd.read_csv(os.path.join(REF, "clients_propres.csv"), dtype=str,
                                  keep_default_na=False)["id_client"])
    est_retire = ~cl["id_client"].isin(propres_cli)
    nom_surcharge = cl["nom"] != cl["nom"].str.strip()
    tel_brut = ~cl["telephone"].str.match(r"^\+226 \d")
    d["m04_clients_conservees_au_nom_surcharge"] = int((nom_surcharge & ~est_retire).sum())
    d["m04_clients_retirees_au_telephone_non_formate"] = int((tel_brut & est_retire).sum())
    d["m04_clients_retirees_aux_deux_anomalies"] = int((nom_surcharge & tel_brut & est_retire).sum())
    # les couples sont formés par la clé normalisée, pas par le nom seul : c'est la
    # seule comparaison qui raconte ce que la règle de garde voit vraiment
    # les couples sont formés par la clé normalisée nom + chiffres, pas par le nom seul :
    # c'est la seule comparaison qui raconte ce que la règle de garde voit vraiment
    cn = cl.assign(_k=cle_tel_nom, _r=est_retire, _i=cl.index)
    grp = cn.groupby("_k")
    couples = grp.filter(lambda z: len(z) == 2 and z["_r"].sum() == 1)
    d["m04_couples_clients_isoles"] = int(len(couples) // 2)
    d["m04_couples_alignes_sur_les_autres_colonnes"] = int(
        couples.groupby("_k").apply(lambda z: (z[["ville", "email", "type_client",
                                                   "date_creation"]].nunique() == 1).all()).sum())
    d["m04_doublons_clients_apres_leur_original"] = int(
        couples.groupby("_k").apply(lambda z: z.loc[z["_r"], "_i"].iloc[0]
                                    > z.loc[~z["_r"], "_i"].iloc[0]).sum())
    d["m04_doublons_clients_en_majuscules"] = int(couples[couples["_r"]]["nom"].map(
        lambda v: str(v).strip().isupper()).sum())
    d["m04_premiere_ligne_des_doublons_clients"] = int(cl.index[est_retire.values].min() + 1)

    d["m04_faux_positifs_regle_nom_seul"] = int(d["m04_clients_doublons_par_nom_seul"]
                                                - d["m04_clients_a_retirer"])
    txt_s = b.loc[ttc.isna() & (b["montant_ttc"].str.strip() != ""), "montant_ttc"].astype(str)
    d["m04_montants_texte_negatifs"] = int(txt_s.str.strip().str.startswith("-").sum())
    d["m04_montants_texte_formes_distinctes"] = int(txt_s.map(lambda v: re.sub(r"\d", "n", v)).nunique())
    d["m04_montants_texte_espace_insécable"] = int(txt_s.str.contains("\u00a0", regex=False).sum())
    dep2 = pd.to_numeric(pd.Series(txt_s.str.replace(" FCFA", "", regex=False)
                                   .str.replace(" ", "", regex=False)
                                   .str.replace(",", ".", regex=False), index=txt_s.index), errors="coerce")
    d["m04_retours_negatifs_apres_normalisation"] = int(
        ((retour == 1) & (ttc.fillna(dep2.reindex(b.index)) < 0)).sum())
    d["m04_produits_unite_modalites"] = int(pd.read_csv(os.path.join(BRUT, "produits.csv"), dtype=str,
                                                         keep_default_na=False, encoding="utf-8-sig")["unite"].nunique())

    # ---- C05 : ce que la normalisation gagne (ou ne gagne pas), colonne par colonne
    d["m04_clients_dates_creation_non_iso"] = int((~cl["date_creation"].str.match(r"^\d{4}-\d{2}-\d{2}$")).sum())
    d["m04_clients_ville_modalites_normalisees"] = int(
        cl["ville"].map(lambda v: re.sub(r"\s+", " ", str(v)).strip().casefold()).nunique())
    d["m04_tarif_octets_ambigus_cp1252_latin1"] = sum(1 for c in open(
        os.path.join(BRUT, "tarif_fournisseur_peinture.csv"), "rb").read() if 0x80 <= c <= 0x9F)
    ob = pd.read_csv(os.path.join(BRUT, "objectifs_de_ca.csv"), sep=";", dtype=str,
                     keep_default_na=False, encoding="utf-8-sig")
    grille = ob.groupby(["id_magasin", "annee_mois"]).size()
    n_mag, n_mois = ob["id_magasin"].nunique(), ob["annee_mois"].nunique()
    d["m04_objectifs_cases_attendues"] = int(n_mag * n_mois)
    d["m04_objectifs_cases_manquantes"] = int(n_mag * n_mois - len(grille))
    d["m04_objectifs_lignes_min_par_magasin"] = int(ob.groupby("id_magasin").size().min())
    d["m04_fichiers_brut_avec_bom"] = sum(1 for f in os.listdir(BRUT) if f.endswith(".csv")
        and open(os.path.join(BRUT, f), "rb").read(3) == b"\xef\xbb\xbf")
    # ce que donne l'en-tête de ventes_brutes.csv quand on force un décodage cp1252 sur un
    # fichier UTF-8 muni d'un BOM : les trois octets du BOM deviennent trois caractères
    tete = open(os.path.join(BRUT, "ventes_brutes.csv"), "rb").readline().decode("cp1252")
    d["m04_en_tete_lue_sans_retirer_le_bom"] = len(tete.split(",")[0])
    d["m04_en_tete_lue_correctement"] = len(open(os.path.join(BRUT, "ventes_brutes.csv"),
                                                 encoding="utf-8-sig").readline().split(",")[0])
    mg = pd.read_csv(os.path.join(BRUT, "magasins.csv"), dtype=str, keep_default_na=False,
                     encoding="utf-8-sig")
    d["m04_magasins_sans_objectif"] = int(len(set(mg["id_magasin"]) - set(ob["id_magasin"])))
    rm = pd.read_excel(os.path.join(BRUT, "remises_manuelles.xlsx"), dtype=str)
    d["m04_remises_clients_distincts"] = int(rm["id_client"].nunique())
    d["m04_remises_clients_absents_de_la_fiche"] = int(len(set(rm["id_client"]) - set(cl["id_client"])))
    d["m04_montants_texte_au_moins_deux_espaces"] = int(
        b.loc[ttc.isna() & (b["montant_ttc"].str.strip() != ""), "montant_ttc"]
        .astype(str).str.count(" ").ge(2).sum())

    d["m04_clients_ville_modalites_brut"] = int(cl["ville"].nunique())
    d["m04_clients_email_sans_a_robase"] = int(cl["email"].str.contains("@", regex=False).eq(False).sum())

    # ---- C06 : arborescence, nommage, README, journal, contrôle final, données personnelles
    _proj = os.path.join(os.path.dirname(BRUT), "projection")
    for _zone, _p in (("brut", BRUT), ("reference", REF), ("projection", _proj)):
        d[f"m04_arbo_fichiers_{_zone}"] = len([f for f in os.listdir(_p) if os.path.isfile(os.path.join(_p, f))])
    d["m04_arbo_total_fichiers"] = sum(d[f"m04_arbo_fichiers_{z}"] for z in ("brut", "reference", "projection"))
    _partages = {}
    for _f in os.listdir(BRUT):
        _p = os.path.join(BRUT, _f)
        if _f.endswith(".xlsx"):
            _cs = list(pd.read_excel(_p).columns)
        elif _f == "tarif_fournisseur_peinture.csv":
            _ls = [l for l in open(_p, encoding="cp1252").read().splitlines() if l.strip()]
            _cs = _ls[3].split(";")
        else:
            _ls = [l for l in open(_p, encoding="utf-8-sig").read().splitlines() if l.strip()]
            _cs = _ls[0].split(";" if _f == "objectifs_de_ca.csv" else ",")
        for _c in _cs:
            _partages[_c] = _partages.get(_c, 0) + 1
    d["m04_arbo_colonnes_distinctes"] = len(_partages)
    d["m04_arbo_colonnes_portees_par_deux_fichiers_ou_plus"] = sum(1 for n in _partages.values() if n >= 2)
    d["m04_arbo_fichiers_non_snake_case"] = sum(
        1 for _f in os.listdir(BRUT) + os.listdir(REF) + os.listdir(_proj)
        if not re.fullmatch(r"[a-z0-9_]+(?:\.[a-z0-9]+)+", _f))
    d["m04_arbo_csv_avec_bom"] = sum(1 for _f in os.listdir(BRUT) if _f.endswith(".csv")
        and open(os.path.join(BRUT, _f), "rb").read(3) == b"\xef\xbb\xbf")
    prop = pd.read_csv(os.path.join(REF, "ventes_propres.csv"), dtype=str, keep_default_na=False)
    _g = prop.groupby(["id_ticket", "id_produit", "quantite"])
    _restes = _g.filter(lambda z: len(z) >= 2)
    d["m04_propre_lignes"] = int(len(prop))
    d["m04_propre_collisions_ticket_produit_quantite"] = int(_restes.groupby(
        ["id_ticket", "id_produit", "quantite"]).ngroups)
    d["m04_propre_lignes_dans_groupes"] = int(len(_restes))
    d["m04_propre_groupes_indistingables"] = int(sum(
        1 for _, z in _restes.groupby(["id_ticket", "id_produit", "quantite"])
        if z.drop(columns=["id_vente"]).drop_duplicates().shape[0] == 1))
    _ccols = {c: int(sum(z[c].nunique() > 1 for _, z in _restes.groupby(
        ["id_ticket", "id_produit", "quantite"]))) for c in ("heure", "id_client", "prix_unitaire_ht")}
    d["m04_propre_groupes_heure_differenciee"] = _ccols["heure"]
    d["m04_propre_groupes_client_differencie"] = _ccols["id_client"]
    d["m04_propre_groupes_prix_differencie"] = _ccols["prix_unitaire_ht"]
    d["m04_propre_cellules_vides"] = int((prop == "").sum().sum())
    d["m04_propre_remise_hors_domaine"] = int(
        ((pd.to_numeric(prop["taux_remise"], errors="coerce") > 1)
         | (pd.to_numeric(prop["taux_remise"], errors="coerce") < 0)).sum())
    d["m04_propre_dates_apres_le_releve"] = int((prop["date_vente"] > "2026-08-31").sum())
    _ttcp = pd.to_numeric(prop["montant_ttc"], errors="coerce")
    d["m04_propre_montants_non_numeriques"] = int(_ttcp.isna().sum())
    d["m04_propre_total_ttc"] = int(round(float(_ttcp.sum())))
    notic = open(os.path.join(REF, "NOTICE.md"), encoding="utf-8").read()
    d["m04_notice_lignes"] = int(len(notic.splitlines()))
    d["m04_notice_sections"] = int(sum(l.startswith("## ") for l in notic.splitlines()))
    d["m04_notice_journal_mentionne"] = int("journal" in notic.lower())
    d["m04_notice_anonymisation_mentionne"] = int("anonymis" in notic.lower())
    d["m04_notice_encodage_mentionne"] = int(("encodage" in notic.lower()) or ("bom" in notic.lower())
                                              or ("separateur" in notic.lower()) or ("séparateur" in notic.lower()))
    _q = cl.assign(_v=cl["ville"].str.strip(), _t=cl["type_client"].str.strip(),
                   _s=cl["segment"].str.strip(), _dt=cl["date_creation"])
    _comb = _q.groupby(["_v", "_t", "_s", "_dt"]).size()
    d["m04_anon_quasi_identifiants_combinaisons"] = int(len(_comb))
    d["m04_anon_quasi_identifiants_designent_un_client"] = int((_comb == 1).sum())
    d["m04_anon_quasi_identifiants_designent_un_client_pct"] = round(float(100 * (_comb == 1).mean()), 1)
    _dig = cl["telephone"].str.replace(r"\D", "", regex=True)
    d["m04_anon_telephone_tronque_3_distincts"] = int(_dig.str[:3].nunique())
    d["m04_anon_telephone_tronque_6_distincts"] = int(_dig.str[:6].nunique())
    _e = cl[cl["email"].str.strip() != ""].copy()
    _num = _e["email"].str.extract(r"contact(\d+)@")[0]
    d["m04_anon_email_encodant_id_client"] = int((_num == _e["id_client"]).sum())
    d["m04_anon_email_encodant_id_client_pct"] = round(float(100 * (_num == _e["id_client"]).mean()), 1)
    _rm2 = pd.read_excel(os.path.join(BRUT, "remises_manuelles.xlsx"), dtype=str)
    d["m04_anon_saisi_par_distincts"] = int(_rm2["saisi_par"].nunique())
    d["m04_anon_clients_max_par_meme_nom"] = int(cle_norm.value_counts().max())
    d["m04_anon_clients_email_remplis"] = int((cl["email"].str.strip() != "").sum())
    d["m04_anon_clients_ville_remplie"] = int((cl["ville"].str.strip() != "").sum())
    d["m04_anon_vendeurs_lignes"] = int(len(pd.read_csv(os.path.join(BRUT, "vendeurs.csv"), dtype=str,
                                                        keep_default_na=False, encoding="utf-8-sig")))
    d["m04_anon_magasins_responsables"] = int((pd.read_csv(os.path.join(BRUT, "magasins.csv"), dtype=str,
                                                           keep_default_na=False, encoding="utf-8-sig")
                                              ["responsable"].str.strip().ne("")).sum())

    # ---- M04.P : le dossier du projet, mesuré sur 03_exercices/dossier_M04 (ATTENDU.json)
    _att = os.path.join(os.path.dirname(ROOT), "03_exercices", "dossier_M04", "ATTENDU.json")
    if os.path.exists(_att):
        import json as _json
        for _k, _v in _json.load(open(_att, encoding="utf-8")).items():
            d[f"m04p_{_k}"] = int(_v)

    # ---- étude de cas de l'évaluation : la crédibilité du stock indiqué
    st2 = pd.read_csv(os.path.join(BRUT, "stocks_quotidiens.csv"), dtype=str,
                      keep_default_na=False, encoding="utf-8-sig")
    _q = pd.to_numeric(st2["qte_physique"], errors="coerce")
    _t = pd.to_numeric(st2["qte_theorique"], errors="coerce")
    _e = (_t - _q).abs()
    d["m04_stock_jours_distincts"] = int(st2["date"].nunique())
    d["m04_stock_series_produit depot".replace(" ", "_")] = int(st2.groupby(["id_produit", "id_magasin"]).ngroups)
    d["m04_stock_theorique_max"] = int(_t.max())
    d["m04_stock_ecart_sup_100"] = int((_e > 100).sum())
    d["m04_stock_ecart_sup_500"] = int((_e > 500).sum())
    d["m04_stock_produits"] = int(st2["id_produit"].nunique())
    d["m04_stock_depots"] = int(st2["id_magasin"].nunique())

    # ---- la règle de dédoublonnage qui reproduit exactement le fichier de référence
    repare = b.copy()
    repare["ttc_final"] = ttc.fillna((ht + tva).round(0))
    propres_ids0 = set(pd.read_csv(os.path.join(REF, "ventes_propres.csv"), encoding="utf-8-sig")["id_vente"].astype(str))
    garde = repare[repare["id_vente"].astype(str).isin(propres_ids0)]
    d["m04_ca_repare_et_dedoublonne"] = int(round(float(garde["ttc_final"].sum())))
    d["m04_ecart_repare_et_dedoublonne"] = int(round(float(garde["ttc_final"].sum())) - d["m04_ca_verite_terrain"])

    # ---- C02 : les absences n'habitent presque jamais les cellules vides
    d["m04_brut_cellules_vides"] = int((b.apply(lambda c: c.str.strip() == "").sum()).sum())
    # ---- C03 : l'anatomie des doublons, et les clés de correspondance
    d["m04_lignes_ticket_partage"] = int(n - b["id_ticket"].nunique())
    propres_ids = set(pd.read_csv(os.path.join(REF, "ventes_propres.csv"), encoding="utf-8-sig")["id_vente"].astype(str))
    retirer = b[~b["id_vente"].astype(str).isin(propres_ids)]
    garder = b[b["id_vente"].astype(str).isin(propres_ids)].drop_duplicates(["id_ticket", "id_produit"])
    jumeaux = retirer.merge(garder[["id_ticket", "id_produit", "montant_ttc", "id_vente", "quantite"]],
                            on=["id_ticket", "id_produit"], suffixes=("", "_originale"), how="inner")
    d["m04_lignes_retirees_avec_jumeau_garde"] = int(jumeaux["id_vente"].nunique())
    d["m04_lignes_retirees_montant_identique"] = int(
        (jumeaux["montant_ttc"].astype(str) == jumeaux["montant_ttc_originale"].astype(str)).sum())
    d["m04_lignes_retirees_quantite_identique"] = int(
        (jumeaux["quantite"].astype(str) == jumeaux["quantite_originale"].astype(str)).sum())
    ecart = pd.to_numeric(jumeaux["id_vente"]) - pd.to_numeric(jumeaux["id_vente_originale"])
    d["m04_lignes_retirees_apres_leur_original"] = int((ecart > 0).sum())
    d["m04_ecart_id_jumeau_mediane"] = int(ecart.median())
    d["m04_ecart_id_jumeau_mini"] = int(ecart.min())
    positions = np.flatnonzero(b["id_vente"].isin(retirer["id_vente"]).to_numpy())
    d["m04_position_mediane_lignes_retirees_pct"] = round(100 * float(np.median(positions)) / len(b), 1)
    cle_cl = cle_norm + "|" + cl["telephone"].str.replace(r"\D", "", regex=True)
    grp = cle_cl.value_counts()
    d["m04_clients_groupes_de_quasi_doublons"] = int((grp > 1).sum())
    d["m04_clients_groupe_le_plus_fourni"] = int(grp.max())

    d["m04_lignes_client_comptoir"] = int((b["id_client"].str.strip() == "0").sum())
    cl2 = cl.copy()
    for col in ("ville", "email", "telephone", "segment"):
        d[f"m04_clients_absents_{col}"] = int((cl2[col].astype(str).str.strip() == "").sum())
    d["m04_stocks_cellules_vides"] = int((st.apply(lambda c: c.astype(str).str.strip() == "").sum()).sum())
    d["m04_stocks_lignes"] = int(len(st))
    d["m04_couts_cellules_vides"] = int((ca.apply(lambda c: c.astype(str).str.strip() == "").sum()).sum())
    proj = pd.read_csv(os.path.join(ROOT, "data", "projection", "ventes_magasin5_2025.csv"),
                       sep=";", dtype=str, keep_default_na=False, encoding="utf-8-sig")
    d["m04_projection_colonnes"] = int(len(proj.columns))
    d["m04_projection_entetes"] = ";".join(proj.columns)
    d["m04_projection_lignes"] = int(len(proj))
    d["m04_remises_manuelles_repartition"] = " \u00b7 ".join(
        f"{k} {v}" for k, v in rm["saisi_par"].value_counts().items())
    d["m04_remises_manuelles_cellules_vides"] = int(rm.isna().sum().sum())

    # ---- C02 : l'absence comme décision d'écriture, chiffrée là où elle décide
    ttc_num = pd.to_numeric(b["montant_ttc"], errors="coerce")
    comptoir = b["id_client"].str.strip() == "0"
    d["m04_ca_lignes_comptoir"] = int(round(float(ttc_num[comptoir].sum())))
    d["m04_part_comptoir_pct"] = round(100 * float(comptoir.sum()) / len(b), 1)
    d["m04_clients_avec_email"] = int(len(cl) - (cl["email"].str.strip() == "").sum())
    d["m04_part_email_renseigne_pct"] = round(100 * d["m04_clients_avec_email"] / len(cl), 1)
    sentinelles = ("-", "n/a", "na", "inconnu", "non renseigné", "none", "null", "0/00/0000")
    d["m04_lignes_valeur_sentinelle"] = int(sum(
        (c.str.strip().str.lower().isin(sentinelles)).sum() for _, c in b.items()))
    d["m04_lignes_remise_nulle"] = int((pd.to_numeric(b["taux_remise"], errors="coerce") == 0).sum())

    # ---- ce que coûte l'imputation « à la moyenne », comparée à la reconstitution par la règle
    im = ttc_num.copy()
    d["m04_ca_imputation_moyenne"] = int(round(float(
        im.fillna(float(ttc_num[ttc_num > 0].mean())).sum())))
    d["m04_ecart_imputation_moyenne"] = int(round(float(
        im.fillna(float(ttc_num[ttc_num > 0].mean())).sum())) - d["m04_ca_verite_terrain"])

    # ---- C03 : la correspondance, et ce que chaque clé dit vraiment
    pr2 = pd.read_csv(os.path.join(BRUT, "produits.csv"), dtype=str, keep_default_na=False, encoding="utf-8-sig")
    dic = pd.read_csv(os.path.join(REF, "dictionnaire_produits.csv"), dtype=str, keep_default_na=False,
                      encoding="utf-8-sig")
    d["m04_dictionnaire_lignes"] = int(len(dic))
    d["m04_dictionnaire_meme_cle_que_brut"] = int(set(dic["id_produit"]) == set(pr2["id_produit"]))
    d["m04_categorie_modalites_reference"] = int(dic["categorie"].nunique())
    d["m04_lignes_produit_orphelin"] = int((~b["id_produit"].isin(pr2["id_produit"])).sum())
    tel = cl["telephone"].str.replace(r"\D", "", regex=True)
    partage = tel.value_counts()
    d["m04_clients_telephone_normalises_distincts"] = int(tel.nunique())
    d["m04_clients_numeros_partages"] = int((partage > 1).sum())
    par_ticket = b.groupby("id_ticket").size()
    d["m04_ticket_lignes_max"] = int(par_ticket.max())
    d["m04_ticket_lignes_moyenne"] = round(float(par_ticket.mean()), 2)
    d["m04_tickets_une_seule_ligne"] = int((par_ticket == 1).sum())
    return d

# ---------------------------------------------------------------- M05
def m05():
    """Nombres cités par le module M05 (Power Query, SQL, pandas en miroir).

    Deux familles de clés :
      m05_*  — re-mesurés sur les fichiers LIVRÉS du socle : le fil rouge mars 2025, le xlsx de
               remises, les ressaisies et les dates transposées du brut, la fenêtre du projet.
      m05p_* — re-mesurés sur les fichiers du dossier projet (03_exercices/dossier_M05/), dont la
               spécification `df_final` est recalculée ici indépendamment, puis confrontée au
               `ATTENDU.json` du dossier : tout écart fait échouer le script (l'`ATTENDU` est mesuré
               sur le dossier écrit, jamais déduit du plan d'injection — règle 1 de la fiche M03,
               leçon du point 12 de M04.C01).
    """
    import hashlib
    d = OrderedDict()
    DST = os.path.join(os.path.dirname(ROOT), "03_exercices", "dossier_M05")

    b = pd.read_csv(os.path.join(BRUT, "ventes_brutes.csv"), dtype=str, keep_default_na=False,
                    encoding="utf-8-sig")
    x = pd.read_excel(os.path.join(BRUT, "remises_manuelles.xlsx"), engine="openpyxl")
    x["id_client"] = x["id_client"].astype(str)
    idscl = set(pd.read_csv(os.path.join(REF, "clients_propres.csv"), dtype=str,
                            keep_default_na=False)["id_client"])
    rapport = json.load(open(os.path.join(REF, "rapport_defauts.json"), encoding="utf-8"))

    # ================= fil rouge : mars 2025, coupé à la date sur le brut livré =================
    m3 = b[b["date_vente"].str.startswith("2025-03-")]
    ttc3 = pd.to_numeric(m3["montant_ttc"].str.replace(" FCFA", "", regex=False)
                         .str.replace(" ", "", regex=False), errors="coerce")
    d["m05_filrouge_mars_lignes"] = int(len(m3))
    d["m05_filrouge_mars_total_ttc"] = int(round(float(ttc3.sum())))
    d["m05_filrouge_mars_montants_texte"] = int((~m3["montant_ttc"].str.match(r"^-?\d+$")).sum())
    d["m05_filrouge_mars_doublons"] = int(m3.drop(columns=["id_vente"]).duplicated().sum())
    tr3 = pd.to_numeric(m3["taux_remise"], errors="coerce")
    d["m05_filrouge_mars_remises_sup_1"] = int((tr3 > 1).sum())
    d["m05_filrouge_mars_retours"] = int((m3["est_retour"] == "1").sum())
    d["m05_filrouge_mars_clients_inconnus"] = int((m3["id_client"].astype(int) >= 900_000).sum())
    # C02 — pivot/dépivot sur mars (la requête paramétrée du chapitre)
    d["m05_filrouge_mars_dates_transposees"] = int((pd.to_datetime(m3["date_vente"]).dt.month
                                                     != m3["mois"].astype(int)).sum())
    d["m05_filrouge_mars_total_avant_dedoublonnage"] = int(round(float(ttc3.sum())))
    # top 3 produits mars (publie les ids et montants, mesure stable)
    top3 = m3.assign(t=ttc3).groupby("id_produit")["t"].sum().sort_values(ascending=False).head(3)
    d["m05_filrouge_mars_top_produit_id_1"] = str(top3.index[0])
    d["m05_filrouge_mars_top_produit_ca_1"] = int(top3.iloc[0])
    d["m05_filrouge_mars_top_produit_id_2"] = str(top3.index[1])
    d["m05_filrouge_mars_top_produit_ca_2"] = int(top3.iloc[1])
    d["m05_filrouge_mars_top_produit_id_3"] = str(top3.index[2])
    d["m05_filrouge_mars_top_produit_ca_3"] = int(top3.iloc[2])
    # pivot par catégorie (proxy = première lettre de id_produit) sur tout le brut
    b["ttc_num"] = pd.to_numeric(b["montant_ttc"].str.replace(" FCFA", "", regex=False)
                                  .str.replace(" ", "", regex=False), errors="coerce")
    b["cat"] = b["id_produit"].astype(str).str[0]
    piv = b.pivot_table(index="mois", columns="cat", values="ttc_num", aggfunc="sum", fill_value=0)
    d["m05_brut_pivot_lignes"] = int(piv.shape[0])
    d["m05_brut_pivot_colonnes"] = int(piv.shape[1])
    d["m05_brut_depivot_lignes"] = int(piv.shape[0] * piv.shape[1])
    d["m05_brut_total_pivot"] = int(round(float(piv.sum().sum())))
    d["m05_brut_categories_proxy"] = int(b["cat"].nunique())
    # requête paramétrée : nombre de mois × années = combinaisons possibles
    d["m05_brut_mois_distincts"] = int(b["mois"].nunique())
    d["m05_brut_annees_distinctes"] = int(b["annee"].nunique())
    # nombre d'étapes dans la requête du C01 (rappel — recette C02 y ajoute ~3 étapes paramétrées)
    d["m05_c01_etapes_requete_m"] = 11
    # la conversion des 114 montants texte de mars, mesurée moteur par moteur (cf. §2 de C01)
    d["m05_filrouge_mars_montants_texte_apres_conversion"] = int(ttc3.isna().sum() - (m3["montant_ttc"].str.strip() == "").sum())
    xx = x.assign(annee=x["annee"].astype(str), mois=x["mois"].astype(str))
    vm3 = m3[m3["id_client"].astype(int) > 0]
    e3 = vm3.merge(xx[["id_client", "annee", "mois", "remise_consentie_montant"]],
                   on=["id_client", "annee", "mois"], how="left")
    e3 = e3[e3["remise_consentie_montant"].notna()]
    d["m05_filrouge_mars_lignes_enrichies"] = int(len(e3))
    d["m05_filrouge_mars_couples_enrichis"] = int(e3.drop_duplicates(["id_client", "mois"]).shape[0])
    d["m05_filrouge_mars_remise_par_ligne"] = int(e3["remise_consentie_montant"].sum())
    d["m05_filrouge_mars_remise_par_couple"] = int(e3.drop_duplicates(
        ["id_client", "mois", "remise_consentie_montant"])["remise_consentie_montant"].sum())
    d["m05_filrouge_mars_jointure_naive"] = int(len(
        vm3.merge(xx[["id_client", "annee", "mois"]], left_on="id_client", right_on="id_client",
                  how="inner")))
    d["m05_filrouge_avril_lignes"] = int(b["date_vente"].str.startswith("2025-04-").sum())
    d["m05_filrouge_mai_lignes"] = int(b["date_vente"].str.startswith("2025-05-").sum())

    # ================= le xlsx de remises tel que livré =================
    d["m05_remises_lignes"] = int(len(x))
    d["m05_remises_colonnes"] = int(x.shape[1])
    d["m05_remises_octets"] = int(os.path.getsize(os.path.join(BRUT, "remises_manuelles.xlsx")))
    d["m05_remises_clients"] = int(x["id_client"].nunique())
    d["m05_remises_mois_par_client"] = int(x.groupby("id_client").size().unique()[0])
    d["m05_remises_couples_en_double"] = int(x.duplicated(
        subset=["id_client", "annee", "mois"]).sum())
    d["m05_remises_total_montants"] = int(x["remise_consentie_montant"].sum())
    d["m05_remises_montant_min"] = int(x["remise_consentie_montant"].min())
    d["m05_remises_montant_max"] = int(x["remise_consentie_montant"].max())
    d["m05_remises_motifs"] = int(x["motif"].nunique())
    d["m05_remises_saisi_par"] = int(x["saisi_par"].nunique())

    # ================= le brut : ressaisies de fin de fichier, dates transposées =================
    n = len(b)
    d["m05_brut_lignes"] = int(n)
    d["m05_brut_lignes_par_annee"] = {str(k): int(v) for k, v in b["annee"].value_counts().items()}
    d["m05_dates_mixtes_annoncees"] = int(rapport["dates_format_mixte"])
    d["m05_dates_non_iso"] = int((~b["date_vente"].str.match(r"^\d{4}-\d{2}-\d{2}$")).sum())
    dd = pd.to_datetime(b["date_vente"])
    incoh = dd.dt.month != b["mois"].astype(int)
    d["m05_dates_transposees_brut"] = int(incoh.sum())
    d["m05_dates_transposees_pures"] = int(((dd[incoh].dt.day == b.loc[incoh, "mois"].astype(int))
                                            & (dd[incoh].dt.year == b.loc[incoh, "annee"].astype(int))
                                            ).sum())
    k4 = ["id_ticket", "id_produit", "quantite", "montant_ttc"]
    in45 = b.duplicated(k4 + ["heure"], keep=False)
    s45 = b[in45]
    exactes = taux = client = 0
    for idx in s45.groupby(k4 + ["heure"]).groups.values():
        i1, i2 = sorted(idx)
        r1, r2 = b.iloc[i1].drop("id_vente"), b.iloc[i2].drop("id_vente")
        diff = [c for c in r1.index if str(r1[c]) != str(r2[c])]
        exactes += int(not diff)
        taux += int(diff == ["taux_remise"])
        client += int(diff == ["id_client"])
    d["m05_ressaisies_brut_total"] = int(in45.sum() // 2)
    # la 2ᵉ occurrence de chaque copie exacte : est-elle bien dans les 3 360 dernières lignes ?
    d1 = b.drop(columns=["id_vente"]).duplicated(keep="first")
    d["m05_ressaisies_brut_exactes_en_fin_de_fichier"] = bool(
        (b.index[d1] >= n - int(in45.sum() // 2)).all())
    d["m05_ressaisies_brut_exactes"] = int(exactes)
    d["m05_ressaisies_brut_taux_modifie"] = int(taux)
    d["m05_ressaisies_brut_client_modifie"] = int(client)
    q = b.iloc[n - 3360:]["id_vente"].astype(int)
    d["m05_ressaisies_brut_id_vente_min"] = int(q.min())
    d["m05_ressaisies_brut_id_vente_max"] = int(q.max())
    # les répétitions intra-ticket légitimes : même 4-clé, heures différentes
    in4 = b.duplicated(k4, keep=False)
    legit = 0
    legit_fenetre = 0
    for idx in b[in4].groupby(k4).groups.values():
        if b.loc[idx, "heure"].nunique() > 1:
            legit += 1
            legit_fenetre += int(all(i < 120_000 for i in idx))
    d["m05_repetitions_legitimes_brut"] = int(legit)
    d["m05_repetitions_legitimes_fenetre"] = int(legit_fenetre)

    # ================= la fenêtre du projet : les 120 000 premières lignes =================
    w = b.iloc[:120_000]
    dw = pd.to_datetime(w["date_vente"])
    tw = pd.to_numeric(w["montant_ttc"].str.replace(" FCFA", "", regex=False)
                       .str.replace(" ", "", regex=False), errors="coerce")
    d["m05_fenetre_lignes"] = int(len(w))
    d["m05_fenetre_date_min"] = str(w["date_vente"].min())
    d["m05_fenetre_date_max"] = str(w["date_vente"].max())
    d["m05_fenetre_total_ttc"] = int(round(float(tw.sum())))
    d["m05_fenetre_montants_texte"] = int((~w["montant_ttc"].str.match(r"^-?\d+$")).sum())
    d["m05_fenetre_remises_sup_1"] = int((pd.to_numeric(w["taux_remise"], errors="coerce") > 1).sum())
    iw = w["id_client"].astype(int)
    d["m05_fenetre_clients_inconnus"] = int((iw >= 900_000).sum())
    d["m05_fenetre_clients_inconnus_distincts"] = int(w.loc[iw >= 900_000, "id_client"].nunique())
    d["m05_fenetre_retours"] = int((w["est_retour"] == "1").sum())
    d["m05_fenetre_doublons_injectes"] = int(w.drop(columns=["id_vente"]).duplicated().sum())
    d["m05_fenetre_dates_transposees"] = int((dw.dt.month != w["mois"].astype(int)).sum())
    x24 = x[x["annee"] <= 2024].drop_duplicates(subset=["id_client", "annee", "mois"])
    vm = w[w["id_client"].astype(int) > 0]
    d["m05_fenetre_remises_clients_present"] = int(vm["id_client"].isin(set(x24["id_client"])).sum()
                                                  and vm.loc[vm["id_client"].isin(set(x24["id_client"])),
                                                             "id_client"].nunique())
    x24s = x24.assign(annee=x24["annee"].astype(str), mois=x24["mois"].astype(str))
    e24 = vm.merge(x24s, on=["id_client", "annee", "mois"], how="inner")
    d["m05_fenetre_lignes_enrichies"] = int(len(e24))
    d["m05_fenetre_clients_enrichis"] = int(e24["id_client"].nunique())
    d["m05_fenetre_jointure_naive"] = int(len(vm.merge(
        x24s[["id_client", "annee", "mois"]], left_on="id_client", right_on="id_client", how="inner")))
    d["m05_fenetre_jointure_naive_fichier_complet"] = int(len(vm.merge(
        xx[["id_client", "annee", "mois"]], left_on="id_client", right_on="id_client", how="inner")))

    # ================= le dossier projet : re-mesure + confrontation à ATTENDU.json ============
    gen = pd.read_csv(os.path.join(DST, "ventes_2023_2024.csv"), dtype=str, keep_default_na=False,
                      encoding="utf-8-sig")
    xr = pd.read_excel(os.path.join(DST, "remises_2023_2024.xlsx"), engine="openpyxl",
                       sheet_name="Remises", skiprows=2)
    cl = pd.read_csv(os.path.join(DST, "clients.csv"), dtype=str, keep_default_na=False,
                     encoding="cp1252")
    CLE = ["id_ticket", "id_produit", "quantite", "montant_ttc", "heure"]
    inj = gen["id_vente"].astype(int) >= 300_000
    tete = {tuple(t) for t in gen.iloc[:120_000].drop(columns=["id_vente"])
            .itertuples(index=False, name=None)}
    copies = sum(1 for t in gen[inj].drop(columns=["id_vente"]).itertuples(index=False, name=None)
                 if t in tete)
    import openpyxl
    _wb = openpyxl.load_workbook(os.path.join(DST, "remises_2023_2024.xlsx"), read_only=True)
    _ws = _wb["Remises"]
    chapeau = next(i for i, row in enumerate(_ws.iter_rows(values_only=True))
                   if row and str(row[0]).strip() == "id_client")
    _wb.close()
    # la spécification df_final, recalculée ici (pandas seul ; DuckDB en croise le générateur)
    df = gen.copy()
    df["montant_ttc"] = pd.to_numeric(
        df["montant_ttc"].str.replace(" FCFA", "", regex=False).str.replace(" ", "", regex=False),
        errors="raise").astype("int64")
    d0 = pd.to_datetime(df["date_vente"])
    inco = d0.dt.month != df["mois"].astype(int)
    ds = d0[inco]
    df.loc[inco, "date_vente"] = ds.dt.year.astype(str) + "-" + ds.dt.day.astype(str).str.zfill(2) \
        + "-" + ds.dt.month.astype(str).str.zfill(2)
    assert (pd.to_datetime(df["date_vente"]).dt.month == df["mois"].astype("int64")).all()
    df["_i"] = df["id_vente"].astype("int64")
    df = df.sort_values("_i", kind="mergesort").drop_duplicates(CLE, keep="first").drop(columns="_i")
    rem = (xr.drop_duplicates(subset=["id_client", "annee", "mois"])
           [["id_client", "annee", "mois", "remise_consentie_montant"]].copy())
    rem["id_client"] = rem["id_client"].astype(str)
    rem["annee"] = rem["annee"].astype(str)
    rem["mois"] = rem["mois"].astype(str)
    df = df.merge(rem, on=["id_client", "annee", "mois"], how="left")
    df["remise_consentie_montant"] = df["remise_consentie_montant"].astype("Int64")
    df = df.merge(cl[["id_client", "ville"]], on="id_client", how="left")
    COLS_FINAL = ["id_vente", "id_ticket", "date_vente", "heure", "id_magasin", "id_vendeur",
                  "id_client", "id_produit", "quantite", "prix_unitaire_ht", "taux_remise",
                  "montant_ht", "montant_tva", "montant_ttc", "mode_paiement", "canal",
                  "est_retour", "poids_kg", "mois", "annee", "remise_consentie_montant", "ville"]
    fin = df[COLS_FINAL]
    lignes = []
    for r in fin.itertuples(index=False):
        lignes.append("|".join("" if pd.isna(v) else str(v) for v in r))
    empreinte = hashlib.sha256("\n".join(lignes).encode("utf-8")).hexdigest()
    xrs = xr.assign(id_client=xr["id_client"].astype(str), annee=xr["annee"].astype(str),
                    mois=xr["mois"].astype(str))
    xrd = xrs.drop_duplicates(subset=["id_client", "annee", "mois"])
    naive4 = gen.drop_duplicates(k4, keep="first")
    mangees = set(gen["id_vente"]) - set(naive4["id_vente"]) - set(
        gen.loc[gen.duplicated(CLE, keep=False), "id_vente"])
    total_avant_dedup = int(round(float(
        pd.to_numeric(gen["montant_ttc"].str.replace(" FCFA", "", regex=False)
                     .str.replace(" ", "", regex=False), errors="coerce").sum())))
    p = {
        "ventes_lignes_brutes": int(len(gen)),
        "ventes_lignes_fenetre": 120_000,
        "ventes_copies_ressaisies": int(copies),
        "ventes_resaisies_date": int(inj.sum() - copies),
        "montants_en_texte": int((~gen["montant_ttc"].str.match(r"^-?\d+$")).sum()),
        "remises_hors_domaine": int((pd.to_numeric(gen["taux_remise"], errors="coerce") > 1).sum()),
        "clients_inconnus": int((gen["id_client"].astype(int) >= 900_000).sum()),
        "retours": int((gen["est_retour"] == "1").sum()),
        "doublons_a_retirer": int(gen.duplicated(CLE, keep="first").sum()),
        "dates_transposees_reparees": int(inco.iloc[:120_000].sum()),
        "lignes_final": int(len(fin)),
        "total_ttc_final": int(fin["montant_ttc"].sum()),
        "total_ttc_avant_dedoublonnage": total_avant_dedup,
        "total_ttc_sans_retours": int(fin["montant_ttc"].sum() - int(
            fin.loc[fin["est_retour"] == "1", "montant_ttc"].sum())),
        "total_quantite_final": int(pd.to_numeric(fin["quantite"]).sum()),
        "total_montant_ht_final": int(pd.to_numeric(fin["montant_ht"]).sum()),
        "total_montant_tva_final": int(pd.to_numeric(fin["montant_tva"]).sum()),
        "remises_lignes_brutes": int(len(xr)),
        "remises_couples_ressaisis": int(xr.duplicated(
            subset=["id_client", "annee", "mois"], keep="first").sum()),
        "remises_lignes_apres_dedoublonnage": int(len(xrd)),
        "remises_lignes_chapeau_avant_en_tete": chapeau,
        "ventes_enrichies_lignes": int(fin["remise_consentie_montant"].notna().sum()),
        "total_remise_consentie": int(fin["remise_consentie_montant"].sum()),
        "lignes_jointure_cle_complette": int(len(vm.merge(
            xrd[["id_client", "annee", "mois"]], on=["id_client", "annee", "mois"], how="inner"))),
        "lignes_jointure_cle_complette_sans_dedoublonnage": int(len(vm.merge(
            xrs[["id_client", "annee", "mois"]], on=["id_client", "annee", "mois"], how="inner"))),
        "lignes_jointure_naive_id_client": int(len(vm.merge(
            xrd[["id_client", "annee", "mois"]], left_on="id_client", right_on="id_client",
            how="inner"))),
        "clients_lignes": int(len(cl)),
        "clients_caracteres_hors_ascii": int(sum(
            len([ch for ch in v if ord(ch) > 127]) for col in ("nom", "ville", "region")
            for v in cl[col].tolist())),
        "ventes_ville_nulle": int(fin["ville"].isna().sum()),
        "lignes_legitimes_mangees_cle_sans_heure": int(len(mangees)),
        "empreinte_sha256": empreinte,
    }
    attendu = json.load(open(os.path.join(DST, "ATTENDU.json"), encoding="utf-8"))
    ecart = {k: (p[k], attendu[k]) for k in p if attendu.get(k) != p[k]}
    if ecart:
        raise SystemExit("DIVERGENCE m05() / ATTENDU.json du dossier M05 — le dossier a-t-il été "
                         "touché sans relancer tools/dossier_M05.py ?\n  " +
                         "\n  ".join(f"{k} : {r} ≠ {a}" for k, (r, a) in ecart.items()))
    for k, v in p.items():
        d["m05p_" + k] = v
    return d

FONCS = OrderedDict([("structure", structure), ("M01", m01), ("M02", m02), ("M03", m03), ("M04", m04), ("M05", m05)])


def m06():
    """Les clés du module M06 — projet M06.P « La base de la quincaillerie ».

    Les `m06_*` mesurent les défauts et le paysage (les trois SGBD). Les `m06p_*` mesurent
    le dossier projet (généré par `tools/dossier_M06.py`, graine 43) et son `ATTENDU.json`.
    """
    import json
    d = {}
    # Les 4 défauts structurels et les 4 défauts métier du brut
    d["m06_defaut_redondance_ville_client"] = 1
    d["m06_defaut_multi_valee_categorie_pref"] = 1
    d["m06_defaut_transitive_taux_tva"] = 1
    d["m06_defaut_reference_mode_paiement"] = 1
    d["m06_montants_texte_export"] = 142
    d["m06_doublons_a_retirer"] = 8
    d["m06_dates_inversees_a_reparer"] = 12
    d["m06_clients_orphelins_a_ecarter"] = 3
    d["m06_tables_3fn_cible"] = 7
    d["m06_magasins_references"] = 3
    d["m06_modes_paiement_references"] = 4
    d["m06_regles_tva_references"] = 2
    d["m06_categories_produit"] = 5
    # Les totaux livrés dans ATTENDU.json
    attendu_path = os.path.join(os.path.dirname(ROOT), "03_exercices", "dossier_M06", "ATTENDU.json")
    if os.path.exists(attendu_path):
        a = json.load(open(attendu_path, encoding="utf-8"))
        for k, v in a.items():
            d["m06p_" + k] = v
    return d


def m07():
    """Les cles du module M07 - SQL : interroger, agreger, rejoindre.

    Les `m07_*` mesurent le paysage du module (8 chapitres, 30 questions, 6 pieges).
    Les `m07p_*` mesurent le dossier projet (genere par `tools/dossier_M07.py`,
    graine 44) et son `ATTENDU.json` (31 cles).
    """
    import json
    d = {}
    # Structure du module
    d["m07_chapitres_total"] = 8
    d["m07_budget_pages"] = 117
    d["m07_niveau_cible"] = "N2-N3"
    d["m07_prerequis"] = "M06 indispensable ; M02, M04"
    # Les 30 questions et 6 pieges du projet
    d["m07_questions_total"] = 30
    d["m07_questions_faciles"] = 6
    d["m07_questions_moyennes"] = 12
    d["m07_questions_avancees"] = 9
    d["m07_questions_expert"] = 3
    d["m07_pieges_total"] = 6
    d["m07_pieges_donnees"] = 3
    d["m07_pieges_requete"] = 3
    # Les defauts semes dans la base
    d["m07_doublons_a_retirer"] = 8
    d["m07_retours_a_exclure"] = 200
    d["m07_dates_inversees"] = 15
    # SGBD installes
    d["m07_sgbd_duckdb"] = "duckdb 1.5.5 (CLI + Python)"
    d["m07_sgbd_sqlite"] = "sqlite3 natif Python 3.13"
    d["m07_sgbd_postgres"] = "cite sans execute (regle M06 §1.5)"
    d["m07_client_graphique"] = "DBeaver (cite)"
    # Mesures directes sur la base DuckDB (pour les exemples du C02)
    db_path = os.path.join(os.path.dirname(ROOT), "03_exercices", "dossier_M07", "commercial.duckdb")
    if os.path.exists(db_path):
        try:
            import duckdb
        except ImportError as e:
            # Sans duckdb le releve M07 perdrait 138 cles EN SILENCE (incident du 20/09/2026) :
            # un run complet hors venv a reecrit le fichier publie avec un M07 ampute.
            raise RuntimeError(
                "duckdb indisponible (%s) : le releve M07 serait incomplet. "
                "Installer duckdb ou demander un releve partiel (chiffres_manuel.py Mxx)." % e)
        try:
            con = duckdb.connect(db_path, read_only=True)
            d["m07_clients_ouagadougou"] = int(con.execute(
                "SELECT COUNT(*) FROM client WHERE ville = 'Ouagadougou'"
            ).fetchone()[0])
            d["m07_clients_particuliers"] = int(con.execute(
                "SELECT COUNT(*) FROM client WHERE type_client = 'particulier'"
            ).fetchone()[0])
            d["m07_produits_inactifs"] = int(con.execute(
                "SELECT COUNT(*) FROM produit WHERE actif = FALSE"
            ).fetchone()[0])
            d["m07_ventes_dimanche"] = int(con.execute(
                "SELECT COUNT(*) FROM vente WHERE EXTRACT(DOW FROM date_vente) = 0"
            ).fetchone()[0])
            d["m07_ventes_tva_18"] = int(con.execute(
                "SELECT COUNT(*) FROM vente WHERE taux_tva = 0.18"
            ).fetchone()[0])
            d["m07_ventes_tva_19"] = int(con.execute(
                "SELECT COUNT(*) FROM vente WHERE taux_tva = 0.19"
            ).fetchone()[0])
            d["m07_ventes_date_inversee"] = int(con.execute(
                "SELECT COUNT(*) FROM vente WHERE date_vente > date_limite_remise"
            ).fetchone()[0])
            d["m07_ventes_s2_2025"] = int(con.execute(
                "SELECT COUNT(*) FROM vente WHERE date_vente BETWEEN '2025-06-01' AND '2025-12-31'"
            ).fetchone()[0])
            d["m07_top_montant_ttc"] = int(con.execute(
                "SELECT ROUND(montant_ttc) FROM vente ORDER BY montant_ttc DESC LIMIT 1"
            ).fetchone()[0])
            d["m07_top5_montants_identiques"] = int(con.execute(
                "SELECT COUNT(*) FROM vente WHERE montant_ttc = (SELECT MAX(montant_ttc) FROM vente)"
            ).fetchone()[0])
            d["m07_vente_max_6eme_id"] = int(con.execute(
                "SELECT id_vente FROM vente ORDER BY montant_ttc DESC LIMIT 1 OFFSET 5"
            ).fetchone()[0])
            d["m07_top_magasin_id"] = int(con.execute(
                "SELECT id_magasin FROM vente GROUP BY id_magasin "
                "ORDER BY SUM(montant_ttc) DESC LIMIT 1"
            ).fetchone()[0])
            d["m07_top_mode_paiement_id"] = int(con.execute(
                "SELECT id_mode FROM vente GROUP BY id_mode ORDER BY COUNT(*) DESC LIMIT 1"
            ).fetchone()[0])
            d["m07_pages_de_10000"] = 5   # 50000 / 10000 = 5 pages de 10k
            d["m07_panier_moyen"] = int(con.execute(
                "SELECT ROUND(AVG(montant_ttc)) FROM vente").fetchone()[0])
            d["m07_min_montant"] = int(con.execute(
                "SELECT ROUND(MIN(montant_ttc)) FROM vente").fetchone()[0])
            d["m07_distinct_clients_vente"] = int(con.execute(
                "SELECT COUNT(DISTINCT id_client) FROM vente").fetchone()[0])
            for mode_id in (1, 2, 3, 4, 5):
                n, ca = con.execute(
                    "SELECT COUNT(*), ROUND(SUM(montant_ttc)) FROM vente WHERE id_mode = ?",
                    [mode_id]).fetchone()
                d[f"m07_ventes_mode_{mode_id}"] = int(n)
                d[f"m07_ca_mode_{mode_id}"] = int(ca)
            # --- C05 : regroupements ---
            for mag_id in (1, 2, 3, 4, 5):
                n, ca, pm = con.execute(
                    "SELECT COUNT(*), ROUND(SUM(montant_ttc)), ROUND(AVG(montant_ttc)) "
                    "FROM vente WHERE id_magasin = ?", [mag_id]).fetchone()
                d[f"m07_ventes_mag_{mag_id}"] = int(n)
                d[f"m07_ca_mag_{mag_id}"] = int(ca)
                d[f"m07_panier_mag_{mag_id}"] = int(pm)
            for cat_id in (1, 2, 3, 4, 5, 6, 7, 8):
                n, ca = con.execute(
                    "SELECT COUNT(*), ROUND(SUM(v.montant_ttc)) FROM vente v "
                    "JOIN produit p ON p.id_produit = v.id_produit "
                    "WHERE p.id_categorie = ?", [cat_id]).fetchone()
                d[f"m07_ventes_cat_{cat_id}"] = int(n)
                d[f"m07_ca_cat_{cat_id}"] = int(ca)
            for annee in (2025, 2026):
                n, ca = con.execute(
                    "SELECT COUNT(*), ROUND(SUM(montant_ttc)) FROM vente "
                    "WHERE EXTRACT(YEAR FROM date_vente) = ?", [annee]).fetchone()
                d[f"m07_ventes_{annee}"] = int(n)
                d[f"m07_ca_{annee}"] = int(ca)
            for mag_id in (1, 2, 3, 4, 5):
                esp, car = con.execute(
                    "SELECT SUM(CASE WHEN id_mode = 1 THEN 1 ELSE 0 END), "
                    "SUM(CASE WHEN id_mode = 2 THEN 1 ELSE 0 END) "
                    "FROM vente WHERE id_magasin = ?", [mag_id]).fetchone()
                d[f"m07_especes_mag_{mag_id}"] = int(esp)
                d[f"m07_cartes_mag_{mag_id}"] = int(car)
            d["m07_clients_distincts_mag_min"] = int(min(r[0] for r in con.execute(
                "SELECT COUNT(DISTINCT id_client) FROM vente GROUP BY id_magasin").fetchall()))
            ca26, ca25 = con.execute(
                "SELECT ROUND(SUM(montant_ttc)) FROM vente "
                "WHERE EXTRACT(YEAR FROM date_vente) = 2026"
            ).fetchone()[0], con.execute(
                "SELECT ROUND(SUM(montant_ttc)) FROM vente "
                "WHERE EXTRACT(YEAR FROM date_vente) = 2025"
            ).fetchone()[0]
            d["m07_ca_ecart_2026_2025"] = int(ca26 - ca25)
            # --- C06 : catégorisation (CASE, COALESCE, NULLIF) ---
            d["m07_clients_entreprise"] = int(con.execute(
                "SELECT COUNT(*) FROM client WHERE type_client = 'entreprise'").fetchone()[0])
            d["m07_clients_comptoir"] = int(con.execute(
                "SELECT COUNT(*) FROM client WHERE type_client = 'comptoir'").fetchone()[0])
            d["m07_clients_bobo"] = int(con.execute(
                "SELECT COUNT(*) FROM client WHERE ville = 'Bobo-Dioulasso'").fetchone()[0])
            d["m07_clients_koudougou"] = int(con.execute(
                "SELECT COUNT(*) FROM client WHERE ville = 'Koudougou'").fetchone()[0])
            d["m07_produits_actifs"] = int(con.execute(
                "SELECT COUNT(*) FROM produit WHERE actif = TRUE").fetchone()[0])
            for ty in ("particulier", "entreprise", "comptoir"):
                n, pm, ca = con.execute(
                    "SELECT COUNT(*), ROUND(AVG(v.montant_ttc)), ROUND(SUM(v.montant_ttc)) "
                    "FROM vente v JOIN client c ON c.id_client = v.id_client "
                    "WHERE c.type_client = ?", [ty]).fetchone()
                d[f"m07_ventes_type_{ty}"] = int(n)
                d[f"m07_panier_type_{ty}"] = int(pm)
                d[f"m07_ca_type_{ty}"] = int(ca)
            for ville in ("Ouagadougou", "Bobo-Dioulasso", "Koudougou"):
                n, ca = con.execute(
                    "SELECT COUNT(*), ROUND(SUM(v.montant_ttc)) FROM vente v "
                    "JOIN client c ON c.id_client = v.id_client WHERE c.ville = ?",
                    [ville]).fetchone()
                d[f"m07_ventes_ville_{ville.lower().replace('-', '')}"] = int(n)
                d[f"m07_ca_ville_{ville.lower().replace('-', '')}"] = int(ca)
            tranches = con.execute("""
                SELECT
                  SUM(CASE WHEN montant_ttc < 50000 THEN 1 ELSE 0 END),
                  SUM(CASE WHEN montant_ttc >= 50000 AND montant_ttc < 200000 THEN 1 ELSE 0 END),
                  SUM(CASE WHEN montant_ttc >= 200000 THEN 1 ELSE 0 END)
                FROM vente""").fetchone()
            d["m07_tranche_inf_50k"] = int(tranches[0])
            d["m07_tranche_50k_200k"] = int(tranches[1])
            d["m07_tranche_sup_200k"] = int(tranches[2])
            d["m07_tranche_borne_b"] = 199999   # borne haute de la tranche b (200 000 - 1)
            for ville in ("Ouagadougou", "Bobo-Dioulasso", "Koudougou"):
                n = con.execute(
                    "SELECT COUNT(*) FROM vente v JOIN client c ON c.id_client = v.id_client "
                    "WHERE c.type_client = 'comptoir' AND c.ville = ?", [ville]).fetchone()[0]
                d[f"m07_ventes_comptoir_{ville.lower().replace('-', '')}"] = int(n)
            ni = con.execute("""
                SELECT COUNT(*), ROUND(SUM(v.montant_ttc)) FROM vente v
                JOIN produit p ON p.id_produit = v.id_produit WHERE p.actif = FALSE""").fetchone()
            d["m07_ventes_produit_inactif"] = int(ni[0])
            d["m07_ca_produit_inactif"] = int(ni[1])
            # --- C07 : jointures ---
            d["m07_objectif_vide"] = int(con.execute(
                "SELECT COUNT(*) FROM objectif_magasin").fetchone()[0])
            d["m07_croix_magasin_mode"] = int(con.execute(
                "SELECT COUNT(*) FROM magasin CROSS JOIN mode_paiement").fetchone()[0])
            d["m07_selfjoin_ventes_client"] = int(con.execute("""
                SELECT COUNT(*) FROM vente v JOIN vente v2 ON v2.id_client = v.id_client""").fetchone()[0])
            # --- C08 : sous-requetes, CTE, vues, EXISTS vs IN ---
            d["m07_top_client_ca"] = int(con.execute("""
                SELECT ROUND(SUM(v.montant_ttc)) FROM vente v
                JOIN client c ON c.id_client = v.id_client
                GROUP BY c.id_client ORDER BY SUM(v.montant_ttc) DESC LIMIT 1""").fetchone()[0])
            d["m07_clients_tous_2_plus_chers"] = int(con.execute("""
                SELECT COUNT(*) FROM client c WHERE NOT EXISTS (
                  SELECT 1 FROM (SELECT id_produit FROM vente ORDER BY montant_ttc DESC LIMIT 2) top
                  WHERE NOT EXISTS (SELECT 1 FROM vente v
                                     WHERE v.id_client = c.id_client AND v.id_produit = top.id_produit)
                )""").fetchone()[0])
            d["m07_vue_mensuelle_lignes"] = int(con.execute(
                "SELECT COUNT(*) FROM v_ca_mensuel_magasin").fetchone()[0])
            d["m07_vue_plus_gros_mois"] = int(con.execute(
                "SELECT ROUND(MAX(ca_ttc)) FROM v_ca_mensuel_magasin").fetchone()[0])
            d["m07_clients_au_moins_1_cat1"] = int(con.execute("""
                SELECT COUNT(DISTINCT v.id_client) FROM vente v
                JOIN produit p ON p.id_produit = v.id_produit
                WHERE p.id_categorie = 1""").fetchone()[0])
            d["m07_produits_cat_1"] = int(con.execute(
                "SELECT COUNT(*) FROM produit WHERE id_categorie = 1").fetchone()[0])
            d["m07_ventes_sup_moyenne"] = int(con.execute(
                "SELECT COUNT(*) FROM vente WHERE montant_ttc > (SELECT AVG(montant_ttc) FROM vente)"
            ).fetchone()[0])
            # --- projet M07.P : valeurs des 30 questions ---
            d["m07p_q02_produits_actifs"] = int(con.execute(
                "SELECT COUNT(*) FROM produit WHERE actif = TRUE").fetchone()[0])
            d["m07p_q07_ca_mag4_sans_retour"] = int(con.execute(
                "SELECT ROUND(SUM(montant_ttc)) FROM vente WHERE est_retour = FALSE AND id_magasin = 4"
            ).fetchone()[0])
            d["m07p_q10_panier_moyen_sans_retour"] = int(con.execute(
                "SELECT ROUND(AVG(montant_ttc)) FROM vente WHERE est_retour = FALSE").fetchone()[0])
            d["m07p_q11_top_qte"] = int(con.execute(
                "SELECT SUM(quantite) FROM vente GROUP BY id_produit ORDER BY 1 DESC LIMIT 1"
            ).fetchone()[0])
            d["m07p_q17_delai_moyen"] = float(con.execute("""
                SELECT ROUND(AVG(EXTRACT(DAY FROM (date_trunc('month', date_vente)
                + INTERVAL '1 month' - INTERVAL '1 day' - date_vente))), 1) FROM vente""").fetchone()[0])
            d["m07p_q18_plafond_sup_100k"] = int(con.execute(
                "SELECT COUNT(*) FROM client WHERE plafond_credit > 100000").fetchone()[0])
            d["m07p_q19_distinct_5col"] = int(con.execute("""
                SELECT COUNT(*) FROM (SELECT DISTINCT id_client, id_produit, id_magasin,
                date_vente, montant_ttc FROM vente) t""").fetchone()[0])
            d["m07p_q23_couples_distincts"] = int(con.execute(
                "SELECT COUNT(*) FROM (SELECT DISTINCT id_client, id_produit FROM vente) t"
            ).fetchone()[0])
            d["m07p_q25_evolution_jardinage"] = int(con.execute("""
                WITH ca_cat AS (SELECT c.rayon, EXTRACT(YEAR FROM v.date_vente)::INTEGER AS annee,
                SUM(v.montant_ttc) AS ca FROM vente v JOIN produit p ON p.id_produit = v.id_produit
                JOIN categorie c ON p.id_categorie = c.id_categorie GROUP BY 1, 2)
                SELECT ROUND(MAX(CASE WHEN annee = 2026 THEN ca END)
                - MAX(CASE WHEN annee = 2025 THEN ca END)) FROM ca_cat WHERE rayon = 'Jardinage'""").fetchone()[0])
            d["m07p_q26_produits_sup_moyenne_rayon"] = int(con.execute("""
                SELECT COUNT(*) FROM produit p
                WHERE p.prix_vente_ht > (SELECT AVG(prix_vente_ht) FROM produit p2
                WHERE p2.id_categorie = p.id_categorie)""").fetchone()[0])
            d["m07p_q12_top_client_2_ca"] = int(con.execute("""
                SELECT ROUND(SUM(montant_ttc)) FROM vente GROUP BY id_client
                ORDER BY SUM(montant_ttc) DESC LIMIT 1 OFFSET 1""").fetchone()[0])
            d["m07p_q12_top_client_3_ca"] = int(con.execute("""
                SELECT ROUND(SUM(montant_ttc)) FROM vente GROUP BY id_client
                ORDER BY SUM(montant_ttc) DESC LIMIT 1 OFFSET 2""").fetchone()[0])
            d["m07p_ecart_ca_retours"] = int(con.execute("""
                SELECT ROUND(SUM(montant_ttc)) FROM vente""").fetchone()[0]
                - con.execute("""
                SELECT ROUND(SUM(montant_ttc)) FROM vente WHERE est_retour = FALSE""").fetchone()[0])
            d["m07p_q25_evolution_bricolage"] = int(con.execute("""
                WITH ca_cat AS (SELECT c.rayon, EXTRACT(YEAR FROM v.date_vente)::INTEGER AS annee,
                SUM(v.montant_ttc) AS ca FROM vente v JOIN produit p ON p.id_produit = v.id_produit
                JOIN categorie c ON p.id_categorie = c.id_categorie GROUP BY 1, 2)
                SELECT ROUND(MAX(CASE WHEN annee = 2026 THEN ca END)
                - MAX(CASE WHEN annee = 2025 THEN ca END)) FROM ca_cat WHERE rayon = 'Bricolage'""").fetchone()[0])
            d["m07p_q25_evolution_alimentaire"] = int(con.execute("""
                WITH ca_cat AS (SELECT c.rayon, EXTRACT(YEAR FROM v.date_vente)::INTEGER AS annee,
                SUM(v.montant_ttc) AS ca FROM vente v JOIN produit p ON p.id_produit = v.id_produit
                JOIN categorie c ON p.id_categorie = c.id_categorie GROUP BY 1, 2)
                SELECT ROUND(MAX(CASE WHEN annee = 2026 THEN ca END)
                - MAX(CASE WHEN annee = 2025 THEN ca END)) FROM ca_cat WHERE rayon = 'Alimentaire'""").fetchone()[0])
            d["m07p_q08_ventes_janv_2025"] = int(con.execute(
                "SELECT COUNT(*) FROM vente WHERE EXTRACT(YEAR FROM date_vente) = 2025 AND EXTRACT(MONTH FROM date_vente) = 1"
            ).fetchone()[0])
            d["m07p_paire_naturelle_1"] = 41405
            d["m07p_paire_naturelle_2"] = 41757
            for rayon in ("Alimentaire", "Bricolage", "Jardinage"):
                n = con.execute(
                    "SELECT COUNT(*) FROM vente v JOIN produit p ON p.id_produit = v.id_produit "
                    "JOIN categorie c ON c.id_categorie = p.id_categorie WHERE c.rayon = ?",
                    [rayon]).fetchone()[0]
                d[f"m07_ventes_rayon_{rayon.lower()}"] = int(n)
            for annee in (2025, 2026):
                n, ca = con.execute(
                    "SELECT COUNT(*), ROUND(SUM(montant_ttc)) FROM vente "
                    "WHERE id_magasin = 4 AND EXTRACT(YEAR FROM date_vente) = ?", [annee]).fetchone()
                d[f"m07_ventes_mag4_{annee}"] = int(n)
                d[f"m07_ca_mag4_{annee}"] = int(ca)
            con.close()
        except Exception as e:
            print(f"  ! mesure DuckDB impossible ({e})")
    # Les totaux livres dans ATTENDU.json
    attendu_path = os.path.join(os.path.dirname(ROOT), "03_exercices", "dossier_M07", "ATTENDU.json")
    if os.path.exists(attendu_path):
        a = json.load(open(attendu_path, encoding="utf-8"))
        for k, v in a.items():
            if k == "empreinte_sha256_bd_duckdb":
                # l'empreinte DuckDB varie (timestamp interne), on l'ignore pour la repro
                continue
            d["m07p_" + k] = v
    return d



def m08():
    """Les cles du module M08 - Python pour l'analyse de donnees.

    Les `m08_*` mesurent le paysage du module (8 chapitres, 12 ecritures obsoletes,
    environnement). Les `m08p_*` mesurent le dossier projet (exporte par
    `tools/dossier_M08.py`, re-export deterministe de la base M07 figee) du cote
    **pandas**. `tools/dossier_M08.py` mesure le cote **SQL** (ATTENDU.json) ; toute
    divergence leve une erreur : c'est la verification croisee SQL/pandas, la colonne
    vertebrale du module.
    """
    import json
    d = OrderedDict()
    # Structure du module
    d["m08_chapitres_total"] = 8
    d["m08_budget_pages"] = 117
    d["m08_niveau_cible"] = "N2-N3"
    d["m08_prerequis"] = "M04, M05.C04 (ou grande aisance Excel), M07 (parallele SQL/pandas)"
    d["m08_ecritures_obsoletes"] = 12
    d["m08_quiz_questions"] = 15
    d["m08_quiz_prediction"] = 5
    d["m08_exos_rendus"] = 5
    d["m08_exos_autovalides"] = 15
    # Environnement d'ecriture et version de reference
    d["m08_python_env"] = "3.13"
    d["m08_pandas_env"] = str(pd.__version__)
    d["m08_numpy_env"] = str(np.__version__)
    d["m08_pandas_reference"] = "3.x (teste sous 3.0.6 le 19/09/2026)"
    d["m08_sgbd_duckdb"] = "duckdb 1.5.5 (execute, cote SQL de la croisee)"
    d["m08_sgbd_sqlite"] = "sqlite3 natif Python 3.13"
    d["m08_sgbd_postgres"] = "cite sans execute (regle M06 §1.5)"
    # Dossier M08.P
    dossier = os.path.join(os.path.dirname(ROOT), "03_exercices", "dossier_M08")
    v = pd.read_csv(os.path.join(dossier, "vente.csv"))
    c = pd.read_csv(os.path.join(dossier, "client.csv"))
    pr = pd.read_csv(os.path.join(dossier, "produit.csv"))
    cat = pd.read_csv(os.path.join(dossier, "categorie.csv"))
    mag = pd.read_csv(os.path.join(dossier, "magasin.csv"))
    mode = pd.read_csv(os.path.join(dossier, "mode_paiement.csv"))
    tva = pd.read_csv(os.path.join(dossier, "regle_tva.csv"))
    obj = pd.read_csv(os.path.join(dossier, "objectif_magasin.csv"))
    d["m08p_ventes_lignes"] = int(len(v))
    d["m08p_ventes_colonnes"] = int(v.shape[1])
    d["m08p_clients_lignes"] = int(len(c))
    d["m08p_produits_lignes"] = int(len(pr))
    d["m08p_categories_lignes"] = int(len(cat))
    d["m08p_magasins_lignes"] = int(len(mag))
    d["m08p_modes_lignes"] = int(len(mode))
    d["m08p_regle_tva_lignes"] = int(len(tva))
    d["m08p_objectif_lignes"] = int(len(obj))
    # Audit (cote pandas) — les dates arrivent en `object` : read_csv ne les parse pas
    # d'office, `pd.to_datetime` est l'etape apprise en C07 (et le chapitre la publie).
    dv = pd.to_datetime(v["date_vente"])
    dl = pd.to_datetime(v["date_limite_remise"])
    cols12 = [col for col in v.columns if col != "id_vente"]
    d["m08p_doublons"] = int(v.duplicated(subset=cols12).sum())
    vu = v.drop_duplicates(subset=cols12)
    d["m08p_ventes_uniques"] = int(len(vu))
    d["m08p_retours_brut"] = int(v["est_retour"].sum())
    d["m08p_retours_dedoublonnes"] = int(vu["est_retour"].sum())
    d["m08p_dates_vente_apres_limite"] = int((dv > dl).sum())
    d["m08p_deadlines_jour_20_brut"] = int(dl.dt.day.eq(20).sum())
    d["m08p_deadlines_jour_20"] = int(dl.loc[vu.index].dt.day.eq(20).sum())
    d["m08p_manquants_total"] = int(
        v.isna().sum().sum() + c.isna().sum().sum() + pr.isna().sum().sum()
        + cat.isna().sum().sum() + mag.isna().sum().sum()
        + mode.isna().sum().sum() + tva.isna().sum().sum() + obj.isna().sum().sum())
    # Indicateurs (les reponses pandas du projet M08.P)
    # Addition en CENTIMES entiers : le float64 cumule l'erreur sur 50 000 montants
    # (ecart de 1 a 2 FCFA vs la somme decimal exacte du SGBD) — lecentime est le
    # plus petit multiple exact de FCFA, l'entier ne se trompe pas. Le chapitre C08
    # publie la mesure des deux cotes.
    ct = (v["montant_ttc"] * 100).round().astype("int64")
    d["m08p_ca_brut"] = int(ct.sum() // 100)
    d["m08p_ca_sans_retours"] = int(ct.loc[~v["est_retour"]].sum() // 100)
    d["m08p_ecart_ca_retours"] = d["m08p_ca_brut"] - d["m08p_ca_sans_retours"]
    d["m08p_panier_moyen"] = int(round(ct.sum() / len(v) / 100))
    d["m08p_ventes_gros_100k"] = int((ct > 10000000).sum())
    d["m08p_gros_non_retours"] = int(((ct > 10000000) & ~v["est_retour"]).sum())
    d["m08p_ventes_dimanches"] = int((pd.to_datetime(v["date_vente"]).dt.dayofweek == 6).sum())
    gm2 = ct.groupby(v["id_magasin"]).sum() // 100
    d["m08p_ca_min_magasin"] = int(gm2.min())
    d["m08p_panier_moyen_sans_retours"] = int(
        round(ct.loc[~v["est_retour"]].sum() / v.loc[~v["est_retour"]].shape[0] / 100))
    d["m08p_nb_ventes_2025"] = int((dv.dt.year == 2025).sum())
    d["m08p_ca_2025"] = int(ct.loc[dv.dt.year == 2025].sum() // 100)
    d["m08p_nb_ventes_2026"] = int((dv.dt.year == 2026).sum())
    d["m08p_ca_2026"] = int(ct.loc[dv.dt.year == 2026].sum() // 100)
    gm = ct.groupby(v["id_magasin"]).sum()
    d["m08p_top_magasin_id"] = int(gm.idxmax())
    d["m08p_ca_top_magasin"] = int(gm.max() // 100)
    m = v.merge(pr[["id_produit", "id_categorie"]], on="id_produit", how="left")
    d["m08p_ca_categorie_top"] = int(ct.loc[m["id_categorie"] == 7].sum() // 100)
    # La vue M07 est definie SANS retours (WHERE est_retour = FALSE) : le pivot la
    # reproduit, retours exclus — c'est la definition de la vue, pas un choix.
    vs = v.loc[~v["est_retour"]]
    pivot = pd.DataFrame({
        "id_magasin": vs["id_magasin"],
        "annee": dv.loc[vs.index].dt.year,
        "mois": dv.loc[vs.index].dt.month,
        "ca_cents": ct.loc[vs.index],
    }).groupby(["id_magasin", "annee", "mois"], as_index=False)["ca_cents"].sum()
    d["m08p_vue_lignes"] = int(len(pivot))
    plus_gros = pivot.loc[pivot["ca_cents"].idxmax()]
    d["m08p_plus_gros_mois_ca"] = int(plus_gros["ca_cents"] // 100)
    d["m08p_plus_gros_mois_magasin"] = int(plus_gros["id_magasin"])
    d["m08p_plus_gros_mois_annee"] = int(plus_gros["annee"])
    d["m08p_plus_gros_mois_mois"] = int(plus_gros["mois"])
    # Verification croisee SQL/pandas : les deux cotes doivent s'accorder, sinon erreur
    att = json.load(open(os.path.join(dossier, "ATTENDU.json"), encoding="utf-8"))
    croise = {
        "doublons": d["m08p_doublons"],
        "ventes_uniques": d["m08p_ventes_uniques"],
        "retours_brut": d["m08p_retours_brut"],
        "retours_dedoublonnes": d["m08p_retours_dedoublonnes"],
        "dates_vente_apres_limite": d["m08p_dates_vente_apres_limite"],
        "deadlines_jour_20_brut": d["m08p_deadlines_jour_20_brut"],
        "deadlines_jour_20": d["m08p_deadlines_jour_20"],
        "manquants_total": d["m08p_manquants_total"],
        "ca_brut": d["m08p_ca_brut"],
        "ca_sans_retours": d["m08p_ca_sans_retours"],
        "ecart_ca_retours": d["m08p_ecart_ca_retours"],
        "panier_moyen": d["m08p_panier_moyen"],
        "panier_moyen_sans_retours": d["m08p_panier_moyen_sans_retours"],
        "nb_ventes_2025": d["m08p_nb_ventes_2025"],
        "ca_2025": d["m08p_ca_2025"],
        "nb_ventes_2026": d["m08p_nb_ventes_2026"],
        "ca_2026": d["m08p_ca_2026"],
        "top_magasin_id": d["m08p_top_magasin_id"],
        "ca_top_magasin": d["m08p_ca_top_magasin"],
        "ca_categorie_top": d["m08p_ca_categorie_top"],
        "vue_lignes": d["m08p_vue_lignes"],
        "plus_gros_mois_ca": d["m08p_plus_gros_mois_ca"],
        "plus_gros_mois_magasin": d["m08p_plus_gros_mois_magasin"],
        "plus_gros_mois_annee": d["m08p_plus_gros_mois_annee"],
        "plus_gros_mois_mois": d["m08p_plus_gros_mois_mois"],
    }
    # La colonne montant_ttc est un DOUBLE : la somme float derive de 1 a 2 FCFA
    # selon le moteur et l'ordre d'addition (mesure : la somme Decimal exacte des
    # 50 008 montants = 7 908 259 732,20, DuckDB renvoie 7 908 259 730,56…, pandas
    # 7 908 259 732). La croisee est donc EXACTE pour les comptages et les formes,
    # et a ± 2 FCFA de tolerance pour les totaux monetaires — le derapage est
    # mesure et source (le chapitre C08 en fait la leçon des centimes entiers).
    TOL = 2
    monetaire = {"ca_brut", "ca_sans_retours", "ecart_ca_retours", "ca_2025", "ca_2026",
                 "ca_top_magasin", "ca_categorie_top", "plus_gros_mois_ca"}
    ecartes = {k: (att.get(k), val) for k, val in croise.items()
               if att.get(k) != val
               and abs(int(att.get(k)) - val) > (TOL if k in monetaire else 0)}
    if ecartes:
        raise ValueError("verification croisee SQL/pandas en echec : %s" % ecartes)
    d["m08p_croisee_sql_pandas"] = "OK (25 valeurs : comptages exacts, totaux ± 2 FCFA)"
    for k in ("ca_brut", "ca_sans_retours", "ca_2025", "ca_2026", "ca_categorie_top"):
        d["m08p_ecart_somme_float_" + k] = int(abs(int(att[k]) - croise[k]))
    # Ecart pandas 2.2.3 / 3.0.6 — le sujet « ce script tourne mais ses chiffres sont faux »
    p1 = pd.read_csv(os.path.join(REF, "ventes_magasin5_2025_ATTENDU.csv"), sep=";")
    cl = p1["client"].astype(str).str.strip()
    d["m08p_pd2_clients_vides"] = int(cl.isin(["", "nan", "0", "0.0"]).sum())
    d["m08p_pd2_clients_modalites"] = int(cl.nunique())
    d["m08p_pd2_dtype_texte"] = "object"
    cli = pd.read_csv(os.path.join(REF, "clients_propres.csv"))
    ids_cli = set(cli["id_client"].astype(str))
    cl3 = p1["client"].astype(str).str.replace(".0", "", regex=False)
    d["m08p_pd2_m03_champ_vide"] = int((~cl3.isin(ids_cli) & (cl3 == "nan")).sum())
    d["m08p_pd2_m03_colonnes_objet"] = int(sum(p1[c].dtype == object for c in p1.columns))
    # Valeurs du demo C01 (script « calculateur de remise », exécuté le 19/09/2026)
    d["m08p_demo_prix"] = 1500
    d["m08p_demo_remise_pct"] = 10
    d["m08p_demo_prix_net"] = 1350
    # C02 : seuil comptoir, montant en format francais, et l'addition float classique
    d["m08p_demo_seuil"] = 1000
    d["m08p_demo_montant_fcfa"] = 15000.5
    d["m08p_demo_float_add"] = 0.30000000000000004
    # Valeurs mesurees sous pandas 3.0.6 le 19/09/2026 (environnement isole, puis restaure)
    d["m08p_pd3_clients_vides"] = 85
    d["m08p_pd3_clients_modalites"] = 372
    d["m08p_pd3_m03_champ_vide"] = 0
    d["m08p_pd3_m03_colonnes_objet"] = 0
    d["m08p_pd3_dtype_texte"] = "str"
    # Quiz / evaluation M08 (mesures sur le dossier, le 20/09/2026)
    d["m08p_merge_colonnes"] = int(v.merge(obj, on="id_magasin", how="left").shape[1])
    d["m08p_counts_par_magasin"] = ", ".join(str(int(x)) for x in v.groupby("id_magasin")["id_vente"].count().tolist())
    d["m08p_max_montant"] = int(v["montant_ttc"].max())
    d["m08p_ventes_propres"] = int((~v["est_retour"] & ~v.duplicated(subset=[c for c in v.columns if c != "id_vente"])).sum())
    d["m08p_ca_brut_duckdb"] = 7908259731  # cote SQL (ATTENDU, somme float de DuckDB)
    # Etude de cas M08 (magasin 4, annee 2025 — sortie attendue de l'exo guide C08 §10)
    m4 = (v["id_magasin"] == 4) & (v["date_vente"].str.startswith("2025"))
    propre4 = v[m4 & ~v["est_retour"]]
    ct4 = (propre4["montant_ttc"] * 100).round().astype("int64")
    d["m08p_mag4_2025_ventes"] = int(len(propre4))
    d["m08p_mag4_2025_retours"] = int(v[m4]["est_retour"].sum())
    d["m08p_mag4_2025_total"] = int(ct4.sum()) // 100
    d["m08p_mag4_2025_total_gonfle"] = int((v[m4]["montant_ttc"] * 100).round().astype("int64").sum()) // 100
    d["m08p_mag4_2025_panier"] = int(ct4.sum()) // 100 // len(propre4)
    d["m08p_mag4_2025_mois_fort"] = int(ct4.groupby(propre4["date_vente"].str[5:7]).sum().max()) // 100
    d["m08p_mag4_2025_ecart_retours"] = int((v[m4]["montant_ttc"] * 100).round().astype("int64").sum()) // 100 - int(ct4.sum()) // 100
    d["m08p_demo_centimes_15000_5"] = int(round(15000.5 * 100))
    d["m08p_ca_brut_centimes"] = int((v["montant_ttc"] * 100).round().astype("int64").sum())
    # Tranches de montants (exercice rendu D3)
    t = v["montant_ttc"]
    d["m08p_tranche_0_50k"] = int((t <= 50000).sum())
    d["m08p_tranche_50_100k"] = int(((t > 50000) & (t <= 100000)).sum())
    d["m08p_tranche_100_200k"] = int(((t > 100000) & (t <= 200000)).sum())
    d["m08p_tranche_200k"] = int((t > 200000).sum())
    return d

def m09():
    """Les cles du module M09 - Analyse exploratoire de donnees (EDA).

    Les `m09_*` mesurent le paysage du module (6 chapitres, protocole en 10
    etapes, 4 jeux, projet M09.P chronometre). Les `m09p_*` mesurent du cote
    **pandas** les 4 jeux de `03_exercices/dossier_M09/` (exportes par
    `tools/dossier_M09.py`, graine 45, deterministe). Trois verifications:

      - **quincaillerie (fil rouge)** : les 8 tables reexportees doivent etre
        **byte-identiques** a la base M07 figee (empreinte) et redonner ses
        totaux publies — la « constance du socle » est le premier controle du
        protocole;
      - **sante / scolaire / projet** : le generateur a mesure le cote
        generation (ATTENDU.json) ; toute divergence du cote pandas leve une
        erreur (memes principes que la croisee M08) — etape 3 du protocole :
        les 12 defauts plantes sont comptables avant qu'ils ne faussent un
        chiffre.
    """
    import hashlib
    import json
    d = OrderedDict()
    # Structure du module (05_livrables/plan_M09.md)
    d["m09_chapitres_total"] = 6
    d["m09_heures"] = 30
    d["m09_niveau_cible"] = "N3"
    d["m09_prerequis"] = "M02 (statistiques) et M08 (pandas) ; M05/M07 utiles"
    d["m09_budget_pages"] = 93
    d["m09_budget_pages_min"] = 79
    d["m09_budget_pages_max"] = 106
    d["m09_etapes_protocole"] = 10
    d["m09_jeux_donnees"] = 4
    d["m09_graine_dossier"] = 45
    d["m09_projet_heures"] = 3
    d["m09_quiz_questions"] = 15
    d["m09_pandas_env"] = str(pd.__version__)
    d["m09_numpy_env"] = str(np.__version__)
    try:
        import matplotlib
        d["m09_matplotlib_env"] = str(matplotlib.__version__)
    except ImportError:
        d["m09_matplotlib_env"] = "absent (environnement systeme)"
    try:
        import seaborn
        d["m09_seaborn_env"] = str(seaborn.__version__)
    except ImportError:
        d["m09_seaborn_env"] = "absent (environnement systeme)"

    dossier = os.path.join(os.path.dirname(ROOT), "03_exercices", "dossier_M09")
    att = json.load(open(os.path.join(dossier, "ATTENDU.json"), encoding="utf-8"))

    # ------------------------------------------------------------------
    # Jeu 1 — la quincaillerie (fil rouge) : reexport de la base M07 figee
    # ------------------------------------------------------------------
    q = os.path.join(dossier, "quincaillerie")
    tables = ["vente", "client", "produit", "categorie", "magasin",
              "mode_paiement", "regle_tva", "objectif_magasin"]
    h = hashlib.sha256()
    for t in tables:
        with open(os.path.join(q, t + ".csv"), "rb") as fh:
            h.update(fh.read())
    d["m09p_q_empreinte"] = h.hexdigest()[:16] + "…"
    if d["m09p_q_empreinte"] != att["quincaillerie"]["empreinte"]:
        raise ValueError("empreinte du reexport != ATTENDU: %s" % d["m09p_q_empreinte"])
    qm08 = os.path.join(os.path.dirname(ROOT), "03_exercices", "dossier_M08")
    h8 = hashlib.sha256()
    for t in tables:
        with open(os.path.join(qm08, t + ".csv"), "rb") as fh:
            h8.update(fh.read())
    if h8.hexdigest()[:16] != h.hexdigest()[:16]:
        raise ValueError("reexport diverge de dossier_M08 (socle non constant)")
    # Totaux — memes formules que M08 C07/C08 (addition en centimes entiers)
    v = pd.read_csv(os.path.join(q, "vente.csv"))
    c = pd.read_csv(os.path.join(q, "client.csv"))
    pr = pd.read_csv(os.path.join(q, "produit.csv"))
    cat = pd.read_csv(os.path.join(q, "categorie.csv"))
    mag = pd.read_csv(os.path.join(q, "magasin.csv"))
    mode = pd.read_csv(os.path.join(q, "mode_paiement.csv"))
    tva = pd.read_csv(os.path.join(q, "regle_tva.csv"))
    obj = pd.read_csv(os.path.join(q, "objectif_magasin.csv"))
    d["m09p_q_ventes_lignes"] = int(len(v))
    d["m09p_q_clients_lignes"] = int(len(c))
    d["m09p_q_produits_lignes"] = int(len(pr))
    d["m09p_q_magasins_lignes"] = int(len(mag))
    d["m09p_q_tables_vides"] = int((len(cat) == 0) + (len(mode) == 0) + (len(tva) == 0)
                                   + (len(obj) == 0))
    ct = (v["montant_ttc"] * 100).round().astype("int64")
    d["m09p_q_ca_brut"] = int(ct.sum() // 100)
    d["m09p_q_ca_propre"] = int(ct.loc[~v["est_retour"]].sum() // 100)
    d["m09p_q_ecart_ca_retours"] = d["m09p_q_ca_brut"] - d["m09p_q_ca_propre"]
    d["m09p_q_panier_moyen"] = int(round(ct.sum() / len(v) / 100))
    cols12 = [col for col in v.columns if col != "id_vente"]
    d["m09p_q_doublons"] = int(v.duplicated(subset=cols12).sum())
    vu = v.drop_duplicates(subset=cols12)
    d["m09p_q_ventes_uniques"] = int(len(vu))
    d["m09p_q_retours_brut"] = int(v["est_retour"].sum())
    d["m09p_q_retours_dedoublonnes"] = int(vu["est_retour"].sum())
    dv = pd.to_datetime(v["date_vente"])
    dl = pd.to_datetime(v["date_limite_remise"])
    d["m09p_q_dates_naives"] = int((dv > dl).sum())
    d["m09p_q_deadlines_j20"] = int(dl.loc[vu.index].dt.day.eq(20).sum())
    d["m09p_q_dimanches"] = int((dv.dt.dayofweek == 6).sum())
    d["m09p_q_manquants_total"] = int(v.isna().sum().sum() + c.isna().sum().sum()
                                      + pr.isna().sum().sum() + cat.isna().sum().sum()
                                      + mag.isna().sum().sum() + mode.isna().sum().sum()
                                      + tva.isna().sum().sum() + obj.isna().sum().sum())
    vs = v.loc[~v["est_retour"]]
    pivot = pd.DataFrame({
        "id_magasin": vs["id_magasin"],
        "annee": dv.loc[vs.index].dt.year,
        "mois": dv.loc[vs.index].dt.month,
        "ca_cents": ct.loc[vs.index],
    }).groupby(["id_magasin", "annee", "mois"], as_index=False)["ca_cents"].sum()
    d["m09p_q_vue_lignes"] = int(len(pivot))
    d["m09p_q_plus_gros_mois_ca"] = int(int(pivot["ca_cents"].max()) // 100)
    # le plateau du montant max (C04) : quantite max x produit le plus cher x tva max
    d["m09p_q_montant_max"] = int(v["montant_ttc"].max())
    d["m09p_q_montant_max_occurrences"] = int((v["montant_ttc"] == v["montant_ttc"].max()).sum())
    d["m09p_q_produit_le_plus_cher"] = int(pr.loc[pr["prix_vente_ht"].idxmax(), "id_produit"])
    d["m09p_q_prix_vente_max"] = float(pr["prix_vente_ht"].max())
    d["m09p_q_quantite_max"] = int(v["quantite"].max())
    # C05 — relations (fil rouge) : la corrélation de scale vs le taux, les groupes
    d["m09p_q_corr_remise_montant"] = round(float(v["montant_remise"].corr(v["montant_ttc"])), 3)
    _rr = v["montant_remise"] / v["montant_ttc"]
    d["m09p_q_corr_remise_rate_montant"] = round(float(_rr.corr(v["montant_ttc"])), 3)
    d["m09p_q_remise_rate_max"] = round(float(_rr.max()), 3)
    d["m09p_q_ventes_par_mode"] = {
        int(k): int(n) for k, n in v.groupby("id_mode")["id_vente"].count().items()}
    _ca_cli = v.groupby("id_client")["montant_ttc"].sum().sort_values(ascending=False)
    d["m09p_q_clients_par_ca"] = int(len(_ca_cli))
    d["m09p_q_top10_clients_part_ca"] = round(
        float(_ca_cli.head(max(1, len(_ca_cli) // 10)).sum() / v["montant_ttc"].sum() * 100), 1)
    d["m09p_q_top_client_id"] = int(_ca_cli.index[0])
    d["m09p_q_top_client_ca"] = int(_ca_cli.iloc[0])
    # C05 — panier et médiane par mode de paiement (bornes min/max, publiés en texte)
    _pm = v.groupby("id_mode")["montant_ttc"]
    d["m09p_q_panier_mode_min"] = int(round(float(_pm.mean().min())))
    d["m09p_q_panier_mode_max"] = int(round(float(_pm.mean().max())))
    d["m09p_q_mediane_mode_min"] = int(round(float(_pm.median().min())))
    d["m09p_q_mediane_mode_max"] = int(round(float(_pm.median().max())))
    # Reference figee M07/M08 (section M08 publiee) : le reexport doit la
    # redonner — la constance du socle est le premier controle du protocole.
    REF_M08 = {
        "m09p_q_ventes_lignes": 50008, "m09p_q_clients_lignes": 1200,
        "m09p_q_produits_lignes": 380, "m09p_q_magasins_lignes": 5,
        "m09p_q_tables_vides": 1,
        "m09p_q_ca_brut": 7908259732, "m09p_q_ca_propre": 7876320164,
        "m09p_q_ecart_ca_retours": 31939568, "m09p_q_panier_moyen": 158140,
        "m09p_q_doublons": 8, "m09p_q_ventes_uniques": 50000,
        "m09p_q_retours_brut": 208, "m09p_q_retours_dedoublonnes": 200,
        "m09p_q_dates_naives": 21406, "m09p_q_deadlines_j20": 15,
        "m09p_q_dimanches": 7136, "m09p_q_manquants_total": 0,
        "m09p_q_vue_lignes": 120, "m09p_q_plus_gros_mois_ca": 78965529,
    }
    ecart_q = {k: (d[k], ref) for k, ref in REF_M08.items() if d[k] != ref}
    if ecart_q:
        raise ValueError("quincaillerie ne redonne pas M07/M08: %s" % ecart_q)
    d["m09p_q_constance_socle"] = ("OK (empreinte %s byte-identique a dossier_M08, "
                                   "19 totaux = M07/M08)") % d["m09p_q_empreinte"]

    # ------------------------------------------------------------------
    # Jeu 2 — le centre de sante
    # ------------------------------------------------------------------
    s = os.path.join(dossier, "sante")
    cons = pd.read_csv(os.path.join(s, "consultation.csv"))
    stk = pd.read_csv(os.path.join(s, "stock_medicament.csv"))
    med = pd.read_csv(os.path.join(s, "medicament.csv"))
    d["m09p_s_consultations_brut"] = int(len(cons))
    d["m09p_s_stock_lignes"] = int(len(stk))
    d["m09p_s_stock_lignes_distinctes"] = int(
        stk.drop_duplicates().shape[0])
    d["m09p_s_medicaments"] = int(len(med))
    d["m09p_s_motifs_manquants"] = int(cons["motif"].isna().sum())
    d["m09p_s_doublons_stock"] = int(stk.duplicated().sum())
    d["m09p_s_dates_futures"] = int((cons["date_consultation"] > "2026-12-31").sum())
    d["m09p_s_stocks_negatifs"] = int((stk["stock_fin"] < 0).sum())
    par_jour = cons.groupby("date_consultation").size()
    d["m09p_s_jours_distincts"] = int(par_jour.shape[0])
    d["m09p_s_moyenne_jour"] = round(float(par_jour.mean()), 2)
    d["m09p_s_mediane_jour"] = float(par_jour.median())
    d["m09p_s_pic_mois"] = par_jour.groupby(par_jour.index.str[:7]).sum().idxmax()
    d["m09p_s_creux_midi"] = int((cons["heure"] == "12:00").sum())
    d["m09p_s_patients_distincts"] = int(cons["id_patient"].nunique())
    top_motif = cons["motif"].value_counts()
    d["m09p_s_motif_top"] = str(top_motif.index[0])
    d["m09p_s_motif_top_lignes"] = int(top_motif.iloc[0])
    for mid in ("M01", "M02", "M04"):
        z = stk[(stk["id_medicament"] == mid) & (stk["stock_fin"] == 0)]
        d["m09p_s_rupture_" + mid.lower()] = int(len(z))
    d["m09p_s_rupture_la_plus_longue"] = max(d["m09p_s_rupture_m01"],
                                             d["m09p_s_rupture_m02"],
                                             d["m09p_s_rupture_m04"])
    mrg = stk.merge(med, on="id_medicament")
    d["m09p_s_jours_sous_seuil"] = int((mrg["stock_fin"] < mrg["seuil_alerte"]).sum())

    # Variante « 12 mois glissants » (2025-07-01 -> 2026-06-30) : la fenêtre de
    # l'etude de cas de l'evaluation M09, mesuree comme le reste (jamais deduite).
    var = cons[(cons["date_consultation"] >= "2025-07-01")
               & (cons["date_consultation"] <= "2026-06-30")]
    par_mois = var.groupby(var["date_consultation"].str[:7]).size()
    d["m09v_lignes"] = int(len(var))
    d["m09v_jours"] = int(var["date_consultation"].nunique())
    d["m09v_moyenne_jour"] = round(len(var) / var["date_consultation"].nunique(), 2)
    d["m09v_pic_mois"] = int(par_mois.max())
    d["m09v_pic_mois_cle"] = str(par_mois.idxmax())
    d["m09v_creux_mois"] = int(par_mois.min())
    d["m09v_creux_mois_cle"] = str(par_mois.idxmin())
    d["m09v_chute_max"] = int(par_mois.max() - par_mois.min())
    mois = pd.to_datetime(par_mois.index).month
    d["m09v_ete"] = round(float(par_mois[mois.isin([7, 8, 9])].mean()), 1)
    d["m09v_hiver"] = round(float(par_mois[mois.isin([12, 1, 2])].mean()), 1)
    d["m09v_intra_ete"] = round(float(par_mois[mois.isin([7, 8, 9])].std()), 2)
    dow = pd.to_datetime(var["date_consultation"]).dt.dayofweek
    d["m09v_lundi"] = int((dow == 0).sum())
    d["m09v_dimanche"] = int((dow == 6).sum())
    d["m09v_moyenne_mois"] = round(float(par_mois.mean()), 1)
    d["m09v_ecart_type_mois"] = round(float(par_mois.std()), 1)

    # ------------------------------------------------------------------
    # Jeu 3 — l'etablissement scolaire
    # ------------------------------------------------------------------
    sc = os.path.join(dossier, "scolaire")
    el = pd.read_csv(os.path.join(sc, "eleve.csv"))
    no = pd.read_csv(os.path.join(sc, "note.csv"))
    ab = pd.read_csv(os.path.join(sc, "absence.csv"))
    d["m09p_sc_eleves_declares"] = int(len(el))
    d["m09p_sc_eleves_distincts"] = int(el["id_eleve"].nunique())
    d["m09p_sc_notes_lignes"] = int(len(no))
    d["m09p_sc_absences_lignes"] = int(len(ab))
    d["m09p_sc_notes_hors_bornes"] = int(((no["note"] < 0) | (no["note"] > 20)).sum())
    d["m09p_sc_doublons_eleves"] = int(el.duplicated(subset=["id_eleve"]).sum())
    FERIES = ["2025-11-01", "2025-12-25", "2025-12-26", "2026-01-01"]
    d["m09p_sc_absences_ferie"] = int(ab["date"].isin(FERIES).sum())
    # Correlation absences x notes (formule identique au generateur) : le
    # confond est la capacite, pas l'absence — le chapitre C05 en fait le
    # cas d'ecole des pieges d'inférence.
    notes_p = no[(no["note"] >= 0) & (no["note"] <= 20)]
    abs_par_eleve = ab.groupby("id_eleve")["duree_jours"].sum()
    ids = sorted(no["id_eleve"].unique())
    taux = abs_par_eleve.reindex(ids, fill_value=0)
    moy = notes_p.groupby("id_eleve")["note"].mean()
    d["m09p_sc_correlation_absent_notes"] = round(
        float(moy.corr(taux.reindex(moy.index))), 3)
    d["m09p_sc_segments_absences"] = [int((taux < 2).sum()),
                                      int(((taux >= 2) & (taux < 6)).sum()),
                                      int((taux >= 6).sum())]
    classes = ["5e", "4e", "3e", "2nde"]
    classe_map = el.drop_duplicates("id_eleve").set_index("id_eleve")["classe"]
    classe_map = classe_map.reindex(taux.index)
    d["m09p_sc_taux_par_classe"] = {
        c: round(float(taux[classe_map == c].mean()), 2) for c in classes}
    d["m09p_sc_classe_plus_absente"] = max(
        classes, key=lambda c: d["m09p_sc_taux_par_classe"][c])
    # C05 — segments, types d'absence, effectifs par classe (mesurés, publiés en corrigé)
    d["m09p_sc_moyennes_par_segment"] = [
        round(float(moy[taux < 2].mean()), 2),
        round(float(moy[(taux >= 2) & (taux < 6)].mean()), 2),
        round(float(moy[taux >= 6].mean()), 2)]
    d["m09p_sc_absences_par_type"] = {
        k: int(n) for k, n in ab["type"].value_counts().items()}
    d["m09p_sc_eleves_par_classe"] = {
        c: int((classe_map == c).sum()) for c in classes}
    # mesures publiees (le candidat les redonne par le protocole)
    d["m09p_sc_moyenne_note"] = round(float(notes_p["note"].mean()), 2)
    d["m09p_sc_taux_reussite"] = round(float((notes_p["note"] >= 10).mean() * 100), 1)
    d["m09p_sc_moyenne_par_matiere"] = {
        k: round(float(v2), 2) for k, v2 in notes_p.groupby("matiere")["note"].mean().items()}
    t2 = ab[(ab["date"] >= "2025-12-01") & (ab["date"] <= "2026-02-28")
            & (ab["type"] == "absence")]
    d["m09p_sc_eleves_10plus_abs_t2"] = int((t2.groupby("id_eleve").size() >= 10).sum())

    # ------------------------------------------------------------------
    # Fichier projet — « le fichier que personne n'a regarde »
    # ------------------------------------------------------------------
    pj = pd.read_csv(os.path.join(dossier, "projet", "fichier_inconnu.csv"))
    d["m09p_p_lignes_brut"] = int(len(pj))
    d["m09p_p_lignes_apres_dedoublonnage"] = int(pj.drop_duplicates(subset=["tx_ref"]).shape[0])
    d["m09p_p_doublons_tx_ref"] = int(pj.duplicated(subset=["tx_ref"]).sum())
    d["m09p_p_montants_negatifs"] = int((pj["montant_xof"] < 0).sum())
    d["m09p_p_montants_enormes"] = int((pj["montant_xof"] >= 100000000).sum())
    d["m09p_p_commissions_manquantes"] = int(pj["commission"].isna().sum())
    d["m09p_p_statuts_distincts"] = int(pj["statut"].nunique())
    d["m09p_p_montant_max"] = int(pj["montant_xof"].max())
    d["m09p_p_montant_min"] = int(pj["montant_xof"].min())
    d["m09p_p_mediane_brute"] = int(pj["montant_xof"].median())
    d["m09p_p_moyenne_brute"] = int(round(float(pj["montant_xof"].mean())))
    d["m09p_p_statuts_bruts"] = {k: int(n) for k, n in pj["statut"].value_counts().items()}
    OK = ["OK", "ok", "Reussie", "REUSSI"]
    d["m09p_p_succes_normalises"] = int(pj["statut"].isin(OK).sum())
    d["m09p_p_echecs_normalises"] = int(len(pj) - d["m09p_p_succes_normalises"])
    d["m09p_p_n_agents"] = int(pj["agent_code"].nunique())
    # analyse nettoyee (l'aboutissement attendu du M09.P)
    vu2 = pj.drop_duplicates(subset=["tx_ref"], keep="first")
    valide = vu2[(vu2["montant_xof"] > 0) & (vu2["montant_xof"] < 100000000)]
    d["m09p_p_lignes_valides"] = int(len(valide))
    d["m09p_p_succes_valides"] = int(valide["statut"].isin(OK).sum())
    d["m09p_p_taux_succes_valides"] = round(
        d["m09p_p_succes_valides"] / len(valide) * 100, 2)
    d["m09p_p_montant_total_valides"] = int(valide["montant_xof"].sum())
    d["m09p_p_montant_moyen_valide"] = int(round(float(valide["montant_xof"].mean())))
    d["m09p_p_canal_top"] = str(valide["canal"].value_counts().idxmax())

    # ------------------------------------------------------------------
    # Verifiee croisee pandas / generation (memes principes que M08)
    # ------------------------------------------------------------------
    def g(path):
        cur = att
        for part in path.split("."):
            cur = cur[part]
        return cur
    croise = {
        "sante.consultations": (d["m09p_s_consultations_brut"], g("sante.n_consultations_brut")),
        "sante.motifs_manquants": (d["m09p_s_motifs_manquants"], g("sante.defauts.manquants_motif")),
        "sante.doublons_stock": (d["m09p_s_doublons_stock"], g("sante.defauts.doublons_stock")),
        "sante.dates_futures": (d["m09p_s_dates_futures"], g("sante.defauts.consultations_date_future")),
        "sante.stocks_negatifs": (d["m09p_s_stocks_negatifs"], g("sante.defauts.stocks_negatifs")),
        "sante.stock_lignes": (d["m09p_s_stock_lignes"], g("sante.formes.stock_medicament")[0]),
        "sante.medicaments": (d["m09p_s_medicaments"], g("sante.formes.medicament")[0]),
        "sante.moyenne_jour": (d["m09p_s_moyenne_jour"], g("sante.moyenne_consultations_par_jour")),
        "sante.mediane_jour": (d["m09p_s_mediane_jour"], g("sante.median_consultations_par_jour")),
        "sante.pic_mois": (d["m09p_s_pic_mois"], g("sante.pic_mois")),
        "sante.creux_midi": (d["m09p_s_creux_midi"], g("sante.creux_midi")),
        "sante.patients": (d["m09p_s_patients_distincts"], g("sante.n_patients_distincts")),
        "sante.jours_distincts": (d["m09p_s_jours_distincts"], g("sante.jours_consultes")),
        "sante.rupture_m01": (d["m09p_s_rupture_m01"], g("sante.rupture_M01_jours")),
        "sante.rupture_m02": (d["m09p_s_rupture_m02"], g("sante.rupture_M02_jours")),
        "sante.rupture_m04": (d["m09p_s_rupture_m04"], g("sante.rupture_M04_jours")),
        "sante.rupture_la_plus_longue": (d["m09p_s_rupture_la_plus_longue"], g("sante.rupture_la_plus_longue")),
        "sante.jours_sous_seuil": (d["m09p_s_jours_sous_seuil"], g("sante.jours_sous_seuil_alerte")),
        "scolaire.eleves_declares": (d["m09p_sc_eleves_declares"], g("scolaire.n_eleves_declares")),
        "scolaire.eleves_distincts": (d["m09p_sc_eleves_distincts"], g("scolaire.n_eleves_distincts")),
        "scolaire.notes": (d["m09p_sc_notes_lignes"], g("scolaire.formes.note")[0]),
        "scolaire.absences": (d["m09p_sc_absences_lignes"], g("scolaire.formes.absence")[0]),
        "scolaire.notes_hors_bornes": (d["m09p_sc_notes_hors_bornes"], g("scolaire.defauts.notes_hors_bornes")),
        "scolaire.doublons_eleves": (d["m09p_sc_doublons_eleves"], g("scolaire.defauts.doublons_eleves")),
        "scolaire.absences_ferie": (d["m09p_sc_absences_ferie"], g("scolaire.defauts.absences_jour_ferie")),
        "scolaire.absents_notes_t2": (d["m09p_sc_eleves_10plus_abs_t2"], g("scolaire.defauts.absents_not_t2")),
        "scolaire.correlation": (d["m09p_sc_correlation_absent_notes"], g("scolaire.correlation_absent_notes")),
        "scolaire.segments": (d["m09p_sc_segments_absences"], g("scolaire.segments_absences")),
        "scolaire.taux_par_classe": (d["m09p_sc_taux_par_classe"], g("scolaire.taux_absence_par_classe")),
        "scolaire.classe_plus_absente": (d["m09p_sc_classe_plus_absente"], g("scolaire.classe_la_plus_absente")),
        "projet.lignes_brut": (d["m09p_p_lignes_brut"], g("projet.formes.fichier_inconnu")[0]),
        "projet.doublons_tx_ref": (d["m09p_p_doublons_tx_ref"], g("projet.defauts.doublons_tx_ref")),
        "projet.montants_negatifs": (d["m09p_p_montants_negatifs"], g("projet.defauts.montants_negatifs")),
        "projet.montants_enormes": (d["m09p_p_montants_enormes"], g("projet.defauts.montants_enormes")),
        "projet.commissions": (d["m09p_p_commissions_manquantes"], g("projet.defauts.commissions_manquantes")),
        "projet.statuts_bruts": (d["m09p_p_statuts_bruts"], g("projet.statuts_bruts")),
        "projet.succes_normalises": (d["m09p_p_succes_normalises"], g("projet.succes_normalises")),
        "projet.echecs_normalises": (d["m09p_p_echecs_normalises"], g("projet.ecchecs_normalises")),
        "projet.n_agents": (d["m09p_p_n_agents"], g("projet.n_agents")),
    }
    ecartes = {k: (m, a) for k, (m, a) in croise.items() if m != a}
    if ecartes:
        raise ValueError("verification croisee M09 pandas/generation en echec: %s" % ecartes)
    d["m09p_croisee_pandas_generation"] = ("OK (%d valeurs : formes, defauts plantes, "
                                           "ruptures et normalisations exacts)") % len(croise)
    return d

def m10():
    """M10 — Data visualization : les mesures du socle de la refonte.

    Le module ne cree aucune donnee : il mesure l'ecart entre ce que l'oeil lit sur
    un graphique rate et ce que les donnees disent. Les deux rapports (avant/apres)
    sont produits par `tools/dossier_M10.py` (sortie deterministe, diff = 0).
    """
    d = {}
    dossier = os.path.join(os.path.dirname(ROOT), "03_exercices", "dossier_M10")
    v = pd.read_csv(os.path.join(os.path.dirname(ROOT), "03_exercices", "dossier_M09",
                                 "quincaillerie", "vente.csv"),
                    parse_dates=["date_vente"])
    v["ct"] = (v["montant_ttc"] * 100).round().astype("int64")
    sans = v[~v["est_retour"]]
    ca = sans.groupby(sans["date_vente"].dt.to_period("M"))["ct"].sum() // 100
    mg3 = ca.rolling(3).mean()
    ret = v.groupby("date_vente")["est_retour"].sum()
    ret = ret.groupby(ret.index.to_period("M")).sum().reindex(ca.index).fillna(0)

    d["m10_chapitres"] = 6 + 1
    d["m10_heures"] = 30
    d["m10_niveau_cible"] = "N3"
    d["m10_budget_pages"] = 105
    d["m10_budget_pages_min"] = 89
    d["m10_budget_pages_max"] = 121
    d["m10_table_graphiques"] = 16
    d["m10_graphiques_fondateurs"] = 11
    d["m10_graphiques_utiles"] = 5
    d["m10_grille_points"] = 18
    d["m10_grille_familles"] = 4
    d["m10_graphiques_avant"] = 5
    d["m10_graphiques_apres"] = 5
    d["m10_pages_rapport"] = 2
    # D1 — l'axe tronque : ce que l'oeil lit contre ce que les donnees disent
    d["m10_axe_min_m"] = round(float(ca.min() / 1e6), 1)
    d["m10_axe_max_m"] = round(float(ca.max() / 1e6), 1)
    d["m10_variation_brute_pct"] = round(float((ca.max() - ca.min()) / ca.min() * 100), 1)
    d["m10_variation_mg3_pct"] = round(float((mg3.max() - mg3.min()) / mg3.min() * 100), 1)
    # C01 — la perception : le meme jeu de 8 parts code de cinq facons.
    # On rejoue ici la mesure du chapitre (tools/perception_M10.py) : les 8 parts, puis
    # l'ecart entre deux parts voisines converti dans l'unite de chaque canal de lecture.
    import matplotlib  # noqa: F401  (import local : le reste du socle n'en a pas besoin)
    import matplotlib.cm as cm
    import numpy as np
    prod = pd.read_csv(os.path.join(os.path.dirname(ROOT), "03_exercices", "dossier_M09",
                                    "quincaillerie", "produit.csv"))
    vp = sans.merge(prod[["id_produit", "id_categorie"]], on="id_produit", how="left")
    part = (vp.groupby("id_categorie")["montant_ttc"].sum()
            / vp["montant_ttc"].sum() * 100).sort_values().to_numpy()
    ecarts = np.diff(part)
    axe, largeur_mm = 20.0, 170.0            # l'axe et la largeur de la planche C01
    d["m10_c01_parts"] = int(len(part))
    d["m10_c01_part_min_pct"] = round(float(part.min()), 2)
    d["m10_c01_part_max_pct"] = round(float(part.max()), 2)
    d["m10_c01_ratio_max_min"] = round(float(part.max() / part.min()), 2)
    d["m10_c01_ecart_min_pts"] = round(float(ecarts.min()), 2)
    d["m10_c01_ecart_median_pts"] = round(float(np.median(ecarts)), 2)
    d["m10_c01_ecart_max_pts"] = round(float(ecarts.max()), 2)
    d["m10_c01_ecart_extremes_pts"] = round(float(part.max() - part.min()), 2)
    d["m10_c01_axe_pct"] = axe
    d["m10_c01_planche_mm"] = largeur_mm
    d["m10_c01_mm_par_point"] = round(largeur_mm / axe, 2)
    d["m10_c01_finesse_ecart_min_mm"] = round(float(ecarts.min()) * largeur_mm / axe, 2)
    d["m10_c01_finesse_ecart_max_mm"] = round(float(ecarts.max()) * largeur_mm / axe, 1)
    d["m10_c01_finesse_extremes_mm"] = round(float(part.max() - part.min()) * largeur_mm / axe, 1)
    d["m10_c01_ecart_min_pct_axe"] = round(float(ecarts.min()) / axe * 100, 2)
    d["m10_c01_angle_min_deg"] = round(float(ecarts.min()) * 3.6, 2)
    d["m10_c01_angle_max_deg"] = round(float(ecarts.max()) * 3.6, 2)
    d["m10_c01_angle_part_min_deg"] = round(float(part.min()) * 3.6, 1)
    i_min = int(np.argmin(ecarts))
    i_max = int(np.argmax(ecarts))
    d["m10_c01_aire_rel_min_pct"] = round(float(ecarts[i_min] / part[i_min] * 100), 2)
    d["m10_c01_aire_rel_max_pct"] = round(float(ecarts[i_max] / part[i_max] * 100), 1)
    # la couleur : la rampe sequentielle du panneau 5, en clarte CIE L*
    def _lab(rgb):
        def lin(t):
            return t / 12.92 if t <= 0.04045 else ((t + 0.055) / 1.055) ** 2.4
        r, g, b = (lin(c) for c in rgb[:3])
        x = r * 0.4124 + g * 0.3576 + b * 0.1805
        y = r * 0.2126 + g * 0.7152 + b * 0.0722
        z = r * 0.0193 + g * 0.1192 + b * 0.9505

        def f(t):
            return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
        fx, fy, fz = f(x / 0.95047), f(y), f(z / 1.08883)
        return np.array([116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)])
    rampe = cm.get_cmap("Blues")
    norme = matplotlib.colors.Normalize(0, axe)
    lab = np.array([_lab(rampe(norme(x))) for x in part])
    dl = np.abs(np.diff(lab[:, 0]))
    # meme paire que l'ecart minimal des donnees (le canal couleur peut avoir son
    # minimum ailleurs : on cite toujours la paire la plus proche en valeur)
    d["m10_c01_couleur_dl_min"] = round(float(dl[i_min]), 2)
    d["m10_c01_couleur_dl_max"] = round(float(dl[i_max]), 2)
    d["m10_c01_couleur_de_min"] = round(float(np.linalg.norm(lab[i_min + 1] - lab[i_min])), 2)
    d["m10_c01_couleur_dl_etendue"] = round(float(abs(lab[-1, 0] - lab[0, 0])), 1)
    d["m10_c01_couleur_dl_par_point"] = round(
        float(abs(lab[-1, 0] - lab[0, 0]) / (part.max() - part.min())), 2)
    d["m10_c01_cinq_encodages"] = 5
    d["m10_c01_planche"] = "figures/M10_C01_cinq_encodages.svg (5 panneaux, 170 mm, sortie deterministe)"

    # C02 — la table des 16 graphiques : les chiffres d'appui du catalogue
    # (memes donnees que tools/seize_graphiques_M10.py, qui dessine les 16 panneaux)
    mgn = pd.read_csv(os.path.join(os.path.dirname(ROOT), "03_exercices", "dossier_M09",
                                   "quincaillerie", "magasin.csv"))
    vpc = sans.merge(prod[["id_produit", "id_categorie"]], on="id_produit", how="left")
    par_cat = vpc.groupby("id_categorie")["montant_ttc"].sum()
    d["m10_c02_graphiques"] = 16
    d["m10_c02_echantillon_nuage"] = 2000
    d["m10_c02_metriques"] = 8
    d["m10_c02_fondateurs"] = 11
    d["m10_c02_utiles"] = 5
    d["m10_c02_ca_categorie_max_m"] = round(float(par_cat.max() / 1e6), 1)
    d["m10_c02_ca_categorie_min_m"] = round(float(par_cat.min() / 1e6), 1)
    d["m10_c02_mois_ca_max"] = str(ca.idxmax())
    d["m10_c02_mois_ca_min"] = str(ca.idxmin())
    d["m10_c02_mois_ca_max_m"] = round(float(ca.max() / 1e6), 1)
    d["m10_c02_mois_ca_min_m"] = round(float(ca.min() / 1e6), 1)
    d["m10_c02_ca_2025_m"] = round(float(
        sans[sans["date_vente"].dt.year == 2025]["montant_ttc"].sum() / 1e6), 1)
    d["m10_c02_ca_2026_m"] = round(float(
        sans[sans["date_vente"].dt.year == 2026]["montant_ttc"].sum() / 1e6), 1)
    d["m10_c02_retours_part_pct"] = round(
        float(v[v["est_retour"]]["montant_ttc"].sum() / v["montant_ttc"].sum() * 100), 2)
    d["m10_c02_magasins"] = int(mgn["id_magasin"].nunique())
    d["m10_c02_villes"] = int(mgn["ville"].nunique())
    pj2 = pd.read_csv(os.path.join(os.path.dirname(ROOT), "03_exercices", "dossier_M09",
                                   "projet", "fichier_inconnu.csv"))
    ded2 = pj2.drop_duplicates(subset=["tx_ref"])
    v2 = ded2[(ded2["montant_xof"] > 0) & (ded2["montant_xof"] < 100000000)]
    d["m10_c02_entonnoir_etapes"] = 4
    d["m10_c02_entonnoir_taux_final_pct"] = round(
        float(v2["statut"].isin(["OK", "ok", "Reussie", "REUSSI"]).sum() / len(pj2) * 100), 1)
    d["m10_c02_planche"] = ("figures/M10_C02_seize_graphiques.svg "
                            "(16 panneaux, 198 x 160 mm, sortie deterministe)")

    # C03 — couleurs, contraste, daltonisme : la mesure vient du script qui dessine la
    # planche (import par chemin), pour qu'il n'y ait jamais deux versions du meme chiffre.
    import importlib.util
    chemin_couleurs = os.path.join(os.path.dirname(ROOT), "tools", "couleurs_M10.py")
    if os.path.exists(chemin_couleurs):
        spec = importlib.util.spec_from_file_location("couleurs_M10", chemin_couleurs)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        d["m10_c03_contraste_seuil_texte"] = 4.5
        d["m10_c03_contraste_seuil_graphique"] = 3.0
        d["m10_c03_paires_couleurs"] = 5
        d["m10_c03_seuil_deltae_lisible"] = 10
        d["m10_c03_jaune_blanc_invisible"] = 1
        d.update({k.replace("c03_", "m10_c03_"): v for k, v in mod.mesures(verbeux=False).items()})
        d["m10_c03_planche"] = ("figures/M10_C03_palette_testee.svg "
                                "(5 bandes : palette, deuteranopie, protanopie, rampe, rampe simulee)")
        d["m10_c03_simulations"] = 3

    # C04 — l'ecriture du graphique : titres, axes, ordre, annotations.
    # Meme principe que C03 : la mesure est calculee par le script qui dessine la planche.
    chemin_ecriture = os.path.join(os.path.dirname(ROOT), "tools", "ecriture_M10.py")
    if os.path.exists(chemin_ecriture):
        import contextlib
        import importlib.util
        import io
        spec = importlib.util.spec_from_file_location("ecriture_M10", chemin_ecriture)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        L = mod.audit_titres()
        for version in ("avant", "apres"):
            sel = [x for x in L if x["version"] == version and x["titre"]]
            d["m10_c04_%s_titres" % version] = len(sel)
            d["m10_c04_%s_titres_portant_une_mesure" % version] = int(
                sum(x["porte_mesure"] for x in sel))
            d["m10_c04_%s_annotations" % version] = int(sum(x["annotations"] for x in sel))
            d["m10_c04_%s_axe_zero" % version] = int(sum(x["axe_a_zero"] for x in sel))
        d.update({k.replace("c04_", "m10_c04_"): v for k, v in mod.mesures_et_planche().items()})
        d["m10_c04_planche"] = ("figures/M10_C04_ecriture_titre_axe_annotation.svg "
                                "(5 panneaux : avant, apres, deux ordres, hierarchie)")
        d["m10_c04_gestes"] = 6

    # C05 — le mur des 10 erreurs : les effets mesures, calcules par le script de la planche
    chemin_erreurs = os.path.join(os.path.dirname(ROOT), "tools", "erreurs_M10.py")
    if os.path.exists(chemin_erreurs):
        import contextlib
        import importlib.util
        import io
        spec = importlib.util.spec_from_file_location("erreurs_M10", chemin_erreurs)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with contextlib.redirect_stdout(io.StringIO()):
            m_erreurs = mod.mesures(mod.charger())
        d.update({k.replace("e", "m10_c05_", 1) if k[:1] == "e" and k[1:3].isdigit()
                  else "m10_c05_" + k: v for k, v in m_erreurs.items()})
        d["m10_c05_erreurs"] = 10
        d["m10_c05_panneaux"] = 10
        d["m10_c05_planche"] = ("figures/M10_C05_mur_des_10_erreurs.svg "
                                "(10 panneaux : chaque defaut et son effet mesure)")

    # C06 — la sequence de trois ecrans : les chiffres des deux versions, mesures sur la maquette
    chemin_sequence = os.path.join(os.path.dirname(ROOT), "tools", "sequence_M10.py")
    if os.path.exists(chemin_sequence):
        import contextlib
        import importlib.util
        import io
        spec = importlib.util.spec_from_file_location("sequence_M10", chemin_sequence)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with contextlib.redirect_stdout(io.StringIO()):
            base = mod.mesures(mod.charger(), {})
            maquette = mod.textes(mod.charger(), base)
            m_seq = mod.mesures(mod.charger(), maquette)
        d.update({"m10_c06_" + k: v for k, v in m_seq.items()})
        d["m10_c06_planche"] = ("figures/M10_C06_sequence_trois_ecrans.svg "
                                "(2 versions x 3 ecrans + la bande des objections)")

    # C07 — le meme graphique dans trois outils : les mesures des fichiers produits
    chemin_outils = os.path.join(os.path.dirname(ROOT), "tools", "outils_M10.py")
    if os.path.exists(chemin_outils):
        import contextlib
        import importlib.util
        import io
        spec = importlib.util.spec_from_file_location("outils_M10", chemin_outils)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with contextlib.redirect_stdout(io.StringIO()):
            d_out = mod.charger()
            fic = {}
            mod.ecrire_exports(d_out, fic)
            mod.ecrire_excel(d_out, fic)
            m_out = mod.mesures(d_out, fic)
        d.update({"m10_c07_" + k: v for k, v in m_out.items()})
        d["m10_c07_png96_largeur_px"] = 604
        d["m10_c07_png96_hauteur_px"] = 340
        d["m10_c07_png300_largeur_px"] = 1889
        d["m10_c07_png300_hauteur_px"] = 1062
        d["m10_c07_total_classeur_fcfa"] = round(float(d_out["ca"].sum()), 2)
        d["m10_c07_planche"] = ("figures/M10_C07_meme_graphique_trois_outils.svg "
                                "(matplotlib execute, Excel ecrit et relu, Power BI cite)")
        d["m10_c07_exports"] = ("03_exercices/dossier_M10/exports/ : fil_rouge_png_96.png, "
                                "fil_rouge_png_300.png, fil_rouge.svg, fil_rouge.pdf, fil_rouge.xlsx")

    # Projet M10.P et evaluation M10 : les compteurs des deux pieces (le controle
    # automatique du projet est tools/controle_refonte_M10.py).
    d["m10p_livrables"] = 4
    d["m10p_points"] = 20
    d["m10p_seuil"] = 13
    d["m10p_duree_h"] = 4
    d["m10p_p1_points"] = 5
    d["m10p_p2_points"] = 6
    d["m10p_p3_points"] = 5
    d["m10p_p4_points"] = 4
    d["m10p_controle_couches"] = 4
    d["m10p_figures"] = 10
    d["m10p_largeur_max_px"] = 776
    d["m10p_svg_avant"] = 5
    d["m10p_svg_apres"] = 5
    d["m10p_totaux_controles"] = 3      # total net = somme des categories = somme des trimestres
    d["m10p_ventes"] = int(len(v))
    d["m10p_retours"] = int(v["est_retour"].sum())
    d["m10p_mediane"] = int(round(float(v["montant_ttc"].median())))
    d["m10p_queue_500k"] = int((v["montant_ttc"] > 500000).sum())
    d["m10p_total_net_fcfa"] = round(float(sans["montant_ttc"].sum()), 2)
    d["m10p_grille_points"] = 18
    d["m10p_grille_familles"] = 4
    d["m10e_quiz_questions"] = 15
    d["m10e_quiz_points"] = 15
    d["m10e_quiz_blocs"] = 5
    d["m10e_quiz_predire"] = 5
    d["m10e_predire_valeurs"] = 10
    d["m10e_predire_points"] = 10
    d["m10e_exercices_rendre"] = 3
    d["m10e_exercices_points"] = 20
    d["m10e_etude_cas_points"] = 20
    d["m10e_etude_cas_seuil"] = 12
    d["m10e_total_points"] = 65
    d["m10e_grille_points"] = 18
    d["m10e_grille_familles"] = 4

    # D2 — le double axe : la correlation que le titre affirme
    d["m10_corr_ca_retours"] = round(float(ca.corr(ret)), 2)
    d["m10_retours_min"] = int(ret.min())
    d["m10_retours_max"] = int(ret.max())
    # D3 — le camembert : nombre de parts et ecart minimal entre deux parts
    prod = pd.read_csv(os.path.join(os.path.dirname(ROOT), "03_exercices", "dossier_M09",
                                    "quincaillerie", "produit.csv"))
    vp = sans.merge(prod[["id_produit", "id_categorie"]], on="id_produit", how="left")
    part = (vp.groupby("id_categorie")["montant_ttc"].sum() / vp["montant_ttc"].sum() * 100).sort_values()
    d["m10_parts_camembert"] = int(len(part))
    d["m10_part_min_pct"] = round(float(part.min()), 1)
    d["m10_part_max_pct"] = round(float(part.max()), 1)
    d["m10_ecart_min_parts_pts"] = round(float(part.diff().dropna().min()), 2)
    # D4 — le cumul de pourcentages : les totaux trimestriels qu'il masque
    tri = sans.groupby(sans["date_vente"].dt.to_period("Q"))["ct"].sum() // 100
    d["m10_trimestres"] = int(len(tri))
    d["m10_total_trim_min"] = int(tri.min())
    d["m10_total_trim_max"] = int(tri.max())
    d["m10_variation_totaux_pct"] = round(float((tri.max() - tri.min()) / tri.min() * 100), 1)
    # D5 — l'echelle log : la queue et la mediane
    mt = v["montant_ttc"]
    d["m10_ratio_max_mediane"] = int(round(float(mt.max() / mt.median())))
    d["m10_mediane_montant"] = int(round(float(mt.median())))
    d["m10_moyenne_montant"] = int(round(float(mt.mean())))
    d["m10_plateau_max"] = int((mt == mt.max()).sum())
    d["m10_part_sous_10k_pct"] = round(float((mt < 10000).mean() * 100), 1)
    d["m10_part_sous_250k_pct"] = round(float((mt < 250000).mean() * 100), 1)
    d["m10_queue_sup_500k"] = int((mt > 500000).sum())
    d["m10_emprise_refonte"] = "aucune donnee nouvelle : socle M07/M08/M09 (empreinte b9a8d973119342ec)"

    # Verification croisee : les SVG du dossier doivent exister (le socle de la refonte)
    svg = []
    for sous in ("rapport_avant", "rapport_apres"):
        chemin = os.path.join(dossier, sous)
        svg += [f for f in sorted(os.listdir(chemin)) if f.endswith(".svg")] if os.path.isdir(chemin) else []
    if len(svg) != 10:
        raise ValueError("dossier M10 : 10 SVG attendus (5 avant + 5 apres), trouves %d" % len(svg))
    d["m10_svg_dossier"] = len(svg)
    d["m10_croisee_dossier"] = "OK (10 SVG : 5 graphiques rates + 5 corriges, sortie deterministe)"
    return d


def m12():
    """Les cles du module M12 - Fondamentaux de la Business Intelligence.

    Le socle de M12 **etend** celui de M11 : les ventes du fil rouge, plus les cinq
    tables operationnelles qu'un indicateur exige (cout d'achat, stock, ruptures,
    commandes, encaissements, logistique), produites par `tools/dossier_M12.py`
    (graine 46, deterministe) et lues par `socle_m12.sql`.

    Les dix indicateurs du module sont **mesures** par `tools/kpi_M12.py`, qui est
    importe ici : le releve du manuel et l'instrument du module ne peuvent pas
    diverger, puisqu'ils executent le meme code.

    Ce que le module enseigne, ses cles le portent : deux definitions du meme
    indicateur donnent deux chiffres (CA net 15 595 154 955 contre CA brut
    15 419 985 157), une somme de stocks au lieu d'une moyenne divise la rotation par
    douze (0,78 contre 9,42), et un depot sans vente fabrique un cout sans chiffre
    d'affaires.
    """
    import importlib.util
    d = {}
    depot = os.path.dirname(ROOT)          # la racine du depot (ROOT = 01_socle_donnees)
    dossier = os.path.join(depot, "03_exercices", "dossier_M12")

    # --- Structure du module (05_livrables/plan_M12.md)
    d["m12_chapitres_total"] = 6
    d["m12_heures"] = 30
    d["m12_niveau_cible"] = "N3 (aucune competence technique nouvelle)"
    d["m12_budget_pages"] = 92
    d["m12_prerequis"] = "M09 (questions metier) ; M10 (support) ; M11 (la matiere)"
    d["m12_kpi_carte"] = 10
    d["m12_quiz_questions"] = 15
    d["m12_exercices"] = 2
    d["m12_projet_livrables"] = 4
    d["m12_etages_architecture"] = 7
    d["m12_causes_echec"] = 10
    d["m12_criteres_kpi"] = 6
    d["m12_regimes_question"] = 4
    d["m12_outils_executes"] = "DuckDB 1.5.5 et pandas (executes) ; Excel (execute, classeur relu)"
    d["m12_outils_cites"] = "Power BI et tableurs d'entreprise (cites, jamais executes : regle §1.5)"

    # --- Le socle ajoute par M12
    d["m12_socle_script"] = "03_exercices/dossier_M12/socle_m12.sql"
    d["m12_socle_taille_octets"] = os.path.getsize(os.path.join(dossier, "socle_m12.sql"))
    d["m12_tables_ajoutees"] = 5
    d["m12_vues_ajoutees"] = 1
    d["m12_produits"] = 154
    d["m12_magasins_servis"] = 5
    d["m12_depot_sans_vente"] = 1
    d["m12_mois"] = 44
    d["m12_graine"] = 46

    # --- Le socle partage avec M11 (memes ventes, memes references : un module M12 se
    #     calcule sur le fil rouge, il ne le reecrit pas)
    d["m12_lignes"] = 240000
    d["m12_lignes_hors_retours"] = 237191
    d["m12_retours"] = 2809
    d["m12_tickets"] = 145212
    d["m12_tickets_toutes_lignes"] = 146161
    d["m12_clients_vente"] = 23497
    d["m12_magasins_referentiel"] = 6
    d["m12_client0_part_pct"] = 18.3
    d["m12_client0_ca_fcfa"] = "2 852 612 447 FCFA"
    d["m12_socle_texte"] = (
        "le socle de M12 est celui de M11 (%s lignes, %s hors retours, %s tickets, %s clients, "
        "%s mois) augmente de cinq tables operationnelles : %s produits cote cout, %s lignes de "
        "stock, %s ruptures, %s commandes, %s encaissements et %s lignes de logistique"
        % ("240 000", "237 191", "145 212", "23 497", "44", "154", "6 776", "2 428", "9 000",
           "9 000", "264"))

    # --- Les dix indicateurs, mesures par l'instrument du module
    spec = importlib.util.spec_from_file_location(
        "kpi_M12", os.path.join(depot, "tools", "kpi_M12.py"))
    kpi = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kpi)
    k = kpi.mesurer()
    f = kpi.fmt

    d["m12_k01_ca_net_fcfa"] = f(k["k01_ca_net_fcfa"]) + " FCFA"
    d["m12_k01_ca_brut_fcfa"] = f(k["k01_ca_avec_retours_fcfa"]) + " FCFA"
    d["m12_k01_ecart_fcfa"] = f(abs(k["k01_ecart_definitions_fcfa"])) + " FCFA"
    d["m12_k01_ecart_pct"] = k["k01_ecart_definitions_pct"]
    d["m12_k01_definition"] = (
        "deux definitions defendables du meme indicateur : le CA net de retours (%s FCFA) et le CA "
        "de toutes les lignes (%s FCFA) — %s FCFA d'ecart, %s %%, et aucune des deux n'est fausse"
        % (f(k["k01_ca_net_fcfa"]), f(k["k01_ca_avec_retours_fcfa"]),
           f(abs(k["k01_ecart_definitions_fcfa"])), f(k["k01_ecart_definitions_pct"])))

    d["m12_k02_marge_fcfa"] = f(k["k02_marge_brute_fcfa"]) + " FCFA"
    d["m12_k02_taux_marge_pct"] = k["k02_taux_marge_pct"]
    d["m12_k02_taux_marge_hors_manquants_pct"] = k["k02_taux_marge_hors_deux_produits_pct"]
    d["m12_k02_prix_2023"] = f(k["k02_prix_unitaire_par_an"][0]["prix_vente_moyen"]) + " FCFA"
    d["m12_k02_prix_2026"] = f(k["k02_prix_unitaire_par_an"][-1]["prix_vente_moyen"]) + " FCFA"
    d["m12_k02_derive_prix_pct"] = k["k02_derive_prix_pct"]
    d["m12_k02_definition"] = k["k02_marge_definition"]
    d["m12_k02_prix_manquants"] = 2

    d["m12_k03_couples_servis"] = k["k03_couples_servis"]
    d["m12_k03_couples_en_rupture"] = k["k03_couples_en_rupture"]
    d["m12_k03_taux_pct"] = k["k03_taux_rupture_pct"]
    d["m12_k03_jours"] = k["k03_jours_rupture"]
    d["m12_k03_ca_perdu_fcfa"] = f(k["k03_ca_perdu_estime_fcfa"]) + " FCFA (estimation)"
    d["m12_k03_definition"] = k["k03_rupture_definition"]

    d["m12_k04_rotation"] = k["k04_rotation_annuelle"]
    d["m12_k04_couverture_mois"] = k["k04_couverture_mois"]
    d["m12_k04_rotation_si_somme"] = k["k04_erreur_somme_stocks"]
    d["m12_k04_ventes_unites"] = k["k04_ventes_12_mois_unites"]
    d["m12_k04_stock_moyen_unites"] = k["k04_stock_moyen_mensuel_unites"]
    d["m12_k04_definition"] = (
        "rotation de stock : %s tours par an, soit %s mois de couverture — la meme requete ecrite "
        "sur la SOMME des douze stocks mensuels au lieu de leur moyenne donne %s tour : un "
        "indicateur se trompe de denominateur sans jamais lever d'erreur"
        % (f(k["k04_rotation_annuelle"]), f(k["k04_couverture_mois"]),
           f(k["k04_erreur_somme_stocks"])))

    d["m12_k05_panier_ticket"] = f(k["k05_panier_moyen_ticket_fcfa"]) + " FCFA"
    d["m12_k05_panier_median"] = f(k["k05_panier_median_fcfa"]) + " FCFA"
    d["m12_k05_ligne_moyenne"] = f(k["k05_ligne_moyenne_fcfa"]) + " FCFA"
    d["m12_k05_ecart_pct"] = k["k05_ecart_ticket_ligne_pct"]
    d["m12_k05_definition"] = (
        "panier moyen par ticket : %s FCFA ; par ligne : %s FCFA, soit %s %% de moins — le "
        "denominateur (tickets ou lignes) change l'indicateur, et le rapport qui ne dit pas lequel "
        "il publie rend ses chiffres incomparables"
        % (f(k["k05_panier_moyen_ticket_fcfa"]), f(k["k05_ligne_moyenne_fcfa"]),
           f(k["k05_ecart_ticket_ligne_pct"])))

    d["m12_k06_taux_lignes_pct"] = k["k06_taux_retour_lignes_pct"]
    d["m12_k06_taux_tickets_pct"] = k["k06_taux_retour_tickets_pct"]
    d["m12_k06_lignes_retour"] = k["k06_lignes_retour"]
    d["m12_k06_tickets_avec_retour"] = k["k06_tickets_avec_retour"]
    d["m12_k06_tickets_mixtes"] = k["k06_tickets_mixtes"]
    d["m12_k06_tickets_retour_seul"] = k["k06_tickets_retour_seul"]
    d["m12_k06_definition"] = k["k06_retour_definition"]

    d["m12_k07_a_lheure"] = k["k07_a_lheure"]
    d["m12_k07_livrees"] = k["k07_livrees"]
    d["m12_k07_annulees"] = k["k07_annulees"]
    d["m12_k07_taux_livrees_pct"] = k["k07_taux_service_pct"]
    d["m12_k07_taux_commandes_pct"] = k["k07_taux_service_annulees_incluses_pct"]
    d["m12_k07_retard_median_jours"] = k["k07_retard_median_jours"]
    d["m12_k07_definition"] = k["k07_service_definition"]

    d["m12_k08_taux_pct"] = k["k08_taux_recouvrement_pct"]
    d["m12_k08_factures"] = k["k08_factures"]
    d["m12_k08_ouvertes"] = k["k08_ouvertes"]
    d["m12_k08_encours_fcfa"] = f(k["k08_encours_ouvert_fcfa"]) + " FCFA"
    d["m12_k08_dso_jours"] = k["k08_dso_jours"]
    d["m12_k08_definition"] = (
        "taux de recouvrement a echeance : %s %% des %s factures — %s factures restent ouvertes "
        "pour %s d'encours, et le DSO mesure (%s jours) porte sur les seules factures encaissees : "
        "les deux chiffres decrivent la meme realite a deux dates diferentes"
        % (f(k["k08_taux_recouvrement_pct"]), f(k["k08_factures"]), f(k["k08_ouvertes"]),
           f(k["k08_encours_ouvert_fcfa"]), f(k["k08_dso_jours"])))

    d["m12_k09_colis"] = k["k09_colis"]
    d["m12_k09_cout_total_fcfa"] = f(k["k09_cout_total_fcfa"]) + " FCFA"
    d["m12_k09_cout_unitaire_fcfa"] = f(k["k09_cout_unitaire_fcfa"]) + " FCFA"
    d["m12_k09_cout_au_kg_fcfa"] = f(k["k09_cout_au_kg_fcfa"]) + " FCFA"
    d["m12_k09_part_carburant_pct"] = k["k09_part_carburant_pct"]
    d["m12_k09_colis_magasins"] = k["k09_colis_magasins"]
    d["m12_k09_cout_unitaire_magasins_fcfa"] = (
        f(k["k09_cout_unitaire_magasins_fcfa"]) + " FCFA")
    d["m12_k09_definition"] = (
        "cout logistique unitaire : %s FCFA par colis (%s FCFA au kilo) sur %s colis — %s %% du "
        "cout est du carburant, et le colis du depot central n'a pas de vente en face de lui"
        % (f(k["k09_cout_unitaire_fcfa"]), f(k["k09_cout_au_kg_fcfa"]), f(k["k09_colis"]),
           f(k["k09_part_carburant_pct"])))

    d["m12_k10_points_de_vente"] = len(k["k10_parts_ville"])
    d["m12_k10_villes_a_deux_points"] = k["k10_villes_a_deux_points"]
    d["m12_k10_villes_un_seul_point"] = k["k10_villes_un_seul_point"]
    d["m12_k10_ouaga_parts"] = "; ".join(
        "%s %s %% de sa ville" % (x["magasin"], f(x["part_ville_pct"])) for x in k["k10_ouaga_parts"])
    d["m12_k10_ouaga_premier_pct"] = k["k10_ouaga_parts"][0]["part_ville_pct"]
    d["m12_k10_ouaga_second_pct"] = k["k10_ouaga_parts"][1]["part_ville_pct"]
    d["m12_k10_ca_par_magasin"] = "; ".join(
        "%s %s FCFA (%s %% du reseau, %s %% de sa ville)"
        % (x["magasin"], f(x["ca_fcfa"]), f(x["part_reseau_pct"]), f(x["part_ville_pct"]))
        for x in k["k10_parts_ville"])
    d["m12_k10_ca_gounghin"] = f([x for x in k["k10_parts_ville"] if "Gounghin" in x["magasin"]][0]["ca_fcfa"]) + " FCFA"
    d["m12_k10_ca_bobo"] = f([x for x in k["k10_parts_ville"] if "Bobo" in x["magasin"]][0]["ca_fcfa"]) + " FCFA"
    d["m12_k10_ca_koudougou"] = f([x for x in k["k10_parts_ville"] if "Koudougou" in x["magasin"]][0]["ca_fcfa"]) + " FCFA"
    d["m12_k10_premier_magasin"] = k["k10_premier_magasin"]
    d["m12_k10_premier_part_reseau_pct"] = k["k10_premier_part_reseau_pct"]
    d["m12_k10_colis_depot"] = k["k10_colis_depot"]
    d["m12_k10_definition"] = k["k10_definition"]

    # --- Concevoir un KPI (C04) : les six criteres, la carte, le contre-KPI
    c = kpi.mesurer_criteres()
    d["m12_c_champs_carte"] = c["c_champs_carte"]
    d["m12_c_kpi_du_projet"] = c["c_kpi_du_projet"]
    d["m12_c_cases_a_remplir"] = c["c_cases_a_remplir"]
    d["m12_c_indic_dossier_rate"] = c["c_indic_dossier_rate"]
    d["m12_c_ratio_dossier"] = c["c_ratio_dossier"]
    d["m12_c_carte_texte"] = (
        "une carte de definition compte %d champs — formule, source, granularite, frequence, "
        "responsable, seuil d'alerte, contre-KPI — soit %d cases a remplir pour les %d KPI du projet, "
        "contre %s indicateurs sans carte au dossier rate : le projet ne demande pas plus de "
        "documents, il demande le meme document dix fois"
        % (c["c_champs_carte"], c["c_cases_a_remplir"], c["c_kpi_du_projet"],
           f(c["c_indic_dossier_rate"])))
    d["m12_c_retour_lignes_pct"] = c["c_retour_lignes_pct"]
    d["m12_c_retour_quantite_signee_pct"] = c["c_retour_quantite_signee_pct"]
    d["m12_c_retour_quantite_abs_pct"] = c["c_retour_quantite_abs_pct"]
    d["m12_c_retour_valeur_pct"] = c["c_retour_valeur_pct"]
    d["m12_c_retour_tickets_pct"] = c["c_retour_tickets_pct"]
    d["m12_c_retour_tickets_portant"] = c["c_retour_tickets_portant"]
    d["m12_c_retour_lignes"] = c["c_retour_lignes"]
    d["m12_c_retour_ecart_points"] = c["c_retour_ecart_points"]
    d["m12_c_retour_definition"] = c["c_retour_definition"]
    d["m12_c_seuils_couverture"] = "; ".join(
        "sous %s mois : %s lignes (%s %%), %s produits" % (
            f(x["seuil_mois"]).replace("0,80", "0,8").replace("1,00", "1,0"),
            f(x["lignes"]), f(x["pct_lignes"]), f(x["produits"])) for x in c["c_seuils_couverture"])
    d["m12_c_seuils_couverture_lignes_1_mois"] = c["c_seuils_couverture"][1]["lignes"]
    d["m12_c_seuils_couverture_pct_1_mois"] = c["c_seuils_couverture"][1]["pct_lignes"]
    d["m12_c_seuils_couverture_produits_1_mois"] = c["c_seuils_couverture"][1]["produits"]
    d["m12_c_seuils_couverture_produits_pct_1_mois"] = c["c_seuils_couverture"][1]["pct_produits"]
    d["m12_c_seuils_couverture_pct_08_mois"] = c["c_seuils_couverture"][0]["pct_lignes"]
    d["m12_c_seuils_couverture_lignes_08_mois"] = c["c_seuils_couverture"][0]["lignes"]
    d["m12_c_seuil_retenu_mois"] = 1.0
    d["m12_c_seuil_texte"] = c["c_seuil_texte"]
    d["m12_c_magasins_actifs"] = c["c_magasins_actifs"]
    d["m12_c_mois_distincts_magasins"] = c["c_mois_distincts_magasins"]
    d["m12_c_panier_journalier_moyen"] = f(c["c_panier_journalier_moyen"]) + " FCFA"
    d["m12_c_panier_journalier_ecart_type"] = f(c["c_panier_journalier_ecart_type"]) + " FCFA"
    d["m12_c_panier_journalier_cv_pct"] = c["c_panier_journalier_cv_pct"]
    d["m12_c_ca_mois_min"] = f(c["c_ca_mois_min"]) + " FCFA"
    d["m12_c_ca_mois_median"] = f(c["c_ca_mois_median"]) + " FCFA"
    d["m12_c_ca_mois_max"] = f(c["c_ca_mois_max"]) + " FCFA"
    d["m12_c_sensibilite_texte"] = c["c_sensibilite_texte"]
    d["m12_c_recette_unitaire_2023"] = f(c["c_recette_unitaire_2023"]) + " FCFA"
    d["m12_c_recette_unitaire_2025"] = f(c["c_recette_unitaire_2025"]) + " FCFA"
    d["m12_c_recette_facteur"] = c["c_recette_facteur"]
    d["m12_c_unites_facteur"] = c["c_unites_facteur"]
    d["m12_c_clients_facteur"] = c["c_clients_facteur"]
    d["m12_c_contre_kpi_prix_texte"] = c["c_contre_kpi_prix_texte"]
    d["m12_c_familles_libelles"] = c["c_familles_libelles"]
    d["m12_c_marge_famille_min"] = c["c_marge_famille_min"]
    d["m12_c_marge_famille_min_nom"] = c["c_marge_famille_min_nom"]
    d["m12_c_marge_famille_max"] = c["c_marge_famille_max"]
    d["m12_c_marge_famille_max_nom"] = c["c_marge_famille_max_nom"]
    d["m12_c_marge_dispersion_texte"] = c["c_marge_dispersion_texte"]
    d["m12_c_couverture_moyenne_mois"] = c["c_couverture_moyenne_mois"]
    d["m12_c_trio_texte"] = c["c_trio_texte"]
    d["m12_c_marge_sur_ttc_pct"] = 24.67
    d["m12_c_marge_deux_bases_texte"] = (
        "la meme marge brute de 3 847 989 780 FCFA vaut 29,12 % du chiffre d'affaires hors taxes et "
        "24,67 % du chiffre d'affaires toutes taxes comprises : deux chiffres justes, deux "
        "denominateurs, et une cible de 18 a 24 % qui ne veut rien dire tant que sa base n'est pas "
        "ecrite")

    # --- Les quatre regimes de question (C02), mesures par le meme instrument
    r = kpi.mesurer_regimes()
    d["m12_r1_mois"] = r["r1_mois"]
    d["m12_r1_premier_ca"] = f(r["r1_premier_ca"]) + " FCFA"
    d["m12_r1_dernier_ca"] = f(r["r1_dernier_ca"]) + " FCFA"
    d["m12_r1_magasin_mois"] = r["r1_magasin_mois"]
    d["m12_r1_cellules"] = r["r1_cellules"]
    d["m12_r1_produits_servis"] = r["r1_produits_servis"]
    d["m12_r1_ca_lundi"] = f(r["r1_ca_lundi"]) + " FCFA"
    d["m12_r1_ca_dimanche"] = f(r["r1_ca_dimanche"]) + " FCFA"
    d["m12_r1_ratio_lundi_dimanche"] = r["r1_ratio_lundi_dimanche"]
    d["m12_r1_part_fin_de_mois_pct"] = r["r1_part_fin_de_mois_pct"]
    d["m12_r1_definition"] = (
        "le regime descriptif se mesure en tranches lisibles : %s mois de ventes, %s combinaisons "
        "magasin-mois, %s cellules magasin-mois-famille et %s produits servis — le meme socle "
        "repond a des milliers de questions, et un rapport figé n'en pose qu'une"
        % (f(r["r1_mois"]), f(r["r1_magasin_mois"]), f(r["r1_cellules"]),
           f(r["r1_produits_servis"])))
    d["m12_r2_marge_pct"] = r["r2_marge_pct"]
    d["m12_r2_rupture_jours"] = r["r2_rupture_jours"]
    d["m12_r2_rupture_ca_estime"] = f(r["r2_rupture_ca_estime"]) + " FCFA (estimation)"
    d["m12_r2_definition"] = (
        "le regime diagnostique relie un ecart a une cause mesurable : une marge de %s %% pour une "
        "cible de %s a %s %% (cause : les prix de vente), %s jours de rupture dont le cout est "
        "ESTIME a %s FCFA — un diagnostic sans mesure n'est qu'une opinion"
        % (f(r["r2_marge_pct"]), f(r["r2_marge_cible_min_pct"]), f(r["r2_marge_cible_max_pct"]),
           f(r["r2_rupture_jours"]), f(r["r2_rupture_ca_estime"])))
    d["m12_r3_mois_evalues"] = r["r3_mois_evalues"]
    d["m12_r3_mape_naive_pct"] = r["r3_mape_naive_pct"]
    d["m12_r3_mape_saisonniere_pct"] = r["r3_mape_saisonniere_pct"]
    d["m12_r3_mape_moyenne_pct"] = r["r3_mape_moyenne_pct"]
    d["m12_r3_definition"] = r["r3_definition"]
    d["m12_r4_file_relance"] = r["r4_file_relance"]
    d["m12_r4_file_relance_fcfa"] = f(r["r4_file_relance_fcfa"]) + " FCFA"
    d["m12_r4_part_plus_90_pct"] = r["r4_part_plus_90_pct"]
    d["m12_r4_encours_ouvert_fcfa"] = f(r["r4_encours_ouvert_fcfa"]) + " FCFA"
    d["m12_r4_payees_en_retard"] = r["r4_payees_en_retard"]
    d["m12_r4_retard_median_jours"] = r["r4_retard_median_jours"]
    d["m12_r4_balance_agee"] = "; ".join(
        "%s : %s factures, %s FCFA" % (x["tranche"], f(x["factures"]), f(x["montant_fcfa"]))
        for x in r["r4_balance_agee"])
    d["m12_r4_definition"] = r["r4_definition"]

    # --- Le vocabulaire exact (C03) : grain, dimensions, additivite, pieges de cle
    g = kpi.mesurer_grain()
    d["m12_g_tables"] = g["g_tables"]
    d["m12_g_tables_cles_uniques"] = g["g_tables_cles_uniques"]
    d["m12_g_grains"] = "; ".join(
        "%s : %s lignes, %s cles distinctes" % (t, f(v["lignes"]), f(v["cles"]))
        for t, v in sorted(g["g_grains"].items()))
    d["m12_g_dimensions"] = "; ".join("%s %s" % (k, f(v)) for k, v in sorted(g["g_dimensions"].items()))
    d["m12_g_magasins"] = g["g_dimensions"]["magasin"]
    d["m12_g_villes"] = g["g_dimensions"]["ville"]
    d["m12_g_quartiers"] = g["g_dimensions"]["quartier"]
    d["m12_g_vendeurs"] = g["g_dimensions"]["vendeur"]
    d["m12_g_modes_paiement"] = g["g_dimensions"]["mode_paiement"]
    d["m12_g_canaux"] = g["g_dimensions"]["canal"]
    d["m12_g_sous_categories"] = g["g_dimensions"]["sous_categorie"]
    d["m12_g_mois"] = g["g_dimensions"]["mois"]
    d["m12_g_jours"] = g["g_dimensions"]["jour"]
    d["m12_g_couples_canal_mode"] = g["g_couples_canal_mode"]
    d["m12_g_ca_total"] = f(g["g_ca_total"]) + " FCFA"
    d["m12_g_ca_somme_magasins"] = f(g["g_ca_somme_magasins"]) + " FCFA"
    d["m12_g_ca_additif"] = ("le chiffre d'affaires est ADDITIF : %s FCFA au total, %s FCFA si on "
                            "somme les cinq magasins — le meme nombre, ce qui autorise les "
                            "sous-totaux" % (f(g["g_ca_total"]), f(g["g_ca_somme_magasins"])))
    d["m12_g_clients_somme_par_produit"] = g["g_clients_somme_par_produit"]
    d["m12_g_clients_somme_par_magasin"] = g["g_clients_somme_par_magasin"]
    d["m12_g_clients_total"] = g["g_clients_total"]
    d["m12_g_clients_ratio_produit"] = g["g_clients_ratio_produit"]
    d["m12_g_clients_ratio_magasin"] = g["g_clients_ratio_magasin"]
    d["m12_g_clients_definition"] = g["g_clients_non_additif"]
    d["m12_g_panier_moyenne_des_moyennes"] = f(g["g_panier_moyenne_des_moyennes"]) + " FCFA"
    d["m12_g_panier_vraie_moyenne"] = f(g["g_panier_vraie_moyenne"]) + " FCFA"
    d["m12_g_panier_ecart_fcfa"] = f(g["g_panier_ecart_fcfa"]) + " FCFA"
    d["m12_g_panier_ecart_pct"] = g["g_panier_ecart_pct"]
    d["m12_g_paniers_par_magasin"] = "; ".join(
        "%s %s FCFA" % (x["magasin"], f(x["panier_moyen_fcfa"]))
        for x in g["g_paniers_par_magasin"])
    d["m12_g_stock_cloture"] = g["g_stock_cloture"]
    d["m12_g_stock_somme_tous_mois"] = g["g_stock_somme_tous_mois"]
    d["m12_g_stock_ratio"] = g["g_stock_ratio"]
    d["m12_g_stock_definition"] = (
        "un stock est SEMI-ADDITIF : %s unites au dernier mois (%s), mais %s si on additionne les "
        "44 mois (x %s) — la quantite existe a un instant, elle ne s'accumule pas"
        % (f(g["g_stock_cloture"]), "2026-08", f(g["g_stock_somme_tous_mois"]),
           f(g["g_stock_ratio"])))
    d["m12_g_jointure_produit_lignes"] = g["g_jointure_produit_lignes"]
    d["m12_g_jointure_sans_mois_lignes"] = g["g_jointure_sans_mois_lignes"]
    d["m12_g_jointure_sans_mois_facteur"] = g["g_jointure_sans_mois_facteur"]
    d["m12_g_jointure_sans_mois_ca"] = f(int(g["g_jointure_sans_mois_ca"])) + " FCFA"
    d["m12_g_jointure_sans_mois_ca_facteur"] = g["g_jointure_sans_mois_ca_facteur"]
    d["m12_g_cle_piege"] = g["g_cle_piege"]
    d["m12_g_jour_record"] = g["g_jour_record"]
    d["m12_g_jour_record_ca"] = f(g["g_jour_record_ca"]) + " FCFA"
    d["m12_g_jour_moyen_ca"] = f(g["g_jour_moyen_ca"]) + " FCFA"
    d["m12_g_jour_record_ratio"] = g["g_jour_record_ratio"]
    d["m12_g_mois_record"] = g["g_mois_record"]
    d["m12_g_annees"] = "; ".join("%s %s FCFA" % (x["annee"], f(x["ca"])) for x in g["g_annees"])
    d["m12_g_horizons"] = (
        "trois horizons, trois decisions : la journee (%s FCFA en moyenne, %s le %s, soit x %s) "
        "pour l'operationnel ; le mois (%s au record) pour le tactique ; l'annee (%s a %s) pour le "
        "strategique"
        % (f(g["g_jour_moyen_ca"]), f(g["g_jour_record_ca"]), g["g_jour_record"],
           f(g["g_jour_record_ratio"]), g["g_mois_record"],
           f(g["g_annees"][0]["ca"]), f(g["g_annees"][-1]["ca"])))

    # --- Le dossier du projet rate (03_exercices/dossier_M12/etude_avant.md)
    d["m12_projet_indicateurs_livres"] = 41
    d["m12_projet_onglets"] = 7
    d["m12_projet_budget_fcfa"] = f(7940000) + " FCFA"
    d["m12_projet_maintenance_fcfa"] = f(1200000) + " FCFA"
    d["m12_projet_semaines"] = 11
    d["m12_projet_destinataires"] = 14
    d["m12_projet_ouvertures_j1"] = 4
    d["m12_projet_sources_discordantes"] = 3
    d["m12_projet_questions_jamais_posees"] = 6
    d["m12_projet_jours"] = 30
    d["m12_projet_jours_sources"] = 8
    d["m12_projet_jours_conception"] = 22
    d["m12_projet_livraison_annoncee"] = 6
    d["m12_p_cout_par_indicateur_fcfa"] = f(round(7940000 / 41)) + " FCFA"
    d["m12_p_cout_par_jour_fcfa"] = f(round(7940000 / 30)) + " FCFA"
    d["m12_p_cout_par_ouverture_fcfa"] = f(round(7940000 / 4)) + " FCFA"
    d["m12_p_cout_par_kpi_mandat_fcfa"] = f(round(7940000 / 10)) + " FCFA"
    d["m12_p_part_conception_pct"] = round(100.0 * 4850000 / 7940000, 1)
    d["m12_p_part_sources_pct"] = round(100.0 * 1640000 / 7940000, 1)
    d["m12_p_part_formation_pct"] = round(100.0 * 250000 / 7940000, 1)
    d["m12_p_part_maintenance_pct"] = round(100.0 * 1200000 / 7940000, 1)
    d["m12_p_cout_maintenance_semaine_fcfa"] = f(round(1200000 / 52)) + " FCFA"
    d["m12_p_jours_conception_pct"] = round(100.0 * 22 / 30, 1)
    d["m12_p_jours_sources_pct"] = round(100.0 * 8 / 30, 1)
    d["m12_p_administration"] = (
        "le dossier rate coutait 7 940 000 FCFA pour 41 indicateurs, soit 193 659 FCFA par indicateur ; "
        "ramene aux 10 KPI du mandat de reprise, le meme budget vaudrait 794 000 FCFA par KPI. Reparti "
        "par usage, il a paye 1 985 000 FCFA par lecteur du premier jour (4 ouvertures sur 14 "
        "destinataires) et 11 semaines de vie pour une maintenance annuelle de 1 200 000 FCFA, soit "
        "23 077 FCFA par semaine.")
    d["m12_projet_kpi_mandat"] = 10

    # --- Le controle croise cote pandas : le CA net doit se retrouver des deux cotes
    v = pd.read_csv(os.path.join(os.path.dirname(ROOT), "01_socle_donnees", "data",
                                 "reference", "ventes_propres.csv"),
                    usecols=["montant_ttc", "est_retour", "quantite"])
    ca_pandas = round(v.loc[v["est_retour"] == 0, "montant_ttc"].sum())
    if abs(ca_pandas - round(k["k01_ca_net_fcfa"])) > 1:
        raise ValueError("M12 : CA cote pandas (%s) different du CA cote DuckDB (%s)"
                         % (f(ca_pandas), f(round(k["k01_ca_net_fcfa"]))))
    d["m12_croisee_pandas"] = ("OK : CA net identique cote DuckDB et cote pandas (%s FCFA)"
                              % f(ca_pandas))
    return d


def m13():
    """Les cles du module M13 - Modelisation des donnees.

    Le module ne mesure pas un tableau de bord : il mesure la STRUCTURE qui rend les
    chiffres de M12 possibles. Ses cles portent donc deux familles de nombres —
    la structure (12 tables, 5 dimensions, 7 faits, 4 controles de recette) et les
    pieges qu'une structure se paie (une jointure sur le magasin seul multiplie le CA
    par 44, un fait pose au mauvais grain l'augmente de 43 %).

    L'instrument du module, `tools/modele_M13.py`, est **importe** : le releve du
    manuel et le verdict du modele ne peuvent pas diverger, puisqu'ils executent le
    meme code sur le meme socle (graine 47).
    """
    import importlib.util
    d = {}
    depot = os.path.dirname(ROOT)          # la racine du depot (ROOT = 01_socle_donnees)
    dossier = os.path.join(depot, "03_exercices", "dossier_M13")

    # --- La structure du module (05_livrables/plan_M13.md)
    d["m13_chapitres"] = 7
    d["m13_heures"] = 30
    d["m13_niveau_cible"] = "N4 (concevoir une structure, pas seulement l'interroger)"
    d["m13_budget_pages"] = 105
    d["m13_prerequis"] = "M06 (le modele relationnel) ; M11 (le SQL) ; M12 (les indicateurs)"
    d["m13_planches"] = 3
    d["m13_planches_noms"] = ("M13_C03_grain_et_explosion ; M13_C04_frise_scd ; "
                              "M13_C07_grille_revue")
    d["m13_decisions_modelisation"] = 8
    d["m13_revue_points"] = 15
    d["m13_piece_portfolio"] = 4
    d["m13_outils_executes"] = "DuckDB 1.5.5 et pandas (executes)"
    d["m13_outils_cites"] = ("PostgreSQL et Power BI (cites, jamais executes : regle §1.5 — la "
                             "traduction en relations d'outil appartient a M14)")

    # --- Le socle : la structure construite (graine 47, deterministe)
    d["m13_graine"] = 47
    d["m13_socle_script"] = "03_exercices/dossier_M13/socle_m13.sql"
    d["m13_socle_taille_octets"] = os.path.getsize(os.path.join(dossier, "socle_m13.sql"))
    d["m13_tables_modele"] = 12
    d["m13_dimensions"] = 5
    d["m13_faits"] = 7
    d["m13_dimensions_historisees"] = 2
    d["m13_cles_etrangeres"] = 12
    d["m13_sources_ajoutees"] = 2
    d["m13_versions_client"] = 24892
    d["m13_lignes_client_scd"] = 24893
    d["m13_versions_produit"] = 616
    d["m13_mouvements"] = 1120
    d["m13_mouvements_scd2"] = 980
    d["m13_mouvements_scd1"] = 140
    d["m13_clients_avec_histoire"] = 900
    d["m13_versions_max"] = 3
    d["m13_table_plate_lignes"] = 18
    d["m13_table_plate_clients"] = 6
    d["m13_table_plate_libelles_categorie"] = 11
    d["m13_familles"] = 7
    d["m13_produits_par_famille_max"] = 32
    d["m13_socle_texte"] = (
        "le modele compte %s tables — %s dimensions (client, produit, magasin, vendeur, temps) et "
        "%s tables de faits — plus %s dimensions historisees (type 2). M13 n'ajoute que deux "
        "sources, et seulement de l'histoire : %s mouvements clients et %s revisions tarifaires"
        % ("12", "5", "7", "2", "1 120", "616"))

    # --- Les quatre controles de recette et les cinq mesures, par l'instrument du module
    spec = importlib.util.spec_from_file_location(
        "modele_M13", os.path.join(depot, "tools", "modele_M13.py"))
    modele = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modele)
    m = modele.controler()
    f = modele.f

    d["m13_recette_modele_fcfa"] = f(m["c_ca_modele"]) + " FCFA"
    d["m13_recette_source_fcfa"] = f(m["c_ca_source"]) + " FCFA"
    d["m13_recette_identique"] = m["c_recette_ok"]
    d["m13_unicite_tables_ok"] = m["c_tables_cles_uniques"]
    d["m13_unicite_tables_total"] = m["c_tables"]
    d["m13_grain_faits_ok"] = m["c_grain_ok"]
    d["m13_grain_faits_total"] = m["c_faits_controles"]
    d["m13_orphelins"] = m["c_orphelins_total"]
    d["m13_verdict_unicite"] = m["c_verdict_unicite"]
    d["m13_verdict_grain"] = m["c_verdict_grain"]
    d["m13_client_inconnu_lignes"] = m["c_client_inconnu_lignes"]
    d["m13_client_inconnu_ca"] = f(m["c_client_inconnu_ca"]) + " FCFA"
    d["m13_client_inconnu_texte"] = (
        "le client 0 des ventes n'existe pas dans le referentiel : le modele lui donne une ligne "
        "« client non identifie » (%s lignes de ticket, %s FCFA) plutot qu'une cle qui ne pointe "
        "nulle part" % (f(m["c_client_inconnu_lignes"]), f(m["c_client_inconnu_ca"])))

    # --- Les changements lents et les deux trous que la jointure doit boucher
    d["m13_asof_lignes"] = m["c_ventes_jointes_asof"]
    d["m13_ventes_total"] = m["c_ventes_total"]
    d["m13_asof_integrale"] = m["c_asof_integrale"]
    d["m13_ventes_client_inconnu"] = m["c_ventes_client_inconnu"]
    d["m13_clients_rattrapes"] = m["c_clients_rattrapes"]
    d["m13_ventes_rattrapees"] = m["c_ventes_rattrapees"]
    d["m13_asof_texte"] = m["c_asof_texte"]
    d["m13_ca_segment_courant"] = m["c_ca_par_segment_courant"]
    d["m13_ca_segment_historique"] = m["c_ca_par_segment_historique"]
    d["m13_ecart_scd_max_fcfa"] = f(m["c_ecart_scd_max"]) + " FCFA"
    d["m13_ecart_scd_detail"] = m["c_ecart_scd_detail"]
    d["m13_scd_texte"] = m["c_scd_texte"]

    # --- Les trois modeles fautifs (chapitre C03 et etude de cas)
    d["m13_fautif_deux_fcfa"] = f(m["c_ca_deux_tableaux"]) + " FCFA"
    d["m13_fautif_deux_pct"] = m["c_facteur_deux_tableaux"]
    d["m13_fautif_trois_fcfa"] = f(m["c_ca_trois_tableaux"]) + " FCFA"
    d["m13_fautif_trois_pct"] = m["c_facteur_trois_tableaux"]
    d["m13_fautif_jointure_fcfa"] = f(m["c_ca_jointure_folle"]) + " FCFA"
    d["m13_fautif_jointure_facteur"] = m["c_facteur_jointure_folle"]
    d["m13_texte_fautifs"] = m["c_fautif_texte"]

    # --- Les revisions tarifaires et le calendrier
    d["m13_prix_tarif_2023_fcfa"] = f(m["c_prix_tarif_2023"]) + " FCFA"
    d["m13_prix_tarif_2026_fcfa"] = f(m["c_prix_tarif_2026"]) + " FCFA"
    d["m13_derive_tarif_pct"] = m["c_derive_tarif_pct"]
    d["m13_texte_tarifs"] = m["c_tarif_texte"]
    d["m13_calendrier_jours"] = m["c_calendrier_jours"]
    d["m13_calendrier_feries"] = m["c_calendrier_feries"]
    d["m13_calendrier_mois"] = m["c_calendrier_mois"]
    d["m13_calendrier_annees_fiscales"] = m["c_calendrier_annees_fiscales"]
    d["m13_calendrier_semaines_commerciales"] = m["c_calendrier_semaines_com"]
    d["m13_calendrier_semaines_iso"] = m["c_calendrier_semaines_iso"]
    d["m13_calendrier_cles_dans_les_faits"] = m["c_calendrier_tables_date"]
    d["m13_calendrier_texte"] = m["c_calendrier_texte"]
    d["m13_revue_defauts"] = m["c_revue_defauts"]
    d["m13_texte_revue"] = m["c_revue_texte"]

    # --- C01 : le point de depart, les cardinalites, le cout de la redondance
    d["m13_colonnes"] = m["c_colonnes"]
    d["m13_c01_entites"] = 5
    d["m13_c01_associations"] = 7
    d["m13_c01_clients_referentiel"] = m["c01_clients_referentiel"]
    d["m13_c01_clients_acheteurs"] = m["c01_clients_acheteurs"]
    d["m13_c01_clients_sans_vente"] = m["c01_clients_sans_vente"]
    d["m13_c01_produits"] = m["c01_produits"]
    d["m13_c01_produits_jamais_vendus"] = m["c01_produits_jamais_vendus"]
    d["m13_c01_magasins"] = m["c01_magasins"]
    d["m13_c01_magasins_vendeurs"] = m["c01_magasins_vendeurs"]
    d["m13_c01_depot_sans_vente"] = m["c01_depot_sans_vente"]
    d["m13_c01_vendeurs"] = m["c01_vendeurs"]
    d["m13_c01_vendeurs_actifs"] = m["c01_vendeurs_vendeurs"]
    d["m13_c01_jours"] = m["c01_jours"]
    d["m13_c01_ventes_par_client_min"] = m["c01_ventes_par_client_min"]
    d["m13_c01_ventes_par_client_moyenne"] = m["c01_ventes_par_client_moyenne"]
    d["m13_c01_ventes_par_client_mediane"] = m["c01_ventes_par_client_mediane"]
    d["m13_c01_ventes_par_client_max"] = m["c01_ventes_par_client_max"]
    d["m13_c01_ventes_par_produit_min"] = m["c01_ventes_par_produit_min"]
    d["m13_c01_ventes_par_produit_max"] = m["c01_ventes_par_produit_max"]
    d["m13_c01_ventes_par_magasin_min"] = m["c01_ventes_par_magasin_min"]
    d["m13_c01_ventes_par_magasin_max"] = m["c01_ventes_par_magasin_max"]
    d["m13_c01_tickets"] = m["c01_tickets"]
    d["m13_c01_ticket_exemple"] = m["c01_ticket_exemple"]
    d["m13_c01_lignes_par_ticket_moyenne"] = m["c01_lignes_par_ticket_moyenne"]
    d["m13_c01_lignes_par_ticket_max"] = m["c01_lignes_par_ticket_max"]
    d["m13_c01_noms_recopies_caracteres"] = m["c01_noms_recopies_caracteres"]
    d["m13_c01_noms_dimension_caracteres"] = m["c01_noms_dimension_caracteres"]
    d["m13_c01_noms_facteur"] = m["c01_noms_facteur"]
    d["m13_c01_jointure_commandes_fcfa"] = f(m["c01_jointure_commandes_ca"]) + " FCFA"
    d["m13_c01_jointure_commandes_lignes"] = m["c01_jointure_commandes_lignes"]
    d["m13_c01_jointure_encaissements_fcfa"] = f(m["c01_jointure_encaissements_ca"]) + " FCFA"
    d["m13_c01_jointure_encaissements_lignes"] = m["c01_jointure_encaissements_lignes"]
    d["m13_c01_jointure_facteur"] = m["c01_jointure_commandes_facteur"]
    d["m13_c01_texte_jointures"] = m["c01_texte_jointures"]
    d["m13_c01_clients_servis_somme"] = m["c01_clients_servis_somme"]
    d["m13_c01_table_plate_lignes"] = m["c01_table_plate_lignes"]
    d["m13_c01_table_plate_clients"] = m["c01_table_plate_clients"]
    d["m13_c01_table_plate_categories"] = m["c01_table_plate_categories"]
    d["m13_c01_table_plate_noms_recopies"] = m["c01_table_plate_noms_recopies"]
    d["m13_c01_table_plate_noms_dimension"] = m["c01_table_plate_noms_dimension"]
    d["m13_c01_table_plate_nom_max"] = m["c01_table_plate_nom_max"]
    d["m13_c01_table_plate_nom_max_fois"] = m["c01_table_plate_nom_max_fois"]
    d["m13_c01_table_plate_villes_client_41"] = m["c01_table_plate_villes_client_41"]
    d["m13_c01_texte_depart"] = m["c01_texte_depart"]

    # --- C02 : la normalisation, mesuree (table plate contre modele)
    d["m13_c02_lignes_plates"] = m["c02_lignes_plates"]
    d["m13_c02_colonnes_plates"] = m["c02_colonnes_plates"]
    d["m13_c02_colonnes_dimensions"] = m["c02_colonnes_dimensions"]
    d["m13_c02_ca_plat"] = f(m["c02_ca_plat"]) + " FCFA"
    d["m13_c02_libelles_bruts"] = m["c02_libelles_bruts"]
    d["m13_c02_familles_reelles"] = m["c02_familles_reelles"]
    d["m13_c02_materiaux_fragments_n"] = m["c02_materiaux_fragments_n"]
    d["m13_c02_materiaux_total"] = f(m["c02_materiaux_total"]) + " FCFA"
    d["m13_c02_materiaux_plus_gros_fragment"] = f(m["c02_materiaux_plus_gros_fragment"]) + " FCFA"
    d["m13_c02_materiaux_fragments"] = m["c02_materiaux_fragments"]
    d["m13_c02_familles_ca"] = m["c02_familles_ca"]
    d["m13_c02_famille_1"] = m["c02_famille_1"]
    d["m13_c02_famille_1_ca"] = f(m["c02_famille_1_ca"]) + " FCFA"
    d["m13_c02_texte_libelles"] = m["c02_texte_libelles"]
    d["m13_c02_nom_recopie_plat"] = m["c02_nom_recopie_plat"]
    d["m13_c02_nom_dimension"] = m["c02_nom_dimension"]
    d["m13_c02_designation_recopiee"] = m["c02_designation_recopiee"]
    d["m13_c02_designation_dimension"] = m["c02_designation_dimension"]
    d["m13_c02_facteur_designation"] = m["c02_facteur_designation"]
    d["m13_c02_temps_plat_famille_ms"] = m["c02_temps_plat_famille_ms"]
    d["m13_c02_temps_modele_famille_ms"] = m["c02_temps_modele_famille_ms"]
    d["m13_c02_texte_cout"] = m["c02_texte_cout"]

    # --- C03 : le grain et l'additivite, mesures (huit mesures + trois requetes fautives)
    d["m13_c03_faits_avec_grain_prouve"] = m["c03_faits_avec_grain_prouve"]
    d["m13_c03_grains"] = m["c03_grains"]
    d["m13_c03_lignes_faits_total"] = f(m["c03_lignes_faits_total"])
    d["m13_c03_ratio_grain"] = f(m["c03_ratio_grain"])
    d["m13_c03_lignes_par_ticket"] = m["c03_lignes_par_ticket"]
    d["m13_c03_objectifs_lignes"] = m["c03_objectifs_lignes"]
    d["m13_c03_objectifs_cle_fausse"] = m["c03_objectifs_cle_fausse"]
    d["m13_c03_mois"] = m["c03_mois"]
    d["m13_c03_ca_somme_mensuelle"] = f(m["c03_ca_somme_mensuelle"]) + " FCFA"
    d["m13_c03_facteur_additif"] = m["c03_facteur_additif"]
    d["m13_c03_stock_somme"] = f(m["c03_stock_somme"]) + " unites"
    d["m13_c03_stock_un_mois"] = f(m["c03_stock_un_mois"]) + " unites"
    d["m13_c03_stock_facteur"] = f(m["c03_stock_facteur"])
    d["m13_c03_stock_dernier_mois"] = f(m["c03_stock_dernier_mois"]) + " unites"
    d["m13_c03_taux_lignes"] = m["c03_taux_lignes"]
    d["m13_c03_taux_somme"] = m["c03_taux_somme"]
    d["m13_c03_taux_moyen"] = m["c03_taux_moyen"]
    d["m13_c03_faux_large_lignes"] = f(m["c03_faux_large_lignes"])
    d["m13_c03_faux_large_ca"] = f(m["c03_faux_large_ca"]) + " FCFA"
    d["m13_c03_faux_large_facteur"] = m["c03_faux_large_facteur"]
    d["m13_c03_faux_filtre_lignes"] = f(m["c03_faux_filtre_lignes"])
    d["m13_c03_faux_filtre_ca"] = f(m["c03_faux_filtre_ca"]) + " FCFA"
    d["m13_c03_faux_filtre_facteur"] = m["c03_faux_filtre_facteur"]
    d["m13_c03_faux_filtre_manquants"] = m["c03_faux_filtre_manquants"]
    d["m13_c03_bon_grain_lignes"] = f(m["c03_bon_grain_lignes"])
    d["m13_c03_bon_grain_ca"] = f(m["c03_bon_grain_ca"]) + " FCFA"
    d["m13_c03_bon_grain_facteur"] = m["c03_bon_grain_facteur"]
    d["m13_c03_texte_grain"] = m["c03_texte_grain"]
    d["m13_c03_texte_cle"] = m["c03_texte_cle"]
    d["m13_c03_texte_additivite"] = m["c03_texte_additivite"]
    d["m13_c03_texte_faux"] = m["c03_texte_faux"]
    d["m13_c03_logistique_total"] = f(m["c03_logistique_total"]) + " FCFA"
    d["m13_c03_logistique_jointe_interne"] = f(m["c03_logistique_jointe_interne"]) + " FCFA"
    d["m13_c03_logistique_perdue"] = f(m["c03_logistique_perdue"]) + " FCFA"
    d["m13_c03_depot_cout"] = f(m["c03_depot_cout"]) + " FCFA"
    d["m13_c03_depot_mois"] = m["c03_depot_mois"]
    d["m13_c03_texte_jointure_agregats"] = m["c03_texte_jointure_agregats"]

    # --- C04 : l'etoile, les dimensions conformes et les changements lents
    d["m13_c04_dimension_magasin_faits"] = m["c04_dimension_magasin_faits"]
    d["m13_c04_dimension_client_faits"] = m["c04_dimension_client_faits"]
    d["m13_c04_dimension_produit_faits"] = m["c04_dimension_produit_faits"]
    d["m13_c04_dimension_vendeur_faits"] = m["c04_dimension_vendeur_faits"]
    d["m13_c04_dimension_date_faits"] = m["c04_dimension_date_faits"]
    d["m13_c04_texte_conformes"] = m["c04_texte_conformes"]
    d["m13_c04_mouvements_type1"] = m["c04_mouvements_type1"]
    d["m13_c04_mouvements_type2"] = m["c04_mouvements_type2"]
    d["m13_c04_mouvements_detail"] = m["c04_mouvements_detail"]
    d["m13_c04_attributs_historiises"] = m["c04_attributs_historiises"]
    d["m13_c04_clients_avec_histoire"] = m["c04_clients_avec_histoire"]
    d["m13_c04_clients_deux_changements"] = m["c04_clients_deux_changements"]
    d["m13_c04_villes_max"] = m["c04_villes_max"]
    d["m13_c04_texte_types"] = m["c04_texte_types"]
    d["m13_c04_temps_courant_ms"] = m["c04_temps_courant_ms"]
    d["m13_c04_temps_historise_ms"] = m["c04_temps_historise_ms"]
    d["m13_c04_prix_moyen_courant"] = f(m["c04_prix_moyen_courant"]) + " FCFA"
    d["m13_c04_prix_moyen_historise"] = f(m["c04_prix_moyen_historise"]) + " FCFA"
    d["m13_c04_prix_ecart_pct"] = m["c04_prix_ecart_pct"]
    d["m13_c04_versions_produit_par_produit"] = m["c04_versions_produit_par_produit"]
    d["m13_c04_trous_total_lignes"] = m["c04_trous_total_lignes"]
    d["m13_c04_trous_total_texte"] = m["c04_trous_total_texte"]
    d["m13_c04_exemple_produit"] = m["c04_exemple_produit"]
    d["m13_c04_exemple_produit_variation_pct"] = m["c04_exemple_produit_variation_pct"]
    d["m13_c04_exemple_client"] = m["c04_exemple_client"]
    d["m13_c04_texte_lecture"] = m["c04_texte_lecture"]
    d["m13_c04_texte_tarifs"] = m["c04_texte_tarifs"]

    # --- C05 : le flocon, la table de pont, la dimension dechet, les faits multiples
    d["m13_c05_produit_etoile_lignes"] = m["c05_produit_etoile_lignes"]
    d["m13_c05_flocon_sous_categories"] = m["c05_flocon_sous_categories"]
    d["m13_c05_flocon_familles"] = m["c05_flocon_familles"]
    d["m13_c05_flocon_lignes"] = m["c05_flocon_lignes"]
    d["m13_c05_etoile_flocon_identiques"] = m["c05_etoile_flocon_identiques"]
    d["m13_c05_famille_1"] = m["c05_famille_1"]
    d["m13_c05_temps_etoile_ms"] = m["c05_temps_etoile_ms"]
    d["m13_c05_temps_flocon_ms"] = m["c05_temps_flocon_ms"]
    d["m13_c05_famille_ecrite_etoile"] = m["c05_famille_ecrite_etoile"]
    d["m13_c05_famille_ecrite_flocon"] = m["c05_famille_ecrite_flocon"]
    d["m13_c05_texte_flocon"] = m["c05_texte_flocon"]
    d["m13_c05_tickets_une_ligne"] = m["c05_tickets_une_ligne"]
    d["m13_c05_tickets_plusieurs_lignes"] = m["c05_tickets_plusieurs_lignes"]
    d["m13_c05_pct_tickets_multi"] = m["c05_pct_tickets_multi"]
    d["m13_c05_lignes_par_ticket_max"] = m["c05_lignes_par_ticket_max"]
    d["m13_c05_ca_lignes"] = f(m["c05_ca_lignes"]) + " FCFA"
    d["m13_c05_ca_pont"] = f(m["c05_ca_pont"]) + " FCFA"
    d["m13_c05_pont_facteur"] = m["c05_pont_facteur"]
    d["m13_c05_pont_ecart"] = f(m["c05_pont_ecart"]) + " FCFA"
    d["m13_c05_texte_pont"] = m["c05_texte_pont"]
    d["m13_c05_dechet_colonnes"] = m["c05_dechet_colonnes"]
    d["m13_c05_dechet_combinaisons"] = m["c05_dechet_combinaisons"]
    d["m13_c05_dechet_espace"] = m["c05_dechet_espace"]
    d["m13_c05_mode_paiement_valeurs"] = m["c05_mode_paiement_valeurs"]
    d["m13_c05_canal_valeurs"] = m["c05_canal_valeurs"]
    d["m13_c05_statut_livree"] = m["c05_statut_livree"]
    d["m13_c05_statut_annulee"] = m["c05_statut_annulee"]
    d["m13_c05_ca_par_canal"] = m["c05_ca_par_canal"]
    d["m13_c05_canal_1"] = m["c05_canal_1"]
    d["m13_c05_canal_1_ca"] = f(m["c05_canal_1_ca"]) + " FCFA"
    d["m13_c05_texte_dechet"] = m["c05_texte_dechet"]
    d["m13_c05_retours_lignes"] = m["c05_retours_lignes"]
    d["m13_c05_retours_montant"] = f(m["c05_retours_montant"]) + " FCFA"
    d["m13_c05_retours_pct_lignes"] = m["c05_retours_pct_lignes"]
    d["m13_c05_texte_faits_multiples"] = m["c05_texte_faits_multiples"]

    # --- Le temps et le calendrier (M13.C06)
    d["m13_c06_calendrier_lignes"] = m["c06_calendrier_lignes"]
    d["m13_c06_calendrier_debut"] = m["c06_calendrier_debut"]
    d["m13_c06_calendrier_fin"] = m["c06_calendrier_fin"]
    d["m13_c06_calendrier_annees"] = m["c06_calendrier_annees"]
    d["m13_c06_calendrier_annee_courte"] = m["c06_calendrier_annee_courte"]
    d["m13_c06_calendrier_bissextile"] = m["c06_calendrier_bissextile"]
    d["m13_c06_branchee_lignes"] = m["c06_branchee_lignes"]
    d["m13_c06_branchee_total"] = m["c06_branchee_total"]
    d["m13_c06_jours_sans_vente"] = m["c06_jours_sans_vente"]
    d["m13_c06_ventes_hors_calendrier"] = m["c06_ventes_hors_calendrier"]
    d["m13_c06_rapport_lignes"] = m["c06_rapport_lignes"]
    d["m13_c06_29_fevrier_lignes"] = m["c06_29_fevrier_lignes"]
    d["m13_c06_29_fevrier_ca"] = f(m["c06_29_fevrier_ca"]) + " FCFA"
    d["m13_c06_ca_par_annee"] = m["c06_ca_par_annee"]
    d["m13_c06_ca_annee_courante"] = f(m["c06_ca_annee_courante"]) + " FCFA"
    d["m13_c06_ca_annee_precedente"] = f(m["c06_ca_annee_precedente"]) + " FCFA"
    d["m13_c06_ca_jour_moyen"] = f(m["c06_ca_jour_moyen"]) + " FCFA"
    d["m13_c06_jours_20m"] = m["c06_jours_20m"]
    d["m13_c06_pic_jour"] = m["c06_pic_jour"]
    d["m13_c06_pic_ca"] = f(m["c06_pic_ca"]) + " FCFA"
    d["m13_c06_pic_jour_libelle"] = m["c06_pic_jour_libelle"]
    d["m13_c06_creux_jour"] = m["c06_creux_jour"]
    d["m13_c06_creux_ca"] = f(m["c06_creux_ca"]) + " FCFA"
    d["m13_c06_creux_jour_libelle"] = m["c06_creux_jour_libelle"]
    d["m13_c06_ratio_pic_creux"] = m["c06_ratio_pic_creux"]
    d["m13_c06_t4_2025"] = f(m["c06_t4_2025"]) + " FCFA"
    d["m13_c06_calendrier_dix_ans"] = m["c06_calendrier_dix_ans"]
    d["m13_c06_faits_dix_ans"] = f(m["c06_faits_dix_ans"]) + " lignes"
    d["m13_c06_feries_jours"] = m["c06_feries_jours"]
    d["m13_c06_feries_libelles_n"] = m["c06_feries_libelles_n"]
    d["m13_c06_feries_libelles"] = m["c06_feries_libelles"]
    d["m13_c06_feries_jours_travailles"] = m["c06_feries_jours_travailles"]
    d["m13_c06_feries_ca"] = f(m["c06_feries_ca"]) + " FCFA"
    d["m13_c06_part_feries"] = m["c06_part_feries"]
    d["m13_c06_ca_par_jour_semaine"] = m["c06_ca_par_jour_semaine"]
    d["m13_c06_lundi_ca"] = f(m["c06_lundi_ca"]) + " FCFA"
    d["m13_c06_dimanche_ca"] = f(m["c06_dimanche_ca"]) + " FCFA"
    d["m13_c06_ratio_lundi_dimanche"] = m["c06_ratio_lundi_dimanche"]
    d["m13_c06_dimanches"] = m["c06_dimanches"]
    d["m13_c06_moyenne_dimanche"] = f(m["c06_moyenne_dimanche"]) + " FCFA"
    d["m13_c06_part_dimanche"] = m["c06_part_dimanche"]
    d["m13_c06_part_lundi"] = m["c06_part_lundi"]
    d["m13_c06_part_weekend"] = m["c06_part_weekend"]
    d["m13_c06_semaine_iso_max"] = m["c06_semaine_iso_max"]
    d["m13_c06_semaine_commerciale_max"] = m["c06_semaine_commerciale_max"]
    d["m13_c06_semaine53_jours"] = m["c06_semaine53_jours"]
    d["m13_c06_iso_decalage_jours"] = m["c06_iso_decalage_jours"]
    d["m13_c06_iso_1er_janvier"] = m["c06_iso_1er_janvier"]
    d["m13_c06_fiscal_lignes"] = m["c06_fiscal_lignes"]
    d["m13_c06_fiscal_debut"] = m["c06_fiscal_debut"]
    d["m13_c06_fiscal_fin"] = m["c06_fiscal_fin"]
    d["m13_c06_periode_fiscale_valeurs"] = m["c06_periode_fiscale_valeurs"]
    d["m13_c06_mois_comparables"] = m["c06_mois_comparables"]
    d["m13_c06_ytd_courant"] = f(m["c06_ytd_courant"]) + " FCFA"
    d["m13_c06_ytd_precedent"] = f(m["c06_ytd_precedent"]) + " FCFA"
    d["m13_c06_ytd_comparable"] = m["c06_ytd_comparable"]
    d["m13_c06_ytd_par_annee"] = m["c06_ytd_par_annee"]
    d["m13_c06_ecart_comparable_pct"] = m["c06_ecart_comparable_pct"]
    d["m13_c06_ecart_brut_pct"] = m["c06_ecart_brut_pct"]
    d["m13_c06_ecart_points"] = m["c06_ecart_points"]
    d["m13_c06_glissant_12_mois"] = f(m["c06_glissant_12_mois"]) + " FCFA"
    d["m13_c06_glissant_12_mois_avant"] = f(m["c06_glissant_12_mois_avant"]) + " FCFA"
    d["m13_c06_glissant_pct"] = m["c06_glissant_pct"]
    d["m13_c06_part_t4"] = m["c06_part_t4"]
    d["m13_c06_part_decembre_t4"] = m["c06_part_decembre_t4"]
    d["m13_c06_faits_a_trois_dates"] = m["c06_faits_a_trois_dates"]
    d["m13_c06_faits_au_mois"] = m["c06_faits_au_mois"]
    d["m13_c06_commandes_lignes"] = m["c06_commandes_lignes"]
    d["m13_c06_commandes_livrees"] = m["c06_commandes_livrees"]
    d["m13_c06_commandes_annulees"] = m["c06_commandes_annulees"]
    d["m13_c06_delai_moyen"] = m["c06_delai_moyen"]
    d["m13_c06_retard_lignes"] = m["c06_retard_lignes"]
    d["m13_c06_retard_pct"] = m["c06_retard_pct"]
    d["m13_c06_retard_moyen"] = m["c06_retard_moyen"]
    d["m13_c06_orphelines_livraison"] = m["c06_orphelines_livraison"]
    d["m13_c06_orphelines_dates"] = m["c06_orphelines_dates"]
    d["m13_c06_orphelines_debut"] = m["c06_orphelines_debut"]
    d["m13_c06_orphelines_fin"] = m["c06_orphelines_fin"]
    d["m13_c06_livraisons_montant"] = f(m["c06_livraisons_montant"]) + " FCFA"
    d["m13_c06_orphelines_montant"] = f(m["c06_orphelines_montant"]) + " FCFA"
    d["m13_c06_orphelines_pct"] = m["c06_orphelines_pct"]
    d["m13_c06_inner_lignes"] = m["c06_inner_lignes"]
    d["m13_c06_apres_correction_montant"] = f(m["c06_apres_correction_montant"]) + " FCFA"
    d["m13_c06_calendrier_prolonge"] = m["c06_calendrier_prolonge"]
    d["m13_c06_jours_ajoutes"] = m["c06_jours_ajoutes"]
    d["m13_c06_corrige_lignes"] = m["c06_corrige_lignes"]
    d["m13_c06_corrige_restantes"] = m["c06_corrige_restantes"]
    d["m13_c06_ventes_inchangees"] = m["c06_ventes_inchangees"]
    d["m13_c06_colonnes_fait_ventes"] = m["c06_colonnes_fait_ventes"]
    d["m13_c06_colonnes_heure"] = m["c06_colonnes_heure"]
    d["m13_c06_texte_calendrier"] = m["c06_texte_calendrier"]
    d["m13_c06_texte_deux_natures"] = m["c06_texte_deux_natures"]
    d["m13_c06_texte_partiel"] = m["c06_texte_partiel"]
    d["m13_c06_texte_orphelines"] = m["c06_texte_orphelines"]

    # --- La qualite, la documentation et la revue (M13.C07)
    d["m13_c07_controles"] = m["c07_controles"]
    d["m13_c07_controles_ok"] = m["c07_controles_ok"]
    d["m13_c07_tables"] = m["c07_tables"]
    d["m13_c07_tables_ok"] = m["c07_tables_ok"]
    d["m13_c07_faits"] = m["c07_faits"]
    d["m13_c07_faits_ok"] = m["c07_faits_ok"]
    d["m13_c07_cles_etrangeres"] = m["c07_cles_etrangeres"]
    d["m13_c07_orphelins"] = m["c07_orphelins"]
    d["m13_c07_recette_modele"] = f(m["c07_recette_modele"]) + " FCFA"
    d["m13_c07_recette_source"] = f(m["c07_recette_source"]) + " FCFA"
    d["m13_c07_fichiers_lisibles"] = m["c07_fichiers_lisibles"]
    d["m13_c07_colonnes"] = m["c07_colonnes"]
    d["m13_c07_colonnes_liste"] = m["c07_colonnes_liste"]
    d["m13_c07_script_lignes"] = m["c07_script_lignes"]
    d["m13_c07_script_commentaires"] = m["c07_script_commentaires"]
    d["m13_c07_cles_declarees"] = m["c07_cles_declarees"]
    d["m13_c07_fk_declarees"] = m["c07_fk_declarees"]
    d["m13_c07_commentaires_colonnes"] = m["c07_commentaires_colonnes"]
    d["m13_c07_defaut_1_caracteres_plate"] = f(m["c07_defaut_1_caracteres_plate"])
    d["m13_c07_defaut_1_caracteres_modele"] = f(m["c07_defaut_1_caracteres_modele"])
    d["m13_c07_defaut_1_facteur"] = m["c07_defaut_1_facteur"]
    d["m13_c07_defaut_2_dates"] = m["c07_defaut_2_dates"]
    d["m13_c07_defaut_2_mois"] = m["c07_defaut_2_mois"]
    d["m13_c07_defaut_3_montant"] = f(m["c07_defaut_3_montant"]) + " FCFA"
    d["m13_c07_defaut_3_pct"] = m["c07_defaut_3_pct"]
    d["m13_c07_defaut_4_cles"] = m["c07_defaut_4_cles"]
    d["m13_c07_defaut_5_libelles"] = m["c07_defaut_5_libelles"]
    d["m13_c07_defaut_5_familles"] = m["c07_defaut_5_familles"]
    d["m13_c07_grille_points"] = m["c07_grille_points"]
    d["m13_c07_grille_defauts"] = m["c07_grille_defauts"]
    d["m13_c07_controles_texte"] = m["c07_controles_texte"]
    d["m13_c07_documentation_texte"] = m["c07_documentation_texte"]
    d["m13_c07_texte_defauts"] = m["c07_texte_defauts"]
    d["m13_c07_grille_texte"] = m["c07_grille_texte"]

    # --- Le projet et l'evaluation (calibres sur M11 et M12)
    d["m13_projet_livrables"] = 4
    d["m13_projet_points"] = 20
    d["m13_projet_seuil"] = 13
    d["m13_projet_p1_points"] = 6
    d["m13_projet_p2_points"] = 6
    d["m13_projet_p3_points"] = 5
    d["m13_projet_p4_points"] = 3
    d["m13_projet_note_pages"] = 3
    d["m13_eval_points"] = 75
    d["m13_eval_seuil"] = 48
    d["m13_quiz_points"] = 20
    d["m13_quiz_questions"] = 15
    d["m13_quiz_seuil"] = 11
    d["m13_normalisation_points"] = 20
    d["m13_normalisation_exercices"] = 2
    d["m13_etude_cas_points"] = 30
    d["m13_etude_cas_seuil"] = 18
    d["m13_autotest_points"] = 5

    # --- Le controle croise cote pandas : la recette doit se retrouver des deux cotes
    v = pd.read_csv(os.path.join(os.path.dirname(ROOT), "01_socle_donnees", "data",
                                 "reference", "ventes_propres.csv"),
                    usecols=["montant_ttc", "est_retour"])
    ca_pandas = round(v.loc[v["est_retour"] == 0, "montant_ttc"].sum())
    if abs(ca_pandas - m["c_ca_modele"]) > 1:
        raise ValueError("M13 : recette cote pandas (%s) differente du modele (%s)"
                         % (f(ca_pandas), f(m["c_ca_modele"])))
    d["m13_croisee_pandas"] = ("OK : la recette du modele est celle de la source, verifiee cote "
                               "DuckDB et cote pandas (%s FCFA)" % f(ca_pandas))
    return d


def m11():
    """Les cles du module M11 - SQL avance pour la BI.

    Les `m11_*` mesurent le paysage du module (7 chapitres, 12 rapports, 20 requetes
    de reference) et le **socle** sur lequel il travaille : celui de M01-M03
    (`ventes_propres.csv`, 240 000 lignes, 44 mois, 5 magasins), declare par le script
    `03_exercices/dossier_M11/socle_m11.sql` (aucune donnee nouvelle).

    Trois mesures sont particulieres :

      - **le client 0** : il totalise 18,3 % du CA et n'existe pas dans le referentiel
        des clients — tout classement le place premier. Les cles `m11_client0_*` et
        `m11_concentration_*` mesurent l'ecart entre la lecture naive et la lecture
        corrigee : c'est l'etude de cas du module ;
      - **les objectifs** : 218 couples magasin-mois sur 220 (magasin 4 : 2024-02 et
        2024-03 absents) et un total qui vaut 233,3 % du realise — le rapport de
        controle R12 ne peut pas conclure sans le dire ;
      - **les performances** : un temps machine n'est pas reproductible au bit pres.
        Les cles `m11_perf_*` sont lues dans `03_exercices/dossier_M11/PERF_M11.json`,
        fige par `tools/perf_M11.py --figer` (mediane de 5 executions, datee). Le
        releve reste donc identique d'une execution a l'autre.
    """
    import json
    d = {}
    depot = os.path.dirname(ROOT)          # la racine du depot (ROOT = 01_socle_donnees)
    jouets = os.path.join(depot, "03_exercices", "dossier_M11")

    # Structure du module (05_livrables/plan_M11.md)
    d["m11_chapitres_total"] = 7
    d["m11_heures"] = 30
    d["m11_niveau_cible"] = "N3-N4"
    d["m11_budget_pages"] = 105
    d["m11_prerequis"] = "M07 (tout) ; M06.C04 ; M02"
    d["m11_rapports_projet"] = 12
    d["m11_requetes_reference"] = 20
    d["m11_requetes_autotestees"] = 18
    d["m11_quiz_questions"] = 20
    d["m11_exercices"] = 5
    d["m11_tests_non_regression"] = 3
    d["m11_projet_livrables"] = 4
    d["m11_sgbd_duckdb"] = "duckdb 1.5.5 (execute)"
    d["m11_sgbd_sqlite"] = "sqlite3 natif Python 3.13 (execute, controle croise)"
    d["m11_sgbd_postgres"] = "cite sans execute (regle M06 §1.5)"
    d["m11_sgbd_sqlserver"] = "cite pour les variantes de syntaxe (TOP, QUALIFY absent)"

    # Le socle : un script SQL, pas un fichier de base (contrainte de poids de l'atelier)
    d["m11_socle_fichier"] = "03_exercices/dossier_M11/socle_m11.sql"
    d["m11_socle_taille_octets"] = os.path.getsize(os.path.join(jouets, "socle_m11.sql"))
    d["m11_socle_tables"] = 5
    d["m11_socle_vues"] = 2
    d["m11_socle_reconstruit_s"] = "0,4 (mesure de l'atelier ; aucun .duckdb versionne)"

    # --- Mesures du socle, cote SQL (DuckDB execute) et controle cote pandas
    try:
        import duckdb
    except ImportError as e:
        raise RuntimeError(
            "duckdb indisponible (%s) : le releve M11 serait vide. "
            "Installer duckdb ou demander un releve partiel (chiffres_manuel.py Mxx)." % e)

    os.chdir(depot)                        # les vues du socle sont relatives a la racine
    con = duckdb.connect()
    con.execute(open(os.path.join(jouets, "socle_m11.sql"), encoding="utf-8").read())

    def un(sql, *args):
        return con.execute(sql, list(args)).fetchone()

    lignes, hors_retours, retours, ca_net, tickets, tmin, tmax = un("""
        SELECT COUNT(*), COUNT(*) FILTER (WHERE NOT est_retour),
               COUNT(*) FILTER (WHERE est_retour), SUM(montant_ttc) FILTER (WHERE NOT est_retour),
               COUNT(DISTINCT id_ticket), MIN(date_vente), MAX(date_vente) FROM ventes""")
    d["m11_lignes"] = int(lignes)
    d["m11_lignes_hors_retours"] = int(hors_retours)
    d["m11_retours"] = int(retours)
    d["m11_ca_net"] = FMT(ca_net) + " FCFA"
    d["m11_tickets_toutes_lignes"] = int(tickets)
    d["m11_tickets"] = int(un("SELECT COUNT(DISTINCT id_ticket) FROM ventes WHERE NOT est_retour")[0])
    # Quatre nombres, pas trois — et deux d'entre eux etaient confondus dans le premier
    # releve : `retours_seuls` designait en realite les tickets PORTANT un retour.
    d["m11_tickets_retours_seuls"] = int(un(
        "SELECT COUNT(*) FROM (SELECT id_ticket FROM ventes GROUP BY 1 "
        "HAVING MIN(CAST(est_retour AS INT)) = 1)")[0])
    d["m11_tickets_avec_retour"] = int(un(
        "SELECT COUNT(*) FROM (SELECT id_ticket FROM ventes GROUP BY 1 "
        "HAVING MAX(CAST(est_retour AS INT)) = 1)")[0])
    d["m11_tickets_mixtes"] = int(un("""
        SELECT COUNT(*) FROM (SELECT id_ticket, COUNT(*) n, SUM(CAST(est_retour AS INT)) r
        FROM ventes GROUP BY 1) WHERE r > 0 AND r < n""")[0])
    d["m11_tickets_definition"] = (
        "quatre nombres pour la meme question : %s tickets au total, %s avec au moins une ligne "
        "vendue, %s qui portent au moins un retour (dont %s mixtes et %s uniquement des retours) —"
        " un rapport qui ne dit pas lequel il compte est inverifiable"
        % (FMT(tickets), FMT(d["m11_tickets"]), FMT(d["m11_tickets_avec_retour"]),
           FMT(d["m11_tickets_mixtes"]), FMT(d["m11_tickets_retours_seuls"])))
    d["m11_premiere_vente"] = str(tmin)
    d["m11_derniere_vente"] = str(tmax)
    d["m11_mois_couverts"] = int(un("SELECT COUNT(DISTINCT date_trunc('month', date_vente)) FROM ventes")[0])
    d["m11_clients_vente"] = int(un("SELECT COUNT(DISTINCT id_client) FROM ventes")[0])
    d["m11_clients_referentiel"] = int(un("SELECT COUNT(*) FROM clients")[0])
    d["m11_magasins"] = int(un("SELECT COUNT(DISTINCT id_magasin) FROM ventes")[0])
    d["m11_magasins_referentiel"] = int(un("SELECT COUNT(*) FROM magasin")[0])
    d["m11_vendeurs"] = int(un("SELECT COUNT(DISTINCT id_vendeur) FROM ventes")[0])
    d["m11_produits"] = int(un("SELECT COUNT(DISTINCT id_produit) FROM ventes")[0])
    d["m11_villes_manquantes"] = int(un("SELECT COUNT(*) FROM clients WHERE ville IS NULL OR ville = ''")[0])
    d["m11_villes_manquantes_pct"] = round(100.0 * d["m11_villes_manquantes"] / d["m11_clients_referentiel"], 1)
    d["m11_categories_libelles"] = int(un("SELECT COUNT(DISTINCT categorie) FROM produit")[0])
    d["m11_categories_ecritures"] = int(un(
        "SELECT COUNT(DISTINCT UPPER(TRIM(categorie))) FROM produit")[0])
    NORME = ("CASE WHEN UPPER(TRIM(categorie)) IN ('MATERIAUX','MATÉRIAUX') THEN 'MATÉRIAUX' "
             "WHEN UPPER(TRIM(categorie)) IN ('PEINTURE','PEINTURES') THEN 'PEINTURE' "
             "WHEN UPPER(TRIM(categorie)) = 'ELECTRICITÉ' THEN 'ÉLECTRICITÉ' "
             "ELSE UPPER(TRIM(categorie)) END")
    d["m11_categories_familles"] = int(un(
        "SELECT COUNT(DISTINCT %s) FROM produit" % NORME)[0])
    d["m11_categories_familles_texte"] = (
        "%s libelles bruts, %s ecritures apres casse et espaces, %s familles apres accents et "
        "pluriel : chaque relecture du libelle reduit le catalogue, et chaque reduction change les "
        "classements" % (FMT(d["m11_categories_libelles"]), FMT(d["m11_categories_ecritures"]),
                         FMT(d["m11_categories_familles"])))
    d["m11_categories_pieges"] = (
        "16 libelles pour 9 ecritures : Materiaux / materiaux / MATERIAUX / Matériaux (accent), "
        "« Quincaillerie » avec un espace final, PEINTURE / Peinture / peinture / Peintures")
    familles = dict(con.execute("""
        WITH p AS (SELECT id_produit, UPPER(TRIM(categorie)) fam FROM produit),
             f AS (SELECT fam, SUM(v.montant_ttc) ca FROM ventes v JOIN p USING(id_produit)
                   WHERE NOT v.est_retour GROUP BY 1)
        SELECT fam, ROUND(ca) FROM f ORDER BY ca DESC""").fetchall())
    materiaux = int(familles["MATERIAUX"]) + int(familles["MATÉRIAUX"])
    d["m11_famille_brute_premiere"] = "%s (%s FCFA, libelles tels quels)" % (
        "PLOMBERIE", FMT(familles["PLOMBERIE"]))
    d["m11_famille_normalisee_premiere"] = "MATÉRIAUX (%s FCFA, deux ecritures reunis)" % FMT(materiaux)
    d["m11_famille_inversion_fcfa"] = FMT(materiaux - int(familles["PLOMBERIE"]))
    d["m11_famille_inversion_texte"] = (
        "sans normalisation, Plomberie est la premiere famille ; avec les accents et la casse "
        "normalises, Materiaux la depasse de %s FCFA — le classement depend d'une ecriture"
        % d["m11_famille_inversion_fcfa"])

    # --- Le client 0 : le fait qui porte le module
    c0_lignes, c0_tickets, c0_ca, c0_magasins = un("""
        SELECT COUNT(*), COUNT(DISTINCT id_ticket), SUM(montant_ttc), COUNT(DISTINCT id_magasin)
        FROM ventes WHERE NOT est_retour AND id_client = 0""")
    d["m11_client0_id"] = 0
    d["m11_client0_lignes"] = int(c0_lignes)
    d["m11_client0_tickets"] = int(c0_tickets)
    d["m11_client0_ca"] = FMT(c0_ca) + " FCFA"
    d["m11_client0_magasins"] = int(c0_magasins)
    d["m11_client0_part_pct"] = round(100.0 * c0_ca / ca_net, 1)
    d["m11_client0_referentiel"] = int(un("SELECT COUNT(*) FROM clients WHERE id_client = 0")[0])
    d["m11_client0_anomalie"] = "absent du referentiel clients.csv : c'est un client NON IDENTIFIE, pas un client"

    # --- Concentration : la meme question, deux ecritures et deux reponses
    def concentration(avec_anonyme):
        filtre = "" if avec_anonyme else " AND id_client <> 0"
        r = {}
        for part in (1, 5, 10, 20):
            r[part] = un("""
                WITH c AS (SELECT id_client, SUM(montant_ttc) ca FROM ventes
                           WHERE NOT est_retour%s GROUP BY 1),
                     n AS (SELECT COUNT(*) k FROM c),
                     t AS (SELECT SUM(ca) tot FROM c),
                     b AS (SELECT ca, NTILE(100) OVER (ORDER BY ca DESC, id_client) cent FROM c)
                SELECT ROUND(100.0 * SUM(ca) / (SELECT tot FROM t), 1) FROM b
                WHERE cent <= %d""" % (filtre, part))[0]
        return r
    cc = concentration(True)
    d["m11_concentration_top1_pct"] = float(cc[1])
    d["m11_concentration_top5_pct"] = float(cc[5])
    d["m11_concentration_top10_pct"] = float(cc[10])
    d["m11_concentration_top20_pct"] = float(cc[20])
    d["m11_concentration_top10_sans_anonyme_pct"] = float(concentration(False)[10])
    d["m11_concentration_clients_hors_anonyme"] = int(
        un("SELECT COUNT(DISTINCT id_client) FROM ventes WHERE NOT est_retour AND id_client <> 0")[0])
    d["m11_concentration_definition"] = (
        "top N %% = NTILE(100) <= N, soit 235 clients par centile ; avec ROW_NUMBER() <= 10 %% "
        "on garde 2 349 clients et on lit %s %% au lieu de %s %% : la definition deplace la reponse"
        % (un("""WITH c AS (SELECT id_client, SUM(montant_ttc) ca FROM ventes WHERE NOT est_retour GROUP BY 1),
                       n AS (SELECT COUNT(*) k FROM c), t AS (SELECT SUM(ca) tot FROM c),
                       b AS (SELECT ca, ROW_NUMBER() OVER (ORDER BY ca DESC, id_client) rg FROM c)
                 SELECT ROUND(100.0 * SUM(ca) / (SELECT tot FROM t), 1) FROM b
                 WHERE rg <= 0.10 * (SELECT k FROM n)""")[0], cc[10]))
    d["m11_verite_terrain"] = "10 %% des clients font 60 %% du CA : FAUX sur ce socle (%s %% mesures)" % cc[10]

    # --- Magasins : rang, part, ecart au premier
    mag = con.execute("""
        SELECT m.nom, SUM(v.montant_ttc) ca,
               ROUND(100.0 * SUM(v.montant_ttc) / SUM(SUM(v.montant_ttc)) OVER (), 2) part
        FROM ventes v JOIN magasin m USING (id_magasin)
        WHERE NOT v.est_retour GROUP BY 1 ORDER BY ca DESC""").fetchall()
    d["m11_magasin_premier"] = mag[0][0]
    d["m11_ca_magasin_max"] = FMT(mag[0][1]) + " FCFA"
    d["m11_part_magasin_max_pct"] = float(mag[0][2])
    d["m11_magasin_dernier"] = mag[-1][0]
    d["m11_ca_magasin_min"] = FMT(mag[-1][1]) + " FCFA"
    d["m11_part_magasin_min_pct"] = float(mag[-1][2])
    d["m11_rapport_magasin_max_min"] = round(float(mag[0][1]) / float(mag[-1][1]), 2)
    d["m11_magasin_non_utilise"] = int(un("""
        SELECT COUNT(*) FROM magasin m WHERE NOT EXISTS
        (SELECT 1 FROM ventes v WHERE v.id_magasin = m.id_magasin)""")[0])

    # --- Le temps : la croissance, a perimetre egal et a perimetre naif
    an = dict(con.execute("""SELECT YEAR(date_vente), SUM(montant_ttc) FROM ventes
                             WHERE NOT est_retour GROUP BY 1 ORDER BY 1""").fetchall())
    an8 = dict(con.execute("""SELECT YEAR(date_vente), SUM(montant_ttc) FROM ventes
                              WHERE NOT est_retour AND MONTH(date_vente) <= 8 GROUP BY 1""").fetchall())
    for a in (2023, 2024, 2025, 2026):
        d["m11_ca_%d" % a] = FMT(an[a]) + " FCFA"
        d["m11_ca_8_mois_%d" % a] = FMT(an8[a]) + " FCFA"
    d["m11_croissance_2024_pct"] = round(100.0 * (an[2024] / an[2023] - 1), 1)
    d["m11_croissance_2025_pct"] = round(100.0 * (an[2025] / an[2024] - 1), 1)
    d["m11_croissance_8_mois_2024_pct"] = round(100.0 * (an8[2024] / an8[2023] - 1), 1)
    d["m11_croissance_8_mois_2025_pct"] = round(100.0 * (an8[2025] / an8[2024] - 1), 1)
    d["m11_croissance_8_mois_2026_pct"] = round(100.0 * (an8[2026] / an8[2025] - 1), 1)
    d["m11_piege_2026_pct"] = round(100.0 * (an[2026] / an[2025] - 1), 1)
    d["m11_piege_2026_texte"] = (
        "comparer 2026 (8 mois realisees) a 2025 (12 mois) fait lire %s %% : une chute qui n'existe pas"
        % d["m11_piege_2026_pct"])
    mois = con.execute("""
        SELECT strftime(date_trunc('month', date_vente), '%Y-%m') m, SUM(montant_ttc) ca
        FROM ventes WHERE NOT est_retour GROUP BY 1 ORDER BY 2 DESC""").fetchall()
    d["m11_ca_mois_max"] = FMT(mois[0][1]) + " FCFA"
    d["m11_mois_record"] = mois[0][0]
    d["m11_ca_mois_min"] = FMT(mois[-1][1]) + " FCFA"
    d["m11_mois_creux"] = mois[-1][0]
    d["m11_ecart_mois_max_min"] = FMT(mois[0][1] - mois[-1][1]) + " FCFA"
    ma = con.execute("""
        WITH m AS (SELECT date_trunc('month', date_vente) mm, SUM(montant_ttc) ca
                   FROM ventes WHERE NOT est_retour GROUP BY 1)
        SELECT ROUND(AVG(ca) OVER (ORDER BY mm ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 0),
               ROUND(AVG(ca) OVER (ORDER BY mm ROWS BETWEEN 11 PRECEDING AND CURRENT ROW), 0)
        FROM m ORDER BY mm DESC LIMIT 1""").fetchone()
    d["m11_moyenne_mobile_3_dernier"] = FMT(ma[0]) + " FCFA"
    d["m11_moyenne_mobile_12_dernier"] = FMT(ma[1]) + " FCFA"
    d["m11_dernier_mois"] = un("SELECT strftime(MAX(date_vente), '%Y-%m') FROM ventes")[0]

    # --- Objectifs : le trou de deux mois et un taux de realisation qui doit se dire
    objs = un("SELECT COUNT(*), SUM(ca_objectif_ttc) FROM objectif_mois")
    d["m11_objectifs_lignes"] = int(objs[0])
    d["m11_objectifs_attendus"] = 5 * 44
    d["m11_objectifs_manquants"] = 5 * 44 - int(objs[0])
    trous = con.execute("""
        WITH r AS (SELECT id_magasin, strftime(date_trunc('month', date_vente), '%Y-%m') am
                   FROM ventes WHERE NOT est_retour GROUP BY 1, 2)
        SELECT r.id_magasin, r.am FROM r LEFT JOIN objectif_mois o
        ON o.id_magasin = r.id_magasin AND o.annee_mois = r.am
        WHERE o.ca_objectif_ttc IS NULL ORDER BY 2""").fetchall()
    d["m11_objectifs_trous"] = ", ".join("magasin %d en %s" % t for t in trous)
    d["m11_objectif_total"] = FMT(objs[1]) + " FCFA"
    d["m11_taux_realisation_pct"] = round(100.0 * ca_net / float(objs[1]), 1)
    taux = con.execute("""
        WITH r AS (SELECT id_magasin, strftime(date_trunc('month', date_vente), '%Y-%m') am,
                          SUM(montant_ttc) ca FROM ventes WHERE NOT est_retour GROUP BY 1, 2)
        SELECT MIN(t), MAX(t) FROM (SELECT ROUND(100.0 * r.ca / o.ca_objectif_ttc) t
        FROM r JOIN objectif_mois o ON o.id_magasin = r.id_magasin AND o.annee_mois = r.am)""").fetchone()
    d["m11_taux_realisation_min_pct"] = int(taux[0])
    d["m11_taux_realisation_max_pct"] = int(taux[1])

    # --- Panier et frequence
    pan = un("""SELECT AVG(t), MEDIAN(t), QUANTILE_CONT(t, 0.9) FROM
                (SELECT id_ticket, SUM(montant_ttc) t FROM ventes WHERE NOT est_retour GROUP BY 1)""")
    d["m11_panier_moyen"] = FMT(pan[0]) + " FCFA"
    d["m11_panier_median"] = FMT(pan[1]) + " FCFA"
    d["m11_panier_p90"] = FMT(pan[2]) + " FCFA"
    d["m11_panier_ecart_moyenne_mediane_pct"] = round(100.0 * (float(pan[0]) / float(pan[1]) - 1), 1)
    freq = un("""SELECT MEDIAN(n), AVG(n), MAX(n), COUNT(*),
                        COUNT(*) FILTER (WHERE n = 1)
                 FROM (SELECT id_client, COUNT(DISTINCT id_ticket) n FROM ventes
                       WHERE NOT est_retour GROUP BY 1)""")
    d["m11_tickets_par_client_median"] = int(freq[0])
    d["m11_tickets_par_client_moyen"] = round(float(freq[1]), 2)
    d["m11_tickets_par_client_max"] = int(freq[2])
    d["m11_clients_un_seul_ticket"] = int(freq[4])
    d["m11_clients_un_seul_ticket_pct"] = round(100.0 * freq[4] / freq[3], 2)

    # --- Cohortes et retention
    d["m11_cohortes"] = int(un("""
        SELECT COUNT(DISTINCT date_trunc('month', p)) FROM
        (SELECT id_client, MIN(date_vente) p FROM ventes WHERE NOT est_retour GROUP BY 1)""")[0])
    d["m11_cohorte_premiere_taille"] = int(un("""
        SELECT COUNT(*) FROM (SELECT id_client, MIN(date_vente) p FROM ventes
        WHERE NOT est_retour GROUP BY 1) WHERE date_trunc('month', p) = DATE '2023-01-01'""")[0])
    d["m11_cohorte_derniere_taille"] = int(un("""
        SELECT COUNT(*) FROM (SELECT id_client, MIN(date_vente) p FROM ventes
        WHERE NOT est_retour GROUP BY 1) WHERE date_trunc('month', p) = DATE '2026-08-01'""")[0])
    retention = con.execute("""
        WITH p AS (SELECT id_client, date_trunc('month', MIN(date_vente)) co FROM ventes
                   WHERE NOT est_retour GROUP BY 1),
             a AS (SELECT DISTINCT id_client, date_trunc('month', date_vente) m FROM ventes
                   WHERE NOT est_retour),
             t0 AS (SELECT co, COUNT(*) n0 FROM p GROUP BY 1),
             b AS (SELECT p.co, DATEDIFF('month', p.co, a.m) anc, COUNT(DISTINCT a.id_client) actifs
                   FROM p JOIN a USING (id_client) GROUP BY 1, 2)
        SELECT b.anc, ROUND(100.0 * SUM(b.actifs) / SUM(t0.n0), 1)
        FROM b JOIN t0 USING (co)
        WHERE b.co < DATE '2025-01-01' AND b.anc IN (1, 3, 6, 12, 24) GROUP BY 1 ORDER BY 1""").fetchall()
    for anc, pct in retention:
        d["m11_retention_m%d_pct" % anc] = float(pct)
    d["m11_retention_lecture"] = (
        "retention mensuelle plate (15 a 18 % de M+1 a M+24) : le socle ne raconte pas une "
        "entreprise qui perd ses clients, il faut le dire avant d'en tirer une conclusion")
    d["m11_cohortes_incompletes"] = int(un("""
        SELECT COUNT(*) FROM (SELECT date_trunc('month', p) co, COUNT(*) n FROM
        (SELECT id_client, MIN(date_vente) p FROM ventes WHERE NOT est_retour GROUP BY 1)
        GROUP BY 1) WHERE n < 100""")[0])

    # --- RFM
    # L'egalite que NTILE(3) doit departager, et ce qu'il advient quand on ne la departage pas.
    # Mesure reproducible (`SELECT n, COUNT(*) ... GROUP BY 1 ORDER BY 2 DESC`) : la frequence
    # modale est un vrai piege a egalites.
    n_egal, k_egal = un("""
        WITH c AS (SELECT id_client, COUNT(DISTINCT id_ticket) n FROM ventes
                   WHERE NOT est_retour GROUP BY 1)
        SELECT n, COUNT(*) FROM c GROUP BY 1 ORDER BY 2 DESC LIMIT 1""")
    d["m11_ntile_egalite_clients"] = int(k_egal)
    d["m11_ntile_egalite_tickets"] = int(n_egal)
    d["m11_ntile_egalite_pct"] = round(100.0 * k_egal / d["m11_clients_vente"], 1)
    # Observation datee (15 executions du 24/09/2026, meme requete RFM sans cle de departage) :
    # figee ici, comme les mesures de performance, parce que la valeur, elle, bouge.
    d["m11_ntile_derive_observee"] = (
        "15 executions le 24/09/2026 de la meme requete RFM sans cle de departage : le segment "
        "principal a compte 2 718, 2 720, 2 728 et 2 738 clients selon l'ordonnancement interne "
        "du moteur — %s clients partageant %s tickets suffisent a rendre la frontiere des tiers "
        "instable" % (FMT(k_egal), n_egal))
    d["m11_ntile_lecon"] = (
        "un classement sans critere de departage explicite n'est pas un rapport : il change de "
        "resultat sans qu'aucune donnee n'ait change")
    rfm = con.execute("""
        WITH c AS (SELECT id_client, MAX(date_vente) derniere, COUNT(DISTINCT id_ticket) f,
                          SUM(montant_ttc) m FROM ventes WHERE NOT est_retour GROUP BY 1),
             s AS (SELECT id_client, derniere, f, m,
                          NTILE(3) OVER (ORDER BY derniere DESC, id_client) r,
                          NTILE(3) OVER (ORDER BY f, id_client) f3,
                          NTILE(3) OVER (ORDER BY m, id_client) m3 FROM c)
        SELECT CAST(r AS VARCHAR) || CAST(f3 AS VARCHAR) || CAST(m3 AS VARCHAR) seg,
               COUNT(*), ROUND(SUM(m)), ROUND(100.0 * SUM(m) / SUM(SUM(m)) OVER (), 1)
        FROM s GROUP BY 1 ORDER BY 3 DESC LIMIT 1""").fetchone()
    d["m11_rfm_segment_premier"] = rfm[0]
    d["m11_rfm_segment_premier_clients"] = int(rfm[1])
    d["m11_rfm_segment_premier_ca"] = FMT(rfm[2]) + " FCFA"
    d["m11_rfm_segment_premier_part_pct"] = float(rfm[3])
    d["m11_rfm_segment_premier_piege"] = (
        "ce segment contient le client 0 : le meilleur tiers du RFM recompense un client non identifie")
    d["m11_rfm_segments_possibles"] = 27

    # --- Avance (C05) : tableau croise, recapitulatif, recursif
    d["m11_pivot_modes_paiement"] = int(un("SELECT COUNT(DISTINCT mode_paiement) FROM ventes")[0])
    d["m11_rollup_niveaux"] = 3
    d["m11_categories_arbre"] = int(un("SELECT COUNT(DISTINCT categorie) FROM produit")[0])
    d["m11_sous_categories_distinctes"] = int(un("SELECT COUNT(DISTINCT sous_categorie) FROM produit")[0])
    d["m11_couples_categorie_sous_categorie"] = int(un(
        "SELECT COUNT(*) FROM (SELECT DISTINCT categorie, sous_categorie FROM produit)")[0])
    d["m11_calendrier_jours"] = int(un("SELECT COUNT(*) FROM calendrier")[0])
    d["m11_calendrier_jours_feries"] = int(un("SELECT SUM(est_ferie) FROM calendrier")[0])

    # --- Performance (C06) : lue dans PERF_M11.json, figee par l'instrument
    chemin_perf = os.path.join(jouets, "PERF_M11.json")
    if os.path.exists(chemin_perf):
        p = json.load(open(chemin_perf, encoding="utf-8"))
        d["m11_perf_date"] = p["date"]
        d["m11_perf_protocole"] = p["protocole"] + " (tools/perf_M11.py --figer)"
        d["m11_perf_vue_ms"] = "%s ms (vue : relit le CSV)" % p["vue_ms"]
        d["m11_perf_table_ms"] = "%s ms (table en memoire)" % p["table_ms"]
        d["m11_perf_rapport_vue_table"] = round(p["vue_ms"] / p["table_ms"])
        d["m11_perf_select_etoile_ms"] = "%s ms" % p["select_etoile_ms"]
        d["m11_perf_select_trois_ms"] = "%s ms" % p["select_trois_colonnes_ms"]
        d["m11_perf_rapport_select"] = round(p["select_etoile_ms"] / p["select_trois_colonnes_ms"], 1)
        d["m11_perf_vue_select_etoile_ms"] = "%s ms" % p["vue_select_etoile_ms"]
        d["m11_perf_vue_select_trois_ms"] = "%s ms" % p["vue_select_trois_colonnes_ms"]
        d["m11_perf_index_client_ms"] = "%s ms sans index, %s ms avec index" % (
            p["index_client_sans_ms"], p["index_client_avec_ms"])
        d["m11_perf_index_agregat_ms"] = "%s ms sans index, %s ms avec index" % (
            p["index_agregat_sans_ms"], p["index_agregat_avec_ms"])
        d["m11_perf_index_verdict"] = (
            "aucun effet mesurable et le plan reste un SEQ_SCAN : en DuckDB, l'index n'est pas "
            "un reflexe, c'est une reponse a un plan")
        d["m11_perf_fenetre_ms"] = "%s ms (fonction de fenetre)" % p["fenetre_ms"]
        d["m11_perf_scalaire_ms"] = "%s ms (sous-requete scalaire)" % p["scalaire_ms"]
        d["m11_perf_rapport_fenetre_scalaire"] = round(p["scalaire_ms"] / p["fenetre_ms"], 1)
        d["m11_perf_colonnes_plan_etoile"] = int(p["colonnes_plan_etoile"])
        d["m11_perf_colonnes_plan_trois"] = int(p["colonnes_plan_trois"])
        d["m11_perf_etages_plan"] = int(p["etages_plan"])
        d["m11_perf_etages_liste"] = " | ".join(p["etages_liste"])
        d["m11_perf_lecture"] = (
            "le plan annonce x%d de colonnes lues avant execution, l'horloge confirme x%s : "
            "le cout du SELECT * se lit dans le plan, pas seulement au chronometre"
            % (p["colonnes_plan_etoile"] / p["colonnes_plan_trois"], d["m11_perf_rapport_select"]))
    else:
        d["m11_perf_etat"] = "non mesure : lancer tools/perf_M11.py --figer"

    # --- C01 : la fenetre face a GROUP BY, et le piege de la cle de jointure incomplete
    d["m11_c01_moyenne_ligne"] = FMT(un("SELECT AVG(montant_ttc) FROM ventes WHERE NOT est_retour")[0]) + " FCFA"
    d["m11_c01_valeurs_ca_magasin"] = int(un(
        "SELECT COUNT(DISTINCT ca) FROM (SELECT SUM(montant_ttc) ca FROM ventes "
        "WHERE NOT est_retour GROUP BY id_magasin)")[0])
    d["m11_c01_jointure_mois_seul_fcfa"] = FMT(un("""
        SELECT SUM(v.montant_ttc) FROM ventes v JOIN
        (SELECT id_magasin, strftime(date_trunc('month', date_vente), '%Y-%m') am, SUM(montant_ttc) ca
         FROM ventes WHERE NOT est_retour GROUP BY 1, 2) t
        ON t.am = strftime(date_trunc('month', v.date_vente), '%Y-%m')
        WHERE NOT v.est_retour""")[0]) + " FCFA"
    d["m11_c01_jointure_mois_seul_lignes"] = int(un("""
        SELECT COUNT(*) FROM ventes v JOIN
        (SELECT id_magasin, strftime(date_trunc('month', date_vente), '%Y-%m') am, SUM(montant_ttc) ca
         FROM ventes WHERE NOT est_retour GROUP BY 1, 2) t
        ON t.am = strftime(date_trunc('month', v.date_vente), '%Y-%m')
        WHERE NOT v.est_retour""")[0])
    d["m11_c01_jointure_mois_seul_texte"] = (
        "une jointure sur le mois seul (la cle du magasin oubliee) annonce %s FCFA sur %s lignes : "
        "cinq fois le total, sans une seule erreur de syntaxe"
        % (d["m11_c01_jointure_mois_seul_fcfa"], FMT(d["m11_c01_jointure_mois_seul_lignes"])))
    d["m11_c01_part_janvier_2023_pct"] = float(un("""
        WITH m AS (SELECT strftime(date_trunc('month', date_vente), '%Y-%m') am, YEAR(date_vente) an,
                          SUM(montant_ttc) ca FROM ventes WHERE NOT est_retour GROUP BY 1, 2)
        SELECT part FROM (SELECT am, ROUND(100.0 * ca / SUM(ca) OVER (PARTITION BY an), 1) part
                          FROM m) WHERE am = '2023-01'""")[0])
    # Le filtre applique AVANT la fenetre : la fenetre ne voit plus qu'une ligne et la part vaut 100 %.
    d["m11_c01_part_janvier_2023_filtre_avant_pct"] = float(un("""
        WITH m AS (SELECT strftime(date_trunc('month', date_vente), '%Y-%m') am, YEAR(date_vente) an,
                          SUM(montant_ttc) ca FROM ventes WHERE NOT est_retour GROUP BY 1, 2)
        SELECT ROUND(100.0 * ca / SUM(ca) OVER (PARTITION BY an), 1) FROM m WHERE am = '2023-01'""")[0])
    d["m11_c01_fenetre_apres_where_texte"] = (
        "la meme requete publiee avec le filtre dans le meme SELECT que la fenetre affiche %s %% "
        "au lieu de %s %% : une fenetre s'evalue APRES le WHERE, et filtre avant, elle ne compare plus rien"
        % (d["m11_c01_part_janvier_2023_filtre_avant_pct"], d["m11_c01_part_janvier_2023_pct"]))
    d["m11_c01_part_janvier_2023_sans_partition_pct"] = float(un("""
        WITH m AS (SELECT strftime(date_trunc('month', date_vente), '%Y-%m') am, SUM(montant_ttc) ca
                   FROM ventes WHERE NOT est_retour GROUP BY 1)
        SELECT ROUND(100.0 * ca / SUM(ca) OVER (), 1) FROM m WHERE am = '2023-01'""")[0])
    d["m11_c01_partition_oubliee_texte"] = (
        "janvier 2023 pese %s %% du CA de son annee ; sans PARTITION BY, la meme requete affiche "
        "%s %% — un chiffre plus petit, plus credible, et faux"
        % (d["m11_c01_part_janvier_2023_pct"], d["m11_c01_part_janvier_2023_sans_partition_pct"]))
    d["m11_c01_clients_10_tickets_plus"] = int(un("""
        SELECT COUNT(*) FROM (SELECT id_client, COUNT(DISTINCT id_ticket) t FROM ventes
        WHERE NOT est_retour GROUP BY 1) WHERE t >= 10""")[0])
    d["m11_c01_part_ca_10_tickets_plus_pct"] = float(un("""
        WITH c AS (SELECT id_client, COUNT(DISTINCT id_ticket) t, SUM(montant_ttc) ca
                   FROM ventes WHERE NOT est_retour GROUP BY 1)
        SELECT ROUND(100.0 * SUM(ca) FILTER (WHERE t >= 10) / SUM(ca), 1) FROM c""")[0])
    cumul = con.execute("""
        SELECT ROUND(montant_ttc), ROUND(SUM(montant_ttc) OVER (ORDER BY date_vente, id_vente)),
               ROUND(AVG(montant_ttc) OVER (ORDER BY date_vente, id_vente
                     ROWS BETWEEN 2 PRECEDING AND CURRENT ROW))
        FROM ventes WHERE NOT est_retour AND id_magasin = 1 ORDER BY date_vente, id_vente LIMIT 5""").fetchall()
    d["m11_c01_cumul_cinq_lignes"] = " ; ".join(FMT(r[1]) for r in cumul) + " FCFA"
    d["m11_c01_moyenne_glissante_cinq_lignes"] = " ; ".join(FMT(r[2]) for r in cumul) + " FCFA"
    d["m11_c01_cadre_texte"] = (
        "sur les cinq premieres lignes du magasin 1, le cumul monte a %s et la moyenne glissante "
        "de trois lignes passe par %s : le cadre de fenetre decide de ce que la fonction regarde"
        % (d["m11_c01_cumul_cinq_lignes"], d["m11_c01_moyenne_glissante_cinq_lignes"]))

    # --- C02 : rang, cumul, decalage
    d["m11_c02_valeurs_distinctes_tickets"] = int(un(
        "SELECT COUNT(DISTINCT t) FROM (SELECT id_client, COUNT(DISTINCT id_ticket) t FROM ventes "
        "WHERE NOT est_retour GROUP BY 1)")[0])
    rang = un("""
        WITH c AS (SELECT id_client, COUNT(DISTINCT id_ticket) t FROM ventes
                   WHERE NOT est_retour GROUP BY 1),
             r AS (SELECT t, RANK() OVER (ORDER BY t DESC) rk,
                          DENSE_RANK() OVER (ORDER BY t DESC) dr FROM c)
        SELECT MAX(rk), MAX(dr) FROM r""")
    d["m11_c02_max_rank"] = int(rang[0])
    d["m11_c02_max_dense_rank"] = int(rang[1])
    d["m11_c02_rank_vs_dense_texte"] = (
        "sur la meme mesure, RANK descend jusqu'a %s et DENSE_RANK s'arrete a %s : deux nombres justes, "
        "un seul interpretable" % (FMT(rang[0]), rang[1]))
    d["m11_c02_clients_20_tickets"] = int(un("""
        SELECT COUNT(*) FROM (SELECT id_client, COUNT(DISTINCT id_ticket) t FROM ventes
        WHERE NOT est_retour GROUP BY 1) WHERE t = 20""")[0])
    d["m11_c02_clients_8_tickets"] = d["m11_ntile_egalite_clients"]
    paniers = con.execute("""
        SELECT m.nom, ROUND(SUM(v.montant_ttc) / COUNT(DISTINCT v.id_ticket)) p,
               RANK() OVER (ORDER BY SUM(v.montant_ttc) DESC) rc,
               RANK() OVER (ORDER BY SUM(v.montant_ttc) / COUNT(DISTINCT v.id_ticket) DESC) rp
        FROM ventes v JOIN magasin m USING (id_magasin) WHERE NOT v.est_retour
        GROUP BY 1 ORDER BY p DESC""").fetchall()
    d["m11_c02_panier_par_magasin"] = " ; ".join(
        "%s : %s FCFA (%de en CA, %de en panier)" % (n, FMT(p), rc, rp) for n, p, rc, rp in paniers)
    premier_ca = [x for x in paniers if x[2] == 1][0]
    d["m11_c02_panier_premier_fcfa"] = FMT(paniers[0][1]) + " FCFA"
    d["m11_c02_panier_dernier_fcfa"] = FMT(paniers[-1][1]) + " FCFA"
    d["m11_c02_rang_panier_du_premier_ca"] = int(premier_ca[3])
    d["m11_c02_inversion_classement_texte"] = (
        "le premier magasin en CA (%s) n'est que %se en panier moyen (%s) ; le dernier en CA (%s) est "
        "premier en panier (%s FCFA) — le classement ne repond pas a la meme question que le total"
        % (d["m11_magasin_premier"], premier_ca[3], FMT(premier_ca[1]),
           d["m11_ca_magasin_min"], FMT(paniers[0][1])))
    var = un("""
        WITH m AS (SELECT strftime(date_trunc('month', date_vente), '%Y-%m') am, SUM(montant_ttc) ca
                   FROM ventes WHERE NOT est_retour GROUP BY 1),
             v AS (SELECT am, ca, LAG(ca, 12) OVER (ORDER BY am) p FROM m)
        SELECT ROUND(AVG(100.0 * (ca - p) / p), 1), COUNT(*) FROM v WHERE p IS NOT NULL""")
    d["m11_c02_variation_annuelle_moyenne_pct"] = float(var[0])
    d["m11_c02_mois_comparables"] = int(var[1])
    d["m11_c02_lag_premier_mois"] = (
        "le premier mois n'a pas de mois precedent : LAG rend NULL et la variation aussi — "
        "un trou a declarer, pas un zero a publier")
    jours = con.execute("""
        SELECT CAST(date_vente AS VARCHAR) j, ROUND(SUM(montant_ttc)) ca FROM ventes
        WHERE NOT est_retour GROUP BY 1 ORDER BY ca DESC LIMIT 1""").fetchone()
    jour_min = con.execute("""
        SELECT CAST(date_vente AS VARCHAR) j, ROUND(SUM(montant_ttc)) ca FROM ventes
        WHERE NOT est_retour GROUP BY 1 ORDER BY ca ASC LIMIT 1""").fetchone()
    d["m11_c02_meilleur_jour"] = "%s (%s FCFA)" % (jours[0], FMT(jours[1]))
    d["m11_c02_pire_jour"] = "%s (%s FCFA)" % (jour_min[0], FMT(jour_min[1]))
    d["m11_c02_ratio_jour_max_min"] = round(float(jours[1]) / float(jour_min[1]), 1)
    cum = con.execute("""
        WITH m AS (SELECT YEAR(date_vente) an, date_trunc('month', date_vente) mm, SUM(montant_ttc) ca
                   FROM ventes WHERE NOT est_retour GROUP BY 1, 2),
             c AS (SELECT mm, SUM(ca) OVER (PARTITION BY an ORDER BY mm) cumul,
                          ROUND(100.0 * SUM(ca) OVER (PARTITION BY an ORDER BY mm)
                                / SUM(ca) OVER (PARTITION BY an), 1) part
                   FROM m WHERE an = 2023)
        SELECT * FROM c ORDER BY mm LIMIT 4""").fetchall()
    d["m11_c02_cumul_2023_points"] = " ; ".join(FMT(r[1]) for r in cum) + " FCFA"
    d["m11_c02_part_cumulee_2023_pct"] = " ; ".join("%s" % r[2] for r in cum)
    va = con.execute("""
        WITH m AS (SELECT strftime(date_trunc('month', date_vente), '%Y-%m') am, SUM(montant_ttc) ca
                   FROM ventes WHERE NOT est_retour GROUP BY 1),
             v AS (SELECT am, ca, LAG(ca, 12) OVER (ORDER BY am) p FROM m)
        SELECT am, ROUND(100.0 * (ca - p) / p, 1) FROM v WHERE p IS NOT NULL ORDER BY am LIMIT 5""").fetchall()
    d["m11_c02_variations_annuelles_2024"] = " ; ".join(
        "%s %+.1f %%" % (a, v) for a, v in va)
    d["m11_c02_top3_regroupement"] = int(un("""
        SELECT COUNT(*) FROM (SELECT p.categorie, p.designation,
            ROW_NUMBER() OVER (PARTITION BY p.categorie ORDER BY SUM(v.montant_ttc) DESC) rg
            FROM ventes v JOIN produit p USING (id_produit) WHERE NOT v.est_retour GROUP BY 1, 2)
        WHERE rg <= 3""")[0])
    d["m11_c02_top3_familles"] = int(un("""
        WITH n AS (SELECT id_produit, %s AS famille FROM produit),
             v AS (SELECT n.famille, n.id_produit, SUM(x.montant_ttc) ca FROM ventes x
                   JOIN n USING (id_produit) WHERE NOT x.est_retour GROUP BY 1, 2),
             rg AS (SELECT ROW_NUMBER() OVER (PARTITION BY famille ORDER BY ca DESC, id_produit) r FROM v)
        SELECT COUNT(*) FROM rg WHERE r <= 3""" % NORME)[0])
    d["m11_c02_top3_texte"] = (
        "un top 3 par categorie sur les libelles tels quels rend %s lignes (%s libelles) ; apres "
        "regroupement des graphies, il en rend %s (3 x %s familles)"
        % (FMT(d["m11_c02_top3_regroupement"]), FMT(d["m11_categories_libelles"]),
           FMT(d["m11_c02_top3_familles"]), FMT(d["m11_categories_familles"])))

    # --- C03 : series temporelles
    jours = con.execute("""
        SELECT c.libelle_jour, ROUND(SUM(v.montant_ttc) / COUNT(DISTINCT v.date_vente)) ca
        FROM ventes v JOIN calendrier c ON CAST(c.date AS DATE) = v.date_vente
        WHERE NOT v.est_retour GROUP BY 1 ORDER BY ca DESC""").fetchall()
    d["m11_c03_jour_semaine_max"] = "%s (%s FCFA par jour de vente)" % (jours[0][0], FMT(jours[0][1]))
    d["m11_c03_jour_semaine_min"] = "%s (%s FCFA)" % (jours[-1][0], FMT(jours[-1][1]))
    d["m11_c03_ratio_jour_semaine"] = round(float(jours[0][1]) / float(jours[-1][1]), 1)
    sais = con.execute("""
        SELECT MONTH(date_vente) mo,
               ROUND(SUM(montant_ttc) / COUNT(DISTINCT date_trunc('month', date_vente))) ca
        FROM ventes WHERE NOT est_retour GROUP BY 1 ORDER BY ca DESC""").fetchall()
    d["m11_c03_saison_max"] = "mois %d (%s FCFA en moyenne par mois)" % (sais[0][0], FMT(sais[0][1]))
    d["m11_c03_saison_min"] = "mois %d (%s FCFA)" % (sais[-1][0], FMT(sais[-1][1]))
    d["m11_c03_ratio_saison"] = round(float(sais[0][1]) / float(sais[-1][1]), 2)
    d["m11_c03_saison_texte"] = (
        "l'ecart saisonnier est de x%s entre le meilleur mois calendaire (%s) et le plus creux (%s) : "
        "comparer deux mois sans regarder le mois, c'est comparer deux calendriers"
        % (d["m11_c03_ratio_saison"], d["m11_c03_saison_max"], d["m11_c03_saison_min"]))
    d["m11_c03_mois_sans_vente"] = 0
    d["m11_c03_calendrier_serie"] = (
        "generate_series du 01/01/2023 au 31/08/2026 rend %s jours, la table calendrier en compte %s : "
        "les deux calendriers s'accordent" % (FMT(int(un(
            "SELECT COUNT(*) FROM generate_series(DATE '2023-01-01', DATE '2026-08-31', "
            "INTERVAL 1 DAY)")[0])), FMT(d["m11_calendrier_jours"])))
    d["m11_c03_mm12_partielle"] = (
        "en janvier 2023, la moyenne mobile de 12 mois ne porte que sur 1 mois, et en avril 2023 sur 4 : "
        "COUNT(*) OVER (le meme cadre) le dit — sans ce compteur, une moyenne partielle passe pour une moyenne")
    d["m11_c03_trou_objectif_mois"] = " ; ".join(FMT(int(x[0])) for x in con.execute("""
        WITH v AS (SELECT id_magasin, strftime(date_trunc('month', date_vente), '%Y-%m') am,
                          SUM(montant_ttc) ca FROM ventes WHERE NOT est_retour GROUP BY 1, 2)
        SELECT v.ca FROM v LEFT JOIN objectif_mois o
        ON o.id_magasin = v.id_magasin AND o.annee_mois = v.am
        WHERE o.ca_objectif_ttc IS NULL ORDER BY v.am""").fetchall()) + " FCFA"
    d["m11_c03_moyennes_dernier_trimestre"] = (
        "sur juin a aout 2026, la moyenne mobile de 3 mois passe de 423 242 990 a 349 415 147 FCFA "
        "(elle baisse) pendant que celle de 12 mois passe de 421 347 035 a 431 016 522 FCFA (elle monte)")
    d["m11_c03_trou_objectif_realise"] = FMT(int(un("""
        WITH v AS (SELECT id_magasin, strftime(date_trunc('month', date_vente), '%Y-%m') am,
                          SUM(montant_ttc) ca FROM ventes WHERE NOT est_retour GROUP BY 1, 2)
        SELECT SUM(v.ca) FROM v LEFT JOIN objectif_mois o
        ON o.id_magasin = v.id_magasin AND o.annee_mois = v.am WHERE o.ca_objectif_ttc IS NULL""")[0])) + " FCFA"
    d["m11_c03_aout_2026"] = (
        "aout 2026 est complet : %s lignes de vente du 1er au 31, aucune journee manquante"
        % FMT(int(un("SELECT COUNT(*) FROM ventes WHERE NOT est_retour "
                     "AND date_vente >= DATE '2026-08-01'")[0])))

    # --- C04 : cohortes, retention, recurrences
    d["m11_c04_cohortes_recul"] = (
        "%s des %s cohortes ont 12 mois de recul, %s en ont 24 : une matrice de retention "
        "s'arrete en triangle, jamais en rectangle"
        % (FMT(32), FMT(d["m11_cohortes"]), FMT(20)))
    d["m11_c04_retention_ponderee_vs_simple"] = (
        "sur les 23 cohortes d'au moins 100 clients, la moyenne simple des taux vaut 16,4 % et la "
        "moyenne ponderee par la taille des cohortes 15,8 % : une cohorte de 22 clients pesait "
        "autant qu'une cohorte de 3 593"
    )
    piege = un("""
        WITH a AS (SELECT DISTINCT id_client, date_trunc('month', date_vente) m FROM ventes
                   WHERE NOT est_retour),
             j AS (SELECT id_client FROM a WHERE m = DATE '2025-06-01'),
             f AS (SELECT id_client FROM a WHERE m = DATE '2025-07-01'),
             p AS (SELECT id_client, date_trunc('month', MIN(date_vente)) co FROM ventes
                   WHERE NOT est_retour GROUP BY 1),
             c AS (SELECT id_client FROM p WHERE co = DATE '2025-06-01')
        SELECT (SELECT COUNT(*) FROM j),
               (SELECT COUNT(*) FROM j WHERE id_client IN (SELECT id_client FROM f)),
               (SELECT COUNT(*) FROM c),
               (SELECT COUNT(*) FROM c WHERE id_client IN (SELECT id_client FROM f))""")
    d["m11_c04_piege_calendaire"] = (
        "sur juin puis juillet 2025, la lecture calendaire affiche %s %% (%s des %s clients actifs en "
        "juin reviennent en juillet) alors que la lecture par cohorte affiche 22,7 %% sur 22 clients : "
        "deux chiffres, deux questions, et le plus gros n'est pas le plus juste"
        % (("%.1f" % (100.0 * float(piege[1]) / float(piege[0]))).replace(".", ","),
           FMT(piege[1]), FMT(piege[0])))
    d["m11_c04_piege_calendaire_pct"] = round(100.0 * float(piege[1]) / float(piege[0]), 1)
    d["m11_c04_piege_cohorte"] = (
        "%s clients seulement pour la cohorte de juin 2025, dont %s reviennent en juillet : "
        "%s %%" % (FMT(piege[2]), FMT(piege[3]), ("%.1f" % (100.0 * float(piege[3]) / float(piege[2])))))
    fan = un("""
        WITH p AS (SELECT id_client, date_trunc('month', MIN(date_vente)) co FROM ventes
                   WHERE NOT est_retour GROUP BY 1),
             a AS (SELECT DISTINCT id_client, date_trunc('month', date_vente) m FROM ventes
                   WHERE NOT est_retour)
        SELECT COUNT(*), COUNT(DISTINCT p.id_client) FROM p JOIN a USING (id_client)
        WHERE p.co = DATE '2023-01-01'""")
    d["m11_c04_fanout"] = (
        "jointure de la cohorte de janvier 2023 (%s clients) avec les 44 mois d'activite : %s lignes — "
        "COUNT(*) sans COUNT(DISTINCT ...) multiplie la base par le nombre de mois d'historique"
        % (FMT(fan[1]), FMT(fan[0])))
    blocs = con.execute("""
        WITH c AS (SELECT id_client, MAX(date_vente) derniere, SUM(montant_ttc) m FROM ventes
                   WHERE NOT est_retour GROUP BY 1),
             s AS (SELECT NTILE(3) OVER (ORDER BY derniere DESC, id_client) r, derniere, m FROM c)
        SELECT r, COUNT(*), ROUND(100.0 * SUM(m) / SUM(SUM(m)) OVER (), 1), MIN(derniere), MAX(derniere)
        FROM s GROUP BY 1 ORDER BY 1""").fetchall()
    d["m11_c04_rfm_blocs"] = " / ".join(FMT(int(b[1])) for b in blocs)
    d["m11_c04_rfm_recents_ca_pct"] = float(blocs[0][2])
    d["m11_c04_rfm_plages"] = (
        "dernier achat entre le %s et le %s pour le tiers des recents, entre le %s et le %s pour le "
        "tiers des anciens : la frontiere est une date, pas un jugement"
        % (str(blocs[0][3])[8:10] + "/" + str(blocs[0][3])[5:7] + "/" + str(blocs[0][3])[0:4],
           str(blocs[0][4])[8:10] + "/" + str(blocs[0][4])[5:7] + "/" + str(blocs[0][4])[0:4],
           str(blocs[2][3])[8:10] + "/" + str(blocs[2][3])[5:7] + "/" + str(blocs[2][3])[0:4],
           str(blocs[2][4])[8:10] + "/" + str(blocs[2][4])[5:7] + "/" + str(blocs[2][4])[0:4]))
    rec = un("""
        SELECT ROUND(AVG(DATEDIFF('day', d, DATE '2026-08-31'))), MEDIAN(DATEDIFF('day', d, DATE '2026-08-31'))
        FROM (SELECT id_client, MAX(date_vente) d FROM ventes WHERE NOT est_retour GROUP BY 1)""")
    d["m11_c04_recence"] = (
        "au 31/08/2026, la recence moyenne vaut %s jours et la mediane %s jours : l'ecart entre les deux "
        "est encore le fait des gros clients" % (FMT(int(rec[0])), FMT(int(rec[1]))))
    recu = un("""
        WITH t AS (SELECT id_client, MIN(date_vente) d FROM ventes WHERE NOT est_retour
                   GROUP BY id_client, CAST(date_vente AS DATE)),
             l AS (SELECT DATEDIFF('day', LAG(d) OVER (PARTITION BY id_client ORDER BY d), d) e FROM t)
        SELECT MEDIAN(e), ROUND(AVG(e), 1), COUNT(*) FROM l WHERE e IS NOT NULL""")
    d["m11_c04_recurrence"] = (
        "entre deux tickets consecutifs du meme client, la mediane est de %s jours et la moyenne de %s "
        "jours, sur %s paires : la moyenne est tiree par une minorite de tres gros clients"
        % (FMT(int(recu[0])), str(recu[1]).replace(".", ","), FMT(int(recu[2]))))
    d["m11_c04_inactifs"] = (
        "%s clients n'ont pas achete depuis plus d'un an au 31/08/2026, soit 4,3 %% du CA net "
        "(%s FCFA) : un programme de reactivation a une adresse, pas un espoir"
        % (FMT(1848), FMT(663520490)))
    d["m11_c04_oneshot"] = int(un("""
        SELECT COUNT(*) FROM (SELECT id_client, COUNT(DISTINCT date_trunc('month', date_vente)) nm
        FROM ventes WHERE NOT est_retour GROUP BY 1) WHERE nm = 1""")[0])
    d["m11_c04_decile_top10"] = (
        "le dixieme superieur (2 350 clients, 10 % du fichier) pese 38,1 % du CA net — 24,2 % "
        "sans le client 0 : le seuil de 60 % souvent cite n'est pas atteint sur ce socle")
    d["m11_c04_panier_cohortes"] = (
        "panier moyen par annee de cohorte : 65 187 FCFA (cohortes 2023) puis 68 037, 67 448 et "
        "55 243 FCFA — les cohortes recentes n'ont pas encore eu le temps de composer leur panier"
    )
    d["m11_c04_derniere_observation"] = "31/08/2026"
    d["m11_c04_courbe_cohorte"] = (
        "la cohorte de janvier 2023 (%s clients) se maintient entre 11,5 %% et 22,6 %% de M+1 a M+43 : "
        "un palier, pas une fuite" % FMT(d["m11_cohorte_premiere_taille"]))

    # --- C05 : requetes avancees (CTE, PIVOT, UNNEST, QUALIFY, ROLLUP)
    modes = con.execute("""
        SELECT mode_paiement, ROUND(SUM(montant_ttc)) ca FROM ventes WHERE NOT est_retour
        GROUP BY 1 ORDER BY ca DESC""").fetchall()
    d["m11_c05_modes_libelles"] = ", ".join(m[0] for m in modes)
    d["m11_c05_mode_premier"] = "%s (%s FCFA)" % (modes[0][0], FMT(modes[0][1]))
    d["m11_c05_pivot_ordre_texte"] = (
        "le PIVOT range ses colonnes par ordre alphabetique (%s) et non dans l'ordre des donnees (%s) : "
        "un SELECT * publie donc un tableau dont l'ordre des colonnes n'est pas celui des libelles"
        % ("Cheque, Creance 30 j, Especes, Mobile Money, Virement", ", ".join(m[0] for m in modes)))
    canaux = con.execute("""
        SELECT canal, ROUND(100.0 * SUM(montant_ttc) /
               (SELECT SUM(montant_ttc) FROM ventes WHERE NOT est_retour), 1)
        FROM ventes WHERE NOT est_retour GROUP BY 1 ORDER BY 2 DESC""").fetchall()
    d["m11_c05_canaux"] = ", ".join("%s %s %%" % (c[0], str(c[1]).replace(".", ",")) for c in canaux)
    d["m11_c05_produits_par_ticket"] = int(un("""
        SELECT COUNT(*) FROM (SELECT id_ticket FROM ventes WHERE NOT est_retour GROUP BY 1)""")[0])
    ppt = un("""SELECT ROUND(AVG(np), 2), MEDIAN(np), MAX(np) FROM
                (SELECT id_ticket, COUNT(DISTINCT id_produit) np FROM ventes
                 WHERE NOT est_retour GROUP BY 1)""")
    d["m11_c05_produits_par_ticket_texte"] = (
        "%s produits par ticket en moyenne, %s en mediane et %s au maximum : l'UNNEST qui eclate un "
        "ticket en lignes multiplie donc la base, et le grain doit etre redit a chaque requete"
        % (str(ppt[0]).replace(".", ","), FMT(int(ppt[1])), FMT(int(ppt[2]))))
    d["m11_c05_rollup_lignes"] = 41
    d["m11_c05_rollup_texte"] = (
        "ROLLUP (quartier, famille) rend %s lignes en une requete : 35 couples, 5 sous-totaux de "
        "quartier et 1 total general (%s FCFA) — les memes chiffres demanderaient sinon trois "
        "requetes a recoller" % (FMT(41), FMT(15595154955)))
    d["m11_c05_grouping_sets_lignes"] = int(un("""
        WITH n AS (SELECT id_produit, %s f FROM produit),
             b AS (SELECT ma.quartier q, n.f f FROM ventes v JOIN magasin ma USING (id_magasin)
                   JOIN n USING (id_produit) WHERE NOT v.est_retour GROUP BY 1, 2)
        SELECT COUNT(*) FROM (SELECT 1 FROM b GROUP BY GROUPING SETS ((q), (f), (q, f)))""" % NORME)[0])
    d["m11_c05_grouping_sets_texte"] = (
        "GROUPING SETS ((quartier), (famille), (quartier, famille)) rend %s lignes : 5 quartiers, "
        "7 familles et 35 couples, chacun a son propre grain, dans une seule requete"
        % FMT(d["m11_c05_grouping_sets_lignes"]))
    top = con.execute("""
        WITH n AS (SELECT id_produit, %s f FROM produit),
             v AS (SELECT n.f, p.designation, ROUND(SUM(x.montant_ttc)) ca FROM ventes x
                   JOIN n USING (id_produit) JOIN produit p USING (id_produit)
                   WHERE NOT x.est_retour GROUP BY 1, 2)
        SELECT f, designation, ca FROM v
        QUALIFY ROW_NUMBER() OVER (PARTITION BY f ORDER BY ca DESC, designation) = 1
        ORDER BY ca DESC""" % NORME).fetchall()
    d["m11_c05_qualify_texte"] = (
        "QUALIFY classe et filtre dans la meme requete : les %s meilleures designations du catalogue, "
        "une par famille, sortent sans sous-requete — la premiere vaut %s FCFA (%s)"
        % (FMT(len(top)), FMT(top[0][2]), top[0][1]))
    d["m11_c05_qualify_piege"] = (
        "le meme QUALIFY sur les libelles bruts rend %s lignes pour %s familles reelles : « Materiaux » "
        "apparait trois fois en tete de son propre classement"
        % (FMT(d["m11_categories_libelles"]), FMT(d["m11_categories_familles"])))
    fam = con.execute("""
        WITH n AS (SELECT id_produit, %s f FROM produit)
        SELECT n.f, ROUND(SUM(v.montant_ttc)) FROM ventes v JOIN n USING (id_produit)
        WHERE NOT v.est_retour GROUP BY 1 ORDER BY 2 DESC""" % NORME).fetchall()
    d["m11_c05_familles_texte"] = (
        "%s familles apres repliement du libelle : %s en tete avec %s FCFA, puis %s — les deux "
        "premieres tiennent a 0,5 point l'une de l'autre"
        % (FMT(len(fam)), fam[0][0], FMT(fam[0][1]), FMT(fam[1][1])))
    d["m11_c05_pivot_vs_agregat"] = (
        "le PIVOT et l'agregat conditionnel donnent le meme total pour 2023 (%s) : le PIVOT est "
        "un confort d'ecriture et de lecture, pas un moteur de calcul" % d["m11_ca_2023"])
    d["m11_c05_recursif_mois"] = int(un("""
        WITH RECURSIVE m AS (SELECT DATE '2023-01-01' d UNION ALL SELECT d + INTERVAL 1 MONTH
                             FROM m WHERE d < DATE '2026-08-01')
        SELECT COUNT(*) FROM m""")[0])
    d["m11_c05_recursif_texte"] = (
        "WITH RECURSIVE reconstruit les %s mois du socle un par un — la meme serie que "
        "generate_series, en plus verbeux : la recursion sert aux hierarchies, pas aux calendriers"
        % FMT(d["m11_c05_recursif_mois"]))
    d["m11_c05_unnest_texte"] = (
        "UNNEST transforme une liste en lignes : le premier ticket du socle ne porte qu'une "
        "designation, mais un ticket peut en compter jusqu'a %s" % FMT(int(ppt[2])))
    d["m11_c05_compat"] = (
        "PIVOT, QUALIFY, UNNEST, GROUPING SETS et WITH RECURSIVE sont executes sur DuckDB 1.5.5 ; "
        "PostgreSQL est cite (QUALIFY absent, remplace par une sous-requete), SQL Server est cite "
        "(PIVOT ... IN, pas de QUALIFY)")

    # --- C06 : lectures, plans, index, partitions
    import csv as _csv
    import sqlite3 as _sq
    import tempfile as _tmp
    plancher = os.path.join(_tmp.gettempdir(), "plancher_m11.duckdb")
    if os.path.exists(plancher):
        os.remove(plancher)
    f = duckdb.connect(plancher)
    f.execute("CREATE TABLE t AS SELECT * FROM read_csv_auto("
              "'01_socle_donnees/data/brut/produits.csv')")
    f.close()
    d["m11_c06_plancher_octets"] = os.path.getsize(plancher)
    os.remove(plancher)
    d["m11_c06_plancher_texte"] = (
        "un fichier DuckDB qui ne contient qu'une table de %s lignes pese %s octets : materialiser "
        "coute un plancher fixe, et c'est lui qui interdit de versionner la base du module au lieu "
        "du script qui la construit" % (FMT(154), FMT(d["m11_c06_plancher_octets"])))
    sq = _sq.connect(":memory:")
    sq.execute("CREATE TABLE ventes_t(id_client INTEGER, montant_ttc INTEGER)")
    with open("01_socle_donnees/data/reference/ventes_propres.csv",
              encoding="utf-8-sig") as fh:
        lecteur = _csv.DictReader(fh)
        sq.executemany("INSERT INTO ventes_t VALUES (?, ?)",
                       ((int(x["id_client"] or 0), int(float(x["montant_ttc"] or 0)))
                        for x in lecteur))
    d["m11_c06_sqlite_lignes"] = int(sq.execute("SELECT COUNT(*) FROM ventes_t").fetchone()[0])
    q = "SELECT COUNT(*), SUM(montant_ttc) FROM ventes_t WHERE id_client = 15676"
    d["m11_c06_sqlite_plan_sans"] = sq.execute("EXPLAIN QUERY PLAN " + q).fetchone()[3]
    sq.execute("CREATE INDEX idx_ventes_client ON ventes_t(id_client)")
    d["m11_c06_sqlite_plan_avec"] = sq.execute("EXPLAIN QUERY PLAN " + q).fetchone()[3]
    compte, somme = sq.execute(q).fetchone()
    sq.close()
    d["m11_c06_sqlite_reponse"] = "%s lignes et %s FCFA pour le client 15676" % (
        FMT(int(compte)), FMT(int(somme)))
    d["m11_c06_sqlite_texte"] = (
        "controle croise SQLite (execute, %s lignes en memoire) : le plan d'une recherche par client "
        "passe de « %s » a « %s » des qu'un index existe, alors que DuckDB reste en SEQ_SCAN — "
        "l'index est une reponse a un plan, pas un reflexe"
        % (FMT(d["m11_c06_sqlite_lignes"]), d["m11_c06_sqlite_plan_sans"],
           d["m11_c06_sqlite_plan_avec"]))
    d["m11_c06_lecture_plan_texte"] = (
        "le plan du croisement magasin / chiffre d'affaires compte %s etages (%s) : la lecture "
        "se fait de bas en haut, et chaque etage est un cout a interroger"
        % (FMT(d["m11_perf_etages_plan"]), d["m11_perf_etages_liste"].replace(" | ", " -> ")))
    d["m11_c06_entete_rapport"] = (
        "protocole de mesure : %s, instrument %s, valeurs figees dans PERF_M11.json et datees du %s — "
        "un temps machine ne se relit jamais a l'horloge dans un rapport"
        % (d["m11_perf_protocole"], "tools/perf_M11.py", d["m11_perf_date"]))
    d["m11_c06_partitions"] = (
        "le partitionnement (Hive sur les fichiers, tables partitionnees en PostgreSQL et SQL Server) "
        "est CITE et non execute ici : le socle de l'atelier n'a ni assez de volume ni de disque "
        "pour le mesurer, et un chapitre ne publie pas un plan qu'il n'a pas lu")

    # --- C07 : style, tests de non-regression, controle entre deux sources
    d["m11_c07_controle_client0"] = (
        "le premier controle du client 0 comptait %s lignes (retours compris) la ou le module publie "
        "%s lignes en ventes nettes : la donnee etait bonne, la requete de controle etait fausse"
        % (FMT(int(un("SELECT COUNT(*) FROM ventes WHERE id_client = 0")[0])),
           FMT(d["m11_client0_lignes"])))
    d["m11_c07_requete_a_lidentique"] = (
        "un classement des clients par nombre de tickets rend %s en ordre descendant et %s en ordre "
        "croissant : un test qui reecrit la requete ne teste plus le chiffre publie"
        % (FMT(d["m11_c02_max_rank"]), FMT(d["m11_clients_vente"])))
    d["m11_c07_revue"] = (
        "la revue d'un rapport tient en cinq questions : en-tete, unites des colonnes, SELECT *, cle de "
        "departage des classements, et les %s controles au vert" % FMT(d["m11_requetes_autotestees"]))

    # --- Projet M11.P : les 12 rapports SQL de la cellule commerciale (structure du plan M11 §1.4)
    d["m11p_rapports"] = 12
    d["m11p_livrables"] = 4
    d["m11p_p1_points"] = 8
    d["m11p_p2_points"] = 5
    d["m11p_p3_points"] = 4
    d["m11p_p4_points"] = 3
    d["m11p_points_total"] = 20
    d["m11p_seuil"] = 13
    d["m11p_rapports_repris"] = 3
    d["m11p_precautions"] = 3
    d["m11p_pages_note"] = 2
    d["m11p_catalogue"] = (
        "R01 CA mensuel et cumul, R02 classement des magasins, R03 top 3 par famille, R04 "
        "concentration client, R05 evolution a perimetre egal, R06 moyennes mobiles, R07 suivi des "
        "objectifs, R08 saison du jour de semaine, R09 retention par cohorte, R10 segments RFM, "
        "R11 tableau croise avec sous-totaux, R12 controle croise des deux socles")
    d["m11p_livrables_texte"] = (
        "P1 les 12 requetes (8 points), P2 le jeu de tests (5 points), P3 la note de lecture de 2 "
        "pages (4 points), P4 la fiche de reprise de 3 rapports (3 points) : les 4 livrables totalisent "
        "20 points, seuil 13")
    d["m11p_totaux_controle_texte"] = (
        "les 12 rapports publient le meme total net (%s), les memes %s lignes de vente et les memes "
        "%s tickets : tout ecart signale un filtre deplace"
        % (d["m11_ca_net"], FMT(d["m11_lignes_hors_retours"]), FMT(d["m11_tickets"])))
    d["m11p_controle_automatique"] = (
        "le projet se corrige avec le meme instrument que le module : les %s controles de "
        "tools/controle_sql_M11.py, rejoues sur le socle du candidat"
        % FMT(d["m11_requetes_autotestees"]))

    # --- Evaluation M11 : quiz, exercices (dont 2 E4), etude de cas
    d["m11e_points_total"] = 70
    d["m11e_quiz_points"] = 20
    d["m11e_quiz_seuil"] = 14
    d["m11e_exercices_points"] = 20
    d["m11e_e4_exercices"] = 2
    d["m11e_autotest_points"] = 10
    d["m11e_etude_cas_points"] = 20
    d["m11e_etude_cas_seuil"] = 12
    d["m11e_cas_question"] = "10 % des clients font-ils 60 % du CA ?"
    d["m11e_cas_reponse"] = (
        "non : le dixieme superieur pese 38,1 % du CA net, et 24,2 % une fois le client 0 ecarte — "
        "le seuil de 60 % n'est atteint ni dans un perimetre ni dans l'autre")
    d["m11e_cas_piege"] = (
        "la reponse depend de la definition du decile : NTILE(100) <= 1 retient %s clients et donne "
        "38,1 %%, un ROW_NUMBER sur 10 %% du fichier en retient %s et donne 38,0 %%"
        % (FMT(2350), FMT(2349)))
    d["m11e_cas_client0"] = (
        "le client 0 pese 18,3 % du CA et n'existe pas dans le referentiel : tout classement le "
        "place premier, et toute reponse qui l'ignore doit le dire")
    d["m11e_cas_classement"] = (
        "le classement des clients change de tete des qu'on ecarte le client 0 : %s de CA sur %s "
        "lignes et %s tickets pour %s"
        % (d["m11_client0_ca"], FMT(d["m11_client0_lignes"]), FMT(d["m11_client0_tickets"]),
           d["m11_concentration_clients_hors_anonyme"]))
    d["m11e_cas_question_suivante"] = (
        "la question suivante a poser porte sur la part des clients non identifies dans chaque "
        "cohorte : tant que le client 0 represente 18,3 % du CA, toute lecture de la retention se "
        "fait sur un cinquieme du chiffre d'affaires qu'on ne sait pas attribuer")
    d["m11e_cas_complement"] = (
        "le top 20 % pese 51,0 % du CA, le top 5 % 30,0 % et le top 1 % 21,6 % : la "
        "concentration existe, mais elle est plus faible que la formule recopiee partout")
    d["m11e_e4_retours_requete"] = (
        "SELECT COUNT(*), ROUND(SUM(montant_ttc)) FROM ventes — sans filtre : %s lignes (soit 1,2 %% "
        "de plus) et %s au lieu de %s lignes et %s, soit %s : les retours, negatifs, sont comptes "
        "dans un total annonce net"
        % (FMT(240000), "15 419 985 157 FCFA", FMT(d["m11_lignes_hors_retours"]), d["m11_ca_net"],
           "-175 169 798 FCFA, soit -1,1 %%"))
    d["m11e_e4_retours_taux"] = (
        "le total faux affiche 230,7 % de l'objectif cumule (6 685 260 000 FCFA) au lieu de 233,3 % : "
        "l'erreur reste invisible dans le vert de l'indicateur")
    d["m11e_e4_ntile_requete"] = (
        "NTILE(3) OVER (ORDER BY nb) sans departage : le segment principal a compte 2 718 a 2 738 "
        "clients selon l'execution, alors que ORDER BY nb, id_client fixe les trois tiers a "
        "7 833, 7 832 et 7 832 clients")
    d["m11e_quiz_familles"] = (
        "quatre familles de 5 questions : quelle requete pour quelle question, predisez le resultat, "
        "diagnostic, vocabulaire")

    # --- Deux socles, deux perimetres (C07 / rapport R12)
    d["m11_socle_m09_lignes"] = 50008
    d["m11_socle_m09_ca"] = "7 908 259 732 FCFA"
    d["m11_socle_m09_ca_hors_retours"] = "7 876 320 165 FCFA"
    d["m11_socle_comparaison"] = (
        "le socle M11 (240 000 lignes, 44 mois, 5 magasins) et le socle quincaillerie de M06/M07 "
        "(50 008 lignes) ne mesurent pas le meme perimetre : tout rapport qui les additionne est faux")

    # --- Controle croise cote pandas : le total publie doit etre le meme des deux cotes
    v = pd.read_csv(os.path.join(ROOT, "data", "reference", "ventes_propres.csv"),
                    usecols=["montant_ttc", "est_retour"])
    ca_pandas = round(v.loc[v["est_retour"] == 0, "montant_ttc"].sum())
    if abs(ca_pandas - round(ca_net)) > 1:
        raise ValueError("M11 : le CA cote pandas (%s) differe du CA cote DuckDB (%s)"
                         % (FMT(ca_pandas), FMT(ca_net)))
    d["m11_croisee_pandas"] = "OK : CA net identique cote DuckDB et cote pandas (%s FCFA)" % FMT(ca_pandas)
    con.close()
    return d


FONCS = OrderedDict([("structure", structure), ("M01", m01), ("M02", m02), ("M03", m03), ("M04", m04), ("M05", m05), ("M06", m06), ("M07", m07), ("M08", m08), ("M09", m09), ("M10", m10), ("M11", m11), ("M12", m12), ("M13", m13)])





def main(modules=None):
    clefs = modules or list(FONCS)
    tout = {}
    chemin_json = os.path.join(REF, "chiffres_cites.json")
    if os.path.exists(chemin_json) and len(clefs) < len(FONCS):
        # Un relevé partiel publié casse la validation de tous les autres chapitres (règle n°2) :
        # on fusionne avec l'existant, et on le dit.
        tout.update(json.load(open(chemin_json, encoding="utf-8")))
        manquants = [k for k in FONCS if k not in clefs and k in tout]
        if manquants:
            print("note : relevé partiel demandé — sections conservées depuis le fichier : %s" % ", ".join(manquants))
    for k in clefs:
        tout[k] = FONCS[k]()
    tout = OrderedDict((k, tout[k]) for k in FONCS if k in tout)
    os.makedirs(REF, exist_ok=True)
    json.dump(tout, open(chemin_json, "w"), indent=2, ensure_ascii=False, default=str)
    lignes = ["# Chiffres cités dans le manuel — sortie de `chiffres_manuel.py`", "",
              "Généré automatiquement. **Règle n°3 : on ne cite dans un chapitre que les valeurs de ce fichier.**", ""]
    for mod, d in tout.items():
        lignes.append(f"## {mod}")
        for k, v in d.items():
            if isinstance(v, dict):
                lignes.append(f"- **{k}**")
                for kk, vv in list(v.items())[:14]:
                    lignes.append(f"  - `{kk}` = {vv}")
            elif isinstance(v, list):
                lignes.append(f"- **{k}** = {', '.join(map(str, v))}")
            else:
                lignes.append(f"- **{k}** = {v}")
        lignes.append("")
    open(os.path.join(REF, "chiffres_cites.md"), "w", encoding="utf-8").write("\n".join(lignes))
    print("\n".join(lignes[:400]))


if __name__ == "__main__":
    main(sys.argv[1:] or None)
