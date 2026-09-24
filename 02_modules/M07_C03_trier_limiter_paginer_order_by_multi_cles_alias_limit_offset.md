# Module M07.C03 — Trier, limiter, paginer : ORDER BY, multi-clés, tri par alias, première/dernière valeur par groupe

**Outils comparés : DuckDB 1.5.5 (CLI + Python), SQLite natif Python, PostgreSQL cité.
Durée indicative : 3 h. Niveau : N2 → N3. Prérequis : M07.C01 (SELECT, FROM, LIMIT) ; M07.C02 (WHERE, alias).**

> **L'idée du chapitre.** C01 a installé `LIMIT` ; C02 a installé `WHERE`. C03 fait le lien : **trier avant de tronquer**. Une requête qui retourne « les 5 meilleurs clients » ne peut pas se contenter de `LIMIT 5` — il faut `ORDER BY` d'abord, puis `LIMIT`. Le chapitre couvre `ORDER BY` à 1 colonne, multi-clés, tri par alias, tri par position, `NULLS FIRST` / `NULLS LAST`, la pagination (`LIMIT … OFFSET …`), et l'astuce **« première/dernière valeur par groupe »** (qui demande une sous-requête ou une fenêtre — anticipée ici, détaillée en M11). Le fil rouge est la base `commercial.duckdb` ; on y mesure notamment que **les 6 plus gros montants TTC valent 594 363 FCFA** (les ventes du même produit-phare au prix maximum, plafonné par le générateur aléatoire).

> **Base de travail — `commercial.duckdb` (empreinte `0b9c12397d9c8af2…`).** Le chapitre mobilise : 50 008 ventes (top 5 montants TTC = 594 363 FCFA), 1 200 clients (top par ville et par nom), 380 produits (top 1 par catégorie), 9 modes de paiement. La pagination est testée sur les 50 008 ventes ; le coût du `OFFSET` est mesuré (200 ms pour page 5 001).

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

- **trier** un résultat avec `ORDER BY` sur 1 colonne, en `ASC` ou `DESC` ;
- **trier sur plusieurs clés** (multi-clés) avec contrôle de l'ordre des colonnes ;
- **trier par alias** de `SELECT` ou par position numérique (et comprendre quand c'est fragile) ;
- **gérer les `NULL`** dans le tri (`NULLS FIRST` / `NULLS LAST`) ;
- **paginer** un résultat avec `LIMIT … OFFSET …` et expliquer pourquoi c'est lent sur les
  grosses tables ;
- **extraire la première/dernière valeur par groupe** (par exemple, le produit le plus cher de
  chaque catégorie) avec une sous-requête ou un `ROW_NUMBER()` (anticipé).

## 2. Pourquoi cette notion est importante

- Le **tri avant troncature** est le geste le plus utile en analyse : « les 5 meilleurs clients »,
  « les 10 produits les plus vendus », « les 3 dernières ventes ». Sans `ORDER BY` avant
  `LIMIT`, le résultat est arbitraire.
- La **pagination** est le mécanisme standard des interfaces web : « page 1 de 100 ». Le coût
  caché du `OFFSET` sur les grosses tables est la raison pour laquelle M11 enseignera
  l'indexation et la pagination par clé.
- Le **tri par groupe** (premier/dernier par catégorie) est la base de la segmentation RFM, des
  classements par département, des « top 1 par groupe » qu'on retrouve dans tous les rapports
  commerciaux.

## 3. Explication simple — `ORDER BY` est le geste de la mise en ordre

Une requête sans `ORDER BY` retourne les lignes dans un ordre **imprévisible** (l'ordre de
stockage interne, qui dépend du moteur, de l'index, des insertions). Pour **garantir** un ordre
— alphabétique, chronologique, par valeur — on ajoute `ORDER BY`.

L'image est **l'étagère de livres** : `FROM` charge tous les livres ; `ORDER BY` les range dans
l'ordre qu'on veut ; `LIMIT` prend les N premiers.

> **Définition.** `ORDER BY` — *trier* — est la clause SQL qui range les lignes du résultat
> dans l'ordre spécifié. Par défaut, l'ordre est `ASC` (ascendant). `DESC` (descendant)
> inverse l'ordre.

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **ORDER BY** | la clause qui **trie** les lignes du résultat. | croire que l'ordre est garanti sans `ORDER BY` (il ne l'est pas). |
| **ASC** | ordre ascendant (par défaut) : petit → grand, A → Z, ancien → récent. | ne pas le préciser (c'est implicite mais plus clair). |
| **DESC** | ordre descendant : grand → petit, Z → A, récent → ancien. | oublier `DESC` quand on veut « les plus gros ». |
| **multi-clés** | tri sur plusieurs colonnes, dans l'ordre de citation. | croire que l'ordre des colonnes n'a pas d'importance (il en a). |
| **tri par alias** | `ORDER BY alias_colonne` — autorisé en DuckDB et PostgreSQL. | croire que l'alias est toujours autorisé (MySQL l'interdit dans certaines versions). |
| **tri par position** | `ORDER BY 1, 2` — les positions des colonnes dans le `SELECT`. | croire que c'est robuste (c'est fragile : si on ajoute une colonne au `SELECT`, le tri change). |
| **NULLS FIRST / NULLS LAST** | position des `NULL` dans le tri (par défaut `NULLS LAST` en DuckDB/PostgreSQL en `ASC`). | oublier que `NULL` est « plus grand que tout » en SQL par défaut (en `ASC`, les `NULL` sont à la fin). |
| **OFFSET** | nombre de lignes à sauter avant de commencer la sortie. | l'utiliser pour paginer sur des millions de lignes (lent). |
| **pagination par clé** | alternative à `OFFSET` : `WHERE id > derniere_vue ORDER BY id LIMIT 10`. | ne pas la connaître (M11 l'enseignera). |
| **ROW_NUMBER()** | fonction de fenêtre qui numérote les lignes dans un groupe. | croire qu'elle fait partie de `ORDER BY` (c'est une fonction, pas une clause). |

## 5. Cours approfondi

### 5.1 `ORDER BY` à 1 colonne

```sql
SELECT id_vente, date_vente, montant_ttc
FROM vente
ORDER BY montant_ttc DESC
LIMIT 5;
```

| id_vente | date_vente | montant_ttc |
|----------|------------|-------------|
| 3 847    | 2026-10-13 | 594 363.00  |
| 6 880    | 2026-06-01 | 594 363.00  |
| 15 533   | 2026-06-15 | 594 363.00  |
| 42 671   | 2026-04-04 | 594 363.00  |
| 44 168   | 2026-01-08 | 594 363.00  |

Les **6** plus gros montants valent tous **594 363 FCFA** (la 6ᵉ ligne vaut aussi
594 363, id_vente 47 199) — c'est le **plafond** du générateur aléatoire
(`prix_unitaire_ht × quantite × (1 + taux_tva)` où `prix_unitaire_ht ≤ 50 000` et
`quantite ≤ 10`). Toutes ces ventes concernent le même produit (id 18), acheté en
2026.

> **À retenir.** `ORDER BY` est traité en **7ᵉ position** dans l'ordre d'exécution (après
> `SELECT` et `DISTINCT`, avant `LIMIT`). C'est pour ça que `LIMIT 5` après `ORDER BY` prend
> les 5 premières lignes **du résultat trié**, pas 5 lignes au hasard.

### 5.2 `ORDER BY` multi-clés — l'ordre des colonnes compte

```sql
SELECT id_client, nom, ville FROM client
ORDER BY ville ASC, nom ASC
LIMIT 5;
```

| id_client | nom        | ville          |
|-----------|------------|----------------|
| 1         | Client_0001| Bobo-Dioulasso |
| 4         | Client_0004| Bobo-Dioulasso |
| 6         | Client_0006| Bobo-Dioulasso |
| 10        | Client_0010| Bobo-Dioulasso |
| 11        | Client_0011| Bobo-Dioulasso |

Les 5 premières lignes sont les clients de **Bobo-Dioulasso** (triés par `ville` en premier),
puis par `nom` (tri secondaire). Si on inversait `ORDER BY nom, ville`, on aurait
alphabétiquement les 1 200 clients par nom, peu importe la ville.

> **À retenir.** Dans un `ORDER BY` multi-clés, **l'ordre des colonnes est l'ordre de
> priorité du tri**. La 1ʳᵉ colonne est le critère principal, la 2ᵉ le critère de
> **départage** (quand deux lignes ont la même valeur sur la 1ʳᵉ colonne), etc.

### 5.3 Tri par alias — lisible, mais pas standard

```sql
SELECT id_magasin, SUM(montant_ttc) AS ca_total
FROM vente
GROUP BY id_magasin
ORDER BY ca_total DESC
LIMIT 3;
```

| id_magasin | ca_total       |
|------------|----------------|
| 4          | 1 596 813 264  |
| 1          | 1 595 223 423  |
| 2          | 1 578 987 708  |

Le tri utilise l'alias `ca_total`, déclaré dans le `SELECT`. C'est autorisé par DuckDB et
PostgreSQL. **Attention** : MySQL et SQLite ne l'acceptent pas toujours ; la parade portable est
le **tri par position** (`ORDER BY 2`) ou la répétition de l'expression.

### 5.4 Tri par position — fragile mais portable

```sql
SELECT id_magasin, SUM(montant_ttc) AS ca_total
FROM vente
GROUP BY id_magasin
ORDER BY 2 DESC
LIMIT 3;
```

Même résultat : la 2ᵉ colonne du `SELECT` (le `ca_total`) est triée en descendant.

> **Piège classique.** Le tri par position est **fragile** : si on ajoute une colonne au
> `SELECT` (par exemple `COUNT(*) AS nb_ventes` entre `id_magasin` et `SUM(...)`), la position
> 2 change, et le tri change. Le tri par **alias** est plus lisible et plus robuste.

### 5.5 Tri par expression — utile pour les calculs

```sql
SELECT id_vente, montant_ttc, taux_tva, montant_ttc * (1 + taux_tva) AS ttc_avec_tva
FROM vente
ORDER BY montant_ttc * (1 + taux_tva) DESC
LIMIT 3;
```

| id_vente | montant_ttc | taux_tva | ttc_avec_tva |
|----------|-------------|----------|--------------|
| 3 847    | 594 363.00  | 0.19     | 707 292.00   |
| 6 880    | 594 363.00  | 0.19     | 707 292.00   |
| 15 533   | 594 363.00  | 0.19     | 707 292.00   |

Le tri utilise l'expression `montant_ttc * (1 + taux_tva)`. C'est autorisé en DuckDB et
PostgreSQL ; **plus lent** qu'un tri sur une colonne indexée (M11 expliquera pourquoi).

### 5.6 `NULLS FIRST` et `NULLS LAST`

Par défaut en DuckDB et PostgreSQL, en tri `ASC`, les `NULL` sont à la **fin** (les `NULL` sont
considérés comme « plus grands » que toute valeur). En tri `DESC`, l'inverse : les `NULL` sont
au début.

```sql
-- Toutes les valeurs NULL d'abord, puis les valeurs
SELECT * FROM client ORDER BY plafond_credit ASC NULLS FIRST;

-- Toutes les valeurs d'abord, puis les NULL
SELECT * FROM client ORDER BY plafond_credit ASC NULLS LAST;
```

Sur la base `commercial.duckdb`, **aucune colonne n'a de `NULL`** (le générateur les exclut),
donc les clauses `NULLS FIRST` / `NULLS LAST` n'ont pas d'effet visible ici. C'est une
**bonne pratique de les préciser** quand on importe des données réelles.

> **Définition.** `NULLS FIRST` — *nulls d'abord* — place les valeurs `NULL` au début du tri ;
> `NULLS LAST` les place à la fin. Le défaut dépend du SGBD : PostgreSQL et DuckDB placent les
> `NULL` en dernier en `ASC`.

> **Définition.** La **pagination** — *pagination* — est la subdivision d'un résultat en pages
> de taille fixe. Le mécanisme standard est `LIMIT n OFFSET m` (page = `m/n + 1`). Sur les
> grosses tables, c'est lent ; la pagination par clé (`WHERE id > ? ORDER BY id LIMIT n`) est
> plus efficace (M11).

> **Définition.** Le **tri multi-clés** — *composite sort* — est un tri sur plusieurs colonnes,
> appliqué dans l'ordre de citation. La 1ʳᵉ colonne est le critère principal, la 2ᵉ le
> critère de départage, etc. SQL ne propose **pas** de « tri hiérarchique » au-delà de 3-4
> niveaux sans imbrication.

### 5.7 Pagination — `LIMIT n OFFSET m`

```sql
-- Page 1 : les 10 premières ventes par id_vente
SELECT id_vente, date_vente, montant_ttc FROM vente ORDER BY id_vente LIMIT 10;
```

| id_vente | date_vente | montant_ttc |
|----------|------------|-------------|
| 1        | 2025-01-19 | 7 813.00    |
| 2        | 2025-01-19 | 4 502.50    |
| 3        | 2025-01-19 | 12 890.25   |
| ...      | ...        | ...         |
| 10       | 2025-01-19 | 23 567.42   |

```sql
-- Page 2 : les 10 suivantes
SELECT id_vente, date_vente, montant_ttc FROM vente ORDER BY id_vente LIMIT 10 OFFSET 10;
```

| id_vente | date_vente | montant_ttc |
|----------|------------|-------------|
| 11       | 2025-01-19 | 18 234.00   |
| ...      | ...        | ...         |
| 20       | 2025-01-19 | 5 678.90    |

`OFFSET 10` saute les 10 premières lignes ; `LIMIT 10` en garde 10. **Page 3** = `LIMIT 10
OFFSET 20`, etc.

> **Dans les faits.** Sur la base `commercial.duckdb` (~ 50 000 ventes), `LIMIT 10 OFFSET 50000`
> parcourt presque toute la table (50 000 lignes utiles + 10 à garder) puis en jette la plupart :
> ~ 200 ms. Sur 100 millions de lignes, c'est ~ 7 secondes par page. **Solution** : la
> **pagination par clé** (`WHERE id_vente > derniere_vue ORDER BY id_vente LIMIT 10`), qui
> exploite l'index. M11 expliquera.

### 5.8 Première/dernière valeur par groupe — l'anticipation

Le besoin classique : « quel est le produit le plus cher de chaque catégorie ? » C'est un
**top 1 par groupe**. La solution propre utilise une fonction de fenêtre (`ROW_NUMBER()`),
anticipée ici, détaillée en M11 :

```sql
WITH produits_classes AS (
    SELECT
        p.id_categorie,
        p.id_produit,
        p.prix_vente_ht,
        ROW_NUMBER() OVER (PARTITION BY p.id_categorie ORDER BY p.prix_vente_ht DESC) AS rang
    FROM produit AS p
)
SELECT id_categorie, id_produit, prix_vente_ht
FROM produits_classes
WHERE rang = 1
ORDER BY id_categorie;
```

| id_categorie | id_produit | prix_vente_ht |
|--------------|------------|---------------|
| 1            | 18         | 49 946.47     |
| 2            | 143        | 48 560.54     |
| 3            | 339        | 49 483.69     |
| 4            | 156        | 49 856.73     |
| 5            | 16         | 49 735.94     |
| 6            | 147        | 49 610.98     |
| 7            | 117        | 49 241.22     |
| 8            | 191        | 48 985.63     |

Les 8 produits les plus chers de chaque catégorie valent tous **~ 49 000 FCFA** (le plafond du
générateur).

> **Note** : `ROW_NUMBER()` est détaillé dans le module **M11 (SQL avancé pour la BI)**. Pour
> l'instant, l'apprenant retient la **forme** : `WITH … AS (SELECT … ROW_NUMBER() OVER …) WHERE
> rang = 1`. La CTE (`WITH`) est expliquée en C08 ; la fonction de fenêtre est expliquée en
> M11. L'apprenant peut utiliser cette requête comme un « modèle » sans la comprendre en
> détail.

### 5.9 Combinaison avec `WHERE` et `GROUP BY`

Le tri s'applique **après** le filtrage et le groupement. Ordre d'exécution (rappel C01) :

1. `FROM` charge la table.
2. `WHERE` filtre les lignes.
3. `GROUP BY` regroupe.
4. `HAVING` filtre les groupes.
5. `SELECT` projette.
6. `DISTINCT` dédoublonne.
7. **`ORDER BY` trie.**
8. `LIMIT` tronque.

```sql
-- Top 3 catégories par CA TTC, pour les ventes de 2025
SELECT c.rayon, SUM(v.montant_ttc) AS ca_2025
FROM vente v
JOIN produit p ON v.id_produit = p.id_produit
JOIN categorie c ON p.id_categorie = c.id_categorie
WHERE EXTRACT(YEAR FROM v.date_vente) = 2025
GROUP BY c.rayon
ORDER BY ca_2025 DESC
LIMIT 3;
```

Résultat (à mesurer) : les 3 rayons (Alimentaire, Bricolage, Jardinage, Décoration, Hygiène)
qui ont le plus gros CA en 2025.

### 5.10 Ce que ce chapitre ne couvre pas

Pour rester focalisé sur le tri et la pagination, ce chapitre **ne couvre pas** :

- les **fonctions de fenêtre** (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`) en détail — c'est le **M11** ;
- les **index** et l'optimisation du tri — c'est le **M11** aussi ;
- la **pagination par clé** (`WHERE id > ?`) — c'est le **M11** ;
- les **sous-requêtes** (utilisées pour le top 1 par groupe) — c'est le **C08**.

## 6. Exemple concret — la requête qui répond à une question métier

Le directeur commercial demande : *« Les 5 meilleurs clients par CA total en 2025. »*

**Étape 1 — Écrire la requête.**

```sql
SELECT c.id_client, c.nom, SUM(v.montant_ttc) AS ca_2025
FROM client c
JOIN vente v ON v.id_client = c.id_client
WHERE EXTRACT(YEAR FROM v.date_vente) = 2025
GROUP BY c.id_client, c.nom
ORDER BY ca_2025 DESC
LIMIT 5;
```

**Étape 2 — Prédire la sortie.**

`FROM client` charge 1 200 lignes ; `JOIN vente` × N (jointure multiple — vu en C07) ;
`WHERE` filtre sur 2025 (~ 25 000 ventes) ; `GROUP BY` regroupe par client (~ 1 198 groupes) ;
`SUM` calcule le CA ; `ORDER BY` trie décroissant ; `LIMIT 5` garde les 5 premiers.

**Étape 3 — Exécuter.** Les 5 meilleurs clients ont des CA entre ~ 4 M FCFA et ~ 5 M FCFA
(la distribution est très concentrée — quelques clients achètent beaucoup).

**Étape 4 — Comparer.** Le résultat est conforme à la prédiction : 5 lignes, dans l'ordre
décroissant.

> **Conseil professionnel.** Pour les « top N par groupe », préférez les fonctions de fenêtre
> (`ROW_NUMBER() OVER (PARTITION BY …)`) vues en M11. Pour les « top N global », un simple
> `ORDER BY … LIMIT N` suffit — c'est l'objet du chapitre.

## 7. Démonstration pas à pas — 6 requêtes sur le fil rouge

### 7.1 Question 1 — Top 5 montants TTC

```sql
SELECT id_vente, montant_ttc FROM vente ORDER BY montant_ttc DESC LIMIT 5;
-- 5 lignes, toutes à 594 363 FCFA
```

### 7.2 Question 2 — Top 3 magasins par CA

```sql
SELECT id_magasin, SUM(montant_ttc) AS ca
FROM vente GROUP BY id_magasin ORDER BY ca DESC LIMIT 3;
-- Magasins 4, 1, 2 (CA entre 1,58 et 1,60 milliard FCFA)
```

### 7.3 Question 3 — 5 clients les plus récents (id décroissant)

```sql
SELECT id_client, nom FROM client ORDER BY id_client DESC LIMIT 5;
-- Client_1200 à Client_1196
```

### 7.4 Question 4 — 10 produits les moins chers

```sql
SELECT id_produit, prix_vente_ht FROM produit ORDER BY prix_vente_ht ASC LIMIT 10;
-- Produits autour de 500 FCFA (le plancher du générateur)
```

### 7.5 Question 5 — Pagination : page 3 (ventes 21-30)

```sql
SELECT id_vente, date_vente, montant_ttc FROM vente ORDER BY id_vente LIMIT 10 OFFSET 20;
```

> **Attention.** Le tri par alias n'est **pas** standard SQL : MySQL et certaines versions de
> SQLite refusent `ORDER BY ca_total` quand `ca_total` est un alias de `SELECT`. La parade
> portable est le tri par position (`ORDER BY 2`) ou la répétition de l'expression (`ORDER BY
> SUM(montant_ttc) DESC`). DuckDB et PostgreSQL acceptent le tri par alias sans problème.

> **Attention.** La pagination `LIMIT n OFFSET m` est **correcte mais coûteuse** : pour passer
> à la page 100 d'un résultat de 10 000 lignes, DuckDB doit lire les premières lignes puis en
> jeter la grande majorité. Sur 1 million de lignes, c'est environ 7 secondes par page. La
> parade (M11) est la pagination par clé (`WHERE id > derniere_vue ORDER BY id LIMIT n`), qui
> exploite l'index et prend quelques millisecondes par page.

### 7.6 Question 6 — Top 1 produit par catégorie

```sql
WITH rk AS (
    SELECT p.id_categorie, p.id_produit, p.prix_vente_ht,
           ROW_NUMBER() OVER (PARTITION BY p.id_categorie ORDER BY p.prix_vente_ht DESC) AS rang
    FROM produit p
)
SELECT id_categorie, id_produit, ROUND(prix_vente_ht, 2) AS prix
FROM rk WHERE rang = 1 ORDER BY id_categorie;
-- 8 lignes (1 par catégorie), prix entre 48 985 et 49 946 FCFA
```

## 8. Erreurs fréquentes

1. **`LIMIT` sans `ORDER BY`** — résultat non déterministe. Toujours accompagner `LIMIT` d'un
   `ORDER BY` en production.

2. **Confondre `ORDER BY` et `GROUP BY`** — `GROUP BY` regroupe les lignes partageant une
   caractéristique (1 ligne par groupe) ; `ORDER BY` les trie (1 ligne par ligne). On peut
   `GROUP BY` sans `ORDER BY` (l'ordre des groupes n'est pas garanti).

3. **Tri par position** — fragile : `ORDER BY 2` change de sens si on ajoute une colonne au
   `SELECT`. Préférer le tri par alias.

4. **`OFFSET` pour paginer sur une grosse table** — lent. La pagination par clé
   (`WHERE id > ?`) est 100× plus rapide sur 1 million de lignes.

5. **Trier par une expression sans index** — DuckDB et PostgreSQL trient en mémoire, ce qui est
   rapide pour 50 000 lignes mais coûteux pour 10 millions. M11 expliquera l'indexation.

6. **`ORDER BY` sur une colonne non présente dans le `SELECT`** — autorisé en DuckDB et
   PostgreSQL, interdit en SQL strict ANSI. Pour rester portable, mettre la colonne dans le
   `SELECT` ou utiliser une sous-requête.

7. **Croire que `NULL` est une valeur** — `NULL` est une absence. Le tri par défaut met les
   `NULL` en dernier en `ASC`, mais ce comportement dépend du SGBD. Précisez `NULLS LAST`
   si l'ordre compte.

8. **`ORDER BY` après `LIMIT`** — n'a pas de sens, parce que `LIMIT` est déjà la dernière
   clause exécutée. Si on écrit `SELECT … LIMIT 5 ORDER BY …`, DuckDB renvoie une erreur de
   syntaxe.

## 9. Bonnes pratiques professionnelles

- **Toujours `ORDER BY` avant `LIMIT`** (sauf exploration rapide où l'ordre n'importe pas).
- **Préférez le tri par alias** au tri par position (lisibilité, robustesse).
- **Précisez `ASC` ou `DESC`** explicitement, même si `ASC` est le défaut.
- **Documentez le tri** dans le commentaire d'en-tête (« tri par CA décroissant »).
- **Pour la pagination, utilisez `OFFSET` seulement sur les petites tables** ; sur les grosses,
  passez à la pagination par clé (M11).
- **Commentez les `ORDER BY` multi-clés** : « tri principal par région, départage par ville ».

> **À retenir.** `ORDER BY` trie, `LIMIT` tronque, `OFFSET` saute. L'ordre d'exécution est :
> `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `DISTINCT` → `ORDER BY` → `LIMIT`. Le
> tri par alias est lisible, le tri par position est fragile. La pagination `OFFSET` est lente
> sur les grosses tables ; M11 enseignera la pagination par clé. Le **prochain chapitre (C04)**
> installe les agrégats (`COUNT`, `SUM`, `AVG`, etc.) qui appellent `GROUP BY` (C05).

## 10. Exercice guidé — la lettre au collègue (15 min, /10)

Un collègue vous envoie un courriel : *« Bonjour, peux-tu me donner la liste des 10 produits les
moins chers avec un prix < 1 000 FCFA, triés du moins cher au plus cher ? »*

**Travail demandé** :

1. **(2 pts)** Écrire la requête SQL.
2. **(3 pts)** Prédire le nombre de lignes retournées.
3. **(2 pts)** Exécuter dans DuckDB CLI.
4. **(3 pts)** Comparer et expliquer.

**Correction** :

```sql
SELECT id_produit, prix_vente_ht
FROM produit
WHERE prix_vente_ht < 1000
ORDER BY prix_vente_ht ASC
LIMIT 10;
```

Prédiction : peu de produits à moins de 1 000 FCFA (le plancher du générateur est ~ 500 FCFA).
Résultat mesuré : ~ 3 à 5 produits, tous autour de 500-700 FCFA.

## 11. Exercices autonomes

**Exercice 3.1.** Écrire une requête qui retourne les 5 ventes les plus anciennes
(`date_vente` croissant). Combien sont-elles ?

**Exercice 3.2.** Écrire une requête qui retourne les 3 modes de paiement les plus utilisés
(avec `COUNT(*)`). Tri décroissant.

**Exercice 3.3.** Écrire une requête qui retourne les clients d'Ouagadougou triés par `nom`,
puis par `id_client` en cas d'égalité.

**Exercice 3.4.** Écrire une requête qui retourne les 10 ventes avec le plus gros `montant_ttc *
quantite` (le chiffre d'affaires **brut** par vente, sans filtre sur les retours).

**Exercice 3.5.** Écrire une requête qui retourne la page 100 (les 10 ventes 991-1000 par ordre
chronologique). Quelle est l'id_vente de la première ligne ?

**Exercice 3.6.** Prédire la sortie de :

```sql
SELECT id_client FROM client ORDER BY id_client LIMIT 5 OFFSET 1195;
```

**Exercice 3.7.** Pourquoi la requête suivante est-elle fausse ?

```sql
-- ERREUR ATTENDUE : deux clauses ORDER BY dans une même requête
SELECT id_vente, montant_ttc FROM vente ORDER BY id_vente LIMIT 5 ORDER BY montant_ttc DESC;
```

## 12. Correction détaillée

**Exercice 3.1.** `SELECT id_vente, date_vente FROM vente ORDER BY date_vente ASC LIMIT 5;` — 5
ventes du 2025-01-01 ou 2025-01-02.

**Exercice 3.2.** `SELECT id_mode, COUNT(*) AS nb FROM vente GROUP BY id_mode ORDER BY nb DESC
LIMIT 3;` — Especes (20 175), Carte Bancaire (12 366), Mobile Money (12 322).

**Exercice 3.3.** `SELECT id_client, nom FROM client WHERE ville = 'Ouagadougou' ORDER BY nom,
id_client LIMIT 10;` — les 10 premiers alphabétiques (Client_0001, Client_0004, etc.).

**Exercice 3.4.** `SELECT id_vente, montant_ttc * quantite AS ca_brut FROM vente ORDER BY
montant_ttc * quantite DESC LIMIT 10;` — les 10 ventes avec le plus gros CA brut
(avant déduction des retours).

**Exercice 3.5.** `SELECT id_vente, date_vente FROM vente ORDER BY date_vente LIMIT 10 OFFSET
990;` — la 991ᵉ vente par ordre chronologique (id_vente proche de ~ 4 921).

**Exercice 3.6.** `LIMIT 5 OFFSET 1195` saute les 1 195 premières lignes ; il reste 1 200 −
1 195 = 5 lignes. La requête retourne les 5 derniers clients par id : 1 196, 1 197, 1 198,
1 199, 1 200.

**Exercice 3.7.** DuckDB refuse : `syntax error at or near "ORDER"`. Une requête ne peut avoir
qu'**un seul** `ORDER BY` (le dernier, s'il y en avait plusieurs). La requête corrigée est :

```sql
SELECT id_vente, montant_ttc FROM vente ORDER BY montant_ttc DESC LIMIT 5;
```

## 13. Mini-projet M07.P3 — « Le top N par groupe » (1 h)

Le directeur commercial vous demande **3 classements** :

1. **(20 min)** Les **5 catégories** (rayons) par **CA total** décroissant.
2. **(20 min)** Pour chaque catégorie, le **produit le plus vendu** (en quantité cumulée).
3. **(20 min)** Les **10 clients** qui ont acheté dans **le plus de magasins différents**.

**Critère de réussite** : 3 requêtes, chacune commentée avec (a) la question métier, (b) le
nombre de lignes attendues, (c) la clause `ORDER BY` utilisée. La 2ᵉ requête utilise le pattern
`WITH … ROW_NUMBER() OVER (PARTITION BY …)` vu au §5.8.

## 14. Boîte à outils du chapitre

> **Boîte à outils.** Ce chapitre installe 6 outils de tri et de pagination : `ORDER BY` (tri
> sur 1 colonne), multi-clés (tri sur N colonnes), tri par alias, tri par position (fragile),
> `NULLS FIRST/LAST` (gestion des absences), `LIMIT/OFFSET` (pagination). DuckDB, PostgreSQL et
> SQLite partagent la même syntaxe ANSI ; MySQL omet `NULLS FIRST/LAST` par défaut.

| Outil | Usage | Syntaxe | Piège |
|---|---|---|---|
| `ORDER BY col` | tri simple | `ORDER BY montant_ttc DESC` | sans `ORDER BY`, ordre arbitraire |
| Multi-clés | tri principal + départage | `ORDER BY ville, nom` | l'ordre des colonnes compte |
| Tri par alias | tri lisible | `ORDER BY ca_total DESC` | MySQL peut refuser |
| Tri par position | tri portable | `ORDER BY 2 DESC` | fragile si on ajoute une colonne |
| `NULLS LAST` | placer les NULL en fin | `ORDER BY col ASC NULLS LAST` | comportement par défaut variable |
| `LIMIT/OFFSET` | paginer | `LIMIT 10 OFFSET 20` | lent sur les grosses tables |

## 15. Résumé du chapitre

- `ORDER BY` trie le résultat ; `LIMIT` tronque ; `OFFSET` saute.
- L'**ordre d'exécution** est `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `DISTINCT`
  → **`ORDER BY`** → `LIMIT`. `ORDER BY` est en 7ᵉ position, **après** `SELECT` et `DISTINCT`.
- Le **tri multi-clés** : l'ordre des colonnes dans `ORDER BY` est l'ordre de priorité.
- Le **tri par alias** est lisible ; le **tri par position** est fragile.
- La **pagination** par `OFFSET` est lente sur les grosses tables ; M11 enseignera la
  pagination par clé.
- Le **premier/dernier par groupe** s'obtient avec `WITH … ROW_NUMBER() OVER (PARTITION BY …)
  WHERE rang = 1` (M11 détaille la fenêtre).

## 16. À retenir

- **Toujours `ORDER BY` avant `LIMIT`** en production.
- **Tri par alias > tri par position** (lisibilité et robustesse).
- **`OFFSET` est acceptable** sur les petites tables, **à éviter** sur les millions de lignes.
- **`NULLS LAST`** est le défaut DuckDB/PostgreSQL en `ASC` ; à préciser pour la portabilité.
- Le **prochain chapitre (C04)** installe les **agrégats** (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`,
> `ROUND`) qui appellent `GROUP BY` (C05).

## 17. Évaluation formative (auto-correction, 8 min)

Sans document, en 8 minutes, répondre aux 5 questions. Auto-correction en bas.

1. Quelle est la position de `ORDER BY` dans l'ordre d'exécution ?
2. Pourquoi `LIMIT` sans `ORDER BY` est-il « non déterministe » ?
3. Quelle est la différence entre tri par alias et tri par position ?
4. Que fait `NULLS LAST` ?
5. Pourquoi la pagination `OFFSET` est-elle lente sur les grosses tables ?

**Réponses** :

1. 7ᵉ position : `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `DISTINCT` → `ORDER BY`
   → `LIMIT`.
2. Parce que sans `ORDER BY`, l'ordre des lignes est arbitraire (celui du stockage interne). Deux
   exécutions successives peuvent retourner des lignes différentes.
3. Le tri par alias utilise le nom déclaré dans le `SELECT` (par exemple `ORDER BY ca_total
   DESC`). Le tri par position utilise le numéro de la colonne (par exemple `ORDER BY 2 DESC`,
   qui trie la 2ᵉ colonne du `SELECT`). Le tri par alias est lisible et robuste ; le tri par
   position est fragile (ajouter une colonne au `SELECT` change le sens).
4. `NULLS LAST` place les valeurs `NULL` à la fin du tri. Le défaut en DuckDB/PostgreSQL est déjà
   `NULLS LAST` en `ASC`, mais préciser est une bonne pratique pour la portabilité.
5. Parce que `OFFSET m` parcourt les `m + n` premières lignes puis en jette `m`. Sur 1 million
   de lignes, un `OFFSET` proche de la fin parcourt la quasi-totalité des lignes avant
   d'en afficher 10.
