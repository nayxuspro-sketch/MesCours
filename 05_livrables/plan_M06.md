# Plan M06 — Bases de données relationnelles : comprendre avant de requêter

**Module M06 · 5 chapitres · 30 h · niveau N2 · prérequis M01.C03, M04 · porte de transition vers M07 (SQL).**

> **L'idée du module.** Le tableur atteint ses limites à la troisième table jointe et à la cinquantième
> millième ligne. La base de données relationnelle résout trois problèmes que le classeur ne sait pas
> résoudre : (a) **redondance** — la même valeur est recopiée dans 17 colonnes ; (b) **anomalie de mise à
> jour** — on change le nom d'un client à un endroit mais pas aux 11 autres ; (c) **intégrité référentielle**
> — une vente pointe sur un client qui n'existe plus. Le module installe **les concepts** (C01-C03) avant
> **la pratique** (C04 : DuckDB / SQLite / PostgreSQL) avant **le paysage** (C05 : NoSQL, lac, entrepôt).
> Le **projet M06.P** ferme le module : 42 colonnes dénormalisées → 7 tables normalisées en 3ᵉ forme
> normale (3FN), avec contraintes et intégrité vérifiée par 3 requêtes de contrôle.

## 1. Cadrage

### 1.1 Position dans l'architecture

- **Phase** 2 — Maîtrise opérationnelle.
- **Après** M04 (qualité), **avant** M07 (SQL analyste).
- **Prérequis** :
  - **M01.C03** (la table : lignes, colonnes, clés) — indispensable.
  - **M04.C01-C05** (diagnostic en 12 points, normalisation, doublons) — pour la transition vers 3FN.
- **Verrouillé** par M07 (qui requiert le vocabulaire relationnel) et par M13 (modélisation des données en
  étoile/flocon).

### 1.2 Cinq compétences de sortie (la matrice de couverture)

1. **Expliquer** la différence entre classeur Excel et base de données : ce que le SGBD résout (redondance,
   mise à jour, concurrence, volumétrie, sécurité) que le classeur ne sait pas résoudre.
2. **Modéliser** un domaine métier en 3ᵉ forme normale : extraire 7 tables d'un export à 42 colonnes en
   justifiant chaque clé.
3. **Créer** un schéma SQL avec contraintes (PRIMARY KEY, FOREIGN KEY, NOT NULL, CHECK, UNIQUE) et l'**exécuter**
   dans DuckDB / SQLite / PostgreSQL.
4. **Importer** un CSV dans une table, **vérifier** l'intégrité référentielle (les 3 requêtes de contrôle), et
   **réparer** les violations documentées.
5. **Choisir** un SGBD pour un cas d'usage (DuckDB intégré vs SQLite embarqué vs PostgreSQL serveur), et
   **situer** NoSQL, lac et entrepôt dans le paysage.

### 1.3 Fait du socle (mesurés le 19/09/2026)

- **Socle déjà livré** (issu de M04-M05) : `01_socle_donnees/data/brut/` (243 360 lignes de ventes, 20 fichiers),
  `01_socle_donnees/data/sahel.duckdb` (regénéré à la demande par `generation_socle.py`), et
  `01_socle_donnees/data/reference/verites_terrain.csv` (le corrigé des contrôles de qualité).
- **SGBD installé** : DuckDB 1.5.5 (`pip install --no-cache-dir duckdb`). SQLite natif Python 3.13 (rien à
  installer). PostgreSQL **non installé** dans l'atelier — le module cite PostgreSQL dans les encadrés sans
  l'exécuter (même règle que Power Query pour M05).
- **Cinq ajouts au socle** nécessaires pour M06 (à ouvrir en étape 2 du plan) :
  1. `tools/dossier_M06.py` — générateur de la base de la quincaillerie (le projet M06.P), graine **43**.
  2. Le fichier source **dénormalisé** `03_exercices/dossier_M06/quincaillerie_export.csv` (1 table,
     42 colonnes, ~ 24 000 lignes), calqué sur le projet M06 mais livré brut, non normalisé.
  3. Les **7 tables cibles** en SQL DDL dans `03_exercices/dossier_M06/schema_3fn.sql`, livrées avec les
     contraintes et l'ordre de création.
  4. Le **fichier `ATTENDU.json`** à 18 clés (les `m06p_*` dans `chiffres_manuel.py`).
  5. Le **schéma SQL de contrôle** dans `03_exercices/dossier_M06/controles_integrite.sql` (3 requêtes
     qui ferment le module).

### 1.4 Le projet M06.P — « La base de la quincaillerie »

- **Énoncé.** Un gérant de quincaillerie de Koudougou a remis son **export de caisse unique** : 42 colonnes
  dans une seule feuille Excel (CSV après extraction). Le stagiaire chargé de la base reçoit la consigne :
  *« range ça, mais je veux pouvoir retrouver une vente par ticket, par client, par produit, sans que tu
  changes un seul chiffre. »*
- **Livrables** (grille /20, seuil 13) :
  - **E1 — Schéma en 3FN** (4 points) — 7 tables dessinées à la main, chacune avec sa clé primaire, ses clés
    étrangères, et la justification de la forme normale (pas de dépendance transitive, pas de multi-valuée).
  - **E2 — DDL SQL** (4 points) — `schema_3fn.sql` exécutable, avec contraintes `PRIMARY KEY`, `FOREIGN KEY`,
    `NOT NULL`, `CHECK`, exécuté par `tools/controle_sql.py M06`.
  - **E3 — Import CSV** (4 points) — 24 000 ventes importées dans `vente`, 1 891 clients dans `client`,
    etc., avec rapport d'intégrité (lignes rejetées, motifs).
  - **E4 — Les 3 requêtes de contrôle** (4 points) — (a) toutes les `vente.id_client` pointent sur un client
    existant ; (b) tous les `montant_ttc` sont `> 0` ou `< 0` (retour) ; (c) le total par catégorie
    (alimentaire, bricolage, jardinage…) correspond au total du brut. Les 3 requêtes sont publiées dans
    `controles_integrite.sql` et exécutées.
  - **E5 — README de la base** (4 points) — 1 page, 4 sections : schéma (1 schéma texte + 1 tableau),
    cardinalités, contraintes, règles métier (retour = montant négatif, `id_client = 0` = comptoir).

### 1.5 Évaluation M06

- **Quiz** 15 Q (5 blocs : concepts SGBD, schéma, clés, SGBD en pratique, paysage).
- **2 exercices de modélisation papier** — un export de 24 colonnes à décomposer en tables, et un cas de
  relation N-M (clients × produits favoris) à transformer en table de jointure.
- **Étude de cas** — « l'école veut tout dans une seule feuille » : on défend la 3FN par les 5 anomalies
  qu'elle évite.
- **Corrigés** chiffrés sur le dossier livré.

## 2. Vocabulaire du module (à définir au premier emploi)

| Français — English | Première définition | Piège à éviter |
|---|---|---|
| **base de données** — *database* | un ensemble de tables reliées par des contraintes, persisté et requêtable. | confondre avec « fichier plat » : un CSV n'est pas une base, c'est une vue aplatie d'une base. |
| **SGBD** — *Database Management System, DBMS* | le logiciel qui gère la base (DuckDB, SQLite, PostgreSQL, MySQL, SQL Server). | confondre avec « SQL » : le SQL est le *langage*, le SGBD est le *moteur*. |
| **schéma** — *schema* | la structure (tables, colonnes, types, contraintes) d'une base, distincte des données. | confondre avec « table » : une base a *un* schéma et *N* tables. |
| **clé primaire** — *primary key* | la colonne (ou la combinaison) qui identifie une ligne de manière unique et non nulle. | confondre avec « index unique » : la PK a des contraintes fonctionnelles que l'index n'a pas. |
| **clé étrangère** — *foreign key* | une colonne qui pointe sur la clé primaire d'une autre table (intégrité référentielle). | penser qu'elle est « facultative » : sans FK, la colonne n'est qu'un nombre ; avec FK, c'est un lien. |
| **3ᵉ forme normale** — *3rd Normal Form, 3NF* | pas de dépendance transitive : toutes les colonnes non-clés dépendent de la clé, de toute la clé, rien que de la clé. | confondre avec « pas de redondance » : la 3FN autorise la redondance calculable (les *vues*). |
| **intégrité référentielle** — *referential integrity* | la garantie qu'une clé étrangère pointe toujours sur une ligne qui existe. | croire qu'elle est automatique : elle nécessite une `FOREIGN KEY … REFERENCES` dans le DDL. |
| **transaction** — *transaction* | une unité atomique de modifications (tout ou rien), avec propriétés ACID. | confondre avec « script » : un script peut faire 7 étapes mais n'est pas une transaction. |
| **NoSQL** — *Not only SQL* | la famille des bases non-relationnelles (document, clé-valeur, graphe, colonnes). | croire qu'elles remplacent les SGBDR : NoSQL complète le paysage, ne le remplace pas. |

## 3. Structure des 5 chapitres

### M06.C01 — Pourquoi une base et pas un classeur Excel — 5 h, ~12 p.

1. Cinq limites du tableur (cadrage de l'introduction) : redondance, anomalie de mise à jour,
   concurrence d'accès, volumétrie, sécurité.
2. Le cas fil rouge : `quincaillerie_export.csv` (42 colonnes, 24 000 lignes) — pourquoi le classeur
   ne suffit pas.
3. La solution SGBD : ce qu'elle résout, ce qu'elle coûte (installation, sauvegardes, gouvernance).
4. Les 5 critères du choix (calibre du M05 réinvestis) — DuckDB / SQLite / PostgreSQL / MySQL /
   SQL Server en première ligne.
5. Mini Health Check 5 questions sur la lecture de l'export brut.

### M06.C02 — Table, colonne, ligne, schéma, type, contrainte — 6 h, ~13 p.

1. Anatomie d'une table : colonnes typées, lignes atomiques, schéma séparé des données.
2. Les 5 types de base (numérique, texte, date, booléen, binaire) — ce que DuckDB autorise (14 types) et
   ce que les autres restreignent.
3. `NULL` n'est ni 0 ni vide : la logique ternaire du SQL (TRUE, FALSE, UNKNOWN), et `IS NULL` /
   `IS NOT NULL` (le test juste).
4. Contraintes de colonne : `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`.
5. Le mini-projet M06.P1 — créer 3 tables de référence en DDL DuckDB (côté client, côté produit,
   côté mode de paiement) sans encore importer.

### M06.C03 — Clés et relations — 7 h, ~16 p.

1. Clé primaire (`PRIMARY KEY`), clé candidate (et le choix entre elles), clé composite (sur 2 colonnes
   ou plus).
2. Clé étrangère (`FOREIGN KEY … REFERENCES`), avec `ON DELETE` et `ON UPDATE`.
3. Les trois relations : 1-1, 1-N, N-M. La table de jointure pour la N-M (exemple : clients ×
   produits favoris).
4. Intégrité référentielle : ce qui se passe si on viole la contrainte, et `CHECK` qui le détecte.
5. Le mini-projet M06.P2 — dessiner 7 tables à partir du brut, avec clés et cardinalités, et le schéma
   texte (la notation `1--∞` ou `M:N`).

### M06.C04 — Vivre avec DuckDB / SQLite / PostgreSQL — 7 h, ~17 p.

1. Trois moteurs à comparer (cadrage) : DuckDB (intégré, mono-processus), SQLite (embarqué, fichier),
   PostgreSQL (serveur, multi-utilisateurs). Les deux autres cités sans être exécutés (MySQL, SQL Server).
2. Installer DuckDB (déjà fait pour M05), créer une base en mémoire `:memory:`, exécuter un CREATE TABLE.
3. Insérer des données : `INSERT INTO … VALUES`, `INSERT INTO … SELECT … FROM read_csv_auto()`.
4. Importer un CSV — la fonction `read_csv_auto()` (réutilisation de la C03.M05) avec les options
   `header=true`, `sample_size`, `types`.
5. Se connecter avec un client graphique : DBeaver ou DataGrip (cité, non exécuté dans l'atelier),
   pour le **confort** de lecture des grandes tables.
6. Sauvegarder et migrer : `EXPORT DATABASE`, `.backup` SQLite, `pg_dump` PostgreSQL (les trois
   verbes de la portabilité).
7. Mini Health Check 6 questions : tester sa compréhension des trois moteurs.

### M06.C05 — Le paysage : NoSQL, datalake, entrepôt, lac — 5 h, ~12 p.

1. NoSQL quatre familles : **document** (MongoDB, CouchDB), **clé-valeur** (Redis, DynamoDB),
   **graphe** (Neo4j), **colonnes** (Cassandra, Bigtable).
2. Datamart, **datawarehouse** (entrepôt), **datalake** (lac), **lakehouse** — les quatre niveaux
   d'historisation.
3. Le critère de l'analyste : pour quel usage choisit-on quoi ? (transactionnel vs analytique,
   structuré vs non-structuré, fort vs faible volume).
4. Le mot qu'un analyste doit comprendre en entretien : « sharding » (partitionnement horizontal),
   « réplication » (copie asynchrone), « CAP » (cohérence, disponibilité, partitionnement).
5. Mini-projet M06.P3 — rédiger 1 page de glossaire des 5 mots d'entretien, en moins de 200 mots.

---

## 4. Le projet M06.P — « La base de la quincaillerie » — 6 h

*(Détail dans `03_exercices/M06_projet.md` au palier P2.)*

- Énoncé et matériel : `tools/dossier_M06.py` (graine 43) + `quincaillerie_export.csv` (42 colonnes,
  ~ 24 000 lignes) + `schema_3fn.sql` (à valider par le projet) + `controles_integrite.sql` (à valider).
- 5 livrables (E1-E5) + barème /20 + seuil 13.
- Empreinte sha256 du dossier livré : `m06p_empreinte_sha256` (clé attendue, à mesurer après génération).

## 5. Évaluation M06

*(Détail dans `04_evaluations/M06_evaluation.md` au palier P2.)*

- 15 questions de quiz (5 blocs).
- 2 exercices de modélisation papier (un export de 24 colonnes, un cas N-M).
- Étude de cas « l'école veut tout dans une seule feuille ».
- Corrigés chiffrés, table de décision d'orientation.

## 6. Ce qui doit être livré en P1 (palier où l'écriture est bornée à 5 chapitres)

- [ ] **Étape 1 — Plan détaillé** ← ce document. ✅ fait le 19/09/2026.
- [ ] **Étape 2 — Socle** : `tools/dossier_M06.py`, `quincaillerie_export.csv`, `schema_3fn.sql`
       (la cible, à valider par les projets), `controles_integrite.sql` (les 3 requêtes), `ATTENDU.json`
       (18 clés `m06p_*`), ajouts au `chiffres_manuel.py`.
- [ ] **Étape 3 — C01 à C05** (5 chapitres), autovalidation `autovalide.py M06 --strict` après chaque
       chapitre, cadence 1 push par chapitre. Le C04 (DuckDB / SQLite / PostgreSQL) sera le plus dense et
       **exécuté** sur DuckDB ; les encadrés PostgreSQL sont *cités sans exécutés* (même règle que
       Power Query pour M05).
- [ ] **Étape 4 — Figures** : `tools/figures_M06.py` (5 planches SVG).
- [ ] **Étape 5 — Rendu PDF** : `tools/render.py --join "02_modules/M06_*.md"` → `M06.pdf`, budget
       cible 80 p. ±15 %.
- [ ] **Étape 6 — Fiche contrôle** : `controle_pdf.py M06` + `fiche_controle_M06.md` (Q1-Q10, écarts).
- [ ] **Étape 7 — Push final** + `poids.py --strict` (quota 128 Mo).

**Restant (P2)** : `M06_projet.md`, `M06_evaluation.md`, mise à jour du README, push final.

---

**Fait le 19/09/2026 (ouverture).** Plan posé ; prérequis M04 livrés (clé 3FN non encore enseignée mais
l'introduction de M06.C02 la prend en charge sans detour par les formes 1FN/2FN/BCNF — la 3FN est l'objectif
*utilisé*, pas la grammaire formelle) ; DuckDB 1.5.5 opérationnel depuis M05, SQLite natif Python 3.13 ;
PostgreSQL non installé et hors atelier (règle 7 du plan M05 reconduite : *on cite, on n'exécute pas*).
L'export `quincaillerie_export.csv` (42 colonnes) est conçu pour porter **les mêmes défauts structurels que
le brut de M05** (textes, doublons, dates) — c'est ce qui justifie la dénormalisation.

**Reste, dans l'ordre :**

1. `tools/dossier_M06.py` (graine 43), `quincaillerie_export.csv` (~24 000 l.), `schema_3fn.sql` (cible), les
   3 contrôles d'intégrité, `ATTENDU.json` à 18 clés vérifié par 2 moteurs (DuckDB + pandas).
2. Section `m06()` dans `chiffres_manuel.py` (les clés `m06_*` + `m06p_*`), deux exécutions `diff` nul.
3. C01 → C02 → C03 → C04 → C05, autovalidation après chaque ; `controle_sql.py M06` après C04 ;
   `controle_python.py M06` à 0 par défaut (M06 n'enseigne pas Python — c'est M08).
4. `M06_projet.md` (5 livrables /20, seuil 13) et `M06_evaluation.md` (15 Q + 2 exercices + étude de cas).
5. `tools/figures_M06.py` (5 planches auditées, extension ≤ 776 px), `--join` → `M06.pdf` (budget 80 p.),
   `controle_pdf.py M06`, `fiche_controle_M06.md`, mise à jour du README et de ce plan, `poids.py --strict`.

— *fin du plan d'ouverture, suite à l'étape 2 —*
