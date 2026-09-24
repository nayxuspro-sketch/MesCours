#!/usr/bin/env python3
"""seize_graphiques_M10.py — le catalogue des 16 graphiques du manuel, exécuté sur le socle.

Le chapitre C02 est organisé autour d'un tableau de 16 lignes (question servie, encodage,
usage, piège, chiffre du socle). Ce script produit la planche qui l'illustre : les 16
graphiques réellement dessinés à partir du socle M07/M08/M09 (quincaillerie 50 008 ventes,
catalogue produit, clients, magasins) et du jeu projet M09.P pour l'entonnoir.

Sortie : figures/M10_C02_seize_graphiques.svg (16 panneaux, 198 x 160 mm, deterministe :
svg.hashsalt + metadata sans horodatage). Aucune donnee nouvelle n'est creee.

Usage : python3 tools/seize_graphiques_M10.py
"""
from __future__ import annotations

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import Polygon, Rectangle  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(RACINE, "03_exercices", "dossier_M09")
SORTIE = os.path.join(RACINE, "figures", "M10_C02_seize_graphiques.svg")
REF = os.path.join(RACINE, "01_socle_donnees", "data", "reference", "chiffres_cites.json")

BLEU, ORANGE, GRIS, VERT, ROUGE = "#1f4e79", "#c96a1a", "#8895a5", "#2e6f5e", "#a1382c"
LARGEUR_MM, HAUTEUR_MM = 198.0, 160.0

matplotlib.rcParams["svg.hashsalt"] = "seize_graphiques_M10"
plt.rcParams.update({"font.size": 7, "svg.fonttype": "none"})


def sauver(fig, chemin, **kw):
    fig.savefig(chemin, metadata={"Date": None, "Creator": "seize_graphiques_M10.py"}, **kw)


def charger():
    v = pd.read_csv(os.path.join(SRC, "quincaillerie", "vente.csv"), parse_dates=["date_vente"])
    p = pd.read_csv(os.path.join(SRC, "quincaillerie", "produit.csv"))
    c = pd.read_csv(os.path.join(SRC, "quincaillerie", "client.csv"))
    m = pd.read_csv(os.path.join(SRC, "quincaillerie", "magasin.csv"))
    pj = pd.read_csv(os.path.join(SRC, "projet", "fichier_inconnu.csv"))
    return v, p, c, m, pj


def donnees():
    v, p, c, m, pj = charger()
    d = {}
    net = v[~v["est_retour"]]
    vp = net.merge(p[["id_produit", "id_categorie"]], on="id_produit", how="left")
    d["ca_categorie"] = (vp.groupby("id_categorie")["montant_ttc"].sum().sort_values(ascending=False))
    d["ca_mois"] = net.groupby(net["date_vente"].dt.to_period("M"))["montant_ttc"].sum()
    d["retours_mois"] = (v.groupby(v["date_vente"].dt.to_period("M"))["est_retour"].sum())
    d["nb_ventes_mois"] = net.groupby(net["date_vente"].dt.to_period("M")).size()
    d["chat_mois_categorie"] = (vp.assign(mois=vp["date_vente"].dt.to_period("M"))
                                .pivot_table(index="id_categorie", columns="mois",
                                             values="montant_ttc", aggfunc="sum"))
    d["ca_magasin"] = (net.merge(m[["id_magasin", "nom", "ville"]], on="id_magasin", how="left")
                       .groupby("nom")["montant_ttc"].sum())
    d["ca_magasin_mois"] = (net.merge(m[["id_magasin", "nom"]], on="id_magasin", how="left")
                            .assign(mois=lambda x: x["date_vente"].dt.to_period("M"))
                            .pivot_table(index="mois", columns="nom", values="montant_ttc", aggfunc="sum"))
    d["boites"] = [net[net["id_magasin"] == i]["montant_ttc"].to_numpy() for i in sorted(net["id_magasin"].unique())]
    d["magasins"] = m
    ech = net.sample(n=2000, random_state=7)
    d["nuage"] = (ech["quantite"].to_numpy(), ech["montant_ttc"].to_numpy())
    d["ca_brut"] = float(v["montant_ttc"].sum())
    d["retours_montant"] = float(v[v["est_retour"]]["montant_ttc"].sum())
    d["ca_net"] = float(net["montant_ttc"].sum())
    d["ca_2025"] = float(net[net["date_vente"].dt.year == 2025]["montant_ttc"].sum())
    d["ca_2026"] = float(net[net["date_vente"].dt.year == 2026]["montant_ttc"].sum())
    # entonnoir du projet M09.P (le fichier que personne n'a regarde)
    ded = pj.drop_duplicates(subset=["tx_ref"])
    valides = ded[(ded["montant_xof"] > 0) & (ded["montant_xof"] < 100000000)]
    OK = ["OK", "ok", "Reussie", "REUSSI"]
    d["entonnoir"] = [("lignes reçues", len(pj)), ("références uniques", len(ded)),
                      ("montants valides", len(valides)),
                      ("succès confirmés", int(valides["statut"].isin(OK).sum()))]
    d["sankey"] = (net.merge(m[["id_magasin", "ville"]], on="id_magasin", how="left")
                   .groupby("ville")["montant_ttc"].sum())
    d["retours_par_ville"] = (v[v["est_retour"]].merge(m[["id_magasin", "ville"]], on="id_magasin", how="left")
                              .groupby("ville")["montant_ttc"].sum())
    d["montants"] = v["montant_ttc"].to_numpy()
    return d


def cadre(ax, titre):
    ax.set_title(titre, fontsize=7.5, loc="left", pad=3)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=6, length=2)


def lab_mois(mois):
    return [f"{p.year % 100:02d}-{p.month:02d}" for p in mois]


# ----------------------------------------------------------------------
# Les 16 panneaux
# ----------------------------------------------------------------------
def g01_histogramme(ax, d):
    m = d["montants"]
    ax.hist(np.clip(m, 0, 600000) / 1000, bins=40, color=BLEU)
    ax.set_yscale("log")
    ax.set_xlabel("montant TTC (milliers FCFA)", fontsize=6)
    cadre(ax, "1 · histogramme — la forme")
    ax.axvline(float(np.median(m)) / 1000, color=ORANGE, lw=1)
    ax.annotate(f"médiane {np.median(m):,.0f}".replace(",", " "), xy=(np.median(m) / 1000, ax.get_ylim()[1] * 0.3),
                xytext=(np.median(m) / 1000 + 30, ax.get_ylim()[1] * 0.55), fontsize=6, color=ORANGE,
                arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6))


def g02_barres(ax, d):
    s = d["ca_categorie"] / 1e6
    ax.barh([f"C{i}" for i in s.index][::-1], s.to_numpy()[::-1], color=BLEU, height=0.65)
    ax.set_xlabel("CA net (millions FCFA)", fontsize=6)
    cadre(ax, "2 · barres triées — comparer")


def g03_courbe(ax, d):
    ca = d["ca_mois"] / 1e6
    ax.plot(range(len(ca)), ca.to_numpy(), color=BLEU, lw=1.4)
    ax.set_xticks([0, 6, 12, 18, 23], lab_mois([ca.index[i] for i in (0, 6, 12, 18, 23)]), fontsize=6)
    ax.set_ylim(0, ca.max() * 1.15)
    cadre(ax, "3 · courbe — évoluer")


def g04_camembert(ax, d):
    ax.pie(d["ca_categorie"].to_numpy(), startangle=90, counterclock=False,
           colors=[plt.get_cmap("Blues")(0.3 + 0.55 * i / 7) for i in range(8)],
           wedgeprops={"edgecolor": "white", "lw": 0.5})
    cadre(ax, "4 · camembert (≤ 3 parts)")


def g05_nuage(ax, d):
    q, m = d["nuage"]
    ax.scatter(q + np.random.default_rng(3).uniform(-0.15, 0.15, len(q)), m / 1000,
               s=3, alpha=0.25, color=BLEU)
    ax.set_xlabel("quantité", fontsize=6)
    ax.set_ylabel("montant (milliers FCFA)", fontsize=6)
    ax.set_ylim(0, 700)
    cadre(ax, "5 · nuage de points — la relation")


def g06_boites(ax, d):
    bp = ax.boxplot(d["boites"], vert=False, showfliers=False, widths=0.6, patch_artist=True)
    for b in bp["boxes"]:
        b.set(facecolor=BLEU, alpha=0.75, edgecolor=BLEU)
    ax.set_yticks(range(1, 6), [f"M{i}" for i in range(1, 6)], fontsize=6)
    ax.set_xlabel("montant TTC (FCFA)", fontsize=6)
    ax.set_xticks([0, 250000, 500000], ["0", "250 k", "500 k"], fontsize=6)
    ax.set_xlim(0, 620000)
    cadre(ax, "6 · boîte à moustaches")


def g07_chaleur(ax, d):
    t = d["chat_mois_categorie"] / 1e6
    im = ax.imshow(t.to_numpy(), aspect="auto", cmap="Blues")
    ax.set_yticks(range(t.shape[0]), [f"C{i}" for i in t.index], fontsize=6)
    idx = list(range(0, t.shape[1], 5))
    ax.set_xticks(idx, [lab_mois(t.columns)[i] for i in idx], fontsize=5.5)
    cadre(ax, "7 · carte de chaleur (par ligne)")
    cb = ax.figure.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
    cb.ax.tick_params(labelsize=5)


def g08_carte(ax, d):
    coords = {"Ouaga Centre": (12.3686, -1.5275), "Ouaga Patte d'Oie": (12.24, -1.36),
              "Bobo Centre": (11.1771, -4.2979), "Bobo Sarfalao": (11.13, -4.22),
              "Koudougou": (12.2526, -2.3617)}
    ca = d["ca_magasin"]
    for nom, val in ca.items():
        lat, lon = coords[nom]
        r = 30 + 150 * (val / ca.max())
        ax.scatter(lon, lat, s=np.pi * r, color=ORANGE, alpha=0.55, edgecolor=ORANGE, lw=0.5)
        ax.annotate(nom, (lon, lat), fontsize=4.5, ha="center", va="bottom", color="#3a2a12",
                    xytext=(0, 3), textcoords="offset points")
    ax.set_xlabel("longitude", fontsize=6)
    ax.set_ylabel("latitude", fontsize=6)
    ax.set_xlim(-5.6, -0.6)
    ax.set_ylim(10.5, 13.0)
    ax.set_xticks([-5, -4, -3, -2, -1])
    ax.set_yticks([11, 12, 13])
    ax.tick_params(labelsize=6)
    cadre(ax, "8 · carte à symboles — où")


def g09_cascade(ax, d):
    etapes = [("CA brut", d["ca_brut"]), ("retours", -d["retours_montant"]), ("CA net", d["ca_net"])]
    base, cum = 0.0, 0.0
    for i, (nom, val) in enumerate(etapes):
        if i == 1:
            base = cum + val
            ax.bar(i, -val / 1e6, bottom=base / 1e6, color=ROUGE, width=0.6)
        else:
            base = 0.0 if i == 2 else cum
            ax.bar(i, val / 1e6, bottom=base / 1e6, color=BLEU if i != 2 else VERT, width=0.6)
            cum = val if i == 0 else d["ca_net"]
        ax.annotate(f"{abs(val)/1e6:,.0f}".replace(",", " "), (i, (base + abs(val)) / 1e6),
                    fontsize=5.5, ha="center", va="bottom")
    ax.set_xticks(range(3), [e[0] for e in etapes], fontsize=6)
    ax.set_ylim(7800, 8000)
    ax.set_ylabel("millions FCFA", fontsize=6)
    cadre(ax, "9 · cascade — décomposer")


def g10_entonnoir(ax, d):
    et = d["entonnoir"]
    larg = [e[1] / et[0][1] * 0.86 for e in et]
    y = np.arange(len(et))[::-1]
    ax.barh(y, larg, color=[BLEU, BLEU, ORANGE, VERT], height=0.62)
    ax.set_yticks(y, [e[0] for e in et], fontsize=6)
    for yi, (nom, val) in zip(y, et):
        ax.annotate(f"{val:,}".replace(",", " "), (larg[len(et) - 1 - yi], yi), xytext=(4, 0),
                    textcoords="offset points", va="center", fontsize=6)
    ax.set_xlim(0, 1.25)
    ax.set_xticks([])
    cadre(ax, "10 · entonnoir — la perte")


def g11_combine(ax, d):
    ca = (d["ca_mois"] / 1e6).to_numpy()
    ret = d["retours_mois"].reindex(d["ca_mois"].index).to_numpy()
    ax.bar(range(len(ca)), ca, color=BLEU, width=0.75)
    ax.set_ylim(280, 360)
    ax2 = ax.twinx()
    ax2.plot(range(len(ret)), ret, color=ORANGE, lw=1.4)
    ax2.set_ylim(0, ret.max() * 2.2)
    ax2.tick_params(labelsize=6, colors=ORANGE)
    ax.set_xticks([0, 11, 23], lab_mois([d["ca_mois"].index[i] for i in (0, 11, 23)]), fontsize=6)
    cadre(ax, "11 · combiné à deux axes")


def g12_aire(ax, d):
    t = (d["chat_mois_categorie"] / 1e6).to_numpy()
    ax.stackplot(range(t.shape[1]), t, colors=[plt.get_cmap("Blues")(0.25 + 0.6 * i / 7) for i in range(8)], lw=0.2)
    ax.set_xticks([0, 11, 23], lab_mois(list(d["chat_mois_categorie"].columns)[i] for i in (0, 11, 23)), fontsize=6)
    ax.set_ylim(0, 360)
    cadre(ax, "12 · aires empilées")


def g13_treemap(ax, d):
    val = d["ca_categorie"].to_numpy()
    reste, x, y, w, h = val.sum(), 0.0, 0.0, 1.0, 1.0
    for i, v in enumerate(val):
        part = v / reste
        if w >= h:                       # tranche verticale
            r = Rectangle((x, y), w * part, h, facecolor=plt.get_cmap("Blues")(0.25 + 0.65 * i / 7))
            x, w = x + w * part, w * (1 - part)
        else:
            r = Rectangle((x, y), w, h * part, facecolor=plt.get_cmap("Blues")(0.25 + 0.65 * i / 7))
            y, h = y + h * part, h * (1 - part)
        ax.add_patch(r)
        reste -= v
        if part > 0.09:
            ax.annotate(f"C{d['ca_categorie'].index[i]}", (r.get_x() + r.get_width() / 2,
                        r.get_y() + r.get_height() / 2), ha="center", va="center", fontsize=5.5)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    cadre(ax, "13 · treemap — la place")


def g14_bullet(ax, d):
    cible = d["ca_2025"] / 1e6
    mesure = d["ca_2026"] / 1e6
    ax.barh(0, cible * 1.25, height=0.72, color="#dfe6ee")
    ax.barh(0, cible * 1.1, height=0.48, color="#b9c6d6")
    ax.barh(0, mesure, height=0.22, color=BLEU)
    ax.axvline(cible, color=ROUGE, lw=1.6)
    ax.annotate(f"{mesure:,.0f}".replace(",", " "), (mesure, 0), xytext=(4, 0),
                textcoords="offset points", va="center", fontsize=6)
    ax.annotate("cible 2025", (cible, 0.82), fontsize=5.5, color=ROUGE, ha="right", va="top")
    ax.set_yticks([])
    ax.set_ylim(-0.35, 0.9)
    ax.set_xlabel("CA net (millions FCFA)", fontsize=6)
    cadre(ax, "14 · jauge à puces (bullet)")


def g15_petits_multiples(ax, d):
    t = d["ca_magasin_mois"] / 1e6
    ax.axis("off")
    sous = ax.figure.add_gridspec(2, 3, left=0, right=0, top=0, bottom=0)
    return sous, t


def g16_sankey(ax, d):
    villes = list(d["sankey"].index)
    net = d["sankey"]
    ret = d["retours_par_ville"].reindex(villes).fillna(0.0)
    total = float((net + ret).sum())
    y0 = 0.0
    for i, ville in enumerate(villes):
        h = float(net[ville] + ret[ville]) / total
        ax.add_patch(Rectangle((0, y0), 0.12, h, color=BLEU if i % 2 == 0 else "#2f5f8f"))
        ax.annotate(ville.split("-")[0], (0.0, y0 + h / 2), xytext=(-3, 0),
                    textcoords="offset points", ha="right", va="center", fontsize=5)
        hnet, hret = float(net[ville]) / total, float(ret[ville]) / total
        y0b = 0.35 + sum(float(net[v] + ret[v]) / total for v in villes[:i])
        ax.add_patch(Polygon([(0.12, y0), (0.88, y0b), (0.88, y0b + hnet), (0.12, y0 + hnet)],
                             closed=True, color=VERT, alpha=0.45, lw=0))
        ax.add_patch(Polygon([(0.12, y0 + hnet), (0.88, y0b + hnet), (0.88, y0b + hnet + hret),
                              (0.12, y0 + h)][::-1], closed=True, color=ROUGE, alpha=0.45, lw=0))
        y0 += h
    hn, hr = float(net.sum()) / total, float(ret.sum()) / total
    ax.add_patch(Rectangle((0.88, 0.35), 0.12, hn, color=VERT))
    ax.add_patch(Rectangle((0.88, 0.35 + hn), 0.12, hr, color=ROUGE))
    ax.annotate("CA conservé", (1.0, 0.35 + hn / 2), xytext=(3, 0), textcoords="offset points",
                va="center", fontsize=5)
    ax.annotate("retours", (1.0, 0.35 + hn + hr / 2), xytext=(3, 0), textcoords="offset points",
                va="center", fontsize=5)
    ax.set_xlim(-0.30, 1.55)
    ax.set_ylim(0, 1.05)
    ax.axis("off")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis("off")
    ax.set_title("16 · diagramme de flux (Sankey)", fontsize=7.5, loc="left", pad=3)


def main():
    d = donnees()
    fig = plt.figure(figsize=(LARGEUR_MM / 25.4, HAUTEUR_MM / 25.4), dpi=100)
    gs = fig.add_gridspec(4, 4, hspace=0.78, wspace=0.34, top=0.95, bottom=0.05,
                          left=0.05, right=0.98)
    axes = [fig.add_subplot(gs[i // 4, i % 4]) for i in range(14)]   # 14 panneaux dessines
    for ax, fn in zip(axes, [g01_histogramme, g02_barres, g03_courbe, g04_camembert, g05_nuage,
                             g06_boites, g07_chaleur, g08_carte, g09_cascade, g10_entonnoir,
                             g11_combine, g12_aire, g13_treemap, g14_bullet]):
        fn(ax, d)
    ax15 = fig.add_subplot(gs[3, 3])
    ax15.remove()                        # le titre du panneau 15 est porte par la grille de facettes
    fig.text(0.755, 0.258, "15 · petits multiples — 5 magasins", fontsize=7.5)
    sous = gs[3, 3].subgridspec(5, 1, hspace=0.35)
    t = d["ca_magasin_mois"] / 1e6
    ymin, ymax = float(t.min().min()), float(t.max().max())
    for j, nom in enumerate(t.columns):
        a = fig.add_subplot(sous[j, 0])
        a.plot(range(len(t)), t[nom].to_numpy(), lw=0.9, color=BLEU)
        a.set_ylim(ymin * 0.92, ymax * 1.5)
        a.set_xticks([])
        a.set_yticks([])
        a.annotate(nom, (0.01, 0.98), xycoords="axes fraction", fontsize=5, va="top")
        for s in ("top", "right", "bottom", "left"):
            a.spines[s].set_visible(False)
    ax16 = fig.add_subplot(gs[3, 2])
    g16_sankey(ax16, d)
    fig.suptitle("Les 16 graphiques du manuel, dessinés sur le socle de la quincaillerie",
                 fontsize=9, x=0.008, ha="left", y=0.995)
    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    sauver(fig, SORTIE, dpi=100)
    plt.close(fig)
    print(f"planche : {os.path.relpath(SORTIE, RACINE)} ({os.path.getsize(SORTIE)/1024:.1f} Ko)")

    # les chiffres que le tableau du chapitre citera
    m = {}
    m["c02_graphiques"] = 16
    m["c02_fondateurs"] = 11
    m["c02_utiles"] = 5
    m["c02_ca_categorie_max_m"] = round(float(d["ca_categorie"].max() / 1e6), 1)
    m["c02_ca_categorie_min_m"] = round(float(d["ca_categorie"].min() / 1e6), 1)
    m["c02_ca_mois_min_m"] = round(float(d["ca_mois"].min() / 1e6), 1)
    m["c02_ca_mois_max_m"] = round(float(d["ca_mois"].max() / 1e6), 1)
    m["c02_mois_ca_max"] = str(d["ca_mois"].idxmax())
    m["c02_mois_ca_min"] = str(d["ca_mois"].idxmin())
    m["c02_entonnoir_etapes"] = len(d["entonnoir"])
    m["c02_entonnoir_taux_final_pct"] = round(d["entonnoir"][-1][1] / d["entonnoir"][0][1] * 100, 1)
    m["c02_ca_2025_m"] = round(d["ca_2025"] / 1e6, 1)
    m["c02_ca_2026_m"] = round(d["ca_2026"] / 1e6, 1)
    m["c02_retours_part_pct"] = round(d["retours_montant"] / d["ca_brut"] * 100, 2)
    m["c02_mediane_montant"] = int(round(float(np.median(d["montants"]))))
    m["c02_magasins"] = int(len(d["ca_magasin"]))
    m["c02_villes_sankey"] = int(len(d["sankey"]))
    m["c02_planche"] = "figures/M10_C02_seize_graphiques.svg (16 panneaux, 198 x 160 mm, sortie deterministe)"
    print(json.dumps(m, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
