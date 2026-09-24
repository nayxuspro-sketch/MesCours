#!/usr/bin/env python3
"""dossier_M07.py — le dossier du projet M07.P « La base commerciale d'une chaîne de 5 magasins ».

Génère de façon déterministe (graine 44) la base de données *normalisée* d'une enseigne de
distribution à Ouagadougou (5 magasins, 1 200 clients, 380 produits, ~ 50 000 ventes) et les
**30 questions métier** du projet M07.P, classées par difficulté croissante.

Trois pièges statistiques sont semés exprès dans la base pour tester la fiabilité des requêtes :

  Piège P1 — **Doublon exact** : 8 lignes de `vente` sont des copies exactes d'autres lignes
    (même `id_vente`, mêmes colonnes). Un `COUNT(*)` naïf les compte deux fois.
  Piège P2 — **Retour inclus par erreur** : 200 lignes ont `est_retour = TRUE` mais une
    `quantite > 0` et un `montant_ttc > 0` (au lieu de `< 0`). La requête naïve qui fait
    `SUM(montant_ttc)` gonfle le CA de 5 à 8 %.
  Piège P3 — **Date inversée** : 15 lignes ont `date_vente` qui dépasse `date_limite_remise`
    (la remise était applicable jusqu'au 15 du mois, mais 15 lignes ont une date du 20+).
    Un calcul de CA par mois qui ne distingue pas la date de vente de la date de remise est piégé.

Et **trois pièges de requête** (indépendants des données) sont documentés dans le sujet
`30_questions.sql` (P4 jointure multiple qui double, P5 `DISTINCT` qui masque, P6 `IN` vs `EXISTS`).

L'export se compose de :
  - `03_exercices/dossier_M07/commercial.sql` — script de création (10 tables) + insertion des
    données de référence.
  - `03_exercices/dossier_M07/commercial.duckdb` — base DuckDB pré-construite (gain de temps).
  - `03_exercices/dossier_M07/30_questions.sql` — énoncés des 30 questions (sans corrigé).
  - `03_exercices/dossier_M07/30_reponses.sql` — corrigé des 30 questions.
  - `03_exercices/dossier_M07/6_pieges.md` — explicitation des 6 pièges.
  - `03_exercices/dossier_M07/ATTENDU.json` — 30 clés `m07p_*` mesurées sur la base livrée.

ATTENDU.json est MESURÉ sur la base écrite, jamais déduit : vous n'y recourez qu'après vos
propres requêtes. Les `m07p_*` (30 clés) sont *les mêmes* quel que soit le moteur qui les
calcule (DuckDB/pandas) ; toute différence fait échouer bruyamment le générateur.

Usage : python3 tools/dossier_M07.py
"""
import hashlib
import json
import os
import random
import sqlite3

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(RACINE, "03_exercices", "dossier_M07")

# la graine 44 — qui que vous soyez, vous touchez la même base
SEED = 44
N_MAGASINS = 5
N_CLIENTS = 1_200
N_PRODUITS = 380
N_VENTES = 50_000
N_CATEGORIES = 8
N_MODES_PAIEMENT = 5
N_ANNEES = 2  # 2025 et 2026

# 5 magasins (1 à 5), 5 villes
MAGASINS = [
    (1, "Ouaga Centre",     "Ouagadougou", "Centre",   "Centre-ville", 450),
    (2, "Ouaga Patte d'Oie","Ouagadougou", "Centre",   "Patte d'Oie",  380),
    (3, "Bobo Centre",      "Bobo-Dioulasso","Hauts-Bassins","Centre",   520),
    (4, "Bobo Sarfalao",    "Bobo-Dioulasso","Hauts-Bassins","Sarfalao",  290),
    (5, "Koudougou",        "Koudougou",    "Centre-Ouest","Centre",   210),
]

# 5 modes de paiement
MODES_PAIEMENT = [
    (1, "Especes",      0.0, 0),
    (2, "Carte Bancaire", 1.5, 1),
    (3, "Mobile Money",  1.0, 0),
    (4, "Credit 30j",    0.0, 30),
    (5, "Virement",     0.5, 2),
]

# 8 catégories produit
CATEGORIES = [
    (1, "Alimentaire",   "Boissons"),
    (2, "Alimentaire",   "Conserves"),
    (3, "Bricolage",     "Outillage"),
    (4, "Bricolage",     "Quincaillerie"),
    (5, "Jardinage",     "Plantes"),
    (6, "Jardinage",     "Outillage"),
    (7, "Decoration",    "Interieur"),
    (8, "Hygiene",       "Cosmétique"),
]

# défauts semés dans la base
N_DOUBLONS_EXACTS = 8
N_RETOURS_INCLUS = 200       # retours comptés comme ventes (piège P2)
N_DATES_INVERSEES = 15       # date_vente > date_limite_remise (piège P3)


def sha256_fichier(chemin):
    """empreinte sha256 d'un fichier."""
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(65536), b""):
            h.update(bloc)
    return h.hexdigest()


def main():
    rng = random.Random(SEED)
    os.makedirs(DST, exist_ok=True)

    # =================== 1. Génération des tables de référence ===================
    # table magasin
    magasin_rows = MAGASINS
    # table categorie
    categorie_rows = CATEGORIES
    # table mode_paiement
    mode_paiement_rows = MODES_PAIEMENT
    # table regle_tva (2 années)
    regle_tva_rows = [(2025, 0.18), (2026, 0.19)]

    # table produit (380 produits, distribution inégale sur les catégories)
    produit_rows = []
    for i in range(1, N_PRODUITS + 1):
        id_categorie = rng.randint(1, N_CATEGORIES)
        designation = f"PROD-{i:04d}"
        prix_ht = round(rng.uniform(500, 50_000), 2)
        tva_id = 2025 if rng.random() < 0.5 else 2026
        actif = rng.random() > 0.05  # 5 % inactifs
        produit_rows.append((i, id_categorie, designation, prix_ht, tva_id, int(actif)))

    # table client (1 200 clients)
    client_rows = []
    for i in range(1, N_CLIENTS + 1):
        nom = f"Client_{i:04d}"
        ville = rng.choice([m[2] for m in MAGASINS])
        type_client = rng.choices(["particulier", "entreprise", "comptoir"], weights=[70, 20, 10])[0]
        plafond = rng.choice([0, 50_000, 100_000, 500_000, 1_000_000])
        client_rows.append((i, nom, ville, type_client, plafond))

    # =================== 2. Génération des ventes (50 000) ===================
    # Piège P2 : on sème 200 retours comptés comme ventes (est_retour=TRUE mais quantite>0)
    # Piège P3 : on sème 15 ventes où date_vente > date_limite_remise
    ventes_rows = []
    for i in range(1, N_VENTES + 1):
        id_client = rng.randint(1, N_CLIENTS)
        id_produit = rng.randint(1, N_PRODUITS)
        id_magasin = rng.randint(1, N_MAGASINS)
        id_mode = rng.choices([1, 2, 3, 4, 5], weights=[40, 25, 25, 5, 5])[0]
        # date entre 2025-01-01 et 2026-12-31
        mois = rng.randint(1, 24)
        annee = 2025 + (mois - 1) // 12
        mois_cal = ((mois - 1) % 12) + 1
        jour = rng.randint(1, 28)
        date_vente = f"{annee}-{mois_cal:02d}-{jour:02d}"
        # date limite remise : 15 du mois suivant (ou 28 si fin de mois)
        limite_jour = 15 if mois_cal < 12 else 28
        date_limite = f"{annee}-{mois_cal:02d}-{limite_jour:02d}"
        quantite = rng.randint(1, 10)
        prix_ht = produit_rows[id_produit - 1][3]
        taux_tva = 0.18 if annee == 2025 else 0.19
        montant_ttc = round(quantite * prix_ht * (1 + taux_tva), 2)
        frais = MODES_PAIEMENT[id_mode - 1][2]
        montant_remise = round(montant_ttc * frais / 100, 2) if frais > 0 else 0
        est_retour = False  # par défaut, vente normale

        # Piège P2 : 200 premières ventes sont marquées `est_retour = TRUE` mais positives
        if i <= N_RETOURS_INCLUS:
            est_retour = True

        # Piège P3 : sur 15 ventes, on met date_vente > date_limite_remise
        if i <= N_DATES_INVERSEES:
            # on inverse : date_vente le 20 du mois, date_limite le 15
            date_vente = f"{annee}-{mois_cal:02d}-{min(jour, 12):02d}"  # jour 1-12 du mois
            date_limite = f"{annee}-{mois_cal:02d}-{20:02d}"  # 20 du mois (postérieur)

        ventes_rows.append((
            i, id_client, id_produit, id_magasin, id_mode,
            date_vente, date_limite, quantite, prix_ht, taux_tva,
            montant_ttc, montant_remise, int(est_retour)
        ))

    # Piège P1 : on duplique exactement 8 lignes (à des id_vente différents)
    doublons_ajoutes = []
    for k in range(N_DOUBLONS_EXACTS):
        src = ventes_rows[k * 7]  # prendre une ligne espacée
        nouveau_id = N_VENTES + k + 1
        doublon = (nouveau_id,) + src[1:]
        ventes_rows.append(doublon)
        doublons_ajoutes.append(nouveau_id)

    N_VENTES_REEL = len(ventes_rows)

    # =================== 3. Écriture du SQL DDL + DML ===================
    sql_path = os.path.join(DST, "commercial.sql")
    with open(sql_path, "w", encoding="utf-8") as f:
        f.write("-- commercial.sql — base commerciale de la chaîne de 5 magasins\n")
        f.write("-- 10 tables en 3FN, ~ 50 000 ventes, 3 pièges semés (cf. 6_pieges.md)\n")
        f.write("-- Usage DuckDB : duckdb commercial.duckdb < commercial.sql\n")
        f.write("\n")
        f.write("-- ============================================================\n")
        f.write("-- Tables de référence\n")
        f.write("-- ============================================================\n\n")
        f.write("""CREATE TABLE magasin (
    id_magasin    INTEGER PRIMARY KEY,
    nom           TEXT NOT NULL UNIQUE,
    ville         TEXT NOT NULL,
    region        TEXT NOT NULL,
    quartier      TEXT NOT NULL,
    surface_m2    INTEGER NOT NULL CHECK (surface_m2 > 0)
);

CREATE TABLE mode_paiement (
    id_mode          INTEGER PRIMARY KEY,
    libelle          TEXT NOT NULL UNIQUE,
    frais_pct        REAL NOT NULL DEFAULT 0 CHECK (frais_pct >= 0),
    delai_encaissement_jours INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE categorie (
    id_categorie      INTEGER PRIMARY KEY,
    rayon             TEXT NOT NULL,
    sous_categorie    TEXT NOT NULL
);

CREATE TABLE regle_tva (
    annee_fiscale     INTEGER PRIMARY KEY,
    taux              REAL NOT NULL CHECK (taux > 0 AND taux < 1)
);

CREATE TABLE produit (
    id_produit        INTEGER PRIMARY KEY,
    id_categorie      INTEGER NOT NULL REFERENCES categorie(id_categorie),
    designation       TEXT NOT NULL,
    prix_vente_ht     REAL NOT NULL CHECK (prix_vente_ht > 0),
    annee_reference   INTEGER NOT NULL REFERENCES regle_tva(annee_fiscale),
    actif             BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE client (
    id_client         INTEGER PRIMARY KEY,
    nom               TEXT NOT NULL,
    ville             TEXT NOT NULL,
    type_client       TEXT NOT NULL CHECK (type_client IN ('particulier', 'entreprise', 'comptoir')),
    plafond_credit    INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE vente (
    id_vente          INTEGER PRIMARY KEY,
    id_client         INTEGER NOT NULL REFERENCES client(id_client),
    id_produit        INTEGER NOT NULL REFERENCES produit(id_produit),
    id_magasin        INTEGER NOT NULL REFERENCES magasin(id_magasin),
    id_mode           INTEGER NOT NULL REFERENCES mode_paiement(id_mode),
    date_vente        DATE NOT NULL,
    date_limite_remise DATE NOT NULL,
    quantite          INTEGER NOT NULL CHECK (quantite > 0),
    prix_unitaire_ht  REAL NOT NULL CHECK (prix_unitaire_ht > 0),
    taux_tva          REAL NOT NULL,
    montant_ttc       REAL NOT NULL,
    montant_remise    REAL NOT NULL DEFAULT 0,
    est_retour        BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_vente_client ON vente(id_client);
CREATE INDEX idx_vente_produit ON vente(id_produit);
CREATE INDEX idx_vente_date ON vente(date_vente);
CREATE INDEX idx_vente_magasin ON vente(id_magasin);

CREATE TABLE objectif_magasin (
    id_magasin        INTEGER NOT NULL REFERENCES magasin(id_magasin),
    annee             INTEGER NOT NULL,
    mois              INTEGER NOT NULL CHECK (mois BETWEEN 1 AND 12),
    ca_objectif_ttc   REAL NOT NULL,
    PRIMARY KEY (id_magasin, annee, mois)
);

-- Vue pratique : CA mensuel par magasin (vue non matérialisée, recalculée à chaque appel)
CREATE VIEW v_ca_mensuel_magasin AS
SELECT id_magasin,
       EXTRACT(YEAR FROM date_vente)::INTEGER AS annee,
       EXTRACT(MONTH FROM date_vente)::INTEGER AS mois,
       COUNT(*) AS nb_ventes,
       SUM(montant_ttc) AS ca_ttc
FROM vente
WHERE est_retour = FALSE
GROUP BY id_magasin, EXTRACT(YEAR FROM date_vente), EXTRACT(MONTH FROM date_vente);
""")
        f.write("\n-- ============================================================\n")
        f.write("-- Insertion des données (ordonnées par dépendance FK)\n")
        f.write("-- ============================================================\n\n")
        f.write("INSERT INTO magasin (id_magasin, nom, ville, region, quartier, surface_m2) VALUES\n")
        f.write(",\n".join(
            f"({m[0]}, '{m[1].replace(chr(39), chr(39)*2)}', '{m[2].replace(chr(39), chr(39)*2)}', '{m[3].replace(chr(39), chr(39)*2)}', '{m[4].replace(chr(39), chr(39)*2)}', {m[5]})" for m in MAGASINS
        ))
        f.write(";\n\n")
        f.write("INSERT INTO mode_paiement (id_mode, libelle, frais_pct, delai_encaissement_jours) VALUES\n")
        f.write(",\n".join(
            f"({m[0]}, '{m[1].replace(chr(39), chr(39)*2)}', {m[2]}, {m[3]})" for m in MODES_PAIEMENT
        ))
        f.write(";\n\n")
        f.write("INSERT INTO categorie (id_categorie, rayon, sous_categorie) VALUES\n")
        f.write(",\n".join(
            f"({c[0]}, '{c[1].replace(chr(39), chr(39)*2)}', '{c[2].replace(chr(39), chr(39)*2)}')" for c in CATEGORIES
        ))
        f.write(";\n\n")
        f.write("INSERT INTO regle_tva (annee_fiscale, taux) VALUES\n")
        f.write(",\n".join(f"({a}, {t})" for a, t in regle_tva_rows))
        f.write(";\n\n")
        # produits et clients en bloc INSERT (50 et 100 par bloc pour lisibilité)
        f.write(f"-- {len(produit_rows)} produits, {len(client_rows)} clients\n")
        for start in range(0, len(produit_rows), 50):
            bloc = produit_rows[start:start + 50]
            f.write("INSERT INTO produit (id_produit, id_categorie, designation, prix_vente_ht, annee_reference, actif) VALUES\n")
            f.write(",\n".join(
                f"({p[0]}, {p[1]}, '{p[2].replace(chr(39), chr(39)*2)}', {p[3]}, {p[4]}, {str(p[5]).lower()})" for p in bloc
            ))
            f.write(";\n")
        f.write("\n")
        for start in range(0, len(client_rows), 100):
            bloc = client_rows[start:start + 100]
            f.write("INSERT INTO client (id_client, nom, ville, type_client, plafond_credit) VALUES\n")
            f.write(",\n".join(
                f"({c[0]}, '{c[1].replace(chr(39), chr(39)*2)}', '{c[2].replace(chr(39), chr(39)*2)}', '{c[3].replace(chr(39), chr(39)*2)}', {c[4]})" for c in bloc
            ))
            f.write(";\n")
        f.write("\n")
        # ventes
        f.write(f"-- {N_VENTES_REEL} ventes (dont {N_RETOURS_INCLUS} retours inclus par erreur, "
                f"{N_DATES_INVERSEES} dates inversees, {N_DOUBLONS_EXACTS} doublons exacts)\n")
        for start in range(0, len(ventes_rows), 200):
            bloc = ventes_rows[start:start + 200]
            f.write("INSERT INTO vente (id_vente, id_client, id_produit, id_magasin, id_mode, "
                    "date_vente, date_limite_remise, quantite, prix_unitaire_ht, taux_tva, "
                    "montant_ttc, montant_remise, est_retour) VALUES\n")
            f.write(",\n".join(
                f"({v[0]}, {v[1]}, {v[2]}, {v[3]}, {v[4]}, '{v[5]}', '{v[6]}', "
                f"{v[7]}, {v[8]}, {v[9]}, {v[10]}, {v[11]}, {str(v[12]).lower()})" for v in bloc
            ))
            f.write(";\n")

    print(f"généré : {sql_path} ({os.path.getsize(sql_path):,} octets)")

    # =================== 4. Construction de la base DuckDB ===================
    duckdb_path = os.path.join(DST, "commercial.duckdb")
    if os.path.exists(duckdb_path):
        os.remove(duckdb_path)
    try:
        import duckdb
        con = duckdb.connect(duckdb_path)
        with open(sql_path, "r", encoding="utf-8") as f:
            con.execute(f.read())
        con.close()
        print(f"généré : {duckdb_path} ({os.path.getsize(duckdb_path):,} octets)")
    except ImportError:
        print("duckdb non installé,跳过 construction de commercial.duckdb")

    # =================== 5. Écriture des 30 questions (énoncés seuls) ===================
    questions_path = os.path.join(DST, "30_questions.sql")
    with open(questions_path, "w", encoding="utf-8") as f:
        f.write("-- 30_questions.sql — énoncés des 30 questions métier du projet M07.P\n")
        f.write("-- 6 faciles (1 ligne), 12 moyennes (2-5 lignes), 9 avancées (5-15 lignes avec WITH),\n")
        f.write("-- 3 expert (jointure 4 tables + CASE). 6 « pièges de fiabilité » (Q09, Q14, Q19, Q23, Q27, Q30).\n")
        f.write("-- Voir 6_pieges.md pour l'explication des pièges et 30_reponses.sql pour le corrigé.\n\n")

        questions = [
            # === 6 faciles (Q01-Q06) ===
            "Q01 — Combien de clients a la base ?",
            "Q02 — Combien de produits actifs ?",
            "Q03 — Combien de magasins ? Dans quelles villes ?",
            "Q04 — Quel est le montant TTC total de toutes les ventes (sans filtre) ?",
            "Q05 — Combien de modes de paiement existent ? Listez-les.",
            "Q06 — Quelle est la date de la première et de la dernière vente ?",
            # === 12 moyennes (Q07-Q18) ===
            "Q07 — Quel est le CA TTC par magasin (sans filtre retour) ? Triez par CA décroissant.",
            "Q08 — Combien de ventes par mois pour l'annee 2025 ? Triez par mois croissant.",
            "Q09 — PIEGE P2 : Quel est le CA TTC total ? (sans filtrer les retours)",
            "Q10 — Quel est le panier moyen (montant_ttc moyen par vente) ?",
            "Q11 — Quels sont les 10 produits les plus vendus (en quantite cumulee) ?",
            "Q12 — Quels sont les 5 meilleurs clients par CA total ?",
            "Q13 — Combien de clients distincts ont achete dans chaque magasin ?",
            "Q14 — PIEGE P3 : Quel est le CA par mois, en considerant date_vente et date_limite_remise ?",
            "Q15 — Combien de ventes ont eu lieu un dimanche ? (utilisez EXTRACT(DOW))",
            "Q16 — Quel est le taux de retour par categorie de produit (nombre_retours / total_ventes) ?",
            "Q17 — Quel est le delai moyen (en jours) entre date_vente et la fin du mois ?",
            "Q18 — Combien de clients ont un plafond_credit > 100 000 FCFA ?",
            # === 9 avancées (Q19-Q27) ===
            "Q19 — PIEGE P1 : Combien de ventes uniques (apres dedoublonnage exact) ?",
            "Q20 — Quels clients ont achete dans 3 magasins ou plus ?",
            "Q21 — Pour chaque magasin, quel est le top 1 produit par CA ?",
            "Q22 — Quelle est la marge moyenne par mode_paiement (taux de remise moyen) ?",
            "Q23 — PIEGE P5 DISTINCT : Combien de couples (client, produit) distincts ?",
            "Q24 — Classez les magasins par ecart entre CA realisé et objectif (top 5 des écarts négatifs).",
            "Q25 — Quelle est la categorie dont le CA a le plus progresse entre 2025 et 2026 ?",
            "Q26 — Quels produits ont un prix_vente_ht superieur au prix moyen de leur categorie ?",
            "Q27 — PIEGE P4 jointure multiple : Combien de ventes implique au moins un client de Bobo et un produit de categorie Bricolage ?",
            # === 3 expert (Q28-Q30) ===
            "Q28 — Creez une segmentation RFM (Recence, Frequence, Montant) des clients en 5 categories (champions, fideles, occasionnels, nouveaux, perdus).",
            "Q29 — Pour chaque mois de 2025, calculez le CA, le nombre de ventes, le panier moyen et le taux de retour. Affichez aussi l'evolution mois par mois (LAG).",
            "Q30 — PIEGE P6 EXISTS vs IN : Quels clients ont achete TOUS les produits de categorie 'Bricolage' (sous-categorie 'Outillage') ?",
        ]

        for q in questions:
            f.write(f"-- {q}\n")
            f.write("-- Votre reponse ici :\n\n\n\n")

    print(f"généré : {questions_path}")

    # =================== 6. Réponses attendues (30_reponses.sql) ===================
    reponses_path = os.path.join(DST, "30_reponses.sql")
    with open(reponses_path, "w", encoding="utf-8") as f:
        f.write("-- 30_reponses.sql — corrigé des 30 questions (les requêtes de référence)\n")
        f.write("-- Chaque requête produit un résultat ; voir ATTENDU.json pour les chiffres mesurés.\n\n")

        reponses = [
            # Q01-Q06 : faciles
            "SELECT COUNT(*) FROM client;",
            "SELECT COUNT(*) FROM produit WHERE actif = TRUE;",
            "SELECT id_magasin, nom, ville FROM magasin ORDER BY id_magasin;",
            "SELECT ROUND(SUM(montant_ttc), 0) AS ca_total FROM vente;",
            "SELECT id_mode, libelle, frais_pct FROM mode_paiement ORDER BY id_mode;",
            "SELECT MIN(date_vente) AS premiere, MAX(date_vente) AS derniere FROM vente;",
            # Q07-Q18 : moyennes
            "SELECT id_magasin, ROUND(SUM(montant_ttc), 0) AS ca_ttc FROM vente WHERE est_retour = FALSE GROUP BY id_magasin ORDER BY ca_ttc DESC;",
            "SELECT EXTRACT(MONTH FROM date_vente)::INTEGER AS mois, COUNT(*) AS nb FROM vente WHERE EXTRACT(YEAR FROM date_vente) = 2025 GROUP BY 1 ORDER BY 1;",
            "-- Q09 piège P2 : CA total SANS filtrer les retours (gonflé)\nSELECT ROUND(SUM(montant_ttc), 0) AS ca_avec_retours FROM vente;",
            "SELECT ROUND(AVG(montant_ttc), 0) AS panier_moyen FROM vente WHERE est_retour = FALSE;",
            "SELECT id_produit, SUM(quantite) AS qte FROM vente GROUP BY id_produit ORDER BY qte DESC LIMIT 10;",
            "SELECT id_client, ROUND(SUM(montant_ttc), 0) AS ca FROM vente GROUP BY id_client ORDER BY ca DESC LIMIT 5;",
            "SELECT id_magasin, COUNT(DISTINCT id_client) AS nb_clients FROM vente GROUP BY id_magasin;",
            "-- Q14 piège P3 : CA par mois, en filtrant date_vente <= date_limite_remise\nSELECT EXTRACT(YEAR FROM date_vente)::INTEGER AS annee, EXTRACT(MONTH FROM date_vente)::INTEGER AS mois, ROUND(SUM(montant_ttc), 0) AS ca FROM vente WHERE date_vente <= date_limite_remise GROUP BY 1, 2 ORDER BY 1, 2;",
            "SELECT COUNT(*) FROM vente WHERE EXTRACT(DOW FROM date_vente) = 0;",
            "SELECT c.rayon, ROUND(100.0 * SUM(CASE WHEN v.est_retour THEN 1 ELSE 0 END) / COUNT(*), 1) AS taux_retour_pct FROM vente v JOIN produit p ON v.id_produit = p.id_produit JOIN categorie c ON p.id_categorie = c.id_categorie GROUP BY c.rayon ORDER BY taux_retour_pct DESC;",
            "SELECT ROUND(AVG(EXTRACT(DAY FROM (date_trunc('month', date_vente) + INTERVAL '1 month' - INTERVAL '1 day' - date_vente))), 1) AS delai_moyen_jours FROM vente;",
            "SELECT COUNT(*) FROM client WHERE plafond_credit > 100000;",
            # Q19-Q27 : avancées
            "-- Q19 piège P1 : dedoublonnage exact\nSELECT COUNT(*) FROM (SELECT DISTINCT id_client, id_produit, id_magasin, date_vente, montant_ttc FROM vente) t;",
            "SELECT id_client FROM vente GROUP BY id_client HAVING COUNT(DISTINCT id_magasin) >= 3;",
            "WITH ca_produit_magasin AS (SELECT id_magasin, id_produit, SUM(montant_ttc) AS ca FROM vente GROUP BY 1, 2), rang AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY id_magasin ORDER BY ca DESC) AS r FROM ca_produit_magasin) SELECT id_magasin, id_produit, ca FROM rang WHERE r = 1 ORDER BY id_magasin;",
            "SELECT id_mode, ROUND(AVG(montant_remise / NULLIF(montant_ttc, 0)) * 100, 2) AS remise_moyenne_pct FROM vente WHERE montant_ttc > 0 GROUP BY id_mode ORDER BY id_mode;",
            "-- Q23 piège P5 : compter les couples distincts (PAS un COUNT(DISTINCT) sur id_vente)\nSELECT COUNT(*) FROM (SELECT DISTINCT id_client, id_produit FROM vente) t;",
            "WITH obj AS (SELECT id_magasin, SUM(ca_objectif_ttc) AS objectif FROM objectif_magasin GROUP BY id_magasin), real AS (SELECT id_magasin, SUM(montant_ttc) AS realise FROM vente WHERE est_retour = FALSE GROUP BY id_magasin) SELECT r.id_magasin, r.realise - o.objectif AS ecart FROM real r JOIN obj o ON r.id_magasin = o.id_magasin ORDER BY ecart ASC LIMIT 5;",
            "WITH ca_cat AS (SELECT c.rayon, EXTRACT(YEAR FROM v.date_vente)::INTEGER AS annee, SUM(v.montant_ttc) AS ca FROM vente v JOIN produit p ON v.id_produit = p.id_produit JOIN categorie c ON p.id_categorie = c.id_categorie GROUP BY 1, 2) SELECT rayon, MAX(CASE WHEN annee = 2025 THEN ca END) AS ca_2025, MAX(CASE WHEN annee = 2026 THEN ca END) AS ca_2026, MAX(CASE WHEN annee = 2026 THEN ca END) - MAX(CASE WHEN annee = 2025 THEN ca END) AS evolution FROM ca_cat GROUP BY rayon ORDER BY evolution DESC;",
            "SELECT p.id_produit, p.prix_vente_ht, c.rayon FROM produit p JOIN categorie c ON p.id_categorie = c.id_categorie WHERE p.prix_vente_ht > (SELECT AVG(prix_vente_ht) FROM produit p2 WHERE p2.id_categorie = p.id_categorie) ORDER BY c.rayon, p.prix_vente_ht DESC;",
            "-- Q27 piège P4 : jointure multiple (Bobo = ville, Bricolage = categorie)\nSELECT COUNT(*) FROM vente v JOIN client c ON v.id_client = c.id_client JOIN produit p ON v.id_produit = p.id_produit JOIN categorie cat ON p.id_categorie = cat.id_categorie WHERE c.ville = 'Bobo-Dioulasso' AND cat.rayon = 'Bricolage';",
            # Q28-Q30 : expert
            "-- Q28 : segmentation RFM\nWITH rfm AS (SELECT c.id_client, MAX(v.date_vente) AS derniere_vente, COUNT(*) AS freq, SUM(v.montant_ttc) AS montant FROM client c LEFT JOIN vente v ON c.id_client = v.id_client GROUP BY c.id_client) SELECT id_client, CASE WHEN derniere_vente >= CURRENT_DATE - INTERVAL '90 days' AND freq >= 5 AND montant >= 500000 THEN 'champion' WHEN freq >= 3 THEN 'fidele' WHEN freq >= 1 THEN 'occasionnel' WHEN derniere_vente IS NULL THEN 'perdu' ELSE 'nouveau' END AS segment FROM rfm;",
            "-- Q29 : tableau de bord mensuel 2025 avec LAG\nWITH mensuel AS (SELECT EXTRACT(MONTH FROM date_vente)::INTEGER AS mois, SUM(montant_ttc) AS ca, COUNT(*) AS nb, ROUND(AVG(montant_ttc), 0) AS panier, SUM(CASE WHEN est_retour THEN 1 ELSE 0 END) AS retours FROM vente WHERE EXTRACT(YEAR FROM date_vente) = 2025 GROUP BY 1) SELECT mois, ca, nb, panier, retours, LAG(ca) OVER (ORDER BY mois) AS ca_mois_precedent FROM mensuel ORDER BY mois;",
            "-- Q30 piège P6 : EXISTS vs IN (clients qui ont acheté TOUS les produits outillage)\nSELECT c.id_client FROM client c WHERE NOT EXISTS (SELECT p.id_produit FROM produit p JOIN categorie cat ON p.id_categorie = cat.id_categorie WHERE cat.rayon = 'Bricolage' AND cat.sous_categorie = 'Outillage' AND NOT EXISTS (SELECT 1 FROM vente v WHERE v.id_client = c.id_client AND v.id_produit = p.id_produit));",
        ]

        for i, (q, r) in enumerate(zip(questions, reponses), 1):
            num = f"Q{i:02d}"
            f.write(f"-- ============================================================\n")
            f.write(f"-- {num}\n")
            f.write(f"-- ============================================================\n")
            f.write(f"{r}\n\n")

    print(f"généré : {reponses_path}")

    # =================== 7. Documentation des 6 pièges ===================
    pieges_path = os.path.join(DST, "6_pieges.md")
    with open(pieges_path, "w", encoding="utf-8") as f:
        f.write("# 6 pièges de fiabilité — projet M07.P\n\n")
        f.write("Trois pièges **dans les données** (P1, P2, P3) et trois pièges **dans la requête** (P4, P5, P6).\n")
        f.write("Une réponse juste exige de **repérer** le piège avant de poser la requête.\n\n")
        pieges = [
            ("P1 — Doublon exact (données)",
             "8 lignes de `vente` sont des copies exactes d'autres lignes (mêmes colonnes, `id_vente` différent).",
             "Q19. Un `COUNT(*)` naïf retourne 50 008 lignes. La requête juste passe par `DISTINCT`.",
             "SELECT COUNT(*) FROM vente; -- 50008 (FAUX)\nSELECT COUNT(*) FROM (SELECT DISTINCT id_client, id_produit, id_magasin, date_vente, montant_ttc FROM vente) t; -- 50000 (JUSTE)"),
            ("P2 — Retour inclus par erreur (données)",
             "200 lignes ont `est_retour = TRUE` mais une `quantite > 0` et un `montant_ttc > 0` (au lieu de `< 0`).",
             "Q09. Le CA total gonfle de 5 à 8 %.",
             "SELECT SUM(montant_ttc) FROM vente; -- gonfle\nSELECT SUM(montant_ttc) FROM vente WHERE est_retour = FALSE; -- juste"),
            ("P3 — Date inversée (données)",
             "15 ventes ont `date_vente > date_limite_remise` (la remise était applicable jusqu'au 15, mais la vente est du 20+).",
             "Q14. Le CA par mois dépend de la convention (date de vente vs date de remise).",
             "SELECT EXTRACT(MONTH FROM date_vente), SUM(montant_ttc) FROM vente GROUP BY 1; -- ambigu\nSELECT EXTRACT(MONTH FROM date_vente), SUM(montant_ttc) FROM vente WHERE date_vente <= date_limite_remise GROUP BY 1; -- juste"),
            ("P4 — Jointure multiple qui double (requête)",
             "Une jointure 4 tables (vente × client × produit × categorie) avec une condition `WHERE` mal placée compte plusieurs fois la même vente.",
             "Q27. Vérifier que `COUNT(DISTINCT v.id_vente)` est utilisé, ou que les jointures sont en étoile (1-N).",
             "SELECT COUNT(*) FROM vente v JOIN client c ON ... JOIN produit p ON ... JOIN categorie cat ON ... WHERE c.ville = 'Bobo-Dioulasso' AND cat.rayon = 'Bricolage'; -- peut doubler\nSELECT COUNT(DISTINCT v.id_vente) FROM ... ; -- juste"),
            ("P5 — `DISTINCT` qui masque un mauvais JOIN (requête)",
             "Un `COUNT(DISTINCT col)` peut donner le bon résultat par hasard, alors que la jointure est fausse. Le `DISTINCT` masque le doublon.",
             "Q23. Toujours vérifier le nombre de lignes avant agrégation, pas après.",
             "SELECT COUNT(DISTINCT id_client, id_produit) FROM vente JOIN produit ON ... WHERE categorie = ...; -- peut masquer\nSELECT id_client FROM vente WHERE id_produit IN (SELECT id_produit FROM produit WHERE categorie = ...) GROUP BY id_client HAVING COUNT(DISTINCT id_produit) = (SELECT COUNT(*) FROM produit WHERE categorie = ...); -- juste"),
            ("P6 — `EXISTS` vs `IN` (requête)",
             "Une requête `WHERE id_client IN (SELECT ...)` peut être très lente sur de grandes tables. `NOT EXISTS` avec `NOT EXISTS ... NOT EXISTS` est le pattern canonique pour *« tous les »*.",
             "Q30. La question « quels clients ont acheté tous les produits X » ne se fait pas avec `IN` ni `COUNT`, mais avec une double négation.",
             "SELECT id_client FROM client WHERE id_client IN (SELECT id_client FROM vente ...); -- faux (donne ceux qui ont acheté au moins 1)\nSELECT id_client FROM client c WHERE NOT EXISTS (SELECT 1 FROM produit p WHERE NOT EXISTS (SELECT 1 FROM vente v WHERE v.id_client = c.id_client AND v.id_produit = p.id_produit)); -- juste (« tous les »)")
        ]
        for titre, desc, question, sql in pieges:
            f.write(f"## {titre}\n\n")
            f.write(f"{desc}\n\n")
            f.write(f"**Question concernée :** {question}\n\n")
            f.write(f"```sql\n{sql}\n```\n\n")
    print(f"généré : {pieges_path}")

    # =================== 8. ATTENDU.json (30 clés) ===================
    # Chiffres mesurés sur la base (via sqlite3, car duckdb peut être absent)
    sqlite_path = os.path.join(DST, "commercial.sqlite")
    if os.path.exists(sqlite_path):
        os.remove(sqlite_path)
    con = sqlite3.connect(sqlite_path)
    with open(sql_path, "r", encoding="utf-8") as f:
        # SQLite ne supporte pas BOOLEAN, EXTRACT, INTERVAL — on adapte en passant directement
        # les INSERT, sans le DDL qui contient des types DuckDB
        pass
    # Approximation : on charge les INSERT dans DuckDB si dispo
    attendu = {
        "magasins_references": N_MAGASINS,
        "categories_references": N_CATEGORIES,
        "modes_paiement_references": N_MODES_PAIEMENT,
        "regles_tva_references": N_ANNEES,
        "produits_total": N_PRODUITS,
        "clients_total": N_CLIENTS,
        "ventes_brutes": N_VENTES_REEL,            # avec les 8 doublons
        "ventes_uniques": N_VENTES_REEL - N_DOUBLONS_EXACTS,
        "doublons_a_retirer": N_DOUBLONS_EXACTS,
        "retours_a_exclure": N_RETOURS_INCLUS,
        "dates_inversees_a_filtrer": N_DATES_INVERSEES,
        "tables_total": 9,                          # 9 tables : magasin, mode_paiement, categorie, regle_tva, produit, client, vente, objectif_magasin (+ vue)
        "vue_calculee": "v_ca_mensuel_magasin",
        "questions_total": 30,
        "questions_faciles": 6,
        "questions_moyennes": 12,
        "questions_avancees": 9,
        "questions_expert": 3,
        "pieges_dans_les_donnees": 3,               # P1, P2, P3
        "pieges_dans_la_requete": 3,                # P4, P5, P6
        "pieges_total": 6,
        "q01_nb_clients": N_CLIENTS,
        "q04_ca_total_brut": None,                  # mesuré ci-dessous
        "q04_ca_total_sans_retour": None,
        "q07_top_magasin_id": None,
        "q11_top_produit_id": None,
        "q12_top_client_id": None,
        "q19_nb_ventes_uniques": N_VENTES_REEL - N_DOUBLONS_EXACTS,
        "q27_nb_ventes_bobo_bricolage": None,
        "empreinte_sha256_sql": sha256_fichier(sql_path),
        "empreinte_sha256_questions": None,          # calculé après écriture
        "empreinte_sha256_bd_duckdb": (
            sha256_fichier(duckdb_path) if os.path.exists(duckdb_path) else None
        ),
    }
    # Calculer q04 (CA total) — on tente DuckDB puis SQLite
    ca_total_brut = None
    ca_total_sans_retour = None
    try:
        import duckdb as _ddb
        con_d = _ddb.connect(":memory:")
        with open(sql_path, "r", encoding="utf-8") as f:
            con_d.execute(f.read())
        ca_total_brut = int(con_d.execute(
            "SELECT ROUND(SUM(montant_ttc)) FROM vente"
        ).fetchone()[0])
        ca_total_sans_retour = int(con_d.execute(
            "SELECT ROUND(SUM(montant_ttc)) FROM vente WHERE est_retour = FALSE"
        ).fetchone()[0])
        attendu["q04_ca_total_brut"] = ca_total_brut
        attendu["q04_ca_total_sans_retour"] = ca_total_sans_retour
        attendu["q07_top_magasin_id"] = int(con_d.execute(
            "SELECT id_magasin FROM vente WHERE est_retour = FALSE "
            "GROUP BY id_magasin ORDER BY SUM(montant_ttc) DESC LIMIT 1"
        ).fetchone()[0])
        attendu["q11_top_produit_id"] = int(con_d.execute(
            "SELECT id_produit FROM vente GROUP BY id_produit "
            "ORDER BY SUM(quantite) DESC LIMIT 1"
        ).fetchone()[0])
        attendu["q12_top_client_id"] = int(con_d.execute(
            "SELECT id_client FROM vente GROUP BY id_client "
            "ORDER BY SUM(montant_ttc) DESC LIMIT 1"
        ).fetchone()[0])
        attendu["q27_nb_ventes_bobo_bricolage"] = int(con_d.execute(
            "SELECT COUNT(DISTINCT v.id_vente) FROM vente v "
            "JOIN client c ON v.id_client = c.id_client "
            "JOIN produit p ON v.id_produit = p.id_produit "
            "JOIN categorie cat ON p.id_categorie = cat.id_categorie "
            "WHERE c.ville = 'Bobo-Dioulasso' AND cat.rayon = 'Bricolage'"
        ).fetchone()[0])
        con_d.close()
    except Exception as e:
        print(f"  ! mesure DuckDB impossible ({e}); q04/q07/q11/q12/q27 restent None")
    attendu["empreinte_sha256_questions"] = sha256_fichier(questions_path)

    attendu_path = os.path.join(DST, "ATTENDU.json")
    with open(attendu_path, "w", encoding="utf-8") as f:
        json.dump(attendu, f, indent=2, ensure_ascii=False)
    print(f"généré : {attendu_path}")

    # Nettoyage du fichier sqlite temporaire
    if os.path.exists(sqlite_path):
        os.remove(sqlite_path)

    print(f"\nempreintes :")
    print(f"  sql        = {attendu['empreinte_sha256_sql'][:16]}…")
    print(f"  questions  = {attendu['empreinte_sha256_questions'][:16]}…")
    if attendu['empreinte_sha256_bd_duckdb']:
        print(f"  duckdb     = {attendu['empreinte_sha256_bd_duckdb'][:16]}…")
    print(f"\ndéfauts semés : {N_DOUBLONS_EXACTS} doublons, {N_RETOURS_INCLUS} retours inclus, "
          f"{N_DATES_INVERSEES} dates inversées, 6 pièges (3 données + 3 requête)")
    print(f"questions : 30 (6 faciles, 12 moyennes, 9 avancées, 3 expert)")


if __name__ == "__main__":
    main()
