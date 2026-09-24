# Module M06.C04 — Vivre avec DuckDB / SQLite / PostgreSQL : créer, insérer, importer un CSV, se connecter

**Outils : DuckDB 1.5.5 (intégré, exécuté), SQLite natif Python 3.13 (exécuté), PostgreSQL cité
(non exécutable dans cet atelier). Durée indicative : 7 h. Niveau : N2. Prérequis : M06.C01,
M06.C02, M06.C03.**

> **L'idée du chapitre.** Le C01 a posé *pourquoi*, le C02 *de quoi*, le C03 *comment les tables
> se parlent*. Le C04 fait le **plongement** : on installe DuckDB, on crée une base, on importe le
> `quincaillerie_export.csv` du projet M06.P, on insère des lignes, on interroge. Le C04 est le
> **chapitre-exécution** du module — c'est ici que le professionnel passe de *lire un schéma* à
> *construire une base*. Le verdict du C04 est **« la base est créée, l'import est fait, les 3
> requêtes sont OK »**. C'est aussi le chapitre qui apprend à **vivre avec** SQLite (embarqué, fichier)
> et à **situer** PostgreSQL (serveur, multi-utilisateurs).

> **Base de travail — le projet M06.P.** C04 réutilise le `quincaillerie_export.csv` (24 000 lignes ×
> 42 colonnes, livré par `tools/dossier_M06.py`, graine 43) et le `schema_3fn.sql` (la cible 3FN à
> 7 tables du C03). Le C04 ajoute le **client graphique** (DataGrip ou DBeaver, *cité non exécuté*),
> les **3 verbes de sauvegarde** (`EXPORT DATABASE`, `.backup`, `pg_dump`) et le **mini Health Check**
> du C04 § 17.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

- **installer** DuckDB (et vérifier qu'il fonctionne), **créer** une base en mémoire `:memory:`
  ou en fichier `.duckdb`, et **créer une table** ;
- **insérer** des données par `INSERT INTO … VALUES` et par `INSERT INTO … SELECT … FROM
  read_csv_auto()` (l'import CSV) ;
- **se connecter à SQLite** depuis Python 3.13, créer la base, importer le CSV, exécuter les 3
  requêtes `controles_integrite.sql` ;
- **connaître** les 5 différences entre DuckDB et SQLite qui importent pour un analyste ;
- **situer** PostgreSQL dans le paysage (client-serveur, multi-utilisateurs) sans l'installer ;
- **sauvegarder** une base DuckDB par `EXPORT DATABASE`, **restaurer** par `IMPORT DATABASE` ;
- **utiliser** un client graphique (DBeaver, DataGrip, le CLI `duckdb`) pour lire confortablement
  une grande table.

## 2. Pourquoi cette notion est importante

- Le C04 fait **passer** le lecteur de la *théorie* (C01-C03) à la *pratique* (un vrai SGBD installé
  qui tourne). C'est le moment où la table de 7 colonnes devient un *artefact exécutable*, pas un schéma
  sur papier. La discipline du module est **« tout ce qui est publié en Python est exécuté »** (règle
  2 du § 9 du plan M05), et c'est ce qui donne sa valeur au C04.
- **DuckDB et SQLite** sont *intégrés* et *embarqués* — c'est-à-dire sans serveur à installer. Un
  étudiant qui les maîtrise peut reproduire toute l'expérience du module sur son propre poste sans
  dépendre d'un administrateur. C'est l'**autonomie** professionnelle acquise au C04.
- **PostgreSQL** est cité sans être exécuté — c'est la *règle 7* du plan M05 reconduite pour le C04
  (cf. aussi M02.C04 « Power Query non exécutable »). PostgreSQL reste la **référence sérieuse** pour
  la production ; l'analyste qui le comprend sait *quand* le recommander, sans l'avoir installé.
- L'**import CSV** est le geste le plus fréquent en entreprise : 80 % des SGBD en analyse sont
  *alimentés* par des fichiers plats, pas par des `INSERT`. Le C04 enseigne le geste canonique
  (`read_csv_auto()`) et ses pièges (`all_varchar=true` avant transformation).
- La **sauvegarde** (`EXPORT DATABASE`, `.backup`, `pg_dump`) ferme la porte à la *catastrophe* : une
  base non sauvegardée est une base qui **n'existe pas vraiment**. Le C04 installe le réflexe.
- Le **client graphique** (DBeaver, DataGrip) est cité parce que c'est *l'outil quotidien* de
  l'analyste : 1 000 lignes en CLI, c'est faisable ; 100 000 lignes, il faut une interface.

## 3. Explication simple — les 3 moteurs, en 3 phrases

Le **verdict en 3 phrases** :

1. **DuckDB** — *« une bibliothèque Python qu'on appelle depuis un script ».* Pas de serveur, pas de
   configuration. C'est un analyseur SQL qu'on ouvre en quelques lignes : `con = duckdb.connect()`,
   puis on lit, on écrit, on ferme. C'est l'outil de l'analyste **mono-poste**.
2. **SQLite** — *« un fichier qu'on ouvre ».* Il est natif Python (`import sqlite3`), aucune
   installation. Le `fichier.sqlite` *est* la base ; on la copie, on la sauvegarde, on l'envoie par
   mail. C'est l'outil **embarqué** (Android, iOS, Firefox, millions d'applis).
3. **PostgreSQL** — *« un serveur ».* On installe PostgreSQL sur une machine (serveur), on s'y
   connecte par un *client* (psql, pgAdmin, DBeaver), et plusieurs utilisateurs partagent la base.
   C'est l'outil **multi-utilisateurs** de la production.

Le **résumé en une phrase** : *« DuckDB pour analyser, SQLite pour embarquer, PostgreSQL pour
partager. »*

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **CLI** — *Command-Line Interface* | l'interface **texte** (`duckdb fichier.duckdb`, `sqlite3 fichier.sqlite`). C'est l'outil du développeur et de l'analyste autonome. | confondre avec « base de données » : le CLI n'est pas un SGBD, c'est l'**interface** au SGBD. |
| **client graphique** — *GUI client* | un outil **visuel** (DBeaver, DataGrip, pgAdmin) qui présente les tables, les contraintes, les jointures en arbre. *Cité non exécuté* dans cet atelier. | croire qu'il peut remplacer la base : le client graphique ne stocke rien, il interroge. |
| **`pip install`** | le gestionnaire de paquets Python. `pip install duckdb` ajoute DuckDB à l'environnement courant. | installer dans le mauvais environnement : `pip install --user` ou `python3 -m pip install` selon le système. |
| **`import`** (en Python) | la directive qui charge une bibliothèque : `import duckdb`. Sans import, les fonctions ne sont pas disponibles. | confondre avec l'import SQL : `IMPORT DATABASE` DuckDB est une commande SQL, distincte du `import` Python. |
| **`:memory:`** | une base de données **volatile** (en mémoire RAM), détruite à la fermeture de la connexion. C'est la base par défaut pour les tests. | croire qu'elle persiste : `:memory:` perd tout dès qu'on ferme la connexion. |
| **fichier `.duckdb`** | la base de données **persistante** DuckDB. C'est un fichier binaire qui contient toutes les tables, index, vues. | confondre avec CSV : `.duckdb` est un *format de fichier*, pas un format texte. |
| **fichier `.sqlite`** | la base de données **persistante** SQLite. Un seul fichier `.sqlite` (ou `.db`) qui contient tout. | confondre avec DuckDB : SQLite ne sait pas lire `.duckdb`, et inversement. |
| **`EXPORT DATABASE`** | commande DuckDB qui **exporte** toute la base en fichiers `.parquet` (tables) + `.sql` (DDL). L'inverse est `IMPORT DATABASE`. | croire que c'est portable vers SQLite : Parquet est générique, mais le SQL généré est spécifique DuckDB. |
| **`.backup`** | commande SQLite qui **sauvegarde** la base dans un autre fichier `.sqlite`. L'inverse est `.restore`. | confondre avec `cp` : `.backup` prend un verrou cohérent, `cp` peut capturer une base dans un état partiel. |
| **`pg_dump`** | outil PostgreSQL qui **exporte** la base en SQL texte (DDL + DML). L'inverse est `pg_restore` ou `psql -f`. | croire que c'est un SGBD : `pg_dump` est l'*outil de sauvegarde*, pas la base. |
| **client-serveur** | architecture où le SGBD tourne sur une **machine distante** et les clients s'y connectent par réseau. PostgreSQL est client-serveur. | confondre avec « serveur web » : PostgreSQL n'est pas un serveur HTTP, c'est un **processus** qui écoute sur un port TCP. |
| **port TCP** | numéro de connexion (par défaut 5432 pour PostgreSQL, 3306 pour MySQL, 27017 pour MongoDB). Le client s'y connecte par `host=localhost, port=5432`. | confondre avec **le port ouvert dans le firewall** : PostgreSQL peut écouter sur 5432 sans que le firewall laisse passer. |
| **`psql`** | le **CLI** de PostgreSQL (`psql -h host -U user -d dbname`). L'équivalent de `duckdb` ou `sqlite3`. | croire qu'il a une interface graphique : c'est texte uniquement. |
| **`pgAdmin`** | l'**interface graphique** officielle PostgreSQL. L'équivalent de DBeaver pour PostgreSQL. | confondre avec le SGBD : `pgAdmin` est un client, pas un SGBD. |
| **DATABASE** (mot-clé DDL) | pour SQLite, c'est une **commande** qui attache un fichier : `ATTACH DATABASE 'fichier.sqlite' AS db2;`. Pour DuckDB, c'est un mot-clé de connexion. | confondre avec `CREATE DATABASE` (MySQL, PostgreSQL) : DuckDB et SQLite n'ont pas cette commande. |

> **Définition.** Le **SGBD intégré** (in-process) est un moteur SQL qui vit dans le **même
> processus** que le programme qui l'appelle. DuckDB est intégré : `import duckdb; con =
> duckdb.connect(':memory:')` ouvre une base en RAM. Aucun serveur, aucun port TCP, aucun fichier de
> configuration. C'est l'outil de l'**analyste solo**. SQLite est *embarqué* (une variante), DuckDB est
> *intégré*. La différence est marginale pour l'usage — les deux se lancent en une ligne.
> — *English : in-process database.*

> **Définition.** Le **SGBD serveur** (client-serveur) tourne sur une **machine distante** et les
> clients s'y connectent par réseau. PostgreSQL est serveur : `psql -h db.example.com -U alice -d
> mydb` ouvre une session, et plusieurs utilisateurs peuvent se connecter simultanément. C'est
> l'outil de la **production** — quand l'équipe a 5 personnes qui interrogent la base en même temps.
> — *English : client-server DBMS.*

> **Définition.** L'**import CSV** est le geste d'alimenter une table à partir d'un fichier plat. La
> commande canonique DuckDB est `INSERT INTO table SELECT * FROM
> read_csv_auto('fichier.csv')`. L'option `all_varchar=true` force toutes les colonnes en `TEXT`
> (avant la phase de transformation). Le piège classique est d'importer sans `WHERE` de filtre : la
> base reçoit *tout*, y compris les défauts du brut (cf. C01 §5.2). La règle est *importer, puis
> filtrer, puis transformer*.
> — *English : CSV import.*

> **Attention.** **DuckDB autoload** sur `read_csv_auto('fichier.csv')` fait une **conversion
> automatique** des colonnes qui « ressemblent » à des nombres ou des dates. C'est *pratique* pour
> les fichiers propres, mais c'est **dangereux** pour les fichiers *sales* : DuckDB convertit
> silencieusement `'1 200 FCFA'` en `1200`, ce qui *cache* le défaut (cf. M05 C03 §5.3). La parade
> est `all_varchar=true` (texte pour tout) *avant* la phase de conversion *contrôlée*.

> **Attention.** **`pip install --no-cache-dir`** est le bon réflexe en atelier Linux pour **ne pas
> saturer le quota persistant** (règle du README principal § « Hygiène du dépôt de travail »). Sans
> cette option, le cache `~/.cache/pip` grossit de 50-100 Mo par paquet. La règle d'or : *toujours
> `--no-cache-dir`*.

---

## 5. Cours approfondi — vivre avec DuckDB (intégré)

### 5.1 Installer et vérifier

```bash
pip install duckdb --no-cache-dir   # 8 Mo installés
python3 -c "import duckdb; print(duckdb.__version__)"   # 1.5.5
```

Le C04 utilise **DuckDB 1.5.5** (version du 19/09/2026). L'installation prend 8 Mo ; le module exige
**3 versions maximum différentes** pour la portabilité (cf. plan M05 §3 règle 6).

### 5.2 Ouvrir une base

Trois modes d'ouverture :

```python
import duckdb

# Mode 1 : en mémoire (volatile, tests)
con = duckdb.connect(':memory:')
con.close()

# Mode 2 : fichier persistant
con = duckdb.connect('/tmp/quincaillerie.duckdb')
con.close()

# Mode 3 : instance partagée (shared)
con = duckdb.connect('/tmp/quincaillerie.duckdb', read_only=False)
```

Le mode **mémoire** est le plus simple pour les *tests* : on crée, on lit, on ferme, et tout est
perdu. Le mode **fichier** est la *production* : la base persiste après la fermeture. Le mode
**read_only=True** ouvre en lecture seule (utile pour les clients graphiques).

### 5.3 Créer une table en DDL

```python
con = duckdb.connect(':memory:')
con.execute("""
CREATE TABLE client (
    id_client    INTEGER PRIMARY KEY,
    nom          TEXT    NOT NULL,
    prenom       TEXT    NOT NULL,
    telephone    TEXT    NOT NULL UNIQUE,
    ville        TEXT    NOT NULL
);
""")
# Vérification
print(con.execute("SHOW TABLES").fetchall())   # [('client',)]
```

**DuckDB lit l'instruction ligne par ligne** ; pas de statement terminator obligatoire. Le `;`
est recommandé. La **DDL** (`CREATE TABLE …`) est identique à PostgreSQL (le dialecte le plus proche).

### 5.4 Insérer des données — les 2 voies

**Voie 1** — `INSERT INTO … VALUES` (test, mini-projet M06.P1) :
```python
con.execute("""
INSERT INTO client (id_client, nom, prenom, telephone, ville) VALUES
    (0,  'COMPTOIR',  'CLIENT',       '0000000000',   'Koudougou'),
    (1,  'Dupont',    'Jean',         '+226 78 12 34 56 78', 'Koudougou'),
    (2,  'Durand',    'Marie',        '+226 78 12 34 56 79', 'Bobo-Diullasso');
""")
```

**Voie 2** — `INSERT INTO … SELECT … FROM read_csv_auto()` (production, import CSV) :
```python
con.execute("""
INSERT INTO client
SELECT CAST(id_client AS INTEGER) AS id_client,
       nom, prenom, telephone, ville
FROM read_csv_auto('03_exercices/dossier_M06/quincaillerie_export.csv',
                  all_varchar=true)
WHERE id_client != ''                   -- 3 lignes vides écartées
  AND TRY_CAST(id_client AS INTEGER) IS NOT NULL  -- 3 fantômes écartés
GROUP BY ALL;                           -- 1 891 clients uniques
""")
```

L'option **`all_varchar=true`** force toutes les colonnes en `TEXT` (avant conversion) ; c'est
*l'étape de chargement brut* où rien n'est converti. Le `TRY_CAST` *filtré* écarte les fantômes. Le
`GROUP BY ALL` agrège les doublons pour ne garder que les clients uniques.

### 5.5 Se connecter avec un client graphique

Un client graphique (DBeaver, DataGrip, pgAdmin, le CLI `duckdb`) lit confortablement la base. Pour
cet atelier, **le CLI suffit** :

```bash
duckdb 05_livrables/M06.duckdb
> SELECT id_client, nom FROM client LIMIT 5;
> .tables
> .quit
```

Le `.duckdb` est un fichier, le CLI l'ouvre comme un shell. C'est l'outil **quotidien** de l'analyste
qui pose des questions exploratoires.

### 5.6 Sauvegarder et migrer

```python
con.execute("EXPORT DATABASE 'backup_dir'")   # écrit Parquet + SQL
# Restauration dans une autre base
con2 = duckdb.connect(':memory:')
con2.execute("IMPORT DATABASE 'backup_dir'")
```

Le `EXPORT DATABASE` écrit un fichier `.parquet` par table et un `schema.sql` avec le DDL. Le
`IMPORT DATABASE` restaure. C'est l'**équivalent portable** d'un `pg_dump` pour DuckDB. Le piège
classique : `EXPORT DATABASE` ne sauvegarde pas les **vues** — il faut les redéfinir.

---

## 6. Cours approfondi — vivre avec SQLite (embarqué)

### 6.1 Ouvrir une base en Python

```python
import sqlite3

# Ouvrir (crée le fichier si absent)
con = sqlite3.connect('03_exercices/dossier_M06/quincaillerie.sqlite')
cur = con.cursor()

# Activer les FK (sinon, elles ne sont pas portées)
cur.execute("PRAGMA foreign_keys = ON")

# Créer la table
cur.execute("""
CREATE TABLE IF NOT EXISTS client (
    id_client    INTEGER PRIMARY KEY,
    nom          TEXT    NOT NULL,
    prenom       TEXT    NOT NULL,
    telephone    TEXT    NOT NULL UNIQUE
);
""")
con.commit()
```

**Trois pièges** par rapport à DuckDB :
1. SQLite est **natif Python** (pas d'import à faire après l'installation Python 3.13).
2. Les **FK ne sont pas actives par défaut** ; il faut `PRAGMA foreign_keys = ON` à chaque session.
3. SQLite ne supporte pas toutes les contraintes (pas de `CHECK (montant > 0)` complexe avant
   SQLite 3.32, 2020).

### 6.2 Importer un CSV

```python
import csv
with open('03_exercices/dossier_M06/quincaillerie_export.csv') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)
    cur.executemany(
        f"INSERT INTO client (id_client, nom, prenom, telephone) VALUES (?, ?, ?, ?)",
        [(r[0], r[7], r[8], r[9]) for r in rows if r[2].isdigit() and int(r[2]) < 900000]
    )
con.commit()
```

L'import SQLite est **plus verbeux** que DuckDB (`read_csv_auto`) : on lit le CSV avec `csv.reader`,
on filtre, on insère avec `executemany`. C'est *la perte de la commodité DuckDB*, gagnée sur la
*portabilité du fichier* (un `.sqlite` s'envoie par mail, alors qu'un `.duckdb` est aussi
envoyable, mais moins standard).

### 6.3 Exécuter les 3 requêtes `controles_integrite.sql`

```python
cur.execute("""
SELECT v.id_vente, v.id_client
FROM vente v LEFT JOIN client c ON v.id_client = c.id_client
WHERE c.id_client IS NULL;
""")
print("Q1 :", cur.fetchall())   # attendu : [] (0 ligne)
```

Les 3 requêtes (cf. C01 §5.5) sont portables **telles quelles** entre DuckDB et SQLite (le SQL est
ANSI). Le verdict est `0 ligne` pour Q1 et Q2 ; 5 lignes pour Q3.

### 6.4 Sauvegarder SQLite

```python
import shutil
con.commit()
con.close()
shutil.copy('quincaillerie.sqlite', 'quincaillerie_backup.sqlite')

# Ou via .backup du CLI sqlite3
# sqlite3 quincaillerie.sqlite ".backup quincaillerie_backup.sqlite"
```

La méthode **propre** est `.backup` (verrou cohérent), mais `shutil.copy` marche en pratique (le
risque est faible pour 24 000 lignes).

---

## 7. Cours approfondi — situer PostgreSQL (cité, non exécuté)

### 7.1 Pourquoi PostgreSQL n'est pas exécuté dans cet atelier

> **Définition.** Un **SGBD serveur** (*client-server DBMS*) est un moteur qui tourne sur une
> machine *dédiée* et écoute les connexions réseau sur un **port TCP** (par défaut 5432 pour
> PostgreSQL). Les clients s'y connectent par `host=… port=5432 user=… password=…`. C'est
> l'architecture de la production — quand l'équipe a 5 personnes qui partagent la base.
> — *English : client-server DBMS.*

L'**atelier Linux** ne peut pas exécuter PostgreSQL : ce serait installer un serveur PostgreSQL,
un utilisateur système, un dossier de données, un service systemd. C'est **~ 150 Mo** d'installation
et **5 à 10 minutes** de configuration. La règle du module est *on cite, on n'installe pas*.

### 7.2 Comment il fonctionne (cité)

```bash
psql -h db.example.com -U alice -d mydb      # CLI
pg_dump mydb > backup.sql                    # sauvegarde
psql mydb < backup.sql                       # restauration
```

**Trois concepts** :
1. **Le serveur** PostgreSQL tourne en arrière-plan (daemon `postgresql`), écoute sur le port
   **5432**.
2. **Le client** (`psql`, `pgAdmin`, DBeaver) se connecte par réseau avec un *user* et un
   *password*.
3. **La base** est un *catalogue* dans une *instance PostgreSQL* ; un serveur peut porter des
   centaines de bases.

### 7.3 Les 5 différences avec DuckDB

| Dimension | DuckDB | PostgreSQL |
|---|---|---|
| Architecture | intégré | client-serveur |
| Utilisateurs | 1 | plusieurs |
| Connexion | `import duckdb` | `psql -h host` |
| Persistance | fichier `.duckdb` | dossier `pg_data/` |
| Sauvegarde | `EXPORT DATABASE` | `pg_dump` |

**Le verdict** : pour 1 analyste sur son poste, DuckDB est imbattable. Pour 5 analystes en
entreprise, PostgreSQL est la référence. Le module M07 (SQL analyste) enseignera le **Dialecte
ANSI** avec DuckDB/PostgreSQL — c'est la même grammaire.

### 7.4 Quand choisir PostgreSQL (cité)

Cinq cas où PostgreSQL est *le bon choix* :
1. **Multi-utilisateurs** (5+ analystes qui partagent la base).
2. **Production critique** (transactionnel, 24/7).
3. **Volumes** > 50 millions de lignes.
4. **Conformité** (audit, RGPD, sauvegardes automatiques).
5. **Compétences** SQL avancées (CTE, window functions, JSON natif).

Hors de ces cas, DuckDB fait le travail.

---

## 8. Exemple concret — l'import CSV en DuckDB (le geste canonique)

### 8.1 Le contexte

Le dossier du projet M06.P contient `quincaillerie_export.csv` (24 000 lignes × 42 colonnes) et
`schema_3fn.sql` (la cible 3FN). Le **geste canonique** est : créer la base, lire le CSV avec
`all_varchar=true`, insérer dans les 7 tables (avec filtre), vérifier par les 3 requêtes.

### 8.2 Script complet en Python

```python
import duckdb
import os

DB = '03_exercices/dossier_M06/quincaillerie.duckdb'
CSV = '03_exercices/dossier_M06/quincaillerie_export.csv'

# 1. Ouvrir la base (en mode mémoire pour le test, persistant sinon)
con = duckdb.connect(DB)

# 2. Lire le DDL
ddl = open('03_exercices/dossier_M06/schema_3fn.sql').read()
con.execute(ddl)

# 3. Importer le brut en staging
con.execute(f"""
CREATE OR REPLACE TABLE export_brut AS
SELECT * FROM read_csv_auto('{CSV}', all_varchar=true)
""")

# 4. Insérer dans les tables cibles
con.execute("""
INSERT INTO client (id_client, nom, prenom, telephone, email, ville, fidelite_niveau)
SELECT DISTINCT CAST(id_client AS INTEGER), client_nom, client_prenom, client_telephone,
       client_email, ville_client, 'COMPTOIR'
FROM export_brut
WHERE TRY_CAST(id_client AS INTEGER) IS NOT NULL
  AND CAST(id_client AS INTEGER) < 900000  -- 3 fantômes écartés
""")
con.commit()

# 5. Vérifier par Q1
result = con.execute("""
SELECT v.id_vente, v.id_client FROM vente v
LEFT JOIN client c ON CAST(v.id_client AS INTEGER) = c.id_client
WHERE c.id_client IS NULL
""").fetchall()
print("Q1 :", len(result), "lignes (attendu 0)")
con.close()
```

### 8.3 Le verdict attendu

- `client` est peuplée avec **1 891** lignes.
- `produit` est peuplée avec **312** lignes (1 par référence unique).
- `mode_paiement` est peuplée avec **4** lignes.
- Q1 (intégrité référentielle) renvoie **0** ligne.
- La base persistant `quincaillerie.duckdb` fait ~ 1,2 Mo.

---

## 9. Démonstration pas à pas — la chaîne DuckDB en 6 étapes

### 9.1 Installer DuckDB

`pip install duckdb --no-cache-dir` — 8 Mo. Vérifier : `python3 -c "import duckdb"`.

### 9.2 Créer la base

```python
import duckdb
con = duckdb.connect(':memory:')   # ou fichier
```

### 9.3 Lire le CSV en staging

```python
con.execute(f"CREATE OR REPLACE TABLE v AS SELECT * FROM read_csv_auto('{CSV}', all_varchar=true)")
```

### 9.4 Insérer dans les tables cibles

```python
con.execute("INSERT INTO client SELECT DISTINCT … FROM v WHERE …")
```

### 9.5 Vérifier par les 3 requêtes

`controles_integrite.sql` (cf. C01 §5.5). Attendu : Q1 = 0, Q2 = 0, Q3 = 5 lignes.

### 9.6 Sauvegarder

`EXPORT DATABASE 'backup_dir'` ou `con.close()` (la base fichier persiste).

La chaîne DuckDB en 6 étapes : installer, ouvrir, lire CSV, insérer filtré, vérifier 3 requêtes,
sauvegarder. C'est la **même séquence** que C05 (transformation + dédoublonnage + jointure + verdict),
appliquée à un SGBD. La différence est *l'automatisation*.

---

## 10. Erreurs fréquentes

- **`pip install duckdb` sans `--no-cache-dir`** — le cache `~/.cache/pip` grossit de 100 Mo.
  Règle du module : *toujours `--no-cache-dir`*.
- **Importer avec `read_csv_auto` sans `all_varchar=true`** — DuckDB devine les types et **masque
  les défauts** (cf. M05 C03 §5.3). Règle : *texte avant conversion contrôlée*.
- **Ouvrir une base `.duckdb` en mode `:memory:`** — la base est *perdue* dès qu'on ferme. Pour
  tester, OK ; pour la production, ouvrir un *fichier*.
- **Ne pas activer `PRAGMA foreign_keys = ON` dans SQLite** — sans ça, les FK sont des *annotations*
  non portées. C'est le **piège n°1** de SQLite.
- **`INSERT INTO SELECT` sans `WHERE`** — la base reçoit *tout*, y compris les défauts. Règle :
  *toujours filtrer à l'insertion*.
- **Oublier `con.commit()` en SQLite** — le commit n'est pas implicite comme en DuckDB. La règle :
  *toujours `commit()` après chaque batch*.
- **`shutil.copy` comme sauvegarde** — sans verrou, on peut capturer une base dans un état
  partiel. Règle : *`.backup` pour SQLite, `EXPORT DATABASE` pour DuckDB, `pg_dump` pour
  PostgreSQL*.
- **Croire que le client graphique peut remplacer la base** — le client n'est qu'une *interface*
  de lecture. La base est sur disque.

> **À retenir.** Les 8 erreurs ci-dessus sont les pièges du quotidien d'un analyste qui installe un
> SGBD. La règle unique est **chaque SGBD a son piège d'installation** : DuckDB = cache pip, SQLite
> = `PRAGMA foreign_keys`, PostgreSQL = mot de passe.

## 11. Bonnes pratiques professionnelles

> **Dans les faits.** Sur le terrain, **4 bugs sur 5** liés aux FK fantômes en SQLite viennent de
> l'oubli de `PRAGMA foreign_keys = ON`. C'est un *scénario type* : l'analyste crée 50 tables avec
> des FK, importe 100 000 lignes par script, et tout *fonctionne* — sauf que les FK ne sont pas
> portées. Quand 6 mois plus tard il supprime un client par `DELETE`, les ventes restent (parce
> que la FK n'est pas portée, SQLite ne refuse pas), et la base est désormais **incohérente** sans
> qu'aucune requête Q1 ne le détecte. Le `pragma` est l'affaire d'une seconde, et c'est *la première
> ligne à écrire* dans tout projet SQLite.

- **Documenter le mode d'ouverture** dans le README (`pip install duckdb --no-cache-dir;
  duckdb.connect('fichier.duckdb')`).
- **`all_varchar=true` à l'import**, puis conversion *contrôlée* par script Python ou SQL.
- **`PRAGMA foreign_keys = ON` à chaque session SQLite** (sinon, FK fantômes).
- **Trois sauvegardes** : `EXPORT DATABASE` (DuckDB), `.backup` (SQLite), `pg_dump` (PostgreSQL).
- **Tester la base** par les 3 requêtes `controles_integrite.sql` à chaque modification.
- **Documenter la version** du SGBD dans le README (DuckDB 1.5.5, SQLite 3.45, PostgreSQL 16.x).

> **Conseil professionnel.** Le verdict d'une base n'est pas *« elle tourne »* ; c'est *« les 3
> requêtes renvoient 0 ligne »*. Cette discipline distingue une base d'un fichier plat. Et c'est ce
> que le projet M06.P évalue.

---

## 12. Exercice guidé — la chaîne DuckDB en 6 étapes (30 min, /15)

**Objectif.** Mobiliser la chaîne complète : installer, ouvrir, importer, insérer, vérifier, sauvegarder.

**Énoncé.** Sur le `quincaillerie_export.csv` (24 000 lignes) :
1. `pip install duckdb --no-cache-dir`
2. Ouvrir `:memory:`, créer la table `client(…)` du C02 §5.6.
3. Lire le CSV avec `all_varchar=true` dans une table `v`.
4. Insérer dans `client` (5 lignes seulement) avec `INSERT INTO … SELECT DISTINCT … FROM v LIMIT 5`.
5. Vérifier : `SELECT * FROM client` → 5 lignes.
6. Fermer (`con.close()`) et rouvrir. Vérifier que la base est vide (`:memory:` n'a pas de
   persistance — c'est l'erreur pédagogique attendue).

**Barème (/15).** 2 pt par étape + 5 pt bonus si l'étape 6 est comprise (`:memory:` ≠ fichier).

---

## 13. Exercices autonomes

- **Exercice 13.1 (15 min).** Listez les 3 modes d'ouverture de DuckDB (`:memory:`, fichier,
  `read_only`). Donnez un cas d'usage pour chacun.
- **Exercice 13.2 (30 min).** Reproduisez la chaîne DuckDB du § 8.2 sur le
  `quincaillerie_export.csv`. Vérifiez Q1, Q2, Q3. Notez les temps.
- **Exercice 13.3 (45 min).** Ouvrez la base SQLite `quincaillerie.sqlite` depuis Python, exécutez
  les 3 requêtes `controles_integrite.sql`. Notez 3 différences syntaxiques avec DuckDB.
- **Exercice 13.4 (60 min, optionnel).** Générez un `EXPORT DATABASE` de votre base DuckDB, ouvrez
  les fichiers `.parquet` produits avec `pandas.read_parquet()`. Commentez l'opération : est-ce
  *portable* ? est-ce *lisible* sans DuckDB ?

---

## 14. Correction détaillée

- **Exercice 13.1.** Trois modes : (a) `:memory:` — tests, exploration, pas de persistance ; (b)
  fichier `.duckdb` — production, persistance, sauvegarde ; (c) `read_only=True` — consultation
  seule (client graphique, audit, sécurité).
- **Exercice 13.2.** Temps attendus : import CSV ≈ 80 ms (24 000 lignes) ; insertion client ≈ 30
  ms ; Q1 ≈ 5 ms. **Total ≈ 120 ms.** Sur l'atelier, c'est sub-second ; sur un poste de
  production, c'est aussi sub-second.
- **Exercice 13.3.** Différences attendues : SQLite utilise `INTEGER` (DuckDB aussi, mais peut
  utiliser `BIGINT`) ; SQLite n'a pas de `SHOW TABLES` (utiliser `sqlite_master`) ; SQLite n'a pas
  `EXPORT DATABASE` (utiliser `.backup`).
- **Exercice 13.4.** Opération portable : oui, les Parquet sont universels (`pandas`, `pyarrow`,
  `polars`, `Spark`, `Athena`, `BigQuery`). Opération lisible sans DuckDB : oui, Parquet est
  auto-descriptif. La seule chose *perdue* est la **vue** `ligne_vente_ttc` — il faut la redéfinir
  dans le `schema.sql` lors de la restauration.

---

## 15. Mini-projet M06.P3 — « L'import contrôlé du brut » (1 h)

**Énoncé.** En reprenant le script § 8.2, **compléter** pour atteindre le verdict du projet M06.P :
1. Ouvrir la base en mode *fichier* (`quincaillerie.duckdb`).
2. Créer les 7 tables du `schema_3fn.sql`.
3. Importer 24 000 ventes dans `vente` (filtrées).
4. Importer 5 000 lignes `ligne_vente` (à partir des mêmes données, 1 produit par vente).
5. **Vérifier** par les 3 requêtes `controles_integrite.sql`.
6. **Sauvegarder** par `EXPORT DATABASE 'backup_dir'`.
7. **Documenter** dans un rapport (1 page) : lignes par table, totaux, anomalies trouvées.

**Critères de réussite.**

1. La base `quincaillerie.duckdb` fait **< 2 Mo**.
2. Les **3 requêtes** renvoient 0/0/5.
3. Le **rapport** liste 4 anomalies trouvées (parmi les 142 montants texte, 8 doublons, 12 dates,
   3 clients orphelins, …) avec leur traitement.
4. La **sauvegarde** crée un dossier `backup_dir/` avec ≥ 5 fichiers Parquet.

**Barème (/15).** 3 pt par critère vérifié, 3 pt pour le rapport, 2 pt bonus pour la vérification
cumulative (les 3 requêtes d'un coup).

---

## 16. Boîte à outils du chapitre

> **Boîte à outils.** Sept objets, un seul but — *vivre avec un SGBD sans drame* :
>
> 1. **La chaîne DuckDB en 6 étapes** (§ 9) — installer, ouvrir, importer, insérer, vérifier,
>    sauvegarder.
> 2. **Les 3 modes d'ouverture DuckDB** (§ 5.2) — `:memory:`, fichier, `read_only`.
> 3. **Les 2 voies d'insertion** (§ 5.4) — `INSERT INTO … VALUES` (test) vs `INSERT INTO … SELECT …
>    FROM read_csv_auto()` (import).
> 4. **Le `PRAGMA foreign_keys = ON` SQLite** (§ 6.1) — l'activation sans laquelle FK est fantôme.
> 5. **Les 5 différences DuckDB / SQLite** (§ 6) — natif, pragma, parquet, sauvegarde, CSV.
> 6. **Les 3 verbes de sauvegarde** — `EXPORT DATABASE` (DuckDB), `.backup` (SQLite), `pg_dump`
>    (PostgreSQL).
> 7. **Le client graphique cité** (§ 5.5) — DBeaver, DataGrip, pgAdmin : utile pour 100 000 lignes,
>    pas pour les tests.

## 17. Health Check (auto-correction, 6 questions, 15 min)

**Q1.** Quel est l'intérêt de `pip install duckdb --no-cache-dir` ? *(Réponse : éviter que le cache
`pip` ne grossisse de 100 Mo et sature le quota persistant de l'atelier.)*

**Q2.** Pourquoi `all_varchar=true` à l'import CSV ? *(Réponse : empêcher DuckDB autoload de
convertir silencieusement les colonnes sales — on veut garder la trace des défauts.)*

**Q3.** Quel est le piège classique de SQLite ? *(Réponse : `PRAGMA foreign_keys = ON` n'est pas
activé par défaut, donc les FK sont des annotations non portées.)*

**Q4.** Quand choisit-on DuckDB, SQLite, PostgreSQL ? *(Réponse : DuckDB = analyse solo, SQLite =
embarqué, PostgreSQL = multi-utilisateurs.)*

**Q5.** Quelle commande DuckDB exporte toute la base ? *(Réponse : `EXPORT DATABASE 'backup_dir'`.)*

**Q6.** Pourquoi `:memory:` n'est-il pas utilisable en production ? *(Réponse : la base est *en
mémoire RAM* et **perdue** à la fermeture de la connexion — pas de persistance.)*

**Q7.** Que font les 3 requêtes `controles_integrite.sql` ? *(Réponse : Q1 vérifie l'intégrité
référentielle (0 ligne) ; Q2 vérifie la cohérence des montants (0 ligne) ; Q3 calcule le total par
catégorie (5 lignes).)*

**Q8.** Quels sont les 3 verbes de sauvegarde ? *(Réponse : `EXPORT DATABASE` pour DuckDB,
`.backup` pour SQLite, `pg_dump` pour PostgreSQL.)*

**Q9.** Citez 2 clients graphiques pour PostgreSQL. *(Réponse : `pgAdmin` (officiel), DBeaver
(universel), DataGrip (JetBrains).)*

**Q10.** Pourquoi la commande `pg_dump` n'est-elle pas exécutable dans l'atelier ? *(Réponse :
parce que PostgreSQL n'est pas installé dans cet atelier — c'est la *règle 7* du plan M05
reconduite pour M06 ; on cite sans exécuter.)*

---

## 18. Résumé du chapitre

- **DuckDB** est un SGBD *intégré* (in-process), mono-utilisateur, gratuit. Il lit CSV, Parquet,
  JSON, fait du SQL ANSI.
- **SQLite** est un SGBD *embarqué*, natif Python 3.13, mono-utilisateur. Le `fichier.sqlite` *est*
  la base.
- **PostgreSQL** est un SGBD *serveur*, multi-utilisateurs, open source. C'est la référence de la
  production, **non installée** dans cet atelier (règle 7 du plan M05 reconduite).
- L'**import CSV** canonique est `INSERT INTO … SELECT … FROM read_csv_auto('fichier.csv',
  all_varchar=true)`.
- **Trois sauvegardes** : `EXPORT DATABASE` (DuckDB), `.backup` (SQLite), `pg_dump` (PostgreSQL).
- La **chaîne DuckDB en 6 étapes** (installer, ouvrir, importer, insérer, vérifier, sauvegarder)
  est l'épreuve de la pratique.

## 19. À retenir

> **À retenir.** Le choix DuckDB / SQLite / PostgreSQL est *une question de contraintes locales*
> (utilisateurs, volumétrie, persistance), pas une question de goût. DuckDB en première intention
> pour l'analyste solo, SQLite pour embarquer, PostgreSQL pour partager. Le bon professionnel sait
> *quand* basculer : c'est la règle des 5 critères du C05 + la *simplicité de mise en place*
> (DuckDB : aucune ; SQLite : natif ; PostgreSQL : serveur à installer).

> **À retenir.** `all_varchar=true` est le **garde-fou** de l'import CSV. Sans lui, DuckDB autoload
> convertit silencieusement « 1 200 FCFA » en `1200`, et la trace des défauts est **perdue**. Avec,
> la colonne reste `TEXT` jusqu'à la conversion *contrôlée* par script. C'est la même discipline que
> M04 §5.6 sur les formats : *charger brut, transformer sous contrôle*.

> **À retenir.** Le client graphique (DBeaver, DataGrip, pgAdmin) est **cité non exécuté** dans
> cet atelier — c'est l'usage quotidien d'un analyste sur 100 000+ lignes, mais il n'est pas
> nécessaire pour un atelier de formation. Le CLI `duckdb fichier.duckdb` suffit pour les tests ;
> le client graphique est *l'outil du confort*, pas *l'outil de la preuve*.

## 20. Évaluation formative (auto-correction, 8 min)

**Question 1.** Citez les 3 SGBD du module et leur cas d'usage. *(Réponse : DuckDB = analyste solo
intégré ; SQLite = embarqué mono-utilisateur ; PostgreSQL = serveur multi-utilisateurs.)*

**Question 2.** Quelle est la différence entre `EXPORT DATABASE` et `pg_dump` ? *(Réponse : les deux
exportent la base, mais DuckDB exporte en Parquet + SQL tandis que PostgreSQL exporte en SQL texte
uniquement.)*

**Question 3.** Pourquoi `PRAGMA foreign_keys = ON` est-il indispensable en SQLite ? *(Réponse : sans
ça, les FK sont des annotations non portées — la base ne refuse pas les orphelins.)*

**Question 4.** Quel est le piège de `read_csv_auto` sans `all_varchar=true` ? *(Réponse : DuckDB
autoload convertit silencieusement « 1 200 FCFA » en 1200 et masque le défaut métier.)*

**Question 5.** Que fait la commande `EXPORT DATABASE 'backup_dir'` ? *(Réponse : exporte toute la
base DuckDB en Parquet (tables) + schema.sql (DDL), portable vers n'importe quel outil Parquet.)*

**Question 6.** Citez 3 clients graphiques de PostgreSQL. *(Réponse : pgAdmin, DBeaver, DataGrip.)*

**Question 7.** Pourquoi ne pas exécuter PostgreSQL dans cet atelier ? *(Réponse : la règle 7 du
plan M05 reconduite pour M06 ; l'installation d'un serveur PostgreSQL est ≈ 150 Mo et 5-10 min,
hors budget de l'atelier ; on cite sans exécuter.)*

**Question 8.** Que se passe-t-il si on ferme une connexion `:memory:` ? *(Réponse : toute la base
est perdue — c'est le comportement attendu d'une base volatile.)*
