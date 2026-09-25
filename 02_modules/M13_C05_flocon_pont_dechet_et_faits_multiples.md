# Module M13.C05 — Le schéma en flocon et ses variantes

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **choisir entre l'étoile et le flocon** en connaissant le prix de chacun : sur le fil rouge, la
   même question posée par famille de produits demande **1** jointure en étoile et **3** en flocon,
   pour un résultat **identique** — le flocon ne rend pas le chiffre plus juste, il rend la
   hiérarchie partageable ;
2. **reconnaître une table de pont** et l'écrire sans doubler les montants : le socle porte un vrai
   N-M (**240 000** lignes pour **146 161** tickets, **1,64** ligne par ticket), et le pont qui
   recopie le montant du ticket sur chacune de ses lignes produit **31 298 080 184** FCFA au lieu de
   **15 595 154 955**, soit un facteur **2,01** ;
3. **ranger les petits drapeaux hétérogènes dans une dimension déchet** : les **5** modes de paiement,
   les **3** canaux et le drapeau de retour occupent **30** combinaisons sur **30** possibles, qu'une
   seule colonne à joindre suffit à porter ;
4. **traiter les faits multiples sans les mélanger** : sur le socle, les **2 809** lignes de retour
   sont des montants **négatifs** (**175 169 798** FCFA, **1,17 %** des lignes) rangés dans la même
   table que les ventes, avec un drapeau — un choix qui se paie d'une règle de filtrage ;
5. **dénormaliser exprès, et le mesurer** : écrire la famille **7** fois (table des familles) ou
   **154** fois (dans la dimension produit) est une décision, pas un accident.

---

## 2. Pourquoi cette notion est importante

Les chapitres précédents ont construit une étoile propre : un fait au centre, des dimensions autour,
une jointure par attribut. Ce chapitre traite les cas où **l'étoile ne suffit plus** — et il n'en
invente aucun : les quatre situations sont déjà dans le socle.

**La hiérarchie partagée.** La famille de produits sert à la fois au rapport de ventes, à celui des
ruptures et à celui du stock. Si elle est écrite dans `dim_produit`, chaque rapport la lit à sa
manière ; si elle est extraite dans sa propre table, elle devient un objet unique, que l'on peut
corriger une fois. C'est **le flocon**, et son prix est visible : **173** lignes au lieu de **154**,
et **3** jointures au lieu d'**1**.

**Le N-M réel.** Un ticket porte **1,64** produit en moyenne, et **45,4 %** des tickets en portent
plus d'un. Chaque ticket est donc relié à plusieurs produits, et chaque produit à plusieurs tickets :
c'est une relation **plusieurs à plusieurs**, que seule une table de pont (ou une table de faits au
grain de la ligne) peut représenter. Le danger n'est pas conceptuel mais arithmétique : un pont qui
porte le montant du ticket sur chacune de ses lignes fabrique un chiffre d'affaires **2,01** fois
trop grand.

**Les drapeaux hétérogènes.** Un fait de ventes porte trois petites listes de valeurs : **5** modes de
paiement, **3** canaux, et le drapeau de retour. Groupées sur trois colonnes, elles encombrent chaque
requête ; rangées dans une petite table, elles deviennent une **dimension déchet** de **30** lignes
que l'on joint une fois.

**Les faits multiples.** Retours, ruptures, coûts logistiques, objectifs : le modèle porte **7**
tables de faits, et **aucune** ne se dit « la même chose » qu'une autre. Le cas le plus trompeur est
le retour, qui ressemble à une vente en négatif — et qui l'est, mais avec une conséquence : tout
rapport qui oublie de le filtrer publie **175 169 798** FCFA d'indicateurs faux.

> **Dans les faits.** Le socle a fait un choix, et ce chapitre le rend visible : les retours vivent
> **dans** `fait_ventes`, distingués par un drapeau, et non dans une table séparée. Ce choix n'est ni
> bon ni mauvais — il déplace la responsabilité du modèle vers **chaque requête**. Un modèle qui fait
> ce choix peut publier un chiffre d'affaires net juste **ou** un chiffre d'affaires brut juste, mais
> il ne peut pas empêcher un rapport de faire la moyenne des deux.

---

## 3. Explication simple — l'entrepôt, la fiche d'expédition et la caisse à objets perdus

**Le flocon, c'est ranger la fiche produit par étagères.** Dans l'étoile, la fiche produit porte tout
en clair : le nom du produit, sa sous-catégorie **et** sa famille. C'est pratique et redondant : la
famille « Matériaux » est écrite **154** fois, une fois par produit. Dans le flocon, on range par
niveaux : une fiche par produit, qui renvoie à une fiche de sous-catégorie (au nombre de **12**), qui
renvoie elle-même à une fiche de famille (**7**). La famille n'est plus écrite que **7** fois — mais
il faut maintenant ouvrir trois tiroirs pour aller du produit à la famille.

**La table de pont, c'est la fiche d'expédition.** Un camion livre plusieurs commandes ; une commande
part dans plusieurs camions. Aucune des deux fiches ne suffit : il faut une troisième fiche, la
**feuille de tournée**, qui dit « ce camion a pris ces commandes ». Sur le fil rouge, le ticket joue
le rôle de la tournée : il porte plusieurs produits (**1,64** en moyenne, jusqu'à **4**). Le piège est
de croire qu'une tournée peut porter le **montant** : un camion qui livre dix commandes ne vaut pas
dix fois le montant de chacune. Le socle le mesure : compter le montant du ticket sur chacune de ses
lignes fait passer le chiffre d'affaires de **15 595 154 955** à **31 298 080 184** FCFA.

**La dimension déchet, c'est la caisse à objets perdus.** Trois petites listes de valeurs qui ne
méritent pas chacune sa propre dimension : le mode de paiement, le canal de vente, le retour. On les
met ensemble dans une même petite table, et chaque ligne de la table devient une combinaison. Le socle
en occupe **30** sur **30** — toutes les combinaisons existent, et cette information a de la valeur :
une combinaison absente serait une anomalie à expliquer.

**Les faits multiples, ce sont les différents compteurs de l'entrepôt.** Un compteur de ventes, un
compteur de retours, un compteur de ruptures, un compteur d'objectifs : quatre appareils, quatre
unités, quatre histoires. Ils se lisent **à côté**, jamais additionnés.

---

## 4. Vocabulaire essentiel

| Terme | Définition | Sur le fil rouge |
|---|---|---|
| **Schéma en flocon** | hiérarchie éclatée en plusieurs tables reliées entre elles | produit → sous-catégorie → famille |
| **Hiérarchie partagée** | niveaux d'agrégation réutilisables par plusieurs rapports | **12** sous-catégories, **7** familles |
| **Dénormalisation volontaire** | recopier un attribut pour économiser une jointure, en le déclarant | famille dans `dim_produit` |
| **Relation N-M** | plusieurs à plusieurs : chaque objet d'un côté en touche plusieurs de l'autre | tickets et produits |
| **Table de pont** | table qui matérialise un lien N-M sans porter de montant | ligne de ticket, tournée |
| **Facteur de répétition** | rapport entre le montant dupliqué et le montant réel | **2,01** sur le socle |
| **Dimension déchet** | table qui rassemble les petits drapeaux peu nombreux | **30** combinaisons |
| **Attribut de fait** | colonne du fait qui n'est ni clé ni mesure | `mode_paiement`, `canal` |
| **Faits multiples** | plusieurs tables de faits, non additionnables entre elles | **7** faits, dont les retours |
| **Table de faits de retours** | fait séparé portant les retours, quand on ne veut pas de drapeau | choix non retenu ici |
| **Agrégat avant jointure** | réduire au grain commun **avant** de joindre | `GROUP BY` puis `JOIN` |
| **Filtre de périmètre** | condition qui définit ce que le rapport couvre | `est_retour = 0` |

> **Définition.** Un **schéma en flocon** est un modèle en étoile dont une ou plusieurs dimensions
> sont **normalisées** : une hiérarchie est éclatée en tables successives, reliées par des clés, au
> prix d'une jointure par niveau. Il s'oppose à l'**étoile**, où chaque dimension porte directement
> tous ses attributs.

> **Définition.** Une **table de pont** (ou table d'association) est une table qui représente une
> relation plusieurs à plusieurs entre deux objets — un ticket et ses produits, une campagne et ses
> produits, une commande et ses tournées. Elle ne porte **aucun montant** : c'est précisément ce qui
> la distingue d'une table de faits.

> **Définition.** Une **dimension déchet** rassemble en une seule table les attributs de faible
> cardinalité et sans hiérarchie (drapeaux, statuts, codes courts), pour éviter d'encombrer la table
> de faits ou de créer une dimension par drapeau.

> **Définition.** Le **facteur de répétition** mesure combien de fois un montant est compté quand on
> le lit à travers une relation N-M : c'est le quotient du total obtenu par le total réel. Sur le fil
> rouge, il vaut **2,01** quand le montant du ticket est répété sur chacune de ses lignes.

> **Définition.** Des **faits multiples** sont plusieurs tables de faits qui décrivent des processus
> différents — ventes, retours, ruptures, objectifs. Elles partagent des dimensions conformes, et ne
> s'additionnent **jamais** entre elles.

---

## 5. Cours approfondi

### 5.1 L'étoile et le flocon : deux façons de ranger la même information

La différence tient en une phrase : dans l'étoile, la dimension porte tous ses attributs ; dans le
flocon, elle renvoie ses niveaux à des tables successives.

Le socle a choisi l'étoile, et le chapitre C02 a montré pourquoi la famille est écrite dans
`dim_produit`. Construisons le flocon pour mesurer ce que ce choix coûte et rapporte :

| | Étoile | Flocon |
|---|---|---|
| Tables pour la hiérarchie produit | `dim_produit` seul | `dim_produit`, `dim_sous_categorie`, `dim_famille` |
| Lignes au total | **154** | **173** (**154** + **12** + **7**) |
| Jointures pour aller du fait à la famille | **1** | **3** |
| Temps mesuré sur le fil rouge | **3** ms | **3** ms |
| Résultat obtenu | Matériaux **3 535 582 421** FCFA | **le même** |
| La famille est écrite | **154** fois | **7** fois |

Deux observations, et elles sont contre-intuitives.

**Le flocon ne rend pas plus juste.** La mesure le prouve : les deux lectures rendent un résultat
**identique**. Choisir le flocon ne protège d'aucune erreur de calcul.

**Le flocon ne coûte rien à la lecture, et beaucoup à la discipline.** **3** ms contre **3** ms sur
ce moteur, médiane de sept exécutions : ces durées changent d'une
exécution et d'une machine à l'autre, seul le rapport entre les deux lectures est stable : l'écart est négligeable, comme celui mesuré en C02 pour la normalisation. Le vrai prix est
ailleurs : trois jointures au lieu d'une, c'est trois fois plus d'occasions de se tromper de clé, et
une requête que le lecteur ne comprend plus d'un coup d'œil.

> **Attention.** Le flocon se justifie quand une **hiérarchie est partagée** par plusieurs
> dimensions ou plusieurs processus, ou quand un niveau doit être **corrigé une fois pour toutes**.
> Il ne se justifie pas par le goût de la normalisation : le socle compte **7** familles pour **154**
> produits, et personne n'a jamais eu besoin de corriger une famille sans toucher ses produits en
> quatre ans d'historique. Le jour où trois référentiels métier se mettront à écrire « Matériaux »
> de trois façons, la question se reposera.

### 5.2 La table de pont : le N-M et son facteur de répétition

Le socle porte une relation plusieurs à plusieurs, et elle est massive :

| Mesure | Valeur |
|---|---|
| Lignes de ventes | **240 000** |
| Tickets distincts | **146 161** |
| Lignes par ticket | **1,64** en moyenne, jusqu'à **4** |
| Tickets à une seule ligne | **79 763** |
| Tickets à plus d'une ligne | **66 398**, soit **45,4 %** |

Chaque ticket est relié à plusieurs produits, et chaque produit apparaît dans plusieurs tickets :
c'est un N-M, et il est résolu **par la table de faits elle-même**, dont le grain est la ligne de
ticket — et non le ticket. C'est le choix le plus robuste : la table de faits *est* le pont, et elle
porte les montants au bon grain.

La faute apparaît quand on fait du **ticket** un objet porteur de montant, puis qu'on le relie à ses
produits par un pont : le montant du ticket se retrouve alors sur chacune de ses lignes.

```sql
-- Ce que fait cette requete : elle recopie le montant du ticket sur TOUTES ses lignes
WITH t AS (
  SELECT id_ticket, SUM(montant_ttc) AS ca_ticket
  FROM fait_ventes WHERE est_retour = 0 GROUP BY id_ticket
)
SELECT ROUND(SUM(t.ca_ticket)) AS ca_duplique
FROM fait_ventes f JOIN t ON t.id_ticket = f.id_ticket
WHERE f.est_retour = 0;
```

Résultat : **31 298 080 184** FCFA au lieu de **15 595 154 955**, facteur **2,01**. Le facteur n'est
pas le nombre moyen de lignes par ticket (**1,64**) : il est **pondéré** par le montant, car les gros
tickets ont tendance à porter plus de lignes. C'est une leçon à retenir : **le facteur de répétition
se mesure, il ne se déduit pas** d'un ratio de comptage.

> **Attention.** Le facteur de répétition d'un montant ne se déduit **jamais** d'un ratio de
> comptage. Le socle compte **1,64** ligne par ticket, et le montant lu à travers un pont est
> multiplié par **2,01** : l'écart vient de la pondération, car les tickets à plusieurs lignes pèsent
> plus lourd que les tickets à une ligne. Un contrôle qui se contenterait de comparer les comptages
> aurait conclu « la duplication est sous contrôle » alors qu'il manquait **15 702 925 229** FCFA.

Réserve honnête et importante : dans cet exemple, la table de pont est `fait_ventes` elle-même, donc
le montant dupliqué vient d'une agrégation préalable au grain du ticket. La règle générale s'écrit
ainsi : **une table de pont ne porte pas de montant** ; si un montant doit être rattaché à un objet du
N-M (une campagne, une tournée), il appartient à une table de faits propre, à un grain déclaré — et
si l'on doit lire les deux ensemble, on agrège chaque côté **avant** de joindre.

Le cas classique — une **campagne** qui couvre plusieurs produits, et un produit couvert par
plusieurs campagnes — n'est pas instrumenté sur le socle : il est **cité, non mesuré**. Sa structure
est la même que celle du ticket, à une différence près qui change tout : le montant de la campagne
n'est rattaché à aucun produit en particulier, donc il n'y a **pas** de grain commun possible, et
toute lecture de type « chiffre d'affaires par campagne » doit s'accompagner d'une règle de partage
écrite (par exemple au prorata du chiffre d'affaires des produits couverts).

### 5.3 La dimension déchet : trois drapeaux, une table

Le fait de ventes porte trois colonnes de faible cardinalité : `mode_paiement` (**5** valeurs),
`canal` (**3** valeurs) et `est_retour` (**2** valeurs). Ensemble, elles occupent **30**
combinaisons — et sur le socle, **30** sur **30** sont effectivement occupées.

Trois façons de les traiter :

| Solution | Ce qu'on écrit dans les requêtes | Ce que ça coûte |
|---|---|---|
| Les laisser dans le fait | `GROUP BY mode_paiement, canal, est_retour` | trois colonnes à répéter partout |
| Trois dimensions séparées | trois jointures | trois tables pour **5**, **3** et **2** lignes |
| Une dimension déchet | une jointure, `GROUP BY id_dechet` | un identifiant opaque à décoder |

Le socle a choisi la première solution — les trois colonnes sont dans le fait — et c'est défendable à
cette taille. La dimension déchet devient préférable dès que le nombre de drapeaux augmente : avec
**6** drapeaux de deux valeurs, la table de faits porterait **6** colonnes là où une seule clé
suffirait.

> **Conseil professionnel.** Construisez la dimension déchet **à partir des données**, pas d'une
> liste théorique de combinaisons : les **30** combinaisons du socle sont toutes occupées, mais rien
> ne garantit qu'elles le restent. Une dimension déchet construite sur les valeurs observées garde sa
> propriété la plus utile : **toute combinaison absente est une anomalie** — et c'est exactement le
> signal qu'un rapport de qualité attend.

### 5.4 Les faits multiples : quatre appareils, quatre unités

Le modèle porte **7** tables de faits. Le chapitre C03 en a mesuré les grains ; ce chapitre traite la
question du **partage des montants**.

Le cas le plus instructif est le retour. Sur le socle, un retour est une **ligne de vente à montant
négatif** : **2 809** lignes, **175 169 798** FCFA, **1,17 %** des lignes, distinguées par
`est_retour = 1`. Deux modélisations possibles :

| Choix | Avantage | Ce qu'il impose |
|---|---|---|
| **Un drapeau** dans `fait_ventes` (retenu) | un seul grain, un seul chiffre à filtrer | chaque requête doit filtrer `est_retour = 0` |
| **Une table de faits** de retours | impossible de l'oublier | toute lecture nette doit joindre ou soustraire deux tables |

Le socle a choisi le drapeau, et le chapitre C02 de M12 en a montré la conséquence chiffrée : le
chiffre d'affaires **net** vaut **15 595 154 955** FCFA et le chiffre d'affaires **toutes lignes**
**15 419 985 157** FCFA — l'écart, **175 169 798** FCFA, est exactement le montant des retours.
Deux chiffres justes, deux définitions, et une seule question à trancher : **laquelle publie-t-on ?**

Les autres faits multiples du modèle — ruptures (**2 428** lignes), logistique (**264**), objectifs
(**218**), stock mensuel (**6 776**), commandes et encaissements (**9 000** chacun) — ne se partagent
aucun montant : chacun mesure son processus. Ce qui les unit, ce sont les **dimensions conformes** du
chapitre C04 : le magasin, le produit, le client et le temps. C'est par elles qu'on les compare, et
jamais par une addition.

### 5.5 Dénormaliser exprès : la seule question qui compte

Le mot « dénormaliser » porte une réputation injuste : il laisserait croire qu'on renonce à la
rigueur. C'est faux. Une dénormalisation assumée est une **décision documentée**, avec un gain et un
coût.

| Décision du socle | Gain mesuré | Coût assumé |
|---|---|---|
| Famille écrite dans `dim_produit` | **1** jointure au lieu de **3** | **154** écritures au lieu de **7** |
| Trois drapeaux laissés dans le fait | aucune jointure pour les lire | **3** colonnes à grouper |
| Retours dans la table de ventes | un seul grain à connaître | un filtre à ne jamais oublier |

> **À retenir.** Le choix entre deux variantes de modèle ne se tranche pas par principe : il se
> tranche par une mesure portant sur quatre chiffres — **combien de lignes**, **combien de
> jointures**, **combien de temps**, **quel résultat**. Sur le fil rouge, l'étoile et le flocon
> donnent le même résultat pour **1** et **3** jointures ; ce n'est que si le résultat avait différé
> que le choix aurait été autre chose qu'une commodité.

La règle qui se dégage de ces trois lignes tient en une phrase : **on dénormalise pour économiser des
gestes, jamais pour économiser de la vérité**. Recopier la famille économise deux jointures et ne
change aucun chiffre — le résultat mesuré est identique. Recopier un montant dans une table de pont
économise une agrégation et **change tous les chiffres** : c'est la frontière.

---

## 6. Exemple concret — le ticket qui vaut quatre fois son montant

Prenez un ticket ordinaire du fil rouge, avec **4** lignes (le maximum du socle) : deux sacs de
ciment, un pot de peinture, un rouleau, une pince.

**Vu au grain de la ligne** — le grain de `fait_ventes` — ce ticket est **4** lignes, chacune avec sa
quantité et son montant. Le chiffre d'affaires du ticket est la somme de ses 4 lignes, comptée
**une fois**.

**Vu au grain du ticket**, si l'on décide que le ticket est l'objet porteur du montant, on obtient une
ligne par ticket, avec le total du ticket. Jusque-là, rien de faux : c'est simplement un autre grain.

**Vu à travers un pont**, le danger apparaît. Si l'on relie le ticket à ses 4 produits par une table
de pont qui porte aussi `ca_ticket`, alors le montant du ticket est lu **4** fois. À l'échelle du
socle, cela donne **31 298 080 184** FCFA au lieu de **15 595 154 955** — facteur **2,01**. Et le
facteur n'est **pas** 1,64 : il est plus grand, parce que les tickets à plusieurs lignes pèsent plus
lourd en montant que les tickets à une seule ligne.

Ce que ce ticket enseigne, en une phrase : **une table de pont sert à relier, pas à mesurer.** Le
montant appartient au grain qui le compte ; le pont dit seulement quels objets vont ensemble.

---

## 7. Démonstration pas à pas — quatre gestes

**Étape 1 — décider étoile ou flocon, et l'écrire.**

Posez la question du partage : la hiérarchie est-elle utilisée par plusieurs rapports, ou par un
seul ? Sur le fil rouge, la famille de produits sert aux ventes, au stock et aux ruptures : elle est
**partagée**. Le socle la garde pourtant dans `dim_produit`, avec **7** valeurs pour **154** lignes :
c'est un choix explicite, écrit dans le commentaire de la table.

**Étape 2 — mesurer le prix de la variante non retenue.**

```sql
CREATE OR REPLACE TABLE dim_sous_categorie AS
SELECT DISTINCT sous_categorie, famille FROM dim_produit;
CREATE OR REPLACE TABLE dim_famille AS SELECT DISTINCT famille FROM dim_produit;
```

Puis la même question, par les deux chemins, et la comparaison : **1** jointure et **3** ms en étoile,
**3** jointures et **3** ms en flocon, résultat **identique**. Une variante se mesure avant d'être
écartée, sinon on ne saura pas répondre à celui qui la proposera dans six mois.

**Étape 3 — écrire la contrainte du pont.**

La règle tient en une ligne, et elle s'écrit dans le modèle : **une table de pont ne porte pas de
montant**. Si un montant doit y apparaître, c'est le signe que l'objet du N-M est en réalité un fait
— et il lui faut sa propre table, à son propre grain déclaré.

**Étape 4 — vérifier le facteur de répétition.**

```sql
-- Controle : le montant doit etre identique avec et sans passage par le pont
SELECT ROUND(SUM(montant_ttc)) FROM fait_ventes WHERE est_retour = 0;
```

Attendu : **15 595 154 955** FCFA, identique à toute autre lecture du même périmètre. Toute valeur
supérieure signale une duplication — le facteur mesuré (**2,01** sur le socle) dit de combien.

---

## 8. Erreurs fréquentes

| Erreur | Ce qu'on observe | La correction |
|---|---|---|
| Mettre un montant dans une table de pont | **31 298 080 184** FCFA au lieu de **15 595 154 955** | le montant reste dans la table de faits |
| Déduire le facteur de répétition du nombre de lignes | on attend **1,64**, on mesure **2,01** | mesurer le facteur, toujours |
| Floconner sans raison | **3** jointures au lieu d'**1** pour un résultat identique | partager la hiérarchie, ou l'écrire dans la dimension |
| Garder un drapeau sans règle de filtre | **175 169 798** FCFA de retours dans le net | écrire la règle, et la contrôler |
| Créer une dimension par drapeau | trois tables de **5**, **3** et **2** lignes | une dimension déchet, ou les colonnes du fait |
| Additionner deux faits multiples | voir chapitre C03 : **+ 43,0 %** | comparer par dimensions conformes |

---

## 9. Bonnes pratiques professionnelles

1. **Une variante de modèle se mesure avant d'être retenue ou écartée** : lignes, jointures, temps,
   résultat. Le socle applique cette règle à l'étoile contre le flocon.
2. **Une table de pont ne porte que des clés** — et, si elle doit porter une pondération, elle la
   déclare comme telle.
3. **Le facteur de répétition se contrôle sur le montant**, jamais sur les comptages : le socle donne
   **2,01** là où le ratio de lignes vaut **1,64**.
4. **Le drapeau de périmètre s'écrit dans le nom du rapport** : « chiffre d'affaires net, retours
   exclus » évite les discussions au moment de la publication.
5. **Une dimension déchet se construit sur les combinaisons observées**, pour que toute combinaison
   absente devienne une anomalie détectable.
6. **Les faits multiples se comparent par les dimensions conformes** du chapitre C04, jamais par
   addition.

---

## 10. Exercice guidé

**Sujet.** Un rapport publie « le chiffre d'affaires par mode de paiement », et un second publie
« le chiffre d'affaires par canal et par mode de paiement ». Les deux doivent sommer au même total.
Un stagiaire a écrit la première requête sans filtrer les retours. Vous avez vingt minutes pour
trouver l'écart, le chiffrer et corriger.

**Étape 1 — écrire les deux requêtes telles quelles.** La première groupe sur `mode_paiement` sans
condition ; la seconde groupe sur `canal` et `mode_paiement` avec `est_retour = 0`.

**Étape 2 — mesurer l'écart.** Le montant des retours est de **175 169 798** FCFA, soit **1,17 %**
des lignes : le total de la première requête vaut **15 419 985 157** FCFA (toutes lignes), celui de la
seconde **15 595 154 955** FCFA (net). Les deux sont **justes** ; elles ne parlent pas du même
périmètre.

**Étape 3 — nommer la règle.** Un fait de ventes porte deux définitions dans une seule table. Le
rapport doit porter sa définition dans son titre : « net, retours exclus » ou « toutes lignes,
retours inclus ». La pire des réponses est de ne rien écrire et de laisser le lecteur comparer deux
chiffres différents en croyant à une erreur de calcul.

**Étape 4 — vérifier la couverture des combinaisons.** Les **5** modes de paiement et les **3** canaux
occupent **30** combinaisons sur **30** possibles : le rapport par canal et mode de paiement affiche
donc **30** lignes, sans trou. Si une combinaison manquait, il faudrait la signaler avant de conclure
à une absence d'activité.

**Barème (15 points) :** les deux requêtes écrites (3) · l'écart chiffré et expliqué (4) · la règle
de nommage formulée (4) · le contrôle des **30** combinaisons (4).

---

## 11. Exercices autonomes

**Exercice 5.1.** Construisez le flocon de la hiérarchie produit sur le socle : deux tables
(`dim_sous_categorie`, `dim_famille`) et la dimension produit allégée. Donnez le nombre de lignes des
trois tables, la requête qui donne le chiffre d'affaires par famille dans chaque modèle, et vérifiez
que les deux résultats sont identiques. Concluez en trois lignes sur ce que le flocon a rapporté.

**Exercice 5.2.** Écrivez la requête qui compte les tickets portant plus d'une ligne, puis celle qui
donne la moyenne de lignes par ticket. Comparez ces deux nombres au facteur de répétition du montant
(**2,01**) et expliquez, en cinq lignes, pourquoi le facteur est plus grand que la moyenne.

**Exercice 5.3.** Le N-M des tickets. Écrivez une table de pont `pont_ticket_produit` (un ticket, un
produit) et la requête qui donne, pour chaque produit, le nombre de tickets distincts où il apparaît.
Puis dites pourquoi il serait faux d'y ajouter une colonne `montant_ticket`, en citant le chiffre que
cette colonne ferait apparaître.

**Exercice 5.4.** La dimension déchet. Construisez `dim_dechet` à partir des combinaisons observées
de `mode_paiement`, `canal` et `est_retour`, puis écrivez la requête qui donne le chiffre d'affaires
par canal **à travers** cette dimension. Combien de lignes contient la dimension, et pourquoi ce
nombre est-il exactement égal à l'espace des combinaisons possibles ?

**Exercice 5.5.** Les retours. Écrivez les deux requêtes du fil rouge : le chiffre d'affaires **net**
et le chiffre d'affaires **toutes lignes**. Donnez les deux totaux et l'écart, puis expliquez en
quatre lignes ce qu'un rapport gagne et ce qu'il perd en choisissant le drapeau plutôt qu'une table de
retours séparée.

---

## 12. Correction détaillée

**Exercice 5.1.** Les trois tables comptent **154** produits, **12** sous-catégories et **7**
familles, soit **173** lignes au total contre **154** en étoile. Les deux requêtes (par famille, avec
**1** jointure et avec **3**) rendent un résultat **identique** : Matériaux **3 535 582 421** FCFA en
tête. Le flocon n'a donc rien changé au chiffre ; il a partagé la hiérarchie et ramené l'écriture de
la famille de **154** à **7** occurrences — au prix de deux jointures supplémentaires, pour un temps
de lecture indiscernable (**3** ms dans les deux cas). Il se justifie le jour où plusieurs référentiels doivent partager le même niveau
« famille », pas avant.

**Exercice 5.2.** Le comptage :

```sql
SELECT COUNT(*) AS tickets_multi FROM (
  SELECT id_ticket FROM fait_ventes GROUP BY id_ticket HAVING COUNT(*) > 1
);
```

**66 398** tickets portent plus d'une ligne, soit **45,4 %**, et la moyenne vaut **1,64** ligne par
ticket. Le facteur de répétition du montant vaut **2,01**, donc **plus grand** que la moyenne : quand
on répète un montant, les tickets lourds — qui portent souvent plus de lignes — comptent davantage.
Le facteur est une moyenne **pondérée par le montant**, pas un ratio de comptage ; c'est pourquoi il
se mesure.

**Exercice 5.3.** La table de pont et la requête :

```sql
CREATE OR REPLACE TABLE pont_ticket_produit AS
SELECT DISTINCT id_ticket, id_produit FROM fait_ventes;

SELECT id_produit, COUNT(DISTINCT id_ticket) AS tickets
FROM pont_ticket_produit GROUP BY id_produit ORDER BY 2 DESC;
```

Ajouter `montant_ticket` à cette table serait faux : le montant du ticket se retrouverait répété
autant de fois que le ticket a de produits, et le chiffre d'affaires lu à travers la table passerait
de **15 595 154 955** à **31 298 080 184** FCFA — facteur **2,01**. Une table de pont relie des
objets ; elle ne mesure pas.

**Exercice 5.4.** La dimension déchet et sa lecture :

```sql
CREATE OR REPLACE TABLE dim_dechet AS
SELECT ROW_NUMBER() OVER (ORDER BY mode_paiement, canal, est_retour) AS id_dechet,
       mode_paiement, canal, est_retour
FROM (SELECT DISTINCT mode_paiement, canal, est_retour FROM fait_ventes);

SELECT COUNT(*) FROM dim_dechet;   -- 30

SELECT d.canal, ROUND(SUM(f.montant_ttc)) AS ca
FROM fait_ventes f
JOIN dim_dechet d
  ON d.mode_paiement = f.mode_paiement
 AND d.canal = f.canal
 AND d.est_retour = f.est_retour
WHERE f.est_retour = 0
GROUP BY 1 ORDER BY 2 DESC;
```

La lecture par la dimension donne Magasin **10 295 255 849** FCFA, Livraison **3 732 464 992** FCFA et
Téléphone **1 567 434 114** FCFA.

La dimension contient **30** lignes, soit exactement l'espace des combinaisons possibles
(**5** modes de paiement × **3** canaux × **2** valeurs de retour). Cette égalité est une information,
pas une coïncidence : elle dit qu'aucune combinaison n'est absente — et donc que toute combinaison
manquante, plus tard, signalera un changement de pratique ou une anomalie.

La jointure se fait sur les **trois** colonnes : c'est le prix de cette dimension, et il faut le
dire — la clé `id_dechet` sert à lire la table, pas à la joindre. Une variante plus économique
consiste à calculer cet identifiant **dans** la table de faits, au chargement ; elle se paie d'une
colonne dans les faits, et se justifie quand la dimension est jointe par plusieurs rapports.

**Exercice 5.5.** Les deux requêtes :

```sql
SELECT ROUND(SUM(montant_ttc)) FROM fait_ventes WHERE est_retour = 0;   -- 15 595 154 955 FCFA
SELECT ROUND(SUM(montant_ttc)) FROM fait_ventes;                        -- 15 419 985 157 FCFA
```

L'écart est de **175 169 798** FCFA, exactement le montant des **2 809** lignes de retour
(**1,17 %** des lignes). Le drapeau gagne la simplicité : un seul grain, un seul objet à connaître.
Il perd l'impossibilité de l'oubli : toute requête doit filtrer, et rien dans le modèle ne l'impose.
La table de retours séparée gagne la sécurité et perd la simplicité : toute lecture nette devient une
opération sur deux tables, et il faut décider ce que signifie « jointure » entre une vente et un
retour.

---

## 13. Mini-projet de chapitre

**« La note de variante : étoile ou flocon pour la hiérarchie produit »** (2 h). Produisez, pour le
fil rouge : (1) le tableau comparatif mesuré des deux modèles — lignes, jointures, temps, résultat —
avec les requêtes qui l'établissent ; (2) la requête du N-M des tickets et son contrôle de
non-duplication ; (3) `dim_dechet` construite sur les combinaisons observées, avec le nombre de
combinaisons occupées et l'espace théorique ; (4) la liste des **3** dénormalisations volontaires du
socle, chacune avec son gain mesuré et son coût assumé ; (5) une page de règle : « quand passer au
flocon, quand garder un drapeau, quand séparer un fait ». Ce livrable alimente **P4** (note de choix,
3 pages) du projet de module.

---

## 14. Résumé du chapitre

| Notion | Ce qu'il faut retenir |
|---|---|
| Flocon | **173** lignes au lieu de **154**, **3** jointures au lieu d'**1** |
| Résultat du flocon | **identique** à l'étoile : Matériaux **3 535 582 421** FCFA |
| Prix du flocon | Deux jointures de plus à écrire juste, et un temps de lecture indiscernable |
| Gain du flocon | la famille écrite **7** fois au lieu de **154** |
| N-M du socle | **240 000** lignes pour **146 161** tickets (**1,64** par ticket) |
| Tickets multi-lignes | **66 398**, soit **45,4 %**, jusqu'à **4** lignes |
| Facteur de répétition | **2,01** (**31 298 080 184** contre **15 595 154 955** FCFA) |
| Dimension déchet | **30** combinaisons occupées sur **30** possibles |
| Retours | **2 809** lignes, **175 169 798** FCFA, **1,17 %** des lignes |
| Deux périmètres | net **15 595 154 955** · toutes lignes **15 419 985 157** FCFA |
| Dénormaliser | pour économiser des gestes, jamais de la vérité |

---

## 15. À retenir

1. **Le flocon ne rend pas le chiffre plus juste** : il rend la hiérarchie partageable et corrigeable
   en un point. Sur le fil rouge, les deux modèles rendent exactement le même résultat.
2. **Une relation N-M se résout par une table de pont**, et cette table ne porte **aucun montant** :
   y recopier le montant du ticket produit **2,01** fois le chiffre d'affaires.
3. **Le facteur de répétition se mesure** : **2,01** ici, quand le ratio de lignes par ticket vaut
   **1,64** — parce que la pondération par le montant n'est pas celle du comptage.
4. **Les petits drapeaux se rangent** dans une dimension déchet construite sur les combinaisons
   observées : **30** occupées sur **30**, et toute absence devient une anomalie lisible.
5. **Un drapeau de périmètre est une règle, pas un détail** : **175 169 798** FCFA séparent le chiffre
   d'affaires net du chiffre d'affaires toutes lignes, et rien dans le modèle n'oblige une requête à
   choisir.

> **À retenir.** Une variante de modèle ne se choisit pas au goût : elle se **mesure**. Ce chapitre a
> mesuré les quatre variantes du socle — flocon, pont, déchet, faits multiples — et chacune a livré le
> même verdict : ce qui coûte cher n'est jamais la ligne supplémentaire, c'est la règle qu'on oublie
> d'écrire.

---

## 16. Évaluation formative

1. Donnez le critère qui distingue l'étoile du flocon, et le prix du flocon sur le fil rouge.
2. Le flocon change-t-il le résultat d'un rapport ? Justifiez par la mesure.
3. Qu'est-ce qu'une table de pont ? Citez le N-M du socle et ses deux nombres.
4. Quelle règle interdit absolument de mettre un montant dans une table de pont, et pourquoi ?
5. Le facteur de répétition vaut **2,01** alors que la moyenne de lignes par ticket vaut **1,64** :
   expliquez l'écart.
6. À quoi sert une dimension déchet, et combien de lignes compte celle du socle ?
7. Pourquoi les **30** combinaisons occupées sur **30** sont-elles une information utile ?
8. Quelles sont les deux modélisations possibles d'un retour, et que coûte chacune ?
9. Que valent le chiffre d'affaires net et le chiffre d'affaires toutes lignes, et quel est l'écart ?
10. « On dénormalise pour économiser des gestes, jamais de la vérité. » Illustrez cette phrase par
    deux décisions du socle, dont une qui change tous les chiffres.

**Corrigé :** 1. Le nombre de jointures pour atteindre un attribut : **1** en étoile, **3** en flocon ;
le flocon coûte **2** jointures, et fait passer la dimension de **154** à **173** lignes
au total. 2. Non : les deux lectures rendent un résultat **identique** (Matériaux **3 535 582 421**
FCFA). 3. Une table qui matérialise une relation plusieurs à plusieurs : sur le socle, tickets et
produits — **240 000** lignes pour **146 161** tickets. 4. Parce que le montant serait répété autant de
fois que l'objet a de liens : **31 298 080 184** au lieu de **15 595 154 955** FCFA. 5. Parce que le
facteur est pondéré par le montant : les tickets à plusieurs lignes pèsent plus lourd que les tickets
à une ligne. 6. À rassembler des drapeaux de faible cardinalité en une seule table : **30** lignes
pour le socle. 7. Parce que l'absence d'une combinaison devient alors un signal : si une combinaison
disparaît, c'est un changement de pratique ou une anomalie, pas un simple vide. 8. Un drapeau dans la
table de ventes (simple, mais chaque requête doit filtrer) ou une table de faits de retours (sûr, mais
toute lecture nette porte sur deux tables). 9. Net **15 595 154 955** FCFA, toutes lignes
**15 419 985 157** FCFA, écart **175 169 798** FCFA, soit les **2 809** lignes de retour. 10.
Dénormalisation qui ne change rien : la famille dans `dim_produit` (**1** jointure au lieu de **3**,
résultat identique). Dénormalisation qui change tout : le montant du ticket dans une table de pont
(**2,01** fois le chiffre d'affaires).
