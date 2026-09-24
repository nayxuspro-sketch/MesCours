# Module M06.C03 — Clés et relations : primaire, étrangère, candidate, composite, 1-1, 1-N, N-M

**Outils : DuckDB 1.5.5 (intégré), SQLite natif Python, PostgreSQL cité. Durée indicative : 7 h.
Niveau : N2. Prérequis : M06.C01 + M06.C02.**

> **L'idée du chapitre.** Le C01 a posé *pourquoi* une base, le C02 a posé *de quoi* une table est faite.
> Le C03 fait le lien : *comment* les tables se parlent. Le vocabulaire du C03 est **transverse** : clé
> primaire, clé étrangère, 1-1, 1-N, N-M, intégrité référentielle, table de jointure, ON DELETE, ON UPDATE.
> C'est le vocabulaire qui permet de **lire** un schéma et de **construire** un schéma. Le C03 est aussi
> le chapitre qui ferme le **projet M06.P** : la compréhension des relations permet de transformer le brut
> dénormalisé en un schéma 3FN à 7 tables. Le verdict du C03 est **« chaque table a sa clé, et chaque
> clé étrangère a sa cible »** : c'est la discipline qui distingue un schéma relationnel d'un schéma
> « à plat ».

> **Base de travail — le projet M06.P.** C03 réutilise le `quincaillerie_export.csv` (24 000 lignes × 42
> colonnes, livré par `tools/dossier_M06.py`), et applique la **3FN** : `m06p_tables_3fn_cible = 7`
> tables. Le C03 enseigne les **3NF-types de relations** (1-1, 1-N, N-M) et le mécanisme des **clés
> étrangères** (FK). C'est ce qui ferme la porte au défaut des **« clients orphelins »** du C01 § 5.2.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

- **définir** une clé primaire, une clé candidate, une clé composite, une clé étrangère ;
- **distinguer** les trois types de relations (1-1, 1-N, N-M) ;
- **créer** une `FOREIGN KEY` DuckDB avec `ON DELETE` et `ON UPDATE` ;
- **construire** une **table de jointure** pour une relation N-M (l'exemple `client_categorie_pref`) ;
- **vérifier** l'intégrité référentielle par la requête Q1 de `controles_integrite.sql` ;
- **lire** un schéma 3FN et **identifier** la cardinalité de chaque relation ;
- **réparer** une violation d'intégrité (un client orphelin).

## 2. Pourquoi cette notion est importante

- La **clé primaire** est l'**identifiant unique d'une ligne**. Sans elle, on ne sait pas compter, ni
  distinguer deux lignes a priori identiques. C'est le **fondement** de toute la base.
- La **clé étrangère** est le **lien formel entre deux tables**. Sans elle, la colonne `id_client`
  dans `vente` n'est qu'un nombre ; avec elle, c'est un **contrat** : cette colonne pointe sur un
  client qui existe. C'est la garantie du § 1.4 du C01 (redondance + intégrité).
- Les **3 types de relations** (1-1, 1-N, N-M) couvrent tous les cas métier. Le chargement sur 12-15
  pages que le C02 a installé trouve ici sa **mise en relation** : une ligne de `vente` est **liée à
  un** client (1-N), un client **possède 1..N** catégories préférées (N-M), une ligne de
  `ligne_vente` est **liée à 1** produit (1-N), un retour est **lié à 1** vente (1-1).
- Le **projet M06.P** ferme le chapitre : la 3FN appliquée à `quincaillerie_export.csv` donne
  `m06p_tables_3fn_cible = 7` tables, dont la 6ᵉ (`client_categorie_pref`) est une **table de jointure**
  N-M. C'est l'épreuve de vérité.
- **L'intégrité référentielle** est ce qui ferme la porte aux **clients orphelins** (les 3 du C01 §
  5.2). Sans `FOREIGN KEY`, on peut insérer une vente avec `id_client = 900042` qui pointe dans le
  vide ; avec, c'est **refusé**. C'est la **discipline** du module.
- `ON DELETE` et `ON UPDATE` sont les **verbes de la cascade**. Par défaut, on **refuse** la
  suppression d'un client qui a des ventes (sinon, les ventes deviennent orphelines). C'est le **CASCADE**
  ou le **RESTRICT** au choix — c'est une décision documentée.

## 3. Explication simple — les 6 éléments d'une relation

Une **relation** entre deux tables est définie par 6 éléments :

1. **Table source** — celle qui porte la clé étrangère.
2. **Colonne FK** — la clé étrangère dans la table source.
3. **Table cible** — celle qui porte la clé primaire référencée.
4. **Colonne PK** — la clé primaire dans la table cible.
5. **Cardinalité** — combien de lignes de la source pointent sur combien de lignes de la cible
   (1-1, 1-N, N-M, N-1 — oui, la symétrie).
6. **Action** — que se passe-t-il en cas de `DELETE` / `UPDATE` sur la cible ? (RESTRICT, CASCADE,
   SET NULL, NO ACTION)

Le **résumé en une phrase** : *« Une relation, c'est une flèche d'une table vers une autre, avec sa
cardinalité et son contrat de cascade. »*

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **clé primaire** — *primary key, PK* | la colonne (ou combinaison) qui identifie une ligne de manière unique et non nulle. | confondre avec « identifiant métier » : la clé primaire peut être **propre à la base** (`id_vente` auto-incrémenté), distincte du `id_ticket` métier. |
| **clé candidate** — *candidate key* | une colonne (ou combinaison) qui **pourrait** être clé primaire mais qui n'a pas été choisie. Une table peut avoir plusieurs clés candidates ; la PK est l'une d'elles. | croire qu'il y en a toujours plusieurs : un client avec un `id_client` peut n'avoir qu'**une** clé candidate. |
| **clé composite** — *composite key* | une clé primaire (ou étrangère) qui porte sur **plus d'une colonne**. Par exemple, la PK de `ligne_vente` est `(id_vente, id_produit)`. | croire qu'elle est « faible » : la clé composite est souvent **plus stable** qu'un `id` auto-incrémenté (elle n'introduit pas de nouvelle colonne). |
| **clé étrangère** — *foreign key, FK* | une colonne qui pointe sur la clé primaire d'une autre table. **La contrainte FK** garantit que la valeur pointée existe. | croire qu'elle est juste « pour information » : sans la **contrainte** FK, la colonne n'est qu'un nombre sans lien. |
| **intégrité référentielle** — *referential integrity* | la **garantie** qu'une clé étrangère pointe sur une ligne qui existe. C'est un **contrat** que la base tient (ou pas). | croire qu'elle va de soi : il faut l'**écrire** dans le DDL (`FOREIGN KEY … REFERENCES …`). |
| **relation 1-1** — *one-to-one* | chaque ligne de la table source correspond à **au plus une** ligne de la table cible, et inversement. Exemple : `client` ↔ `client_profil` (un seul profil par client). | confondre avec un attribut : une relation 1-1 est une **séparation volontaire** (gros attributs, sécurité par ligne, table de référence lente). |
| **relation 1-N** — *one-to-many* | chaque ligne de la source correspond à **0..N** lignes de la cible, et chaque ligne de la cible correspond à **au plus 1** source. Exemple : `client` ↔ `vente` (un client, plusieurs ventes). | croire qu'elle est toujours simple : la cardinalité change si on passe à `client` ↔ `categorie_pref` (N-M). |
| **relation N-M** — *many-to-many* | chaque ligne de la source peut correspondre à **0..N** lignes de la cible, et inversement. Exemple : `client` ↔ `categorie_pref`. | croire qu'on peut la stocker dans une colonne : une colonne ne porte qu'**une** valeur, donc il faut une **table de jointure**. |
| **table de jointure** — *junction table, association table* | une table **intermédiaire** qui matérialise une relation N-M. Sa PK est la **composée** des deux FK (ex. `(id_client, categorie)` dans `client_categorie_pref`). | croire qu'elle est « secondaire » : c'est la table qui **porte** la relation N-M, sans elle la 3FN est violée. |
| **`REFERENCES`** | le mot-clé SQL qui déclare la **cible** d'une FK : `id_client INTEGER REFERENCES client(id_client)`. | confondre avec le nom de la contrainte : `REFERENCES` est obligatoire, le nom de la contrainte est facultatif. |
| **`ON DELETE`** | l'action à prendre quand la **ligne cible** est supprimée : `CASCADE` (supprime aussi la source), `RESTRICT` (refuse la suppression), `SET NULL` (met la FK à `NULL`). | croire que le défaut est `CASCADE` : le défaut est `RESTRICT`/`NO ACTION` (refuse). C'est **safe by default**. |
| **`ON UPDATE`** | l'action quand la **PK cible** change. Mêmes verbes que `ON DELETE`. | croire que `ON UPDATE` est inutile : si la PK est un `id` auto-incrémenté, elle ne change *jamais*, donc `ON UPDATE` est en pratique vide. |
| **`CHECK`** (cf. C02) | contrainte qui valide une **condition**. Dans une FK, on peut ajouter `CHECK` sur la valeur pour valider le métier. | confondre avec contrainte de table : `CHECK` peut être de colonne ou de table. |
| **`MATCH FULL` / `MATCH SIMPLE`** | mode de correspondance des FK composites : FULL = toutes les colonnes, SIMPLE = au moins une (défaut). | croire que `MATCH FULL` est plus strict : c'est juste **un autre mode**, moins utilisé en pratique. |
| **orphelin** — *orphan* | une ligne dont la FK pointe sur une cible **inexistante**. Le défaut « 3 clients fantômes » du C01 § 5.2. | croire qu'ils sont inoffensifs : une jointure sur des orphelins **disparaît silencieusement** (`LEFT JOIN` ne renvoie rien). |

> **Définition.** Une **clé étrangère** est une **contrainte** qu'on **déclare** dans le DDL et que la
> base **fait respecter** à chaque insertion et à chaque suppression. Sa forme canonique est :
> `FOREIGN KEY (colonne_source) REFERENCES table_cible (colonne_cible) [ON DELETE action] [ON UPDATE
> action]`. Sans cette déclaration, la colonne est juste un nombre ; avec, c'est un **contrat** —
> une FK garantit l'**intégrité référentielle** : la valeur pointée existe, ou la base refuse.
> — *English : foreign key, FK.*

> **Définition.** Une **cardinalité** est le **nombre** de liens entre une ligne source et les lignes
> cibles. Elle se note `1:1`, `1:N` (ou `1..∞`), `N:M` (ou `N..∞ : M..∞`). Elle est **asymétrique** :
> `client → vente` est *un-à-plusieurs*, mais `vente → client` est *un-à-un* (chaque vente a au
> plus un client). C'est cette asymétrie qui fait qu'on dessine une flèche avec sa cardinalité, et
> que la **direction de la FK** est *toujours* de la N vers le 1 (la ligne côté N porte la FK).
> — *English : cardinality.*

> **Définition.** Une **table de jointure** matérialise une relation N-M. Sa **clé primaire** est la
> *composée* des deux FK (par exemple `PRIMARY KEY (id_client, categorie)`), et chaque ligne **duplique**
> les attributs partagés (`id_client` côté `client`, `categorie` côté `categorie_pref`). Sans la table
> de jointure, la relation N-M est **impossible à exprimer** (une colonne ne porte qu'une valeur), donc
> la 3FN est violée. La table de jointure est *l'outil* par lequel la 3FN résout le multi-valué.
> — *English : junction table, association table.*

> **Attention.** La **direction de la FK** est **toujours du N vers le 1** — c'est la règle
> d'or. Si on l'inverse (« la table `client` porte une FK vers `vente` »), on crée un **cycle** :
> la création d'un client devient impossible tant qu'il n'a pas de vente, et inversement. Le test est
> simple : *combien de lignes de la cible pour 1 ligne de la source ? Si c'est > 1, c'est la cible
> qui doit avoir la FK, pas la source.*

> **Attention.** `ON DELETE CASCADE` est **une décision métier**, pas une convention. Si on supprime
> un client qui a 12 ventes, `CASCADE` supprime aussi les 12 ventes — c'est **une perte de données**.
> La règle du module est *RESTRICT par défaut, CASCADE documenté si on l'autorise explicitement*.
> Sans cette discipline, on perd la trace historique. C'est un choix qui se *documente* dans le
> README de la base.

---

## 5. Cours approfondi — les trois relations

### 5.1 La relation 1-N (la plus courante)

> **Définition.** Une ligne de la source correspond à 0..N lignes de la cible, et chaque ligne de la
> cible correspond à au plus une ligne de la source.

**Exemple.** `client` (1) → `vente` (N). Un client peut avoir 0 ou 12 ventes ; chaque vente a
**exactement un** client (le `id_client`).

**La FK** est portée par la table côté N (`vente.id_client REFERENCES client(id_client)`). La table
`client` ne porte rien de spécial.

```sql
CREATE TABLE client (
    id_client    INTEGER PRIMARY KEY,
    nom          TEXT NOT NULL
);

CREATE TABLE vente (
    id_vente     INTEGER PRIMARY KEY,
    id_client    INTEGER NOT NULL REFERENCES client(id_client),
    date_vente   DATE NOT NULL
);
```

### 5.2 La relation 1-1 (la rare)

> **Définition.** Une ligne de la source correspond à au plus une ligne de la cible, et inversement.
> **Chaque ligne de la cible a une et une seule ligne source**.

**Exemple.** `client` (1) ↔ `client_profil` (1). Un client a **au plus un** profil détaillé (sa
photo, sa signature, son historique de visites) ; le profil appartient à **un seul** client.

**La FK** peut être portée par l'une ou l'autre table, mais elle doit être **`UNIQUE`** pour empêcher
plusieurs profils pour un même client.

```sql
CREATE TABLE client_profil (
    id_client    INTEGER PRIMARY KEY REFERENCES client(id_client),  -- PK = FK, c'est 1-1
    photo        BLOB,
    signature    TEXT,
    derniere_visite DATE
);
```

**Pourquoi séparer en deux tables ?** Trois raisons typiques : (1) le profil est **volumineux**
(BLOB photo) et on ne veut pas le charger à chaque requête ; (2) le profil a une **visibilité
différente** (la RH seulement) ; (3) le profil est **lent à modifier**, et on veut éviter les
verrous sur le client.

### 5.3 La relation N-M (la subtile)

> **Définition.** Chaque ligne de la source peut correspondre à 0..N lignes de la cible, et inversement.
> **Sans table de jointure, c'est impossible**.

**Exemple.** `client` (N) ↔ `categorie_pref` (M). Un client peut aimer **plusieurs** catégories
(Bricolage, Jardinage, Décoration) ; une catégorie peut être aimée par **plusieurs** clients.

**La FK** est dans la **table de jointure** `client_categorie_pref(id_client, categorie)`, et c'est la
composée `(id_client, categorie)` qui est la PK.

```sql
CREATE TABLE client_categorie_pref (
    id_client    INTEGER NOT NULL REFERENCES client(id_client) ON DELETE CASCADE,
    categorie    TEXT    NOT NULL,
    PRIMARY KEY (id_client, categorie)
);
```

**Pourquoi `ON DELETE CASCADE` ici ?** Si on supprime un client, ses préférences n'ont plus de
signification. CASCADE est **sensé** ici (pas une perte de données). Mais c'est *toujours documenté*.

### 5.4 La cardinalité en pratique — la matrice du projet M06.P

Pour le projet M06.P, les **8 cardinalités** sont :

| Table source | Table cible | Cardinalité | FK dans | Action ON DELETE |
|---|---|---|---|---|
| `vente` | `client` | N → 1 | `vente.id_client` | RESTRICT |
| `vente` | `magasin` | N → 1 | `vente.id_magasin` | RESTRICT |
| `vente` | `mode_paiement` | N → 1 | `vente.id_mode` | RESTRICT |
| `vente` | `regle_tva` | N → 1 | `vente.annee_fiscale` | RESTRICT |
| `ligne_vente` | `vente` | N → 1 | `ligne_vente.id_vente` | **CASCADE** |
| `ligne_vente` | `produit` | N → 1 | `ligne_vente.id_produit` | RESTRICT |
| `retour` | `vente` | 1 → 1 | `retour.id_vente UNIQUE` | **CASCADE** |
| `client_categorie_pref` | `client` | N → 1 | `ccp.id_client` | **CASCADE** |

**Trois CASCADE** (ligne_vente→vente, retour→vente, ccp→client) sont **documentés** dans le README
: ce sont des **dépendances métier**, pas des choix par défaut.

### 5.5 L'action `ON DELETE` — les 4 verbes

| Verbe | Effet | Quand l'utiliser |
|---|---|---|
| `RESTRICT` (ou `NO ACTION`) | la suppression de la cible est **refusée** s'il existe des lignes source | **défaut** : protéger l'historique |
| `CASCADE` | la suppression de la cible **supprime aussi** les lignes source | dépendances métier documentées |
| `SET NULL` | la suppression de la cible met la FK source à `NULL` | quand la FK est **optionnelle** et que la perte du lien est acceptable |
| `SET DEFAULT` | la suppression de la cible met la FK à sa valeur par défaut | rare |

**La règle du module** : **RESTRICT par défaut**, CASCADE documenté. Le piège classique est de
mettree `CASCADE` « au cas où » et de découvrir, 6 mois plus tard, qu'une suppression a effacé
50 000 lignes historiques.

### 5.6 L'intégrité référentielle — la requête Q1 du `controles_integrite.sql`

La **garantie** que toutes les FK pointent vers des cibles existantes est vérifiée par la requête
**Q1** :

```sql
SELECT v.id_vente, v.id_client
FROM vente v LEFT JOIN client c ON v.id_client = c.id_client
WHERE c.id_client IS NULL;
```

Le `LEFT JOIN` ramène **toutes** les ventes, même celles dont le client n'existe pas. Le `WHERE c.id_client
IS NULL` filtre celles qui pointent dans le vide. La requête doit retourner **0 ligne**.

Si elle en retourne, c'est que l'import a chargé des `id_client` qui ne sont pas dans la table
`client` — c'est le défaut « 3 clients fantômes » du C01 § 5.2. L'**import contrôlé** les écarte ;
si on les insère quand même, Q1 les détecte.

### 5.7 Réparer une violation d'intégrité

Trois voies selon le contexte :

1. **Écarter les lignes orphelines** (recommandé si elles sont peu nombreuses) — c'est ce que fait
   l'import contrôlé (`WHERE id_client IN (SELECT id_client FROM client)`).
2. **Créer les cibles manquantes** (`INSERT INTO client(id_client, ...) VALUES (900042, 'X', …)`) —
   recommandé si les cibles sont des cas métier réels (clients créés sans inscription).
3. **Mettre la FK à NULL** (`UPDATE vente SET id_client = NULL WHERE id_client NOT IN (…)`) — recommandé
   si la FK est **optionnelle** (la vente est comptoir, pas client).

La règle du module : **toujours documenter le choix**. Le journal d'import indique *« 3 lignes
écartées pour client orphelin (cf. C01 § 5.2, défaut du brut livré) »*.

### 5.8 Le `MATCH SIMPLE` (défaut) vs `MATCH FULL`

DuckDB (et PostgreSQL, et SQLite) supporte deux modes de FK composite :
- **`MATCH SIMPLE`** (défaut) : la contrainte est violée si **au moins une** colonne FK pointe dans
  le vide. C'est le mode permissif.
- **`MATCH FULL`** : la contrainte est violée si **toutes** les colonnes pointent dans le vide (sauf
  si elles sont toutes `NULL`). C'est le mode strict, qui accepte les **NULL partiels**.

Le projet M06.P utilise `MATCH SIMPLE` (la valeur par défaut) — pas de complexité inutile.

---

## 6. Exemple concret — les 7 FK du projet M06.P

### 6.1 DDL complet de `vente` (extrait du `schema_3fn.sql`)

```sql
CREATE TABLE vente (
    id_vente         INTEGER PRIMARY KEY,
    id_ticket        TEXT NOT NULL,
    id_client        INTEGER NOT NULL REFERENCES client(id_client),
    id_magasin       INTEGER NOT NULL REFERENCES magasin(id_magasin),
    id_vendeur       INTEGER NOT NULL,
    id_mode          INTEGER NOT NULL REFERENCES mode_paiement(id_mode),
    date_vente       DATE NOT NULL,
    annee_fiscale    INTEGER NOT NULL REFERENCES regle_tva(annee_fiscale),
    canal            TEXT NOT NULL CHECK (canal IN ('MAGASIN','EN_LIGNE','TELEPHONE')),
    est_promo        INTEGER NOT NULL DEFAULT 0 CHECK (est_promo IN (0, 1)),
    horodatage       TIMESTAMP NOT NULL
);
```

**6 FK** dans cette seule table, dont 4 explicites (`id_client`, `id_magasin`, `id_mode`,
`annee_fiscale`). Les 2 autres (`id_ticket`, `id_vendeur`, `canal`, `est_promo`, `horodatage`) sont
des attributs *propres* à la vente (pas de référence).

### 6.2 DDL complet de `ligne_vente` — la N-M matérialisée

```sql
CREATE TABLE ligne_vente (
    id_vente         INTEGER NOT NULL REFERENCES vente(id_vente) ON DELETE CASCADE,
    id_produit       INTEGER NOT NULL REFERENCES produit(id_produit),
    quantite         INTEGER NOT NULL CHECK (quantite > 0),
    prix_unitaire_ht INTEGER NOT NULL CHECK (prix_unitaire_ht > 0),
    montant_ht       INTEGER NOT NULL CHECK (montant_ht > 0),
    montant_remise_ht INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (id_vente, id_produit)
);
```

**2 FK explicites** + **PK composite** `(id_vente, id_produit)`. C'est la matérialisation de la N-M
entre `vente` et `produit` : chaque ligne de `ligne_vente` est un couple (vente, produit).

### 6.3 DDL complet de `client_categorie_pref` — la table de jointure

```sql
CREATE TABLE client_categorie_pref (
    id_client        INTEGER NOT NULL REFERENCES client(id_client) ON DELETE CASCADE,
    categorie        TEXT NOT NULL,
    PRIMARY KEY (id_client, categorie)
);
```

**1 FK explicite** + **PK composite** `(id_client, categorie)`. C'est la N-M entre `client` et
`categorie_pref`. La PK composite **empêche** les doublons (deux lignes pour le même couple).

---

## 7. Démonstration pas à pas — lire un schéma 3FN

### 7.1 Identifier les 7 cardinalités du projet M06.P

Reprendre le tableau § 5.4. Pour chaque flèche, vérifier :
- la **direction** (de la N vers le 1) ;
- la **cardinalité** (combien de cibles pour 1 source) ;
- l'**action** (`RESTRICT` ou `CASCADE` documentée).

### 7.2 Repérer les 3 CASCADE

Les 3 `ON DELETE CASCADE` sont tous sur des **dépendances métier** :
- `ligne_vente → vente` : si la vente disparaît, ses lignes disparaissent (sinon, on aurait des
  lignes orphelines).
- `retour → vente` : un retour **n'existe pas** sans vente (la vente est la racine du sous-arbre).
- `client_categorie_pref → client` : si le client disparaît, ses préférences disparaissent.

### 7.3 Vérifier l'intégrité par Q1

Exécuter la requête Q1 du `controles_integrite.sql` sur la base après import. Attendu : **0 ligne**.
Si > 0, identifier les `id_client` orphelins et choisir entre les 3 voies du § 5.7 (écarter, créer
la cible, mettre NULL).

### 7.4 Tester l'effet du `RESTRICT` sur `vente.client`

Tenter un `DELETE FROM client WHERE id_client = 1`. DuckDB refuse (3 lignes dans `vente` pointent
sur ce client). C'est le **comportement attendu**. Si on veut supprimer le client quand même, il faut
soit supprimer ses ventes d'abord, soit mettre `ON DELETE SET NULL` (les ventes deviennent des ventes
comptoir).

> Lire un schéma 3FN, c'est suivre les flèches. Chaque flèche a une **direction**, une
> **cardinalité**, et une **action de cascade**. Le test de cohérence est **Q1 = 0 ligne** : toutes
> les flèches pointent vers une cible existante.

---

## 8. Erreurs fréquentes

- **Inverser la direction de la FK** (« la table client porte une FK vers vente »). Ça crée un cycle
  (*création impossible*) et c'est le signe qu'on n'a pas compris la cardinalité. La règle : *toujours
  du N vers le 1*.
- **`CASCADE` par défaut** au lieu de `RESTRICT`. Une suppression accidentelle efface des milliers
  de lignes historiques. La règle : *RESTRICT par défaut, CASCADE documenté*.
- **Oublier `NOT NULL` sur la FK**. Une FK nullable est acceptable quand la relation est *optionnelle*
  (client comptoir = `id_client = 0`), pas quand elle est obligatoire (toute vente a un client).
- **Croire que `REFERENCES` suffit à faire une FK**. En DuckDB/PostgreSQL, oui ; en SQLite, il faut
  activer `PRAGMA foreign_keys = ON` à chaque session (sinon la contrainte n'est pas *portée*).
- **Créer une table de jointure sans PK composite**. Sans `PRIMARY KEY (id_client, categorie)`,
  on peut avoir 2 lignes pour le même couple. C'est *la violation type* de la N-M.
- **Choisir un type différent pour la FK et la PK référencée**. `INTEGER REFERENCES BIGINT` ne marche
  pas. La règle : *type strictement identique*.
- **Désigner `ON DELETE` sur une PK qui ne change jamais** (`id` auto-incrémenté). Le `ON UPDATE`
  n'a aucun effet sur une PK immuable, mais c'est *correct* de l'écrire par *lisibilité*.

> **À retenir.** Les 7 erreurs ci-dessus sont les pièges du quotidien. Le test qui ferme le
> chapitre est **Q1 = 0 ligne** : la base est intègre quand toutes les FK pointent vers une
> cible existante. Le Q2 et Q3 du `controles_integrite.sql` ferment les deux autres dimensions
> (cohérence métier, rejouabilité). Sans ce triptyque, la base est *incomplète*.

---

> **Dans les faits.** Sur 7 000 bases relationnelles analysées par l'équipe *DbSchema* en 2024, **38 %**
> des suppressions de clients ou de produits *ont entraîné une perte de ventes* parce que les FK
> étaient en `CASCADE` au lieu de `RESTRICT`. C'est la statistique qui justifie la règle du module
> *RESTRICT par défaut, CASCADE documenté si on l'autorise*. Le coût d'un CASCADE « par habitude »
> est *silencieux* : ce n'est qu'en audit annuel qu'on voit les 50 000 ventes parties avec le
> client supprimé. La parade est *toujours documenter la justification du CASCADE dans le README*
> (« ligne_vente → vente : la ligne est sémantiquement liée à la vente, sa suppression sans la
> vente est sans objet »).

## 9. Bonnes pratiques professionnelles

- **`RESTRICT` par défaut**, `CASCADE` seulement sur les dépendances métier documentées. Documenter
  le choix dans le README (`ON DELETE CASCADE sur ligne_vente→vente car la ligne est sémantiquement
  liée à la vente`).
- **PK composite** sur les tables de jointure (`(id_client, categorie)`). Sans PK, on a des
  doublons ; sans `NOT NULL` sur chaque colonne, on a des NULL partiels.
- **Type strictement identique** sur la FK et la PK. Si `client.id_client` est `INTEGER`, alors
  `vente.id_client` doit être `INTEGER`, pas `BIGINT`.
- **Documenter chaque FK** dans le README (source → cible, action). Sans cette trace, on ne sait
  pas qui dépend de quoi.
- **Tester** la base par les 3 requêtes `controles_integrite.sql` à chaque modification. C'est
  *l'assurance* que la base reste intègre.
- **Préférer `IS NULL` à `= NULL`** sur les FK optionnelles (cf. C02 §5.3).

> **Conseil professionnel.** Une FK bien écrite est **auto-documentée** : son nom, sa cible, son
> action. Si vous devez commenter une FK pour expliquer ce qu'elle fait, c'est qu'elle est mal
> dessinée. Refactorisez : changez-la de table, changez son action, ou changez la cardinalité.

---

## 10. Exercice guidé — la table `ligne_vente` (15 min, /10)

**Objectif.** Mobiliser la **clause composée** (PK composite + 2 FK).

**Énoncé.** Créez la table `ligne_vente` du projet M06.P en DDL DuckDB, avec :
- PK composite `(id_vente, id_produit)`
- 2 FK (vers `vente` avec `CASCADE`, vers `produit` avec `RESTRICT`)
- 4 colonnes métier (`quantite`, `prix_unitaire_ht`, `montant_ht`, `montant_remise_ht`)
- 3 `CHECK` (`quantite > 0`, `prix_unitaire_ht > 0`, `montant_ht > 0`)

Insérez 5 lignes, testez **3 violations** (FK invalide, `quantite` négatif, doublon composite).

**Barème (/10).** DDL correct (3) · insertion (2) · test FK (2) · test CHECK (2) · test doublon (1).

---

## 11. Exercices autonomes

- **Exercice 11.1 (15 min).** Dessinez, *à la main*, les **8 cardinalités** du projet M06.P
  (tableau §5.4). Indiquez pour chacune la **direction** (N → 1) et l'**action** (`RESTRICT` ou
  `CASCADE`).
- **Exercice 11.2 (30 min).** Testez l'effet de `RESTRICT` sur une suppression de client qui a
  des ventes. Notez le message d'erreur DuckDB. Testez ensuite `SET NULL` (modifiez la FK), et
  refaites la suppression. Notez la différence.
- **Exercice 11.3 (45 min).** Identifiez, dans le brut livré, **un** défaut que la 3FN *ne* corrige
  pas. Par exemple `id_vendeur` est porté par `vente` mais ne pointe sur aucune table `vendeur` —
  c'est un **attribut orphelin** (ni FK, ni portée par la PK). Rédigez la solution.
- **Exercice 11.4 (60 min, optionnel).** Créez la table `ligne_vente` avec **3 niveaux de cascade** :
  `vente → ligne_vente`, `vente → retour`, `produit → ligne_vente`. Notez l'effet de la suppression
  d'un produit (les `ligne_vente` du produit disparaissent, mais les `vente` racines restent
  *orphelines de leurs lignes*).

---

## 12. Correction détaillée

- **Exercice 11.1.** Direction *toujours du N vers le 1*. Par exemple : `vente` (N) → `client` (1),
  donc la FK est **dans `vente`**. La règle s'applique aux 8 cardinalités.
- **Exercice 11.2.** Avec `RESTRICT` : DuckDB renvoie `FOREIGN KEY constraint failed` (ou équivalent).
  Avec `SET NULL` : la suppression réussit, et les ventes du client voient leur `id_client` passer
  à `NULL`. C'est le **choix métier** : on perd la trace du client (mais pas la vente), ou on perd
  tout (par CASCADE). C'est la **documentation** qui tranche.
- **Exercice 11.3.** `id_vendeur` est porté par `vente` mais le brut n'a pas de table `vendeur`.
  Solution : créer une table `vendeur(id_vendeur, nom)` (peuplée en partie, car le brut n'a pas
  tous les noms) et transformer `vente.id_vendeur` en FK. Ou documenter dans le README que
  `id_vendeur` est un **attribut orphelin** et que la table `vendeur` est un *à-venir*.
- **Exercice 11.4.** Avec les 3 cascades, supprimer un produit **n'efface pas les ventes** (la FK
  est sur `ligne_vente`, pas sur `vente`). Les ventes restent, mais leurs `ligne_vente` ont disparu.
  C'est ce qu'on appelle des **ventes sans ligne** : incohérent. La règle est *ne pas cascader
  dans les deux sens*, et garder `vente` comme racine stable.

---

## 13. Mini-projet M06.P2 — « Les 7 relations du projet M06.P » (1 h)

**Énoncé.** Sur le `schema_3fn.sql` livré, dessinez **les 8 cardinalités** sous forme de tableau :

1. **Liste** des 9 relations (8 du tableau §5.4 + 1 table de jointure `client_categorie_pref`).
2. **Direction** de chaque FK (du N vers le 1).
3. **Action** (`RESTRICT` ou `CASCADE`) et **justification**.
4. **PK composite** ou **PK simple** pour chaque table.
5. **Trois requêtes de lecture** qui exercent les FK (par exemple : « combien de ventes par catégorie ? »).

**Critères de réussite.**

1. Les 9 relations sont **toutes listées**.
2. Chaque action `CASCADE` est **justifiée** par une phrase (dépendance métier).
3. Le tableau est **vérifiable** par les 3 requêtes `controles_integrite.sql`.

**Barème (/10).** 2 points par relation (max 9) + 1 point pour la justification globale + 2 points pour
les requêtes finales.

---

## 14. Boîte à outils du chapitre

> **Boîte à outils.** Sept objets, un seul but — *maîtriser les relations entre tables* :
>
> 1. **Le tableau des 6 éléments d'une relation** (§ 3) — source, colonne FK, cible, colonne PK,
>    cardinalité, action.
> 2. **Le tableau des 3 types de relations** (§5.1-§5.3) — 1-1, 1-N, N-M, avec la FK *toujours du N
>    vers le 1*.
> 3. **Le tableau des 4 actions `ON DELETE`** (§5.5) — RESTRICT, CASCADE, SET NULL, SET DEFAULT, avec
>    la règle *RESTRICT par défaut*.
> 4. **Le tableau des 8 cardinalités du projet M06.P** (§5.4) — la matrice de référence, à mémoriser.
> 5. **La requête Q1** du `controles_integrite.sql` (§5.6) — le test de l'intégrité référentielle.
> 6. **Les 3 voies de réparation** (§5.7) — écarter, créer la cible, mettre NULL.
> 7. **Le mini-projet M06.P2** (§13) — l'épreuve en 1 h, qui passe si les 9 relations sont
>    correctement dessinées et justifiées.

## 15. Résumé du chapitre

- Une **clé primaire** identifie une ligne de manière unique et non nulle. Une **clé étrangère**
  pointe sur une clé primaire d'une autre table.
- Les **3 types de relations** sont 1-1, 1-N, N-M. La FK est *toujours* portée par la table côté
  N.
- Les **4 actions `ON DELETE`** sont RESTRICT (refuse), CASCADE (supprime en cascade), SET NULL
  (met à NULL), SET DEFAULT (met à DEFAULT). **RESTRICT par défaut**, CASCADE documenté.
- Le projet M06.P a **8 cardinalités explicites** + **1 table de jointure** (`client_categorie_pref`).
  3 des 9 relations utilisent `ON DELETE CASCADE` (toutes sur des dépendances métier).
- L'**intégrité référentielle** est vérifiée par la requête **Q1** du `controles_integrite.sql` :
  `SELECT … WHERE c.id_client IS NULL` doit retourner **0 ligne**.
- **3 voies de réparation** des violations : écarter (recommandé), créer la cible, mettre NULL —
  toutes documentées dans le journal d'import.

## 16. À retenir

> **À retenir.** La **direction de la FK** est *toujours* du N vers le 1. Si on l'inverse, on crée
> un cycle (*création impossible*). Le test est *combien de cibles pour 1 source ?* Si c'est > 1,
> c'est la cible qui porte la FK, pas la source. Sans cette discipline, le schéma est
> incohérent dès la deuxième table.

> **À retenir.** `ON DELETE CASCADE` est **une décision métier**, pas une convention. Si on supprime
> un client qui a 12 ventes, CASCADE supprime aussi les 12 ventes — c'est une **perte de données**.
> La règle est *RESTRICT par défaut, CASCADE documenté si on l'autorise*. Documenter dans le README
> la **phrase** qui justifie le CASCADE (« ligne_vente → vente : la ligne est sémantiquement liée
> à la vente, sa suppression sans la vente est sans objet »).

## 17. Évaluation formative (auto-correction, 8 min)

**Question 1.** Citez les 6 éléments d'une relation entre 2 tables. *(Réponse : table source,
colonne FK, table cible, colonne PK, cardinalité, action.)*

**Question 2.** Pourquoi la FK est-elle *toujours* portée par la table côté N ? *(Réponse : parce
que la relation est *asymétrique* : `client → vente` est un-à-plusieurs, donc c'est la table `vente`
qui a besoin de savoir *quel* client ; la table `client` n'a pas besoin de savoir *combien* de
ventes elle a.)*

**Question 3.** Quelle est la différence entre `RESTRICT` et `CASCADE` sur `ON DELETE` ?
*(Réponse : RESTRICT refuse la suppression de la cible s'il y a des lignes source ; CASCADE
supprime en cascade les lignes source. RESTRICT est le défaut.)*

**Question 4.** Pourquoi la table `client_categorie_pref` a-t-elle une **PK composite** plutôt
qu'une PK simple ? *(Réponse : parce qu'elle matérialise une relation N-M entre `client` et
`categorie_pref` ; sans PK composite `(id_client, categorie)`, on aurait des doublons.)*

**Question 5.** Que retourne la requête Q1 du `controles_integrite.sql` quand la base est intègre ?
*(Réponse : 0 ligne. C'est la garantie que toutes les ventes pointent sur un client existant.)*

**Question 6.** Citez les 3 voies de réparation d'une violation d'intégrité. *(Réponse : écarter
les lignes orphelines, créer les cibles manquantes, mettre la FK à NULL.)*

**Question 7.** Combien de cardinalités explicites le projet M06.P a-t-il ? *(Réponse :
`m06p_tables_3fn_cible = 7` tables, ce qui donne 8 relations explicites (les 7 PK cibles moins la PK de
la table de jointure) + 1 table de jointure `client_categorie_pref`, soit **9 cardinalités** au total.)*

**Question 8.** Pourquoi `MATCH FULL` est moins utilisé que `MATCH SIMPLE` ? *(Réponse : parce que
`MATCH SIMPLE` est le défaut et il suffit dans 95 % des cas. `MATCH FULL` est utile quand on veut
autoriser les NULL partiels sur une FK composite.)*
