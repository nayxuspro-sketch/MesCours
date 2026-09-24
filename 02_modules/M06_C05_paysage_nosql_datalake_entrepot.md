# Module M06.C05 — Les autres mondes : NoSQL (document, clé-valeur, graphe, colonnes), datalake, entrepôt, lac

**Outils : aucun outil à installer. Vocabulaire d'entretien. Durée indicative : 5 h. Niveau : N2.
Prérequis : M06.C01, M06.C02, M06.C03.**

> **L'idée du chapitre.** Les quatre chapitres précédents ont installé **le SGBD relationnel** (DuckDB,
> SQLite, PostgreSQL). Le C05 *regarde au-delà* : ce qui vient *autour*, *à côté* et *au-dessus* du
> relationnel. Le C05 n'est pas un détour : c'est l'**ouverture professionnelle** du module. Un analyste
> qui ne connaît que les SGBD relationnels a une *vision tronquée* du paysage. Le module M06 lui
> donne les **5 mots d'entretien** (NoSQL, datalake, entrepôt, lac, lakehouse) et les **5 cas** où un
> autre modèle est meilleur. Le verdict du C05 est *« l'analyste sait où il est, et où il n'est pas »*.

> **Base de travail — pas de fichier livré pour ce chapitre.** Le C05 est **purement descriptif**.
> Il n'enseigne aucun outil à installer (NoSQL n'est pas dans l'atelier), aucun pipeline à exécuter,
> aucune table à vérifier. C'est le chapitre *qui prépare l'entretien d'embauche* et *le vocabulaire
> transversal* du data engineer. Le mini-projet M06.P4 est le seul livrable « concret » : un
> glossaire de 200 mots qui couvre les 5 mots d'entretien.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

- **définir** NoSQL, et distinguer ses **4 familles** (document, clé-valeur, graphe, colonnes) ;
- **expliquer** pourquoi NoSQL ne *remplace pas* le relationnel mais *le complète* ;
- **situer** datamart, datawarehouse (entrepôt), datalake (lac) et lakehouse dans le paysage ;
- **expliquer** les **5 mots d'entretien** : sharding, réplication, CAP, ETL vs ELT, ACID ;
- **reconnaître** le bon choix pour un cas d'usage (transactionnel vs analytique, structuré vs
  non-structuré) ;
- **rédiger** un glossaire de 200 mots sur les 5 mots d'entretien (mini-projet M06.P4).

## 2. Pourquoi cette notion est importante

- Le module M06 a installé **le relationnel** sur **50 % du paysage** (cf. C01 § 5.6). L'autre moitié
  est **NoSQL et Big Data**. Le C05 ferme la porte en montrant ce qui *existe à côté* — sans
  l'enseigner en profondeur, parce que c'est l'objet de modules ultérieurs (M11 « SQL avancé »,
  M13 « Modélisation », M14 « Power BI »).
- **NoSQL** est *un raccourci* pour *« Not only SQL »*. Ce n'est pas *« No SQL »* (pas de SQL) ; c'est
  *« Pas seulement SQL »*. Le C05 enseigne **les 4 familles** (document, clé-valeur, graphe,
  colonnes) et **les cas d'usage** de chacune.
- Le **datalake** et le **datawarehouse** (entrepôt) sont des concepts *complémentaires*, pas
  opposés. Le datawarehouse stocke des **données structurées** (et validées) ; le datalake stocke
  **tout** (CSV, JSON, images, logs). Le **lakehouse** combine les deux. C'est l'architecture
  *moderne*.
- Les **5 mots d'entretien** sont ce qui distingue un *junior* (qui les a lus) d'un *senior* (qui
  les a *vécus*). Le C05 les explique en **moins de 200 mots** par mot, pour que l'analyste junior
  puisse répondre en entretien sans bluff.
- **Le paysage** est ce qui permet de *situer* un projet : « ce projet est *transactionnel*,
  *mono-utilisateur*, *structuré* → SQLite » ; « ce projet est *transactionnel*,
  *multi-utilisateurs*, *gouvernance forte* → PostgreSQL » ; « ce projet est *non-structuré*,
  *multi-utilisateurs*, *documente* → MongoDB ». C'est la **compétence d'orientation** du
  professionnel.

## 3. Explication simple — la carte du monde des données

Le **paysage** se lit en **4 axes** :

1. **Structure** — les données sont-elles **typées** (SGBDR), **semi-structurées** (JSON, MongoDB),
   ou **non-structurées** (texte brut, images) ?
2. **Fréquence** — la base est *transactionnelle* (caisse, bancaire) ou *analytique* (rapports,
   agrégats) ?
3. **Utilisateurs** — *1* (analyste solo), *quelques-uns* (équipe), *milliers* (grand public) ?
4. **Gouvernance** — *locale* (un fichier), *centralisée* (schéma SQL), *fédérée* (multi-sites) ?

Le **résumé en une phrase** : *« Un bon choix d'outil dépend de **où** on est sur ces 4 axes. »*

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **NoSQL** — *Not only SQL* | la famille des bases **non-relationnelles** : document, clé-valeur, graphe, colonnes larges. | confondre avec « pas de SQL » : NoSQL *complète* le relationnel, ne le remplace pas. |
| **base document** — *document store* | la base qui stocke des **JSON-like** (MongoDB, CouchDB). Chaque document est typé mais sans schéma imposé. | confondre avec « base non structurée » : MongoDB a des schémas *implicites* (validés au niveau applicatif). |
| **base clé-valeur** — *key-value store* | la base qui stocke des paires `clé → valeur` (Redis, DynamoDB). Ultra-rapide en lecture/écriture simple. | confondre avec « pas de clé » : la **clé** est l'identité, la *valeur* est opaque. |
| **base graphe** — *graph database* | la base qui stocke des **nœuds + arêtes** (Neo4j, JanusGraph). Optimisée pour les parcours de graphe. | confondre avec « table de jointure » : un graphe est une **structure** dédiée, pas une astuce relationnelle. |
| **base colonnes** — *wide-column store* | la base qui stocke des colonnes *par famille* (Cassandra, Bigtable). Optimisée pour les lectures massives en colonne. | confondre avec « colonne SQL » : c'est une **organisation physique** différente, pas un type logique. |
| **MongoDB** — *MongoDB* | le SGBD **document** le plus populaire, JSON natif, schéma flexible, écrit en C++. Utilisé par 50 % des startups en 2024. | croire qu'il remplace PostgreSQL : MongoDB a des **transactions** depuis 4.0 (2018), mais reste *plus lent* sur les jointures. |
| **Redis** — *Redis* | le SGBD **clé-valeur** ultra-rapide, mémoire RAM, persistance sur disque en option. Utilisé pour le cache, les files, les compteurs. | confondre avec « base principale » : Redis est un *cache*, pas une base canonique. |
| **Neo4j** — *Neo4j* | le SGBD **graphe** le plus populaire, écrit en Java, requête en *Cypher* (`MATCH (a)-[:KNOWS]->(b) RETURN b.name`). | croire qu'il est réservé aux réseaux sociaux : Neo4j sert aussi pour la *traçabilité alimentaire*, les *graphes de dépendance*, etc. |
| **Cassandra** — *Apache Cassandra* | le SGBD **colonnes larges** distribué, écrit en Java, optimisé pour l'écriture massive. Utilisé par Netflix, Apple, Uber. | confondre avec « colonne » : Cassandra organise les données par famille de colonnes, *pas* par colonnes SQL. |
| **NewSQL** — *NewSQL* | la famille des SGBD **relationnels distribués** (CockroachDB, Spanner, YugabyteDB). Le meilleur des deux mondes : SQL + scalable horizontalement. | confondre avec « PostgreSQL distribué » : NewSQL ajoute la *distribution* (sharding automatique) sans abandonner le SQL. |
| **datawarehouse** — *data warehouse, DWH* | l'**entrepôt** de données : un SGBD analytique (SQL Server, Snowflake, BigQuery, Redshift) où les rapports sont calculés. | confondre avec « base de production » : le DWH est *séparé* de la base transactionnelle. |
| **datalake** — *data lake, lac* | le **lac** de données : un stockage brut (S3, HDFS) qui contient des CSV, JSON, Parquet, images, logs, *sans validation préalable*. | confondre avec « SGBD » : un lac *ne valide pas*, c'est juste un gros disque. |
| **lakehouse** — *lakehouse* | l'**architecture hybride** : un lac + un entrepôt, où les données sont stockées brutes *et* validées en SQL via `Delta Lake` ou `Apache Iceberg`. | croire qu'il faut choisir : lakehouse est *les deux* à la fois. |
| **ETL** — *Extract, Transform, Load* | le pipeline classique : on **transforme** les données *avant* de les charger (par exemple, dans un SGBDR). | confondre avec « copie de fichiers » : ETL a une *logique* de nettoyage. |
| **ELT** — *Extract, Load, Transform* | le pipeline moderne : on **charge** d'abord (dans le lac), puis on **transforme** dans le SGBD analytique. | croire qu'il faut choisir : ELT est le standard *moderne* (datalake → entrepôt). |
| **sharding** — *sharding, partitionnement horizontal* | la répartition des données sur **plusieurs machines** (ex. : les clients A-M sur le serveur 1, N-Z sur le serveur 2). C'est la *scalabilité horizontale* des SGBD distribués. | confondre avec « partition verticale » : sharding = *par lignes*, partition verticale = *par colonnes*. |
| **réplication** — *replication* | la **copie** asynchrone (ou synchrone) des données sur plusieurs machines. *Maître-esclave* (un maître, plusieurs copies) ou *multi-maître* (plusieurs maîtres qui se synchronisent). | confondre avec « sauvegarde » : la réplication est *temps réel*, la sauvegarde est *périodique*. |
| **CAP** — *CAP theorem, Brewer's theorem* | l'impossibilité d'avoir simultanément **Cohérence**, **Disponibilité**, **Tolérance au partitionnement** dans un SGBD distribué. Il faut en choisir 2 sur 3. | croire qu'on peut tout avoir : c'est mathématiquement impossible, le théorème de Brewer est *prouvé*. |
| **ACID** — *Atomicity, Consistency, Isolation, Durability* | les **4 propriétés** d'une transaction SGBD (cf. C01 §4 : *atomique, cohérent, isolé, durable*). Tous les SGBDR respectent ACID. | confondre avec BASE (cf. ci-dessous) : NoSQL « sacrifie » souvent ACID pour la disponibilité (BASE). |
| **BASE** — *Basically Available, Soft state, Eventually consistent* | l'**alternative** à ACID pour les SGBD distribués NoSQL : on accepte une cohérence *différée* au profit de la disponibilité. | confondre avec « pas de cohérence » : BASE est *cohérent à terme* (les lectures lointaines convergent), pas « n'importe quoi ». |

> **Définition.** Le **NoSQL** (*Not only SQL*) est la famille des bases **non-relationnelles**,
> optimisées pour des cas où le relationnel est maladroit : documents semi-structurés (MongoDB), paires
> clé-valeur ultra-rapides (Redis), graphes de relations (Neo4j), colonnes larges distribuées
> (Cassandra). NoSQL ne *remplace pas* le relationnel ; il le *complète*. La règle du module est
> *« choisir NoSQL quand le relationnel est inadapté, pas par mode. »*
> — *English : Not only SQL.*

> **Définition.** Le **datawarehouse** (entrepôt) est un SGBD **analytique** où les données
> *validées* sont stockées pour les rapports (tableaux de bord, SQL analytique, OLAP). Le **datalake**
> (lac) est un stockage *brut* où les données sont conservées *telles quelles* (CSV, JSON, images,
> logs). Le **lakehouse** combine les deux : les données sont stockées brutes *et* validées en SQL
> via des couches comme Delta Lake ou Apache Iceberg. La règle du module est *DWH pour les
> rapports, lac pour l'exploration, lakehouse pour les deux*.
> — *English : data warehouse, data lake, lakehouse.*

> **Définition.** Le **théorème CAP** (Brewer, 2000) énonce qu'un SGBD **distribué** (sur plusieurs
> machines) ne peut pas avoir simultanément **Cohérence**, **Disponibilité**, **Tolérance au
> partitionnement**. Le choix se fait entre **CP** (cohérence + partitionnement, e.g. HBase) ou
> **AP** (disponibilité + partitionnement, e.g. Cassandra) ou **CA** (cohérence + disponibilité,
> impossible en distribué — c'est l'apanage du SGBD centralisé). Le module le cite pour que
> l'analyste sache *pourquoi* NoSQL est différemment consistant.
> — *English : CAP theorem.*

> **Attention.** **NoSQL ne supprime pas le schéma** : il le rend *implicite*. Sur MongoDB, le
> document `{nom: "Alice", age: 30}` est valide *parce que l'application le crée ainsi*. Si on change
> le code applicatif, les anciens documents restent dans l'ancien format. La **discipline** est de
> *documenter le schéma attendu dans l'application*, pas dans la base. C'est l'inverse de la
> discipline relationnelle, où la base *porte* le schéma (`CREATE TABLE`). Pour un junior,
> c'est une *surprise* ; pour un senior, c'est une *responsabilité*.

> **Attention.** Le **sharding** est une décision **irréversible**. Si on commence avec un
> sharding par `id_client`, on ne peut pas revenir en arrière sans **réindexer toute la base**.
> Le piège classique est de *sharder trop tôt* (avant d'avoir 100 millions de lignes, le SGBD
> centralisé tient). La règle du module est *sharder quand le SGBD centralisé ne tient plus* — pas
> avant. Sans cette discipline, on prend une *décision de 6 mois* qu'on regrettera.

---

## 5. Cours approfondi — les 4 familles NoSQL

### 5.1 Document store (MongoDB, CouchDB)

**Cas d'usage.** Données **semi-structurées** (JSON, BSON, hiérarchiques) où le **schéma change
souvent**. Exemples : profils utilisateurs (chacun avec des champs différents), catalogues produits
(attributs variables), IoT (capteurs divers).

**Exemple MongoDB.**

```javascript
db.users.insertOne({
    nom: "Alice",
    age: 30,
    adresses: [
        {ville: "Koudougou", pays: "BF"},
        {ville: "Bobo", pays: "BF"}
    ],
    preferences: {langues: ["fr", "moore"], fidelite: "OR"}
});
```

Le **schéma** est *implicite* dans la structure du document ; c'est le code applicatif qui le valide.

### 5.2 Clé-valeur (Redis, DynamoDB)

**Cas d'usage.** Cache, sessions, files d'attente, compteurs. La rapidité en lecture/écriture simple
prime. Exemples : panier d'achat (id_session → liste de produits), cache HTTP (URL → réponse),
leaderboard (id_joueur → score).

**Exemple Redis.**

```bash
SET user:1000 "Alice"           # clé → valeur
GET user:1000                    # "Alice"
INCR compteur:visites:home       # +1 atomique
HSET user:1000 nom "Alice" age 30  # hash (sous-clés)
```

**Redis** vit en mémoire RAM : c'est la base la plus rapide, et c'est aussi la plus *volatile*
(les données sont perdues au redémarrage, sauf configuration `appendonly`).

### 5.3 Graphe (Neo4j, JanusGraph)

**Cas d'usage.** Réseaux sociaux, dépendances logicielles, traçabilité alimentaire, graphes de
connaissances, lutte anti-fraude. La **structure de graphe** (nœuds + arêtes) est *native* : une
requête qui parcourt 3 niveaux est *directe* (pas de 3 jointures).

**Exemple Neo4j (Cypher).**

```cypher
MATCH (a:Person)-[:KNOWS]->(b)-[:KNOWS]->(c)
WHERE a.name = 'Alice'
RETURN c.name, count(*) AS amis_de_amis
```

Le **Cypher** est déclaratif : on décrit le **parcours**, on ne code pas l'algorithme. C'est
*10 × plus court* qu'une jointure SQL équivalente.

### 5.4 Colonnes larges (Cassandra, Bigtable, HBase)

**Cas d'usage.** Écriture massive en continu (capteurs IoT, logs de serveurs, historique de prix). Le
**modèle** est *colonnes par famille* : on regroupe les colonnes par « famille » (par exemple, `info_personnelles`, `metriques`, `preferences`) et on charge par famille.

**Exemple Cassandra (CQL).**

```sql
CREATE TABLE users (
    id_user    UUID PRIMARY KEY,
    nom        TEXT,
    age        INT,
    ville      TEXT
) WITH COMPACT STORAGE;
```

Cassandra est optimisée pour **l'écriture** ; la lecture par clé est rapide, mais le scan par
colonne est moins efficace que sur un SGBD analytique.

---

## 6. Cours approfondi — datamart, datawarehouse, datalake, lakehouse

### 6.1 Le datawarehouse (l'entrepôt, ~30 ans d'histoire)

- **Origine** : années 1990 (Bill Inmon, Ralph Kimball).
- **Concept** : un SGBD analytique où les données sont **validées, agrégées, et orientées sujet**.
- **Outils** : Teradata, Oracle Exadata, SQL Server, Snowflake, BigQuery, Redshift.
- **Cas d'usage** : rapports consolidés (CA par mois par rayon), OLAP, indicateurs de
  performance — *KPI (Key Performance Indicator)*.

### 6.2 Le datamart (le sous-entrepôt)

- **Concept** : un sous-ensemble du DWH, orienté **un sujet métier** (finance, marketing, RH).
- **Avantage** : plus simple, plus rapide à mettre en place.
- **Inconvénient** : risque de silos (chaque datamart a sa propre logique).

### 6.3 Le datalake (le lac, ~10 ans d'histoire)

- **Origine** : 2010 (James Dixon, Pentaho).
- **Concept** : un stockage **brut** (S3, HDFS, blob Azure) où les CSV, JSON, Parquet, images,
  logs sont conservés *telles quelles*, sans validation préalable.
- **Avantage** : on peut tout stocker (logs de 5 ans, archives, médias).
- **Inconvénient** : c'est un *marécage* (swamp) si on ne le gère pas. La phrase consacrée est
  *« datalake »* → *« data swamp »* en 6 mois.

### 6.4 Le lakehouse (la combinaison ~5 ans)

- **Origine** : 2020 (Databricks Delta Lake, Apache Iceberg, Apache Hudi).
- **Concept** : un lac avec une **couche de validation SQL**. Les données sont stockées brutes,
  *mais* les requêtes SQL passent par une couche qui impose un *schéma* (sans modifier le fichier
  d'origine).
- **Outils** : Databricks, Snowflake, BigQuery, DuckDB (sur Parquet natif).
- **Avantage** : le meilleur des deux mondes.

---

## 7. Cours approfondi — les 5 mots d'entretien

### 7.1 Sharding (partitionnement horizontal)

Le **sharding** répartit les lignes d'une table sur **plusieurs machines**. Chaque machine (nœud)
porte un **sous-ensemble** des lignes. Exemple : 1 milliard de clients, répartis en 10 nœuds de
100 millions chacun. Le SGBD route la requête vers le bon nœud en fonction de la **clé de
sharding** (souvent `id_user % 10`).

**Prérequis** : 100 millions de lignes minimum (en dessous, le SGBD centralisé tient).

### 7.2 Réplication (copie asynchrone)

La **réplication** copie les données d'une machine **maître** vers une ou plusieurs machines
**esclaves**. C'est l'inverse du sharding : on copie *toute* la base, pas une partie. C'est le
mécanisme de la **haute disponibilité** : si le maître tombe, un esclave prend le relais.

**Modes** : *synchrone* (la transaction attend que l'esclave confirme) ou *asynchrone* (la
transaction commit sur le maître, l'esclave copie en arrière-plan, avec un délai).

### 7.3 Théorème CAP (Brewer)

Un SGBD **distribué** ne peut pas avoir simultanément :
- **Cohérence** (tous les nœuds voient la même valeur au même moment) ;
- **Disponibilité** (chaque requête reçoit une réponse, succès ou échec) ;
- **Tolérance au partitionnement** (le système continue à fonctionner même si un nœud est isolé).

Le choix est *forcé* : un SGBD distribué fait 2 sur 3. **CP** (cohérence + partition, e.g. HBase)
ou **AP** (disponibilité + partition, e.g. Cassandra) ou **CA** (impossible en distribué — c'est
le SGBD centralisé classique).

### 7.4 ACID vs BASE (modèle transactionnel)

> **Définition.** Le **modèle ACID** (Atomicity, Consistency, Isolation, Durability — atomique,
> cohérent, isolé, durable) est le contrat des transactions SGBDR : chaque transaction est garantie
> *atomique* (tout ou rien), *cohérente* (la base reste valide), *isolée* (les autres transactions
> ne voient pas l'état intermédiaire), *durable* (la modification survit à un crash). Le modèle
> **BASE** (Basically Available, Soft state, Eventually consistent) est le modèle alternatif pour
> les SGBD distribués NoSQL : on accepte une cohérence *différée* au profit de la disponibilité.
> ACID pour le bancaire, BASE pour l'IoT ou le cache. C'est le choix du C05.

**ACID** : Atomicité, Cohérence, Isolation, Durabilité. C'est le modèle **relationnel** : chaque
transaction est garantie isolée des autres et durable.

**BASE** : Basically Available, Soft state, Eventually consistent. C'est le modèle **NoSQL
distribué** : on accepte une cohérence *différée* au profit de la disponibilité.

| Propriété | ACID | BASE |
|---|---|---|
| Cohérence | immédiate | à terme |
| Disponibilité | réduite (verrous) | élevée |
| Cas d'usage | bancaire, transactionnel | IoT, cache, analytique |

### 7.5 ETL vs ELT

**ETL** (Extract, Transform, Load) — pipeline *classique*. On extrait, on transforme (dans un outil
dédié comme Informatica), puis on charge dans l'entrepôt. La transformation est **hors** du SGBD
analytique.

**ELT** (Extract, Load, Transform) — pipeline *moderne*. On extrait, on charge brut (dans le lac),
puis on transforme dans le SGBD analytique (BigQuery, Snowflake). Le SGBD analytique **est** la
machine de transformation.

---

## 8. Exemple concret — le verdict du paysage

Pour le projet M06.P « La base de la quincaillerie », où se trouve la base ?

| Axe | Valeur | Outil adapté |
|---|---|---|
| Structure | typée (3FN, 7 tables) | **SGBDR** (DuckDB / SQLite / PostgreSQL) |
| Fréquence | analytique (rapports hebdo) | SGBDR analytique (DWH) si volumétrie |
| Utilisateurs | 1 analyste (Koudougou) | **DuckDB** intégré |
| Gouvernance | locale (un fichier) | DuckDB + `EXPORT DATABASE` quotidien |

**Le verdict** : DuckDB est le bon outil. Le projet M06.P est *100 % relationnel*. NoSQL et
Big Data sont *hors de ce projet*, mais restent dans **l'horizon professionnel** de l'analyste
qui veut grandir.

---

## 9. Démonstration pas à pas — les 5 mots d'entretien

### 9.1 Préparer une réponse à *« C'est quoi le sharding ? »*

« Le sharding est la répartition horizontale des lignes d'une table sur plusieurs machines. C'est
la scalabilité des SGBD qui grossissent au-delà du téraoctet. Le piège est de *sharder trop tôt*
: en dessous de 100 millions de lignes, le SGBD centralisé tient, et sharding est irréversible. »
(58 mots)

### 9.2 Préparer une réponse à *« ACID ou BASE ? »*

« ACID pour les transactions bancaires (chaque virement doit être garanti). BASE pour les
capteurs IoT (on préfère perdre 1 % des lectures plutôt que bloquer le capteur). Le théorème CAP
nous dit qu'on ne peut pas tout avoir en distribué. » (49 mots)

### 9.3 Préparer une réponse à *« DWH ou datalake ? »*

« Les deux, en lakehouse. Le datalake stocke le brut ; le DWH stocke le validé ; le lakehouse
garde les deux couches et permet des requêtes SQL sur le brut via Parquet. C'est l'architecture
moderne. » (39 mots)

Les 5 mots d'entretien se préparent en **moins de 60 mots chacun**. C'est la règle du
*« dire peu, dire juste »* (cf. M03.C01 § 8 sur la communication).

---

## 10. Erreurs fréquentes

- **Croire que NoSQL remplace SQL** : c'est l'erreur de compréhension n°1. NoSQL *complète* le
  relationnel, ne le remplace pas. La règle est *SQL pour 80 % des cas, NoSQL pour 20 %*.
- **Sharder trop tôt** : la décision est *irréversible*. La règle est *sharder quand le SGBD
  centralisé ne tient plus* (1 To+).
- **Confondre datalake et DWH** : le lac stocke du brut, l'entrepôt stocke du validé. Le
  lakehouse combine les deux.
- **Croire que `MongoDB` est plus rapide que PostgreSQL** : faux dans 80 % des cas. MongoDB est
  rapide *pour les documents JSON* ; sur les jointures classiques, PostgreSQL gagne.
- **Oublier ACID dans une transaction bancaire** : c'est l'erreur *classique*. La règle est
  *toujours ACID pour les transactions critiques* (banque, paie, facturation).
- **Confondre réplication et sauvegarde** : la réplication est *temps réel*, la sauvegarde est
  *périodique*. Les deux sont complémentaires (la réplique peut tomber en panne au même moment que
  le maître, la sauvegarde non).
- **Croire que « BASE = pas de cohérence »** : c'est faux. BASE = *cohérent à terme* (les lectures
  lointaines convergent), pas « n'importe quoi ». C'est une nuance qui *compte* en entretien.

> **À retenir.** Les 7 erreurs ci-dessus sont les **7 pièges** qu'un analyste junior fait en
> entretien. Le test du C05 est *pouvoir répondre aux 5 mots en moins de 60 mots chacun*.

## 11. Bonnes pratiques professionnelles

> **Dans les faits.** L'anecdote qui justifie la prudence sur le datalake : un cadre d'une grande
> banque française disait en 2018 *« nous avons 14 pétaoctets de datalake, et nous ne savons pas
> ce qu'il y a dedans »*. C'est ce qu'on appelle un **data swamp** : un lac sans gouvernance qui
> accumule les fichiers sans qu'on sache les utiliser. La parade est *imposer un schéma implicite*
> dès l'ingestion (par exemple Delta Lake), avec un petit fichier `_schema.json` qui déclare les
> colonnes attendues. Sans cette discipline, le lac devient un marécage en 6-12 mois. Le coût
> d'un lakehouse bien géré est *équivalent* à celui d'un DWH bien géré ; le coût d'un lac mal
> géré est *infiniment supérieur* (parce qu'on ne peut plus rien en extraire).

- **Choisir NoSQL quand le relationnel est inadapté**, pas par mode. Le réflexe junior est *« on
  va essayer MongoDB »* ; le réflexe senior est *« quelle est la donnée ? quelle est la requête ?
  choisir ensuite. »*
- **Documenter le paysage** dans le README du projet (DWH, lac, lakehouse) pour que les
  nouveaux venus s'orientent.
- **Connaître les 5 mots d'entretien** par cœur (sharding, réplication, CAP, ACID/BASE,
  ETL/ELT), en moins de 60 mots chacun.
- **Différencier OLTP et OLAP** : OLTP = *transactionnel* (caisse), OLAP = *analytique* (DWH).
- **Savoir sharder** (en théorie) sans sharder *en pratique* avant 100 millions de lignes.

> **Conseil professionnel.** Un entretien data, c'est 70 % de SQL et 30 % de paysage. Le C05
> installe les 30 % qui manquent à un junior qui ne connaît que SQL.

---

## 12. Exercice guidé — préparer 5 réponses d'entretien (30 min, /15)

**Objectif.** Mobiliser les 5 mots d'entretien dans **des phrases courtes et justes**.

**Énoncé.** Pour chacun des 5 mots (sharding, réplication, CAP, ACID vs BASE, ETL vs ELT),
rédigez **une réponse de 50-80 mots** qui :
- donne la définition ;
- donne un cas d'usage ;
- cite un outil qui l'illustre.

**Barème (/15).** 3 points par mot (définition 1, cas 1, outil 1).

---

## 13. Exercices autonomes

- **Exercice 13.1 (15 min).** Dessinez la **carte du paysage** (§ 6) en 4 colonnes (datamart,
  DWH, datalake, lakehouse) avec : structure, fréquence, gouvernance, coût.
- **Exercice 13.2 (30 min).** Pour chaque famille NoSQL (document, clé-valeur, graphe, colonnes),
  trouvez **un cas d'usage concret dans votre entreprise** (ou dans une startup typique de la
  formation). Justifiez le choix.
- **Exercice 13.3 (45 min).** Prenez une grande entreprise (Netflix, Uber, Airbnb) et trouvez
  *où* ils utilisent chaque famille NoSQL. Cette recherche peut se faire sur le blog tech de
  l'entreprise.
- **Exercice 13.4 (60 min, optionnel).** Lisez l'article Wikipedia sur le *théorème CAP* et
  rédigez un résumé de 100 mots qui distingue CP, AP, CA avec un outil par catégorie.

---

## 14. Correction détaillée

- **Exercice 13.1.** Datamart : un sujet, rapide à monter, silos possibles. DWH : tous les sujets,
  unifié, plus long à monter. Datalake : tout, brut, marécage en 6 mois sans gouvernance. Lakehouse :
  les deux, moderne, nécessite Delta Lake ou Iceberg.
- **Exercice 13.2.** Document (MongoDB) : profils utilisateurs, attributs variables. Clé-valeur
  (Redis) : cache de session, panier. Graphe (Neo4j) : réseau social, recommandation.
  Colonnes (Cassandra) : historique de capteurs IoT, logs massifs.
- **Exercice 13.3.** Netflix : Cassandra pour le *streaming*, EVCache (clé-valeur maison) pour
  le *cache*. Uber : Schemaless (MySQL modifié) + Cassandra + Redis. Airbnb : MySQL +
  Druid (OLAP). Le schéma se précise dans la presse tech.
- **Exercice 13.4.** CAP : (a) **CP** = cohérence + partitionnement, *HBase* ; (b) **AP** =
  disponibilité + partitionnement, *Cassandra* ; (c) **CA** = cohérence + disponibilité,
  impossible en distribué, c'est l'apanage du SGBD centralisé (PostgreSQL, MySQL classique).

---

## 15. Mini-projet M06.P4 — « Le glossaire des 5 mots d'entretien » (1 h)

**Énoncé.** Rédigez **un glossaire** de 200 mots (± 20) qui couvre les 5 mots d'entretien, en
respectant les contraintes suivantes :

- 5 entrées (sharding, réplication, CAP, ACID/BASE, ETL/ELT).
- Chaque entrée fait **30-50 mots**.
- L'entrée est **structurée** : définition, cas d'usage, outil, piège.
- Le glossaire totalise **200 ± 20 mots**.
- Le glossaire est livré en `03_exercices/dossier_M06/glossaire_M06P4.md`.

**Critères de réussite.**

1. Les **5 entrées** sont présentes (1).
2. Chaque entrée a **définition + cas + outil + piège** (1 par champ, 4 points = 4).
3. Le total mots est **180-220** (1).
4. **Pas de phrase de plus de 50 mots** par entrée (1).
5. Le glossaire est **vérifiable** : un relecteur peut le lire sans bloquer.

**Barème (/10).** 2 pt par critère sauf le 4 et 5 (1 pt chacun).

---

## 16. Boîte à outils du chapitre

> **Boîte à outils.** Sept objets, un seul but — *s'orienter dans le paysage des données* :
>
> 1. **Les 4 familles NoSQL** (§5) — document (MongoDB), clé-valeur (Redis), graphe (Neo4j),
>    colonnes larges (Cassandra).
> 2. **Les 4 concepts de stockage** (§6) — datamart, DWH, datalake, lakehouse.
> 3. **Les 5 mots d'entretien** (§7) — sharding, réplication, CAP, ACID/BASE, ETL/ELT.
> 4. **La matrice du projet M06.P** (§8) — où se trouve la quincaillerie : structure / fréquence
>    / utilisateurs / gouvernance = DuckDB.
> 5. **Le CAP theorem** (§7.3) — 2 sur 3, jamais 3 ; c'est *mathématiquement* impossible.
> 6. **Le tableau ACID vs BASE** (§7.4) — bancaire = ACID, IoT = BASE.
> 7. **Le mini-projet M06.P4** — le glossaire de 200 mots, l'épreuve du C05.

## 17. Résumé du chapitre

- Le **NoSQL** est *Not only SQL* — la famille des bases non-relationnelles (document, clé-valeur,
  graphe, colonnes larges). Il *complète* le relationnel, ne le remplace pas.
- **DWH** (entrepôt) stocke du validé ; **datalake** (lac) stocke du brut ; **lakehouse** combine
  les deux.
- Les **5 mots d'entretien** (sharding, réplication, CAP, ACID/BASE, ETL/ELT) sont la discipline
  du C05. Le professionnel qui les connaît passe l'entretien data.
- Le **projet M06.P** est 100 % relationnel (structure typée, 1 utilisateur, gouvernance locale,
  fréquence analytique). DuckDB est le bon choix. NoSQL et Big Data sont *hors de ce projet* mais
  *dans l'horizon professionnel*.
- Le **mini-projet M06.P4** produit un glossaire de 200 mots sur les 5 mots d'entretien.

## 18. À retenir

> **À retenir.** NoSQL *complète* le relationnel, ne le *remplace* pas. La règle du module est
> *« choisir NoSQL quand le relationnel est maladroit »*, pas par mode. Les 4 familles (document,
> clé-valeur, graphe, colonnes) couvrent 4 cas d'usage distincts, et c'est cette **diversité**
> qui fait la force du paysage.

> **À retenir.** Les 5 mots d'entretien se préparent en **moins de 60 mots chacun**. C'est la règle
> du *« dire peu, dire juste »*. Un entretien data est 70 % SQL + 30 % paysage, et le C05 installe
> les 30 % qui manquent.

## 19. Évaluation formative (auto-correction, 8 min)

**Question 1.** Citez les 4 familles NoSQL. *(Réponse : document, clé-valeur, graphe, colonnes
larges.)*

**Question 2.** Quelle est la différence entre un DWH et un datalake ? *(Réponse : le DWH stocke
du validé ; le datalake stocke du brut, sans validation préalable.)*

**Question 3.** Que dit le théorème CAP ? *(Réponse : un SGBD distribué ne peut pas avoir
simultanément Cohérence, Disponibilité, Tolérance au partitionnement — il faut en choisir 2 sur 3.)*

**Question 4.** Donnez un cas d'usage de MongoDB. *(Réponse : profils utilisateurs avec attributs
variables, catalogues produits, IoT.)*

**Question 5.** Donnez un cas d'usage de Redis. *(Réponse : cache de session, panier d'achat,
compteurs temps réel.)*

**Question 6.** Donnez un cas d'usage de Neo4j. *(Réponse : réseau social, traçabilité alimentaire,
graphe de dépendances logicielles.)*

**Question 7.** Donnez un cas d'usage de Cassandra. *(Réponse : historique de capteurs IoT, logs
massifs, écriture en continu.)*

**Question 8.** Quelle est la différence entre ETL et ELT ? *(Réponse : ETL transforme *hors* du
SGBD analytique ; ELT charge brut et transforme *dans* le SGBD analytique.)*

**Question 9.** Quand sharder ? *(Réponse : au-delà de 1 To de données ou de 100 millions de
lignes ; en dessous, le SGBD centralisé tient. Sharding est irréversible.)*

**Question 10.** Quelle est la différence entre ACID et BASE ? *(Réponse : ACID est le modèle
relationnel (transaction bancaire, isolation, durabilité) ; BASE est le modèle NoSQL distribué
(disponibilité élevée, cohérence à terme).)*
