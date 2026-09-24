-- 30_questions.sql — énoncés des 30 questions métier du projet M07.P
-- 6 faciles (1 ligne), 12 moyennes (2-5 lignes), 9 avancées (5-15 lignes avec WITH),
-- 3 expert (jointure 4 tables + CASE). 6 « pièges de fiabilité » (Q09, Q14, Q19, Q23, Q27, Q30).
-- Voir 6_pieges.md pour l'explication des pièges et 30_reponses.sql pour le corrigé.

-- Q01 — Combien de clients a la base ?
-- Votre reponse ici :



-- Q02 — Combien de produits actifs ?
-- Votre reponse ici :



-- Q03 — Combien de magasins ? Dans quelles villes ?
-- Votre reponse ici :



-- Q04 — Quel est le montant TTC total de toutes les ventes (sans filtre) ?
-- Votre reponse ici :



-- Q05 — Combien de modes de paiement existent ? Listez-les.
-- Votre reponse ici :



-- Q06 — Quelle est la date de la première et de la dernière vente ?
-- Votre reponse ici :



-- Q07 — Quel est le CA TTC par magasin (sans filtre retour) ? Triez par CA décroissant.
-- Votre reponse ici :



-- Q08 — Combien de ventes par mois pour l'annee 2025 ? Triez par mois croissant.
-- Votre reponse ici :



-- Q09 — PIEGE P2 : Quel est le CA TTC total ? (sans filtrer les retours)
-- Votre reponse ici :



-- Q10 — Quel est le panier moyen (montant_ttc moyen par vente) ?
-- Votre reponse ici :



-- Q11 — Quels sont les 10 produits les plus vendus (en quantite cumulee) ?
-- Votre reponse ici :



-- Q12 — Quels sont les 5 meilleurs clients par CA total ?
-- Votre reponse ici :



-- Q13 — Combien de clients distincts ont achete dans chaque magasin ?
-- Votre reponse ici :



-- Q14 — PIEGE P3 : Quel est le CA par mois, en considerant date_vente et date_limite_remise ?
-- Votre reponse ici :



-- Q15 — Combien de ventes ont eu lieu un dimanche ? (utilisez EXTRACT(DOW))
-- Votre reponse ici :



-- Q16 — Quel est le taux de retour par categorie de produit (nombre_retours / total_ventes) ?
-- Votre reponse ici :



-- Q17 — Quel est le delai moyen (en jours) entre date_vente et la fin du mois ?
-- Votre reponse ici :



-- Q18 — Combien de clients ont un plafond_credit > 100 000 FCFA ?
-- Votre reponse ici :



-- Q19 — PIEGE P1 : Combien de ventes uniques (apres dedoublonnage exact) ?
-- Votre reponse ici :



-- Q20 — Quels clients ont achete dans 3 magasins ou plus ?
-- Votre reponse ici :



-- Q21 — Pour chaque magasin, quel est le top 1 produit par CA ?
-- Votre reponse ici :



-- Q22 — Quelle est la marge moyenne par mode_paiement (taux de remise moyen) ?
-- Votre reponse ici :



-- Q23 — PIEGE P5 DISTINCT : Combien de couples (client, produit) distincts ?
-- Votre reponse ici :



-- Q24 — Classez les magasins par ecart entre CA realisé et objectif (top 5 des écarts négatifs).
-- Votre reponse ici :



-- Q25 — Quelle est la categorie dont le CA a le plus progresse entre 2025 et 2026 ?
-- Votre reponse ici :



-- Q26 — Quels produits ont un prix_vente_ht superieur au prix moyen de leur categorie ?
-- Votre reponse ici :



-- Q27 — PIEGE P4 jointure multiple : Combien de ventes implique au moins un client de Bobo et un produit de categorie Bricolage ?
-- Votre reponse ici :



-- Q28 — Creez une segmentation RFM (Recence, Frequence, Montant) des clients en 5 categories (champions, fideles, occasionnels, nouveaux, perdus).
-- Votre reponse ici :



-- Q29 — Pour chaque mois de 2025, calculez le CA, le nombre de ventes, le panier moyen et le taux de retour. Affichez aussi l'evolution mois par mois (LAG).
-- Votre reponse ici :



-- Q30 — PIEGE P6 EXISTS vs IN : Quels clients ont achete TOUS les produits de categorie 'Bricolage' (sous-categorie 'Outillage') ?
-- Votre reponse ici :



