-- socle_m13.sql — le modele de Sahel Distribution (module M13)
--
-- Ecrit par `tools/dossier_M13.py`. Ne pas modifier a la main : regenerer.
--
-- `connexion.py` rejoue trois fichiers, dans l'ordre :
--   1. dossier_M11/socle_m11.sql  — les ventes et les referentiels du fil rouge
--   2. dossier_M12/socle_m12.sql  — les cinq sources operationnelles
--   3. dossier_M13/socle_m13.sql  — CE FICHIER : le modele en etoile
--
-- Le modele compte DOUZE tables : CINQ dimensions et SEPT tables de faits.
--
--   Dimensions                      Faits
--   dim_client                      fait_ventes          (ligne de ticket)
--   dim_produit                     fait_commandes       (commande)
--   dim_magasin                     fait_encaissements   (facture)
--   dim_vendeur                     fait_stock_mensuel   (produit x mois)
--   dim_date                        fait_ruptures        (produit x magasin x mois)
--   (+ les versions historisees)    fait_logistique      (magasin x mois)
--                                   fait_objectifs       (magasin x mois)
--
-- Deux dimensions historisees (type 2) completent le modele, parce que la question
-- « quelle etait la valeur de cet attribut AU MOMENT du fait ? » n'a pas la meme
-- reponse que « quelle est sa valeur aujourd'hui » :
--   dim_client_scd   24 892 versions + la ligne « client non identifie »
--   dim_produit_scd     616 versions
--
-- Le grain de chaque table est ecrit AU-DESSUS d'elle : un modele dont les grains ne
-- sont pas ecrits est un modele qu'on ne peut pas auditer.

-- ================================================================ DIMENSIONS

-- ------------------------------------------------------------- dim_client
-- Grain : une ligne par client, etat COURANT de l'attribut.
CREATE OR REPLACE TABLE dim_client AS
SELECT CAST(id_client AS INTEGER)              AS id_client,
       nom,
       type_client,
       ville,
       region,
       TRY_CAST(date_creation AS DATE)         AS date_creation,
       segment,
       conditions_paiement
FROM clients;

-- Le client 0 du fichier de ventes n'existe pas dans le referentiel : le modele lui
-- donne une ligne explicite plutot que de laisser une cle etrangere orpheline. Une
-- dimension doit contenir la ligne « inconnu » — c'est une decision, pas un oubli.
INSERT INTO dim_client VALUES
    (0, 'CLIENT NON IDENTIFIE', 'Inconnu', 'Inconnu', 'Inconnu', NULL, 'Inconnu', 'Inconnu');

-- ------------------------------------------------------------ dim_produit
-- Grain : une ligne par produit. La famille est AJOUTEE : le referentiel porte 16
-- libelles pour 7 familles reelles, et c'est le modele qui porte la correspondance.
CREATE OR REPLACE TABLE dim_produit AS
SELECT CAST(id_produit AS INTEGER)             AS id_produit,
       designation,
       categorie                                AS libelle_source,  -- le libelle BRUT : la preuve
       -- TRIM avant la correspondance : deux libelles du referentiel portent une espace finale
       -- ('Materiaux ' et 'Quincaillerie '). Sans le TRIM, la meme famille se dedouble et le
       -- modele rend NEUF familles au lieu de sept — sans qu'aucune requete ne soit fausse.
       CASE TRIM(categorie)
            WHEN 'PEINTURE' THEN 'Peinture'   WHEN 'Peinture' THEN 'Peinture'
            WHEN 'Peintures' THEN 'Peinture'  WHEN 'peinture' THEN 'Peinture'
            WHEN 'MATÉRIAUX' THEN 'Materiaux' WHEN 'Materiaux' THEN 'Materiaux'
            WHEN 'Matériaux' THEN 'Materiaux' WHEN 'materiaux' THEN 'Materiaux'
            WHEN 'QUINCAILLERIE' THEN 'Quincaillerie'
            WHEN 'Quincaillerie' THEN 'Quincaillerie'
            WHEN 'quincaillerie' THEN 'Quincaillerie'
            WHEN 'Electricité' THEN 'Electricite'
            WHEN 'Bois & panneaux' THEN 'Bois et panneaux'
            WHEN 'Consommables' THEN 'Consommables'
            ELSE TRIM(categorie) END              AS famille,
       sous_categorie,
       unite,
       CAST(prix_vente_ht AS DOUBLE)           AS prix_vente_ht,
       CAST(poids_unite_kg AS DOUBLE)          AS poids_unite_kg,
       fournisseur,
       CAST(tva AS DOUBLE)                     AS tva,
       CAST(actif AS INTEGER)                  AS actif
FROM produit;

-- ------------------------------------------------------------ dim_magasin
-- Grain : une ligne par magasin. Le depot est present : il ne vend pas, mais il
-- recoit des colis — un fait sans vente n'est pas une dimension a supprimer.
CREATE OR REPLACE TABLE dim_magasin AS
SELECT CAST(id_magasin AS INTEGER) AS id_magasin, nom, ville, quartier, region,
       type_magasin, CAST(surface_m2 AS INTEGER) AS surface_m2, responsable,
       TRY_CAST(ouverture AS DATE) AS ouverture,
       CASE WHEN id_magasin IN (SELECT DISTINCT id_magasin FROM ventes)
            THEN 1 ELSE 0 END AS vend
FROM magasin;

-- ------------------------------------------------------------ dim_vendeur
-- Grain : une ligne par vendeur, rattache au magasin (hierarchie magasin -> vendeur).
CREATE OR REPLACE TABLE dim_vendeur AS
SELECT CAST(id_vendeur AS INTEGER) AS id_vendeur, nom_complet,
       CAST(id_magasin AS INTEGER) AS id_magasin,
       TRY_CAST(date_embauche AS DATE) AS date_embauche, statut, secteur_vente
FROM vendeur;

-- --------------------------------------------------------------- dim_date
-- Grain : une ligne par jour. C'est la SEULE table de dates du modele : aucune table
-- de faits ne porte d'attribut de calendrier, elles portent toutes une cle de date.
-- Trois attributs sont ajoutes au calendrier du fil rouge : la semaine commerciale
-- (samedi a vendredi), l'annee fiscale (1er juillet) et le libelle du jour ferie.
CREATE OR REPLACE TABLE dim_date AS
SELECT TRY_CAST(date AS DATE)                        AS date,
       CAST(annee AS INTEGER)                        AS annee,
       CAST(trimestre AS INTEGER)                    AS trimestre,
       CAST(mois AS INTEGER)                         AS mois,
       libelle_mois,
       CAST(semaine_iso AS INTEGER)                  AS semaine_iso,
       CAST(jour_semaine AS INTEGER)                 AS jour_semaine,
       libelle_jour,
       CAST(est_dimanche AS INTEGER)                 AS est_dimanche,
       CAST(est_ferie AS INTEGER)                    AS est_ferie,
       COALESCE(evenement, '')                       AS libelle_ferie,
       annee_mois,
       -- semaine commerciale : la semaine du samedi au vendredi, numerotee dans l'annee
       CAST(floor((dayofyear(date) + 5 - dayofweek(date) + 7) / 7) AS INTEGER)
                                                     AS semaine_commerciale,
       -- annee fiscale : elle commence le 1er juillet (choix du modele, declare)
       CASE WHEN CAST(mois AS INTEGER) >= 7
            THEN CAST(annee AS INTEGER) ELSE CAST(annee AS INTEGER) - 1 END
                                                     AS annee_fiscale,
       CASE WHEN CAST(mois AS INTEGER) >= 7 THEN 1 ELSE 2 END AS periode_fiscale
FROM calendrier;

-- ------------------------------------------------ dim_client_scd (type 2)
-- Grain : une version de client, valide du 1er jour au dernier jour (fin ouverte).
--
-- Un changement lent de dimension de type 2 est une REQUETE, pas un fichier recu.
-- La question a laquelle elle repond : « quelle etait la valeur de cet attribut AU
-- MOMENT du fait ? ». Trois etapes :
--   1. les bornes de version : la date d'entree en vigueur de chaque changement a
--      historiser (type 2), plus l'ouverture du compte client. Cette ouverture est la
--      PLUS ANCIENNE de deux dates : la date de creation ecrite au referentiel et la
--      premiere vente connue. 6 685 clients ont une premiere vente anterieure a leur
--      date de creation — le referentiel porte une date de SAISIE, le fait porte une
--      date de VENTE. Sans ce rattrapage, la jointure « au moment du fait » perdrait
--      28 784 lignes de ticket, sans erreur et sans avertissement ;
--   2. la valeur d'un attribut a une date : la derniere valeur posee a cette date,
--      sinon la valeur d'AVANT le premier changement, sinon celle du referentiel ;
--   3. la periode de validite : jusqu'a la veille du changement suivant, fin ouverte
--      pour la version courante.
-- Les corrections de saisie (type 1) ne creent AUCUNE version : la bonne valeur a
-- toujours ete la bonne.
CREATE OR REPLACE TABLE dim_client_scd AS
WITH prem AS (
    SELECT CAST(id_client AS INTEGER) AS id_client,
           MIN(TRY_CAST(date_vente AS DATE)) AS premiere_vente
    FROM ventes GROUP BY 1),
base AS (
    SELECT CAST(c.id_client AS INTEGER) AS id_client, c.ville, c.segment,
           c.conditions_paiement, c.type_client,
           COALESCE(TRY_CAST(c.date_creation AS DATE), DATE '2023-01-01') AS date_creation,
           p.premiere_vente
    FROM clients c
    LEFT JOIN prem p ON p.id_client = CAST(c.id_client AS INTEGER)),
mvt AS (
    SELECT CAST(id_client AS INTEGER) AS id_client, TRY_CAST(date_effet AS DATE) AS date_effet,
           nature, valeur_avant, valeur_apres, CAST(type_scd AS INTEGER) AS type_scd
    FROM read_csv_auto('03_exercices/dossier_M13/mouvements_clients.csv', header = true)),
bornes AS (
    SELECT id_client, date_effet AS debut FROM mvt WHERE type_scd = 2
    UNION
    SELECT id_client, LEAST(date_creation, COALESCE(premiere_vente, date_creation)) AS debut
    FROM base),
versions AS (
    SELECT id_client, debut,
           row_number() OVER (PARTITION BY id_client ORDER BY debut) AS version,
           lead(debut) OVER (PARTITION BY id_client ORDER BY debut) AS fin
    FROM bornes)
SELECT v.id_client, CAST(v.version AS INTEGER) AS version, v.debut AS date_debut,
       (v.fin - INTERVAL 1 DAY)::DATE                                          AS date_fin,
       COALESCE((SELECT m.valeur_apres FROM mvt m WHERE m.id_client = v.id_client
                   AND m.nature = 'segment' AND m.type_scd = 2 AND m.date_effet <= v.debut
                 ORDER BY m.date_effet DESC LIMIT 1),
                (SELECT m.valeur_avant FROM mvt m WHERE m.id_client = v.id_client
                   AND m.nature = 'segment' AND m.type_scd = 2
                 ORDER BY m.date_effet LIMIT 1),
                (SELECT b.segment FROM base b WHERE b.id_client = v.id_client))       AS segment,
       COALESCE((SELECT m.valeur_apres FROM mvt m WHERE m.id_client = v.id_client
                   AND m.nature = 'ville' AND m.type_scd = 2 AND m.date_effet <= v.debut
                 ORDER BY m.date_effet DESC LIMIT 1),
                (SELECT m.valeur_avant FROM mvt m WHERE m.id_client = v.id_client
                   AND m.nature = 'ville' AND m.type_scd = 2
                 ORDER BY m.date_effet LIMIT 1),
                (SELECT b.ville FROM base b WHERE b.id_client = v.id_client))         AS ville,
       COALESCE((SELECT m.valeur_apres FROM mvt m WHERE m.id_client = v.id_client
                   AND m.nature = 'conditions' AND m.type_scd = 2 AND m.date_effet <= v.debut
                 ORDER BY m.date_effet DESC LIMIT 1),
                (SELECT b.conditions_paiement FROM base b WHERE b.id_client = v.id_client))
                                                                                     AS conditions_paiement,
       (SELECT b.type_client FROM base b WHERE b.id_client = v.id_client)            AS type_client,
       CASE WHEN v.fin IS NULL THEN 1 ELSE 0 END                                 AS est_courante,
       CAST(v.id_client AS VARCHAR) || '-' || CAST(v.version AS VARCHAR)         AS cle_version
FROM versions v;

-- La decision prise pour dim_client vaut aussi pour sa version historisee : sans une
-- ligne « client non identifie », la jointure « au moment du fait » perdrait les
-- 43 161 lignes de ticket du client 0. Une dimension qui gagne une ligne inconnue
-- doit la gagner dans TOUTES ses formes — sinon le fait disparait d'un total.
INSERT INTO dim_client_scd VALUES
    (0, 1, DATE '1900-01-01', NULL, 'Inconnu', 'Inconnu', 'Inconnu', 'Inconnu', 1, '0-1');

-- ----------------------------------------------- dim_produit_scd (type 2)
-- Grain : une version de produit, prix valable sur la periode : 616 versions pour
-- 154 produits et 4 revisions. La dimension produit courante porte le prix ACTUEL ;
-- seule la dimension historisee permet de calculer une marge « au prix de l'epoque ».
CREATE OR REPLACE TABLE dim_produit_scd AS
WITH grille AS (
    SELECT CAST(id_produit AS INTEGER) AS id_produit, TRY_CAST(date_effet AS DATE) AS date_debut,
           CAST(prix_vente_ht AS DOUBLE) AS prix_vente_ht
    FROM read_csv_auto('03_exercices/dossier_M13/tarifs_produits.csv', header = true)),
v AS (
    SELECT id_produit, date_debut, prix_vente_ht,
           row_number() OVER (PARTITION BY id_produit ORDER BY date_debut)      AS version,
           lead(date_debut) OVER (PARTITION BY id_produit ORDER BY date_debut)  AS date_debut_suivante
    FROM grille)
SELECT v.id_produit, CAST(v.version AS INTEGER) AS version, v.date_debut,
       (v.date_debut_suivante - INTERVAL 1 DAY)::DATE   AS date_fin,
       v.prix_vente_ht, p.sous_categorie, p.famille,
       CASE WHEN v.date_debut_suivante IS NULL THEN 1 ELSE 0 END AS est_courante,
       CAST(v.id_produit AS VARCHAR) || '-' || CAST(v.version AS VARCHAR) AS cle_version
FROM v JOIN dim_produit p ON p.id_produit = v.id_produit;

-- ===================================================================== FAITS

-- ------------------------------------------------------------ fait_ventes
-- Grain : UNE LIGNE DE TICKET (240 000 lignes). C'est le grain le plus fin du
-- modele ; tout ce qui est plus agrege se calcule a partir de lui.
CREATE OR REPLACE TABLE fait_ventes AS
SELECT CAST(id_vente AS INTEGER)      AS id_vente,
       id_ticket,                      -- 'T01-230101-000000' : une cle METIER, pas un nombre
       TRY_CAST(date_vente AS DATE)   AS date_vente,
       CAST(id_magasin AS INTEGER)    AS id_magasin,
       CAST(id_vendeur AS INTEGER)    AS id_vendeur,
       CAST(id_client AS INTEGER)     AS id_client,
       CAST(id_produit AS INTEGER)    AS id_produit,
       CAST(quantite AS DOUBLE)       AS quantite,
       CAST(prix_unitaire_ht AS DOUBLE) AS prix_unitaire_ht,
       CAST(taux_remise AS DOUBLE)    AS taux_remise,
       CAST(montant_ht AS DOUBLE)     AS montant_ht,
       CAST(montant_ttc AS DOUBLE)    AS montant_ttc,
       CAST(montant_tva AS DOUBLE)    AS montant_tva,
       mode_paiement, canal,
       CAST(est_retour AS INTEGER)    AS est_retour,
       CAST(poids_kg AS DOUBLE)       AS poids_kg
FROM ventes;

-- ---------------------------------------------------------- fait_commandes
-- Grain : UNE COMMANDE (9 000).
CREATE OR REPLACE TABLE fait_commandes AS
SELECT id_commande, id_client, id_magasin,
       TRY_CAST(date_commande AS DATE)   AS date_commande,
       TRY_CAST(date_promisee AS DATE)   AS date_promisee,
       TRY_CAST(date_livraison AS DATE)  AS date_livraison,
       CAST(montant_ttc AS DOUBLE)       AS montant_ttc, statut
FROM commande;

-- ------------------------------------------------------ fait_encaissements
-- Grain : UNE FACTURE (9 000).
CREATE OR REPLACE TABLE fait_encaissements AS
SELECT id_facture, id_client,
       TRY_CAST(date_facture AS DATE)      AS date_facture,
       TRY_CAST(date_echeance AS DATE)     AS date_echeance,
       TRY_CAST(date_encaissement AS DATE) AS date_encaissement,
       CAST(montant_ttc AS DOUBLE)         AS montant_ttc,
       CAST(montant_encaisse AS DOUBLE)    AS montant_encaisse, conditions_paiement
FROM encaissement;

-- ------------------------------------------------------ fait_stock_mensuel
-- Grain : PRODUIT x MOIS (6 776) — un instantane periodique, donc SEMI-ADDITIF :
-- on additionne dans l'espace, jamais dans le temps.
CREATE OR REPLACE TABLE fait_stock_mensuel AS
SELECT id_produit, mois, CAST(entrees_unites AS DOUBLE) AS entrees_unites,
       CAST(stock_moyen_unites AS DOUBLE) AS stock_moyen_unites,
       CAST(couverture_mois AS DOUBLE)    AS couverture_mois
FROM stock_mensuel;

-- ---------------------------------------------------------- fait_ruptures
-- Grain : PRODUIT x MAGASIN x MOIS (2 428).
CREATE OR REPLACE TABLE fait_ruptures AS
SELECT id_produit, id_magasin, mois, CAST(jours_rupture AS INTEGER) AS jours_rupture,
       CAST(unites_perdues_estimees AS DOUBLE) AS unites_perdues,
       CAST(ca_perdu_estime_fcfa AS DOUBLE)    AS ca_perdu
FROM rupture;

-- --------------------------------------------------------- fait_logistique
-- Grain : MAGASIN x MOIS (264).
CREATE OR REPLACE TABLE fait_logistique AS
SELECT id_magasin, mois, CAST(colis AS INTEGER) AS colis,
       CAST(poids_kg AS DOUBLE) AS poids_kg,
       CAST(cout_carburant_fcfa AS DOUBLE) AS cout_carburant,
       CAST(cout_main_oeuvre_fcfa AS DOUBLE) AS cout_main_oeuvre,
       CAST(cout_vehicule_fcfa AS DOUBLE) AS cout_vehicule,
       CAST(cout_total_fcfa AS DOUBLE) AS cout_total
FROM logistique;

-- --------------------------------------------------------- fait_objectifs
-- Grain : MAGASIN x MOIS (218) — un FAIT, pas un referentiel : il porte un montant
-- et une date, et il se joint aux ventes par la cle (magasin, mois).
CREATE OR REPLACE TABLE fait_objectifs AS
SELECT id_magasin, annee, mois, annee_mois,
       CAST(ca_objectif_ttc AS DOUBLE) AS ca_objectif_ttc,
       CAST(marge_objectif_pct AS DOUBLE) AS marge_objectif_pct
FROM objectif_mois;

-- ------------------------------------------------------------ les vues de recette
-- La recette du modele : les totaux doivent etre IDENTIQUES a ceux des sources.
CREATE OR REPLACE VIEW recette_ca AS
SELECT (SELECT ROUND(SUM(montant_ttc)) FROM fait_ventes WHERE est_retour = 0) AS ca_modele,
       (SELECT ROUND(SUM(montant_ttc)) FROM ventes WHERE est_retour = 0)       AS ca_source;
