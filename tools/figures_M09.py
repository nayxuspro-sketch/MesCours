#!/usr/bin/env python3
"""figures_M09.py — les planches SVG du module M09 (Analyse exploratoire de données).

Six planches (une par chapitre) :
  C01 : les 10 étapes du protocole en chaîne (etape -> question -> outil), 3 jeux ;
  C02 : la matrice « famille de defaut -> controle -> exemple chiffre » ;
  C03 : la decomposition tendance / saisonnalite / bruit, chiffrée ;
  C04 : la boite a outils de preuve (position / recurrence / metier) x 4 cas ;
  C05 : les 3 fausses causes, chacune avec son contre-exemple chiffre ;
  C06 : la table question -> graphique (les 5 questions du module).

Memes contraintes que tools/figures_M08.py :
  * largeur utile 780 px ; extension estimee 0,605 x taille x nb de caracteres ;
  * ancres posees a la main ; jeu de signes latin-1 etendu ; pas de glyphe hors jeu
    (la planche est rendue en PDF, les accents doivent passer).

Usage : python3 tools/figures_M09.py
"""
import os
import random
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(RACINE, "figures")
LARGEUR = 780


def t(x, y, s, taille=13, gras=False, couleur="#1a1a1a", ancre="start"):
    s = str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    poid = ' font-weight="600"' if gras else ""
    return (f'<text x="{x}" y="{y}" font-family="Inter, Segoe UI, sans-serif" font-size="{taille}"'
            f' fill="{couleur}" text-anchor="{ancre}"{poid}>{s}</text>')


def r(x, y, w, h, fond="#ffffff", bord="#c9d3dd", trait=1, rx=4, tirets=""):
    d = f' stroke-dasharray="{tirets}"' if tirets else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fond}" '
            f'stroke="{bord}" stroke-width="{trait}"{d}/>')


def fleche(x1, y1, x2, y2, couleur="#1f4e79"):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{couleur}" stroke-width="1.4" '
            f'marker-end="url(#f)"/>')


def svg_ouverture(hauteur=500):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGEUR} {hauteur}" '
            f'width="{LARGEUR}" height="{hauteur}"><defs>'
            f'<marker id="f" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
            f'<path d="M0,0 L0,6 L7,3 z" fill="#1f4e79"/></marker></defs>')


def fin_svg(g):
    return "".join(g) + "</svg>"


def planche_protocole_c01():
    """C01 : les 10 étapes en chaîne (etape -> question -> outil), 3 jeux."""
    H = 540
    g = [svg_ouverture(H)]
    g.append(t(20, 26, "Le protocole EDA : 10 étapes, un contrat — une étape se déclare, jamais sautée",
               15, True, "#1f4e79"))
    g.append(t(20, 44, "Chaque étape = une question posée au jeu + l'outil principal ; le fil rouge "
               "(quincaillerie) parcourt les 10.", 10, False, "#42566b"))

    etapes = [
        ("1", "Inspecter", "Qu'est-ce que j'ai en main ?", "shape, dtypes, head, info"),
        ("2", "Comprendre", "Que veut dire chaque colonne ?", "la fiche d'entrée (30 min)"),
        ("3", "Détecter", "Doublons, manquants, impossible ?", "duplicated, isna, bornes"),
        ("4", "Statistiques", "Quelle forme par variable ?", "describe, quartiles, value_counts"),
        ("5", "Tendances", "Ca monte, descend, cycle ?", "resample, moyenne glissante"),
        ("6", "Anomalies", "Inhabituel, et comment prouver ?", "iqr, récurrence, métier"),
        ("7", "Relations", "Bougent-elles ensemble ?", "corr, croisé, segments"),
        ("8", "Hypothèses", "Que puis-je affirmer ?", "formulation falsifiable"),
        ("9", "Visuels", "Quel graphique répond ?", "courbe, barres, boxplot, nuage"),
        ("10", "Conclure", "Que dis-je, limites ?", "la note d'EDA (1 page)"),
    ]
    bw, bh = 356, 80
    for i, (num, nom, ques, outil) in enumerate(etapes):
        col, row = i % 2, i // 2
        x = 20 + col * 376
        y = 58 + row * 88
        g.append(r(x, y, bw, bh, "#f4f8fc" if col == 0 else "#fbf7f0",
                   "#8fa8c2" if col == 0 else "#d9b38c", 1.2))
        g.append(t(x + 12, y + 22, num, 13, True, "#1f4e79" if col == 0 else "#7a4a12"))
        g.append(t(x + 34, y + 22, nom, 12, True, "#12365a" if col == 0 else "#5a3a10"))
        g.append(t(x + 12, y + 44, ques, 10, False, "#1a1a1a"))
        g.append(t(x + 12, y + 62, outil, 9.5, False, "#42566b"))
        if col == 0:
            g.append(fleche(x + bw, y + bh / 2, x + bw + 18, y + bh / 2))

    g.append(r(20, 500, 740, 28, "#eef4ea", "#9db88f", 1.2))
    g.append(t(36, 519, "Les 3 jeux = 3 trajets : quincaillerie (les 10 étapes) · santé (arrive en C03) "
               "· scolaire (arrive en C05)", 9.5, True, "#3d5a2e"))
    g.append(t(20, 541, "Le chronomètre (projet M09.P : 3 h) court sur les 10 étapes — la fiche d'entrée "
               "se remplit dans les 30 premières minutes.", 9, False, "#42566b"))
    return fin_svg(g)


def planche_audit_c02():
    """C02 : la matrice « famille de defaut -> controle -> exemple chiffre »."""
    H = 500
    g = [svg_ouverture(H)]
    g.append(t(20, 26, "L'audit (étape 3) : 3 familles de défauts, 3 contrôles, 3 exemples chiffrés",
               15, True, "#1f4e79"))
    g.append(t(20, 44, "Chaque défaut porte sa définition exacte — sans elle, le chiffre n'est pas "
               "publiable (P2 lit la définition).", 10, False, "#42566b"))

    g.append(t(36, 78, "FAMILLE", 10, True, "#42566b"))
    g.append(t(158, 78, "DÉFINITION EXACTE", 10, True, "#42566b"))
    g.append(t(508, 78, "CHIFFRE DU SOCLE", 10, True, "#42566b"))
    g.append(r(20, 86, 740, 2, "#c9d3dd", "#c9d3dd", 1, 0))

    lignes = [
        ("Doublons", "lignes (ou clés) répétées — définies AVANT de compter",
         "7 lignes de stock (5-tuple identique) · 8 métier hors id_vente",
         "contrôle : duplicated(subset=clés métier)", "#f4f8fc", "#8fa8c2"),
        ("Manquants", "valeur absente : NaN OU chaîne vide codée en clair",
         "23 motifs vides sur 18 818 consultations",
         "contrôle : isna().sum() + chaînes vides sur les textes", "#fbf7f0", "#d9b38c"),
        ("Impossible", "hors borne métier ou hors récurrence du flux",
         "4 stocks négatifs (min -12) · 1 date au 2027-01-05",
         "contrôle : bornes métier + récurrence (hier + in - out)", "#f0f4ee", "#9db88f"),
    ]
    for i, (fam, defn, chif, controle, fond, bord) in enumerate(lignes):
        y = 106 + i * 96
        g.append(r(20, y, 740, 86, fond, bord, 1.2))
        g.append(t(36, y + 28, fam, 12, True, "#12365a"))
        g.append(t(158, y + 28, defn, 10, False, "#1a1a1a"))
        g.append(t(508, y + 24, chif[:40], 10, True, "#5a3a10"))
        g.append(t(508, y + 42, chif[40:], 10, True, "#5a3a10"))
        g.append(t(36, y + 62, controle, 9, False, "#42566b"))

    g.append(r(20, 402, 740, 60, "#fff0f0", "#d98c8c", 1.4))
    g.append(t(36, 422, "L'audit vide est suspect, pas réconfortant : 3 contrôles avant de publier « propre ».",
               11, True, "#7a2020"))
    g.append(t(36, 440, "(1) isna par colonne (pas en somme) · (2) chaînes vides sur les textes",
               9.5, False, "#7a2020"))
    g.append(t(36, 456, "(3) clés refermées sur les tables jointes — sur vente.csv : 0 / 0 / 0 vérifié = audit validé vide.",
               9.5, False, "#7a2020"))

    g.append(r(20, 470, 740, 26, "#eef2f7", "#8fa8c2", 1.2))
    g.append(t(36, 489, "Puis l'étape 4 : les statistiques juste nécessaires — médiane 29.0 vs moyenne "
               "25.74/jour, iqr, bornes de Tukey (442 vs -12).", 9.5, True, "#12365a"))
    return fin_svg(g)


def planche_tendances_c03():
    """C03 : la decomposition tendance / saisonnalite / bruit, chiffrée."""
    H = 520
    g = [svg_ouverture(H)]
    g.append(t(20, 26, "Décomposer une série : le lit (tendance), les crues (saison), les vagues (bruit)",
               15, True, "#1f4e79"))
    g.append(t(20, 44, "La bâche (moyenne glissante) pour le lit ; l'amplitude entre positions vs "
               "intra-position pour la saison.", 10, False, "#42566b"))

    g.append(r(20, 60, 440, 300, "#ffffff", "#c9d3dd", 1))
    g.append(t(36, 82, "Série mensuelle du centre (extrait chiffré)", 10.5, True, "#12365a"))
    g.append(fleche(60, 320, 60, 100, "#8895a5"))
    g.append(fleche(60, 320, 430, 320, "#8895a5"))
    g.append(t(52, 336, "mois", 9, False, "#42566b"))
    pts = [(80, 258), (110, 240), (140, 250), (170, 214), (200, 150), (230, 118),
           (260, 132), (290, 140), (320, 246), (350, 262), (380, 254), (410, 236)]
    path = "M" + " L".join(f"{x},{y}" for x, y in pts)
    g.append(f'<path d="{path}" fill="none" stroke="#c96a1a" stroke-width="1.6"/>')
    for x, y in pts:
        g.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#c96a1a"/>')
    g.append(f'<path d="M80,238 L410,232" fill="none" stroke="#1f4e79" stroke-width="2.6"/>')
    g.append(r(168, 100, 130, 190, "#f3e8d8", "#d9b38c", 1, 2, "5 4"))
    g.append(t(176, 96, "été : 853/mois (834-882)", 9, True, "#7a4a12"))
    g.append(t(322, 288, "hiver : 655/mois", 9, True, "#7a4a12"))
    g.append(t(232, 112, "pic 2025-07 : 882", 9, True, "#c96a1a"))
    g.append(t(352, 224, "bâche mg3 : le lit", 9, True, "#1f4e79"))
    g.append(t(84, 316, "déc-2025", 8.5, False, "#42566b"))
    g.append(t(392, 316, "2026", 8.5, False, "#42566b"))
    g.append(f'<line x1="36" y1="342" x2="56" y2="342" stroke="#c96a1a" stroke-width="1.6"/>')
    g.append(t(62, 346, "série (vagues)", 9, False, "#1a1a1a"))
    g.append(f'<line x1="150" y1="342" x2="170" y2="342" stroke="#1f4e79" stroke-width="2.6"/>')
    g.append(t(176, 346, "bâche (lit)", 9, False, "#1a1a1a"))
    g.append(r(250, 336, 20, 12, "#f3e8d8", "#d9b38c", 1, 2, "5 4"))
    g.append(t(276, 346, "crue (saison)", 9, False, "#1a1a1a"))

    g.append(r(478, 60, 282, 300, "#f4f8fc", "#8fa8c2", 1.2))
    g.append(t(494, 84, "La règle du chapitre", 11, True, "#12365a"))
    g.append(t(494, 108, "Un cycle est STRUCTUREL quand", 10, False, "#1a1a1a"))
    g.append(t(494, 128, "l'écart ENTRE positions domine", 10, False, "#1a1a1a"))
    g.append(t(494, 148, "la variabilité DANS chaque position :", 10, False, "#1a1a1a"))
    g.append(r(494, 162, 250, 40, "#ffffff", "#c9d3dd", 1, 2))
    g.append(t(506, 180, "été vs hiver : environ 198", 10, True, "#5a3a10"))
    g.append(t(506, 196, "variabilité intra-été : environ 48", 10, True, "#5a3a10"))
    g.append(t(494, 224, "198 >> 48 (x4) : la saison est", 10, False, "#1a1a1a"))
    g.append(t(494, 242, "structurelle, pas du bruit.", 10, True, "#12365a"))
    g.append(t(494, 270, "Fil rouge (quincaillerie) : la", 10, False, "#1a1a1a"))
    g.append(t(494, 288, "bâche n'est qu'à 17 M d'amplitude", 10, False, "#1a1a1a"))
    g.append(t(494, 306, "vs 10.8 M d'écart-type : PLAT,", 10, False, "#1a1a1a"))
    g.append(t(494, 324, "+1.6 % à mois égal — déclaré.", 10, True, "#12365a"))
    g.append(t(494, 350, "Le zéro-fait : rupture M01 (3 j)", 9.5, False, "#7a2020"))
    g.append(t(494, 366, "au pic de juillet — tendance", 9.5, False, "#7a2020"))
    g.append(t(494, 382, "interrompue, pas retombée.", 9.5, True, "#7a2020"))

    g.append(r(20, 380, 440, 126, "#fff0f0", "#d98c8c", 1.4))
    g.append(t(36, 402, "Le mois partiel ment (décembre 2026 : 28 jours)", 10.5, True, "#7a2020"))
    g.append(t(36, 424, "total : 307 M < 315 M (2025) — « baisse » ?", 10, False, "#7a2020"))
    g.append(t(36, 444, "flux par jour : 11.0 M vs 10.2 M — en réalité +8 %.", 10, True, "#7a2020"))
    g.append(t(36, 466, "Règles : comparer à MOIS ÉGAL, ou au flux", 9.5, False, "#7a2020"))
    g.append(t(36, 482, "par jour — ou DÉCLARER « aucune conclusion »", 9.5, False, "#7a2020"))
    g.append(t(36, 498, "(l'étape se déclare, elle ne se saute pas).", 9.5, True, "#7a2020"))
    return fin_svg(g)


def planche_preuves_c04():
    """C04 : la boite a outils de preuve (position / recurrence / metier) x 4 cas."""
    H = 520
    g = [svg_ouverture(H)]
    g.append(t(20, 26, "L'étape 6 : la borne accuse, la preuve condamne, la décision écrit sa ligne",
               15, True, "#1f4e79"))
    g.append(t(20, 44, "Une anomalie non prouvée est un soupçon — on le signale, on ne le traite pas. "
               "Les 3 témoins, les 4 cas du socle.", 10, False, "#42566b"))

    temoins = [
        ("TÉMOIN 1 — POSITION", "Q1/Q3, iqr, bornes de Tukey", "442 sous la borne : plausible", "#f4f8fc", "#8fa8c2"),
        ("TÉMOIN 2 — RÉCURRENCE", "hier + entrées - sorties = aujourd'hui", "545 déduit pour -12 : condamné", "#fbf7f0", "#d9b38c"),
        ("TÉMOIN 3 — MÉTIER", "stock >= 0 · note sur 20 · période", "pas de -12 boîtes : parle seul", "#f0f4ee", "#9db88f"),
    ]
    for i, (titre, desc1, desc2, fond, bord) in enumerate(temoins):
        x = 20 + i * 253
        g.append(r(x, 60, 240, 92, fond, bord, 1.2))
        g.append(t(x + 12, 82, titre, 10.5, True, "#12365a"))
        g.append(t(x + 12, 104, desc1, 9.5, False, "#1a1a1a"))
        g.append(t(x + 12, 126, desc2, 9.5, True, "#5a3a10"))

    g.append(t(20, 186, "Les 4 cas du socle, jugés (preuve -> décision -> ligne de rapport)", 11, True, "#12365a"))
    g.append(t(36, 214, "CAS", 9.5, True, "#42566b"))
    g.append(t(250, 214, "PREUVE", 9.5, True, "#42566b"))
    g.append(t(470, 214, "DÉCISION", 9.5, True, "#42566b"))
    g.append(r(20, 222, 740, 2, "#c9d3dd", "#c9d3dd", 1, 0))

    cas = [
        ("4 stocks négatifs (-1, -3, -2, -12)", "métier + récurrence (double)",
         "CORRIGER : 411, 253, 278, 545", "#f0f4ee"),
        ("1 date au 2027-01-05 (C000001)", "borne période + 1ère référence",
         "EXCLURE de la série · confirmer source", "#fbf7f0"),
        ("ruptures M01 3j · M02 5j · M04 2j", "zéros vrais (récurrence OK)",
         "GARDER : signal métier, pas défaut", "#fff0f0"),
        ("6 ventes au max 594 363 (fil rouge)", "plafond : 10 x 49 946.47 x 0.19",
         "GARDER : rareté légitime, pas doublon", "#f4f8fc"),
    ]
    for i, (cas, preuve, dec, fond) in enumerate(cas):
        y = 236 + i * 60
        g.append(r(20, y, 740, 52, fond, "#c9d3dd", 1))
        g.append(t(36, y + 30, cas, 10, True, "#1a1a1a"))
        g.append(t(250, y + 30, preuve, 9.5, False, "#42566b"))
        g.append(t(470, y + 30, dec, 10, True, "#5a3a10"))

    g.append(r(20, 484, 740, 30, "#eef2f7", "#8fa8c2", 1.2))
    g.append(t(36, 504, "Jamais la 4e décision : « je supprime » sans ligne — le silence est le seul vice ; "
               "la table P4 se re-joue.", 9.5, True, "#12365a"))
    return fin_svg(g)


def planche_fausses_causes_c05():
    """C05 : les 3 fausses causes, chacune avec son contre-exemple chiffre."""
    H = 520
    g = [svg_ouverture(H)]
    g.append(t(20, 26, "Corrélation, jamais causalité : les 3 fausses causes, chiffrées sur le socle",
               15, True, "#1f4e79"))
    g.append(t(20, 44, "Le brut : absentéisme x moyenne générale = -0.232 (n=400), association négative "
               "modérée. Trois façons de la lire en trop :", 10, False, "#42566b"))

    causes = [
        ("1 — VARIABLE TIERCE (confond)", "la tierce variable (le niveau d'origine)",
         "contrôle par bande de T1 :",
         ["brut (abs T2 x note T2) : -0.206",
          "bande T1 [8,10)  n=107 : -0.145",
          "bande T1 [10,12) n=139 : -0.085",
          "bande T1 [12,14) n=77 : +0.163"],
         "le lien s'EFFONDRE (et change de signe)",
         "une part du lien brut = tierce variable,",
         "pas l'absence en elle-même.",
         "#f4f8fc", "#8fa8c2"),
        ("2 — RÉGRESSION VERS LA MOYENNE", "les extrêmes reviennent vers le milieu",
         "la transition T1 -> T2 :",
         ["T1 < 8 (7.01) -> T2 : 7.21 (monte)",
          "T1 > 14 (14.93) -> T2 : 14.61 (desc.)",
          "moyenne globale : 10.57",
          "les deux sens, même chiffre : 10.57"],
         "les deux extrêmes reviennent vers 10.57",
         "sans qu'on les ait aidés : c'est la variance",
         "d'une note, pas « l'aide a marché ».",
         "#fbf7f0", "#d9b38c"),
        ("3 — SENS INVERSÉ", "B cause A, on affirme A cause B",
         "le fichier ne départage pas :",
         ["absence -> note ? (les absents chutent)",
          "note -> absence ? (chute -> absences)",
          "pas d'intervention, pas de variable",
          "motivation ni d'ordre chronologique"],
         "les deux sens restent compatibles avec",
         "les mêmes chiffres : le fichier ne tranche",
         "Phrase : association, sens non départagé.",
         "#f0f4ee", "#9db88f"),
    ]
    for i, (titre, desc, lab, lignes, l1, l2, l3, fond, bord) in enumerate(causes):
        x = 20 + i * 253
        g.append(r(x, 60, 240, 330, fond, bord, 1.2))
        g.append(t(x + 12, 82, titre, 10.5, True, "#12365a"))
        g.append(t(x + 12, 102, desc, 9, False, "#1a1a1a"))
        g.append(t(x + 12, 126, lab, 9, True, "#42566b"))
        for j, lg in enumerate(lignes):
            g.append(r(x + 12, 136 + j * 26, 216, 21, "#ffffff", "#c9d3dd", 0.8, 2))
            g.append(t(x + 20, 150 + j * 26, lg, 8.5, False, "#1a1a1a"))
        g.append(t(x + 12, 262, l1, 9, True, "#5a3a10"))
        g.append(t(x + 12, 280, l2, 9, False, "#5a3a10"))
        g.append(t(x + 12, 298, l3, 9, True, "#5a3a10"))

    g.append(r(20, 404, 740, 56, "#eef2f7", "#8fa8c2", 1.4))
    g.append(t(36, 426, "Le coefficient va avec ses 4 chiffres : -0.232 · n = 400 · contrôle (bandes de T1) "
               "· limite (proxy, 1 année, sens)", 10.5, True, "#12365a"))
    g.append(t(36, 446, "les 4 ensemble, ou la phrase ne part pas. Test du scale : montants 0.552 -> taux 0.001 "
               "— le scale n'est pas le comportement.", 9.5, False, "#12365a"))

    g.append(r(20, 470, 740, 44, "#f0f4ee", "#9db88f", 1.2))
    g.append(t(36, 488, "Segments (bornes métier, avant de regarder) : 123 / 208 / 69 élèves -> moyennes "
               "11.13 / 10.51 / 9.76", 9.5, True, "#3d5a2e"))
    g.append(t(36, 504, "gradient régulier = la signature d'un lien direct (pas une fausse cause).",
               9.5, False, "#3d5a2e"))
    return fin_svg(g)


def planche_graphiques_c06():
    """C06 : la table question -> graphique (les 5 questions du module)."""
    H = 570
    g = [svg_ouverture(H)]
    g.append(t(20, 26, "Le graphique se choisit PAR QUESTION — la table du module (tout est exécuté)",
               15, True, "#1f4e79"))
    g.append(t(20, 44, "Pas un graphique « joli », celui qui répond. La légende : question + source + n + axe "
               "déclaré s'il n'est pas à zéro.", 10, False, "#42566b"))

    lignes = [
        ("Ca monte, ça descend, ça cycle ?", "courbe (+ bâche)",
         "CA mensuel 307-348 M, mg3 320-337 M", "plat, +1.6 % à mois égal (déclaré)",
         "courbe", "#f4f8fc", "#8fa8c2"),
        ("Les groupes se comparent-ils ?", "barres (+ les n)",
         "panier par mode : écart 2.4 %", "n de 2 552 à 20 175 : c'est le bruit",
         "barres", "#fbf7f0", "#d9b38c"),
        ("La dispersion change par groupe ?", "boxplot",
         "notes par segment : médianes", "11.21 / 10.40 / 9.51 : un gradient",
         "boxplot", "#f0f4ee", "#9db88f"),
        ("Quelle est la forme de la variable ?", "histogramme",
         "montants 762.63 à 594 363 (ratio ~780)", "plateau x6 au maximum (plafond)",
         "histo", "#fff7f0", "#d99a6c"),
        ("Bougent-elles ensemble ?", "nuage (+ le n)",
         "montant x taux : corr 0.001 (n=50 008)", "pas de lien (remise = 45.5 % des ventes)",
         "nuage", "#f4f8fc", "#8fa8c2"),
    ]
    g.append(t(36, 78, "QUESTION", 10, True, "#42566b"))
    g.append(t(330, 78, "GLYPHE", 10, True, "#42566b", "middle"))
    g.append(t(480, 78, "RÉPONSE (sortie exécutée)", 10, True, "#42566b"))
    g.append(r(20, 86, 740, 2, "#c9d3dd", "#c9d3dd", 1, 0))

    for i, (ques, glyph, rep1, rep2, kind, fond, bord) in enumerate(lignes):
        y = 100 + i * 62
        g.append(r(20, y, 740, 54, fond, bord, 1))
        g.append(t(36, y + 22, ques, 10.5, True, "#12365a"))
        g.append(t(36, y + 40, glyph, 9.5, False, "#5a3a10"))
        cx = 330
        if kind == "courbe":
            g.append(f'<path d="M{cx-38},{y+40} L{cx-24},{y+22} L{cx-10},{y+32} L{cx+4},{y+16} '
                     f'L{cx+18},{y+26} L{cx+38},{y+12}" fill="none" stroke="#c96a1a" stroke-width="1.6"/>')
            g.append(f'<path d="M{cx-38},{y+30} L{cx+38},{y+22}" stroke="#1f4e79" stroke-width="2.2"/>')
        elif kind == "barres":
            for j, h in enumerate((26, 24, 27, 23, 28)):
                g.append(r(cx - 36 + j * 16, y + 40 - h, 11, h, "#1f4e79", "#1f4e79", 0, 1))
        elif kind == "boxplot":
            for j in range(3):
                bx = cx - 26 + j * 26
                g.append(r(bx - 7, y + 18, 14, 22, "#ffffff", "#1f4e79", 1, 1))
                g.append(f'<line x1="{bx}" y1="{y+12}" x2="{bx}" y2="{y+46}" stroke="#1f4e79"/>')
                g.append(f'<line x1="{bx-10}" y1="{y+12}" x2="{bx+10}" y2="{y+12}" stroke="#1f4e79"/>')
                g.append(f'<line x1="{bx-10}" y1="{y+46}" x2="{bx+10}" y2="{y+46}" stroke="#1f4e79"/>')
        elif kind == "histo":
            for j, h in enumerate((8, 16, 26, 34, 24, 12, 6, 4)):
                g.append(r(cx - 36 + j * 10, y + 40 - h, 8, h, "#c96a1a", "#c96a1a", 0, 0))
        elif kind == "nuage":
            rng = random.Random(45)
            for _j in range(26):
                px = cx - 34 + rng.random() * 68
                py = y + 14 + rng.random() * 26
                g.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="1.8" fill="#1f4e79" fill-opacity="0.45"/>')
        g.append(t(480, y + 22, rep1, 9.5, True, "#5a3a10"))
        g.append(t(480, y + 40, rep2, 9.5, False, "#5a3a10"))

    g.append(r(20, 428, 740, 44, "#fff0f0", "#d98c8c", 1.4))
    g.append(t(36, 448, "Les 5 contrôles de présentation (la rétro-lecture, dans l'ordre) :", 10.5, True, "#7a2020"))
    g.append(t(36, 464, "(1) question dans le TITRE · (2) axe déclaré si non zéro · (3) couleur avec légende · "
               "(4) log annoncée · (5) n au titre", 9.5, False, "#7a2020"))

    g.append(r(20, 484, 740, 76, "#eef4ea", "#9db88f", 1.4))
    g.append(t(36, 504, "Le livrable de fin : la note d'EDA (1 page par jeu) — affirmation + source + limite",
               10.5, True, "#3d5a2e"))
    g.append(t(36, 522, "« Le CA est plat sur 24 mois (mg3 320-337 M). Source : G1 exécutée. Limite : "
               "décembre 2026 partiel (28 j), exclu. »", 9.5, False, "#3d5a2e"))
    g.append(t(36, 538, "La limite se lit à voix haute : si « et sa limite est que … » reste vide, on recule "
               "l'affirmation.", 9, False, "#3d5a2e"))
    g.append(t(36, 554, "Transition M10 : « Vos résultats sont justes. S'ils sont illisibles, ils ne "
               "serviront à rien. »", 9, True, "#3d5a2e"))
    return fin_svg(g)


def audit(nom, svg):
    """Largeur estimee par ligne et jeu de signes."""
    autorises = set("é·èà—â'\"«»→ê…×î←Éùç▼ô°\xa0§¹²³")
    pire, depasse, hors_jeu = 0, 0, 0
    for m in re.finditer(r"<text (.*?)>([^<]*)</text>", svg):
        at = dict(re.findall(r'(x|font-size|text-anchor)="([^"]+)"', m.group(1)))
        x, taille, ancre, txt = float(at["x"]), float(at["font-size"]), at.get("text-anchor", "start"), m.group(2)
        txt = txt.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        largeur = 0.605 * taille * len(txt)
        fin = x + {"start": largeur, "middle": largeur / 2, "end": 0}[ancre]
        pire = max(pire, fin)
        if fin > 776:
            depasse += 1
            print(f"  [{nom}] deborde (extension {fin:.0f} px) : {txt[:56]!r}")
        inattendus = {c for c in txt if ord(c) > 127 and c not in autorises}
        if inattendus:
            hors_jeu += 1
            print(f"  [{nom}] hors jeu publie : {sorted(inattendus)} dans {txt[:40]!r}")
    print(f"  [{nom}] extension maximale estimee {pire:.0f} px (limite 776) · debordements {depasse} · "
          f"lignes hors jeu {hors_jeu}")
    assert depasse == 0 and hors_jeu == 0, f"planche {nom} non conforme"


def main():
    os.makedirs(FIG, exist_ok=True)
    planches = {
        "M09_C01_protocole_dix_etapes_3_jeux.svg": planche_protocole_c01(),
        "M09_C02_audit_matrice_3_familles.svg": planche_audit_c02(),
        "M09_C03_tendance_saisonnalité_bruit.svg": planche_tendances_c03(),
        "M09_C04_boite_a_outils_preuve_4_cas.svg": planche_preuves_c04(),
        "M09_C05_trois_fausses_causes_chiffrees.svg": planche_fausses_causes_c05(),
        "M09_C06_table_question_graphique.svg": planche_graphiques_c06(),
    }
    for nom, svg in planches.items():
        audit(nom, svg)
        with open(os.path.join(FIG, nom), "w", encoding="utf-8") as fh:
            fh.write(svg)
        print(f"  {nom} ecrit ({len(svg)} octets)")


if __name__ == "__main__":
    main()
