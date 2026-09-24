-- 30_reponses.sql — corrigé des 30 questions (les requêtes de référence)
-- Chaque requête produit un résultat ; voir ATTENDU.json pour les chiffres mesurés.

-- ============================================================
-- Q01
-- ============================================================
SELECT COUNT(*) FROM client;

-- ============================================================
-- Q02
-- ============================================================
SELECT COUNT(*) FROM produit WHERE actif = TRUE;

-- ============================================================
-- Q03
-- ============================================================
SELECT id_magasin, nom, ville FROM magasin ORDER BY id_magasin;

-- ============================================================
-- Q04
-- ============================================================
SELECT ROUND(SUM(montant_ttc), 0) AS ca_total FROM vente;

-- ============================================================
-- Q05
-- ============================================================
SELECT id_mode, libelle, frais_pct FROM mode_paiement ORDER BY id_mode;

-- ============================================================
-- Q06
-- ============================================================
SELECT MIN(date_vente) AS premiere, MAX(date_vente) AS derniere FROM vente;

-- ============================================================
-- Q07
-- ============================================================
SELECT id_magasin, ROUND(SUM(montant_ttc), 0) AS ca_ttc FROM vente WHERE est_retour = FALSE GROUP BY id_magasin ORDER BY ca_ttc DESC;

-- ============================================================
-- Q08
-- ============================================================
SELECT EXTRACT(MONTH FROM date_vente)::INTEGER AS mois, COUNT(*) AS nb FROM vente WHERE EXTRACT(YEAR FROM date_vente) = 2025 GROUP BY 1 ORDER BY 1;

-- ============================================================
-- Q09
-- ============================================================
-- Q09 piège P2 : CA total SANS filtrer les retours (gonflé)
SELECT ROUND(SUM(montant_ttc), 0) AS ca_avec_retours FROM vente;

-- ============================================================
-- Q10
-- ============================================================
SELECT ROUND(AVG(montant_ttc), 0) AS panier_moyen FROM vente WHERE est_retour = FALSE;

-- ============================================================
-- Q11
-- ============================================================
SELECT id_produit, SUM(quantite) AS qte FROM vente GROUP BY id_produit ORDER BY qte DESC LIMIT 10;

-- ============================================================
-- Q12
-- ============================================================
SELECT id_client, ROUND(SUM(montant_ttc), 0) AS ca FROM vente GROUP BY id_client ORDER BY ca DESC LIMIT 5;

-- ============================================================
-- Q13
-- ============================================================
SELECT id_magasin, COUNT(DISTINCT id_client) AS nb_clients FROM vente GROUP BY id_magasin;

-- ============================================================
-- Q14
-- ============================================================
-- Q14 piège P3 : CA par mois, en filtrant date_vente <= date_limite_remise
SELECT EXTRACT(YEAR FROM date_vente)::INTEGER AS annee, EXTRACT(MONTH FROM date_vente)::INTEGER AS mois, ROUND(SUM(montant_ttc), 0) AS ca FROM vente WHERE date_vente <= date_limite_remise GROUP BY 1, 2 ORDER BY 1, 2;

-- ============================================================
-- Q15
-- ============================================================
SELECT COUNT(*) FROM vente WHERE EXTRACT(DOW FROM date_vente) = 0;

-- ============================================================
-- Q16
-- ============================================================
SELECT c.rayon, ROUND(100.0 * SUM(CASE WHEN v.est_retour THEN 1 ELSE 0 END) / COUNT(*), 1) AS taux_retour_pct FROM vente v JOIN produit p ON v.id_produit = p.id_produit JOIN categorie c ON p.id_categorie = c.id_categorie GROUP BY c.rayon ORDER BY taux_retour_pct DESC;

-- ============================================================
-- Q17
-- ============================================================
SELECT ROUND(AVG(EXTRACT(DAY FROM (date_trunc('month', date_vente) + INTERVAL '1 month' - INTERVAL '1 day' - date_vente))), 1) AS delai_moyen_jours FROM vente;

-- ============================================================
-- Q18
-- ============================================================
SELECT COUNT(*) FROM client WHERE plafond_credit > 100000;

-- ============================================================
-- Q19
-- ============================================================
-- Q19 piège P1 : dedoublonnage exact
SELECT COUNT(*) FROM (SELECT DISTINCT id_client, id_produit, id_magasin, date_vente, montant_ttc FROM vente) t;

-- ============================================================
-- Q20
-- ============================================================
SELECT id_client FROM vente GROUP BY id_client HAVING COUNT(DISTINCT id_magasin) >= 3;

-- ============================================================
-- Q21
-- ============================================================
WITH ca_produit_magasin AS (SELECT id_magasin, id_produit, SUM(montant_ttc) AS ca FROM vente GROUP BY 1, 2), rang AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY id_magasin ORDER BY ca DESC) AS r FROM ca_produit_magasin) SELECT id_magasin, id_produit, ca FROM rang WHERE r = 1 ORDER BY id_magasin;

-- ============================================================
-- Q22
-- ============================================================
SELECT id_mode, ROUND(AVG(montant_remise / NULLIF(montant_ttc, 0)) * 100, 2) AS remise_moyenne_pct FROM vente WHERE montant_ttc > 0 GROUP BY id_mode ORDER BY id_mode;

-- ============================================================
-- Q23
-- ============================================================
-- Q23 piège P5 : compter les couples distincts (PAS un COUNT(DISTINCT) sur id_vente)
SELECT COUNT(*) FROM (SELECT DISTINCT id_client, id_produit FROM vente) t;

-- ============================================================
-- Q24
-- ============================================================
WITH obj AS (SELECT id_magasin, SUM(ca_objectif_ttc) AS objectif FROM objectif_magasin GROUP BY id_magasin), real AS (SELECT id_magasin, SUM(montant_ttc) AS realise FROM vente WHERE est_retour = FALSE GROUP BY id_magasin) SELECT r.id_magasin, r.realise - o.objectif AS ecart FROM real r JOIN obj o ON r.id_magasin = o.id_magasin ORDER BY ecart ASC LIMIT 5;

-- ============================================================
-- Q25
-- ============================================================
WITH ca_cat AS (SELECT c.rayon, EXTRACT(YEAR FROM v.date_vente)::INTEGER AS annee, SUM(v.montant_ttc) AS ca FROM vente v JOIN produit p ON v.id_produit = p.id_produit JOIN categorie c ON p.id_categorie = c.id_categorie GROUP BY 1, 2) SELECT rayon, MAX(CASE WHEN annee = 2025 THEN ca END) AS ca_2025, MAX(CASE WHEN annee = 2026 THEN ca END) AS ca_2026, MAX(CASE WHEN annee = 2026 THEN ca END) - MAX(CASE WHEN annee = 2025 THEN ca END) AS evolution FROM ca_cat GROUP BY rayon ORDER BY evolution DESC;

-- ============================================================
-- Q26
-- ============================================================
SELECT p.id_produit, p.prix_vente_ht, c.rayon FROM produit p JOIN categorie c ON p.id_categorie = c.id_categorie WHERE p.prix_vente_ht > (SELECT AVG(prix_vente_ht) FROM produit p2 WHERE p2.id_categorie = p.id_categorie) ORDER BY c.rayon, p.prix_vente_ht DESC;

-- ============================================================
-- Q27
-- ============================================================
-- Q27 piège P4 : jointure multiple (Bobo = ville, Bricolage = categorie)
SELECT COUNT(*) FROM vente v JOIN client c ON v.id_client = c.id_client JOIN produit p ON v.id_produit = p.id_produit JOIN categorie cat ON p.id_categorie = cat.id_categorie WHERE c.ville = 'Bobo-Dioulasso' AND cat.rayon = 'Bricolage';

-- ============================================================
-- Q28
-- ============================================================
-- Q28 : segmentation RFM
WITH rfm AS (SELECT c.id_client, MAX(v.date_vente) AS derniere_vente, COUNT(*) AS freq, SUM(v.montant_ttc) AS montant FROM client c LEFT JOIN vente v ON c.id_client = v.id_client GROUP BY c.id_client) SELECT id_client, CASE WHEN derniere_vente >= CURRENT_DATE - INTERVAL '90 days' AND freq >= 5 AND montant >= 500000 THEN 'champion' WHEN freq >= 3 THEN 'fidele' WHEN freq >= 1 THEN 'occasionnel' WHEN derniere_vente IS NULL THEN 'perdu' ELSE 'nouveau' END AS segment FROM rfm;

-- ============================================================
-- Q29
-- ============================================================
-- Q29 : tableau de bord mensuel 2025 avec LAG
WITH mensuel AS (SELECT EXTRACT(MONTH FROM date_vente)::INTEGER AS mois, SUM(montant_ttc) AS ca, COUNT(*) AS nb, ROUND(AVG(montant_ttc), 0) AS panier, SUM(CASE WHEN est_retour THEN 1 ELSE 0 END) AS retours FROM vente WHERE EXTRACT(YEAR FROM date_vente) = 2025 GROUP BY 1) SELECT mois, ca, nb, panier, retours, LAG(ca) OVER (ORDER BY mois) AS ca_mois_precedent FROM mensuel ORDER BY mois;

-- ============================================================
-- Q30
-- ============================================================
-- Q30 piège P6 : EXISTS vs IN (clients qui ont acheté TOUS les produits outillage)
SELECT c.id_client FROM client c WHERE NOT EXISTS (SELECT p.id_produit FROM produit p JOIN categorie cat ON p.id_categorie = cat.id_categorie WHERE cat.rayon = 'Bricolage' AND cat.sous_categorie = 'Outillage' AND NOT EXISTS (SELECT 1 FROM vente v WHERE v.id_client = c.id_client AND v.id_produit = p.id_produit));

