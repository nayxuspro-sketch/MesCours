# Module M12.C04 — Concevoir un KPI : les 6 critères et la carte de définition

**Outils : DuckDB 1.5.5 (exécuté), pandas (contrôle croisé, exécuté), Excel (exécuté). Power BI
(cité, non exécuté — règle §1.5). Durée indicative : 5 h. Niveau : N3. Prérequis : M12.C01—C03.**

> **L'idée du chapitre.** Un indicateur n'existe pas parce qu'il s'affiche : il existe parce qu'il est
> **défini**, **sourcé**, **attribué**, **comparable**, **pilotable** et **contre-balancé**. Ces six
> critères tiennent sur une **carte de définition** de **7** champs. Ce chapitre construit la carte pièce
> par pièce, et la met à l'épreuve sur les chiffres du socle : le même « taux de retour » vaut **1,12 %**
> ou **1,91 %** selon la définition, et une des six formules possibles donne un nombre **négatif** — voilà
> pourquoi la moitié du travail d'un indicateur se fait **avant** la première requête.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **énumérer et appliquer les six critères** qui font d'une métrique un indicateur clé — sourcé,
   défini, attribué, comparable, pilotable, contre-balancé ;
2. **remplir une carte de définition** : formule, source, granularité, fréquence, responsable, seuil
   d'alerte, contre-KPI — les **7** champs, **70** cases pour les **10** indicateurs du projet ;
3. **écrire une formule sans ambiguïté**, en choisissant explicitement numérateur, dénominateur, base
   de calcul et exclusions — et en sachant ce qu'un autre choix aurait produit ;
4. **poser un seuil d'alerte qui discrimine**, en mesurant ce qu'il déclenche : à **1** mois de
   couverture, **1 650** lignes de stock sont en alerte ; à **0,8** mois, il n'en reste que **176** ;
5. **choisir un contre-KPI** pour chaque indicateur, et **mesurer** ce que le couple protège ;
6. **reconnaître les effets pervers** d'un indicateur : ce qu'un chiffre pousse à faire quand il devient
   l'objectif — et la mesure qui les rend visibles.

---

## 2. Pourquoi cette notion est importante

Le dossier du projet raté est un catalogue de ces six critères manquants, dans l'ordre :

| Ce qui manquait | Ce que cela a produit, dans le dossier |
|---|---|
| **sourcé** | la marge était calculée sur le **coût standard** du référentiel, la comptabilité sur le **dernier prix payé** — deux coûts pour un produit |
| **défini** | « le CA affiché n'est pas celui de la compta : il manque les retours » — **2 809** lignes, et personne n'a tranché |
| **attribué** | **41** indicateurs, **aucun** responsable : deux services ont gardé chacun leur chiffre |
| **comparable** | le panier moyen divisé par le nombre de tickets chez l'un, par le nombre de lignes chez l'autre |
| **pilotable** | un seuil de rupture affiché… et **aucune** action associée : la question « que fait-on si c'est rouge ? » est restée sans réponse |
| **contre-balancé** | rien n'empêchait de « réussir » un indicateur aux dépens d'un autre, sans que personne ne le voie |

Le résultat est chiffré : **7 940 000** FCFA dépensés, dont **1 200 000** de maintenance, **11** semaines
de vie, **14** destinataires, **4** ouvertures le premier jour — et l'abandon. Le mandat de reprise
aujourd'hui tient en une phrase : « pas plus de **10** indicateurs, chacun avec sa définition écrite,
son responsable, sa fréquence, son seuil et son contre-indicateur ».

> **À retenir.** Dans un dispositif qui échoue, le problème n'est presque jamais le calcul : il est dans
> les **six critères** que personne n'a posés. Une requête juste sur un indicateur non défini produit un
> chiffre juste que personne ne peut utiliser.

---

## 3. Explication simple — le passeport du chiffre

Un indicateur sans carte de définition, c'est un médicament sans notice : la substance est peut-être
bonne, mais personne ne sait à quelle dose, pour qui, ni ce qu'il faut faire si l'état empire.

La carte est son **passeport** : elle ne décrit pas le chiffre, elle décrit **les conditions dans
lesquelles ce chiffre a le droit d'être publié**. Sept champs, et chacun répond à une question qui a
déjà provoqué une dispute :

- **Formule** — comment le calcule-t-on, exactement ?
- **Source** — d'où viennent les données ?
- **Granularité** — à quel niveau est-il calculé ?
- **Fréquence** — à quel rythme est-il publié ?
- **Responsable** — qui répond de sa justesse ?
- **Seuil d'alerte** — à partir de quand est-ce un problème ?
- **Contre-KPI** — quel indicateur l'empêche de mentir ?

Un passeport ne se remplit pas une fois pour toutes : il se **signe**. Le responsable, nommé, engage sa
lecture ; le seuil, chiffré, engage une action ; le contre-KPI, choisi, engage un arbitrage.

---

## 4. Vocabulaire essentiel

> **Définition.** Un **indicateur clé** — **KPI**, *Key Performance Indicators* — est une métrique
> **choisie** pour suivre une performance qui compte, dotée d'une carte de définition complète et d'un
> responsable nommé. Une entreprise a des dizaines de métriques, une poignée d'indicateurs et **trois
> ou quatre** indicateurs clés.

> **Définition.** Une **carte de définition** est la fiche d'identité d'un indicateur : formule, source,
> granularité, fréquence, responsable, seuil d'alerte, contre-KPI. Elle se publie **avec** l'indicateur,
> pas dans un classeur à part.

> **Définition.** Un **seuil d'alerte** est la valeur à partir de laquelle l'indicateur déclenche une
> **action** écrite. Un seuil sans action associée est une décoration ; une action sans seuil ne se
> déclenche jamais.

> **Définition.** Un **contre-KPI** — *indicateur de contrepartie* — est l'indicateur qui mesure ce
> qu'on **dégrade** en améliorant le premier. Il se publie à côté de lui, dans le même écran, avec le
> même responsable.

> **Définition.** Un **effet pervers** est une conséquence non voulue d'un indicateur devenu objectif :
> les personnes pilotées par la mesure agissent sur ce qu'elle mesure — pas sur ce qu'elle devait
> mesurer. Le remède n'est pas de supprimer l'indicateur, c'est de lui adjoindre un contre-KPI.

---

## 5. Cours approfondi

### 5.1 Les six critères

| # | Critère | La question posée | Le test de vérification |
|---|---|---|---|
| 1 | **Sourcé** | d'où vient la donnée ? | la source existe, elle est nommée, et elle se met à jour |
| 2 | **Défini** | que calcule-t-on, exactement ? | deux personnes appliquent la formule et trouvent le même nombre |
| 3 | **Attribué** | qui répond de ce chiffre ? | un nom, une fonction, et le droit de trancher les désaccords |
| 4 | **Comparable** | peut-on comparer dans le temps et entre unités ? | même formule partout, variation ni nulle ni frénétique |
| 5 | **Pilotable** | que fait-on quand il est rouge ? | un seuil chiffré et une action écrite |
| 6 | **Contre-balancé** | qu'est-ce qu'on dégrade en l'améliorant ? | un contre-KPI publié à côté |

**Les six critères ne sont pas une liste de bonnes intentions : chacun a un test.** Et chaque test a
échoué, quelque part dans le dossier du projet — c'est ce qui va suivre, critère par critère.

### 5.2 La carte de définition, champ par champ

| Champ | Rôle | Exemple pour le taux de rupture |
|---|---|---|
| **Formule** | lever toute ambiguïté sur numérateur et dénominateur | couples produit-magasin-mois en rupture ÷ couples servis |
| **Source** | nommer la table et le référentiel | `ruptures.csv` et les ventes servies du mois |
| **Granularité** | dire ce que représente une ligne du résultat | produit × magasin × mois |
| **Fréquence** | dire quand il est juste | le 5 du mois suivant, données arrêtées au dernier jour |
| **Responsable** | nommer qui répond de la définition | direction des opérations |
| **Seuil d'alerte** | chiffrer ce qui déclenche | plus de **10 %** des couples servis en rupture |
| **Contre-KPI** | publier ce qui se dégrade | rotation de stock (**9,42** tours) et couverture (**1,27** mois) |

Les sept champs, multipliés par les **10** indicateurs du mandat, font **70** cases à remplir. Le dossier
raté comptait **41** indicateurs et **zéro** case remplie. Le projet n'exige donc pas **plus** de
documents que le prestataire précédent : il exige **4,1 fois moins** d'indicateurs, chacun documenté.

### 5.3 Critère 1 — sourcé : une source absente ne se remplace pas

Le socle de M12 a été construit exactement pour respecter ce critère. Les ventes de M01—M03 existaient
déjà ; le module a ajouté **cinq** sources opérationnelles, et **pas une de plus** :

| Source ajoutée | Lignes | Ce qu'elle rend possible |
|---|---|---|
| coût d'achat | **154** | la marge, donc **3 847 989 780** FCFA |
| stock mensuel | **6 776** | la rotation (**9,42** tours) et la couverture (**1,27** mois) |
| ruptures | **2 428** | le taux de rupture (**7,29 %**) et les **13 129** jours cumulés |
| commandes clients | **9 000** | le taux de service (**81,0 %** ou **78,2 %**) |
| encaissements | **9 000** | le taux de recouvrement (**74,0 %**) et l'encours (**1 202 550 590** FCFA) |

La règle qui a présidé à cette liste tient en une phrase : **un indicateur réclame sa source, et une
source absente ne se remplace pas par une approximation.** Sans coût d'achat, on ne fabrique pas une
marge : on fabrique une opinion sur la marge. Le dossier du projet l'a fait — **deux** coûts pour un
produit, et la question « où perdons-nous de la marge ? » jamais résolue.

> **Attention.** Le tableur sait tout faire, y compris remplir un trou : une colonne de coûts
> manquante se « complète » en recopiant la ligne du dessus. L'approximation ne se voit pas dans le
> résultat — elle se voit dans la décision. Un indicateur dont la source n'existe pas doit être
> **refusé**, puis remplacé par un indicateur dont la source existe.

### 5.4 Critère 2 — défini sans ambiguïté : le cas du taux de retour

Voici la démonstration centrale du chapitre. Le socle porte **2 809** lignes de retour. Le mot « taux de
retour » peut recevoir **six** définitions, toutes défendables :

| Définition | Formule | Résultat mesuré |
|---|---|---|
| valeur | valeur retournée ÷ valeur vendue | **1,12 %** |
| quantité, signée | quantité retournée ÷ quantité vendue | **−1,17 %** |
| quantité, absolue | quantité retournée (valeur absolue) ÷ quantité vendue | **1,16 %** |
| lignes | lignes de retour ÷ lignes totales | **1,17 %** |
| tickets | tickets portant un retour ÷ tickets | **1,91 %** |
| lignes par magasin | lignes de retour du magasin ÷ lignes du magasin | dépend du magasin |

Deux enseignements, et ils sont différents :

1. **L'écart est réel.** Du plus bas (**1,12 %**) au plus haut (**1,91 %**), il y a **0,79** point, soit
   un facteur **1,71**. Publier « le taux de retour est de 1 % » ou « de 2 % » peut donc être juste dans
   les deux cas — et diriger deux décisions opposées.
2. **Une formule fausse ne se voit pas toujours, et parfois si.** En quantités **signées**, le taux vaut
   **−1,17 %** : les retours sont enregistrés avec des quantités négatives, et la division d'une somme
   négative par une somme positive donne un nombre négatif. Un taux négatif ne se discute pas, il
   **crie** — c'est le même genre d'erreur que la rotation tombant de **9,42** à **0,78** quand on
   additionne des stocks (C03).

Le même phénomène frappe la **marge**, et là, il ne crie pas. La marge brute est de **3 847 989 780**
FCFA. Rapportée au chiffre d'affaires **hors taxes**, elle vaut **29,12 %** ; rapportée au chiffre
d'affaires **toutes taxes comprises**, **24,67 %**. La cible du référentiel — **18** à **24 %** — est
formulée hors taxes : sans cette précision, le même résultat serait « au-dessus de la cible » ou
« conforme ». Et l'écart entre CA net et CA brut (**175 169 798** FCFA, **1,12 %**) explique à lui seul
la première dispute du dossier.

### 5.5 Critère 3 — attribué : un nom, pas un comité

Le dossier du projet compte **41** indicateurs, **7** onglets, **14** destinataires et **aucun**
responsable. C'est la cause directe des deux questions de discorde : personne n'était là pour
**trancher**. Un indicateur attribué se reconnaît à trois signes :

1. **Un nom** apparaît sur la carte — une fonction, pas un service.
2. Cette personne **arbitre** les désaccords de définition ; elle n'a pas besoin d'être d'accord avec
   la comptabilité, elle doit décider **quelle définition est publiée**.
3. Elle **répond** de la fraîcheur de la source : si la donnée arrive le 8 au lieu du 5, c'est elle qui
   prévient le lecteur.

Sur les **10** indicateurs du mandat, cela fait **10** responsabilités nommées. Le dossier en comptait
zéro pour **41** indicateurs : ce n'est pas un manque de rigueur, c'est une **absence d'organisation**.

### 5.6 Critère 4 — comparable : ni immobile, ni frénétique

Un indicateur comparable se reconnaît à deux excès qu'il évite. Le socle en fournit un de chaque :

| Indicateur | Comportement mesuré | Verdict |
|---|---|---|
| nombre de magasins actifs | **5**, et **1** seule valeur distincte sur **44** mois | **immobile** : il n'informe pas |
| panier moyen journalier | moyenne **65 655** FCFA, écart-type **89 162** FCFA, soit **135,8 %** | **frénétique** : illisible au jour |
| CA mensuel | de **199 549 035** à **533 572 353** FCFA, médiane **344 872 808** | comparable : la variation raconte la saisonnalité |

La conclusion pratique est une règle de **fréquence** : le CA se lit au **mois**, pas au jour ; le
nombre de magasins se lit **quand le réseau change**, pas tous les matins ; la rupture se lit au jour,
parce qu'elle se répare au jour. Une carte de définition sans fréquence raisonnée produit des lecteurs
qui regardent le mauvais chiffre au mauvais rythme.

### 5.7 Critère 5 — pilotable : le seuil et l'action

La question la plus importante du mandat — « que fait-on quand c'est rouge ? » — se traite en deux
temps : **poser le seuil**, puis **écrire l'action**.

**Poser le seuil se mesure.** Sur la couverture de stock, quatre seuils produisent quatre réalités très
différentes :

| Seuil de couverture | Lignes de stock en alerte | Part des **6 776** | Produits concernés |
|---|---|---|---|
| sous **0,8** mois | **176** | **2,6 %** | **16** |
| sous **1** mois | **1 650** | **24,4 %** | **50** |
| sous **1,2** mois | **3 344** | **49,4 %** | **87** |
| sous **1,5** mois | **5 126** | **75,6 %** | **126** |

Un seuil qui déclenche sur **75,6 %** des lignes ne déclenche rien : il décrit le stockage normal du
distributeur. Un seuil à **2,6 %** ne déclenche pas assez tôt. La carte retient **1** mois, qui met en
alerte **50** produits sur **154** — assez pour agir, assez peu pour que la liste soit traitable.

**Écrire l'action se mesure aussi.** Le modèle du module est la balance âgée : **1 155** factures de
plus de **90** jours, **1 091 339 030** FCFA, **90,8 %** de l'encours ouvert. L'action n'est pas
« surveiller les impayés » : c'est **relancer ces 1 155 factures**, dans cet ordre, avec ce volume. Une
action sans volume ni destinataire n'est pas une action, c'est un souhait.

### 5.8 Critère 6 — contre-balancé : les dix couples

Le mandat exige un contre-indicateur par KPI. Les **10** couples du module, chacun avec ses valeurs
mesurées :

| Indicateur | Ce qu'il pousse à faire | Son contre-KPI | Le couple, mesuré |
|---|---|---|---|
| CA net | vendre plus, vite | taux de retour | **15 595 154 955** FCFA contre **1,17 %** de retour |
| Marge brute | monter les prix | volume vendu | recette unitaire × **1,174** et unités × **1,169** (2023 → 2025) |
| Taux de rupture | stocker plus | rotation | **7,29 %** contre **9,42** tours |
| Rotation | réduire le stock | taux de rupture | **9,42** tours contre **7,29 %** |
| Panier moyen | vendre des lots | marge brute | **107 396** FCFA contre **29,12 %** |
| Taux de retour | contrôler les retours | taux de service | **1,17 %** contre **81,0 %** |
| Taux de service | promettre large | coût logistique unitaire | **81,0 %** contre **3 284** FCFA par colis |
| Taux de recouvrement | relancer vite | CA net | **74,0 %** contre **15 595 154 955** FCFA |
| Coût logistique unitaire | grouper les tournées | taux de service | **3 284** FCFA contre **81,0 %** |
| Part de marché interne | défendre son magasin | CA du réseau | **60,8 %** / **39,2 %** à Ouagadougou |

Trois de ces couples méritent d'être regardés de près, parce que la mesure y tranche un débat :

1. **Marge contre volume.** La direction a augmenté les prix : la recette moyenne par unité vendue est
   passée de **8 714** à **10 226** FCFA entre 2023 et 2025, et les unités vendues ont **augmenté**
   aussi (× **1,169**), avec **4,3 %** de clients de plus. Le contre-KPI **autorise** donc la
   stratégie — c'est précisément son rôle : il ne l'interdit pas, il la **surveille** et l'aurait
   interdite si le volume avait chuté.
2. **Rotation contre rupture.** Couverture moyenne **1,27** mois, rotation **9,42** tours, rupture
   **7,29 %** : ces trois chiffres se publient ensemble, parce que le premier se gagne toujours sur le
   dos des deux autres.
3. **Part de marché interne.** À Ouagadougou, deux magasins se partagent le marché **interne** :
   **60,8 %** pour Ouaga 2000 (**5 312 205 459** FCFA) et **39,2 %** pour Gounghin (**3 424 978 244**
   FCFA). Tout gain de l'un est une perte de l'autre : le contre-KPI est le **CA du réseau**, sans quoi
   l'indicateur récompense un transfert interne — un magasin qui prend des clients à son voisin ne fait
   pas grandir l'enseigne.

### 5.9 Le catalogue des effets pervers

Un effet pervers n'est pas une erreur de mesure : c'est une **conséquence** de la mesure, quand elle
devient un objectif. Les sept mécanismes, chacun avec un exemple mesurable dans ce module :

1. **Déplacer le problème.** Réduire la rupture en sur-stockant dégrade la rotation (**9,42** tours) et
   la trésorerie : **2 034 733** unités si l'on cumule les mois, contre **45 882** en stock réel.
2. **Étrangler le canal.** Améliorer le taux de recouvrement (**74,0 %**) en durcissant les conditions
   tarifaires réduit le CA — c'est pourquoi les deux se publient ensemble.
3. **Rétrécir le périmètre.** Un taux de service calculé sur les seules commandes livrées vaut **81,0 %** ;
   sur toutes les commandes, **78,2 %** — les **319** commandes annulées disparaissent du premier calcul.
4. **Choisir le dénominateur.** Le panier moyen vaut **107 396** FCFA par ticket et **65 749** FCFA par
   ligne, soit **38,8 %** de moins : un indicateur peut être « amélioré » en changeant d'unité de compte.
5. **Doper la mesure.** Un taux de retour de **1,17 %** s'améliore en décourageant les retours : le
   contre-KPI est le taux de service, parce qu'un retour est souvent une livraison qui a échoué.
6. **Geler la cible.** Une marge de **29,12 %** évaluée contre une cible de **18** à **24 %** sans dire
   si la base est hors taxes ou toute taxe comprise : la cible ne veut rien dire (C04, §5.4).
7. **Oublier le coût.** Le coût logistique unitaire est de **3 284** FCFA par colis (**249** FCFA au
   kilo, **50,5 %** de carburant) : toute promesse de service plus rapide doit se chiffrer contre lui.

> **Attention.** Un effet pervers n'est pas une faute professionnelle : c'est la conséquence
> **prévisible** d'un indicateur devenu objectif, produite par des gens compétents qui font exactement
> ce qu'on leur a demandé. Chercher un coupable quand un chiffre est « amélioré » sans que la
> performance suive, c'est se tromper de cible : c'est la **carte** qu'il faut corriger.

**La règle du catalogue** : pour chaque indicateur, demandez-vous ce qu'une personne **astucieuse et
pressée** ferait pour l'améliorer. La réponse est votre contre-KPI.

---

## 6. Exemple concret — la carte remplie du taux de rupture

Le mandat demande des cartes, pas des intentions. Voici une carte complète, telle qu'elle se publie :

| Champ | Contenu |
|---|---|
| **Indicateur** | taux de rupture |
| **Formule** | couples produit-magasin-mois en rupture ÷ couples produit-magasin-mois servis |
| **Source** | `ruptures.csv` (jours de rupture, unités perdues estimées) + ventes servies |
| **Granularité** | produit × magasin × mois |
| **Fréquence** | mensuelle, le 5 du mois suivant |
| **Responsable** | direction des opérations (arbitre les cas litigieux avec les achats) |
| **Valeur actuelle** | **7,29 %** — **2 428** couples sur **33 296** ; **13 129** jours cumulés |
| **Seuil d'alerte** | plus de **10 %** des couples servis du mois, ou plus de **400** jours cumulés |
| **Action si rouge** | liste des 20 produits les plus touchés, revue avec les achats sous 5 jours |
| **Contre-KPI** | rotation (**9,42** tours) et couverture (**1,27** mois) |
| **Coût estimé du phénomène** | **169 386 812** FCFA (estimation, à citer comme telle) |

Ce que cette carte change, concrètement : la question « que fait-on quand c'est rouge ? » a désormais
une réponse nominative et datée, et le chiffre de **169 386 812** FCFA ne peut plus être cité sans son
étiquette d'**estimation**.

> **Dans les faits.** Dans cet atelier, chaque valeur des cartes est **recalculée à chaque exécution**
> par `tools/kpi_M12.py` : les six définitions du taux de retour, les quatre seuils de couverture, la
> dispersion de la marge par famille et les dix couples indicateur / contre-KPI sortent de la même
> exécution, imprimés en console avec leur définition au-dessus du chiffre. Une carte dont les valeurs
> ne se recalculent pas n'est pas une carte : c'est une capture d'écran.

---

## 7. Démonstration pas à pas — six étapes pour fabriquer un indicateur

### 7.1 Étape 1 — partir d'une question de décision, pas d'une donnée

« Le service est-il tenu ? » est une question de décision. « Taux de service » est un mot. La carte
commence par la question : qui décide, quand, et de quoi ?

### 7.2 Étape 2 — choisir le régime et le niveau

D'après C02, « le service est-il tenu ? » est un indicateur **prescriptif** au niveau tactique : il
déclenche une relance ou un arbitrage, une fois par mois.

### 7.3 Étape 3 — écrire la formule et mesurer les deux versions

Taux de service sur les commandes **livrées** : **81,0 %** (**8 681** commandes livrées). Sur **toutes**
les commandes : **78,2 %** — les **319** commandes annulées sortent du dénominateur dans la première
version. La carte retient **78,2 %**, la plus sévère, avec la mention explicite « annulées incluses ».

### 7.4 Étape 4 — vérifier la source et la granularité

Source : `commandes_clients.csv`, **9 000** commandes, une ligne par commande. Granularité de la
publication : le mois et le magasin. Le retard médian (**5** jours) se publie à côté du taux : un taux
tenu avec cinq jours de retard n'est pas un service tenu.

### 7.5 Étape 5 — poser le seuil et l'action

Seuil retenu : **78,2 %**, c'est-à-dire « ne pas descendre sous le niveau actuel ». Action si rouge :
revue des **319** commandes annulées, par cause, avec le responsable logistique.

### 7.6 Étape 6 — choisir le contre-KPI et le publier

Contre-KPI : le coût logistique unitaire, **3 284** FCFA par colis. Un taux de service qui remonte par
des livraisons urgentes se verra immédiatement dans ce coût — et c'est voulu.

**Le test final** : deux personnes différentes remplissent la carte séparément. Si les deux cartes
diffèrent d'un seul chiffre, l'indicateur n'est pas prêt.

---

## 8. Erreurs fréquentes

1. **Publier un indicateur sans carte.** Le chiffre est juste, la définition manque : la discussion
   sera un rapport de force, pas un arbitrage.
2. **Croire que le calcul est le sujet.** Le dossier du projet savait calculer **41** indicateurs ; il
   n'en pilotait aucun.
3. **Utiliser une source absente.** Deux coûts pour un produit, et la marge devient une opinion.
4. **Laisser une formule ambiguë.** **1,12 %** ou **1,91 %** de retours, selon la définition : les deux
   sont justes, une seule sera publiée.
5. **Ne pas nommer de responsable.** **41** indicateurs, **0** nom, deux versions du CA qui cohabitent.
6. **Poser un seuil sans action.** La question « que fait-on si la rupture dépasse le seuil ? » n'aura
   pas de réponse — c'est exactement ce qui s'est passé.
7. **Choisir un seuil qui déclenche partout.** À **1,5** mois de couverture, **75,6 %** des lignes
   s'allument : personne ne regarde plus.
8. **Confondre effet pervers et erreur.** L'effet pervers est produit par des gens compétents qui font
   ce qu'on leur demande de mesurer.
9. **Oublier le contre-KPI sur les indicateurs conflictuels.** Part de marché interne, rotation,
   recouvrement : ce sont les trois où la triche est la plus rentable à court terme.
10. **Multiplier les indicateurs.** **41** indicateurs, **4** ouvertures le premier jour : la surcharge
    tue la lecture avant que les chiffres soient faux.

---

## 9. Bonnes pratiques professionnelles

- **Une carte par indicateur**, publiée avec lui, **7** champs remplis, aucune case vide.
- **Partir de la question de décision** : qui, quand, pour agir sur quoi.
- **Mesurer les variantes de la formule** avant de choisir : les deux versions du taux de service
  (**81,0 %** / **78,2 %**) et les six du taux de retour (**1,12 %** à **1,91 %**) se calculent en
  quelques minutes et évitent six mois de débat.
- **Poser le seuil en regardant ce qu'il déclenche** : **50** produits à **1** mois, **126** à **1,5**
  mois — le seuil est un choix, et il se mesure.
- **Associer une action écrite à chaque seuil**, avec un volume et un destinataire.
- **Publier le contre-KPI dans le même écran**, jamais dans une note de bas de page.

> **Conseil professionnel.** Quand on vous demande un indicateur, la première réponse utile n'est pas un
> chiffre : c'est une carte à remplir. Un lecteur qui remplit les **7** champs découvre lui-même la
> question qu'il n'avait pas posée — et cette découverte vaut plus que les dix indicateurs demandés au
> départ.

---

## 10. Exercice guidé

**Énoncé.** La direction veut suivre « la part des clients non identifiés ». Rédigez la carte complète,
avec les valeurs du socle.

**Étape 1 — la source.** Les ventes portent un identifiant client. Une partie des lignes utilise le
client **0**, hors référentiel (M11.C04) : la source existe, la définition du phénomène est
« identifiant manquant », pas « client inconnu ».

**Étape 2 — la mesure.** Le client **0** représente **18,3 %** du chiffre d'affaires, soit
**2 852 612 447** FCFA. C'est le premier chiffre du dossier, et il est déjà une surprise : près d'un
cinquième du chiffre d'affaires n'est rattaché à aucun client nommé.

**Étape 3 — la formule ambiguë.** Deux définitions : part des **lignes** sans identifiant, ou part du
**chiffre d'affaires**. Les deux se défendent ; la seconde dit la perte de connaissance réelle, la
première dit la qualité de la saisie au comptoir. La carte doit choisir, et écrire pourquoi.

**Étape 4 — le seuil et l'action.** Seuil : **15 %** du chiffre d'affaires. Action si rouge : contrôle
de saisie par magasin, avec la liste des tickets concernés ; l'indicateur est un indicateur de
**qualité de la donnée**, pas de performance commerciale.

**Étape 5 — le contre-KPI.** Le nombre de clients identifiés n'augmente jamais aussi vite qu'en
forçant la création de fiches doublons : le contre-KPI est donc le taux de doublons ou le nombre de
fiches créées par vendeur, à surveiller. Sans lui, l'indicateur s'améliore en polluant le référentiel.

**Étape 6 — la carte.** Formule : CA des lignes à identifiant manquant ÷ CA total. Source : ventes et
référentiel clients. Granularité : magasin × mois. Fréquence : mensuelle. Responsable : responsable
qualité de la donnée. Seuil : **15 %**. Contre-KPI : doublons de fiches clients.

---

## 11. Exercices autonomes

1. **Six critères.** Reprenez les **10** indicateurs du mandat et dites lesquels échouent au critère
   « comparable » si l'on ne précise pas la base (hors taxes ou toute taxe comprise).
2. **Six définitions.** Recalculez le taux de retour de six façons sur le socle et expliquez, pour
   chacune, quelle décision elle sert.
3. **Seuil.** Choisissez un seuil pour le taux de recouvrement (**74,0 %** aujourd'hui) et mesurez ce
   qu'il déclenche sur les **9 000** factures.
4. **Contre-KPI.** Proposez le contre-KPI du panier moyen et vérifiez sur le socle qu'il produit une
   mesure utile.
5. **Effet pervers.** Une direction annonce : « la rotation doit passer de **9,42** à **12** tours ».
   Écrivez ce qui va se passer, en trois phrases, et l'indicateur qui le prouvera.
6. **Carte complète.** Rédigez la carte du coût logistique unitaire (**3 284** FCFA par colis) avec les
   **7** champs.

---

## 12. Correction détaillée

**Exercice 1.** La marge brute (**29,12 %** hors taxes contre **24,67 %** toute taxe comprise), le taux
de service (**81,0 %** livrées contre **78,2 %** toutes commandes) et le panier moyen (**107 396** FCFA
par ticket contre **65 749** par ligne) sont les trois sensibles à la base : leurs cartes doivent
l'écrire.

**Exercice 2.** Valeur **1,12 %** (décision financière), quantité signée **−1,17 %** (formule
inutilisable), quantité absolue **1,16 %** (décision logistique), lignes **1,17 %** (qualité de service),
tickets **1,91 %** (expérience client), par magasin (pilotage local). Le choix se justifie par la
décision, jamais par la facilité.

**Exercice 3.** Un seuil à **70 %** mettrait en alerte la quasi-totalité du portefeuille ; à **74,0 %**,
il signale les mois en recul. Calcul : nombre de factures réglées à échéance ÷ **9 000** ; aujourd'hui
**6 660** factures, **1 272** ouvertes, encours **1 202 550 590** FCFA.

**Exercice 4.** Le contre-KPI naturel du panier moyen est la **marge brute** : vendre des lots à prix
cassé augmente le panier et dégrade la marge. Sur le socle, la marge de **29,12 %** et le panier de
**107 396** FCFA se suivent mois par mois, ce qui rend l'arbitrage visible.

**Exercice 5.** Passer de **9,42** à **12** tours signifie réduire la couverture sous **1** mois
(couverture actuelle **1,27**) ; mécaniquement, la part des produits sous **1** mois de couverture
passerait de **50** à davantage, et le taux de rupture (**7,29 %**) monterait. L'indicateur qui le
prouve est le taux de rupture par famille, publié chaque mois à côté de la rotation.

**Exercice 6.** Formule : coût logistique total ÷ colis expédiés. Source : `logistique_mensuelle.csv`
(**264** lignes) et colis des magasins (**43 830** des **52 596** colis, le dépôt en facture **8 766**
sans vendre). Granularité : magasin × mois. Fréquence : mensuelle. Responsable : responsable
logistique. Seuil : **3 500** FCFA par colis. Contre-KPI : taux de service.

---

## 13. Mini-projet de chapitre

**« Deux cartes, dont une pour un indicateur qu'on n'aime pas »** (2 h). Choisissez deux indicateurs du
mandat : un que vous jugez utile et un que vous jugez dangereux. Remplissez les **7** champs pour les
deux, avec les valeurs mesurées du socle. Puis répondez en une page : le second indicateur est-il
sauvable par un contre-KPI, ou faut-il le retirer ? Argumentez avec des chiffres, jamais avec des
principes. Ce travail est la moitié du livrable P2 du projet.

---

## 14. Résumé du chapitre

| Notion | Ce qu'il faut retenir |
|---|---|
| Les six critères | sourcé, défini, attribué, comparable, pilotable, contre-balancé — chacun a un test |
| La carte | **7** champs, **70** cases pour **10** KPI, contre **41** indicateurs sans carte |
| Défini sans ambiguïté | taux de retour de **1,12 %** à **1,91 %** ; marge de **29,12 %** ou **24,67 %** selon la base |
| Seuil | à **1** mois de couverture : **1 650** lignes (**24,4 %**) et **50** produits ; à **0,8** mois : **176** lignes |
| Action | **1 155** factures de plus de **90** jours, **1 091 339 030** FCFA — une action a un volume |
| Contre-KPI | marge contre volume : recette unitaire × **1,174**, unités × **1,169** |
| Effets pervers | déplacer, étrangler, rétrécir, choisir son dénominateur, doper, geler, oublier le coût |

## 15. À retenir

> **À retenir.** Un indicateur se juge à sa **carte**, pas à sa formule. Les six critères se vérifient en
> quelques minutes chacun, et chacun a déjà coûté cher à quelqu'un : **41** indicateurs sans responsable,
> un seuil sans action, une marge sans base, un service sans dénominateur.

- **Sourcé** : une source absente ne se remplace pas par une approximation — la marge a besoin du coût
  d'achat, pas d'une recopie.
- **Défini** : écrivez la formule, puis calculez **les autres versions possibles** : c'est le seul
  moyen de savoir ce que vous publiez.
- **Attribué** : un nom par indicateur ; **10** KPI, **10** responsables.
- **Pilotable** : un seuil qui discriminate (**50** produits, pas **126**) et une action avec volume et
  destinataire.
- **Contre-balancé** : demandez-vous ce qu'une personne pressée ferait pour améliorer le chiffre — puis
  mesurez-le.

## 16. Évaluation formative

1. Citez les six critères d'un indicateur utilisable.
2. Quels sont les **7** champs d'une carte de définition ?
3. Pourquoi une carte de définition se remplit-elle **avant** d'écrire la requête ?
4. Combien de définitions différentes du taux de retour le socle permet-il de mesurer, et quel est
   l'écart entre la plus basse et la plus haute ?
5. Pourquoi une des formules donne-t-elle un nombre négatif, et que révèle ce signe ?
6. La cible de marge est de **18** à **24 %** : quelle précision manque-t-il pour qu'elle ait un sens ?
7. Un seuil qui met en alerte **75,6 %** des lignes est-il un bon seuil ? Justifiez par la mesure.
8. Qu'est-ce qu'une action associée à un seuil, et qu'est-ce qui la distingue d'un souhait ?
9. Pourquoi la part de marché interne a-t-elle besoin d'un contre-KPI ? Lequel ?
10. Le taux de service vaut **81,0 %** ou **78,2 %** : dites ce qui change entre les deux, et ce que la
    carte doit écrire.

**Corrigé :** 1. Sourcé, défini, attribué, comparable, pilotable, contre-balancé. 2. Formule, source,
granularité, fréquence, responsable, seuil d'alerte, contre-KPI. 3. Parce que la formule découle de la
décision, et non l'inverse : commencer par la requête revient à laisser la source choisir l'indicateur.
4. Six, de **1,12 %** à **1,91 %** — **0,79** point d'écart, un facteur **1,71**. 5. Parce que les
retours portent des quantités **négatives** : le signe révèle que le numérateur et le dénominateur ne
parlent pas de la même population. 6. La **base** : hors taxes (**29,12 %**) ou toute taxe comprise
(**24,67 %**). 7. Non : un seuil qui s'allume sur les trois quarts des lignes décrit la normale et ne
déclenche aucune action ; **1** mois (**24,4 %**) est retenu. 8. Une action a un **volume**, un
**destinataire** et une **date** : les **1 155** factures de plus de **90** jours relancées sous
quinzaine. 9. Parce que le gain d'un magasin est la perte d'un autre dans la même ville (**60,8 %**
contre **39,2 %** à Ouagadougou) : le contre-KPI est le CA du **réseau**. 10. Le premier ne compte que
les commandes **livrées** ; le second inclut les **319** commandes annulées : la carte publie **78,2 %**,
la version la plus sévère.
