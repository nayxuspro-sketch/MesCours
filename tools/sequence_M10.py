#!/usr/bin/env python3
"""sequence_M10.py — la sequence de 3 ecrans du chapitre C06, en deux versions (direction, equipe).

Le chapitre C06 quitte le graphique isole : il assemble une SEQUENCE qui va de l'ecran a la decision.
Le script produit la maquette des six ecrans et mesure la maquette elle-meme (mots, chiffres, elements
par ecran) — la meme discipline qu'en C04 : on audite le texte qui produit la figure, pas l'image.

Sortie : figures/M10_C06_sequence_trois_ecrans.svg (2 versions x 3 ecrans + la bande des objections)
         + le rapport chiffre sur stdout (repris par le socle des chiffres).

Usage : python3 tools/sequence_M10.py
"""
from __future__ import annotations

import json
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(RACINE, "03_exercices", "dossier_M09")
SORTIE = os.path.join(RACINE, "figures", "M10_C06_sequence_trois_ecrans.svg")

BLEU, ORANGE, GRIS, VERT, ROUGE = "#1f4e79", "#c96a1a", "#8895a5", "#2e6f5e", "#a1382c"
BARGE = 500000.0          # le seuil du panier : 500 000 FCFA
PETIT = 250000.0          # le seuil de la masse : 250 000 FCFA

matplotlib.rcParams["svg.hashsalt"] = "sequence_M10"
plt.rcParams.update({"font.size": 7, "svg.fonttype": "none"})


def charger():
    v = pd.read_csv(os.path.join(SOURCE, "quincaillerie", "vente.csv"), parse_dates=["date_vente"])
    net = v[~v["est_retour"]]
    ca = net["montant_ttc"].sum()
    annee = net.groupby(net["date_vente"].dt.year)["montant_ttc"].sum()
    return dict(v=v, net=net, ca=ca, annee=annee)


def textes(d, m):
    """Les six ecrans de la maquette, ecrits en clair : la mesure porte sur ces textes.

    Regle de redaction (heritee de C04) : 46 caracteres au plus par ligne, 3 lignes par ecran.
    """
    n = lambda x: f"{x:,}".replace(",", " ")          # 1044 -> 1 044
    fr = lambda x: f"{x:,.1f}".replace(",", " ").replace(".", ",")   # 3965.4 -> 3 965,4
    return {
        "direction": [
            ("Écran 1 — le niveau",
             [f"CA net 2026 : {fr(m['annee_2'])} M FCFA",
              f"+{fr(m['ecart_pct'])} % sur un an ({fr(m['annee_1'])} M en 2025)",
              f"{m['mois']} mois comparés, retours exclus"],
             "→ où en est-on ? · la saisonnalité ?"),
            ("Écran 2 — le levier",
             [f"{fr(m['part_ventes_sous_250k_pct'])} % des ventes = "
              f"{fr(m['part_ca_sous_250k_pct'])} % du CA",
              f"{n(m['ventes_plus_500k'])} ventes > 500 000 = "
              f"{fr(m['part_ca_plus_500k_pct'])} % du CA",
              f"médiane {n(m['panier_median'])} FCFA : la queue paie"],
             "→ où est le levier ?"),
            ("Écran 3 — la décision",
             [f"Objectif : {fr(m['gain_vise_m'])} M FCFA (+10 %)",
              f"Mesure : {n(m['ventes_plus_500k'])} paniers, 4 semaines",
              "Coût : 2 vendeurs ; suivi : la queue"],
             "→ combien ça rapporte ? · qui fait quoi ?"),
        ],
        "equipe": [
            ("Écran 1 — la base",
             [f"{m['mois']} mois, la même courbe qu'au rapport",
              f"Retours : {m['retours']} lignes, {fr(m['part_ca_retours_pct'])} % du CA",
              "Rien n'a été lissé ni recalculé"],
             "→ les données sont-elles propres ?"),
            ("Écran 2 — le mécanisme",
             [f"La queue ({fr(m['part_ventes_plus_500k_pct'])} % des ventes) : "
              f"{fr(m['part_ca_plus_500k_pct'])} % du CA",
              "Sous le panier médian : la moitié du fichier",
              "Un devis qui traîne : 2 semaines de CA"],
             "→ pourquoi ça se passe comme ça ?"),
            ("Écran 3 — le plan",
             [f"Semaine 1 : extraire les {n(m['ventes_plus_500k'])} paniers",
              "Semaine 2-4 : relancer, noter les refus",
              "Vendredi : revue de 10 min, 3 chiffres"],
             "→ qui fait quoi ? · comment on saura ?"),
        ],
    }


def mesures(d, maquette):
    m, net, v, ca = {}, d["net"], d["v"], d["ca"]
    m["annee_1"] = round(float(d["annee"].iloc[0]) / 1e6, 1)
    m["annee_2"] = round(float(d["annee"].iloc[1]) / 1e6, 1)
    m["ecart_pct"] = round(float(d["annee"].iloc[1] / d["annee"].iloc[0] - 1) * 100, 1)
    m["mois"] = int(net["date_vente"].dt.to_period("M").nunique())
    mont = net["montant_ttc"]
    sous = mont[mont < PETIT]
    queue = mont[mont > BARGE]
    m["ventes_sous_250k"] = int(len(sous))
    m["part_ventes_sous_250k_pct"] = round(len(sous) / len(mont) * 100, 1)
    m["part_ca_sous_250k_pct"] = round(float(sous.sum() / ca * 100), 1)
    m["ventes_plus_500k"] = int((v["montant_ttc"] > BARGE).sum())   # toutes lignes (socle d5)
    m["ventes_plus_500k_net"] = int(len(queue))
    m["part_ventes_plus_500k_pct"] = round(len(queue) / len(mont) * 100, 1)
    m["part_ca_plus_500k_pct"] = round(float(queue.sum() / ca * 100), 1)
    m["retours"] = int(v["est_retour"].sum())
    m["montant_retours"] = int(v.loc[v["est_retour"], "montant_ttc"].sum())
    m["part_ca_retours_pct"] = round(m["montant_retours"] / float(v["montant_ttc"].sum()) * 100, 2)
    m["panier_median"] = int(round(float(mont.median())))
    m["panier_moyen"] = int(round(float(mont.mean())))
    m["ratio_moyenne_mediane"] = round(float(mont.mean() / mont.median()), 2)
    # gain vise par la sequence : le CA des paniers de plus de 500 000 FCFA, +10 % de relance
    m["gain_vise_m"] = round(float(queue.sum()) * 0.10 / 1e6, 1)
    # la sequence elle-meme, mesuree sur la maquette
    m["ecrans"] = 3
    m["versions"] = 2
    m["temps_par_ecran_s"] = 20
    m["temps_sequence_s"] = m["ecrans"] * m["temps_par_ecran_s"]
    for version, ecrans in maquette.items():
        mots = [len(x[1]) * 8 for x in ecrans]          # 3 a 4 lignes par ecran, mesurees plus bas
        m[f"{version}_ecrans"] = len(ecrans)
        m[f"{version}_mots"] = int(sum(len(" ".join(x[1]).split()) for x in ecrans))
        m[f"{version}_chiffres"] = int(sum(len(re.findall(r"\d[\d\s,.]*\d|\d", " ".join(x[1])))
                                           for x in ecrans))
        m[f"{version}_chiffres_par_ecran"] = int(round(m[f"{version}_chiffres"] / len(ecrans)))
        m[f"{version}_lignes_par_ecran"] = int(round(sum(len(x[1]) for x in ecrans) / len(ecrans)))
        m[f"{version}_lignes_max"] = int(max(len(x[1]) for x in ecrans))
        del mots
    m["objections"] = 5
    m["objections_couvertes_v1"] = 2      # le cadre unique du rapport : niveau et levier, rien d'autre
    m["objections_couvertes_sequence"] = 5
    m["objections_couvertes_pct"] = int(round(m["objections_couvertes_sequence"]
                                              / m["objections"] * 100))
    m["ecrans_avant_v1"] = 1
    m["ecrans_apres"] = 3
    m["chiffres_v1"] = 12                 # le cadre unique empile 12 chiffres (compte sur le rapport)
    if "direction_chiffres" in m:
        m["chiffres_sequence"] = m["direction_chiffres"] + m["equipe_chiffres"]
        m["chiffres_par_ecran_max"] = max(m["direction_chiffres_par_ecran"],
                                          m["equipe_chiffres_par_ecran"])
    return m


def planche(d, maquette, m):
    fig = plt.figure(figsize=(190 / 25.4, 178 / 25.4), dpi=100)
    gs = fig.add_gridspec(5, 3, height_ratios=[0.16, 1.0, 0.22, 1.0, 0.30],
                          hspace=0.30, wspace=0.09, top=0.925, bottom=0.03,
                          left=0.035, right=0.975)
    couleurs = {"direction": BLEU, "equipe": VERT}
    lignes_grille = {0: (0, 1), 1: (2, 3)}

    for r, version in enumerate(("direction", "equipe")):
        ligne_titre, ligne_cadres = lignes_grille[r]
        axl = fig.add_subplot(gs[ligne_titre, :])
        axl.set_axis_off()
        axl.text(0.0, 0.95, f"Version {'direction' if r == 0 else 'équipe'} — "
                            f"{m[version + '_mots']} mots, {m[version + '_chiffres']} chiffres, "
                            f"{m[version + '_lignes_par_ecran']} lignes par écran",
                 transform=axl.transAxes, fontsize=8, color=couleurs[version],
                 fontweight="bold", va="top")
        for c, (titre, lignes, reponse) in enumerate(maquette[version]):
            ax = fig.add_subplot(gs[ligne_cadres, c])
            ax.set_xticks([]); ax.set_yticks([])
            for sp in ax.spines.values():
                sp.set_color(couleurs[version]); sp.set_linewidth(1.1)
            ax.set_facecolor("#fbfcfe")
            ax.text(0.04, 0.92, titre, transform=ax.transAxes, fontsize=7.5,
                    fontweight="bold", color=couleurs[version], va="top")
            for i, ligne in enumerate(lignes):
                ax.text(0.05, 0.71 - i * 0.165, "· " + ligne, transform=ax.transAxes,
                        fontsize=6.3, va="top")
            ax.text(0.05, 0.06, reponse, transform=ax.transAxes, fontsize=5.9,
                    color=GRIS, va="bottom", style="italic")

    ax = fig.add_subplot(gs[4, :])
    ax.set_axis_off()
    ax.text(0.0, 1.05, "Les cinq objections, et l'écran qui y répond", transform=ax.transAxes,
            fontsize=8, fontweight="bold", va="top", color=BLEU)
    obj = [("où en est-on ? la saisonnalité ?", "écran 1"),
           ("où est le levier ?", "écran 2"),
           ("combien ça rapporte ?", "écran 3"),
           ("qui fait quoi ?", "écran 3"),
           ("comment on saura si ça marche ?", "écran 3")]
    for i, (question, ou) in enumerate(obj):
        ax.text(0.0, 0.62 - i * 0.155, f"« {question} » → {ou}", transform=ax.transAxes,
                fontsize=6.4)
    ax.text(0.52, 0.62, f"Le cadre unique du rapport (v1) : {m['ecrans_avant_v1']} écran, "
                        f"{m['chiffres_v1']} chiffres,\n{m['objections_couvertes_v1']} objections sur "
                        f"{m['objections']} couvertes.", transform=ax.transAxes, fontsize=6.4,
            color=ROUGE, va="top")
    ax.text(0.52, 0.14, f"La séquence : {m['ecrans']} écrans, {m['chiffres_sequence']} chiffres "
                        f"({m['chiffres_par_ecran_max']} par écran au plus),\n"
                        f"{m['objections_couvertes_sequence']} objections sur {m['objections']} "
                        f"({m['objections_couvertes_pct']} %), "
                        f"{m['temps_sequence_s']} s de lecture.", transform=ax.transAxes,
            fontsize=6.4, color=VERT, va="top")

    fig.suptitle("La séquence de trois écrans : le même fil rouge, deux destinataires",
                 fontsize=9.5, x=0.035, ha="left", y=0.985)
    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    fig.savefig(SORTIE, metadata={"Date": None, "Creator": "sequence_M10.py"}, dpi=100)
    plt.close(fig)
    return SORTIE


def main():
    d = charger()
    # les textes portent les chiffres mesures : deux passes, la seconde sur les textes definitifs
    maquette = textes(d, mesures(d, {}))
    m = mesures(d, maquette)
    print("=" * 78)
    print("C06 — LA SEQUENCE DE TROIS ECRANS, MESUREE SUR LE FIL ROUGE")
    print("=" * 78)
    for k, val in m.items():
        print(f"  {k:34s} = {val}")
    chemin = planche(d, maquette, m)
    print()
    print(f"  planche : {os.path.relpath(chemin, RACINE)} ({os.path.getsize(chemin)/1024:.1f} Ko)")
    print()
    print(json.dumps(m, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
