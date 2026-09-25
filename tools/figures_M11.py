#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""figures_M11.py — les 2 planches du module M11 (SQL avance pour la BI).

Le module est un module de REQUETES : il ne publie que deux figures, celles qui montrent
une notion que le texte decrit mal.

  (a) `M11_C01_carte_des_fenetres.svg` — la carte des fenetres : partition, ordre, cadre,
      sur un extrait de table.
  (b) `M11_C04_matrice_retention.svg` — la matrice de retention par cohorte, en triangle
      (les cases non observables sont grisees, pas nulles).

Les deux planches respectent les contraintes du manuel : largeur <= 776 px, jeu latin-1
etendu, rendu DETERMINISTE (`svg.hashsalt` + date de metadonnee neutralisee).

Usage :
    python3 tools/figures_M11.py            # produit les 2 SVG et controle tout
    python3 tools/figures_M11.py --apercu   # produit, puis affiche dimensions et poids
"""
from __future__ import annotations

import hashlib
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "figures")
DOSSIER = os.path.join(RACINE, "03_exercices", "dossier_M11")
LARGEUR_MAX_PX = 776
DPI = 100

matplotlib.rcParams["svg.hashsalt"] = "mesCours-M11"
matplotlib.rcParams["svg.fonttype"] = "none"   # texte reel dans le SVG : extractible du PDF
matplotlib.rcParams["font.family"] = "DejaVu Sans"
matplotlib.rcParams["axes.unicode_minus"] = False


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


# --------------------------------------------------------------------------- (a) C01
def carte_des_fenetres() -> str:
    """Partition, ordre, cadre : la table, les frontieres et la fenetre courante."""
    fig, ax = plt.subplots(figsize=(7.6, 3.9), dpi=DPI)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    lignes = [
        ("2026-01", "Kaya", 12, 1), ("2026-02", "Kaya", 12, 2),
        ("2026-03", "Kaya", 12, 3), ("2026-04", "Kaya", 12, 4),
        ("2026-01", "Bobo", 12, 1), ("2026-02", "Bobo", 12, 2),
        ("2026-03", "Bobo", 12, 3), ("2026-04", "Bobo", 12, 4),
    ]
    x0, larg, haut = 0.10, 0.30, 0.083
    y = 0.80
    for i, (mois, magasin, _, rg) in enumerate(lignes):
        cadre = i == 2                       # la ligne courante
        couleur = "#cfe3ff" if cadre else "#f4f4f4"
        ax.add_patch(Rectangle((x0, y - haut), larg, haut, facecolor=couleur,
                               edgecolor="#8a8a8a", linewidth=0.6))
        ax.text(x0 + 0.015, y - haut / 2, "%s · %s" % (magasin, mois), fontsize=7.5,
                va="center", color="#202020")
        if i == 1:
            ax.add_patch(Rectangle((x0, y - haut), larg, 3 * haut, facecolor="none",
                                   edgecolor="#1f4e9c", linewidth=1.6))
        ax.text(x0 + larg + 0.02, y - haut / 2, "rang %d" % rg, fontsize=7, va="center",
                color="#404040")
        y -= haut

    # les deux partitions
    for yb, nom in ((0.80, "partition 1 : Kaya"), (0.80 - 4 * haut, "partition 2 : Bobo")):
        ax.annotate("", xy=(x0 - 0.005, yb), xytext=(x0 - 0.005, yb - 4 * haut),
                    arrowprops=dict(arrowstyle="-", color="#1f4e9c", linewidth=2.2))
        ax.text(x0 - 0.02, yb - 2 * haut, nom, fontsize=7.5, rotation=90, va="center",
                ha="center", color="#1f4e9c")

    # l'ordre
    ax.add_patch(FancyArrowPatch((x0 + larg + 0.13, 0.80), (x0 + larg + 0.13, 0.80 - 4 * haut),
                                 arrowstyle="-|>", mutation_scale=12, color="#8c5a00",
                                 linewidth=1.6))
    ax.text(x0 + larg + 0.15, 0.80 - 2 * haut, "ORDER BY mois", fontsize=7.5, rotation=270,
            va="center", color="#8c5a00")

    # le cadre
    ax.add_patch(FancyArrowPatch((x0 + 0.02, 0.80 - 3 * haut - 0.03),
                                 (x0 + larg - 0.02, 0.80 - 3 * haut - 0.03),
                                 arrowstyle="<|-|>", mutation_scale=10, color="#b00020",
                                 linewidth=1.4))
    ax.text(x0 + larg / 2, 0.80 - 3.6 * haut, "cadre : 2 lignes avant + la courante",
            fontsize=7.5, ha="center", color="#b00020")
    ax.text(x0 + larg / 2, 0.90, "Partition, ordre, cadre : la carte des fenetres",
            fontsize=9.0, ha="center", color="#202020")
    ax.text(x0 + larg / 2, 0.10, "La partition separe les groupes de lignes.",
            fontsize=7.5, ha="center", color="#404040")
    ax.text(x0 + larg / 2, 0.03, "Le cadre decide ce qui entre dans le calcul.",
            fontsize=7.5, ha="center", color="#404040")
    return enregistrer(fig, "M11_C01_carte_des_fenetres.svg")


# --------------------------------------------------------------------------- (b) C04
def matrice_retention() -> str:
    """La matrice de retention : 44 cohortes, 13 anciennetes, et le triangle des cases vides."""
    try:
        import duckdb
    except ImportError as e:                       # pragma: no cover
        raise SystemExit("duckdb indisponible (%s) : installer duckdb avant de produire la planche" % e)

    os.chdir(RACINE)                               # les vues du socle sont relatives a la racine
    con = duckdb.connect()
    con.execute(open(os.path.join(DOSSIER, "socle_m11.sql"), encoding="utf-8").read())
    lignes = con.execute("""
        WITH p AS (SELECT id_client, date_trunc('month', MIN(date_vente)) co FROM ventes
                   WHERE NOT est_retour GROUP BY 1),
             a AS (SELECT DISTINCT id_client, date_trunc('month', date_vente) m FROM ventes
                   WHERE NOT est_retour),
             t AS (SELECT co, COUNT(*) n0 FROM p GROUP BY 1),
             b AS (SELECT p.co, t.n0, DATEDIFF('month', p.co, a.m) k,
                          COUNT(DISTINCT a.id_client) actifs
                   FROM p JOIN a USING (id_client) JOIN t USING (co) GROUP BY 1, 2, 3)
        SELECT strftime(co, '%Y-%m'), n0, k, ROUND(100.0 * actifs / n0, 1)
        FROM b WHERE k BETWEEN 0 AND 12 ORDER BY co, k""").fetchall()
    con.close()

    cohortes = sorted({r[0] for r in lignes})
    tailles = {r[0]: r[1] for r in lignes}
    valeurs = {(r[0], r[2]): r[3] for r in lignes}

    fig, ax = plt.subplots(figsize=(7.6, 6.2), dpi=DPI)
    ax.set_xlim(-0.5, 13.6)
    ax.set_ylim(len(cohortes) - 0.5, -1.4)
    ax.axis("off")

    for i, co in enumerate(cohortes):
        for k in range(13):
            v = valeurs.get((co, k))
            x = k
            if k == 0:
                ax.add_patch(Rectangle((x - 0.45, i - 0.45), 0.9, 0.9,
                                       facecolor="#dfe3e8", edgecolor="none"))
                ax.text(x, i, "100", fontsize=5.4, ha="center", va="center", color="#333333")
            elif v is None:
                ax.add_patch(Rectangle((x - 0.45, i - 0.45), 0.9, 0.9,
                                       facecolor="#f2f2f2", edgecolor="#e0e0e0",
                                       linewidth=0.4, hatch="///"))
            else:
                intensite = min(v / 25.0, 1.0)
                ax.add_patch(Rectangle((x - 0.45, i - 0.45), 0.9, 0.9,
                                       facecolor=(1 - 0.75 * intensite, 1 - 0.35 * intensite,
                                                  1 - 0.15 * intensite),
                                       edgecolor="white", linewidth=0.4))
                ax.text(x, i, ("%d" % round(v)) if v >= 10 else "", fontsize=5.2,
                        ha="center", va="center", color="#1f2933")

    for k in range(13):
        ax.text(k, -0.9, "M+%d" % k, fontsize=6.4, ha="center", color="#404040")
    for i, co in enumerate(cohortes):
        if i % 3 == 0:
            ax.text(-0.9, i, "%s (%d)" % (co, tailles[co]), fontsize=5.6, ha="right",
                    va="center", color="#404040")

    ax.text(6.0, -1.35, "Retention par cohorte de premiere commande, en %",
            fontsize=7.6, ha="center", color="#202020")
    ax.text(6.0, -1.05, "case grisee : recul insuffisant",
            fontsize=7.0, ha="center", color="#808080")
    ax.text(6.0, len(cohortes) + 0.2, "Une matrice de retention s'arrete en triangle",
            fontsize=8.0, ha="center", color="#202020")
    return enregistrer(fig, "M11_C04_matrice_retention.svg")


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    os.makedirs(SORTIE, exist_ok=True)
    produits = [("C01", carte_des_fenetres()), ("C04", matrice_retention())]
    print("=== figures_M11 : 2 planches ===")
    ok = True
    for chapitre, chemin in produits:
        nom = os.path.basename(chemin)
        larg = _largeur_px(chemin)
        # determinisme : deux productions, meme empreinte
        h1 = hashlib.sha256(open(chemin, "rb").read()).hexdigest()
        regenere = carte_des_fenetres() if chapitre == "C01" else matrice_retention()
        h2 = hashlib.sha256(open(regenere, "rb").read()).hexdigest()
        stable = h1 == h2
        cite = False
        for f in sorted(os.listdir(os.path.join(RACINE, "02_modules"))):
            if f.startswith("M11_%s" % chapitre):
                texte = open(os.path.join(RACINE, "02_modules", f), encoding="utf-8").read()
                cite = nom in texte
        print("  %-4s %-38s largeur %6.1f px · %5.1f ko · deterministe %s · cite %s"
              % (chapitre, nom, larg, os.path.getsize(chemin) / 1024.0,
                 "oui" if stable else "NON", "oui" if cite else "NON"))
        ok = ok and stable and larg <= LARGEUR_MAX_PX and cite
    print("  verdict :", "OK" if ok else "A CORRIGER")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
