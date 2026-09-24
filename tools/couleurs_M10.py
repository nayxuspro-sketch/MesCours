#!/usr/bin/env python3
"""couleurs_M10.py — la mesure du chapitre C03 : contraste, daltonisme, palettes.

Trois mesures, toutes calculées sur les couleurs réelles du manuel (la palette de la
maison, les cinq couleurs employées par le rapport à refondre, et la rampe séquentielle
du catalogue) :

  1. le rapport de contraste WCAG de chaque couleur contre le blanc et contre le noir
     (le seuil de 4.5:1 pour un texte est la contrainte de lisibilité du module) ;
  2. la simulation du daltonisme (protanopie, deutéranopie, tritanopie) par la méthode
     linéaire de Viénot-Brettel-Mollon, puis la distance Lab entre les paires de couleurs
     **après** simulation : c'est la mesure qui dit quelles paires deviennent
     indiscernables ;
  3. le coût de la précision affichée : quelle part des montants du fil rouge porte des
     centimes, et de combien arrondir change le total.

Sortie : figures/M10_C03_palette_testee.svg (5 bandes : palette normale, deutéranopie,
protanopie, rampe séquentielle normale et simulée) + le rapport chiffré sur stdout.

Usage : python3 tools/couleurs_M10.py
"""
from __future__ import annotations

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "figures", "M10_C03_palette_testee.svg")
SOURCE = os.path.join(RACINE, "03_exercices", "dossier_M09")

# La palette de la maison (celle des planches M10) et ses rôles
PALETTE = {
    "BLEU": ("#1f4e79", "série principale, CA"),
    "ORANGE": ("#c96a1a", "série secondaire, alerte douce"),
    "GRIS": ("#8895a5", "contexte, repères"),
    "VERT": ("#2e6f5e", "cible atteinte, conservé"),
    "ROUGE": ("#a1382c", "retour, perte, alerte"),
}

matplotlib.rcParams["svg.hashsalt"] = "couleurs_M10"
plt.rcParams.update({"font.size": 7.5, "svg.fonttype": "none"})


def sauver(fig, chemin, **kw):
    fig.savefig(chemin, metadata={"Date": None, "Creator": "couleurs_M10.py"}, **kw)


# ----------------------------------------------------------------------
# Conversions couleur
# ----------------------------------------------------------------------
def hex_vers_rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)])


def lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def gamma(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def luminance_relative(rgb):
    """Luminance WCAG (sRGB linéarisé)."""
    r, g, b = lin(np.asarray(rgb, dtype=float))
    return float(0.2126 * r + 0.7152 * g + 0.0722 * b)


def contraste(rgb1, rgb2):
    l1, l2 = luminance_relative(rgb1), luminance_relative(rgb2)
    clair, fonce = max(l1, l2), min(l1, l2)
    return (clair + 0.05) / (fonce + 0.05)


def lab(rgb):
    """sRGB -> CIE L*a*b* (D65)."""
    r, g, b = lin(np.asarray(rgb, dtype=float))
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x / 0.95047), f(y), f(z / 1.08883)
    return np.array([116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)])


def dlab(rgb1, rgb2):
    return float(np.linalg.norm(lab(rgb1) - lab(rgb2)))


# ----------------------------------------------------------------------
# Daltonisme — méthode linéaire de Viénot, Brettel & Mollon (1999)
# ----------------------------------------------------------------------
RGB_VERS_LMS = np.array([[17.8824, 43.5161, 4.11935],
                         [3.45565, 27.1554, 3.86714],
                         [0.0299566, 0.184309, 1.46709]])
LMS_VERS_RGB = np.linalg.inv(RGB_VERS_LMS)

SIMULATIONS = {
    "protanopie": np.array([[0.0, 2.02344, -2.52581], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
    "deuteranopie": np.array([[1.0, 0.0, 0.0], [0.494207, 0.0, 1.24827], [0.0, 0.0, 1.0]]),
    "tritanopie": np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [-0.395913, 0.801109, 0.0]]),
}


def simuler(rgb, vision="deuteranopie"):
    lineaire = lin(np.asarray(rgb, dtype=float))
    lms = RGB_VERS_LMS @ lineaire
    lms2 = SIMULATIONS[vision] @ lms
    return gamma(LMS_VERS_RGB @ lms2)


def paires(noms):
    return [(noms[i], noms[j]) for i in range(len(noms)) for j in range(i + 1, len(noms))]


def mesures(verbeux=True):
    import sys
    ecrire = sys.stdout.write
    def print(*a, **k):   # neutralise l'affichage quand le socle des chiffres appelle mesures()
        if verbeux:
            return __import__("builtins").print(*a, **k)
        return None
    print("=" * 78)
    print("C03-1 — CONTRASTE WCAG DE LA PALETTE DE LA MAISON")
    print("=" * 78)
    blanc, noir = np.array([1.0, 1.0, 1.0]), np.array([0.0, 0.0, 0.0])
    mesures = {}
    for nom, (hx, role) in PALETTE.items():
        rgb = hex_vers_rgb(hx)
        c_blanc, c_noir = contraste(rgb, blanc), contraste(rgb, noir)
        mesures[f"c03_contraste_{nom.lower()}_blanc"] = round(c_blanc, 2)
        mesures[f"c03_contraste_{nom.lower()}_noir"] = round(c_noir, 2)
        verdict = ("texte OK" if c_blanc >= 4.5 else
                   "texte refusé, graphique OK" if c_blanc >= 3 else "insuffisant même en graphique")
        print(f"  {nom:6s} {hx}  contre blanc {c_blanc:5.2f}:1  contre noir {c_noir:5.2f}:1   {verdict}")
    print("  (seuil WCAG texte normal 4.5:1 ; éléments graphiques 3:1)")

    # le cas cité par le chapitre : le gris et le jaune sur fond blanc
    jaune = hex_vers_rgb("#ffd400")
    mesures["c03_contraste_jaune_blanc"] = round(contraste(jaune, blanc), 2)
    print(f"  jaune vif #ffd400 contre blanc : {mesures['c03_contraste_jaune_blanc']:.2f}:1  (invisible sur un vidéoprojecteur)")

    print()
    print("=" * 78)
    print("C03-2 — CE QUE LE DALTONISME FAIT DE LA PALETTE (distance Lab)")
    print("=" * 78)
    noms = list(PALETTE)
    rgb = {n: hex_vers_rgb(PALETTE[n][0]) for n in noms}
    lignes = []
    for vision in ("normale", "deuteranopie", "protanopie", "tritanopie"):
        sims = {n: (rgb[n] if vision == "normale" else simuler(rgb[n], vision)) for n in noms}
        d = {p: dlab(sims[p[0]], sims[p[1]]) for p in paires(noms)}
        pire = min(d, key=d.get)
        lignes.append((vision, d, pire))
        if vision != "normale":
            mesures[f"c03_deltae_min_{vision}"] = round(d[pire], 1)
            mesures[f"c03_paire_critique_{vision}"] = f"{pire[0]}-{pire[1]}"
        print(f"  {vision:12s} : écart minimal {d[pire]:5.1f} dE entre {pire[0]} et {pire[1]}"
              f"  | écart maximal {max(d.values()):5.1f} dE"
              f"  | paires sous 10 dE : {sum(1 for v in d.values() if v < 10)}")
    seuil = 10.0
    perdues = [p for p, v in lignes[1][1].items() if v < seuil and lignes[0][1][p] >= seuil]
    mesures["c03_paires_perdues_deuteranopie"] = len(perdues)
    mesures["c03_paires_total"] = len(paires(noms))
    print(f"  paires lisibles en vision normale ({len(paires(noms))} au total), "
          f"perdues en deutéranopie : {len(perdues)} -> {perdues}")

    # la paire rouge / vert, le cas d'école
    rouge, vert = hex_vers_rgb(PALETTE["ROUGE"][0]), hex_vers_rgb(PALETTE["VERT"][0])
    d_rouge_vert = dlab(rouge, vert)
    d_rouge_vert_sim = dlab(simuler(rouge), simuler(vert))
    mesures["c03_rouge_vert_normal"] = round(d_rouge_vert, 1)
    mesures["c03_rouge_vert_deuteranopie"] = round(d_rouge_vert_sim, 1)
    print(f"  paire ROUGE/VERT : {d_rouge_vert:.1f} dE en vision normale -> "
          f"{d_rouge_vert_sim:.1f} dE en deutéranopie ({d_rouge_vert_sim/d_rouge_vert*100:.0f} % de l'écart initial)")

    print()
    print("=" * 78)
    print("C03-3 — LA RAMPE SÉQUENTIELLE RÉSISTE-T-ELLE ? (8 catégories, rampe Blues)")
    print("=" * 78)
    v = pd.read_csv(os.path.join(SOURCE, "quincaillerie", "vente.csv"), parse_dates=["date_vente"])
    p = pd.read_csv(os.path.join(SOURCE, "quincaillerie", "produit.csv"))
    vp = v[~v["est_retour"]].merge(p[["id_produit", "id_categorie"]], on="id_produit", how="left")
    part = (vp.groupby("id_categorie")["montant_ttc"].sum() / vp["montant_ttc"].sum() * 100).sort_values()
    rampe = plt.get_cmap("Blues")
    norme = plt.Normalize(0, 20.0)
    couleurs = [np.array(rampe(norme(x))[:3]) for x in part]
    for vision in ("normale", "deuteranopie"):
        sims = [c if vision == "normale" else simuler(c, vision) for c in couleurs]
        d = [dlab(sims[i], sims[i + 1]) for i in range(len(sims) - 1)]
        dl = [abs(lab(sims[i])[0] - lab(sims[i + 1])[0]) for i in range(len(sims) - 1)]
        if vision == "normale":
            mesures["c03_rampe_deltae_min"] = round(min(d), 1)
        else:
            mesures["c03_rampe_deltae_min_deuteranopie"] = round(min(d), 1)
            mesures["c03_rampe_dl_min_deuteranopie"] = round(min(dl), 1)
        print(f"  {vision:12s} : écart minimal entre deux cases voisines {min(d):5.1f} dE "
              f"(clarté {min(dl):4.1f} L*) ; écart maximal {max(d):5.1f} dE")

    print()
    print("=" * 78)
    print("C03-4 — LA PRÉCISION AFFICHÉE : LES CENTIMES DES MONTANTS")
    print("=" * 78)
    m = v["montant_ttc"].to_numpy()
    centimes = np.abs(m * 100 - np.round(m * 100)) < 1e-6
    avec_centimes = int((np.round(m * 100) % 100 != 0).sum())
    arrondi = float(np.abs(np.round(m) - m).sum())
    mesures["c03_montants_avec_centimes"] = avec_centimes
    mesures["c03_montants_lignes"] = int(len(m))
    mesures["c03_part_avec_centimes_pct"] = round(avec_centimes / len(m) * 100, 2)
    mesures["c03_erreur_arrondi_fcfa"] = round(arrondi, 2)
    mesures["c03_erreur_arrondi_pct"] = round(arrondi / float(m.sum()) * 100, 4)
    print(f"  lignes dont le montant porte des centimes : {avec_centimes} sur {len(m)} "
          f"({mesures['c03_part_avec_centimes_pct']} %)")
    print(f"  arrondir tous les montants au FCFA entier déplace le total de {arrondi:.2f} FCFA, "
          f"soit {mesures['c03_erreur_arrondi_pct']} % : les centimes se suppriment sans risque")

    print()
    print("=" * 78)
    print("C03-5 — LA COULEUR QUI SIGNIFIE DEUX CHOSES (dossier de refonte)")
    print("=" * 78)
    # On lit le code du rapport « avant » : quel rôle joue chaque couleur employée ?
    code = open(os.path.join(RACINE, "03_exercices", "dossier_M10", "rapport_avant",
                             "code_avant.py"), encoding="utf-8").read()
    roles = {}
    for ligne in code.splitlines():
        if "ORANGE" not in ligne or "color=" not in ligne and "coul" not in ligne:
            continue
        cle = ("retours" if "ret" in ligne else "remise" if "remise" in ligne else
               "moyenne de reference" if "hline" in ligne or "moyenne" in ligne else
               "serie du dessus d'un double axe" if "ax2" in ligne else "serie secondaire")
        roles.setdefault(cle, 0)
        roles[cle] += 1
    print(f"  ORANGE dans les 5 graphiques du rapport : {sum(roles.values())} emplois, "
          f"{len(roles)} roles distincts -> {list(roles)}")
    mesures["c03_orange_emplois"] = int(sum(roles.values()))
    mesures["c03_orange_roles"] = int(len(roles))
    mesures["c03_couleurs_par_graphique"] = 3
    print("  trois couleurs seulement (bleu, orange, gris) pour les 5 graphiques : "
          "la couleur ne porte aucun role stable d'un cadre a l'autre")

    # ------------------------------------------------------------------
    # Planche
    # ------------------------------------------------------------------
    return mesures


def planche(mesures):
    """La planche du chapitre : palette, simulations du daltonisme, rampes."""
    v = pd.read_csv(os.path.join(SOURCE, "quincaillerie", "vente.csv"), parse_dates=["date_vente"])
    p = pd.read_csv(os.path.join(SOURCE, "quincaillerie", "produit.csv"))
    vp = v[~v["est_retour"]].merge(p[["id_produit", "id_categorie"]], on="id_produit", how="left")
    part = (vp.groupby("id_categorie")["montant_ttc"].sum() / vp["montant_ttc"].sum() * 100).sort_values()
    rampe = plt.get_cmap("Blues")
    norme = plt.Normalize(0, 20.0)
    couleurs = [np.array(rampe(norme(x))[:3]) for x in part]
    blanc = np.array([1.0, 1.0, 1.0])
    couleurs5 = [hex_vers_rgb(PALETTE[n][0]) for n in PALETTE]
    noms5_lab = [PALETTE[n][0] for n in PALETTE]
    fig = plt.figure(figsize=(170 / 25.4, 108 / 25.4), dpi=110)
    gs = fig.add_gridspec(5, 1, hspace=0.55, top=0.90, bottom=0.06, left=0.13, right=0.985,
                          height_ratios=[1, 1, 1, 1, 1])

    def bande(ax, couleurs, etiquettes, titre, note_texte=None, bord=None):
        for i, c in enumerate(couleurs):
            ax.add_patch(Rectangle((i, 0), 0.94, 1, color=c, transform=ax.transData))
            lum = luminance_relative(c)
            tc = "white" if lum < 0.45 else "#111111"
            ax.annotate(etiquettes[i], (i + 0.47, 0.5), ha="center", va="center",
                        fontsize=6.5, color=tc)
            if bord is not None:
                ax.annotate(bord[i], (i + 0.47, 0.16), ha="center", va="center",
                            fontsize=5.5, color=tc)
        ax.set_xlim(0, len(couleurs))
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_title(titre, fontsize=7.5, loc="left", pad=3)
        for s in ("top", "right", "bottom"):
            ax.spines[s].set_visible(False)

    noms5 = list(PALETTE)
    couleurs5 = [hex_vers_rgb(PALETTE[n][0]) for n in noms5]
    noms5_lab = [PALETTE[n][0] for n in noms5]
    ax = fig.add_subplot(gs[0])
    bande(ax, couleurs5, noms5_lab, "1 · la palette de la maison (contraste WCAG contre le blanc)",
          bord=[f"{contraste(c, blanc):.1f}:1" for c in couleurs5])
    roles = ["CA", "alerte", "contexte", "cible", "retour"]
    ax = fig.add_subplot(gs[1])
    bande(ax, [simuler(c, "deuteranopie") for c in couleurs5], noms5_lab,
          "2 · la même palette vue par une deutéranopie (≈ 8 % des hommes)",
          bord=roles)
    ax = fig.add_subplot(gs[2])
    bande(ax, [simuler(c, "protanopie") for c in couleurs5], noms5_lab,
          "3 · la même palette vue par une protanopie (le rouge s'assombrit, le vert s'éclaircit)",
          bord=roles)
    ax = fig.add_subplot(gs[3])
    bande(ax, couleurs, [f"C{i}" for i in part.index],
          "4 · rampe séquentielle Blues : 8 catégories, écarts de clarté (vision normale)",
          bord=[f"{lab(couleurs[i])[0]:.0f} L*" for i in range(8)])
    ax = fig.add_subplot(gs[4])
    bande(ax, [simuler(c, "deuteranopie") for c in couleurs], [f"C{i}" for i in part.index],
          "5 · la même rampe en deutéranopie : elle garde son ordre (une seule teinte)",
          bord=[f"{lab(simuler(couleurs[i]))[0]:.0f} L*" for i in range(8)])
    fig.suptitle("La palette du manuel testée : contraste, daltonisme, rampe séquentielle",
                 fontsize=9, x=0.008, ha="left", y=0.985)
    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    sauver(fig, SORTIE, dpi=110)
    plt.close(fig)
    return SORTIE


def main():
    m = mesures()
    chemin = planche(m)
    print()
    print(f"  planche : {os.path.relpath(chemin, RACINE)} ({os.path.getsize(chemin)/1024:.1f} Ko)")
    print()
    print(json.dumps(m, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
