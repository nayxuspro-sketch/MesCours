# Module M13.C04 — Le schéma en étoile et les changements lents

![La frise des quatre types de changement lent : un tarif qui monte de 24 % en quatre ans, ce que type 0, type 1, type 2 et type 3 gardent de cette histoire, et ce que coûte la lecture du passé (production : `tools/figures_M13.py`)](../figures/M13_C04_frise_scd.svg)

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **reconnaître une étoile** et dire ce qui la distingue d'un schéma en flocon : une table de faits
   au centre, des dimensions autour, et **une seule jointure** pour atteindre un attribut ;
2. **repérer une dimension conforme** et la mesurer : `dim_magasin` sert **5** des **7** tables de
   faits du fil rouge, `dim_client` et `dim_produit` en servent **3** chacune — c'est ce qui rend deux
   rapports comparables ;
3. **distinguer les quatre types de changement lent** (SCD **0**, **1**, **2**, **3**) et **choisir**
   le bon selon ce que l'historique doit permettre : sur le socle, **980** mouvements sont des
   versions (type 2) et **140** des corrections (type 1) ;
4. **écrire la requête « au moment du fait »** — une jointure par intervalle, et non par égalité de
   clé — puis **vérifier** qu'elle rend exactement **240 000** lignes pour **240 000** ventes, sans
   doublon ni perte ;
5. **mesurer ce que l'historique change** : le même chiffre d'affaires par segment vaut
   **7 838 286 840** FCFA lu sur la dimension courante et **7 735 369 260** FCFA lu sur la dimension
   historisée — **102 917 580** FCFA d'écart sur un seul segment.

---

## 2. Pourquoi cette notion est importante

Le chapitre C03 a fixé le grain : chaque table de faits dit ce qu'elle compte. Il reste à savoir
**autour de quoi** elle le compte.

Une table de faits ne contient que des clés et des mesures : `id_client`, `id_produit`, `id_magasin`,
un montant, une quantité. Toutes les questions qu'on pose à un rapport — *par segment*, *par région*,
*par famille de produits* — passent par une **dimension**. C'est la dimension qui porte le sens
métier, et c'est elle qui pose le problème que ce chapitre résout : **les attributs changent**.

Le fil rouge en donne la mesure exacte. Le référentiel clients contient **1 120** mouvements : **980**
changements d'état (un client change de ville, ou passe du segment Argent au segment Or) et **140**
corrections de saisie. Si la dimension écrase tout — un client, une seule ligne, toujours à jour —,
alors les ventes de 2023 sont attribuées à la ville **d'aujourd'hui**, et le chiffre d'affaires par
segment devient faux de **102 917 580** FCFA. Personne ne le verra : le rapport s'affiche, les
segments se somment au total, et le total est juste. Seule la **répartition** est fausse.

> **Dans les faits.** L'écart mesuré sur le fil rouge est de **102 917 580** FCFA, et il ne porte que
> sur la répartition : le total des trois segments est identique dans les deux lectures
> (**15 595 154 955** FCFA). C'est le pire genre de défaut — celui qu'aucun contrôle de total ne
> détecte. Trois segments, dont deux se déplacent de **34** à **61** millions de francs, et un
> tableau de bord qui attribue à la mauvaise région l'effort commercial de l'année.

Ce chapitre construit donc la partie du modèle qui **gère le temps qui passe** : les dimensions
historisées. C05 complétera l'étoile quand elle ne suffit plus (flocon, table de pont, faits
multiples), C06 branchera le calendrier, C07 vérifiera et documentera l'ensemble.

---

## 3. Explication simple — l'étoile, la fiche et la photographie

**L'étoile.** Imaginez un entrepôt de quincaillerie. Au centre, un comptoir où l'on enregistre chaque
mouvement : *telle date, tel client, tel produit, tel magasin, telle quantité, tel montant*. Autour du
comptoir, quatre classeurs : le classeur des clients, celui des produits, celui des magasins, celui
des vendeurs. Le registre central ne recopie pas les adresses et les désignations — il écrit un
**numéro de fiche**. Pour savoir quelle famille de produits a été vendue, on ouvre le classeur des
produits à la bonne fiche. Une jointure, et l'on sait. C'est une **étoile**.

**La fiche.** Chaque fiche porte plusieurs attributs : pour un client, sa ville, son segment, ses
conditions de paiement. Ces attributs ne sont pas de même nature. Certains ne changeront **jamais**
(la date de création du compte) : c'est le **type 0**. D'autres sont des **erreurs de saisie** qu'on
corrige (un « 30 j » noté avec une espace finale) : on écrase l'ancienne valeur, c'est le **type 1**.
D'autres encore **changent pour de vrai** (le client déménage, il devient un gros client) : là, on
garde l'ancienne fiche **et** la nouvelle, en datant chacune — c'est le **type 2**, celui qui porte
l'histoire.

**La photographie.** Le type 2 revient à photographier la fiche chaque fois qu'elle change, et à
inscrire au dos de chaque photo la période pendant laquelle elle était vraie. Le client **2 030** a
trois photos : *Koudougou du 2020-03-06 au 2023-06-08*, *Kaya du 2023-06-09 au 2025-08-22*,
*Ouagadougou depuis le 2025-08-23*. Quand vous vendez quelque chose à ce client, vous ne lui donnez pas
« sa » ville : vous lui donnez la ville de **la photo en vigueur ce jour-là**.

Le **type 3**, enfin, est une variante paresseuse : au lieu de garder toutes les photos, on garde
seulement la valeur actuelle et la précédente, dans deux colonnes. Sur le fil rouge, **4** clients ont
changé **3** fois de ville : le type 3 perdrait la première, et il aurait fallu une colonne par
changement possible.

---

## 4. Vocabulaire essentiel

| Terme | Définition | Sur le fil rouge |
|---|---|---|
| **Schéma en étoile** | une table de faits au centre, des dimensions autour, une jointure par attribut | **7** faits, **5** dimensions |
| **Dimension conforme** | dimension partagée par plusieurs tables de faits | `dim_magasin`, **5** faits |
| **Attribut de dimension** | colonne descriptive d'un objet (ville, segment, famille) | `segment`, `ville`, `famille` |
| **Hiérarchie** | niveaux d'agrégation d'une dimension | produit, sous-catégorie (**12**), famille (**7**) |
| **SCD** | *Slowly Changing Dimension* : changement lent de dimension | les **4** types ci-dessous |
| **SCD type 0** | attribut qui ne change jamais | `date_creation`, `nom` |
| **SCD type 1** | on **écrase** l'ancienne valeur (correction) | **140** mouvements (ville, conditions) |
| **SCD type 2** | on **ajoute une version**, datée et conservée | **980** mouvements, **24 892** versions |
| **SCD type 3** | on garde la valeur **précédente** dans une colonne | insuffisant ici : **4** clients à **3** villes |
| **Version courante** | la ligne ouverte, sans date de fin | `est_courante = 1` |
| **Clé de version** | identifiant de la version d'un objet | `cle_version` : `12-4` |
| **Jointure par intervalle** | jointure sur `date BETWEEN date_debut AND date_fin` | **240 000** lignes, aucune perte |

> **Définition.** Un **schéma en étoile** est un modèle où une table de faits, au grain unique,
> pointe par des clés étrangères vers des tables de dimensions qui décrivent le *qui*, le *quoi* et
> le *où*. Pour atteindre un attribut, une seule jointure suffit.

> **Définition.** Une **dimension conforme** est une dimension **partagée** par plusieurs tables de
> faits : les mêmes valeurs, la même clé, la même signification. C'est la condition pour que deux
> rapports construits sur deux processus différents parlent des mêmes objets — et donc pour qu'ils
> soient comparables.

> **Définition.** Un **changement lent de dimension** (*Slowly Changing Dimension*, SCD) est la
> manière dont un modèle traite la modification d'un attribut de dimension : ne rien faire (type 0),
> écraser (type 1), versionner (type 2), ou garder la valeur précédente (type 3).

> **Définition.** Une **dimension historisée** (ou dimension de type 2) est une dimension dont
> chaque ligne porte une **période de validité** (`date_debut`, `date_fin`) et un indicateur de
> version courante. Chaque objet peut donc y apparaître plusieurs fois, à des périodes différentes.

> **Définition.** La **jointure au moment du fait** est la jointure entre une table de faits et une
> dimension historisée qui rend l'attribut **tel qu'il était** à la date du fait : elle porte sur un
> intervalle, pas sur une égalité de clé.

---

## 5. Cours approfondi

### 5.1 L'étoile, et pourquoi pas autre chose

Un schéma en étoile se reconnaît à trois signes : une table de faits au centre, des dimensions tout
autour, et **une seule jointure** pour aller d'une mesure à un attribut. Sa force n'est pas
esthétique, elle est mécanique : moins de jointures, moins d'occasions de se tromper, et des
jointures qui restent compréhensibles par un lecteur qui découvre le modèle.

Le fil rouge s'y range exactement : **7** tables de faits, **5** dimensions, **8** clés étrangères
déclarées. Les faits portent les mesures et les clés ; les dimensions portent les attributs. Aucune
table intermédiaire, aucun attribut recopié dans les faits.

### 5.2 Les dimensions conformes, mesurées

Une dimension conforme est une dimension **partagée**. Le socle permet de la mesurer, fait par fait :

| Dimension | Nombre de faits servis | Lesquels |
|---|---|---|
| `dim_magasin` | **5** | ventes, commandes, ruptures, logistique, objectifs |
| `dim_client` | **3** | ventes, commandes, encaissements |
| `dim_produit` | **3** | ventes, stock mensuel, ruptures |
| `dim_vendeur` | **1** | ventes |
| `dim_date` | **0** | aucun fait ne pointe dessus par clé |

Ce tableau se lit comme une carte des comparaisons possibles. Parce que `dim_magasin` est conforme, on
peut mettre côte à côte le chiffre d'affaires, les ruptures, le coût logistique et l'objectif d'un
même magasin — quatre processus différents, un seul objet, donc un seul découpage. Parce que
`dim_vendeur` n'est servie que par les ventes, aucun rapport ne pourra confronter un vendeur à ses
coûts logistiques : la dimension n'a pas été conçue pour cela.

> **Attention.** `dim_date` existe, elle est juste (**1 339** jours, avec trimestres, semaines et
> jours fériés) et **aucun fait ne pointe dessus par clé** : les ventes portent une date inline. Le
> trou est déclaré, pas caché ; c'est le chapitre C06 qui le fermera, en branchant le calendrier sur
> les faits. En attendant, un rapport qui veut agréger par trimestre doit dériver le trimestre de la
> date — ce que le calendrier aurait évité.

### 5.3 Attributs et hiérarchies : ce qu'une dimension porte

Une dimension porte des **attributs** (des colonnes descriptives) et souvent une **hiérarchie** (des
niveaux qui s'emboîtent). Sur le fil rouge :

- `dim_produit` — **154** produits, **12** sous-catégories, **7** familles : trois niveaux, deux pas
  de jointure pour aller de la mesure au niveau le plus agrégé ;
- `dim_magasin` — **6** magasins, **4** villes, **4** régions ;
- `dim_client` — **23 913** lignes (les **23 912** clients plus la ligne « client non identifié »),
  avec type, segment, ville, région, conditions de paiement.

Deux règles de modélisation se déduisent de cette description. D'abord, **un attribut appartient à une
dimension, jamais aux faits** : recopier la ville du client dans les ventes reviendrait à la figer à
la date de la vente, ce que le §5.5 va exploiter. Ensuite, **une hiérarchie se déclare** : personne ne
devine que `famille` est au-dessus de `sous_categorie` — cela s'écrit dans la documentation de la
dimension.

### 5.4 Les quatre types de changement lent

Voici la partie du chapitre qui décide de ce qu'un rapport pourra dire du passé. Les quatre types, sur
le socle, sont mesurables.

**Type 0 — ne jamais changer.** L'attribut est réputé figé : `date_creation` du compte client, `nom`
du magasin, `date_embauche` du vendeur. Aucune ligne de mouvement ne les touche, et c'est heureux : si
l'un d'eux doit changer, c'est en général le signe qu'il n'était pas le bon attribut.

**Type 1 — écraser.** La valeur change, l'historique n'est pas conservé. Sur le socle, **140**
mouvements : **73** sur la ville et **67** sur les conditions de paiement. Ce sont des **corrections**
(« 30 j » au lieu de « 30 j »), pas des changements d'état. Le type 1 a un effet brutal et qu'il faut
assumer : le passé est **réécrit**. Une vente de 2023 attribuée à une ville corrigée en 2026 sera
publiée avec la ville corrigée, comme si elle y avait toujours été.

**Type 2 — versionner.** C'est le type qui porte l'histoire : **980** mouvements sur le socle (**658**
sur le segment, **322** sur la ville), pour **24 892** versions de clients concernant **900** clients
(dont certains ont jusqu'à **3** versions). La ligne ancienne reste, datée et fermée ; la ligne
nouvelle s'ouvre. Le prix à payer est triple : la dimension grossit (de **23 912** lignes à
**24 893**), chaque objet peut apparaître plusieurs fois — donc **aucune jointure naïve ne doit
servir la dimension historisée sans sa clause de date** —, et il faut décider ce qui se passe pour un
fait **antérieur à la première version**.

**Type 3 — colonne de la valeur précédente.** Deux colonnes (`ville`, `ville_precedente`) au lieu
d'une historisation complète. C'est économique en lignes et catastrophique en information : le socle
compte **4** clients qui ont changé de ville plus de deux fois, avec jusqu'à **3** villes distinctes.
Le type 3 en perd une, et il faudrait une colonne par changement possible. Sa seule justification est
la comparaison « avant / après » à date fixe, jamais la vraie histoire.

> **À retenir.** Le choix du type de SCD n'est pas technique, il est **métier** : il dit ce qu'un
> rapport a le droit de demander au passé. Sur le fil rouge, la ville et le segment sont en type 2
> parce qu'un directeur régional doit pouvoir lire le chiffre d'affaires **de sa région au moment de
> la vente** ; les conditions de paiement sont en type 1 parce qu'une correction de saisie n'est pas
> un changement d'état.

### 5.5 La requête « au moment du fait »

Une dimension historisée ne se joint pas sur une égalité de clé. Elle se joint sur un **intervalle** :

```sql
SELECT h.segment, ROUND(SUM(f.montant_ttc)) AS ca
FROM fait_ventes f
JOIN dim_client_scd h
  ON h.id_client = f.id_client
 AND f.date_vente BETWEEN h.date_debut AND COALESCE(h.date_fin, DATE '2100-01-01')
WHERE f.est_retour = 0
GROUP BY 1
ORDER BY 2 DESC;
```

Trois détails décident de la justesse de cette requête.

Le premier est `BETWEEN` : c'est lui qui choisit **la bonne photo**. Le deuxième est le
`COALESCE` sur la date de fin : la version courante n'a pas de date de fin (la valeur est nulle), et
un `BETWEEN` sur une valeur nulle ne renvoie rien — le client le plus important, celui dont la ville
est actuelle, serait purement et simplement exclu du rapport. Le troisième est la **clé de version** :
si deux versions se chevauchaient d'un jour, la jointure doublerait les lignes et le chiffre
d'affaires avec elles.

Le contrôle est donc double, et il se mesure : la jointure « au moment du fait » rend **240 000**
lignes pour **240 000** ventes — aucun doublon, aucune perte.

### 5.6 Les deux trous, et pourquoi il faut les boucher exprès

La même requête, appliquée à un socle moins soigné, aurait deux trous. Le socle les a traités, et le
détail vaut la leçon.

**Le client non identifié.** Le client `0` apparaît dans **43 161** ventes et n'existe pas dans le
référentiel — un défaut classique de caisse, où l'on encaisse sans identifier l'acheteur. Le modèle
lui donne une ligne : « client non identifié », **43 161** lignes de ticket, **2 852 612 447** FCFA.
Sans cette ligne, une jointure **interne** ferait disparaître **43 161** ventes du rapport, et
**2 852 612 447** FCFA avec elles.

**Le fait antérieur à la première version.** Le référentiel porte une date de **création** du compte ;
la première version historisée s'ouvre à cette date. Mais **28 784** ventes ont été enregistrées
**avant** cette date de création, pour **6 685** clients — un décalage normal : la fiche a été saisie
après la première vente. La première version commence donc à la **plus ancienne** des deux dates,
`LEAST(date_creation, premiere_vente)`. Sans ce rattrapage, ces **28 784** ventes ne trouvent aucune
version à rejoindre, et disparaissent.

> **Attention.** Une dimension historisée trouée ne lève **aucune erreur**. Une jointure interne perd
> simplement les lignes qui ne trouvent rien : **43 161** ventes sans client identifié et **28 784**
> ventes antérieures à la création du compte représentent à elles deux **71 945** lignes de ticket qui
> s'évaporeraient d'un rapport, sans un mot d'avertissement. Le contrôle est le même qu'au chapitre
> C03 : compter les lignes avant et après.

### 5.7 Ce que la lecture historisée coûte, et ce qu'elle rapporte

Faut-il historiser ? La question se tranche par la mesure, et le socle donne les deux termes.

**Ce qu'elle coûte.** La jointure par intervalle est plus chère qu'une égalité de clé : **9** ms
contre **5** ms sur le fil rouge, médiane de sept exécutions, pour le même rapport par segment. Le
surcoût est modeste ici et il grandit avec la taille des dimensions — mais il se paie une fois, à la
conception, pas à chaque lecture.

**Ce qu'elle rapporte.** Le même rapport, sur les mêmes ventes, donne deux réponses différentes :
**7 735 369 260** FCFA pour le segment Standard et **3 503 366 365** FCFA pour Argent, lus sur la
dimension historisée, contre **7 838 286 840** et **3 442 257 458** lus sur la dimension courante.
L'écart atteint **102 917 580** FCFA sur un seul segment, et le total, lui, ne bouge pas : les deux
lectures somment à **15 595 154 955** FCFA. La question n'est donc pas « quel total est juste ? » —
les deux le sont — mais « **quelle répartition voulons-nous publier ?** ». Celle du temps des faits,
évidemment : un commercial de Koudougou ne peut pas être crédité de ses ventes dans la ville où son
client habite aujourd'hui.

> **Conseil professionnel.** Avant d'historiser un attribut, posez la question qui tranche :
> « un rapport doit-il pouvoir dire *où c'était* / *combien c'était* à une date passée ? » Si la
> réponse est non, le type 1 suffit ; si la réponse est oui, le type 2 est obligatoire, avec son
> coût — **24 893** lignes au lieu de **23 912** sur le seul référentiel clients. Historiser par
> principe alourdit le modèle sans rien apporter ; ne pas historiser un attribut qu'on interrogera
> dans le temps rend les rapports faux en silence.

**Le cas des tarifs.** La même logique s'applique aux prix. La grille tarifaire est historisée :
**616** versions pour **154** produits, **4** versions par produit, une nouvelle version chaque 1er
janvier, **8 783** FCFA en moyenne en 2023 et **10 873** FCFA en 2026 (**+ 24 %**). Lire le prix
**du jour** sur des ventes de 2023 gonfle ou écrase la marge. Mesure sur le fil rouge : le prix moyen
des ventes vaut **9 045** FCFA lu sur la dimension historisée et **8 222** FCFA lu sur la dimension
courante — **9,1 %** d'écart. Un prix moyen de 9 045 FCFA n'est pas « un peu » différent de 8 222 : le
second compare des ventes de quatre années au tarif d'aujourd'hui.

### 5.8 La clé de version, et la ligne qu'on n'oublie pas

Une dimension historisée a besoin d'une clé qui identifie **une version**, pas un objet : `id_client`
seul est ambigu dès qu'un client a deux versions. Le socle emploie une **clé de version** construite
(`cle_version`, de la forme `12-4` : le produit 12, sa quatrième version). Elle sert à deux choses :
joindre sans ambiguïté depuis une table qui référence une version précise, et **compter** les
versions d'un objet sans se tromper.

La ligne qu'on n'oublie pas est celle de l'**inconnu** : « client non identifié » dans `dim_client`,
porte ouverte aux **43 161** ventes orphelines. Une dimension qui refuse l'inconnu est une dimension
qui perd des faits — et un modèle qui perd des faits est un modèle qui publie des totaux faux sans le
dire.

---

## 6. Exemple concret — deux fiches qui bougent

**Un produit, quatre versions de prix.** Le produit **12** (ciment) a quatre versions :

| Version | Période | Prix de vente HT |
|---|---|---|
| 1 | 2023 | **5 415** FCFA |
| 2 | 2024 | **5 769** FCFA |
| 3 | 2025 | **6 225** FCFA |
| 4 | depuis 2026 | **6 816** FCFA |

C'est **+ 25,9 %** en quatre ans, soit quatre lignes dans `dim_produit_scd` là où une dimension
courante n'en garderait qu'une. La conséquence est directe : une vente de mars 2023 dont on lit le
tarif sur la dimension courante est valorisée au prix de 2026. Le chiffre d'affaires, lui, ne bouge
pas — il est dans les faits —, mais **toute analyse de prix ou de marge devient fausse**, parce que la
comparaison oppose des montants réels à un tarif anachronique.

**Un client, trois villes.** Le client **2 030** apparaît trois fois :

| Version | Période | Ville |
|---|---|---|
| 1 | du 2020-03-06 au 2023-06-08 | Koudougou |
| 2 | du 2023-06-09 au 2025-08-22 | Kaya |
| 3 | depuis le 2025-08-23 | Ouagadougou |

Trois ans de ventes à Koudougou, deux ans à Kaya, le reste à Ouagadougou. Lu sur la dimension courante,
ce client est un client d'Ouagadougou, point final : l'effort commercial de 2021 à Kaya et sa
contribution à la région du Centre-Ouest disparaissent des rapports régionaux. Lu sur la dimension
historisée, chaque vente va à la ville de son époque. C'est exactement l'écart de **102 917 580** FCFA
mesuré au §5.7, sauf qu'ici on peut nommer le client et dater chaque changement.

---

## 7. Démonstration pas à pas — quatre gestes

**Étape 1 — déclarer les attributs et leur type de changement.**

Pour chaque attribut d'une dimension, écrire son type : 0 (figé), 1 (écrasé), 2 (historisé). C'est une
décision de conception, prise avec le métier, et elle se documente — sinon chaque nouveau rapport
invente sa propre règle.

**Étape 2 — construire les colonnes de période.**

Le socle construit les versions en SQL, à partir de deux sources : le référentiel clients et le
fichier des mouvements. Les bornes d'abord — chaque changement de type 2 ouvre une version, et la
première borne est la plus ancienne des deux dates (création du compte, première vente) :

```sql
WITH prem AS (
    SELECT CAST(id_client AS INTEGER) AS id_client,
           MIN(TRY_CAST(date_vente AS DATE)) AS premiere_vente
    FROM ventes GROUP BY 1),
base AS (
    SELECT CAST(c.id_client AS INTEGER) AS id_client,
           COALESCE(TRY_CAST(c.date_creation AS DATE), DATE '2023-01-01') AS date_creation,
           p.premiere_vente
    FROM clients c LEFT JOIN prem p ON p.id_client = CAST(c.id_client AS INTEGER)),
mvt AS (
    SELECT CAST(id_client AS INTEGER) AS id_client, TRY_CAST(date_effet AS DATE) AS date_effet
    FROM read_csv_auto('03_exercices/dossier_M13/mouvements_clients.csv', header = true)
    WHERE CAST(type_scd AS INTEGER) = 2),
bornes AS (
    SELECT id_client, date_effet AS debut FROM mvt
    UNION
    SELECT id_client, LEAST(date_creation, COALESCE(premiere_vente, date_creation)) AS debut
    FROM base),
versions AS (
    SELECT id_client, debut,
           row_number() OVER (PARTITION BY id_client ORDER BY debut) AS version,
           lead(debut) OVER (PARTITION BY id_client ORDER BY debut) AS fin
    FROM bornes)
SELECT COUNT(*) AS versions, COUNT(DISTINCT id_client) AS clients FROM versions;
```

Résultat : **24 892** versions pour **23 912** clients — **900** clients ont donc une histoire. Le
`lead` ouvre la version suivante, et la fermeture de la précédente s'en déduit par `fin - INTERVAL 1
DAY`. Deux colonnes disent tout : `date_debut` (obligatoire) et `date_fin` (`NULL` pour la version en
cours) ; la clé de version (`12-4`) identifie une version, pas un objet.

**Étape 3 — ouvrir et fermer les versions.**

Quand un attribut de type 2 change, on **ferme** la version courante la veille du changement et l'on
**ouvre** une nouvelle version au jour du changement. La fermeture est la partie qu'on oublie : une
dimension dont deux versions restent ouvertes au même instant double les lignes de toute jointure qui
la lit.

**Étape 4 — écrire la jointure et son contrôle.**

```sql
-- la jointure au moment du fait
SELECT COUNT(*) AS lignes_jointes
FROM fait_ventes f
JOIN dim_client_scd h
  ON h.id_client = f.id_client
 AND f.date_vente BETWEEN h.date_debut AND COALESCE(h.date_fin, DATE '2100-01-01');
```

Attendu : **240 000** lignes pour **240 000** ventes. Plus petit, la dimension est trouée (clients
inconnus, faits antérieurs) ; plus grand, deux versions se chevauchent. Ce contrôle s'exécute à chaque
chargement, comme celui du grain au chapitre C03.

---

## 8. Erreurs fréquentes

| Erreur | Ce qu'on observe | La correction |
|---|---|---|
| Joindre une dimension historisée sans clause de date | le rapport double les lignes | `BETWEEN date_debut AND COALESCE(date_fin, …)` |
| Oublier le `COALESCE` sur la date de fin | les clients actuels disparaissent du rapport | traiter le `NULL` comme « encore vrai » |
| Laisser deux versions ouvertes | **240 000** lignes deviennent davantage | fermer la version précédente la veille |
| Écraser un attribut qui change pour de vrai | **102 917 580** FCFA d'écart de répartition | type 2 sur les attributs d'analyse |
| Historiser un attribut qui ne change jamais | dimension inutilement plus grosse | type 0, et on l'écrit |
| Croire que le total contrôle la répartition | le total est juste, les segments non | comparer **chaque** segment, pas le total |
| Refuser la ligne « inconnu » | **43 161** ventes perdues sans erreur | une ligne porteuse de l'inconnu |

---

## 9. Bonnes pratiques professionnelles

1. **Le type de changement se décide avec le métier**, pas avec le développeur : « voulez-vous
   retrouver les ventes d'un client dans la ville où il était, ou dans celle où il est ? » suffit à
   trancher.
2. **Une dimension historisée porte toujours trois colonnes de service** : date de début, date de fin,
   indicateur de version courante.
3. **La table de faits ne se joint jamais deux fois à une dimension historisée** sans agrégation
   intermédiaire : deux jointures par intervalle sur la même table multiplient les lignes.
4. **Le contrôle « lignes après jointure = lignes avant »** s'exécute à chaque chargement, et son
   résultat se publie.
5. **La ligne « inconnu » fait partie du modèle** : elle est documentée, elle porte un nom lisible,
   et elle ne se supprime pas pour faire propre.
6. **On date les corrections de type 1** dans le journal de chargement, même si la donnée n'en garde
   pas trace : le prochain analyste doit pouvoir savoir que l'histoire a été réécrite.

---

## 10. Exercice guidé

**Sujet.** Le rapport régional publie « chiffre d'affaires par region du client ». Le service
commercial conteste : d'après lui, les ventes de l'année 2023 ne sont pas dans les bonnes régions. Vous
avez trente minutes pour dire qui a raison, et le prouver.

**Étape 1 — écrire les deux requêtes, mot pour mot.** La première lit la dimension courante
(`dim_client`), la seconde la dimension historisée (`dim_client_scd`) avec la clause d'intervalle. Les
deux comptent les mêmes ventes, sur la même période, avec le même filtre de retours.

**Étape 2 — comparer les répartitions, pas les totaux.** Les deux requêtes donnent le même total
(**15 595 154 955** FCFA). La comparaison utile porte sur **chaque** région et **chaque** segment :
Standard **7 838 286 840** contre **7 735 369 260**, Argent **3 442 257 458** contre **3 503 366 365**,
Or **1 461 998 210** contre **1 503 806 883**.

**Étape 3 — nommer la cause.** Les écarts ne viennent pas d'une erreur de calcul, mais du **sens** de
la lecture : la dimension courante applique à toutes les ventes la ville **d'aujourd'hui**, alors que
**900** clients ont changé d'au moins un attribut, et que le référentiel porte **980** changements
d'état.

**Étape 4 — trancher et l'écrire.** Le service commercial a raison : publier dans la ville actuelle
revient à créditer un commercial d'une vente qu'il n'a pas faite. La règle se documente : « tout
rapport régional lit la dimension historisée ; la dimension courante ne sert qu'aux listes de
contacts. »

**Barème (15 points) :** les deux requêtes écrites (4) · la comparaison des trois segments, chiffrée
(4) · la cause nommée (3) · la règle écrite et justifiée (4).

---

## 11. Exercices autonomes

**Exercice 4.1.** Pour chacun de ces attributs du fil rouge, choisissez un type de changement (0, 1, 2)
et justifiez en une ligne : `date_creation` d'un client, `ville` d'un client, `conditions_paiement`,
`famille` d'un produit, `prix_vente_ht` d'un produit, `segment` d'un client. Donnez, pour chaque
choix de type 2, la question métier qui l'exige.

**Exercice 4.2.** Écrivez la jointure « au moment du fait » entre les ventes et la dimension clients
historisée, puis son contrôle : le nombre de lignes après jointure doit égaler le nombre de ventes.
Exécutez, et donnez les deux nombres obtenus. Expliquez ensuite ce qui se passerait si vous retiriez
le `COALESCE` sur `date_fin`.

**Exercice 4.3.** Le client **2 030** a trois versions. Écrivez la requête qui donne son chiffre
d'affaires **par ville et par année**, et vérifiez que la somme par ville correspond bien aux périodes
de ses versions. Combien de villes trouve-t-on, et lesquelles ?

**Exercice 4.4.** Le type 3 : écrivez, sur `dim_client_scd`, la requête qui compte les clients ayant
changé de ville **plus de deux fois**. Donnez le nombre obtenu, puis la liste des colonnes qu'il aurait
fallu ajouter pour représenter ces clients en type 3 — et concluez en trois lignes.

**Exercice 4.5.** Un collègue propose de « simplifier » le modèle en supprimant `dim_client_scd` et en
recopiant `region` dans les ventes au moment de l'achat. Écrivez ce que cette solution donne de juste
(le rapport régional devient exact), et ce qu'elle coûte : citez deux requêtes que le modèle ne
permettra plus d'écrire, et un chiffre du socle qui montre le prix de la redondance.

---

## 12. Correction détaillée

**Exercice 4.1.** Type 0 : `date_creation` (une date de création ne change pas) et `famille` d'un
produit (elle se corrige si le classement est faux, mais elle n'est pas une histoire). Type 1 :
`conditions_paiement` — c'est une donnée contractuelle qui se corrige, et l'historique du contrat n'est
pas géré ici. Type 2 : `ville` et `segment` du client (le directeur régional doit lire la ville **de
l'époque de la vente**), `prix_vente_ht` (la marge se calcule avec le tarif de la période). Chaque
choix de type 2 répond à une question datée : « où ce client habitait-il quand il a acheté ? »,
« quel prix s'appliquait ce jour-là ? ».

**Exercice 4.2.** La requête et son contrôle :

```sql
SELECT COUNT(*) FROM fait_ventes f;
SELECT COUNT(*) FROM fait_ventes f
JOIN dim_client_scd h
  ON h.id_client = f.id_client
 AND f.date_vente BETWEEN h.date_debut AND COALESCE(h.date_fin, DATE '2100-01-01');
```

**240 000** puis **240 000** : la jointure est complète. Sans le `COALESCE`, la condition `date_vente
BETWEEN date_debut AND NULL` est inconnue pour toutes les versions courantes : les ventes des clients
dont la fiche est à jour — donc l'immense majorité — disparaîtraient du rapport.

**Exercice 4.3.** Le chiffre d'affaires du client **2 030** par ville et par année :

```sql
SELECT h.ville, MIN(f.date_vente) AS premiere, MAX(f.date_vente) AS derniere,
       COUNT(*) AS ventes, ROUND(SUM(f.montant_ttc)) AS ca
FROM fait_ventes f
JOIN dim_client_scd h
  ON h.id_client = f.id_client
 AND f.date_vente BETWEEN h.date_debut AND COALESCE(h.date_fin, DATE '2100-01-01')
WHERE f.id_client = 2030 AND f.est_retour = 0
GROUP BY 1
ORDER BY 1;
```

Trois villes apparaissent — **Koudougou**, **Kaya**, **Ouagadougou** — et les périodes de ventes
tombent dans les intervalles de validité des versions. Si une seule ville ressortait, c'est que la
jointure aurait lu la dimension courante.

**Exercice 4.4.** La requête de comptage :

```sql
SELECT COUNT(*) FROM (
  SELECT id_client FROM dim_client_scd
  GROUP BY id_client HAVING COUNT(DISTINCT ville) > 2
);
```

Résultat : **4** clients (jusqu'à **3** villes distinctes). En type 3, il faudrait les colonnes
`ville`, `ville_precedente`, `ville_avant_precedente` — et l'on devrait recommencer à chaque nouveau
changement. Le type 3 ne représente pas une histoire ; il représente une comparaison.

**Exercice 4.5.** La solution « recopier la région dans les ventes » rend le rapport régional exact —
c'est son seul mérite. Elle coûte d'abord la **redondance** : la région est recopiée sur les
**240 000** lignes de ventes au lieu de **6** lignes de magasins, et la moindre correction devient une
mise à jour de masse. Elle coûte ensuite deux requêtes que le modèle ne permettra plus d'écrire : (a)
« quelle est la répartition actuelle de mes clients par région ? » — les ventes portent une région
figée, la dimension porte la région vivante ; (b) « quels clients ont changé de région cette année ? » —
l'information n'existe plus nulle part. Le chiffre qui mesure le prix de la redondance est celui du
chapitre C02 : **2 826 394** caractères de noms de clients recopiés dans la table plate, contre
**239 599** dans la dimension — un facteur **11,8**.

---

## 13. Mini-projet de chapitre

**« La note de choix de la dimension client »** (2 h 30). Produisez, pour la dimension clients du fil
rouge : (1) la liste de ses attributs avec, pour chacun, le type de changement retenu (0, 1, 2) et la
justification métier ; (2) le tableau des **980** mouvements de type 2 par attribut (**658** segment,
**322** ville) et des **140** mouvements de type 1 (**73** ville, **67** conditions) ; (3) la requête
qui prouve que la jointure historisée ne perd ni ne duplique aucune ligne (**240 000** pour
**240 000**) ; (4) la requête qui chiffre l'écart de répartition entre lecture courante et lecture
historisée, segment par segment ; (5) une page de règle : « quel rapport lit quelle dimension ». Ce
livrable alimente directement **P2** (SQL et contrôles) et **P4** (note de choix de 3 pages) du projet
de module.

---

## 14. Résumé du chapitre

| Notion | Ce qu'il faut retenir |
|---|---|
| Étoile | un fait au centre, des dimensions autour, **une** jointure par attribut |
| Dimensions conformes | `dim_magasin` sert **5** faits, `dim_client` et `dim_produit` **3** ; `dim_date` **0** |
| Hiérarchie | produit, **12** sous-catégories, **7** familles |
| SCD type 0 | `date_creation`, `nom` : jamais modifiés |
| SCD type 1 | **140** corrections, l'ancienne valeur est écrasée |
| SCD type 2 | **980** mouvements, **24 892** versions, **900** clients |
| SCD type 3 | insuffisant : **4** clients ont **3** villes |
| Jointure au moment du fait | `BETWEEN` et `COALESCE` : **240 000** lignes pour **240 000** ventes |
| Les deux trous | client inconnu (**43 161** ventes) et faits antérieurs à la création (**28 784** ventes) |
| Coût de l'historique | **9** ms contre **5** ms, médiane de sept exécutions |
| Gain de l'historique | répartition par segment juste à **102 917 580** FCFA près |
| Tarif historisé | **616** versions, **4** par produit, **9,1 %** d'écart de prix moyen |

---

## 15. À retenir

1. **Une dimension est le seul endroit où vit le sens métier.** Le fait porte des clés et des
   montants ; la ville, le segment et la famille sont dans les dimensions.
2. **Une dimension conforme rend deux rapports comparables** : `dim_magasin` sert **5** faits, et
   c'est pour cela que l'on peut confronter ventes, ruptures, logistique et objectifs d'un magasin.
3. **Les quatre types de SCD sont une décision métier**, pas un réglage technique : figer, écraser,
   versionner, ou comparer avant et après.
4. **La jointure au moment du fait impose deux écritures précises** : `BETWEEN` sur l'intervalle et
   `COALESCE` sur la date de fin ; et son contrôle est un comptage — **240 000** lignes pour
   **240 000** ventes.
5. **Une dimension historisée qui perd un fait ne prévient personne** : **43 161** ventes sans client
   identifié et **28 784** ventes antérieures à la création du compte, soit **71 945** lignes de
   ticket qui disparaîtraient d'un rapport en silence.

> **À retenir.** Le total ne contrôle pas la répartition : les deux lectures du chiffre d'affaires par
> segment somment au même **15 595 154 955** FCFA, et pourtant l'une des deux attribue mal
> **102 917 580** FCFA. Un rapport juste au total peut être faux dans chaque case.

> **À retenir.** Historiser coûte deux choses et en rapporte une. Cela coûte des lignes (**24 893**
> au lieu de **23 912**), une clause de date dans **chaque** jointure, et **4** ms de lecture en plus
> sur le fil rouge. Cela rapporte la seule chose qu'un modèle ne peut pas fabriquer après coup :
> **l'état du monde au moment du fait**.

---

## 16. Évaluation formative

1. Qu'est-ce qui distingue un schéma en étoile d'un schéma en flocon ? Donnez le critère pratique.
2. Citez une dimension conforme du fil rouge et le nombre de faits qu'elle sert.
3. Que signifie « dimension historisée » ? Citez ses trois colonnes de service.
4. Décrivez les quatre types de SCD et donnez, pour chacun, un attribut du socle (ou la raison de son
   absence).
5. Pourquoi le type 3 ne convient-il pas au socle clients ? Donnez le chiffre.
6. Écrivez, en cinq lignes, la jointure « au moment du fait », `COALESCE` compris.
7. Que se passe-t-il si l'on omet le `COALESCE` sur `date_fin` ?
8. La jointure historisée rend **240 000** lignes pour **240 000** ventes : que prouve ce contrôle, et
   que ne prouve-t-il pas ?
9. Pourquoi le total des ventes par segment est-il identique dans les deux lectures, alors que les
   segments diffèrent de **102 917 580** FCFA ?
10. Le prix moyen des ventes vaut **9 045** FCFA en lecture historisée et **8 222** FCFA en lecture
    courante : expliquez l'écart en une phrase, et dites laquelle des deux valeurs doit figurer dans
    un rapport de marge.

**Corrigé :** 1. Le nombre de jointures nécessaires pour atteindre un attribut : une seule dans
l'étoile, plusieurs dans le flocon (la hiérarchie est éclatée en tables). 2. `dim_magasin`, servie par
**5** des **7** tables de faits. 3. Une dimension dont chaque objet peut avoir plusieurs lignes
datées : `date_debut`, `date_fin`, `est_courante`. 4. Type 0 : `date_creation` ; type 1 : les **140**
corrections (ville, conditions) ; type 2 : les **980** changements d'état (segment, ville) ; type 3 :
pas retenu, car **4** clients ont changé plus de deux fois de ville. 5. Parce qu'il ne peut garder
qu'une valeur précédente : il faudrait une colonne par changement, et le socle compte **4** clients à
**3** villes distinctes. 6. `JOIN dim_client_scd h ON h.id_client = f.id_client AND f.date_vente
BETWEEN h.date_debut AND COALESCE(h.date_fin, DATE '2100-01-01')`. 7. Les versions courantes ont une
date de fin nulle : la condition devient inconnue, et les ventes concernées disparaissent du rapport.
8. Il prouve qu'aucune ligne n'est perdue ni dupliquée par la jointure. Il ne prouve pas que la
**bonne** version a été choisie, ni que l'intervalle est correctement borné : pour cela, il faut
vérifier les dates, version par version. 9. Parce que la répartition change sans que le total change :
les ventes sont les mêmes, seule la ville ou le segment **attribué** diffère. 10. Le tarif ou le prix
de référence lu est celui d'aujourd'hui, alors que les ventes s'étalent sur quatre ans d'inflation
tarifaire (**+ 24 %** au total) ; c'est la valeur historisée (**9 045** FCFA) qui doit figurer dans un
rapport de marge, parce qu'elle correspond au prix réellement pratiqué.
