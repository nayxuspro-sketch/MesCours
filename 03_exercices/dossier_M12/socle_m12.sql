-- socle_m12.sql — socle du module M12 « Fondamentaux de la Business Intelligence »
--
-- Écrit par `tools/dossier_M12.py`. Ne pas modifier à la main : régénérer.
--
-- CE FICHIER NE CONTIENT QUE LES CINQ TABLES AJOUTÉES PAR M12.
-- `connexion.py` rejoue d'abord `dossier_M11/socle_m11.sql` (les ventes et les
-- référentiels du fil rouge), puis ce fichier : le socle de M12 est le socle de
-- M11 **plus** les sources opérationnelles qu'un KPI exige.
--
-- Pourquoi ces cinq tables ? Dix indicateurs de commerce de gros ne se calculent
-- pas sur des lignes de vente :
--   * marge brute          → il faut un COÛT D'ACHAT (cout_produits)
--   * rotation de stock    → il faut un STOCK (stock_mensuel)
--   * taux de rupture      → il faut un ÉTAT DE RUPTURE (ruptures)
--   * taux de service      → il faut une PROMESSE et une LIVRAISON (commandes_clients)
--   * taux de recouvrement → il faut une ÉCHÉANCE et un ENCAISSEMENT (encaissements)
--   * coût logistique      → il faut des COLIS et des COÛTS (logistique_mensuelle)
-- Toute la leçon du module tient dans ce commentaire : **un indicateur réclame sa
-- source, et une source absente ne se remplace pas par une approximation.**

-- ---------------------------------------------------------------- coût d'achat
CREATE OR REPLACE TABLE cout_produit AS
SELECT * FROM read_csv_auto('03_exercices/dossier_M12/cout_produits.csv', header = true);

-- ------------------------------------------------------------ stock mensuel
CREATE OR REPLACE TABLE stock_mensuel AS
SELECT * FROM read_csv_auto('03_exercices/dossier_M12/stock_mensuel.csv', header = true);

-- ----------------------------------------------------------------- ruptures
CREATE OR REPLACE TABLE rupture AS
SELECT * FROM read_csv_auto('03_exercices/dossier_M12/ruptures.csv', header = true);

-- --------------------------------------------------- commandes des clients
-- Les deux dates vides (commande annulée, facture non encaissée) sont lues en
-- TEXTE puis converties par TRY_CAST : un `read_csv_auto` qui devine un DATE
-- échoue sur la chaîne vide, et un socle qui échoue à l'ouverture ne sert à rien.
CREATE OR REPLACE TABLE commande AS
SELECT CAST(id_commande AS INTEGER)  AS id_commande,
       CAST(id_client  AS INTEGER)   AS id_client,
       CAST(id_magasin AS INTEGER)   AS id_magasin,
       CAST(date_commande  AS DATE)  AS date_commande,
       CAST(date_promisee  AS DATE)  AS date_promisee,
       TRY_CAST(date_livraison AS DATE) AS date_livraison,
       CAST(montant_ttc AS DOUBLE)   AS montant_ttc,
       statut
FROM read_csv_auto('03_exercices/dossier_M12/commandes_clients.csv',
                   header = true, all_varchar = true);

-- ------------------------------------------------------------ encaissements
CREATE OR REPLACE TABLE encaissement AS
SELECT CAST(id_facture AS INTEGER) AS id_facture,
       CAST(id_client  AS INTEGER) AS id_client,
       CAST(date_facture  AS DATE) AS date_facture,
       CAST(date_echeance AS DATE) AS date_echeance,
       TRY_CAST(date_encaissement AS DATE) AS date_encaissement,
       CAST(montant_ttc AS DOUBLE) AS montant_ttc,
       CAST(montant_encaisse AS DOUBLE) AS montant_encaisse,
       conditions_paiement
FROM read_csv_auto('03_exercices/dossier_M12/encaissements.csv',
                   header = true, all_varchar = true);

-- ----------------------------------------------------------------- logistique
CREATE OR REPLACE TABLE logistique AS
SELECT * FROM read_csv_auto('03_exercices/dossier_M12/logistique_mensuelle.csv',
                            header = true);

-- ------------------------------------------------------- vue de marge, par ligne
-- La marge brute n'est pas un champ : c'est `vente HT` MOINS `coût × quantité`.
-- La vue la calcule une fois, pour que les six chapitres ne la réécrivent pas —
-- et pour qu'on puisse la vérifier à un seul endroit.
CREATE OR REPLACE VIEW vente_marge AS
SELECT v.id_vente, v.id_ticket, v.date_vente, v.id_magasin, v.id_client, v.id_produit,
       v.quantite, v.montant_ht, v.montant_ttc, v.est_retour,
       p.categorie, p.sous_categorie,
       c.cout_unitaire_ht,
       ROUND(v.montant_ht - c.cout_unitaire_ht * v.quantite, 2) AS marge_fcfa
FROM ventes v
JOIN produit p        ON p.id_produit  = v.id_produit
JOIN cout_produit c   ON c.id_produit  = v.id_produit;
