"""analyse_commerciale.py — le script qui fait le travail de trois matinées.

Projet M08.P : un seul script, 6 sections, exécuté d'une traite.
Dossier : 03_exercices/dossier_M08/ (8 CSV, dont un vide).
"""
import pandas as pd

DOSSIER = "03_exercices/dossier_M08/"

# ---------------- S1. Import des 8 CSV + contrôle des formes ----------------
FICHIERs = {
    "v": "vente.csv", "c": "client.csv", "p": "produit.csv",
    "cat": "categorie.csv", "m": "magasin.csv", "mode": "mode_paiement.csv",
    "tva": "regle_tva.csv", "o": "objectif_magasin.csv",
}
donnees = {k: pd.read_csv(DOSSIER + f) for k, f in FICHIERs.items()}
formes = {k: len(df) for k, df in donnees.items()}
print("S1 formes :", formes)

# ---------------- S2. Audit (les 4 défauts du socle) ----------------
v = donnees["v"]
cols12 = [c for c in v.columns if c != "id_vente"]
doublons = int(v.duplicated(subset=cols12).sum())
retours_brut = int(v["est_retour"].sum())
uniques = v.drop_duplicates(subset=cols12)
retours_net = int(uniques["est_retour"].sum())
dv = pd.to_datetime(v["date_vente"])
dl = pd.to_datetime(v["date_limite_remise"])
dates_naives = int((dv > dl).sum())
deadlines_j20 = int(uniques.loc[dl[uniques.index].dt.day == 20].shape[0])
manquants = int(v.isna().sum().sum())
print(f"S2 audit : doublons={doublons} retours_brut={retours_brut} retours_net={retours_net}")
print(f"          dates_naives={dates_naives} deadlines_j20={deadlines_j20} manquants={manquants}")
print("          table vide :", [k for k, f in FICHIERs.items() if f == "objectif_magasin.csv" and len(donnees[k]) == 0])

# ---------------- S3. Nettoyage (dédoublonnage, retours exclus) ----------------
propres = uniques[~uniques["est_retour"]].copy()
ct = (propres["montant_ttc"] * 100).round().astype("int64")
ct_brut = (uniques["montant_ttc"] * 100).round().astype("int64")
print("S3 propres :", len(propres), "lignes (doublons sortis, retours exclus)")

# ---------------- S4. Indicateurs (les 30 questions M07, en pandas) ----------------
# Les CA "brut" sont SANS filtre (les 50 008 lignes, Q04 de M07) ; la vue mensuelle
# et les indicateurs "propres" excluent les retours (la definition M07).
ct_toutes = (v["montant_ttc"] * 100).round().astype("int64")
ca_brut = int(ct_toutes.sum() // 100)
ca_propre = int(ct.sum() // 100)
panier = int(round(ct_toutes.sum() / len(v) / 100))
par_mag = ct_toutes.groupby(v["id_magasin"]).sum() // 100
m_produit = v.merge(donnees["p"][["id_produit", "id_categorie"]], on="id_produit", how="left")
par_cat = ct_toutes.groupby(m_produit["id_categorie"]).sum() // 100
vue = pd.DataFrame({"id_magasin": propres["id_magasin"],
                    "mois": pd.to_datetime(propres["date_vente"]).dt.to_period("M").astype(str),
                    "ca_cents": ct[propres.index]}).groupby(["id_magasin", "mois"], as_index=False)["ca_cents"].sum()
vue["ca"] = vue["ca_cents"] // 100
plus_gros = vue.loc[vue["ca"].idxmax()]
print(f"S4 ca_brut={ca_brut} ca_propre={ca_propre} panier={panier}")
print("   top magasin :", par_mag.idxmax(), par_mag.max())
print("   top categorie :", par_cat.idxmax(), par_cat.max())
print(f"   plus gros mois : magasin {int(plus_gros['id_magasin'])} ({plus_gros['mois']}) : {int(plus_gros['ca'])}")

# ---------------- S5. Les 4 graphiques ----------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
mensuel = vue.groupby("mois")["ca"].sum()
mensuel.plot(kind="bar", title="CA mensuel (sans retours)", figsize=(10, 3))
plt.tight_layout(); plt.savefig("/tmp/c07/g1_ca_mensuel.png"); plt.close()
par_mag.plot(kind="bar", title="CA par magasin (sans retours)")
plt.tight_layout(); plt.savefig("/tmp/c07/g2_ca_magasin.png"); plt.close()
par_cat.plot(kind="bar", title="CA par catégorie (sans retours)")
plt.tight_layout(); plt.savefig("/tmp/c07/g3_ca_categorie.png"); plt.close()
propres["montant_ttc"].plot(kind="hist", bins=30, title="Distribution des montants (sans retours)")
plt.tight_layout(); plt.savefig("/tmp/c07/g4_hist_montants.png"); plt.close()
import os
print("S5 graphiques :", sorted(os.path.basename(f) for f in __import__("glob").glob("/tmp/c07/g*.png")))

# ---------------- S6. Export du classeur de synthèse (4 feuilles) ----------------
audit = pd.DataFrame({"controle": ["doublons", "retours_brut", "retours_net",
                                   "dates_naives", "deadlines_j20", "manquants", "tables_vides"],
                      "valeur": [doublons, retours_brut, retours_net,
                                 dates_naives, deadlines_j20, manquants, 1]})
indicateurs = pd.DataFrame({"indicateur": ["ca_brut", "ca_propre", "panier_moyen",
                                           "plus_gros_mois_ca"],
                            "valeur": [ca_brut, ca_propre, panier, int(plus_gros["ca"])]})
with pd.ExcelWriter("/tmp/c07/synthese_commerciale.xlsx", engine="openpyxl") as w:
    audit.to_excel(w, sheet_name="audit", index=False)
    indicateurs.to_excel(w, sheet_name="indicateurs", index=False)
    par_mag.rename("ca").to_frame().to_excel(w, sheet_name="par_magasin", index=False)
    vue.drop(columns=["ca_cents"]).to_excel(w, sheet_name="par_mois", index=False)
feuilles = pd.read_excel("/tmp/c07/synthese_commerciale.xlsx", sheet_name=None)
print("S6 classeur :", {k: v.shape for k, v in feuilles.items()})
