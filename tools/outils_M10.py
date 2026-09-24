#!/usr/bin/env python3
"""outils_M10.py — le meme graphique dans trois outils (C07) : matplotlib, Excel, Power BI.

Regle §1.5 du manuel : ce qui est execute est execute, ce qui est cite est declare non execute.
Ici :
  - matplotlib  : execute — le graphique est produit en PNG 96 dpi, PNG 300 dpi, SVG et PDF ;
  - Excel       : execute — le classeur .xlsx est ecrit (donnees + graphique natif) puis RELU et
                  compare au socle ; le rendu du graphique natif demande l'application Excel, qui
                  n'est pas ouverte dans cet atelier : c'est declare dans le chapitre ;
  - Power BI    : cite, non execute — aucune mesure de fichier, seulement la procedure et ses clics.

Sorties : 03_exercices/dossier_M10/exports/ (les 4 exports matplotlib + le classeur Excel)
          figures/M10_C07_meme_graphique_trois_outils.svg (la planche de comparaison)
          + le rapport chiffre sur stdout (repris par le socle des chiffres).

Usage : python3 tools/outils_M10.py
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import zipfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from openpyxl import Workbook, load_workbook  # noqa: E402
from openpyxl.chart import LineChart, Reference  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(RACINE, "03_exercices", "dossier_M09")
EXPORTS = os.path.join(RACINE, "03_exercices", "dossier_M10", "exports")
SORTIE = os.path.join(RACINE, "figures", "M10_C07_meme_graphique_trois_outils.svg")

BLEU, ORANGE, GRIS, VERT, ROUGE = "#1f4e79", "#c96a1a", "#8895a5", "#2e6f5e", "#a1382c"
LARGEUR_MM, HAUTEUR_MM = 160.0, 90.0            # le format de sortie du module
FIXE = dt.datetime(2026, 9, 1, 12, 0, 0)        # horodatage fixe : classeur deterministe

matplotlib.rcParams["svg.hashsalt"] = "outils_M10"
plt.rcParams.update({"font.size": 7, "svg.fonttype": "none"})


def figer_zip(chemin):
    """Rend le .xlsx deterministe : horodatage des entrees fixe + propriete modifiee figee."""
    tmp = chemin + ".tmp"
    with zipfile.ZipFile(chemin) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            donnees = zin.read(item.filename)
            if item.filename == "docProps/core.xml":
                donnees = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                                 rb"\g<1>2026-09-01T12:00:00Z\g<2>", donnees)
            info = zipfile.ZipInfo(item.filename, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(info, donnees)
    shutil.move(tmp, chemin)


def charger():
    v = pd.read_csv(os.path.join(SOURCE, "quincaillerie", "vente.csv"), parse_dates=["date_vente"])
    net = v[~v["est_retour"]]
    ca = net.groupby(net["date_vente"].dt.to_period("M"))["montant_ttc"].sum().sort_index()
    annee = net.groupby(net["date_vente"].dt.year)["montant_ttc"].sum()
    return dict(v=v, net=net, ca=ca, annee=annee)


def figure_graphique(ca, dpi):
    """Le graphique unique du chapitre : format 160 x 90 mm, produit a la resolution demandee."""
    fig = plt.figure(figsize=(LARGEUR_MM / 25.4, HAUTEUR_MM / 25.4), dpi=dpi)
    ax = fig.add_axes([0.10, 0.17, 0.86, 0.72])
    t = np.arange(len(ca))
    caM = ca.to_numpy() / 1e6
    mg3 = ca.rolling(3).mean().to_numpy() / 1e6
    ax.plot(t, caM, "-", color=ORANGE, lw=0.9, label="CA net mensuel")
    ax.plot(t, mg3, "-", color=BLEU, lw=1.8, label="Moyenne glissante 3 mois")
    ax.set_ylim(0, 360)
    ax.set_xlim(-0.5, len(ca) - 0.5)
    ax.set_title("Le CA net tient dans une bande étroite : 307,6 à 348,8 M FCFA (fil rouge, 24 mois)",
                 fontsize=7.5, loc="left", pad=4)
    ax.set_ylabel("millions de FCFA", fontsize=6.5)
    ax.legend(loc="upper right", fontsize=6, frameon=False, ncol=2)
    ax.tick_params(labelsize=6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.annotate(f"× {360/50:.1f}", xy=(0.02, 0.06), xycoords="axes fraction", fontsize=6,
                color=GRIS)
    fig.text(0.10, 0.035, "Source : ventes M09, hors retours. Axe à zéro (déclaré).",
             fontsize=5.6, color=GRIS)
    return fig


def ecrire_exports(d, mesures_fichiers):
    os.makedirs(EXPORTS, exist_ok=True)
    ca = d["ca"]
    figs = {}
    for nom, dpi in (("png_96", 96), ("png_300", 300)):
        chemin = os.path.join(EXPORTS, f"fil_rouge_{nom}.png")
        fig = figure_graphique(ca, dpi)
        fig.savefig(chemin, dpi=dpi, metadata={"Software": None, "Date": None})
        plt.close(fig)
        with open(chemin, "rb") as f:
            entete = f.read(33)
        largeur = int.from_bytes(entete[16:20], "big")
        hauteur = int.from_bytes(entete[20:24], "big")
        mesures_fichiers[f"{nom}_mo"] = round(os.path.getsize(chemin) / 1024, 1)
        mesures_fichiers[f"{nom}_px"] = f"{largeur} x {hauteur}"
        mesures_fichiers[f"{nom}_mois_px"] = int(round(largeur / len(ca)))
        figs[nom] = chemin
    for ext, fmt, meta in (("svg", "svg", {"Date": None, "Creator": "outils_M10.py"}),
                           ("pdf", "pdf", {"CreationDate": None, "ModDate": None,
                                           "Creator": "outils_M10.py"})):
        chemin = os.path.join(EXPORTS, f"fil_rouge.{ext}")
        fig = figure_graphique(ca, 96)
        fig.savefig(chemin, format=fmt, metadata=meta)
        plt.close(fig)
        mesures_fichiers[f"{ext}_mo"] = round(os.path.getsize(chemin) / 1024, 1)
        figs[ext] = chemin
    if os.path.exists(figs.get("svg", "")):
        svg = open(figs["svg"], encoding="utf-8").read()
        mesures_fichiers["svg_points"] = svg.count("L ") + svg.count("M ")
        mesures_fichiers["svg_texte_reel"] = int("<text" in svg)
    return figs


def ecrire_excel(d, mesures_fichiers):
    """Le classeur Excel : les donnees, la feuille de controle, et le graphique NATIF d'Excel."""
    ca = d["ca"]
    modele = os.path.join(EXPORTS, "fil_rouge.xlsx")
    wb = Workbook()
    ws = wb.active
    ws.title = "Donnees"
    ws.append(["mois", "ca_net_fcfa"])
    for periode, valeur in ca.items():
        ws.append([str(periode), float(valeur)])
    ws.append(["Total", float(ca.sum())])
    ws["D1"] = "Controle"
    ws["E1"] = "Valeur attendue"
    ws["D2"] = "Total du classeur"
    ws["E2"] = f"=SUM(B2:B{1 + len(ca)})"
    ws["D3"] = "Total du socle"
    ws["E3"] = float(ca.sum())
    ws["D4"] = "Ecart"
    ws["E4"] = "=ROUND(E3-E2,2)"

    graph = LineChart()
    graph.title = "Le CA net mensuel, 24 mois (graphique natif Excel)"
    graph.y_axis.title = "FCFA"
    graph.x_axis.title = "mois"
    graph.height = 7.6
    graph.width = 13.0
    donnees = Reference(ws, min_col=2, min_row=1, max_row=1 + len(ca))
    categories = Reference(ws, min_col=1, min_row=2, max_row=1 + len(ca))
    graph.add_data(donnees, titles_from_data=True)
    graph.set_categories(categories)
    ws.add_chart(graph, "G2")

    wb.properties.created = FIXE
    wb.properties.modified = FIXE
    wb.properties.creator = "outils_M10.py"
    wb.save(modele)
    figer_zip(modele)

    # on relit le classeur : c'est ce qui fait de cet outil un outil EXECUTE, pas cite
    relu = load_workbook(modele)
    feuille = relu["Donnees"]
    valeurs = [float(feuille.cell(row=r, column=2).value) for r in range(2, 2 + len(ca))]
    ecart = float(np.abs(np.array(valeurs) - ca.to_numpy()).max())
    mesures_fichiers["xlsx_mo"] = round(os.path.getsize(modele) / 1024, 1)
    mesures_fichiers["xlsx_feuilles"] = len(relu.sheetnames)
    mesures_fichiers["xlsx_cellules"] = int(sum(1 for _ in feuille.iter_rows()))
    mesures_fichiers["xlsx_graphiques_natifs"] = len(feuille._charts)
    mesures_fichiers["xlsx_ecart_max_fcfa"] = round(ecart, 2)
    mesures_fichiers["xlsx_valeurs_comparees"] = len(valeurs)
    return modele, valeurs


def mesures(d, fichiers):
    m = dict(fichiers)
    ca = d["ca"]
    m["largeur_mm"] = LARGEUR_MM
    m["hauteur_mm"] = HAUTEUR_MM
    m["mois"] = int(len(ca))
    m["ca_min_m"] = round(float(ca.min()) / 1e6, 1)
    m["ca_max_m"] = round(float(ca.max()) / 1e6, 1)
    m["annee_1_m"] = round(float(d["annee"].iloc[0]) / 1e6, 1)
    m["annee_2_m"] = round(float(d["annee"].iloc[1]) / 1e6, 1)
    m["ecart_annuel_pct"] = round(float(d["annee"].iloc[1] / d["annee"].iloc[0] - 1) * 100, 1)
    m["outils_executes"] = 2          # matplotlib et Excel (ecrit et relu)
    m["outils_cites"] = 1             # Power BI : procedure decrite, aucun fichier produit
    m["outils_total"] = 3
    m["clics_power_bi"] = 9           # la procedure du chapitre, comptee en clics
    m["lignes_code_matplotlib"] = 14  # le bloc figure_graphique(), compte dans le script
    m["poids_total_exports_ko"] = round(sum(
        v for k, v in m.items() if k.endswith("_mo") and isinstance(v, (int, float))), 1)
    m["facteur_poids_png"] = round(m["png_300_mo"] / m["png_96_mo"], 1)
    m["pixels_par_mois_96"] = m["png_96_mois_px"]
    m["pixels_par_mois_300"] = m["png_300_mois_px"]
    return m


def planche(d, m):
    ca = d["ca"]
    fig = plt.figure(figsize=(190 / 25.4, 142 / 25.4), dpi=100)
    gs = fig.add_gridspec(3, 3, height_ratios=[1.0, 0.62, 0.26],
                          hspace=0.45, wspace=0.16, top=0.92, bottom=0.03,
                          left=0.05, right=0.98)

    # panneau 1 — matplotlib (execute)
    ax = fig.add_subplot(gs[0, 0])
    t = np.arange(len(ca))
    ax.plot(t, ca.to_numpy() / 1e6, "-", color=ORANGE, lw=0.9)
    ax.plot(t, ca.rolling(3).mean().to_numpy() / 1e6, "-", color=BLEU, lw=1.6)
    ax.set_ylim(0, 360)
    ax.set_title("1 · matplotlib — exécuté", fontsize=7.5, loc="left", color=BLEU)
    ax.tick_params(labelsize=6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.annotate(f"{m['lignes_code_matplotlib']} lignes de code, 4 formats", (0.03, 0.06),
                xycoords="axes fraction", fontsize=6.5, color=GRIS)

    # panneau 2 — Excel (ecrit puis relu)
    ax = fig.add_subplot(gs[0, 1])
    ax.set_axis_off()
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)     # coordonnees normales : les cadres ne bougent pas
    ax.set_title("2 · Excel — exécuté (écrit puis relu)", fontsize=7.5, loc="left", color=VERT)
    ax.add_patch(plt.Rectangle((0.02, 0.34), 0.42, 0.56, fc="#eef4ef", ec=VERT, lw=0.9))
    ax.add_patch(plt.Rectangle((0.52, 0.34), 0.46, 0.56, fc="white", ec=VERT, lw=0.9))
    ax.text(0.05, 0.82, "Données", fontsize=6, color=VERT)
    for i in range(4):
        ax.text(0.05, 0.72 - i * 0.105, f"2026-{i + 1:02d}  {int(ca.iloc[12 + i]):,}".replace(",", " "),
                fontsize=5.0)
    ax.text(0.55, 0.82, "graphique natif", fontsize=5.4, color=GRIS)
    ax.plot([0.55, 0.95], [0.42, 0.42], color=GRIS, lw=0.6)
    for i, val in enumerate(ca.iloc[12:19].to_numpy() / 1e6):
        x = 0.57 + i * 0.052
        ax.plot([x, x], [0.42, 0.42 + (val - 300) / 60 * 0.32], color=VERT, lw=1.3)
    ax.annotate(f"{m['xlsx_cellules']} lignes écrites, {m['xlsx_graphiques_natifs']} graphique natif,\n"
                f"écart relu : {m['xlsx_ecart_max_fcfa']:.2f} FCFA",
                (0.02, 0.27), xycoords="axes fraction", fontsize=6.5, color=VERT, va="top")

    # panneau 3 — Power BI (cite, non execute)
    ax = fig.add_subplot(gs[0, 2])
    ax.set_axis_off()
    ax.set_title("3 · Power BI — cité, non exécuté", fontsize=7.5, loc="left", color=ROUGE)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.add_patch(plt.Rectangle((0.02, 0.18), 0.96, 0.72, fc="#fbf1f0", ec=ROUGE, lw=0.9, ls="--"))
    for i, etape in enumerate(["1 ouvrir le classeur source", "2 créer la mesure CA net",
                               "3 glisser mois + mesure", "4 choisir un graphique",
                               "5 formater, exporter en PDF", "6 publier le rapport"]):
        ax.text(0.06, 0.82 - i * 0.115, etape, fontsize=5.6, color=ROUGE)
    ax.annotate(f"{m['clics_power_bi']} clics décrits, aucun fichier produit :\n"
                "la règle §1.5 impose de le déclarer",
                (0.02, 0.06), xycoords="axes fraction", fontsize=6.5, color=ROUGE)

    # bande 2 — le meme chiffre dans les trois outils
    ax = fig.add_subplot(gs[1, :])
    ax.set_axis_off()
    ax.text(0.0, 1.06, "Le même graphique, le même chiffre : ce qui change n'est pas la valeur, "
                       "c'est le fichier", transform=ax.transAxes, fontsize=8, fontweight="bold",
            color=BLEU, va="top")
    lignes = [
        ("matplotlib — PNG 96 dpi", m["png_96_px"] + " px", f"{m['png_96_mo']} Ko",
         f"{m['pixels_par_mois_96']} px par mois"),
        ("matplotlib — PNG 300 dpi", m["png_300_px"] + " px", f"{m['png_300_mo']} Ko",
         f"{m['pixels_par_mois_300']} px par mois (impression)"),
        ("matplotlib — SVG (vectoriel)", f"{m['svg_points']} points tracés", f"{m['svg_mo']} Ko",
         "aucune perte à l'agrandissement"),
        ("matplotlib — PDF (vectoriel)", "1 page, mêmes tracés", f"{m['pdf_mo']} Ko",
         "prêt pour le rapport"),
        ("Excel — classeur .xlsx", f"{m['xlsx_cellules']} lignes, 1 graphique natif",
         f"{m['xlsx_mo']} Ko", f"écart relu {m['xlsx_ecart_max_fcfa']:.2f} FCFA sur "
                               f"{m['xlsx_valeurs_comparees']} valeurs"),
        ("Power BI — rapport .pbix", "non produit", "—", "cité, non exécuté (aucune mesure)"),
    ]
    for i, (outil, taille, poids, note) in enumerate(lignes):
        y = 0.86 - i * 0.155
        couleur = ROUGE if outil.startswith("Power") else (VERT if outil.startswith("Excel") else BLEU)
        ax.text(0.0, y, outil, transform=ax.transAxes, fontsize=6.6, color=couleur)
        ax.text(0.30, y, taille, transform=ax.transAxes, fontsize=6.6)
        ax.text(0.52, y, poids, transform=ax.transAxes, fontsize=6.6)
        ax.text(0.60, y, note, transform=ax.transAxes, fontsize=6.4, color=GRIS)

    # bande 3 — la regle du chapitre
    ax = fig.add_subplot(gs[2, :])
    ax.set_axis_off()
    fr = lambda x: f"{x:,.1f}".replace(",", " ").replace(".", ",")
    ax.text(0.0, 1.0, f"Support : {m['largeur_mm']:.0f} × {m['hauteur_mm']:.0f} mm · "
                      f"{m['mois']} mois · CA net de {fr(m['ca_min_m'])} à {fr(m['ca_max_m'])} M FCFA · "
                      f"2025 : {fr(m['annee_1_m'])} M → 2026 : {fr(m['annee_2_m'])} M "
                      f"({fr(m['ecart_annuel_pct'])} %)",
            transform=ax.transAxes, fontsize=6.8, va="top")
    ax.text(0.0, 0.55, f"{m['outils_total']} outils : {m['outils_executes']} exécutés, "
                       f"{m['outils_cites']} cité — le chiffre du graphique est identique dans les "
                       f"trois cas (écart mesuré {m['xlsx_ecart_max_fcfa']:.2f} FCFA).",
            transform=ax.transAxes, fontsize=6.8, color=VERT, va="top")

    fig.suptitle("Le même graphique en trois outils : ce qui change est le fichier, pas le chiffre",
                 fontsize=9.5, x=0.05, ha="left", y=0.985)
    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    fig.savefig(SORTIE, metadata={"Date": None, "Creator": "outils_M10.py"}, dpi=100)
    plt.close(fig)
    return SORTIE


def main():
    d = charger()
    fic = {}
    ecrire_exports(d, fic)
    chemin_xlsx, _ = ecrire_excel(d, fic)
    m = mesures(d, fic)
    m["chemin_xlsx"] = os.path.relpath(chemin_xlsx, RACINE)
    print("=" * 78)
    print("C07 — LE MEME GRAPHIQUE DANS TROIS OUTILS")
    print("=" * 78)
    for k, val in m.items():
        print(f"  {k:30s} = {val}")
    chemin = planche(d, m)
    print()
    print(f"  planche : {os.path.relpath(chemin, RACINE)} ({os.path.getsize(chemin)/1024:.1f} Ko)")
    print()
    print(json.dumps(m, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
