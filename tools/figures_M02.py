#!/usr/bin/env python3
"""Figures SVG du module M02. Style identique à tools/figures_M01.py, texte en DejaVu Sans.

Usage : python3 tools/figures_M02.py  →  figures/M02_C04_boxplot.svg, figures/M02_C05_histogramme.svg
Tous les nombres affichés sont lus dans data/reference/chiffres_cites.json (règle de production n° 3) :
aucune valeur n'est saisie à la main dans ce script.
"""
import json
import os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RACINE, "figures")
REF = os.path.join(RACINE, "01_socle_donnees", "data", "reference")
L = 760
BLEU, VERT, AMBRE, GRIS, ROUGE = "#e8f0fb", "#e8f5ec", "#fdf3dd", "#f0f0ee", "#fbe9e7"
TRAIT, FOND, GRIS_T = "#3c4653", "#ffffff", "#c3ccd8"
TITRE, NOTE = 13.5, 10.5
ALERTES = []

CH = json.load(open(os.path.join(REF, "chiffres_cites.json"), encoding="utf-8"))["M02"]


def f(n):
    """Entier en français, séparateur d' milliers."""
    return f"{int(n):,}".replace(",", " ")


def svg(hauteur, corps, legende=""):
    h = hauteur + (26 if legende else 0)
    entete = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{L}" height="{h}" viewBox="0 0 {L} {h}" '
              f'font-family="DejaVu Sans"><rect width="{L}" height="{h}" fill="{FOND}"/>')
    bas = (f'<text x="8" y="{hauteur + 17}" font-size="11" fill="#6a7382">{legende}</text>' if legende else '') + '</svg>'
    return entete + corps + bas


def _largeur(s, taille):
    return 0.605 * taille * len(s)


def txt(x, y, s, taille=11.5, gras=False, couleur="#1c2430", ancre="start"):
    larg = _largeur(s, taille)
    gauche = x - larg / 2 if ancre == "middle" else x
    if gauche + larg > L - 8 or gauche < 4:
        ALERTES.append(f"débord : « {s[:58]}… » y={y} x={gauche:.0f}")
    return (f'<text x="{x}" y="{y}" font-size="{taille}" font-weight="{"bold" if gras else "normal"}" '
            f'fill="{couleur}" text-anchor="{ancre}">{s}</text>')


def ligne(x1, y1, x2, y2, couleur=TRAIT, épaisseur=1.0, tirets=""):
    t = f' stroke-dasharray="{tirets}"' if tirets else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{couleur}" '
            f'stroke-width="{épaisseur}"{t}/>')


# ------------------------------------------------------------------ C04 : boîte à moustaches
VMIN, VMAX = -200000, 1400000
X0, X1 = 60, 700


def xlin(v):
    return X0 + (v - VMIN) * (X1 - X0) / (VMAX - VMIN)


q1, q3 = CH["panier_p25"], CH["panier_p75"]
med, moy = CH["panier_mediane"], CH["panier_moyenne"]
moust_b, moust_h = CH["c04_moustache_basse"], CH["c04_moustache_haute"]
mini, maxi = CH["panier_min"], CH["panier_max"]
seuil = CH["panier_seuil_iqr"]
n_hors = CH["panier_nb_aberrants_iqr"]

c = [txt(10, 20, "Boîte à moustaches des 316 paniers, échelle linéaire : la moitié du milieu tient à gauche", TITRE, True)]
Yc = 62
c.append(ligne(X0, Yc, xlin(moust_b), Yc, épaisseur=1.1))
c.append(ligne(xlin(moust_h), Yc, xlin(maxi), Yc, épaisseur=1.1))
c.append(ligne(xlin(moust_b), Yc - 12, xlin(moust_b), Yc + 12, épaisseur=1.1))
for i in range(n_hors):                                   # les points hors moustaches, espacés pour rester lisibles
    c.append(f'<circle cx="{xlin(seuil) + 6 + i * 4:.1f}" cy="{Yc + (i % 3 - 1) * 5}" r="1.9" fill="{ROUGE}" '
             f'stroke="{TRAIT}" stroke-width="0.35"/>')
c.append(f'<rect x="{xlin(q1):.1f}" y="{Yc - 20}" width="{xlin(q3) - xlin(q1):.1f}" height="40" '
         f'fill="{BLEU}" stroke="{TRAIT}" stroke-width="1"/>')
c.append(ligne(xlin(med), Yc - 20, xlin(med), Yc + 20, couleur="#1257a6", épaisseur=2.2))
c.append(ligne(xlin(moy), Yc - 26, xlin(moy), Yc + 26, couleur="#8a5b06", épaisseur=1.3, tirets="3,2"))
c.append(ligne(xlin(seuil), Yc - 30, xlin(seuil), Yc + 30, couleur="#9c2f2f", épaisseur=1.0, tirets="2,3"))
c.append(f'<circle cx="{xlin(mini):.1f}" cy="{Yc}" r="2.6" fill="{ROUGE}" stroke="{TRAIT}" stroke-width="0.4"/>')
# repères gradués
for v in (0, 200000, 400000, 600000, 800000, 1000000, 1200000):
    c.append(ligne(xlin(v), 96, xlin(v), 101))
    c.append(txt(xlin(v), 113, f"{v // 1000} k", 9.5, ancre="middle"))
c.append(ligne(X0, 96, X1, 96, couleur=GRIS_T, épaisseur=0.8))
# légende des valeurs
etiq = [("moustache basse", moust_b, "#1257a6"), ("Q1", q1, "#1257a6"), ("médiane", med, "#1257a6"),
        ("Q3", q3, "#1257a6"), ("moustache haute", moust_h, "#1257a6")]
x = 10
for nom, val, col in etiq:
    s = f"{nom} {f(val)}"
    c.append(txt(x, 138, s, 10.5, couleur="#1c2430"))
    x += _largeur(s, 10.5) + 16
c.append(txt(10, 156, f"tirets ocre : la moyenne, {f(moy)} FCFA · rouge pointillé : borne de Tukey, {f(seuil)} FCFA",
             10, couleur="#41505f"))
c.append(txt(10, 171, f"{n_hors} tickets au-dessus de la borne, dont le plus gros à {f(maxi)} FCFA", 10,
             couleur="#41505f"))
c.append(txt(10, 186, f"plus basse valeur {f(mini)} FCFA · la boîte est minuscule devant la queue de droite", 10,
             couleur="#41505f"))
open(os.path.join(OUT, "M02_C04_boxplot.svg"), "w", encoding="utf-8").write(
    svg(196, "".join(c), "Figure — Boîte à moustaches des paniers du magasin 5 (fichier nettoyé, n = 316)."))

# ------------------------------------------------------------------ C05 : histogramme des paniers
classes = CH["c05_classes_50k"]        # [3, 133, 84, 25, 23, 17, 31] — 1re et dernière classes ouvertes
etiq_c = ["négatifs", "0 – 50 k", "50 – 100 k", "100 – 150 k", "150 – 200 k", "200 – 250 k", "250 k et plus"]
Y0, Y1 = 40, 178
X_A, X_B = 96, 700
largeur = (X_B - X_A) / len(classes)
hmax = max(classes)
c = [txt(10, 20, "Combien de tickets dans chaque tranche de 50 000 FCFA (dernière classe ouverte)", TITRE, True)]
c.append(ligne(X_A, Y1, X_B, Y1, couleur=GRIS_T, épaisseur=0.8))
for i, eff in enumerate(classes):
    h = (Y1 - Y0) * eff / hmax
    xa = X_A + i * largeur
    c.append(f'<rect x="{xa + 1.5:.1f}" y="{Y1 - h:.1f}" width="{largeur - 3:.1f}" height="{h:.1f}" '
             f'fill="{BLEU if i else VERT}" stroke="{TRAIT}" stroke-width="0.9"/>')
    c.append(txt(xa + largeur / 2, Y1 - h - 5, f(eff), 11, gras=True, ancre="middle"))
    c.append(txt(xa + largeur / 2, Y1 + 14, etiq_c[i], 9.5, ancre="middle"))
c.append(txt(X_A - 6, Y1 + 4, "0", 9.5, ancre="end"))
c.append(txt(X_A - 6, Y0 + 4, f"hmax", 9.5, ancre="end"))
for v, nom, col, saut in ((med, "médiane", "#1257a6", 4), (moy, "moyenne", "#8a5b06", 4)):
    xv = X_A + (v + 50000) / 350000 * (X_B - X_A)
    c.append(ligne(xv, Y0 - 4, xv, Y1, couleur=col, épaisseur=1.4, tirets="" if nom == "médiane" else "4,2"))
    c.append(txt(xv + saut, Y0 - 8, f"{nom} {f(v)}", 10, couleur=col))
c.append(txt(X_A - 6, Y1 + 16, "tickets", 9, ancre="end"))
c.append(txt(10, Y1 + 30, "133 tickets sur 316 entre 0 et 50 000 FCFA · 3 en dessous de zéro", 10,
             couleur="#41505f"))
c.append(txt(10, Y1 + 44, f"la moyenne ({f(moy)} FCFA) tombe une classe à droite de la médiane ({f(med)} FCFA)",
             10, couleur="#41505f"))
c.append(txt(10, Y1 + 58, f"{CH['c05_tickets_sup_100k']} tickets dépassent 100 000 FCFA "
                          f"({CH['c05_pct_sup_100k']} %) ; {CH['c05_tickets_au_dessus_moyenne']} dépassent la "
                          f"moyenne ({CH['c05_pct_au_dessus_moyenne']} %).", 10, couleur="#41505f"))
open(os.path.join(OUT, "M02_C05_histogramme.svg"), "w", encoding="utf-8").write(
    svg(Y1 + 70, "".join(c), "Figure — Histogramme des paniers, six classes de 50 000 FCFA, la dernière ouverte "
                             "(chiffres lus dans chiffres_cites.json)."))

# ------------------------------------------------------------------ C07 : distribution d'échantillonnage
import numpy as _np
import pandas as _pd

_p = _pd.read_csv(os.path.join(REF, "ventes_magasin5_2025_ATTENDU.csv"), sep=";")
_pan = _p.groupby("n_ticket").montant_ttc.sum().to_numpy(dtype=float)
_N = len(_pan)
_tir, _k, _graine = CH["c07_tirages"], CH["c07_taille_tirage"], CH["c07_graine"]
_r = _np.random.default_rng(_graine)
_moy = _pan[_np.argsort(_r.random((_tir, _N)), axis=1)[:, :_k]].mean(axis=1)
_r = _np.random.default_rng(_graine)
_med = _np.median(_pan[_np.argsort(_r.random((_tir, _N)), axis=1)[:, :_k]], axis=1)
assert int(round(_moy.std(ddof=1))) == CH["c07_sd_dist_moyenne_n30"], "tirages non conformes à chiffres_cites.json"
assert int(round(_med.std(ddof=1))) == CH["c07_sd_dist_mediane_n30"], "tirages non conformes à chiffres_cites.json"

PAS = 20000
BORDS = list(range(0, 300001, PAS))
hA = _np.histogram(_moy, bins=BORDS)[0]
hB = _np.histogram(_med, bins=BORDS)[0]
hmax = max(int(hA.max()), int(hB.max()))
XA, XB = 96, 700
HAUT, BAS = 46, 122          # panneau haut : les moyennes
HC, BC = 176, 252            # panneau bas : les médianes


def xvv(v):
    return XA + v / BORDS[-1] * (XB - XA)


def d1(v):
    return f"{v:.1f}".replace(".", ",")


c = [txt(10, 16, f"Ce que donne le hasard : {f(_tir)} tirages de {_k} tickets dans l'extrait (graine {_graine})",
         TITRE, True)]
c.append(txt(XA - 6, HAUT + 6, f"hmax {hmax}", 9, ancre="end", couleur="#41505f"))
PANNEAUX = [
    (HAUT, BAS, hA, "moyennes des tirages",
     ((CH["panier_moyenne"], "#1257a6", "valeur de l'extrait", "4,2"),
      (CH["c07_pop_moyenne_panier"], "#8a5b06", "valeur du mois complet", ""))),
    (HC, BC, hB, "médianes des tirages",
     ((CH["panier_mediane"], "#1257a6", "extrait", "4,2"),
      (CH["c07_pop_mediane_panier"], "#8a5b06", "mois complet", ""))),
]
for ytop, ybot, hh, titre, etiq in PANNEAUX:
    c.append(ligne(XA, ybot, XB, ybot, couleur=GRIS_T, épaisseur=0.8))
    c.append(txt(XB - 132, ytop - 20, titre, 10.5, gras=True))
    for i in range(len(hh)):
        n = int(hh[i])
        if not n:
            continue
        h = (ybot - ytop) * n / hmax
        xa = XA + (XB - XA) * i / len(hh)
        w = (XB - XA) / len(hh)
        c.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" stroke-width="0.8"/>'
                 % (xa + 0.8, ybot - h, w - 1.6, h, BLEU, TRAIT))
    for pos, (v, col, nom, tirets) in enumerate(etiq):
        xv = xvv(v)
        c.append(ligne(xv, ytop - 4, xv, ybot, couleur=col, épaisseur=1.4, tirets=tirets))
        if pos:
            c.append(txt(xv + 5, ytop - 20, f"{nom} {f(v)}", 10, couleur=col))
        else:
            c.append(txt(xv - 5, ytop - 20, f"{nom} {f(v)}", 10, couleur=col, ancre="end"))
lo, hi = CH["c07_ic95_dist_moyenne_n30"]
c.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#1257a6" opacity="0.07"/>'
         % (xvv(lo), HAUT - 4, xvv(hi) - xvv(lo), BAS - HAUT + 8))
for v in (0, 60000, 120000, 180000, 240000, 300000):
    c.append(txt(xvv(v), BC + 14, f(v), 9.5, ancre="middle"))
c.append(txt(8, BC + 30, f"bande bleue = les 95 % du milieu, de {f(lo)} à {f(hi)} FCFA, soit un facteur "
                         f"{d1(hi / lo)}", 10, couleur="#41505f"))
c.append(txt(8, BC + 44, f"écart type des moyennes observé {f(_moy.std(ddof=1))} · théorique "
                         f"{f(CH['c07_theorie_sd_racine_n30'])} · corrigé du tirage sans remise "
                         f"{f(CH['c07_theorie_sd_corrigee_n30'])}", 10, couleur="#41505f"))
c.append(txt(8, BC + 58, f"{f(_tir)} tirages sans remise de {_k} paniers parmi {_N} : un tirage sur vingt tombe "
                         f"hors de la bande", 10, couleur="#41505f"))
open(os.path.join(OUT, "M02_C07_distribution_echantillonnage.svg"), "w", encoding="utf-8").write(
    svg(BC + 72, "".join(c), "Figure — Distribution d'échantillonnage de la moyenne et de la médiane des paniers "
                             "(n = 30), calculée sur le fichier nettoyé du projet M01."))

# ------------------------------------------------------------------ C08 : forêt des six comparaisons
PAIRES = CH["c08_paires"]
import unicodedata as _ud


def _sans_accent(s):
    return "".join(ch for ch in _ud.normalize("NFKD", str(s)) if not _ud.combining(ch))


_noms = _pd.read_csv(os.path.join(REF, "ventes_magasin5_2025_ATTENDU.csv"), sep=";")
_eta = {}
for v in sorted(_noms.vendeur.unique()):
    _eta["_".join(_sans_accent(v).lower().split())] = str(v).split()[-1]


def libelle(cle):
    a, b = cle.split("__")
    return f"{_eta[a]} − {_eta[b]}"


def slug(nom):
    return "_".join(str(nom).lower().split())


rang = sorted(PAIRES, key=lambda k: -PAIRES[k]["ecart"])
VMIN, VMAX = -60000, 80000
XA2, XB2 = 232, 640
y0, dy = 44, 26


def xv2(v):
    return XA2 + (v - VMIN) / (VMAX - VMIN) * (XB2 - XA2)


c = [txt(10, 16, "Écart de montant moyen par ligne entre vendeurs, avec intervalle de confiance à 95 %", TITRE, True)]
c.append(ligne(xv2(0), y0 - 10, xv2(0), y0 + dy * len(rang) + 6, couleur="#8a5b06", épaisseur=1.2, tirets="4,2"))
for i, cle in enumerate(rang):
    v = PAIRES[cle]
    y = y0 + i * dy
    c.append(txt(XA2 - 12, y + 12, libelle(cle), 11, ancre="end"))
    c.append(ligne(xv2(v["ic_bas"]), y + 8, xv2(v["ic_haut"]), y + 8, couleur=GRIS_T, épaisseur=2.2))
    for born in (v["ic_bas"], v["ic_haut"]):
        c.append(ligne(xv2(born), y + 3, xv2(born), y + 13, couleur=TRAIT, épaisseur=1.0))
    c.append(f'<rect x="{xv2(v["ecart"]) - 4:.1f}" y="{y + 4:.1f}" width="8" height="8" fill="{BLEU}" '
             f'stroke="{TRAIT}" stroke-width="0.9"/>')
    c.append(txt(XB2 + 14, y + 12, f"p = {v['p_welch']:,}".replace(".", ","), 10, couleur="#41505f"))
for v in (-60000, -30000, 0, 30000, 60000, 80000):
    c.append(ligne(xv2(v), y0 + dy * len(rang) + 6, xv2(v), y0 + dy * len(rang) + 11, couleur=GRIS_T))
    c.append(txt(xv2(v), y0 + dy * len(rang) + 24, f(v), 9.5, ancre="middle"))
bas = y0 + dy * len(rang) + 38
c.append(txt(8, bas, f"le plus petit p des six comparaisons vaut {CH['c08_p_min_comparaisons']:,} — aucun écart "
                   f"n'est établi au seuil de 5 %".replace(".", ","), 10, couleur="#41505f"))
c.append(txt(8, bas + 14, f"première ligne, « {libelle(rang[0])} » : écart {f(PAIRES[rang[0]]['ecart'])}, intervalle "
                         f"[{f(PAIRES[rang[0]]['ic_bas'])} ; {f(PAIRES[rang[0]]['ic_haut'])}]",
             10, couleur="#41505f"))
c.append(txt(8, bas + 28, f"n par groupe : {CH['c08_n_bationo']} et {CH['c08_n_ilboudo']} lignes ; marge de "
                         f"détection à 80 % de puissance : {f(CH['c08_mde_puissance80'])} FCFA", 10, couleur="#41505f"))
open(os.path.join(OUT, "M02_C08_foret_comparaisons.svg"), "w", encoding="utf-8").write(
    svg(bas + 42, "".join(c), "Figure — Six comparaisons deux à deux sur les montants par ligne : tous les "
                              "intervalles contiennent zéro."))


if ALERTES:
    print("\n".join(dict.fromkeys(ALERTES)))
    raise SystemExit("corriger les débordements ci-dessus (largeur max %d px)" % (L - 8))
print("4 figures M02 écrites dans", OUT)
