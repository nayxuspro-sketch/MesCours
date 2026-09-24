#!/usr/bin/env python3
"""dossier_M10.py — le socle du module M10 (Data visualization).

Le module ne crée AUCUNE donnée nouvelle : il change le regard porté sur le socle
M07/M08/M09 (quincaillerie, centre de santé, établissement scolaire). Ce que le
générateur produit, c'est le **rapport à refondre** :

    03_exercices/dossier_M10/
      00_brief.md                 le brief remis à l'apprenant
      rapport_avant/              les 5 graphiques RATÉS (SVG) + le code qui les produit
        g1_axe_tronque.svg            défaut dominant : axe tronqué
        g2_double_axe.svg             défaut dominant : double axe
        g3_camembert.svg              défaut dominant : camembert surchargé
        g4_cumul_pourcent.svg         défaut dominant : cumul de pourcentages
        g5_log_surcharge.svg          défaut dominant : échelle log surprise + surcharge
        code_avant.py                 le script qui produit les 5 (rejouable)
        rapport_avant.md              les 2 pages de rapport que ces graphiques illustrent
      rapport_apres/              les 5 graphiques CORRIGÉS (SVG) + le code
        g1_corrige.svg ... g5_corrige.svg
        code_apres.py
      ATTENDU.json                les mesures des défauts (clés m10p_*)

Reproductibilité : aucune graine aléatoire n'est utilisée ; le dossier doit être
byte-identique d'une exécution à l'autre (`diff -rq` = 0).

Usage : python3 tools/dossier_M10.py
"""
from __future__ import annotations

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(RACINE, "03_exercices", "dossier_M09")
DEST = os.path.join(RACINE, "03_exercices", "dossier_M10")
AVANT = os.path.join(DEST, "rapport_avant")
APRES = os.path.join(DEST, "rapport_apres")

BLEU, ORANGE, GRIS = "#1f4e79", "#c96a1a", "#8895a5"

# Sortie SVG déterministe : sans ces deux réglages, matplotlib inscrit un horodatage
# et des identifiants tirés au hasard — le dossier ne serait pas reproductible (diff != 0).
matplotlib.rcParams["svg.hashsalt"] = "dossier_M10"


def sauver(fig, chemin, **kw):
    """Sauvegarde sans horodatage : le fichier doit être byte-identique d'un run à l'autre."""
    fig.savefig(chemin, metadata={"Date": None, "Creator": "dossier_M10.py"}, **kw)


# ----------------------------------------------------------------------
# Chargement du socle (le fil rouge et ses satellites)
# ----------------------------------------------------------------------
def charger():
    v = pd.read_csv(os.path.join(SOURCE, "quincaillerie", "vente.csv"),
                    parse_dates=["date_vente"])
    v["ct"] = (v["montant_ttc"] * 100).round().astype("int64")
    ca = v[~v["est_retour"]].groupby(v["date_vente"].dt.to_period("M"))["ct"].sum() // 100
    nv = v[~v["est_retour"]].groupby(v["date_vente"].dt.to_period("M")).size()
    return v, ca, nv


def mesures(v, ca, nv):
    """Toutes les mesures des défauts plantés — elles alimentent ATTENDU.json."""
    mg3 = ca.rolling(3).mean()
    m = {}
    # D1 — l'axe tronqué : variation réelle de la moyenne glissante contre hauteur occupée
    m["d1_axe_min_m"] = round(float(np.floor(ca.min() / 1e7) * 10), 1)
    m["d1_axe_max_m"] = round(float(np.ceil(ca.max() / 1e7) * 10), 1)
    m["d1_variation_mg3_pct"] = round(float((mg3.max() - mg3.min()) / mg3.min() * 100), 1)
    m["d1_variation_brute_pct"] = round(float((ca.max() - ca.min()) / ca.min() * 100), 1)
    m["d1_facteur_exageration"] = int(round(100 / m["d1_variation_mg3_pct"]))
    # D2 — le double axe : deux séries que les deux échelles font coïncider
    ret = v.groupby("date_vente")["est_retour"].sum()
    ret = ret.groupby(ret.index.to_period("M")).sum().reindex(ca.index).fillna(0)
    m["d2_corr_ca_retours"] = round(float(ca.corr(ret)), 2)
    m["d2_retours_min"] = int(ret.min())
    m["d2_retours_max"] = int(ret.max())
    m["d2_serie_longueur"] = int(len(ca))
    # D3 — le camembert surchargé : la part par catégorie et l'écart minimal entre deux parts
    prod = pd.read_csv(os.path.join(SOURCE, "quincaillerie", "produit.csv"))
    vp = v[~v["est_retour"]].merge(prod[["id_produit", "id_categorie"]], on="id_produit", how="left")
    part = (vp.groupby("id_categorie")["montant_ttc"].sum() / vp["montant_ttc"].sum() * 100).sort_values()
    m["d3_nb_parts"] = int(len(part))
    m["d3_part_min"] = round(float(part.min()), 1)
    m["d3_part_max"] = round(float(part.max()), 1)
    ecarts = part.diff().dropna()
    m["d3_ecart_min_entre_parts"] = round(float(ecarts.min()), 2)
    m["d3_nb_parts_sous_5pct"] = int((part < 5).sum())
    # D4 — le cumul de pourcentages : les totaux par trimestre sont différents
    tri = v[~v["est_retour"]].groupby(v["date_vente"].dt.to_period("Q"))["ct"].sum() // 100
    m["d4_nb_trimestres"] = int(len(tri))
    m["d4_total_min"] = int(tri.min())
    m["d4_total_max"] = int(tri.max())
    m["d4_variation_totaux_pct"] = round(float((tri.max() - tri.min()) / tri.min() * 100), 1)
    # D5 — l'échelle log surprise : ce que le log gomme (le plateau et la queue)
    mt = v["montant_ttc"]
    m["d5_ratio_max_median"] = int(round(float(mt.max() / mt.median())))
    m["d5_plateau"] = int((mt == mt.max()).sum())
    m["d5_part_sous_10k_pct"] = round(float((mt < 10000).mean() * 100), 1)
    m["d5_part_sous_1k_pct"] = round(float((mt < 1000).mean() * 100), 1)
    m["d5_mediane_montant"] = int(round(float(mt.median())))
    m["d5_part_sous_250k_pct"] = round(float((mt < 250000).mean() * 100), 1)
    m["d5_queue_sup_500k"] = int((mt > 500000).sum())
    # La grille et la table, qui sont des artefacts du module (pas des mesures)
    m["grille_points"] = 18
    m["grille_familles"] = 4
    m["table_graphiques"] = 16
    m["table_graphiques_fondateurs"] = 11
    m["graphiques_avant"] = 5
    m["graphiques_apres"] = 5
    return m


# ----------------------------------------------------------------------
# Les 5 graphiques ratés (rapport_avant)
# ----------------------------------------------------------------------
def avant(v, ca, nv):
    """Chaque figure porte UN défaut dominant, volontairement, et rien d'autre."""
    faits = {}
    t = ca.index.to_timestamp()

    # D1 — axe tronqué : l'axe commence au minimum observé, la platitude devient une pente
    fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
    ax.plot(t, ca.values / 1e6, "-", color=ORANGE, lw=1.4)
    ax.plot(t, ca.rolling(3).mean().values / 1e6, "-", color=BLEU, lw=2.4)
    ax.set_ylim(ca.min() / 1e6 - 1, ca.max() / 1e6 + 2)
    ax.set_title("Evolution du chiffre d'affaires")
    ax.set_ylabel("M FCFA")
    fig.tight_layout()
    sauver(fig, os.path.join(AVANT, "g1_axe_tronque.svg"))
    plt.close(fig)
    faits["g1"] = "courbe, axe des ordonnees tronque au minimum observe, titre d'etiquetage"

    # D2 — double axe : deux échelles choisies pour faire coïncider les deux courbes
    ret = v.groupby("date_vente")["est_retour"].sum()
    ret = ret.groupby(ret.index.to_period("M")).sum().reindex(ca.index).fillna(0)
    fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
    ax.plot(t, ca.values / 1e6, "-", color=BLEU, lw=2)
    ax.set_ylabel("CA (M FCFA)", color=BLEU)
    ax2 = ax.twinx()
    ax2.plot(t, ret.values, "-", color=ORANGE, lw=2)
    ax2.set_ylabel("Nombre de retours", color=ORANGE)
    ax.set_title("Les retours suivent le chiffre d'affaires")
    fig.tight_layout()
    sauver(fig, os.path.join(AVANT, "g2_double_axe.svg"))
    plt.close(fig)
    faits["g2"] = "deux axes verticaux, deux series sans correlation reelle, titre causal"

    # D3 — camembert surchargé : toutes les catégories, étiquettes en pourcentage
    prod = pd.read_csv(os.path.join(SOURCE, "quincaillerie", "produit.csv"))
    vp = v[~v["est_retour"]].merge(prod[["id_produit", "id_categorie"]], on="id_produit", how="left")
    part = vp.groupby("id_categorie")["montant_ttc"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(7, 5), dpi=100)
    ax.pie(part.values, labels=[f"{c}" for c in part.index],
           autopct="%1.1f%%", startangle=90, pctdistance=0.78,
           colors=plt.cm.tab20(np.linspace(0, 1, len(part))))
    ax.set_title("Repartition du chiffre d'affaires par categorie")
    fig.tight_layout()
    sauver(fig, os.path.join(AVANT, "g3_camembert.svg"))
    plt.close(fig)
    faits["g3"] = f"camembert a {len(part)} parts, etiquettes superposees, aucune valeur absolue"

    # D4 — cumul de pourcentages : des parts qui masquent des totaux différents
    q = v[~v["est_retour"]].copy()
    q["trim"] = q["date_vente"].dt.to_period("Q").astype(str)
    q["mode"] = q["id_mode"].astype(str)
    tab = q.pivot_table(index="trim", columns="mode", values="montant_ttc", aggfunc="sum")
    pct = tab.div(tab.sum(axis=1), axis=0) * 100
    fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
    bas = np.zeros(len(pct))
    for col in pct.columns:
        ax.bar(pct.index, pct[col], bottom=bas, label=f"mode {col}")
        bas += pct[col].values
    ax.set_ylim(0, 100)
    ax.set_title("Part du CA par mode de paiement et par trimestre")
    ax.legend(fontsize=8, ncol=5)
    fig.tight_layout()
    sauver(fig, os.path.join(AVANT, "g4_cumul_pourcent.svg"))
    plt.close(fig)
    faits["g4"] = "barres empilees a 100 %, totaux trimestriels masques, parts lues comme des volumes"

    # D5 — échelle log surprise + surcharge : la queue et le plateau disparaissent
    fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
    for lib, serie, coul in (("montant TTC", v["montant_ttc"], BLEU),
                             ("montant remise", v["montant_remise"], ORANGE),
                             ("prix unitaire HT", v["montant_ttc"] / v["quantite"], GRIS)):
        ax.hist(serie.clip(lower=1), bins=40, histtype="step", lw=1.6, color=coul, label=lib)
    ax.set_yscale("log")
    ax.set_title("Distribution des montants")
    ax.legend(fontsize=8)
    fig.tight_layout()
    sauver(fig, os.path.join(AVANT, "g5_log_surcharge.svg"))
    plt.close(fig)
    faits["g5"] = "echelle logarithmique non annoncee, trois series superposees, queue et plateau gommes"
    return faits


# ----------------------------------------------------------------------
# Les 5 graphiques corrigés (rapport_apres)
# ----------------------------------------------------------------------
def apres(v, ca, nv):
    faits = {}
    t = ca.index.to_timestamp()
    mg3 = ca.rolling(3).mean()

    # C1 — l'axe à zéro, et le titre qui affirme ce que la donnée dit
    fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
    ax.plot(t, ca.values / 1e6, "-", color=ORANGE, lw=1.2, label="CA mensuel (sans retours)")
    ax.plot(t, mg3.values / 1e6, "-", color=BLEU, lw=2.6, label="moyenne glissante 3 mois")
    ax.set_ylim(0, 360)
    ax.annotate("la moyenne glissante reste\nentre 320 et 337 M : le CA est plat",
                xy=(t[12], mg3.values[12] / 1e6), xytext=(0.36, 0.30), textcoords="axes fraction",
                fontsize=8.5, color=BLEU,
                arrowprops=dict(arrowstyle="->", color=BLEU, lw=1))
    ax.set_title("Le CA est plat sur 24 mois (axe a zero ; moyenne glissante 320-337 M)",
                 fontsize=10.5, color="#12365a")
    ax.set_ylabel("M FCFA")
    ax.legend(fontsize=8.5, loc="lower left")
    fig.tight_layout()
    sauver(fig, os.path.join(APRES, "g1_corrige.svg"))
    plt.close(fig)
    faits["c1"] = "axe a zero, titre qui affirme, annotation du chiffre cle, source et unite"

    # C2 — deux graphiques séparés, une seule échelle par graphique
    fig, (axa, axb) = plt.subplots(2, 1, figsize=(8, 5.2), dpi=100, sharex=True)
    axa.plot(t, ca.values / 1e6, "-", color=BLEU, lw=2)
    axa.set_ylabel("CA (M FCFA)", fontsize=8.5)
    ret = v.groupby("date_vente")["est_retour"].sum()
    ret = ret.groupby(ret.index.to_period("M")).sum().reindex(ca.index).fillna(0)
    r = ca.corr(ret)
    axa.set_title("Le CA et les retours : r = " f"{r:+.2f} sur {len(ca)} mois — un lien non concluant,"
                  " deux graphiques, deux echelles", fontsize=10.5, color="#12365a")
    axb.plot(t, ret.values, "-", color=ORANGE, lw=2)
    axb.set_ylabel("Retours (nb)", fontsize=8.5)
    fig.tight_layout()
    sauver(fig, os.path.join(APRES, "g2_corrige.svg"))
    plt.close(fig)
    faits["c2"] = "petits multiples verticaux, une echelle par graphique, correlation annoncee"

    # C3 — barres triées, valeurs absolues, catégories faibles regroupées
    prod = pd.read_csv(os.path.join(SOURCE, "quincaillerie", "produit.csv"))
    vp = v[~v["est_retour"]].merge(prod[["id_produit", "id_categorie"]], on="id_produit", how="left")
    part = vp.groupby("id_categorie")["montant_ttc"].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(7.5, 4), dpi=100)
    ax.barh([str(c) for c in part.index], part.values / 1e6, color=BLEU)
    for i, val in enumerate(part.values / 1e6):
        ax.text(val + 2, i, f"{val:,.1f} M".replace(",", " "), va="center", fontsize=8)
    ax.set_xlim(0, part.max() / 1e6 * 1.18)
    ax.set_title(f"Le CA par categorie : {len(part)} categories, de "
                 f"{part.min() / 1e6:.1f} a {part.max() / 1e6:.1f} M FCFA (barres triees)",
                 fontsize=10.5, color="#12365a")
    ax.set_xlabel("M FCFA")
    fig.tight_layout()
    sauver(fig, os.path.join(APRES, "g3_corrige.svg"))
    plt.close(fig)
    faits["c3"] = "barres triees, longueur au lieu d'angle, valeurs absolues ecrites"

    # C4 — les volumes absolus par trimestre (ce que le cumul masquait)
    q = v[~v["est_retour"]].copy()
    q["trim"] = q["date_vente"].dt.to_period("Q").astype(str)
    tot = q.groupby("trim")["ct"].sum() // 100
    fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
    ax.bar(tot.index.astype(str), tot.values / 1e6, color=BLEU)
    ax.axhline(tot.mean() / 1e6, color=ORANGE, lw=1.6, ls="--",
               label=f"moyenne {tot.mean() / 1e6:.1f} M")
    ax.set_title("Les totaux trimestriels varient de "
                 f"{(tot.max() - tot.min()) / tot.min() * 100:.1f} % — un cumul a 100 % le cachait",
                 fontsize=10.5, color="#12365a")
    ax.set_ylabel("M FCFA")
    ax.legend(fontsize=8.5)
    fig.tight_layout()
    sauver(fig, os.path.join(APRES, "g4_corrige.svg"))
    plt.close(fig)
    faits["c4"] = "volumes absolus par trimestre, ligne de moyenne, ecart mesure en titre"

    # C5 — histogramme linéaire, échelle annoncée, zoom séparé sur la queue
    fig, (axa, axb) = plt.subplots(1, 2, figsize=(8.0, 3.6), dpi=100)
    axa.hist(v["montant_ttc"], bins=50, color=BLEU)
    part250 = (v["montant_ttc"] < 250000).mean() * 100
    axa.set_title(f"Echelle lineaire annoncee : {part250:.0f} % des ventes\nsous 250 000 FCFA "
                  f"(mediane {v['montant_ttc'].median():,.0f})".replace(",", " "),
                  fontsize=9.5, color="#12365a")
    axa.set_xlabel("montant TTC (FCFA)", fontsize=8.5)
    queue = v[v["montant_ttc"] > 500000]["montant_ttc"]
    axb.hist(queue, bins=20, color=ORANGE)
    axb.set_title(f"Zoom separe sur la queue : {len(queue)} ventes\nau-dessus de 500 000 FCFA (max "
                  f"{v['montant_ttc'].max():,.0f}, soit 5 x la mediane)".replace(",", " "),
                  fontsize=9.5, color="#12365a")
    axb.set_xlabel("montant TTC (FCFA)", fontsize=8.5)
    fig.tight_layout()
    sauver(fig, os.path.join(APRES, "g5_corrige.svg"))
    plt.close(fig)
    faits["c5"] = "un seul jeu de donnees par graphique, echelle annoncee, zoom separe sur la queue"
    return faits


BRIEF = """# Brief M10 — « La refonte »

Vous recevez un **rapport commercial** d'une enseigne de quincaillerie (5 magasins, 24 mois,
50 008 ventes). Ce rapport n'est pas faux : **ses chiffres sont justes**. Ce sont ses
**graphiques** qui font lire autre chose que ce que les données disent.

| Dossier | Contenu |
|---|---|
| `rapport_avant/` | les **5 graphiques** du rapport, tels qu'ils ont été publiés (et le code qui les produit) |
| `rapport_avant/rapport_avant.md` | les **2 pages** du rapport : ce que la direction en a retenu |
| `rapport_apres/` | les 5 graphiques **corrigés** — à ne consulter qu'après avoir proposé les vôtres |
| `ATTENDU.json` | les mesures des défauts (à comparer à vos propres mesures, **pas à recopier**) |

**Ce qu'on vous demande (`M10.P — La refonte`) :**

1. **Diagnostiquer** chaque graphique : nommer le défaut, **mesurer** l'écart qu'il crée entre
   ce que l'œil lit et ce que les données disent, et dire **quelle décision il ferait prendre à tort**.
2. **Corriger** : le bon graphique pour la question, titre qui affirme, axes honnêtes, annotation
   du chiffre clé, couleur justifiée.
3. **Produire deux versions du même constat** : une version **direction** (1 écran, l'idée et la
   décision) et une version **équipe opérationnelle** (le détail et les libellés exacts).
4. **Auto-évaluer** votre refonte avec la **grille de conception en 18 points**, puis la faire
   relire par un pair.

**La règle du projet.** Une refonte qui change un **chiffre** en changeant un **graphique** est
rejetée : les totaux avant/après doivent être **identiques** (contrôle automatique). Le module
change la **lisibilité**, jamais la donnée.
"""

RAPPORT = """# Rapport commercial — synthèse mensuelle (extrait)

*Service commercial · enseigne de quincaillerie · 5 magasins · période 2025-2026*

## Page 1 — L'activité

**Le chiffre d'affaires est en croissance continue.** Le graphique 1 montre une progression
régulière de l'activité sur les douze derniers mois, portée par une accélération au
deuxième semestre.

**Les retours suivent le chiffre d'affaires.** Le graphique 2 superpose les deux
indicateurs : ils évoluent dans le même sens, mois après mois. La qualité de service se
dégraderait donc avec l'activité, et il faudrait renforcer les contrôles les mois de pointe.

**Les catégories sont déséquilibrées.** Le graphique 3 donne la répartition du chiffre
d'affaires par catégorie de produits : la catégorie principale pèse environ un quart du
total, et plusieurs catégories se disputent la suite du classement.

## Page 2 — Le mix et les marges

**Le mix par mode de paiement est stable.** Le graphique 4 présente la répartition du
chiffre d'affaires par mode de paiement, trimestre après trimestre : aucune bascule notable,
les parts restent dans les mêmes proportions.

**Les gros montants sont rares.** Le graphique 5 montre la distribution des montants :
l'essentiel des ventes se situe dans les tranches basses, la queue de distribution étant
peu peuplée.

---

*Conclusion du rapport : la croissance est là, le volume la porte, le mix est stable ; le
service recommande de renforcer l'animation commerciale sur la catégorie principale et de
suivre la conversion du canal en magasin.*

*(Note du formateur : les cinq affirmations ci-dessus sont exactement ce que les cinq
graphiques donnent à lire — et trois d'entre elles ne résistent pas à la vérification. Le
travail du module est de dire lesquelles, de mesurer l'écart, et de corriger la lecture.)*
"""


def main():
    os.makedirs(AVANT, exist_ok=True)
    os.makedirs(APRES, exist_ok=True)
    v, ca, nv = charger()
    m = mesures(v, ca, nv)
    faits_avant = avant(v, ca, nv)
    faits_apres = apres(v, ca, nv)

    open(os.path.join(DEST, "00_brief.md"), "w", encoding="utf-8").write(BRIEF)
    open(os.path.join(AVANT, "rapport_avant.md"), "w", encoding="utf-8").write(RAPPORT)

    import shutil
    shutil.copyfile(os.path.abspath(__file__), os.path.join(AVANT, "code_avant.py"))
    shutil.copyfile(os.path.abspath(__file__), os.path.join(APRES, "code_apres.py"))

    attendu = {
        "graine": "aucune (socle M09 reutilise, empreinte b9a8d973119342ec)",
        "forme": {"avant": len(faits_avant), "apres": len(faits_apres),
                  "defauts_dominants_distincts": 5, "pages_de_rapport": 2},
        "defauts": faits_avant,
        "corrections": faits_apres,
        "mesures": m,
    }
    with open(os.path.join(DEST, "ATTENDU.json"), "w", encoding="utf-8") as fh:
        json.dump(attendu, fh, ensure_ascii=False, indent=2)

    print("dossier M10 ecrit dans", DEST)
    for k, val in m.items():
        print(f"  {k} = {val}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
