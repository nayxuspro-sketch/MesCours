#!/usr/bin/env python3
"""perception_M10.py — la mesure de l'etape 1 de C01 : le meme jeu de valeurs code
de cinq facons, et ce que l'oeil peut y lire.

Le chapitre C01 affirme une hierarchie de lecture (position > longueur > angle >
aire > intensite de couleur) et en tire une prescription : l'encodage se choisit
apres la question. Ce script **mesure** l'affirmation sur le socle M09 (les 8 parts
de CA par categorie de la quincaillerie, deja mesurees pour le defaut D3 du dossier) :

    pour chaque encodage, quel ecart entre deux categories voisines l'oeil doit-il
    detecter, et dans quelle unite ?

Les cinq panneaux sont dessines a l'echelle d'une planche du manuel (170 mm de
large) et les ecarts sont convertis depuis les coordonnees reelles de la figure
(`ax.transData` -> pixels -> millimetres), pas depuis une formule de coin.

Sortie : un rapport chiffre sur stdout + la planche figures/M10_C01_cinq_encodages.svg
(deterministe : hashsalt + metadata sans horodatage).

Usage : python3 tools/perception_M10.py
"""
from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.cm as cm  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(RACINE, "03_exercices", "dossier_M09")
SORTIE = os.path.join(RACINE, "figures", "M10_C01_cinq_encodages.svg")

BLEU, ORANGE, GRIS = "#1f4e79", "#c96a1a", "#8895a5"
LARGEUR_MM = 170.0          # largeur utile de la planche dans le manuel
AXE_MAX = 20.0              # les parts vont de 8,9 a 15,6 % : l'axe va de 0 a 20 %

matplotlib.rcParams["svg.hashsalt"] = "perception_M10"
plt.rcParams.update({"font.size": 8, "svg.fonttype": "none"})


def sauver(fig, chemin, **kw):
    fig.savefig(chemin, metadata={"Date": None, "Creator": "perception_M10.py"}, **kw)


# ----------------------------------------------------------------------
# Les 8 valeurs du socle : la part de CA par categorie (le defaut D3 du dossier)
# ----------------------------------------------------------------------
def parts():
    v = pd.read_csv(os.path.join(SOURCE, "quincaillerie", "vente.csv"),
                    parse_dates=["date_vente"])
    prod = pd.read_csv(os.path.join(SOURCE, "quincaillerie", "produit.csv"))
    vp = v[~v["est_retour"]].merge(prod[["id_produit", "id_categorie"]],
                                   on="id_produit", how="left")
    part = (vp.groupby("id_categorie")["montant_ttc"].sum()
            / vp["montant_ttc"].sum() * 100).sort_values()
    return part


# ----------------------------------------------------------------------
# Couleur : L* et a*/b* CIE depuis un triplet sRGB (aucune dependance en plus)
# ----------------------------------------------------------------------
def srgb_vers_lab(rgb):
    def lin(t):
        return t / 12.92 if t <= 0.04045 else ((t + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb[:3])
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    xn, yn, zn = 0.95047, 1.0, 1.08883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x / xn), f(y / yn), f(z / zn)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def mm(ax, p0, p1):
    """Distance en millimetres entre deux points donnes en coordonnees donnees."""
    t = ax.transData.transform(np.array([p0, p1], dtype=float))
    d_px = float(np.hypot(*(t[1] - t[0])))
    return d_px * 25.4 / ax.figure.dpi


def main():
    part = parts()
    val = part.to_numpy()
    noms = list(part.index)
    ecarts = np.diff(val)
    i_min = int(np.argmin(ecarts))
    i_max = int(np.argmax(ecarts))

    print("=" * 78)
    print("C01 — LES 8 PARTS DU SOCLE (CA quincaillerie par categorie, en %)")
    print("=" * 78)
    print("  " + " · ".join(f"{n}={v:.2f}" for n, v in zip(noms, val)))
    print(f"  parts : {len(val)} ; min {val.min():.1f} % ; max {val.max():.1f} % ; "
          f"rapport max/min {val.max()/val.min():.2f}")
    print(f"  ecart entre deux parts VOISINES : min {ecarts.min():.2f} pt "
          f"({noms[i_min]} → {noms[i_min+1]}) ; max {ecarts.max():.2f} pt "
          f"({noms[i_max]} → {noms[i_max+1]}) ; median {np.median(ecarts):.2f} pt")
    print(f"  ecart des extremes : {val.max()-val.min():.2f} pt "
          f"(soit {val.max()/val.min():.2f} fois la plus petite part)")

    fig = plt.figure(figsize=(LARGEUR_MM / 25.4, 128 / 25.4), dpi=105)
    gs = fig.add_gridspec(3, 2, height_ratios=[1.0, 1.0, 0.85], hspace=0.75,
                          wspace=0.16, top=0.85, bottom=0.11, left=0.115, right=0.98)
    resultats = {}
    note = dict(ha="left", va="top", fontsize=7, color="#222222")

    # -------- 1. position : nuage aligne (l'echelle commune) -------------
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.scatter(val, np.arange(len(val)), s=18, color=BLEU, zorder=3)
    ax1.set_yticks(range(len(val)), [f"C{n}" for n in noms], fontsize=7)
    ax1.set_xlim(0, AXE_MAX)
    ax1.grid(axis="x", lw=0.3, color=GRIS)
    ax1.tick_params(labelsize=7)
    ax1.set_title("1 \u00b7 position (echelle commune)", fontsize=8, loc="left")
    e_pos = mm(ax1, (val[i_min], 0), (val[i_min + 1], 0))
    e_pos_max = mm(ax1, (val[i_max], 0), (val[i_max + 1], 0))
    resultats["position_min_mm"] = e_pos
    resultats["position_max_mm"] = e_pos_max
    ax1.annotate(f"ecart a lire : {e_pos:.2f} mm", xy=(0.02, 0.95),
                 xycoords="axes fraction", ha="left", va="top", fontsize=7,
                 color="#222222",
                 bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.2))

    # -------- 2. longueur : barres alignees sur le zero -------------------
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.barh(np.arange(len(val)), val, height=0.6, color=BLEU)
    ax2.set_yticks(range(len(val)), [f"C{n}" for n in noms], fontsize=7)
    ax2.set_xlim(0, AXE_MAX)
    ax2.tick_params(labelsize=7)
    ax2.set_title("2 \u00b7 longueur (barres depuis zero — meme geometrie)", fontsize=8,
                  loc="left")
    resultats["longueur_min_mm"] = mm(ax2, (val[i_min], 0), (val[i_min + 1], 0))
    resultats["longueur_max_mm"] = mm(ax2, (val[i_max], 0), (val[i_max + 1], 0))
    # -------- 3. angle : le camembert ------------------------------------
    ax3 = fig.add_subplot(gs[0, 1])
    ax3.pie(val, startangle=90, counterclock=False,
            colors=[cm.Blues(0.30 + 0.55 * (x - val.min()) / (val.max() - val.min())) for x in val],
            wedgeprops={"width": 0.42, "edgecolor": "white", "lw": 0.5})
    ax3.set_title("3 \u00b7 angle (camembert)", fontsize=8, loc="left")
    deg = 360 / 100
    resultats["angle_min_deg"] = ecarts.min() * deg
    resultats["angle_max_deg"] = ecarts.max() * deg
    resultats["angle_total_min_deg"] = val.min() * deg
    cum = float(np.cumsum(val)[i_min]) * deg          # frontiere C5 / C8 dans le sens horaire
    th = np.radians(90 - cum)
    ax3.annotate(f"C{noms[i_min]} / C{noms[i_min+1]}\n{ecarts.min() * deg:.2f}\u00b0",
                 xy=(0.99 * np.cos(th), 0.99 * np.sin(th)),
                 xytext=(1.62 * np.cos(th), 1.62 * np.sin(th)),
                 fontsize=6.5, ha="center", va="center", color=ORANGE,
                 arrowprops=dict(arrowstyle="-", lw=0.6, color=ORANGE))

    # -------- 4. aire : bulles (aire proportionnelle) --------------------
    ax4 = fig.add_subplot(gs[1, 1])
    r = np.sqrt(val / val.max()) * 6
    ax4.scatter(np.arange(len(val)), np.zeros(len(val)), s=(r * 3.2) ** 2,
                color=ORANGE, alpha=0.9, edgecolor="white", lw=0.4)
    ax4.set_xticks(range(len(val)), [f"C{n}" for n in noms], fontsize=7)
    ax4.set_xlim(-0.75, len(val) - 0.25)
    ax4.set_ylim(-7, 9)
    ax4.set_yticks([])
    ax4.tick_params(labelsize=7)
    ax4.set_title("4 \u00b7 aire (disques proportionnels)", fontsize=8, loc="left")
    resultats["aire_min_rel_pct"] = ecarts.min() / val[i_min] * 100
    resultats["aire_max_rel_pct"] = ecarts.max() / val[i_max] * 100
    ax4.annotate(f"ecart a lire : {resultats['aire_min_rel_pct']:.2f} % de la surface",
                 xy=(0.03, 0.06), xycoords="axes fraction", ha="left", va="bottom",
                 fontsize=7, color="#222222",
                 bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.2))

    # -------- 5. intensite : la meme rampe, une ligne --------------------
    ax5 = fig.add_subplot(gs[2, :])
    cmap = plt.get_cmap("Blues")
    norm = plt.Normalize(0, AXE_MAX)
    ax5.imshow(val[np.newaxis, :], aspect="auto", cmap=cmap, norm=norm,
               extent=(0, len(val), 0, 1))
    ax5.set_xticks(np.arange(len(val)) + 0.5, [f"C{n}" for n in noms], fontsize=7)
    ax5.set_yticks([])
    ax5.tick_params(labelsize=7)
    ax5.set_title("5 \u00b7 intensite de couleur (rampe sequentielle)", fontsize=8, loc="left")
    labs = [srgb_vers_lab(cmap(norm(x))) for x in val]
    dl_min = abs(labs[i_min + 1][0] - labs[i_min][0])
    dl_max = abs(labs[i_max + 1][0] - labs[i_max][0])
    de_min = float(np.linalg.norm(np.array(labs[i_min + 1]) - np.array(labs[i_min])))
    de_max = float(np.linalg.norm(np.array(labs[i_max + 1]) - np.array(labs[i_max])))
    resultats["couleur_dl_min"] = dl_min
    resultats["couleur_dl_max"] = dl_max
    resultats["couleur_de_min"] = de_min
    resultats["couleur_de_max"] = de_max
    labs_ref = srgb_vers_lab(cmap(norm(val.max())))
    resultats["couleur_dl_etendue"] = abs(srgb_vers_lab(cmap(norm(val.min())))[0] - labs_ref[0])
    resultats["couleur_dl_par_point"] = resultats["couleur_dl_etendue"] / (val.max() - val.min())
    ax5.annotate(f"ecart a lire : {dl_min:.2f} L* (l'echelle entiere en fait {resultats['couleur_dl_etendue']:.0f})",
                 xy=(0.5, 0.5), xycoords="axes fraction", ha="center", va="center",
                 fontsize=7, color="white")

    fig.suptitle("Le meme jeu de 8 parts de CA code de cinq facons — et l'ecart que l'oeil doit y lire",
                 fontsize=9.5, x=0.01, ha="left", y=0.985)
    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    sauver(fig, SORTIE)
    plt.close(fig)

    # -------- le rapport : chaque encodage dans son unite ----------------
    print()
    print("=" * 78)
    print("CE QUE L'OEIL DOIT DETECTER — planche de 170 mm, axe 0 a 20 %")
    print("=" * 78)
    print(f"  1. position  : ecart a lire {e_pos:.2f} mm (le plus petit) / "
          f"{e_pos_max:.2f} mm (le plus grand)")
    print(f"  2. longueur  : idem en geometrie, {resultats['longueur_min_mm']:.2f} mm / "
          f"{resultats['longueur_max_mm']:.2f} mm")
    print(f"  3. angle     : {resultats['angle_min_deg']:.2f}° (le plus petit) / "
          f"{resultats['angle_max_deg']:.2f}° (le plus grand) ; la plus petite part "
          f"occupe {resultats['angle_total_min_deg']:.1f}°")
    print(f"  4. aire      : variation relative de la surface "
          f"{resultats['aire_min_rel_pct']:.2f} % / {resultats['aire_max_rel_pct']:.2f} %")
    print(f"  5. couleur   : ecart de clarte L* {dl_min:.2f} (le plus petit) / "
          f"{dl_max:.2f} (le plus grand) ; distance Lab dE {de_min:.2f} / {de_max:.2f}")
    print(f"     (rampe : {resultats['couleur_dl_etendue']:.1f} L* sur toute l'echelle, "
          f"soit {resultats['couleur_dl_par_point']:.2f} L* par point)")
    mm_pt = LARGEUR_MM / AXE_MAX        # millimetres par point sur un axe large comme la page
    print()
    print(f"  ecart minimal : {ecarts.min() / AXE_MAX * 100:.2f} % de l'axe — "
          f"{ecarts.min() * mm_pt:.2f} mm sur un axe de 170 mm, {e_pos:.2f} mm dans la planche")
    print(f"  plus grand ecart entre voisines : {ecarts.max() * mm_pt:.1f} mm ; "
          f"ecart des extremes : {val.max()-val.min():.2f} pt = "
          f"{(val.max()-val.min()) * mm_pt:.1f} mm = "
          f"{(val.max()-val.min()) / AXE_MAX * 100:.1f} % de l'axe")
    print(f"  le rapport que le graphique PEUT dire : {val.max()/val.min():.2f} fois "
          f"(la plus grande part contre la plus petite), sur {LARGEUR_MM:.0f} mm de long")
    print(f"  planche : {os.path.relpath(SORTIE, RACINE)} "
          f"({os.path.getsize(SORTIE)/1024:.1f} Ko)")


if __name__ == "__main__":
    main()
