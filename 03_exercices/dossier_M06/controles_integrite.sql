
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
