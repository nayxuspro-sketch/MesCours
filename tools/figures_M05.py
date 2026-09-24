#!/usr/bin/env python3
"""figures_M05.py — les planches SVG du module M05 (langage commun des transformations).

Cinq planches pour le module M05, mêmes contraintes que tools/figures_M04.py :
  * largeur utile 780 px ; texte jamais plus large que 0,605 × taille × nb de caractères ;
  * ancres posées à la main (``start`` par défaut, ``middle`` pour les chiffres centrés) ;
  * jeu de signes latin-1 étendu (accents, guillemets français, flèche →) ;
  * pas de glyphe hors latin-1 : la planche est rendue en PDF, les accents doivent passer.

Usage : python3 tools/figures_M05.py
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


# Planche 1 — Le langage commun des transformations (C01) : 10 cases
def planche_langage_commun():
    g = [svg_ouverture()]
    g.append(t(20, 26, "Le langage commun : 10 opérations, 4 classes, 3 moteurs", 14, True, "#1f4e79"))
    g.append(t(20, 46, "Le pipeline se décrit en 10 verbes exécutés par Power Query, SQL DuckDB ou pandas.", 10, False, "#42566b"))
    # Les 4 classes en colonnes
    classes = [
        ("M", "manipulation", "#1f4e79", 60, 90, 4),
        ("Op", "opérateurs", "#7a3b12", 240, 90, 4),
        ("P", "paramètres", "#3f7d3f", 420, 90, 1),
        ("Ag", "agrégations", "#5b3a8e", 600, 90, 1),
    ]
    for code, nom, couleur, x, y, n in classes:
        g.append(r(x, y, 160, 30, fond="#ffffff", bord=couleur, trait=2))
        g.append(t(x + 8, y + 20, f"{code} — {nom}", 11, True, couleur))
        # Les verbes
        verbes = {
            "M": ["extraire", "convertir", "renommer", "réparer"],
            "Op": ["projet", "filtre", "tri", "jointure"],
            "P": ["paramètres"],
            "Ag": ["agréger"],
        }[code]
        for i, verbe in enumerate(verbes):
            vx = x
            vy = y + 38 + i * 26
            g.append(r(vx, vy, 160, 22, fond="#f7fafc", bord="#c9d3dd"))
            g.append(t(vx + 8, vy + 15, verbe, 10, False, "#1a1a1a"))
    # Bandeau bas : les 3 moteurs
    g.append(r(20, 320, 740, 130, fond="#eef3f8", bord="#1f4e79"))
    g.append(t(36, 342, "Trois moteurs, une même grammaire", 12, True, "#1f4e79"))
    moteurs = [
        ("Power Query", "Excel M · clic + formule", 60),
        ("SQL DuckDB", "SELECT ... FROM v", 320),
        ("pandas", "df.assign(...).query(...)", 580),
    ]
    for nom, detail, x in moteurs:
        g.append(t(x, 372, nom, 12, True, "#1a1a1a"))
        g.append(t(x, 392, detail, 10, False, "#42566b"))
    g.append(t(36, 432, "Le même pipeline produit la même table dans les trois moteurs :", 10, False, "#1a1a1a"))
    g.append(t(36, 448, "mars = 6 884 lignes, total 464 096 003 FCFA, 101 enrichies, empreinte sha256 identique.", 10, False, "#42566b"))
    return "".join(g) + "</svg>"


# Planche 2 — Le pipeline Power Query (C02) — 14 étapes
def planche_pipeline_pq():
    g = [svg_ouverture()]
    g.append(t(20, 26, "Power Query : 14 étapes pour transformer mars 2025", 14, True, "#1f4e79"))
    g.append(t(20, 46, "Chaque étape est nommée, rejouable, et alimente le verdict du fil rouge.", 10, False, "#42566b"))
    etapes = [
        ("Source", "Dossier brut CSV"),
        ("Navigation", "Sélection table ventes"),
        ("Typage texte", "Forcer le type texte"),
        ("Colonne cond.", "Vide si nul"),
        ("Promouvoir en-têtes", "Première ligne"),
        ("Supprimer le haut", "1 ligne"),
        ("Remplir vers le bas", "Down-fill"),
        ("Fractionner", "date_vente par tirets"),
        ("Remplacer", "« FCFA », virgules"),
        ("Convertir", "Texte → Nombre"),
        ("Fusion", "Jointure clients"),
        ("Col. conditionnelle", "Catégorie, mois, retour"),
        ("Suppr. doublons", "5-colonnes métier"),
        ("Charger", "Table propre mars2025"),
    ]
    cols = 4
    cellw, cellh = 180, 38
    x0, y0 = 20, 80
    for i, (e1, e2) in enumerate(etapes):
        col = i % cols
        row = i // cols
        x = x0 + col * (cellw + 8)
        y = y0 + row * (cellh + 8)
        g.append(r(x, y, cellw, cellh, fond="#f7fafc", bord="#c9d3dd"))
        g.append(t(x + 8, y + 14, f"{i+1}. {e1}", 10, True, "#1f4e79"))
        g.append(t(x + 8, y + 28, e2, 9, False, "#42566b"))
    # Bandeau bas : verdict
    g.append(r(20, 290, 740, 100, fond="#eef3f8", bord="#1f4e79"))
    g.append(t(36, 312, "Verdict du fil rouge (mars 2025)", 12, True, "#1f4e79"))
    g.append(t(36, 332, "6 884 lignes · total 464 096 003 FCFA · 101 enrichies · empreinte sha256 identique", 10, False, "#1a1a1a"))
    g.append(t(36, 350, "Rejouable : avril = 6 639 lignes, mai = 5 530 lignes, même schéma → même qualité.", 10, False, "#42566b"))
    return "".join(g) + "</svg>"


# Planche 3 — Le pipeline SQL DuckDB (C03) — 11 tables temporaires
def planche_pipeline_sql():
    g = [svg_ouverture()]
    g.append(t(20, 26, "SQL DuckDB : 11 tables temporaires, un seul verdict", 14, True, "#1f4e79"))
    g.append(t(20, 46, "Le pipeline SQL passe par 11 CTE (Common Table Expressions) nommées v1...v6.", 10, False, "#42566b"))
    tables = [
        ("v_brut", "Source brute (6 884 + reste)", "#eef3f8"),
        ("v_dates", "Dates transposées (23 → 0)", "#f7fafc"),
        ("v_types", "TRY_CAST sur toutes colonnes", "#f7fafc"),
        ("v_montants", "1 200 FCFA → 1200 (114 texte)", "#fdf7f4"),
        ("v_remises", "> 1 = corrigé (32)", "#fdf7f4"),
        ("v_retours", "filtre 'retour' (74)", "#fdf7f4"),
        ("v_clients", "EXCLUDE clients inconnus", "#f7fafc"),
        ("v_mars", "BETWEEN 01-03 et 31-03", "#f7fafc"),
        ("v_cle", "ROW_NUMBER sur 5 colonnes", "#eef3f8"),
        ("v_dedup", "DISTINCT (6 798, 86 doublons)", "#f2f7f2"),
        ("v_final", "Jointure 101", "#f2f7f2"),
    ]
    n = len(tables)
    colh, colw = 170, 36
    for i, (nom, detail, fond) in enumerate(tables):
        x = 12 + i * 70
        y = 90
        g.append(r(x, y, 64, colh, fond=fond, bord="#c9d3dd"))
        g.append(t(x + 32, y + 16, nom, 10, True, "#1f4e79", "middle"))
        # Détail sous le bloc
        lignes = [detail]
        if len(detail) > 12:
            mots = detail.split()
            l1, l2 = [], []
            for m in mots:
                (l1 if len(" ".join(l1)) < 14 else l2).append(m)
            lignes = [" ".join(l1), " ".join(l2)]
        ly = y + colh + 14
        for lig in lignes[:2]:
            g.append(t(x + 32, ly, lig, 7, False, "#42566b", "middle"))
            ly += 10
        # Flèche entre blocs
        if i < n - 1:
            g.append(fleche(x + 64, y + colh / 2, x + 70, y + colh / 2))
    # Bandeau bas : commande
    g.append(r(20, 320, 740, 90, fond="#1f4e79", bord="#1f4e79"))
    g.append(t(36, 346, "Commande DuckDB : CREATE OR REPLACE TABLE v AS SELECT ... FROM ...", 11, True, "#ffffff"))
    g.append(t(36, 370, "11 CTE nommées v1...v6, EXCLUDE rn pour retirer la colonne de rang,", 10, False, "#ffffff"))
    g.append(t(36, 386, "BIGINT TRY_CAST tolérant, LPAD pour la longueur fixe.", 10, False, "#ffffff"))
    return "".join(g) + "</svg>"


# Planche 4 — Le pipeline pandas (C04) — 8 cellules de notebook
def planche_pipeline_pandas():
    g = [svg_ouverture()]
    g.append(t(20, 26, "pandas 2,2,3 : 8 cellules de notebook, une seule chaîne assign/pipe", 14, True, "#1f4e79"))
    g.append(t(20, 46, "Chaque cellule a un en-tête, un code, des assertions, et un verdict.", 10, False, "#42566b"))
    cellules = [
        ("1", "Préambule", "import pandas, openpyxl"),
        ("2", "Lecture Excel", "pd.read_excel → brutes"),
        ("3", "Conversion", "montant_ttc texte → BIGINT"),
        ("4", "Coupe mars", "between 01-03 et 31-03"),
        ("5", "Dédoublonnage", "sort_values + drop_duplicates"),
        ("6", "Renommage", "rename lower_snake_case"),
        ("7", "Jointure", "merge clé complète 101"),
        ("8", "Verdict", "sha256 == OK · export"),
    ]
    cols = 4
    cellw, cellh = 180, 60
    x0, y0 = 20, 80
    for i, (n, t1, t2) in enumerate(cellules):
        col = i % cols
        row = i // cols
        x = x0 + col * (cellw + 8)
        y = y0 + row * (cellh + 8)
        g.append(r(x, y, cellw, cellh, fond="#f7fafc", bord="#c9d3dd"))
        g.append(t(x + 8, y + 14, f"Cellule {n}", 10, True, "#7a3b12"))
        g.append(t(x + 8, y + 30, t1, 11, True, "#1f4e79"))
        g.append(t(x + 8, y + 46, t2, 9, False, "#42566b"))
    # Bandeau bas : verdict
    g.append(r(20, 240, 740, 100, fond="#fdf7f4", bord="#c9d3dd"))
    g.append(t(36, 262, "Verdict — empreintes identiques Power Query == SQL DuckDB == pandas", 12, True, "#7a3b12"))
    g.append(t(36, 282, "mars = 6 884 lignes · total 464 096 003 FCFA · 101 enrichies · 0 montant texte", 10, False, "#1a1a1a"))
    g.append(t(36, 302, "SettingWithCopyWarning : df = df.assign(...).copy() pour le neutraliser", 10, False, "#42566b"))
    g.append(t(36, 320, "Chaîne canonique : assign → sort_values → drop_duplicates", 10, False, "#42566b"))
    return "".join(g) + "</svg>"


# Planche 5 — La grille de décision 4 critères × 3 outils (C05)
def planche_grille_decision():
    g = [svg_ouverture()]
    g.append(t(20, 26, "Arbitrer un outil : 4 critères, 3 moteurs, 1 verdict", 14, True, "#1f4e79"))
    g.append(t(20, 46, "La grille croise taille, fréquence, compétences, gouvernance avec Power Query / DuckDB / pandas.", 10, False, "#42566b"))
    # En-têtes de colonnes
    outils = ["Power Query", "SQL DuckDB", "pandas"]
    criteres = [
        ("< 100 000 lignes",       ["V", "V",  "V"]),
        ("100 k — 1 M",            ["X", "V",  "V"]),
        ("> 1 M",                  ["X", "V",  "limite RAM"]),
        ("Fréq. mensuelle",        ["V", "V",  "V"]),
        ("Fréq. quotidienne",      ["V", "V",  "V"]),
        ("Temps réel",             ["X", "V",  "V"]),
        ("Équipe bureautique",     ["V", "cli", "X"]),
        ("Équipe SQL",             ["vis", "V", "vis"]),
        ("Équipe Python",          ["X", "V",  "V"]),
        ("Gouvernance centrale",   ["svc", "V", "lock"]),
        ("Gouvernance locale",     ["V",  "V",  "V"]),
    ]
    x0, y0 = 30, 80
    cellw = 130
    cellh = 28
    # Première colonne : critères
    g.append(r(x0, y0, cellw + 80, cellh * (len(criteres) + 1), fond="#f7fafc", bord="#1f4e79"))
    g.append(t(x0 + 10, y0 + 18, "Critère", 11, True, "#1f4e79"))
    # En-têtes outils
    for j, outil in enumerate(outils):
        g.append(r(x0 + 130 + j * 180, y0, 180, cellh, fond="#1f4e79", bord="#1f4e79"))
        g.append(t(x0 + 130 + j * 180 + 90, y0 + 18, outil, 12, True, "#ffffff", "middle"))
    # Cellules
    for i, (crit, _) in enumerate(criteres):
        y = y0 + (i + 1) * cellh
        g.append(r(x0 + 130 + 0, y, 540, cellh, fond="#ffffff", bord="#c9d3dd"))
        # Le critère
        g.append(t(x0 + 10, y + 18, crit, 10, True, "#1a1a1a"))
        # Les 3 cellules par outil
        for j, verdit in enumerate(criteres[i][1]):
            cx = x0 + 130 + j * 180
            g.append(r(cx, y, 180, cellh, fond="#ffffff", bord="#c9d3dd"))
            couleur = {"V": "#3f7d3f", "X": "#a02020"}.get(verdit, "#1a1a1a")
            g.append(t(cx + 90, y + 18, verdit, 12, True, couleur, "middle"))
    # Bandeau bas : règle
    g.append(r(20, 410, 740, 60, fond="#fdf7f4", bord="#7a3b12"))
    g.append(t(36, 432, "Règle unique — le critère limitant tranche en premier", 12, True, "#7a3b12"))
    g.append(t(36, 452, "Le verdict n'est pas une règle absolue : c'est une aide à la décision réversible.", 10, False, "#42566b"))
    return "".join(g) + "</svg>"


def audit(nom, svg):
    """Largeur estimée par ligne et jeu de signes.

    Mêmes seuils et même jeu autorisé que figures_M04.py.
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
    planches = {
        "M05_C01_langage_commun_des_transformations.svg": planche_langage_commun(),
        "M05_C02_pipeline_power_query.svg": planche_pipeline_pq(),
        "M05_C03_pipeline_sql_duckdb.svg": planche_pipeline_sql(),
        "M05_C04_pipeline_pandas.svg": planche_pipeline_pandas(),
        "M05_C05_grille_de_decision.svg": planche_grille_decision(),
    }
    for nom, contenu in planches.items():
        chemin = os.path.join(FIG, nom)
        open(chemin, "w", encoding="utf-8").write(contenu)
        print("figure →", nom, "(%.1f Ko)" % (os.path.getsize(chemin) / 1024))
        audit(nom, contenu)


if __name__ == "__main__":
    main()
