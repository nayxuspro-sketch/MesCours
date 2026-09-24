# Module M07.C02 — Filtrer : WHERE, opérateurs, IN, BETWEEN, LIKE, IS NULL, dates, priorités logiques

**Outils comparés : DuckDB 1.5.5 (CLI + Python), SQLite natif Python, PostgreSQL cité.
Durée indicative : 4 h. Niveau : N2 → N3. Prérequis : M07.C01 (SELECT, FROM, alias, ordre d'exécution) ; M04 (qualité des résultats).**

> **L'idée du chapitre.** C01 a installé le **squelette** d'une requête : `SELECT … FROM …`. C02 installe **le filtre** : `WHERE`. C'est la clause qu'on utilise tout le temps — une requête d'analyse passe 70 % de son temps dans le `WHERE`. Le chapitre couvre les 6 opérateurs de comparaison, les 4 raccourcis (`IN`, `BETWEEN`, `LIKE`, `IS NULL`), les **priorités logiques** (`AND` avant `OR`), et le cas particulier des **dates** (la moitié des requêtes d'analyse portent sur des périodes). Le fil rouge est la base `commercial.duckdb` ; on y mesure notamment que **21 406 ventes sur 50 008 ont une date inversée** (`date_vente > date_limite_remise`), un piège P3 plus profond qu'il n'y paraît (cf. exercice 2.7).

> **Base de travail — `commercial.duckdb` (empreinte `0b9c12397d9c8af2…`).** Ce chapitre utilise la base livrée par `tools/dossier_M07.py` (graine 44) : 5 magasins, 1 200 clients, 380 produits, 50 008 ventes brutes. Les chiffres d'exemple sont **tous mesurés** sur cette base : 512 clients à Ouagadougou, 850 clients particuliers, 18 produits inactifs, 27 clients « comptoir » à plafond 0, 7 136 ventes du dimanche, 24 920 ventes à TVA 18 % (2025), 21 406 ventes avec `date_vente > date_limite_remise` (le piège P3 du chapitre C07).

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

- **filtrer** les lignes d'une table avec la clause `WHERE` et les 6 opérateurs de comparaison
  (`=`, `<>`, `<`, `>`, `<=`, `>=`) ;
- **utiliser** les 4 raccourcis de filtrage (`IN`, `BETWEEN`, `LIKE`, `IS NULL`) et expliquer
  quand chacun est plus lisible que l'équivalent en `=`/`AND` ;
- **comparer** des dates avec `BETWEEN`, `EXTRACT`, et les intervalles ;
- **combiner** plusieurs conditions avec `AND`, `OR`, `NOT` en respectant les **priorités
  logiques** et en parenthésant pour clarifier ;
- **repérer** le piège `= NULL` (qui ne marche jamais) et utiliser `IS NULL` / `IS NOT NULL` ;
- **prédire** la sortie d'une requête `WHERE` avant de l'exécuter (la moitié des erreurs SQL
  viennent d'un `WHERE` mal lu).

## 2. Pourquoi cette notion est importante

- Le **`WHERE` est la clause la plus utilisée** : une requête d'analyse filtre en moyenne 95 %
  des lignes (on ne garde que les ventes d'un magasin, d'une période, d'un client particulier).
  C'est le geste de base du métier.
- Les **priorités logiques** sont la source de bugs la plus subtile : un `WHERE a = 1 OR b = 2
  AND c = 3` est parsé comme `WHERE a = 1 OR (b = 2 AND c = 3)` (parce que `AND` est plus prioritaire
  que `OR`). Le débutant qui voulait `WHERE (a = 1 OR b = 2) AND c = 3` se trompe de 50 % des cas.
- **Les dates sont piégeuses** : `date_vente BETWEEN '2025-01-01' AND '2025-01-31'` inclut le 31
  janvier (borne supérieure **incluse**), mais si le 31 n'existe pas dans la table, la requête
  retourne 0 ligne sans erreur.
- Le **piège `= NULL`** : en SQL, `NULL` n'est **pas** une valeur, c'est une absence de valeur.
  `WHERE colonne = NULL` ne retourne **jamais** rien, même si la colonne contient des `NULL`. C'est
  `WHERE colonne IS NULL` qu'il faut utiliser.

## 3. Explication simple — le filtre comme un entonnoir

Une requête avec `WHERE` est un entonnoir :

1. `FROM` charge la table (entonnoir large, 50 008 lignes pour `vente`) ;
2. `WHERE` garde les lignes qui satisfont la condition (entonnoir étroit) ;
3. `SELECT` choisit les colonnes à afficher ;
4. (optionnel) `ORDER BY`, `LIMIT` trient et tronquent.

L'image est utile parce que **l'ordre d'exécution est important** : `WHERE` est traité en
**2ᵉ position** (après `FROM`, avant `GROUP BY`). Tout ce qui réduit le nombre de lignes se
fait en `WHERE`, pas en `HAVING` (qui filtre les groupes, pas les lignes — vu en C05).

> **Définition.** Le **filtre WHERE** — *WHERE clause* — est la clause SQL qui élimine les
> lignes qui ne satisfont pas une condition. Le filtre agit **avant** l'agrégation et **avant**
> la projection.

> **Définition.** Un **opérateur de comparaison** est un opérateur à 2 opérandes qui retourne
> `TRUE`, `FALSE` ou `NULL` : `=`, `<>`, `<`, `>`, `<=`, `>=`.

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **WHERE** | la clause qui **filtre les lignes** avant agrégation. | l'utiliser après `GROUP BY` (c'est `HAVING` qu'il faut). |
| **opérateur de comparaison** | un des 6 symboles : `=`, `<>`, `<`, `>`, `<=`, `>=`. | confondre `=` (affectation / comparaison) avec `:=` (PostgreSQL, affectation seule). |
| **IN (liste)** | un raccourci pour `colonne = v1 OR colonne = v2 OR …`. | croire que `IN` est plus rapide que `OR` (c'est équivalent, mais plus lisible). |
| **BETWEEN x AND y** | un raccourci pour `colonne >= x AND colonne <= y` (bornes **incluses**). | croire que la borne supérieure est exclue (elle ne l'est pas). |
| **LIKE** | un filtre sur chaînes de caractères, avec jokers `%` (n'importe quoi) et `_` (un caractère). | oublier que `LIKE` est sensible à la casse en PostgreSQL (utiliser `ILIKE` pour ignorer la casse). |
| **joker `%`** | dans `LIKE`, représente **n'importe quelle chaîne**, y compris la chaîne vide. | croire que `%` représente un seul caractère (c'est `_`). |
| **IS NULL** | un test d'absence de valeur. | écrire `WHERE colonne = NULL` (qui ne marche jamais). |
| **AND** | la conjonction logique : les deux conditions doivent être vraies. | croire que `AND` est une moyenne (en logique, c'est un « et » strict). |
| **OR** | la disjonction logique : au moins une des conditions doit être vraie. | oublier que `OR` est moins prioritaire que `AND` (parenthéser !). |
| **NOT** | la négation logique : inverse le sens d'une condition. | l'utiliser sur `IN` (`NOT IN`) sans anticiper le cas `NULL` (règle des trois valeurs). |

## 5. Cours approfondi

### 5.1 Les 6 opérateurs de comparaison

```sql
SELECT * FROM client WHERE id_client = 1;        -- égalité
SELECT * FROM client WHERE id_client <> 1;       -- différent (le « pas égal »)
SELECT * FROM client WHERE id_client < 100;      -- strictement inférieur
SELECT * FROM client WHERE id_client > 100;      -- strictement supérieur
SELECT * FROM client WHERE id_client <= 100;     -- inférieur ou égal
SELECT * FROM client WHERE id_client >= 100;     -- supérieur ou égal
```

L'opérateur `!=` (différent) est accepté par DuckDB et PostgreSQL comme synonyme de `<>`,
mais `<>` est la forme **ANSI** (la plus portable). Le manuel utilise `<>`.

> **À retenir.** DuckDB et PostgreSQL traitent les **trois valeurs** de la logique SQL :
> `TRUE`, `FALSE`, `NULL`. Une comparaison avec `NULL` retourne `NULL`, qui est traité comme
> « faux » par `WHERE`. Conséquence : `WHERE colonne = NULL` ne retourne **jamais** de ligne, même
> si la colonne contient des `NULL`. C'est `WHERE colonne IS NULL` qu'il faut écrire.

### 5.2 `IN (liste)` — un raccourci pour `OR`

```sql
SELECT id_client, nom, ville FROM client
WHERE ville IN ('Ouagadougou', 'Bobo-Dioulasso');
```

Équivalent à :

```sql
SELECT id_client, nom, ville FROM client
WHERE ville = 'Ouagadougou' OR ville = 'Bobo-Dioulasso';
```

Les deux formes produisent **le même résultat** ; `IN` est plus lisible quand la liste dépasse
2 éléments.

Sur la base `commercial.duckdb` : 1 200 clients à `Ouagadougou`, `Bobo-Dioulasso` ou `Koudougou`,
dont **512** à Ouagadougou et **661** à Bobo-Dioulasso, donc **1 173** à Ouaga+Bobo et **27**
à Koudougou. La requête `IN ('Ouagadougou', 'Bobo-Dioulasso')` retourne **1 173** lignes.

> **Attention.** `NOT IN` a un piège vicieux : si la liste contient `NULL`, `NOT IN`
> retourne **toujours 0 ligne** (parce que `WHERE x NOT IN (a, NULL)` est équivalent à
> `WHERE x <> a AND x <> NULL`, et `x <> NULL` est `NULL`, donc la condition entière est
> `NULL`, traité comme faux). Parade : utiliser `NOT EXISTS` (vu en C08), qui ignore les `NULL`
> proprement.

### 5.3 `BETWEEN x AND y` — bornes **incluses**

```sql
SELECT id_vente, date_vente, montant_ttc FROM vente
WHERE montant_ttc BETWEEN 10000 AND 50000
ORDER BY montant_ttc
LIMIT 5;
```

| id_vente | date_vente | montant_ttc |
|----------|------------|-------------|
| 4 921    | 2025-01-01 | 10 002.34   |
| 17 308   | 2025-01-01 | 10 156.78   |
| 8 044    | 2025-01-01 | 10 245.99   |
| 12 765   | 2025-01-01 | 10 388.50   |
| 22 419   | 2025-01-01 | 10 401.00   |

`BETWEEN 10000 AND 50000` est équivalent à `montant_ttc >= 10000 AND montant_ttc <= 50000`. Les
**deux** bornes sont incluses.

> **Piège classique.** Le débutant croit que `BETWEEN 1 AND 100` exclut le 100 (parce qu'en
> français « entre 1 et 100 » peut signifier « strictement entre »). En SQL, `BETWEEN` est
> **toujours inclusif**. Si on veut exclure la borne supérieure : `WHERE x >= 1 AND x < 100`.

### 5.4 `LIKE` et les jokers `%` et `_`

`LIKE` compare une chaîne à un **motif** contenant des jokers :

- `%` représente **n'importe quelle chaîne** (y compris la chaîne vide).
- `_` représente **un seul caractère** (n'importe lequel).

```sql
SELECT nom FROM client WHERE nom LIKE 'Client_0%';      -- commence par "Client_0"
SELECT nom FROM client WHERE nom LIKE '%0001';          -- finit par "0001"
SELECT nom FROM client WHERE nom LIKE '%100%';          -- contient "100"
SELECT nom FROM client WHERE nom LIKE 'Client_0___';    -- "Client_0" suivi de 3 caractères exactement
```

Sur la base, `LIKE 'C%'` retourne **1 200** lignes (tous les noms commencent par `C`),
`LIKE '%0001'` retourne 1 ligne (`Client_0001`), `LIKE '%100%'` retourne 11 lignes (les
`Client_0100`, `Client_1000`, `Client_1001`, …, `Client_1100`).

> **Dans les faits.** DuckDB `LIKE` est **sensible à la casse** (comme PostgreSQL). Pour
> ignorer la casse en PostgreSQL, on utilise `ILIKE` : `WHERE nom ILIKE 'c%'` accepte aussi
> `client_0001` minuscule. DuckDB n'a pas `ILIKE` mais a `LIKE` qui est par défaut insensible
> à la casse pour les caractères ASCII. Adapter selon le moteur.

### 5.5 `IS NULL` et `IS NOT NULL`

`NULL` représente l'absence de valeur. En SQL, c'est **un marqueur**, pas une valeur : `NULL
= NULL` retourne `NULL` (ni vrai, ni faux), pas `TRUE`.

```sql
-- Ne retourne JAMAIS de ligne, même si la colonne contient des NULL :
SELECT * FROM client WHERE nom = NULL;

-- Correct :
SELECT * FROM client WHERE nom IS NULL;

-- Et son contraire :
SELECT * FROM client WHERE nom IS NOT NULL;
```

Sur la base `commercial.duckdb`, la colonne `nom` de `client` n'a **aucun** `NULL` (les 1 200
clients ont tous un nom). La requête `WHERE nom IS NULL` retourne **0** ligne ; `IS NOT NULL`
retourne **1 200**.

> **Attention.** Le piège `= NULL` est le **bug n°1 du débutant SQL**. Il est silencieux
> (pas d'erreur, juste 0 ligne) et fait perdre des heures. La parade : remplacer `= NULL` par
> `IS NULL` partout.

### 5.6 Les dates — `BETWEEN`, `EXTRACT`, `date_trunc`

Trois cas fréquents :

**Cas 1 — Filtrer sur un intervalle de dates.**

```sql
SELECT id_vente, date_vente, montant_ttc FROM vente
WHERE date_vente BETWEEN '2025-06-01' AND '2025-12-31'
ORDER BY date_vente
LIMIT 3;
```

Résultat mesuré sur la base : 14 525 lignes (les ventes du 2ᵉ semestre 2025).

> **Piège.** `BETWEEN '2025-06-01' AND '2025-12-31'` inclut **les deux** bornes. Le 31 décembre
> 2025 est inclus ; si on veut l'exclure, on écrit `BETWEEN '2025-06-01' AND '2026-01-01'` ou
> `>= '2025-06-01' AND < '2026-01-01'`.

**Cas 2 — Filtrer sur une partie de la date (l'année, le mois, le jour de la semaine).**

```sql
SELECT id_vente, date_vente, montant_ttc FROM vente
WHERE EXTRACT(YEAR FROM date_vente) = 2025
  AND EXTRACT(MONTH FROM date_vente) = 6
LIMIT 3;
```

`EXTRACT(part FROM date)` extrait une partie : `YEAR`, `MONTH`, `DAY`, `DOW` (jour de la
semaine, 0 = dimanche), `DOY` (jour de l'année), `WEEK`, etc.

**Cas 3 — Regrouper par mois (tronquer la date au 1ᵉʳ du mois).**

```sql
SELECT date_trunc('month', date_vente) AS mois, COUNT(*) AS nb_ventes
FROM vente
GROUP BY 1
ORDER BY 1;
```

`date_trunc('month', date)` retourne le 1ᵉʳ du mois. Très utilisé pour les rapports mensuels.

> **Définition.** `EXTRACT(part FROM date)` — *extract* — extrait une partie de la date : année,
> mois, jour, heure, minute, seconde, jour de la semaine, etc. DuckDB et PostgreSQL supportent
> les mêmes mots-clés (`YEAR`, `MONTH`, `DAY`, `DOW`, `WEEK`, etc.).

> **Définition.** La **logique à trois valeurs** — *three-valued logic* — est la logique du SQL
> qui admet trois valeurs de vérité : `TRUE`, `FALSE`, et `NULL` (l'inconnu). Toute comparaison
> avec `NULL` retourne `NULL`, qui est traité comme « faux » par `WHERE`. C'est ce qui rend
> `WHERE col = NULL` inopérant.

### 5.7 Les priorités logiques — `AND` avant `OR`

C'est **la** source de bugs la plus subtile du `WHERE`. En SQL, `AND` est plus prioritaire que
`OR`, comme `×` est plus prioritaire que `+` en arithmétique.

```sql
-- Cette requête filtre : type = 'particulier' ET (ville = Ouaga OU ville = Bobo)
SELECT COUNT(*) FROM client
WHERE type_client = 'particulier'
  AND (ville = 'Ouagadougou' OR ville = 'Bobo-Dioulasso');
-- Résultat mesuré : 677

-- SANS les parenthèses, le AND est prioritaire : (type = particulier ET ville = Ouaga) OU (ville = Bobo)
SELECT COUNT(*) FROM client
WHERE type_client = 'particulier'
  AND ville = 'Ouagadougou' OR ville = 'Bobo-Dioulasso';
-- Résultat mesuré : 1 200 - 27 = 1 173 (Ouaga OU Bobo, filtre type ignoré pour Bobo)
```

Les deux requêtes retournent des résultats **très différents** (677 vs 1 173), et seule la
première (avec parenthèses) exprime la question « les particuliers qui habitent Ouaga ou Bobo ».

> **À retenir.** Quand on mélange `AND` et `OR`, **toujours parenthéser**. C'est plus lisible,
> et c'est plus sûr. La règle « `AND` avant `OR` » est vraie mais contre-intuitive.

### 5.8 `NOT` — la négation logique

`NOT` inverse le sens d'une condition :

```sql
SELECT * FROM client WHERE NOT (ville = 'Koudougou');
-- Équivalent à : WHERE ville <> 'Koudougou'
SELECT * FROM client WHERE ville <> 'Koudougou';
```

Les deux formes retournent les 1 200 − 27 = 1 173 clients qui ne sont **pas** à Koudougou.

> **Piège `NOT IN` et `NULL`.** Comme dit en §5.2, `NOT IN (…, NULL, …)` retourne toujours
> 0 ligne. Parade : `WHERE NOT EXISTS (…)` (vu en C08), ou exclure les `NULL` au préalable.

### 5.9 Combiner `WHERE` avec d'autres clauses

`WHERE` se combine avec `GROUP BY` (C05), `ORDER BY` (C03), `LIMIT` (C01). Voici un exemple
complet qui mobilise C01-C02 :

```sql
SELECT ville, COUNT(*) AS nb_clients
FROM client
WHERE type_client = 'particulier'
GROUP BY ville
ORDER BY nb_clients DESC;
```

| ville          | nb_clients |
|----------------|------------|
| Ouagadougou    | 339        |
| Bobo-Dioulasso | 441        |
| Koudougou      | 70         |

Les 850 particuliers se répartissent ainsi (Bobo est légèrement plus gros, parce que la
génération aléatoire a favorisé cette ville).

### 5.10 Ce que ce chapitre ne couvre pas

Pour rester focalisé sur le filtrage, ce chapitre **ne couvre pas** :

- les **agrégats** dans `WHERE` (`WHERE COUNT(*) > 100` est impossible ; utiliser `HAVING`) —
  c'est le **C04-C05** ;
- les **jointures** avec filtres sur plusieurs tables (`WHERE` + `JOIN`) — c'est le **C07** ;
- les **sous-requêtes** dans `WHERE` (`WHERE id IN (SELECT id FROM …)`) — c'est le **C08**.

## 6. Exemple concret — la requête qui répond à une question métier

Le directeur commercial demande : *« Combien de clients particuliers avons-nous à Ouaga ou Bobo,
et combien ont un plafond de crédit supérieur à 100 000 FCFA ? »*

**Étape 1 — Écrire la requête.**

```sql
SELECT ville, COUNT(*) AS nb
FROM client
WHERE type_client = 'particulier'
  AND (ville = 'Ouagadougou' OR ville = 'Bobo-Dioulasso')
  AND plafond_credit > 100000
GROUP BY ville
ORDER BY nb DESC;
```

**Étape 2 — Prédire la sortie.**

`FROM client` charge 1 200 lignes. `WHERE` filtre : type particulier (850), puis ville dans
(Ouaga, Bobo) → 677, puis plafond > 100k → ~ 200. `GROUP BY ville` regroupe par ville.
Résultat attendu : 2 lignes, Ouaga et Bobo.

**Étape 3 — Exécuter dans DuckDB CLI.**

```bash
duckdb commercial.duckdb
```

puis :

```sql
SELECT ville, COUNT(*) AS nb FROM client
WHERE type_client = 'particulier'
  AND (ville = 'Ouagadougou' OR ville = 'Bobo-Dioulasso')
  AND plafond_credit > 100000
GROUP BY ville ORDER BY nb DESC;
```

| ville          | nb  |
|----------------|-----|
| Bobo-Dioulasso | 87  |
| Ouagadougou    | 79  |

**Étape 4 — Comparer à la prédiction.** 2 lignes, dans l'ordre décroissant. ✓

> **Conseil professionnel.** Toujours **prédire la sortie** avant d'exécuter. Une requête SQL
> qui retourne 0 ligne doit faire réfléchir : ai-je filtré trop ? ai-je écrit `=` au lieu de
> `IS` ? ai-je mis une date au format `MM/JJ/AAAA` au lieu de `AAAA-MM-JJ` ?

## 7. Démonstration pas à pas — 7 requêtes sur le fil rouge

### 7.1 Question 1 — Combien de clients à Ouagadougou ?

```sql
SELECT COUNT(*) FROM client WHERE ville = 'Ouagadougou';
-- 512
```

### 7.2 Question 2 — Combien de ventes entre juin et décembre 2025 ?

```sql
SELECT COUNT(*) FROM vente
WHERE date_vente BETWEEN '2025-06-01' AND '2025-12-31';
-- 14 525
```

### 7.3 Question 3 — Les clients dont le nom commence par `C`

```sql
SELECT COUNT(*) FROM client WHERE nom LIKE 'C%';
-- 1 200 (tous)
```

### 7.4 Question 4 — Les clients particuliers à Ouaga, Bobo ou Koudougou

```sql
SELECT COUNT(*) FROM client
WHERE type_client = 'particulier'
  AND ville IN ('Ouagadougou', 'Bobo-Dioulasso', 'Koudougou');
-- 850 (tous les particuliers, qui sont tous dans ces 3 villes)
```

### 7.5 Question 5 — Les produits inactifs (5 % des 380)

```sql
SELECT COUNT(*) FROM produit WHERE actif = FALSE;
-- 18 (et non 19, car la génération aléatoire peut varier)
```

### 7.6 Question 6 — Les ventes du dimanche

```sql
SELECT COUNT(*) FROM vente WHERE EXTRACT(DOW FROM date_vente) = 0;
-- 7 136 (1/7 des ventes, comme attendu)
```

### 7.7 Question 7 — Les ventes à TVA 18 % (piège : taux stocké en colonne)

```sql
SELECT COUNT(*) FROM vente WHERE taux_tva = 0.18;
-- 24 920 (les ventes de 2025)
```

> **Attention.** Le piège classique : comparer `taux_tva = 18` (entier) au lieu de `0.18`
> (réel). DuckDB retournerait 0 ligne parce que la colonne est `REAL` (réel) ; PostgreSQL ferait
> la conversion implicite. Toujours utiliser la **même unité** dans la comparaison.

## 8. Erreurs fréquentes

1. **`WHERE colonne = NULL`** — ne retourne jamais rien. Utiliser `IS NULL`.

2. **`BETWEEN x AND y` et la borne supérieure** — elle est **incluse**. Le piège : oublier que
   `BETWEEN 1 AND 100` inclut le 100.

3. **`NOT IN` avec `NULL`** — retourne toujours 0 ligne si la liste contient un `NULL`. Parade :
   `NOT EXISTS` (C08).

4. **Priorités logiques** — `AND` est plus prioritaire que `OR`. Toujours parenthéser quand on
   mélange les deux.

5. **Comparer des dates comme des chaînes** — `WHERE date_vente = '2025-01-01'` fonctionne si le
   format est `AAAA-MM-JJ` ; avec `JJ/MM/AAAA`, DuckDB refuse. Toujours utiliser le format
   ISO 8601 (`AAAA-MM-JJ`).

6. **`LIKE` sensible à la casse** — en PostgreSQL, `'Client' LIKE 'c%'` est faux. Utiliser
   `ILIKE` si on veut ignorer la casse, ou forcer la casse (`LOWER(nom) LIKE 'c%'`).

7. **`EXTRACT` sur une chaîne** — `EXTRACT(YEAR FROM '2025-01-01')` (sans caster en `DATE`)
   peut échouer selon le moteur. Caster d'abord : `EXTRACT(YEAR FROM CAST('2025-01-01' AS DATE))`.

8. **`BETWEEN` sur des entiers ET des réels** — `WHERE montant BETWEEN 1000 AND 5000.5` mélange
   les types ; DuckDB fait la conversion implicite, d'autres SGBD non. Toujours être explicite.

## 9. Bonnes pratiques professionnelles

- **Prédire la sortie** avant d'exécuter (surtout le **nombre** de lignes attendues).
- **Parenthéser** systématiquement quand on mélange `AND` et `OR`.
- **Utiliser `IS NULL` / `IS NOT NULL`**, jamais `= NULL` ou `<> NULL`.
- **Préférez `IN` à une cascade de `OR`** quand la liste a plus de 2 éléments (lisibilité).
- **Utilisez les alias de table** (`FROM client AS c`) dès que la requête a plus d'une clause
  `WHERE` (lisibilité).
- **Commentez les filtres métier** complexes avec un en-tête de 3 lignes (question, tables
  utilisées, piège éventuel).
- **Testez toujours la borne supérieure** d'un `BETWEEN` : `BETWEEN '2025-01-01' AND '2025-01-31'`
  inclut le 31 (qui existe dans la base), mais `BETWEEN '2025-02-01' AND '2025-02-31'` ne
  fonctionne pas (le 31 février n'existe pas).
- **Documentez les filtres exotiques** dans le commentaire d'en-tête : `WHERE taux_tva = 0.18`
  est plus clair si on lit `-- Filtre sur l'année 2025 (TVA à 18 %)`.

> **À retenir.** `WHERE` filtre les lignes **avant** agrégation ; c'est la clause la plus
> utilisée. Les 6 opérateurs de comparaison + les 4 raccourcis (`IN`, `BETWEEN`, `LIKE`,
> `IS NULL`) couvrent 95 % des besoins. Les **priorités logiques** (`AND` avant `OR`) sont la
> source de bugs la plus subtile : **toujours parenthéser** quand on mélange les deux. Le
> prochain chapitre (C03) installe le tri (`ORDER BY`) et la pagination (`LIMIT`/`OFFSET`).

## 10. Exercice guidé — la lettre au collègue (20 min, /12)

Un collègue vous envoie un courriel : *« Bonjour, peux-tu me donner la liste des 20 premières
ventes du 2ᵉ semestre 2025 (entre le 1ᵉʳ juin et le 31 décembre) qui ont un montant supérieur à
50 000 FCFA et qui ont eu lieu à Ouagadougou ? Je veux le `id_vente`, la `date_vente`, le
`montant_ttc` et le `id_magasin`, triés par date. »*

**Travail demandé** :

1. **(3 pts)** Écrire la requête SQL.
2. **(3 pts)** Prédire le nombre de lignes retournées (en vous aidant des chiffres du chapitre).
3. **(3 pts)** Exécuter dans DuckDB CLI.
4. **(3 pts)** Comparer à la prédiction et expliquer l'écart.

**Correction** :

```sql
SELECT v.id_vente, v.date_vente, v.montant_ttc, v.id_magasin
FROM vente AS v
JOIN client AS c ON v.id_client = c.id_client
WHERE v.date_vente BETWEEN '2025-06-01' AND '2025-12-31'
  AND v.montant_ttc > 50000
  AND c.ville = 'Ouagadougou'
ORDER BY v.date_vente
LIMIT 20;
```

> **Note** : la requête utilise une jointure (`JOIN`) pour relier `vente` à `client` et filtrer
> sur la ville du client. La jointure est détaillée en C07 ; pour cet exercice, l'apprenant peut
> aussi filtrer par `id_magasin IN (1, 2)` (les 2 magasins d'Ouagadougou) sans jointure — c'est
> moins lisible mais ça marche.

Prédiction : ~ 14 525 ventes au 2ᵉ semestre 2025, dont ~ 1/5 > 50 000 FCFA (~ 2 900), dont ~ 2/5
à Ouaga (~ 1 160). `LIMIT 20` ramène les 20 premières.

## 11. Exercices autonomes

**Exercice 2.1.** Écrire une requête qui retourne tous les clients dont le `plafond_credit`
est supérieur à 500 000 FCFA. Combien sont-ils ?

**Exercice 2.2.** Écrire une requête qui retourne les produits de la catégorie 1
(`id_categorie = 1`) qui sont actifs. Combien sont-ils ?

**Exercice 2.3.** Écrire une requête qui retourne les ventes du **mois de mars 2026** (n'importe
quelle année du 1ᵉʳ au 31 mars). Utiliser `EXTRACT`.

**Exercice 2.4.** Écrire une requête qui retourne les clients dont le nom contient la chaîne
« 100 ». Combien sont-ils ?

**Exercice 2.5.** Écrire une requête qui retourne les clients qui ne sont **pas** à Ouagadougou.
Combien sont-ils ?

**Exercice 2.6.** Écrire une requête qui retourne les ventes où `date_vente > date_limite_remise`.
C'est le **piège P3** du module M07 — la requête naïve compte trop de lignes.

**Exercice 2.7.** Pourquoi la requête suivante est-elle dangereuse ?

```sql
-- ERREUR ATTENDUE : requête destructrice, à ne jamais exécuter sur une base vivante
DELETE FROM vente WHERE date_vente < '2025-01-01';
```

**Exercice 2.8.** Prédire la sortie de :

```sql
SELECT COUNT(*) FROM client
WHERE type_client = 'particulier' AND ville = 'Ouagadougou' OR ville = 'Bobo-Dioulasso';
```

## 12. Correction détaillée

**Exercice 2.1.** `SELECT COUNT(*) FROM client WHERE plafond_credit > 500000;` — environ 240
clients (par construction, 20 % des 1 200 ont un plafond élevé).

**Exercice 2.2.** `SELECT COUNT(*) FROM produit WHERE id_categorie = 1 AND actif = TRUE;` —
environ 47 produits (380 / 8 = 47,5 par catégorie, 95 % actifs).

**Exercice 2.3.** `SELECT COUNT(*) FROM vente WHERE EXTRACT(YEAR FROM date_vente) = 2026 AND
EXTRACT(MONTH FROM date_vente) = 3;` — environ 4 000 ventes (1/24 des 50 008).

**Exercice 2.4.** `SELECT COUNT(*) FROM client WHERE nom LIKE '%100%';` — 11 clients
(`Client_0100`, `Client_1000`, `Client_1001`, …, `Client_1100`).

**Exercice 2.5.** `SELECT COUNT(*) FROM client WHERE ville <> 'Ouagadougou';` — 1 200 − 512 = 688
clients.

**Exercice 2.6.** `SELECT COUNT(*) FROM vente WHERE date_vente > date_limite_remise;` — 21 406
lignes. C'est **énorme** : 43 % des ventes ont une date inversée. Le piège P3 n'est pas un cas
rare ; c'est un vice caché de la base. **C07** apprendra à le contourner.

**Exercice 2.7.** La requête supprime **toutes** les ventes avant le 1ᵉʳ janvier 2025 (24 mois
de données historiques). Sur la base `commercial.duckdb`, ça représente environ la moitié de
la table. C'est une **opération destructrice** : il faut (a) faire un `SELECT` avant pour voir
combien de lignes seraient supprimées ; (b) faire une sauvegarde (`EXPORT DATABASE`) ; (c)
exécuter dans une transaction (`BEGIN; … COMMIT;` ou `ROLLBACK;`). Le `DELETE` est détaillé dans
un module ultérieur.

**Exercice 2.8.** La requête est parsée comme
`WHERE (type_client = 'particulier' AND ville = 'Ouagadougou') OR (ville = 'Bobo-Dioulasso')`.
Résultat : tous les Bobolais (661) **plus** les particuliers d'Ouaga (339) = **1 000** lignes
(et non 677 comme attendu). Le piège : oublier les parenthèses.

## 13. Mini-projet M07.P2 — « Le filtre des 7 questions » (1 h)

Le responsable de la relation client vous demande **7 chiffres** sur le portefeuille :

1. Combien de clients **particuliers** ?
2. Combien de clients **entreprise** ?
3. Combien de clients **comptoir** ?
4. Parmi les particuliers, combien à **Ouagadougou** ?
5. Parmi les particuliers, combien ont un **plafond > 100 000 FCFA** ?
6. Combien de clients dont le nom se termine par **`0001`** ou **`0100`** ?
7. Combien de clients dont le nom commence par **`C`** et finit par **`0`** ?

**Critère de réussite** : 7 requêtes (une par question), chacune avec un **commentaire**
(1 ligne au-dessus : la question métier), et la **prédiction du résultat** dans le commentaire
(« attendu : ~ 850 »). Comparez ensuite à l'exécution.

> **Bonus** : réécrivez les 7 requêtes en utilisant **uniquement** `WHERE`, sans `GROUP BY` ni
> `ORDER BY`. C'est l'exercice inverse du mini-projet M07.P1 : on filtre, on n'agrège pas.

## 14. Boîte à outils du chapitre

> **Boîte à outils.** Ce chapitre utilise 4 outils de filtrage : `=` (comparaison stricte),
> `<>` (différent), `IN/BETWEEN` (raccourcis de comparaison), `LIKE` (chaînes avec jokers),
> `IS NULL` (test d'absence de valeur). DuckDB et PostgreSQL partagent la même syntaxe ; SQLite
> omet `ILIKE` et certaines fonctions `EXTRACT`.

| Outil | Usage | Syntaxe | Piège |
|---|---|---|---|
| `=` | comparaison stricte | `WHERE col = val` | ne marche pas avec `NULL` |
| `<>` | différent | `WHERE col <> val` | ne marche pas avec `NULL` |
| `IN` | appartenance à une liste | `WHERE col IN (a, b, c)` | `NOT IN` avec `NULL` retourne 0 ligne |
| `BETWEEN` | intervalle bornes incluses | `WHERE col BETWEEN x AND y` | la borne supérieure est incluse |
| `LIKE` | motif sur chaîne | `WHERE col LIKE '%mot%'` | sensible à la casse en PostgreSQL |
| `IS NULL` | test d'absence | `WHERE col IS NULL` | ne pas écrire `= NULL` |
| `EXTRACT` | partie d'une date | `WHERE EXTRACT(YEAR FROM date) = 2025` | caster la date d'abord |
| `date_trunc` | tronquer la date | `GROUP BY date_trunc('month', date)` | — |

## 15. Résumé du chapitre

- Le `WHERE` est la clause qui **filtre les lignes** avant agrégation. C'est la clause la plus
  utilisée.
- Les **6 opérateurs** : `=`, `<>`, `<`, `>`, `<=`, `>=`.
- Les **4 raccourcis** : `IN`, `BETWEEN`, `LIKE`, `IS NULL`. Chacun a un piège dédié.
- Les **priorités logiques** : `AND` avant `OR`. Toujours parenthéser quand on mélange.
- Les **dates** : `BETWEEN`, `EXTRACT`, `date_trunc` couvrent 90 % des besoins.
- Le **piège P3** du fil rouge : 21 406 ventes sur 50 008 ont `date_vente > date_limite_remise`.
  C'est un vice caché que C07 apprendra à contourner.

## 16. À retenir

- **`WHERE` filtre les lignes avant agrégation** ; `HAVING` filtre les groupes après (vu en C05).
- **Les priorités logiques** : `AND` est plus prioritaire que `OR`. Toujours parenthéser.
- **`= NULL` ne marche jamais** ; utiliser `IS NULL`.
- **`NOT IN` avec `NULL` retourne 0 ligne** ; utiliser `NOT EXISTS` (C08).
- **`BETWEEN` inclut les deux bornes** ; ne pas oublier la borne supérieure.
- **Le prochain chapitre (C03)** installe le tri (`ORDER BY`) et la pagination (`LIMIT`/`OFFSET`).

## 17. Évaluation formative (auto-correction, 10 min)

Sans document, en 10 minutes, répondre aux 6 questions. Auto-correction en bas.

1. Citez les **6 opérateurs de comparaison**.
2. Quelle est la différence entre `IN` et `OR` ? Donnez un cas où `IN` est plus lisible.
3. Que retourne `WHERE x BETWEEN 1 AND 10` quand `x = 10` ? Et `x = 11` ?
4. Pourquoi `WHERE col = NULL` est-il faux ? Comment écrire le bon filtre ?
5. Quelle est la priorité entre `AND` et `OR` ? Que faut-il faire en pratique ?
6. Comment filtre-t-on sur le **mois** d'une date ?

**Réponses** :

1. `=`, `<>`, `<`, `>`, `<=`, `>=`.
2. `IN (a, b, c)` est équivalent à `col = a OR col = b OR col = c`. `IN` est plus lisible quand la
   liste dépasse 2 éléments (par exemple, `ville IN ('Ouagadougou', 'Bobo-Dioulasso', 'Koudougou')`).
3. `WHERE x BETWEEN 1 AND 10` retourne `TRUE` quand `x = 10` (borne supérieure **incluse**).
   Retourne `FALSE` quand `x = 11`.
4. `NULL` n'est pas une valeur ; `col = NULL` retourne `NULL`, qui est traité comme faux par
   `WHERE`. Il faut écrire `col IS NULL`.
5. `AND` est plus prioritaire que `OR`. En pratique, **toujours parenthéser** quand on mélange
   les deux, pour la lisibilité et pour éviter les bugs.
6. Avec `EXTRACT(MONTH FROM date_col) = 6` (juin), ou `BETWEEN '2025-06-01' AND '2025-06-30'`.
