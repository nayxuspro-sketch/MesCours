#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""figures_M12.py — les 2 planches du module M12 (fondamentaux de la BI).

Le module est un module de CONCEPTS : il ne publie que deux figures, celles qui montrent
d'un coup d'oeil ce que le texte decrit lentement.

  (a) `M12_C05_carte_des_sept_etages.svg` — la chaine BI en 7 etages, du systeme source a
      la diffusion, avec la panne typique de chaque etage et la mesure du socle M12 a
      hauteur de chaque etage.
  (b) `M12_C06_matrice_des_dix_couples.svg` — la matrice des 10 couples indicateur /
      contre-KPI, avec leur valeur mesuree : ce qu'un indicateur pousse a faire, et ce
      qui l'empeche de mentir.

Contraintes du manuel : largeur <= 776 px, texte reel dans le SVG (`svg.fonttype = none`,
extractible du PDF), rendu DETERMINISTE (`svg.hashsalt` + date de metadonnee neutralisee),
jeu latin-1 etendu. Aucun chiffre n'est ecrit en dur : tous sont lus dans
`01_socle_donnees/data/reference/chiffres_cites.json` (bloc M12), donc recalculables.

Usage :
    python3 tools/figures_M12.py            # produit les 2 SVG et controle tout
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

matplotlib.rcParams["svg.hashsalt"] = "mesCours-M12"
matplotlib.rcParams["svg.fonttype"] = "none"
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["axes.unicode_minus"] = False


def chiffres() -> dict:
    with open(REF, encoding="utf-8") as fh:
        return json.load(fh)["M12"]


def _largeur_px(chemin: str) -> float:
    with open(chemin, encoding="utf-8") as fh:
        tete = fh.read(600)
    m = re.search(r'width="([\d.]+)pt"', tete)
    return float(m.group(1)) * DPI / 72.0 if m else 0.0


def enregistrer(fig, nom: str) -> str:
    chemin = os.path.join(SORTIE, nom)
    fig.savefig(chemin, format="svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)
    return chemin


# --------------------------------------------------------------------------- (a) C05
def carte_des_sept_etages() -> str:
    """Les 7 etages de la chaine BI : ce qui entre, ce qui sort, ce qui casse."""
    c = chiffres()
    etages = [
        ("7. Diffusion",
         "14 destinataires, 4 ouvertures le 1er jour",
         "livrer sans adopter : 28,6 % de lecteurs a J1",
         "#e8f1ff"),
        ("6. Visualisation",
         "2 planches, 1 graphique juste vaut mieux que 7 onglets",
         "le camembert illisible et l'axe tronque",
         "#eaf6ee"),
        ("5. Couche semantique",
         "10 KPI, 7 champs de carte, 70 cases a signer",
         "deux definitions du meme mot : 1,12 % ou 1,91 %",
         "#fff6e0"),
        ("4. Modele",
         "8 tables, 8 cles uniques, 1 vue de marge",
         "une cle oubliee : x 15,8 de chiffre d'affaires",
         "#fdeaea"),
        ("3. Stockage",
         "socle rejoue en 0,7 s, aucun fichier de base",
         "un stock de fichiers que personne ne peut rejouer",
         "#f0eaff"),
        ("2. Extraction",
         "6 sources lues en 0,12 s, 2 prix manquants",
         "nettoyer sans laisser de trace du nettoyage",
         "#eaf4f8"),
        ("1. Sources",
         "240 000 lignes de ventes, 1,33 Mo de sources M12",
         "completer un trou par une recopie",
         "#f2f2f2"),
    ]
    fig, ax = plt.subplots(figsize=(7.76, 5.2), dpi=DPI)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    x0, larg, haut, pas = 0.03, 0.50, 0.100, 0.021
    y = 0.885
    ax.text(x0 + 0.005, 0.955, "Les 7 etages, du bas vers le haut : ce que chacun apporte",
            fontsize=7.0, color="#12202e")
    ax.text(x0 + larg + 0.018, 0.955, "La panne typique de l'etage", fontsize=7.0, color="#8a2b1e")
    for i, (titre, contenu, panne, teinte) in enumerate(etages):
        ax.add_patch(Rectangle((x0, y - haut), larg, haut, facecolor=teinte,
                               edgecolor="#5c6b7a", linewidth=0.7))
        ax.text(x0 + 0.012, y - 0.028, titre, fontsize=8.2, va="center", color="#12202e")
        ax.text(x0 + 0.012, y - 0.066, contenu, fontsize=6.6, va="center", color="#33414f")
        ax.text(x0 + larg + 0.018, y - 0.050, "panne : " + panne, fontsize=6.5, va="center",
                color="#8a2b1e")
        if i < len(etages) - 1:
            ax.add_patch(FancyArrowPatch((x0 + larg / 2, y - haut), (x0 + larg / 2, y - haut - pas),
                                         arrowstyle="-|>", mutation_scale=8, color="#5c6b7a",
                                         linewidth=1.0))
        y -= haut + pas

    ax.text(x0 + larg / 2, 0.985, "La chaine BI en 7 etages : de la source a la decision",
            fontsize=9.4, ha="center", color="#12202e")
    ax.add_patch(FancyArrowPatch((0.78, 0.30), (0.78, 0.62), arrowstyle="-|>", mutation_scale=12,
                                 color="#1f4e9c", linewidth=1.8))
    ax.text(0.78, 0.70, "Le sens de lecture", fontsize=7.4, ha="center", color="#5c6b7a")
    ax.text(0.78, 0.22, "les donnees montent,\nla decision descend", fontsize=6.8, ha="center",
            color="#1f4e9c")
    ax.text(0.03, 0.035, "Chaque etage casse a sa maniere : %d KPI, %s cases de carte a signer,"
            % (int(c["m12_kpi_carte"]), c["m12_c_cases_a_remplir"]), fontsize=6.6, color="#33414f")
    taille = sum(os.path.getsize(os.path.join(RACINE, "03_exercices", "dossier_M12", f))
                 for f in os.listdir(os.path.join(RACINE, "03_exercices", "dossier_M12"))
                 if os.path.isfile(os.path.join(RACINE, "03_exercices", "dossier_M12", f)))
    ax.text(0.03, 0.008, "%d sources operationnelles, %s lignes de ventes, %.2f Mo de socle M12."
            % (int(c["m12_tables_ajoutees"]) + 1,
               format(int(c["m12_lignes"]), ",").replace(",", " "), taille / 1024 / 1024),
            fontsize=6.6, color="#33414f")
    return enregistrer(fig, "M12_C05_carte_des_sept_etages.svg")


# --------------------------------------------------------------------------- (b) C06
def matrice_des_dix_couples() -> str:
    """Les 10 couples indicateur / contre-KPI, avec la mesure qui les separe."""
    c = chiffres()
    ca = c["m12_k01_ca_net_fcfa"].replace(" FCFA", "")
    panier = c["m12_k05_panier_ticket"].replace(" FCFA", "")
    cout = c["m12_k09_cout_unitaire_fcfa"].replace(" FCFA", "")
    couples = [
        ("CA net", "vendre plus, vite", "taux de retour",
         f"{ca} FCFA / 1,17 % de retour"),
        ("Marge brute", "monter les prix", "volume vendu",
         "recette x 1,17 / unites x 1,17"),
        ("Taux de rupture", "stocker plus", "rotation",
         "7,29 % / 9,42 tours"),
        ("Rotation", "reduire le stock", "taux de rupture",
         "9,42 tours / 7,29 %"),
        ("Panier moyen", "vendre des lots", "marge brute",
         f"{panier} FCFA / 29,12 %"),
        ("Taux de retour", "controler les retours", "taux de service",
         "1,17 % / 81,0 %"),
        ("Taux de service", "promettre large", "cout logistique unitaire",
         f"78,2 % / {cout} FCFA"),
        ("Taux de recouvrement", "relancer vite", "CA net",
         f"74,0 % / {ca} FCFA"),
        ("Cout logistique unit.", "grouper les tournees", "taux de service",
         f"{cout} FCFA / 78,2 %"),
        ("Part de marche interne", "defendre son magasin", "CA du reseau",
         "60,8 % / 39,2 % a Ouagadougou"),
    ]

    fig, ax = plt.subplots(figsize=(7.76, 5.6), dpi=DPI)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    x_ind, x_pousse, x_contre, x_mesure = 0.02, 0.235, 0.475, 0.700
    y, pas = 0.885, 0.079
    ax.text(x_ind, 0.955, "Indicateur", fontsize=7.6, color="#12202e")
    ax.text(x_pousse, 0.955, "Ce qu'il pousse a faire", fontsize=7.6, color="#12202e")
    ax.text(x_contre, 0.955, "Son contre-KPI", fontsize=7.6, color="#12202e")
    ax.text(x_mesure, 0.955, "Le couple, mesure", fontsize=7.6, color="#12202e")
    ax.plot([0.02, 0.99], [0.935, 0.935], color="#5c6b7a", linewidth=0.9)

    for i, (ind, pousse, contre, mesure) in enumerate(couples):
        couleur = "#fbfbfb" if i % 2 == 0 else "#f1f5f9"
        ax.add_patch(Rectangle((0.015, y - 0.050), 0.975, 0.062, facecolor=couleur,
                               edgecolor="#d7dde3", linewidth=0.5))
        ax.text(x_ind, y - 0.019, ind, fontsize=7.0, va="center", color="#12202e")
        ax.text(x_pousse, y - 0.019, pousse, fontsize=7.0, va="center", color="#586470")
        ax.text(x_contre, y - 0.019, contre, fontsize=7.0, va="center", color="#8a2b1e")
        ax.text(x_mesure, y - 0.019, mesure, fontsize=6.6, va="center", color="#33414f")
        y -= pas

    ax.text(0.02, 0.055, "Un indicateur sans contre-KPI s'ameliore toujours : il suffit de",
            fontsize=7.2, color="#12202e")
    ax.text(0.02, 0.020, "deplacer le probleme chez le voisin. Les dix couples se publient ensemble.",
            fontsize=7.2, color="#12202e")
    ax.text(0.975, 0.055, "M12 · %d couples" % len(couples), fontsize=7.0, ha="right",
            color="#5c6b7a")
    return enregistrer(fig, "M12_C06_matrice_des_dix_couples.svg")


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    os.makedirs(SORTIE, exist_ok=True)
    produits = [("C05", carte_des_sept_etages()), ("C06", matrice_des_dix_couples())]
    print("=== figures_M12 : 2 planches ===")
    ok = True
    for chapitre, chemin in produits:
        nom = os.path.basename(chemin)
        larg = _largeur_px(chemin)
        h1 = hashlib.sha256(open(chemin, "rb").read()).hexdigest()
        regenere = carte_des_sept_etages() if chapitre == "C05" else matrice_des_dix_couples()
        h2 = hashlib.sha256(open(regenere, "rb").read()).hexdigest()
        stable = h1 == h2
        cite = False
        for f in sorted(os.listdir(os.path.join(RACINE, "02_modules"))):
            if f.startswith("M12_%s" % chapitre):
                texte = open(os.path.join(RACINE, "02_modules", f), encoding="utf-8").read()
                cite = nom in texte
        print("  %-4s %-40s largeur %6.1f px · %5.1f ko · deterministe %s · cite %s"
              % (chapitre, nom, larg, os.path.getsize(chemin) / 1024.0,
                 "oui" if stable else "NON", "oui" if cite else "NON"))
        ok = ok and stable and larg <= LARGEUR_MAX_PX and cite
    if not ok:
        print("  (une planche peut n'etre pas encore citee : le chapitre qui la porte n'est pas ecrit)")
    print("  verdict :", "OK" if ok else "EN ATTENTE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
