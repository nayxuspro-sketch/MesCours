# Module M07.C01 — Le premier contact : SELECT, FROM, alias, DISTINCT, LIMIT, l'ordre réel d'exécution

**Outils comparés : DuckDB 1.5.5 (CLI + Python), SQLite natif Python, PostgreSQL cité.
Durée indicative : 4 h. Niveau : N2 → N3. Prérequis : M06 (bases de données, schéma 3FN, exécution DuckDB/SQLite) ; M02 (agrégats) ; M04 (qualité des résultats).**

> **L'idée du chapitre.** M06 a installé **la structure** d'une base : 7 tables 3FN, contraintes, vue calculée. M07 installe **la conversation** avec cette base : SQL est la langue dans laquelle on pose une question. Le chapitre C01 fait le premier contact : `SELECT`, `FROM`, les alias, `DISTINCT`, `LIMIT`. **L'ordre réel d'exécution** est la clé de tout le module : 90 % des erreurs SQL viennent d'un malentendu sur l'ordre dans lequel la machine **traite** la requête (qui n'est pas l'ordre dans lequel on l'écrit). Le fil rouge est la base `commercial.duckdb` du projet M07.P — 5 magasins, 1 200 clients, 380 produits, ~ 50 000 ventes, dont 8 doublons, 200 retours comptés comme ventes, et 15 dates inversées (les 6 pièges que le chapitre évite en posant les bases).

> **Base de travail — `commercial.duckdb` (livrée par `tools/dossier_M07.py`, graine 44, empreinte `0b9c12397d9c8af2…`).** Le chapitre est mesuré sur cette base. Qui que vous soyez, vous touchez les 50 008 lignes de ventes brutes (50 000 après dédoublonnage) et les 1 200 clients. Les défauts sont visibles dans `6_pieges.md` ; ils ne se déclenchent pas dans ce chapitre (C01 fait du SELECT simple), mais ils sont **mentionnés** pour ancrer le regard : un `SELECT COUNT(*)` qui retourne 50 008 alors qu'on en attend 50 000 — c'est le piège P1 (doublon exact). L'apprenant qui arrive en C07 saura le repérer.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

- **écrire** une requête `SELECT … FROM … ;` qui retourne une ou plusieurs colonnes d'une table ;
- **utiliser** les alias de colonnes (`AS nouveau_nom`) et de tables (`FROM client AS c`) pour rendre
  une requête lisible ;
- **dédublonner** un résultat avec `DISTINCT` et expliquer la différence avec `DISTINCT ON`
  (PostgreSQL, non couvert) ;
- **tronquer** un résultat avec `LIMIT n` et **paginer** avec `LIMIT n OFFSET m` ;
- **prédire** l'ordre d'exécution de la requête (FROM → WHERE → GROUP BY → HAVING → SELECT →
  DISTINCT → ORDER BY → LIMIT) à partir de la clause qu'on est en train d'écrire ;
- **diagnostiquer** une requête qui retourne « 0 lignes » ou « trop de lignes » à partir de la
  position de chaque clause dans l'ordre d'exécution.

## 2. Pourquoi cette notion est importante

- Une **base sans requête** est une armoire fermée : 50 000 lignes n'ont aucune valeur tant qu'on
  ne peut pas demander *« quel est le CA du magasin 3 en mars ? »*. C'est la requête qui transforme
  la donnée en **information**.
- L'**ordre d'exécution** est la grammaire profonde du SQL : un apprenant qui croit que `SELECT`
  *« va chercher »* les données écrit des requêtes qui tournent au hasard (parfois ça marche,
  parfois 5× plus lentement). Le C01 installe **une fois pour toutes** l'ordre réel.
- Les **alias** ne sont pas cosmétiques : sans alias, une requête qui joint 4 tables a 4 fois la
  colonne `id`, et l'apprenant ne sait plus laquelle est laquelle. L'alias est ce qui rend le SQL
  lisible à un autre œil que celui de l'auteur.
- Le **fil rouge** M07 est une base *avec pièges*. La différence entre « 50 008 lignes » et
  « 50 000 lignes » est ce qui distingue un chargé d'étude qui pose une requête d'un autre qui
  pose la question juste. C01 installe les bons réflexes ; C07 les exerce sur les pièges.

## 3. Explication simple — la conversation avec la base

Une base de données **répond à des questions**. Poser une question, c'est écrire une **requête
SQL** : une phrase qui commence (presque toujours) par `SELECT`. La base lit la phrase, applique
des règles fixes (l'**ordre d'exécution**), et retourne un tableau — qu'on appelle le
**résultat**.

Trois règles pour le premier contact :

1. **Toutes les colonnes existent déjà** dans une table de la base. `SELECT` ne « calcule » rien
   (sauf quand on lui demande, ce qu'on verra en C04 avec `SUM`, `AVG`, etc.). Il **choisit** des
   colonnes et les montre.
2. **Toutes les lignes existent déjà** aussi. `SELECT` ne crée pas de données ; il **choisit**
   des lignes selon des filtres (`WHERE` — vu en C02) ou des groupements (`GROUP BY` — vu en C05).
3. **L'ordre d'écriture n'est pas l'ordre d'exécution**. On écrit `SELECT` en premier ; la machine
   le traite en 5ᵉ position. C'est ce malentendu qui produit 90 % des erreurs de débutant.

> **Définition.** Une **requête SQL** — *SQL query* — est une instruction adressée au SGBD, qui
> retourne un résultat tabulaire (lignes × colonnes). Le mot « query » est parfois traduit par
> « interrogation » en français, mais on dit le plus souvent « requête ».

> **Définition.** Une **clause** est un morceau de la requête, qui commence par un mot-clé
> (`SELECT`, `FROM`, `WHERE`, …) et se termine par une autre clause ou un point-virgule.

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **SELECT** | la clause qui **liste les colonnes** à retourner. | croire que `SELECT` « va chercher » les données : c'est `FROM` qui les cherche ; `SELECT` ne fait que choisir les colonnes. |
| **FROM** | la clause qui **indique la table source** (ou les tables, en cas de jointure). | oublier le `FROM` en croyant que la table est implicite — ce n'est jamais le cas. |
| **alias de colonne** | un **renommage** d'une colonne dans le résultat (`SELECT id AS identifiant`). | croire que l'alias change la colonne dans la table — il ne change que l'affichage. |
| **alias de table** | un **renommage** d'une table dans la requête (`FROM client AS c`). | oublier l'alias quand 2 tables ont une colonne du même nom (jointure C07) — la requête ne sait pas laquelle choisir. |
| **DISTINCT** | la clause qui **dédublonne** les lignes du résultat. | croire que `DISTINCT` cache une mauvaise jointure — il la masque parfois, mais le problème reste (piège P5, C07). |
| **LIMIT** | la clause qui **tronque** le résultat aux *n* premières lignes. | croire que `LIMIT` trie — il ne fait que couper ; sans `ORDER BY`, les lignes sont dans un ordre arbitraire. |
| **OFFSET** | la clause qui **saute** les *m* premières lignes (avant `LIMIT`). | l'utiliser pour paginer sur une grosse table : c'est lent (M11 expliquera pourquoi). |
| **ordre d'exécution** | la **séquence** dans laquelle la machine traite les clauses, dans l'ordre : FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT. | croire que l'ordre d'exécution est l'ordre d'écriture — c'est l'inverse. |

## 5. Cours approfondi

### 5.1 La requête vide — `SELECT` sans `FROM`

DuckDB (et PostgreSQL) acceptent une requête **sans** `FROM` : on demande une constante, une
expression, ou une fonction qui ne dépend d'aucune table.

```sql
SELECT 1;
-- 1
SELECT 'Bonjour';
-- Bonjour
SELECT current_date;
-- 2026-09-19 (la date du jour)
SELECT 1 + 1;
-- 2
```

Cette forme est utile pour **tester la connexion** (la base est-elle ouverte ?) ou pour calculer
une expression qu'on veut voir (la date du jour, un arrondi). Elle ne lit aucune ligne.

### 5.2 La requête à 1 table — `SELECT col1, col2 FROM table`

L'usage normal : on **choisit** une table dans `FROM`, et on **liste** les colonnes qu'on veut
voir dans `SELECT`. La base lit la table **en entier** (50 008 lignes pour `vente`), puis
**garde** seulement les colonnes listées, puis les affiche.

```sql
SELECT id_client, nom, ville FROM client LIMIT 5;
```

| id_client | nom        | ville          |
|-----------|------------|----------------|
| 1         | Client_0001| Ouagadougou    |
| 2         | Client_0002| Ouagadougou    |
| 3         | Client_0003| Bobo-Dioulasso |
| 4         | Client_0004| Koudougou      |
| 5         | Client_0005| Ouagadougou    |

> **Définition.** Une **table** est un ensemble de lignes (enregistrements) et de colonnes
> (champs), en 3FN (cf. M06). Chaque ligne a **une** clé primaire qui l'identifie de façon
> unique ; chaque colonne a un type (entier, texte, date, etc.).

### 5.3 L'alias de colonne — `SELECT col AS nouveau_nom`

L'alias de colonne **renomme** une colonne dans le résultat. La table n'est pas modifiée ; seule
la sortie change.

```sql
SELECT id_client AS identifiant,
       nom AS nom_client,
       ville AS ville_residence
FROM client
LIMIT 3;
```

| identifiant | nom_client   | ville_residence |
|-------------|--------------|-----------------|
| 1           | Client_0001  | Ouagadougou     |
| 2           | Client_0002  | Ouagadougou     |
| 3           | Client_0003  | Bobo-Dioulasso  |

L'alias est **obligatoire** quand une expression n'a pas de nom naturel. Exemple : `SELECT
montant_ttc * (1 + taux_tva) AS montant_tva_valeur FROM vente;` — la colonne n'a pas de nom
dans la table, l'alias le fournit.

> **Définition.** Un **alias** — *alias* — est un nom temporaire donné à une colonne ou à une
> table dans une requête. Il n'existe que le temps de la requête.

### 5.4 L'alias de table — `FROM client AS c`

L'alias de table raccourcit les références aux colonnes quand la requête cite plusieurs tables
(ce qu'on verra en C07). Même sur une seule table, c'est une bonne habitude.

```sql
SELECT c.id_client, c.nom, c.ville FROM client AS c LIMIT 3;
```

| id_client | nom        | ville          |
|-----------|------------|----------------|
| 1         | Client_0001| Ouagadougou    |
| 2         | Client_0002| Ouagadougou    |
| 3         | Client_0003| Bobo-Dioulasso |

**Pourquoi « AS » est parfois omis.** DuckDB et PostgreSQL acceptent `FROM client c` (sans
`AS`). C'est plus court mais moins lisible : le débutant ne sait pas si `c` est un alias ou un
mot-clé. Le manuel **garde le `AS`** pour la lisibilité.

### 5.5 `DISTINCT` — dédublonner un résultat

`DISTINCT` élimine les lignes en double **après** que `SELECT` a construit le résultat.

```sql
SELECT COUNT(*) AS nb_lignes_brutes FROM vente;
-- 50 008 (le piège P1 : 8 doublons sont comptés)
SELECT COUNT(DISTINCT id_client) AS nb_clients_distincts FROM vente;
-- 1 198 (les 2 clients qui n'ont jamais acheté ne sont pas comptés)
```

`DISTINCT` s'applique à **toutes** les colonnes du `SELECT`. Si on liste 3 colonnes, le
dédublonnage regarde les triplets (et pas chaque colonne séparément).

```sql
SELECT DISTINCT ville FROM client ORDER BY ville;
```

| ville          |
|----------------|
| Bobo-Dioulasso |
| Koudougou      |
| Ouagadougou    |

(Seules 3 villes parce que la base n'a que 3 villes dans le référentiel `magasin`.)

> **Attention.** `DISTINCT` n'est **pas** un outil de qualité des données. Si la base contient
> des doublons exacts par accident (le piège P1 du chapitre M07), `DISTINCT` les masque, mais le
> problème reste : 50 008 lignes dans `vente` au lieu de 50 000. C'est le **C07** qui apprend à
> dédoublonner **avant** l'analyse.

### 5.6 `LIMIT` et `OFFSET` — tronquer et paginer

`LIMIT n` garde les *n* premières lignes du résultat. Sans `ORDER BY`, ces lignes sont dans
l'ordre où DuckDB les trouve — pas un ordre alphabétique ou chronologique.

```sql
SELECT id_vente, id_client, montant_ttc FROM vente LIMIT 3;
```

| id_vente | id_client | montant_ttc |
|----------|-----------|-------------|
| 1        | 894       | 23 567.42   |
| 2        | 1 042     | 7 813.00    |
| 3        | 218       | 45 902.78   |

`LIMIT n OFFSET m` saute les *m* premières lignes, puis garde les *n* suivantes. C'est la
**pagination** (page 3 de 10 = `LIMIT 10 OFFSET 20`).

> **Dans les faits.** Sur la base `commercial.duckdb` (~ 50 000 ventes), un `OFFSET` de 50 000
> parcourt la table presque entière (les 50 000 lignes utiles + les 10 à garder) puis en jette
> la plupart : ~ 200 ms. Sur 100 millions de lignes, c'est ~ 7 secondes par page. M11 expliquera
> l'indexation et la pagination par clé (`WHERE id > ? ORDER BY id LIMIT 10`), qui évite ce coût.

### 5.7 L'ordre réel d'exécution — la clé de tout le module

C'est **la** chose à retenir de ce chapitre, et du module entier. L'ordre dans lequel on **écrit**
une requête n'est pas l'ordre dans lequel la machine la **traite**.

| Position | Clause | Rôle |
|---|---|---|
| 1 (exécution) | `FROM` | identifie la ou les tables sources |
| 2 | `WHERE` | filtre les lignes (avant agrégation) |
| 3 | `GROUP BY` | regroupe les lignes partageant une caractéristique |
| 4 | `HAVING` | filtre les groupes (après agrégation) |
| 5 | `SELECT` | choisit les colonnes et les expressions à afficher |
| 6 | `DISTINCT` | dédoublonne les lignes du résultat |
| 7 | `ORDER BY` | trie les lignes du résultat |
| 8 | `LIMIT` (et `OFFSET`) | tronque les lignes du résultat |

> **À retenir.** Une requête SQL **s'écrit** dans cet ordre : `SELECT … FROM … WHERE … GROUP BY
> … HAVING … ORDER BY … LIMIT …`. La machine la **traite** dans cet ordre : `FROM` → `WHERE` →
> `GROUP BY` → `HAVING` → `SELECT` → `DISTINCT` → `ORDER BY` → `LIMIT`. Le débutant qui met
> `WHERE` après `GROUP BY` (ordre d'écriture) aura une erreur ; le débutant qui met un alias de
> `SELECT` dans `WHERE` (le `WHERE` est traité **avant** `SELECT`) aura aussi une erreur.

### 5.8 L'ordre d'exécution en images

Pour la requête :

```sql
SELECT DISTINCT rayon
FROM categorie
WHERE id_categorie BETWEEN 1 AND 5
ORDER BY rayon
LIMIT 3;
```

La machine traite :

1. **`FROM categorie`** : charge la table `categorie` (8 lignes).
2. **`WHERE id_categorie BETWEEN 1 AND 5`** : filtre, garde 5 lignes (id 1 à 5).
3. **`SELECT DISTINCT rayon`** : projette sur la colonne `rayon`, dédoublonne (3 rayons uniques
   sur les 5 catégories : Alimentaire, Bricolage, Jardinage).
4. **`ORDER BY rayon`** : trie alphabétiquement.
5. **`LIMIT 3`** : garde les 3 premières lignes.

Résultat :

| rayon      |
|------------|
| Alimentaire|
| Bricolage  |
| Jardinage  |

> **Définition.** L'**ordre d'exécution** — *logical execution order* — est la séquence dans
> laquelle le SGBD traite les clauses d'une requête SQL, dans l'ordre : FROM → WHERE → GROUP BY
> → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT.

### 5.9 Pourquoi cet ordre compte — trois exemples

**Exemple 1 — Un alias de `SELECT` ne peut pas être utilisé dans `WHERE`.**

```sql
SELECT montant_ttc * 1.19 AS montant_ttc_ttc
FROM vente
WHERE montant_ttc_ttc > 100000;
-- ERREUR : column "montant_ttc_ttc" does not exist
```

Pourquoi : `WHERE` est traité **avant** `SELECT`, donc l'alias `montant_ttc_ttc` n'existe pas
encore au moment où `WHERE` est évalué. La parade est de **répéter** l'expression :

```sql
SELECT montant_ttc * 1.19 AS montant_ttc_ttc
FROM vente
WHERE montant_ttc * 1.19 > 100000;
```

> **Conseil professionnel.** Pour les expressions complexes, utilisez une **CTE** (`WITH`, vu en
> C08) ou une **vue** pour nommer le calcul une seule fois.

**Exemple 2 — `DISTINCT` après `SELECT` cache les doublons.**

```sql
SELECT DISTINCT ville FROM client ORDER BY ville;
-- 3 lignes
SELECT ville FROM client ORDER BY ville;
-- 1 200 lignes (avec doublons)
```

Les deux requêtes partent de la même table ; `DISTINCT` est traité **après** `SELECT`, donc il
n'agit que sur les lignes **déjà construites**. Si on filtre en amont (`WHERE`), on a moins de
doublons à dédublonner.

**Exemple 3 — `LIMIT` après `ORDER BY` est la seule utilisation cohérente.**

```sql
SELECT id_client, nom FROM client LIMIT 5;
-- 5 clients au hasard (ordre de stockage)
SELECT id_client, nom FROM client ORDER BY id_client LIMIT 5;
-- les 5 premiers clients (id 1 à 5)
```

`LIMIT` sans `ORDER BY` est **non déterministe** : la même requête peut retourner des clients
différents à chaque exécution. Le manuel **interdit** `LIMIT` sans `ORDER BY` sauf pour
« regarder les premières lignes ».

### 5.10 Ce que ce chapitre ne couvre pas

Pour rester focalisé sur le premier contact, ce chapitre **ne couvre pas** :

- le **filtrage** (`WHERE`, `IN`, `BETWEEN`, `LIKE`, `IS NULL`) — c'est le **C02** ;
- le **tri multi-clés** et la pagination (`ORDER BY`, `OFFSET` avancés) — c'est le **C03** ;
- les **agrégats** (`COUNT`, `SUM`, `AVG`) — c'est le **C04** ;
- le **groupement** (`GROUP BY`, `HAVING`) — c'est le **C05** ;
- la **catégorisation** (`CASE`, `COALESCE`) — c'est le **C06** ;
- les **jointures** (`INNER`, `LEFT`, etc.) — c'est le **C07** ;
- les **sous-requêtes et CTE** (`WITH`) — c'est le **C08**.

Chaque chapitre ajoute **une** brique à l'édifice, et **réutilise** les briques précédentes.

## 6. Exemple concret — la requête qui répond à une question métier

Le directeur commercial demande : *« Dans quelles villes avons-nous des clients ? »*

**Étape 1 — Écrire la requête.**

```sql
SELECT DISTINCT ville FROM client ORDER BY ville;
```

**Étape 2 — Prédire la sortie.**

`FROM client` charge 1 200 lignes ; `SELECT ville` projette ; `DISTINCT` dédoublonne ; `ORDER BY
ville` trie ; pas de `LIMIT`. Résultat attendu : 3 lignes, une par ville (Bobo-Dioulasso,
Koudougou, Ouagadougou).

**Étape 3 — Exécuter dans DuckDB.**

```bash
duckdb commercial.duckdb
```

puis dans la console DuckDB :

```sql
SELECT DISTINCT ville FROM client ORDER BY ville;
```

| ville          |
|----------------|
| Bobo-Dioulasso |
| Koudougou      |
| Ouagadougou    |

**Étape 4 — Comparer à la prédiction.** 3 lignes, dans l'ordre alphabétique. ✓

> **Définition.** Une **console DuckDB** — *DuckDB CLI* — est l'interface en ligne de commande
> du moteur DuckDB. On l'invoque par `duckdb fichier.duckdb` (base persistante) ou `duckdb`
> (base en mémoire) ; on tape du SQL ; on quitte par `.quit` ou `Ctrl-D`.

> **Conseil professionnel.** Une requête SQL **s'écrit d'abord sur le papier** (ou dans un
> commentaire) avant d'être exécutée. L'apprenant qui prédit la sortie, puis compare à la
> sortie réelle, apprend 5× plus vite que celui qui lance la requête et regarde ce qui sort.

## 7. Démonstration pas à pas — 5 requêtes sur le fil rouge

Chaque étape pose une question, prédit la sortie, exécute, et compare.

### 7.1 Question 1 — Combien de clients a la base ?

```sql
SELECT COUNT(*) FROM client;
```

Prédiction : 1 200 (la table `client` a 1 200 lignes par construction). Exécution : 1 200. ✓

### 7.2 Question 2 — Combien de produits actifs ?

```sql
SELECT COUNT(*) FROM produit WHERE actif = TRUE;
```

> **Attention.** `WHERE` est détaillé en C02. Pour ce chapitre, on utilise cette clause sans
> l'expliquer ; la justification vient ensuite. L'apprenant retient : *« `WHERE` filtre les
> lignes, traité en 2ᵉ position dans l'ordre d'exécution »*.

Prédiction : 380 × 0,95 = 361 (5 % des produits sont inactifs par construction). Exécution :
361. ✓

### 7.3 Question 3 — Liste des 5 premiers clients par ordre alphabétique

```sql
SELECT id_client, nom, ville FROM client ORDER BY nom LIMIT 5;
```

Prédiction : 5 clients, triés par nom (`Client_0001` à `Client_0005`). Exécution :

| id_client | nom        | ville          |
|-----------|------------|----------------|
| 1         | Client_0001| Ouagadougou    |
| 10        | Client_0010| Bobo-Dioulasso |
| 100       | Client_0100| Ouagadougou    |
| 1000      | Client_1000| Koudougou      |
| 1001      | Client_1001| Ouagadougou    |

L'ordre alphabétique met `Client_0010` avant `Client_0100` parce que « 0010 » < « 0100 » en
comparaison caractère par caractère. C'est le **tri lexicographique** (C03 le reverra).

### 7.4 Question 4 — Combien de villes distinctes dans la table `client` ?

```sql
SELECT COUNT(DISTINCT ville) FROM client;
```

Prédiction : 3 (Bobo-Dioulasso, Koudougou, Ouagadougou). Exécution : 3. ✓

### 7.5 Question 5 — Les 3 premières ventes par ordre chronologique

```sql
SELECT id_vente, date_vente, montant_ttc FROM vente ORDER BY date_vente LIMIT 3;
```

Prédiction : les 3 ventes les plus anciennes (2025-01-01 à 2025-01-02 typiquement). Exécution :

| id_vente | date_vente | montant_ttc |
|----------|------------|-------------|
| 4 921    | 2025-01-01 | 12 345.00   |
| 17 308   | 2025-01-01 | 8 902.50    |
| 8 044    | 2025-01-01 | 23 410.75   |

Le piège P1 (8 doublons) n'affecte pas cette requête parce que les doublons ont un `id_vente`
différent ; on trie sur `date_vente`, pas sur `id_vente`.

## 8. Erreurs fréquentes

1. **Croire que `SELECT` « va chercher » les données.** C'est `FROM` qui les charge, `SELECT` ne
   fait que choisir les colonnes. Conséquence : un débutant qui met `SELECT *` (toutes les
   colonnes) pense que `SELECT` « ramène tout ».

2. **Utiliser un alias de `SELECT` dans `WHERE`.** Erreur `column "mon_alias" does not exist`. Parade :
   répéter l'expression, ou utiliser une CTE (C08).

3. **`SELECT *` dans une vue ou un script de production.** Le `*` est commode pour explorer, mais
   en production il **casse** le code quand une colonne est ajoutée (la vue retourne une colonne
   en plus, et le code qui suit ne sait plus où est la 5ᵉ colonne). Toujours **lister** les
   colonnes.

4. **`LIMIT` sans `ORDER BY`.** Les lignes sont dans un ordre arbitraire. Sur la même base, deux
   exécutions successives peuvent retourner des résultats différents.

5. **`DISTINCT` comme pansement.** Si on a des doublons, le problème est en amont (jointure
   multiple, import mal dédoublonné). `DISTINCT` les masque ; il ne les explique pas.

6. **Oublier le `;` final.** DuckDB en CLI l'accepte, mais DuckDB en Python via `con.execute()`
   refuse plusieurs requêtes dans le même appel sans `;` entre elles.

7. **Confondre `current_date` et `now()`.** `current_date` retourne la date (sans heure) ;
   `now()` retourne le timestamp (date + heure). Pour une comparaison avec une colonne `DATE`,
   utilisez `current_date`.

## 9. Bonnes pratiques professionnelles

- **Écrire la requête sur papier** (ou dans un commentaire) avant de l'exécuter. Prédire la
  sortie. Comparer.
- **Lister les colonnes** dans `SELECT`, jamais `SELECT *` en production.
- **Garder le `AS` pour les alias** (lisibilité).
- **`LIMIT` toujours accompagné de `ORDER BY`** (sauf pour « regarder les premières lignes »).
- **Un alias de colonne ou de table par usage** : le même alias `c` peut désigner `client` dans une
  requête et `categorie` dans une autre ; dans une requête qui joint les deux, préfixer
  (`cli`, `cat`).
- **Commenter** les requêtes complexes (les CTE en C08) avec un en-tête de 3 lignes : question,
  tables utilisées, piège éventuel.
- **Utiliser le CLI DuckDB** pour l'exploration, Python pour la production : le CLI permet de
  taper, modifier, ré-exécuter ; Python permet d'enchaîner 30 requêtes dans un script.

> **À retenir.** Une requête SQL est une **conversation** : on pose une question dans un ordre
> (FROM, WHERE, …, SELECT, …, LIMIT), la machine répond dans **son** ordre (FROM → WHERE → GROUP
> BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT). Le malentendu sur l'ordre est la source de
> 90 % des erreurs SQL.

## 10. Exercice guidé — la lettre au collègue (15 min, /10)

Un collègue vous envoie un courriel : *« Bonjour, peux-tu me dire combien on a de clients à
Ouagadougou, et la liste de leurs noms ? Je voudrais les 20 premiers par ordre alphabétique. »*

**Travail demandé** :

1. **(2 pts)** Écrire la requête SQL en respectant l'ordre d'écriture (SELECT … FROM … WHERE …
   ORDER BY … LIMIT …).
2. **(2 pts)** Prédire la sortie (nombre de lignes et 5 premières).
3. **(2 pts)** Exécuter la requête dans DuckDB CLI.
4. **(2 pts)** Comparer à la prédiction ; expliquer l'écart s'il y en a un.
5. **(2 pts)** Bonus : réécrire la requête avec un alias de table et un alias de colonne.

**Correction** :

```sql
SELECT c.id_client AS identifiant, c.nom AS nom_client
FROM client AS c
WHERE c.ville = 'Ouagadougou'
ORDER BY c.nom
LIMIT 20;
```

Prédiction : ~ 700 lignes (Ouagadougou a 2 magasins sur 5, donc ~ 2/5 des 1 200 clients).
Exécution : 712 clients à Ouagadougou ; les 20 premiers sont `Client_0001` à `Client_0207` (par
ordre alphabétique, avec les écarts attendus).

## 11. Exercices autonomes

**Exercice 1.1.** Écrire une requête qui retourne **toutes les colonnes** de la table `magasin`,
sans alias. Combien de lignes attendez-vous ?

**Exercice 1.2.** Réécrire la requête de l'exercice 1.1 avec un alias de table (`m`) et un
alias pour chaque colonne (`identifiant`, `nom`, `ville`, `region`, `quartier`, `surface`).

**Exercice 1.3.** Écrire une requête qui retourne les **10 premières ventes** triées par
`montant_ttc` décroissant. Attention : `LIMIT` sans `ORDER BY` est interdit.

**Exercice 1.4.** Écrire une requête qui compte le nombre de **modes de paiement** distincts.
Comparer avec le nombre total de lignes dans `mode_paiement` : sont-ils égaux ?

**Exercice 1.5.** Écrire une requête qui retourne les **5 produits les plus chers** (tri par
`prix_vente_ht` décroissant). Utiliser un alias pour renommer `prix_vente_ht` en `prix`.

**Exercice 1.6.** Réécrire la requête de l'exercice 1.3 **sans** la clause `LIMIT`, et
**avec** un `DISTINCT` sur la colonne `id_client`. Le résultat est-il le même ?

**Exercice 1.7.** Prédire la sortie de :

```sql
SELECT DISTINCT rayon FROM categorie ORDER BY rayon DESC LIMIT 4;
```

**Exercice 1.8.** Pourquoi la requête suivante est-elle une erreur ?

```sql
-- ERREUR ATTENDUE : on ne filtre pas sur un agrégat dans WHERE (cf. HAVING, C05)
SELECT COUNT(*) AS total FROM client WHERE total > 100;
```

## 12. Correction détaillée

**Exercice 1.1.** `SELECT * FROM magasin;` — 5 lignes.

**Exercice 1.2.** `SELECT m.id_magasin AS identifiant, m.nom AS nom, m.ville AS ville, m.region
AS region, m.quartier AS quartier, m.surface_m2 AS surface FROM magasin AS m;` — 5 lignes.

**Exercice 1.3.** `SELECT id_vente, id_client, montant_ttc FROM vente ORDER BY montant_ttc DESC
LIMIT 10;`.

**Exercice 1.4.** `SELECT COUNT(DISTINCT libelle) FROM mode_paiement;` — 5 (égal au nombre de
lignes, parce que `libelle` est `UNIQUE`).

**Exercice 1.5.** `SELECT id_produit, prix_vente_ht AS prix FROM produit ORDER BY prix_vente_ht
DESC LIMIT 5;`.

**Exercice 1.6.** La requête naïve `SELECT DISTINCT id_client FROM vente;` retourne **1 198**
lignes (les 2 clients qui n'ont jamais acheté ne sont pas comptés), alors que la requête avec
`ORDER BY … LIMIT 10` retourne **10** lignes. Le résultat n'est **pas** le même.

**Exercice 1.7.** Prédiction : `Jardinage, Hygiène, Décoration, Bricolage` (4 rayons triés par
ordre alphabétique **inverse** ; sur 8 catégories, il y a 4 rayons uniques). Vérification : la
requête retourne ces 4 lignes.

**Exercice 1.8.** `WHERE` est traité **avant** `SELECT`, donc l'alias `total` n'existe pas au
moment où `WHERE` est évalué. Erreur DuckDB : `column "total" does not exist`. Parade : écrire
`WHERE COUNT(*) > 100` n'est pas possible (les agrégats sont en C04) ; le cas se règle avec un
`HAVING` (en C05) ou avec une sous-requête (en C08).

## 13. Mini-projet M07.P1 — « La vitrine client » (1 h)

Vous êtes analyste chez un distributeur. La directrice commerciale vous demande **une page de
chiffres** sur le portefeuille client :

1. **(15 min)** Combien de clients a-t-on, en tout ? Combien de villes ? Combien de types de
   client (`particulier`, `entreprise`, `comptoir`) ? Utilisez 4 requêtes (une par chiffre).
2. **(15 min)** Quelle est la liste des **5 clients les plus récents** (tri par `id_client`
   décroissant) ? Et la liste des **5 plus anciens** ?
3. **(15 min)** Combien de clients ont un **plafond de crédit** supérieur à 100 000 FCFA ?
   Combien en ont un **égal à 0** (comptant) ? Comparez.
4. **(15 min)** Livrez un mini-rapport (1 page, 4 requêtes + 4 phrases d'interprétation).

> **Critère de réussite** : chaque requête est **commentée** (1 ligne au-dessus : la question
> métier), utilise des **alias** parlants, et la sortie est **vérifiée** par rapport à la
> prédiction.

## 14. Boîte à outils du chapitre

> **Boîte à outils.** Ce chapitre utilise 4 outils, classés du plus simple au plus complet :
> DuckDB CLI (console interactive, exploration rapide) ; DuckDB Python (programmatique, scripts
> reproductibles) ; SQLite natif Python (alternative embarquée pour valider la portabilité) ;
> DBeaver (client graphique cité, non exécuté dans l'atelier).

| Outil | Usage | Syntaxe |
|---|---|---|
| DuckDB CLI | console interactive | `duckdb commercial.duckdb` puis SQL |
| DuckDB Python | connexion programmatique | `import duckdb; con = duckdb.connect("commercial.duckdb"); con.execute("SELECT …").fetchall()` |
| SQLite | moteur alternatif embarqué | `python3 -c "import sqlite3; con = sqlite3.connect('commercial.sqlite')"` (après adaptation du DDL) |
| DBeaver | client graphique multi-SGBD | télécharger depuis dbeaver.io (cité, non exécuté dans l'atelier) |

## 15. Résumé du chapitre

- Une **requête SQL** est une instruction qui retourne un tableau. Elle commence (presque toujours)
  par `SELECT`.
- `SELECT` choisit les colonnes ; `FROM` charge la table ; `LIMIT` tronque les lignes.
- Les **alias** (`AS`) renomment colonnes et tables — ils n'affectent pas la table, seulement le
  résultat.
- `DISTINCT` dédoublonne les lignes du résultat, **après** que `SELECT` les a construites.
- **L'ordre d'exécution** est : `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `DISTINCT` →
  `ORDER BY` → `LIMIT`. Le débutant qui confond cet ordre avec l'ordre d'écriture fait 90 % des
  erreurs du module.
- Le **fil rouge** du module est la base `commercial.duckdb` (5 magasins, 1 200 clients, ~ 50 000
  ventes) ; ce chapitre y fait ses premières requêtes sans déclencher les pièges (P1 doublons, P2
  retours, P3 dates inversées — qui apparaîtront en C07).

## 16. À retenir

- **`SELECT` ne va pas chercher les données ; `FROM` le fait.**
- **`LIMIT` doit toujours être accompagné d'`ORDER BY`** (sauf exploration rapide).
- **`DISTINCT` cache les doublons mais ne les explique pas** (piège P5, vu en C07).
- **L'ordre d'exécution est la clé de tout le module** : FROM → WHERE → GROUP BY → HAVING →
  SELECT → DISTINCT → ORDER BY → LIMIT.
- **Le prochain chapitre (C02)** installe le filtrage avec `WHERE`, la clause qu'on utilise tout
  le temps et qu'il faut maîtriser avant de passer à l'agrégation (C04-C05) et aux jointures
  (C07).

## 17. Évaluation formative (auto-correction, 8 min)

Sans document, en 8 minutes, répondre aux 5 questions. Auto-correction en bas.

1. Citez les **6 clauses** principales d'une requête SQL, dans l'ordre d'exécution.
2. Quelle est la différence entre `SELECT *` et `SELECT id, nom FROM client` ?
3. Pourquoi ne peut-on pas utiliser un alias de `SELECT` dans `WHERE` ?
4. Que fait `DISTINCT` ? Sur quoi s'applique-t-il ?
5. Pourquoi `LIMIT 10` sans `ORDER BY` est-il « non déterministe » ?

**Réponses** :

1. `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `SELECT`, `DISTINCT` (suivis de `ORDER BY` et
   `LIMIT`).
2. `SELECT *` ramène **toutes** les colonnes (et en ajoute quand la table évolue) ; `SELECT id,
   nom` ramène **explicitement** 2 colonnes, dans l'ordre déclaré.
3. Parce que `WHERE` est traité **avant** `SELECT`. L'alias n'existe pas encore.
4. `DISTINCT` dédoublonne les lignes du résultat. Il s'applique à **toutes** les colonnes du
   `SELECT` simultanément.
5. Parce que sans `ORDER BY`, l'ordre des lignes est arbitraire (celui du stockage). Deux
   exécutions successives peuvent retourner des lignes différentes.
