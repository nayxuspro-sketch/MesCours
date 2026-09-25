# Module M14.C06 — Construire les visuels

**Outils : DuckDB 1.5.5 (exécuté) ; pandas (non requis). Power BI Desktop est *cité* — l'outil n'est pas
installé dans cet atelier (règle §1.5). Ce que les données imposent au dessin est **mesuré** sur le socle
à chaque exécution de `tools/mesures_M14.py`, section `visuels` : les cinq magasins qui vendent, les sept
familles, les quarante-quatre mois, la matrice des familles et le taux de réalisation des objectifs.**

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **dessiner les trois pages du rapport commercial** et ses **14** visuels — 5 pour la page Direction,
   5 pour la page Commercial, 4 pour la page Approvisionnement — plus deux pages de détail et une page
   d'aide sans donnée ;
2. **choisir un type de visuel à partir d'une question**, pas d'une préférence : les **5** magasins qui
   vendent vont de **11,1 %** à **34,1 %** du chiffre d'affaires, un rapport de **3,06** entre le premier
   et le dernier ;
3. **régler une échelle** : le chiffre d'affaires mensuel va de **199 549 035** à **533 572 353** FCFA
   (**2,67** fois), et une courbe qui ne part pas de zéro transforme cette variation en feuilleton ;
4. **calibrer une jauge sur la donnée**, pas sur l'usage : le taux de réalisation des objectifs vaut
   **259,1 %** sur les huit mois de 2026, et va de **163,9 %** à **329,5 %** selon le magasin et le mois ;
5. **écrire la mise en page, le thème, la charte et l'accessibilité** du rapport — dont les **4** signets
   de navigation et les **6** erreurs de visuel qui se voient.

---

## 2. Pourquoi cette notion est importante

Un rapport ne se juge pas sur ce qu'il contient, mais sur ce qu'un lecteur en fait en dix secondes. Ce
chapitre est celui où le travail des cinq précédents devient visible — ou invisible.

**La première conséquence est la décision.** Un visuel qui ne répond pas à une question nommée occupe
une place sans travailler. Le rapport du fil rouge porte **14** visuels, et chacun répond à une phrase
écrite dans le dossier de conception. Un quinzième visuel sans question est un bruit de plus : à trois
pages, la contrainte n'est pas l'espace, c'est l'attention.

**La deuxième est la hiérarchie des perceptions.** L'œil classe mieux des positions et des longueurs
que des angles ou des aires — c'est le résultat que M10 a posé avec Cleveland et McGill, et il se
vérifie ici : cinq magasins entre **11,1 %** et **34,1 %** se comparent très bien en barres, beaucoup
moins bien dans un disque. Le même constat vaut pour les sept familles, qui vont de
**1 056 068 339** à **3 535 582 421** FCFA, un rapport de **3,35**.

**La troisième est l'honnêteté de l'échelle.** La donnée du fil rouge contient un piège mesuré : le
taux de réalisation des objectifs dépasse **259 %**. Une jauge réglée à 100 % comme maximum ne peut pas
l'afficher, et un graphique qui ne peut pas montrer le chiffre juste oblige à mentir au lecteur — ou à
changer de graphique. C'est exactement ce que ce chapitre apprend à faire.

---

## 3. Explication simple — le visuel est une phrase, pas une décoration

Pensez à un visuel comme à une phrase. Un titre, un sujet, un chiffre, une unité, une période :

- le **titre** affirme le constat — « le réseau vend 34,1 % de son chiffre d'affaires à Ouaga 2000 » ;
- le **sujet** est la catégorie dessinée — les cinq magasins, les sept familles, les quarante-quatre
  mois ;
- le **chiffre** est la mesure — `[CA net]`, `[Panier moyen]`, `[Taux de rupture %]` ;
- l'**unité** est écrite quelque part — FCFA, pourcentage, nombre de tickets ;
- la **période** est écrite aussi — les douze derniers mois, l'exercice 2026, le mois choisi.

Une phrase sans sujet n'existe pas ; un visuel sans question non plus. La différence entre un rapport
d'école et un rapport professionnel tient rarement au code des mesures — il tient à ces cinq éléments,
répétés sur les **14** visuels sans exception. Et quand l'un des cinq manque, l'erreur n'est pas
esthétique : le lecteur tire une conclusion fausse, puis décide.

---

## 4. Vocabulaire essentiel

| Terme | Ce qu'il désigne sur le fil rouge |
|---|---|
| **Visuel** | le dessin d'une mesure sous un filtre : les **14** visuels des trois pages du rapport |
| **Carte** | la vignette d'une **seule** valeur — « carte du CA net » —, à ne pas confondre avec la carte géographique |
| **Page** | le groupe de visuels qui servent une même décision : Direction, Commercial, Approvisionnement |
| **Barres ordonnées** | des barres **triées** par la mesure, du plus grand au plus petit : le classement fait le travail |
| **Matrice** | un tableau croisé avec des valeurs au centre : magasin × famille, **42** cases |
| **Nuage de points** | deux mesures sur deux axes, une catégorie par point : couverture × rotation |
| **Jauge** | un cadran à un seul chiffre, avec un maximum choisi — et c'est ce maximum qui fait la jauge |
| **Signet** | une vignette d'état du rapport : page, filtres, visuels visibles — le rapport en porte **4** |
| **Thème** | le fichier de styles du rapport : couleurs, polices, tailles, format des nombres |
| **Charte** | la règle écrite qui dit quel usage pour quelle couleur : **7** familles, **3** couleurs de statut |
| **Contraste** | l'écart de luminance entre un texte et son fond, minimum **4,5** pour 1 pour un texte courant |
| **Table de données** | l'affichage des valeurs sous un visuel, pour ceux qui ne voient pas la forme |
| **Ordre de tabulation** | l'ordre dans lequel la touche de tabulation parcourt la page, du titre à la source |
| **Gestion des vides** | la règle qui dit quoi faire d'une case sans valeur : **7** des **42** cases de la matrice |

> **Définition.** Un **visuel** est la représentation d'une **mesure** sous un contexte de filtre, et il
> n'est lisible que si le rapport dit **quoi**, **où**, **quand** et **en quelle unité**. Quatre mentions
> écrites, ou le visuel sera relu de travers.

> **Définition.** Une **carte** — en anglais *card* — est la vignette qui affiche **une seule** valeur,
> très grande, pour le chiffre dont on veut se souvenir en entrant dans la page. Le même mot désigne
> aussi le visuel géographique : dans un dossier de conception, on écrit laquelle des deux, sans quoi
> deux personnes construiront deux choses différentes.

> **Définition.** La **charte** est la règle écrite qui associe un usage à une couleur : les sept
> familles de produits, trois couleurs de statut, aucune couleur qui ne veuille rien dire. Une palette
> sans usage est une décoration, et une décoration prend la place d'une information.

---

## 5. Cours approfondi

### 5.1 Les trois pages du rapport, et la question de chacune

Le rapport « Ventes Sahel Distribution » tient en **3** pages de fond, et chaque page sert **une**
décision — pas un service, pas une source, pas un thème :

| Page | Visuels | La décision qu'elle sert |
|---|---|---|
| **Direction** | **5** | où va l'activité du réseau, et tient-on l'objectif |
| **Commercial** | **5** | quels magasins et quelles familles vendent, et où le retour coûte |
| **Approvisionnement** | **4** | où l'on manque de stock, et sur quoi l'effort doit porter |

Les **5** visuels de la page Direction sont la carte du chiffre d'affaires net, la jauge de l'objectif
atteint, les barres du chiffre d'affaires par magasin **ordonnées**, la courbe du chiffre d'affaires
mensuel et la carte du taux de marge. La page Commercial porte la matrice magasin × famille, les barres
du panier moyen par magasin, la courbe des retours par mois, le segment des familles et la carte du
taux de retour. La page Approvisionnement porte la carte du taux de rupture, les barres des ruptures par
famille, le nuage couverture × rotation et la matrice des ruptures par magasin et par mois.

À ces **14** visuels s'ajoutent les **deux pages de détail** — détail magasin et détail produit —,
ouvertes par exploration, et une **page d'aide** qui ne contient aucune donnée : les définitions des
indicateurs, les exclusions, la fraîcheur de l'actualisation. Une page d'aide n'est pas un luxe ; c'est
la page qui évite que la question « est-ce que les retours sont dedans ? » se règle par téléphone.

### 5.2 Choisir le visuel : la question d'abord

Le type de visuel ne se choisit pas dans la liste des icônes, il se déduit de la question. Quatre
questions, quatre familles de réponses :

1. **« Combien, en tout ? »** — une **carte** : le chiffre d'affaires net du réseau,
   **15 595 154 955** FCFA.
2. **« Qui est devant qui ? »** — des **barres ordonnées** : les **5** magasins qui vendent.
3. **« Comment cela a-t-il évolué ? »** — une **courbe** : les **44** mois du socle.
4. **« Deux mesures sont-elles liées ? »** — un **nuage de points** : la couverture et la rotation.

Et une question qu'on pose souvent mal : **« où est-ce ? »**. Le socle tient dans **4** villes, dont
**56,0 %** du chiffre d'affaires à Ouagadougou. Une carte géographique montrerait cinq points là où des
barres montrent le même classement ; elle ajoute une projection, une échelle et une surface, et elle
serait lue comme une information alors qu'elle n'en porte pas plus. Le rapport ne retient donc **pas**
de visuel géographique, et cette décision est **écrite** avec ses chiffres — une décision non écrite se
rejoue à chaque réunion.

> **Définition.** La **hiérarchie des perceptions** classe les encodages par ce que l'œil compare le
> mieux : la **position** d'abord, puis la **longueur**, puis l'**angle** et l'**aire**, enfin la
> saturation. Un graphique se choisit en descendant cette liste, jamais en montant.

> **Dans les faits.** Sur le socle du fil rouge, les sept familles vont de **1 056 068 339** à
> **3 535 582 421** FCFA. En barres, la comparaison est immédiate ; en disque, l'écart entre les deux
> dernières familles — 13,0 % du total contre 11,1 % pour les magasins — devient un exercice de
> géométrie. La même question, deux efforts de lecture très différents.

> **À retenir.** Le type de visuel découle de la question, jamais du goût : une carte pour un total, des
> barres triées pour un classement, une courbe pour une évolution, un nuage pour un lien. Les **14**
> visuels du rapport tiennent dans ces quatre familles.

### 5.3 Les barres et le tri : le classement fait la moitié du travail

Une barre non triée cache le message qu'elle porte. Prenons les **5** magasins qui vendent, avec leur
part du chiffre d'affaires du réseau :

| Magasin | Part du chiffre d'affaires |
|---|---|
| Sahel Distribution — Ouaga 2000 | **34,1 %** |
| Sahel Distribution — Gounghin | **22,0 %** |
| Sahel Distribution — Bobo Kibidwé | **19,9 %** |
| Sahel Distribution — Koudougou Centre | **13,0 %** |
| Sahel Distribution — Kaya Marché | **11,1 %** |

Triées du plus grand au plus petit, ces cinq barres racontent en une seconde ce que le comité mettra
vingt minutes à découvrir : le premier magasin pèse **3,06** fois le dernier, et deux magasins font plus
de la moitié du réseau. Rangées dans l'ordre alphabétique — Bobo, Gounghin, Kaya, Koudougou, Ouaga
2000 —, les mêmes barres ne montrent plus rien : l'œil cherche le maximum, le trouve au milieu, et
recommence. Une catégorie non triée ne cache pas un chiffre, elle cache un **classement**.

### 5.4 La courbe, l'axe et la période

Le chiffre d'affaires mensuel du socle couvre **44** mois. Le mois le plus faible vaut
**199 549 035** FCFA, le plus fort **533 572 353** FCFA : un rapport de **2,67** entre les deux. Selon
l'axe, cette même série raconte deux histoires :

- avec un axe qui **part de zéro**, la courbe monte doucement, et l'on voit la **tendance** ;
- avec un axe tronqué au plus près des valeurs, chaque mois devient un événement, et l'on ne voit plus
  que des **variations**.

Aucune des deux lectures n'est fausse ; l'une est adaptée à la question posée, l'autre fabrique une
émotion. La règle est simple : **une courbe de gestion part de zéro**, sauf si le titre dit explicitement
que l'axe est tronqué et pourquoi. Et la période s'écrit : les douze derniers mois du socle portent
**72 068** lignes de vente et **5 172 198 264** FCFA, soit **33,2 %** d'un chiffre d'affaires qui couvre
**44** mois. Un chiffre affiché sans période sera comparé à un autre — et la comparaison sera fausse.

### 5.5 La matrice et les cases vides

La matrice magasin × famille est le visuel le plus dense du rapport : **42** cases — 6 magasins fois
7 familles — dont **35** seulement portent des ventes. Les **7** cases vides ne sont pas des erreurs de
donnée : elles disent qu'un magasin ne référence pas une famille, ce qui est une information
commerciale de premier ordre. Trois façons de traiter le vide, et une seule est professionnelle :

1. le laisser **blanc** et l'expliquer sous le visuel : « blanc = famille non référencée dans ce
   magasin » ;
2. le remplacer par un **zéro** : le lecteur croit alors à une vente nulle, donc à une demande
   insatisfaite — l'inverse du message ;
3. le **masquer** par un filtre : le visuel montre alors une gamme complète, et c'est faux.

Le chapitre 5 avait déjà chiffré ce sujet par un autre chemin : **44** des **264** combinaisons magasin
× mois du socle sont vides, soit **16,7 %**. Une case vide se comprend, elle ne se cache pas — c'est la
ligne « gestion des vides » de la grille de conception en **18** points.

> **Attention.** Un vide n'est pas un zéro. Dans le modèle, une case vide signifie « aucune ligne ne
> répond à cette combinaison » ; un zéro signifie « il y a des lignes, et leur somme est nulle ». Deux
> messages opposés pour le même pixel.

### 5.6 La jauge : un maximum qui vient des données

La page Direction porte une jauge : « l'objectif est-il atteint ? ». Sur les huit mois de 2026, le socle
donne un objectif de **1 297 150 000** FCFA pour **3 360 553 372** FCFA vendus, soit un taux de
réalisation de **259,1 %**. Par magasin et par mois, ce taux va de **163,9 %** à **329,5 %**. Trois
années de suite, il s'établit à **206,4 %** en 2023, **230,0 %** en 2024, **242,0 %** en 2025 puis
**259,1 %** en 2026 : l'objectif n'est pas un plafond, c'est un plancher dépassé.

Une jauge par défaut est graduée de 0 à 100 %. Elle affichera donc une aiguille bloquée en butée, et le
lecteur croira à une saisie erronée — alors que le chiffre est juste. Trois issues, toutes défendables,
à écrire dans le dossier :

1. **régler le maximum sur la donnée** : un cadran gradué jusqu'à **300 %** affiche les cinq magasins et
   laisse voir la dispersion ;
2. **ajouter une cible** au cadran — ici **100 %** —, pour que le dépassement se voie ;
3. **changer de visuel** : une barre avec un repère d'objectif, ou une carte « 259,1 % » avec la
   comparaison en dessous, se lit mieux qu'un demi-cercle saturé.

La leçon dépasse les jauges : **un graphique a des limites, et ses limites doivent être choisies à
partir des valeurs**, sinon ce sont les valeurs qui s'y adaptent — ou qui se taisent.

> **Conseil professionnel.** Avant de poser un visuel à graduation fixe — jauge, compteur, jauge de
> vitesse, barre à maximum —, calculez le minimum et le maximum réels de la mesure sur la période
> affichée. Sur ce socle, ce sont **163,9 %** et **329,5 %** : le réglage par défaut n'aurait pas tenu
> un seul mois.

### 5.7 Les cartes : une valeur, une phrase

Une carte — vignette — affiche **une** valeur, très grande. Elle ne sert pas à informer : elle sert à
**cadrer**. La page Direction en porte deux, et le rapport en totalise plusieurs, toujours pour le même
usage : le chiffre que le lecteur doit avoir en tête avant de lire le reste. Trois règles :

1. **une carte, une mesure** : jamais deux nombres dans la même vignette, sinon le lecteur ne sait plus
   lequel est le sujet ;
2. **l'unité et la période dans le titre ou le sous-titre** : **15 595 154 955** FCFA sur
   **44** mois n'est pas la même information que **5 172 198 264** FCFA sur les **12** derniers ;
3. **pas de carte pour un chiffre qui doit être comparé** : une carte seule ne montre ni rang ni écart ;
   elle s'accompagne du visuel qui classe.

> **Attention.** Un même montant change de sens avec sa période : **5 172 198 264** FCFA sur les
> **12** derniers mois et **15 595 154 955** FCFA sur les **44** mois du socle. Une carte qui ne dit pas
> laquelle des deux périodes elle affiche sera comparée à l'autre, et la comparaison sera fausse.

Le rapport joue sur les deux tableaux : la carte donne l'ordre de grandeur, la barre ordonnée donne le
classement, la courbe donne l'évolution. Un rapport qui n'aurait que des cartes serait un tableau de
chiffres ; un rapport qui n'aurait que des graphiques perdrait le chiffre de tête.

### 5.8 Le camembert : ce qu'on ne dessine pas

Le disque — camembert, anneau — reste le visuel le plus demandé et le plus mal employé. Sur les
**5** magasins du réseau, les parts vont de **11,1 %** à **34,1 %** : cinq angles qu'un œil ne classe
pas, alors que cinq longueurs se classent sans effort. M10 a posé le résultat expérimental — les
comparaisons de longueur sont plus fiables que les comparaisons d'angle —, et le socle en donne l'ordre
de grandeur.

Deux exceptions, et elles sont étroites :

- **deux parts** — « 56,0 % à Ouagadougou, le reste ailleurs » : la lecture est binaire, le disque passe ;
- **une part contre un tout**, quand le message est « cette part, dans l'ensemble » et que le lecteur n'a
  pas à comparer les parts entre elles.

Partout ailleurs — cinq magasins, sept familles, quatre segments — les barres ordonnées gagnent. Et
quand les catégories dépassent la dizaine, aucune des deux formes ne tient : on regroupe, ou l'on change
de question.

### 5.9 Mise en page, thème et charte

Une page de rapport se lit comme une page de journal : un titre qui dit le constat, une zone d'attention
en haut à gauche, des visuels grands et peu nombreux, une source et une date en bas. Trois règles de
densité, vérifiables sur le rapport du fil rouge :

1. **un visuel, une question** : **14** visuels pour **3** pages, soit cinq par page au maximum ;
2. **une taille qui suit l'importance** : le visuel qui porte la décision de la page est le plus grand ;
3. **une bande de contexte** : la période, le magasin, la fraîcheur de la donnée, écrites une fois pour
   toute la page.

Le **thème** transporte les polices, les tailles et le format des nombres — l'unité comprise, jamais
trois décimales là où une suffit. La **charte** va plus loin : elle dit **quel usage pour quelle
couleur**. Sur ce rapport, cela se traduit par une palette courte : les **7** familles de produits ont
leurs couleurs, et **3** couleurs de statut disent l'état — conforme, à surveiller, en alerte. Une
couleur qui ne porte ni catégorie ni statut est du bruit, et le bruit coûte le contraste dont
l'accessibilité a besoin.

### 5.10 Les 4 signets et la navigation par boutons

Un rapport de trois pages plus deux pages de détail ne se parcourt pas à la souris : il se **pilote**.
Le fil rouge pose **4** signets, et chacun mémorise un état complet — page, filtres, visuels visibles :

| # | Signet | Ce qu'il montre |
|---|---|---|
| 1 | **Vue d'ensemble** | les visuels de la page Direction, sans filtre de magasin |
| 2 | **Focus magasin** | le même écran filtré sur le magasin choisi dans le segment |
| 3 | **Détail produit** | l'exploration ouverte depuis la matrice des familles |
| 4 | **Aide à la lecture** | la page des définitions, des exclusions et de la fraîcheur |

La navigation par boutons va avec : un bouton par page, un bouton de retour, et un bouton « aide » visible
depuis les trois pages. Un rapport navigable se reconnaît à ceci qu'un lecteur qui ne connaît ni le
modèle ni les mesures arrive à la page d'aide **sans appeler personne**.

### 5.11 Accessibilité : le rapport se lit aussi sans la couleur

L'accessibilité n'est pas une option de confort : un rapport professionnel est lu par des collègues
daltoniens, sur des écrans mal calibrés, en plein soleil, et parfois par un lecteur d'écran. Cinq
exigences, toutes vérifiables avant publication :

1. **contraste** d'au moins **4,5** pour 1 pour un texte courant, **3** pour 1 pour un grand titre ;
2. **jamais la couleur seule** : un statut porte aussi une forme, un mot ou une position ;
3. **titres de visuels explicites** — un lecteur d'écran lit le titre, pas le dessin ;
4. **ordre de tabulation** cohérent : titre, visuels dans l'ordre de lecture, source ;
5. **table de données** disponible sous les visuels qui portent un chiffre décisif.

> **Définition.** L'**accessibilité** d'un rapport est la propriété qui permet de le lire **sans** ce que
> tout le monde n'a pas : la couleur, la vue, la souris, la connaissance du modèle. Elle se vérifie avec
> le clavier et un contraste, pas avec une intention.

### 5.12 Les 6 erreurs de visuel qui se voient

Voici les **6** erreurs que le comité repère en trois secondes — chacune avec le chiffre du socle qui la
rend visible :

1. **le camembert à cinq parts** — de **11,1 %** à **34,1 %**, un classement que l'œil ne fait pas ;
2. **le classement non trié** — **3,06** entre le premier et le dernier magasin, invisible en ordre
   alphabétique ;
3. **l'axe tronqué sans mention** — **2,67** fois d'écart transformé en série de catastrophes ;
4. **la jauge plafonnée à 100 %** — un taux de **259,1 %** illisible, donc un lecteur qui doute du
   chiffre juste ;
5. **la case vide masquée** — **7** cases sur **42** effacées, et une gamme qui paraît complète ;
6. **le chiffre sans période ni unité** — **5 172 198 264** FCFA sur les douze derniers mois se confond
   avec un total historique de **15 595 154 955** FCFA.

---

## 6. Exemple concret — la page Direction, visuel par visuel

| Visuel | Question posée | Mesure | Échelle et réglage | Décision servie |
|---|---|---|---|---|
| Carte « CA net » | combien vend-on ? | `[CA net]` | **15 595 154 955** FCFA, unité FCFA | cadrer la réunion |
| Jauge « objectif » | tient-on l'objectif ? | `[CA net]` / objectif | maximum **300 %**, cible **100 %** | alerter ou rassurer |
| Barres « par magasin » | qui est devant qui ? | `[CA net]` | trié, **34,1 %** contre **11,1 %** | arbitrer les moyens |
| Courbe « par mois » | comment évolue-t-on ? | `[CA net]` | axe dès zéro, **44** mois, **2,67** fois | lire la tendance |
| Carte « taux de marge » | la marge tient-elle ? | `[Taux de marge %]` | **29,12 %**, une décimale | déclencher une analyse |

Ce tableau est le **cœur** du dossier de conception : il se relit en réunion, il se contredit rarement,
et il évite la discussion la plus coûteuse d'un projet de rapport — « ce visuel sert à quoi ? ». Les
quatre questions de la page se répondent ensuite seules : le magasin de tête fait **3,06** fois le
dernier, la marge du réseau est à **29,12 %**, et l'objectif est dépassé partout — trois constats, trois
décisions possibles.

---

## 7. Démonstration pas à pas — construire les visuels dans l'outil

L'outil n'est pas installé dans cet atelier : ces gestes se rejouent devant votre écran, et les valeurs
de contrôle sont celles mesurées sur le socle.

1. **Créez les trois pages** et nommez-les : `Direction`, `Commercial`, `Approvisionnement`. Nommez la
   page de détail `Détail` et la page d'aide `Aide à la lecture` — un nom de page est une information,
   pas un numéro.
2. **Posez la bande de contexte** sur chaque page : titre du rapport, période, magasin, fraîcheur.
3. **Créez les cartes** : champ `[CA net]` pour la page Direction, puis réglez le format en FCFA avec
   séparateur de milliers, **sans** décimale. Contrôle : **15 595 154 955** FCFA.
4. **Créez la jauge** de l'objectif : valeur `[CA net]`, cible **100 %**, maximum **300 %**. Contrôle :
   sur les huit mois de 2026, la jauge est à **259,1 %** et reste dans le cadran.
5. **Créez les barres** du chiffre d'affaires par magasin, puis ouvrez le menu du visuel et **triez** par
   la mesure, décroissant. Contrôle : la première barre est Ouaga 2000, **34,1 %** du réseau.
6. **Créez la courbe** mensuelle : axe `dim_date[date]`, mesure `[CA net]`, axe des ordonnées **démarrant
   à zéro**. Contrôle : le mois le plus faible affiche **199 549 035** FCFA, le plus fort
   **533 572 353** FCFA.
7. **Créez la matrice** magasin × famille avec `[CA net]` au centre. Contrôle : **42** cases, dont
   **35** remplies ; laissez les **7** vides blanches et écrivez la légende.
8. **Créez le nuage de points** de la page Approvisionnement : couverture en abscisse, rotation en
   ordonnée. Contrôle : la rotation du réseau vaut **9,42**.
9. **Ajoutez le visuel des retours** par mois, en pourcentage à une décimale : **1,17 %** des lignes,
   **1,91 %** des tickets — les deux définitions s'écrivent dans l'info-bulle.
10. **Créez les quatre segments** — période, magasin, famille, segment de client — et synchronisez-les
    avec les deux pages de détail, jamais avec la page d'aide.
11. **Rangez les signets** : vue d'ensemble, focus magasin, détail produit, aide à la lecture. Ajoutez un
    bouton « retour » sur les deux pages de détail.
12. **Passez la page en revue avec 6 tests** : les titres affirment, les unités sont écrites, les axes
    partent de zéro sauf mention, les vides sont expliqués, les contrastes tiennent, et la table de
    données est disponible sur les trois visuels décisifs.

---

## 8. Erreurs fréquentes

1. **Dessiner avant d'écrire la question.** Le visuel existe, personne ne sait à quoi il répond, et il
   survit parce qu'il est joli. La question s'écrit **avant** le visuel, dans le dossier.
2. **Confondre carte et carte.** La vignette d'une valeur et le visuel géographique portent le même nom
   français : dans un dossier, on précise laquelle — sans quoi deux personnes construisent deux choses.
3. **Laisser le tri par défaut.** L'outil trie par ordre alphabétique ou par ordre d'arrivée : dans les
   deux cas, le classement se perd, et **3,06** fois d'écart devient invisible.
4. **Régler un maximum « parce que c'est un pourcentage ».** Un plafond à 100 % sur un taux qui monte à
   **259,1 %** produit un visuel faux dans sa forme et juste dans son chiffre : le pire des deux mondes.
5. **Mettre un zéro à la place d'un vide.** Les **7** cases vides de la matrice deviennent des ventes
   nulles, et le lecteur cherche une rupture de stock qui n'existe pas.
6. **Publier sans regarder en noir et blanc.** Les couleurs de statut disparaissent, et avec elles le
   message — alors qu'un mot, une forme ou un signe l'aurait sauvé.

---

## 9. Bonnes pratiques professionnelles

1. **Écrivez la question avant le visuel**, et gardez-la dans la fiche du rapport : le visuel se justifie,
   la question se relit.
2. **Triez tout ce qui classe** : barres, matrices de classement, tableaux de magasins. Un tri est un
   cadeau fait au lecteur.
3. **Choisissez l'échelle à partir des valeurs** — min, max, dispersion — et notez le réglage dans le
   dossier : **163,9 %** à **329,5 %** pour le taux de réalisation.
4. **Écrivez l'unité et la période** dans le titre ou le sous-titre de chaque visuel. Un chiffre sans
   période sera comparé à un autre.
5. **Traitez les vides** par une règle unique, écrite et visible, sur tous les visuels du rapport.
6. **Limitez la palette** : sept familles, trois statuts, et rien d'autre. Une couleur qui ne porte rien
   prend la place d'une information.
7. **Testez au clavier et en noir et blanc** avant de publier : ordre de tabulation, contrastes, titres
   explicites, table de données.
8. **Faites relire la page par quelqu'un qui n'a pas construit le rapport** : la grille en **18** points
   sert exactement à cela.

> **Boîte à outils.** Pour chaque visuel, quatre contrôles : la **question** est écrite · le **tri** est
> fait · l'**échelle** est réglée sur les valeurs · l'**unité et la période** sont visibles. Quatre
> contrôles, **14** visuels, et la page se défend sans vous.

---

## 10. Exercice guidé

**Énoncé.** Un collègue publie la page Direction avec une jauge réglée entre 0 et 100 % : l'aiguille est
en butée, et le comité conclut que le rapport est faux. La mesure, elle, est juste. Rétablissez la
situation.

**Étape 1 — vérifier le chiffre.** La mesure `[CA net]` donne **3 360 553 372** FCFA sur les huit mois
de 2026, pour un objectif de **1 297 150 000** FCFA : le taux est donc bien **259,1 %**. Le chiffre n'est
pas en cause ; le réglage l'est.

**Étape 2 — mesurer la dispersion.** Avant de régler un maximum, il faut connaître les extrêmes : par
magasin et par mois, le taux va de **163,9 %** à **329,5 %**. Un cadran doit contenir le plus petit
comme le plus grand.

**Étape 3 — choisir le réglage.** Trois options : un maximum à **300 %** avec une cible à **100 %** —
une valeur au-dessus reste visible ; une barre avec un repère d'objectif ; une carte « 259,1 % » complétée
par les barres par magasin.

**Étape 4 — écrire la décision.** Le dossier note le réglage retenu, la raison, et l'alternative
écartée. Sans cette note, le réglage sera « corrigé » par le prochain lecteur — dans le mauvais sens.

**Attendu.** Le chiffre confirmé par la mesure, les deux extrêmes cités, le réglage choisi, et la
décision écrite dans le dossier de conception.

---

## 11. Exercices autonomes

**Exercice 6.1.** Les **5** magasins qui vendent et les **7** familles de produits sont disponibles.
Choisissez le type de visuel pour chacune des deux questions suivantes, et justifiez : « quels magasins
font le réseau ? » et « quelles familles dominent ? ».

**Exercice 6.2.** Un visuel affiche les retours par mois avec un axe des ordonnées allant de **1,10 %** à
**2,00 %**. Que va conclure un lecteur pressé, et que faut-il écrire ou changer ?

**Exercice 6.3.** La matrice magasin × famille montre **42** cases, dont **35** remplies. Rédigez la
légende des cases vides en une phrase, et dites pourquoi un zéro serait un contresens.

**Exercice 6.4.** Un rapport affiche **5 172 198 264** FCFA en grand, sans autre mention. Rédigez le
titre et le sous-titre qui rendent ce chiffre inexploitable autrement que dans le bon sens.

**Exercice 6.5.** Vous devez faire passer la page Commercial à un collègue daltonien. Citez les **4**
contrôles que vous ferez avant de lui montrer la page, et le résultat attendu pour chacun.

---

## 12. Correction détaillée

**Exercice 6.1.** Pour « quels magasins font le réseau ? », des **barres ordonnées** : cinq catégories,
une mesure, un classement — et le tri porte le message, du premier à **34,1 %** jusqu'au dernier à
**11,1 %**. Pour « quelles familles dominent ? », des **barres ordonnées** également, triées : sept
catégories, des valeurs de **1 056 068 339** à **3 535 582 421** FCFA. Dans les deux cas, un camembert
donnerait cinq et sept angles à comparer, ce que l'œil fait mal ; et un nuage de points ne répondrait à
aucune des deux questions, faute d'une seconde mesure à croiser.

**Exercice 6.2.** Un lecteur pressé conclura que les retours ont doublé, alors que l'amplitude réelle est
d'un point de pourcentage. Deux corrections, à faire ensemble : l'axe des ordonnées **part de zéro**
pour un taux de gestion, et le titre porte la **période** — les douze derniers mois — ainsi que la
définition employée, **1,17 %** des lignes ou **1,91 %** des tickets. Un axe tronqué n'est acceptable
que si le titre le dit et explique pourquoi.

**Exercice 6.3.** Légende possible : « une case blanche signale une famille non référencée dans ce
magasin ; aucune vente n'existe sur cette combinaison ». Un zéro serait un contresens parce qu'il
affirme une mesure — « les ventes s'annulent » — là où il n'y a aucune ligne dans les faits : **7** cases
sur **42** décriraient alors une demande insatisfaite imaginaire, et le comité chercherait une cause
commerciale à un trou de référencement.

**Exercice 6.4.** Titre : « Le réseau a vendu 5 172 198 264 FCFA sur les douze derniers mois ». Sous-titre :
« soit 33,2 % du chiffre d'affaires des 44 mois du socle, retours exclus — huit mois de 2026 inclus ».
Sans ces deux mentions, le même nombre se confond avec le total historique de **15 595 154 955** FCFA, et
la réunion débat d'un chiffre qui ne parle pas de la même période.

**Exercice 6.5.** Les quatre contrôles : **contraste** d'au moins **4,5** pour 1 entre texte et fond ;
**statuts non portés par la couleur seule** — un mot ou une forme accompagne chaque état ; **titres
explicites** de chaque visuel, pour que le dessin se raconte ; **table de données** disponible sous les
visuels décisifs. Résultat attendu : la page reste lisible sans distinguer le vert du rouge, et chaque
chiffre reste accessible sans la forme.

---

## 13. Mini-projet de chapitre — la page Direction dessinée et défendue

**Énoncé.** Produisez la **page Direction** du rapport : ses **5** visuels, leur question écrite, leur
réglage d'échelle, et la légende des vides. Livrez la page sous forme de maquette ou de capture, avec
la fiche qui l'accompagne — et défendez chaque visuel en une phrase.

**Barème indicatif** : les **5** visuels présents avec leur question nommée (**5** points) · les
réglages d'échelle justifiés par les valeurs mesurées, jauge comprise (**5** points) · la mise en page,
le thème et la charte appliqués — titres, unités, périodes, palette courte (**5** points) · la ligne
d'accessibilité et la gestion des vides écrites (**3** points) · sur **18** points.

> **Pourquoi ce mini-projet.** Parce qu'une page se défend visuel par visuel, et que la question la plus
> fréquente d'un comité n'est pas « comment as-tu fait ce graphique » mais « pourquoi celui-là ». Une
> page qui répond à cette question en une phrase par visuel est une page publiée ; les autres reviennent
> en réunion.

---

## 14. Résumé du chapitre

| Notion | Mesure du module | Ce qu'elle enseigne |
|---|---|---|
| Les trois pages | **14** visuels : 5 + 5 + 4 | une page sert une décision, pas un service |
| Les barres et le tri | **34,1 %** contre **11,1 %**, rapport **3,06** | le classement fait la moitié du message |
| La courbe et l'axe | **44** mois, **199 549 035** à **533 572 353** FCFA (**2,67**) | une échelle tronquée raconte une autre histoire |
| La matrice | **42** cases, **35** remplies, **7** vides | un vide s'explique, il ne se masque pas |
| La jauge | **259,1 %**, de **163,9 %** à **329,5 %** | le maximum vient des données |
| La carte géographique | **4** villes, dont **56,0 %** à Ouagadougou | le visuel écarté se justifie aussi, chiffres à l'appui |
| Les cartes (vignettes) | **15 595 154 955** FCFA, puis **5 172 198 264** sur 12 mois | une carte cadre, elle ne classe pas |
| Accessibilité | contraste **4,5** pour 1, **4** signets | un rapport se lit sans la couleur |

**Instrument.** `python3 tools/mesures_M14.py` recalcule les parts des magasins, les valeurs extrêmes des
familles et des mois, les cases de la matrice, le taux de réalisation et sa dispersion, et le poids des
douze derniers mois. Les gestes de construction, eux, se rejouent devant votre écran.

**Le module en une ligne.** Les cinq chapitres précédents ont posé l'outil, la donnée, sa transformation,
le modèle et les mesures ; celui-ci a décidé **ce que le lecteur voit** — et il a montré qu'un visuel se
choisit comme une phrase se construit : une question, un sujet, un chiffre, une unité, une période.

---

## 15. À retenir

1. **La question précède le visuel.** Les **14** visuels du rapport portent chacun une phrase écrite dans
   le dossier ; un visuel sans question est une place prise.
2. **Le tri et l'échelle portent le message.** **34,1 %** contre **11,1 %** en barres triées,
   **199 549 035** à **533 572 353** FCFA sur un axe qui part de zéro : deux réglages, deux constats
   immédiats.
3. **Un cadran a un maximum, et ce maximum vient des données.** **259,1 %** de réalisation, de
   **163,9 %** à **329,5 %** selon le magasin et le mois : le réglage par défaut n'aurait pas tenu.

> **À retenir.** Un rapport ne vaut pas par ce qu'il montre mais par ce qu'il fait décider. Écrire la
> question d'un visuel prend trente secondes ; la relire en réunion prend une phrase ; ne pas l'écrire
> coûte une réunion entière.

---

## 16. Évaluation formative

1. Combien de visuels portent les trois pages du rapport, et comment se répartissent-ils ?
2. Citez les quatre questions qui décident du type de visuel, avec un visuel du rapport pour chacune.
3. Pourquoi les barres du rapport sont-elles triées, et quel rapport chiffré le justifie ?
4. Que se passe-t-il si l'axe d'une courbe de chiffre d'affaires ne part pas de zéro ?
5. Combien de cases compte la matrice magasin × famille, et que signifient les cases vides ?
6. Pourquoi une jauge graduée de 0 à 100 % est-elle inutilisable sur ce rapport ?
7. Quelles sont les trois informations minimales d'une carte — vignette ?
8. Dans quels cas un camembert reste-t-il défendable ?
9. Citez quatre exigences d'accessibilité et la valeur de contraste attendue.
10. Que porte une page d'aide, et pourquoi n'affiche-t-elle aucune donnée ?

**Corrigé.** 1. **14** visuels : **5** pour la page Direction, **5** pour la page Commercial, **4** pour
la page Approvisionnement — auxquels s'ajoutent deux pages de détail et une page d'aide. 2. « combien, en
tout ? » — la carte du chiffre d'affaires net · « qui est devant qui ? » — les barres par magasin ·
« comment cela évolue-t-il ? » — la courbe mensuelle · « deux mesures sont-elles liées ? » — le nuage
couverture × rotation. 3. Parce que le classement porte le message : le premier magasin fait **3,06** fois
le dernier, et l'ordre alphabétique disperse cette hiérarchie. 4. Chaque variation mensuelle est
exagérée : la série couvre **44** mois et va de **199 549 035** à **533 572 353** FCFA, un rapport de
**2,67** que l'axe tronqué transforme en succession d'incidents. 5. **42** cases — 6 magasins fois
7 familles — dont **35** remplies ; les **7** vides signalent une famille non référencée dans ce
magasin. 6. Parce que le taux de réalisation vaut **259,1 %** sur les huit mois de 2026 et va de
**163,9 %** à **329,5 %** : l'aiguille est en butée, et le lecteur doute d'un chiffre juste. 7. La
mesure, l'unité et la période — une carte affiche **une** valeur, cadrée, jamais un comparatif.
8. À **deux parts** seulement, ou pour une part contre un tout que le lecteur n'a pas à comparer :
« 56,0 % à Ouagadougou ». 9. Contraste d'au moins **4,5** pour 1 pour le texte courant, statut jamais
porté par la couleur seule, titres explicites pour la lecture vocale, ordre de tabulation cohérent, et
une table de données sous les visuels décisifs — quatre de ces cinq suffisent à la réponse. 10. Les
définitions des indicateurs, les exclusions — retours, dépôt — et la fraîcheur de l'actualisation :
aucune donnée, parce qu'une page d'aide qui affiche des chiffres devient une page de rapport de plus.
