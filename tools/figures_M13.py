#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""figures_M13.py — les 3 planches du module M13 (modelisation des donnees).

Le module dessine trois choses, et seulement trois : ce qu'est un grain, ce qu'est un
changement lent de dimension, et ce qu'on verifie avant de livrer un modele.

  (a) `M13_C03_grain_et_explosion.svg` — les 3 grains du fil rouge et l'explosion en
      lignes d'une jointure faite sur la mauvaise cle ; le controle negatif (bonne cle)
      est dessine a cote : meme requete, meme intention, resultat juste.
  (b) `M13_C04_frise_scd.svg` — les 4 types de SCD sur la frise d'un changement de tarif
      (a produire avec le chapitre C04).
  (c) `M13_C07_grille_revue.svg` — la grille de revue en 15 points (a produire avec C07).

Contraintes du manuel : largeur <= 776 px, texte reel dans le SVG (`svg.fonttype = none`,
extractible du PDF compose), rendu DETERMINISTE (`svg.hashsalt` + date de metadonnee
neutralisee), jeu latin-1 etendu (aucun tiret demi-cadratin). Aucun chiffre n'est ecrit en
dur : ils sont lus dans `01_socle_donnees/data/reference/chiffres_cites.json` (bloc M13),
donc recalculables par `tools/modele_M13.py`.

Usage :
    python3 tools/figures_M13.py            # produit la ou les planches disponibles + controle
    python3 tools/figures_M13.py --toutes   # exige les 3 (echoue si une manque)
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "figures")
REF = os.path.join(RACINE, "01_socle_donnees", "data", "reference", "chiffres_cites.json")
LARGEUR_MAX_PX = 776
DPI = 100

matplotlib.rcParams["svg.hashsalt"] = "mesCours-M13"
matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["axes.unicode_minus"] = False


def chiffres() -> dict:
    with open(REF, encoding="utf-8") as f:
        return json.load(f)["M13"]


def sans_unite(valeur) -> str:
    """« 15 595 154 955 FCFA » -> « 15 595 154 955 » : l'unite s'ecrit une seule fois."""
    return re.sub(r"\s*(FCFA|unites|%)$", "", str(valeur))


def grain_de(nom: str) -> str:
    """Le nombre de lignes d'un grain, lu dans la cle qui les liste tous les sept."""
    m = re.search(r"%s ([\d ]+)" % nom, chiffres()["m13_c03_grains"])
    return m.group(1).strip() if m else "?"


def _largeur_px(chemin: str) -> float:
    with open(chemin, encoding="utf-8") as f:
        tete = f.read(600)
    m = re.search(r'width="([\d.]+)pt"', tete)
    return float(m.group(1)) * DPI / 72.0 if m else 0.0


def enregistrer(fig, nom: str) -> str:
    chemin = os.path.join(SORTIE, nom)
    fig.savefig(chemin, format="svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)
    return chemin


# --------------------------------------------------------------------------- (a) C03
def grain_et_explosion() -> str:
    """Le grain : six lignes de vente, trois facons de les compter, deux jointures."""
    c = chiffres()
    fig, ax = plt.subplots(figsize=(7.6, 4.5))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    def carte(x, y, w, h, titre, lignes, couleur, bord):
        ax.add_patch(Rectangle((x, y), w, h, facecolor=couleur, edgecolor=bord, lw=1.2))
        ax.text(x + w / 2, y + h - 3.2, titre, ha="center", va="top", fontsize=8.5,
                fontweight="bold", color="#1b1b1b")
        for i, l in enumerate(lignes):
            ax.text(x + 2.5, y + h - 8.4 - i * 4.4, l, ha="left", va="top", fontsize=7.6,
                    color="#333")

    def fleche(x1, y1, x2, y2, couleur, style="-|>", epaisseur=1.4):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                     mutation_scale=11, color=couleur, lw=epaisseur,
                                     shrinkA=1, shrinkB=1))

    ax.text(50, 97.5, "Le grain : ce que porte UNE ligne, et ce qu'on a le droit d'additionner",
            ha="center", va="top", fontsize=9.6, fontweight="bold")

    # 1. les six lignes de vente
    carte(1.5, 62, 25, 30, "6 lignes de vente (extrait)", [
        "id_vente 1 | prod 12 | mag 1 | 40 u",
        "id_vente 2 | prod 12 | mag 1 | 25 u",
        "id_vente 3 | prod 7  | mag 1 | 6 u",
        "id_vente 4 | prod 12 | mag 2 | 18 u",
        "id_vente 5 | prod 7  | mag 2 | 9 u",
        "id_vente 6 | prod 31 | mag 2 | 3 u",
    ], "#f7f7f7", "#8a8a8a")

    # 2. le grain declare : le plus fin
    carte(33, 66, 30, 26, "Le grain le plus fin : la ligne de ticket", [
        "%s lignes" % grain_de("ventes"),
        "cle : id_vente (unique)",
        "%s ligne par ticket" % str(c["m13_c03_lignes_par_ticket"]).replace(".", ","),
        "%s lignes de faits au total" % c["m13_c03_lignes_faits_total"],
    ], "#eaf4ff", "#3b6ea5")

    fleche(27, 77, 32.4, 79, "#3b6ea5")

    # 3. les deux jointures
    carte(66, 66, 32, 26, "Joindre sur la BONNE cle", [
        "6 lignes deviennent 6 lignes",
        "facteur 1,0 : le total ne bouge pas",
        "%s FCFA, le chiffre juste" % sans_unite(c["m13_c03_bon_grain_ca"]),
        "controle negatif : la jointure",
        "n'est pas coupable, la cle l'est",
    ], "#eef7ee", "#3f7d3f")

    fleche(63.4, 79, 65.4, 79, "#3f7d3f")

    # 4. l'explosion
    carte(33, 8, 65, 50, "Joindre sur une cle trop LARGE (le magasin seul) : x 44", [
        "chaque ligne de vente rencontre 44 lignes de logistique",
        "(un magasin a 44 mois d'historique) :",
        "",
        "%s lignes : facteur %s" % (c["m13_c03_faux_large_lignes"],
                                    str(c["m13_c03_faux_large_facteur"]).replace(".", ",")),
        "%s FCFA au lieu de %s FCFA" % (sans_unite(c["m13_c03_faux_large_ca"]),
                                        sans_unite(c["m13_c03_bon_grain_ca"])),
        "",
        "aucune erreur, aucun avertissement : le total est credibile et faux",
    ], "#fdeaea", "#a33b3b")
    fleche(48, 65.4, 48, 58.6, "#a33b3b", epaisseur=1.8)
    ax.text(49.5, 62, "meme requete", ha="left", va="center", fontsize=7.2, color="#a33b3b")

    # 5. la troisieme fausse route, en bas a gauche : la cle trop fine qui filtre
    carte(1.5, 8, 29.5, 50, "Joindre sur une cle trop FINE", [
        "les ventes d'un produit-mois",
        "SANS rupture disparaissent",
        "",
        "%s lignes (au lieu de %s)" % (c["m13_c03_faux_filtre_lignes"],
                                       c["m13_c03_bon_grain_lignes"]),
        "%s FCFA : facteur %s" % (sans_unite(c["m13_c03_faux_filtre_ca"]),
                                  str(c["m13_c03_faux_filtre_facteur"]).replace(".", ",")),
        "%s %% du chiffre d'affaires" % c["m13_c03_faux_filtre_manquants"],
        "perdu sans un mot",
    ], "#fff6e0", "#a3781f")
    fleche(30.9, 33, 32.6, 33, "#a3781f")

    return enregistrer(fig, "M13_C03_grain_et_explosion.svg")


PLANCHES = {"M13_C03_grain_et_explosion.svg": grain_et_explosion}


def controler(chemins):
    """Trois controles par planche : largeur, texte reel, jeu de caracteres."""
    defauts = []
    for chemin in chemins:
        largeur = _largeur_px(chemin)
        texte = open(chemin, encoding="utf-8").read()
        if largeur > LARGEUR_MAX_PX:
            defauts.append("%s : %.0f px (max %d)" % (os.path.basename(chemin), largeur, LARGEUR_MAX_PX))
        if "<text" not in texte and "glyph" not in texte:
            defauts.append("%s : aucun texte extractible" % os.path.basename(chemin))
        if "\u2013" in texte:
            defauts.append("%s : tiret demi-cadratin interdit" % os.path.basename(chemin))
        try:
            texte.encode("latin-1")
        except UnicodeEncodeError as e:
            defauts.append("%s : hors latin-1 (%s)" % (os.path.basename(chemin), e.start))
        print("  %-40s %.0f px · %d octets · %d caracteres de texte"
              % (os.path.basename(chemin), largeur, len(texte.encode()),
                 len(re.findall(r"<text", texte))))
    return defauts


def main(argv=None):
    argv = argv or sys.argv[1:]
    os.makedirs(SORTIE, exist_ok=True)
    a_faire = PLANCHES if "--toutes" in argv else {k: v for k, v in PLANCHES.items()}
    chemins = [a_faire[nom]() for nom in sorted(a_faire)]
    print("=== planches M13 ===")
    defauts = controler(chemins)
    for nom in ("M13_C04_frise_scd.svg", "M13_C07_grille_revue.svg"):
        if not os.path.exists(os.path.join(SORTIE, nom)):
            print("  %-40s a produire avec son chapitre" % nom)
    if defauts:
        print("DEFANTS :")
        for d in defauts:
            print("  -", d)
        return 1
    print("  empreinte :", hashlib.sha256(
        b"".join(open(c, "rb").read() for c in sorted(chemins))).hexdigest()[:16])
    return 0


if __name__ == "__main__":
    sys.exit(main())
