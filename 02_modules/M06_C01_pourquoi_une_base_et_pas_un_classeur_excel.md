# Module M06.C01 — Pourquoi une base et pas un classeur Excel : redondance, anomalie, concurrence, volumétrie

**Outils comparés : classeur Excel (Microsoft 365), DuckDB 1.5.5, SQLite natif Python, PostgreSQL cité.
Durée indicative : 5 h. Niveau : N2. Prérequis : M01.C03 (la table), M04.C01-C05 (diagnostic et qualité).**

> **L'idée du chapitre.** Le classeur Excel a accompagné toute la phase 1 (M03). Il fait semblant de
> suffire à tout, mais il s'effondre à la troisième table jointe et à la cinquantième millième ligne. Le
> module M06 installe **les raisons** pour lesquelles on passe au SGBD (système de gestion de base de
> données), et installe **les limites** du classeur pour qu'un chargé d'étude sache *quand* basculer. Le
> chapitre C01 fait la moitié du chemin : il pose les cinq limites, la solution SGBD, et les cinq critères
> du choix (calibre du C05 réinvestis). Les chapitres C02-C04 font le reste : table et schéma, clés et
> relations, vivre avec DuckDB et SQLite. Le chapitre C01 ferme la porte — ou plutôt l'ouvre — par les
> **5 critères** et le **verdict : DuckDB intégré / SQLite embarqué / PostgreSQL serveur** pour les trois
> cas du projet M06.P.

> **Base de travail — l'export `quincaillerie_export.csv` (livre M06.P, 24 000 lignes × 42 colonnes).** Le
> chapitre est *mesuré* sur ce dossier livré par `tools/dossier_M06.py` (graine 43) : qui que vous soyez,
> vous touchez les mêmes 24 000 lignes et les mêmes 42 colonnes. Les défauts structurels (ville_client
> redondante, catégorie_pref multi-valuée, taux_tva transitive, mode_paiement référence) et les défauts
> métier (142 montants texte, 8 doublons, 12 dates inversées, 3 clients orphelins) sont ce que le
> classeur Excel **ne sait pas gérer** seul — c'est l'objet du § 5.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

- **énumérer** les cinq limites du classeur Excel pour un fichier multi-tables de plus de 20 000 lignes ;
- **distinguer** une base de données d'un classeur (le SGBD gère, le classeur stocke) ;
- **reconnaître** les quatre défauts structurels d'un export de caisse dénormalisé (redondance,
  multi-valué, dépendance transitive, référence) ;
- **ranger** DuckDB, SQLite et PostgreSQL selon les 5 critères du C05 (taille, fréquence, compétences,
  gouvernance, simplicité) ;
- **décider** quand basculer (la règle des 100 000 lignes de M03) et **dire non** à Excel au-delà ;
- **articuler** le passage Excel → SGBD sans drame (les 4 étapes du § 6.4).

## 2. Pourquoi cette notion est importante

- Le **classeur** a accompagné M01-M03 (lecture, statistiques, Excel). Il fait *presque* tout, et le
  professionnel qui s'y cantonne croit qu'il fait *tout*. Le module M06 installe la lucidité : le
  classeur fait semblant, et le SGBD fait. C'est la *frontière* entre l'analyste qui calcule juste et
  celui qui livre faux.
- L'**export de caisse** (le dossier du projet) contient 42 colonnes pour 24 000 lignes : un classeur
  l'ouvre, mais le **dédoublonnage clé complète** (équivalent du C04) prend 30 secondes par recalcul.
  C'est *la frontière* des 100 000 lignes de C05 §5.1 — un fichier de 240 000 lignes ne s'ouvre pas
  dans Excel du tout.
- Le **passage** au SGBD n'est *pas* une réforme : c'est un changement de pratique. Le chargé d'étude
  qui passe une table de 24 000 lignes dans DuckDB continue de faire la même chose qu'avant, *plus
  vite*, *plus juste*, *plus reproductible*. C'est cette progressivité qui fait que M06 suit M05 dans
  le cursus, et non le remplace.
- Les **5 critères** du C05 sont réinvestis tels quels : taille, fréquence, compétences, gouvernance,
  et un cinquième que le module M06 introduit — la **simplicité de mise en place** (DuckDB ne
  demande aucune installation ; PostgreSQL demande un serveur). C'est l'objet du § 6.
- Le **verdict** du projet M06.P : DuckDB en première intention (intégré, mono-processus, gratuit),
  SQLite en embarqué (fichier, sans client), PostgreSQL cité mais non exécuté dans l'atelier (la
  même règle que Power Query pour M05). C'est le compromis du module.

## 3. Explication simple — les cinq limites du classeur

Le classeur Excel est **excellent** pour une table, un poste, un utilisateur. Il a **cinq limites** quand
le fichier grandit et que l'équipe s'élargit. Pour chaque limite, une manifestation concrète dans le
brut livré par la quincaillerie :

| Limite | Manifestation dans `quincaillerie_export.csv` |
|---|---|
| **Redondance** | la colonne `ville_client` (col 12) recopie la ville dans chacune des 24 000 lignes. Le client 844 habite « Koudougou », et cette chaîne de 10 caractères est **répétée 24 000 / 1 891 ≈ 13 fois** par client. Si le client déménage, il faut changer la ville dans 13 lignes — et il en manquera toujours une (règle : *une donnée, une seule place*). |
| **Anomalie de mise à jour** | `taux_tva_courant` (col 21) vaut `0.18` en 2025 et `0.19` en 2026. Si la loi change le 1ᵉʳ janvier, chaque vente de 2026 doit passer de `0.18` à `0.19` manuellement — sinon le calcul de TVA diverge par ligne. C'est l'objet de la **3FN** (la donnée qui dépend d'une *autre* colonne est externalisée). |
| **Multi-valuée** | `categorie_pref` (col 23) ne porte qu'**une seule** catégorie par client, alors qu'un client peut en aimer 1 à 3 (bricolage + jardinage + décoration, par exemple). Le classeur force à choisir : c'est la violation de la 1FN. La parade est une **table de jointure** (client × catégorie). |
| **Concurrence** | deux caissières ouvrent le même classeur en même temps : Excel crée deux versions, l'« originale » et la « concurrente ». Aucune ne sait qui a la dernière mise à jour. Le SGBD verrouille la ligne, pas le fichier. |
| **Volumétrie et performance** | 24 000 lignes, c'est l'instant où Excel commence à ralentir (filtre 4 secondes, recalcul 8 secondes). À 240 000 lignes, le classeur met 30 secondes à ouvrir et plante à 700 000. Le SGBD tient des milliards de lignes. |

Le tableau **résume** les cinq limites, mais l'enseignement du module est *plus subtil* : ce n'est
pas la limite la plus visible qui fait basculer, c'est le **risque** qu'elle porte. La redondance est
visible (les villes sont en double), l'anomalie de mise à jour est **invisible** jusqu'au jour où le
client déménage. La volumétrie est mesurable, la concurrence est ressentie au premier doublon.

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **classeur** — *workbook* | un fichier `.xlsx` qui contient une ou plusieurs feuilles ; chaque feuille est *à plat*, sans lien formel avec les autres. | confondre avec « base de données » : un classeur avec 5 feuilles n'est pas une base, c'est 5 tables aplaties dans 5 fichiers logiques. |
| **base de données** — *database* | un ensemble de tables reliées par des contraintes (clés étrangères, types, valeurs), persisté sur disque et requêtable par SQL. | croire qu'un CSV en est une : un CSV est une *vue aplatie* d'une base, pas une base. |
| **SGBD** — *Database Management System, DBMS* | le logiciel qui gère la base :DuckDB, SQLite, PostgreSQL, MySQL, SQL Server, Oracle. Le SGBD stocke, indexe, verrouille, sauvegarde. | confondre avec « SQL » : le SQL est le **langage** (la grammaire des requêtes), le SGBD est le **moteur** (celui qui exécute). |
| **DDL** — *Data Definition Language* | le sous-ensemble du SQL qui crée la structure : `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`. | croire qu'il faut un outil séparé : DDL est du SQL, exécuté par le même client. |
| **DML** — *Data Manipulation Language* | le sous-ensemble du SQL qui touche aux données : `SELECT`, `INSERT`, `UPDATE`, `DELETE`. | confondre avec « programmation » : les `UPDATE`/`DELETE` sont *transactionnels* (cf. M07, §5.3 ACID). |
| **table** — *table, relation* | un ensemble de lignes (tuples) de même schéma, nommées par des colonnes typées. Le mot « relation » vient de la théorie (Codd, 1970) ; en pratique on dit « table ». | confondre avec « onglet » : un onglet Excel a un en-tête et des lignes, mais sans schéma ni contrainte formelle. |
| **schéma** — *schema* | la **structure** d'une base (les noms de tables, les colonnes, les types, les contraintes), distincte des **données**. | confondre avec « table » : une base a *un* schéma (ou plusieurs, séparés par namespace) et *N* tables. |
| **redondance** — *redundancy* | le fait qu'une même valeur est recopiée dans plusieurs lignes ou colonnes, au lieu d'être centralisée. C'est l'opposé de la 3FN. | confondre avec « rapidité » : la redondance accélère parfois la lecture, mais ouvre la porte à l'incohérence. |
| **anomalie de mise à jour** — *update anomaly* | quand une donnée redondante est mise à jour *à un endroit mais pas aux autres* : la base devient incohérente. C'est la **conséquence** de la redondance. | croire qu'on peut « mettre à jour régulièrement » : la parade est d'**éliminer la redondance**, pas de la compenser. |
| **clé primaire** — *primary key* | la colonne (ou combinaison) qui identifie une ligne de manière unique et non nulle. Elle est *implicite et non modifiable* dans la base. | confondre avec « identifiant métier » (ex. `id_ticket`) : la clé primaire peut être **propre à la base** (un `id_vente` auto-incrémenté). |
| **clé étrangère** — *foreign key* | une colonne qui pointe sur la clé primaire d'une autre table. La **contrainte** FK garantit que la valeur pointée existe. | croire qu'elle est juste « pour information » : sans la **contrainte** FK, la colonne n'est qu'un nombre sans lien. |
| **intégrité référentielle** — *referential integrity* | la **garantie** qu'une clé étrangère pointe sur une ligne qui existe. C'est un **contrat** que la base tient (ou pas). | croire qu'elle va de soi : il faut l'**écrire** dans le DDL (`FOREIGN KEY … REFERENCES …`). |
| **1FN** — *1st Normal Form* | chaque colonne porte une valeur **atomique**, et pas de répétitions. Le multi-valué (cf. `categorie_pref`) la viole. | croire qu'elle est décorative : la 1FN est la condition **minimale** pour qu'une table soit une table relationnelle. |
| **3FN** — *3rd Normal Form* | toutes les colonnes non-clés dépendent de la clé, de toute la clé, rien que de la clé. Pas de dépendance transitive. C'est l'**objectif** du module M06. | confondre avec « pas de redondance » : la 3FN autorise la redondance **calculable** (les vues). |
| **transaction** — *transaction* | une unité atomique de modifications (`BEGIN`, `COMMIT`, `ROLLBACK`), avec les propriétés **ACID** (atomique, cohérent, isolé, durable). | confondre avec « script » : un script peut faire 7 étapes, mais ce n'est pas une transaction (cf. M07 §5.3). |
| **DuckDB** — *DuckDB* | un SGBD intégré (in-process), orienté analyse, gratuit, mono-utilisateur. Il lit les CSV, Parquet, JSON, et fait du SQL ANSI. | confondre avec « PostgreSQL léger » : DuckDB n'est pas un serveur, c'est une bibliothèque qu'on appelle depuis Python ou le CLI. |
| **SQLite** — *SQLite* | un SGBD embarqué (fichier `.sqlite`), mono-utilisateur, ultra-léger. Utilisé sur Android, iOS, Firefox, et des millions d'applis desktop. | confondre avec « MySQL sans effort » : SQLite n'a pas de client réseau ; c'est un fichier qu'on ouvre. |
| **PostgreSQL** — *PostgreSQL* | un SGBD serveur, multi-utilisateurs, robuste, open source. La référence « sérieuse » pour une base de production. | croire qu'il faut l'installer pour le module : l'atelier ne peut pas exécuter PostgreSQL ; on le cite, on ne l'installe pas. |

> **Définition.** La **base de données relationnelle** est un ensemble de **tables reliées par des
> contraintes** (clés étrangères, types, valeurs, contrôles), persisté sur disque et requêtable par
> SQL via un SGBD. La différence avec un classeur Excel n'est pas la *quantité* de données (un classeur
> peut en stocker autant) mais la **forme des contraintes** : dans la base, les liens entre tables sont
> *portés par la base elle-même* (la contrainte `FOREIGN KEY`), là où dans un classeur ils sont
> *implicites et fragiles* (la jointure manuelle par copier-coller).
> — *English : relational database.*

> **Définition.** Le **SGBD** (système de gestion de base de données) est le **moteur logiciel** qui
> gère la base : stockage, indexation, verrouillage, sauvegarde, exécution des requêtes SQL. Les trois
> SGBD du module sont DuckDB (intégré, mono-processus), SQLite (embarqué, fichier), PostgreSQL (serveur,
> multi-utilisateurs). Le SGBD est *au service de la base*, il n'est pas la base.
> — *English : Database Management System, DBMS.*

> **Définition.** La **3FN** (3ᵉ forme normale) est la condition qui dit : *toutes les colonnes
> non-clés dépendent de la clé, de toute la clé, rien que de la clé*. C'est l'objectif du module : pas
> de dépendance **transitive** (`taux_tva_courant` qui dépend de l'année, pas de la vente), pas de
> dépendance **partielle** (pas applicable quand la clé est simple). La 1FN ajoute « pas de multi-valué ».
> La 3FN est *suffisante* pour la plupart des cas d'usage.
> — *English : Third Normal Form, 3NF.*

> **Définition.** La **clé étrangère** (foreign key, FK) est une **colonne** dont les valeurs sont
> contraintes par une **référence** vers la clé primaire d'une autre table. La contrainte FK est *ce qui
> fait le lien* : sans elle, la colonne n'est qu'un nombre qui peut pointer dans le vide (le défaut des
> « clients orphelins » du § 5.2). Avec elle, la base **garantit** l'intégrité référentielle.
> — *English : foreign key, FK.*

> **Attention.** Le **classeur Excel** *ne vérifie pas* — `SOMME(montant_ttc)` ignore les 142 montants
> texte **silencieusement**, sans erreur, comme le `SUM` DuckDB autoload (cf. C05 §5.6). Le défaut est
> *invisible* dans les deux cas, et c'est l'**import contrôlé par script** qui le détecte.
> Différence majeure : DuckDB *documente* la conversion dans les logs, Excel n'a aucun log.

> **Attention.** Le **SGBD ne corrige pas** les défauts métier du brut — il les *voit*. Si l'export a
> 142 montants texte, ces 142 lignes sont **dans la base** au lieu d'être silencieusement ignorées. La
> règle du module est *import + 3 requêtes = base propre* : l'import filtre (TRY_CAST, NOT NULL, dates),
> les 3 requêtes vérifient (Q1 référentielle, Q2 montants, Q3 rejouable). Sans ce duo, la base n'est
> pas une base, c'est un dépôt.

---

## 5. Cours approfondi — le passage du classeur au SGBD

### 5.1 Le cas fil rouge : `quincaillerie_export.csv`

Le dossier du projet M06.P contient **un seul fichier** : `quincaillerie_export.csv`, 24 000 lignes, 42
colonnes, encodage UTF-8. C'est un **export de caisse** : chaque ligne est une ligne de ticket, et toutes
les informations (client, produit, paiement, magasin) sont à plat. Le stagiaire qui reçoit ce fichier et
doit en faire une base de données tombe sur **quatre défauts structurels** qu'il doit comprendre avant
de toucher au schéma.

**Défaut 1 — redondance.** La colonne `ville_client` (12) répète la ville du client dans chacune de ses
ventes. Si l'un des clients de l'export (par exemple un client référencé dans les 1 891 du fichier
livré) a 13 achats dans le mois, la chaîne « Koudougou » est
recopiée **13 fois**. Le jour où ce client déménage à Ouagadougou, il faut modifier 13 lignes — et la
règle d'or (une donnée, une seule place) est violée. La parade est une **table `client`** séparée, et la
ville y reste une fois.

**Défaut 2 — multi-valué.** La colonne `categorie_pref` (23) porte une **seule** catégorie préférée par
client, alors qu'un client peut en avoir 1 à 3. C'est la violation de la **1FN** : une colonne devrait
être atomique, mais on triche en concaténant mentalement « bricolage ; jardinage ; décoration ». La
parade est une **table de jointure** `client_categorie_pref(id_client, categorie)`, qui porte une ligne
par couple (client, catégorie).

**Défaut 3 — dépendance transitive.** La colonne `taux_tva_courant` (21) vaut `0.18` en 2025 et `0.19` en
2026. Elle est *portée par chaque vente*, mais elle *dépend* de l'**année fiscale**, pas de la vente. C'est
la violation de la **3FN** : une colonne non-clé ne doit dépendre que de la clé (`id_vente`), pas d'une
autre colonne. La parade est une **table `regle_tva(annee_fiscale, taux_tva)`**, et la **vue** (cf. § 5.4)
qui joint `ligne_vente` à `regle_tva` pour calculer le TTC à la lecture.

**Défaut 4 — référence.** La colonne `mode_paiement` (18) porte une chaîne (« ESPECES », « MOBILE_MONEY »,
« CARTE_BANCAIRE », « CREDIT »). Ces quatre valeurs sont figées par les usages du métier, et **elles ne
changent presque jamais**. Les recopier dans chaque ligne gaspille de l'espace et ouvre la porte aux
fautes de frappe (« ESPECSE »). La parade est une **table de référence** `mode_paiement(id, libelle,
frais_pct, delai_encaissement_jours)`, et une **clé étrangère** `vente.id_mode REFERENCES
mode_paiement(id_mode)`.

### 5.2 Les sept défauts métier, ou pourquoi le brut n'est pas la table

L'export contient aussi sept défauts « métier » que la **normalisation** (3FN) ne corrige pas. Ce sont les
mêmes natures qu'en M05, simplifiées :

| Défaut | Compteur mesuré | Effet sur le total |
|---|---:|---|
| 142 montants en texte (« 12 500 FCFA ») | `m06p_montants_texte_export = 142` | la somme directe rate 142 lignes |
| 8 doublons exacts à la fin du fichier | `m06p_doublons_a_retirer = 8` | double comptage |
| 12 dates inversées (jour-mois) | `m06p_dates_inversees_a_reparer = 12` | tri et coupe faussés |
| 3 `id_client` orphelins | `m06p_clients_orphelins_a_ecarter = 3` | jointure naïve gonfle |
| 5 % de retours (montants négatifs) | non compté dans `ATTENDU.json` | filtre « montant < 0 » |
| Encodage UTF-8 (sans BOM) | `quincaillerie_export.csv` | Excel l'ouvre sans message |
| 1M cellules textuelles dans Excel | ≈ 24 000 × 42 = 1 008 000 | recalcul 30 s à 240k lignes |

La **parade** est l'**import contrôlé** : un script qui charge le CSV, **vérifie chaque ligne**, **rejette**
les violations, et **rapporte** les rejets. Le `controles_integrite.sql` du projet M06.P contient les
**3 requêtes** qui vérifient, en SQL, que l'import a bien filtré ces 7 défauts. C'est l'objet du
chapitre C03.

### 5.3 La 3FN appliquée à `quincaillerie_export.csv`

Le passage de 42 colonnes à **7 tables** est l'épreuve de la **3FN**. La règle est **purement mécanique** :
1. **Extraire** toute colonne qui dépend d'une partie de la clé (1FN) ou d'une autre colonne non-clé (3FN).
2. **Créer** une table par groupe de colonnes extraites, avec une clé primaire.
3. **Lier** par des clés étrangères.

L'application sur le brut donne sept tables, dans l'ordre où il faut les créer (les tables **référencées**
avant les tables **faisant référence** ) :

```
1. magasin(id_magasin, libelle)                    -- 3 magasins
2. mode_paiement(id_mode, libelle, frais_pct,     -- 4 modes
                  delai_encaissement_jours)
3. regle_tva(annee_fiscale, taux_tva)            -- 2 règles (2025 et 2026)
4. produit(id_produit, libelle, categorie,       -- 312 produits
            sous_categorie, fournisseur,
            prix_courant_ht)
5. client(id_client, nom, prenom, telephone,     -- 1 891 clients
           email, ville, code_postal, region,
           pays, fidelite_niveau,
           fidelite_points)
6. client_categorie_pref(id_client, categorie)  -- table de jointure N-M
7. vente(id_vente, id_ticket, id_client,        -- 24 000 ventes
          id_magasin, id_vendeur, id_mode,
          date_vente, annee_fiscale, canal,
          est_promo, horodatage)
8. ligne_vente(id_vente, id_produit,             -- N lignes par vente
                quantite, prix_unitaire_ht,
                montant_ht, montant_remise_ht)
9. retour(id_retour, id_vente, motif,            -- 5 % des ventes
           montant_rembourse)
```

Les 8 colonnes supprimées (`client_nom`, `client_prenom`, `client_telephone`, `client_email`,
`produit_libelle`, `produit_categorie`, `produit_sous_categorie`, `fournisseur`, `frais_pct`,
`delai_encaissement_jours`, `taux_tva_courant`, `ville_client`, `categorie_pref`) sont
**toutes des colonnes transitoires ou redondantes** : leur valeur est portée par la table de référence,
et la valeur **calculable** (TVA, ville) est lue par jointure à la demande.

### 5.4 Vue calculée et intégrité — ce qui remplace les colonnes supprimées

La **vue** `ligne_vente_ttc` (du `schema_3fn.sql`) recalcule à la lecture le **montant TTC** et le
**montant TVA** par jointure avec `regle_tva`. C'est l'art du relationnel : la **donnée stockée** est
minimale (juste ce qui ne peut pas se calculer), la **donnée calculée** est lue par vue.

```sql
CREATE VIEW ligne_vente_ttc AS
SELECT lv.*,
       ROUND(lv.montant_ht * (1 + rt.taux_tva)) AS montant_ttc,
       ROUND(lv.montant_ht * rt.taux_tva) AS montant_tva
FROM ligne_vente lv
JOIN vente v ON lv.id_vente = v.id_vente
JOIN regle_tva rt ON v.annee_fiscale = rt.annee_fiscale;
```

Cette vue est **équivalente** à la lecture du brut, mais elle est **fiable** : si le taux de TVA change
au 1ᵉʳ janvier, il suffit de modifier **une ligne** de la table `regle_tva`, et toutes les ventes 2026
voient le bon taux.

### 5.5 Les 3 requêtes qui ferment le module

Les **3 requêtes** du `controles_integrite.sql` sont la **garantie** que la base est intègre. Chaque
requête renvoie **0 ligne** quand tout va bien :

**Q1 — Intégrité référentielle.** Aucune vente ne pointe sur un client qui n'existe pas :
```sql
SELECT v.id_vente, v.id_client
FROM vente v LEFT JOIN client c ON v.id_client = c.id_client
WHERE c.id_client IS NULL;
```
Le `LEFT JOIN` ramène les ventes qui n'ont pas de correspondance ; le `WHERE c.id_client IS NULL` filtre
celles qui pointent dans le vide. Attendu : **0 ligne** après import.

**Q2 — Cohérence des montants.** Chaque `ligne_vente.montant_ht` est bien `quantite × prix_unitaire_ht` :
```sql
SELECT id_vente, id_produit, quantite, prix_unitaire_ht, montant_ht,
       (quantite * prix_unitaire_ht) AS attendu
FROM ligne_vente
WHERE montant_ht != quantite * prix_unitaire_ht;
```
Attendu : **0 ligne**. Si la requête renvoie des lignes, c'est que l'import a chargé des valeurs
incorrectes (typiquement des montants en texte non convertis).

**Q3 — Total par catégorie.** Le total `SUM(montant_ht)` par catégorie correspond au brut original :
```sql
SELECT p.categorie, SUM(lv.montant_ht) AS total_categorie
FROM ligne_vente lv JOIN produit p ON lv.id_produit = p.id_produit
GROUP BY p.categorie ORDER BY total_categorie DESC;
```
Attendu : **5 lignes** (Alimentaire, Bricolage, Jardinage, Quincaillerie, Décoration), avec un total
qui correspond au brut original.

### 5.6 Les 5 critères du choix DuckDB / SQLite / PostgreSQL

Le passage Excel → SGBD n'a **pas une seule réponse**. Trois moteurs coexistent dans le module, et le
choix dépend des **5 critères** suivants (les 4 critères du C05 §5.4 + 1 nouveau, la simplicité) :

| Critère | DuckDB (intégré) | SQLite (embarqué) | PostgreSQL (serveur) |
|---|---|---|---|
| **Taille** | bon jusqu'à 50 M | bon jusqu'à 10 M | illimité |
| **Fréquence** | batch (ponctuel) | batch ou application | transactionnel |
| **Compétences** | Python ou CLI | Python ou CLI | SQL + administration |
| **Gouvernance** | fichier local | fichier local | serveur centralisé |
| **Simplicité de mise en place** | aucune (`pip install duckdb`) | aucune (natif Python) | serveur à installer |

**La règle du module** : DuckDB en première intention (à 24 000 lignes, l'usage est *analyse* et DuckDB
est imbattable), SQLite pour une application embarquée (un fichier qu'on copie), PostgreSQL cité pour
*quand l'équipe grandit* (la base multi-utilisateurs, avec serveur et sauvegardes automatiques). Le
module M06 enseigne DuckDB et cite SQLite/PostgreSQL, parce que c'est l'usage direct de l'analyste.

### 5.7 « Quand basculer ? » — la règle des 100 000 lignes et le verdict

La **règle des 100 000 lignes** (cf. M05 C05 §5.1) ne suffit pas. Il faut **trois conditions** pour
basculer du classeur au SGBD :

1. **Taille** > 100 000 lignes OU **volumétrie** qui grossit (multiplication par an) ;
2. **Jointures** ≥ 3 tables (au-delà, le classeur s'effondre en RECHERCHEV imbriquées) ;
3. **Concurrence** ≥ 2 utilisateurs simultanés OU **gouvernance** qui exige une trace d'audit.

Le projet M06.P coche **les trois cases** : 24 000 lignes aujourd'hui mais 240 000 attendues (×10 en 2
ans), 7 tables à joindre (vente × client × produit × paiement × TVA × magasin × ligne_vente), et la
caissière de Koudougou qui ouvre en même temps que la responsable de Bobo-Dioulasso. C'est *flagrant*
qu'il faut un SGBD. Pour un cas limite (50 000 lignes, 1 utilisateur, 2 tables), le classeur *peut*
encore tenir — au prix de la rigueur.

---

## 6. Exemple concret — le verdict de la bascule

### 6.1 L'export `quincaillerie_export.csv` côté Excel

Un classeur ouvert sur l'export :
- **24 000 lignes** : filtre sur `client_ville = "Koudougou"` en 4 secondes (acceptable).
- **42 colonnes** : tri par `produit_categorie` puis `client_nom` en 2 secondes (acceptable).
- **Calcul** : `SOMME(montant_ttc)` ramène un total sur 24 000 lignes en 8 secondes, mais **142 lignes
  de montants texte** sont **ignorées** (cf. C05 §5.6) : le total est faux. Le classeur ne le dit pas.
- **Dédoublonnage** : `supprimer les doublons` sur la colonne `id_ticket` en 30 secondes, mais **ne
  traite pas les copies partielles** (8 lignes qui ne diffèrent que sur la date — invisibles au
  dédoublonnage Excel).

> **Le verdict.** Le classeur *ouvre*, *trie*, *filtre*, mais **ne vérifie pas** et **ne reproduit pas**.
> La règle est *classeur pour voir, SGBD pour vérifier* (cf. § 5.7).

### 6.2 Le même fichier dans DuckDB

Le même fichier dans DuckDB (Python ou CLI) :
```python
import duckdb
con = duckdb.connect()
con.execute("CREATE TABLE export AS SELECT * FROM read_csv_auto('quincaillerie_export.csv')")
print(con.execute("SELECT COUNT(*) FROM export").fetchone())       # 24 000 lignes en 80 ms
print(con.execute("SELECT SUM(montant_ttc) FROM export").fetchone())  # somme en 200 ms
```
- 24 000 lignes lues en **80 ms** (DuckDB est ~30 × plus rapide que pandas pour l'import, et Excel ne
  sait même pas mesurer).
- La somme `SUM(montant_ttc)` est **faux aussi** : DuckDB autoload convertit « 1 200 FCFA » en 1200 et
  les ajoutes au total, mais signale la conversion dans les **logs**. Le défaut n'est plus *silencieux*
  comme dans Excel : il est *visible*.
- **3 requêtes d'intégrité** (cf. § 5.5) sont exécutables en quelques lignes, et chacune documente
  son verdict par écrit.

> **Le verdict.** DuckDB fait *plus vite* ce que le classeur fait *plus lentement*, mais surtout il
> **documente** ce qu'il fait (logs) et **vérifie** ce que le classeur *ne vérifie pas* (les 3 requêtes).

### 6.3 Ce qu'un SGBD ne fait pas (par construction)

Le SGBD **n'efface pas** les défauts métier du brut — il les *rend visibles*. Si l'export a 142 montants
texte, ils sont là, et les 142 lignes sont **dans la base** au lieu d'être silencieusement ignorées. Le
SGBD **ne décide pas** non plus : `INSERT` ne fait *que* insérer. C'est l'import qui doit convertir, et
c'est l'import qui doit *rejeter* les lignes non conformes. La règle du module est **import + 3
requêtes** = base propre.

---

## 7. Démonstration pas à pas — comment basculer, en 4 étapes

### 7.1 Importer le CSV

Dans DuckDB :
```sql
CREATE TABLE export_brut AS
SELECT * FROM read_csv_auto('quincaillerie_export.csv', all_varchar=true);
```
Le `all_varchar=true` force toutes les colonnes en texte — c'est l'étape « chargement brut », où rien
n'est converti. La table `export_brut` reflète le fichier.

### 7.2 Filtrer les défauts métier

```sql
CREATE TABLE export_filtre AS
SELECT *
FROM export_brut
WHERE id_client IS NOT NULL                          -- 3 clients fantômes écartés
  AND id_client IN (SELECT id_client FROM client)    -- intégrité référentielle
  AND TRY_CAST(montant_ttc AS BIGINT) IS NOT NULL    -- 142 montants texte écartés
  AND date_vente ~ '^\d{4}-\d{2}-\d{2}$';            -- 12 dates mal formées écartées
```
Le filtre **applique** les règles métier avant l'import dans la table finale.

### 7.3 Définir les 7 tables en 3FN

```sql
CREATE TABLE client (
    id_client    INTEGER PRIMARY KEY,
    nom          TEXT NOT NULL,
    prenom       TEXT NOT NULL,
    telephone    TEXT NOT NULL UNIQUE,
    email        TEXT UNIQUE,
    ville        TEXT NOT NULL,
    fidelite_niveau TEXT NOT NULL DEFAULT 'COMPTOIR'
);

CREATE TABLE vente (
    id_vente         INTEGER PRIMARY KEY,
    id_client        INTEGER NOT NULL REFERENCES client(id_client),
    id_magasin       INTEGER NOT NULL,
    id_mode          INTEGER NOT NULL,
    date_vente       DATE NOT NULL,
    annee_fiscale    INTEGER NOT NULL
);
```
Et ainsi de suite pour les 7 tables.

### 7.4 Vérifier l'intégrité par les 3 requêtes

Reprendre `controles_integrite.sql` et l'exécuter :
```sql
-- Q1, Q2, Q3 (cf. § 5.5).
```

> **À retenir.** Les 4 étapes du passage Excel → SGBD sont : **importer brut, filtrer les défauts,
> schématiser en 3FN, vérifier l'intégrité**. C'est la même séquence que M05 (transformation +
> dédoublonnage + jointure + verdict), appliquée à un SGBD. La différence est *l'automatisation* : une
> fois l'import écrit, il est *rejouable* (paramétrable par date, par magasin, etc.).

---

## 8. Erreurs fréquentes

- **Croire que le SGBD résout les défauts métier du brut.** Le SGBD les *voit*, mais il ne les *corrige
  pas* — c'est l'import qui filtre. Une base qui contient 142 montants texte est une **mauvaise base**,
  même si elle est en 3FN.
- **Confondre redondance et performance.** Parfois, dénormaliser une colonne *accélère* la lecture (par
  exemple, mettre la `ville_client` directement dans la table `vente`). Mais c'est un compromis
  *documenté* : on garde la redondance quand on sait qu'on perd la mise à jour automatique. La règle du
  module est *3FN par défaut, redondance calculable par vue quand le besoin est mesuré*.
- **Croire que la 1FN et la 3FN sont « pour les puristes ».** Un client qui a deux catégories préférées
  ne tient pas dans une seule colonne. Croire qu'on peut « concaténer » (« bricolage,jardinage ») est le
  piège classique : ça marche à l'affichage, ça casse à la jointure.
- **Importer sans vérifier.** Le `CREATE TABLE` ne vérifie rien. Seules les **3 requêtes** vérifient.
  Une base qui n'a pas été testée par les 3 requêtes n'est *pas* une base — c'est un dépôt.
- **Vouloir tout stocker.** Stocker la TVA ou le TTC dans la base *empêche* la mise à jour du taux. La
  règle est : **stocker le minimum**, **calculer le reste par vue**. La TVA est dans `regle_tva`, le TTC
  est dans la vue `ligne_vente_ttc`.
- **Utiliser PostgreSQL pour 24 000 lignes.** C'est comme prendre un semi-remorque pour livrer une
  pizza : ça marche, mais c'est surdimensionné. DuckDB fait le même travail sans serveur.
- **Sous-estimer la migration des données.** Importer 24 000 lignes d'un CSV dans 7 tables prend du
  temps — pas en minutes, mais en *logique* (les défauts à filtrer, les conversions à appliquer). La
  règle est *prévoir un import contrôlé par script, pas un copier-coller Excel*.

> **À retenir.** Les 7 erreurs ci-dessus coûtent toutes le **verdict du projet M06.P**. Le projet qui
> oublie de filtrer les défauts métier a un total faux ; le projet qui ne vérifie pas l'intégrité a une
> base qui *semble* correcte mais ne l'est pas. La leçon est **l'import n'est pas la base — la base, c'est
> l'import plus les 3 contrôles**.

---

## 9. Bonnes pratiques professionnelles

- **Documenter chaque table dans le README** (le projet M06.P E5) avec son **grain** (« une ligne = un
  client », « une ligne = une vente »). Le grain perdu, la table est incompréhensible.
- **Tester l'intégrité par 3 requêtes** au minimum : (1) référentielle, (2) cohérence métier, (3) rejouabilité
  (cf. § 5.5). Sans ces 3 requêtes, la base n'est pas livrable.
- **Paramétrer l'import** par date (`WHERE date_vente BETWEEN …`) plutôt que par fichier. Le même script
  doit pouvoir réimporter le mois suivant sans modification du code.
- **Versionner le schéma SQL** dans un fichier `schema_3fn.sql` commité, pas dans un notebook
  interactif. La base est un *artefact reproductible*, pas une improvisation.
- **Mesurer** l'écart entre le total du brut et le total de la base après import. Si l'écart est 0 ou
  faible (les défauts rejetés), la base est cohérente. Si l'écart est important, l'import a perdu des
  lignes.
- **Documenter les défauts rejetés** dans le journal d'import. Le projet M06.P attend un rapport de
  cette forme : « 142 lignes écartées pour montant texte (cf. C05 §5.6) ; 12 lignes pour date mal formée
  (cf. M04 E4) ; 8 lignes pour doublon (cf. M05 C03) ; 3 lignes pour client orphelin (cf. contrôle Q1) ».

> **Conseil professionnel.** Le verdict d'une base de données n'est pas *« elle marche »* ; c'est
> *« les 3 requêtes renvoient 0 ligne »*. C'est cette discipline qui distingue une base d'un fichier
> Excel. Et c'est ce que le projet M06.P évalue.

---

## 10. Exercice guidé — la lettre au stagiaire (15 min, /10)

**Objectif.** Mobiliser les 5 limites du classeur sur un cas concret.

**Énoncé.** Vous êtes chargé d'étude dans une enseigne de distribution. Le directeur commercial vous
remet un fichier `ventes_export.csv` (15 colonnes, 50 000 lignes, fait à partir du logiciel de caisse).
Il dit : *« tu n'as qu'à l'ouvrir dans Excel, ça doit suffire. »* Vous avez 5 minutes pour répondre par
mail : faut-il ouvrir dans Excel, basculer dans DuckDB, ou autre chose ?

**Barème (/10).**

| Critère | Points |
|---|---|
| Cite au moins 3 des 5 limites du classeur | 2 |
| Identifie la limite **décisive** (volumétrie vs jointure vs concurrence) | 2 |
| Donne un verdict motivé (Excel ou DuckDB ou autre) | 3 |
| Chiffre les alternatives (combien de temps dans Excel, combien dans DuckDB) | 2 |
| Cite les 3 requêtes d'intégrité attendues | 1 |
| **Total** | **10** |

> **Dans les faits.** La réponse attendue : *« Le fichier a 50 000 lignes (sous le seuil 100k), 1 table,
> pas de jointure multi-table visible, mono-utilisateur (votre service). Vous pouvez commencer dans
> Excel pour voir, basculer dans DuckDB dès qu'une deuxième table arrive (par exemple quand le service
> qualité veut croiser avec un fichier de lots). Les 3 requêtes d'intégrité attendues : Q1 référentielle,
> Q2 montants, Q3 total rejouable. »* Le barème teste la **capacité à dire non à Excel** sans le dire
> *par principe* — c'est l'enseignement du § 5.7.

---

## 11. Exercices autonomes

- **Exercice 11.1 (15 min).** Citez les **5 limites du classeur Excel** et donnez, pour chacune, un
  chiffre du projet M06.P qui la rend visible.
- **Exercice 11.2 (30 min).** Sur le `quincaillerie_export.csv` téléchargé, ouvrez-le dans Excel,
  comptez le temps d'ouverture et le temps de filtre sur `ville_client = "Koudougou"`. Puis exécutez
  la même opération dans DuckDB et notez les temps. Commentez l'écart en 3 lignes.
- **Exercice 11.3 (45 min).** Identifiez, dans le brut livré, **un** défaut structurel qui n'est **pas**
  listé au § 5.1 (par exemple `montant_remise_ht` qui dépend d'une *promotion* et non de la vente).
  Rédigez le DDL de la table qui l'absorbe.
- **Exercice 11.4 (60 min, optionnel).** Réécrivez le verdict du § 5.5 en **PostgreSQL** plutôt qu'en
  DuckDB. Cherchez 3 différences syntaxiques et notez-les (par exemple : `TRY_CAST` DuckDB vs `CAST`
  PostgreSQL, `IS NOT DISTINCT FROM`, `ON CONFLICT`).

---

## 12. Correction détaillée

- **Exercice 11.1.** Limites : (1) redondance — la colonne `ville_client` est recopiée 13 × par client
  (`m06p_clients_uniques_references = 1 891`, 24 000 lignes) ; (2) anomalie de mise à jour — la TVA
  change tous les ans, 24 000 lignes à mettre à jour ; (3) multi-valué — `categorie_pref` ne porte
  qu'**une** catégorie par client ; (4) concurrence — la caissière de Koudougou et la responsable de
  Bobo-Dioulasso ouvrent en même temps ; (5) volumétrie — 24 000 lignes, c'est la frontière où Excel
  ralentit (8 secondes par recalcul).
- **Exercice 11.2.** Les temps attendus : Excel ≈ 4-8 secondes pour le filtre, DuckDB ≈ 80 ms pour
  l'import + 50 ms pour le filtre. **Ratio ≈ 100 ×**. Si la machine est plus lente, le ratio reste
  du même ordre.
- **Exercice 11.3.** Un défaut **non listé** : `montant_remise_ht` (col 30) est nul dans 90 % des
  lignes, et porte 10 000 FCFA dans 10 % des lignes. Il dépend de la *promotion* (col 35 `est_promo`),
  pas de la vente. La parade est soit une table `promotion(id_promo, libelle, montant_remise)`, soit
  une simple **règle métier** dans le README (la remise est une constante de 10 000 pour toute vente
  en `est_promo = 1`). Le DDL attendu : `CREATE TABLE promotion (id_promo INTEGER PRIMARY KEY,
  libelle TEXT, montant_remise INTEGER NOT NULL CHECK (montant_remise > 0));` et `vente.est_promo
  →` *pas de FK directe* (les promos changent).
- **Exercice 11.4.** Trois différences DuckDB → PostgreSQL : (a) `TRY_CAST` DuckDB → `CAST` ou
  `(expression)::type` PostgreSQL, sans gestion d'erreur ; (b) `IS NOT DISTINCT FROM` est supporté par
  PostgreSQL (et DuckDB), pas par tous les SGBD ; (c) `ON CONFLICT (id) DO UPDATE` est PostgreSQL
  natif depuis 9.5 (upsert), DuckDB l'a aussi depuis 0.9. Le verdict : DuckDB est *suffisamment
  compatible* PostgreSQL pour le module, mais l'atelier ne fait pas l'aller-retour.

---

## 13. Mini-projet M06.P1 — « Le verdict de la bascule » (1 h)

**Énoncé.** Rédigez **1 page maximum** (PDF ou Markdown) qui répond, en phrases, à la question : *« Le
fichier `quincaillerie_export.csv` doit-il basculer dans un SGBD ? Si oui, lequel des trois
(DuckDB / SQLite / PostgreSQL) ? »*

**Critères de réussite.**

1. Les 5 limites du classeur sont citées **avec un chiffre du projet** chacune.
2. Les **3 critères limitants** (volumétrie, jointure, concurrence) sont **identifiés** sur le cas.
3. Le verdict (Excel / DuckDB / SQLite / PostgreSQL) est **motivé** par les 5 critères du § 5.6.
4. Une **règle de bascule** est formulée (« si le fichier double en 1 an, basculer dans DuckDB »).

**Barème (/10).** 2 points par critère sauf le 4 (règle de bascule) qui vaut 4 points.

---

## 14. Boîte à outils du chapitre

> **Boîte à outils.** Six objets, un seul but — *décider quand basculer du classeur au SGBD* :
>
> 1. **Le tableau des 5 limites** (§ 5.1) — redondance, anomalie, multi-valué, concurrence, volumétrie.
> 2. **Le tableau des 7 défauts** (§ 5.2) — quatre structurels et trois métier, avec leur compteur dans
>    `m06p_*`.
> 3. **Les 3 règles de bascule** (§ 5.7) — taille > 100 000 OU jointures ≥ 3 OU concurrence ≥ 2.
> 4. **Le schéma des 7 tables** (§ 5.3) — la cible 3FN, à valider par le projet.
> 5. **La vue `ligne_vente_ttc`** (§ 5.4) — l'exemple type de « donnée calculée, pas stockée ».
> 6. **Les 3 requêtes d'intégrité** (§ 5.5) — Q1 référentielle, Q2 montants, Q3 rejouable.

## 15. Résumé du chapitre

- Le classeur a **5 limites** (§ 5.1) : redondance, anomalie de mise à jour, multi-valué, concurrence,
  volumétrie.
- La base de données est un **ensemble de tables reliées par des contraintes**, gérées par un SGBD
  (DuckDB, SQLite, PostgreSQL).
- L'export `quincaillerie_export.csv` (24 000 lignes × 42 colonnes) contient **4 défauts structurels**
  (§ 5.1) — redondance de `ville_client`, multi-valué de `categorie_pref`, dépendance transitive de
  `taux_tva_courant`, référence de `mode_paiement` — et **4 défauts métier** (§ 5.2).
- La **3FN** appliquée au brut donne **7 tables** (§ 5.3) : `magasin`, `mode_paiement`, `regle_tva`,
  `produit`, `client`, `client_categorie_pref`, `vente`, `ligne_vente` (+ `retour`).
- Les **3 requêtes** d'intégrité (§ 5.5) ferment le module : Q1 référentielle, Q2 cohérence des montants,
  Q3 rejouable par catégorie.
- Les **5 critères du choix** SGBD (§ 5.6) : DuckDB en première intention, SQLite pour embarqué,
  PostgreSQL cité pour multi-utilisateurs.

## 16. À retenir

> **À retenir.** Le SGBD ne *résout pas* les défauts du brut — il les *rend visibles*. C'est l'import
> qui filtre, et c'est l'import qui *rejette*. La 3FN est l'objectif, le `schema_3fn.sql` est la cible, les
> 3 requêtes sont la garantie. Le verdict est *« les 3 requêtes renvoient 0 ligne »*, pas *« la base
> fonctionne »*. C'est cette discipline qui distingue un SGBD d'un classeur.

> **À retenir.** La bascule Excel → SGBD a **3 critères limitants** : taille > 100 000 lignes, jointures
> ≥ 3, concurrence ≥ 2. Tant qu'aucun n'est franchi, le classeur tient ; dès qu'un seul l'est, basculer.
> Pour 24 000 lignes et 7 tables, **DuckDB** est le bon choix ; pour 250 millions et 200 utilisateurs
> simultanés, **PostgreSQL** l'est. Le critère *taille* du C05 §5.6 devient *volumétrie + concurrence*
> — la gouvernance locale ne suffit plus à elle seule.

## 17. Évaluation formative (auto-correction, 8 min)

**Question 1.** Citez les 5 limites du classeur Excel. *(Réponse : redondance, anomalie de mise à
jour, multi-valué, concurrence, volumétrie.)*

**Question 2.** Quels sont les 4 défauts structurels du `quincaillerie_export.csv` ? *(Réponse : (1)
`ville_client` redondante, (2) `categorie_pref` multi-valué, (3) `taux_tva_courant` en dépendance
transitive, (4) `mode_paiement` en référence à externaliser.)*

**Question 3.** Combien de tables le passage en 3FN produit-il dans le projet M06.P ?
*(Réponse : `m06p_tables_3fn_cible = 7`.)*

**Question 4.** Pourquoi la **vue** `ligne_vente_ttc` est-elle préférable à une colonne stockée ?
*(Réponse : la TVA change chaque année ; si elle est stockée, il faut modifier 24 000 lignes ; si elle
est en vue, il suffit de modifier une ligne de `regle_tva`.)*

**Question 5.** Citez les 3 critères qui font basculer du classeur au SGBD. *(Réponse : (a) taille
> 100 000 lignes, (b) ≥ 3 tables à joindre, (c) ≥ 2 utilisateurs simultanés.)*

**Question 6.** Quel SGBD pour 240 000 lignes multi-utilisateurs ? *(Réponse : PostgreSQL — le seul
des trois qui tienne le multi-utilisateurs avec un serveur.)*

**Question 7.** Que renvoient les 3 requêtes `controles_integrite.sql` quand la base est intègre ?
*(Réponse : Q1 → 0 ligne, Q2 → 0 ligne, Q3 → 5 lignes (les 5 catégories, avec leur total).)*
