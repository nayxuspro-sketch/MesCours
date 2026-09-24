#!/usr/bin/env python3
"""figures_M04.py — les planches SVG du module M04 (qualité des données).

Mêmes contraintes de composition que tools/figures_M03.py :
  * largeur utile 780 px ; un texte ne dépasse jamais 0,605 × taille × nombre de caractères ;
  * ancres posées à la main (`anchor="start"` par défaut, `"middle"` pour les chiffres centrés) ;
  * aucun glyphe hors latin-1 : la planche est rendue en PDF, les accents doivent passer.

L'audit en bas de fichier imprime la largeur maximale observée et le nombre de dépassements :
un contrôle qui ne dit pas ce qu'il a vu est un faux négatif poli (leçon de la fiche M03, Q9).

Usage : python3 tools/figures_M04.py
"""
import math
import os
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(RACINE, "figures")
LARGEUR, HAUTEUR = 780, 500
FACTEUR = 0.605  # largeur moyenne d'un glyphe, en ém


def t(x, y, s, taille=13, gras=False, couleur="#1a1a1a", ancre="start"):
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


def svg_ouverture(largeur=LARGEUR, hauteur=HAUTEUR):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largeur} {hauteur}" '
            f'width="{largeur}" height="{hauteur}"><defs>'
            f'<marker id="f" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">'
            f'<path d="M0,0 L0,6 L7,3 z" fill="#1f4e79"/></marker></defs>')


# Les douze points, tels que le chapitre les numérote, avec le verdict mesuré sur le socle.
GRILLE = [
    ("1", "identité", "28 516 920 o · cp1252 testé", "#eef3f8", "structure"),
    ("2", "structure", "243 360 lignes · 20 colonnes", "#eef3f8", "structure"),
    ("3", "complétude", "0 vide au brut · 1 911 villes absentes", "#eef3f8", "structure"),
    ("4", "unicité (technique)", "243 360 clés distinctes · 0 doublon", "#f2f7f2", "clé"),
    ("5", "unicité (métier)", "3 440 collisions · 3 360 à retirer", "#fdf7f4", "clé"),
    ("6", "types", "3 421 montants en texte", "#fdf7f4", "valeur"),
    ("7", "domaines", "973 remises > 1 · max lu 30", "#fdf7f4", "valeur"),
    ("8", "cohérence interne", "973 lignes · les mêmes qu\u2019au point 7", "#eef3f8", "valeur"),
    ("9", "cohérence externe", "486 lignes · 372 clients inconnus", "#eef3f8", "valeur"),
    ("10", "actualité", "51 dates après le 31/08/2026", "#fdf7f4", "temps"),
    ("11", "exactitude", "écart -2 111 789 puis +219 766 129", "#fbe9e7", "décision"),
    ("12", "traçabilité", "rapport fourni faux sur 3 lignes sur 5", "#fbe9e7", "décision"),
]


def c01_douze_points():
    """La grille de douze points et son verdict sur le socle entier."""
    g = [svg_ouverture()]
    g.append(t(6, 22, "Diagnostic de qualité — les douze points, dans l\u2019ordre d\u2019exécution", 14, True, "#1f4e79"))
    g.append(t(6, 40, "Chaque case : la question, le nombre, le dénominateur. Filet rouge = le point change le verdict.",
               10, False, "#42566b"))
    x0, y0, lw, lh = 6, 54, 252, 66
    for i, (num, nom, verdict, fond, groupe) in enumerate(GRILLE):
        col, lig = i % 3, i // 3
        x, y = x0 + col * (lw + 8), y0 + lig * (lh + 8)
        bord = "#c9a0a0" if fond in ("#fdf7f4", "#fbe9e7") else "#c9d3dd"
        g.append(r(x, y, lw, lh, fond=fond, bord=bord, trait=1.3 if bord != "#c9d3dd" else 1))
        g.append(r(x, y, 22, lh, fond="#1f4e79", bord="#1f4e79", rx=4))
        g.append(t(x + 11, y + 27, num, 15, True, "#ffffff", "middle"))
        g.append(t(x + 30, y + 20, nom, 11, True, "#1f4e79"))
        g.append(t(x + 30, y + 36, groupe, 8, False, "#8a99a8"))
        for j, portion in enumerate(_coupe(verdict, 34)):
            g.append(t(x + 30, y + 50 + j * 12, portion, 9, False, "#1a1a1a"))
    bas = y0 + 4 * (lh + 8) + 4
    g.append(r(6, bas, 768, 62, fond="#f7fafc", bord="#c9d3dd"))
    g.append(t(16, bas + 18, "Trois points décident du nettoyage :", 10, True, "#1f4e79"))
    g.append(t(16, bas + 32, "5 · la clé métier (le doublon invisible à id_vente)  ·  6 · les types (les montants texte)", 9, False, "#1a1a1a"))
    g.append(t(16, bas + 45, "11 · l\u2019exactitude (le total contre source extérieure). Sur le socle : 3 421 + 3 360 - 61", 9, False, "#1a1a1a"))
    g.append(t(16, bas + 58, "= 6 720 lignes à traiter, soit 2,8 % du fichier. Les neuf autres points changent la confiance.", 9, False, "#42566b"))
    return "".join(g) + "</svg>"


def c02_absences():
    """Cinq mécanismes d'absence, cinq traitements, et le nombre de lignes touchées sur le socle."""
    LARGEUR2, HAUTEUR2 = 780, 452
    g = [svg_ouverture(LARGEUR2, HAUTEUR2)]
    g.append(t(6, 22, "Les absences d\u2019un fichier de ventes : cinq mécanismes, cinq traitements", 14, True, "#1f4e79"))
    g.append(t(6, 40, "243 360 lignes, 0 cellule vide : ici, l\u2019absence est toujours \u00e9crite comme une valeur.", 10, False, "#42566b"))
    meca = [("A", "non-applicable", "id_client = 0 \u00b7 \u00e9crit par la r\u00e8gle", "43 681 lignes", "assumer, nommer \u00ab Comptoir \u00bb", "#eef3f8"),
            ("B", "non-collect\u00e9", "clients.email jamais demand\u00e9", "16 514 clients", "changer le formulaire, en amont", "#eef3f8"),
            ("C", "non-r\u00e9pondu", "clients.ville laiss\u00e9e vide", "1 911 clients", "joindre, sinon compter", "#eef3f8"),
            ("D", "perdu \u00e0 l\u2019import", "montant_ttc devenu du texte", "3 421 lignes", "d\u00e9river : ht + tva", "#fdf7f4"),
            ("E", "absence d\u00e9guis\u00e9e", "taux_remise \u00e0 0, nulle part vide", "157 634 lignes", "croiser un autre fichier", "#fdf7f4")]
    y = 58
    for num, nom, marqueur, nombre, traitem, fond in meca:
        g.append(r(6, y, 372, 58, fond=fond, bord="#c9d3dd"))
        g.append(r(6, y, 22, 58, fond="#1f4e79", bord="#1f4e79", rx=4))
        g.append(t(17, y + 25, num, 13, True, "#ffffff", "middle"))
        g.append(t(36, y + 18, nom, 11, True, "#1f4e79"))
        g.append(t(36, y + 33, marqueur, 9, False, "#42566b"))
        g.append(t(36, y + 48, "touch\u00e9es : " + nombre, 9, False, "#1a1a1a"))
        g.append(fleche(382, y + 29, 402, y + 29))
        g.append(r(406, y, 368, 58, fond="#f7fafc", bord="#c9d3dd"))
        g.append(t(416, y + 18, traitem, 10, True, "#1f4e79"))
        g.append(t(416, y + 34, "une cellule modifi\u00e9e : " + ("non" if num in "ABCE" else "oui, par la r\u00e8gle"), 9, False, "#42566b"))
        g.append(t(416, y + 48, "marqueur de manque \u00e0 poser : " + ("oui" if num in "DE" else "inutile"), 9, False, "#42566b"))
        y += 64
    g.append(r(6, y, 768, 62, fond="#f2f7f2", bord="#cfe0cf"))
    g.append(t(16, y + 18, "Le prix des deux traitements de la colonne D, mesur\u00e9 sur le m\u00eame fichier :", 10, True, "#1f4e79"))
    g.append(t(16, y + 34, "d\u00e9river par la r\u00e8gle \u00b7 15 639 751 286 FCFA   |   imputer \u00e0 la moyenne \u00b7 15 642 826 075 FCFA", 10, False, "#1a1a1a"))
    g.append(t(16, y + 50, "cible v\u00e9rifi\u00e9e : 15 419 985 157 FCFA. L\u2019\u00e9cart restant n\u2019est pas une histoire d\u2019absence : ce sont les lignes en trop (C03).", 9, False, "#42566b"))
    return "".join(g) + "</svg>"


def c03_doublons():
    """Les quatre niveaux de doublon, l'entonnoir, et la règle de garde qui en découle."""
    LARGEUR2, HAUTEUR2 = 780, 470
    g = [svg_ouverture(LARGEUR2, HAUTEUR2)]
    g.append(t(6, 22, "Doublons : ce que chaque niveau de clé voit, et ce qu’il laisse passer", 14, True, "#1f4e79"))
    g.append(t(6, 40, "Le même fichier, quatre questions. Une seule tombe sur le bon tas de lignes.", 10, False, "#42566b"))
    niveaux = [("Ligne entièrement identique", "colonne par colonne, A à Z", "0 ligne",
                "aucun copié-collé intégral dans le fichier", "#eef3f8"),
               ("Clé technique · id_vente", "243 360 valeurs distinctes", "0 doublon",
                "la clé du fichier est vierge de soupçon", "#eef3f8"),
               ("Ticket + produit + quantité", "collision sur la clé métier", "3 440 lignes",
                "le seul test qui voie le défaut", "#fdf7f4"),
               ("Ticket + produit, sans quantité", "toutes les lignes concernées", "8 453 lignes",
                "le dénominateur à citer, pas le résultat", "#eef3f8")]
    y = 58
    for titre, test, nombre, note, fond in niveaux:
        g.append(r(6, y, 470, 46, fond=fond, bord="#c9a0a0" if fond == "#fdf7f4" else "#c9d3dd"))
        g.append(t(16, y + 19, titre, 11, True, "#1f4e79"))
        g.append(t(16, y + 35, test, 9, False, "#42566b"))
        g.append(t(340, y + 27, nombre, 13, True, "#7a3b12" if fond == "#fdf7f4" else "#1a1a1a", "end"))
        g.append(r(486, y, 288, 46, fond="#ffffff", bord="#e3eaf1"))
        g.append(t(496, y + 27, note, 9, False, "#42566b"))
        y += 54
    g.append(r(6, y, 768, 84, fond="#f7fafc", bord="#c9d3dd"))
    g.append(t(16, y + 18, "L’entonnoir, et ce qui reste à traiter :", 10, True, "#1f4e79"))
    for i, ligne in enumerate(["243 360 lignes  →  97 199 partagent un ticket (normal : 1,67 ligne par ticket)",
                               "→  8 453 lignes en collision  →  3 440 collisions sur la clé complète",
                               "→  3 360 lignes à retirer  →  dont 61 aussi en montant texte (le recouvrement)"]):
        g.append(t(16, y + 36 + i * 15, ligne, 10, False, "#1a1a1a"))
    y += 94
    g.append(r(6, y, 768, 116, fond="#fdf7f4", bord="#c9a0a0"))
    g.append(t(16, y + 18, "La trace du mécanisme, lue dans l’ordre des identifiants :", 10, True, "#7a3b12"))
    for i, ligne in enumerate(["3 360 doublons, tous numérotés après leur original — écart médian 123 285, le plus proche 838",
                               "position médiane dans le fichier : 99,3 % du parcours. Un bloc ajouté à la fin :",
                               "signal d’un export rejoué sur une période récente, jamais d’une double saisie au clavier.",
                               "Règle de garde : le plus petit id_vente du groupe, jamais le dernier.",
                               "3 346 fois sur 3 360 le montant est identique des deux côtés ; les 14 autres divergent —",
                               "leur règle ne peut pas être « la première venue » mais « la première conforme à ht + tva »."]):
        g.append(t(16, y + 38 + i * 13, ligne, 9, i in (3,) and True or False, "#1a1a1a" if i < 4 else "#42566b"))
    return "".join(g) + "</svg>"


def c04_regles():
    """Quatre familles de règles de contrôle, leur rendement mesuré et la décision attachée."""
    LARGEUR2, HAUTEUR2 = 780, 430
    g = [svg_ouverture(LARGEUR2, HAUTEUR2)]
    g.append(t(6, 22, "Quatre familles de règles \u2014 rendement mesur\u00e9 sur 243 360 lignes", 14, True, "#1f4e79"))
    g.append(t(6, 40, "Le nombre de lignes signal\u00e9es ne dit rien de la qualit\u00e9 de la r\u00e8gle : la deuxi\u00e8me colonne si.", 10, False, "#42566b"))
    lignes = [("Domaine", "remise dans [0 ; 1]", "973 lignes", "973 erreurs d\u00e9sign\u00e9es", "2 \u00b7 corriger par reconstitution", "#f2f7f2"),
              ("Seuil m\u00e9tier", "quantit\u00e9 au-dessus de 50", "800 lignes", "0 erreur \u2014 \u00e0 surveiller", "3 \u00b7 liste au magasin", "#eef3f8"),
              ("Bande au r\u00e9f\u00e9rentiel", "prix dans [0,95 ; 1,35]", "0 ligne", "0 : le z\u00e9ro est un r\u00e9sultat", "3 \u00b7 indicateur de d\u00e9rive", "#f2f7f2"),
              ("Statistique (IQR)", "Q1 - 1,5 IQR \u00e0 Q3 + 1,5 IQR", "24 180 lignes", "0 erreur \u2014 bruit pur", "retirer du registre", "#fdf7f4"),
              ("\u00c9galit\u00e9 au catalogue", "prix = prix affich\u00e9", "232 981 lignes", "0 erreur \u2014 r\u00e8gle fausse", "retirer du registre", "#fdf7f4")]
    y = 56
    g.append(t(16, y, "Famille", 9, True, "#42566b")); g.append(t(150, y, "R\u00e8gle", 9, True, "#42566b"))
    g.append(t(360, y, "Signal\u00e9es", 9, True, "#42566b")); g.append(t(470, y, "Erreurs r\u00e9ellement d\u00e9sign\u00e9es", 9, True, "#42566b"))
    g.append(t(700, y, "D\u00e9cision", 9, True, "#42566b", "end"))
    y += 10
    for fam, regle, sig, err, deci, fond in lignes:
        g.append(r(6, y, 768, 40, fond=fond, bord="#c9a0a0" if fond == "#fdf7f4" else "#c9d3dd"))
        g.append(t(16, y + 17, fam, 10, True, "#1f4e79"))
        g.append(t(150, y + 17, regle, 9, False, "#1a1a1a"))
        g.append(t(360, y + 17, sig, 10, True, "#7a3b12" if fond == "#fdf7f4" else "#1a1a1a"))
        g.append(t(470, y + 17, err, 9, False, "#42566b"))
        g.append(t(700, y + 17, deci, 9, False, "#3f7d3f" if fond == "#f2f7f2" else "#42566b", "end"))
        g.append(t(150, y + 31, "", 9, False, "#42566b"))
        y += 46
    g.append(r(6, y, 768, 62, fond="#f7fafc", bord="#c9d3dd"))
    g.append(t(16, y + 17, "Le contr\u00f4le qui r\u00e9siste \u00e0 tout le monde : la r\u00e9paration avant de corriger", 10, True, "#1f4e79"))
    g.append(t(16, y + 34, "973 remises \u00e0 12, 18, 25 ou 30. Divis\u00e9es par 100 : 258 lignes restent hors du plafond de 0,25.", 9, False, "#1a1a1a"))
    g.append(t(16, y + 48, "Reconstitu\u00e9es depuis les montants : 0,000 \u00e0 0,110, les 973 dans le domaine. Le montant, lui, n'a jamais \u00e9t\u00e9 faux.", 9, False, "#42566b"))
    return "".join(g) + "</svg>"


def c05_normalisation():
    """Trois niveaux d'anomalie, le gain mesuré colonne par colonne, et la preuve par deux voies."""
    LARGEUR2, HAUTEUR2 = 780, 452
    g = [svg_ouverture(LARGEUR2, HAUTEUR2)]
    g.append(t(6, 22, "Normaliser n'est pas nettoyer \u2014 le gain de chaque colonne, mesuré", 14, True, "#1f4e79"))
    g.append(t(6, 40, "Gain = valeurs distinctes avant, moins valeurs distinctes après. Une formule à gain nul est un décor.", 10, False, "#42566b"))
    lignes = [("montant_ttc (N)", "retirer le suffixe puis les espaces", "3 421 textes", "3 421 nombres", "type · à convertir", "#fdf7f4"),
              ("clients.nom", "élaguer, minuscule, ponctuation", "12 640", "12 342 · gain 298", "écriture · c'est la clé du C03", "#f2f7f2"),
              ("clients.telephone", "garder les chiffres seuls", "23 499", "23 499 · gain 0", "écriture · pour la clé, pas l'affichage", "#eef3f8"),
              ("clients.ville", "élaguer et harmoniser la casse", "6", "6 · gain 0", "ne pas toucher : formule à retirer", "#eef3f8"),
              ("produits.unite", "élaguer et harmoniser la casse", "4", "4 · gain 0", "propre en texte, muette en physique", "#fdf7f4"),
              ("date_vente", "aucune conversion à écrire", "0 hors norme", "51 dates impossibles", "le format n'est pas le monde", "#fbe9e7")]
    y = 56
    g.append(t(16, y, "Colonne", 9, True, "#42566b")); g.append(t(150, y, "Opération envisagée", 9, True, "#42566b"))
    g.append(t(360, y, "Avant", 9, True, "#42566b")); g.append(t(470, y, "Après", 9, True, "#42566b"))
    g.append(t(700, y, "Verdict", 9, True, "#42566b", "end"))
    y += 10
    for col, op, av, ap, verd, fond in lignes:
        g.append(r(6, y, 768, 40, fond=fond, bord="#c9a0a0" if fond in ("#fdf7f4", "#fbe9e7") else "#c9d3dd"))
        g.append(t(16, y + 17, col, 10, True, "#1f4e79"))
        g.append(t(150, y + 17, op, 9, False, "#1a1a1a"))
        g.append(t(360, y + 17, av, 10, True, "#1a1a1a"))
        g.append(t(470, y + 17, ap, 9, False, "#7a3b12" if fond == "#fdf7f4" else "#42566b"))
        g.append(t(700, y + 17, verd, 9, False, "#3f7d3f" if fond == "#f2f7f2" else "#42566b", "end"))
        y += 46
    g.append(r(6, y, 768, 74, fond="#f7fafc", bord="#c9d3dd"))
    g.append(t(16, y + 17, "La preuve qui ferme le dossier : deux voies indépendantes, un écart à l'unité", 10, True, "#1f4e79"))
    g.append(t(16, y + 34, "Voie A → somme des 3 421 textes découpés et des 239 939 nombres : 15 639 751 286 FCFA", 9, False, "#1a1a1a"))
    g.append(t(16, y + 48, "Voie B → somme de (montant_ht + montant_tva) sur les mêmes lignes : 15 639 751 286 FCFA · écart 0", 9, False, "#1a1a1a"))
    g.append(t(16, y + 62, "Contrôle de rattrapage : les retours à montant positif passent de 47 à 0 sur 2 848 lignes.", 9, False, "#42566b"))
    return "".join(g) + "</svg>"


def c06_boite():
    """La boîte à données : trois zones, un journal qui se referme, un contrôle qui attend des résidus."""
    LARGEUR2, HAUTEUR2 = 780, 440
    g = [svg_ouverture(LARGEUR2, HAUTEUR2)]
    g.append(t(6, 22, "Livrer une boîte à données \u2014 trois zones, un journal, un contrôle qui attend", 14, True, "#1f4e79"))
    g.append(t(6, 40, "La documentation n'est pas la récompense du travail : c'est la condition de son rejeu.", 10, False, "#42566b"))
    zones = [("brut/", "10 fichiers", "l'arrivée, telle qu reçue", "lecture seule — jamais réécrite", "#eef3f8"),
             ("reference/", "12 fichiers", "la vérité : propres, dictionnaires, verites_terrain", "écrit par décision, jamais à la volée", "#f2f7f2"),
             ("projection/", "2 fichiers", "les échantillons distribués aux modules", "dérivé : recréable, avec son ATTENDU", "#eef3f8")]
    y = 54
    for z, nb, role, regle, fond in zones:
        g.append(r(6, y, 768, 34, fond=fond))
        g.append(t(16, y + 21, z, 11, True, "#1f4e79"))
        g.append(t(120, y + 21, nb, 10, False, "#1a1a1a"))
        g.append(t(260, y + 21, role, 9, False, "#42566b"))
        g.append(t(700, y + 21, regle, 9, False, "#7a3b12", "end"))
        y += 40
    g.append(r(6, y, 380, 110, fond="#f7fafc", bord="#c9d3dd"))
    g.append(t(16, y + 18, "Le journal se referme par un compteur", 10, True, "#1f4e79"))
    g.append(t(16, y + 36, "ventes : 243 360 → 240 000 (3 360, règle du C03)", 9, False, "#1a1a1a"))
    g.append(t(16, y + 52, "montants texte : 3 421 → 0 (convergence à 0 franc)", 9, False, "#1a1a1a"))
    g.append(t(16, y + 68, "clients : 23 912 → 23 500 (412, clé nom + chiffres)", 9, False, "#1a1a1a"))
    g.append(t(16, y + 84, "catégories : 16 modalités dont 1 vide → 7", 9, False, "#1a1a1a"))
    g.append(t(16, y + 100, "avant - après = retirés : sinon, c'est une note, pas une ligne", 9, False, "#42566b"))
    x2 = 394
    g.append(r(x2, y, 380, 110, fond="#f7fafc", bord="#c9d3dd"))
    g.append(t(x2 + 10, y + 18, "Le contrôle final attend des résidus, pas des zéros", 10, True, "#1f4e79"))
    g.append(t(x2 + 10, y + 36, "12 points : 0 vides, 0 texte, 0 domaine, 0 actualité", 9, False, "#1a1a1a"))
    g.append(t(x2 + 10, y + 52, "unicité métier : 80 groupes (160 lignes) — attendus", 9, False, "#1a1a1a"))
    g.append(t(x2 + 10, y + 68, "distincts par l'heure 80/80, client 77, prix 72 ; indistincts : 0", 9, False, "#1a1a1a"))
    g.append(t(x2 + 10, y + 84, "total : 15 419 985 157 FCFA = verites_terrain, écart 0", 9, False, "#3f7d3f"))
    g.append(t(x2 + 10, y + 100, "le résidu attendu s'écrit avant le contrôle", 9, False, "#42566b"))
    y += 122
    g.append(r(6, y, 768, 54, fond="#fdf7f4", bord="#c9a0a0"))
    g.append(t(16, y + 18, "Protéger, c'est chiffrer : 4 fichiers de personnes, un risque mesuré", 10, True, "#7a3b12"))
    g.append(t(16, y + 36, "nom 23 912 · téléphone 23 912 · e-mail 7 398 · ville 22 001 · 22 vendeurs · 6 responsables · 3 rôles", 9, False, "#1a1a1a"))
    g.append(t(16, y + 50, "sans nom/tél/e-mail, 87,3 % des clients restent désignés par 4 colonnes anonymes ; l'e-mail encode l'id dans 7 265 cas", 9, False, "#42566b"))
    return "".join(g) + "</svg>"


def _coupe(s, n):
    """Découpe un libellé en lignes de n caractères maximum, sans couper un mot."""
    lignes, courant = [], ""
    for mot in s.split():
        if courant and len(courant) + 1 + len(mot) > n:
            lignes.append(courant)
            courant = mot
        else:
            courant = f"{courant} {mot}".strip()
    if courant:
        lignes.append(courant)
    return lignes[:3]


def audit(nom, svg):
    """Largeur estimée par ligne (0,605 × taille × caractères, ancre comprise) et jeu de signes.

    Le seuil de 776 px est celui des planches M03, rendu et validé en PDF. Le jeu de signes autorisé est
    exactement celui des SVG publiés : pas de moins typographique (U+2212), pas d’espace insécable large,
    parce que ces deux-là n'ont jamais été rendus dans ce projet.
    """
    autorises = set("é·èà—’«»→ê…×î←Éùç▼ô°\xa0")
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
            print(f"  [{nom}] déborde (extension {fin:.0f} px) : {txt[:56]!r}")
        inattendus = {c for c in txt if ord(c) > 127 and c not in autorises}
        if inattendus:
            hors_jeu += 1
            print(f"  [{nom}] hors jeu publié : {sorted(inattendus)} dans {txt[:40]!r}")
    print(f"  [{nom}] extension maximale estimée {pire:.0f} px (limite 776) · débordements {depasse} · "
          f"lignes hors jeu {hors_jeu}")
    assert depasse == 0 and hors_jeu == 0, f"planche {nom} non conforme"


def main():
    os.makedirs(FIG, exist_ok=True)
    planches = {"M04_C01_diagnostic_en_douze_points.svg": c01_douze_points(),
                "M04_C02_cinq_mecanismes_cinq_traitements.svg": c02_absences(),
                "M04_C03_quatre_niveaux_de_doublon.svg": c03_doublons(),
                "M04_C04_quatre_familles_de_regles.svg": c04_regles(),
                "M04_C05_trois_niveaux_deux_preuves.svg": c05_normalisation(),
                "M04_C06_boite_a_donnees.svg": c06_boite()}
    for nom, contenu in planches.items():
        chemin = os.path.join(FIG, nom)
        open(chemin, "w", encoding="utf-8").write(contenu)
        print("figure →", nom, "(%.1f Ko)" % (os.path.getsize(chemin) / 1024))
        audit(nom, contenu)


if __name__ == "__main__":
    main()
