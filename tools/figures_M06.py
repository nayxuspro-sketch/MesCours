#!/usr/bin/env python3
"""figures_M06.py — les planches SVG du module M06 (bases de données relationnelles).

Cinq planches pour le module M06, mêmes contraintes que tools/figures_M05.py :
  * largeur utile 780 px ; un texte ne dépasse jamais 0,605 × taille × nombre de caractères ;
  * ancres posées à la main (``start`` par défaut, ``middle`` pour les chiffres centrés) ;
  * aucun glyphe hors latin-1 : la planche est rendue en PDF, les accents doivent passer.

Cinq planches :
  M06_C01_cinq_limites_classeur_excel.svg  - les cinq limites + la solution SGBD
  M06_C02_anatomie_table.svg              - les 6 attributs d'une table + le squelette CREATE
  M06_C03_trois_relations_cardinalite.svg - 1-1, 1-N, N-M + la table de jointure
  M06_C04_trois_moteurs_ducksqlpg.svg     - DuckDB intégré / SQLite embarqué / PG serveur
  M06_C05_carte_paysage_nosql.svg         - 4 familles NoSQL + datalake/DWH/lakehouse + 5 mots

Usage : python3 tools/figures_M06.py
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


# Planche 1 — Cinq limites du classeur Excel (C01)
def planche_cinq_limites():
    g = [svg_ouverture()]
    g.append(t(20, 26, "Cinq limites du classeur Excel — pourquoi une base de données ?", 14, True, "#1f4e79"))
    g.append(t(20, 46, "Le classeur s'effondre a la 3e table jointe et a la 50000e ligne. Cinq limites, "
                       "une solution : le SGBD.", 10, False, "#42566b"))
    # 5 limites en colonne
    limites = [
        ("1. Redondance", "la ville_client est recopiée 13 × par client", "#fdf7f4"),
        ("2. Anomalie", "TVA 18 % → 19 % : 24 000 lignes à modifier", "#fdf7f4"),
        ("3. Multi-valué", "categorie_pref ne porte qu'une seule catégorie", "#fdf7f4"),
        ("4. Concurrence", "deux caissières ouvrent le même classeur en double", "#eef3f8"),
        ("5. Volumétrie", "240 000 lignes : Excel met 30 s à ouvrir", "#fbe9e7"),
    ]
    for i, (t1, t2, fond) in enumerate(limites):
        y = 80 + i * 50
        g.append(r(20, y, 740, 42, fond=fond, bord="#c9d3dd"))
        g.append(t(36, y + 17, t1, 11, True, "#1f4e79"))
        g.append(t(36, y + 33, t2, 9, False, "#1a1a1a"))
    # Bandeau bas : la solution SGBD
    g.append(r(20, 350, 740, 80, fond="#f2f7f2", bord="#3f7d3f"))
    g.append(t(36, 372, "La solution — un SGBD (DuckDB / SQLite / PostgreSQL)", 12, True, "#3f7d3f"))
    g.append(t(36, 392, "Contraintes portees par la base : PRIMARY KEY, FOREIGN KEY, NOT NULL, CHECK.", 10, False, "#1a1a1a"))
    g.append(t(36, 408, "Verifier l'integrite par 3 requetes : Q1 referentielle, Q2 montants, Q3 rejouable.", 10, False, "#1a1a1a"))
    g.append(t(36, 424, "3 criteres de bascule : taille > 100k lignes, joints >= 3, concurrence >= 2.", 10, False, "#1a1a1a"))
    return "".join(g) + "</svg>"


# Planche 2 — Anatomie d'une table (C02)
def planche_anatomie_table():
    g = [svg_ouverture()]
    g.append(t(20, 26, "Anatomie d'une table — 6 attributs + le squelette CREATE TABLE", 14, True, "#1f4e79"))
    g.append(t(20, 46, "Une table n'est pas un fichier plat : elle est un objet à 6 attributs portees "
                       "par le SGBD.", 10, False, "#42566b"))
    # Les 6 attributs
    attributs = [
        ("1. Nom", "client", "l'identifiant unique, non-renommable"),
        ("2. Schéma", "11 colonnes", "la structure, distincte des donnees"),
        ("3. Types", "INTEGER, TEXT, DATE", "chaque colonne a un type logique"),
        ("4. Contraintes", "NOT NULL, UNIQUE, CHECK", "les regles que les donnees suivent"),
        ("5. Lignes", "0 a 1 891", "les donnees qui respectent le schema"),
        ("6. PK", "id_client INTEGER", "l'identifiant unique d'une ligne"),
    ]
    for i, (t1, t2, t3) in enumerate(attributs):
        y = 80 + i * 44
        g.append(r(20, y, 740, 38, fond="#ffffff", bord="#c9d3dd"))
        g.append(t(36, y + 16, t1, 11, True, "#1f4e79"))
        g.append(t(200, y + 16, t2, 11, True, "#7a3b12"))
        g.append(t(390, y + 16, t3, 9, False, "#1a1a1a"))
    # Bandeau bas : squelette CREATE
    g.append(r(20, 350, 740, 100, fond="#f7fafc", bord="#1f4e79"))
    g.append(t(36, 372, "Squelette : CREATE TABLE nom (col1 type contraintes, ..., PK, FK)", 11, True, "#1f4e79"))
    g.append(t(36, 392, "CREATE TABLE client (", 10, False, "#1a1a1a"))
    g.append(t(60, 408, "id_client INTEGER PRIMARY KEY,", 10, False, "#1a1a1a"))
    g.append(t(60, 424, "telephone TEXT NOT NULL UNIQUE,", 10, False, "#1a1a1a"))
    g.append(t(60, 440, "fidelite_niveau TEXT DEFAULT 'COMPTOIR' CHECK (fidelite_niveau IN (...))", 10, False, "#1a1a1a"))
    g.append(t(36, 458, ");", 10, False, "#1a1a1a"))
    return "".join(g) + "</svg>"


# Planche 3 — Trois relations (C03)
def planche_trois_relations():
    g = [svg_ouverture()]
    g.append(t(20, 26, "Trois relations — 1-1, 1-N, N-M, et la table de jointure", 14, True, "#1f4e79"))
    g.append(t(20, 46, "La FK est TOUJOURS du N vers le 1. La N-M exige une table de jointure a cle "
                       "composee.", 10, False, "#42566b"))
    # 3 colonnes : 1-1 / 1-N / N-M
    titres = [
        ("1-1 (rare)", "client <-> client_profil", "#eef3f8"),
        ("1-N (la plus courante)", "client (1) -> vente (N)", "#eef3f8"),
        ("N-M (la subtile)", "client (N) <-> categorie (M)", "#fdf7f4"),
    ]
    for i, (t1, t2, fond) in enumerate(titres):
        x = 20 + i * 256
        g.append(r(x, 80, 240, 32, fond=fond, bord="#1f4e79"))
        g.append(t(x + 12, 100, t1, 12, True, "#1f4e79"))
        g.append(t(x + 12, 122, t2, 10, False, "#1a1a1a"))
        # schema simplifie selon la relation
        if i == 0:
            # 1-1 : deux boxes relies par une fleche simple
            g.append(r(x + 20, 150, 80, 36, fond="#ffffff", bord="#c9d3dd"))
            g.append(t(x + 60, 172, "client", 10, True, "#1f4e79", "middle"))
            g.append(r(x + 140, 150, 80, 36, fond="#ffffff", bord="#c9d3dd"))
            g.append(t(x + 180, 172, "profil", 10, True, "#1f4e79", "middle"))
            g.append(t(x + 60, 200, "id_client PK", 8, False, "#7a3b12", "middle"))
            g.append(fleche(x + 100, 168, x + 140, 168))
            g.append(t(x + 120, 165, "1", 9, True, "#3f7d3f", "middle"))
        elif i == 1:
            # 1-N : client au centre, vente a droite
            g.append(r(x + 20, 150, 70, 36, fond="#ffffff", bord="#c9d3dd"))
            g.append(t(x + 55, 172, "client", 10, True, "#1f4e79", "middle"))
            g.append(r(x + 140, 150, 70, 36, fond="#ffffff", bord="#c9d3dd"))
            g.append(t(x + 175, 172, "vente", 10, True, "#1f4e79", "middle"))
            g.append(fleche(x + 90, 168, x + 140, 168))
            g.append(t(x + 115, 165, "N", 9, True, "#a02020", "middle"))
            g.append(t(x + 55, 200, "id_client PK", 8, False, "#7a3b12", "middle"))
            g.append(t(x + 175, 200, "id_client FK", 8, False, "#7a3b12", "middle"))
        else:
            # N-M : trois boxes (client, ccp, categorie)
            g.append(r(x + 10, 150, 60, 36, fond="#ffffff", bord="#c9d3dd"))
            g.append(t(x + 40, 172, "client", 9, True, "#1f4e79", "middle"))
            g.append(r(x + 90, 150, 60, 36, fond="#fdf7f4", bord="#7a3b12"))
            g.append(t(x + 120, 168, "ccp", 9, True, "#7a3b12", "middle"))
            g.append(t(x + 120, 180, "PK=(id_client,categorie)", 7, False, "#7a3b12", "middle"))
            g.append(r(x + 170, 150, 60, 36, fond="#ffffff", bord="#c9d3dd"))
            g.append(t(x + 200, 172, "categorie", 9, True, "#1f4e79", "middle"))
            g.append(fleche(x + 70, 168, x + 90, 168))
            g.append(fleche(x + 150, 168, x + 170, 168))
            g.append(t(x + 80, 160, "N", 9, True, "#a02020", "middle"))
            g.append(t(x + 160, 160, "M", 9, True, "#a02020", "middle"))
    # Bandeau bas : regle d'or + Cascade
    g.append(r(20, 350, 740, 100, fond="#f7fafc", bord="#1f4e79"))
    g.append(t(36, 372, "Regle d'or : la FK est TOUJOURS du N vers le 1.", 11, True, "#1f4e79"))
    g.append(t(36, 392, "Direction : vente FK client, pas l'inverse (sinon cycle).", 10, False, "#1a1a1a"))
    g.append(t(36, 408, "Action par defaut : ON DELETE RESTRICT (refuse). CASCADE documente.", 10, False, "#1a1a1a"))
    g.append(t(36, 424, "Integrite referentielle : SELECT ... FROM v LEFT JOIN c ... WHERE c.id IS NULL -> 0.", 10, False, "#1a1a1a"))
    g.append(t(36, 440, "Reparation : exclure, creer la cible, ou mettre la FK a NULL (toujours documenter).", 10, False, "#1a1a1a"))
    return "".join(g) + "</svg>"


# Planche 4 — Trois moteurs (C04)
def planche_trois_moteurs():
    g = [svg_ouverture()]
    g.append(t(20, 26, "Trois moteurs — DuckDB integre, SQLite embarque, PostgreSQL serveur", 14, True, "#1f4e79"))
    g.append(t(20, 46, "Le bon moteur depend du nombre d'utilisateurs, de la volumetrie et de la "
                       "gouvernance (cf. C05 §5.6).", 10, False, "#42566b"))
    # 3 colonnes : DuckDB / SQLite / PostgreSQL
    titres = [
        ("DuckDB (integre)", "in-process, mono-utilisateur, gratuit", "#eef3f8"),
        ("SQLite (embarque)", "fichier .sqlite, mono-utilisateur, natif", "#eef3f8"),
        ("PostgreSQL (serveur)", "client-serveur, multi-utilisateurs", "#fdf7f4"),
    ]
    for i, (t1, t2, fond) in enumerate(titres):
        x = 20 + i * 256
        g.append(r(x, 80, 240, 32, fond=fond, bord="#1f4e79"))
        g.append(t(x + 12, 100, t1, 12, True, "#1f4e79"))
        g.append(t(x + 12, 122, t2, 9, False, "#1a1a1a"))
        # Corps : install / ouverture / sauvegarde / portee
        if i == 0:
            g.append(r(x + 16, 140, 208, 220, fond="#ffffff", bord="#c9d3dd"))
            g.append(t(x + 28, 160, "Install :", 10, True, "#7a3b12"))
            g.append(t(x + 28, 178, "  pip install duckdb", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 196, "  --no-cache-dir", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 218, "Ouverture :", 10, True, "#7a3b12"))
            g.append(t(x + 28, 236, "  con = duckdb.", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 250, "    connect(':memory:')", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 272, "Sauvegarde :", 10, True, "#7a3b12"))
            g.append(t(x + 28, 290, "  EXPORT DATABASE", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 308, "  'backup_dir'", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 330, "Verdict :", 10, True, "#7a3b12"))
            g.append(t(x + 28, 348, "  1 analyste solo,", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 356, "  jusqu'a 50M l.", 9, False, "#1a1a1a"))
        elif i == 1:
            g.append(r(x + 16, 140, 208, 220, fond="#ffffff", bord="#c9d3dd"))
            g.append(t(x + 28, 160, "Install :", 10, True, "#7a3b12"))
            g.append(t(x + 28, 178, "  import sqlite3", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 196, "  (natif Python)", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 218, "Ouverture :", 10, True, "#7a3b12"))
            g.append(t(x + 28, 236, "  con = sqlite3.", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 250, "    connect('b.sqlite')", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 272, "ATTENTION :", 10, True, "#a02020"))
            g.append(t(x + 28, 290, "  PRAGMA foreign_keys", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 304, "  = ON", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 330, "Verdict :", 10, True, "#7a3b12"))
            g.append(t(x + 28, 348, "  embarque (Android,", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 356, "  iOS, Firefox, ...)", 9, False, "#1a1a1a"))
        else:
            g.append(r(x + 16, 140, 208, 220, fond="#fdf7f4", bord="#c9d3dd"))
            g.append(t(x + 28, 160, "Install :", 10, True, "#7a3b12"))
            g.append(t(x + 28, 178, "  serveur dedie", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 196, "  (~ 150 Mo)", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 218, "Connexion :", 10, True, "#7a3b12"))
            g.append(t(x + 28, 236, "  psql -h host", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 250, "    -U user", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 272, "Sauvegarde :", 10, True, "#7a3b12"))
            g.append(t(x + 28, 290, "  pg_dump mydb", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 304, "  > backup.sql", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 330, "Verdict :", 10, True, "#7a3b12"))
            g.append(t(x + 28, 348, "  multi-utilisateurs,", 9, False, "#1a1a1a"))
            g.append(t(x + 28, 356, "  production", 9, False, "#1a1a1a"))
    # Bandeau bas
    g.append(r(20, 380, 740, 70, fond="#f7fafc", bord="#1f4e79"))
    g.append(t(36, 402, "Verdict M06 : DuckDB en premiere intention (analyste solo),", 11, True, "#1f4e79"))
    g.append(t(36, 420, "SQLite pour embarquer (Android, iOS), PostgreSQL pour partager (production).", 10, False, "#1a1a1a"))
    g.append(t(36, 438, "L'atelier n'execute PAS PostgreSQL (regle 7 du plan M05 reconduite : on cite, on installe pas).", 9, False, "#7a3b12"))
    return "".join(g) + "</svg>"


# Planche 5 — Carte du paysage (C05)
def planche_carte_paysage():
    g = [svg_ouverture()]
    g.append(t(20, 26, "Carte du paysage — 4 familles NoSQL + DWH/lac/lakehouse + 5 mots", 14, True, "#1f4e79"))
    g.append(t(20, 46, "NoSQL complete le relationnel, ne le remplace pas. Le verdict depend "
                       "du cas d'usage, pas de la mode.", 10, False, "#42566b"))
    # Bloc A : 4 familles NoSQL
    g.append(r(20, 80, 360, 200, fond="#f7fafc", bord="#1f4e79"))
    g.append(t(36, 100, "Les 4 familles NoSQL", 12, True, "#1f4e79"))
    nosql = [
        ("Document", "MongoDB, CouchDB"),
        ("Cle-valeur", "Redis, DynamoDB"),
        ("Graphe", "Neo4j, JanusGraph"),
        ("Colonnes", "Cassandra, Bigtable"),
    ]
    for i, (n, ex) in enumerate(nosql):
        y = 124 + i * 36
        g.append(t(36, y, n, 11, True, "#7a3b12"))
        g.append(t(160, y, ex, 10, False, "#1a1a1a"))
    # Bloc B : DWH / lac / lakehouse
    g.append(r(400, 80, 360, 200, fond="#fdf7f4", bord="#7a3b12"))
    g.append(t(416, 100, "Stockage : DWH, lac, lakehouse", 12, True, "#7a3b12"))
    stockages = [
        ("Entrepot (DWH)", "donnees validees, analytique"),
        ("Lac (datalake)", "brut, tout, sans validation"),
        ("Lakehouse", "les deux : Delta / Iceberg"),
    ]
    for i, (n, ex) in enumerate(stockages):
        y = 124 + i * 50
        g.append(t(416, y, n, 11, True, "#7a3b12"))
        g.append(t(540, y, ex, 9, False, "#1a1a1a"))
    # Bloc C : 5 mots d'entretien
    g.append(r(20, 290, 740, 110, fond="#eef3f8", bord="#1f4e79"))
    g.append(t(36, 310, "Les 5 mots d'entretien (en moins de 60 mots chacun)", 12, True, "#1f4e79"))
    mots = [
        ("Sharding", "partition horizontale, irreversible, > 1 To"),
        ("Replication", "copie maitre/esclave, haute disponibilite"),
        ("CAP", "coherence + disponibilite + partition : 2 sur 3"),
        ("ACID vs BASE", "transactionnel strict vs distribue souple"),
        ("ETL vs ELT", "transfo hors/dans l'entrepot"),
    ]
    for i, (m, ex) in enumerate(mots):
        x = 36 + i * 145
        g.append(t(x, 334, m, 11, True, "#7a3b12"))
        # wrap si trop long (max ~22 car)
        mots_d = ex.split(",")
        for j, sub in enumerate(mots_d):
            g.append(t(x, 352 + j * 14, sub.strip(), 8, False, "#1a1a1a"))
    # Bandeau bas
    g.append(r(20, 410, 740, 50, fond="#f2f7f2", bord="#3f7d3f"))
    g.append(t(36, 432, "Verdict : NoSQL complete le relationnel, ne le remplace pas.", 11, True, "#3f7d3f"))
    g.append(t(36, 450, "80 % SQL / 20 % NoSQL : choisir NoSQL quand le relationnel est inadapte, pas par mode.", 10, False, "#1a1a1a"))
    return "".join(g) + "</svg>"


def audit(nom, svg):
    """Largeur estimée par ligne et jeu de signes.

    Mêmes seuils et même jeu autorisé que figures_M04.py et figures_M05.py : caractères accentués
    latin-1 (é, è, à, ê, etc.), flèche →, esperluette, ×, point médian, esperluette inversée.
    """
    autorises = set("é·èà—’«»→ê…×î←Éùç▼ô°\xa0§¹²³")
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
        "M06_C01_cinq_limites_classeur_excel.svg": planche_cinq_limites(),
        "M06_C02_anatomie_table.svg": planche_anatomie_table(),
        "M06_C03_trois_relations_cardinalite.svg": planche_trois_relations(),
        "M06_C04_trois_moteurs_ducksqlpg.svg": planche_trois_moteurs(),
        "M06_C05_carte_paysage_nosql.svg": planche_carte_paysage(),
    }
    for nom, contenu in planches.items():
        chemin = os.path.join(FIG, nom)
        open(chemin, "w", encoding="utf-8").write(contenu)
        print("figure →", nom, "(%.1f Ko)" % (os.path.getsize(chemin) / 1024))
        audit(nom, contenu)


if __name__ == "__main__":
    main()
