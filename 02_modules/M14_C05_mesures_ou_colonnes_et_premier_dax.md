# Module M14.C05 — Mesures ou colonnes, et le premier DAX

**Outils : DuckDB 1.5.5 (exécuté) ; pandas (non requis). Power BI Desktop et son langage DAX sont
*cités* — l'outil n'est pas installé dans cet atelier (règle §1.5). Les coûts, les dénominateurs et les
contrôles de ce chapitre sont **mesurés** sur le socle à chaque exécution de `tools/mesures_M14.py`,
section `dax`.**

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **choisir entre une mesure et une colonne calculée** sur un cas chiffré : la marge ne stocke **rien**
   en mesure, **154** valeurs dans la dimension produit et **240 000** si elle devient une colonne du
   fait — un facteur **1 558,4** sur ce qui entre dans le modèle ;
2. **écrire les onze mesures du rapport** avec **huit** fonctions DAX, dont les **cinq** de survie —
   `SUM`, `COUNTROWS`, `DISTINCTCOUNT`, `DIVIDE`, `CALCULATE` ;
3. **savoir ce qu'un dénominateur change** : le même chiffre d'affaires donne **107 396** FCFA par
   ticket et **65 749** FCFA par ligne, soit **38,8 %** d'écart entre deux réponses défendables ;
4. **écrire `DIVIDE` partout où un dénominateur peut être nul** : **44** des **264** combinaisons
   magasin × mois du socle sont vides (**16,7 %**), et c'est là que le taux cesse d'être une division ;
5. **nommer, formater et documenter** une mesure, et **dire ce que M15 prendra en charge** — pour que
   la frontière du module soit écrite, et pas devinée.

---

## 2. Pourquoi cette notion est importante

Un rapport ne contient pas des tables : il contient des **chiffres**. Ce sont les mesures qui les
produisent, et une mesure est un objet particulier — elle n'existe nulle part dans le modèle, elle se
calcule au moment où on la regarde, sous les filtres de la page.

Trois conséquences, toutes mesurées sur le fil rouge.

**La première est le volume.** Une colonne calculée **se stocke** : la même marge coûte **240 000**
valeurs si elle vit dans le fait, **154** si elle vit dans la dimension produit, et **zéro** si elle est
une mesure. Sur un modèle qui grossit, ce n'est pas une question de goût : c'est un facteur **1 558,4**
sur la matière à charger, à compresser et à actualiser.

**La deuxième est la justesse.** Une mesure juste avec un dénominateur faux reste fausse. Le panier
moyen du rapport vaut **107 396** FCFA par ticket ; divisé par les lignes au lieu des tickets, il vaut
**65 749** FCFA — **38,8 %** de moins, sans qu'aucune erreur n'apparaisse. Le même mot, « panier
moyen », ne veut pas dire la même chose selon ce qu'on met en bas de la fraction.

**La troisième est la maintenance.** Onze mesures nommées et définies se relisent ; trente mesures
appelées `mesure1`, `mesure2` et `Total général 2` ne se relisent pas. Et un rapport dont personne ne
sait ce que veulent dire les chiffres finit par être refait — deux fois par an, par des gens différents.

---

## 3. Explication simple — la photographie et le thermomètre

Une **colonne calculée** est une **photographie**. Elle est prise au moment où le modèle s'actualise,
puis elle ne bouge plus : elle est stockée dans la table, avec ses valeurs figées. Une marge en colonne
calculée porte la valeur du coût **du dernier chargement**.

Une **mesure** est un **thermomètre**. Elle ne stocke rien : on la lit au moment où on regarde le
rapport, et elle suit les filtres de la page. Le même rapport, filtré sur un magasin, un mois ou une
famille de produits, affichera la marge **de ce magasin**, **de ce mois**, **de cette famille** — parce
que la mesure a été recalculée à la lecture.

Deuxième image utile, pour le dénominateur. Un taux est une **question posée à une division** :
« combien, sur combien ? ». Le « sur combien » décide de tout. Le panier moyen se demande **par
ticket** — sinon on compte trente fois le même client qui a rempli trente paniers. Le taux de retour se
demande **par ligne** — parce que la question logistique est « quelle part de mes lignes me revient ».
Le taux de rupture se demande **par couple produit-magasin-mois** — parce qu'un couple peut n'avoir
jamais été servi, et qu'il ne compte alors pas comme une rupture. Trois taux, trois dénominateurs
différents, et c'est la définition écrite qui les sépare.

Enfin, une mesure est une **phrase courte** : `DIVIDE(le haut, le bas)`. Si vous ne savez pas dire
« le haut » et « le bas » en une phrase, vous n'avez pas encore de mesure — vous avez une formule.

---

## 4. Vocabulaire essentiel

| Terme | Ce qu'il désigne sur le fil rouge |
|---|---|
| **Mesure** | un calcul évalué à la lecture, sous les filtres de la page : `[Panier moyen]` |
| **Colonne calculée** | un calcul évalué à l'actualisation et **stocké** dans la table : le coût d'achat produit |
| **Table calculée** | une table entière fabriquée par une expression : le socle n'en a pas besoin, la table de dates est importée |
| **DAX** | le langage d'expression du modèle — *Data Analysis Expressions* —, une syntaxe proche d'Excel et une sémantique de filtres |
| **Contexte de filtre** | l'ensemble des filtres appliqués à une mesure au moment où elle s'affiche : page, visuel, segment, exploration |
| **Agrégateur** | une fonction qui réduit plusieurs lignes à une valeur : `SUM`, `COUNTROWS`, `DISTINCTCOUNT`, `MIN`, `MAX` |
| **Itérateur** | une fonction qui parcourt les lignes une par une puis agrège : `SUMX`, employé **une** fois dans le module |
| **`DIVIDE`** | la division du modèle : elle rend un **vide** quand le dénominateur est nul, au lieu d'une erreur |
| **`DISTINCTCOUNT`** | le compteur de valeurs distinctes : **145 212** tickets sur **237 191** lignes de vente |
| **`CALCULATE`** | la fonction qui modifie le contexte de filtre d'une expression — **un** usage dans tout le module |
| **`RELATED`** | la fonction qui va chercher un attribut dans la dimension, du côté « un » de la relation |
| **`ISBLANK`** | le test du vide : les **1 272** factures ouvertes ont une date d'encaissement vide |
| **Format** | la façon dont un nombre s'affiche : **7** mesures de montant, **4** mesures de pourcentage |
| **Table de mesures** | la table qui ne contient aucune donnée et range les mesures, pour qu'elles se trouvent |
| **Chiffre de contrôle** | la valeur qu'une mesure doit rendre quand on la regarde sans filtre : **15 595 154 955** FCFA pour `[CA net]` |

> **Définition.** Une **mesure** est une expression évaluée **au moment où un visuel s'affiche**, sous
> les filtres en vigueur. Elle ne consomme pas de place dans le modèle : elle consomme du temps de
> calcul, à chaque affichage.

> **Définition.** Une **colonne calculée** est une expression évaluée **pendant l'actualisation**, dont
> le résultat est **stocké** dans la table. Elle se comporte ensuite comme n'importe quelle colonne :
> elle se filtre, se groupe, et ne suit pas les filtres du rapport.

> **Définition.** Le **contexte de filtre** est l'état des filtres au moment du calcul : ceux de la page,
> du visuel, des segments, et ceux qu'une fonction comme `CALCULATE` ajoute ou retire. Deux mesures
> écrites avec les mêmes fonctions peuvent rendre deux nombres différents dans deux visuels : c'est
> presque toujours le contexte qui a changé.

> **Définition.** Le **dénominateur** d'un taux est la population sur laquelle la question est posée.
> Un taux n'est juste que si son dénominateur est **écrit** dans la définition de la mesure — sans quoi
> deux personnes calculeront deux chiffres, et toutes deux auront raison.

---

## 5. Cours approfondi

### 5.1 Mesure ou colonne calculée : la photographie a un prix

Reprenons le seul calcul que le modèle doit ajouter : la marge. Elle existe en trois versions, et elles
ne coûtent pas la même chose.

| Version | Ce qui est stocké | Ce que ça suit |
|---|---|---|
| **Colonne calculée dans le fait** | **240 000** valeurs, une par ligne de vente | rien : la valeur est recalculée à l'actualisation |
| **Colonne calculée dans la dimension** | **154** valeurs, une par produit | le coût du produit, qui vit dans la dimension |
| **Mesure** | **0** valeur | les filtres de la page, à chaque affichage |

Le facteur entre l'hypothèse haute et l'hypothèse basse est **1 558,4** — sur la seule matière du
modèle. Et ce n'est pas qu'une question de poids : une colonne calculée **fige** une valeur qui dépend
souvent d'une autre table. Une marge en colonne du fait reconstruite à l'actualisation devient fausse
le jour où le coût change, sans que personne ne recharge.

La règle tient en trois lignes.

1. **Colonne calculée** si la valeur doit servir à **filtrer**, à **trier**, ou à **découper** un visuel.
   C'est le cas du coût d'achat du produit : le rapport filtre les produits par coût, donc le coût doit
   exister dans la dimension.
2. **Mesure** dès qu'il s'agit d'un **calcul de rapport** : un total, un taux, un panier, un encours.
3. **Jamais de colonne calculée dans un fait** pour un calcul qui se fait à la lecture : c'est le seul
   cas où les deux règles précédentes sont violées en même temps.

> **Attention.** Une colonne calculée n'est pas fausse parce qu'elle est calculée : elle est **figée**.
> Un rapport dont une colonne porte une marge périmée est plus dangereux qu'un rapport qui n'affiche pas
> de marge, parce qu'il a l'air de savoir.

### 5.2 Les onze mesures du rapport

Les **onze** mesures tiennent dans une table qui ne porte aucune donnée, et chacune a un nom
d'indicateur, une définition écrite et un format. Leur code complet est dans le dossier du module
(`03_exercices/dossier_M14/modele_powerbi.md`, § 4) ; voici leur inventaire.

| # | Mesure | Ce qu'elle rend | Fonction(s) | Format |
|---|---|---|---|---|
| 1 | `[CA net]` | le chiffre d'affaires hors retours | `CALCULATE`, `SUM` | montant |
| 2 | `[CA HT]` | le chiffre d'affaires hors taxes | `CALCULATE`, `SUM` | montant |
| 3 | `[Coût HT]` | la quantité vendue × le coût standard du produit | `SUMX`, `RELATED` | montant |
| 4 | `[Marge brute]` | le chiffre d'affaires HT moins le coût HT | soustraction de mesures | montant |
| 5 | `[Taux de marge %]` | la marge rapportée au chiffre d'affaires | `DIVIDE` | pourcentage |
| 6 | `[Panier moyen]` | le chiffre d'affaires net par ticket | `DIVIDE`, `DISTINCTCOUNT` | montant |
| 7 | `[Taux de rupture %]` | la part des couples servis en rupture | `DIVIDE`, `COUNTROWS` | pourcentage |
| 8 | `[Taux de retour lignes %]` | la part des lignes de retour | `DIVIDE`, `CALCULATE` | pourcentage |
| 9 | `[Taux de service %]` | la part des commandes livrées à la date promise | `DIVIDE`, `CALCULATE` | pourcentage |
| 10 | `[Encours client]` | les factures non encaissées | `SUM`, `ISBLANK` | montant |
| 11 | `[Coût logistique par colis]` | le coût moyen d'un colis | `DIVIDE` | montant |

**Une dépendance s'y cache** : `[Taux de marge %]` divise `[Marge brute]`, qui soustrait `[Coût HT]` de
`[CA HT]`. Trois mesures s'enchaînent, et chaque étage est lisible. C'est ce qu'on appelle une chaîne de
mesures : elle se relit de bas en haut, comme une démonstration.

### 5.3 Les cinq fonctions de survie, et les trois auxiliaires

Les onze mesures n'emploient que **huit** fonctions DAX. Cinq suffisent à tout rapport de gestion.

| Fonction | Ce qu'elle fait | Sur le fil rouge |
|---|---|---|
| **`SUM`** | additionne une colonne | **15 595 154 955** FCFA de chiffre d'affaires net |
| **`COUNTROWS`** | compte les lignes d'une table | **2 428** couples en rupture |
| **`DISTINCTCOUNT`** | compte les valeurs distinctes | **145 212** tickets, pour **237 191** lignes |
| **`DIVIDE`** | divise sans jamais échouer | **44** dénominateurs nuls sur **264** combinaisons |
| **`CALCULATE`** | change le contexte de filtre | **un** usage : les retours exclus |

Trois fonctions auxiliaires complètent la boîte, et aucune ne s'ajoute à la liste : `SUMX` parcourt les
lignes avant d'additionner (**un** usage, pour le coût), `RELATED` va chercher un attribut dans la
dimension (**un** usage, le coût du produit), `ISBLANK` teste le vide (**un** usage, la date
d'encaissement).

> **Conseil professionnel.** Apprenez ces cinq fonctions avant d'apprendre les autres. Un rapport de
> gestion complet se construit avec elles — et les fonctions temporelles, qui viendront en M15, ne
> remplacent aucune d'elles.

### 5.4 Le dénominateur : le seul mot qui change le chiffre

Le panier moyen divise le chiffre d'affaires net par le nombre de **tickets**. Écrit avec les **lignes**,
il donne une autre réponse — et les deux réponses sont vraies, parce qu'elles répondent à deux
questions différentes.

```sql
-- le même chiffre d'affaires, deux dénominateurs
SELECT SUM(montant_ttc) / COUNT(DISTINCT id_ticket) AS par_ticket,   -- 107 396 FCFA
       SUM(montant_ttc) / COUNT(*)                   AS par_ligne     --  65 749 FCFA
FROM fait_ventes WHERE est_retour = 0;
```

**145 212** tickets, **237 191** lignes : un écart de **38,8 %** entre les deux paniers. Un ticket
contient en moyenne 1,6 ligne, et c'est tout l'écart. Le rapport affiche `[Panier moyen]` par ticket,
parce que la question du comité était « combien un client dépense-t-il en une visite » — et la réponse
est écrite dans la définition de la mesure, pas devinée par le lecteur.

> **À retenir.** Ecrire un taux, c'est écrire **deux** choses : le haut et le bas. Une mesure dont le
> dénominateur n'est pas nommé dans sa définition est une mesure qui sera recalculée autrement par la
> personne suivante — et personne ne saura laquelle des deux versions était la bonne.

### 5.5 `DIVIDE` : le zéro qui n'arrête rien

Le socle porte un magasin qui ne vend rien : le dépôt central. Sur l'axe magasin × mois, cela fait
**44** combinaisons vides sur **264**, soit **16,7 %** des cases — et chacune de ces cases est un
dénominateur nul pour un taux par magasin.

```sql
-- les combinaisons magasin x mois sans aucune vente
SELECT COUNT(*) FROM (SELECT DISTINCT id_magasin FROM dim_magasin) m
CROSS JOIN (SELECT DISTINCT annee_mois FROM dim_date) d
WHERE NOT EXISTS (SELECT 1 FROM fait_ventes v
                  WHERE v.id_magasin = m.id_magasin
                  AND strftime(v.date_vente, '%Y-%m') = d.annee_mois);
--  44   ->  16,7 % des 264 cases : autant de divisions par zéro
```

Écrite avec `/`, la mesure **s'arrête** sur la première de ces cases : le visuel affiche une erreur, et
l'erreur se propage à la page. Écrite avec `DIVIDE`, elle rend un **vide** — que le visuel affiche comme
une absence. Une absence se comprend ; une erreur se contourne.

> **Attention.** `DIVIDE` ne rend pas un taux juste : elle rend un taux **calculable**. Un magasin sans
> vente n'a pas un taux de marge de zéro pour cent, il n'a **pas de taux du tout**. Confondre le vide et
> le zéro est la deuxième erreur de ce chapitre, après le mauvais dénominateur.

### 5.6 `CALCULATE`, une fois, et expliqué

`CALCULATE` modifie le contexte de filtre. C'est la fonction la plus puissante du DAX, et le module ne
l'emploie **qu'une** fois : pour exclure les retours.

```sql
-- ce que fait le seul CALCULATE du module : retirer les lignes de retour
SELECT SUM(montant_ttc) AS toutes_lignes,                       -- 15 419 985 157 FCFA
       SUM(CASE WHEN est_retour = 0 THEN montant_ttc END) AS net -- 15 595 154 955 FCFA
FROM fait_ventes;
```

L'écart, **175 169 798** FCFA, vaut **1,12 %** du net : c'est la valeur des retours. Les retours sont des
lignes **négatives** — elles ne s'ajoutent pas, elles se déduisent — et c'est pour cela que le chiffre
d'affaires « sans les retours » est **plus élevé** que le chiffre d'affaires de toutes les lignes. Un
rapport qui n'exclut pas les retours n'est pas faux : il affiche un autre indicateur, qui doit alors
s'appeler autrement.

> **Dans les faits.** Les deux définitions du chiffre d'affaires cohabitent dans le rapport du fil
> rouge : **15 595 154 955** FCFA (net de retours) et **15 419 985 157** FCFA (toutes lignes), avec
> **175 169 798** FCFA d'écart. Le rapport « avant » du dossier du module affichait les deux côte à
> côte sans dire laquelle était laquelle — c'est précisément le défaut que la définition écrite corrige.

### 5.7 Nommer, formater, documenter

Onze mesures, **sept** formats de montant et **quatre** formats de pourcentage. Trois règles, et elles
tiennent en trois mots : **un nom d'indicateur**, **une unité visible**, **une définition écrite**.

- **Le nom dit la question**, pas la formule : `[Taux de retour lignes %]`, jamais `[somme_retours_div]`.
  Et quand deux définitions cohabitent — retour par ligne, retour par ticket — le nom porte la
  différence : **1,17 %** des lignes, **1,91 %** des tickets.
- **L'unité est visible** : soit dans le nom (`%`, « par colis »), soit dans le format d'affichage. Un
  montant sans unité est un nombre ; **3 284** FCFA et 3 284 colis ne se ressemblent pas longtemps.
- **La définition est écrite** : une phrase par mesure, dans la table de mesures ou dans le dossier du
  rapport. C'est cette phrase qui permettra à quelqu'un d'autre de vérifier le chiffre **107 396** FCFA
  sans vous appeler.

### 5.8 Ce que M15 prendra en charge

La frontière du module est écrite dans le plan, et elle s'arrête **au seuil du DAX**. M14 écrit les
mesures de survie ; M15 ouvre la bibliothèque complète.

| Ce que M15 apportera | Ce que M14 laisse volontairement de côté |
|---|---|
| Les fonctions temporelles : cumuls, année précédente, moyenne mobile | toute comparaison de périodes dans ce module |
| `ALL` et les filtres qui retirent un filtre | le pourcentage d'un total — affiché par un **graphique**, ici |
| Les itérateurs avancés et les tables virtuelles | au-delà du seul `SUMX` du coût |
| Les groupes de calcul et la réutilisation de mesures | la chaîne de mesures reste locale et courte |
| Le débogage fin du contexte de filtre | une seule leçon de contexte, pas un cours |

> **Dans les faits.** La part du premier magasin du réseau — Sahel Distribution, Ouaga 2000 — vaut
> **34,1 %** du chiffre d'affaires : c'est un pourcentage du total, qui demande `ALL`. Le rapport
> l'affiche par un **graphique**, pas par une mesure. Un module qui enseigne `ALL` trop tôt fabrique des
> mesures que personne ne sait relire.

---

## 6. Exemple concret — la fiche de `[Panier moyen]`

Une mesure se documente comme une fiche d'identité. Voici la fiche complète, et c'est le modèle des
onze.

| Rubrique | Contenu |
|---|---|
| **Nom** | `[Panier moyen]` |
| **Question posée** | « combien un client dépense-t-il en une visite » |
| **Haut** | le chiffre d'affaires net de retours : **15 595 154 955** FCFA |
| **Bas** | le nombre de **tickets** distincts : **145 212** |
| **Définition écrite** | chiffre d'affaires net divisé par le nombre de tickets distincts, retours exclus |
| **Format** | montant, sans décimale, en FCFA |
| **Chiffre de contrôle** | **107 396** FCFA, à comparer au panier par ligne (**65 749** FCFA) |
| **Ce qu'elle ne fait pas** | elle ne suit pas les périodes : la comparaison annuelle est en M15 |

**Trois contrôles avant de la déclarer finie.** Le calcul sans filtre rend **107 396** FCFA. Le même
calcul en changeant le dénominateur rend **65 749** FCFA, et l'écart de **38,8 %** est expliqué par le
nombre de lignes par ticket. Et la mesure se comporte correctement sur une case vide — le dépôt central
n'affiche pas d'erreur, il n'affiche rien.

---

## 7. Démonstration pas à pas — les mesures, dans l'outil

> **Boîte à outils.** Ce chapitre se rejoue dans **un** endroit de l'outil — la table de mesures — et il
> se **prouve** ailleurs : dans l'atelier, chaque affirmation est vérifiée en SQL sur le socle, parce
> que l'outil n'y est pas installé (règle §1.5). Les gestes sont décrits ; les contrôles sont exécutés.

**Avertissement d'exécution.** Rien de ce qui suit n'a été cliqué : Power BI Desktop n'est pas installé
dans cet atelier. Chaque geste est décrit par son libellé et son emplacement, et chaque chiffre du
chapitre est mesuré par `tools/mesures_M14.py` (section `dax`) sur les mêmes tables.

**Les dix gestes, dans l'ordre.**

1. **Créer la table de mesures** : une table sans données, qui ne sert qu'à ranger — et à retrouver.
2. **Écrire `[CA net]`** : `CALCULATE(SUM(fait_ventes[montant_ttc]), fait_ventes[est_retour] = 0)`, et
   vérifier **15 595 154 955** FCFA.
3. **Écrire `[CA HT]`**, puis `[Coût HT]` avec le seul `SUMX` et le seul `RELATED` du module.
4. **Écrire `[Marge brute]`** comme une soustraction **de mesures**, jamais d'une colonne : la chaîne
   restera lisible.
5. **Écrire `[Taux de marge %]`, `[Panier moyen]`, `[Taux de rupture %]`, `[Taux de retour lignes %]`,
   `[Taux de service %]`, `[Encours client]`, `[Coût logistique par colis]`** — toutes avec `DIVIDE`.
6. **Nommer chaque mesure par son indicateur**, et écrire sa définition dans la table de mesures.
7. **Régler les formats** : **sept** montants, **quatre** pourcentages, aucune unité laissée implicite.
8. **Contrôler les dénominateurs** un par un : tickets pour le panier, couples servis pour la rupture,
   lignes pour le retour, colis pour la logistique.
9. **Tester le vide** : afficher le taux de marge du dépôt central — la mesure doit rendre un vide, pas
   une erreur.
10. **Rejouer la recette** : les **10** valeurs du rapport, **8** comparaisons avec M12, **0** écart.

**Les contrôles exécutés, et ce qu'ils rendent.**

| Contrôle | Requête | Résultat |
|---|---|---|
| Le dénominateur du panier | `COUNT(DISTINCT id_ticket)` contre `COUNT(*)`, retours exclus | **145 212** tickets contre **237 191** lignes : **107 396** FCFA contre **65 749** FCFA |
| Le seul `CALCULATE` | total de toutes les lignes contre total hors retours | **15 419 985 157** contre **15 595 154 955** : écart **175 169 798** FCFA (**1,12 %**) |
| Le zéro du dépôt | combinaisons magasin × mois sans vente | **44** sur **264** (**16,7 %**) : autant de divisions à protéger |
| Le coût du stockage | valeurs stockées selon la version de la marge | **240 000** dans le fait, **154** dans la dimension, **0** en mesure |
| La recette des mesures | les **10** valeurs du rapport rejouées | **8** comparaisons avec M12, **0** écart |

---

## 8. Erreurs fréquentes

1. **Diviser par les lignes quand la question parle de tickets.** Le panier passe de **107 396** à
   **65 749** FCFA, et le rapport ne signale rien.
2. **Écrire `/` au lieu de `DIVIDE`.** La première case vide arrête le visuel : **44** cases sur **264**
   attendent ce moment.
3. **Confondre le vide et le zéro.** Un magasin sans vente n'a pas un taux nul : il n'a pas de taux.
4. **Créer une colonne calculée pour un calcul de rapport.** **240 000** valeurs stockées au lieu de
   **0**, et une valeur figée à l'actualisation.
5. **Nommer une mesure par sa formule.** `mesure1`, `Total général 2` : personne ne saura ce qu'elle
   veut dire, y compris vous dans six mois.
6. **Oublier le format.** Un taux affiché en décimal — 0,07 au lieu de 7,29 % — fait douter du
   chiffre, alors que le format seul était en cause.
7. **Laisser deux définitions cohabiter sous le même nom.** Retour par ligne (**1,17 %**) et retour par
   ticket (**1,91 %**) ne sont pas la même chose : le nom doit le dire.
8. **Multiplier les mesures au lieu de réutiliser.** Une chaîne de mesures se relit ; trente mesures
   plates qui recopient la même somme se contredisent à la première correction.

---

## 9. Bonnes pratiques professionnelles

1. **Ranger les mesures dans une table de mesures**, jamais éparpillées dans les tables de données.
2. **Nommer par indicateur**, avec l'unité quand elle n'est pas dans le format.
3. **Écrire la définition** de chaque mesure en une phrase, et la garder à côté du code.
4. **`DIVIDE` partout**, et jamais `/` dans une mesure.
5. **Vérifier le dénominateur** en écrivant la mesure : « sur combien ? » doit avoir une réponse écrite.
6. **Préférer la mesure à la colonne calculée** dès qu'il s'agit d'un calcul de rapport.
7. **Donner un chiffre de contrôle** à chaque mesure : la valeur qu'elle doit rendre sans filtre.

> **À retenir.** Une mesure est un **contrat** : un nom, une question, un dénominateur, un format, un
> chiffre de contrôle. Le rapport tiendra tant que ce contrat est écrit — et il se dégradera au premier
> calcul fait à la va-vite sous un nom qui ne dit rien.

---

## 10. Exercice guidé

**Énoncé.** Le rapport affiche un panier moyen de **65 749** FCFA, alors que le comité attend
**107 396** FCFA. Trouvez la cause, corrigez la mesure, et prouvez que le rapport est revenu juste.

**Étape 1 — constater.** Les deux montants existent dans le socle : le premier est le chiffre d'affaires
net divisé par les lignes (**237 191**), le second par les tickets (**145 212**). Le rapport n'a donc pas
un chiffre faux : il a le **mauvais dénominateur**.

**Étape 2 — nommer la question.** Le comité a demandé « combien un client dépense-t-il en une visite » :
la visite est le **ticket**. Le dénominateur est donc `DISTINCTCOUNT(fait_ventes[id_ticket])`.

**Étape 3 — corriger.** Écrivez `DIVIDE([CA net], DISTINCTCOUNT(fait_ventes[id_ticket]))` et vérifiez le
chiffre : **107 396** FCFA sans filtre.

**Étape 4 — contrôler l'écart.** L'écart de **38,8 %** entre les deux versions doit être **expliqué**
dans le dossier : un ticket contient en moyenne **1,6** ligne. Un chiffre qui change sans explication
est une régression, même s'il change dans le bon sens.

**Attendu.** Le dénominateur identifié, la question du comité reformulée, la mesure corrigée, et
l'écart documenté — pas seulement la correction.

---

## 11. Exercices autonomes

**Exercice 5.1.** Classez les trois calculs suivants en « mesure » ou « colonne calculée », et justifiez
en une phrase : le coût d'achat du produit, la marge brute, le rang du client dans son magasin.

**Exercice 5.2.** Le taux de retour du rapport affiche **1,17 %** des lignes et **1,91 %** des tickets.
Écrivez les deux dénominateurs, et dites dans quel cas chacun est la bonne réponse.

**Exercice 5.3.** Un taux de marge par magasin affiche une erreur sur une seule ligne du tableau.
Écrivez la cause probable, la requête qui la confirme, et la correction.

**Exercice 5.4.** Vous devez afficher « les 10 premiers clients par chiffre d'affaires ». Pourquoi cette
demande ne se traite-t-elle pas dans ce module, et à quoi faut-il la renvoyer ?

**Exercice 5.5.** Reprenez `[Encours client]` et écrivez sa fiche complète : nom, question, haut, bas,
format, chiffre de contrôle.

---

## 12. Correction détaillée

**Exercice 5.1.** Le **coût d'achat du produit** est une **colonne calculée** — ou plutôt une colonne
apportée par une fusion : il vit dans la dimension, le rapport filtre les produits par coût, et
**154** valeurs suffisent. La **marge brute** est une **mesure** : elle se calcule à la lecture, sous
les filtres, et ne stocke rien. Le **rang du client dans son magasin** est une **colonne calculée** :
un rang se filtre et se trie, donc il doit exister comme valeur ; il se calcule à l'actualisation, ce
qui le fige pour un mois donné — et cette limite doit être écrite.

**Exercice 5.2.** Par ligne : **237 191** lignes de vente hors retours ; par ticket : **145 212**
tickets. Le taux par ligne répond à la question logistique — « quelle part de ce que j'expédie me
revient » — et c'est celui du rapport. Le taux par ticket répond à une question commerciale — « quelle
part de mes visites donne lieu à un retour » — et il est plus élevé parce qu'un ticket peut contenir
plusieurs lignes. Les deux sont justes ; **1,17 %** et **1,91 %** ne se comparent pas.

**Exercice 5.3.** La cause probable : une division par zéro sur la combinaison vide — le **dépôt**
central, qui porte **44** mois de coûts logistiques et aucune vente. La requête qui confirme :
`SELECT COUNT(*) FROM (SELECT DISTINCT id_magasin FROM dim_magasin) m CROSS JOIN (SELECT DISTINCT
annee_mois FROM dim_date) d WHERE NOT EXISTS (SELECT 1 FROM fait_ventes v WHERE v.id_magasin =
m.id_magasin AND strftime(v.date_vente, '%Y-%m') = d.annee_mois);` rend **44**. La correction :
réécrire la mesure avec `DIVIDE`, et vérifier que la ligne concernée affiche un vide — pas un zéro.

**Exercice 5.4.** Parce qu'un classement demande de **retirer** le filtre des autres clients, donc
`ALL` ou une fonction de fenêtre : c'est le domaine de M15. La demande se renvoie à M15 avec sa
définition écrite — « par chiffre d'affaires net, retours exclus, sur la période sélectionnée » — et elle
ne se bricole pas dans M14.

**Exercice 5.5.** Nom : `[Encours client]`. Question : « combien de factures ne m'ont pas encore été
payées ». Haut : la somme des montants TTC des factures ouvertes — **1 202 550 590** FCFA. Bas : aucun,
c'est un total, pas un taux. Format : montant en FCFA. Chiffre de contrôle : **1 202 550 590** FCFA pour
**1 272** factures ouvertes. Et la définition doit dire que « ouvert » veut dire **date d'encaissement
vide** — sans quoi la moitié des lecteurs cherchera une notion de retard.

---

## 13. Mini-projet de chapitre — la fiche des onze mesures

**Énoncé.** Produisez la **fiche des onze mesures** du rapport : pour chacune, son nom d'indicateur, la
question qu'elle pose, son haut, son bas, son format, son chiffre de contrôle, et la fonction DAX
employée.

**Barème indicatif** : les **onze** mesures listées avec leur nom, leur question et leur format
(**6** points) · les **cinq** fonctions de survie identifiées et reliées à au moins une mesure chacune
(**6** points) · les dénominateurs des quatre taux écrits explicitement (**4** points) · les deux
chiffres de contrôle du panier — par ticket et par ligne — avec l'écart expliqué (**2** points) · sur
**18** points.

> **Pourquoi ce mini-projet.** Parce que la fiche est ce qui reste du rapport quand le rapport change.
> Le jour où une mesure rend un autre nombre, la fiche dit laquelle des deux est la bonne — et c'est la
> quatrième pièce qui entrera dans le dossier de conception du projet.

---

## 14. Résumé du chapitre

| Notion | Mesure du module | Ce qu'elle enseigne |
|---|---|---|
| Mesure ou colonne | **0**, **154** ou **240 000** valeurs stockées | une colonne calculée se paie au stockage et se fige |
| Les mesures du rapport | **11** mesures, **8** fonctions | cinq fonctions de survie suffisent à un rapport de gestion |
| Le dénominateur | **107 396** FCFA par ticket, **65 749** par ligne (**38,8 %**) | un taux sans dénominateur écrit est un taux à refaire |
| `DIVIDE` | **44** cases vides sur **264** (**16,7 %**) | un vide se comprend, une erreur se contourne |
| Le seul `CALCULATE` | **175 169 798** FCFA (**1,12 %**) | exclure les retours change le chiffre, pas la vérité |
| Noms et formats | **7** montants, **4** pourcentages | l'unité est une information, pas une décoration |
| Frontière du module | M15 : temps, `ALL`, itérateurs avancés | ce qu'on n'écrit pas ici doit être écrit quelque part |

**Instrument.** `python3 tools/mesures_M14.py` recalcule le nombre de mesures, les fonctions employées,
les deux dénominateurs du panier, l'effet du seul `CALCULATE`, les combinaisons vides et le coût de
stockage des trois versions de la marge. Les gestes, eux, se rejouent devant votre écran.

**Le module en une ligne.** Les quatre chapitres précédents ont posé l'outil, la donnée, sa
transformation et le modèle ; celui-ci a écrit ce que le rapport **affiche** — et il a montré qu'une
mesure n'est pas une formule mais un contrat : un nom, une question, un dénominateur, un format, un
chiffre de contrôle.

---

## 15. À retenir

1. **Mesure ou colonne calculée ne se décide pas au goût** : une colonne calculée si la valeur se filtre
   ou se trie, une mesure si le calcul se fait à la lecture — jamais de colonne calculée dans un fait
   pour un calcul de rapport.
2. **Le dénominateur est la moitié du taux.** **107 396** FCFA par ticket, **65 749** par ligne : les
   deux sont justes, une seule répond à la question posée.
3. **`DIVIDE`, jamais `/`.** Avec **44** combinaisons vides sur **264** dans le seul socle du fil rouge,
   la division par zéro n'est pas un cas d'école : c'est une case sur six.

> **À retenir.** Ecrire une mesure, c'est écrire **deux** phrases : le calcul, et la question à laquelle
> il répond. La première se vérifie en trois minutes ; la seconde décide de ce que le comité achètera —
> et c'est celle qu'on oublie d'écrire.

---

## 16. Évaluation formative

1. Donnez les trois versions de la marge et le nombre de valeurs que chacune stocke.
2. Quand une colonne calculée est-elle le bon choix ?
3. Citez les cinq fonctions de survie et une mesure du rapport qui emploie chacune.
4. Pourquoi `DISTINCTCOUNT` change-t-il le panier moyen ?
5. Que rend `DIVIDE` quand le dénominateur est nul, et que rend `/` ?
6. Pourquoi le chiffre d'affaires hors retours est-il plus élevé que celui de toutes les lignes ?
7. Combien de fois `CALCULATE` est-il employé dans le module, et pourquoi ?
8. Pourquoi faut-il écrire la définition d'une mesure, et où l'écrit-on ?
9. Qu'est-ce que la part du premier magasin (**34,1 %**) demande, et pourquoi n'est-elle pas une mesure
   dans ce module ?
10. Quels sont les trois contrôles qui déclarent une mesure finie ?

**Corrigé.** 1. Colonne calculée dans le fait : **240 000** valeurs ; dans la dimension produit :
**154** ; en mesure : **0**. 2. Quand la valeur doit se **filtrer**, se **trier** ou découper un visuel
— et qu'elle vit dans une dimension. 3. `SUM` (le chiffre d'affaires), `COUNTROWS` (les couples en
rupture), `DISTINCTCOUNT` (les tickets du panier), `DIVIDE` (les quatre taux et le coût par colis),
`CALCULATE` (l'exclusion des retours). 4. Parce que le dénominateur passe des lignes (**237 191**) aux
tickets (**145 212**) : le panier passe de **65 749** à **107 396** FCFA, soit **38,8 %** d'écart.
5. `DIVIDE` rend un **vide** ; `/` provoque une **erreur** qui remonte au visuel. 6. Parce que les
retours sont des lignes **négatives** : elles se déduisent, et les exclure remonte le total de
**175 169 798** FCFA (**1,12 %**). 7. **Une** fois, pour exclure les retours ; le reste du langage,
notamment les fonctions temporelles, appartient à M15. 8. Parce qu'une mesure dont la question n'est pas
écrite sera recalculée autrement par quelqu'un d'autre ; on l'écrit dans la table de mesures et dans le
dossier du rapport. 9. Un pourcentage du total, donc la fonction `ALL` : c'est du ressort de M15, et le
rapport l'affiche par un graphique. 10. Le calcul sans filtre rend le chiffre de contrôle, le
dénominateur est justifié, et le comportement sur une case vide est vérifié — sans erreur.
