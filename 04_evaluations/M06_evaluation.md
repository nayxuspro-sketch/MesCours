# Évaluation M06 — « Bases de données relationnelles : comprendre avant de requêter »

**Module M06 · durée totale 2 h 30 · quatre épreuves · seuils : quiz 11/15, exercices 14/20, étude de cas 12/20**

| Épreuve | Durée | Barème | Noté | Ce qui est attendu |
|---|---|---|---|---|
| A · Questions de récupération | 15 min | non noté | non | vérifier qu'on a lu les cinq chapitres avant de se tromper cher |
| B · Quiz | 25 min | /15 | oui | quinze questions à réponse unique, cinq blocs |
| C · Exercices pratiques | 50 min | /20 (auto-corrigé) | oui | deux exercices menés jusqu'au chiffre sur le dossier du module |
| D · Étude de cas | 60 min | /20, seuil 12 | oui | un dossier en deux pages : « sept tables pour une quincaillerie » |

> Le score du module se lit ainsi : **B ≥ 11** et **D ≥ 12** valident le module ; le projet M06.P doit
> atteindre 13. Un candidat qui réussit B et échoue à D repasse uniquement D : savoir qu'une clé
> étrangère pointe vers une primary key ne dispense pas de vérifier qu'elle ne pointe pas dans le
> vide. Tout nombre de cette évaluation est mesuré sur le socle livré ; les corrections le citent
> avec leur clé `m06_*`/`m06p_*` dans `chiffres_cites.json`.

---

## A · Questions de récupération (non notées)

À traiter sans document, en une ou deux phrases chacune. Elles ne sont pas comptées ; elles servent à
repérer ce qui n'est pas assimilé avant de perdre des points sur un détail.

1. Citez les **5 limites** d'un classeur Excel listées en C01, et la solution qu'apporte un SGBD pour chacune.
2. Quelle est la différence entre une **clé primaire** et une **clé étrangère** ? Laquelle des deux est
   forcément indexée ?
3. Citez les **3 formes normales** (1NF, 2NF, 3NF) et donnez, pour chacune, le défaut qu'elle élimine
   (atomicité, dépendance partielle, dépendance transitive).
4. Citez les **5 actions** de `ON DELETE` (RESTRICT, CASCADE, SET NULL, SET DEFAULT, NO ACTION) et
   indiquez celle qui est la valeur par défaut en SQLite.
5. Pourquoi `PRAGMA foreign_keys = ON` est-il **obligatoire** en SQLite mais pas en PostgreSQL ?
6. Donnez la **règle d'or** des relations (direction de la FK) et l'erreur qu'elle évite.
7. Quelle est la différence entre **ACID** et **BASE** ? Lequel des deux s'applique à DuckDB ?
8. Citez les **4 familles NoSQL** et, pour chacune, un cas d'usage où elle bat le relationnel.
9. Qu'est-ce qu'un **entrepôt de données** (DWH), un **lac** (datalake) et un **lakehouse** ? Lequel
   stocke des données brutes sans validation ?
10. Pourquoi le module M06 **ne fait pas exécuter** PostgreSQL, et dans quel module suivant cette
    exécution aura-t-elle lieu ?

---

## B · Quiz (15 questions · 15 points)

**Barème : 1 point par question, une seule bonne réponse. Les réponses justifiées en une ligne
rapportent un demi-point de bonus, plafonné à 15.**

### Bloc 1 — Pourquoi une base (C01) (Q1 à Q3)

**Q1.** Le classeur Excel s'effondre typiquement à partir de : a) 100 lignes · b) **50 000 lignes ou la
3ᵉ table jointe** · c) 1 million de lignes · d) il ne s'effondre jamais, c'est un mythe.

**Q2.** Le SGBD apporte **5 propriétés** qu'Excel ne garantit pas. Laquelle manque le plus dans une
feuille de calcul partagée ? a) la couleur des cellules · b) **l'intégrité référentielle** · c) le
tri alphabétique · d) le formatage conditionnel.

**Q3.** « Une base de données, c'est juste un fichier avec des tables. » Cette phrase est : a) vraie ·
b) **fausse** — un SGBD est un moteur qui gère la concurrence, les transactions et l'intégrité ; le
fichier n'en est qu'un effet · c) vraie pour SQLite uniquement · d) vraie pour PostgreSQL
uniquement.

### Bloc 2 — Tables, colonnes, schéma (C02) (Q4 à Q6)

**Q4.** La 1NF exige que chaque cellule soit : a) **atomique** (une seule valeur) · b) coloriée en
jaune · c) numérique · d) en majuscules.

**Q5.** Le type `DECIMAL(14, 2)` pour `montant_ttc` : a) accepte les lettres si elles sont en
majuscules · b) **refuse tout caractère non numérique et tronque à 2 décimales** · c) est identique
à `FLOAT` · d) est réservé à PostgreSQL.

**Q6.** Une colonne `mode_paiement` qui prend les valeurs `{Espèces, Carte, Mobile money, Crédit}` est
mieux modélisée par : a) une colonne `VARCHAR` libre · b) **une table de référence `mode_paiement`
avec une FK** (1NF + 3NF, évite les fautes de frappe) · c) une colonne `INTEGER` avec des codes
magiques (1=Espèces, 2=Carte…) sans documentation · d) un fichier JSON par ligne.

### Bloc 3 — Clés et relations (C03) (Q7 à Q9)

**Q7.** Une clé primaire : a) peut être dupliquée si on l'écrit en rouge · b) **identifie **une** ligne
de façon unique et n'est jamais `NULL`** · c) peut être `NULL` une fois par table · d) doit toujours
être un entier auto-incrémenté.

**Q8.** Dans une relation 1-N entre `client` (1) et `vente` (N) : a) la clé étrangère est dans
`client.id_client` · b) **la clé étrangère est dans `vente.id_client` (du N vers le 1)** · c) la
clé étrangère est dans les deux tables · d) il n'y a pas de clé étrangère, juste un lien logique.

**Q9.** L'action `ON DELETE RESTRICT` : a) supprime la ligne parente et toutes ses filles · b) **refuse
la suppression de la ligne parente si des filles existent** (sécurité par défaut) · c) met la FK
des filles à `NULL` · d) ne fait rien, sans message d'erreur.

### Bloc 4 — DuckDB / SQLite / PostgreSQL (C04) (Q10 à Q12)

**Q10.** DuckDB est : a) un serveur client-serveur comme PostgreSQL · b) **un moteur embarqué,
in-process, mono-utilisateur** (comme SQLite mais orienté analytique) · c) un outil NoSQL · d) une
interface graphique.

**Q11.** SQLite et PostgreSQL diffèrent sur : a) le langage utilisé (l'un parle SQL, l'autre non) · b)
**l'activation des FK par défaut (OFF en SQLite, ON en PostgreSQL)** et la portee (fichier vs
serveur) · c) le prix (l'un est gratuit, l'autre non) · d) ils sont identiques.

**Q12.** Dans ce module, PostgreSQL est : a) **cité sans exécuté** (règle M06 §1.5) ; les commandes
sont publiées mais non lancées · b) exécuté sur le serveur de l'école · c) ignoré complètement · d)
exécuté via DuckDB.

### Bloc 5 — Paysage NoSQL / DWH / datalake (C05) (Q13 à Q15)

**Q13.** Les **4 familles NoSQL** sont : a) **document, clé-valeur, graphe, colonnes** (MongoDB,
Redis, Neo4j, Cassandra) · b) relationnel, objet, XML, JSON · c) MySQL, PostgreSQL, SQLite, DuckDB
· d) Excel, Access, LibreOffice, Google Sheets.

**Q14.** Un **datalake** stocke : a) uniquement des données validées et propres · b) **des données
brutes, sans validation préalable, au format natif** · c) exclusivement des données structurées · d)
des fichiers Excel uniquement.

**Q15.** Le verdict 80/20 du module signifie : a) 80 % de NoSQL, 20 % de SQL · b) **80 % des cas
utilisent SQL (relationnel) ; 20 % justifient NoSQL** quand le relationnel est inadapté · c) 80 %
des données sont propres, 20 % sont sales · d) le module est fini à 80 %.

---

## C · Exercices pratiques (2 exercices · 20 points)

### Exercice 1 — Vérifier l'intégrité référentielle (10 points)

À partir de `03_exercices/dossier_M06/quincaillerie_export.csv` (24 000 l. × 42 col, graine 43) :

1. **(3 pts)** En DuckDB, charger le CSV, créer la table `client(id_client PRIMARY KEY, …)` puis
   vérifier combien de `id_client` du CSV **n'existent pas** dans la liste des clients. Réponse
   attendue : `3` (`m06_clients_orphelins_a_ecarter`).
2. **(3 pts)** Écrire la requête DuckDB qui retourne les `id_vente` concernés par ces 3 orphelins.
   Donnez la requête et le nombre de lignes retournées (24 000 ventes initiales - N ventes
   touchées).
3. **(2 pts)** Reprendre la même requête en SQLite (en activant `PRAGMA foreign_keys = ON` et en
   utilisant le schéma 3FN). Comparer le résultat : doit être identique.
4. **(2 pts)** Citer la commande PostgreSQL qui ferait la même vérification, **sans l'exécuter**.

### Exercice 2 — Convertir 142 montants en texte (10 points)

1. **(4 pts)** En DuckDB, écrire la requête qui convertit `montant_ttc` (texte avec « FCFA » et
   espaces) en `DECIMAL(14, 2)` et qui retourne le nombre de lignes où la conversion a réussi.
   Indice : `TRY_CAST(REPLACE(REPLACE(montant_ttc, ' FCFA', ''), ' ', '') AS DECIMAL(14, 2))`. Le
   nombre attendu : 24 000 - 142 = 23 858 lignes converties (`m06_montants_texte_export = 142`).
2. **(3 pts)** Pourquoi `TRY_CAST` plutôt que `CAST` ? Que retourne `TRY_CAST` quand la conversion
   échoue ?
3. **(3 pts)** Écrire l'équivalent en pandas
   (`pd.to_numeric(df['montant_ttc'].str.replace(...), errors='coerce')`). Citer le module où cette
   opération a été vue pour la première fois.

---

## D · Étude de cas (1 cas · 20 points · seuil 12/20)

### « Sept tables pour une quincaillerie »

Une enseigne de quincaillerie à Bobo-Dioulasso vous confie son export quotidien
(`quincaillerie_export.csv`, 24 000 l. × 42 col, 4 défauts : 142 montants en texte, 8 doublons,
12 dates inversées, 3 clients orphelins).

Le directeur vous demande de produire un dossier en deux pages comprenant :

1. **(5 pts)** Le **schéma 3FN en 7 tables** avec PK, FK et contraintes CHECK. Vous nommerez
   explicitement chaque défaut que la 3FN élimine (atomicité, redondance, dépendance transitive).
2. **(5 pts)** La **démarche de chargement DuckDB** qui nettoie les 4 défauts (étape par étape,
   avec la commande DuckDB et la sortie observée). Vous citerez les **3 chiffres mesurés** :
   142, 8, 12, 3.
3. **(5 pts)** La **démarche SQLite** équivalente, avec `PRAGMA foreign_keys = ON` et
   `INTEGER PRIMARY KEY` (au lieu de `SERIAL` PostgreSQL). Différences et points communs avec
   DuckDB.
4. **(5 pts)** Le **verdict structuré** : quel moteur choisir pour ce cas (volumétrie,
   utilisateurs, gouvernance), et dans quel cas on basculerait vers PostgreSQL ou NoSQL. Citez
   le « 80 / 20 » du module.

**Critères de notation** :
- 12/20 : les 4 défauts sont identifiés et le schéma 3FN est juste, mais le verdict est imprécis.
- 16/20 : tout est juste, DuckDB et SQLite sont cités avec une commande exécutée, le verdict est
  chiffré.
- 20/20 : idem + au moins un cas de basculement justifié (« si on passait à 5 data analysts
  en production, on prendrait PostgreSQL parce que… »).

---

## Barème récapitulatif

| Épreuve | Barème | Seuil | Pondération module |
|---|---|---|---|
| A · Récupération | non noté | — | 0 % |
| B · Quiz | /15 | ≥ 11/15 | 30 % |
| C · Exercices | /20 | ≥ 14/20 | 30 % |
| D · Étude de cas | /20 | ≥ 12/20 | 40 % |
| **M06.P (projet)** | /20 | **≥ 13/20** | indépendant |

**Score module = 0,3·B + 0,3·C + 0,4·D.** Module validé si score ≥ 13/20 **et** chaque seuil
respecté. Un candidat qui échoue à D peut repasser uniquement D ; un candidat qui échoue à B
doit reprendre le module entier.
