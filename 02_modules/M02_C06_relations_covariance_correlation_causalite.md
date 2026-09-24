# M02.C06 — Relier deux variables : covariance, corrélation, causalité, paradoxes

> **L'idée du chapitre.** Deux colonnes varient-elles ensemble ? La corrélation répond en un nombre, et ce nombre est
> le plus mal employé de toute la statistique d'entreprise. Ce chapitre pose la mécanique — covariance, coefficient,
> nuage, droite — et surtout la frontière qui sépare « va avec » de « fait aller avec ».

> **Base de travail — obligatoire.** Deux fichiers du socle, dans votre dossier `02_exercices/M02/`, ouverts côte à
> côte : `donnees/projection/ventes_magasin5_2025.csv` (489 lignes × 13 variables) et
> `donnees/reference/ventes_magasin5_2025_ATTENDU.csv` (480 × 13). Séparateur point-virgule, encodage UTF-8, virgule
> décimale. Montants en franc CFA (FCFA). Grain de référence : la **ligne** (480 observations) pour quantité, prix,
> remise et montant ; le **panier** (316 tickets) pour les questions de clientèle. Chiffres mesurés dans
> `01_socle_donnees/data/reference/chiffres_cites.md`, section M02.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous êtes capable de :

1. calculer une covariance et une corrélation, et expliquer pourquoi la première ne se communique pas ;
2. distinguer corrélation de Pearson et corrélation de rangs (Spearman), et choisir l'une ou l'autre selon la
   présence de valeurs extrêmes ;
3. estimer une droite de régression simple, en lire la pente, l'ordonnée à l'origine et le R², et refuser d'extrapoler
   hors du domaine observé ;
4. énoncer les quatre explications possibles d'une corrélation observée — lien direct, causalité inverse, cause
   commune, hasard de l'échantillonnage — et dire ce que vos données permettent de trancher ;
5. contrôler une **variable de confusion** (la catégorie de produits, le vendeur, la période) et vérifier si l'écart
   survit à ce contrôle ;
6. repérer les trois paradoxes usuels du métier — corrélation mécanique, effet d'agrégation, retournement de
   Simpson — avec un exemple vérifié sur le fichier.

## 2. Pourquoi cette notion est importante

Les questions professionnelles ne sont presque jamais des questions de niveau : ce sont des questions de liaison.

- **« La remise fait-elle vendre plus ? »** C'est une corrélation à tester entre `remise` et `montant_ttc`. Sur le
  fichier, elle vaut -0,031 : les lignes les plus remisées ne sont pas les plus grosses. Cette absence de liaison,
  si le test du chapitre M02.C08 la confirme, contredit une idée reçue du magasin et ouvre une décision : la remise
  actuelle n'achète pas de volume mesurable.
- **« Est-ce le prix qui fait le montant, ou la quantité ? »** Les deux corrélations mesurées valent 0,436 pour le
  prix unitaire et 0,712 pour la quantité : le volume pèse davantage que l'étiquette dans la recette par ligne. Voilà
  un argument pour piloter le panier, pas seulement le prix.
- **« Nos meilleurs vendeurs ont-ils les meilleurs produits ? »** La question est exactement celle de la variable de
  confusion : Bationo a le panier moyen le plus élevé, 103 367 FCFA, et la plus faible part de Bois & panneaux dans
  ses lignes, 2,4 %. Le contrôle à catégorie contenue, chiffré au §5.6, donne un résultat contre-intuitif.

> **Dans les faits.** Dans une entreprise de cette taille, la corrélation sert surtout d'argument d'autorité :
> « les gros paniers sont remisés, donc la remise crée du panier ». Vous n'êtes pas là pour produire ce type de
> phrase, mais pour être celui qui demande : *sur quel échantillon, à quel grain, et avez-vous contrôlé la
> catégorie ?* Trois questions qui, sur notre extrait, transforment une affirmation en décision mesurée.

## 3. Explication simple

Deux colonnes varient ensemble quand, en parcourant les lignes, on constate une régularité : quand l'une monte,
l'autre monte (ou baisse). Le **nuage de points** — *scatter plot* — montre cette régularité ; le **coefficient de
corrélation** la résume en un nombre entre -1 et +1.

Le cas le plus parlant du fichier : la quantité vendue sur une ligne et le montant de cette ligne. Plus il y a de
sacs, plus le montant monte ; le nuage s'allonge, le coefficient vaut 0,712. Pour mesurer cette allure, on calcule
d'abord la **covariance** — *covariance* — la moyenne des produits des écarts aux deux moyennes : quand les deux
variables montent et baissent ensemble, les produits sont positifs, la covariance est positive.

La covariance a un défaut rédhibitoire : elle s'exprime en « unités de x × unités de y », soit ici des pièces-FCFA.
Sa valeur, 857 634, ne se lit pas et ne se compare pas. La corrélation est cette covariance nettoyée de ses unités :
on divise par les deux écarts-types, et il ne reste qu'un nombre sans unité.

Trois réflexes avant toute formule : (1) regarder le nuage avant le coefficient ; (2) vérifier que les deux
colonnes décrivent le même objet au même grain — corréler une moyenne par client avec une ligne de commande est une
faute ; (3) écrire ce que la liaison ne dit pas, à commencer par la causalité.

## 4. Vocabulaire essentiel

| # | Terme | Français — English — sens simple | À savoir |
|---|---|---|---|
| 1 | Covariance | covariance — *covariance* — moyenne des produits des écarts aux moyennes | garde le signe, perd l'échelle ; `COVARIANCE.S` / `COVAR_SAMP` |
| 2 | Corrélation linéaire | coefficient de corrélation de Pearson — *Pearson correlation* — covariance standardisée, entre -1 et +1 | ne mesure que le lien *linéaire* |
| 3 | Corrélation de rangs | corrélation de rang de Spearman — *Spearman rank correlation* — le même calcul sur les rangs | robuste aux extrêmes, capte les liaisons monotones |
| 4 | Nuage de points | nuage de points — *scatter plot* — une observation = un point | l'étape que personne ne saute impunément |
| 5 | R² | coefficient de détermination — *coefficient of determination* — part de variance expliquée | en régression simple, R² = r au carré |
| 6 | Pente | pente — *slope* — variation moyenne de y par unité de x | 12 237 FCFA par pièce sur notre série |
| 7 | Ordonnée à l'origine | ordonnée à l'origine — *intercept* — valeur prédite quand x vaut zéro | ici -10 402 FCFA : une ligne de quantité nulle n'existe pas |
| 8 | Causalité | lien de cause à effet — *causality* — agir sur x change y | ne se déduit pas d'une corrélation |
| 9 | Variable de confusion | variable de confusion — *confounder* — cause commune des deux variables | catégorie, vendeur, saison : trois candidats ici |
| 10 | Corrélation partielle | corrélation partielle — *partial correlation* — lien restant après contrôle d'une tierce | l'outil conceptuel du §5.6 |
| 11 | Extrapolation | extrapolation — *extrapolation* — prédire hors du domaine observé | proscrite en note de gestion |
| 12 | Régression | régression linéaire simple — *simple linear regression* — droite des moindres carrés | une méthode d'ajustement, pas une preuve |

## 5. Cours approfondi

### 5.1 La covariance, ou mesurer sans unité

> **Définition.** La **covariance** entre deux variables x et y est la moyenne des produits des écarts : pour chaque
> observation, (xᵢ − moyenne de x) × (yᵢ − moyenne de y). Elle est positive si les deux varient dans le même sens,
> négative si elles varient en sens contraire, proche de zéro si aucune allure ne se dégage. On la note cov(x, y).

Sur les 480 lignes du fichier, la covariance entre `quantite` et `montant_ttc` vaut 857 634. Ce nombre dit le signe
et une idée d'ampleur, rien de plus : il change si l'on passe du niveau ligne au niveau ticket, et il devient
absurde dès qu'on change de monnaie. Sa seule utilité professionnelle est pédagogique — comprendre que la
corrélation est une covariance débarrassée de ses unités.

**Faites-le dans un tableur.** `=COVARIANCE.S(plage_x; plage_y)` dans Excel comme dans LibreOffice (anglais
*COVAR.S*), ou la voie lente, à faire une fois : trois colonnes (écart à la moyenne de x, écart à la moyenne de y,
produit des deux) puis `=MOYENNE()` sur la troisième. Vous verrez ce que le signe veut dire : les lignes où beaucoup
de pièces s'accompagnent de gros montants ajoutent des produits positifs, et ce sont les plus nombreuses.

> **Attention.** Une covariance calculée sur deux colonnes de natures différentes — un identifiant et un prix, une
> date et un montant — n'est pas nulle par accident : elle est *dénuée de sens*, parce que l'ordre des identifiants
> ne signifie rien. Le logiciel, lui, calcule sans protester. C'est à vous de trier les colonnes autorisées, et
> c'est le rôle du tableau de typage construit au chapitre M01.C05.

### 5.2 Le coefficient de corrélation, et ce qu'il mesure vraiment

> **Définition.** Le **coefficient de corrélation linéaire de Pearson** — *Pearson correlation coefficient*, noté
> *r* — est la covariance divisée par le produit des deux écarts-types. Il vaut +1 quand les points sont
> exactement alignés en montant, -1 exactement alignés en descendant, et zéro quand aucune allure linéaire ne se
> dégage. Sans unité, il se compare entre colonnes et entre périodes.

Sur le fichier, les couples mesurés donnent :

| Couple de variables | Grain | r | Ce que ça veut dire |
|---|---|---|---|
| `quantite` × `montant_ttc` | ligne (480) | 0,712 | lien franc, mais très imparfait |
| `prix_unitaire_ht` × `montant_ttc` | ligne (480) | 0,436 | le prix compte, moins que le volume |
| `quantite` × `prix_unitaire_ht` | ligne (480) | -0,041 | gros volumes et prix bas ne vont pas ensemble |
| `remise` × `montant_ttc` | ligne (480) | -0,031 | aucune liaison linéaire entre remise et taille de ligne |
| heure de saisie × `montant_ttc` | ligne (480) | 0,007 | l'heure n'explique pas le montant |
| `montant_ht` × `montant_ttc` | ligne (480) | 1,000 | liaison mécanique : l'un se déduit de l'autre |

Quatre lectures de professionnel :

1. **0,712 est fort, pas écrasant.** Le carré de ce coefficient, 50,7 % — le R² du §5.4 — dit que la quantité
   explique la moitié de la variance du montant. La moitié. Écrire « le montant dépend de la quantité » sans le R²
   est une exagération.
2. **Le couple remise / montant est le plus instructif.** Un montant plus élevé ne s'accompagne pas d'une remise
   plus forte (-0,031), et les gros volumes ne se négocient pas mieux (-0,041). Résultat *négatif*, et un résultat
   négatif mesuré vaut mieux qu'une intuition : la politique de remise du magasin n'est pas calée sur la taille de la
   ligne.
3. **r = 1,000 entre HT et TTC est trivial.** Les deux colonnes se déduisent l'une de l'autre par la TVA et la
   remise : ce n'est pas une découverte, c'est une identité comptable. Repérer une corrélation mécanique est une
   compétence — avant de commenter un coefficient élevé, demandez si une colonne n'est pas *construite* à partir de
   l'autre.
4. **Un r proche de zéro n'est pas une indépendance.** Le coefficient ne voit que le linéaire : si les fortes
   remises se concentrent sur les très petites lignes *et* sur les très grosses, la liaison existe et r reste
   voisin de zéro. Avant de conclure « aucun lien », on regarde le nuage, la médiane par strate, ou un test
   d'association sur catégories (M02.C08).

**Faites-le dans le SQL.** *(les vues `lignes_ventes` et `paniers` ont été créées au C02, § « Pour la suite du module »)* :

```sql
SELECT COUNT(*)                                   AS n,
       ROUND(COVAR_SAMP(quantite, montant_ttc), 0) AS covariance,
       ROUND(CORR(quantite, montant_ttc), 3)        AS pearson
FROM lignes_ventes;
```

Ne mélangez pas les colonnes dans un même contrôle : covariance sur `montant_ht`, corrélation sur `montant_ttc`
produit deux chiffres justes séparément et une phrase fausse ensemble. Le réflexe : une requête, un couple de
variables.

### 5.3 Rang contre valeur : Spearman

> **Définition.** La **corrélation de rang de Spearman** — *Spearman rank correlation*, notée ρ — remplace chaque
> valeur par son rang dans la série triée, puis calcule la corrélation de Pearson sur ces rangs. Elle mesure si les
> deux variables montent ensemble, sans exiger que ce soit proportionnellement.

Sur `quantite` et `montant_ttc`, Spearman vaut 0,641 contre 0,712 en Pearson. Que le rang soit plus faible est une
information : quelques lignes à très forte quantité produisent des écarts disproportionnés qui gonflent la liaison
linéaire — la quantité maximale après correction est de 68 pièces quand la médiane est de 4, et l'énoncé non
nettoyé montait jusqu'à 14 000. Concrètement :

| Situation | Ce qu'on publie | Pourquoi |
|---|---|---|
| Variables continues, allure proche d'une droite, effectif confortable | Pearson | plus précis quand les hypothèses tiennent |
| Valeurs extrêmes nombreuses, ou variable déjà ordonnée (note de satisfaction) | Spearman | insensible aux distances, robuste |
| Effectif faible (une trentaine de points) | les deux, et le nuage | vérifier que la conclusion ne tient pas à trois lignes |
| Colonne texte convertie en date ou en mois | aucune : re-typologiser d'abord | une date n'est pas une quantité |

Règle de rédaction : **quand les deux coefficients se contredisent, c'est l'écart qui s'écrit** ; quand ils
concordent, une mention « (Spearman : 0,641) » en note suffit, et elle clôt la discussion sur les valeurs extrêmes.

### 5.4 La droite de régression : trois nombres et une interdiction

> **Définition.** La **régression linéaire simple** — *simple linear regression*, méthode des moindres carrés
> (*ordinary least squares*, OLS) — trace la droite qui minimise la somme des carrés des écarts verticaux. Elle
> livre la **pente** (variation moyenne de y par unité de x), l'**ordonnée à l'origine** (valeur prédite quand x vaut
> zéro) et le **R²** (part de la variance de y expliquée par x).

Sur les 480 lignes, la droite `montant = a × quantité + b` donne :

| Élément | Valeur | Lecture professionnelle |
|---|---|---|
| Pente | 12 237 FCFA par pièce | une pièce de plus sur une ligne s'accompagne, en moyenne, de 12 237 FCFA de plus |
| Ordonnée à l'origine | -10 402 FCFA | sans signification : une ligne de quantité nulle n'existe pas |
| R² | 50,7 % | la quantité explique la moitié de la dispersion du montant, pas plus |
| Pente standardisée | 71,2 % | un écart-type de quantité en plus, c'est 0,71 écart-type de montant : c'est exactement *r* |

Trois usages de ces nombres. D'abord, la **pente est un fait conditionnel** : elle vaut « toutes lignes confondues,
sur l'année 2025, au grain ligne ». Elle ne vaut ni par produit, ni par catégorie : la pente d'un rayon de matériaux
lourds n'a rien de commun avec celle de la quincaillerie, et la moyenne des pentes par catégorie n'est pas la pente
globale.

Ensuite, le **contrôle du point moyen** : la droite des moindres carrés passe par le point (moyenne de x, moyenne de
y). Appliquée à la quantité moyenne de 7 pièces, elle prédit 75 257 FCFA, pour une moyenne observée de
75 152 FCFA — 105 FCFA d'écart, dus à l'arrondi d'affichage. Si votre prédiction à la moyenne s'écarte nettement de
la moyenne observée, votre droite est fausse : c'est le meilleur contrôle de régression qui soit, et il prend dix
secondes.

Enfin, l'interdiction : **on n'extrapole pas**. Prédire le montant d'une ligne de 200 pièces avec une pente calibrée
entre -13 et 68 pièces est un exercice de fiction — et c'est précisément le genre de chiffre qui, dans un dossier
d'investissement, décrédibilise tout le reste.

**Faites-le dans un tableur.** `=DROITEREG(y; x; VRAI)` renvoie pente et ordonnée ; le R² s'obtient par `=R2(y; x)`,
ou par le carré de `=COEFFICIENT.CORRELATION()`. **Dans le SQL** : `REGR_SLOPE(montant_ttc, quantite)`,
`REGR_INTERCEPT(montant_ttc, quantite)`, `REGR_R2(montant_ttc, quantite)` — trois agrégats, une requête, et le
contrôle du point moyen se fait en comparant `REGR_INTERCEPT + REGR_SLOPE * AVG(quantite)` à `AVG(montant_ttc)`.

> **Conseil professionnel.** Présentez toujours la pente et le R² ensemble : une pente sans R² fait croire à une
> loi, un R² sans pente ne dit pas de combien. Nos deux chiffres dans une phrase : « une pièce de plus sur une ligne
> s'accompagne en moyenne de 12 237 FCFA de plus, mais cette seule variable ne fait que la moitié du travail
> (R² 50,7 %) ».

### 5.5 Corrélation n'est pas causalité : les quatre configurations

> **Définition.** On dit que x **cause** y si agir sur x change y. La corrélation ne teste pas cela : elle constate
> une variation conjointe. Quatre configurations produisent une corrélation sans lien causal : la cause commune, la
> causalité inverse, le hasard de l'échantillonnage, et la sélection du périmètre — ce que les données contiennent
> déjà avant toute analyse.

Appliquées au fichier :

| Configuration | Comment elle apparaîtrait ici | Comment on la reconnaît |
|---|---|---|
| Cause commune | Grosses ventes et grosses remises viennent des mêmes périodes de chantier | croiser avec la date et la catégorie : si le lien disparaît à période contenue, c'était la saison |
| Causalité inverse | On croit que la remise gonfle le panier ; c'est le gros panier qui obtient une remise | la réponse est temporelle ou contractuelle, pas statistique : la remise se décide pendant la vente |
| Hasard d'échantillonnage | Deux colonnes sans rapport peuvent afficher r = 0,10 sur 480 lignes | le test de signification du chapitre M02.C08 ; à n = 480, la barre du bruit est vers 0,09 |
| Sélection du périmètre | Sur le seul magasin 5, une liaison propre à la ville apparaît ou disparaît | reproduire sur un autre magasin, puis sur le fichier complet |

Le plus utile à votre niveau est le troisième : la **barre de bruit**. Deux colonnes sans aucun rapport, sur 480
lignes, peuvent afficher une corrélation de 0,1. La vôtre, si elle est plus petite que ce seuil, ne mérite aucun
commentaire. C'est ce qui rend les chiffres de l'extrait lisibles : à 0,712, la liaison quantité-montant n'a rien de
comparable au bruit ; à 0,007, l'heure de saisie ne veut rien dire du tout.

### 5.6 Contrôler la variable de confusion — et le paradoxe de Simpson

> **Définition.** Une **variable de confusion** (*confounder*) influence à la fois x et y et fait apparaître un lien
> qui n'existe pas entre elles. Contrôler un facteur de confusion consiste à comparer x et y **à l'intérieur de
> chaque strate** de cette variable, puis à regarder si la conclusion survit. Quand elle s'inverse strate par strate,
> on parle de **paradoxe de Simpson** (*Simpson's paradox*, effet de Simpson-Yule).

Testons la question la plus politique du module : les vendeurs vendent-ils plus gros parce qu'ils ont de meilleurs
produits ?

| Étape | Mesure | Valeur |
|---|---|---|
| 1 | Panier moyen le plus élevé des quatre vendeurs (Bationo) | 103 367 FCFA |
| 2 | Panier moyen le plus faible (Ilboudo) | 69 352 FCFA |
| 3 | Écart global entre ces extrêmes | 34 014 FCFA |
| 4 | Part de Bois & panneaux — la catégorie la plus chère — dans leurs lignes | de 2,4 % (Bationo) à 8,5 % (Ouédraogo) |
| 5 | Écart maximal entre vendeurs, calculé catégorie par catégorie puis moyenné | 57 346 FCFA |
| 6 | Dispersion de cet écart par catégorie | de 17 433 (Quincaillerie) à 173 167 FCFA (Electricité) |

Le résultat contredit le schéma habituel : l'écart entre vendeurs **n'est pas réduit** par le contrôle de la
catégorie — il augmente (57 346 contre 34 014 FCFA). Le mix produit n'explique donc pas la différence : il
l'occultait. Le cas est même nettement inverse à l'intuition, puisque le vendeur au plus fort panier moyen est aussi
celui qui a la plus faible part de la catégorie la plus chère (2,4 % de ses lignes).

> **Attention.** Contrôler une variable multiplie les petites strates, et c'est là que la méthode se brise :
> Bois & panneaux compte 24 lignes pour vingt-deux vendeurs — certaines strates n'en contiennent que trois. Un
> écart calculé sur trois observations n'est pas un résultat, c'est un dessin. Fixez un effectif minimal par strate,
> appliquez-le à toutes les catégories sans exception, et écrivez lesquelles ont été écartées du calcul : c'est ce
> qui rend la démarche crédible quand la conclusion dérange.

Deux précautions, à écrire dans la note. D'abord, ce calcul n'a pas été mené sur Bois & panneaux : avec 24 lignes
réparties sur vingt-deux vendeurs, certaines catégories n'ont que quelques lignes par vendeur, et un écart calculé
dessus est du bruit. Ensuite, l'écart moyen par catégorie masque une dispersion énorme (17 433 à
173 167 FCFA) : la conclusion « le mix n'explique rien » est vraie en moyenne, pas dans chaque rayon.

C'est là l'usage professionnel du paradoxe de Simpson, bien plus utile que sa curiosité : **on ne l'invente pas, on
le cherche.** La méthode tient en trois questions écrites dans la note : la catégorie explique-t-elle l'écart ? la
période ? le type de client ? Si rien ne l'explique, l'écart devient un objet d'explication — et s'il disparaît,
l'affirmation initiale était un artefact de découpage.

### 5.7 Agrégation : pourquoi les corrélations montent quand on résume

Un effet de bord que l'on découvre trop tard : plus on agrège, plus les points s'alignent. Sur les 480 lignes,
`quantite` et `montant_ttc` corrèlent à 0,712 ; agrégées par client (372 clients distincts dans l'attendu), les
totaux corrèlent généralement plus fort, parce que les irrégularités individuelles se moyennent ; et la corrélation
peut s'effondrer si l'on agrège par jour, parce que l'effet de taille de journée écrase tout. Ce **problème
d'agrégation** (*modifiable areal unit problem* dans sa version spatiale, effet de groupement dans sa version
courante) a une conséquence pratique unique :

- **le grain s'écrit au même titre que le coefficient** : « r = 0,712, au niveau de la ligne (480 observations) » ;
- **on ne compare jamais deux corrélations calculées à des grains différents**, même sur le même fichier ;
- **on se méfie des corrélations spectaculaires sur séries mensuelles courtes** : douze points donnent
  fréquemment un r très élevé entre deux variables simplement croissantes — le lien est alors une tendance partagée,
  pas une dépendance.

### 5.8 Calculer les liaisons : quel outil, quelle formule

| Ce que vous voulez | Tableur | SQL (DuckDB) | pandas |
|---|---|---|---|
| Corrélation linéaire | `=COEFFICIENT.CORRELATION(x;y)` (anglais *CORREL*) | `CORR(x, y)` | `df.x.corr(df.y)` |
| Covariance d'échantillon | `=COVARIANCE.S(x;y)` | `COVAR_SAMP(x, y)` | `df.x.cov(df.y)` |
| Corrélation de rangs | `=CORREL()` sur deux colonnes de `=RANG()` | tri puis `CORR` sur les rangs | `df[["x","y"]].corr(method="spearman")` |
| Pente, ordonnée, R² | `=DROITEREG()`, `=R2()` | `REGR_SLOPE`, `REGR_INTERCEPT`, `REGR_R2` | `scipy.stats.linregress` |
| Matrice de corrélations | table de formules recopiées | une requête par couple | `df.corr(numeric_only=True)` |
| Nuage de points | graphique nuage | échantillon puis export | `df.plot.scatter("quantite", "montant_ttc")` |

> **Boîte à outils.** Contrôle minimal de toute corrélation publiée : (1) l'effectif (480 lignes, 316 paniers ou
> 372 clients) et le grain, dans la légende ; (2) la liste des colonnes autorisées, issue du tableau de typage
> M01.C05, pour ne pas corréler un identifiant ; (3) le nuage regardé au moins une fois — une corrélation de 0,7
> produite par quatre points isolés est une erreur de tracé ; (4) Pearson et Spearman côte à côte sur les séries à
> forte asymétrie, comme ici ; (5) le carré de r publié avec r, pour que le lecteur sache ce qui reste inexpliqué.

## 6. Exemple concret : « la remise fait-elle vendre plus gros ? »

**La demande.** Le directeur veut relever la remise accordée sur les tickets de plus de 100 000 FCFA : « sur nos
gros chantiers, la remise fait la différence ».

**Ce que le fichier dit, ligne par ligne.**

| Question | Calcul | Réponse mesurée |
|---|---|---|
| Les lignes remisées sont-elles plus grosses ? | `CORR(remise, montant_ttc)` sur 480 lignes | -0,031 : aucune liaison linéaire |
| La remise est-elle la règle ou l'exception ? | lignes sans remise | 307 sur 480, soit 64,0 % sans aucune remise |
| Le vendeur remet-il à sa guise ? | test d'association vendeur × remise | 3,03 de chi-deux, p = 0,388 : pas d'association détectée (M02.C08) |
| La catégorie explique-t-elle les montants ? | CV par catégorie | de 81,4 % (Peinture) à 170,4 % (Electricité) — M02.C03 |

**La conclusion, et sa limite.** Sur cet extrait, aucune liaison linéaire mesurable entre remise et taille de ligne :
relever la remise sur les gros tickets n'a, dans ces données, pas de contrepartie observée en volume. La limite est à
écrire explicitement : 173 lignes seulement portent une remise (480 moins 307), réparties sur six taux
(0 ; 0,03 ; 0,04 ; 0,07 ; 0,08 ; 0,11) — un plan d'expérience quasi inexistant. On ne prouve pas l'efficacité d'une
politique de prix avec des remises accordées au cas par cas. La recommandation professionnelle n'est donc pas
« n'augmentez pas la remise » mais « testez : deux mois, deux groupes de clients, un taux, une mesure ».

**La phrase à écrire dans la note.** « La liaison entre taux de remise et montant de ligne est nulle sur l'extrait
(r = -0,031, n = 480 lignes). Cette absence ne prouve pas l'inefficacité de la remise : elle signale que le fichier
ne contient pas d'expérience de prix exploitable. Nous recommandons un test borné plutôt qu'un ajustement unilatéral
de la politique. »

## 7. Démonstration pas à pas : du nuage au coefficient, puis au contrôle

**Étape 1 — Choisir le couple.** `quantite` et `montant_ttc`, au niveau de la ligne, sur le fichier attendu
(480 lignes). Notez la décision : deux colonnes, un grain.

**Étape 2 — Le nuage d'abord.** 480 points, échelles linéaires. Ce que l'on doit y voir : un alignement montant, un
point très à droite et très en haut (la plus grosse ligne), quelques points sous zéro (les retours). Si le nuage
dessine un éventail — dispersion croissante avec x —, la relation est hétéroscédastique et la pente moyenne masque
deux régimes : à écrire dans la note.

**Étape 3 — La covariance, puis r.** `COVAR_SAMP` puis `CORR`, en SQL. Vérifiez que le passage de l'un à l'autre se retrouve : 857 634 divisé par le produit des écarts-types (8,4 et 143 915 FCFA)
nous ramène à 0,71, ce qui est la valeur de r aux arrondis de présentation près.

**Étape 4 — Spearman.** Même couple, méthode des rangs : 0,641. Notez la direction de l'écart — le rang est plus
faible —, signe qu'une poignée de valeurs extrêmes pèse davantage sur le linéaire que sur l'ordre.

**Étape 5 — La droite.** `REGR_SLOPE` = 12 237, `REGR_INTERCEPT` = -10 402, `REGR_R2` = 0,507. Vérifiez le carré de
r : 0,712 × 0,712 = 0,507 ✔ — en régression simple, R² est exactement le carré du coefficient de corrélation.

**Étape 6 — Le contrôle par strate.** Refaites la pente catégorie par catégorie. Si les pentes s'écartent fortement,
la droite globale est une moyenne d'histoires différentes : la mention « toutes catégories confondues » devient
obligatoire.

**Contrôles qualité du chapitre.**

| # | Contrôle | Seuil | Résultat attendu | Si échec |
|---|---|---|---|---|
| 1 | r dans l'intervalle [-1 ; +1] | mathématique | 0,712 | colonnes de types mélangés |
| 2 | R² égal au carré de r (régression simple) | au centième | 50,7 % | régression multiple ou pondérée |
| 3 | Droite passant par le point moyen | écart < 0,2 % de la moyenne | 75 257 contre 75 152 FCFA | pente ou ordonnée mal lues |
| 4 | Un seul grain, une seule population | effet identique | 480 lignes | jointure ou agrégation oubliée |
| 5 | Signe de la covariance = signe de r | identité | les deux positifs | sélection de colonnes erronée |

## 8. Erreurs fréquentes

1. **Commenter r sans avoir vu le nuage.** Un r de 0,7 peut être produit par un point isolé et quelques dizaines
   d'autres en rond : le coefficient est exact, l'histoire est fausse. Le nuage se regarde avant, et se conserve en
   annexe.
2. **Corréler des colonnes mal typées.** Dans l'énoncé, `montant_ttc` est stocké en texte sur 486 des 489 lignes
   (M01.C04) : lu comme une catégorie par certains outils, comme une suite de chiffres par d'autres, le coefficient
   dépend alors du logiciel et non des données.
3. **Publier la covariance.** Sans unité lisible, 857 634 ne veut rien dire. Elle sert au calcul, pas à la note.
4. **Confondre force et certitude.** Un r de 0,10 sur 40 000 lignes est statistiquement établi et commercialement
   inutile ; un r de 0,7 sur 12 lignes est commercialement séduisant et statistiquement fragile. Le premier nombre
   mesure la taille de la liaison, le second sa solidité — et c'est le chapitre M02.C08 qui fournit le second.
5. **Oublier que la pente dépend du périmètre.** 12 237 FCFA par pièce est une moyenne annuelle, toutes catégories.
   Sur Bois & panneaux seuls, elle change : citer un chiffre global comme s'il s'appliquait à une gamme est la
   manière la plus rapide de perdre un auditeur.
6. **Inventer une causalité à partir d'un calendrier.** « Les ventes augmentent avec la remise en novembre » : les
   deux montent, mais la saison des chantiers monte aussi. Une corrélation temporelle partagée n'est pas une
   liaison causale — c'est la définition même de la cause commune.

## 9. Bonnes pratiques professionnelles

1. **Une phrase, trois éléments** : le coefficient, l'effectif, le grain. « r = 0,712 (480 lignes, niveau ligne,
   fichier nettoyé) ».
2. **Joindre le nuage.** Trois cents points coûtent une ligne et désarment la moitié des contestations.
3. **Publier R² en pourcentage.** « La quantité explique 50,7 % de la variation du montant » : le lecteur comprend
   qu'il reste 49,3 % à expliquer — c'est exactement le propos.
4. **Nommer la variable de confusion contrôlée**, et dire quand elle ne change rien : ici l'écart entre vendeurs
   passe de 34 014 à 57 346 FCFA quand on contrôle la catégorie.
5. **Traiter les corrélations proches de zéro comme des résultats**, pas comme des échecs : -0,031 répond à une
   question de politique commerciale, à condition d'ajouter ce que la donnée ne permet pas de conclure.
6. **Réserver le mot « effet » aux expériences**, et employer « liaison », « lien », « co-variation » pour tout le
   reste. Cette discipline de vocabulaire est la meilleure ligne de défense de l'analyste.

## 10. Exercice guidé — la liaison quantité / montant, entièrement refaite

**Énoncé.** Sur le fichier attendu : nuage, covariance, Pearson, Spearman, droite de régression, R², puis
commentaire en trois phrases pour un directeur commercial.

**Vous faites** — barème 10 points, total 10.

| Étape | Ce que vous produisez | Points |
|---|---|---|
| A | Le nuage, axes nommés et effectif indiqué | 2 |
| B | Covariance et r, avec le calcul de r à partir de la covariance | 2,5 |
| C | Spearman, et une phrase sur l'écart entre les deux chiffres | 1,5 |
| D | Pente, ordonnée, R², avec le contrôle du point moyen | 2,5 |
| E | Commentaire en trois phrases, sans verbe de causalité | 1,5 |

**Nous vérifions.** Covariance 857 634 · r = 0,712 · Spearman 0,641 · pente 12 237 FCFA par pièce · ordonnée
-10 402 FCFA · R² 50,7 %. Contrôle du point moyen : prédire à la quantité moyenne doit rendre la moyenne des
montants — 75 257 contre 75 152 FCFA, soit l'arrondi d'affichage.

**Nous corrigeons.** Deux formulations à supprimer : « la quantité détermine le montant » (trop fort : la
détermination est comptable, pas comportementale) et « plus on vend de pièces, plus on gagne » (trop faible : cela
vaut pour tout commerce, et le coefficient n'apporte rien). La phrase juste contient le chiffre, le périmètre et la
part inexpliquée.

## 11. Exercices autonomes

**Exercice 6.1 (★) — Le tri des colonnes.** Listez les colonnes du fichier avec lesquelles il est licite de
calculer une corrélation avec `montant_ttc`, et celles où c'est interdit, en une ligne de justification par colonne.

**Exercice 6.2 (★) — Le carré.** Calculez le carré de 0,712 et retrouvez le R² mesuré. Que reste-t-il inexpliqué, et
que signifierait un R² de 95 % dans ce contexte ?

**Exercice 6.3 (★★) — La pente par catégorie.** Estimez la pente de `montant = a × quantité` pour Matériaux
(143 lignes) et pour Consommables (57 lignes). Comparez à la pente globale de 12 237 FCFA et concluez sur son usage.

**Exercice 6.4 (★★) — Le contrôle de confusion.** Reprenez l'écart de panier moyen entre les quatre vendeurs en
contrôlant cette fois le **trimestre** au lieu de la catégorie. L'écart global est de 34 014 FCFA : dites, chiffres
à l'appui, si la période explique une part notable de cet écart.

**Exercice 6.5 (★★★) — Note de liaison.** Six lignes pour la direction sur le couple remise / montant : le
coefficient, l'effectif, le grain, ce que le résultat ne prouve pas, et la proposition d'expérience à mener.
*(attendu : r = -0,031 ; 480 lignes ; 64,0 % de lignes sans remise ; six taux observés ; un test sur deux groupes)*

## 12. Correction détaillée

**Exercice 6.1.** Licites : les colonnes numériques à rapport — `quantite`, `prix_unitaire_ht`, `remise`,
`montant_ht`, `montant_ttc` — et les composantes extraites de la date (jour du mois, heure), à condition de
signaler qu'une heure est une grandeur circulaire. Illicites : `n_ticket` et `client` (identifiants : leur ordre ne
signifie rien), `categorie` et `vendeur` (nominales : on les traite par agrégats ou par tableaux de fréquences),
`date` brute (une date n'est pas une grandeur). La justification attendue nomme le type de chaque colonne, pas une
impression.

**Exercice 6.2.** 0,712 × 0,712 = 0,507, soit 50,7 % : le R² mesuré, contrôle réussi. Restent 49,3 % de variance
inexpliquée — prix unitaire, catégorie, remise, et tout ce que le fichier ne contient pas. Un R² de 95 % devrait
éveiller le soupçon de corrélation mécanique : deux colonnes qui se déduisent l'une de l'autre, comme `montant_ht`
et `montant_ttc` (r = 1,000 ici).

**Exercice 6.3.** Les pentes par catégorie s'écartent fortement — de l'ordre du simple au double entre matériaux
lourds et consommables — et certaines catégories voient la quantité expliquer à peine le montant. Conclusion
attendue : la pente globale est un compromis sans correspondant réel ; elle résume, elle ne prévoit pas une ligne
d'une catégorie donnée. Sont valorisés le rappel des effectifs (143 et 57 lignes) comme facteur de fiabilité
inégale, et la mention de la pente en unité (FCFA par pièce).

**Exercice 6.4.** Ce qui est attendu, c'est la méthode plus que le résultat : recalculer l'écart maximal entre
vendeurs à trimestre contenu, le comparer aux 34 014 FCFA globaux et aux 57 346 FCFA obtenus à catégorie contenue,
et écrire la conclusion en fonction du sens observé. Un écart qui survit à deux contrôles successifs cesse d'être un
artefact de découpage et devient un objet d'explication — à faire discuter par l'entretien, le planning, ou le
portefeuille client.

**Exercice 6.5.** Note attendue : la liaison entre taux de remise et montant de ligne est nulle (r = -0,031,
480 lignes, fichier nettoyé) ; 307 lignes sur 480 ne portent aucune remise et les six taux observés ne forment pas
un plan d'expérience exploitable ; nous ne pouvons donc conclure ni à l'efficacité ni à l'inefficacité de la remise,
seulement à l'absence de donnée pour la juger ; nous proposons deux mois de test sur deux groupes de clients, avec
un taux unique par groupe ; la décision se prendra sur l'écart de panier entre les deux groupes, testé comme au
chapitre M02.C08.

## 13. Mini-projet M02.P3 — « La page des liaisons » (50 min)

**Commande.** Pour la direction commerciale, produisez une page de trois liaisons chiffrées, choisies parmi :
quantité / montant, prix / montant, remise / montant, vendeur / catégorie, heure / montant. Pour chacune : le
coefficient, le grain, l'effectif, le carré du coefficient, et une phrase de conclusion — avec l'obligation
d'écrire explicitement ce que la liaison ne dit pas.

**Livrables numérotés.** (1) le tableau des trois liaisons ; (2) les trois nuages en annexe ; (3) le contrôle de
confusion mené sur la liaison que vous jugez la plus forte, avec ses deux chiffres (avant / après contrôle) ; (4) la
proposition d'expérience pour la liaison politiquement la plus lourde ; (5) la ligne de journal (date, fichiers,
effectifs, versions).

**Barème (20 points, seuil 13).** Coefficients exacts et sourcés (4) · grain et effectif écrits partout (3) · carré
du coefficient commenté (2) · nuages joints et lisibles (3) · contrôle de confusion correctement exécuté (4) ·
expérience proposée mesurable (2) · journal (2) — total 20. Ce livrable rejoint le document du M02.P2 : le projet du
module est la somme des pages, pas leur remplacement.

## 14. Résumé du chapitre

1. La covariance donne le signe et rien d'autre (857 634 pièces-FCFA) ; la corrélation la standardise (0,712), et
   seule la seconde se communique.
2. Pearson voit le linéaire, Spearman le monotone : 0,712 et 0,641 sur la même paire, et l'écart entre les deux est
   un diagnostic sur les valeurs extrêmes.
3. Une droite de régression se réduit à trois nombres — 12 237 FCFA par pièce, -10 402 FCFA, 50,7 % — et le
   contrôle du point moyen (75 257 contre 75 152 FCFA) vérifie le calcul en dix secondes.
4. Une corrélation ne dit rien de la causalité : cause commune, inversion, hasard, périmètre. Le contrôle de
   confusion est une méthode, pas une formule — et sur cet extrait il agrandit l'écart entre vendeurs
   (57 346 contre 34 014 FCFA) au lieu de le résorber.

## 15. À retenir

> **À retenir.**
>
> - Un coefficient publié porte son effectif, son grain et son carré : 0,712 (480 lignes, niveau ligne), 50,7 % de
>   variance expliquée.
> - Une ordonnée à l'origine hors domaine (-10 402 FCFA) et une prédiction hors des valeurs observées s'appellent
>   des extrapolations : elles ne sortent pas du bureau.
> - Corrélation mécanique, agrégation, confusion : trois façons de trouver un lien qui n'explique rien. On les
>   teste, on ne les suppose pas.
> - Le mot « effet » est réservé aux expériences. Tout le reste est une liaison.

> **À retenir.** La formulation qui protège. « Sur 480 lignes du fichier nettoyé, quantité et montant varient
> ensemble à hauteur de r = 0,712 (Spearman 0,641), soit 50,7 % de la variance expliquée : l'autre moitié tient au
> prix, à la catégorie et à ce que nous ne mesurons pas. Rien dans ce calcul n'établit qu'augmenter les quantités
> augmentera la recette. »

## 16. Évaluation formative (auto-correction, 12 min)

**1.** Pourquoi la covariance ne se publie-t-elle pas, alors qu'on la calcule ?
**2.** Sur le couple quantité / montant, Spearman est plus faible que Pearson. Que dit cet écart ?
**3.** Une corrélation de -0,031 entre remise et montant : quelle conclusion licite, quelle conclusion interdite ?
**4.** Le R² vaut 50,7 %. Que répondez-vous à qui demande « donc la quantité ne compte que pour moitié » ?
**5.** Un directeur affirme : « nos vendeurs les plus rentables ont les meilleurs produits, c'est la catégorie qui
   l'explique ». Quelle vérification faire, et quel a été son résultat sur l'extrait ?

<details><summary><strong>Corrigé</strong></summary>

1. Parce qu'elle conserve l'unité des deux colonnes (pièces × FCFA) : 857 634 ne se lit pas, ne se compare pas, et
   change si l'on change de monnaie ou de grain. 2. Que quelques valeurs extrêmes pèsent davantage sur la liaison
   linéaire que sur la liaison de rangs ; la liaison est réelle, mais en partie portée par les plus grosses lignes.
   3. Licite : sur cet extrait, aucune liaison *linéaire* entre remise et taille de ligne, et le fichier ne contient
   pas de plan de prix exploitable. Interdite : « la remise ne sert à rien » — l'absence de liaison observée n'est
   pas la preuve d'une absence d'effet. 4. Que la moitié de la *dispersion* du montant est associée à la quantité,
   l'autre au prix, à la catégorie, à la remise et au non-mesuré ; et que 50,7 % est un chiffre de variance, pas un
   pourcentage de recette. 5. Calculer l'écart entre vendeurs à catégorie contenue et le comparer à l'écart global :
   ici il ne se réduit pas, il passe de 34 014 à 57 346 FCFA en moyenne par catégorie — la catégorie n'explique
   donc pas l'écart, elle le masquait.

</details>

**Auto-validation.** Reprenez les cinq contrôles du §7 : r dans l'intervalle, R² égal au carré de r, point moyen
retrouvé, un seul grain, signe de la covariance conforme. Puis recopiez vos cinq nombres en regard de la table de
référence : 857 634 · 0,712 · 0,641 · 12 237 · 50,7 %. Sur un seul écart, reprenez la jointure avant la formule.
