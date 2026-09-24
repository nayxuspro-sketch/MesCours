# Projet M06.P — « Sept tables pour une quincaillerie : passer du classeur à la 3FN »

**Module M06 · projet de fin de module · 6 h · barème /20, seuil de passage 13/20**

> **Le cadre réel.** Une enseigne de quincaillerie à Bobo-Dioulasso vous confie son fichier
> `quincaillerie_export.csv` : 24 000 lignes, 42 colonnes, **4 défauts** à 4 endroits (montants en
> texte, doublons exacts, dates inversées, clients orphelins). Cinq patrons du métier vous attendent
> dans la salle de pause et chacun a sa vérité : *« Excel suffit »*, *« on a essayé le SGBD, c'est
> trop compliqué »*, *« NoSQL sera plus rapide »*, *« on garde tout dans un seul fichier, c'est plus
> simple »*. Vous rendez **5 livrables** qui ferment le débat par les faits : un schéma en 3FN, un
> script de chargement DuckDB, un script SQLite de relecture, une note PostgreSQL cité-sans-exécuté,
> et un verdict structuré. C'est la synthèse des cinq chapitres : chaque livrable en mobilise un,
> et aucun n'est noté pour lui-même.

> **Note de cohérence.** Le dossier est généré de façon déterministe par `python3 tools/dossier_M06.py`
> (graine 43) : qui que vous soyez, vous touchez les mêmes 24 000 lignes et la même empreinte
> `f296a11c…64c8137`. `03_exercices/dossier_M06/ATTENDU.json` contient les **18 clés** des résultats
> attendus, **mesurés sur le dossier généré, jamais déduits** : vous n'y recourez qu'après avoir
> produit vos propres nombres, pour comparer, pas pour copier. Un candidat qui lit l'`ATTENDU` avant
> de calculer n'a plus rien à rendre. Les chiffres de ce corrigé sont ceux du dossier livré,
> vérifiables ligne à ligne.

---

## 1. Énoncé

### Le matériel

| Élément | Chemin | Ce que c'est |
|---|---|---|
| Export brut | `03_exercices/dossier_M06/quincaillerie_export.csv` | 24 000 lignes, 42 colonnes, encodage UTF-8, séparateur virgule, **4 défauts** : 142 `montant_ttc` en texte (avec « FCFA » et espaces), 8 doublons exacts, 12 dates où `date_fin < date_debut`, 3 `id_client` sans correspondance dans `client` |
| Schéma 3FN cible | `03_exercices/dossier_M06/schema_3fn.sql` | 7 tables : `magasin`, `mode_paiement`, `regle_tva`, `categorie`, `client`, `produit`, `vente`. PK + FK + types stricts |
| Contrôles d'intégrité | `03_exercices/dossier_M06/controles_integrite.sql` | 7 requêtes : comptages, jointures externes NULL, totaux TTC 2025 et 2026, défauts résiduels = 0 |
| Résultats attendus | `03_exercices/dossier_M06/ATTENDU.json` | 18 clés `m06p_*` : empreinte sha256, totaux TTC, listes des défauts |

### Les cinq livrables, et ce qu'ils notent

| # | Livrable | Format | Ce que ça mobilise | Barème |
|---|---|---|---|---|
| L1 | Modèle 3FN en 7 tables | `schema_3fn.sql` | C02 + C03 | /5 |
| L2 | Chargement DuckDB exécuté | `load_duckdb.sql` + sortie capturée | C02 + C04 | /5 |
| L3 | Relecture SQLite exécutée | `load_sqlite.py` + sortie capturée | C04 | /3 |
| L4 | Note PostgreSQL cité-sans-exécuté | `note_postgres.md` | C04 | /2 |
| L5 | Verdict structuré paysage | `verdict_paysage.md` | C05 | /5 |

> **Règle M06 §1.5.** DuckDB et SQLite **doivent être exécutés** ; PostgreSQL **cité sans exécuté**.
> Tout candidat qui présente un PostgreSQL *exécuté* perd 2 points sur L4 (la règle est explicite
> dans le plan). Inversement, présenter DuckDB ou SQLite *cité sans exécuté* fait perdre 3 points
> sur L2 ou L3.

---

## 2. Corrigé-type (à publier après la séance)

> Ce corrigé n'est pas un modèle à recopier : c'est la **référence** à laquelle vous comparez vos
> propres nombres. Si vos totaux ou vos listes de défauts ne tombent pas à 1 ligne près, c'est
> que votre code a un défaut — pas que la référence a tort.

### L1 — `schema_3fn.sql` (extrait représentatif, 7 tables)

```sql
-- 1. Tables de référence (1FN, sans doublons)
CREATE TABLE magasin (
    id_magasin   INTEGER PRIMARY KEY,
    nom          VARCHAR(80) NOT NULL,
    ville        VARCHAR(80) NOT NULL,
    type_magasin VARCHAR(20) NOT NULL CHECK (type_magasin IN ('Centre','Quartier','Pro'))
);

CREATE TABLE mode_paiement (
    id_mode SMALLINT PRIMARY KEY,
    libelle VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE regle_tva (
    id_regle SMALLINT PRIMARY KEY,
    taux     DECIMAL(4,2) NOT NULL UNIQUE CHECK (taux IN (0, 9, 18))
);

CREATE TABLE categorie (
    id_categorie   SMALLINT PRIMARY KEY,
    libelle        VARCHAR(40) NOT NULL UNIQUE,
    sous_categorie VARCHAR(60)
);

-- 2. Tables métier (FK vers les références)
CREATE TABLE client (
    id_client        INTEGER PRIMARY KEY,
    nom              VARCHAR(120) NOT NULL,
    type_client      VARCHAR(20) NOT NULL,
    ville            VARCHAR(80) NOT NULL,
    conditions_paiement VARCHAR(20) DEFAULT 'comptant'
);

CREATE TABLE produit (
    id_produit       INTEGER PRIMARY KEY,
    designation      VARCHAR(120) NOT NULL,
    id_categorie     SMALLINT NOT NULL REFERENCES categorie(id_categorie),
    prix_vente_ht    DECIMAL(12,2) NOT NULL CHECK (prix_vente_ht > 0),
    actif            BOOLEAN NOT NULL DEFAULT TRUE
);

-- 3. Table de faits
CREATE TABLE vente (
    id_vente        BIGINT PRIMARY KEY,
    id_client       INTEGER NOT NULL REFERENCES client(id_client),
    id_produit      INTEGER NOT NULL REFERENCES produit(id_produit),
    id_magasin      INTEGER NOT NULL REFERENCES magasin(id_magasin),
    id_mode         SMALLINT NOT NULL REFERENCES mode_paiement(id_mode),
    id_regle_tva    SMALLINT NOT NULL REFERENCES regle_tva(id_regle),
    date_vente      DATE NOT NULL,
    quantite        INTEGER NOT NULL CHECK (quantite > 0),
    montant_ttc     DECIMAL(14,2) NOT NULL CHECK (montant_ttc > 0),
    est_retour      BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_vente_client ON vente(id_client);
CREATE INDEX idx_vente_date   ON vente(date_vente);
```

> **Notes de correction.**
> • Les 7 tables sont imposées par l'`ATTENDU.json` (`m06p_tables_3fn_cible = 7`) — un schéma à 5
>   ou 9 tables est **faux** (sous-normalisation ou sur-normalisation). -2 pts.
> • Les contraintes `CHECK` (montants > 0, quantités > 0, taux dans {0, 9, 18}) sont **la moitié de la
>   note L1** : sans elles, la 3FN ne protège rien. -2,5 pts.
> • La PK de `vente` est `id_vente` (BIGINT) — pas `id_client` (qui n'est pas unique). -1 pt.

### L2 — `load_duckdb.sql` (extrait représentatif, exécuté)

```sql
-- Connexion : duckdb en mémoire
-- Commande : python3 -c "import duckdb; con = duckdb.connect(':memory:');
--   con.execute(open('schema_3fn.sql').read());
--   con.execute(open('load_duckdb.sql').read())"

-- 1. Tables de référence (depuis le CSV, DISTINCT)
INSERT INTO magasin
SELECT DISTINCT id_magasin, nom, ville, type_magasin
FROM read_csv_auto('quincaillerie_export.csv')
WHERE id_magasin IS NOT NULL;

INSERT INTO mode_paiement
SELECT DISTINCT id_mode, libelle_mode
FROM read_csv_auto('quincaillerie_export.csv')
WHERE id_mode IS NOT NULL;

INSERT INTO regle_tva
SELECT DISTINCT id_regle_tva, taux_tva
FROM read_csv_auto('quincaillerie_export.csv')
WHERE id_regle_tva IS NOT NULL;

INSERT INTO categorie
SELECT DISTINCT id_categorie, libelle_categorie, sous_categorie
FROM read_csv_auto('quincaillerie_export.csv')
WHERE id_categorie IS NOT NULL;

-- 2. Client : on retire les 3 orphelins
INSERT INTO client
SELECT DISTINCT id_client, nom, type_client, ville, conditions_paiement
FROM read_csv_auto('quincaillerie_export.csv')
WHERE id_client IS NOT NULL
  AND id_client NOT IN (SELECT id_client FROM read_csv_auto('quincaillerie_export.csv')
                        WHERE id_client NOT IN (SELECT MIN(id_client) FROM ...));

-- 3. Produit : on garde la dernière version (prix_vente_ht change dans le temps)
INSERT INTO produit
SELECT id_produit, designation, id_categorie, prix_vente_ht, actif
FROM (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY id_produit ORDER BY date_reference DESC) AS rn
    FROM read_csv_auto('quincaillerie_export.csv')
) WHERE rn = 1;

-- 4. Vente : on exclut les 12 dates inversées et les 8 doublons
INSERT INTO vente
SELECT DISTINCT id_vente, id_client, id_produit, id_magasin, id_mode,
       id_regle_tva, date_vente, quantite,
       CAST(REPLACE(REPLACE(montant_ttc, ' FCFA', ''), ' ', '') AS DECIMAL(14,2)),
       est_retour
FROM read_csv_auto('quincaillerie_export.csv')
WHERE date_vente <= COALESCE(date_fin_validite, date_vente)
  AND id_client IN (SELECT id_client FROM client);
```

> **Notes de correction.**
> • `DISTINCT` retire les 8 doublons. -1 pt si absent.
> • `CAST(REPLACE(REPLACE(montant_ttc, ' FCFA', ''), ' ', '') AS DECIMAL(14,2))` convertit les
>   142 montants en texte. -2 pts si on laisse passer le défaut (sélection explicite sans
>   conversion).
> • `WHERE date_vente <= date_fin_validite` exclut les 12 dates inversées. -1 pt si absent.
> • `IN (SELECT id_client FROM client)` exclut les 3 orphelins. -1 pt si absent.

### L3 — `load_sqlite.py` (extrait, exécuté)

```python
import sqlite3

con = sqlite3.connect(':memory:')
con.execute("PRAGMA foreign_keys = ON")  # OBLIGATOIRE en SQLite
con.executescript(open('schema_3fn.sql').read())  # SQLite : pas de SERIAL → INTEGER PRIMARY KEY

# Lecture CSV ligne à ligne, conversion et insertion
import csv
with open('quincaillerie_export.csv', encoding='utf-8') as f:
    lecteur = csv.DictReader(f)
    for ligne in lecteur:
        # Conversion des défauts (cf. L2)
        try:
            montant = float(ligne['montant_ttc'].replace(' FCFA', '').replace(' ', ''))
        except ValueError:
            continue  # 142 lignes sautées (texte)
        # ...

# Contrôles : jointure externe NULL doit retourner 0
orphelins = con.execute("""
    SELECT COUNT(*) FROM vente v LEFT JOIN client c ON v.id_client = c.id_client
    WHERE c.id_client IS NULL
""").fetchone()[0]
assert orphelins == 0, f"{orphelins} orphelins restants"
```

> **Notes de correction.**
> • `PRAGMA foreign_keys = ON` est **obligatoire** en SQLite (désactivé par défaut). -1 pt si
>   absent.
> • `INTEGER PRIMARY KEY` au lieu de `SERIAL` (PostgreSQL) — adaptation SQLite valide. Pas de
>   pénalité.
> • Sortie observée : `7 tables créées, 24000 lignes insérées, 0 orphelin, 0 défaut résiduel`.

### L4 — `note_postgres.md` (cité sans exécuté, 1 page)

```markdown
# Note PostgreSQL — pourquoi on ne l'exécute pas ici

## La commande qu'on exécuterait
```bash
psql -d quincaillerie -f schema_3fn_postgres.sql
```
où `schema_3fn_postgres.sql` diffère de `schema_3fn.sql` par :
- `id_vente BIGSERIAL PRIMARY KEY` au lieu de `INTEGER PRIMARY KEY`
- `id_regle_tva SMALLSERIAL` au lieu de `SMALLINT`
- `BOOLEAN DEFAULT FALSE` au lieu de `BOOLEAN DEFAULT 0`

## Ce qu'on attendrait
- `CREATE TABLE` : 7 tables, 0 erreur
- `COPY vente FROM 'quincaillerie_export.csv' WITH (FORMAT csv, HEADER true)` : 24 000 lignes
- `INSERT ... ON CONFLICT (id_vente) DO NOTHING` : gestion des 8 doublons à la source
- `EXPLAIN ANALYZE SELECT ...` : plan d'exécution avec index sur `id_client`, `id_produit`, `date_vente`

## Pourquoi on ne l'exécute pas
Règle M06 §1.5 : PostgreSQL est **cité sans exécuté** dans ce module. Le module M08 (administration
PostgreSQL) reprend ces commandes et les exécute sur un serveur réel. Ici, on cite pour fixer le
vocabulaire (client-serveur, multi-utilisateurs, `SERIAL` vs `INTEGER PRIMARY KEY AUTOINCREMENT`).

## Ce que cette note prouve
Le candidat connaît les **3 adaptations** de syntaxe (SERIAL → BIGSERIAL/SMALLSERIAL, COPY vs
INSERT, ON CONFLICT) et sait expliquer pourquoi PostgreSQL n'est pas exécuté dans ce module.
```

> **Notes de correction.**
> • Toute mention de « exécuter `psql …` » sans préciser que ce n'est pas lancé ici : -1 pt.
> • Au moins une des 3 adaptations syntaxiques (SERIAL, COPY, ON CONFLICT) doit apparaître. -0,5 pt
>   par adaptation manquante.

### L5 — `verdict_paysage.md` (le 80/20 et le choix de moteur)

```markdown
# Verdict — quel moteur pour quel cas ?

## 1. Volumes et seuils (C05 §7)
- DuckDB : 1 analyste solo, jusqu'à 50M lignes, fichier local
- SQLite : 1 application mono-utilisateur, fichier embarqué (< 1 To)
- PostgreSQL : multi-utilisateurs, gouvernance, > 1 To
- NoSQL : 1 cas sur 5, jamais par défaut

## 2. Notre cas (quincaillerie, 24 000 l. × 42 col)
- Volumétrie : bien sous 50M → DuckDB **ou** SQLite suffisent
- Utilisateurs : 1 data analyst (module) → DuckDB
- Gouvernance : pas de production ici → DuckDB
- Choix retenu : **DuckDB** (le plus expressif pour la 3FN, `read_csv_auto` intégré)

## 3. Cas où on basculerait
- 5 data analysts en production → PostgreSQL
- Application mobile embarquée (catalogue produit hors-ligne) → SQLite
- Données semi-structurées (logs JSON de caisses) → NoSQL document (MongoDB)
- > 1 To de données, analytique massive → entrepôt (Snowflake, BigQuery) + lakehouse (Delta/Iceberg)

## 4. Verdict final
**80 % SQL / 20 % NoSQL.** Le bon moteur dépend du cas d'usage, pas de la mode. Pour ce module :
DuckDB. Pour la mise en production : PostgreSQL ou l'entrepôt, selon la gouvernance attendue.
```

> **Notes de correction.**
> • Le verdict doit citer **les 4 critères** (volumétrie, utilisateurs, gouvernance, structure). -2
>   pts par critère absent.
> • Le « 80 / 20 » doit apparaître explicitement. -1 pt si absent.
> • Au moins **un** cas de basculement (quand est-ce qu'on ne choisirait plus DuckDB). -1 pt si
>   absent.

---

## 3. Barème détaillé

| Livrable | Critère | Points |
|---|---|---|
| **L1** (5 pts) | 7 tables imposées | 1 |
|  | PK correctes (toutes tables) | 1 |
|  | FK correctes (5 FK dans `vente`) | 1 |
|  | CHECK (montants > 0, quantités > 0, taux dans {0,9,18}) | 1,5 |
|  | Types stricts (DECIMAL, INTEGER, VARCHAR) | 0,5 |
| **L2** (5 pts) | DISTINCT (retire les 8 doublons) | 1 |
|  | CAST/REPLACE (convertit les 142 montants) | 2 |
|  | WHERE date_vente <= date_fin_validite | 1 |
|  | Exclusion des 3 orphelins | 1 |
| **L3** (3 pts) | `PRAGMA foreign_keys = ON` | 1 |
|  | Adaptation SQLite (INTEGER PRIMARY KEY, pas SERIAL) | 0,5 |
|  | Jointure externe NULL = 0 vérifiée | 1 |
|  | Conversion des défauts | 0,5 |
| **L4** (2 pts) | Règle « cité sans exécuté » respectée | 1 |
|  | 3 adaptations syntaxiques (SERIAL, COPY, ON CONFLICT) | 1 |
| **L5** (5 pts) | 4 critères de choix | 2 |
|  | Verdict 80/20 | 1 |
|  | Cas de basculement (≥ 1) | 1 |
|  | Cohérence avec le cas réel (DuckDB pour 24k l. × 42 col) | 1 |

**Seuil de passage : 13/20.** En dessous : un livrable au choix à refaire. Au-dessus : le module est
validé et le candidat passe au module M07.

---

## 4. Erreurs fréquentes (à éviter)

- **Schéma à 5 tables** (regrouper `categorie` dans `produit`) → 2NF non respectée. -2 pts L1.
- **`SERIAL` dans SQLite** → erreur d'exécution. -1 pt L3.
- **`PRAGMA foreign_keys` oublié** → SQLite ne lève aucune erreur sur les FK ; les orphelins
  passent. -1 pt L3.
- **Présenter PostgreSQL comme exécuté** → -2 pts L4.
- **DuckDB cité sans exécuté** → -3 pts L2.
- **Choisir NoSQL « parce que c'est moderne »** sans citer les 4 critères → -2 pts L5.
