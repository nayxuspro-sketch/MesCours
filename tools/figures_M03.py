#!/usr/bin/env python3
"""figures_M03.py — les planches SVG du module M03 (Excel).

Deux contraintes de composition, les mêmes que pour les figures des modules précédents :
  * largeur utile 752 px ; un texte n'est jamais plus large que 0,605 × taille × nombre de
    caractères, et il est ancré à gauche (anchor="start") pour ne pas déborder ;
  * les libellés sont écrits tels qu'ils apparaissent dans Excel FR, avec le nom anglais
    entre parenthèses quand l'ordre des mots change.

Usage : python3 tools/figures_M03.py
"""
import os, re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(RACINE, "figures")
LARGEUR, HAUTEUR = 780, 470


def t(x, y, s, taille=13, gras=False, couleur="#1a1a1a", ancre="start"):
    """Texte SVG échappé : les formules Excel contiennent & < >, illégaux en XML."""
    s = str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    poid = ' font-weight="600"' if gras else ""
    return (f'<text x="{x}" y="{y}" font-family="Inter, Segoe UI, sans-serif" font-size="{taille}"'
            f' fill="{couleur}" text-anchor="{ancre}"{poid}>{s}</text>')


def r(x, y, w, h, fond="#ffffff", bord="#c9d3dd", trait=1, rx=4):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fond}" '
            f'stroke="{bord}" stroke-width="{trait}"/>')


def fleche(x1, y1, x2, y2, couleur="#1f4e79"):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{couleur}" stroke-width="1.4" '
            f'marker-end="url(#f)"/>')


def c01_fenetre():
    """Anatomie de la fenêtre, et les trois visages d'une même cellule — sur le fichier reçu."""
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGEUR} {HAUTEUR}" '
         f'width="{LARGEUR}" height="{HAUTEUR}"><defs>'
         f'<marker id="f" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
         f'<path d="M0,0 L0,6 L7,3 z" fill="#1f4e79"/></marker></defs>']
    g.append(r(6, 6, 528, 356, fond="#f7fafc", bord="#9fb0c0", trait=1.5))
    g.append(r(6, 6, 528, 24, fond="#1f4e79", bord="#1f4e79"))
    g.append(t(16, 23, "m03_classeur_atelier.xlsx", 12, True, "#ffffff"))
    g.append(r(6, 30, 528, 22, fond="#e8eff7", bord="#c9d3dd"))
    g.append(t(16, 45, "Accueil   Insertion   Formules   Données   Affichage", 11, False, "#1f4e79"))
    g.append(r(6, 52, 528, 26, fond="#f2f6fa", bord="#c9d3dd"))
    g.append(t(16, 69, "Presse-papiers   Police   Alignement   Nombre   Styles   Édition", 10, False, "#42566b"))
    g.append(r(16, 86, 84, 24, fond="#ffffff", bord="#9fb0c0"))
    g.append(t(26, 102, "M2", 12, True, "#1f4e79"))
    g.append(r(106, 86, 418, 24, fond="#ffffff", bord="#9fb0c0"))
    g.append(t(114, 102, "fx", 11, False, "#6b7785"))
    g.append(t(134, 102, "56 658", 12, False, "#1a1a1a"))
    xg, lg = 214, 106
    g.append(r(6, 116, 528, 190, fond="#ffffff", bord="#c9d3dd"))
    g.append(r(6, 116, 24, 190, fond="#eef3f8", bord="#c9d3dd"))
    for c in range(3):
        g.append(r(xg + c * lg, 116, lg, 22, fond="#eef3f8", bord="#c9d3dd"))
        g.append(t(xg + c * lg + lg // 2, 131, "KLM"[c], 11, True, "#42566b", "middle"))
    for i in range(3):
        y = 152 + i * 26
        g.append(t(18, y + 4, str(i + 1), 11, False, "#42566b", "middle"))
        for c in range(3):
            g.append(r(xg + c * lg, y - 14, lg, 26, fond="#ffffff", bord="#e3eaf1"))
    entetes = {"K": "remise", "L": "montant_ht", "M": "montant_ttc"}
    for c, lettre in enumerate("KLM"):
        g.append(t(xg + c * lg + 6, 152, entetes[lettre], 9, True, "#6b7785"))
    # ligne 2 et ligne 3 : ce que la feuille ventes_brutes contient vraiment
    for n, vals in enumerate([["0.03", "48015", "56 658"], ["0.0", "43900", "51 802"]]):
        y = 178 + n * 26
        for c, v in enumerate(vals):
            g.append(t(xg + c * lg + 8, y, v, 12, False, "#1a1a1a", "start"))
    g.append(r(xg + 2 * lg, 164, lg, 26, fond="#fff3cd", bord="#e0a800", trait=1.6))
    g.append(t(xg + 2 * lg + 8, 178, "56 658", 12, True, "#1a1a1a", "start"))
    g.append(t(30, 232, "la même valeur dans la feuille nettoyée", 9, False, "#3f7d3f"))
    g.append(t(250, 232, "ventes!M2 : un nombre", 9, False, "#3f7d3f"))
    g.append(r(xg + 2 * lg, 218, lg, 26, fond="#eaf5ea", bord="#3f7d3f", trait=1.4))
    g.append(t(xg + 2 * lg + lg - 8, 232, "56 658 FCFA", 11, True, "#1a1a1a", "end"))
    g.append(t(30, 262, "Feuille ventes_brutes : 489 lignes × 13 colonnes, et pas un seul montant", 11))
    g.append(t(30, 280, "reconnu comme nombre — d'où « Somme : 0 ». Un texte se colle à gauche,", 11, False, "#6b7785"))
    g.append(t(30, 296, "un nombre à droite : l'alignement est un diagnostic, pas un style.", 11, False, "#6b7785"))
    g.append(r(6, 306, 528, 22, fond="#eef3f8", bord="#c9d3dd"))
    onglets = [(14, "Aidez-moi"), (92, "ventes_brutes"), (186, "ventes"), (244, "clients"),
               (306, "objectifs"), (378, "Calculs"), (446, "TCD")]
    for x, nom in onglets:
        g.append(t(x, 321, nom, 10, nom == "ventes_brutes", "#1f4e79" if nom == "ventes_brutes" else "#42566b"))
    g.append(r(6, 328, 528, 34, fond="#1f4e79", bord="#1f4e79"))
    g.append(t(16, 350, "Prêt      Nombre : 489      valeurs numériques : 0      Somme : 0", 11, True, "#ffffff"))
    x0 = 550
    g.append(r(x0, 6, 202, 172, fond="#fbfdff", bord="#9fb0c0"))
    g.append(t(x0 + 10, 24, "Une cellule, trois visages", 11, True))
    g.append(t(x0 + 10, 48, "Son adresse", 10, True, "#1f4e79"))
    g.append(t(x0 + 10, 62, "M2 — lue dans la zone de nom", 10))
    g.append(t(x0 + 10, 88, "Son contenu", 10, True, "#1f4e79"))
    g.append(t(x0 + 10, 102, "du texte : « 56 658 », pas 56658", 10))
    g.append(t(x0 + 10, 128, "Son affichage", 10, True, "#1f4e79"))
    g.append(t(x0 + 10, 142, "56 658, collé à gauche", 10))
    g.append(t(x0 + 10, 166, "le format ne change pas le fond", 9, False, "#6b7785"))
    g.append(r(x0, 186, 202, 134, fond="#f4f9f4", bord="#3f7d3f"))
    g.append(t(x0 + 10, 204, "Ce que la barre d'état dit", 10, True, "#3f7d3f"))
    g.append(t(x0 + 10, 218, "de la colonne M entière :", 10))
    g.append(t(x0 + 10, 240, "489 textes · Somme : 0", 11, True, "#1a1a1a"))
    g.append(t(x0 + 10, 258, "un double-clic sur le CSV", 9, False, "#6b7785"))
    g.append(t(x0 + 10, 272, "en convertit 3 : 2 444 FCFA", 9, False, "#6b7785"))
    g.append(t(x0 + 10, 292, "la feuille ventes, elle :", 9, False, "#6b7785"))
    g.append(t(x0 + 10, 306, "480 lignes · 36 073 185", 9, False, "#1a1a1a"))
    g.append(fleche(300, 384, 300, 366))
    g.append(t(6, 392, "Sélectionnez la colonne M en entier (Ctrl+Maj+Bas) et lisez le bas de l'écran :", 11))
    g.append(t(6, 410, "aucun message d'erreur n'apparaîtra — c'est précisément le problème.", 11, True, "#a1650b"))
    g.append("</svg>")
    return "".join(g)


def c04_adresses():
    """Ce qui change (et ne change pas) quand on recopie une formule."""
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGEUR} 312" width="{LARGEUR}" '
         f'height="312"><defs><marker id="f" markerWidth="8" markerHeight="8" refX="7" refY="3" '
         f'orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#1f4e79"/></marker></defs>']
    g.append(r(6, 6, 384, 300, fond="#fbfdff"))
    g.append(t(20, 28, "Recopier vers le bas : ce qui bouge, ce qui reste", 12, True))
    x0, lg = 20, 84
    g.append(t(x0 + lg // 2 - lg, 46, "1", 10, True, "#6b7785", "middle"))
    for c in range(4):
        g.append(r(x0 + c * lg, 52, lg, 18, fond="#eef3f8"))
        g.append(t(x0 + c * lg + lg // 2, 65, "ABCD"[c], 10, True, "#42566b", "middle"))
    grille = [("1", ["taux TVA", "1,18", "", ""]),
              ("2", ["ligne 2", "48 015", "=B2*$B$1", "56 658"]),
              ("3", ["ligne 3", "78 402", "=B3*$B$1", "92 514"])]
    for n, (lig, vals) in enumerate(grille):
        y = 90 + n * 38
        g.append(t(10, y + 4, lig, 10, True, "#6b7785", "middle"))
        for c, v in enumerate(vals):
            g.append(r(x0 + c * lg, y - 12, lg, 26, fond="#ffffff"))
            if v:
                g.append(t(x0 + c * lg + lg // 2, y + 5, v, 10 if len(v) < 12 else 9, c == 2,
                           "#1f4e79" if c == 2 else "#1a1a1a", "middle"))
    g.append(t(20, 194, "C3 est C2 recopiée : B2 → B3, $B$1 n'a pas bougé.", 10, False, "#6b7785"))
    g.append(r(14, 206, 368, 0.6, fond="#dde3ea", bord="#dde3ea"))
    g.append(t(20, 224, "B2 suit le déplacement · $B$1 reste · B$1 et $B2", 10, False, "#42566b"))
    g.append(t(20, 240, "ne bloquent chacun qu'un seul bord.", 10, False, "#42566b"))
    g.append(t(20, 266, "Règle du module : une donnée = une plage", 11, True, "#1f4e79"))
    g.append(t(20, 282, "absolue, un calcul = une ligne relative. F4", 11, True, "#1f4e79"))
    g.append(t(20, 298, "fait tourner les trois écritures.", 11, True, "#1f4e79"))
    g.append(r(398, 6, 352, 300, fond="#fff8f0", bord="#e0a800"))
    g.append(t(396, 28, "Les erreurs, et ce qu'elles disent vraiment", 13, True))
    errs = [("#N/A", "clé absente de la colonne cherchée"),
            ("#VALEUR!", "du texte là où un nombre est attendu"),
            ("#DIV/0!", "dénominateur nul, souvent un filtre actif"),
            ("#RÉF!", "la plage n'existe plus, ligne supprimée"),
            ("#NOM?", "fonction inconnue, nom anglais ou faute"),
            ("####", "pas une erreur : colonne trop étroite")]
    for i, (e, d) in enumerate(errs):
        y = 56 + i * 36
        g.append(t(396, y, e, 12, True, "#a1650b"))
        g.append(t(462, y, d, 10))
    g.append(t(396, 268, "Le tableur affiche ce qu'il a trouvé, rien de plus.", 10, False, "#6b7785"))
    g.append("</svg>")
    return "".join(g)


def audit(nom, svg):
    """Avertis si un texte déborde de la largeur utile (752 px) — estimation 0,605 × taille × caractères."""
    pire = 0
    for m in re.finditer(r"<text (.*?)>([^<]*)</text>", svg):
        at = dict(re.findall(r'(x|font-size|text-anchor)="([^"]+)"', m.group(1)))
        x, taille, ancre, txt = float(at["x"]), float(at["font-size"]), at.get("text-anchor", "start"), m.group(2)
        largeur = 0.605 * taille * len(txt)
        fin = x + {"start": largeur, "middle": largeur / 2, "end": 0}[ancre]
        pire = max(pire, fin)
    if pire > 776:
        print("  attention : %s déborde (extension maximale estimée %.0f px)" % (nom, pire))
    else:
        print("  largeur ok : %s (extension maximale estimée %.0f px)" % (nom, pire))


def c02_formats():
    """Un meme montant, trois traitements ; et la regle de saisie qui arrete 14 000."""
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGEUR} 312" width="{LARGEUR}" '
         f'height="312"><defs><marker id="f" markerWidth="8" markerHeight="8" refX="7" refY="3" '
         f'orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#1f4e79"/></marker></defs>']
    g.append(r(6, 6, 384, 300, fond="#fbfdff"))
    g.append(t(20, 28, "Un meme montant, trois traitements", 12, True))
    x0, lg = 24, 116
    ligne = [("texte", "56 658", "0", "#fff3cd", "#e0a800", "SOMME() ignore"),
             ("nombre", "56658", "36 073 185", "#eaf5ea", "#3f7d3f", "compte : 480"),
             ("nombre + format", "56 658 FCFA", "36 073 185", "#eaf5ea", "#3f7d3f", "le format ne change rien")]
    g.append(t(x0 + 8, 54, "nature de la cellule", 10, True, "#6b7785"))
    g.append(t(x0 + lg + 8, 54, "la grille affiche", 10, True, "#6b7785"))
    g.append(t(x0 + 2 * lg + 8, 54, "somme de la colonne", 9, True, "#6b7785"))
    for n, (nom, vues, total, fond, bord, nota) in enumerate(ligne):
        y = 76 + n * 44
        g.append(r(x0, y - 14, lg - 6, 34, fond="#eef3f8", bord="#c9d3dd"))
        g.append(t(x0 + 8, y + 2, nom, 10, True, "#1f4e79"))
        g.append(t(x0 + 8, y + 16, nota, 8, False, "#6b7785"))
        g.append(r(x0 + lg, y - 14, lg - 6, 34, fond=fond, bord=bord))
        g.append(t(x0 + lg + lg - 14, y + 6, vues, 11, False, "#1a1a1a", "end"))
        g.append(r(x0 + 2 * lg, y - 14, lg * 2 - 30, 34, fond=fond, bord=bord))
        g.append(t(x0 + 2 * lg + lg - 44, y + 6, total, 11, n > 0, "#1a1a1a", "end"))
    g.append(r(14, 208, 368, 0.6, fond="#dde3ea", bord="#dde3ea"))
    g.append(t(20, 228, "Sur le fichier recu : 486 montants sur 489", 11, True, "#1f4e79"))
    g.append(t(20, 244, "a gauche, 3 a droite. La barre d'etat dit 0,", 11, True, "#1f4e79"))
    g.append(t(20, 260, "puis 2 444, puis 36 073 185 : trois etats", 11, True, "#1f4e79"))
    g.append(t(20, 276, "d'un meme fichier, aucun message d'erreur.", 11, True, "#1f4e79"))
    g.append(t(20, 296, "Un format n'est jamais une conversion : la nature du contenu", 10, False, "#6b7785"))
    g.append(t(20, 310, "se verifie au compteur, pas a l'oeil.", 10, False, "#6b7785"))
    # panneau droit : la regle de saisie
    g.append(r(398, 6, 352, 300, fond="#fff8f0", bord="#e0a800"))
    g.append(t(412, 28, "Validation : la regle qui arrete 14 000", 12, True))
    champs = [("Autoriser", "Nombre entier"), ("Donnees", "comprise entre"), ("Minimum", "1"),
              ("Maximum", "500"), ("Message d'erreur", "La quantite doit tenir entre 1 et 500")]
    for i, (k, v) in enumerate(champs):
        y = 54 + i * 26
        g.append(t(412, y, k, 10, True, "#6b7785"))
        g.append(r(508, y - 13, 226, 22, fond="#ffffff", bord="#c9d3dd"))
        g.append(t(516, y, v, 10, False, "#1a1a1a"))
    g.append(r(412, 190, 322, 44, fond="#fdecea", bord="#a1650b", trait=1.4))
    g.append(t(424, 206, "Attention : 8 lignes de retour portent une", 10, True, "#a1650b"))
    g.append(t(424, 220, "quantite negative, jusqu'a -13. Une regle a 1", 10, False, "#1a1a1a"))
    g.append(t(424, 234, "les rejetterait : la regle juste est person-", 10, False, "#1a1a1a"))
    g.append(t(424, 248, "nalisee, de -500 a 500 pour les retours.", 10, False, "#1a1a1a"))
    g.append(t(412, 268, "Dans le fichier recu : 7 lignes au-dessus de 500,", 11))
    g.append(t(412, 284, "au maximum 14 000. Apres nettoyage : 68.", 11))
    g.append("</svg>")
    return "".join(g)



def c03_structure():
    """Plage filtrée ou tableau structuré ; et le dédoublonnage, où tout se joue sur la clé."""
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGEUR} {HAUTEUR}" '
         f'width="{LARGEUR}" height="{HAUTEUR}"><defs>'
         f'<marker id="f" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
         f'<path d="M0,0 L0,6 L7,3 z" fill="#1f4e79"/></marker></defs>']
    xs, wcols = [18, 168, 238, 348], [150, 70, 110, 110]
    entetes = ["n_ticket", "quantite", "montant_ttc"]

    def grille(y0, nlig, fond_pair, hauteur=24, saut=24, gras=False):
        out = []
        for n in range(nlig):
            y = y0 + n * saut
            for cx, cw in zip(xs, wcols):
                out.append(r(cx, y - 14, cw, hauteur, fond=fond_pair if n % 2 else "#ffffff", bord="#e9eef4"))
            for cx, v in zip(xs, vals[n]):
                out.append(t(cx + 6, y + 2, v, 10, gras, "#1a1a1a"))
        return out

    # ---------- panneau A : plage + filtre automatique ----------
    g.append(r(6, 6, 470, 214, fond="#fbfdff", bord="#9fb0c0"))
    g.append(t(18, 26, "Deux façons de tenir la même table", 12, True))
    g.append(t(18, 44, "Plage + filtre automatique \u2014 feuille ventes_brutes, A1:M490", 10, False, "#42566b"))
    g.append(r(18, 52, 440, 22, fond="#eef3f8", bord="#c9d3dd"))
    for c, nom in enumerate(entetes):
        g.append(t(xs[c] + 6, 67, nom, 9, True, "#42566b"))
    g.append(t(xs[3] + 6, 67, "\u25bc sur 490 lignes", 9, False, "#6b7785"))
    vals = [("T05-250101-075845", "11", "56 658", ""),
            ("T05-250101-075846", "2 000", "51 802", ""),
            ("T05-250101-075847", "2", "58 396", "")]
    g += grille(92, 3, "#f7fafc")
    for n in range(3):
        g.append(t(10, 96 + n * 24, str(n + 2), 9, False, "#6b7785", "middle"))
    g.append(r(18, 152, 440, 24, fond="#fff3cd", bord="#e0a800", trait=1.4))
    g.append(t(24, 168, "\u2026 486 lignes \u2026", 10, False, "#6b7785"))
    g.append(t(124, 168, "491 coll\u00e9e apr\u00e8s : hors du filtre, hors des totaux", 10, True, "#a1650b"))
    g.append(t(18, 192, "Le filtre porte une adresse fig\u00e9e : \u00e0 chaque import, on la refait.", 10, False, "#42566b"))
    g.append(t(18, 208, "Trier une colonne seule : lignes d\u00e9synchronis\u00e9es, aucun signal.", 10, False, "#a33636"))

    # ---------- panneau B : tableau structuré ----------
    g.append(r(6, 228, 470, 130, fond="#f4f9f4", bord="#3f7d3f"))
    g.append(t(18, 246, "Tableau structur\u00e9 \u2014 TableVentes, A1:M481 (Ctrl+L)", 11, True, "#3f7d3f"))
    g.append(r(18, 254, 440, 20, fond="#eaf5ea", bord="#cfe3cf"))
    for c, nom in enumerate(entetes):
        g.append(t(xs[c] + 6, 268, nom, 9, True, "#3f7d3f"))
    vals = [("T05-250101-075845", "11", "56 658", ""), ("T05-250101-075846", "2 000", "51 802", "")]
    g += grille(288, 2, "#eef6ee", hauteur=18, saut=18)
    g.append(r(18, 312, 440, 22, fond="#eaf5ea", bord="#3f7d3f"))
    g.append(t(24, 327, "Total \u2192 36 073 185 FCFA \u00b7 ligne 481 : le tableau s\u2019\u00e9tend", 10, True, "#1a1a1a"))
    g.append(t(18, 350, "colonne N rest\u00e9e dehors : la 14e ne suit pas toute seule", 10, False, "#a1650b"))

    # ---------- panneau C : le choix de la clé de dédoublonnage ----------
    g.append(r(490, 6, 262, 352, fond="#fff8f0", bord="#e0a800"))
    g.append(t(500, 26, "Supprimer les doublons :", 12, True, "#a1650b"))
    g.append(t(500, 42, "tout se d\u00e9cide sur la cl\u00e9", 10, False, "#42566b"))
    clé = [("les 13 colonnes", 9, "266 132", "#3f7d3f"),
           ("ticket + produit", 12, "481 978", "#a1650b"),
           ("ticket seul", 173, "11 424 263", "#a33636")]
    for n, (nom, nl, ca, col) in enumerate(clé):
        y = 70 + n * 76
        g.append(t(500, y, nom, 11, True, "#1a1a1a"))
        g.append(r(500, y + 8, 242, 16, fond="#fdf3e6", bord="#e8d6bd"))
        g.append(r(500, y + 8, max(6, int(242 * nl / 173)), 16, fond=col, bord=col, rx=2))
        g.append(t(500, y + 40, "%d lignes \u00b7 %s FCFA" % (nl, ca), 10, False, col))
    g.append(t(500, 292, "Un ticket porte plusieurs lignes :", 10, True, "#a33636"))
    g.append(t(500, 308, "489 lignes, 316 tickets \u2014 d\u00e9doubler", 10))
    g.append(t(500, 324, "sur le ticket efface 173 ventes", 10))
    g.append(t(500, 344, "r\u00e9elles, 11 424 263 FCFA", 10, True, "#a33636"))

    # ---------- bandeau bas ----------
    g.append(r(6, 366, 746, 68, fond="#f7fafc", bord="#c9d3dd"))
    g.append(t(18, 384, "Trier : s\u00e9lectionner toute la ligne, ou cliquer dans le tableau ; puis deux niveaux \u2014 date, puis n_ticket.",
               11, True, "#1f4e79"))
    g.append(t(18, 402, "Filtrer : 40 lignes par mois \u00d7 12 mois = 480 \u00b7 Mat\u00e9riaux \u2192 143 \u00b7 contient \u00ab Sable \u00bb \u2192 11 \u00b7 quantit\u00e9 > 50 \u2192 3.",
               10, False, "#42566b"))
    g.append(t(18, 420, "Le filtre \u00ab Magasin \u00bb rend 480 lignes sur 480 : un filtre qui ne filtre rien est un filtre \u00e0 supprimer.",
               10, False, "#42566b"))
    g.append("</svg>")
    return "".join(g)


def c05_agregats():
    """Même colonne, trois questions — et ce que NB, NBVAL et MOYENNE ne disent pas."""
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGEUR} {HAUTEUR}" '
         f'width="{LARGEUR}" height="{HAUTEUR}"><defs>'
         f'<marker id="f" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
         f'<path d="M0,0 L0,6 L7,3 z" fill="#1f4e79"/></marker></defs>']
    # ---------- panneau gauche : la même colonne, trois questions ----------
    g.append(r(6, 6, 470, 236, fond="#fbfdff", bord="#9fb0c0"))
    g.append(t(18, 26, "TableVentes[montant_ttc] : 480 lignes, 7 catégories", 12, True))
    g.append(t(18, 44, "La formule ne vaut que par la question qu\u2019elle pose", 10, False, "#42566b"))
    rows = [
        ("=SOMME(TableVentes[montant_ttc])", "36 073 185 FCFA", "#1a1a1a"),
        ("=SOMME.SI.ENS(\u2026;[categorie];\"Plomberie\")", "8 754 982 FCFA", "#1f4e79"),
        ("=NB.SI.ENS([remise];\">0\")", "173 lignes sur 480", "#1f4e79"),
        ("=MOYENNE(TableVentes[remise])", "1,8 %", "#a1650b"),
        ("=MOYENNE.SI.ENS([remise];[remise];\">0\")", "5,1 %", "#a1650b"),
        ("=MEDIANE(TableVentes[montant_ttc])", "37 966 FCFA", "#1a1a1a"),
        ("=MOYENNE(TableVentes[montant_ttc])", "75 152 FCFA", "#1a1a1a"),
    ]
    for n, (f_, v, col) in enumerate(rows):
        y = 68 + n * 22
        if n % 2 == 0:
            g.append(r(14, y - 13, 454, 21, fond="#f4f8fb", bord="#f4f8fb"))
        g.append(t(20, y, f_, 10, False, "#1f4e79"))
        g.append(t(462, y, v, 10, True, col, "end"))
    g.append(t(18, 226, "75 152 de moyenne contre 37 966 de m\u00e9diane : la queue, pas une erreur.", 10, False, "#a33636"))
    # ---------- panneau droit : NB / NBVAL / vides ----------
    g.append(r(490, 6, 262, 236, fond="#fff8f0", bord="#e0a800"))
    g.append(t(500, 26, "Compter : quatre r\u00e9ponses", 12, True, "#a1650b"))
    g.append(t(500, 42, "colonne \u00ab client \u00bb, 480 lignes", 10, False, "#42566b"))
    bars = [("NBVAL \u2014 non vides", 462, "#3f7d3f"), ("NB \u2014 nombres", 462, "#1f4e79"),
            ("\u00ab 0 \u00bb \u00e0 l\u2019\u00e9cran", 85, "#a1650b"), ("vraiment vides", 18, "#a33636")]
    for n, (nom, v, col) in enumerate(bars):
        y = 62 + n * 40
        g.append(t(500, y, nom, 10, False, "#1a1a1a"))
        g.append(r(500, y + 5, 200, 13, fond="#fdf3e6", bord="#e8d6bd"))
        g.append(r(500, y + 5, max(4, int(200 * v / 480)), 13, fond=col, bord=col, rx=2))
        g.append(t(748, y + 15, str(v), 10, True, col, "end"))
    g.append(t(500, 226, "=MOYENNE(client) rend 9 548,75.", 10, True, "#a33636"))
    # ---------- bandeau : trois pièges ----------
    g.append(r(6, 250, 746, 180, fond="#f7fafc", bord="#c9d3dd"))
    g.append(t(18, 272, "Trois pi\u00e8ges \u00e0 conna\u00eetre avant de citer un agr\u00e9gat", 12, True, "#1f4e79"))
    pièges = [
        ("1. Agr\u00e9ger du texte",
         "=SOMME(ventes_brutes!M2:M490) rend 0 et =NB rend 3 : les 489 montants sont du texte, aucune erreur affich\u00e9e."),
        ("2. Une condition sur une colonne texte",
         "=SOMME.SI.ENS([montant_ttc];[date];\">=01/09/2025\") rend 0 sur le fichier re\u00e7u : les dates sont du texte."),
        ("3. Le quartile qui change de m\u00e9thode",
         "QUARTILE.INC rend 12 950 / 74 234 ; QUARTILE.EXC rend 12 891,5 / 74 304,5. M\u00eame question, deux r\u00e9ponses."),
    ]
    for n, (titre, texte) in enumerate(pièges):
        y = 296 + n * 44
        g.append(r(14, y - 16, 730, 40, fond="#ffffff", bord="#e3eaf1"))
        g.append(t(22, y, titre, 11, True, "#a1650b"))
        g.append(t(22, y + 18, texte, 10, False, "#42566b"))
    g.append(t(18, 422, "R\u00e9flexe : un compte de lignes \u00e0 c\u00f4t\u00e9 de chaque agr\u00e9gat \u2014 8 754 982 FCFA sur 57 lignes ne se lit "
                       "pas comme sur 480.", 10, True, "#1f4e79"))
    g.append("</svg>")
    return "".join(g)


def c06_recherches():
    """Le voyage d'une cle : ce que RECHERCHEV rate, ce que RECHERCHEX repare."""
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGEUR} {HAUTEUR}" '
         f'width="{LARGEUR}" height="{HAUTEUR}"><defs>'
         f'<marker id="f" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
         f'<path d="M0,0 L0,6 L7,3 z" fill="#1f4e79"/></marker></defs>']
    # ---------- panneau gauche : la cle et ses trois eclairages ----------
    g.append(r(6, 6, 400, 250, fond="#fbfdff", bord="#9fb0c0"))
    g.append(t(18, 26, "Une clé, trois éclairages", 12, True))
    g.append(t(18, 44, "n_ticket = T05-250101-075845 (17 caractères)", 10, False, "#42566b"))
    g.append(r(18, 54, 376, 26, fond="#eef3f8", bord="#c9d3dd"))
    g.append(t(26, 71, "T05-250101-075845", 12, True, "#1f4e79"))
    lignes = [("=GAUCHE(A2;3)", "T05", "le magasin (colonne D)"),
              ("=STXT(A2;5;6)", "250101", "la date du ticket, vérifiée"),
              ("=DROITE(A2;6)", "075845", "le n° du ticket, pas de la ligne"),
              ("=NBCAR(A2)", "17", "17, ici comme en population")]
    for n, (f_, v, com) in enumerate(lignes):
        y = 100 + n * 26
        g.append(t(22, y, f_, 10, False, "#1f4e79"))
        g.append(t(176, y, v, 10, True, "#1a1a1a"))
        g.append(t(252, y, com, 9, False, "#42566b"))
    g.append(r(18, 206, 376, 40, fond="#f2f8f2", bord="#9dbf9d"))
    g.append(t(26, 222, '=JOINDRE.TEXTE(" — ";VRAI;[vendeur];[categorie])', 10, False, "#1f4e79"))
    g.append(t(26, 238, "une clé de regroupage fabriquée, pas recopiée", 9, False, "#3f7d3f"))
    # ---------- panneau droit : quatre pièges chiffrés ----------
    g.append(r(420, 6, 332, 250, fond="#fff8f0", bord="#e0a800"))
    g.append(t(432, 26, "Quatre pièges, un chiffre chacun", 12, True, "#a1650b"))
    pieges = [
        ("1. Le 4e argument omis",
         "vaut VRAI : recherche approximative.",
         "0 faute ici, 233 sur 377 après un tri par nom."),
        ("2. Le premier match seulement",
         "il ne rend qu'une ligne sur quatre.",
         "CA lu 24 915 054 au lieu de 36 073 185."),
        ("3. #N/A se propage",
         "une clé absente contamine la formule fille.",
         "103 lignes : 85 zéros, 18 vides."),
        ("4. Rechercher à gauche",
         "RECHERCHEV n'en sait rien faire.",
         "id_produit est avant designation."),
    ]
    for n, (titre, l1, l2) in enumerate(pieges):
        y = 48 + n * 48
        g.append(r(428, y - 14, 316, 44, fond="#ffffff", bord="#e8d6bd"))
        g.append(t(436, y, titre, 11, True, "#a1650b"))
        g.append(t(436, y + 15, l1, 9, False, "#42566b"))
        g.append(t(436, y + 28, l2, 9, False, "#1a1a1a"))
    g.append(t(432, 250, "RECHERCHEX ferme 3 et 4 ; INDEX/EQUIV ferme 2 et 4.", 10, True, "#1f4e79"))
    # ---------- bandeau : les trois voies ----------
    g.append(r(6, 264, 746, 166, fond="#f7fafc", bord="#c9d3dd"))
    g.append(t(18, 286, "La même recherche, écrite de trois manières", 12, True, "#1f4e79"))
    voies = [
        ('=RECHERCHEV(F2;clients!A:B;2;FAUX)', "une colonne insérée casse l’index 2"),
        ('=INDEX(clients!B:B;EQUIV(F2;clients!A:A;0))', "compatible 2019 et LibreOffice, sans index fixe"),
        ('=RECHERCHEX(F2;clients!A:A;clients!B:B;"comptoir";0;-1)', "repli, match exact, et il cherche à gauche"),
    ]
    for n, (form, com) in enumerate(voies):
        y = 312 + n * 30
        g.append(r(14, y - 15, 730, 26, fond="#ffffff" if n % 2 else "#f2f6fa", bord="#e3eaf1"))
        g.append(t(22, y, form, 10, False, "#1f4e79"))
        g.append(t(404, y, com, 9, False, "#42566b"))
    g.append(t(18, 404, '=CNUM(SUBSTITUE(ventes_brutes!M2;" ";"")) rend 56 658 : réparer avant de chercher.',
               10, False, "#a1650b"))
    g.append(t(18, 422, "RECHERCHEX et JOINDRE.TEXTE exigent Microsoft 365 ou Excel 2021 ; en 2019, ces noms rendent #NOM?.",
               10, True, "#1f4e79"))
    g.append("</svg>")
    return "".join(g)


def c07_dates():
    """Le calendrier de l'extrait : ce que les dates disent, et les deux voies pour le calculer."""
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGEUR} {HAUTEUR}" '
         f'width="{LARGEUR}" height="{HAUTEUR}"><defs>'
         f'<marker id="f" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
         f'<path d="M0,0 L0,6 L7,3 z" fill="#1f4e79"/></marker></defs>']
    # ---------- panneau gauche : les 4 jours du mois ----------
    g.append(r(6, 6, 250, 240, fond="#fbfdff", bord="#9fb0c0"))
    g.append(t(18, 26, "Jours du mois couverts", 12, True))
    g.append(t(18, 42, "480 lignes, 4 valeurs de JOUR()", 10, False, "#42566b"))
    jours = [("1er", 256, "#1f4e79"), ("2", 163, "#1f4e79"), ("3", 55, "#3f7d3f"), ("4", 6, "#a1650b")]
    for n, (lab, v, col) in enumerate(jours):
        y = 62 + n * 34
        g.append(t(18, y + 10, lab, 10, False, "#1a1a1a"))
        g.append(r(46, y, 150, 14, fond="#eef3f8", bord="#dbe4ec"))
        g.append(r(46, y, max(3, int(150 * v / 256)), 14, fond=col, bord=col, rx=2))
        g.append(t(240, y + 10, str(v), 10, True, col, "end"))
    g.append(r(14, 200, 234, 36, fond="#fff8f0", bord="#e0a800"))
    g.append(t(22, 215, "=NB.SI(TableVentes[date];1)", 9, False, "#a1650b"))
    g.append(t(22, 229, "rend 0 : le 1er est une date, pas le nombre 1", 9, False, "#a33636"))
    # ---------- panneau milieu : la semaine ----------
    g.append(r(266, 6, 250, 240, fond="#fbfdff", bord="#9fb0c0"))
    g.append(t(278, 26, "Jours de la semaine", 12, True))
    g.append(t(278, 42, "=JOURSEM(date;2) : lundi = 1", 10, False, "#42566b"))
    sem = [("lun", 103), ("mar", 76), ("mer", 82), ("jeu", 61), ("ven", 35), ("sam", 91), ("dim", 32)]
    for n, (lab, v) in enumerate(sem):
        y = 60 + n * 22
        col = "#a33636" if n >= 5 else "#1f4e79"
        g.append(t(278, y + 10, lab, 9, False, "#1a1a1a"))
        g.append(r(306, y, 160, 12, fond="#eef3f8", bord="#dbe4ec"))
        g.append(r(306, y, max(2, int(160 * v / 103)), 12, fond=col, bord=col, rx=2))
        g.append(t(504, y + 10, str(v), 9, True, col, "end"))
    g.append(t(278, 222, "123 lignes le samedi ou le dimanche :", 10, True, "#a33636"))
    g.append(t(278, 236, "25,6 % de l\u2019extrait", 10, False, "#a33636"))
    # ---------- panneau droit : les deux dénominateurs ----------
    g.append(r(526, 6, 226, 240, fond="#f2f8f2", bord="#9dbf9d"))
    g.append(t(538, 26, "Un total, deux rythmes", 12, True, "#3f7d3f"))
    g.append(t(538, 46, "CA de l\u2019extrait", 9, False, "#42566b"))
    g.append(t(538, 62, "36 073 185 FCFA", 12, True, "#1a1a1a"))
    g.append(t(538, 92, "=NB.JOURS.OUVRES(min ; max)", 9, False, "#42566b"))
    g.append(t(538, 106, "240 jours ouvrés", 10, True, "#1f4e79"))
    g.append(t(538, 122, "150 305 FCFA par jour ouvré", 10, True, "#1f4e79"))
    g.append(t(538, 152, "=max-min+1  (jours courus)", 9, False, "#42566b"))
    g.append(t(538, 166, "336 jours calendaires", 10, True, "#a1650b"))
    g.append(t(538, 182, "107 361 FCFA par jour couru", 10, True, "#a1650b"))
    g.append(r(534, 198, 210, 40, fond="#ffffff", bord="#cfe0cf"))
    g.append(t(540, 213, "Les deux sont justes ;", 9, True, "#3f7d3f"))
    g.append(t(540, 227, "aucun n\u2019est une moyenne de vente.", 9, False, "#3f7d3f"))
    # ---------- bandeau : la fiche double ----------
    g.append(r(6, 254, 746, 190, fond="#f7fafc", bord="#c9d3dd"))
    g.append(t(18, 276, "La fiche double : la voie moderne, et la voie que tout le classeur peut lire",
               12, True, "#1f4e79"))
    voies = [
        ("Les lignes de décembre",
         "=FILTRE(TableVentes!A2:M481;MOIS(TableVentes!B2:B481)=12)",
         '=SOMME.SI.ENS([montant_ttc];[date];">="&DATE(2025;12;1);[date];"<"&DATE(2026;1;1)) puis un filtre sur la date'),
        ("Le chiffre d'affaires mois par mois",
         "=TRIERPAR(SEQUENCE(12);1;1;1) en ancre de la grille mensuelle",
         "la feuille Mensuel de l'atelier : douze fois =SOMME.SI.ENS avec DATE(2025;n;1) pour borne, et FIN.MOIS pour la seconde"),
        ("Les catégories réellement présentes",
         "=UNIQUE(TableVentes[categorie])",
         "=JOINDRE.TEXTE(…;VRAI;…) de la fiche 23, ou une colonne triée puis dédupliquée"),
    ]
    y = 296
    for titre, moderne, accessible in voies:
        g.append(r(14, y - 15, 730, 42, fond="#ffffff", bord="#e3eaf1"))
        g.append(t(22, y - 2, titre, 10, True, "#1a1a1a"))
        g.append(t(22, y + 14, "moderne  " + moderne, 9, False, "#1f4e79"))
        g.append(t(22, y + 26, "accessible  " + accessible, 9, False, "#42566b"))
        y += 46
    g.append(t(22, y + 6, "FILTRE · UNIQUE · TRIERPAR · SEQUENCE · LET : Microsoft 365, Excel 2021 et 2024 (en 2019 : #NOM?).",
               9, True, "#a33636"))
    g.append(t(22, y + 20, "LibreOffice 24.8+ connaît ces fonctions mais ne renverse pas : pré-allouer la plage, Ctrl + Maj + Entrée.",
               9, False, "#a1650b"))
    g.append("</svg>")
    return "".join(g)


def c08_tcd_modele():
    """Le TCD écrit à la main, ce qu'il ne sait pas faire, et le modèle de données qui le débloque."""
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGEUR} {HAUTEUR}" '
         f'width="{LARGEUR}" height="{HAUTEUR}"><defs>'
         f'<marker id="f" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
         f'<path d="M0,0 L0,6 L7,3 z" fill="#1f4e79"/></marker></defs>']
    # ---------- panneau gauche : la grille TCD reproduite en formules ----------
    g.append(r(6, 8, 462, 236, fond="#ffffff", bord="#c9d3dd"))
    g.append(t(18, 30, "Le TCD de l\u2019atelier, écrit à la main", 12, True, "#1f4e79"))
    g.append(t(18, 47, "feuille TCD : sept catégories, cinq mesures, une ligne de total", 9, False, "#42566b"))
    cols = [(18, "categorie", "start"), (140, "lignes", "end"), (212, "CA (FCFA)", "end"),
            (296, "moy./ligne", "end"), (368, "part", "end"), (424, "remises", "end")]
    for x, lib, ancre in cols:
        g.append(t(x, 70, lib, 8, True, "#42566b", ancre))
    g.append('<line x1="14" y1="76" x2="460" y2="76" stroke="#c9d3dd" stroke-width="1"/>')
    lignes = [("Plomberie", 57, "8 754 982", "153 596", "24,3 %", 22),
              ("Matériaux", 143, "6 519 357", "45 590", "18,1 %", 49),
              ("Electricité", 53, "6 311 645", "119 088", "17,5 %", 21),
              ("Bois & panneaux", 24, "4 844 758", "201 865", "13,4 %", 10),
              ("Consommables", 57, "2 500 964", "43 877", "6,9 %", 18)]
    y = 94
    for nom, nb, ca, moy, part, rem in lignes:
        g.append(t(18, y, nom, 9, False, "#1a1a1a"))
        g.append(t(140, y, str(nb), 9, False, "#1a1a1a", "end"))
        g.append(t(212, y, ca, 9, False, "#1a1a1a", "end"))
        g.append(t(296, y, moy, 9, False, "#42566b", "end"))
        g.append(t(368, y, part, 9, False, "#42566b", "end"))
        g.append(t(424, y, str(rem), 9, False, "#8a5a12", "end"))
        y += 17
    g.append(r(14, y - 13, 446, 18, fond="#eef3f8", bord="#dce6f0", rx=3))
    g.append(t(18, y, "Total", 9, True, "#1f4e79"))
    g.append(t(140, y, "480", 9, True, "#1f4e79", "end"))
    g.append(t(212, y, "36 073 185", 9, True, "#1f4e79", "end"))
    g.append(t(296, y, "75 152", 9, False, "#42566b", "end"))
    g.append(t(368, y, "100,0 %", 9, True, "#1f4e79", "end"))
    g.append(t(424, y, "173", 9, False, "#8a5a12", "end"))
    g.append(r(14, y + 12, 446, 44, fond="#fffaf2", bord="#e8d9bd"))
    g.append(t(22, y + 27, "« Le TOTAL de la ligne CA doit être exactement le total de la feuille :", 8, False, "#7a3b12"))
    g.append(t(22, y + 41, "s\u2019il diffère d\u2019un centime, un filtre est resté actif quelque part. »", 8, True, "#7a3b12"))
    # ---------- panneau droit : la limite du TCD sans modèle ----------
    g.append(r(476, 8, 298, 236, fond="#fdf7f4", bord="#e3c9bd"))
    g.append(t(488, 30, "Ce que le TCD simple ne peut pas faire", 12, True, "#7a3b12"))
    g.append(t(488, 47, "la demande : des clients distincts, pas des lignes", 9, False, "#7a3b12"))
    pas = [("champ Valeurs = Nombre sur [client]", "480 : ce sont les lignes"),
           ("somme des sept cases « clients »", "384, pas 372"),
           ("vraie valeur distincte, toute la table", "372 clients")]
    yy = 72
    for question, reponse in pas:
        g.append(t(488, yy, question, 9, False, "#1a1a1a"))
        g.append(t(488, yy + 14, reponse, 9, True, "#a83232"))
        yy += 38
    g.append(r(484, yy - 4, 282, 60, fond="#ffffff", bord="#e3c9bd"))
    g.append(t(492, yy + 10, "la case « Ajouter ces données au modèle de", 8, False, "#3f7d3f"))
    g.append(t(492, yy + 24, "données » débloque « Nombre distincts »", 8, True, "#3f7d3f"))
    g.append(t(492, yy + 38, "— et elle n\u2019existe pas sur Excel pour Mac", 8, False, "#3f7d3f"))
    # ---------- bandeau : le modèle de données ----------
    g.append(r(6, 252, 768, 210, fond="#f7fafc", bord="#c9d3dd"))
    g.append(t(18, 274, "Le modèle de données : des relations au lieu de colonnes recopiées", 12, True, "#1f4e79"))
    g.append(r(24, 292, 168, 56, fond="#ffffff", bord="#1f4e79", trait=1.6))
    g.append(t(34, 312, "ventes", 11, True, "#1f4e79"))
    g.append(t(34, 328, "480 lignes · 13 colonnes", 8, False, "#42566b"))
    g.append(t(34, 341, "une seule table de faits", 8, False, "#8a99a8"))
    cibles = [("produits", "154 lignes · prix catalogue", 288),
              ("clients", "23 500 au référentiel · 103 lignes sans clé", 320),
              ("magasins", "6 magasins · ville, région, ouverture", 352),
              ("objectifs", "218 lignes · 2 lignes de vente sans cible", 384)]
    for nom, detail, yc in cibles:
        g.append(r(430, yc, 200, 28, fond="#ffffff", bord="#c9d3dd"))
        g.append(t(438, yc + 13, nom, 9, True, "#1a1a1a"))
        g.append(t(438, yc + 24, detail, 7.5, False, "#8a99a8"))
        g.append(fleche(192, 316, 426, yc + 14, couleur="#8a99a8"))
    g.append(r(24, 372, 288, 74, fond="#ffffff", bord="#cfe0cf"))
    g.append(t(34, 388, "Trois mesures DAX, dans Power Pivot", 10, True, "#3f7d3f"))
    yy = 404
    for m in ["CA       \u2190 =SUM(ventes[montant_ttc])",
              "Clients  \u2190 =DISTINCTCOUNT(ventes[client])",
              "Part     \u2190 =DIVIDE([CA];[CA objectif])"]:
        g.append(t(34, yy, m, 8, False, "#1a1a1a"))
        yy += 14
    g.append(t(18, 456, "relations\u00a0: produit \u2192 id_produit · client \u2192 id_client · magasin \u2192 id_magasin · objectifs \u2192 annee_mois",
               8, False, "#42566b"))
    g.append(r(660, 288, 106, 158, fond="#eef3f8", bord="#dce6f0"))
    g.append(t(668, 304, "au lieu de", 9, True, "#1f4e79"))
    g.append(t(668, 320, "7 colonnes", 9, False, "#42566b"))
    g.append(t(668, 334, "RECHERCHEV", 9, False, "#42566b"))
    g.append(t(668, 348, "recopiées", 9, False, "#42566b"))
    g.append(t(668, 368, "sur 480 lignes", 8, False, "#8a99a8"))
    g.append(t(668, 382, "et à ressaisir", 8, False, "#8a99a8"))
    g.append(t(668, 396, "à chaque import", 8, False, "#8a99a8"))
    g.append(t(668, 418, "1 relation", 9, True, "#3f7d3f"))
    g.append(t(668, 432, "= 0 formule", 9, True, "#3f7d3f"))
    return "".join(g) + "</svg>"


def c08_chemin():
    """Le chemin de la donnée : brut, Power Query, modèle, TCD ; et qui peut le refaire."""
    LARGEUR2, HAUTEUR2 = 780, 316
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGEUR2} {HAUTEUR2}" '
         f'width="{LARGEUR2}" height="{HAUTEUR2}"><defs>'
         f'<marker id="f" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
         f'<path d="M0,0 L0,6 L7,3 z" fill="#1f4e79"/></marker></defs>']
    etapes = [("ventes_brutes.csv", ["489 lignes énoncées", "486 montants en texte", "dates en texte"], "#fdf7f4", "#e3c9bd"),
              ("Power Query", ["6 étapes appliquées", "dans l\u2019ordre, rejouées", "à chaque actualisation"], "#f7fafc", "#c9d3dd"),
              ("modèle de données", ["4 relations", "3 mesures DAX", "aucune colonne utilitaire"], "#f2f7f2", "#cfe0cf"),
              ("TCD + segments", ["7 catégories × 5 mesures", "3 segments connectés", "4 graphiques liés"], "#eef3f8", "#dce6f0")]
    x = 6
    for titre, lignes, fond, bord in etapes:
        g.append(r(x, 12, 176, 100, fond=fond, bord=bord, trait=1.3))
        g.append(t(x + 10, 32, titre, 11, True, "#1f4e79"))
        yy = 52
        for lib in lignes:
            g.append(t(x + 10, yy, lib, 8, False, "#42566b"))
            yy += 15
        if x < 550:
            g.append(fleche(x + 180, 58, x + 194, 58))
        x += 192
    g.append(t(6, 152, "Le même résultat, deux contrats : la requête garde la recette, le TCD garde la mise en page.", 10, True, "#1f4e79"))
    qui = [("Excel pour Microsoft 365 · 2021 · 2024 (Windows)", "les quatre étapes, complètes", "#3f7d3f"),
           ("Excel 2019 (Perpetual)", "les quatre étapes aussi ; sans les fonctions dynamiques ni Python dans Excel", "#3f7d3f"),
           ("Excel pour Mac", "Obtenir des données depuis la version 16.69, mais ni modèle ni Power Pivot", "#8a5a12"),
           ("LibreOffice Calc", "tableaux croisés en natif, ni segments ni Power Query ni modèle : tout en formules", "#8a5a12")]
    y = 172
    for machine, detail, couleur in qui:
        g.append(r(6, y - 12, 768, 24, fond="#ffffff", bord="#e3eaf1", rx=3))
        g.append(t(14, y + 3, machine, 9, True, "#1a1a1a"))
        g.append(t(300, y + 3, detail, 9, False, couleur))
        y += 26
    g.append(t(6, y + 16, "Python dans Excel : Microsoft 365 seulement (Windows depuis 2024, web depuis 2025).", 9, False, "#7a3b12"))
    g.append(t(6, y + 30, "Le calcul part dans le cloud : hors connexion rien ne se recalcule, et ni 2021 ni 2024 perpétuels ne le proposent.", 9, False, "#7a3b12"))
    return "".join(g) + "</svg>"

def main():
    os.makedirs(FIG, exist_ok=True)
    for nom, contenu in (("M03_C01_fenetre_excel.svg", c01_fenetre()),
                         ("M03_C02_formats_saisie.svg", c02_formats()),
                         ("M03_C03_structure_tableur.svg", c03_structure()),
                         ("M03_C04_adresses_erreurs.svg", c04_adresses()),
                         ("M03_C05_agregats_conditionnels.svg", c05_agregats()),
                         ("M03_C06_recherches_assemblage.svg", c06_recherches()),
                         ("M03_C07_dates_periodes.svg", c07_dates()),
                         ("M03_C08_tcd_et_modele.svg", c08_tcd_modele()),
                         ("M03_C08_chemin_donnees.svg", c08_chemin())):
        chemin = os.path.join(FIG, nom)
        open(chemin, "w", encoding="utf-8").write(contenu)
        print("figure →", nom, "(%.1f Ko)" % (os.path.getsize(chemin) / 1024))
        audit(nom, contenu)


if __name__ == "__main__":
    main()