# Module M06.C02 — Table, colonne, ligne, schéma, type, contrainte, valeur nulle

**Outils : DuckDB 1.5.5 (intégré), SQLite natif Python, PostgreSQL cité. Durée indicative : 6 h.
Niveau : N2. Prérequis : M06.C01 + M01.C03.**

> **L'idée du chapitre.** Le C01 a posé **pourquoi** une base : redondance, anomalie, concurrence,
> volumétrie. Le C02 pose **de quoi** une base est faite : table, colonne, ligne, schéma, type, contrainte.
> Le vocabulaire du C02 est **transverse** : il vaut pour DuckDB, SQLite, PostgreSQL et au-delà — un
> professionnel qui le maîtrise passe d'un SGBD à l'autre sans réapprendre. Le chapitre **aligne le
> langage** (les 5 types de base, `NULL` n'est ni 0 ni vide, les 4 contraintes de colonne) et installe
> le **mini-projet M06.P1** : 3 tables de référence créées en DDL DuckDB. Le verdict du C02 est
> **« la table est un objet à 6 attributs »** : nom, colonnes typées, clé primaire, contraintes,
> insertion atomique, lecture en bloc.

> **Base de travail — le projet M06.P.** C02 réutilise le `quincaillerie_export.csv` (24 000 lignes × 42
> colonnes, livré par `tools/dossier_M06.py`), mais ne crée **aucune table projet** : le projet est
> l'affaire du C03 (clés + relations) et du mini-projet C03 §10. C02 ne crée que les **3 tables de
> référence** du mini-projet M06.P1 : `client`, `produit`, `mode_paiement`. Ces 3 tables sont *le
> squelette* du schéma 3FN que le C03 et le projet M06.P assemblent.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

- **définir** les 6 attributs d'une table : nom, schéma, colonnes, types, contraintes, lignes ;
- **distinguer** les 5 types SQL de base (numérique, texte, date, booléen, binaire) et leurs variantes
  DuckDB ;
- **comprendre** que `NULL` n'est ni 0 ni vide, et lire la logique ternaire (`TRUE`, `FALSE`, `UNKNOWN`) ;
- **utiliser** les 4 contraintes de colonne (`NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`) et **tester** leur
  effet ;
- **créer** 3 tables de référence en DDL DuckDB, **insérer** 5 lignes, **vérifier** par requête de
  lecture ;
- **reconnaître** les erreurs courantes (`NOT NULL` violé, `UNIQUE` dupliqué, `CHECK` rejeté, `NULL` non
  géré).

## 2. Pourquoi cette notion est importante

- La **table** est l'unité de base du relationnel. Tout le reste (schéma, contraintes, requêtes) en
  découle. C'est l'objet que le professionnel doit savoir *créer*, *lire*, *modifier*, *détruire*. Le
  C02 installe la **création** ; le C03 installe les **relations** ; le C04 installe la **vie en
  production**.
- Les **5 types** (numérique, texte, date, booléen, binaire) couvrent 95 % des cas. DuckDB en ajoute 9
  (`HUGEINT`, `UUID`, `JSON`, `STRUCT`, `LIST`, etc.) qui sont *rarement nécessaires*. Le C02 enseigne
  les 5, pas les 14 : c'est le **profil minimal** d'un analyste.
- `NULL` est le **piège statistique** n°1 : `SUM(col)` ignore les `NULL`, `COUNT(col)` aussi, mais
  `COUNT(*)` les compte. Sans comprendre `NULL`, on ** produit des chiffres faux** sans s'en rendre
  compte. Le M01.B02 l'a enseigné pour le tableur ; le C02 l'enseigne pour le SQL.
- Les **4 contraintes de colonne** sont ce qui distingue la table d'un fichier texte. Sans contraintes,
  on peut écrire 1 client avec un `telephone` à `'abc'` ou un `id_client` en double. Avec, le SGBD
  refuse. C'est la **discipline** du relationnel.
- Le **mini-projet M06.P1** (3 tables de référence en DDL DuckDB) est l'épreuve : il passe si les tables
  se créent, si les contraintes rejettent les violations, si les 5 lignes insérées se lisent. C'est
  *avant* le projet M06.P, qui assemble ces 3 tables aux 4 autres (vente, ligne_vente, retour,
  client_categorie_pref).

## 3. Explication simple — la table est un objet à 6 attributs

Une table est un objet à 6 attributs, **dans cet ordre** :

1. **Nom** — `client`, `produit`, `vente`, etc. Le nom est *immuable* : on ne renomme pas sans casser
   les requêtes.
2. **Schéma** — la liste ordonnée des colonnes, chacune avec son **nom**, son **type**, et ses
   **contraintes**. Le schéma est *distinct* des données : la table `client` a 11 colonnes, qu'elle
   contienne 0 ligne ou 1 891.
3. **Colonnes typées** — chaque colonne a un **type** (`INTEGER`, `TEXT`, `DATE`, etc.) qui contraint
   la valeur (DuckDB rejette `'abc'` dans un `INTEGER`).
4. **Contraintes** — les **règles** que les données doivent suivre (`PRIMARY KEY`, `NOT NULL`, `UNIQUE`,
   `CHECK`, `FOREIGN KEY`).
5. **Lignes** — les **données elles-mêmes**, qui *respectent* le schéma et les contraintes. Une ligne
   qui viole une contrainte est **refusée** à l'insertion.
6. **Clé primaire** — la colonne (ou combinaison) qui identifie la ligne. Sa présence est **facultative**
   d'un point de vue syntaxe, mais **obligatoire** d'un point de vue métier.

Le **résumé en une phrase** : *« Une table, c'est un nom, un schéma typé, des contraintes, des lignes
qui les respectent, et une clé pour les compter. »*

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **table** — *table, relation* | un ensemble de lignes (tuples) de même schéma, nommées par des colonnes typées. | confondre avec « onglet » : un onglet Excel a un en-tête et des lignes, mais sans schéma ni contrainte formelle. |
| **colonne** — *column, attribute* | un **slot typé** dans la table. Chaque ligne porte une valeur pour chaque colonne. | croire que l'ordre des colonnes compte : il ne compte pas pour la *logique* (on les nomme), mais l'ordre *physique* peut affecter la performance. |
| **ligne** — *row, tuple* | une **valeur** pour chaque colonne, qui respecte le schéma et les contraintes. | confondre avec « enregistrement » : une ligne est *typée* par ses colonnes, un enregistrement est juste un paquet de données. |
| **schéma** — *schema* | la **structure** d'une base (les noms de tables, les colonnes, les types, les contraintes), distincte des **données**. | confondre avec « table » : une base a *un* schéma (ou plusieurs namespaces) et *N* tables. |
| **type** — *data type* | la **famille** des valeurs qu'une colonne peut prendre (`INTEGER`, `TEXT`, `DATE`, `BOOLEAN`, etc.). | confondre avec « format » : le type est *logique* (DuckDB sait que c'est une date), le format est *visuel* (JJ/MM/AAAA est l'affichage). |
| **`NULL`** — *null value* | une **absence de valeur**, distincte de `0`, de `''` et de `'NA'`. C'est le marqueur « pas de réponse ». | confondre avec 0 ou vide : `NULL + 1` n'est pas 1, c'est `NULL` ; la logique ternaire (`TRUE`/`FALSE`/`UNKNOWN`) traite `NULL` comme *inconnu*. |
| **`NOT NULL`** | contrainte qui interdit `NULL` sur la colonne. C'est *l'engagement* que la colonne porte toujours une valeur. | croire que c'est facultatif : `NOT NULL` rend la colonne *porteuse de sens* (une date manquante n'est pas `NULL` silencieuse). |
| **`UNIQUE`** | contrainte qui interdit les **doublons** sur la colonne (ou la combinaison). C'est *l'engagement* que la colonne identifie de manière unique. | confondre avec `PRIMARY KEY` : `UNIQUE` accepte `NULL`, `PRIMARY KEY` non. |
| **`CHECK`** | contrainte qui valide une **condition** sur la valeur (par exemple `montant > 0`, ou `taux IN (0.18, 0.19)`). | croire qu'elle est universelle : `CHECK` peut être contournée par certaines opérations (`COPY`, `LOAD DATA`). |
| **`DEFAULT`** | la valeur **par défaut** quand l'insertion ne précise pas la colonne. C'est *l'engagement* sur la valeur en cas d'oubli. | confondre avec `NULL` implicite : `DEFAULT` n'est pas `NULL`, c'est une valeur que vous choisissez. |

> **Attention.** **`UNIQUE` n'est pas `PRIMARY KEY`** — c'est un piège classique, surtout en SQLite
> où `UNIQUE` accepte plusieurs `NULL`. Si vous voulez *une* ligne par valeur, *sans* `NULL`,
> utilisez `PRIMARY KEY` ou `UNIQUE NOT NULL`. Et si la colonne peut être `NULL`, dites-le (`UNIQUE`
> accepte alors des `NULL` non-dupliqués, ce qui veut dire *« plusieurs lignes peuvent avoir la même
> absence »* — c'est rarement ce qu'on attend).

> **Attention.** **`CHECK` n'est pas une règle métier** — c'est un **garde-fou syntaxique**. La règle
> du module est *CHECK valide l'évidence, pas la complexité*. Un `CHECK (montant > 0)` rate les retours ;
> un `CHECK (montant != 0)` est correct mais **inutile** (tout `0` est probablement une erreur de
> saisie, pas une saisie vraie) ; un `CHECK (montant > -1 000 000 AND montant < 1 000 000)` est une
> plage par défaut, pas une règle métier. Pour les invariants métier, le code applicatif + les 3
> requêtes `controles_integrite.sql` du C01 sont *plus adaptés*.

> **Dans les faits.** En production, **la moitié des bugs de base viennent des contraintes oubliées**.
> Une table `email` sans `UNIQUE` accepte 50 clients avec le même e-mail, et c'est *visible* quand
> on essaie d'envoyer la newsletter (« 50 exemplaires à la même adresse »). Une table `prix_unitaire`
> sans `CHECK (prix > 0)` accepte un prix à `-1000`, et c'est *visible* quand le calcul de marge
> donne un résultat aberrant. Le test qui ferme le chapitre est l'**insertion négative** : insérer
> une ligne qui *devrait* être refusée, et vérifier qu'elle l'est. C'est l'épreuve du mini-projet
> M06.P1 §13.
| **`INTEGER`** | le type **entier signé** sur 32 bits (de -2 147 483 648 à 2 147 483 647). Pour aller au-delà : `BIGINT`. | croire qu'il gère les décimales : pour les décimales, c'est `DOUBLE`, `DECIMAL` ou `NUMERIC`. |
| **`BIGINT`** | le type **entier signé** sur 64 bits (de -9 223 372 036 854 775 808 à 9 223 372 036 854 775 807). Le défaut dans beaucoup de SGBD. | confondre avec `HUGEINT` (128 bits, DuckDB) : pour 99 % des cas, `BIGINT` suffit. |
| **`TEXT`** | le type **chaîne** de longueur variable, sans limite stricte (DuckDB ne fixe pas de limite ; PostgreSQL impose une limite pratique). | croire que `VARCHAR(255)` est obligatoire : c'est l'habitude de l'époque mainframe, pas une nécessité. |
| **`DATE`** | le type **date calendaire** (AAAA-MM-JJ), distinct de `TIMESTAMP` (qui ajoute l'heure). | confondre avec le format : `DATE '2025-03-15'` est un littéral date, `'15/03/2025'` est une chaîne. |
| **`BOOLEAN`** | le type **booléen** à 3 valeurs (`TRUE`, `FALSE`, `NULL` en SQL ANSI ; DuckDB utilise `TRUE`/`FALSE`/`NULL`). | croire que c'est 0/1 : en SQL, c'est `TRUE`/`FALSE`/`NULL`, pas `0`/`1`/`2`. |
| **`PRIMARY KEY`** | la **clé primaire** : la colonne (ou combinaison) qui identifie la ligne. Implique `NOT NULL` + `UNIQUE`. | croire qu'elle est obligatoire : techniquement non, mais sans elle la base ne sait pas *compter* les lignes. |

> **Définition.** Une **contrainte** est une **règle** que les données doivent suivre, **portée par
> la base elle-même** (pas par le code applicatif). Les 4 contraintes de colonne du C02 sont `NOT NULL`,
> `UNIQUE`, `CHECK`, `DEFAULT`. Les contraintes de **table** (cf. C03) sont `PRIMARY KEY` et
> `FOREIGN KEY`. Une contrainte **refuse** l'insertion qui la viole — c'est ce qui distingue une base
> d'un fichier texte.
> — *English : constraint.*

> **Définition.** Le **type SQL** est la **famille** des valeurs qu'une colonne accepte. Les 5 types
> *de base* sont : numérique (`INTEGER`, `BIGINT`, `DOUBLE`, `DECIMAL`), texte (`TEXT`, `VARCHAR`),
> date (`DATE`, `TIMESTAMP`), booléen (`BOOLEAN`), binaire (`BLOB`). DuckDB en ajoute 9 (JSON, UUID,
> LIST, STRUCT, etc.) qui sont *rarement* nécessaires. Le type est *logique* : il valide à l'insertion
> (le SGBD refuse `'abc'` dans un `INTEGER`) et *opère* sur les valeurs (`+` sur des `INTEGER` fait de
> l'arithmétique, pas de la concaténation).
> — *English : data type.*

> **Définition.** La valeur **`NULL`** représente l'**absence de valeur**. Elle est distincte de `0`,
> de `''` (chaîne vide) et de `'NA'`. La logique ternaire SQL (`TRUE`, `FALSE`, `UNKNOWN`) traite `NULL`
> comme *inconnu* : `NULL = NULL` n'est pas `TRUE`, c'est `UNKNOWN`. Le test juste est **`IS NULL` /
> `IS NOT NULL`**. Les fonctions d'agrégat **ignorent** `NULL` par défaut : `SUM(col)` produit
> `NULL` si toutes les valeurs sont `NULL`, et ignore les `NULL` sinon (sans compter la ligne).
> — *English : null value.*

> **Définition.** Le **`DDL`** (Data Definition Language) est le sous-ensemble du SQL qui crée, modifie,
> et supprime la **structure** : `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`, `CREATE INDEX`,
> `CREATE VIEW`. Le `DML` (Data Manipulation Language) touche aux **données** : `SELECT`, `INSERT`,
> `UPDATE`, `DELETE`. Le `DCL` (Data Control Language) gère les **droits** : `GRANT`, `REVOKE`. Le C02
> enseigne le DDL ; le C03 et le C07 enseignent le DML.
> — *English : Data Definition Language.*

---

## 5. Cours approfondi — la grammaire d'une table

### 5.1 Le squelette d'un `CREATE TABLE`

La syntaxe canonique en DuckDB / PostgreSQL / SQLite est :

```sql
CREATE TABLE nom_table (
    nom_col1  TYPE  CONTRAINTES,
    nom_col2  TYPE  CONTRAINTES,
    ...
    PRIMARY KEY (col1, col2),          -- contrainte de table
    FOREIGN KEY (col3) REFERENCES autre_table(col3)  -- contrainte de table (cf. C03)
);
```

Le **nom** est suivi des **colonnes**, chacune avec son **type** et ses **contraintes** (de colonne).
Les contraintes de **table** (`PRIMARY KEY`, `FOREIGN KEY`) sont à la fin.

### 5.2 Les 5 types SQL de base, et leur usage

| Type | Usage courant | Piège |
|---|---|---|
| `INTEGER` / `BIGINT` | compteurs, identifiants, montants entiers (en FCFA) | croire que ça gère les décimales |
| `DOUBLE` / `DECIMAL` | montants avec décimales, mesures physiques | `DOUBLE`perd en précision ; `DECIMAL(p, s)` est exact |
| `TEXT` | noms, libellés, descriptions | confondre avec `VARCHAR(n)` (longueur fixe) |
| `DATE` / `TIMESTAMP` | dates de vente, dates de naissance | `DATE '2025-03-15'` est un littéral ; `'15/03/2025'` est une chaîne |
| `BOOLEAN` | flags (`est_promo`, `est_retour`) | en SQL c'est `TRUE`/`FALSE`/`NULL`, pas `0`/`1`/`NULL` |

DuckDB **étend** ces 5 types avec `HUGEINT` (128 bits), `UUID`, `JSON`, `STRUCT`, `LIST`, `MAP`,
`ENUM`. Pour 95 % des cas d'usage, les 5 de base suffisent. Le projet M06.P n'utilise que `INTEGER`,
`TEXT`, `DATE`, `BOOLEAN`, `BIGINT` (pour les montants *en entier FCFA*).

### 5.3 `NULL` et la logique ternaire

En SQL, `NULL` est une **valeur spéciale** qui signifie « **je ne sais pas** ». Ce n'est pas 0, ce n'est
pas vide, ce n'est pas `'NA'`. Les **comparaisons** avec `NULL` retournent `UNKNOWN`, pas `TRUE` ou
`FALSE` :

```sql
SELECT NULL = 0;        -- NULL (UNKNOWN, pas FALSE)
SELECT NULL = NULL;     -- NULL (UNKNOWN, pas TRUE)
SELECT NULL IS NULL;    -- TRUE  (le test juste)
SELECT NULL IS NOT NULL; -- FALSE (le test juste)
```

La **logique ternaire** (`TRUE`, `FALSE`, `UNKNOWN`) affecte les agrégats. `SUM(col)` ignore les `NULL`,
`COUNT(col)` aussi, mais `COUNT(*)` les compte. La règle du module est *toujours tester `IS NULL` /
`IS NOT NULL`*, jamais `= NULL` (qui retourne `UNKNOWN`).

### 5.4 Les 4 contraintes de colonne

| Contrainte | Effet | Exemple |
|---|---|---|
| `NOT NULL` | la colonne ne peut pas être `NULL` | `telephone TEXT NOT NULL` |
| `UNIQUE` | la colonne (ou combinaison) n'a pas de doublon | `id_client INTEGER UNIQUE` |
| `CHECK` | la valeur doit satisfaire une condition | `prix_courant_ht INTEGER CHECK (prix_courant_ht > 0)` |
| `DEFAULT` | la valeur par défaut si l'insertion omet la colonne | `fidelite_niveau TEXT DEFAULT 'COMPTOIR'` |

Une contrainte **`PRIMARY KEY`** est la combinaison **`NOT NULL` + `UNIQUE`** appliquée à la colonne
désignée. Le C03 l'approfondit.

### 5.5 Erreurs courantes

| Erreur | Symptôme | Parade |
|---|---|---|
| Oublier `NOT NULL` | la colonne est `NULL` par défaut | ajouter `NOT NULL` *à la création* (sinon, recréer la table) |
| Mettre `VARCHAR(255)` sans raison | les chaînes de plus de 255 caractères sont **tronquées** silencieusement | utiliser `TEXT` (DuckDB) ou `VARCHAR(N)` avec un N *réaliste* |
| `CHECK (montant_ttc > 0)` sur des retours | les retours (montants négatifs) sont **refusés** | `CHECK (montant_ttc != 0)` ou pas de CHECK (la règle métier est dans le code applicatif) |
| Comparer avec `= NULL` | retourne `UNKNOWN`, jamais `TRUE` | utiliser `IS NULL` / `IS NOT NULL` |
| Insérer des dates en `JJ/MM/AAAA` | DuckDB **autoload** devine (parfois faux) | utiliser `DATE 'AAAA-MM-JJ'` ou `STRPTIME(col, '%d/%m/%Y')` |
| Oublier `UNIQUE` sur `email` | plusieurs clients partagent le même e-mail | ajouter `UNIQUE` (et migrer les doublons d'abord) |

### 5.6 La table `client` du mini-projet M06.P1, en DDL DuckDB

```sql
CREATE TABLE client (
    id_client       INTEGER PRIMARY KEY,
    nom             TEXT    NOT NULL,
    prenom          TEXT    NOT NULL,
    telephone       TEXT    NOT NULL UNIQUE,
    email           TEXT    UNIQUE,                            -- nullable : un client comptoir n'en a pas
    ville           TEXT    NOT NULL,
    code_postal     TEXT,
    region          TEXT,
    pays            TEXT    NOT NULL DEFAULT 'Burkina Faso',
    fidelite_niveau TEXT    NOT NULL DEFAULT 'COMPTOIR'
                          CHECK (fidelite_niveau IN ('COMPTOIR','BRONZE','OR','PLATINE')),
    fidelite_points INTEGER NOT NULL DEFAULT 0 CHECK (fidelite_points >= 0)
);
```

Lecture de la table :
- **`id_client`** : la clé primaire, `INTEGER`, identifie chaque ligne.
- **`nom`** et **`prenom`** : `TEXT NOT NULL`, on refuse un client sans nom.
- **`telephone`** : `TEXT NOT NULL UNIQUE`, on refuse un téléphone vide ET un doublon.
- **`email`** : `TEXT UNIQUE` (sans `NOT NULL`), un client comptoir peut ne pas avoir d'e-mail ; mais deux
  clients ne partagent pas le même e-mail.
- **`ville`** : `TEXT NOT NULL`, on refuse un client sans ville.
- **`pays`** : `TEXT NOT NULL DEFAULT 'Burkina Faso'`, valeur par défaut pour la quincaillerie locale.
- **`fidelite_niveau`** : `CHECK` qui contraint à 4 valeurs admises.
- **`fidelite_points`** : `CHECK (>= 0)`, on refuse les points négatifs.

---

## 6. Exemple concret — les 3 tables de référence du mini-projet M06.P1

### 6.1 Table `client` (vue § 5.6)

C'est la table **principale** du projet M06.P — 1 891 lignes à terme, et la **cible** des clés
étrangères de `vente`, `retour`, `client_categorie_pref`. La clé primaire est `id_client`, et
l'**unicité** est sur `telephone` (clé métier, pas technique).

### 6.2 Table `produit` en DDL DuckDB

```sql
CREATE TABLE produit (
    id_produit         INTEGER PRIMARY KEY,
    libelle            TEXT    NOT NULL,
    categorie          TEXT    NOT NULL,
    sous_categorie     TEXT    NOT NULL,
    fournisseur        TEXT    NOT NULL,
    prix_courant_ht    INTEGER NOT NULL CHECK (prix_courant_ht > 0),
    UNIQUE (libelle, fournisseur)       -- un produit est unique par (nom, fournisseur)
);
```

Cette table respecte la **3FN** : pas de transitivité, pas de multi-valué. Le `prix_courant_ht` est
l'attribut *propre* du produit (pas d'une autre entité).

### 6.3 Table `mode_paiement` en DDL DuckDB

```sql
CREATE TABLE mode_paiement (
    id_mode                    INTEGER PRIMARY KEY,
    libelle                    TEXT    NOT NULL UNIQUE,
    frais_pct                  REAL    NOT NULL DEFAULT 0 CHECK (frais_pct >= 0),
    delai_encaissement_jours   INTEGER NOT NULL DEFAULT 0
);
```

Les 4 valeurs canoniques (`ESPECES`, `MOBILE_MONEY`, `CARTE_BANCAIRE`, `CREDIT`) sont insérées une fois,
et la table `vente` y fait référence par `id_mode`. C'est l'**externalisation de la référence** du § 1.4.

### 6.4 Insertion de 5 lignes et lecture de contrôle

```sql
INSERT INTO client (id_client, nom, prenom, telephone, email, ville, fidelite_niveau) VALUES
    (0,  'COMPTOIR',  'CLIENT',      '0000000000',                          NULL,                  'Koudougou', 'COMPTOIR'),
    (1,  'Nom0001',   'Prenom0001',  '+226 78 12 34 56 78',                 'p1.n1@example.bf',    'Koudougou', 'OR'),
    (2,  'Nom0002',   'Prenom0002',  '+226 78 12 34 56 79',                 'p2.n2@example.bf',    'Bobo-Diullasso', 'BRONZE'),
    (3,  'Nom0003',   'Prenom0003',  '+226 78 12 34 56 80',                 NULL,                  'Ouagadougou', 'COMPTOIR'),
    (4,  'Nom0004',   'Prenom0004',  '+226 78 12 34 56 81',                 'p4.n4@example.bf',    'Banfora', 'PLATINE');

SELECT COUNT(*) AS nb_clients FROM client;                              -- 5
SELECT * FROM client WHERE fidelite_points > 0;                          -- 1 si on a inséré des points
SELECT * FROM client WHERE fidelite_niveau = 'COMPTOIR';                -- 2
SELECT * FROM client WHERE email IS NULL;                                -- 2
```

Ce mini-projet **valide** la création : si DuckDB renvoie `5` pour `COUNT(*)`, si les contraintes
refusent les violations (test : `INSERT INTO client (id_client, nom, prenom, telephone) VALUES (5,
NULL, 'X', '+226 X')` — `NOT NULL` violé sur `nom`), si les tris par `fidelite_niveau` renvoient
2 lignes, alors la table est **opérationnelle**. C'est l'épreuve du C02.

---

## 7. Démonstration pas à pas — créer une table en 6 lignes

### 7.1 Choisir le nom

`client`. Pas de pluriel, pas de préfixe (sauf contexte). En SQL ANSI, le nom est insensible à la casse.

### 7.2 Lister les colonnes

11 colonnes : `id_client`, `nom`, `prenom`, `telephone`, `email`, `ville`, `code_postal`, `region`,
`pays`, `fidelite_niveau`, `fidelite_points`.

### 7.3 Typer chaque colonne

5 types : `INTEGER` pour `id_client` et `fidelite_points` ; `TEXT` pour tout le reste.

### 7.4 Ajouter les contraintes

`NOT NULL` sur les colonnes porteuses de sens (`nom`, `prenom`, `telephone`, `ville`, `pays`,
`fidelite_niveau`) ; `UNIQUE` sur `telephone` et `email` ; `DEFAULT` sur `pays` et `fidelite_niveau`
et `fidelite_points` ; `CHECK` sur `fidelite_niveau` (4 valeurs) et `fidelite_points` (≥ 0) ; `PRIMARY
KEY` sur `id_client`.

### 7.5 Ordonner les contraintes de table

`PRIMARY KEY` (et `FOREIGN KEY`, cf. C03) en bas du `CREATE TABLE`.

### 7.6 Tester en 3 requêtes

`INSERT`, lecture (`SELECT *`), contrainte violée (test négatif).

> **À retenir.** Les 6 étapes du `CREATE TABLE` sont **mécaniques** : nom, colonnes, types,
> contraintes, ordre, test. La discipline est de *ne pas en sauter*. Une table sans contrainte de
> colonne est un fichier texte ; avec, c'est une **table relationnelle**.

---

## 8. Erreurs fréquentes

- **Oublier `NOT NULL` sur la clé primaire.** Une `PRIMARY KEY` *impose* `NOT NULL` ; une colonne
  ordinaire `INTEGER` accepte `NULL`. La règle est `PRIMARY KEY = NOT NULL + UNIQUE` *implicite*.
- **`CHECK` trop restrictif.** Un `CHECK (montant > 0)` rate les retours (montants **négatifs**). Le
  piège classique : on copie la règle métier dans la base, et la base refuse les cas métier qui
  *paraissent* marginaux mais qui existent. La règle du module : **`CHECK` doit valider l'évidence, pas
  la complexité**.
- **`TEXT` vs `VARCHAR(N)`.** `TEXT` (DuckDB, PostgreSQL) est sans limite ; `VARCHAR(N)` tronque à N
  caractères. Utiliser `VARCHAR(255)` par défaut est une habitude qui **coûte des données** quand un nom
  dépasse 255 caractères (les noms composés africain en témoignent).
- **`BOOLEAN` et `INTEGER`.** En SQL `BOOLEAN` n'est pas un `INTEGER`. DuckDB peut **convertir**
  implicitement, mais la lecture est ambiguë. La règle : `BOOLEAN` pour les flags, `INTEGER` pour les
  quantités.
- **Confondre `DEFAULT` et `NOT NULL`.** `DEFAULT` ne refuse pas `NULL` ; il propose une valeur par
  défaut *quand l'insertion omet la colonne*. Si l'insertion **précise** `NULL`, c'est `NULL`. Pour
  refuser `NULL`, il faut `NOT NULL`.
- **Sous-estimer la différence de comportement entre SGBD.** SQLite ne respecte pas `CHECK` *avant*
  la 3.32 (2020) ; PostgreSQL applique `CHECK` *par défaut* mais permet `INITIALLY DEFERRED` ; DuckDB
  applique `CHECK` immédiatement. Le **mini-projet** DuckDB ne garantit pas la portabilité : le code
  doit être testé sur le SGBD cible.
- **Croire que `UNIQUE` suffit à faire une clé primaire.** `UNIQUE` accepte `NULL` (plusieurs `NULL`
  sont autorisés — DuckDB et PostgreSQL divergent ici). Une **`PRIMARY KEY`** est `NOT NULL` + `UNIQUE`,
  point.

> **À retenir.** Les 7 erreurs ci-dessus sont les **pièges du quotidien** d'un analyste qui crée une
> table. La règle unique : *tester la table par une insertion qui doit échouer* (`INSERT … VALUES (NULL,
> NULL)` sur une colonne `NOT NULL`). Sans ce test, on ne sait pas si la contrainte est portée par la
> base ou par l'espoir.

---

## 9. Bonnes pratiques professionnelles

- **Lire la documentation des types** de votre SGBD. DuckDB a 14 types, PostgreSQL a 30+, SQLite en a
  5. Le **profil minimal** est les 5 de base.
- **`NOT NULL` par défaut** sauf raison. Une colonne nullable est une **permission d'ignorer**, et
  c'est rarement ce qu'on veut.
- **`UNIQUE`** sur les clés **métier** (téléphone, e-mail, n° de série), pas sur les clés techniques
  (`id_vente`). Les clés techniques sont immuables par construction (auto-incrément) ; les clés métier
  sont immuables par contrainte.
- **`CHECK`** sur les **valeurs énumérées** (`fidelite_niveau IN (4 valeurs)`), pas sur les **bornes
  métier** (`montant > 0` rate les retours). Les énumérations sont stables ; les bornes métier
  changent.
- **Documenter** chaque table dans le README du projet : nom, grain, 1 phrase d'usage.
- **Tester** la table par **insertion négative** (la violation attendue doit lever une erreur). C'est
  l'épreuve de vérité.

> **Conseil professionnel.** Une table bien dessinée est **auto-vérifiée** : si vous insérez une ligne
> qui viole une règle métier, le SGBD refuse, et c'est *visible*. Si la table passe tout (toutes les
> insertions sont acceptées), c'est qu'elle ne porte pas assez de contraintes — ou que vos insertions
> n'ont pas *testé* les bons cas.

---

## 10. Exercice guidé — la table `mode_paiement` (15 min, /10)

**Objectif.** Mobiliser le `CREATE TABLE` sur 4 colonnes et 2 contraintes.

**Énoncé.** Créez la table `mode_paiement` du mini-projet M06.P1 en DDL DuckDB, avec les colonnes :

- `id_mode INTEGER PRIMARY KEY`
- `libelle TEXT NOT NULL UNIQUE`
- `frais_pct REAL NOT NULL DEFAULT 0 CHECK (frais_pct >= 0)`
- `delai_encaissement_jours INTEGER NOT NULL DEFAULT 0`

Insérez les 4 lignes (`ESPECES`, `MOBILE_MONEY`, `CARTE_BANCAIRE`, `CREDIT`), testez les contraintes
(insertion d'un `frais_pct` négatif : doit échouer).

**Barème (/10).** DDL correct (3) · insertion des 4 lignes (2) · test négatif (2) · tri par `frais_pct
DESC` (1) · filtrage par `delai_encaissement_jours > 0` (1) · `SELECT *` rendu final (1).

---

## 11. Exercices autonomes

- **Exercice 11.1 (15 min).** Citez les 6 attributs d'une table (§ 3) et donnez, pour chacun, un
  exemple tiré du mini-projet M06.P1.
- **Exercice 11.2 (30 min).** Créez la table `client` du mini-projet M06.P1 dans un autre SGBD
  (SQLite par Python, ou PostgreSQL par psql si votre poste l'a). Notez 3 différences de syntaxe.
- **Exercice 11.3 (45 min).** Insérez une ligne qui viole **chacune** des 4 contraintes (`NOT NULL`,
  `UNIQUE`, `CHECK`, `DEFAULT`) sur la table `client`, et notez le message d'erreur de DuckDB. Ces
  messages sont ce que les utilisateurs voient.
- **Exercice 11.4 (60 min, optionnel).** Réécrivez la table `produit` du § 6.2 en ajoutant une
  contrainte `CHECK` qui valide que `categorie IN ('Alimentaire', 'Bricolage', 'Jardinage',
  'Quincaillerie', 'Décoration')`. Notez l'effet sur la lisibilité du DDL et le risque d'erreur quand
  on ajoute une 6ᵉ catégorie.

---

## 12. Correction détaillée

- **Exercice 11.1.** Attributs : (1) nom = `client` ; (2) schéma = 11 colonnes ; (3) colonnes typées =
  `INTEGER`, `TEXT` ; (4) contraintes = `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT` ; (5) lignes = 5
  insérées ; (6) clé primaire = `id_client`.
- **Exercice 11.2.** Différences attendues : SQLite natif = pas de `BOOLEAN` natif (`INTEGER 0/1`) ;
  pas de `REAL` (utilise `NUMERIC` ou `FLOAT`) ; PostgreSQL = `SERIAL` pour auto-incrément
  (DuckDB n'en a pas, on utilise `INTEGER` plus une séquence applicative).
- **Exercice 11.3.** Les 4 violations : (a) `NOT NULL` : `INSERT INTO client (id_client, nom, prenom,
  telephone, ville) VALUES (5, NULL, 'X', '+226 X', 'K')` — DuckDB renvoie `NOT NULL constraint
  failed: client.nom` ; (b) `UNIQUE` : insérer deux fois le même `telephone` — DuckDB renvoie `UNIQUE
  constraint failed: client.telephone` ; (c) `CHECK` : `INSERT … VALUES (5, 'N', 'P', '+226',
  'e@e.bf', 'V', 'PLATINE_RUSSE')` — DuckDB renvoie `CHECK constraint failed: client.fidelite_niveau`
  ; (d) `DEFAULT` : tester en omettant `pays` dans une insertion (DuckDB insère `'Burkina Faso'`).
- **Exercice 11.4.** L'effet : le DDL devient plus bavard (la liste des 5 catégories est explicite), mais
  c'est *une garantie supplémentaire* contre les fautes de frappe. Le risque : si on ajoute une 6ᵉ
  catégorie (par exemple « Outillage »), il faut modifier le DDL **et** migrer les anciennes lignes
  qui avaient une autre catégorie. La règle du module est *DDL paramétrable quand la liste est
  stable*. Pour la quincaillerie, **5 catégories** est probablement stable.

---

## 13. Mini-projet M06.P1 — « Les 3 tables de référence » (1 h)

**Énoncé.** Créez les **3 tables de référence** du projet M06.P en DDL DuckDB :
- `client` (§ 5.6 — 11 colonnes, contraintes complètes)
- `produit` (§ 6.2 — 6 colonnes, `UNIQUE (libelle, fournisseur)`)
- `mode_paiement` (§ 6.3 — 4 colonnes, `UNIQUE` sur `libelle`)

Insérez **5 lignes** dans chaque table, testez **2 violations** par table, et rendez **1 page** de
sortie (les `SELECT *` finaux).

**Critères de réussite.**

1. Les 3 `CREATE TABLE` passent sans erreur (DDL valide).
2. Les **5 lignes** par table sont insérées (`INSERT` accepté).
3. Les **2 tests négatifs** par table (6 au total) déclenchent une erreur DuckDB.
4. Les **3 lectures finales** renvoient 5 lignes chacune.
5. La **page rendue** montre les `INSERT`, les `SELECT *`, et les messages d'erreur des tests négatifs.

**Barème (/10).** 2 points par table ; le critère 5 vaut 1 point, le critère 1 vaut 1 point.

---

## 14. Boîte à outils du chapitre

> **Boîte à outils.** Six objets, un seul but — *créer une table relationnelle qui se vérifie elle-même* :
>
> 1. **Les 5 types SQL de base** (§ 5.2) — `INTEGER`, `TEXT`, `DATE`, `BOOLEAN`, `BLOB` (+ variantes).
> 2. **Les 4 contraintes de colonne** (§ 5.4) — `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`.
> 3. **La logique ternaire `NULL`** (§ 5.3) — `TRUE`, `FALSE`, `UNKNOWN`, et `IS NULL`.
> 4. **Le squelette `CREATE TABLE`** (§ 5.1) — nom, colonnes, types, contraintes, ordre.
> 5. **La table `client` complète** (§ 5.6) — l'exemple type de DDL avec 11 colonnes et 6 contraintes.
> 6. **Le mini-projet M06.P1** (§ 13) — l'épreuve en 1 h, qui passe si les 3 tables se créent et se
>    testent.

## 15. Résumé du chapitre

- Une table est un objet à **6 attributs** : nom, schéma, colonnes typées, contraintes, lignes, clé
  primaire.
- Les **5 types SQL de base** sont : numérique, texte, date, booléen, binaire (DuckDB en ajoute 9).
- **`NULL`** est une **absence de valeur**, distincte de `0` et de `''`, traité par la logique
  ternaire (`TRUE`, `FALSE`, `UNKNOWN`).
- Les **4 contraintes de colonne** sont `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`. Les contraintes de
  table (cf. C03) sont `PRIMARY KEY` et `FOREIGN KEY`.
- La **table `client`** du mini-projet M06.P1 a 11 colonnes, dont 5 `NOT NULL`, 2 `UNIQUE`, 2 `CHECK`,
  3 `DEFAULT`, et `id_client PRIMARY KEY`.
- Le **mini-projet M06.P1** crée 3 tables (`client`, `produit`, `mode_paiement`) et teste les
  contraintes par **insertion négative** (la violation attendue doit échouer).

## 16. À retenir

> **À retenir.** Une **table relationnelle** est un *fichier de règles*, pas un *fichier de valeurs*.
> Les valeurs sont les lignes ; les **règles** sont les contraintes (`NOT NULL`, `UNIQUE`, `CHECK`,
> `DEFAULT`) et les types (`INTEGER`, `TEXT`, `DATE`). Le SGBD **porte** ces règles, et c'est cela qui
> distingue une base d'un fichier texte. Le test qui ferme le chapitre est **l'insertion négative** :
> si elle passe, la contrainte est faible ; si elle échoue, la contrainte est forte.

> **À retenir.** `NULL` n'est ni 0 ni vide, et le test juste est `IS NULL` / `IS NOT NULL`. Le piège
> classique est `col = NULL` qui retourne `UNKNOWN` (jamais `TRUE`). La règle du module est
> **`IS NULL`** partout où on cherche l'absence.

## 17. Évaluation formative (auto-correction, 8 min)

**Question 1.** Citez les 6 attributs d'une table. *(Réponse : nom, schéma, colonnes typées,
contraintes, lignes, clé primaire.)*

**Question 2.** Quels sont les 5 types SQL de base ? *(Réponse : numérique, texte, date, booléen,
binaire.)*

**Question 3.** Pourquoi `col = NULL` est-il faux ? *(Réponse : la logique ternaire SQL évalue toute
comparaison avec `NULL` comme `UNKNOWN`, jamais `TRUE`. Le test juste est `IS NULL`.)*

**Question 4.** Citez les 4 contraintes de colonne. *(Réponse : `NOT NULL`, `UNIQUE`, `CHECK`,
`DEFAULT`.)*

**Question 5.** Quelle est la différence entre `PRIMARY KEY` et `UNIQUE` ? *(Réponse : `PRIMARY KEY`
est `NOT NULL` + `UNIQUE`, et désigne **une** clé par table. `UNIQUE` accepte `NULL` (sauf si `NOT NULL`
est ajoutée) et peut porter sur plusieurs colonnes.)*

**Question 6.** Que retourne `SUM(col)` sur une table où toutes les valeurs sont `NULL` ?
*(Réponse : `NULL`. C'est pour ça que la convention est d'utiliser `COALESCE(SUM(col), 0)` pour le
total comptable.)*

**Question 7.** Pourquoi `CHECK (montant > 0)` rate-t-il les retours ? *(Réponse : les retours ont
des montants **négatifs**. La règle métier correcte est `CHECK (montant != 0)` ou pas de `CHECK` du
tout.)*
