# Module M07.C04 — Agréger : COUNT, SUM, AVG, MIN, MAX, ROUND

**Outils comparés : DuckDB 1.5.5 (CLI + Python), SQLite natif Python, PostgreSQL cité.
Durée indicative : 4 h. Niveau : N2 → N3. Prérequis : M07.C01 (SELECT, FROM, alias) ; M07.C02 (WHERE) ; M07.C03 (ORDER BY, LIMIT).**

> **L'idée du chapitre.** Jusqu'ici, nos requêtes renvoyaient des **lignes** : une vente, un
> client, un produit. C04 change d'échelle : **réduire N lignes à un chiffre**. « Quel est le
> chiffre d'affaires total ? » « Quel est le panier moyen ? » « Quel est le plus gros montant ? »
> Ce sont des questions d'**agrégation** : `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, complétées par
> `ROUND`. Le chapitre couvre les cinq fonctions d'agrégat, le comptage de valeurs distinctes,
> le comportement particulier des `NULL` (ignorés par tous les agrégats sauf `COUNT(*)`), et la
> règle d'or qui prépare C05 : **une colonne non agrégée dans `SELECT` exige `GROUP BY`**.
> Le fil rouge est la base `commercial.duckdb` : on y mesure un CA brut de
> **7 908 259 731 FCFA**, un panier moyen de **158 140 FCFA**, et un montant minimum de
> **763 FCFA**.

> **Base de travail — `commercial.duckdb` (empreinte `0b9c12397d9c8af2…`).** Le chapitre
> mobilise : 50 008 ventes (CA brut 7 908 259 731 FCFA), 1 200 clients, 5 modes de paiement
> (Especes : 20 175 ventes ; Carte Bancaire : 12 366 ; Mobile Money : 12 322 ; Credit 30j :
> 2 593 ; Virement : 2 552), et des montants TTC compris entre **763** et **594 363 FCFA**.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

- **compter** les lignes avec `COUNT(*)`, les valeurs non nulles avec `COUNT(colonne)`, les
  valeurs distinctes avec `COUNT(DISTINCT colonne)` ;
- **totaliser** avec `SUM`, **moyenner** avec `AVG`, extraire le **minimum** et le
  **maximum** avec `MIN` / `MAX` ;
- **arrondir** un résultat avec `ROUND(valeur, nb_decimales)` ;
- **expliquer pourquoi** les `NULL` disparaissent des agrégats (sauf `COUNT(*)`) ;
- **combiner** plusieurs agrégats dans une même requête pour produire une ligne de synthèse ;
- **identifier l'erreur** « colonne non agrégée sans GROUP BY » et la résoudre (anticipation
  de C05).

## 2. Pourquoi cette notion est importante

- Presque toute question métier est une question d'agrégat : « combien de ventes ? », « quel
  CA ? », « quel est le panier moyen ? », « quelle est la plus grosse facture ? ». C'est le
  passage de **l'exploration de données** (C01–C03) à **la mesure** (C04–C05).
- Le **comportement des `NULL`** dans les agrégats est l'une des sources d'erreur les plus
  classiques : `AVG` qui sous-estime, `COUNT` qui diverge de `COUNT(*)`, `SUM` qui renvoie
  `NULL` sur une colonne tout entière vide.
- La **règle colonne non agrégée / `GROUP BY`** est la frontière entre C04 (une ligne de
  synthèse sur toute la table) et C05 (une ligne de synthèse par groupe). La comprendre
  maintenant évite les erreurs les plus fréquentes du module.

## 3. Explication simple — l'agrégat est une plieuse de lignes

Imaginez un tas de 50 008 tickets de caisse sur un bureau. La question « quel est le montant
minimum ? » ne demande pas de lire les tickets un par un et de les recopier : on **scanne**
le tas, on retient un seul ticket — le plus petit. La question « quel est le total ? »
demande d'**additionner** — mais, encore une fois, un seul chiffre sort du tas.

C'est exactement ce que fait un agrégat : il **consomme N lignes** et **produit 1 valeur**.
La requête

```sql
SELECT SUM(montant_ttc) AS ca_total
FROM vente;
```

lit les 50 008 lignes de `vente`, additionne la colonne `montant_ttc`, et renvoie **une
seule ligne contenant un seul chiffre** : 7 908 259 731 FCFA (arrondi au franc). Le mot-clé
`SELECT` n'a pas changé de syntaxe ; c'est le **comportement** qui change : dès qu'une
fonction d'agrégat apparaît, le résultat est **réduit à une ligne** (sauf `GROUP BY`, C05).

> **Définition.** Une **fonction d'agrégat** — *aggregate function* — est une fonction qui
> prend un ensemble de valeurs (les lignes d'un groupe) en entrée et produit une **unique
> valeur** en sortie. Les cinq agrégats standard sont `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`.
> Ils s'écrivent `fonction(arg)`, par exemple `SUM(montant_ttc)`.

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **agrégat** | fonction qui consomme N valeurs et produit 1 valeur. | l'utiliser sur une colonne texte avec `SUM` (erreur de type). |
| **COUNT(\*)** | nombre de **lignes** (tout contenu, `NULL` inclus). | le confondre avec `COUNT(colonne)`. |
| **COUNT(DISTINCT …)** | nombre de **valeurs différentes** d'une colonne. | croire qu'il compte les lignes (il compte les valeurs uniques). |
| **SUM** | somme des valeurs non nulles. | attendre 0 sur une colonne 100 % `NULL` (on obtient `NULL`). |
| **AVG** | moyenne arithmétique = `SUM` / `COUNT(non-NULL)`. | croire que les `NULL` comptent dans le dénominateur (ils ne comptent pas). |
| **MIN / MAX** | valeur minimale / maximale (montants, dates, textes). | les appliquer sur un texte en oubliant l'ordre lexicographique. |
| **ROUND(x, n)** | arrondi de `x` à `n` décimales (défaut 0). | arrondir trop tôt (fausse les totaux en aval). |
| **ligne de synthèse** | résultat unique d'agrégats sans `GROUP BY`. | y mélanger une colonne non agrégée (erreur `GROUP BY`). |
| **comptage conditionnel** | `SUM(CASE WHEN … THEN 1 ELSE 0 END)` : compter « les X qui ». | l'écrire en `WHERE` quand on veut plusieurs mesures à la fois. |
| **null-skipping** | les `NULL` sont ignorés par les agrégats (sauf `COUNT(*)`). | oublier que `SUM` renvoie `NULL` si tout est `NULL`. |

## 5. Cours approfondi

### 5.1 `COUNT(*)` : compter les lignes

```sql
SELECT COUNT(*) AS nb_ventes
FROM vente;
```

`COUNT(*)` compte **toutes les lignes** du résultat, qu'elles contiennent des `NULL` ou
non. Sur la base de travail : **50 008** lignes. C'est l'agrégat de vérification de
premier rang : il confirme qu'une table « contient bien » le volume attendu.

### 5.2 `COUNT(colonne)` : compter les valeurs non nulles

```sql
SELECT COUNT(montant_ttc) AS nb_montants
FROM vente;
```

`COUNT(colonne)` ne compte **que les valeurs non nulles** de la colonne. Sur la base de
travail, `montant_ttc` n'a aucun `NULL` : le résultat est **50 008**, identique à
`COUNT(*)`. La différence n'apparaît que quand des `NULL` existent : c'est alors un
indicateur de qualité de données (« combien de lignes ont un montant ? »).

### 5.3 `COUNT(DISTINCT colonne)` : compter les valeurs différentes

```sql
SELECT COUNT(DISTINCT id_client) AS nb_clients_actifs
FROM vente;
```

`COUNT(DISTINCT …)` compte les **valeurs différentes**. Sur les 50 008 ventes, il y a
**1 200** clients distincts — chaque client a au moins une vente (la plupart, beaucoup).
Cette écriture est le geste standard pour répondre à « combien de clients ont réellement
acheté ? ».

> **Définition.** Le **comptage distinct** — *distinct count* — compte les valeurs uniques
> d'une colonne au lieu de toutes les lignes. `COUNT(DISTINCT id_client)` répond à « combien
> de clients différents ? » ; il ignore les répétitions. C'est plus coûteux qu'un
> `COUNT(*)` car le moteur doit mémoriser (ou trier) les valeurs déjà vues.

### 5.4 `SUM` et `AVG` : totaliser et moyenner

```sql
SELECT SUM(montant_ttc) AS ca_total,
       AVG(montant_ttc) AS panier_moyen
FROM vente;
```

Le total s'élève à **7 908 259 731 FCFA** (arrondi au franc) — c'est le **CA brut**,
retours inclus (piège P2, rappelé en C02). Le panier moyen vaut **158 140 FCFA**
(arrondi). `AVG` est défini par le moteur comme `SUM(colonne) / COUNT(colonne)` : les
`NULL` sont exclus du dénominateur comme du numérateur, ce qui évite la sous-estimation.

> **Définition.** Le **panier moyen** — *average order value* (AOV) — est le montant moyen
> d'une vente, calculé par `AVG(montant_ttc)`. Sur la base de travail : **158 140 FCFA**.
> Il est l'un des indicateurs commerciaux de premier rang, car il mesure la valeur d'une
> transaction type sans dépendre du volume de ventes.

### 5.5 `MIN` et `MAX` : les bornes

```sql
SELECT MIN(montant_ttc) AS montant_min,
       MAX(montant_ttc) AS montant_max
FROM vente;
```

Le montant minimum est de **763 FCFA** (arrondi) et le maximum de **594 363 FCFA**
(plafond du générateur, mesuré en C03). `MIN` et `MAX` fonctionnent aussi sur les dates
(`MIN(date_vente)` = première vente) et les textes (ordre lexicographique) — pas seulement
sur les montants.

### 5.6 `ROUND` : arrondir pour présenter

Les agrégats produisent souvent des décimales inutiles en FCFA. `ROUND` sert à
**présenter** le chiffre :

```sql
SELECT ROUND(SUM(montant_ttc))       AS ca_total,
       ROUND(AVG(montant_ttc))       AS panier_moyen,
       ROUND(AVG(montant_ttc), 2)    AS panier_precis
FROM vente;
```

`ca_total` = 7 908 259 731 ; `panier_moyen` = 158 140 ; `panier_precis` conserve deux
décimales. Règle : **`ROUND(valeur, n)` arrondit à `n` décimales** ; sans `n`, l'arrondi
est à l'entier.

### 5.7 Les `NULL` et les agrégats : la règle unique

**Règle.** Tous les agrégats **ignorent les `NULL` de leur colonne**, à une exception :
`COUNT(*)`, qui compte les lignes (pas les valeurs).

| Agrégat              | `NULL` dans la colonne         | Colonne 100 % `NULL` |
|----------------------|--------------------------------|----------------------|
| `COUNT(*)`           | ignoré (compte les lignes)     | nombre de lignes     |
| `COUNT(colonne)`     | ignoré (ne compte que non-NULL)| `0`                  |
| `SUM(colonne)`       | ignoré (non compté)            | `NULL`               |
| `AVG(colonne)`       | ignoré (non compté)            | `NULL`               |
| `MIN` / `MAX`        | ignoré (non comparé)           | `NULL`               |

Sur la base de travail, **aucune colonne n'a de `NULL`** (le générateur les exclut, comme
noté en C03 §5.6) : `SUM`, `AVG`, `MIN`, `MAX` donnent donc des chiffres partout. La règle
reste essentielle dès qu'on importe des données réelles — et c'est l'objet de la
démonstration qui suit.

> **Définition.** L'**ignorance des `NULL`** — *null-skipping* — est le comportement par
> défaut des agrégats `SUM`, `AVG`, `MIN`, `MAX` (et `COUNT(colonne)`) : les valeurs
> `NULL` ne participent ni à la somme, ni au dénombrement, ni à la comparaison. Seule
> l'écriture `COUNT(*)` dénombre les lignes quelle que soit leur contenu.

> **Attention.** `SUM` et `AVG` renvoient **`NULL`** (pas 0) sur une colonne entièrement
> `NULL`. Si votre rapport affiche `NULL` là où il devrait afficher 0, c'est ce cas. La
> parade : `COALESCE(SUM(x), 0)` — fonction de M07.C06.

### 5.8 Position dans l'ordre d'exécution

Rappel de C01/C03 : `FROM` → `WHERE` → **`GROUP BY`** → `HAVING` → `SELECT` → `DISTINCT` →
`ORDER BY` → `LIMIT`. Sans `GROUP BY` (ce chapitre), les agrégats du `SELECT` agissent sur
**l'ensemble** des lignes survivantes après `WHERE` :

```sql
SELECT SUM(montant_ttc) AS ca_2025
FROM vente
WHERE date_vente >= '2025-01-01'
  AND date_vente <  '2026-01-01';
```

`WHERE` filtre d'abord (le filtre est appliqué **avant** l'agrégation) : le CA 2025 ne
tient compte que des ventes de 2025. C'est la différence fondamentale avec `HAVING`
(C05) : `WHERE` filtre **les lignes**, `HAVING` filtre **les groupes**.

### 5.9 Plusieurs agrégats dans une même requête

Rien n'interdit de combiner les agrégats dans un seul `SELECT` — le résultat reste
**une seule ligne** :

```sql
SELECT COUNT(*)                       AS nb_ventes,
       COUNT(DISTINCT id_client)      AS nb_clients,
       ROUND(SUM(montant_ttc))        AS ca_total,
       ROUND(AVG(montant_ttc))        AS panier_moyen,
       ROUND(MIN(montant_ttc))        AS montant_min,
       ROUND(MAX(montant_ttc))        AS montant_max
FROM vente;
```

| nb_ventes | nb_clients | ca_total       | panier_moyen | montant_min | montant_max |
|-----------|------------|----------------|--------------|-------------|-------------|
| 50 008    | 1 200      | 7 908 259 731  | 158 140      | 763         | 594 363     |

Une ligne, six chiffres : c'est le **format de synthèse** d'un rapport exécutif.

### 5.10 Agrégat conditionnel : compter « les X qui »

Question : « combien de ventes par Espèces, et combien par Carte Bancaire, **en une
seule ligne** ? » Le filtre `WHERE` ne suffit pas (il ne permet qu'un filtre unique) ; on
utilise une expression conditionnelle dans l'agrégat :

```sql
SELECT SUM(CASE WHEN id_mode = 1 THEN 1 ELSE 0 END) AS nb_especes,
       SUM(CASE WHEN id_mode = 2 THEN 1 ELSE 0 END) AS nb_cartes
FROM vente;
```

`nb_especes` = **20 175**, `nb_cartes` = **12 366**. Ce motif — agréguer une expression
`CASE` — est un outil central de C05 (comptages conditionnels).

> **À retenir.** Le motif `SUM(CASE WHEN … THEN 1 ELSE 0 END)` transforme un comptage
> conditionnel en **agrégat ordinaire** : il s'additionne, se combine avec d'autres
> agrégats, et ne produit toujours qu'une ligne. C'est l'outil des « tableaux de bord »
> (une ligne, plusieurs colonnes de mesures).

### 5.11 Ce que ce chapitre ne couvre pas

- `GROUP BY` (une ligne de synthèse **par groupe**) : C05.
- `HAVING` (filtre sur les groupes) : C05.
- `COALESCE`, `NULLIF` (traiter les `NULL` avant l'agrégation) : C06.
- Les fonctions de fenêtre (`SUM() OVER (PARTITION BY …)`) : M11.

## 6. Exemple concret — la requête qui répond à une question métier

La directrice financière demande : *« Quel est notre CA brut, et quel est le panier moyen
sur l'ensemble de l'historique ? »*

**Étape 1 — Écrire la requête.**

```sql
SELECT ROUND(SUM(montant_ttc))  AS ca_brut,
       ROUND(AVG(montant_ttc))  AS panier_moyen,
       COUNT(*)                 AS nb_ventes
FROM vente;
```

**Étape 2 — Prédire la sortie.** `FROM vente` charge 50 008 lignes ; aucun `WHERE` ;
pas de `GROUP BY` ; `SUM`, `AVG`, `COUNT` réduisent le tout à **une ligne de synthèse**.

**Étape 3 — Exécuter.** Sortie : ca_brut = 7 908 259 731, panier_moyen = 158 140,
nb_ventes = 50 008.

**Étape 4 — Comparer.** Trois chiffres, une ligne, tous cohérents : 7 908 259 731 / 50 008
≈ 158 140. Si le panier moyen ne redonnait pas le CA divisé par le nombre de ventes, il
faudrait revoir la requête (filtre oublié, table erronée).

> **Conseil professionnel.** Vérifiez **toujours la cohérence croisée** des agrégats
> d'une ligne de synthèse : `CA / nombre de ventes ≈ panier moyen`, `MAX ≥ AVG ≥ MIN`.
> Une incohérence (par exemple `MIN > MAX`) signale une erreur de requête ou de
> type — elle se repère en 5 secondes, bien avant le rapport.

## 7. Démonstration pas à pas — 6 requêtes sur le fil rouge

### 7.1 Question 1 — Combien de ventes au total ?

```sql
SELECT COUNT(*) AS nb_ventes
FROM vente;
```

→ **50 008** (dont 8 doublons et 200 retours inclus, cf. `6_pieges.md`).

### 7.2 Question 2 — Quel est le CA brut total ?

```sql
SELECT ROUND(SUM(montant_ttc)) AS ca_brut
FROM vente;
```

→ **7 908 259 731 FCFA**.

### 7.3 Question 3 — Quel est le panier moyen ?

```sql
SELECT ROUND(AVG(montant_ttc)) AS panier_moyen
FROM vente;
```

→ **158 140 FCFA**.

### 7.4 Question 4 — Bornes des montants

```sql
SELECT ROUND(MIN(montant_ttc)) AS min_m,
       ROUND(MAX(montant_ttc)) AS max_m
FROM vente;
```

→ **763** / **594 363 FCFA** (le maximum est le plafond du générateur, mesuré en C03).

### 7.5 Question 5 — Répartition par mode de paiement, en une ligne

```sql
SELECT SUM(CASE WHEN id_mode = 1 THEN 1 ELSE 0 END) AS especes,
       SUM(CASE WHEN id_mode = 2 THEN 1 ELSE 0 END) AS carte,
       SUM(CASE WHEN id_mode = 3 THEN 1 ELSE 0 END) AS mobile,
       SUM(CASE WHEN id_mode = 4 THEN 1 ELSE 0 END) AS credit_30j,
       SUM(CASE WHEN id_mode = 5 THEN 1 ELSE 0 END) AS virement
FROM vente;
```

→ 20 175 / 12 366 / 12 322 / 2 593 / 2 552. Les Espèces représentent plus de 40 % des
ventes ; le crédit 30j et le virement sont marginaux (5 % chacun).

### 7.6 Question 6 — CA par mode de paiement, en une ligne

```sql
SELECT ROUND(SUM(CASE WHEN id_mode = 1 THEN montant_ttc ELSE 0 END)) AS ca_especes,
       ROUND(SUM(CASE WHEN id_mode = 2 THEN montant_ttc ELSE 0 END)) AS ca_carte
FROM vente;
```

→ 3 184 889 570 FCFA (Especes) / 1 944 001 846 FCFA (Carte). Le même motif `CASE`
s'applique au **montant** au lieu du comptage : c'est la forme générale du « tableau de
bord en une ligne ».

> **À retenir.** Le motif `SUM(CASE WHEN … THEN montant ELSE 0 END)` est la forme
> générale du **tableau de bord en une ligne** : chaque colonne est une mesure
> conditionnelle. C'est exactement ce que `GROUP BY` (C05) généralisera en plusieurs
> lignes, une par groupe.

## 8. Erreurs fréquentes

| # | Erreur | Symptôme | Correction |
|---|--------|----------|------------|
| 1 | `SELECT id_client, COUNT(*) FROM vente;` sans `GROUP BY` | erreur « must appear in the GROUP BY clause » | `GROUP BY id_client` (C05), ou retirer la colonne non agrégée. |
| 2 | Attendre 0 de `SUM` sur une colonne vide | résultat `NULL` dans le rapport | `COALESCE(SUM(x), 0)`. |
| 3 | Confondre `COUNT(*)` et `COUNT(colonne)` | décompte inexpliqué | `COUNT(*)` = lignes ; `COUNT(col)` = valeurs non nulles. |
| 4 | Arrondir trop tôt | totaux incohérents en aval | `ROUND` uniquement dans le dernier `SELECT` affiché. |
| 5 | `SUM` sur une colonne texte | erreur de type | `SUM`/`AVG` sur des colonnes numériques uniquement. |
| 6 | `COUNT(DISTINCT a, b)` sur 2 colonnes | syntaxe refusée en DuckDB/PostgreSQL | `COUNT(DISTINCT a \|\| b)` ou table temporaire (C06+). |

> **Attention.** L'erreur 1 est **la plus fréquente** du module : on demande « une valeur
> par client » sans dire comment grouper. Le message du moteur est explicite (« must
> appear in the GROUP BY clause or be used in an aggregate function ») : dès qu'une
> colonne non agrégée est dans `SELECT`, le `GROUP BY` est obligatoire (C05).

## 9. Bonnes pratiques professionnelles

- **Un agrégat, un alias** : `SUM(montant_ttc) AS ca_total` — jamais de colonne sans nom
  dans un rapport.
- **`ROUND` à la présentation** : précision pleine en amont, arrondi au dernier `SELECT`.
- **Vérifier la cohérence croisée** : `CA / nb_ventes ≈ panier moyen` ; `MIN ≤ AVG ≤ MAX`.
- **`COUNT(*)` en contrôle** : avant tout agrégat, vérifier le volume de lignes attendues
  (sur `vente` : 50 008).
- **Documenter les `NULL`** : une colonne avec `NULL` doit être annotée dans le dictionnaire
  de données (M06), sinon `SUM`/`AVG` surprennent.
- **Commenter les comptages conditionnels** : « Espèces = id_mode 1, cf. `mode_paiement` ».

## 10. Exercice guidé — la synthèse mensuelle (15 min, /10)

**Énoncé.** Le chef de produit demande une **ligne de synthèse** de l'activité : nombre de
ventes, nombre de clients actifs, CA total, panier moyen, montant minimum, montant
maximum — le tout arrondi au franc, en une seule requête.

**Grille de correction (/10).**

| Critère | Points |
|---|---|
| 6 agrégats bien choisis (`COUNT(*)`, `COUNT(DISTINCT id_client)`, `SUM`, `AVG`, `MIN`, `MAX`) | 3 |
| 6 alias lisibles | 1 |
| 5 `ROUND` sur les montants | 1 |
| Une seule ligne produite (pas de colonne non agrégée) | 2 |
| `FROM vente` correct | 1 |
| Valeurs conformes (50 008 / 1 200 / 7 908 259 731 / 158 140 / 763 / 594 363) | 2 |

**Corrigé.**

```sql
SELECT COUNT(*)                   AS nb_ventes,
       COUNT(DISTINCT id_client)  AS nb_clients,
       ROUND(SUM(montant_ttc))    AS ca_total,
       ROUND(AVG(montant_ttc))    AS panier_moyen,
       ROUND(MIN(montant_ttc))    AS min_m,
       ROUND(MAX(montant_ttc))    AS max_m
FROM vente;
```

→ 50 008 / 1 200 / 7 908 259 731 / 158 140 / 763 / 594 363.

## 11. Exercices autonomes

### Exercice 1 — CA total, arrondi

Écrire la requête qui renvoie le CA brut total de `vente`, arrondi au franc.

### Exercice 2 — Panier moyen à deux décimales

### Exercice 3 — Nombre de clients distincts dans `vente`

### Exercice 4 — Bornes des montants (minimum et maximum arrondis)

### Exercice 5 — `COUNT(*)` vs `COUNT(montant_ttc)`

Expliquer pourquoi les deux renvoient 50 008 sur cette base, et dans quel cas ils
divergeraient.

### Exercice 6 — Comptage conditionnel par mode

Compter, dans une même requête, le nombre de ventes Espèces (id_mode 1) et Virement
(id_mode 5).

### Exercice 7 — CA par deux modes, en une ligne

Produire, en une ligne : le CA total Espèces et le CA total Carte Bancaire (arrondis).

### Exercice 8 — Diagnostic d'erreur

Que renvoie ce `SELECT`, et pourquoi ?

```sql
SELECT SUM(plafond_credit) FROM client;
```

## 12. Correction détaillée

**Exercice 1.**

```sql
SELECT ROUND(SUM(montant_ttc)) AS ca_total
FROM vente;
```

→ 7 908 259 731 FCFA.

**Exercice 2.**

```sql
SELECT ROUND(AVG(montant_ttc), 2) AS panier_moyen
FROM vente;
```

→ le panier moyen avec deux décimales (arrondi de la moyenne exacte).

**Exercice 3.**

```sql
SELECT COUNT(DISTINCT id_client) AS nb_clients
FROM vente;
```

→ 1 200.

**Exercice 4.**

```sql
SELECT ROUND(MIN(montant_ttc)) AS min_m,
       ROUND(MAX(montant_ttc)) AS max_m
FROM vente;
```

→ 763 / 594 363 FCFA.

**Exercice 5.** Sur `vente`, `montant_ttc` n'a aucun `NULL` : les deux comptent donc les
mêmes lignes (50 008). Ils divergeraient dès qu'une ligne de `vente` aurait
`montant_ttc = NULL` : `COUNT(*)` la compterait, `COUNT(montant_ttc)` non.

**Exercice 6.**

```sql
SELECT SUM(CASE WHEN id_mode = 1 THEN 1 ELSE 0 END) AS nb_especes,
       SUM(CASE WHEN id_mode = 5 THEN 1 ELSE 0 END) AS nb_virement
FROM vente;
```

→ 20 175 / 2 552.

**Exercice 7.**

```sql
SELECT ROUND(SUM(CASE WHEN id_mode = 1 THEN montant_ttc ELSE 0 END)) AS ca_especes,
       ROUND(SUM(CASE WHEN id_mode = 2 THEN montant_ttc ELSE 0 END)) AS ca_carte
FROM vente;
```

→ 3 184 889 570 / 1 944 001 846 FCFA.

**Exercice 8.** Sur le socle M07, les 1 200 clients ont tous un plafond (le générateur
exclut les `NULL`) : la somme additionne donc les 1 200 plafonds. Sur des données réelles
contenant des `NULL`, les clients sans plafond seraient **ignorés** par `SUM` ; et si aucun
client n'avait de plafond, le résultat serait `NULL` — pas 0. Pour afficher 0, écrire
`COALESCE(SUM(plafond_credit), 0)`.

## 13. Mini-projet — « La fiche de synthèse commerciale » (30 min)

Produire la **fiche de synthèse** de la base commerciale : une requête unique qui renvoie,
en une ligne, les 8 indicateurs ci-dessous. Vérifier chaque chiffre à la main (relever les
valeurs dans un tableur puis comparer).

| Indicateur               | Valeur attendue (arrondie) |
|--------------------------|----------------------------|
| Nombre de ventes         | 50 008                     |
| Clients actifs           | 1 200                      |
| CA brut total (FCFA)     | 7 908 259 731              |
| Panier moyen (FCFA)      | 158 140                    |
| Montant minimum (FCFA)   | 763                        |
| Montant maximum (FCFA)   | 594 363                    |
| Ventes Espèces            | 20 175                     |
| Ventes Virement           | 2 552                      |

**Corrigé.**

```sql
SELECT COUNT(*)                                    AS nb_ventes,
       COUNT(DISTINCT id_client)                  AS nb_clients,
       ROUND(SUM(montant_ttc))                    AS ca_total,
       ROUND(AVG(montant_ttc))                    AS panier_moyen,
       ROUND(MIN(montant_ttc))                    AS min_m,
       ROUND(MAX(montant_ttc))                    AS max_m,
       SUM(CASE WHEN id_mode = 1 THEN 1 ELSE 0 END) AS ventes_especes,
       SUM(CASE WHEN id_mode = 5 THEN 1 ELSE 0 END) AS ventes_virement
FROM vente;
```

**Critères de validation.** 8 colonnes, 1 ligne ; les 8 valeurs ci-dessus ; aucun avertissement
`GROUP BY` (toutes les colonnes du `SELECT` sont agrégées).

> **Dans les faits.** PostgreSQL accepte la même syntaxe avec le même résultat ; MySQL, en
> mode `ONLY_FULL_GROUP_BY` activé par défaut depuis la version 5.7, renvoie la même erreur
> qu'ici si une colonne non agrégée est présente, mais en mode permissif (ancien défaut) il
> **devine** une valeur arbitraire — la requête passe, et le chiffre est faux sans aucun
> signal. C'est pourquoi le mode permissif MySQL est à éviter en production.

## 14. Boîte à outils du chapitre

> **Boîte à outils.** Ce chapitre installe 6 outils de mesure : `COUNT` (lignes, valeurs,
> distinct), `SUM` (total), `AVG` (moyenne), `MIN`/`MAX` (bornes), `ROUND` (présentation),
> plus le motif `SUM(CASE WHEN …)` pour les comptages conditionnels. La règle d'or —
> colonne non agrégée ⇒ `GROUP BY` — est la porte d'entrée de C05.

| Outil | Usage | Syntaxe | Piège |
|---|---|---|---|
| `COUNT(*)` | nombre de lignes | `COUNT(*)` | confondre avec `COUNT(col)` |
| `COUNT(col)` | valeurs non nulles | `COUNT(montant_ttc)` | diverger de `COUNT(*)` si `NULL` |
| `COUNT(DISTINCT col)` | valeurs uniques | `COUNT(DISTINCT id_client)` | plus coûteux qu'un `COUNT(*)` |
| `SUM` / `AVG` | total / moyenne | `SUM(montant_ttc)` | renvoyer `NULL` si colonne 100 % `NULL` |
| `MIN` / `MAX` | bornes | `MAX(date_vente)` | ordre lexicographique sur texte |
| `ROUND(x, n)` | arrondi | `ROUND(AVG(montant_ttc), 2)` | arrondir trop tôt |
| `SUM(CASE …)` | comptage / somme conditionnelle | `SUM(CASE WHEN id_mode = 1 THEN 1 ELSE 0 END)` | `ELSE 0` obligatoire |

## 15. Résumé du chapitre

- **Un agrégat consomme N lignes et produit 1 valeur** : `COUNT`, `SUM`, `AVG`, `MIN`,
  `MAX`, plus `ROUND` pour la présentation.
- **`COUNT(*)`** compte les lignes ; **`COUNT(colonne)`** les valeurs non nulles ;
  **`COUNT(DISTINCT colonne)`** les valeurs différentes.
- **Les `NULL` sont ignorés** par `SUM`, `AVG`, `MIN`, `MAX`, `COUNT(colonne)` ; sur une
  colonne 100 % `NULL`, `SUM`/`AVG`/`MIN`/`MAX` renvoient `NULL` (pas 0) — parade :
  `COALESCE(agrégat, 0)`.
- **`WHERE` filtre les lignes avant l'agrégation** ; `HAVING` (C05) filtrera les groupes.
- **Colonne non agrégée dans `SELECT` sans `GROUP BY` = erreur** : c'est la règle d'or
  qui sépare C04 (synthèse globale) de C05 (synthèse par groupe).
- Le motif **`SUM(CASE WHEN …)`** produit les « tableaux de bord en une ligne » : une
  mesure conditionnelle par colonne.

## 16. À retenir

- **Un agrégat = N lignes → 1 valeur.** Toujours un alias par agrégat.
- **`COUNT(*)` ≠ `COUNT(colonne)`** dès qu'un `NULL` existe.
- **`NULL` ignorés** : `SUM`/`AVG` renvoient `NULL` sur une colonne vide — `COALESCE`
  pour forcer 0.
- **`ROUND` à la présentation** : précision pleine en amont, arrondi au dernier `SELECT`.
- **Colonne non agrégée sans `GROUP BY` = erreur** : la règle d'or, porte d'entrée de C05.

> **À retenir.** `AVG(colonne) = SUM(colonne) / COUNT(colonne)` : le dénominateur exclut
> les `NULL`. C'est la définition même du panier moyen — et la raison pour laquelle une
> moyenne « qui baisse sans raison » est souvent une entrée de `NULL` en moins.

## 17. Évaluation formative (auto-correction, 8 min)

Sans document, en 8 minutes, répondre aux 5 questions. Auto-correction en bas.

1. Quelle est la différence entre `COUNT(*)` et `COUNT(colonne)` ?
2. Que renvoie `SUM(colonne)` si toutes les valeurs de `colonne` sont `NULL` ?
3. `AVG` est-il défini comment par le moteur ?
4. Pourquoi `SELECT id_client, COUNT(*) FROM vente;` est-il une erreur ?
5. À quelle position de l'ordre d'exécution sont appliqués les agrégats du `SELECT` sans
   `GROUP BY` ?

**Réponses** :

1. `COUNT(*)` dénombre **les lignes** (tout contenu, `NULL` inclus) ; `COUNT(colonne)`
   dénombre **les valeurs non nulles** de la colonne. Les deux divergent dès qu'un `NULL`
   existe dans la colonne.
2. `NULL` — pas 0. L'agrégat n'a rien à sommer : l'absence de valeur s'exprime par
   `NULL`. La parade est `COALESCE(SUM(colonne), 0)`.
3. `AVG(colonne) = SUM(colonne) / COUNT(colonne)` — le dénominateur exclut les `NULL`,
   donc la moyenne est calculée sur les seules valeurs présentes.
4. Parce qu'`id_client` n'est **pas agrégé** et n'est **pas groupé** : le moteur ne sait
   pas quelle valeur de `id_client` retourner pour la ligne de synthèse. Il faut
   `GROUP BY id_client` (C05).
5. Après le `WHERE` (le filtre de lignes) : l'agrégat sans `GROUP BY` consomme
   l'ensemble des lignes survivantes à ce stade, avant le `SELECT` et le `DISTINCT`.
