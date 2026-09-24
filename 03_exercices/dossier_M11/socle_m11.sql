-- socle_m11.sql — socle du module M11 « SQL avancé pour la BI »
--
-- Écrit par `tools/dossier_M11.py`. Ne pas modifier à la main : régénérer.
--
-- MODE D'EMPLOI. Les chemins de ce fichier sont relatifs à la RACINE du dépôt.
-- Ouvrir le socle par `03_exercices/dossier_M11/connexion.py`, ou depuis la racine :
--
--     python3 -c "import sys; sys.path.insert(0,'03_exercices/dossier_M11'); \
--                 from connexion import ouvrir; con = ouvrir()"
--
-- Le socle ne crée aucune donnée : il DÉCLARE ce qui existe déjà.
--   * tables : les référentiels courts, chargés une fois (produits, magasins, vendeurs,
--              objectifs, calendrier) ;
--   * vues   : les deux gros volumes (ventes, clients), lus dans leurs CSV d'origine
--              et donc jamais recopiés.

-- ------------------------------------------------------------------ référentiels
CREATE OR REPLACE TABLE produit AS
SELECT * FROM read_csv_auto('01_socle_donnees/data/brut/produits.csv', header = true);

CREATE OR REPLACE TABLE magasin AS
SELECT * FROM read_csv_auto('01_socle_donnees/data/brut/magasins.csv', header = true);

CREATE OR REPLACE TABLE vendeur AS
SELECT * FROM read_csv_auto('01_socle_donnees/data/brut/vendeurs.csv', header = true);

-- `objectifs_de_ca.csv` est séparé par des points-virgules, pas par des virgules :
-- sans `delim`, la table se charge en UNE colonne et le rapport est faux en silence.
CREATE OR REPLACE TABLE objectif_mois AS
SELECT * FROM read_csv_auto('01_socle_donnees/data/brut/objectifs_de_ca.csv',
                            header = true, delim = ';');

-- Le calendrier : une ligne par jour, y compris les jours sans vente.
CREATE OR REPLACE TABLE calendrier AS
SELECT * FROM read_csv_auto('01_socle_donnees/data/reference/dim_date.csv', header = true);

-- ------------------------------------------------------------------ volumes (vues)
CREATE OR REPLACE VIEW ventes AS
SELECT
    id_vente            AS id_vente,
    id_ticket           AS id_ticket,
    CAST(date_vente AS DATE) AS date_vente,
    CAST(heure AS TIME)      AS heure,
    id_magasin          AS id_magasin,
    id_vendeur          AS id_vendeur,
    id_client           AS id_client,
    id_produit          AS id_produit,
    quantite            AS quantite,
    prix_unitaire_ht    AS prix_unitaire_ht,
    taux_remise         AS taux_remise,
    montant_ht          AS montant_ht,
    montant_tva         AS montant_tva,
    montant_ttc         AS montant_ttc,
    mode_paiement       AS mode_paiement,
    canal               AS canal,
    CAST(est_retour AS BOOLEAN) AS est_retour,
    poids_kg            AS poids_kg
FROM read_csv_auto('01_socle_donnees/data/reference/ventes_propres.csv', header = true);

CREATE OR REPLACE VIEW clients AS
SELECT
    id_client           AS id_client,
    nom                 AS nom,
    type_client         AS type_client,
    ville               AS ville,
    region              AS region,
    CAST(date_creation AS DATE) AS date_creation,
    segment             AS segment,
    conditions_paiement AS conditions_paiement
FROM read_csv_auto('01_socle_donnees/data/brut/clients.csv', header = true);

-- ------------------------------------------------- copie de travail (performance)
-- Les deux vues relisent le CSV à chaque requête : 0,14 s pour un simple comptage.
-- `connexion.py(materialiser=True)` crée les copies en mémoire `ventes_m` et
-- `clients_m` (0,46 s) : la même requête tombe alors sous la milliseconde. C'est la
-- mesure d'ouverture du chapitre C06 — une vue n'est pas lente, elle est relue.
