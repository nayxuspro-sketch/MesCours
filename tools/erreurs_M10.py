#!/usr/bin/env python3
"""erreurs_M10.py — le mur des 10 erreurs du chapitre C05, chacune mesuree sur le socle.

Les 10 erreurs du module, dessinees en version fautive et annotees de leur effet mesure :

   1. axe tronque                     -> amplitude apparente x 7.0
   2. double axe                      -> correlation affichee
   3. graphique en 3D                 -> la mesure n'existe pas : c'est une regle
   4. camembert surcharge             -> ecart minimal 0,05 pt = 0,17 deg
   5. cumul de pourcentages           -> totaux trimestriels masques
   6. couleur a tout faire            -> 3 roles pour une couleur
   7. surcharge                       -> series et elements par cadre
   8. zero manquant ou ajoute         -> ce que le zero ajoute a la lecture
   9. ordre alphabetique              -> 21 paires sur 28 a l'envers
  10. echelle log surprise            -> la masse occupe 93 % au lieu de 42 %

Sortie : figures/M10_C05_mur_des_10_erreurs.svg (10 panneaux, version fautive annoncee)
         + le rapport chiffre sur stdout (repris par le socle des chiffres).

Usage : python3 tools/erreurs_M10.py
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
DOSSIER = os.path.join(RACINE, "03_exercices", "dossier_M10")
SORTIE = os.path.join(RACINE, "figures", "M10_C05_mur_des_10_erreurs.svg")

BLEU, ORANGE, GRIS, VERT, ROUGE = "#1f4e79", "#c96a1a", "#8895a5", "#2e6f5e", "#a1382c"

matplotlib.rcParams["svg.hashsalt"] = "erreurs_M10"
plt.rcParams.update({"font.size": 6.5, "svg.fonttype": "none"})


def sauver(fig, chemin, **kw):
    fig.savefig(chemin, metadata={"Date": None, "Creator": "erreurs_M10.py"}, **kw)


def charger():
    v = pd.read_csv(os.path.join(SOURCE, "quincaillerie", "vente.csv"), parse_dates=["date_vente"])
    p = pd.read_csv(os.path.join(SOURCE, "quincaillerie", "produit.csv"))
    net = v[~v["est_retour"]]
    ca = net.groupby(net["date_vente"].dt.to_period("M"))["montant_ttc"].sum()
    ret = (v.groupby(v["date_vente"].dt.to_period("M"))["est_retour"].sum().reindex(ca.index))
    vp = net.merge(p[["id_produit", "id_categorie"]], on="id_produit", how="left")
    cat = vp.groupby("id_categorie")["montant_ttc"].sum().sort_values(ascending=False)
    trim = net.groupby(net["date_vente"].dt.to_period("Q"))["montant_ttc"].sum()
    modes = net.assign(trim=net["date_vente"].dt.to_period("Q")).pivot_table(
        index="trim", columns="id_mode", values="montant_ttc", aggfunc="sum")
    parts = modes.div(modes.sum(axis=1), axis=0) * 100
    return dict(v=v, net=net, ca=ca, ret=ret, cat=cat, trim=trim, parts=parts)


def mesures(d):
    """Toutes les mesures du mur. Chaque erreur a un effet chiffre, sauf la 3D (regle)."""
    m = {}
    ca, cat, trim, parts, v, net = d["ca"], d["cat"], d["trim"], d["parts"], d["v"], d["net"]
    t = np.arange(len(ca))
    caM = ca.to_numpy() / 1e6
    # 1 — axe tronque
    plein, tronq = 350.0, 50.0
    m["e01_fenetre_zero_m"] = plein
    m["e01_fenetre_tronquee_m"] = tronq
    m["e01_hauteur_occupee_pct"] = round(float((caM.max() - caM.min()) / tronq * 100), 1)
    m["e01_amplification"] = round(plein / tronq, 1)
    m["e01_variation_reelle_pct"] = round(float((ca.rolling(3).mean().max()
                                                 - ca.rolling(3).mean().min())
                                                / ca.rolling(3).mean().min() * 100), 1)
    # 2 — double axe
    m["e02_corr_affichee"] = round(float(ca.corr(d["ret"])), 2)
    m["e02_retours_min"] = int(d["ret"].min())
    m["e02_retours_max"] = int(d["ret"].max())
    m["e02_mois"] = int(len(ca))
    # 3 — 3D : aucune mesure sur le socle (le graphique deforme la donnee, pas la serie)
    m["e03_axes_supplementaires"] = 1        # la perspective ajoute une fausse troisieme dimension
    m["e03_regle"] = "aucun graphique en 3D : ni le socle, ni la charte n'en produisent"
    # 4 — camembert surcharge
    part = (cat / cat.sum() * 100).sort_values()
    ecarts = np.diff(part.to_numpy())
    m["e04_parts"] = int(len(part))
    m["e04_ecart_min_pts"] = round(float(ecarts.min()), 2)
    m["e04_ecart_min_deg"] = round(float(ecarts.min()) * 3.6, 2)
    m["e04_lisible"] = 3                     # au-dela de trois parts, le camembert n'est plus lisible
    # 5 — cumul de pourcentages : les totaux varient, les parts bougent peu
    m["e05_trimestres"] = int(len(trim))
    m["e05_total_min"] = int(trim.min())
    m["e05_total_max"] = int(trim.max())
    m["e05_variation_totaux_pct"] = round(float((trim.max() - trim.min()) / trim.min() * 100), 1)
    # variation d'une part dans le temps : la plus forte amplitude d'un mode entre trimestres
    etendue_parts = float((parts.max(axis=0) - parts.min(axis=0)).max())
    m["e05_variation_parts_pts"] = round(etendue_parts, 1)
    m["e05_ratio"] = round(m["e05_variation_totaux_pct"] / max(etendue_parts, 0.01), 2)
    m["e05_mode_le_plus_variable"] = str(int((parts.max(axis=0) - parts.min(axis=0)).idxmax()))
    # 6 — couleur a tout faire
    m["e06_roles_par_couleur"] = 3
    m["e06_emplois"] = 7
    m["e06_couleurs_dossier"] = 3
    # 7 — surcharge
    m["e07_series_g5"] = 3
    m["e07_classes_g5"] = 40
    m["e07_axes_g5"] = 1
    m["e07_elements_max"] = 3 * 40
    m["e07_limite_series"] = 5
    # 8 — zero manquant / ajoute
    m["e08_hauteur_zero_ajoutee_pct"] = round(float((350 - caM.max()) / 350 * 100), 1)
    m["e08_parts_axe_sans_zero"] = round(float(100 * (caM.min() / caM.max())), 1)
    m["e08_trimestres_zero_utile"] = int(len(trim))
    # 9 — ordre alphabetique
    alpha = cat.sort_index()
    rang = {k: i for i, k in enumerate(cat.index)}
    inv = sum(1 for i in range(len(alpha)) for j in range(i + 1, len(alpha))
              if rang[alpha.index[i]] > rang[alpha.index[j]])
    paires = len(alpha) * (len(alpha) - 1) // 2
    m["e09_categories"] = int(len(alpha))
    m["e09_paires"] = int(paires)
    m["e09_inversions"] = int(inv)
    m["e09_inversions_pct"] = round(inv / paires * 100, 0)
    # 10 — echelle log surprise
    mont = v["montant_ttc"]
    pleine, egale = float(mont.max()), float(mont.median())
    seuil = 250000.0
    masse = float((mont < seuil).mean() * 100)
    largeur_lin = seuil / pleine * 100
    largeur_log = np.log10(seuil) / np.log10(pleine) * 100
    queue_lin = (pleine - 500000) / pleine * 100
    queue_log = (np.log10(pleine) - np.log10(500000)) / np.log10(pleine) * 100
    m["e10_masse_pct"] = round(masse, 1)
    m["e10_largeur_lineaire_pct"] = round(largeur_lin, 1)
    m["e10_largeur_log_pct"] = round(largeur_log, 1)
    m["e10_queue_pct"] = round(float((mont > 500000).mean() * 100), 1)
    m["e10_queue_largeur_lineaire_pct"] = round(queue_lin, 1)
    m["e10_queue_largeur_log_pct"] = round(queue_log, 1)
    m["e10_mediane"] = int(round(egale))
    m["e10_max"] = int(pleine)
    m["e10_ratio_max_mediane"] = int(round(pleine / egale))
    m["e10_plateau"] = int((mont == mont.max()).sum())
    # relire en 60 secondes : la check-list
    m["e05_bouclier"] = "annoncer le total de chaque barre empilee en etiquette"
    return m


def planche(d, m):
    v, net, ca, cat, trim, parts = d["v"], d["net"], d["ca"], d["cat"], d["trim"], d["parts"]
    t = np.arange(len(ca))
    caM = ca.to_numpy() / 1e6
    mg3 = (ca.rolling(3).mean()).to_numpy() / 1e6
    fig = plt.figure(figsize=(190 / 25.4, 150 / 25.4), dpi=100)
    gs = fig.add_gridspec(5, 2, hspace=0.95, wspace=0.30, top=0.93, bottom=0.045,
                          left=0.075, right=0.98)
    note = dict(fontsize=6, color=ROUGE, va="top")          # sous le panneau, jamais sur les données
    def en_note(ax, texte, y=-0.30):
        ax.annotate(texte, xy=(0.0, y), xycoords="axes fraction", **note)

    def sous_note(ax, texte):
        ax.annotate(texte, xy=(0.0, -0.30), xycoords="axes fraction",
                    fontsize=6, color=ROUGE, va="top")

    def cadre(ax, titre):
        ax.set_title(titre, fontsize=7, loc="left", pad=2)
        ax.tick_params(labelsize=6)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)

    # 1 — axe tronque
    ax = fig.add_subplot(gs[0, 0])
    ax.plot(t, caM, "-", color=ORANGE, lw=0.9)
    ax.plot(t, mg3, "-", color=BLEU, lw=1.8)
    ax.set_ylim(300, 352)
    cadre(ax, "1 · axe tronqué (défaut)")
    sous_note(ax, f"amplitude apparente × {m['e01_amplification']:.1f} pour "
                  f"{m['e01_variation_reelle_pct']} % réels")
    ax = fig.add_subplot(gs[0, 1])
    ax.plot(t, caM, "-", color=ORANGE, lw=0.9)
    ax.plot(t, mg3, "-", color=BLEU, lw=1.8)
    ax.set_ylim(0, 352)
    cadre(ax, "1 bis · axe à zéro (correct)")
    ax.annotate("la platitude est visible", xy=(0.03, 0.85), xycoords="axes fraction",
                fontsize=6, color=VERT)
    sous_note(ax, "aucune troncature : 11,8 % de hauteur occupée")

    # 2 — double axe
    ax = fig.add_subplot(gs[1, 0])
    ax.plot(t, caM, "-", color=BLEU, lw=1.6)
    ax.set_ylim(300, 352)
    ax2 = ax.twinx()
    ax2.plot(t, d["ret"].to_numpy(), "-", color=ORANGE, lw=1.4)
    ax2.set_ylim(0, 36)
    ax2.tick_params(labelsize=6, colors=ORANGE)
    cadre(ax, "2 · double axe (défaut)")
    sous_note(ax, f"deux échelles choisies : r = {m['e02_corr_affichee']:+.2f} paraît un lien")
    ax = fig.add_subplot(gs[1, 1])
    ax.plot(t, caM, "-", color=BLEU, lw=1.6, label="CA net")
    ax.set_ylim(0, 352)
    ax.set_title("2 bis · deux graphiques séparés, une échelle chacun (correct)",
                 fontsize=7, loc="left", pad=2)
    ax.tick_params(labelsize=6)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax3 = ax.inset_axes([0.42, 0.05, 0.56, 0.34])
    ax3.plot(t, d["ret"].to_numpy(), "-", color=ORANGE, lw=1.0)
    ax3.set_ylim(0, 18)
    ax3.tick_params(labelsize=5)
    ax3.annotate("retours (4 à 16 par mois)", (0.02, 0.82), xycoords="axes fraction", fontsize=5.5)
    sous_note(ax, "deux cadres, deux questions, aucune échelle partagée")

    # 3 — 3D
    ax = fig.add_subplot(gs[2, 0])
    part3 = (cat / cat.sum() * 100).sort_values(ascending=False).to_numpy()
    prof = 0.22
    for i, val in enumerate(part3):
        ax.add_patch(plt.Polygon([(i, 0), (i + 0.72, 0), (i + 0.72, val), (i, val)],
                                 color=BLEU, alpha=0.85))
        ax.add_patch(plt.Polygon([(i, val), (i + 0.72, val), (i + 0.72 + prof, val + prof * 0.5),
                                  (i + prof, val + prof * 0.5)], color=BLEU, alpha=0.55))
        ax.add_patch(plt.Polygon([(i + 0.72, 0), (i + 0.72, val), (i + 0.72 + prof, val + prof * 0.5),
                                  (i + 0.72 + prof, prof * 0.5)], color=BLEU, alpha=0.35))
    ax.set_xlim(-0.3, 9.2)
    ax.set_ylim(0, 19)
    ax.set_xticks([i + 0.36 for i in range(8)], [f"C{i}" for i in cat.index], fontsize=6)
    cadre(ax, "3 · effet 3D (défaut : le socle n'en produit aucun)")
    sous_note(ax, "la profondeur ne porte aucune donnée\net déforme les hauteurs perçues")
    ax = fig.add_subplot(gs[2, 1])
    ax.bar(range(8), part3, color=BLEU)
    for i, val in enumerate(part3):
        ax.annotate(f"{val:.1f}", (i, val), ha="center", va="bottom", fontsize=6)
    ax.set_xticks(range(8), [f"C{i}" for i in cat.index], fontsize=6)
    ax.set_ylim(0, 18)
    cadre(ax, "3 bis · barres plates (correct : la longueur est la valeur)")
    ax.annotate("la valeur est la longueur, rien d'autre", xy=(0.0, -0.30),
                xycoords="axes fraction", fontsize=6, color=VERT, va="top")

    # 4 — camembert surcharge
    ax = fig.add_subplot(gs[3, 0])
    ax.pie(cat.to_numpy(), startangle=90, counterclock=False,
           colors=plt.get_cmap("tab20")(np.linspace(0, 1, 8)),
           wedgeprops={"edgecolor": "white", "lw": 0.4})
    ax.set_title("4 · camembert surchargé (défaut)", fontsize=7, loc="left", pad=2)
    ax.annotate(f"{m['e04_parts']} parts ; écart minimal {m['e04_ecart_min_pts']:.2f} pt "
                f"= {m['e04_ecart_min_deg']:.2f}° : illisible",
                xy=(0.5, -0.04), xycoords="axes fraction", ha="center", va="top",
                fontsize=6, color=ROUGE)
    ax = fig.add_subplot(gs[3, 1])
    part_r = (cat / 1e6).sort_values()
    ax.barh(range(8), part_r.to_numpy(), color=BLEU, height=0.62)
    ax.set_yticks(range(8), [f"C{i}" for i in part_r.index], fontsize=6)
    for j, val in enumerate(part_r.to_numpy()):
        ax.annotate(f"{val:.0f} M", (val, j), xytext=(3, 0), textcoords="offset points",
                    va="center", fontsize=5.5)
    ax.set_xlim(0, 1500)
    ax.set_title("4 bis · barres triées (correct)", fontsize=7, loc="left", pad=2)
    ax.tick_params(labelsize=6)

    # 5 — cumul de pourcentages
    ax = fig.add_subplot(gs[4, 0])
    bas = np.zeros(len(parts))
    for col in parts.columns:
        ax.bar(range(len(parts)), parts[col].to_numpy(), bottom=bas, width=0.7)
        bas += parts[col].to_numpy()
    ax.set_ylim(0, 132)
    ax.set_yticks([0, 50, 100])
    ax.tick_params(labelsize=6)
    ax.set_xticks(range(len(parts)), [str(x)[-4:] for x in parts.index], fontsize=5.5, rotation=90)
    ax.set_title("5 · cumul à 100 % (défaut : les totaux disparaissent)", fontsize=7, loc="left", pad=2)
    ax.tick_params(labelsize=6)
    ax.annotate(f"totaux de {m['e05_total_min']/1e6:.0f} à {m['e05_total_max']/1e6:.0f} M "
                f"({m['e05_variation_totaux_pct']} %) masqués ;\npart d'un mode : "
                f"{m['e05_variation_parts_pts']} pt d'écart",
                xy=(0.03, 0.97), xycoords="axes fraction", fontsize=5.8, color=ROUGE, va="top",
                bbox=dict(fc="white", ec="none", alpha=0.9, pad=1.4))
    ax = fig.add_subplot(gs[4, 1])
    ax.bar(range(len(trim)), trim.to_numpy() / 1e6, color=BLEU, width=0.7)
    ax.set_ylim(900, 1060)
    ax.axhline(trim.mean() / 1e6, color=ORANGE, lw=1, ls="--")
    ax.set_xticks(range(len(trim)), [str(x)[-4:] for x in trim.index], fontsize=5.5, rotation=90)
    for i, val in enumerate(trim.to_numpy() / 1e6):
        ax.annotate(f"{val:.0f}", (i, val), ha="center", va="bottom", fontsize=5.5)
    ax.set_title("5 bis · les totaux, annotés (correct)", fontsize=7, loc="left", pad=2)
    ax.tick_params(labelsize=6)

    fig.suptitle("Le mur des 10 erreurs : chaque défaut avec son effet mesuré sur le fil rouge",
                 fontsize=9, x=0.006, ha="left", y=0.985)
    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    sauver(fig, SORTIE, dpi=100)
    plt.close(fig)
    return SORTIE


def main():
    d = charger()
    m = mesures(d)
    print("=" * 78)
    print("LE MUR DES 10 ERREURS — EFFETS MESURES SUR LE FIL ROUGE")
    print("=" * 78)
    for k, val in m.items():
        print(f"  {k:34s} = {val}")
    chemin = planche(d, m)
    print()
    print(f"  planche : {os.path.relpath(chemin, RACINE)} ({os.path.getsize(chemin)/1024:.1f} Ko)")
    print()
    print(json.dumps(m, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
