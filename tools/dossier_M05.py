#!/usr/bin/env python3
"""dossier_M05.py — le dossier du projet M05.P « Trois chemins, une même table propre ».

Généré de façon déterministe (même graine = même dossier) depuis les fichiers LIVRÉS du socle
(jamais régénéré) :
  - ventes_2023_2024.csv  : les 120 000 premières lignes du brut livré + 1 680 copies exactes
                            ressaisies + 40 resaisies à la date + 1 jour ;
  - remises_2023_2024.xlsx : sous-ensemble ≤ 2024 de remises_manuelles.xlsx, 35 couples en double
                            (ressaisie de l'assistante) et 2 lignes de chapeau avant l'en-tête ;
  - clients.csv           : les 23 500 clients propres, écrits en cp1252.

ATTENDU.json est MESURÉ sur le dossier écrit, jamais déduit du plan d'injection (règle 1 de la
fiche M03, leçon du point 12 de M04.C01). La spécification `df_final` (22 colonnes) est vérifiée
par DEUX moteurs indépendants (pandas puis DuckDB) : mêmes lignes, mêmes sommes, même empreinte
SHA-256, sinon le générateur échoue bruyamment.

Usage : python3 tools/dossier_M05.py
"""
import hashlib
import json
import os
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRUT = os.path.join(RACINE, "01_socle_donnees", "data", "brut")
REF = os.path.join(RACINE, "01_socle_donnees", "data", "reference")
DST = os.path.join(RACINE, "03_exercices", "dossier_M05")

SEED = 42
N_FENETRE = 120_000      # les 120 000 premières lignes du brut livré
N_DUP = 1_680            # copies exactes ressaisies (densité du brut : 1,4 %)
K_DATE = 40              # resaisies à la date + 1 jour
P_REM = 35               # couples (client, annee, mois) ressaisis dans le xlsx de remises
ID_DEPART_COPIES = 300_001  # au-dessus du maximum du brut (243 360)

# la spécification `df_final` : ordre imposé des 22 colonnes (l'énoncé le répète)
COLS_FINAL = ["id_vente", "id_ticket", "date_vente", "heure", "id_magasin", "id_vendeur",
              "id_client", "id_produit", "quantite", "prix_unitaire_ht", "taux_remise",
              "montant_ht", "montant_tva", "montant_ttc", "mode_paiement", "canal",
              "est_retour", "poids_kg", "mois", "annee", "remise_consentie_montant", "ville"]

# la clé métier du dédoublonnage : la ligne ignorée de son id et de sa date porte l'heure
# (les 3 groupes intra-ticket légitimes de la fenêtre ont des heures différentes ; les copies
# exactes et les resaisies à la date ont la même heure)
CLE_DEDUP = ["id_ticket", "id_produit", "quantite", "montant_ttc", "heure"]


def main():
    import numpy as np
    import pandas as pd

    g = np.random.default_rng(SEED)
    os.makedirs(DST, exist_ok=True)

    b = pd.read_csv(os.path.join(BRUT, "ventes_brutes.csv"), dtype=str, keep_default_na=False,
                    encoding="utf-8-sig")
    x = pd.read_excel(os.path.join(BRUT, "remises_manuelles.xlsx"), engine="openpyxl")
    cli = pd.read_csv(os.path.join(REF, "clients_propres.csv"), dtype=str, keep_default_na=False)
    assert len(b) == 243_360, f"brut : {len(b)} lignes au lieu de 243 360"
    assert len(cli) == 23_500, f"clients propres : {len(cli)} au lieu de 23 500"

    # ---------------- fenêtre du projet : les 120 000 premières lignes du brut livré ----------------
    w = b.iloc[:N_FENETRE].reset_index(drop=True).copy()
    d_w = pd.to_datetime(w["date_vente"])
    inco0 = d_w.dt.month != w["mois"].astype(int)
    n_inco0 = int(inco0.sum())
    assert bool(((d_w[inco0].dt.year == w.loc[inco0, "annee"].astype(int))).all()), \
        "date incohérente dont l'année ne colle pas à la colonne annee"
    # la clé métier est propre dans la fenêtre (sinon le dédoublonnage mangerait des lignes légitimes)
    assert int(w.duplicated(CLE_DEDUP, keep=False).sum()) == 0, \
        "clé métier non unique dans la fenêtre : la spécification de dédoublonnage est cassée"

    # ---- défaut 2 : N copies exactes ressaisies (id_vente neuf, ajoutées en fin de fichier)
    pool = np.arange(N_FENETRE)
    src_dup = g.choice(pool, size=N_DUP, replace=False)
    src_dup = np.sort(src_dup)

    # ---- défaut 3 : K resaisies à la date + 1 jour (jamais sur le 31/12 : la ressaisie ne
    #      traverse pas l'année) ; mois/annee recalculés depuis la nouvelle date, comme le ferait
    #      le système de caisse
    pool_k = np.setdiff1d(pool, src_dup)
    fin_dec = w["date_vente"].to_numpy() == "2023-12-31"
    pool_k = pool_k[~fin_dec[pool_k]]
    src_date = np.sort(g.choice(pool_k, size=K_DATE, replace=False))

    copies = w.loc[src_dup].copy()
    copies["id_vente"] = [str(ID_DEPART_COPIES + i) for i in range(len(copies))]
    resaisies = w.loc[src_date].copy()
    resaisies["id_vente"] = [str(ID_DEPART_COPIES + N_DUP + i) for i in range(len(resaisies))]
    nd = pd.to_datetime(resaisies["date_vente"]) + pd.Timedelta(days=1)
    resaisies["date_vente"] = nd.dt.strftime("%Y-%m-%d")
    resaisies["mois"] = nd.dt.month.astype(str)
    resaisies["annee"] = nd.dt.year.astype(str)

    ventes = pd.concat([w, copies, resaisies], ignore_index=True)
    ventes.to_csv(os.path.join(DST, "ventes_2023_2024.csv"), index=False, encoding="utf-8-sig")

    # ---------------- défauts 6 et 7 : remises — 35 couples en double + 2 lignes de chapeau ----------------
    xr = x[x["annee"] <= 2024].reset_index(drop=True).copy()
    assert len(xr) == 9_907, f"remises ≤ 2024 : {len(xr)} au lieu de 9 907"
    src_p = np.sort(g.choice(len(xr), size=P_REM, replace=False))
    xr = pd.concat([xr, xr.loc[src_p]], ignore_index=True)
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Remises"
    ws.append(["Suivi des remises consenties — Sahel Distribution"])
    ws.append(["édition du 05/01/2025 — assistante commerciale"])
    ws.append(list(xr.columns))
    for row in xr.itertuples(index=False):
        ws.append(list(row))
    wb.save(os.path.join(DST, "remises_2023_2024.xlsx"))

    # ---------------- défaut 8 : clients écrits en cp1252 ----------------
    cli.to_csv(os.path.join(DST, "clients.csv"), index=False, encoding="cp1252")

    # ---------------- ATTENDU : la spécification df_final, mesurée sur le dossier ÉCRIT ----------------
    gen = pd.read_csv(os.path.join(DST, "ventes_2023_2024.csv"), dtype=str, keep_default_na=False,
                      encoding="utf-8-sig")
    xr2 = pd.read_excel(os.path.join(DST, "remises_2023_2024.xlsx"), engine="openpyxl",
                        sheet_name="Remises", skiprows=2)
    cl2 = pd.read_csv(os.path.join(DST, "clients.csv"), dtype=str, keep_default_na=False,
                      encoding="cp1252")

    # moteur A : pandas
    fin_pd = spec_pandas(gen, xr2, cl2)
    assert len(fin_pd) == N_FENETRE, f"df_final : {len(fin_pd)} lignes au lieu de {N_FENETRE}"
    empreinte_pd = empreinte(fin_pd)
    sommes_pd = {c: int(pd.to_numeric(fin_pd[c]).sum()) for c in
                 ("quantite", "prix_unitaire_ht", "montant_ht", "montant_tva", "montant_ttc")}
    total_remise_pd = int(fin_pd["remise_consentie_montant"].sum())

    # moteur B : DuckDB (relit les fichiers du disque ; le xlsx passe par son export CSV,
    # qui est exactement ce que fait l'apprenant avant d'ouvrir la requête)
    tmp = tempfile.mkdtemp(prefix="m05p_")
    try:
        # l'export CSV du xlsx, avec le chapeau, comme un « enregistrer sous CSV » d'Excel le ferait
        lignes = ["Suivi des remises consenties — Sahel Distribution",
                  "édition du 05/01/2025 — assistante commerciale",
                  ",".join(xr2.columns)]
        for row in xr2.itertuples(index=False):
            lignes.append(",".join(str(v) for v in row))
        open(os.path.join(tmp, "remises_export.csv"), "w", encoding="utf-8").write("\n".join(lignes) + "\n")
        empreinte_dd, n_dd, sommes_dd, total_remise_dd = spec_duckdb(tmp)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)

    if (n_dd, empreinte_dd, sommes_dd, total_remise_dd) != (
            N_FENETRE, empreinte_pd, sommes_pd, total_remise_pd):
        raise SystemExit(
            "DIVERGENCE DE MOTEURS pandas/duckdb — la spécification n'est pas unique :\n"
            f"  pandas  : {N_FENETRE} lignes, empreinte {empreinte_pd[:16]}…,\n"
            f"            sommes {sommes_pd}, remises {total_remise_pd}\n"
            f"  duckdb  : {n_dd} lignes, empreinte {empreinte_dd[:16]}…,\n"
            f"            sommes {sommes_dd}, remises {total_remise_dd}")

    # ---------------- les pièges mesurés (pour le corrigé, jamais dérivés à chaud) ----------------
    ttc_num = pd.to_numeric(gen["montant_ttc"].str.replace(" FCFA", "", regex=False)
                            .str.replace(" ", "", regex=False), errors="coerce")
    total_avant_dedup = int(round(ttc_num.sum()))
    total_sans_retours = int(sommes_pd["montant_ttc"] - int(
        fin_pd.loc[fin_pd["est_retour"] == "1", "montant_ttc"].sum()))
    # jointures sur les ventes de la fenêtre, types alignés en str comme dans le fichier
    vm = gen.iloc[:120_000]
    vm = vm[vm["id_client"].astype(int) > 0].copy()
    xr_s = xr2.assign(id_client=xr2["id_client"].astype(str),
                      annee=xr2["annee"].astype(str), mois=xr2["mois"].astype(str))
    xr_d = xr_s.drop_duplicates(subset=["id_client", "annee", "mois"])
    # jointure naïve sur id_client seul : chaque ligne de vente × tous les mois du client
    lignes_naive = int(len(vm.merge(xr_d[["id_client", "annee", "mois"]],
                                    left_on="id_client", right_on="id_client", how="inner")))
    # clé complète : avec et sans dédoublonnage préalable des remises
    cle_complette = int(len(vm.merge(xr_s.drop_duplicates(
        subset=["id_client", "annee", "mois"])[["id_client", "annee", "mois"]],
        on=["id_client", "annee", "mois"], how="inner")))
    cle_complette_brute = int(len(vm.merge(xr_s[["id_client", "annee", "mois"]],
                                           on=["id_client", "annee", "mois"], how="inner")))
    # la règle naïve de M04 (clé sans l'heure) : elle mange des lignes légitimes
    naive4 = (gen.drop_duplicates(["id_ticket", "id_produit", "quantite", "montant_ttc"],
                                  keep="first"))
    mangées = set(gen["id_vente"]) - set(naive4["id_vente"]) - set(
        gen.loc[gen.duplicated(CLE_DEDUP, keep=False), "id_vente"])

    attendu = {
        # le fichier de ventes
        "ventes_lignes_brutes": int(len(gen)),
        "ventes_lignes_fenetre": N_FENETRE,
        "ventes_copies_ressaisies": N_DUP,
        "ventes_resaisies_date": K_DATE,
        "montants_en_texte": int((~gen["montant_ttc"].str.match(r"^-?\d+$")).sum()),
        "remises_hors_domaine": int((pd.to_numeric(gen["taux_remise"], errors="coerce") > 1).sum()),
        "clients_inconnus": int((gen["id_client"].astype(int) >= 900_000).sum()),
        "retours": int((gen["est_retour"] == "1").sum()),
        "doublons_a_retirer": int(gen.duplicated(CLE_DEDUP, keep="first").sum()),
        "dates_transposees_reparees": int(inco0.sum()),
        "lignes_final": N_FENETRE,
        "total_ttc_final": int(sommes_pd["montant_ttc"]),
        "total_ttc_avant_dedoublonnage": total_avant_dedup,
        "total_ttc_sans_retours": total_sans_retours,
        "total_quantite_final": int(sommes_pd["quantite"]),
        "total_montant_ht_final": int(sommes_pd["montant_ht"]),
        "total_montant_tva_final": int(sommes_pd["montant_tva"]),
        # le xlsx de remises
        "remises_lignes_brutes": int(len(xr2)),
        "remises_couples_ressaisis": int(xr2.duplicated(subset=["id_client", "annee", "mois"],
                                                        keep="first").sum()),
        "remises_lignes_apres_dedoublonnage": int(xr2.drop_duplicates(
            subset=["id_client", "annee", "mois"]).shape[0]),
        "remises_lignes_chapeau_avant_en_tete": 2,
        "ventes_enrichies_lignes": int(fin_pd["remise_consentie_montant"].notna().sum()),
        "total_remise_consentie": int(total_remise_pd),
        "lignes_jointure_cle_complette": cle_complette,
        "lignes_jointure_cle_complette_sans_dedoublonnage": cle_complette_brute,
        "lignes_jointure_naive_id_client": lignes_naive,
        # les fichiers de référence
        "clients_lignes": int(len(cl2)),
        "clients_caracteres_hors_ascii": int(sum(
            len([ch for ch in v if ord(ch) > 127]) for col in ("nom", "ville", "region")
            for v in cl2[col].tolist())),
        "ventes_ville_nulle": int(fin_pd["ville"].isna().sum()),
        # la règle naïve de M04, version fenêtre : elle retire des lignes légitimes
        "lignes_legitimes_mangees_cle_sans_heure": int(len(mangées)),
        # le contrôle automatisé du livrable
        "empreinte_sha256": empreinte_pd,
    }
    json.dump(attendu, open(os.path.join(DST, "ATTENDU.json"), "w"), indent=2, ensure_ascii=False)
    print(json.dumps(attendu, indent=2, ensure_ascii=False))
    print("moteurs pandas/duckdb : mêmes lignes, mêmes sommes, même empreinte — OK")
    print("dossier ->", DST)


# ---------------------------------------------------------------- la spécification, moteur A
def spec_pandas(gen, xr2, cl2):
    """df_final à partir des fichiers lus (pandas). Renvoie (table, compteurs)."""
    import pandas as pd

    df = gen.copy()
    df["montant_ttc"] = pd.to_numeric(
        df["montant_ttc"].str.replace(" FCFA", "", regex=False).str.replace(" ", "", regex=False),
        errors="raise").astype("int64")
    df = (df.assign(_i=df["id_vente"].astype("int64"))
          .sort_values("_i", kind="mergesort")
          .drop_duplicates(CLE_DEDUP, keep="first")
          .drop(columns="_i"))
    # réparation des dates transposées : le mois de la date ne colle pas à la colonne mois
    d = pd.to_datetime(df["date_vente"])
    i = d.dt.month != df["mois"].astype("int64")
    ds = d[i]
    df.loc[i, "date_vente"] = (ds.dt.year.astype(str) + "-" + ds.dt.day.astype(str).str.zfill(2)
                               + "-" + ds.dt.month.astype(str).str.zfill(2))
    assert int((pd.to_datetime(df["date_vente"]).dt.month
                == df["mois"].astype("int64")).all())

    rem = (xr2.drop_duplicates(subset=["id_client", "annee", "mois"])
           [["id_client", "annee", "mois", "remise_consentie_montant"]].copy())
    rem["id_client"] = rem["id_client"].astype(str)
    rem["annee"] = rem["annee"].astype(str)
    rem["mois"] = rem["mois"].astype(str)
    df = df.merge(rem, on=["id_client", "annee", "mois"], how="left")
    # le merge gauche fait flotter la colonne (NaN → float) : on la fige en entier nullable,
    # c'est la convention du livrable (entier, ou vide)
    df["remise_consentie_montant"] = df["remise_consentie_montant"].astype("Int64")
    df = df.merge(cl2[["id_client", "ville"]], on="id_client", how="left")
    df = df[COLS_FINAL]
    return df


def empreinte(df):
    import pandas as pd
    lignes = []
    for r in df.itertuples(index=False):
        lignes.append("|".join("" if pd.isna(v) else str(v) for v in r))
    return hashlib.sha256("\n".join(lignes).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- la spécification, moteur B
def spec_duckdb(tmp):
    """La même spécification en SQL sur DuckDB. Renvoie (empreinte, lignes, sommes, remises)."""
    import duckdb

    rac = os.path.join(RACINE)
    con = duckdb.connect()
    con.execute("CREATE TABLE v AS SELECT * FROM read_csv(?, all_varchar=true)",
                [os.path.join(rac, "03_exercices/dossier_M05/ventes_2023_2024.csv")])
    con.execute("CREATE TABLE r AS SELECT * FROM read_csv(?, all_varchar=true, skip=2)",
                [os.path.join(tmp, "remises_export.csv")])
    con.execute("CREATE TABLE c AS SELECT * FROM read_csv(?, all_varchar=true, encoding='cp1252')",
                [os.path.join(rac, "03_exercices/dossier_M05/clients.csv")])
    con.execute("""
    CREATE TABLE v_ttc AS
    SELECT v.*,
           TRY_CAST(REPLACE(TRIM(REPLACE(montant_ttc, ' FCFA', '')), ' ', '') AS BIGINT) AS ttc,
           ROW_NUMBER() OVER (PARTITION BY id_ticket, id_produit, quantite, montant_ttc, heure
                              ORDER BY CAST(id_vente AS BIGINT)) AS rn
    FROM v
    """)
    con.execute("""
    CREATE TABLE v1 AS
    SELECT id_vente, id_ticket, date_vente, heure, id_magasin, id_vendeur, id_client,
           id_produit, quantite, prix_unitaire_ht, taux_remise, montant_ht, montant_tva, ttc,
           mode_paiement, canal, est_retour, poids_kg, mois, annee
    FROM v_ttc WHERE rn = 1
    """)
    con.execute("""
    CREATE TABLE v2 AS
    SELECT *,
           CASE WHEN CAST(substr(date_vente, 6, 2) AS INT) != CAST(mois AS INT)
                THEN strftime(make_date(CAST(annee AS INT), CAST(substr(date_vente, 9, 2) AS INT),
                                          CAST(substr(date_vente, 6, 2) AS INT)), '%Y-%m-%d')
                ELSE date_vente END AS date_fixe
    FROM v1
    """)
    con.execute("""
    CREATE TABLE fin AS
    SELECT v2.id_vente, v2.id_ticket, v2.date_fixe AS date_vente, v2.heure, v2.id_magasin,
           v2.id_vendeur, v2.id_client, v2.id_produit, v2.quantite, v2.prix_unitaire_ht,
           v2.taux_remise, v2.montant_ht, v2.montant_tva, v2.ttc AS montant_ttc,
           v2.mode_paiement, v2.canal, v2.est_retour, v2.poids_kg, v2.mois, v2.annee,
           rr.remise_consentie_montant, c.ville
    FROM v2
    LEFT JOIN (SELECT id_client, annee, mois, remise_consentie_montant
               FROM (SELECT *, ROW_NUMBER() OVER (
                        PARTITION BY id_client, annee, mois
                        ORDER BY remise_consentie_montant) AS rn2 FROM r)
               WHERE rn2 = 1) rr
      ON v2.id_client = rr.id_client AND v2.annee = rr.annee AND v2.mois = rr.mois
    LEFT JOIN c ON v2.id_client = c.id_client
    """)
    con.execute("""
    CREATE TABLE canon AS
    SELECT CAST(id_vente AS BIGINT) AS iv,
           coalesce(id_vente, '') || '|' || coalesce(id_ticket, '') || '|' ||
           coalesce(date_vente, '') || '|' || coalesce(heure, '') || '|' ||
           coalesce(id_magasin, '') || '|' || coalesce(id_vendeur, '') || '|' ||
           coalesce(id_client, '') || '|' || coalesce(id_produit, '') || '|' ||
           coalesce(quantite, '') || '|' || coalesce(prix_unitaire_ht, '') || '|' ||
           coalesce(taux_remise, '') || '|' || coalesce(montant_ht, '') || '|' ||
           coalesce(montant_tva, '') || '|' || CAST(montant_ttc AS VARCHAR) || '|' ||
           coalesce(mode_paiement, '') || '|' || coalesce(canal, '') || '|' ||
           coalesce(est_retour, '') || '|' || coalesce(poids_kg, '') || '|' ||
           coalesce(mois, '') || '|' || coalesce(annee, '') || '|' ||
           coalesce(CAST(remise_consentie_montant AS VARCHAR), '') || '|' ||
           coalesce(ville, '') AS ligne
    FROM fin
    """)
    row = con.execute("""
    SELECT (SELECT sha256(string_agg(ligne, chr(10) ORDER BY iv)) FROM canon),
           count(*),
           sum(CAST(quantite AS BIGINT)), sum(CAST(prix_unitaire_ht AS BIGINT)),
           sum(CAST(montant_ht AS BIGINT)), sum(CAST(montant_tva AS BIGINT)),
           sum(CAST(montant_ttc AS BIGINT)),
           coalesce(sum(CAST(remise_consentie_montant AS BIGINT)), 0)
    FROM fin
    """).fetchone()
    (empreinte, n, q, p, mh, mtv, mtt, rem) = row
    return (empreinte, int(n),
            {"quantite": int(q), "prix_unitaire_ht": int(p), "montant_ht": int(mh),
             "montant_tva": int(mtv), "montant_ttc": int(mtt)}, int(rem))


if __name__ == "__main__":
    main()
