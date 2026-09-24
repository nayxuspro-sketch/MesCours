#!/usr/bin/env python3
"""ecriture_M10.py — la mesure du chapitre C04 : titres, axes, annotations, ordre.

Quatre mesures, toutes exécutées :

  1. l'audit des titres du dossier : les 5 graphiques « avant » et les 5 « après » sont
     relus **dans le code qui les produit** (le SVG matplotlib ne contient pas de texte,
     il contient des tracés) — longueur du titre, présence d'un chiffre, présence de
     l'unité, mention de la source ;
  2. le coût d'un axe tronqué : quelle part de la hauteur de l'axe les données occupent
     réellement, et combien de fois l'amplitude apparente est multipliée ;
  3. l'ordre des barres : combien de paires de catégories l'ordre alphabétique classe à
     l'envers (inversions de Kendall) par rapport à l'ordre des valeurs ;
  4. le compte des annotations : quel chiffre clé chaque graphique corrigé porte, et
     combien de chiffres les graphiques « avant » laissaient au lecteur.

Sortie : figures/M10_C04_ecriture_titre_axe_annotation.svg (4 panneaux : l'avant, l'après,
les deux ordres, la hiérarchie visuelle) + le rapport chiffré sur stdout.

Usage : python3 tools/ecriture_M10.py
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
DOSSIER = os.path.join(RACINE, "03_exercices", "dossier_M10")
SOURCE = os.path.join(RACINE, "03_exercices", "dossier_M09")
SORTIE = os.path.join(RACINE, "figures", "M10_C04_ecriture_titre_axe_annotation.svg")
REF = os.path.join(RACINE, "01_socle_donnees", "data", "reference", "chiffres_cites.json")

BLEU, ORANGE, GRIS, VERT, ROUGE = "#1f4e79", "#c96a1a", "#8895a5", "#2e6f5e", "#a1382c"

matplotlib.rcParams["svg.hashsalt"] = "ecriture_M10"
plt.rcParams.update({"font.size": 7.5, "svg.fonttype": "none"})


def sauver(fig, chemin, **kw):
    fig.savefig(chemin, metadata={"Date": None, "Creator": "ecriture_M10.py"}, **kw)


# ----------------------------------------------------------------------
# 1. L'audit des titres, lu dans le code du dossier
# ----------------------------------------------------------------------
def bloc(fichier, fonction):
    """Extrait le corps d'une fonction (`avant` ou `apres`) du script du dossier."""
    txt = open(fichier, encoding="utf-8").read()
    m = re.search(rf"^def {fonction}\(.*?\n(?=^def |\Z)", txt, flags=re.M | re.S)
    return m.group(0) if m else ""


def titre_du_corps(corps):
    """Relève l'appel set_title/suptitle d'un graphique (les titres s'écrivent sur 2 lignes)."""
    m = re.search(r"\.(?:set_title|suptitle)\(", corps)
    if not m:
        return None
    i, prof, depart = m.end(), 1, m.end()
    while i < len(corps) and prof:
        if corps[i] == "(":
            prof += 1
        elif corps[i] == ")":
            prof -= 1
        i += 1
    appel = corps[depart:i - 1]
    texte = re.split(r",\s*(?:fontsize|loc|color|pad|x=|y=)", appel)[0]
    texte = texte.strip().rstrip(",").strip()
    propre = re.sub(r'^(?:f)?["\']', "", texte)
    propre = re.sub(r'["\']$', "", propre)
    propre = re.sub(r"\s+", " ", propre.replace("\n", " ")).strip()
    return texte, propre


def titres_du_bloc(code):
    """Relève, dans un bloc de code, le titre de chaque graphique et ce que la figure porte."""
    trouves = []
    for morceau in re.split(r"\n    # ([A-Z]\d) — ", code)[1:]:
        lettre, corps = morceau[0], morceau
        t = titre_du_corps(corps)
        if t is None:
            continue
        texte, propre = t
        porte_mesure = bool(re.search(r"\d", texte)) or "{" in texte
        trouves.append(dict(cas=lettre, titre=propre, longueur=len(propre),
                            porte_mesure=porte_mesure,
                            unite=bool(re.search(r"FCFA", corps)),
                            source=bool(re.search(r"[Ss]ource", corps)),
                            annotations=len(re.findall(r"\.annotate\(|\.text\(", corps)),
                            axe_a_zero=bool(re.search(r"set_ylim\(\s*0", corps))
                                       or bool(re.search(r"ax\.bar", corps))))
    return trouves


def audit_titres():
    """Compte, graphique par graphique, ce que le titre affirme et ce que la figure porte."""
    avant = bloc(os.path.join(DOSSIER, "rapport_avant", "code_avant.py"), "avant")
    apres = bloc(os.path.join(DOSSIER, "rapport_apres", "code_apres.py"), "apres")
    lignes = (titres_du_bloc(avant) + titres_du_bloc(apres))
    for L in lignes[:len(titres_du_bloc(avant))]:
        L["version"] = "avant"
    for L in lignes[len(titres_du_bloc(avant)):]:
        L["version"] = "apres"
    return lignes


# ----------------------------------------------------------------------
# Les données du fil rouge
# ----------------------------------------------------------------------
def charger():
    v = pd.read_csv(os.path.join(SOURCE, "quincaillerie", "vente.csv"), parse_dates=["date_vente"])
    p = pd.read_csv(os.path.join(SOURCE, "quincaillerie", "produit.csv"))
    ca = (v[~v["est_retour"]].groupby(v["date_vente"].dt.to_period("M"))["montant_ttc"].sum())
    vp = v[~v["est_retour"]].merge(p[["id_produit", "id_categorie"]], on="id_produit", how="left")
    part = (vp.groupby("id_categorie")["montant_ttc"].sum() / 1e6).sort_values(ascending=False)
    return v, ca, part


def mesures_et_planche():
    v, ca, part = charger()
    att = json.load(open(os.path.join(DOSSIER, "ATTENDU.json"), encoding="utf-8"))
    m = att["mesures"]
    mesures = {}

    print("=" * 80)
    print("C04-1 — L'AUDIT DES TITRES : 5 GRAPHIQUES AVANT, 5 APRÈS (relus dans le code)")
    print("=" * 80)
    lignes = audit_titres()
    for L in lignes:
        print(f"  {L['version']:5s} {L['cas']} | {L['longueur']:3d} car. | mesure {int(L['porte_mesure'])} | "
              f"unité {int(L['unite'])} | source {int(L['source'])} | annot. {L['annotations']:2d} | "
              f"axe zéro {int(L['axe_a_zero'])} | « {L['titre'][:56]} »")
    for version in ("avant", "apres"):
        sel = [L for L in lignes if L["version"] == version]
        mesures[f"c04_{version}_titres"] = len(sel)
        mesures[f"c04_{version}_titres_portant_une_mesure"] = sum(L["porte_mesure"] for L in sel)
        mesures[f"c04_{version}_scripts_avec_unite"] = sum(L["unite"] for L in sel)
        mesures[f"c04_{version}_scripts_avec_source"] = sum(L["source"] for L in sel)
        mesures[f"c04_{version}_annotations"] = sum(L["annotations"] for L in sel)
        mesures[f"c04_{version}_axe_zero"] = sum(L["axe_a_zero"] for L in sel)
        mesures[f"c04_{version}_longueur_moyenne_titre"] = round(
            float(np.mean([L["longueur"] for L in sel])), 1)
    print(f"  -> titres portant une mesure : {mesures['c04_avant_titres_portant_une_mesure']}/"
          f"{mesures['c04_avant_titres']} avant, {mesures['c04_apres_titres_portant_une_mesure']}/"
          f"{mesures['c04_apres_titres']} après ; annotations explicites : "
          f"{mesures['c04_avant_annotations']} avant, {mesures['c04_apres_annotations']} après ; "
          f"axes à zéro : {mesures['c04_avant_axe_zero']}/{mesures['c04_avant_titres']} avant, "
          f"{mesures['c04_apres_axe_zero']}/{mesures['c04_apres_titres']} après")

    print()
    print("=" * 80)
    print("C04-2 — L'AXE HONNÊTE : CE QUE LA TRONCATURE MULTIPLIE")
    print("=" * 80)
    mg3 = ca.rolling(3).mean()
    mini, maxi = float(ca.min() / 1e6), float(ca.max() / 1e6)
    base = 0.0
    haut = float(m["d1_axe_max_m"])
    bas_tronque = float(m["d1_axe_min_m"])
    part_zero = (maxi - mini) / (haut - base) * 100
    part_tronq = (maxi - mini) / (haut - bas_tronque) * 100
    facteur = (haut - base) / (haut - bas_tronque)
    mesures["c04_axe_zero_fenetre_m"] = round(haut - base, 1)
    mesures["c04_axe_tronque_fenetre_m"] = round(haut - bas_tronque, 1)
    mesures["c04_hauteur_occupee_zero_pct"] = round(part_zero, 1)
    mesures["c04_hauteur_occupee_tronque_pct"] = round(part_tronq, 1)
    mesures["c04_facteur_amplification"] = round(facteur, 2)
    print(f"  axe à zéro : fenêtre {haut - base:.0f} M, les données occupent {part_zero:.1f} % de la hauteur")
    print(f"  axe tronqué ({bas_tronque:.0f} → {haut:.0f} M) : fenêtre {haut - bas_tronque:.0f} M, "
          f"les données occupent {part_tronq:.1f} % — amplitude apparente × {facteur:.2f}")
    print(f"  variation réelle de la moyenne glissante : {m['d1_variation_mg3_pct']} % "
          f"(brute {m['d1_variation_brute_pct']} %) ; facteur d'exagération mesuré : {m['d1_facteur_exageration']}")

    print()
    print("=" * 80)
    print("C04-3 — L'ORDRE DES BARRES : ALPHABÉTIQUE CONTRE TRIÉ")
    print("=" * 80)
    alpha = part.sort_index()
    par_valeur = part.sort_values(ascending=False)
    rang = {k: i for i, k in enumerate(par_valeur.index)}
    inv = sum(1 for i in range(len(alpha)) for j in range(i + 1, len(alpha))
              if rang[alpha.index[i]] > rang[alpha.index[j]])
    paires = len(alpha) * (len(alpha) - 1) // 2
    mesures["c04_categories"] = int(len(alpha))
    mesures["c04_paires_comparees"] = int(paires)
    mesures["c04_inversions_alphabetique"] = int(inv)
    mesures["c04_inversions_pct"] = round(inv / paires * 100, 1)
    mesures["c04_premier_alpha"] = str(alpha.index[0])
    mesures["c04_dernier_alpha"] = str(alpha.index[-1])
    mesures["c04_premier_valeur"] = str(par_valeur.index[0])
    mesures["c04_dernier_valeur"] = str(par_valeur.index[-1])
    print(f"  ordre alphabétique : {list(alpha.index)}")
    print(f"  ordre des valeurs  : {list(par_valeur.index)}")
    print(f"  paires classées à l'envers : {inv} sur {paires} ({inv/paires*100:.1f} %) — "
          f"la première barre de l'ordre alphabétique ({alpha.index[0]}) est la "
          f"{list(par_valeur.index).index(alpha.index[0]) + 1}e valeur")

    print()
    print("=" * 80)
    print("C04-4 — LES ANNOTATIONS : LE CHIFFRE CLÉ DE CHAQUE GRAPHIQUE CORRIGÉ")
    print("=" * 80)
    annonces = [
        ("g1 · le CA est plat", f"moyenne glissante à {m['d1_variation_mg3_pct']} % d'amplitude"),
        ("g2 · deux graphiques", f"corrélation mesurée r = {m['d2_corr_ca_retours']:+.2f}, non concluante"),
        ("g3 · barres triées", f"de {m['d3_part_min']} % à {m['d3_part_max']} % de part"),
        ("g4 · totaux trimestriels", f"variation des totaux de {m['d4_variation_totaux_pct']} %"),
        ("g5 · échelle annoncée", f"{m['d5_part_sous_250k_pct']} % des ventes sous 250 000 FCFA"),
    ]
    for nom, chiffre in annonces:
        print(f"  {nom:26s} -> {chiffre}")
    mesures["c04_annotations_attendues"] = len(annonces)
    mesures["c04_mediane_annots"] = int(m["d5_mediane_montant"])

    # ------------------------------------------------------------------
    # La planche : avant / après, les deux ordres, la hiérarchie
    # ------------------------------------------------------------------
    fig = plt.figure(figsize=(170 / 25.4, 132 / 25.4), dpi=105)
    gs = fig.add_gridspec(3, 2, hspace=0.78, wspace=0.30, top=0.87, bottom=0.07,
                          left=0.09, right=0.975, height_ratios=[1, 0.85, 0.85])
    t = np.arange(len(ca))
    caM = ca.to_numpy() / 1e6
    mg3M = mg3.to_numpy() / 1e6

    def lib_mois():
        idx = [0, 6, 12, 18, 23]
        return idx, [f"{ca.index[i].year % 100:02d}-{ca.index[i].month:02d}" for i in idx]

    # A — l'avant : titre qui étiquette, axe tronqué
    ax = fig.add_subplot(gs[0, 0])
    ax.plot(t, caM, "-", color=ORANGE, lw=1.0)
    ax.plot(t, mg3M, "-", color=BLEU, lw=2.0)
    ax.set_ylim(mini - 1, maxi + 2)
    i, lab = lib_mois()
    ax.set_xticks(i, lab, fontsize=6.5)
    ax.tick_params(labelsize=6.5)
    ax.set_title("A · avant — « Évolution du chiffre d'affaires »", fontsize=8, loc="left")
    ax.annotate("axe tronqué : de 307 à 350 M\nla platitude devient une pente",
                xy=(0.02, 0.06), xycoords="axes fraction", fontsize=6.5, color=ROUGE,
                bbox=dict(fc="white", ec="none", alpha=0.85, pad=1.2))

    # B — l'après : titre qui affirme, axe à zéro, annotation
    ax = fig.add_subplot(gs[0, 1])
    ax.plot(t, caM, "-", color=ORANGE, lw=1.0, label="CA mensuel")
    ax.plot(t, mg3M, "-", color=BLEU, lw=2.0, label="moyenne glissante 3 mois")
    ax.set_ylim(0, maxi * 1.12)
    ax.set_xticks(i, lab, fontsize=6.5)
    ax.tick_params(labelsize=6.5)
    ax.set_title(f"B · après — « Le CA est plat sur {len(ca)} mois :\n"
                 f"{m['d1_variation_mg3_pct']} % d'amplitude »", fontsize=8, loc="left")
    k = int(np.argmax(mg3M))
    ax.annotate(f"{mg3M.max():.0f} M (pic de la moyenne)", xy=(k, mg3M[k]),
                xytext=(k - 9, maxi * 1.02), fontsize=6.5, color=BLEU,
                arrowprops=dict(arrowstyle="->", color=BLEU, lw=0.7))
    ax.annotate("Source : vente.csv, 24 mois, hors retours", xy=(0.98, 0.02),
                xycoords="axes fraction", fontsize=6, color=GRIS, ha="right")
    ax.legend(fontsize=6, loc="upper right", frameon=False, ncol=1)

    # C — les deux ordres
    ax = fig.add_subplot(gs[1, 0])
    ax.barh(range(8), alpha.to_numpy(), color=GRIS, height=0.62)
    ax.set_yticks(range(8), [f"C{c}" for c in alpha.index], fontsize=6.5)
    ax.tick_params(labelsize=6.5)
    ax.set_xlim(0, 1500)
    ax.set_title("C · ordre alphabétique (l'outil par défaut)", fontsize=8, loc="left")
    ax = fig.add_subplot(gs[1, 1])
    ax.barh(range(8)[::-1], par_valeur.to_numpy(), color=BLEU, height=0.62)
    ax.set_yticks(range(8)[::-1], [f"C{c}" for c in par_valeur.index], fontsize=6.5)
    ax.tick_params(labelsize=6.5)
    ax.set_xlim(0, 1500)
    for j, (c, val) in enumerate(par_valeur.items()):
        ax.annotate(f"{val:.0f} M", (val, 7 - j), xytext=(3, 0), textcoords="offset points",
                    va="center", fontsize=6)
    ax.set_title(f"D · ordre des valeurs : {inv} paires sur {paires}\nétaient à l'envers",
                 fontsize=8, loc="left")

    # E — la hiérarchie visuelle : un chiffre principal, le reste en appui
    ax = fig.add_subplot(gs[2, :])
    ax.axis("off")
    ax.set_title("E · la hiérarchie visuelle : un chiffre principal, deux appuis, une source",
                 fontsize=8, loc="left")
    ax.annotate("15,63 %", (0.02, 0.66), fontsize=16, color=BLEU, va="center")
    ax.annotate("première catégorie", (0.02, 0.46), fontsize=6.5, color="#333333", va="center")
    ax.annotate("8,85 %", (0.21, 0.66), fontsize=11, color=ORANGE, va="center")
    ax.annotate("dernière catégorie", (0.21, 0.46), fontsize=6.5, color="#333333", va="center")
    ax.annotate("× 1,77", (0.38, 0.66), fontsize=11, color=VERT, va="center")
    ax.annotate("rapport entre les deux", (0.38, 0.46), fontsize=6.5, color="#333333", va="center")
    ax.annotate("Source : vente.csv, 50 008 ventes hors retours,\ncatégories 1-8 · classeur M10 · 20/09/2026",
                (0.62, 0.60), fontsize=6.5, color=GRIS, va="center")
    ax.annotate("Le classement fin est impossible (0,05 point sépare C5 et C8) :\n"
                "l'étendue, elle, est nette — c'est elle qu'on annonce.",
                (0.02, 0.16), fontsize=7.5, color="#333333", va="center")

    fig.suptitle("Écrire un graphique : le titre affirme, l'axe est honnête, le chiffre est annoté",
                 fontsize=9, x=0.008, ha="left", y=0.995)
    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    sauver(fig, SORTIE, dpi=105)
    plt.close(fig)
    mesures["c04_planche"] = ("figures/M10_C04_ecriture_titre_axe_annotation.svg "
                              "(5 panneaux : avant, après, deux ordres, hiérarchie)")
    mesures["c04_panneaux"] = 5
    print()
    print(f"  planche : {os.path.relpath(SORTIE, RACINE)} ({os.path.getsize(SORTIE)/1024:.1f} Ko)")
    return mesures


def main():
    m = mesures_et_planche()
    print()
    print(json.dumps(m, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
