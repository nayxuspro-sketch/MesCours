#!/usr/bin/env python3
"""figures_M08.py — les planches SVG du module M08 (Python pour l'analyse de donnees).

Huit planches prevues (une par chapitre). Pour l'instant, les planches C01 et C02
sont generees ; les planches C03 a C08 seront ajoutees au fil de l'eau (1 push par chapitre).

Memes contraintes que tools/figures_M07.py :
  * largeur utile 780 px ; texte jamais plus large que 0,605 x taille x nb de caracteres ;
  * ancres posees a la main (``start`` par defaut, ``middle`` pour les chiffres centres) ;
  * jeu de signes latin-1 etendu (accents, guillemets francais, fleche ->, etc.) ;
  * pas de glyphe hors latin-1 : la planche est rendue en PDF, les accents doivent passer.

Usage : python3 tools/figures_M08.py
"""
import os
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(RACINE, "figures")
LARGEUR, HAUTEUR = 780, 500
FACTEUR = 0.605


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


def svg_ouverture(largeur=LARGEUR, hauteur=HAUTEUR):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largeur} {hauteur}" '
            f'width="{largeur}" height="{hauteur}"><defs>'
            f'<marker id="f" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
            f'<path d="M0,0 L0,6 L7,3 z" fill="#1f4e79"/></marker></defs>')


def fin_svg(g):
    return "".join(g) + "</svg>"


def planche_4_couches():
    """Planche 1 - C01 : les 4 couches de l'environnement Python (machine, interpreteur,
    paquets, projet) avec le venv comme paroi et les symptomes rattaches a leur couche."""
    g = [svg_ouverture()]
    g.append(t(20, 26, "Les 4 couches de l'environnement Python", 15, True, "#1f4e79"))
    g.append(t(20, 46, "Chaque symptome d'installation se rattache a UNE couche — la nommer, "
               "c'est diagnostiquer.", 10, False, "#42566b"))

    couches = [
        (392, 74, "1 · LA MACHINE", "votre ordinateur : Windows, disque, memoire — on la respecte",
         "#eef2f6", "#8fa3b5"),
        (308, 78, "2 · L'INTERPRETEUR", "Python 3.13 lit le code ligne a ligne — installe UNE fois, case PATH",
         "#dbe7f3", "#5b7fa6"),
        (220, 82, "3 · LES PAQUETS", "pip + pandas, numpy… : la couche qui change le plus — "
         "c'est ELLE qu'on isole", "#cfe0f1", "#2f5d8a"),
        (128, 84, "4 · LE PROJET", "scripts, donnees, requirements.txt — se versionne (Git) "
         "et se partage", "#b7d3ec", "#1f4e79"),
    ]
    for y, h, titre, detail, fond, bord in couches:
        g.append(r(300, y, 460, h, fond, bord, 1.2))
        g.append(t(316, y + 24, titre, 13, True, "#12365a"))
        g.append(t(316, y + 46, detail, 10, False, "#33475b"))

    g.append(r(292, 212, 476, 98, "none", "#b3541e", 1.6, 8, "6 4"))
    g.append(t(560, 205, "venv — la trousse scellée du projet", 10, True, "#b3541e", "middle"))

    g.append(fleche(360, 308, 360, 302))
    g.append(t(372, 300, "pip — la boutique (python -m pip install)", 10, False, "#7a3b12"))

    g.append(fleche(530, 212, 530, 220))
    g.append(t(542, 219, "le projet importe les paquets", 9, False, "#42566b"))

    g.append(t(20, 96, "Le diagnostic par couche", 12, True, "#7a3b12"))
    symptomes = [
        (118, 44, "« python n'est pas reconnu »", "→ couche 2 : PATH non coche", 347),
        (172, 44, "ModuleNotFoundError", "→ couche 3 : mauvaise trousse", 261),
        (226, 44, "le notebook ne voit pas", "les paquets → couche 3 (noyau)", 261),
        (280, 44, "« ca tourne ici, pas", "chez lui » → couche 4", 170),
    ]
    for y, h, l1, l2, cible in symptomes:
        g.append(r(20, y, 240, h, "#fff7ef", "#d99a6c", 1))
        g.append(t(32, y + 18, l1, 10, True, "#7a3b12"))
        g.append(t(32, y + 34, l2, 10, False, "#7a3b12"))
        g.append(fleche(260, y + h / 2, 298, cible, "#b3541e"))

    g.append(r(20, 470, 740, 24, "#f4f7fa", "#c9d3dd", 1))
    g.append(t(380, 486, "Règle : un symptôme = une couche. PATH (2) · trousse (3) · noyau (3) · "
               "requirements (4) — dans cet ordre.", 10, False, "#12365a", "middle"))

    return fin_svg(g)


def planche_types_c02():
    """Planche 2 - C02 : les 4 types de base et les operations qu'ils autorisent (matrice),
    avec les 4 erreurs de famille en bas."""
    g = [svg_ouverture()]
    g.append(t(20, 26, "Les 4 types de base : la famille autorise les operations", 15, True, "#1f4e79"))
    g.append(t(20, 46, "type(x) dit la famille ; la famille decide ce qui passe et ce qui proteste.",
               10, False, "#42566b"))

    colonnes = [(20, "Type"), (150, "+ (addition)"), (320, "comparaison"),
                (480, "conversion"), (620, "en condition")]
    for x, nom in colonnes:
        g.append(t(x, 84, nom, 11, True, "#12365a"))
    g.append(r(20, 92, 740, 2, "#c9d3dd", "#c9d3dd", 1, 0))

    g.append(r(20, 100, 740, 50, "#ffffff", "#c9d3dd", 1))
    g.append(t(24, 130, "int", 12, True, "#1f4e79"))
    g.append(t(150, 118, "1500 + 500 = 2000", 9, False, "#33475b"))
    g.append(t(150, 134, "17 // 5 = 3 · 17 % 5 = 2", 9, False, "#33475b"))
    g.append(t(320, 118, "1500 < 2000 → True", 9, False, "#33475b"))
    g.append(t(320, 134, "1000 <= 1200 < 1500 (chaînée)", 9, False, "#33475b"))
    g.append(t(480, 118, "int('1500') → 1500", 9, False, "#33475b"))
    g.append(t(480, 134, "str(1500) → '1500'", 9, False, "#33475b"))
    g.append(t(620, 118, "1500 → True", 9, False, "#33475b"))
    g.append(t(620, 134, "0 → False (le piège du if)", 9, False, "#7a3b12"))

    g.append(r(20, 160, 740, 50, "#ffffff", "#c9d3dd", 1))
    g.append(t(24, 190, "float", 12, True, "#2f5d8a"))
    g.append(t(150, 178, "1500.5 + 0.5 = 1501.0", 9, False, "#33475b"))
    g.append(t(150, 194, "500 * 1.19 = 595.0 (TVA 2026)", 9, False, "#33475b"))
    g.append(t(320, 178, "1500.5 < 2000 → True", 9, False, "#33475b"))
    g.append(t(320, 194, "0.1 + 0.2 != 0.3 (approximatif)", 9, False, "#7a3b12"))
    g.append(t(480, 178, "float('1500.5') → 1500.5", 9, False, "#33475b"))
    g.append(t(480, 194, "le point, pas la virgule", 9, False, "#7a3b12"))
    g.append(t(620, 178, "1500.5 → True", 9, False, "#33475b"))
    g.append(t(620, 194, "0.0 → False", 9, False, "#33475b"))

    g.append(r(20, 220, 740, 50, "#ffffff", "#c9d3dd", 1))
    g.append(t(24, 250, "str", 12, True, "#7a3b12"))
    g.append(t(150, 238, "'15' + '00' = '1500' (concat.)", 9, False, "#33475b"))
    g.append(t(150, 254, "pas d'addition de nombres", 9, False, "#7a3b12"))
    g.append(t(320, 238, "'Ouaga' < 'Bobo' → True (alpha)", 9, False, "#33475b"))
    g.append(t(320, 254, "la casse compte : 'A' < 'a'", 9, False, "#33475b"))
    g.append(t(480, 238, "int('1500,50') → ValueError", 9, True, "#b3541e"))
    g.append(t(480, 254, "recette : replace puis float", 9, False, "#7a3b12"))
    g.append(t(620, 238, "'x' → True (texte non vide)", 9, False, "#33475b"))
    g.append(t(620, 254, "'' → False (texte vide)", 9, False, "#7a3b12"))

    g.append(r(20, 280, 740, 50, "#ffffff", "#c9d3dd", 1))
    g.append(t(24, 310, "bool", 12, True, "#5b7fa6"))
    g.append(t(150, 298, "and · or · not (pas de +)", 9, False, "#33475b"))
    g.append(t(150, 314, "priorité : not, and, or (comme SQL)", 9, False, "#33475b"))
    g.append(t(320, 298, "True == True → True", 9, False, "#33475b"))
    g.append(t(320, 314, "True == 1 → True (attention)", 9, False, "#7a3b12"))
    g.append(t(480, 298, "bool(0) → False", 9, False, "#33475b"))
    g.append(t(480, 314, "bool(1500) → True", 9, False, "#33475b"))
    g.append(t(620, 298, "True / False", 9, False, "#33475b"))
    g.append(t(620, 314, "le if les lit directement", 9, False, "#33475b"))

    g.append(r(20, 340, 740, 34, "#f4f7fa", "#8fa3b5", 1, 4, "5 3"))
    g.append(t(24, 362, "list · tuple · dict · set", 11, True, "#42566b"))
    g.append(t(190, 362, "les conteneurs — C04 : des listes de ces 4 types, des clés vers valeurs",
               9, False, "#42566b"))

    g.append(r(20, 386, 740, 100, "#fff7ef", "#d99a6c", 1.2))
    g.append(t(36, 408, "Les 4 protestations du débutant (C02 §5.6) — le nom de la famille d'abord :",
               10, True, "#7a3b12"))
    g.append(t(36, 428, "SyntaxError — le texte ne se lit pas (deux-points manquant)", 9, False, "#7a3b12"))
    g.append(t(36, 444, "NameError — le nom n'existe pas (montannt, ou cellule Jupyter non exécutée)", 9, False, "#7a3b12"))
    g.append(t(36, 460, "TypeError — mauvaise famille (1500 + 'abc')", 9, False, "#7a3b12"))
    g.append(t(36, 476, "ValueError — mauvaise valeur (int('1500,50'))", 9, False, "#7a3b12"))

    return fin_svg(g)


def planche_decider_repetir_c03():
    """Planche 3 - C03 : l'echelle if/elif/else a gauche, la boucle a droite
    (for, while, break, continue, for...else), avec les regles en bas."""
    g = [svg_ouverture()]
    g.append(t(20, 26, "Décider et répéter : le flux de plusieurs valeurs", 15, True, "#1f4e79"))
    g.append(t(20, 46, "C02 a donné la grammaire d'une valeur ; C03 donne le flux : carrefour, tapis, porte de sortie.",
               10, False, "#42566b"))

    # --- Gauche : l'echelle de decision ---
    g.append(t(20, 84, "Décider — l'échelle if/elif/else", 12, True, "#12365a"))
    echelons = [
        (100, "if total < 1 000", "→ comptant", "#ffffff"),
        (156, "elif total <= 15 000", "→ dossier", "#ffffff"),
        (212, "else", "→ financement (le reste)", "#f4f7fa"),
    ]
    for y, cond, res, fond in echelons:
        g.append(r(40, y, 310, 48, fond, "#5b7fa6", 1.2))
        g.append(t(54, y + 20, cond, 11, True, "#12365a"))
        g.append(t(54, y + 38, res, 10, False, "#7a3b12"))
        if y < 212:
            g.append(fleche(350, y + 48, 350, y + 56))
    g.append(t(40, 282, "la 1re condition vraie gagne — le reste est sauté", 9, False, "#33475b"))
    g.append(t(40, 298, "(le CASE WHEN de M06, ligne par ligne)", 9, False, "#33475b"))
    g.append(t(40, 314, "l'indentation EST la syntaxe : 4 espaces par niveau", 9, True, "#b3541e"))

    # --- Droite : la boucle ---
    g.append(t(400, 84, "Répéter — for / while", 12, True, "#12365a"))
    g.append(r(410, 100, 340, 58, "#eef2f6", "#8fa3b5", 1.2))
    g.append(t(422, 116, "for : le tapis roulant (5 magasins)", 9, True, "#33475b"))
    magasins_courts = ["Ouaga C.", "Patte d'Oie", "Bobo C.", "Bobo S.", "Koudougou"]
    for i, nom in enumerate(magasins_courts):
        x = 418 + i * 67
        g.append(r(x, 126, 60, 22, "#ffffff", "#5b7fa6", 1, 3))
        g.append(t(x + 30, 141, nom, 8, False, "#12365a", "middle"))

    g.append(r(410, 170, 340, 40, "#dbe7f3", "#5b7fa6", 1.2))
    g.append(t(422, 188, "while : « tant que credit > 0 » — la fin est votre contrat", 9, False, "#33475b"))
    g.append(t(422, 202, "sans break ni décrement : tuée à 2 s dans l'atelier (code 124)", 8, False, "#b3541e"))

    g.append(r(410, 222, 165, 56, "#fff7ef", "#d99a6c", 1.2))
    g.append(t(422, 240, "break", 11, True, "#b3541e"))
    g.append(t(422, 256, "sortir tout de suite", 8, False, "#7a3b12"))
    g.append(t(422, 269, "le rapport dit 7 sur 10", 8, False, "#7a3b12"))

    g.append(r(585, 222, 165, 56, "#fff7ef", "#d99a6c", 1.2))
    g.append(t(597, 240, "continue", 11, True, "#b3541e"))
    g.append(t(597, 256, "sauter le tour, repartir", 8, False, "#7a3b12"))
    g.append(t(597, 269, "compter les pourries", 8, False, "#7a3b12"))

    g.append(t(410, 298, "for...else : l'else parle si personne n'a cassé", 9, False, "#33475b"))
    g.append(t(410, 314, "(le « magasin introuvable » sans variable drapeau)", 9, False, "#33475b"))

    # --- Bandeau bas : compréhensions + zip + regles ---
    g.append(r(20, 330, 740, 64, "#f4f7fa", "#c9d3dd", 1))
    g.append(t(36, 350, "Résumer : [m for m in montants if m > 1000] — le tapis avec filtre, en une ligne", 9, True, "#12365a"))
    g.append(t(36, 368, "zip(magasins, surfaces) : deux listes en lockstep — le SELECT de 2 colonnes, en Python", 9, False, "#33475b"))
    g.append(t(36, 386, "Règles : for si on compte · while si on ne compte pas · compréhension = 1 niveau, 1 condition",
               9, False, "#33475b"))

    return fin_svg(g)


def planche_5_conteneurs_c04():
    """Planche 4 - C04 : les 5 conteneurs + le tri, chacun avec sa question
    metier, son operateur signature et son equivalent SQL."""
    g = [svg_ouverture()]
    g.append(t(20, 26, "Ranger : 5 conteneurs, 5 questions métier", 15, True, "#1f4e79"))
    g.append(t(20, 46, "Choisir le contenant, c'est choisir la réponse — l'autre, c'est du débogage.",
               10, False, "#42566b"))

    cases = [
        (20, 90, "liste", "#1f4e79", "« le n-ieme ? » — l'ordre", "l[i] · l[1:3] · append",
         "la ligne n a l'index n-1", "IndexError sinon"),
        (260, 90, "tuple", "#2f5d8a", "« le fait figé » — la clé", "n, p = t · clé de dict",
         "immuable : scellé", "TypeError si on répare"),
        (500, 90, "str", "#7a3b12", "« le texte propre »", "strip · split · replace",
         "format français : replace puis float", "f\"{158140:,.0f}\""),
        (20, 225, "dict", "#5b7fa6", "« le comptage par… »", "d.get(k, 0) + 1",
         "= le GROUP BY de M06", "KeyError sans .get"),
        (260, 225, "set", "#b3541e", "« combien de distincts ? »", "len(set(x)) · c1 & c2",
         "= COUNT(DISTINCT) · JOIN interne", "le tamis : doublons sortis"),
        (500, 225, "tri", "#12365a", "« le top N »", "sorted(items, key=…)[:n]",
         "= ORDER BY … LIMIT n", "sorted renvoie · sort modifie"),
    ]
    for x, y, nom, couleur, question, op, note, er in cases:
        g.append(r(x, y, 220, 118, "#ffffff", "#c9d3dd", 1.2))
        g.append(r(x, y, 220, 30, couleur, couleur, 0, 4))
        g.append(t(x + 12, y + 21, nom, 12, True, "#ffffff"))
        g.append(t(x + 12, y + 52, question, 9, True, "#33475b"))
        g.append(t(x + 12, y + 72, op, 9, False, "#12365a"))
        g.append(t(x + 12, y + 92, note, 8, False, "#42566b"))
        g.append(t(x + 12, y + 108, er, 8, False, "#7a3b12"))

    g.append(r(20, 368, 740, 44, "#f4f7fa", "#c9d3dd", 1))
    g.append(t(36, 388, "C07 : le DataFrame reprend tout — une colonne = une liste indexée (loc/iloc),",
               9, True, "#12365a"))
    g.append(t(36, 404, "une table = un dictionnaire de colonnes — les 50 008 lignes du socle attendent.",
               9, False, "#33475b"))

    return fin_svg(g)


def planche_traceback_c05():
    """Planche 5 - C05 : lire une traceback — la pile d'appels annotee
    (cadres, ligne fautive, message) + la discipline et les 5 familles."""
    g = [svg_ouverture()]
    g.append(t(20, 26, "Lire une traceback : les 3 couches", 15, True, "#1f4e79"))
    g.append(t(20, 46, "Une erreur avec des fonctions a une hauteur : la pile d'appels. "
               "La lire, c'est le travail.", 10, False, "#42566b"))

    # Boite gauche : la traceback reelle (NameError, 2 cadres)
    g.append(r(20, 70, 430, 272, "#ffffff", "#8fa3b5", 1.2))
    g.append(t(36, 92, "La protestation réelle (exécutée dans l'atelier) :", 9, True, "#42566b"))
    lignes = [
        (116, "Traceback (most recent call last):", "#42566b", False),
        (138, '  File "<string>", line 4, in <module>', "#12365a", True),
        (158, "    print(calculer_net(1500))", "#12365a", False),
        (178, '  File "<string>", line 3, in calculer_net', "#12365a", True),
        (198, "    return montant * (1 - remise)", "#12365a", False),
        (218, "                          ^^^^^^", "#b3541e", True),
        (244, "NameError: name 'remise' is not defined", "#b3541e", True),
    ]
    for y, s, couleur, gras in lignes:
        g.append(t(36, y, s, 9.5, gras, couleur))

    # Boites d'annotation (droite)
    g.append(r(466, 84, 294, 62, "#eef2f6", "#5b7fa6", 1.2))
    g.append(t(478, 104, "1 · La pile d'appels", 10, True, "#12365a"))
    g.append(t(478, 122, "le chemin parcouru, du haut vers le bas", 9, False, "#33475b"))
    g.append(t(478, 136, "(le module appelle calculer_net)", 8, False, "#42566b"))

    g.append(r(466, 162, 294, 62, "#fff7ef", "#d99a6c", 1.2))
    g.append(t(478, 182, "2 · La ligne fautive + la fleche", 10, True, "#7a3b12"))
    g.append(t(478, 200, "l'erreur est DANS la fonction ;", 9, False, "#33475b"))
    g.append(t(478, 214, "l'appel (cadre du haut) est le témoin", 8, False, "#42566b"))

    g.append(r(466, 240, 294, 62, "#f4f7fa", "#8fa3b5", 1.2))
    g.append(t(478, 260, "3 · Le message, tout en bas", 10, True, "#12365a"))
    g.append(t(478, 278, "le nom de la famille d'abord :", 9, False, "#33475b"))
    g.append(t(478, 292, "NameError, pas la phrase", 8, False, "#42566b"))

    # Flèches des annotations vers les zones
    g.append(fleche(466, 115, 452, 140, "#5b7fa6"))
    g.append(fleche(466, 193, 452, 200, "#b3541e"))
    g.append(fleche(466, 271, 452, 244, "#8fa3b5"))

    # Bandeau bas : discipline + familles
    g.append(r(20, 368, 740, 76, "#f4f7fa", "#c9d3dd", 1))
    g.append(t(36, 390, "La discipline : lire de haut en bas pour le POURQUOI, s'arrêter en bas pour le QUOI.",
               10, True, "#12365a"))
    g.append(t(36, 412, "Les 5 familles du debutant : SyntaxError (texte) · NameError (nom) · "
               "TypeError (famille)", 9, False, "#33475b"))
    g.append(t(36, 430, "· ValueError (valeur) · KeyError / FileNotFoundError (cle / fichier)", 9, False, "#33475b"))

    return fin_svg(g)


def planche_boucle_vecteur_c06():
    """Planche 6 - C06 : la mesure boucle for vs ligne vectorisee
    (les 2 mesures de l'atelier, les 2 rapports, la lecon sur la publication)."""
    g = [svg_ouverture()]
    g.append(t(20, 26, "Mesurer la vecteurisation : boucle for vs une ligne", 15, True, "#1f4e79"))
    g.append(t(20, 46, "Mesuré le 19/09/2026 (atelier) — 50 008 montants réels du socle ; "
               "le rapport tient, l'absolu change de machine.", 10, False, "#42566b"))

    # --- Panneau 1 : la somme ---
    g.append(r(20, 70, 360, 272, "#ffffff", "#c9d3dd", 1.2))
    g.append(t(36, 92, "Mesure 1 — la somme", 12, True, "#12365a"))
    g.append(t(36, 120, "boucle for — montant par montant", 9, True, "#7a3b12"))
    g.append(r(36, 128, 280, 26, "#fff7ef", "#d99a6c", 1, 3))
    g.append(t(324, 146, "3,8 ms", 10, True, "#7a3b12"))
    g.append(t(36, 182, "np.sum(montants) — une ligne", 9, True, "#12365a"))
    g.append(r(36, 190, 12, 26, "#eef2f6", "#5b7fa6", 1, 3))
    g.append(t(56, 208, "0,149 ms", 10, True, "#1f4e79"))
    g.append(t(36, 250, "rapport : 25×", 14, True, "#b3541e"))
    g.append(t(36, 276, "même total des deux côtés :", 9, False, "#33475b"))
    g.append(t(36, 294, "7 908 259 732,20 FCFA", 9, True, "#33475b"))
    g.append(t(36, 318, "(l'absolu est petit : 50 000 éléments ;", 8, False, "#42566b"))
    g.append(t(36, 332, "le rapport, lui, est stable)", 8, False, "#42566b"))

    # --- Panneau 2 : le controle qualite de C03 ---
    g.append(r(400, 70, 360, 272, "#ffffff", "#c9d3dd", 1.2))
    g.append(t(416, 92, "Mesure 2 — le contrôle qualité de C03", 12, True, "#12365a"))
    g.append(t(416, 120, "boucle for — isinstance + test + compteur", 9, True, "#7a3b12"))
    g.append(r(416, 128, 280, 26, "#fff7ef", "#d99a6c", 1, 3))
    g.append(t(704, 146, "6,2 ms", 10, True, "#7a3b12"))
    g.append(t(416, 182, "vecteur — (m > 100000).sum()", 9, True, "#12365a"))
    g.append(r(416, 190, 9, 26, "#eef2f6", "#5b7fa6", 1, 3))
    g.append(t(433, 208, "0,193 ms", 10, True, "#1f4e79"))
    g.append(t(416, 250, "rapport : 32×", 14, True, "#b3541e"))
    g.append(t(416, 276, "même comptage des deux côtés :", 9, False, "#33475b"))
    g.append(t(416, 294, "28 065 « gros »", 9, True, "#33475b"))
    g.append(t(416, 318, "(la boucle fait plus de Python", 8, False, "#42566b"))
    g.append(t(416, 332, "par élément → le rapport monte)", 8, False, "#42566b"))

    # --- Bandeau bas : la lecon ---
    g.append(r(20, 368, 740, 76, "#f4f7fa", "#c9d3dd", 1))
    g.append(t(36, 390, "La leçon : la vecteurisation ne change PAS la réponse — elle change le chemin.",
               10, True, "#12365a"))
    g.append(t(36, 412, "Publier une vitesse = les deux temps + le rapport + la date + la taille : "
               "un rapport non daté est une opinion,", 9, False, "#33475b"))
    g.append(t(36, 430, "un rapport mesuré et daté est une preuve.", 9, False, "#33475b"))

    return fin_svg(g)


def planche_loc_iloc_c07():
    """Planche 7 - C07 : loc vs iloc — le tableau des 4 cas (2x2) sur un
    extrait reel 5x4 du dossier M08, avec le piege des tranches en bas."""
    g = [svg_ouverture()]
    g.append(t(20, 26, "loc vs iloc : le tableau des 4 cas", 15, True, "#1f4e79"))
    g.append(t(20, 46, "La même pièce, 4 portes — les étiquettes (loc) ou les numéros (iloc).",
               10, False, "#42566b"))

    # --- Gauche : le vrai extrait 5x4 ---
    colx = [20, 52, 114, 188, 280]
    coll = ["", "id_vente", "id_magasin", "montant_ttc", "est_retour"]
    colw = [32, 62, 74, 92, 72]
    lignes = [
        ("0", "1", "2", "213566.20", "True"),
        ("1", "2", "1", "359109.80", "True"),
        ("2", "3", "2", "85939.05", "True"),
        ("3", "4", "3", "390891.06", "True"),
        ("4", "5", "4", "110866.60", "True"),
    ]
    y0, hh = 84, 26
    for j, (x, w, nom) in enumerate(zip(colx, colw, coll)):
        g.append(r(x, y0, w, hh, "#eef2f6", "#5b7fa6", 1, 0))
        g.append(t(x + w / 2, y0 + 17, nom, 9, True, "#12365a", "middle"))
    for i, vals in enumerate(lignes):
        y = y0 + hh * (i + 1)
        for j, (x, w, val) in enumerate(zip(colx, colw, vals)):
            fond, bord = ("#fff7ef", "#d99a6c") if (i == 1 and j == 3) \
                else ("#eef2f6", "#5b7fa6") if (i != 1 and j == 2) \
                else ("#ffffff", "#c9d3dd")
            g.append(r(x, y, w, hh, fond, bord, 1, 0))
            ancre = "start" if j == 0 else "middle"
            xx = x + 8 if j == 0 else x + w / 2
            g.append(t(xx, y + 17, val, 9, j in (0, 3), "#12365a" if j else "#7a3b12", ancre))
    g.append(t(20, y0 + 6 * hh + 20, "l'extrait réel : v.head(5), 4 colonnes de vente.csv",
               8, False, "#42566b"))
    g.append(t(20, y0 + 6 * hh + 36, "cellule orange = (ligne 1, montant_ttc) · colonne bleue = id_magasin",
               8, False, "#42566b"))

    # --- Droite : la grille 2x2 ---
    g.append(t(477, 80, "par NOM (loc)", 10, True, "#7a3b12", "middle"))
    g.append(t(662, 80, "par POSITION (iloc)", 10, True, "#12365a", "middle"))
    g.append(t(570, 100, "— une LIGNE —", 9, True, "#42566b", "middle"))
    g.append(t(570, 205, "— une COLONNE —", 9, True, "#42566b", "middle"))
    boites = [
        (390, 110, "ligne · par nom", "v4.loc[1, 'montant_ttc']", "359109.80", "#fff7ef", "#d99a6c"),
        (575, 110, "ligne · par position", "v4.iloc[1, 2]", "359109.80", "#eef2f6", "#5b7fa6"),
        (390, 215, "colonne · par nom", "v4.loc[:, 'id_magasin']", "[2, 1, 2, 3, 4]", "#fff7ef", "#d99a6c"),
        (575, 215, "colonne · par position", "v4.iloc[:, 1]", "[2, 1, 2, 3, 4]", "#eef2f6", "#5b7fa6"),
    ]
    for x, y, lib, code, res, fond, bord in boites:
        g.append(r(x, y, 175, 88, fond, bord, 1.2, 6))
        g.append(t(x + 12, y + 20, lib, 9, True, "#33475b"))
        g.append(t(x + 12, y + 44, code, 9.5, False, "#1f4e79"))
        g.append(t(x + 12, y + 68, "→ " + res, 10, True, "#7a3b12"))
    g.append(t(477, 330, "les 4 portes donnent la même valeur :", 9, False, "#33475b", "middle"))
    g.append(t(477, 348, "la cellule orange (359109.80) ou la colonne bleue — toujours la même pièce",
               8.5, False, "#42566b", "middle"))

    # --- Bandeau bas : le piege des tranches ---
    g.append(r(20, 372, 740, 72, "#f4f7fa", "#c9d3dd", 1))
    g.append(t(36, 394, "Le piège des tranches : v4.loc[1:3] → 3 lignes · v4.iloc[1:3] → 2 lignes",
               10, True, "#12365a"))
    g.append(t(36, 414, "la borne haute est INCLUE par nom (loc), EXCLUE par position (iloc) —",
               9, False, "#33475b"))
    g.append(t(36, 430, "même écriture, une ligne de moins : le contrôle len() est la garde-fou.",
               9, False, "#33475b"))

    return fin_svg(g)


def planche_groupby_c08():
    """Planche 8 - C08 : GROUP BY SQL <-> groupby pandas — le meme pipeline,
    deux syntaxes, une meme sortie (5 magasins, CA en centimes)."""
    g = [svg_ouverture()]
    g.append(t(20, 26, "GROUP BY SQL et groupby pandas : la même chaîne de calcul", 15, True, "#1f4e79"))
    g.append(t(20, 46, "Deux syntaxes, une même sortie — les 5 magasins du socle, additionnés en centimes.",
               10, False, "#42566b"))

    # --- Gauche : SQL ---
    g.append(r(20, 70, 360, 158, "#ffffff", "#5b7fa6", 1.2))
    g.append(t(36, 92, "SQL — le moteur M07", 10, True, "#12365a"))
    sql = ["SELECT id_magasin,", "SUM(montant_ttc)", "FROM vente",
           "GROUP BY id_magasin", "ORDER BY 2 DESC;"]
    for i, l in enumerate(sql):
        g.append(t(48, 118 + i * 20, l, 10.5, i in (1, 3), "#1f4e79"))

    # --- Droite : pandas ---
    g.append(r(400, 70, 360, 158, "#ffffff", "#d99a6c", 1.2))
    g.append(t(416, 92, "pandas — C08, en centimes entiers", 10, True, "#7a3b12"))
    py = ['ct = (v["montant_ttc"] * 100)', '.round().astype("int64")',
          'ct.groupby(v["id_magasin"])', '.sum() // 100']
    for i, l in enumerate(py):
        g.append(t(416, 118 + i * 20, l, 10.5, i in (0, 3), "#7a3b12"))

    # --- Flèches vers la sortie commune ---
    g.append(fleche(200, 228, 380, 252, "#5b7fa6"))
    g.append(fleche(580, 228, 400, 252, "#b3541e"))

    # --- La meme sortie : les 5 magasins ---
    g.append(r(20, 256, 740, 176, "#f4f7fa", "#c9d3dd", 1))
    g.append(t(380, 280, "la même sortie — CA par magasin (FCFA)", 11, True, "#12365a", "middle"))
    rows = [("4", "1 596 813 264", "#fff7ef", "#d99a6c"),
            ("1", "1 595 223 423", "#ffffff", "#c9d3dd"),
            ("2", "1 578 987 709", "#ffffff", "#c9d3dd"),
            ("5", "1 572 297 451", "#ffffff", "#c9d3dd"),
            ("3", "1 564 937 883", "#ffffff", "#c9d3dd")]
    g.append(t(310, 306, "id_magasin", 9, True, "#42566b", "middle"))
    g.append(t(520, 306, "CA (FCFA)", 9, True, "#42566b", "middle"))
    for i, (mid, ca, fond, bord) in enumerate(rows):
        y = 314 + i * 22
        g.append(r(290, y - 14, 40, 20, fond, bord, 1, 0))
        g.append(r(400, y - 14, 240, 20, fond, bord, 1, 0))
        g.append(t(310, y, mid, 9.5, True, "#12365a", "middle"))
        g.append(t(520, y, ca, 9.5, i == 0, "#12365a", "middle"))
    g.append(t(380, 424, "top magasin : 4 — 1 596 813 264 FCFA (m08p_ca_top_magasin)",
               9, True, "#7a3b12", "middle"))

    # --- Bandeau bas : la regle des centimes ---
    g.append(r(20, 448, 740, 40, "#fff7ef", "#d99a6c", 1.2))
    g.append(t(36, 466, "Les centimes : additionner en entiers, diviser après l'agrégat —",
               9, True, "#7a3b12"))
    g.append(t(36, 482, "la dérive float (1 à 2 FCFA sur 7,9 milliards) est mesurée et documentée, pas cachée.",
               9, False, "#7a3b12"))

    return fin_svg(g)


def audit(nom, svg):
    """Largeur estimee par ligne et jeu de signes."""
    autorises = set("é·èà—'\"«»→ê…×î←Éùç▼ô°\xa0§¹²³")
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
        "M08_C01_quatre_couches_environnement_python.svg": planche_4_couches(),
        "M08_C02_types_operations_matrice.svg": planche_types_c02(),
        "M08_C03_decider_repetir_flux.svg": planche_decider_repetir_c03(),
        "M08_C04_cinq_conteneurs.svg": planche_5_conteneurs_c04(),
        "M08_C05_lire_traceback.svg": planche_traceback_c05(),
        "M08_C06_boucle_vs_vecteur.svg": planche_boucle_vecteur_c06(),
        "M08_C07_loc_vs_iloc_4_cas.svg": planche_loc_iloc_c07(),
        "M08_C08_groupby_sql_pandas.svg": planche_groupby_c08(),
    }
    for nom, contenu in planches.items():
        chemin = os.path.join(FIG, nom)
        open(chemin, "w", encoding="utf-8").write(contenu)
        print("figure ->", nom, "(%.1f Ko)" % (os.path.getsize(chemin) / 1024))
        audit(nom, contenu)


if __name__ == "__main__":
    main()
