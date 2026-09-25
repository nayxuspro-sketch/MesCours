# Module M13.C07 — La qualité du modèle, sa documentation et sa revue

![La grille de revue en 15 points : les dix points qui passent sur le modèle du fil rouge, les cinq qui échouent sur le modèle fautif, et les cinq mesures qui le prouvent (production : `tools/figures_M13.py`)](../figures/M13_C07_grille_revue.svg)

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **exécuter les quatre contrôles qui décident qu'un modèle est livrable** : l'unicité des clés
   (**14** tables sur **14**), l'égalité du grain (**7** faits sur **7**), l'absence d'orphelin
   (**12** clés étrangères vérifiées, **0** orphelin) et la recette (**15 595 154 955** FCFA des deux
   côtés, le modèle et la source) ;
2. **documenter un modèle sans l'alourdir** : le script du socle compte **315** lignes dont **99** de
   commentaire, et il ne déclare **aucune** clé primaire, **aucune** clé étrangère et **aucun**
   commentaire de colonne — la garantie est déplacée des contraintes vers les contrôles, et cela se
   dit ;
3. **passer la grille de revue en 15 points** sur un modèle qu'on n'a pas écrit, et transformer
   chaque point en une preuve : une requête, un compte ou un nom ;
4. **chiffrer les cinq défauts d'un modèle fautif** : un nom de client recopié sur **2 826 394**
   caractères au lieu de **239 599**, deux colonnes pour dire le temps, un objectif posé sur la
   ligne de vente qui ajoute **42,9 %** au chiffre d'affaires, **0** clé déclarée, et **16** libellés
   de catégorie pour **7** familles ;
5. **refuser de livrer** : trois modèles fautifs du socle s'exécutent sans erreur et rendent
   **22 305 610 960** FCFA (**+ 43,0 %**), **29 474 916 530** FCFA (**+ 89,0 %**) et
   **686 186 818 020** FCFA (**44** fois le chiffre juste).

---

## 2. Pourquoi cette notion est importante

Un modèle de données ne se juge pas à son élégance. Il se juge à ce qu'il **prouve**, et une preuve
se répète. Les six chapitres précédents ont construit un modèle : entités, normalisation, grain,
étoile, historisation, calendrier. Ce chapitre répond à la seule question que se pose un
responsable avant de s'appuyer dessus : **comment savez-vous que c'est juste ?**

La réponse tient en quatre contrôles qui ne coûtent rien et qui prennent l'essentiel : l'unicité des
clés, l'égalité du grain, l'absence d'orphelin, la recette. Sur le socle, les quatre passent, et ils
passent **parce qu'ils sont écrits** : un modèle juste dont personne ne peut le démontrer ne vaut
pas mieux, en pratique, qu'un modèle faux.

Le reste du chapitre est consacré à ce qu'aucun contrôle automatique ne voit. Les contrôles
comparent des comptes et des totaux ; ils ne savent pas qu'un nom de client est recopié, que la même
réalité porte deux colonnes de temps, qu'un objectif a été posé au mauvais grain, ou que la
catégorie du fichier source n'est pas celle du référentiel. Ces cinq-là se voient à la **lecture**,
guidée par une grille de 15 points, et le chapitre les chiffre un par un.

---

## 3. Explication simple — le contrôle technique et la fiche de visite

Avant de reprendre une voiture à un garagiste, deux choses se passent, et elles ne se remplacent pas.

Le **contrôle technique** : des appareils mesurent des choses comparables à des valeurs de
référence. Freinage, émissions, éclairage. Ils rendent un verdict binaire, et ils ne savent
absolument pas dire si la voiture est agréable à conduire, si le siège est à la bonne hauteur ou si
le coffre convient à la famille.

La **fiche de visite** : un mécanicien suit une liste écrite, point par point, et répond par oui ou
par non, en montrant ce qu'il a vu. État des pneus, jeu de la direction, propreté du filtre. La
liste est la même pour toutes les voitures, ce qui la rend comparable d'une visite à l'autre.

Un modèle suit exactement ce parcours. Les **quatre contrôles automatiques** sont le contrôle
technique : ils comparent le modèle à sa source, à son grain déclaré et à son référentiel, et ils
rendent **14** verdicts d'unicité, **7** verdicts de grain, **12** verdicts de clé étrangère et un
verdict de recette. La **grille de revue en 15 points** est la fiche de visite : elle porte sur ce
qu'aucun appareil ne mesure, et elle exige une réponse **documentée** à chaque point.

Un modèle qui passe les quatre contrôles et rate la grille est un modèle complet et faux. Un modèle
qui passe la grille et rate un contrôle ne peut pas être livré du tout : la recette se vérifie
d'abord.

---

## 4. Vocabulaire essentiel

> **Définition.** Un **contrôle de recette** est une requête qui compare le modèle à une référence
> extérieure et rend un verdict binaire. Les quatre du socle comparent : les valeurs distinctes d'une
> clé au nombre de lignes (unicité), les lignes d'un fait aux lignes de sa source (grain), les clés
> étrangères au référentiel (orphelins), et le total du modèle au total de la source (recette).

> **Définition.** L'**unicité d'une clé** est la propriété qui fait d'une colonne une clé : le nombre
> de valeurs distinctes égale le nombre de lignes. Elle se **prouve** en une comparaison, jamais en
> la déclarant. Sur le socle, **14** tables sur **14** la vérifient — la table des clients en porte
> **23 913** lignes et **23 913** valeurs distinctes.

> **Définition.** Un **orphelin** est une clé étrangère qui ne trouve pas sa ligne dans le
> référentiel : une vente dont le produit n'existe pas. Un orphelin ne produit pas d'erreur : il
> produit une ligne qui disparaît d'un rapport groupé. Le socle en compte **0** sur **12** clés
> vérifiées, et la seule clé absente du référentiel — le client non identifié — reçoit une ligne
> déclarée.

> **Définition.** La **recette d'un modèle** est l'égalité entre le total d'une mesure lue dans le
> modèle et le même total lu dans la source. C'est le contrôle le plus fort et le plus simple :
> **15 595 154 955** FCFA des deux côtés. Aucune autre vérification ne remplace celle-là, parce que
> c'est la seule qui porte sur le chiffre que les rapports publieront.

> **Définition.** Un **dictionnaire de données** est la liste écrite des tables et des colonnes du
> modèle, avec pour chacune son type, sa définition métier, son grain et ses règles. Le socle compte
> **127** colonnes, la plus large des tables en portant **17** : c'est le volume à documenter, et il
> tient en quelques pages.

> **Définition.** Une **revue par grille** est une relecture conduite avec une liste fermée de points,
> chaque point devant être justifié par une preuve. La grille du socle compte **15** points ; elle
> transforme « le modèle me paraît bon » en quinze réponses vérifiables par un tiers.

---

## 5. Cours approfondi

### 5.1 Les quatre contrôles, et ce qu'ils ont en commun

| Contrôle | Question posée | Résultat sur le socle |
|---|---|---|
| Unicité | le nombre de valeurs distinctes égale-t-il le nombre de lignes ? | **14** tables sur **14** |
| Grain | le fait porte-t-il exactement les lignes de sa source ? | **7** faits sur **7** |
| Orphelins | chaque clé étrangère trouve-t-elle sa ligne ? | **12** clés vérifiées, **0** orphelin |
| Recette | le total du modèle égale-t-il celui de la source ? | **15 595 154 955** FCFA des deux côtés |

Ces quatre contrôles ont une propriété commune qui explique leur puissance : **aucun ne regarde le
modèle seul**. L'unicité compare la clé à elle-même mais aussi au grain déclaré ; le grain compare le
fait à sa source ; les orphelins comparent le fait à ses dimensions ; la recette compare le modèle
entier à la source. Un contrôle qui ne compare rien à rien ne vaut rien : compter les lignes d'une
table et annoncer « la table contient 240 000 lignes » n'est pas un contrôle, c'est une
description.

### 5.2 Ce qu'aucun contrôle automatique ne voit

Les quatre contrôles passent sur le socle, et ils passeraient tout aussi bien sur un modèle
parfaitement faux. Voici pourquoi, en trois exemples.

Un fait dont les montants seraient ceux d'une autre période garde le même nombre de lignes et le
même total : le contrôle de recette ne verrait rien. Un fait dont les catégories seraient celles du
fichier source, avec ses majuscules et ses espaces, garde son grain : le contrôle de grain ne verrait
rien. Un objectif posé sur la ligne de vente au lieu de la table des objectifs garde toutes ses clés
valides : le contrôle d'orphelins ne verrait rien.

Ce sont exactement les trois défauts du modèle fautif de la planche, et ils sont mesurés. La
conclusion est nette : **l'automatique couvre la forme, la relecture couvre le sens**. Livrer un
modèle avec les quatre contrôles et sans relecture revient à livrer un modèle dont on sait seulement
qu'il ne s'est pas trompé de volume.

### 5.3 La documentation : ce que le script dit de lui-même

| Élément | Mesure |
|---|---|
| Lignes du script de construction | **315** |
| Lignes de commentaire | **99** |
| Clés primaires déclarées | **0** |
| Clés étrangères déclarées | **0** |
| Commentaires de colonne | **0** |
| Tables du modèle | **14** |
| Colonnes du modèle | **127** |

Le script commente presque une ligne sur trois, et il ne contraint rien. Ce n'est pas un oubli : le
socle est construit par des requêtes qui fabriquent les tables à partir de leurs sources, et les
moteurs de cette famille n'imposent pas de contrainte sur une table fabriquée. Le choix se défend,
à une condition : **ce que la base n'impose pas, le contrôle doit le prouver à chaque chargement**.

> **Attention.** Une garantie déplacée n'est plus une garantie tant qu'elle n'est pas exécutée. Sur
> le socle, l'unicité des clés n'est protégée par aucune déclaration : elle est **mesurée** quatorze
> fois par l'instrument. Le jour où quelqu'un charge une table sans lancer l'instrument, plus rien
> n'empêche un doublon d'entrer. Une clé primaire déclarée se défend toute seule, la nuit et sans
> témoin ; un contrôle ne se défend que si quelqu'un le lance. Écrire les contrôles ne suffit pas :
> il faut les brancher sur le chargement, et faire échouer le chargement quand un contrôle échoue.

La documentation d'un modèle se juge donc sur deux pièces, et non une : le script commenté, qui
explique **comment** le modèle est construit, et le dictionnaire de données, qui explique **ce que**
chaque colonne veut dire. Le socle a la première, partiellement ; la seconde reste à écrire, et
c'est l'un des livrables du projet.

### 5.4 Le dictionnaire de données, colonne par colonne

Le socle compte **127** colonnes. Les trois tables les plus larges sont le fait de ventes avec
**17** colonnes, le calendrier avec **15** et la dimension produit avec **11**. Un dictionnaire de
données utile porte quatre informations par colonne, et pas une de moins.

| Information | Exemple, sur le fait de ventes | Pourquoi elle est indispensable |
|---|---|---|
| Nom et type | `montant_ttc`, décimal | deux lecteurs, deux usages |
| Définition métier | montant de la ligne, taxes comprises, remise déduite, hors retours | lève l'ambiguïté que le nom laisse |
| Grain | une ligne de ticket | dit ce qu'on a le droit d'additionner |
| Règles | positif pour une vente, négatif pour un retour | évite le contresens le plus coûteux |

La quatrième ligne du tableau vaut **175 169 798** FCFA sur le socle : c'est le montant des
**2 809** lignes de retour, rangées dans le même fait avec un drapeau et des montants négatifs. Un
lecteur qui ne connaît pas la règle additionne tout et publie un chiffre d'affaires trop faible de
ce montant. Le dictionnaire est le seul endroit où cette règle se lit sans exécuter une requête.

### 5.5 La grille de revue en 15 points

La planche de ce chapitre porte la grille complète. Les points s'ordonnent en quatre familles, et
chacune répond à une question différente.

| Famille | Points | Question posée |
|---|---|---|
| Structure | **1** à **5** | les clés, le grain, les liens et les totaux tiennent-ils ? |
| Sémantique | **6** à **10** | le modèle dit-il la vérité des données, ou seulement leur forme ? |
| Histoire | **11** à **13** | le temps qui passe et le temps du calendrier sont-ils maîtrisés ? |
| Usage | **14** et **15** | un lecteur qui ne connaît pas le modèle peut-il s'en servir ? |

Sur le modèle du fil rouge, les **15** points passent. Sur le modèle fautif du chapitre, les points
**6** à **10** échouent, et ce sont exactement les cinq défauts du paragraphe suivant. La grille n'a
de valeur que si elle est appliquée **par quelqu'un qui n'a pas écrit le modèle** : un auteur relit
ses intentions, un relecteur lit ce qui est écrit.

> **Dans les faits.** La grille se remplit en une réunion, et elle produit deux choses : une liste de
> corrections, et une liste de justifications. La seconde est la plus utile à long terme. Un modèle
> livré avec ses quinze réponses écrites se reprend six mois plus tard sans que personne n'ait à
> deviner pourquoi les choses sont ainsi. C'est la différence entre un modèle qu'on possède et un
> modèle qu'on subit.

### 5.6 Les cinq défauts du modèle fautif, et ce que chacun coûte

| Point de la grille | Défaut | Mesure sur le socle | La bonne pratique |
|---|---|---|---|
| **6** | attributs du client recopiés dans les faits | **2 826 394** caractères recopiés au lieu de **239 599**, soit **11,8** fois | une dimension client, une clé étrangère |
| **7** | deux colonnes pour dire le temps | **1 339** dates d'un côté, **44** mois de l'autre | une seule table de dates |
| **8** | objectif posé sur la ligne de vente | **6 685 260 000** FCFA ajoutés au chiffre d'affaires, soit **42,9 %** | un fait d'objectifs à son grain de **218** lignes |
| **9** | aucune clé déclarée | **0** clé primaire et **0** clé étrangère | des contrôles exécutés à chaque chargement |
| **10** | libellés repris tels quels du fichier | **16** libellés pour **7** familles réelles | la correspondance vit dans le référentiel |

Aucun de ces cinq défauts n'empêche une requête de s'exécuter. C'est ce qui les rend dangereux : ils
se manifestent dans les chiffres, jamais dans les messages d'erreur. Le défaut **8** est le plus
coûteux, parce qu'il ne se contente pas de fausser une ligne de rapport : il fausse le total, ce que
le chapitre 3 a nommé l'erreur de grain.

Le défaut **6** mérite d'être lu deux fois, parce que son coût n'est pas seulement une question de
volume. Un nom recopié **11,8** fois crée autant d'endroits où la même information peut diverger :
une correction d'adresse faite sur une seule ligne produit deux villes pour un client, et donc deux
lignes dans un rapport par ville. Le chapitre 4 a mesuré cette conséquence sur le socle : **4**
clients portent plus de deux villes dans l'historique du fait, et c'est le signe que l'information
de référence a été recopiée trop longtemps.

### 5.7 La revue coûte une heure, l'erreur coûte un trimestre

Il reste à répondre à l'objection habituelle : pourquoi relire un modèle qui s'exécute ? Parce que
trois modèles fautifs du socle s'exécutent parfaitement, et rendent des chiffres qu'aucun
gestionnaire n'accepterait.

| Modèle fautif | Ce qu'il fait | Chiffre d'affaires annoncé | Écart |
|---|---|---|---|
| Deux tableaux additionnés | ventes plus commandes, sans vérifier qu'ils parlent du même fait | **22 305 610 960** FCFA | **+ 43,0 %** |
| Trois tableaux additionnés | on y ajoute les encaissements, troisième comptage du même argent | **29 474 916 530** FCFA | **+ 89,0 %** |
| Jointure sur la mauvaise clé | ventes et logistique reliées par le seul magasin | **686 186 818 020** FCFA | **44** fois le chiffre juste |

Ces trois requêtes ont été exécutées, et elles ont rendu ces trois nombres sans un avertissement.
C'est l'argument le plus fort en faveur de la revue : **le danger n'est pas le modèle qui plante,
c'est le modèle qui répond**. Une requête cassée se répare en dix minutes ; un chiffre faux publié
en réunion se répare en un trimestre de crédibilité.

> **Attention.** Un total juste ne prouve rien à lui seul. Sur le socle, les deux lectures d'un même
> rapport par segment somment au même **15 595 154 955** FCFA, et l'une des deux se trompe de
> **102 917 580** FCFA dans la répartition. La recette valide le **total** ; elle ne valide pas les
> **cases**. Un contrôle de recette sans contrôle de répartition laisse passer l'erreur la plus
> difficile à voir de tout le module.

> **Conseil professionnel.** Automatisez les quatre contrôles dans cet ordre, et faites **échouer le
> chargement** quand l'un d'eux échoue : la recette d'abord, parce qu'un écart de total est le signe
> d'une erreur de jointure ou de filtre, qui rend tout le reste inutile ; le grain ensuite, qui
> attrape les multiplications ; les orphelins après, qui attrapent les lignes muettes ; l'unicité en
> dernier, parce qu'un doublon se voit déjà dans les trois précédents. Puis faites relire le modèle
> par quelqu'un d'autre avec la grille des 15 points, et gardez ses réponses. Une revue de modèle
> tient en une heure ; le temps qu'elle coûte est le meilleur investissement du projet.

> **À retenir.** La qualité d'un modèle se compose de deux choses qui ne se remplacent pas : ce qu'il
> **prouve**, par quatre contrôles exécutés à chaque chargement, et ce qu'il **explique**, par un
> dictionnaire de données et une revue en **15** points. Le socle prouve beaucoup (**14** tables sur
> **14**, **7** faits sur **7**, **0** orphelin, la recette au franc près) et documente encore peu ;
> cette asymétrie est ordinaire, et c'est celle qu'un chef de projet doit savoir lire avant de
> signer.

---

## 6. Exemple concret — cinq défauts, cinq totaux faux

Reprenons le modèle du stagiaire, celui de la fiche de revue. Il tient en deux tables : une table de
ventes à **13** colonnes et une table de magasins. Il s'ouvre, il répond aux questions simples, et
il porte les cinq défauts du paragraphe 5.6.

**Le premier défaut** copie le nom, la ville et le segment du client sur chaque ligne de vente. Cela
coûte **2 826 394** caractères de noms recopiés, contre **239 599** dans une dimension dédiée. Le
rapport par ville qui en sort est vrai le jour du chargement, et faux le lendemain si une adresse
change.

**Le deuxième défaut** garde deux colonnes de temps : une date et un mois écrit à la main. Les deux
valent **1 339** jours et **44** mois, et rien ne garantit qu'elles racontent la même histoire. Un
mois corrigé dans une colonne et pas dans l'autre produit un rapport hebdomadaire qui ne colle plus
au rapport mensuel.

**Le troisième défaut** pose l'objectif du magasin sur chaque ligne de vente. L'objectif vaut
**6 685 260 000** FCFA pour l'ensemble du socle ; recopié sur **240 000** lignes, il s'additionne
avec elles et gonfle le total de **42,9 %**. C'est le défaut le plus coûteux des cinq, et il ne se
voit pas : le rapport s'exécute, les lignes sont valides, le total est faux.

**Le quatrième défaut** ne déclare aucune clé : **0** clé primaire, **0** clé étrangère. Rien
n'empêche d'écrire deux fois le même identifiant de vente, ni de vendre un produit qui n'existe pas.

**Le cinquième défaut** recopie la catégorie telle qu'elle arrive du fichier source : **16** libellés
pour **7** familles réelles. Un tableau par catégorie affiche donc seize lignes dont neuf sont des
doublons déguisés, avec des majuscules et des espaces en trop. La somme reste juste, la répartition
est fausse — exactement le type d'erreur que le contrôle de recette laisse passer.

Corriger ces cinq défauts demande une journée. Les avoir laissés passer coûte un trimestre de
décisions prises sur des chiffres faux.

---

## 7. Démonstration pas à pas — les quatre contrôles en SQL

Les quatre contrôles s'écrivent en quatre requêtes, et chacun rend un verdict binaire.

**Contrôle 1 — l'unicité de la clé.**

```sql
SELECT COUNT(*) AS lignes,
       COUNT(DISTINCT id_client) AS valeurs
FROM dim_client;
```

**23 913** lignes et **23 913** valeurs : la clé est unique, le grain est prouvé. La même requête
répétée sur les **14** tables du modèle donne **14** fois l'égalité.

**Contrôle 2 — le grain du fait face à sa source.**

```sql
SELECT COUNT(*) AS lignes_du_fait FROM fait_ventes;
```

**240 000** lignes, à comparer aux **240 000** lignes de la source. L'égalité se lit dans le rapport
d'exécution, ligne par ligne, pour les **7** faits du modèle.

**Contrôle 3 — les orphelins.**

```sql
SELECT COUNT(*) AS orphelins
FROM fait_ventes f
LEFT JOIN dim_client c ON c.id_client = f.id_client
WHERE c.id_client IS NULL;
```

**0** orphelin sur la clé client, **0** sur la clé produit. Le **left join** est ici obligatoire : une
jointure interne compterait **0** orphelin en supprimant les lignes fautives, ce qui est la
démonstration par l'absurde du contrôle.

**Contrôle 4 — la recette.**

```sql
SELECT ROUND(SUM(montant_ttc)) AS recette
FROM fait_ventes
WHERE est_retour = 0;
```

**15 595 154 955** FCFA, identiques au total de la source. Ce contrôle-là se pose en dernier dans la
lecture, et en premier dans les priorités : si le total est faux, aucun autre verdict n'a
d'importance.

**La lecture de la grille.** Les quinze points se remplissent dans l'ordre de la planche, et chacun
se justifie par une preuve : une requête pour les points structurels, une mesure pour les cinq
défauts, un nom de table pour les points d'usage. Un point sans preuve se note « non revu », jamais
« conforme ».

---

## 8. Erreurs fréquentes

1. **Se contenter du contrôle de recette.** Un total juste peut cacher une répartition fausse de
   **102 917 580** FCFA, comme le montre le rapport par segment du chapitre 4.
2. **Confondre décrire et contrôler.** Compter les lignes d'une table n'est pas un contrôle :
   un contrôle compare à une référence extérieure.
3. **Croire qu'une contrainte déclarée est une contrainte appliquée.** Une clé primaire dans un schéma
   ne dit rien du chargement ; et **0** déclaration ne veut pas dire **0** garantie, si le contrôle
   tourne à chaque chargement.
4. **Livrer sans dictionnaire de données.** Les **127** colonnes du socle portent des règles qui ne
   se devinent pas : **2 809** lignes de retour à montants négatifs, un mois stocké tantôt en texte
   tantôt en entier, une période fiscale qui n'a que **2** valeurs.
5. **Faire relire son modèle par son auteur.** Une relecture faite par celui qui a écrit le modèle
   valide ses intentions, pas son résultat.
6. **Ne pas dater la revue.** Un modèle juste en janvier peut devenir faux en juillet, quand les
   données changent : une revue sans date n'est pas une preuve.

---

## 9. Bonnes pratiques professionnelles

1. **Brancher les quatre contrôles sur le chargement**, dans l'ordre recette, grain, orphelins,
   unicité, et faire échouer le chargement plutôt que publier.
2. **Écrire un dictionnaire de données** pour les **127** colonnes du modèle, avec type, définition
   métier, grain et règles, et le tenir à côté du script.
3. **Relire par grille**, avec les **15** points, par une personne qui n'a pas écrit le modèle, et
   conserver les réponses avec leur date.
4. **Prouver chaque point par une requête ou un nom**, jamais par une opinion : « le grain est bon »
   n'est pas une réponse, « **7** faits sur **7** portent les lignes de leur source » en est une.
5. **Déclarer les exceptions.** Le client non identifié, avec ses **43 161** ventes et
   **2 852 612 447** FCFA, est une exception assumée : une exception écrite ne se confond pas avec un
   défaut.
6. **Mesurer le coût de chaque défaut avant de le corriger**, pour arbitrer : les cinq défauts du
   modèle fautif ne coûtent pas la même chose, entre **0** clé déclarée et **42,9 %** de chiffre
   d'affaires en trop.

---

## 10. Exercice guidé

**Énoncé.** Vous recevez le modèle fautif et la grille en **15** points. Remplissez les points **6**
à **10**, chiffrez chaque défaut, et proposez la correction de deux d'entre eux.

**Étape 1.** Point **6**, les attributs recopiés. Comptez les caractères de noms de clients dans le
fait et dans la dimension : **2 826 394** contre **239 599**, soit **11,8** fois plus.

**Étape 2.** Point **7**, les deux temps. Comptez les valeurs distinctes de chaque colonne de temps :
**1 339** dates et **44** mois. Deux colonnes, deux vérités possibles.

**Étape 3.** Point **8**, l'objectif au mauvais grain. Additionnez l'objectif avec les ventes :
**6 685 260 000** FCFA de trop, soit **42,9 %** du chiffre d'affaires.

**Étape 4.** Points **9** et **10**. Comptez les clés déclarées, puis les libellés : **0** clé de
toute nature, et **16** libellés pour **7** familles.

**Attendu.** Cinq réponses chiffrées, et deux corrections : une dimension client avec une clé
étrangère pour le point **6** ; une table d'objectifs au grain magasin et mois pour le point **8**,
ce qui ramène le total à **15 595 154 955** FCFA.

---

## 11. Exercices autonomes

**Exercice 7.1.** Écrivez les quatre contrôles de recette du socle, et donnez pour chacun la
référence extérieure à laquelle il compare. Quels sont ceux qui ne pourraient pas passer sur un
modèle faux ?

**Exercice 7.2.** Le contrôle d'unicité donne **23 913** lignes et **23 913** valeurs distinctes sur
la dimension client. Écrivez la même requête sur le fait de ventes : la clé de vente est-elle unique,
et que se passerait-il si elle ne l'était pas ?

**Exercice 7.3.** Un modèle publie **22 305 610 960** FCFA de chiffre d'affaires quand la source en
donne **15 595 154 955**. Écrivez la requête fautive probable, calculez l'écart en pourcentage, et
expliquez quel contrôle l'aurait arrêtée.

**Exercice 7.4.** Choisissez trois points de la grille des **15** et écrivez, pour chacun, la preuve
exacte que vous demanderiez à un stagiaire : la requête, ou le nom de la table.

**Exercice 7.5.** Le socle déclare **0** clé primaire et **0** clé étrangère, et il compte
**0** orphelin sur **12** clés vérifiées. Expliquez en trois phrases comment ces deux affirmations
peuvent être vraies ensemble, et ce qui manque pour que la garantie soit permanente.

---

## 12. Correction détaillée

**Exercice 7.1.** L'unicité compare la clé au grain déclaré ; le grain compare le fait à sa source ;
les orphelins comparent les clés étrangères au référentiel ; la recette compare le total du modèle à
celui de la source. Aucun ne compare le modèle à lui-même. Les quatre peuvent passer sur un modèle
faux : un fait dont les dates seraient celles d'une autre période garde son nombre de lignes, son
grain et ses clés valides, et son total serait identique — c'est pourquoi la relecture existe.

**Exercice 7.2.** `SELECT COUNT(*) AS lignes, COUNT(DISTINCT id_vente) AS valeurs FROM fait_ventes;`
rend **240 000** et **240 000** : la clé de vente est unique. Si elle ne l'était pas, chaque montant
porté par un doublon serait compté deux fois dans tout rapport, et le contrôle de recette échouerait
sur la différence exacte des montants dupliqués.

**Exercice 7.3.** La requête fautive additionne deux tables qui portent toutes les deux un montant :
`SELECT (SELECT SUM(montant_ttc) FROM ventes WHERE NOT est_retour) + (SELECT SUM(montant_ttc) FROM
commande)`. Elle rend **22 305 610 960** FCFA, soit **+ 43,0 %** au-dessus des **15 595 154 955**
FCFA de la source. Le contrôle de recette l'aurait arrêtée immédiatement, puisque son unique rôle est
de comparer le total au chiffre de référence.

**Exercice 7.4.** Point **2**, l'unicité : `SELECT COUNT(*), COUNT(DISTINCT id_client) FROM
dim_client` doit rendre deux fois le même nombre, **23 913**. Point **4**, les orphelins : un
**left join** suivi d'un test de valeur nulle, qui doit rendre **0**. Point **13**, la complétude du
calendrier : deux comptages, les jours du calendrier sans fait et les dates de fait sans jour
correspondant — **0** et **0** pour les ventes, **13** pour les dates de livraison.

**Exercice 7.5.** Les deux affirmations sont vraies ensemble parce que le socle n'est pas construit
par des contraintes mais par des requêtes, et que l'unicité est vérifiée **après** construction, par
comptage, sur les **14** tables. Ce qui manque est la permanence : la garantie n'existe qu'au moment
où l'instrument s'exécute. Pour la rendre permanente, il faut brancher le contrôle sur le chargement
et refuser la publication quand il échoue.

---

## 13. Mini-projet de chapitre

**Objet.** Passer la grille de revue en **15** points sur votre propre modèle, et publier le
dictionnaire de données.

**Livrables.**

1. La grille des **15** points remplie, chaque réponse accompagnée de sa preuve : une requête, un
   compte ou un nom. Les points non revus sont écrits « non revu », jamais « conforme ».
2. Le dictionnaire des **127** colonnes du modèle, au format tableau, avec type, définition métier,
   grain et règles.
3. Les quatre contrôles de recette en un seul script, exécuté et joint au rendu avec sa sortie.
4. Une note d'une page sur les trois défauts les plus coûteux trouvés, chacun chiffré, avec la
   correction proposée et son coût estimé.

**Barème indicatif.** Grille remplie et prouvée : **4** points. Dictionnaire : **3** points.
Contrôles exécutés : **2** points. Note sur les défauts : **1** point. Total : **10** points.

**Critère de réussite.** Les quatre contrôles passent, la grille est signée et datée, et chaque point
portant sur la sémantique est justifié par une mesure, pas par une intention.

---

## 14. Résumé du chapitre

| Notion | Mesure du socle | Ce qu'elle enseigne |
|---|---|---|
| Unicité | **14** tables sur **14** | le grain se prouve en comparant deux comptages |
| Grain | **7** faits sur **7** | un fait porte exactement les lignes de sa source |
| Orphelins | **12** clés vérifiées, **0** orphelin | une clé muette disparaît d'un rapport groupé |
| Recette | **15 595 154 955** FCFA des deux côtés | la seule vérification qui porte sur le chiffre publié |
| Documentation | **315** lignes dont **99** de commentaire | le script explique la construction, pas le sens |
| Contraintes | **0** clé déclarée, **0** commentaire de colonne | la garantie est déplacée vers le contrôle, et doit être exécutée |
| Dictionnaire | **127** colonnes, **17** pour le fait principal | c'est là que vivent les règles, dont celle des retours |
| Grille de revue | **15** points, **5** échouent sur le modèle fautif | l'automatique couvre la forme, la relecture couvre le sens |
| Défaut le plus coûteux | **42,9 %** de chiffre d'affaires en trop | un objectif au mauvais grain fausse le total, pas une case |
| Le danger | **+ 43,0 %**, **+ 89,0 %** et **44** fois | trois requêtes fautives s'exécutent sans un avertissement |
| Répartition | **102 917 580** FCFA d'écart pour un total juste | la recette valide le total, jamais les cases |

**Instrument.** Les valeurs de ce chapitre sont reproductibles : `python3 tools/modele_M13.py`
exécute la section **16** de l'instrument, qui compte les tables, les faits, les clés étrangères et
les colonnes, mesure ce que le script déclare, chiffre les cinq défauts du modèle fautif et rend les
quatre textes de synthèse de la revue.

**Le module en une ligne.** Sept chapitres ont transformé un fichier plat de **240 000** lignes en un
modèle de **14** tables dont la recette est prouvée : entités et cardinalités, formes normales, grain
et additivité, étoile et historisation, flocon et variantes, temps et calendrier, et cette revue
finale.

---

## 15. À retenir

1. **Quatre contrôles suffisent à décider qu'un modèle est livrable** : unicité (**14** sur **14**),
   grain (**7** sur **7**), orphelins (**0** sur **12** clés) et recette (**15 595 154 955** FCFA des
   deux côtés). Ils ont tous la même force : ils comparent le modèle à une référence extérieure.
2. **Ce qu'un contrôle ne voit pas décide de ce qu'un modèle vaut.** Un nom recopié **11,8** fois,
   deux colonnes de temps, un objectif posé sur la ligne de vente (**+ 42,9 %**), **0** clé
   déclarée, **16** libellés pour **7** familles : cinq défauts que seule la relecture attrape.
3. **Le danger n'est pas le modèle qui plante, c'est le modèle qui répond.** **+ 43,0 %**,
   **+ 89,0 %**, **44** fois : trois modèles fautifs du socle s'exécutent sans erreur.

> **À retenir.** Un modèle de données se livre avec deux choses : la preuve qu'il est juste et la
> mémoire de ses choix. La preuve tient en quatre requêtes exécutées à chaque chargement ; la mémoire
> tient dans un dictionnaire de données et dans les **15** réponses d'une grille de revue, signées et
> datées. Le modèle du fil rouge a les preuves : **14** tables sur **14**, **7** faits sur **7**,
> **0** orphelin, la recette au franc près. Il lui manque la mémoire, et la produire est l'objet du
> projet.

---

## 16. Évaluation formative

1. Citez les quatre contrôles de recette et la référence extérieure de chacun.
2. Pourquoi un contrôle qui ne compare rien à une référence extérieure n'est-il pas un contrôle ?
3. Le socle déclare **0** clé primaire. L'unicité est-elle pour autant non vérifiée ? Justifiez.
4. Que manque-t-il pour que la garantie d'unicité soit permanente plutôt que ponctuelle ?
5. Combien de colonnes compte le modèle, et quelle est la table la plus large ?
6. Quelles sont les quatre familles de la grille des **15** points, et que demande chacune ?
7. Citez les cinq défauts du modèle fautif et la mesure qui prouve chacun.
8. Le défaut des attributs recopiés coûte **2 826 394** caractères au lieu de **239 599** : quelle
   conséquence cela a-t-il au-delà du volume ?
9. Le contrôle de recette passe sur un modèle dont le rapport par segment est faux de
   **102 917 580** FCFA. Comment est-ce possible, et quel contrôle faut-il ajouter ?
10. Trois modèles fautifs rendent **22 305 610 960**, **29 474 916 530** et **686 186 818 020** FCFA.
    Donnez l'écart de chacun par rapport au chiffre juste, et la leçon commune.

**Corrigé.** 1. Unicité (le grain déclaré de la table), grain (la source du fait), orphelins (le
référentiel), recette (le total de la source). 2. Parce qu'il se contente de décrire : compter les
lignes d'une table ne prouve aucune de ses propriétés. 3. Non : l'unicité est mesurée sur les
**14** tables, et la dimension client rend **23 913** lignes pour **23 913** valeurs distinctes.
4. Le branchement du contrôle sur le chargement, avec échec du chargement en cas de verdict négatif.
5. **127** colonnes, la plus large étant le fait de ventes avec **17** colonnes. 6. Structure
(clés, grain, liens, totaux), sémantique (le modèle dit-il la vérité des données), histoire
(historisations et calendrier), usage (un tiers peut-il s'en servir). 7. Attributs recopiés
(**2 826 394** caractères recopiés contre **239 599** dans la dimension, soit **8,5 %** du volume
utile), deux temps (**1 339** dates et **44** mois),
objectif sur la vente (**6 685 260 000** FCFA, **42,9 %**), **0** clé déclarée, **16** libellés pour
**7** familles. 8. La divergence : la même information vit à des dizaines de milliers d'endroits, et
une correction faite à un seul endroit crée deux versions de la vérité. 9. Parce que le total est
juste et que les cases ne le sont pas : une jointure qui déplace des montants entre segments ne
change pas la somme. Il faut ajouter un contrôle de répartition, segment par segment. 10.
**+ 43,0 %**, **+ 89,0 %** et **44** fois. La leçon : une requête qui s'exécute n'est pas une requête
juste, et un chiffre faux ne prévient jamais.
