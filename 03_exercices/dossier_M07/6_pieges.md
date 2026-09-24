# 6 pièges de fiabilité — projet M07.P

Trois pièges **dans les données** (P1, P2, P3) et trois pièges **dans la requête** (P4, P5, P6).
Une réponse juste exige de **repérer** le piège avant de poser la requête.

## P1 — Doublon exact (données)

8 lignes de `vente` sont des copies exactes d'autres lignes (mêmes colonnes, `id_vente` différent).

**Question concernée :** Q19. Un `COUNT(*)` naïf retourne 50 008 lignes. La requête juste passe par `DISTINCT`.

```sql
SELECT COUNT(*) FROM vente; -- 50008 (FAUX)
SELECT COUNT(*) FROM (SELECT DISTINCT id_client, id_produit, id_magasin, date_vente, montant_ttc FROM vente) t; -- 50000 (JUSTE)
```

## P2 — Retour inclus par erreur (données)

200 lignes ont `est_retour = TRUE` mais une `quantite > 0` et un `montant_ttc > 0` (au lieu de `< 0`).

**Question concernée :** Q09. Le CA total gonfle de 5 à 8 %.

```sql
SELECT SUM(montant_ttc) FROM vente; -- gonfle
SELECT SUM(montant_ttc) FROM vente WHERE est_retour = FALSE; -- juste
```

## P3 — Date inversée (données)

15 ventes ont `date_vente > date_limite_remise` (la remise était applicable jusqu'au 15, mais la vente est du 20+).

**Question concernée :** Q14. Le CA par mois dépend de la convention (date de vente vs date de remise).

```sql
SELECT EXTRACT(MONTH FROM date_vente), SUM(montant_ttc) FROM vente GROUP BY 1; -- ambigu
SELECT EXTRACT(MONTH FROM date_vente), SUM(montant_ttc) FROM vente WHERE date_vente <= date_limite_remise GROUP BY 1; -- juste
```

## P4 — Jointure multiple qui double (requête)

Une jointure 4 tables (vente × client × produit × categorie) avec une condition `WHERE` mal placée compte plusieurs fois la même vente.

**Question concernée :** Q27. Vérifier que `COUNT(DISTINCT v.id_vente)` est utilisé, ou que les jointures sont en étoile (1-N).

```sql
SELECT COUNT(*) FROM vente v JOIN client c ON ... JOIN produit p ON ... JOIN categorie cat ON ... WHERE c.ville = 'Bobo-Dioulasso' AND cat.rayon = 'Bricolage'; -- peut doubler
SELECT COUNT(DISTINCT v.id_vente) FROM ... ; -- juste
```

## P5 — `DISTINCT` qui masque un mauvais JOIN (requête)

Un `COUNT(DISTINCT col)` peut donner le bon résultat par hasard, alors que la jointure est fausse. Le `DISTINCT` masque le doublon.

**Question concernée :** Q23. Toujours vérifier le nombre de lignes avant agrégation, pas après.

```sql
SELECT COUNT(DISTINCT id_client, id_produit) FROM vente JOIN produit ON ... WHERE categorie = ...; -- peut masquer
SELECT id_client FROM vente WHERE id_produit IN (SELECT id_produit FROM produit WHERE categorie = ...) GROUP BY id_client HAVING COUNT(DISTINCT id_produit) = (SELECT COUNT(*) FROM produit WHERE categorie = ...); -- juste
```

## P6 — `EXISTS` vs `IN` (requête)

Une requête `WHERE id_client IN (SELECT ...)` peut être très lente sur de grandes tables. `NOT EXISTS` avec `NOT EXISTS ... NOT EXISTS` est le pattern canonique pour *« tous les »*.

**Question concernée :** Q30. La question « quels clients ont acheté tous les produits X » ne se fait pas avec `IN` ni `COUNT`, mais avec une double négation.

```sql
SELECT id_client FROM client WHERE id_client IN (SELECT id_client FROM vente ...); -- faux (donne ceux qui ont acheté au moins 1)
SELECT id_client FROM client c WHERE NOT EXISTS (SELECT 1 FROM produit p WHERE NOT EXISTS (SELECT 1 FROM vente v WHERE v.id_client = c.id_client AND v.id_produit = p.id_produit)); -- juste (« tous les »)
```

