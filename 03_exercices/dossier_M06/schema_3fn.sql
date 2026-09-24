
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
