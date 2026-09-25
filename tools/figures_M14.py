#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""figures_M14.py — les planches du module M14 (Power BI : de l'import a la publication).

Quatre planches prevues ; celle du chapitre C01 est produite ici, les autres le seront
avec leur chapitre :

  (a) `M14_C01_ecosysteme_et_licences.svg` — les 4 surfaces de l'ecosysteme et ce que
      chacune coute, avec l'echelle des licences et le seuil F64 ;
  (b) `M14_C02_quatre_modes_de_connexion.svg` — a produire avec C02 ;
  (c) `M14_C04_modele_etoile_powerbi.svg` — a produire avec C04 ;
  (d) `M14_C08_grille_conception_enrichie.svg` — a produire avec C08.

Aucune capture d'ecran, aucun faux bouton : le module decrit des libelles, il ne les
dessine pas. Contraintes du manuel : largeur <= 776 px, texte reel dans le SVG
(`svg.fonttype = none`), rendu deterministe, jeu latin-1 (aucun accent, aucun tiret
demi-cadratin). Les chiffres sont lus dans `chiffres_cites.json` (bloc M14) : aucune
valeur n'est ecrite en dur.

Usage :
    python3 tools/figures_M14.py            # produit les planches disponibles + controle
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

matplotlib.rcParams["svg.hashsalt"] = "mesCours-M14"
matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["axes.unicode_minus"] = False


def chiffres() -> dict:
    with open(REF, encoding="utf-8") as f:
        return json.load(f)["M14"]


def f(x) -> str:
    return "{:,}".format(int(round(float(x)))).replace(",", " ")


def sans_unite(valeur) -> str:
    return re.sub(r"\s*(FCFA|unites|%)$", "", str(valeur))


def _largeur_px(chemin: str) -> float:
    m = re.search(r'width="([\d.]+)pt"', open(chemin, encoding="utf-8").read())
    return float(m.group(1)) * DPI / 72.0 if m else 0.0


def enregistrer(fig, nom: str) -> str:
    chemin = os.path.join(SORTIE, nom)
    fig.savefig(chemin, format="svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)
    return chemin


# --------------------------------------------------------------------------- (a) C01
def ecosysteme_et_licences() -> str:
    """Quatre surfaces, quatre reponses a la question « et ca coute combien ? »."""
    c = chiffres()
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.text(50, 98.5, "L'ecosysteme Power BI : quatre surfaces, et ce que chacune coute",
            ha="center", va="top", fontsize=9.4, fontweight="bold", color="#1b1b1b")
    ax.text(50, 93.5, "prix de septembre 2026, au taux pedagogique de 600 FCFA pour 1 USD",
            ha="center", va="top", fontsize=7.2, color="#555")

    surfaces = (
        ("Desktop", "creer et analyser\nsur son poste", "GRATUIT",
         "aucune licence,\naucun compte", "#e8f4ea", "#2f7d4f"),
        ("Service", "publier, partager,\nactualiser", "PRO",
         "%s par\nutilisateur et par mois" % sans_unite(c["m14_prix_pro_fcfa"]),
         "#fdf3e3", "#b07a1e"),
        ("Fabric", "la plateforme :\nentrepot et flux", "CAPACITE",
         "des F%d : les lecteurs\nne paient plus" % c["m14_prix_f64_unites"], "#e9eef7", "#2f5d9e"),
        ("Mobile", "consulter\na distance", "INCLUS",
         "lire ce que l'on a\nle droit de voir", "#f2ecf7", "#6b4b9e"),
    )
    largeur, ecart = 22.0, 2.6
    x = 3.0
    for nom, role, pastille, detail, fond, bord in surfaces:
        ax.add_patch(Rectangle((x, 46), largeur, 42, facecolor=fond, edgecolor=bord, lw=1.3))
        ax.text(x + largeur / 2, 84.5, nom, ha="center", va="top", fontsize=10.0,
                fontweight="bold", color=bord)
        ax.text(x + largeur / 2, 79.4, role, ha="center", va="top", fontsize=7.5, color="#333",
                linespacing=1.5)
        ax.text(x + largeur / 2, 68.5, pastille, ha="center", va="top", fontsize=8.4,
                fontweight="bold", color=bord, bbox=dict(boxstyle="round,pad=0.28",
                                                         facecolor="white", edgecolor=bord, lw=0.9))
        ax.text(x + largeur / 2, 61.0, detail, ha="center", va="top", fontsize=7.2, color="#333",
                linespacing=1.6)
        x += largeur + ecart

    ax.text(3.0, 41.0, "L'echelle des licences, du gratuit au capacitaire", ha="left", va="top",
            fontsize=8.4, fontweight="bold", color="#1b1b1b")
    etapes = (
        ("Desktop", "0 FCFA", "#2f7d4f"),
        ("Pro", "%s / utilisateur" % sans_unite(c["m14_prix_pro_fcfa"]), "#b07a1e"),
        ("Premium Per User", "%s / utilisateur" % sans_unite(c["m14_prix_ppu_fcfa"]), "#b05a1e"),
        ("Fabric F%d" % c["m14_prix_f64_unites"], "lecteurs gratuits", "#2f5d9e"),
    )
    y = 29.5
    x = 3.0
    for i, (nom, prix, couleur) in enumerate(etapes):
        larg = 22.0
        ax.add_patch(Rectangle((x, y), larg, 8.0, facecolor="white", edgecolor=couleur, lw=1.2))
        ax.text(x + 1.6, y + 5.4, nom, ha="left", va="center", fontsize=7.8, fontweight="bold",
                color=couleur)
        ax.text(x + 1.6, y + 2.2, prix, ha="left", va="center", fontsize=7.0, color="#333")
        if i < len(etapes) - 1:
            ax.add_patch(FancyArrowPatch((x + larg + 0.3, y + 4.0), (x + larg + 2.2, y + 4.0),
                                         arrowstyle="-|>", mutation_scale=10, color="#8a8a8a",
                                         lw=1.1, shrinkA=0, shrinkB=0))
        x += larg + 2.5
    ax.text(3.0, 27.4,
            "Le seuil F%d est le seul point de rupture : en dessous, chaque lecteur a besoin d'une licence ; "
            "a partir de la,\nles lecteurs consultent gratuitement, et l'on paie la puissance au mois plutot "
            "qu'a la personne." % c["m14_prix_f64_unites"],
            ha="left", va="top", fontsize=7.2, color="#333", linespacing=1.6)

    ax.add_patch(Rectangle((3.0, 5.0), 94.0, 17.0, facecolor="#f7f7f4", edgecolor="#c9c9c0", lw=1.1))
    ax.text(5.0, 20.0, "Ce que le fil rouge demande, en regard", ha="left", va="top", fontsize=8.2,
            fontweight="bold", color="#1b1b1b")
    ax.text(5.0, 16.6,
            "%s lignes de ventes · modele de %d Go en Pro, %d Go en Premium Per User"
            % (c["m14_import_ventes_lignes"], c["m14_prix_modele_pro_go"],
               c["m14_prix_modele_ppu_go"]),
            ha="left", va="top", fontsize=7.3, color="#333")
    ax.text(5.0, 13.0,
            "%d puis %d actualisations par jour · une journee de ventes se recharge la nuit"
            % (c["m14_prix_actualisations_pro"], c["m14_prix_actualisations_ppu"]),
            ha="left", va="top", fontsize=7.3, color="#333")
    ax.text(5.0, 9.4,
            "Le mode de connexion se decide sur la fraicheur attendue, pas sur la taille du fichier.",
            ha="left", va="top", fontsize=7.3, color="#333")

    return enregistrer(fig, "M14_C01_ecosysteme_et_licences.svg")



# --------------------------------------------------------------------------- (b) C02
def quatre_modes_de_connexion() -> str:
    """Les quatre modes de connexion : ou vit la donnee, et ce que cela coute."""
    c = chiffres()
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.text(50, 98.5, "Quatre facons de brancher la donnee sur un rapport",
            ha="center", va="top", fontsize=9.4, fontweight="bold", color="#1b1b1b")
    ax.text(50, 93.6,
            "la question n'est jamais « quel mode est le meilleur », mais « quelle fraicheur ce rapport exige »",
            ha="center", va="top", fontsize=7.2, color="#555")

    modes = (
        ("Import", "la copie", "#e8f4ea", "#2f7d4f",
         ("une copie rangee\ndans le modele",
          "aussi fraiche que la\nderniere actualisation",
          "oui : le rapport\ns'ouvre sans reseau",
          "%s lignes relues\na chaque fois" % c["m14_import_ventes_lignes"])),
        ("DirectQuery", "le robinet", "#fdf3e3", "#b07a1e",
         ("la donnee reste\ndans la source",
          "a la seconde,\na chaque visuel",
          "non : sans source,\nplus rien",
          "une requete par\nvisuel et par clic")),
        ("Connexion directe", "le modele du voisin", "#e9eef7", "#2f5d9e",
         ("un modele deja\nconstruit ailleurs",
          "celle du modele\nque l'on consomme",
          "non",
          "aucune : le modele\nn'est pas copie")),
        ("Direct Lake", "la citerne", "#f2ecf7", "#6b4b9e",
         ("les fichiers de la\nplateforme, lus sur place",
          "a la seconde,\nsans requete SQL",
          "non : la plateforme\nrepond",
          "aucune : la lecture\nse fait sur le fichier")),
    )
    largeur, ecart = 22.4, 2.6
    x = 2.8
    lignes = ("Ou vit la donnee", "Fraicheur", "Hors ligne", "Cout d'une actualisation")
    for nom, sous_titre, fond, bord, details in modes:
        ax.add_patch(Rectangle((x, 12.0), largeur, 76.0, facecolor=fond, edgecolor=bord, lw=1.3))
        ax.text(x + largeur / 2, 85.0, nom, ha="center", va="top", fontsize=9.2,
                fontweight="bold", color=bord)
        ax.text(x + largeur / 2, 80.6, sous_titre, ha="center", va="top", fontsize=7.0,
                color="#666", style="italic")
        y = 73.0
        for titre, detail in zip(lignes, details):
            ax.text(x + 1.6, y, titre, ha="left", va="top", fontsize=6.6, color="#777")
            ax.text(x + 1.6, y - 3.4, detail, ha="left", va="top", fontsize=7.0, color="#222",
                    linespacing=1.5)
            y -= 15.6
        x += largeur + ecart

    ax.text(2.8, 8.0,
            "Le fil rouge se decide sur trois mesures : %s lignes, dont %s pour le seul mois de 2026-08 (%s %% du total),"
            % (c["m14_import_ventes_lignes"], c["m14_c02_dernier_mois_lignes"],
               str(c["m14_c02_dernier_mois_pct"]).replace(".", ",")),
            ha="left", va="top", fontsize=7.0, color="#333")
    ax.text(2.8, 4.6,
            "et un fichier qui passe de %s Mo a %s Mo une fois range au format colonne (facteur %s)."
            % (str(c["m14_c02_ventes_mo_plein"]).replace(".", ","),
               str(c["m14_c02_parquet_mo"]).replace(".", ","),
               str(c["m14_c02_parquet_ratio"]).replace(".", ",")),
            ha="left", va="top", fontsize=7.0, color="#333")
    return enregistrer(fig, "M14_C02_quatre_modes_de_connexion.svg")


PLANCHES = {"M14_C01_ecosysteme_et_licences.svg": ecosysteme_et_licences,
            "M14_C02_quatre_modes_de_connexion.svg": quatre_modes_de_connexion}

A_PRODURE = ("M14_C04_modele_etoile_powerbi.svg",
             "M14_C08_grille_conception_enrichie.svg")


def controler(chemins):
    defauts = []
    for chemin in chemins:
        largeur = _largeur_px(chemin)
        texte = open(chemin, encoding="utf-8").read()
        if largeur > LARGEUR_MAX_PX:
            defauts.append("%s : %.0f px (max %d)" % (os.path.basename(chemin), largeur,
                                                      LARGEUR_MAX_PX))
        if "<text" not in texte:
            defauts.append("%s : aucun texte extractible" % os.path.basename(chemin))
        if "\u2013" in texte:
            defauts.append("%s : tiret demi-cadratin interdit" % os.path.basename(chemin))
        try:
            texte.encode("latin-1")
        except UnicodeEncodeError as e:
            defauts.append("%s : hors latin-1 (%s)" % (os.path.basename(chemin), e.start))
        print("  %-44s %.0f px · %d octets · %d caracteres de texte"
              % (os.path.basename(chemin), largeur, len(texte.encode()),
                 len(re.findall(r"<text", texte))))
    return defauts


def main(argv=None):
    argv = argv or sys.argv[1:]
    os.makedirs(SORTIE, exist_ok=True)
    chemins = [PLANCHES[nom]() for nom in sorted(PLANCHES)]
    print("=== planches M14 ===")
    defauts = controler(chemins)
    for nom in A_PRODURE:
        if not os.path.exists(os.path.join(SORTIE, nom)):
            print("  %-44s a produire avec son chapitre" % nom)
    if defauts:
        print("DEFAUTS :")
        for d in defauts:
            print("  -", d)
        return 1
    print("  empreinte :", hashlib.sha256(
        b"".join(open(c, "rb").read() for c in sorted(chemins))).hexdigest()[:16])
    return 0


if __name__ == "__main__":
    sys.exit(main())
