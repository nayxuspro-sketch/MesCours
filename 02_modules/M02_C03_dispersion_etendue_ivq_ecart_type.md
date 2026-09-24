# M02.C03 — Mesurer la dispersion : étendue, intervalle interquartiles, écart-type

> **L'idée du chapitre.** Deux séries peuvent avoir la même moyenne et n'avoir rien de commun. La dispersion est ce
> qui les sépare dans une note, et c'est elle — pas le centre — qui décide si un indicateur est utilisable pour
> négocier, alerter ou comparer.

> **Base de travail — obligatoire.** Deux fichiers du socle, dans votre dossier `02_exercices/M02/`, ouverts côte à
> côte : `donnees/projection/ventes_magasin5_2025.csv` (l'énoncé, 489 lignes × 13 variables) et
> `donnees/reference/ventes_magasin5_2025_ATTENDU.csv` (480 × 13). Séparateur point-virgule, encodage UTF-8, virgule
> décimale. Montants en franc CFA (FCFA). Tous les chiffres cités sont lus sur l'attendu, au niveau de la ligne
> (480 lignes) et du panier (316 tickets), et figurent dans
> `01_socle_donnees/data/reference/chiffres_cites.md`, section M02.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous êtes capable de :

1. calculer et comparer les trois dispersions usuelles — étendue, intervalle interquartiles, écart-type — sur la
   même série, et dire laquelle répond à quelle question ;
2. expliquer pourquoi l'écart-type d'une série d'entiers s'écrit avec des décimales alors qu'aucune valeur ne les
   contient ;
3. choisir entre écart-type et coefficient de variation pour comparer la variabilité de deux colonnes qui n'ont
   pas la même échelle ;
4. estimer la précision d'une moyenne grâce à l'erreur type, et dire si un écart entre deux vendeurs mérite une
   réunion ;
5. décider, chiffres à l'appui, si une catégorie de produits est assez stable pour être pilotée sur sa moyenne ;
6. rédiger une note de dispersion qui ne laisse pas le lecteur deviner de quoi l'on parle.

## 2. Pourquoi cette notion est importante

Un indicateur sans dispersion est une décision prise à l'aveugle. Trois situations du module le montrent, toutes
chiffrées plus bas dans ce chapitre :

- **La négociation.** « Le montant moyen d'une ligne de Bois & panneaux est de 201 865 FCFA, accordons 5 % ». Si
  l'écart-type de la catégorie vaut 318 080 FCFA, la moyenne ne décrit rien : la remise porte sur un chiffre qui
  n'existe pas.
- **L'alerte.** Le contrôle de gestion veut être prévenu quand un ticket sort de l'ordinaire. Le seuil retenu change
  tout : à une fois et demie l'écart interquartiles, il vaut 295 445 FCFA et signale 25 tickets ; à deux
  écarts-types, il ne signale qu'une douzaine de tickets et laisse filer tout le reste.
- **Le classement.** L'écart de panier moyen entre les deux vendeurs les plus éloignés des quatre principaux vaut
  34 014 FCFA. Sans erreur type, c'est un classement ; avec elle (10 244 FCFA), c'est une comparaison qui tient ou
  qui tombe.

> **Dans les faits.** Le vocabulaire de la dispersion est le premier endroit où un non-statisticien est disqualifié
> en réunion, souvent injustement. Deux réflexes vous mettent à l'abri : ne jamais prononcer un écart-type sans la
> moyenne qui l'accompagne, et ne jamais parler de « variance » à l'oral — dites « écart-type », tout le monde voit
> de quoi il retourne, et vous aussi.

## 3. Explication simple

Imaginez deux caisses du magasin. À la première, dix clients paient des tickets tous proches de 60 000 FCFA. À la
seconde, dix clients encore : cinq paient 5 000 FCFA, cinq paient 115 000 FCFA. Les deux files ont la même moyenne.
La première est réglée, la seconde est un tirage.

La dispersion est exactement ce qui distingue les deux files, et elle répond à une question unique : **les valeurs
sont-elles serrées autour du centre, ou étalées ?** Trois manières de le mesurer, de la plus naïve à la plus utile :

- **l'étendue** regarde les deux bouts — 1 494 470 FCFA sur nos tickets : vrai, et inutile ;
- **l'intervalle interquartiles (IQR)** regarde la moitié du milieu — 109 924 FCFA, et résiste aux extrêmes ;
- **l'écart-type** regarde toutes les valeurs, chacune comptant pour sa distance au centre — 182 095 FCFA, et
  sert de matière première à tout le reste du module.

Le mot « dispersion » recouvre donc trois chiffres très différents. En anglais *spread*, *dispersion*,
*variability* : le concept est le même, et le mot employé dépend du logiciel plus que du théorème.

## 4. Vocabulaire essentiel

| # | Terme | Français — English — sens simple | À savoir |
|---|---|---|---|
| 1 | Étendue | étendue — *range* — plus grande valeur moins plus petite | deux lignes du fichier décident de tout |
| 2 | IQR | intervalle interquartiles — *interquartile range* — Q3 moins Q1 | « écart interquartile » en français |
| 3 | Variance | variance — *variance* — moyenne des carrés des écarts | unité au carré, donc peu lisible |
| 4 | Écart-type | écart-type — *standard deviation* — racine carrée de la variance | σ pour une population, *s* pour un échantillon |
| 5 | CV | coefficient de variation — *coefficient of variation* — écart-type divisé par la moyenne | sans unité, seul comparable entre colonnes |
| 6 | Erreur type | erreur type de la moyenne — *standard error* (SE) — écart-type divisé par racine de *n* | précision d'un indicateur, pas diversité des clients |
| 7 | MAD | écart absolu médian — *median absolute deviation* — médiane des écarts à la médiane | robuste, absente des tableurs |
| 8 | Moyenne tronquée | moyenne tronquée — *trimmed mean* — moyenne après retrait des extrêmes | change le périmètre, pas le calcul |
| 9 | Bornes de Tukey | bornes de Tukey — *Tukey fences* — Q1 − 1,5 × IQR et Q3 + 1,5 × IQR | définit l'extraordinaire sans le subir |
| 10 | Degré de liberté | degré de liberté — *degree of freedom* — valeurs libres après estimation | explique le *n* − 1 de la variance |
| 11 | Hétérogénéité | hétérogénéité — *heterogeneity* — mélange de populations dans un même chiffre | le vrai danger, pas la variance |

## 5. Cours approfondi

### 5.1 Trois dispersions, trois usages

> **Définition.** L'**étendue** (*range*) est la différence entre maximum et minimum. L'**intervalle
> interquartiles** (*IQR*) est la différence entre le troisième et le premier quartile. L'**écart-type** est la
> racine carrée de la **variance**, moyenne des carrés des écarts à la moyenne. Les deux premières se lisent sur la
> distribution, la troisième sur toutes les valeurs à la fois.

| Dispersion | Sur les paniers (316) | Sur les lignes (480) | Ce qu'elle autorise à dire |
|---|---|---|---|
| Étendue | 1 494 470 FCFA | 1 380 482 FCFA | « du pire au meilleur ticket » — exact, non décisionnel |
| IQR | 109 924 FCFA | à calculer à l'exercice 3.1 | « la moitié du milieu tient dans… » |
| Écart-type | 182 095 FCFA | 143 915 FCFA | « un ticket s'écarte typiquement de… » |
| CV | 159,5 % | 191,5 % | « la moyenne ne décrit pas la série » |

Sur 316 valeurs très asymétriques, l'écart-type dépasse nettement l'IQR (rapport de 1,7) : c'est la signature
arithmétique de l'asymétrie, que M02.C05 confirmera graphiquement. L'étendue, elle, vaut plus de treize fois l'IQR
(rapport mesuré : 13,6) — les 300 tickets du centre tiennent dans un espace treize fois plus petit que celui que la
série occupe au total.

**Faites-le dans un tableur.** Sur la colonne des paniers : `=MAX(plage)-MIN(plage)` pour l'étendue,
`=QUARTILE.INC(plage;3)-QUARTILE.INC(plage;1)` pour l'IQR, `=ECARTYPE.STANDARD(plage)` pour l'écart-type. La
fonction s'appelle `STDEV.S` en anglais, `ECARTYPE.STANDARD` en français ; la variante `ECARTYPEP` (*STDEV.P*)
suppose que vous tenez la population entière. Gardez la version échantillon : vous travaillez sur un extrait de
0,23 % du fichier du magasin.

> **Attention.** Une étendue est une information sur deux lignes. Un seul ticket à 1 343 666 FCFA ou un seul avoir
> à -150 804 FCFA la change, sans que personne d'autre n'ait changé de comportement. C'est la plus sensible des
> trois dispersions à l'erreur de saisie, donc la moins bonne candidate à un seuil d'alerte.

### 5.2 D'où vient l'écart-type, et pourquoi il a des décimales

Quatre pas, tous faisables à la main sur dix lignes :

1. écart de chaque valeur à la moyenne : xᵢ − moyenne ;
2. carré de cet écart ;
3. somme des carrés divisée par *n* − 1 → la **variance** ;
4. racine carrée de la variance → l'**écart-type**.

Sur les 316 paniers, la variance vaut 33 158 631 393 — des FCFA au carré, unité qui n'existe pas dans la nature —
et sa racine carrée 182 095 FCFA. Le passage par les carrés explique deux choses. D'abord la **sensibilité** : un
ticket de 1 343 666 FCFA pèse sur la variance proportionnellement au carré de son écart, donc des milliers de fois
plus qu'un ticket ordinaire. Ensuite le **format** : extraire une racine carrée produit des décimales, même quand
les données sont des entiers — la dispersion d'une série d'entiers n'a aucune raison d'être un entier.

**Faites-le dans un tableur**, en trois colonnes, pour voir le mécanisme plutôt que le résultat : écart en `A2`
par `=B2-MOYENNE(panier)`, carré en `C2` par `=A2^2`, variance par `=SOMME(C2:C317)/(NB(B2:B317)-1)`, écart-type
par `=RACINE()` du résultat. Vous venez de reconstituer `VAR.S` et `ECARTYPE.STANDARD` : comparez, vous devez
retrouver 182 095 au franc près.

Le dénominateur *n* − 1 mérite deux phrases. Il s'appelle le **degré de liberté** (*degree of freedom*) : une
valeur sur 316 a déjà servi, la moyenne, et n'est plus libre. On divise par *n* − 1 quand la moyenne a été calculée
sur le même échantillon ; sans cette correction, la variance serait systématiquement trop petite. Sur 316 lignes,
l'écart entre les deux conventions vaut un facteur de 1,0016 : négligeable en valeur, décisif en cohérence — tout
le module raisonne en échantillon, y compris le test du chapitre M02.C08.

### 5.3 L'IQR et la règle des 1,5 : une borne qui résiste à ce qu'elle détecte

> **Définition.** Les **bornes de Tukey** (*Tukey fences*, « moustaches » ou limites externes en français) sont
> Q1 − 1,5 × IQR et Q3 + 1,5 × IQR. Une valeur est dite **aberrante au sens de Tukey** si elle les franchit. Le
> coefficient 1,5 est une convention, pas une loi : on le porte à 3,0 pour ne signaler que l'exceptionnel.

Sur les paniers : Q1 = 20 635, Q3 = 130 559, IQR = 109 924, et 1,5 × IQR = 164 886. La borne haute vaut donc
295 445 FCFA, la borne basse -144 251 FCFA. Vingt-cinq tickets franchissent la haute ; un seul franchit la basse,
et c'est le retour de 150 804 FCFA rencontré au chapitre M02.C02.

Comparez avec une borne « à deux écarts-types », soit ±364 190 FCFA autour de la moyenne. D'un côté la borne basse
descend bien au-dessous de tout ce que le fichier contient — la règle ne signale jamais rien en bas ; de l'autre la
borne haute ne rattrape qu'une douzaine de tickets et laisse filer les autres. Voilà, en deux lignes de calcul,
pourquoi une borne de détection doit être bâtie sur un indicateur robuste : une règle qui intègre les détectés dans
son calcul se laisse fixer par eux.

**Faites-le dans le SQL.** *(les vues `lignes_ventes` et `paniers` ont été créées au C02, § « Pour la suite du module »)* :

```sql
WITH q AS (
  SELECT percentile_cont(0.25) WITHIN GROUP (ORDER BY panier) AS q1,
         percentile_cont(0.75) WITHIN GROUP (ORDER BY panier) AS q3
  FROM paniers
)
SELECT ROUND(q1 - 1.5 * (q3 - q1)) AS borne_basse,
       ROUND(q3 + 1.5 * (q3 - q1)) AS borne_haute,
       q3 - q1                     AS iqr
FROM q;
```

> **Conseil professionnel.** Une borne basse négative sur des montants est un diagnostic, pas un résultat : elle
> dit que la série est si large que rien ne peut y être « anormalement petit ». Dites-le en réunion — « aucune
> alerte possible en bas » — plutôt que de supprimer la borne ou de la plaquer à zéro en silence.

### 5.4 Comparer deux colonnes : le coefficient de variation

> **Définition.** Le **coefficient de variation** (*CV*, coefficient of variation) est l'écart-type divisé par la
> moyenne, exprimé en pourcentage. Il est sans unité, donc comparable entre séries d'échelles différentes ; il n'a
> aucun sens si la moyenne est proche de zéro, ni sur une grandeur sans rapport (un code client, une température en
> Celsius).

| Série | Moyenne | Écart-type | CV | Lecture |
|---|---|---|---|---|
| Panier (316 tickets) | 114 156 FCFA | 182 095 FCFA | 159,5 % | dispersion très supérieure au centre |
| Montant par ligne (480 lignes) | 75 152 FCFA | 143 915 FCFA | 191,5 % | plus large encore |
| Pièces par ligne (480 lignes) | 7 | 8,4 | 119,7 % | même nature de désordre |

Les trois CV dépassent 100 %. Ce n'est pas une anomalie de l'extrait : c'est la nature d'un commerce de matériaux,
où une commande de chantier côtoie trois achats de vis. La grille de lecture d'usage — une convention d'équipe, pas
un théorème : CV inférieur à 15 %, série stable, la moyenne se suffit ; de 15 à 30 %, moyenne utile à accompagner de
l'écart-type ; au-delà de 50 %, la moyenne seule ne décrit plus rien, il faut montrer la distribution (M02.C05).

### 5.5 Par catégorie : où la moyenne est-elle descriptive ?

Voici le tableau qu'un acheteur réclame, et celui qui clôt une discussion. Sur les lignes, par CV croissant, avec
l'effectif de chaque catégorie :

| Catégorie | Lignes | Moyenne (FCFA) | Écart-type (FCFA) | CV |
|---|---|---|---|---|
| Peinture | 34 | 86 422 | 70 320 | 81,4 % |
| Consommables | 57 | 43 877 | 45 130 | 102,9 % |
| Matériaux | 143 | 45 590 | 49 286 | 108,1 % |
| Quincaillerie | 112 | 37 528 | 45 358 | 120,9 % |
| Bois & panneaux | 24 | 201 865 | 318 080 | 157,6 % |
| Plomberie | 57 | 153 596 | 247 146 | 160,9 % |
| Electricité | 53 | 119 088 | 202 897 | 170,4 % |

Trois lectures professionnelles :

1. **Peinture contre Electricité** : des moyennes proches (86 422 et 119 088 FCFA), des écarts-types sans rapport
   (70 320 contre 202 897 FCFA). Piloter ces deux rayons avec le même indicateur, c'est piloter mal le second.
2. **Consommables contre Quincaillerie** : des écarts-types presque identiques (45 130 et 45 358 FCFA) mais des CV
   différents (102,9 % contre 120,9 %), parce que les niveaux diffèrent. Cas d'école de l'écart-type qui ment et du
   CV qui dit vrai.
3. **Bois & panneaux** : 24 lignes, une moyenne de 201 865 FCFA, un CV de 157,6 %. Chiffre peu descriptif et peu
   précis : deux raisons de ne pas négocier dessus.

**Faites-le dans le SQL.** *(les vues `lignes_ventes` et `paniers` ont été créées au C02, § « Pour la suite du module »)* :

```sql
SELECT categorie,
       COUNT(*)                                        AS lignes,
       ROUND(AVG(montant_ttc))                         AS moyenne,
       ROUND(STDDEV_SAMP(montant_ttc))                 AS ecart_type,
       ROUND(100.0 * STDDEV_SAMP(montant_ttc)
             / NULLIF(AVG(montant_ttc), 0), 1)         AS cv_pct
FROM lignes_ventes
GROUP BY categorie
ORDER BY cv_pct DESC;
```

Le `NULLIF` n'est pas un ornement : sans lui, une catégorie vide ou de moyenne nulle fait échouer la requête
entière, et six lignes justes ne servent à rien si la septième plante le calcul.

### 5.6 L'erreur type : de combien votre moyenne est-elle fausse ?

> **Définition.** L'**erreur type de la moyenne** (*standard error of the mean*, SE) est l'écart-type divisé par la
> racine carrée de l'effectif. Elle ne décrit pas la diversité des clients : elle décrit votre ignorance de la
> moyenne, c'est-à-dire de combien une autre collecte vous aurait donné un autre chiffre.

Pour les paniers : 10 244 FCFA, soit 9,0 % de la moyenne de 114 156 FCFA. La phrase à tenir en réunion : « notre
panier moyen est de 114 156 FCFA, précis d'environ deux fois 10 244 FCFA au niveau de confiance usuel de 95 % ».
Un écart de 5 000 FCFA entre deux vendeurs est du bruit ; un écart de 40 000 FCFA commence à être une information ;
l'écart maximal observé entre les quatre vendeurs de l'extrait, 34 014 FCFA, est en zone intermédiaire — le
chapitre M02.C08 tranche cette question par un test, et la tranche en faveur du doute.

Notez le comportement de la formule : la précision progresse comme la racine de l'effectif, donc pour diviser
l'erreur type par deux il faut quadrupler le nombre de tickets. C'est la phrase à prononcer quand un collègue
réclame « encore un mois de données » pour arbitrer un écart de 2 %.

**Faites-le dans un tableur** : `=ECARTYPE.STANDARD(plage)/RACINE(NB(plage))`. **En pandas** :
`s["montant_ttc"].std(ddof=1) / np.sqrt(len(s))`. Une formule, trois outils, un effet immédiat sur la qualité des
discussions : à ce stade du manuel, c'est l'indicateur au meilleur rapport effort-utilité.

> **Attention.** Erreur type et écart-type se calculent avec la même fonction selon les logiciels, se notent tous
> deux en « ± », et se confondent couramment dans les tableaux de bord. Multiplier l'erreur type par 1,96 donne un
> intervalle de confiance sur la moyenne ; multiplier l'écart-type par 1,96 donne un intervalle où se trouve 95 %
> des clients. Deux phrases entièrement différentes, deux décisions opposées.

### 5.7 Deux dispersions robustes, et ce que leur écart apprend

> **Définition.** L'**écart absolu médian** (*MAD*, median absolute deviation) est la médiane des valeurs absolues
> des écarts à la médiane. Dispersion entièrement robuste : aucune valeur extrême ne peut la déplacer, puisqu'elle
> est elle-même un ordre statistique.

Sur nos paniers, la MAD vaut 43 372 FCFA contre 182 095 FCFA à l'écart-type : l'écart entre les deux *est* le
diagnostic. Une MAD au quart de l'écart-type annonce une série tenue par quelques valeurs. Le tableur ne la
connaît pas ; trois colonnes suffisent, `=ABS(valeur-MEDIANE(plage))` puis `=MEDIANE()` sur la colonne obtenue.

Second garde-fou, la **moyenne tronquée** (*trimmed mean*) : on retire les 25 tickets hors borne haute et le CV
tombe de 159,5 % à 96,6 %. Le niveau reste élevé mais devient descriptible ; la médiane, elle, ne bouge que de
quelques milliers de francs (58 423 contre 54 044 FCFA). Règle de lecture : un indicateur qui se stabilise
fortement quand on retire quelques lignes est *tenu* par ces lignes — et cela s'écrit dans la note.

Sur les quantités, le même raisonnement donne 7 pièces en moyenne, 4 au centre, un écart-type de 8,4 (CV 119,7 %)
et une amplitude de 81 — de -13 à 68 dans le fichier nettoyé, de -13 à 14 000 dans l'énoncé, avant correction des
7 lignes multipliées par mille. Le seul énoncé de ces nombres suffit à dire que `quantite` ne se prête à aucune
prévision en l'état : c'est une affaire de dispersion, pas de moyenne.

### 5.8 Quel outil pour quelle dispersion

| Situation | Outil recommandé | Pourquoi | Ce qu'on évite |
|---|---|---|---|
| CV et écart-type par catégorie, sur 480 lignes | SQL (`GROUP BY` + `STDDEV_SAMP`) | un bloc pour moyenne, écart-type, CV, effectifs | sept tableaux croisés recopiés à la main |
| Vérification pédagogique du calcul | tableur, colonnes intermédiaires | on voit les carrés, on comprend la variance | la calculette : le résultat sans le chemin |
| MAD, moyenne tronquée | tableur ou pandas | le tableur n'a pas de fonction dédiée, pandas si | tout recalculer à la main sur 316 lignes |
| Erreur type d'une moyenne | les trois | une formule, effet immédiat | conclure sans elle |
| Seuil d'alerte publié | tableur puis SQL | bornes lisibles et rejouables | une borne bâtie sur l'écart-type, contaminée |
| Indicateur de dispersion en diffusion | Power BI ou équivalent, plus tard | le lecteur a besoin du contexte du grain | l'export d'un tableau de valeurs brutes |

**Pourquoi pas un outil de BI dès maintenant ?** Vous publierez ces mesures dans un tableau de bord — *dashboard*, dans le jargon — au
module M06, et ce sera le bon endroit. Mais un indicateur de dispersion diffusé sans sélecteur de grain ni légende
se lit comme une anomalie : le lecteur ne sait jamais si l'écart-type qu'il voit décrit les clients, les tickets ou
les lignes. À l'étape de préparation, le tableur ou le SQL obligent à nommer le grain — c'est pour cela qu'on y
reste.

> **Boîte à outils.** Le contrôle minimal de toute mesure de dispersion : (1) l'effectif utilisé s'écrit à côté de
> l'indicateur — *n* = 316 pour les paniers, 480 pour les lignes, jamais « nos données » ; (2) l'écart-type doit
> être plus grand que la MAD et plus petit que l'étendue, sinon vous avez publié une variance ou un écart-type de
> population sans le vouloir ; (3) un CV supérieur à 100 % s'accompagne d'une phrase sur la nature de la série,
> sinon l'interlocuteur entendra « erreur de données » ; (4) si la dispersion est calculée après nettoyage,
> avant/après en deux colonnes, jamais l'une sans l'autre.

## 6. Exemple concret : négocier le bois de chauffage, ou non

**La demande.** Le responsable des achats hésite à accorder une remise annuelle à un fournisseur de bois et
panneaux, sur la foi d'un montant moyen de 201 865 FCFA par ligne. Sa question réelle : « ce niveau est-il assez
stable pour que je négocie dessus ? »

**Ce que dit le calcul.**

| Élément | Valeur | Interprétation |
|---|---|---|
| Lignes de la catégorie | 24 | trop peu pour une moyenne contractuelle |
| Moyenne | 201 865 FCFA | le chiffre avancé en négociation |
| Médiane | 77 904 FCFA | la ligne typique vaut un quart de la moyenne |
| Écart-type | 318 080 FCFA | la dispersion dépasse le centre |
| CV | 157,6 % | hors de toute zone négociable sur la moyenne |

**La décision.** On ne négocie pas sur la moyenne de la catégorie. On négocie une **remise par gamme** (ciments,
panneaux, bois de charpente séparément) ou un plafond de remise par commande : dans les deux cas l'indicateur de
pilotage devient la médiane par gamme, pas la moyenne par catégorie. Le tableau tient en une page, sans test
statistique, et il évite un contrat mal calibré.

**La phrase à écrire dans la note.** « La catégorie Bois & panneaux de l'extrait compte 24 lignes, une moyenne de
201 865 FCFA et une médiane de 77 904 FCFA ; l'écart-type (318 080 FCFA) excède la moyenne. Une remise assise sur
la moyenne catégorie serait versée sur des lignes qui ne lui ressemblent pas. Nous recommandons de conduire la
négociation par gamme, avec la médiane de chaque gamme pour base. »

## 7. Démonstration pas à pas : les trois dispersions, trois outils, un contrôle

**Point de départ.** Fiche `donnees/reference/ventes_magasin5_2025_ATTENDU.csv` ouverte dans le tableur : 480 lignes
de données, lignes 2 à 481, colonne `montant_ttc` en `I`.

**Étape 1 — Le bon effectif.** `=NB(I2:I481)` doit renvoyer 480. Si vous obtenez 478 ou moins, des valeurs texte
se sont glissées dans la colonne et la dispersion portera sur un sous-ensemble — c'est l'erreur du chapitre
M01.C04, rejouée.

**Étape 2 — L'étendue.** `=MAX(I2:I481)-MIN(I2:I481)` → 1 380 482 FCFA, entre le maximum de 1 229 678 FCFA et le
minimum de -150 804 FCFA. Écrivez les deux bornes à côté du résultat : une étendue sans ses deux termes est
invérifiable par un tiers.

**Étape 3 — L'IQR et les bornes.** `=QUARTILE.INC(I2:I481;1)` et `=QUARTILE.INC(I2:I481;3)`, leur différence, puis
les bornes à 1,5 × IQR. Contrôle de cohérence : l'IQR d'une colonne de montants doit rester inférieur à son
écart-type ; si l'inverse se produit, vous comparez deux colonnes différentes.

**Étape 4 — L'écart-type par la voie longue.** Colonnes intermédiaires comme au §5.2, sur les paniers : variance
33 158 631 393, écart-type 182 095. Comparez à `=ECARTYPE.STANDARD()` : au franc près c'est bon ; sinon vous avez
divisé par *n* au lieu de *n* − 1.

**Étape 5 — L'erreur type.** `=ECARTYPE.STANDARD(plage_paniers)/RACINE(NB(plage_paniers))` → 10 244 FCFA. Écrivez
la phrase complète dans votre journal de travail, avec les trois nombres.

**Étape 6 — Rejouer en SQL, puis en pandas.** Reprenez la requête du §5.5 : le CV de Plomberie doit ressortir à
160,9 %.

```python
pan = df.groupby("n_ticket")["montant_ttc"].sum().rename("panier")
stat = pan.agg(["count", "mean", "median", "std", "min", "max"])
cv = 100 * stat["std"] / stat["mean"]
se = stat["std"] / np.sqrt(stat["count"])
q1, q3 = pan.quantile([0.25, 0.75])
borne_haute = q3 + 1.5 * (q3 - q1)
n_hors = int((pan > borne_haute).sum())
```

Dernière ligne : 25. Si vous obtenez 24 ou 26, c'est la borne ou le comparateur qui n'est pas le bon — strict
contre inclus est la cause la plus fréquente de cet écart d'une unité.

**Contrôles qualité du chapitre.**

| # | Contrôle | Seuil | Résultat attendu | Si échec |
|---|---|---|---|---|
| 1 | Écart-type des paniers recompté par la voie des carrés | ±1 FCFA | 182 095 | dénominateur *n* − 1 oublié |
| 2 | CV des lignes recompté | 0,1 point | 191,5 % | arrondis d'affichage |
| 3 | Effectif hors borne haute de Tukey, par filtre | identité | 25 tickets | opérateur de comparaison |
| 4 | Couverture du tableau §5.5 | 7 catégories, 480 lignes | 7 / 480 | une catégorie sans ligne est restée |
| 5 | Ordre MAD < écart-type < étendue | les trois inégalités | 43 372 · 182 095 · 1 494 470 | indicateur mal identifié |

## 8. Erreurs fréquentes

1. **Comparer des écart-types entre colonnes d'échelles différentes.** « La quantité varie moins que le montant :
   8,4 contre 143 915. » Les CV sont de 119,7 % et 191,5 % : la conclusion est juste, l'argument était faux — et il
   eût été faux en sens inverse. Règle réflexe : jamais un écart-type sans sa moyenne.
2. **Confondre écart-type et erreur type** (§5.6) : mêmes fonctions, mêmes noms selon le logiciel, même signe « ± ».
3. **Choisir `ECARTYPEP` par principe.** L'écart est minime sur 316 tickets, mais l'incohérence se propage à tout le
   module, qui raisonne en échantillon.
4. **Publier un CV de 191,5 % en rouge comme une anomalie.** C'est la nature du commerce de matériaux : un CV élevé
   se commente, il ne se signale pas — sauf référence métier explicite.
5. **Recalculer les bornes de Tukey après avoir retiré les valeurs extrêmes.** On détruit le bénéfice : la borne se
   calcule sur la série complète puis s'applique. Si vous écarter 25 tickets, énoncez la règle avant.
6. **Lire « 68 % des valeurs dans l'intervalle moyenne ± écart-type ».** Cette lecture suppose une distribution
   approximativement symétrique, ce que M02.C05 montre faux ici : sur 316 tickets asymétriques, l'intervalle ne
   couvre pas 68 % de la série.

## 9. Bonnes pratiques professionnelles

1. **Toujours deux dispersions, jamais une** : l'IQR pour borner, l'écart-type ou le CV pour comparer. Celui qui
   n'en cite qu'une se fait surprendre par la question suivante.
2. **Écrire l'effectif à côté de l'indicateur.** « CV de 159,5 % (316 tickets) » n'a pas la même valeur que
   « CV de 159,5 % (24 lignes) » : dans le second cas, le chiffre est incertain.
3. **Nommer le périmètre de nettoyage.** Un CV sur la série complète et un CV après retrait des 8 lignes de retours
   (-283 933 FCFA) sont deux chiffres corrects : le lecteur doit savoir lequel il a sous les yeux.
4. **Transformer l'indicateur en décision explicite.** « CV de 157,6 % → pas de remise assise sur la moyenne
   catégorie » : une dispersion qui ne change aucun comportement n'est qu'un chiffre de plus.
5. **Prévenir, pas punir.** Un seuil d'alerte sert à regarder, pas à noter un vendeur. Le premier usage d'une borne
   de Tukey en entreprise est d'ouvrir une enquête, presque jamais de fermer un compte.
6. **Conserver la requête de dispersion en annexe.** Dix lignes, rejouables : c'est elles qui vous feront gagner la
   réunion de l'année prochaine.

## 10. Exercice guidé — trois dispersions sur la colonne des prix

**Énoncé.** Sur la colonne `prix_unitaire_ht` du fichier attendu (480 lignes), calculez étendue, IQR, écart-type,
puis CV, et concluez en deux lignes sur l'usage de la moyenne de prix en négociation.

**Vous faites** — barème 10 points, total 10.

| Étape | Ce que vous produisez | Points |
|---|---|---|
| A | Effectif et unité (480 lignes, FCFA) écrits en tête | 1 |
| B | Étendue, avec ses deux termes | 2 |
| C | IQR, et bornes de Tukey qui en découlent | 2 |
| D | Écart-type et CV, avec la moyenne à côté | 3 |
| E | Conclusion en deux lignes, un usage décidé | 2 |

**Nous vérifions.** Les bornes du prix unitaire sont 675 et 40 550 FCFA : deux extrêmes plausibles dans un catalogue
de quincaillerie, à confronter au fichier fournisseur (M01.C06) avant d'en faire un argument. La moyenne de la
colonne ne décrit pas le catalogue, elle décrit son arithmétique : ce qu'on en peut tirer n'est pas « le prix moyen
est de tant » mais « la moitié du catalogue tient dans telle plage » — c'est l'IQR qui répond, et c'est lui qui se
négocie.

**Nous corrigeons.** Deux erreurs classiques : comparer ce CV à celui d'une autre colonne sans dire que les grains
diffèrent (prix par produit contre montant par ligne) ; proposer de « supprimer les produits à prix aberrants »
avant d'avoir regardé ce qu'ils vendent réellement.

## 11. Exercices autonomes

**Exercice 3.1 (★) — Les trois dispersions, une par une.** Sur les montants **par ligne** (480 lignes), calculez
étendue, IQR, écart-type et CV. *(attendu : étendue 1 380 482 FCFA, écart-type 143 915 FCFA, CV 191,5 %)*

**Exercice 3.2 (★) — Deux fournisseurs de ciment.** L'un annonce 50 kg par sac avec un écart-type de 0,4 kg,
l'autre 49,8 kg avec 0,2 kg. Le cahier des charges accepte de 49,5 à 50,5 kg. Lequel choisir, et que calculez-vous ?

**Exercice 3.3 (★★) — Le CV par catégorie, sans recopier.** Retrouvez le CV de la catégorie Plomberie et
l'effectif qui le soutient. *(attendu : 160,9 %, écart-type 247 146 FCFA, 57 lignes)*

**Exercice 3.4 (★★) — Écart-type ou MAD ?** Pour chacune de ces séries, dites lequel vous citez en priorité, en une
ligne de justification : (a) 480 montants de lignes ; (b) les effectifs de 30 magasiniers répartis sur six sites ;
(c) 500 délais de livraison dont trois retards de 40 jours.

**Exercice 3.5 (★★★) — Note de stabilité pour l'acheteur.** Six lignes à destination du responsable des achats :
deux catégories dont la moyenne est utilisable, une où elle ne l'est pas, une borne d'alerte sur les tickets avec sa
justification, et la précision de vos chiffres. *(attendu : Peinture 81,4 % et Consommables 102,9 % ; Electricité
170,4 % ; borne 295 445 FCFA, 25 tickets ; erreur type 10 244 FCFA)*

## 12. Correction détaillée

**Exercice 3.1.** Étendue : 1 229 678 moins -150 804, soit 1 380 482 FCFA. Écart-type : 143 915 FCFA pour une
moyenne de 75 152 FCFA, d'où un CV de 191,5 % — sur cette colonne, la moyenne ne décrit pas la série. L'IQR se lit
par `=QUARTILE.INC` : notez-le avec ses deux quartiles, sinon un tiers ne peut pas le vérifier. Point de méthode
valorisé : l'effectif de 480 écrit à côté de chaque ligne du tableau.

**Exercice 3.2.** On calcule les CV : 0,8 % et 0,4 %. Le second est deux fois plus régulier et son centre est dans
la tolérance, donc on le retient à caractéristiques égales. Réserve attendue : un écart-type ne dit pas quelle part
des sacs sort de la tolérance sans hypothèse sur la distribution ; la réponse professionnelle est d'exiger un
contrôle sur cent sacs, pas de signer sur la foi du seul écart-type.

**Exercice 3.3.** 57 lignes pour Plomberie, moyenne de 153 596 FCFA, écart-type de 247 146 FCFA, CV de 160,9 %.
Avec un tel effectif, l'erreur type de la moyenne dépasse le cinquième de la moyenne : la conclusion « la moyenne ne
décrit rien » est robuste, la valeur exacte du CV ne l'est pas. La phrase attendue tient en deux parties, et les
deux doivent être là.

**Exercice 3.4.** (a) les deux : l'écart entre écart-type et MAD est lui-même le signal (182 095 contre
43 372 FCFA sur les paniers). (b) IQR ou MAD : effectif faible, un départ ou un recrutement domine. (c) MAD : trois
délais extrêmes sur cinq cents faussent l'écart-type, et le sujet est précisément ces trois délais — on ne veut pas
qu'ils entrent dans le critère qui doit les révéler.

**Exercice 3.5.** Note attendue. Peinture (CV 81,4 %) et Consommables (102,9 %) : moyennes utilisables comme base
d'échange, même si le second CV dépasse encore la zone de confort. Electricité (CV 170,4 %, écart-type
202 897 FCFA) : aucune remise assise sur la moyenne. Borne d'alerte : 295 445 FCFA, soit Q3 plus une fois et demie
l'IQR, justifiée parce qu'elle ne se laisse pas fixer par les tickets qu'elle signale ; 25 tickets la franchissent.
Précision : moyenne à environ deux fois 10 244 FCFA près, CV connu à plusieurs points près. Toute ligne citant un
nombre absent des mesures du socle est comptée 0.

## 13. Mini-projet M02.P2 — suite : la colonne « précision » (30 min)

Reprenez le **M02.P2** du chapitre précédent (deux pages, six nombres, une décision ; barème 20 points, seuil de
validation 13) et ajoutez **deux colonnes** au tableau : le CV et l'erreur type, chacun avec son effectif. La règle
d'écriture devient : *toute comparaison entre deux vendeurs ou deux catégories est accompagnée de la précision des
deux nombres comparés* ; une comparaison dont l'écart reste inférieur à deux erreurs types est présentée comme
« non discriminante à ce stade ». Deux conséquences à faire apparaître explicitement : la catégorie qui résiste le
moins à l'analyse (Bois & panneaux, 24 lignes, CV 157,6 %) est écartée de la page de décision, et le seuil
d'alerte proposé est calculé sur la série complète, avant tout retrait.

## 14. Résumé du chapitre

1. Trois dispersions, trois usages : l'**étendue** décrit les extrêmes (1 494 470 FCFA sur les tickets, 13,6 fois
   l'IQR), l'**IQR** décrit la moitié du milieu et sert de borne (109 924 FCFA), l'**écart-type** décrit la distance
   typique au centre et sert de matière première (182 095 FCFA).
2. Un écart-type ne se compare jamais seul : le **CV** le rend comparable (Peinture 81,4 %, Electricité 170,4 %),
   et c'est lui qui décide si une moyenne est pilotable.
3. L'**erreur type** (10 244 FCFA, 9,0 % de la moyenne) dit de combien votre moyenne est fausse ; sans elle, toute
   comparaison entre deux vendeurs est une opinion.
4. La **MAD** (43 372 FCFA) et le **CV tronqué** (96,6 % au lieu de 159,5 %) sont les garde-fous des séries sales —
   et l'écart entre robuste et non robuste est, lui aussi, une information.

## 15. À retenir

> **À retenir.**
>
> - Une moyenne sans dispersion est une opinion ; deux dispersions suffisent à décider : l'IQR pour borner, le CV
>   pour comparer.
> - Sur les tickets : étendue 1 494 470 · IQR 109 924 · écart-type 182 095 FCFA · CV 159,5 % · erreur type 10 244
>   FCFA (9,0 % de la moyenne) · MAD 43 372 FCFA, le tout sur 316 tickets.
> - Une borne de détection se calcule sur la série complète, avant tout retrait ; sinon les détectés fixent la règle
>   qui doit les détecter.
> - CV supérieur à 50 % : la moyenne ne décrit rien, on montre la distribution.

> **À retenir.** La formulation qui protège. Dans une note : « écart-type de *X* FCFA (moyenne *Y* FCFA, CV *Z* %,
> *n* = *N* tickets, fichier nettoyé) ». À l'oral : « cette moyenne est précise à *p* % près ; l'écart que vous
> voyez est plus petit que cette précision, donc nous ne statuons pas ».

## 16. Évaluation formative (auto-correction, 10 min)

**1.** Quelle dispersion est la moins affectée par une erreur de saisie sur une seule ligne, et pourquoi ?
**2.** Comment passe-t-on de la variance à l'écart-type, et que faire des décimales obtenues ?
**3.** Une série a une moyenne de 250 et un écart-type de 60 ; une autre, une moyenne de 4 000 et un écart-type de
900. Laquelle est la plus instable, et que calcule-t-on pour le savoir ?
**4.** À quoi sert l'erreur type, concrètement, en réunion ?
**5.** Vrai ou faux : la borne de Tukey se calcule après retrait des valeurs extrêmes. Justifiez.

<details><summary><strong>Corrigé</strong></summary>

1. L'IQR et la MAD : ils ignorent les extrêmes par construction, alors que l'étendue est entièrement portée par eux.
2. On extrait la racine carrée, ce qui ramène l'indicateur dans l'unité de la variable ; on affiche arrondi, on
   calcule avec les décimales. 3. Les CV : 24,0 % et 22,5 % — la première série est la plus instable, malgré un
   écart-type trois fois plus petit. 4. À traduire une moyenne en « valeur ± précision », donc à décider si un écart
   constaté vaut une action, une réunion, ou rien. 5. Faux : la borne se calcule sur la série complète puis
   s'applique ; sinon on écarte des valeurs d'après un critère qu'elles ont elles-mêmes fabriqué.

</details>

**Auto-validation.** Reprenez les cinq contrôles du §7 sur votre fichier, puis comparez vos cinq nombres à la table
de référence : 182 095 · 109 924 · 43 372 · 10 244 · 295 445. En cas d'écart, vérifiez le grain avant
l'arithmétique : *n* = 316 tickets, et non 480 lignes.
