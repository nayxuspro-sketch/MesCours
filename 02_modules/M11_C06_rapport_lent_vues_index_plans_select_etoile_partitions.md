# Module M11.C06 — Le rapport lent : vues, index, plans d'exécution, `SELECT *`, partitions

**Outils : DuckDB 1.5.5 (exécuté), SQLite (contrôle croisé, exécuté), PostgreSQL et SQL Server (cités, non exécutés — règle §1.5.
Durée indicative : 5 h. Niveau : N3 → N4. Prérequis : M11.C01 à C05 (fenêtres, cohortes, requêtes avancées) ;
M07.C06 (volumétrie) ; M09.C05 (lecture d'un plan d'exécution).**

> **L'idée du chapitre.** Un rapport juste et lent n'est pas un rapport. Sur le socle du module, la même
> question — « combien de lignes de retour ? » — coûte **142 ms** posée sur la vue et **1 ms** posée sur la
> même table recopiée en mémoire : le rapport entre les deux est **×142**, pour un résultat identique au
> chiffre près. Plus frappant encore, `SELECT *` coûte **581 ms** là où trois colonnes nommées coûtent
> **96 ms** (**×6,1**) : le plan annonce **18** colonnes lues contre **3**, et l'horloge confirme. Ce
> chapitre apprend à **lire** ces nombres avant de les subir : ce qu'une vue relit, ce qu'un `SELECT *`
> transporte, ce qu'un index change vraiment (mesuré : presque rien, en DuckDB), comment un plan se lit de
> bas en haut, et pourquoi une mesure de performance se **fige** dans un fichier daté au lieu de se relire à
> l'horloge.

> **Matériel de l'atelier — DuckDB 1.5.5 · socle M11 (`03_exercices/dossier_M11/socle_m11.sql`).**
> Les temps cités sont des **médianes de 5 exécutions**, produites par `tools/perf_M11.py` et **gelées** le
> **24/09/2026** dans `03_exercices/dossier_M11/PERF_M11.json`. Le chapitre ne relit jamais l'horloge : il
> relit ce fichier.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **Distinguer une vue d'une table** dans ses conséquences pratiques, et dire ce qu'une vue **relit** à
   chaque appel.
2. **Mesurer un protocole** : médiane de plusieurs exécutions, instrument nommé, valeurs **figées et datées**.
3. **Chiffrer le coût d'un `SELECT *`** à l'horloge **et** dans le plan d'exécution, sur une table et sur une vue.
4. **Lire un plan d'exécution** : les étages, leur ordre, le nombre de colonnes lues, et ce qu'un `SEQ_SCAN`
   annonce du travail à venir.
5. **Décider de l'utilité d'un index sur une mesure**, pas par réflexe — et savoir pourquoi un même index
   change tout dans un moteur et rien dans un autre.
6. **Arbitrer entre lisibilité et performance** quand les deux se contredisent (§5.5).
7. **Écrire la note de méthode d'un rapport** : périmètre, protocole, valeurs gelées, ce qui n'a pas été mesuré.

## 2. Pourquoi cette notion est importante

Le module M11 produit **12** rapports. Chacun d'eux lit le même socle de **240 000** lignes de ventes. Si le
rapport type met **841** ms au lieu de **277** ms — c'est-à-dire écrit sur la vue et en `SELECT *` au lieu
de la table et de trois colonnes — l'écart paraît dérisoire. Multiplié par douze rapports, par les
rafraîchissements quotidiens et par les relances de chaque utilisateur, il devient une salle d'attente.

Mais le vrai enjeu du chapitre n'est pas la vitesse : c'est la **confiance**. Un rapport dont la note de
méthode dit « médiane de 5 exécutions, DuckDB 1.5.5, valeurs figées le 24/09/2026 dans PERF_M11.json »
est un rapport **reproductible**. Un rapport dont les temps ont été copiés une fois, sans protocole, est un
rapport qu'on ne peut ni vérifier ni défendre. La performance, en BI, se **documente** avant de s'optimiser.

Enfin, le chapitre désarme un réflexe coûteux : sur ce socle, ajouter un index fait passer une recherche par
client de **0,6** ms à **0,5** ms — et le plan continue d'annoncer `SEQ_SCAN`. L'index n'est pas une bonne
pratique à appliquer partout : c'est une réponse à un problème que le **plan** doit avoir montré.

## 3. Explication simple — le classeur, le sommaire et le chariot

**La vue, c'est un raccourci vers le classeur.** Chaque fois qu'on ouvre le raccourci, il faut ressortir le
classeur et le relire. La table, c'est le tableau recopié sur le bureau : on l'a payé une fois (la copie) et
on le consulte gratuitement ensuite. Sur le socle : **142** ms à chaque appel de la vue, **1** ms pour la
table équivalente.

**Le `SELECT *`, c'est le chariot trop large.** Demander toutes les colonnes d'une table large revient à
sortir du magasin les **18** rayons pour n'utiliser que **3** produits. Le plan le dit avant l'exécution :
**18** colonnes lues au lieu de **3**, et l'horloge confirme (**581** ms contre **96**).

**Le plan d'exécution, c'est la fiche de préparation du cuisinier.** Avant de cuisiner, il annonce :
« je vais chercher les fichiers, les joindre, les regrouper, projeter les colonnes ». Trois étages sur le
socle (`HASH_GROUP_BY`, `PROJECTION`, `HASH_JOIN`), lus **de bas en haut**. On ne discute pas une
performance sans cette fiche.

**L'index, c'est l'index alphabétique d'un dictionnaire.** Utile pour trouver **une** page précise, inutile
pour lire le dictionnaire entier. Sur DuckDB — un moteur en colonnes — la recherche d'un client reste un
`SEQ_SCAN` : le moteur lit la colonne entière, et cela lui coûte moins que de naviguer dans un index. Sur
SQLite — un moteur en lignes — le même index **remplace** le balayage complet : le plan passe de
« `SCAN ventes_t` » à « `SEARCH ventes_t USING INDEX idx_ventes_client (id_client=?)` ».

## 4. Vocabulaire essentiel

| Terme (français) | Équivalent anglais | Définition en une phrase |
|---|---|---|
| **vue** | *view* | Une requête nommée ; elle ne contient pas de données et **relit** sa source à chaque appel. |
| **matérialisation** | *materialization* | Le fait de copier le résultat d'une vue dans une table, pour ne le calculer qu'une fois. |
| **table en mémoire** | *in-memory table* | Une table dont les données sont copiées dans la mémoire du moteur : rapide, mais rien n'est persisté. |
| **plan d'exécution** | *execution plan* | Le programme que le moteur se propose d'exécuter : les opérateurs, leur ordre et les colonnes lues. |
| **étage** | *operator / stage* | Un opérateur du plan : `SEQ_SCAN`, `HASH_JOIN`, `HASH_GROUP_BY`, `PROJECTION`, `ORDER_BY`. |
| **balayage séquentiel** | *sequential scan* | Lire toute une colonne, ligne après ligne : le mode normal d'un moteur en colonnes. |
| **index** | *index* | Une structure de recherche par valeur : indispensable en moteur en lignes, souvent ignorée en colonnes. |
| **projection** | *projection* | La liste des colonnes réellement lues et transmises aux étages suivants. |
| **coût du `SELECT *`** | *star-select overhead* | Le travail de lecture de colonnes inutilisées, visible dans la projection du plan. |
| **médiane de 5** | *median of 5 runs* | Le protocole de mesure retenu : cinq exécutions, on publie la valeur médiane. |
| **valeur gelée** | *frozen measurement* | Un temps machine écrit dans un fichier daté, que la prose relit au lieu de relancer l'horloge. |
| **partition** | *partition* | Un découpage physique des données (par date, par magasin) qui permet de ne pas lire ce dont on n'a pas besoin. |

> **Définition.** Le **plan d'exécution** est la description, par le moteur, de ce qu'il va faire : les
> opérateurs, leur ordre d'enchaînement et les colonnes lues. Il se demande par `EXPLAIN` **avant**
> l'exécution — et c'est ce qui en fait l'outil d'un analyste : il annonce le coût sans faire le travail. Sur
> le socle, le croisement magasin / chiffre d'affaires se prépare en **3** étages : `HASH_GROUP_BY`,
> `PROJECTION`, `HASH_JOIN`.

> **Définition.** Une **vue** ne stocke pas de données : c'est une requête à laquelle on a donné un nom. Sa
> conséquence pratique est immense et souvent ignorée : **chaque appel relit la source**. Sur le socle, la
> vue `ventes` relit le CSV des ventes ; compter les retours coûte **142** ms sur la vue contre **1** ms sur
> la table équivalente — soit **×142** pour un résultat identique.

> **Définition.** Un **index** est une structure de recherche par valeur, qui évite de parcourir toutes les
> lignes. Il n'est **pas** universel : son utilité dépend du moteur (lignes ou colonnes), de la requête
> (recherche ponctuelle ou agrégat) et de la sélectivité. La seule façon honnête de trancher est de lire le
> plan et de mesurer : sur ce socle, l'index ne change ni le plan de DuckDB ni ses temps.

> **Définition.** Le **coût du `SELECT *`** est le travail de lecture des colonnes qui ne serviront pas à la
> sortie. Il se lit dans la **projection** du plan — **18** colonnes lues pour un `SELECT *`, **3** pour
> trois colonnes nommées — et se vérifie à l'horloge (**581** ms contre **96** ms). C'est le gaspillage le
> plus fréquent des rapports, et le plus simple à corriger.

## 5. Cours approfondi

### 5.1 La vue : ce qu'elle relit, à chaque fois

Le socle du module est une suite de vues posées sur des CSV. C'est un choix assumé (aucun fichier de base à
versionner, voir §5.6), mais il a un prix :

```sql
-- sur la vue : le CSV est relu à chaque appel
SELECT COUNT(*) FROM ventes WHERE est_retour;
-- sur la table équivalente, recopiée en mémoire
CREATE OR REPLACE TABLE ventes_m AS SELECT * FROM ventes;
SELECT COUNT(*) FROM ventes_m WHERE est_retour;
```

| Mesure | Sans matérialisation | Avec matérialisation | Rapport |
|---|---|---|---|
| Comptage des retours | **142** ms (vue) | **1** ms (table) | **×142** |
| `SELECT *` | **841** ms (vue) | **581** ms (table) | **×1,4** |
| 3 colonnes nommées | **277** ms (vue) | **96** ms (table) | **×2,9** |

La dernière ligne mérite attention : sur la **vue**, `SELECT *` coûte **×3,0** de plus que trois colonnes
(**841** contre **277**) ; sur la **table**, l'écart est de **×6,1** (**581** contre **96**). Le gaspillage des
colonnes est donc plus visible quand la lecture de fichier ne le masque pas.

### 5.2 `SELECT *` : le lire dans le plan, pas seulement au chronomètre

Deux requêtes, un seul chiffre d'affaires attendu :

```sql
EXPLAIN SELECT * FROM ventes_m;
EXPLAIN SELECT date_vente, id_magasin, montant_ttc FROM ventes_m;
```

Le premier plan annonce **18** colonnes lues, le second **3**. Le rapport est de **×6** — et il est **écrit
dans le plan**, vérifiable sans exécuter. À l'horloge : **581** ms contre **96** ms, soit **×6,1**. Le plan
avait raison avant la mesure, et c'est exactement l'intérêt de le lire : on peut refuser une requête avant
de payer son temps.

> **Dans les faits.** Le plan annonce **×6** de colonnes, l'horloge mesure **×6,1**. C'est la démonstration la
> plus utile du chapitre pour un débutant : la lecture d'un plan n'est pas un rituel de spécialiste, c'est
> un **devis** — proposé gratuitement par le moteur avant chaque requête.

### 5.3 Lire un plan : trois étages, de bas en haut

```sql
EXPLAIN SELECT m.nom, SUM(v.montant_ttc)
FROM ventes_m v JOIN magasin m USING (id_magasin) GROUP BY 1;
```

```text
HASH_GROUP_BY
  PROJECTION
    HASH_JOIN
```

**3** étages : le moteur joint les ventes et les magasins (`HASH_JOIN`), projette les colonnes utiles
(`PROJECTION`), puis regroupe (`HASH_GROUP_BY`). La lecture se fait **de bas en haut** : les données
remontent l'arbre, chaque étage transmettant son résultat à celui du dessus. Trois questions suffisent pour
auditer un plan :

1. **Combien de colonnes** chaque lecture annonce-t-elle ? (les projections, §5.2)
2. **Quel opérateur domine** ? Un `SEQ_SCAN` sur une table large précède presque toujours un plan lent.
3. **Y a-t-il un étage inutile** ? Une jointure ou un tri qui ne servent à aucune réponse du rapport.

### 5.4 L'index : mesuré, puis contrôlé dans un second moteur

Sur le socle matérialisé, on cherche un client précis et on agrège par magasin :

| Requête | Sans index | Avec index | Effet |
|---|---|---|---|
| Recherche par client (**15676**) | **0,6** ms | **0,5** ms | aucun effet mesurable |
| Agrégat par magasin | **1,5** ms | **1,5** ms | aucun effet |
| Plan de la recherche | `SEQ_SCAN` | `SEQ_SCAN` | l'index n'est **pas** utilisé |

DuckDB est un moteur **en colonnes** : lire une colonne entière de **240 000** valeurs compactées coûte moins
que parcourir un index. Le contrôle croisé dans un moteur **en lignes** renverse la conclusion :

```text
SQLite, 240 000 lignes chargées en mémoire
sans index : SCAN ventes_t
avec index : SEARCH ventes_t USING INDEX idx_ventes_client (id_client=?)
réponse    : 14 lignes et 5 578 688 FCFA pour le client 15676
```

Le même index, la même requête, le même résultat — et un plan qui change du tout au tout. La leçon n'est pas
« l'index est inutile », elle est « l'index est une réponse à un plan » : on regarde le plan, on voit un
balayage complet qui coûte, on indexe, on remesure.

> **Attention.** Une colonne indexée dans un moteur en lignes peut ralentir les **écritures** : chaque
> insertion met l'index à jour. Sur un rapport de lecture, l'arbitrage est simple ; sur une table alimentée
> en continu, il se mesure des deux côtés — et se documente.

### 5.5 Lisibilité contre performance : le cas de la fenêtre

Toutes les écritures lisibles ne sont pas les plus rapides. Le module l'a mesuré sur la question la plus
fréquente de C01 — la part d'une ligne dans son ensemble :

| Écriture | Temps | Avantage |
|---|---|---|
| Fonction de fenêtre (`SUM(...) OVER ()`) | **150** ms | une seule requête, une seule passe à écrire, robuste au filtre ajouté |
| Sous-requête scalaire | **292** ms | aucune |

La fenêtre est **×1,9** plus rapide **et** plus lisible : ici, les deux critères vont dans le même sens. Ce
n'est pas toujours le cas — une CTE bien nommée peut être recalculée plusieurs fois. La règle du chapitre
n'est donc pas « préférer le plus lisible » : c'est **mesurer avant de choisir**, puis écrire le choix.

> **Attention.** Un temps machine n'est pas reproductible au bit près : le premier appel paie la lecture du
> fichier, les suivants non, et la machine hôte varie. C'est pourquoi le protocole est **publié** (médiane de
> **5** exécutions) et pourquoi les valeurs sont **gelées** dans un fichier daté — `PERF_M11.json`, figé le
> **24/09/2026** par `tools/perf_M11.py --figer`. Un rapport qui relit l'horloge à chaque exécution publie un
> chiffre différent chaque matin, et ne peut plus être comparé à lui-même.

### 5.6 Matérialiser ou non : le plancher d'un fichier

On pourrait écrire le socle matérialisé sur le disque une fois pour toutes. Le coût de ce confort est
mesurable : un fichier DuckDB qui ne contient **qu'une** table de **154** lignes pèse **536 576** octets. Ce
plancher fixe interdit de versionner la base du module — c'est pour cela que le socle M11 est un **script**
(`socle_m11.sql`) qui reconstruit les vues et les tables de référence en une fraction de seconde, et que les
démonstrations de volume se font **en mémoire** (`ouvrir(materialiser=True)` dans
`03_exercices/dossier_M11/connexion.py`).

> **Conseil professionnel.** Mesurez **avant** d'optimiser, et écrivez la mesure **dans** le rapport.
> Une note de trois lignes — « ce rapport lit la vue (donc le CSV) et dix-huit colonnes ; en nommant trois
> colonnes il passe de **581** ms à **96** ms ; l'index n'apporte rien ici » — vaut mieux qu'un rapport
> rapide et muet. Six mois plus tard, c'est cette note qui empêchera un collègue d'ajouter un index inutile
> ou de croire que le rapport était lent « pour de bonnes raisons ».

### 5.7 Les partitions

Le **partitionnement** découpe physiquement les données — par année, par magasin — pour qu'une requête ne
lise que les partitions concernées. Trois familles d'usage : le partitionnement **Hive** sur des fichiers
(dossier `annee=2026/mois=08/`), les tables partitionnées de PostgreSQL et SQL Server, et les filtres de
partition dans les moteurs analytiques.

> **Attention.** Le partitionnement est **cité, non exécuté** dans ce chapitre : le socle de l'atelier n'a ni
> le volume ni le disque pour qu'une mesure soit interprétable. Aucun plan de partition n'est donc publié
> ici — un chapitre qui montre un plan qu'il n'a pas lu fabrique une preuve, ce que ce manuel interdit
> depuis le premier module (§1.5).

### 5.8 La note de méthode d'un rapport de performance

Tout rapport de performance doit pouvoir répondre à cinq questions, et les cinq tiennent en quatre lignes :

1. **Quel moteur et quelle version ?** DuckDB 1.5.5, sur l'atelier.
2. **Quel protocole ?** Médiane de **5** exécutions, requête complète, résultat consommé.
3. **Quand ?** Le **24/09/2026**.
4. **Où sont les valeurs ?** `03_exercices/dossier_M11/PERF_M11.json`, produit par `tools/perf_M11.py`.
5. **Qu'est-ce qui n'a pas été mesuré ?** Les partitions, PostgreSQL et SQL Server — cités, non exécutés.

## 6. Exemple concret — la facture d'un rapport mal écrit

Un rapport quotidien lit le socle et publie le chiffre d'affaires par magasin avec sa part. Deux écritures,
mesurées :

| Version | Écriture | Temps | Sur 12 rapports × 3 exécutions |
|---|---|---|---|
| A | vue + `SELECT *` + sous-requête scalaire | ≈ **841** ms + **292** ms | ≈ **41** s |
| B | table matérialisée + 3 colonnes + fenêtre | ≈ **96** ms + **150** ms | ≈ **9** s |

Le même contenu, la même justesse, et un facteur **4,5** — sans changer une seule ligne de logique métier,
seulement la **forme** de la lecture. C'est le résultat le plus utile du chapitre : la première optimisation
d'un rapport n'est presque jamais un index, c'est de **lire ce qu'on utilise**.

## 7. Démonstration pas à pas — six étapes sur le socle

### 7.1 Étape 1 — le protocole d'abord

Cinq exécutions, on publie la médiane, et l'instrument est nommé : `tools/perf_M11.py`. Sans protocole, un
temps ne vaut rien.

### 7.2 Étape 2 — la vue contre la table

**142** ms contre **1** ms (**×142**) pour compter les retours. La vue relit le CSV ; la table est en mémoire.

### 7.3 Étape 3 — le plan du `SELECT *`

**18** colonnes annoncées contre **3**, **×6** dans le plan et **×6,1** à l'horloge (**581** ms contre
**96** ms). Le devis du moteur suffisait à trancher.

### 7.4 Étape 4 — l'index, mesuré puis contrôlé

**0,6** ms contre **0,5** ms, agrégat inchangé, plan toujours `SEQ_SCAN` : en DuckDB, aucun effet. Le
contrôle croisé SQLite montre un plan qui passe de `SCAN ventes_t` à `SEARCH ventes_t USING INDEX
idx_ventes_client (id_client=?)` — et le même résultat, **14** lignes et **5 578 688** FCFA pour le client
**15676**.

### 7.5 Étape 5 — fenêtre contre sous-requête

**150** ms contre **292** ms (**×1,9**) pour la même part : ici, la forme la plus lisible est aussi la plus
rapide.

### 7.6 Étape 6 — le plancher de matérialisation

**536 576** octets pour une table de **154** lignes : rien ne justifie de versionner une base là où un script
de reconstruction suffit.

## 8. Erreurs fréquentes

1. **Optimiser sans mesurer.** Ajouter un index par réflexe n'a **aucun** effet mesurable sur ce socle
   (**0,6** ms contre **0,5** ms) et le plan reste `SEQ_SCAN` : le travail n'est pas là où on le croyait.
   C'est mesurer d'abord, écrire ensuite.
2. **Publier un temps sans protocole.** Un chiffre isolé, sans version de moteur, sans nombre d'exécutions et
   sans date, n'est pas une mesure : c'est une anecdote. Le protocole tient en une ligne (**médiane de 5**,
   DuckDB 1.5.5, **24/09/2026**, `PERF_M11.json`).
3. **Laisser `SELECT *` dans un rapport.** **581** ms contre **96** ms, **18** colonnes contre **3** : le
   gaspillage est dans le plan, donc évitable sans exécuter.
4. **Confondre vue et table dans l'estimation d'un coût.** Le même comptage vaut **142** ms ou **1** ms selon
   la source : annoncer « ce rapport coûte 1 ms » en l'ayant mesuré sur la table, pour un rapport qui lit la
   vue, est un chiffre faux.
5. **Recopier les temps d'un autre moteur.** Un index qui transforme un plan SQLite (`SEARCH`) ne change rien
   à un plan DuckDB (`SEQ_SCAN`) : les conclusions ne se transportent pas.
6. **Relire l'horloge dans un rapport.** Deux exécutions doivent donner le même document ; un temps mesuré
   « en direct » fait varier le rapport d'un jour à l'autre sans qu'aucune donnée n'ait changé.

## 9. Bonnes pratiques professionnelles

1. **Écrire le protocole avant le chiffre.** Médiane de **5** exécutions, version du moteur, date, instrument
   nommé : la même phrase que celle du fichier `PERF_M11.json`.
2. **Geler les valeurs, dater le fichier.** `tools/perf_M11.py --figer` écrit le JSON ; la prose le relit.
   C'est ce qui rend deux relevés identiques sur une machine plus lente.
3. **Lire le plan avant d'optimiser.** Le devis est gratuit : **18** contre **3** colonnes annoncées, pour
   **581** contre **96** ms mesurées.
4. **Nommer ses colonnes.** `SELECT date_vente, id_magasin, montant_ttc` plutôt que `SELECT *` : même réponse,
   **×6** de travail en moins.
5. **Déclarer ce qui n'a pas été mesuré.** Les partitions, PostgreSQL et SQL Server sont **cités** ici ; c'est
   écrit dans la note de méthode et dans le corps du chapitre.

## 10. Exercice guidé

**Situation.** Un rapport de suivi met **841** ms sur la machine de l'analyste. Le collègue en conclut :
« il faut indexer la table des ventes ».

**Consigne.**

1. Reproduisez la mesure et donnez le protocole complet (moteur, nombre d'exécutions, date, instrument).
   (2 pts)
2. Montrez, plan à l'appui, ce que la requête lit réellement, et quelle correction simple divise son coût.
   (3 pts)
3. Mesurez l'effet de l'index proposé par le collègue, et rédigez la réponse à lui faire en deux phrases.
   (3 pts)
4. Ajoutez la ligne de note de méthode que ce rapport doit porter. (2 pts)

## 11. Exercices autonomes

**E1 — La même question, deux sources (40 min).** Mesurez le comptage des retours sur la vue puis sur la
table matérialisée, cinq fois chacune, et publiez la médiane. Puis répondez en quatre lignes : de combien le
rapport est-il plus rapide, et que faut-il écrire dans la note de méthode pour que ce gain soit vérifiable
par quelqu'un d'autre.

**E2 — L'index, dans les deux moteurs (40 min).** Reproduisez la mesure d'index en DuckDB, puis le contrôle
croisé en SQLite : relevez les deux plans et le résultat identique. Terminez par trois conseils destinés à un
analyste qui doit décider d'indexer — trois phrases, une par critère (moteur, requête, écriture).

## 12. Correction détaillée

**Exercice guidé.**

1. **La mesure.** Comptage des retours sur la vue : médiane de **5** exécutions, DuckDB 1.5.5, atelier,
   **24/09/2026**, instrument `tools/perf_M11.py` — **841** ms si la requête prend aussi `SELECT *`, et
   **142** ms pour le seul comptage sur la vue.
2. **Le plan.** `EXPLAIN SELECT * FROM ventes_m` annonce **18** colonnes lues, contre **3** pour la version
   nommée : la correction est d'**écrire les colonnes**, ce qui ramène la mesure de **581** ms à **96** ms
   (**×6,1**).
3. **L'index.** Sans index **0,6** ms, avec index **0,5** ms, agrégat **1,5** ms dans les deux cas, et le plan
   reste un `SEQ_SCAN` : « l'index n'est pas le problème : le rapport relit la vue et lit dix-huit colonnes
   pour en utiliser trois ; corrigeons la lecture, puis remesurons. »
4. **La note de méthode.** « Médiane de **5** exécutions, DuckDB 1.5.5, atelier, valeurs figées le
   **24/09/2026** dans `03_exercices/dossier_M11/PERF_M11.json` ; partitions, PostgreSQL et SQL Server cités,
   non exécutés. »

**E1 (deux sources).** **142** ms contre **1** ms, soit **×142** : le gain est réel mais **conditionnel** — il
suppose que la table soit déjà matérialisée, ce qui a un coût (mémoire) et une durée de vie (le temps de la
session). La note de méthode doit donc dire **quand** la table est créée et **ce qui se passe** si elle ne
l'est pas : un gain non déclaré se transforme en régression chez le collègue qui exécute le rapport sans
matérialisation.

**E2 (deux moteurs).** Trois critères : le **moteur** (DuckDB en colonnes ignore l'index, SQLite en lignes
l'utilise) ; la **requête** (recherche ponctuelle ou agrégat complet : un agrégat ne profite pas d'un index) ;
l'**écriture** (chaque index ralentit les insertions — à mesurer sur une table alimentée). Le contrôle
croisé donne le même résultat dans les deux moteurs — **14** lignes et **5 578 688** FCFA pour le client
**15676** — ce qui est la moindre des choses : un index ne change pas la réponse, il change le **chemin**.

## 13. Mini-projet de chapitre

**La note de performance d'un rapport, 2 pages.** Choisissez l'un des **12** rapports du projet de module.
Mesurez-le sur la vue et sur la table, avec et sans `SELECT *`, et produisez sa note de performance.

**Livrables et barème.**

| Critère | Ce qui est vérifié | Points |
|---|---|---|
| Le protocole | médiane de 5 exécutions, moteur et version, date, instrument nommé | 5 |
| Les mesures | deux sources × deux façons d'écrire la projection, valeurs publiées | 5 |
| Le plan | lecture commentée du plan de la requête (étages, colonnes lues) | 4 |
| La note de méthode | ce qui a été mesuré, ce qui ne l'a pas été, et la décision d'optimisation | 4 |
| **Total** | | **18** |

## 14. Résumé du chapitre

La performance d'un rapport se **lit** avant de se mesurer, et se **mesure** avant de s'optimiser. Sur le
socle du module : une vue relit sa source et coûte **142** ms là où la table équivalente coûte **1** ms
(**×142**) ; `SELECT *` lit **18** colonnes au lieu de **3**, ce que le plan annonce (**×6**) et que
l'horloge confirme (**581** ms contre **96** ms, **×6,1**) ; un index ne change **rien** en DuckDB (**0,6** ms
contre **0,5** ms, plan toujours `SEQ_SCAN`) mais transforme le plan SQLite en `SEARCH`, pour la même
réponse (**14** lignes, **5 578 688** FCFA) ; une fenêtre coûte **150** ms là où la sous-requête scalaire en
coûte **292** (**×1,9**), alliant ici lisibilité et vitesse ; et matérialiser a un plancher
(**536 576** octets pour **154** lignes), ce qui justifie un socle en script plutôt qu'en fichier. Enfin,
aucun de ces chiffres ne serait publiable sans protocole : médiane de **5** exécutions, DuckDB 1.5.5,
valeurs gelées le **24/09/2026** dans `PERF_M11.json`.

## 15. À retenir

1. **Une vue relit sa source à chaque appel.** **142** ms contre **1** ms pour le même comptage.
2. **Le `SELECT *` se voit dans le plan avant de coûter.** **18** colonnes annoncées contre **3**.
3. **Le plan se lit de bas en haut**, et trois questions suffisent : colonnes lues, opérateur dominant,
   étage inutile. Sur le socle : **3** étages.
4. **L'index est une réponse à un plan, pas une habitude.** Aucun effet mesurable en DuckDB ; plan transformé
   en SQLite.
5. **Un temps sans protocole n'est pas une mesure.** Médiane de **5** exécutions, moteur, date, instrument.
6. **Les valeurs de performance se gèlent dans un fichier daté.** Deux exécutions du relevé doivent donner
   le même document.
7. **La première optimisation est de lire ce qu'on utilise** — pas d'ajouter un index.

> **À retenir.** Le chiffre qui résume le chapitre est un écart entre deux façons d'écrire la même question :
> **×6,1**. Rien n'a changé dans le métier — seul le nombre de colonnes lues a changé. C'est l'optimisation la
> moins coûteuse et la plus souvent oubliée.

> **À retenir.** Le protocole fait partie du résultat. « **0,5** ms » sans protocole ne vaut rien ; « médiane
> de **5** exécutions, DuckDB 1.5.5, **24/09/2026**, `PERF_M11.json` » se vérifie, se compare et se défend.

## 16. Évaluation formative

Répondez sans machine, puis vérifiez avec l'atelier (5 minutes) :

1. Combien coûte le comptage des retours sur la vue, et sur la table équivalente ?
2. Combien de colonnes le plan annonce-t-il pour un `SELECT *`, et combien pour trois colonnes nommées ?
3. Quels sont les trois étages du plan du croisement magasin / chiffre d'affaires ?
4. Quels temps et quels plans donnent la recherche par client, avec et sans index, en DuckDB ?
5. Que répond le plan SQLite de la même recherche, sans index puis avec ?
6. Quel résultat commun les deux moteurs renvoient-ils pour le client 15676 ?
7. Que coûtent la fenêtre et la sous-requête scalaire sur la même part, et lequel des deux est le plus lisible ?
8. Combien pèse un fichier DuckDB contenant une table de 154 lignes, et qu'en déduit-on pour le socle du module ?
9. Que contient une note de méthode de performance, en cinq points ?
10. Pourquoi les valeurs de performance du module sont-elles gelées dans un fichier, et de quelle date ?

**Réponses.** 1. **142** ms sur la vue, **1** ms sur la table (**×142**). 2. **18** contre **3** (rapport
**×6** dans le plan, **×6,1** à l'horloge : **581** ms contre **96** ms). 3. `HASH_GROUP_BY`, `PROJECTION`,
`HASH_JOIN`. 4. **0,6** ms sans index, **0,5** ms avec, plan `SEQ_SCAN` dans les deux cas. 5. `SCAN ventes_t`
puis `SEARCH ventes_t USING INDEX idx_ventes_client (id_client=?)`. 6. **14** lignes et **5 578 688** FCFA.
7. **150** ms pour la fenêtre, **292** ms pour la sous-requête scalaire (**×1,9**) : la fenêtre est aussi la
plus lisible. 8. **536 576** octets — un plancher fixe : le socle reste un script plutôt qu'un fichier de
base. 9. Moteur et version, protocole, date, emplacement des valeurs, et ce qui n'a pas été mesuré.
10. Pour que deux exécutions du relevé donnent le même document ; elles sont gelées le **24/09/2026** dans
`PERF_M11.json`.
