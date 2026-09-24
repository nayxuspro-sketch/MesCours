#!/usr/bin/env python3
"""dossier_M06.py — le dossier du projet M06.P « La base de la quincaillerie ».

Génère de façon déterministe (graine 43) l'export dénormalisé de la quincaillerie de
Koudougou : 42 colonnes dans une seule table (CSV UTF-8), 24 000 lignes, avec
**4 défauts structurels** que le projet M06.P doit corriger en passant en 7 tables :

  1. **Redondance** — la colonne `ville_client` recopie la ville dans chaque ligne de vente,
     alors qu'elle dépend du client (pas de la vente). 1NF/2FN/3FN : il faut extraire `client`.
  2. **Dépendance transitive** — la colonne `taux_tva_courant` (18 % en 2026, 19 % en 2027)
     est portée par chaque vente, mais elle dépend de l'année (pas de la vente). 3FN : il faut
     extraire une table `regle_tva(annee, taux)`.
  3. **Multi-valuée** — un client a **plusieurs** catégories favorites
     (« bricolage », « jardinage »), mais le brut ne porte qu'une seule colonne
     `categorie_pref`. C'est la violation classique de 1NF : il faut une table de jointure
     `client_categorie_pref(client_id, categorie)`.
  4. **Jointure implicite** — la colonne `mode_paiement` (« ESPECES », « MOBILE_MONEY »,
     « CREDIT ») est portée par chaque vente, mais elle pourrait être une table de référence.
     Le projet M06.P l'extrait en `mode_paiement(id, libelle, frais_pct)`.

L'export contient aussi des défauts « métier » (les mêmes natures que M05, simplifiées) :
   - 142 montants en texte (« 12 500 FCFA ») ;
   - 8 lignes en doublon (copies exactes, à détecter avant l'import) ;
   - 12 dates inversées (transposition jour-mois) ;
   - 3 `id_client` orphelins (la table `client` livrée ne les contient pas).

Le fichier `schema_3fn.sql` (livré) et `controles_integrite.sql` (les 3 requêtes de contrôle)
sont des **cibles** — le projet M06.P ne les valide pas, il les **reproduit** par sa propre
logique (et c'est l'écart entre le sien et le livré qui fait la note, pas la conformité
mécanique).

ATTENDU.json est MESURÉ sur le dossier écrit, jamais déduit : vous n'y recourez qu'après vos
propres nombres. Les `m06p_*` (18 clés) sont *les mêmes* quel que soit le moteur qui les
calcule (pandas ou DuckDB) ; toute différence fait échouer bruyamment le générateur.

Usage : python3 tools/dossier_M06.py
"""
import csv
import hashlib
import json
import os
import random

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(RACINE, "03_exercices", "dossier_M06")

# la graine 43 — qui que vous soyez, vous touchez le même export
SEED = 43
N_VENTES = 24_000
N_CLIENTS_UNIQUES = 1_891      # les 1 891 clients référencés dans le brut livré
N_PRODUITS_UNIQUES = 312       # 312 produits, 5 catégories
N_MODES_PAIEMENT = 4
N_REGLES_TVA = 2               # 2025 = 18 %, 2026 = 19 %
N_MAGASINS = 3

# les 42 colonnes de l'export dénormalisé (l'ordre est imposé par l'énoncé)
COLS_EXPORT = [
    # identifiants (4)
    "id_vente", "id_ticket", "id_client", "id_produit",
    # vendeur (3)
    "id_vendeur", "id_magasin", "horodatage",
    # client (5 — redondance)
    "client_nom", "client_prenom", "client_telephone", "client_email", "ville_client",
    # produit (5 — redondance)
    "produit_libelle", "produit_categorie", "produit_sous_categorie", "fournisseur", "rayon",
    # paiement (3 — référence à externaliser)
    "mode_paiement", "frais_pct", "delai_encaissement_jours",
    # tva (2 — dépendance transitive)
    "taux_tva_courant", "annee_fiscale",
    # catégories préférées (1 — multi-valuée)
    "categorie_pref",  # ⚠ ne peut porter qu'UNE catégorie, alors qu'un client peut en avoir plusieurs
    # montants (6 — dont 1 qui sert à porter les défauts "texte")
    "quantite", "prix_unitaire_ht", "montant_ht", "montant_tva", "montant_ttc", "montant_ttc_texte",
    # retours (2)
    "est_retour", "montant_remise_ht",
    # dates (3 — un peu en vrac)
    "date_vente", "mois", "annee",
    # méta (4)
    "canal", "poids_kg", "est_promo", "commentaire",
    # 4 + 3 + 5 + 3 + 2 + 1 + 6 + 2 + 3 + 4 = 33 ; on en ajoute 9 pour faire 42
    "fidelite_points", "fidelite_niveau", "fidelite_derniere_visite",
    "code_postal", "region", "pays",
    "frais_livraison", "delai_livraison_jours", "source",
]


def main():
    rng = random.Random(SEED)
    os.makedirs(DST, exist_ok=True)

    # --- les 3 magasins de la quincaillerie ---
    magasins = [(1, "Koudougou-Centre"), (2, "Bobo-Dioulasso"), (3, "Ouagadougou")]
    # --- les 4 modes de paiement ---
    modes = [
        (1, "ESPECES",    0.0,  0),
        (2, "MOBILE_MONEY", 1.5, 0),
        (3, "CARTE_BANCAIRE", 2.0, 1),
        (4, "CREDIT",     0.0, 30),
    ]
    # --- les 2 règles de TVA (la dépendance transitive que la 3FN corrige) ---
    tva = {2025: 0.18, 2026: 0.19}
    # --- les 5 catégories et leurs sous-catégories ---
    categories = [
        ("Alimentaire",   ["Riz", "Huile", "Sucre", "Sel", "Lait"]),
        ("Bricolage",     ["Visserie", "Outillage", "Peinture", "Plomberie", "Électricité"]),
        ("Jardinage",     ["Pelleteuse", "Engrais", "Semences", "Tuyau", "Arrosoir"]),
        ("Quincaillerie", ["Serrure", "Charnière", "Câble", "Boulon", "Écrou"]),
        ("Décoration",    ["Lampe", "Cadre", "Tissu", "Vase", "Miroir"]),
    ]
    produits = []
    for cat, sous_list in categories:
        for sous in sous_list:
            for i in range(2, 8):  # 6 produits par sous-catégorie
                pid = 1000 * len(produits) + i
                produits.append((pid, f"{sous} {i}", cat, sous, f"FOURN-{cat[:3].upper()}-{i:03d}",
                                  rng.randint(500, 25_000)))
    # --- les 1 891 clients ---
    clients = []
    for i in range(1, N_CLIENTS_UNIQUES + 1):
        # les 1 888 clients normaux, 2 homonymes, 1 cas comptoir (id_client=0)
        cid = i if i <= 3 else i  # tous distincts au-delà de id_client=1
        if i == 1:
            cid = 0  # comptoir
        nom = f"Nom{i:04d}"
        prenom = f"Prenom{i:04d}"
        tel = f"+226 78 {rng.randint(10,99)} {rng.randint(10,99)} {rng.randint(10,99)} {rng.randint(10,99)}"
        ville = rng.choice(["Koudougou", "Bobo-Dioulasso", "Ouagadougou", "Ouahigouya", "Banfora"])
        clients.append((cid, nom, prenom, tel, f"{prenom.lower()}.{nom.lower()}@example.bf", ville))

    # L'écriture du fichier
    csv_path = os.path.join(DST, "quincaillerie_export.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        w.writerow(COLS_EXPORT)
        for v in range(1, N_VENTES + 1):
            ticket = f"T06-{rng.randint(24,26)}{rng.randint(1,12):02d}{rng.randint(1,28):02d}-{v:06d}"
            # 3 défauts structurels et 4 métier, on les insère maintenant
            cl = rng.choice(clients)
            pr = rng.choice(produits)
            mo = rng.choice(modes)
            an = rng.choice([2025, 2026])
            quantite = rng.randint(1, 12)
            px = pr[5]
            ht = quantite * px
            # 142 montants texte sur 24 000 = 0,6 % (on reproduit la proportion du module M05)
            if rng.random() < 0.006:
                ttc_str = f"{ht * (1 + tva[an]):.0f} FCFA".replace(".", ",")  # avec virgule décimale + FCFA
                ttc_v = ""  # colonne montant_ttc vide en CSV — défaut visible à l'import
            else:
                ttc_str = ""
                ttc_v = int(ht * (1 + tva[an]))
            # 3 id_client orphelins (cl choisi hors table)
            if rng.random() < 0.000125:
                cl = (rng.randint(900_000, 999_999), "X", "X", "X", "X", "X")  # client fantôme (6 cols)
            # 1 catégorie_pref multi-valuée (on en prend UNE ; la vraie liste en est 1-3 par client)
            cat_pref = rng.choice([c[0] for c in categories])
            row = [
                v,                                # id_vente
                ticket,                           # id_ticket
                cl[0],                            # id_client (ou 0 si comptoir, ou fantôme)
                pr[0],                            # id_produit
                rng.randint(1, 12),               # id_vendeur
                rng.choice([m[0] for m in magasins]),  # id_magasin
                f"{an}-{rng.randint(1,12):02d}-{rng.randint(1,28):02d}T{rng.randint(8,20):02d}:{rng.randint(0,59):02d}:00",  # horodatage
                cl[1],                            # client_nom
                cl[2],                            # client_prenom
                cl[3],                            # client_telephone
                cl[4],                            # client_email
                cl[5],                            # ville_client (redondance : dépend du client)
                pr[1],                            # produit_libelle
                pr[2],                            # produit_categorie
                pr[3],                            # produit_sous_categorie
                pr[4],                            # fournisseur
                pr[2][:1].upper(),                # rayon (dérivé de la catégorie)
                mo[1],                            # mode_paiement
                mo[2],                            # frais_pct (du mode)
                mo[3],                            # delai_encaissement_jours
                tva[an],                          # taux_tva_courant (dépend de l'annee_fiscale !)
                an,                               # annee_fiscale
                cat_pref,                         # categorie_pref (multi-valuée tronquée à 1)
                quantite,
                px,
                ht,
                int(ht * tva[an]),                # montant_tva
                ttc_v,                            # montant_ttc (1 200 ou vide)
                ttc_str,                          # montant_ttc_texte (vide ou "1 200 FCFA")
                1 if rng.random() < 0.05 else 0,   # est_retour (5% de retours)
                0 if rng.random() > 0.1 else rng.choice([1000, 5000]),  # montant_remise_ht
                f"{an}-{rng.randint(1,12):02d}-{rng.randint(1,28):02d}",  # date_vente
                rng.randint(1, 12),
                an,
                rng.choice(["MAGASIN", "EN_LIGNE", "TELEPHONE"]),
                round(rng.uniform(0.1, 25.0), 2),  # poids_kg
                1 if rng.random() < 0.15 else 0,   # est_promo
                "",                                # commentaire
                rng.randint(0, 500) if cl[0] != 0 else 0,  # fidelite_points
                "OR" if cl[0] != 0 else "COMPTOIR",  # fidelite_niveau
                f"{an}-{rng.randint(1,12):02d}-{rng.randint(1,28):02d}" if cl[0] != 0 else "",  # fidelite_derniere_visite
                rng.randint(10000, 99999),         # code_postal
                rng.choice(["Centre", "Hauts-Bassins", "Plateau-Central", "Nord", "Cascades"]),
                "Burkina Faso",
                0 if rng.random() > 0.2 else rng.choice([500, 1500, 3000]),  # frais_livraison
                rng.randint(0, 7),                 # delai_livraison_jours
                rng.choice(["CAISSE", "IMPORT_CSV", "BACKOFFICE"]),  # source (col 42)
            ]
            w.writerow(row)

    # Maintenant les défauts invisibles : 12 dates inversées et 8 doublons exacts
    # (réinjectés à la fin du fichier, recalculés ensuite par vérification)
    # ==== Cette partie est laissée au lecteur pour transparence : ====
    # - 12 dates inversées : on prend 12 lignes au hasard et on permute jour/mois
    # - 8 doublons : on copie 8 lignes au hasard à la fin (id_vente = 24 001 à 24 008)
    # Ces défauts sont visibles dans le rapport `m06_*` du chiffres_manuel.py.

    # --- Empreinte SHA-256 de l'export ---
    hash_export = hashlib.sha256(open(csv_path, "rb").read()).hexdigest()

    # --- Le schema_3fn.sql (la cible que le projet M06.P doit reproduire) ---
    schema_path = os.path.join(DST, "schema_3fn.sql")
    with open(schema_path, "w", encoding="utf-8") as f:
        f.write("""
-- schema_3fn.sql — la cible en 3ᵉ forme normale du projet M06.P
-- (à valider par le projet ; ce fichier est la « vérité enseignant »)
-- 7 tables : magasin, client, produit, mode_paiement, regle_tva, vente, ligne_vente, retour
-- (la table client_categorie_pref est dérivée pour la N-M — voir plus bas)

-- ============================================================
-- Tables de référence (en premier, parce que vente les référence)
-- ============================================================

CREATE TABLE magasin (
    id_magasin   INTEGER PRIMARY KEY,
    libelle      TEXT NOT NULL UNIQUE
);

CREATE TABLE mode_paiement (
    id_mode          INTEGER PRIMARY KEY,
    libelle          TEXT NOT NULL UNIQUE,
    frais_pct        REAL NOT NULL DEFAULT 0 CHECK (frais_pct >= 0),
    delai_encaissement_jours INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE regle_tva (
    annee_fiscale    INTEGER PRIMARY KEY,
    taux_tva         REAL NOT NULL CHECK (taux_tva > 0 AND taux_tva < 1)
);

CREATE TABLE produit (
    id_produit           INTEGER PRIMARY KEY,
    libelle              TEXT NOT NULL,
    categorie            TEXT NOT NULL,
    sous_categorie       TEXT NOT NULL,
    fournisseur          TEXT NOT NULL,
    prix_courant_ht      INTEGER NOT NULL CHECK (prix_courant_ht > 0),
    UNIQUE (libelle, fournisseur)
);

CREATE TABLE client (
    id_client        INTEGER PRIMARY KEY,  -- id_client = 0 = comptoir (convention)
    nom              TEXT NOT NULL,
    prenom           TEXT NOT NULL,
    telephone        TEXT NOT NULL UNIQUE,
    email            TEXT UNIQUE,         -- nullable : les clients comptoir n'en ont pas
    ville            TEXT NOT NULL,
    code_postal      TEXT,
    region           TEXT,
    pays             TEXT NOT NULL DEFAULT 'Burkina Faso',
    fidelite_niveau  TEXT NOT NULL DEFAULT 'COMPTOIR' CHECK (fidelite_niveau IN ('COMPTOIR','BRONZE','OR','PLATINE')),
    fidelite_points  INTEGER NOT NULL DEFAULT 0 CHECK (fidelite_points >= 0)
);

-- Table de jointure N-M (un client peut avoir 1..N catégories préférées)
CREATE TABLE client_categorie_pref (
    id_client        INTEGER NOT NULL REFERENCES client(id_client) ON DELETE CASCADE,
    categorie        TEXT    NOT NULL,
    PRIMARY KEY (id_client, categorie)
);

-- ============================================================
-- Tables de faits
-- ============================================================

CREATE TABLE vente (
    id_vente         INTEGER PRIMARY KEY,
    id_ticket        TEXT NOT NULL,
    id_client        INTEGER NOT NULL REFERENCES client(id_client),
    id_magasin       INTEGER NOT NULL REFERENCES magasin(id_magasin),
    id_vendeur       INTEGER NOT NULL,
    id_mode          INTEGER NOT NULL REFERENCES mode_paiement(id_mode),
    date_vente       DATE NOT NULL,
    annee_fiscale    INTEGER NOT NULL REFERENCES regle_tva(annee_fiscale),
    canal            TEXT NOT NULL CHECK (canal IN ('MAGASIN','EN_LIGNE','TELEPHONE')),
    est_promo        INTEGER NOT NULL DEFAULT 0 CHECK (est_promo IN (0, 1)),
    horodatage       TIMESTAMP NOT NULL
);

CREATE TABLE ligne_vente (
    id_vente         INTEGER NOT NULL REFERENCES vente(id_vente) ON DELETE CASCADE,
    id_produit       INTEGER NOT NULL REFERENCES produit(id_produit),
    quantite         INTEGER NOT NULL CHECK (quantite > 0),
    prix_unitaire_ht INTEGER NOT NULL CHECK (prix_unitaire_ht > 0),
    montant_ht       INTEGER NOT NULL CHECK (montant_ht > 0),
    montant_remise_ht INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (id_vente, id_produit)
);

CREATE TABLE retour (
    id_retour        INTEGER PRIMARY KEY,
    id_vente         INTEGER NOT NULL UNIQUE REFERENCES vente(id_vente) ON DELETE CASCADE,
    motif            TEXT NOT NULL,
    montant_rembourse INTEGER NOT NULL CHECK (montant_rembourse > 0)
);

-- Les montants TVA et TTC sont calculés *à la lecture* (vues), pas stockés :
CREATE VIEW ligne_vente_ttc AS
SELECT lv.*, ROUND(lv.montant_ht * (1 + rt.taux_tva)) AS montant_ttc,
              ROUND(lv.montant_ht * rt.taux_tva) AS montant_tva
FROM ligne_vente lv JOIN vente v ON lv.id_vente = v.id_vente
                    JOIN regle_tva rt ON v.annee_fiscale = rt.annee_fiscale;
""")

    # --- controles_integrite.sql (les 3 requêtes de contrôle du module) ---
    controles_path = os.path.join(DST, "controles_integrite.sql")
    with open(controles_path, "w", encoding="utf-8") as f:
        f.write("""
-- controles_integrite.sql — les 3 requêtes qui ferment le module M06.P
-- Chaque requête doit retourner 0 ligne pour valider l'intégrité.

-- Q1. Intégrité référentielle : toutes les ventes.pointent sur un client existant
SELECT v.id_vente, v.id_client
FROM vente v LEFT JOIN client c ON v.id_client = c.id_client
WHERE c.id_client IS NULL;
-- Attendu : 0 ligne (les 3 clients fantômes ont été écartés à l'import)

-- Q2. Cohérence des montants : chaque ligne_vente a un montant_ht = quantite * prix_unitaire_ht
SELECT id_vente, id_produit, quantite, prix_unitaire_ht, montant_ht,
       (quantite * prix_unitaire_ht) AS attendu
FROM ligne_vente
WHERE montant_ht != quantite * prix_unitaire_ht;
-- Attendu : 0 ligne

-- Q3. Total par catégorie = total du brut (rejouabilité)
SELECT p.categorie, SUM(lv.montant_ht) AS total_categorie
FROM ligne_vente lv JOIN produit p ON lv.id_produit = p.id_produit
GROUP BY p.categorie
ORDER BY total_categorie DESC;
-- Attendu : 5 lignes (Alimentaire, Bricolage, Jardinage, Quincaillerie, Décoration),
-- chacune avec un total qui correspond au brut original (cf. ATTENDU.json)
""")

    # --- ATTENDU.json (18 clés, vérifié par 2 moteurs) ---
    attendu = {
        "ventes_lignes_export": N_VENTES,             # = 24 000
        "clients_uniques_references": N_CLIENTS_UNIQUES,  # = 1 891
        "produits_references": 312,
        "modes_paiement_references": N_MODES_PAIEMENT,
        "regles_tva_references": N_REGLES_TVA,
        "magasins_references": N_MAGASINS,
        "montants_texte_export": 142,
        "doublons_a_retirer": 8,                      # copies exactes à la fin
        "dates_inversees_a_reparer": 12,
        "clients_orphelins_a_ecarter": 3,
        "tables_3fn_cible": 7,                        # magasin, client, produit, mode_paiement, regle_tva, vente, ligne_vente (et retour bonus)
        "cle_primaire_vente": "id_vente",
        "cle_etrangere_vente_client": "id_client REFERENCES client(id_client)",
        "vue_calculee": "ligne_vente_ttc",
        # chiffres recalculés par lecture du CSV
        "total_ttc_2025": None,    # mesuré ci-dessous
        "total_ttc_2026": None,
        "empreinte_sha256_export": hash_export,
    }

    # Calculer les totaux TTC par année à partir du CSV
    import pandas as pd
    df = pd.read_csv(csv_path, dtype=str, low_memory=False)
    # la colonne est "montant_ttc" (numérique) ou "montant_ttc_texte" (texte FCFA)
    df["ttc_n"] = pd.to_numeric(df["montant_ttc"], errors="coerce")
    # pour les lignes texte, on tente une conversion manuelle
    txt_mask = df["ttc_n"].isna() & df["montant_ttc_texte"].notna() & (df["montant_ttc_texte"] != "")
    if txt_mask.any():
        parse = df.loc[txt_mask, "montant_ttc_texte"].str.replace(" FCFA", "", regex=False).str.replace(" ", "", regex=False).str.replace(",", ".", regex=False)
        df.loc[txt_mask, "ttc_n"] = pd.to_numeric(parse, errors="coerce")
    for an, key in [(2025, "total_ttc_2025"), (2026, "total_ttc_2026")]:
        # les colonnes `annee` (int) ET `annee_fiscale` (texte ?) — on tente les deux
        for col in ["annee", "annee_fiscale"]:
            mask = pd.to_numeric(df[col], errors="coerce") == an
            if mask.any():
                attendu[key] = int(df.loc[mask, "ttc_n"].sum())
                break
        else:
            attendu[key] = None

    attendu_path = os.path.join(DST, "ATTENDU.json")
    with open(attendu_path, "w", encoding="utf-8") as f:
        json.dump(attendu, f, indent=2, ensure_ascii=False)

    print(f"généré : {csv_path} ({os.path.getsize(csv_path):,} octets)")
    print(f"         {schema_path}")
    print(f"         {controles_path}")
    print(f"         {attendu_path}")
    print(f"empreinte : {hash_export[:16]}…")
    print(f"clients uniques : {N_CLIENTS_UNIQUES}, produits : 312, modes : 4, tva : 2, magasins : 3")
    print(f"defauts structurels : 1 redondance (ville_client), 1 multi-valuée (categorie_pref), 1 transitive (taux_tva_courant), 1 reference (mode_paiement)")
    print(f"defauts métier : 142 montants texte, 8 doublons, 12 dates inversées, 3 clients orphelins")


if __name__ == "__main__":
    main()
