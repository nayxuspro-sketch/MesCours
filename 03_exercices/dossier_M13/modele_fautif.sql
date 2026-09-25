-- modele_fautif.sql — les modeles qui donnent un chiffre d'affaires faux
--
-- Ecrit par `tools/dossier_M13.py`. Ne pas modifier a la main : regenerer.
--
-- Ces trois vues sont les trois erreurs de modelisation les plus courantes du
-- chapitre C03 et de l'etude de cas :
--   * `ca_deux_tableaux`  : on additionne deux tables qui portent TOUTES LES DEUX
--                           un montant, sans verifier qu'elles parlent du meme fait ;
--   * `ca_trois_tableaux` : on y ajoute les encaissements — trois fois le meme
--                           argent, compte trois fois ;
--   * `ca_jointure_folle` : on joint les ventes a la logistique sur le magasin
--                           seul, et chaque ligne de vente est repetee 44 fois.

CREATE OR REPLACE VIEW ca_deux_tableaux AS
SELECT (SELECT SUM(montant_ttc) FROM ventes WHERE NOT est_retour)
     + (SELECT SUM(montant_ttc) FROM commande) AS ca;

CREATE OR REPLACE VIEW ca_trois_tableaux AS
SELECT (SELECT SUM(montant_ttc) FROM ventes WHERE NOT est_retour)
     + (SELECT SUM(montant_ttc) FROM commande)
     + (SELECT SUM(montant_encaisse) FROM encaissement) AS ca;

CREATE OR REPLACE VIEW ca_jointure_folle AS
SELECT SUM(v.montant_ttc) AS ca
FROM ventes v JOIN logistique l ON l.id_magasin = v.id_magasin
WHERE NOT v.est_retour;
