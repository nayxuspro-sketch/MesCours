#!/usr/bin/env python3
"""figures_M07.py — les planches SVG du module M07 (SQL : interroger, agreger, rejoindre).

Huit planches prevues (une par chapitre). Pour l'instant, seule la planche C01 est generee ;
les planches C02 a C08 seront ajoutees au fil de l'eau (1 push par chapitre).

Memes contraintes que tools/figures_M06.py :
  * largeur utile 780 px ; texte jamais plus large que 0,605 x taille x nb de caracteres ;
  * ancres posees a la main (``start`` par defaut, ``middle`` pour les chiffres centres) ;
  * jeu de signes latin-1 etendu (accents, guillemets francais, fleche ->, etc.) ;
  * pas de glyphe hors latin-1 : la planche est rendue en PDF, les accents doivent passer.

Usage : python3 tools/figures_M07.py
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


def planche_entonnoir_where():
    """Planche 2 - C02 : l'entonnoir WHERE (filtrage des lignes avant agregation)."""
    g = [svg_ouverture()]
    g.append(t(20, 26, "L'entonnoir WHERE : filtrer les lignes, etape par etape", 14, True, "#1f4e79"))
    g.append(t(20, 46, "Une requete SELECT traverse 8 etapes ; le WHERE agit en 2e position.",
               10, False, "#42566b"))

    # 5 etages de l'entonnoir (de haut en bas)
    etages = [
        ("1. FROM",       "charger la table",                    "50008 ventes",     "#1f4e79", 50008),
        ("2. WHERE",      "filtrer (avant agregat)",             "selon condition",  "#7a3b12", None),
        ("3. SELECT",     "projeter (colonnes / alias)",         "sortie tabulaire", "#1f4e79", None),
        ("4. ORDER BY",   "trier (option)",                      "selon cle",        "#7a3b12", None),
        ("5. LIMIT",      "tronquer (option)",                   "5 premieres",      "#7a3b12", None),
    ]
    y0, h, w0 = 80, 50, 200
    for i, (titre, desc, exemple, couleur, n_lignes) in enumerate(etages):
        y = y0 + i * (h + 10)
        # bandeau degrade : plus etroit au fur et a mesure (entonnoir)
        reduction = 30 * i
        g.append(r(20 + reduction // 2, y, w0 - reduction, h, fond="#ffffff", bord=couleur, trait=1.5))
        g.append(t(36 + reduction // 2, y + 22, titre, 12, True, couleur))
        g.append(t(36 + reduction // 2, y + 40, desc, 10, False, "#1a1a1a"))
        # exemple a droite
        if n_lignes is not None:
            g.append(t(640, y + 22, f"lignes : {n_lignes:,}".replace(",", " "), 11, True, "#1f4e79"))
            g.append(t(640, y + 40, exemple, 9, False, "#42566b"))
        else:
            g.append(t(640, y + 22, exemple, 11, False, "#1a1a1a"))

    # Bandeau d'avertissement : les priorites
    g.append(r(20, 380, 740, 90, fond="#fdf7f4", bord="#7a3b12"))
    g.append(t(36, 402, "Pieges frequents du WHERE", 12, True, "#7a3b12"))
    g.append(t(36, 422, "= NULL ne marche jamais (utiliser IS NULL)", 10, False, "#1a1a1a"))
    g.append(t(36, 438, "AND est plus prioritaire que OR (toujours parentheses)", 10, False, "#1a1a1a"))
    g.append(t(36, 454, "BETWEEN inclut les DEUX bornes (la borne superieure n'est pas exclue)", 10, False, "#1a1a1a"))
    return "".join(g) + "</svg>"


def planche_pipeline_order_by():
    """Planche 3 - C03 : pipeline ORDER BY + LIMIT + OFFSET."""
    g = [svg_ouverture()]
    g.append(t(20, 26, "Pipeline ORDER BY + LIMIT + OFFSET", 14, True, "#1f4e79"))
    g.append(t(20, 46, "Le tri (7e) precede la troncature (8e) ; OFFSET est la cle de la pagination.",
               10, False, "#42566b"))

    # Bandeau du haut : ordre d'execution (rappel)
    g.append(r(20, 70, 740, 32, fond="#f7fafc", bord="#1f4e79"))
    g.append(t(36, 90, "Ordre d'execution : FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT",
               10, True, "#1f4e79"))

    # 3 colonnes : ORDER BY / LIMIT / OFFSET
    cols = [
        ("ORDER BY", "trier", "ASC par defaut", "#7a3b12",
         ["ORDER BY col ASC", "ORDER BY col DESC", "ORDER BY a, b   (multi-cles)", "ORDER BY alias_colonne", "ORDER BY 2         (position)"]),
        ("LIMIT", "tronquer", "garder N lignes", "#1f4e79",
         ["LIMIT 5              (5 premieres)", "LIMIT 10 OFFSET 20  (page 3)", "LIMIT 1             (top 1)", "LIMIT ALL           (tout)", "OFFSET seul         (rare)"]),
        ("OFFSET", "sauter", "avant LIMIT", "#1f4e79",
         ["OFFSET 10           (sauter 10)", "OFFSET 100          (sauter 100)", "OFFSET 1000         (sauter 1000)", "Dangereux sur > 1M  (lent)", "Pagine par cle en M11 (rapide)"]),
    ]
    y0 = 120
    col_w = 240
    for i, (titre, role, sous, couleur, lignes) in enumerate(cols):
        x = 20 + i * (col_w + 10)
        g.append(r(x, y0, col_w, 32, fond="#ffffff", bord=couleur, trait=1.5))
        g.append(t(x + 12, y0 + 22, titre, 12, True, couleur))
        g.append(t(x + 80, y0 + 22, role, 10, False, "#1a1a1a"))
        g.append(t(x + 12, y0 + 50, sous, 9, False, "#42566b"))
        for j, l in enumerate(lignes):
            g.append(t(x + 12, y0 + 70 + j * 18, l, 9, False, "#1a1a1a", "start"))

    # Bandeau du bas : pieges
    g.append(r(20, 410, 740, 60, fond="#fdf7f4", bord="#7a3b12"))
    g.append(t(36, 432, "Pieges", 12, True, "#7a3b12"))
    g.append(t(36, 452, "LIMIT sans ORDER BY -> ordre arbitraire (non deterministe)",
               10, False, "#1a1a1a"))
    return "".join(g) + "</svg>"


def planche_requetes_composees_c08():
    """Planche 8 - C08 : sous-requetes, CTE, vues, EXISTS/IN, double negation."""
    g = [svg_ouverture()]
    g.append(t(20, 26, "Requêtes composées : la question dans la question", 14, True, "#1f4e79"))
    g.append(t(20, 46, "D'abord calculer, puis utiliser le resultat : sous-requete, CTE nommee, vue enregistree.",
               10, False, "#42566b"))

    # Sous-requete scalaire : requete dans requete
    g.append(r(20, 70, 360, 110, fond="#ffffff", bord="#1f4e79", trait=1.5))
    g.append(t(36, 90, "Sous-requete : la question dans la question", 11, True, "#1f4e79"))
    g.append(r(36, 102, 328, 34, fond="#f7fafc", bord="#9db3c8"))
    g.append(t(48, 118, "WHERE montant_ttc >", 10, False, "#1a1a1a"))
    g.append(r(180, 102, 176, 34, fond="#fff8e1", bord="#7a3b12"))
    g.append(t(192, 118, "(SELECT AVG(...) FROM vente)", 9, False, "#7a3b12"))
    g.append(t(36, 152, "1) AVG = 158 140 FCFA  puis  2) filtrer : 20 289 ventes", 10, False, "#1a1a1a"))
    g.append(t(36, 170, "Scalaire = 1 valeur. De liste = un IN (colonne de valeurs).", 9, False, "#42566b"))

    # 3 colonnes : CTE / Vue / EXISTS
    cols = [
        ("CTE (WITH)", "sous-requete NOMMEE", "ephemere (1 requete)", "#1f4e79",
         ["WITH ca AS (SELECT ...)", "une etape par nom", "lisibilite, pas optimisation"]),
        ("Vue", "CTE ENREGISTREE", "persiste dans le schema", "#1f4e79",
         ["CREATE VIEW v AS SELECT ...", "lue comme une table", "se recalcule (ne fige pas)"]),
        ("EXISTS / IN", "appartenance", "IN = au moins un", "#7a3b12",
         ["IN (SELECT ...)  ->  au moins un", "NOT IN + NULL = 0 ligne (piege)", "NOT EXISTS : sans NULL"]),
    ]
    y0 = 196
    bw = 240
    for i, (titre, sous, note, c, lignes) in enumerate(cols):
        x = 20 + i * (bw + 10)
        g.append(r(x, y0, bw, 32, fond="#ffffff", bord=c, trait=1.5))
        g.append(t(x + 12, y0 + 22, titre, 11, True, c))
        g.append(t(x + 12, y0 + 52, sous, 9, True, "#1a1a1a"))
        g.append(t(x + 12, y0 + 70, note, 8, False, "#42566b"))
        for j, l in enumerate(lignes):
            g.append(t(x + 12, y0 + 90 + j * 16, l, 8, False, "#1a1a1a"))

    # Bande du bas : double negation
    g.append(r(20, 400, 740, 70, fond="#fdf7f4", bord="#7a3b12"))
    g.append(t(36, 422, "Double negation : le pattern des « tous les » (piege P6)", 12, True, "#7a3b12"))
    g.append(t(36, 444, "« le client a achete TOUS les produits X »  =  « il n'existe AUCUN produit X qu'il n'a PAS achete »",
               10, False, "#1a1a1a"))
    g.append(t(36, 462, "NOT EXISTS (SELECT 1 FROM X WHERE NOT EXISTS (SELECT 1 ...))  ->  119 clients (top 2 produits)",
               10, False, "#7a3b12"))
    return "".join(g) + "</svg>"


def planche_jointures_c07():
    """Planche 7 - C07 : jointure en etoile + 4 types + explosion P4."""
    g = [svg_ouverture()]
    g.append(t(20, 26, "Joindre : la jointure en etoile et les 4 types", 14, True, "#1f4e79"))
    g.append(t(20, 46, "La table centrale (vente) est reliee aux tables de reference par leurs cles.",
               10, False, "#42566b"))

    # Etoile : vente au centre
    g.append(r(310, 90, 160, 56, fond="#fff8e1", bord="#7a3b12", trait=1.5))
    g.append(t(330, 112, "vente", 13, True, "#7a3b12"))
    g.append(t(330, 132, "50 008 lignes (centrale)", 9, False, "#1a1a1a"))

    refs = [
        (40, 70, "client", "1 200", "ON v.id_client = c.id_client"),
        (560, 70, "produit", "380", "ON v.id_produit = p.id_produit"),
        (40, 165, "magasin", "5", "ON v.id_magasin = m.id_magasin"),
        (560, 165, "mode_paiement", "5", "ON v.id_mode = mp.id_mode"),
    ]
    for x, y, nom, nb, on in refs:
        g.append(r(x, y, 180, 40, fond="#f7fafc", bord="#1f4e79"))
        g.append(t(x + 12, y + 17, nom, 11, True, "#1f4e79"))
        g.append(t(x + 12, y + 33, nb + " lignes", 9, False, "#42566b"))
        g.append(t(x + 60, y + 52, on, 8, False, "#42566b"))

    fleche(222, 90, 308, 104)    # client -> vente
    fleche(472, 104, 558, 90)    # vente -> produit
    fleche(180, 163, 330, 148)   # magasin -> vente
    fleche(620, 163, 470, 148)   # mode -> vente

    g.append(t(240, 240, "4 relations N -> 1 : le resultat garde 50 008 lignes (enrichi, pas double).",
               10, True, "#1f4e79"))

    # 4 types
    types = [
        ("INNER", "les paires des deux cotes", "50 008", "#1f4e79"),
        ("LEFT", "tout le gauche, NULL a droite", "5 (objectifs vides)", "#1f4e79"),
        ("FULL", "les deux cotes", "absent de SQLite", "#1f4e79"),
        ("CROSS", "produit cartésien 5 x 5", "25", "#7a3b12"),
    ]
    y0 = 262
    bw = 182
    for i, (nom, desc, val, c) in enumerate(types):
        x = 20 + i * (bw + 6)
        g.append(r(x, y0, bw, 66, fond="#ffffff", bord=c, trait=1.5))
        g.append(t(x + 12, y0 + 20, nom, 12, True, c))
        g.append(t(x + 12, y0 + 38, desc, 8, False, "#42566b"))
        g.append(t(x + 12, y0 + 56, val, 9, True, "#1a1a1a"))

    # Bande P4
    g.append(r(20, 344, 740, 52, fond="#fdf7f4", bord="#7a3b12"))
    g.append(t(36, 366, "Piege P4 : jointure qui double", 12, True, "#7a3b12"))
    g.append(t(36, 386, "vente JOIN vente ON id_client : 50 008 -> 2 131 064 lignes (facteur ~42). Controle : COUNT(*) avant/apres.",
               10, False, "#1a1a1a"))
    return "".join(g) + "</svg>"


def planche_categorisation_c06():
    """Planche 6 - C06 : CASE, COALESCE, NULLIF."""
    g = [svg_ouverture()]
    g.append(t(20, 26, "Catégoriser : CASE, COALESCE, NULLIF", 14, True, "#1f4e79"))
    g.append(t(20, 46, "Trois outils de transformation : etiqueter (CASE), replier les absences (COALESCE),",
               10, False, "#42566b"))
    g.append(t(20, 62, "produire des absences (NULLIF). Syntaxe standard : DuckDB, PostgreSQL, SQLite identiques.",
               10, False, "#42566b"))

    # CASE : le carrefour
    g.append(r(20, 84, 240, 40, fond="#f7fafc", bord="#1f4e79"))
    g.append(t(36, 100, "montant_ttc", 11, True, "#1f4e79"))
    g.append(t(36, 116, "(50 008 ventes)", 9, False, "#42566b"))
    g.append(fleche(270, 104, 320, 104))
    g.append(r(330, 80, 130, 50, fond="#fff8e1", bord="#7a3b12"))
    g.append(t(346, 100, "CASE", 12, True, "#7a3b12"))
    g.append(t(346, 118, "WHEN / ELSE", 9, False, "#1a1a1a"))
    branches = [
        (490, 70, "< 50 000", "a) 12 753 ventes", "#1f4e79"),
        (490, 108, "< 200 000", "b) 21 509 ventes", "#1f4e79"),
        (490, 146, "sinon (ELSE)", "c) 15 746 ventes", "#1f4e79"),
    ]
    for x, y, cond, res, c in branches:
        g.append(fleche(470, 104, x - 6, y + 12))
        g.append(r(x, y, 120, 26, fond="#ffffff", bord=c))
        g.append(t(x + 10, y + 18, cond, 10, False, "#1a1a1a"))
        g.append(r(x + 128, y, 152, 26, fond="#f7fafc", bord="#9db3c8"))
        g.append(t(x + 138, y + 18, res, 10, False, "#1a1a1a"))
    g.append(t(36, 190, "Total des 3 tranches : 12 753 + 21 509 + 15 746 = 50 008 (controle)", 10, True, "#7a3b12"))

    # COALESCE
    g.append(r(20, 210, 350, 84, fond="#ffffff", bord="#1f4e79", trait=1.5))
    g.append(t(36, 232, "COALESCE(a, b, ...) : la 1re non NULL", 12, True, "#1f4e79"))
    g.append(t(36, 254, "COALESCE(ville, '(non renseignee)')", 10, False, "#1a1a1a"))
    g.append(t(36, 274, "-> ville si presente, sinon le repli", 10, False, "#1a1a1a"))
    g.append(t(36, 292, "Ne regarde QUE les NULL (pas 0, pas vide).", 10, False, "#7a3b12"))

    # NULLIF
    g.append(r(390, 210, 370, 84, fond="#ffffff", bord="#7a3b12", trait=1.5))
    g.append(t(406, 232, "NULLIF(a, b) : NULL si a = b, sinon a", 12, True, "#7a3b12"))
    g.append(t(406, 254, "NULLIF(plafond, 0)  ->  le 0 devient NULL", 10, False, "#1a1a1a"))
    g.append(t(406, 274, "COALESCE(NULLIF(x, 0), -1)  ->  vider puis replier", 10, False, "#1a1a1a"))
    g.append(t(406, 292, "Le miroir de COALESCE : il produit le NULL.", 10, False, "#7a3b12"))

    # Bande du bas : regles
    g.append(r(20, 312, 740, 76, fond="#fdf7f4", bord="#7a3b12"))
    g.append(t(36, 334, "Regles du CASE", 12, True, "#7a3b12"))
    g.append(t(36, 356, "1. Toujours un ELSE (sinon NULL sur les non couverts).  2. Les WHEN sont testes dans l'ordre.",
               10, False, "#1a1a1a"))
    g.append(t(36, 376, "3. Tranches disjointes : borne haute seulement (< 50 000, < 200 000, sinon).",
               10, False, "#1a1a1a"))
    g.append(t(36, 396, "4. Meme type des deux cotes du COALESCE (pas de nombre et de texte melanges).",
               10, False, "#1a1a1a"))
    return "".join(g) + "</svg>"


def planche_group_by_c05():
    """Planche 5 - C05 : GROUP BY / HAVING / comptages conditionnels."""
    g = [svg_ouverture()]
    g.append(t(20, 26, "GROUP BY : une ligne de synthese par groupe", 14, True, "#1f4e79"))
    g.append(t(20, 46, "Les tiroirs : chaque ligne va dans le groupe de sa cle ; l'agregat se recalcule par tiroir.",
               10, False, "#42566b"))

    # Bande du haut : 50 008 -> 5 groupes
    g.append(r(20, 66, 300, 54, fond="#f7fafc", bord="#1f4e79"))
    g.append(t(36, 86, "50 008 ventes", 11, True, "#1f4e79"))
    g.append(t(36, 104, "montant_ttc, id_magasin, id_mode …", 9, False, "#1a1a1a"))
    g.append(fleche(330, 93, 390, 93))
    g.append(r(400, 66, 180, 54, fond="#fff8e1", bord="#7a3b12"))
    g.append(t(416, 86, "GROUP BY", 12, True, "#7a3b12"))
    g.append(t(416, 104, "id_magasin (la cle)", 9, False, "#1a1a1a"))
    g.append(fleche(590, 93, 650, 93))
    g.append(r(660, 66, 100, 54, fond="#fff8e1", bord="#7a3b12"))
    g.append(t(676, 86, "5 lignes", 11, True, "#7a3b12"))
    g.append(t(676, 104, "1 par groupe", 9, False, "#1a1a1a"))

    # Table de resultat mini
    g.append(r(20, 138, 400, 130, fond="#ffffff", bord="#9db3c8"))
    g.append(t(36, 158, "id_magasin", 10, True, "#42566b"))
    g.append(t(150, 158, "nb_ventes", 10, True, "#42566b"))
    g.append(t(270, 158, "ca (FCFA)", 10, True, "#42566b"))
    lignes = [
        ("4", "10 061", "1 596 813 264"),
        ("1", "10 099", "1 595 223 423"),
        ("2", "10 033", "1 578 987 708"),
        ("5", "9 942", "1 572 297 452"),
        ("3", "9 873", "1 564 937 883"),
    ]
    for i, (a, b, c) in enumerate(lignes):
        y = 178 + i * 18
        g.append(t(36, y, a, 10, False, "#1a1a1a"))
        g.append(t(150, y, b, 10, False, "#1a1a1a"))
        g.append(t(270, y, c, 10, False, "#1a1a1a"))
    g.append(r(20, 268, 400, 22, fond="#fdf7f4", bord="#7a3b12"))
    g.append(t(36, 284, "somme des ca = 7 908 259 731 (controle C04)", 9, True, "#7a3b12"))

    # Colonne droite : HAVING
    g.append(r(440, 138, 320, 152, fond="#fff8e1", bord="#7a3b12"))
    g.append(t(456, 158, "HAVING : filtre sur les GROUPES", 11, True, "#7a3b12"))
    g.append(t(456, 180, "HAVING COUNT(*) > 9900", 10, False, "#1a1a1a"))
    g.append(t(456, 200, "-> 4 groupes : le magasin 3 (9 873) sort", 10, False, "#1a1a1a"))
    g.append(t(456, 222, "Le seuil est une decision métier : le documenter.", 9, False, "#42566b"))
    g.append(t(456, 244, "Agreger puis filtrer : HAVING voit les totaux.", 9, False, "#42566b"))
    g.append(t(456, 266, "WHERE voit les lignes, HAVING voit les groupes.", 9, False, "#42566b"))

    # Bande du bas : pieges
    g.append(r(20, 306, 740, 76, fond="#fdf7f4", bord="#7a3b12"))
    g.append(t(36, 328, "Pieges du GROUP BY", 12, True, "#7a3b12"))
    g.append(t(36, 350, "1. Regrouper par un libelle double (rayon) : 8 categories fondent en 5 groupes, sans erreur.",
               10, False, "#1a1a1a"))
    g.append(t(36, 370, "2. Un agrégat dans WHERE : interdit (\"WHERE clause cannot contain aggregates\") -> HAVING.",
               10, False, "#1a1a1a"))
    g.append(t(36, 390, "3. Oublier le ELSE 0 dans SUM(CASE WHEN …) : les NULL ne s'additionnent pas.",
               10, False, "#1a1a1a"))
    return "".join(g) + "</svg>"


def planche_agregats_c04():
    """Planche 4 - C04 : les 5 agregats + regle des NULL."""
    g = [svg_ouverture()]
    g.append(t(20, 26, "Les 5 agregats : de N lignes a 1 valeur", 14, True, "#1f4e79"))
    g.append(t(20, 46, "Chaque agregat consomme un ensemble de valeurs et renvoie une unique valeur.",
               10, False, "#42566b"))

    # Bande du haut : N lignes -> 1 ligne de synthese
    g.append(r(20, 66, 350, 60, fond="#f7fafc", bord="#1f4e79"))
    g.append(t(36, 88, "50 008 lignes de vente", 11, True, "#1f4e79"))
    g.append(t(36, 108, "montant_ttc : 763 a 594 363 FCFA", 9, False, "#1a1a1a"))
    g.append(fleche(392, 96, 448, 96))
    g.append(r(450, 66, 310, 60, fond="#fff8e1", bord="#7a3b12"))
    g.append(t(466, 88, "1 ligne de synthese", 11, True, "#7a3b12"))
    g.append(t(466, 108, "ca_brut = 7 908 259 731 FCFA", 9, False, "#1a1a1a"))

    # Bande du milieu : les 5 agregats
    funcs = [
        ("COUNT", "compter", "50 008", "#1f4e79"),
        ("SUM", "totaliser", "7 908 259 731", "#1f4e79"),
        ("AVG", "moyenner", "158 140", "#1f4e79"),
        ("MIN", "borne basse", "763", "#1f4e79"),
        ("MAX", "borne haute", "594 363", "#1f4e79"),
    ]
    y0 = 150
    bw = 144
    for i, (nom, role, val, c) in enumerate(funcs):
        x = 20 + i * (bw + 7)
        g.append(r(x, y0, bw, 74, fond="#ffffff", bord=c, trait=1.5))
        g.append(t(x + 10, y0 + 20, nom, 12, True, c))
        g.append(t(x + 10, y0 + 38, role, 9, False, "#42566b"))
        g.append(r(x, y0 + 44, bw, 24, fond="#f7fafc", bord="#9db3c8"))
        g.append(t(x + 10, y0 + 60, val + " FCFA", 9, True, "#1a1a1a"))

    g.append(t(20, 246, "Variante : COUNT(DISTINCT id_client) = 1 200 (valeurs differentes, pas lignes).",
               10, False, "#1a1a1a"))
    g.append(t(20, 264, "ROUND : arrondi a la presentation.  ROUND(AVG(montant_ttc), 2) garde 2 decimales.",
               10, False, "#1a1a1a"))

    # Bande du bas : regle des NULL
    g.append(r(20, 286, 740, 96, fond="#fdf7f4", bord="#7a3b12"))
    g.append(t(36, 308, "Regle unique des NULL : tous les agregats ignorent les NULL de leur colonne", 12, True, "#7a3b12"))
    g.append(t(36, 330, "COUNT(*)           -> compte les lignes  (les NULL comptent dans le nombre de lignes)",
               10, False, "#1a1a1a"))
    g.append(t(36, 348, "COUNT(col)         -> compte les valeurs non NULL  (colonne 100 % NULL : resultat 0)",
               10, False, "#1a1a1a"))
    g.append(t(36, 366, "SUM / AVG / MIN / MAX  -> ignorent les NULL  (colonne 100 % NULL : resultat NULL, pas 0)",
               10, False, "#1a1a1a"))
    g.append(t(36, 384, "Parade :  COALESCE(SUM(x), 0)   (M07.C06)", 10, False, "#7a3b12"))
    return "".join(g) + "</svg>"


# Planche 1 - C01 : l'ordre reel d'execution d'une requete SQL
def planche_ordre_execution():
    g = [svg_ouverture()]
    g.append(t(20, 26, "L'ordre reel d'execution d'une requete SQL", 14, True, "#1f4e79"))
    g.append(t(20, 46, "La machine traite les clauses dans cet ordre, PAS dans l'ordre d'ecriture.",
               10, False, "#42566b"))

    # 8 etapes en pipeline horizontal (de haut en bas, comme une cascade)
    etapes = [
        ("1. FROM",       "charger la table",                   "#1f4e79"),
        ("2. WHERE",      "filtrer les lignes (avant agregat)",  "#1f4e79"),
        ("3. GROUP BY",   "regrouper les lignes partageant ...","#1f4e79"),
        ("4. HAVING",     "filtrer les groupes (apres agregat)","#1f4e79"),
        ("5. SELECT",     "choisir les colonnes / expressions", "#7a3b12"),
        ("6. DISTINCT",   "dedoublonner les lignes",             "#7a3b12"),
        ("7. ORDER BY",   "trier les lignes du resultat",        "#7a3b12"),
        ("8. LIMIT",      "tronquer (OFFSET pour paginer)",      "#7a3b12"),
    ]

    y0 = 80
    h_box = 38
    for i, (titre, desc, couleur) in enumerate(etapes):
        y = y0 + i * h_box
        # le numero d'ordre en pastille
        g.append(r(20, y, 36, h_box - 6, fond="#1a1a1a", bord="#1a1a1a", rx=18))
        num = titre.split(".")[0]
        g.append(t(38, y + 22, num, 12, True, "#ffffff", "middle"))
        # la clause
        g.append(r(70, y, 130, h_box - 6, fond="#ffffff", bord=couleur, trait=1.5))
        g.append(t(80, y + 22, titre.split(" ", 1)[1], 11, True, couleur))
        # la description
        g.append(t(210, y + 22, desc, 10, False, "#1a1a1a"))
        # fleche vers le bas (sauf la derniere)
        if i < len(etapes) - 1:
            g.append(fleche(38, y + h_box - 4, 38, y + h_box + 4))

    # Bandeau bas : la cle du module
    g.append(r(20, 400, 740, 70, fond="#f7fafc", bord="#1f4e79"))
    g.append(t(36, 422, "90 % des erreurs SQL viennent d'un malentendu sur cet ordre.", 11, True, "#1f4e79"))
    g.append(t(36, 442, "On ecrit SELECT en premier ; la machine le traite en 5e position.", 10, False, "#1a1a1a"))
    g.append(t(36, 458, "Un alias de SELECT n'existe pas encore au moment du WHERE : erreur 'column does not exist'.", 9, False, "#42566b"))
    return "".join(g) + "</svg>"


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
        "M07_C01_ordre_execution_requete_sql.svg": planche_ordre_execution(),
        "M07_C02_entonnoir_where.svg": planche_entonnoir_where(),
        "M07_C03_pipeline_order_by_limit_offset.svg": planche_pipeline_order_by(),
        "M07_C04_agregats_n_lignes_1_valeur.svg": planche_agregats_c04(),
        "M07_C05_group_by_having_comptages.svg": planche_group_by_c05(),
        "M07_C06_case_coalesce_nullif.svg": planche_categorisation_c06(),
        "M07_C07_jointures_etoile_et_4_types.svg": planche_jointures_c07(),
        "M07_C08_requetes_composees_cte_vue_exists.svg": planche_requetes_composees_c08(),
    }
    for nom, contenu in planches.items():
        chemin = os.path.join(FIG, nom)
        open(chemin, "w", encoding="utf-8").write(contenu)
        print("figure ->", nom, "(%.1f Ko)" % (os.path.getsize(chemin) / 1024))
        audit(nom, contenu)


if __name__ == "__main__":
    main()
