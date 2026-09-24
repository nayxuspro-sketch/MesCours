#!/usr/bin/env python3
"""dossier_M04.py — le « dossier pourri » du projet M04.P, généré de façon déterministe.

Le dossier vit dans 03_exercices/dossier_M04/ (zone exercices, pas data/ : la zone de données
reste celle que le C06 décrit). Sept défauts de natures différentes, dont deux qui cassent les
totaux (montants en texte ; lignes en doublon). ATTENDU.json est MESURÉ sur le dossier généré,
pas déduit : c'est la règle 1 de la fiche M03, appliquée au projet.

Usage : python3 tools/dossier_M04.py
"""
import json
import os
import random

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(RACINE, "01_socle_donnees", "data", "reference")
DST = os.path.join(RACINE, "03_exercices", "dossier_M04")
SEED = 41
N_LIGNES = 150
N_TXT = 14
N_RETOURS = 2
N_DUP = 8
N_REM = 5
N_DAT = 12


def main():
    import pandas as pd

    r = random.Random(SEED)
    propres = pd.read_csv(os.path.join(SRC, "ventes_propres.csv"), dtype=str, keep_default_na=False)
    cli = pd.read_csv(os.path.join(SRC, "clients_propres.csv"), dtype=str, keep_default_na=False)
    pro = pd.read_csv(os.path.join(SRC, "dictionnaire_produits.csv"), dtype=str, keep_default_na=False)
    os.makedirs(DST, exist_ok=True)

    base = propres[propres["id_magasin"] == "1"].head(N_LIGNES).reset_index(drop=True).copy()
    for col in ("montant_ht", "montant_tva", "montant_ttc"):
        base[col] = base[col].astype(float).astype(int).astype(str)
    id_max = int(base["id_vente"].max())

    # ---- défaut 1 : montants en texte (cassent le total) — 14 lignes, « n nnn FCFA »
    idx_txt = r.sample(range(len(base)), N_TXT)
    base["montant_ttc"] = base["montant_ttc"].astype(object)
    for i in idx_txt:
        v = int(base.loc[i, "montant_ttc"])
        signe = "-" if v < 0 else ""
        base.loc[i, "montant_ttc"] = f"{signe}{abs(v):,}".replace(",", " ") + " FCFA"

    # ---- défaut (retours) : 2 lignes de retour ajoutées, montant en texte — le contrôle
    #      « retour = montant négatif » ne passe qu'après conversion, comme dans le socle
    sel = base[base["quantite"].astype(int) > 0].head(N_RETOURS).copy().reset_index(drop=True)
    for k in range(N_RETOURS):
        sel.loc[k, "id_vente"] = str(id_max + 1 + k)
        sel.loc[k, "quantite"] = str(-int(sel.loc[k, "quantite"]))
        for col in ("montant_ht", "montant_tva"):
            sel.loc[k, col] = str(-int(sel.loc[k, col]))
        v = -int(base.loc[sel.index[k], "montant_ttc"])
        sel.loc[k, "montant_ttc"] = f"-{abs(v):,}".replace(",", " ") + " FCFA"
        sel.loc[k, "est_retour"] = "1"
    base = pd.concat([base, sel], ignore_index=True).reset_index(drop=True)

    # ---- défaut 2 : lignes en doublon (cassent le total) — 8 copies exactes, id_vente neuf
    idx_dup = r.sample(range(N_LIGNES), N_DUP)
    dup = base.loc[idx_dup].copy()
    dup["id_vente"] = [str(id_max + N_RETOURS + 1 + k) for k in range(N_DUP)]
    base = pd.concat([base, dup], ignore_index=True)

    # ---- défaut 3 : remises en points de pourcentage (5 lignes, valeurs 12/18/25/30/18)
    base["taux_remise"] = base["taux_remise"].astype(object)
    base.loc[r.sample(range(len(base)), N_REM), "taux_remise"] = ["12.0", "18.0", "25.0", "30.0", "18.0"]

    # ---- défaut 4 : dates en deux écritures (12 lignes passées en JJ/MM/AAAA)
    base["date_vente"] = base["date_vente"].astype(object)
    for i in r.sample(range(len(base)), N_DAT):
        y, m, d = base.loc[i, "date_vente"].split("-")
        base.loc[i, "date_vente"] = f"{int(d):02d}/{int(m):02d}/{y}"

    # ---- défaut 5 (hérité, assumé) : ventes au comptoir, id_client = 0 — rien à corriger,
    #      une convention à documenter (le C02 l'a nommé)
    cols = ["id_vente", "id_ticket", "date_vente", "heure", "id_magasin", "id_vendeur", "id_client",
            "id_produit", "quantite", "prix_unitaire_ht", "taux_remise", "montant_ht", "montant_tva",
            "montant_ttc", "mode_paiement", "canal", "est_retour", "poids_kg", "mois", "annee"]
    base[cols].to_csv(os.path.join(DST, "commandes_2026.csv"), index=False, encoding="utf-8-sig")

    # ---- défaut 6 : clients — 2 quasi-doublons (nom surchargé + téléphone sans espaces) et
    #      au moins une paire d'homonymes (même nom, téléphones distincts)
    ids_utilises = set(base.loc[base["id_client"] != "0", "id_client"])
    ccli = cli[cli["id_client"].isin(ids_utilises)].reset_index(drop=True)
    jumeaux = ccli.head(2).copy()
    jumeaux["id_client"] = ["900010", "900011"]
    jumeaux["nom"] = [f"  {n.upper()} " for n in jumeaux["nom"]]
    jumeaux["telephone"] = jumeaux["telephone"].str.replace(r"\s", "", regex=True)
    hon = ccli.assign(_n=lambda d: d["nom"].str.strip().str.lower()).groupby("_n")["telephone"].nunique()
    if int((hon >= 2).sum()) < 1:
        src2 = ccli.head(2).copy()
        src2["id_client"] = ["900001", "900002"]
        src2["nom"] = ["ETS SA", "ETS SA"]
        src2["telephone"] = ["+226 70 11 22 33 44", "+226 70 55 66 77 88"]
        src2["email"] = ["", ""]
        ccli = pd.concat([ccli, src2], ignore_index=True)
    ccli = pd.concat([ccli, jumeaux], ignore_index=True)
    ccli.to_csv(os.path.join(DST, "clients_2026.csv"), index=False, encoding="utf-8-sig")

    # ---- défaut 7 : tarif fournisseur — cp1252, point-virgule, 3 lignes de bruit, virgule décimale
    prods = pro[pro["id_produit"].isin(set(base["id_produit"]))].head(10)
    lignes = ["export genere depuis ELODIE v3", "edition le 17/09/2026", "peinture saaba sarl \u2014 tarif 2026",
              "code_article;libelle;conditionnement;prix_unitaire;unite_mesure;tva"]
    for _, p in prods.iterrows():
        prix = float(p["prix_vente_ht"])
        s = f"{prix:.2f}".replace(".", ",")
        lignes.append(f"T-{p['id_produit']};{p['designation']} \u2014 r\u00e9f {p['reference_fournisseur']};"
                      f"{p['unite']} 25 kg;{s};{p['unite']};0,18")
    open(os.path.join(DST, "tarif_fournisseur.csv"), "w", encoding="cp1252").write("\n".join(lignes) + "\n")

    # ---------------- ATTENDU : mesuré sur le dossier généré, jamais déduit ----------------
    # règle de garde (celle que le projet doit trouver) : retirer les copies exactes
    # (2e occurrence du même contenu), puis les « resaisies » : lignes jumelles qui ne diffèrent
    # que d'un seul champ et portent la plus grande id_vente. Les multi-lignes légitimes
    # (deux champs ou plus différents : heure, client, prix) survivent.
    gen = pd.read_csv(os.path.join(DST, "commandes_2026.csv"), dtype=str, keep_default_na=False)
    brut_num = pd.to_numeric(gen["montant_ttc"], errors="coerce")
    net_num = pd.to_numeric(gen["montant_ttc"].str.replace(" FCFA", "", regex=False)
                            .str.replace(" ", "", regex=False), errors="coerce")
    g19 = gen.drop(columns=["id_vente"])
    copie = g19.duplicated(keep="first")
    tri = gen.assign(_i=pd.to_numeric(gen["id_vente"])).sort_values("_i").reset_index(drop=True)
    resaisie, legitemes = [], []
    for k, z in tri.groupby(["id_ticket", "id_produit", "quantite"]):
        if len(z) < 2:
            continue
        nz = z.drop(columns=["id_vente", "_i"])
        if nz.drop_duplicates().shape[0] == 1:
            continue  # copies exactes : gérées ci-dessus
        colonnes_diff = [c for c in nz.columns if nz[c].nunique() > 1]
        if len(colonnes_diff) == 1:
            resaisie.append(str(z["id_vente"].iloc[-1]))
        else:
            legitemes.append(len(z))
    # le retrait se fait par id_vente (jamais par position)
    a_retirer = set(gen.loc[copie, "id_vente"]) | set(resaisie)
    garde = gen[~gen["id_vente"].isin(a_retirer)]
    grp = gen.groupby(["id_ticket", "id_produit", "quantite"])
    attendu = {
        "lignes_brutes": int(len(gen)),
        "lignes_doublon_a_retirer": int(len(a_retirer)),
        "lignes_doublon_copies_exactes": int(copie.sum()),
        "lignes_doublon_resaisie": int(len(resaisie)),
        "lignes_attendues": int(len(garde)),
        "groupes_en_collision": int((grp.size() > 1).sum()),
        "groupes_multilignes_legitimes": int(len(legitemes)),
        "lignes_multilignes_legitimes": int(sum(legitemes)),
        "montants_en_texte": int((brut_num.isna() & (gen["montant_ttc"].str.strip() != "")).sum()),
        "montants_negatifs_texte": int(gen["montant_ttc"].str.strip().str.startswith("-").sum()),
        "retours_montant_non_numerique": int((gen["est_retour"] == "1").mul(brut_num.isna()).sum()),
        "remises_hors_domaine": int((pd.to_numeric(gen["taux_remise"], errors="coerce") > 1).sum()),
        "dates_hors_iso": int((~gen["date_vente"].str.match(r"^\d{4}-\d{2}-\d{2}$")).sum()),
        "lignes_comptoir_id_0": int((gen["id_client"] == "0").sum()),
        "total_ttc_repare": int(round(float(net_num[gen["id_vente"].isin(set(garde["id_vente"]))].sum()))),
    }
    ccli = pd.read_csv(os.path.join(DST, "clients_2026.csv"), dtype=str, keep_default_na=False)
    cc = ccli.assign(_n=ccli["nom"].str.strip().str.lower(),
                     _d=ccli["telephone"].str.replace(r"\D", "", regex=True))
    attendu["clients_bruts"] = int(len(ccli))
    attendu["clients_attendus"] = int(cc.groupby(["_n", "_d"]).ngroups)
    attendu["quasi_doublons_clients"] = int(len(ccli) - attendu["clients_attendus"])
    attendu["paires_homonymes_clients"] = int((cc.groupby("_n")["_d"].nunique() >= 2).sum())
    t = pd.read_csv(os.path.join(DST, "tarif_fournisseur.csv"), sep=";", dtype=str,
                    keep_default_na=False, encoding="cp1252", skiprows=3)
    attendu["tarif_lignes_utiles"] = int(len(t))
    attendu["tarif_prix_virgule"] = int(t["prix_unitaire"].str.contains(",").sum())
    attendu["tarif_lignes_bruit_avant_en_tete"] = 3
    # la règle naïve (une ligne par groupe, plus petit id_vente) mange le groupe légitime :
    # les deux chiffres sont publiés pour que le projet puisse les opposer sans les dériver
    naive = (gen.assign(_i=pd.to_numeric(gen["id_vente"])).sort_values("_i")
             .drop_duplicates(["id_ticket", "id_produit", "quantite"], keep="first"))
    attendu["lignes_regle_naive"] = int(len(naive))
    attendu["total_regle_naive"] = int(round(float(
        net_num[gen["id_vente"].isin(set(naive["id_vente"]))].sum())))
    attendu["montant_ligne_legitime_mangee"] = attendu["total_ttc_repare"] - attendu["total_regle_naive"]
    json.dump(attendu, open(os.path.join(DST, "ATTENDU.json"), "w"), indent=2, ensure_ascii=False)
    print(json.dumps(attendu, indent=2, ensure_ascii=False))
    print("dossier ->", DST)


if __name__ == "__main__":
    main()
