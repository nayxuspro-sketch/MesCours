# Module M02.C01 — Population, échantillon, individu, variable, modalité, fréquence

**Outil de ce chapitre : un tableur et une base SQL, au choix ; aucun logiciel de statistiques.** Durée indicative : 4 h. Niveau : N1.

> **L'idée du chapitre.** Avant de calculer quoi que ce soit, il faut savoir **de quoi l'on parle** : sur
> combien de choses, sur lesquelles de ces choses, et si ce que l'on a sous la main ressemble à ce que l'on
> voudrait connaître. Ces cinq mots — population, individu, échantillon, variable, modalité — ne sont pas du
> vocabulaire scolaire : ce sont les cinq lignes d'en-tête de tout travail qui engage une décision. Une
> moyenne calculée sur le mauvais objet est juste, et fausse à la fois ; c'est précisément ce qui rend le
> chapitre obligatoire avant les sept suivants.

> **Base de travail — deux chemins pour une seule donnée.** Les fichiers du module vivent à deux endroits, et il faut
> le trancher une fois pour toutes. Dans l'atelier du manuel — le dépôt qui contient ces fichiers — ils sont sous
> `01_socle_donnees/data/`. Chez vous, copiez-les dans votre dossier de module et rangez-les dans deux
> sous-dossiers, `donnees/projection/` pour le fichier de l'énoncé et `donnees/reference/` pour l'attendu et les
> référentiels. **Les blocs de code des huit chapitres écrivent le chemin de l'atelier, parce que c'est celui qui
> s'exécute sans préparation** : si vous travaillez dans votre dossier, remplacez le préfixe `01_socle_donnees/data/`
> par `donnees/` et ne changez rien d'autre. Séparateur point-virgule, encodage UTF-8, montants en franc CFA (FCFA),
> virgule décimale au tableur. Tous les chiffres cités dans le module sont lisibles dans
> `01_socle_donnees/data/reference/chiffres_cites.md`, section M02.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

1. **Nommer** la population, l'échantillon, l'individu, la variable et la modalité d'un jeu de données donné, sans hésiter sur les deux derniers.
2. **Compter** ce que vous avez : effectif total, effectifs par modalité, fréquences en pourcentage, et les écrire avec l'unité.
3. **Distinguer** une ligne d'un individu statistique, et dire lequel des deux compte pour la question posée.
4. **Repérer** une variable à une seule modalité dans un extrait et expliquer ce que cela interdit comme conclusion.
5. **Écrire** la fiche d'identité statistique d'un fichier — celle qui, en entreprise, se joint au chiffre et le rend défendable.

---

## 2. Pourquoi cette notion est importante

**Situation 1 — la réunion qui dérape sur un mot.** Un responsable commercial annonce : « notre panier moyen est à 114 156 FCFA ». Un autre répond : « c'est faux, je vends tous les jours à des clients qui repartent avec moins de 60 000 ». Aucun des deux n'a tort : le premier a calculé une moyenne sur des tickets, le second pense au ticket le plus courant. La dispute n'est pas un désaccord de chiffres mais **un désaccord d'objet** — sur quoi porte le compte. Ce chapitre règle ces disputes avant qu'elles n'aient lieu.

**Situation 2 — le rapport qui ne dit pas ce qu'il couvre.** Vous remettez un document qui affirme « 29,8 % des lignes concernent les Matériaux ». Trois remarques peuvent arriver, et elles arrivent : *sur quelles lignes ?*, *sur quelle période ?*, *et si l'on compte les tickets au lieu des lignes ?*. Un rapport qui répond à ces trois questions dans son premier paragraphe met son lecteur en confiance ; un rapport qui n'y répond pas laisse le doute travailler pour lui.

**Situation 3 — l'échantillon qui ne représente rien.** Vous disposez du fichier complet de quatre années (240 000 lignes propres), mais votre extrait de travail en contient 480 — 0,2 % des lignes. Ce n'est pas un problème en soi : c'est un fait à **dire**. Le problème commence quand on écrit « décembre est notre meilleur mois » comme si l'on avait parlé de l'entreprise, alors que l'on a parlé d'un extrait construit à des fins pédagogiques, à raison de 40 lignes par mois.

> **Dans les faits.** La règle « sur un échantillon, on ne conclut pas sur la population » n'est pas une coquetterie de statisticien : c'est ce qui sépare une analyse d'une rumeur chiffrée. Dans les grandes organisations, les chiffres qui circulent sans mention de périmètre finissent par produire deux tableaux de bord qui se contredisent, et des réunions qui arbitrent au lieu de décider.

---

## 3. Explication simple

Imaginez un marché, un samedi matin. Vous voulez savoir « ce que vend le marché ». Vous ne pouvez pas tout voir : vous vous postez à **un** étal, pendant **une** heure, et vous notez chaque vente sur un carnet.

- **Le marché entier, toutes les ventes de toutes les journées** : c'est la **population** — l'ensemble que vous aimeriez décrire.
- **Les ventes que vous avez réellement notées** : c'est l'**échantillon** — la partie visible, celle sur laquelle vous calculez.
- **Chaque vente notée sur une ligne du carnet** : c'est un **individu** statistique — l'unité sur laquelle on compte. Pas le client, pas l'objet vendu : *la vente*, si c'est elle que vous avez décidé de compter.
- **Une caractéristique que vous notez à chaque fois** (le montant, l'étal, l'heure) : c'est une **variable**.
- **Une valeur prise par cette variable** (« légumes », « 1 500 FCFA ») : c'est une **modalité**.
- **Combien de fois apparaît une modalité** : c'est l'**effectif** ; ramené au total, c'est la **fréquence**.

Tout le reste du manuel applique ce petit vocabulaire. Un tableau de statistiques mal lu est presque toujours un tableau où l'individu n'était pas celui que le lecteur imaginait.

---

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **Population — population** | L'ensemble complet des choses que l'on voudrait décrire. | La confondre avec le fichier ouvert : le fichier n'est souvent qu'un extrait. |
| **Individu — statistical unit / record** | L'unité que l'on compte : une ligne, un ticket, un client, un mois, selon la décision prise. | Compter des lignes en croyant compter des clients. |
| **Échantillon — sample** | La partie réellement observée de la population. | Oublier de dire comment il a été choisi : le mode de choix décide de ce qu'il autorise. |
| **Recensement — census** | Observer toute la population, sans échantillon. | Croire qu'un gros fichier est un recensement : 240 000 lignes peuvent n'être qu'un mois. |
| **Variable** | Une caractéristique relevée pour tous les individus (une colonne). | Appeler « variable » un identifiant : il varie, mais ne mesure rien. |
| **Modalité — value / category** | Une valeur possible d'une variable (« Peinture », 0,04, vrai). | Compter les modalités comme des individus. |
| **Effectif — count / frequency count** | Combien d'individus prennent cette modalité. | Donner un effectif sans dire sur combien de lignes il porte. |
| **Fréquence — relative frequency** | Effectif divisé par l'effectif total, en pourcentage. | Arrondir chaque ligne à l'entier et obtenir 99 % ou 101 % au total. |
| **Cardinalité — cardinality** | Nombre de modalités distinctes d'une variable. | Une cardinalité de 1 dans un extrait : elle interdit la comparaison qu'on voulait faire. |
| **Représentativité — representativeness** | Propriété d'un échantillon qui ressemble à sa population sur les variables qui comptent. | La revendiquer sans la discuter : elle s'examine, elle ne se décrète pas. |

---

## 5. Cours approfondi

### 5.1 Les cinq questions qui précèdent tout calcul

Avant la moindre formule, un professionnel écrit cinq lignes. Sur le fichier de travail de ce module — l'extrait nettoyé de 480 lignes du magasin 5 pour 2025 — cela donne :

1. **Quelle population ?** Les ventes du magasin 5, sur l'année 2025, telles que la caisse les a enregistrées.
2. **Quel individu ?** La ligne de ticket (un article facturé), parce que le fichier est livré à ce grain.
3. **Quel échantillon ?** 480 lignes, construites à raison de 40 lignes par mois, dans un fichier complet de 240 000 lignes propres.
4. **Quelles variables ?** 13 colonnes : `n_ticket`, `date`, `heure`, `magasin`, `vendeur`, `client`, `produit`, `categorie`, `quantite`, `prix_unitaire_ht`, `remise`, `montant_ht`, `montant_ttc`.
5. **Quelles modalités compte-t-on ?** Selon la question : 7 catégories, 4 vendeurs, 145 produits, 372 clients distincts (hors vides), 1 magasin.

Ces cinq lignes occupent trois minutes. Elles suppriment la moitié des allers-retours d'une analyse, et elles se recopient mot pour mot dans la note qui accompagne le chiffre.

### 5.2 Population et échantillon : deux noms, un écart à déclarer

> **Définition.** **Population** — *population* — l'ensemble complet des individus que l'on voudrait décrire. Elle
> est presque toujours inatteignable : ce que l'on a sous la main est un fichier, un mois, un magasin.

> **Définition.** **Échantillon** — *sample* — la partie réellement observée de la population, sélectionnée par une
> règle. Ce qui la rend utilisable n'est pas sa taille mais sa **description** : sans la règle de sélection écrite,
> aucun pourcentage ne peut être discuté, seulement cru.

Un échantillon n'est pas « un petit morceau au hasard des fichiers » : c'est un morceau **choisi par quelque chose**. Ici, le choix est explicite : 40 lignes par mois, en prenant les premières du mois après tri par date. Ce mode de fabrication a une conséquence que vous devez savoir énoncer : la **répartition mensuelle est forcée** — chaque mois pèse le même poids (40 lignes sur 480, soit 8,3 %), alors que dans la population les mois ne pèsent pas pareil. Un graphique de la répartition par mois sur cet extrait est donc **faux d'office** sur une seule question : « quel mois vend le plus ? » — et parfaitement utilisable sur une autre : « comment se répartissent les catégories de produits ? ».

> **À retenir.** La bonne question n'est jamais « l'échantillon est-il petit ? » mais « **sur quoi le mode de fabrication fausse-t-il le raisonnement ?** ». Un échantillon de 480 lignes bien décrit répond à six questions ; un échantillon de 240 000 lignes mal décrit n'en répond correctement à aucune.

### 5.3 L'individu n'est pas la ligne

Le fichier contient 480 lignes et 316 tickets : un ticket porte en moyenne 1,52 ligne, certains jusqu'à 4. Les deux objets sont légitimes, mais ils ne répondent pas aux mêmes questions, et ils ne donnent pas les mêmes pourcentages.

| Question | Individu à compter | Ce que l'on obtient |
|---|---|---|
| Combien d'articles sont facturés ? | la ligne | 480 |
| Combien de ventes (paniers) ? | le ticket | 316 |
| Quelle part des ventes comportent plusieurs articles ? | le ticket | 104 sur 316, soit 32,9 % |
| Quelle catégorie domine le catalogue vendu ? | la ligne (ou le montant, si l'on pondère) | Matériaux, 143 lignes, 29,8 % |

Un même fait, deux énoncés justes : les Matériaux sont la première catégorie **en lignes** (143 sur 480) ; ils ne le sont pas forcément **en montants**, et encore moins en nombre de tickets contenant au moins un article de la catégorie. La règle du métier : **on nomme l'individu avant de nommer le pourcentage**.

> **Définition.** **Tirage — sampling** — la règle, écrite et reproductible, qui a sélectionné les individus de
> l'échantillon dans la population. Elle se note avec son effet attendu : « 40 premières lignes par mois après tri
> par date » dit à la fois ce qui a été pris et ce que cela écrase (les volumes relatifs des mois).

> **Attention.** Une phrase comme « 30 % de nos clients achètent du bois » est doublement ambiguë : 30 % des
> *lignes* ou 30 % des *clients* ? Sur cet extrait, la seconde lecture n'est même pas calculable en l'état, parce
> que la colonne `client` est vide sur 103 lignes (18 cases vides et 85 ventes au comptoir codées `0`). Nommer
> l'individu, c'est aussi vérifier qu'il est **identifiable** partout où l'on compte dessus.

### 5.4 Variable, modalité, cardinalité : trois mots, trois usages

> **Définition.** **Variable** — *variable* — une caractéristique relevée pour **tous** les individus, c'est-à-dire
> une colonne dont on peut dire en une phrase ce qu'elle mesure et dans quelle unité.

> **Définition.** **Modalité** — *value, category* — une valeur prise par la variable (« Peinture », 0,04, vide).
> Compter des modalités, ce n'est pas compter des individus : 6 remises différentes s'appliquent à 480 lignes.

Pour chaque colonne, on mesure trois choses — et elles s'écrivent dans un tableau, pas dans une conversation :

| Colonne | Nature | Modalités distinctes (mesuré) | Ce que la cardinalité autorise ou interdit |
|---|---|---|---|
| `magasin` | qualitative nominale | 1 | Aucune comparaison entre magasins : elle est impossible, pas seulement déconseillée. |
| `vendeur` | qualitative nominale | 4 | Comparaison possible, mais sur 4 individus seulement : un « classement » n'a de sens que comme constat. |
| `categorie` | qualitative nominale | 7 | Répartition exploitable ; c'est la colonne reine de ce chapitre. |
| `produit` | qualitative nominale | 145 | Listes et classements ; jamais un graphique en secteurs (145 parts illisibles). |
| `client` | identifiant (nominal, quasi-continu) | 372 distincts, 103 lignes sans client | Comptage d'objets, aucun calcul sur la valeur. |
| `remise` | quantitative discrète | 6 modalités (0 ; 0,03 ; 0,04 ; 0,07 ; 0,08 ; 0,11) | Fréquences et moyenne pondérée : deux réponses différentes, les deux utiles. |
| `quantite`, `montant_ht`, `montant_ttc`, `prix_unitaire_ht` | quantitatives | respectivement 45, 456, 456 et 323 valeurs distinctes | Résumés de position et de dispersion : le chapitre suivant. |
| `date`, `heure` | quantitatives (ordinal pour `date`) | 31 jours d'écriture, 12 mois | Analyses calendaires, à condition de se souvenir du tirage (5.2). |

Une cardinalité de **1** est une information précieuse : elle dit qu'une variable ne portera aucune réponse comparative. Sur l'extrait, `magasin` vaut « Magasin 5 — Kaya Marché » sur les 480 lignes. Écrire « le magasin 5 réalise 36 073 185 FCFA » est vrai ; en déduire qu'il est « le meilleur magasin » est une faute de logique, pas d'arithmétique.

> **Définition.** **Cardinalité — cardinality** — le nombre de modalités distinctes d'une variable. Elle ne se
> devine pas : elle se compte, et elle conditionne le choix du graphique autant que celui de la statistique.

> **Conseil professionnel.** Faites tenir ce tableau dans une page, avec trois colonnes seulement : *combien de
> modalités*, *y a-t-il des valeurs manquantes*, *quel calcul cette colonne autorise*. C'est la fiche que l'on
> demande à un analyste qui reprend un dossier laissé par un autre, et c'est ce qui vous évitera de refaire le
> travail de quelqu'un d'autre dans trois mois.

### 5.5 Effectif et fréquence : le calcul, et son total qui doit tomber juste

La fréquence d'une modalité est son effectif divisé par l'effectif total. Sur les 480 lignes :

| Catégorie | Effectif (lignes) | Fréquence |
|---|---|---|
| Matériaux | 143 | 29,8 % |
| Quincaillerie | 112 | 23,3 % |
| Consommables | 57 | 11,9 % |
| Plomberie | 57 | 11,9 % |
| Electricité | 53 | 11,0 % |
| Peinture | 34 | 7,1 % |
| Bois & panneaux | 24 | 5,0 % |
| **Total** | **480** | **100,0 %** |

Trois réflexes de rédaction, qui viennent de l'impression et non des mathématiques : on affiche les **effectifs**
à côté des pourcentages (un pourcentage sans dénominateur ne se vérifie pas) ; on garde **une décimale**, pas
trois ; on **additionne les pourcentages affichés** pour vérifier qu'ils retombent sur 100 — ici 29,8 + 23,3 +
11,9 + 11,9 + 11,0 + 7,1 + 5,0 = 100,0 ✔. Si l'arrondi faisait manquer 0,1 point, on le dirait (« totaux
légèrement différents de 100 % pour cause d'arrondi ») au lieu de retoucher une ligne au hasard pour que ça
tombe juste.

### 5.6 Deux fréquences qui se discutent, et pourquoi elles se discutent

**Les remises.** 173 lignes sur 480 portent une remise, 307 n'en portent aucune : 64,0 % des lignes sont vendues
au prix affiché. La moyenne simple des valeurs de la colonne est de 0,0185 (1,85 %), la moyenne **pondérée par les
montants** est de 0,0172 (1,72 %). Les deux chiffres sont corrects ; ils répondent à deux questions différentes —
« sur une ligne, quelle remise applique-t-on ? » et « sur un franc facturé, quelle remise concède-t-on ? ». La
seconde est celle qui intéresse le directeur financier ; la première est celle qui intéresse le responsable de
magasin. Un analyste qui ne connaît qu'une des deux se fera corriger en réunion.

**Les dates.** 480 lignes se répartissent sur 12 mois et 31 jours distincts, avec une particularité mesurée dans
le fichier brut d'origine : 55 écritures de dates différentes pour 31 jours réels (`12/01/2025` et `2025-01-12`
désignent le même jour). Le nettoyage a ramené tout le monde à l'écriture ISO ; la fréquence par jour, elle, ne
s'appuie que sur les 31 jours réellement présents dans l'extrait. Annoncer une fréquentation journalière moyenne
sans dire que le tirage a forcé 40 lignes par mois serait une conclusion tirée d'un artefact de fabrication.

> **Attention.** Le pourcentage qui suit le mot « la majorité » mérite le même contrôle que les autres. Sur ce
> fichier, « la majorité des lignes sont des Matériaux » est **faux** (29,8 %), alors que « deux lignes sur trois
> sont vendues sans remise » est **vrai** (64,0 %). Une majorité exige plus de 50 % ; une modalité *dominante*
> n'exige rien de plus que la première place, et le mot juste change le verdict.

### 5.7 Comment un échantillon se construit — et ce que chaque méthode coûte

| Méthode | Ce qu'elle garantit | Ce qu'elle écrase |
|---|---|---|
| **Tirage systématique** (une ligne sur *k*) | une couverture du temps, de la simplicité | les structures fines ; faux si la source est périodique |
| **Par strate** (40 lignes par mois, par catégorie) | que chaque groupe sera représenté | les poids relatifs des groupes — c'est le cas ici |
| **Aléatoire simple** | l'absence de biais de choix | le risque de n'avoir aucune ligne d'un petit groupe |
| **De convenance** (« les premières lignes du fichier ») | rien | tout : la représentativité n'est pas même discutée |

Le vocabulaire statistique complet de l'échantillonnage aléatoire (loi des grands nombres, intervalle
d'estimation) tient au chapitre M02.C07. Ici, l'essentiel tient en une phrase : **on choisit une méthode, on la
dit, et on écrit ce qu'elle écrase.**

> **Boîte à outils.** Compter proprement, en trois outils : tableur `=NBVAL(plage)` pour l'effectif,
> `=NB.SI(plage;modalité)/NBVAL(plage)` pour la fréquence, et la formule de comptage des valeurs distinctes
> `=SOMMEPROD(1/NB.SI(plage;plage))` ; SQL (DuckDB) `SELECT categorie, COUNT(*) AS effectif, ROUND(100.0 *
> COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS freq_pct FROM ventes GROUP BY categorie ORDER BY effectif DESC ;` ;
> Python (pandas) `df["categorie"].value_counts(normalize=True).mul(100).round(1)`. Les trois doivent rendre le
> même tableau : quand ils divergent, ce n'est pas le logiciel qui a tort, c'est le périmètre qui a bougé.

---

## 6. Exemple concret : le même fichier, trois descriptions

Un collègue remet une note qui dit : « 145 produits, 372 clients, 29,8 % de Matériaux, un magasin ». Elle est
juste et inutilisable, parce qu'elle ne dit pas ce qu'elle compte. Réécrivons la même information avec les cinq
mots du chapitre, sur le fichier de 480 lignes :

- **Population visée** : les ventes du magasin 5 en 2025, à la ligne de ticket.
- **Échantillon observé** : 480 lignes (0,2 % des 240 000 lignes propres du socle), tirées à raison de 40 lignes
  par mois après tri par date.
- **Individu** : la ligne de ticket. Les 480 lignes portent 316 tickets (1,52 ligne par ticket, maximum 4), donc
  32,9 % des tickets contiennent plusieurs articles.
- **Variables et cardinalités** : 7 catégories, 4 vendeurs, 145 produits, 372 clients distincts hors vides,
  6 modalités de remise, 1 seul magasin.
- **Fréquences retenues** : Matériaux 143 lignes (29,8 %), Quincaillerie 112 (23,3 %), sans remise 307 (64,0 %).

Deux lignes de plus que la note du collègue, et la discussion d'après-réunion devient impossible — c'est le but.

---

## 7. Démonstration pas à pas : produire la fiche d'identité statistique

Nous fabriquons le document qui accompagnera tous vos chiffres du module. Douze minutes, deux outils.

**Étape 1 — Ouvrir le bon fichier.** `01_socle_donnees/data/reference/ventes_magasin5_2025_ATTENDU.csv`
(480 lignes, séparateur `;`, encodage UTF-8 avec BOM). Importez **toutes les colonnes en texte** : c'est le
réflexe du chapitre M01.C04, il évite que le typage automatique ne décide à votre place.

**Étape 2 — L'effectif, pas le nombre de lignes affichées.** Dans le tableur, la formule `=NBVAL(A2:A481)` sur la
colonne `n_ticket` renvoie 480. Notez-le : c'est le *n* de toutes les fréquences du document.

**Étape 3 — Les individus qui ne sont pas des lignes.** `=SOMMEPROD(1/COUNTIF(A2:A481;A2:A481))` renvoie 316 :
le nombre de tickets distincts. Écrivez les deux chiffres côte à côte, avec leur nom — c'est la ligne qui tue
l'ambiguïté « on compte quoi ? ».

**Étape 4 — La cardinalité de chaque colonne.** Appliquez la même formule de valeurs distinctes aux 13 colonnes.
Le résultat doit donner, entre autres : 7 (catégories), 4 (vendeurs), 145 (produits), 372 (clients distincts non
vides), 6 (remises), 31 (jours), 1 (magasin). Si une valeur vous surprend, c'est un défaut du fichier, pas de la
formule : cherchez avant de publier.

**Étape 5 — Les effectifs par modalité.** Tableau croisé : lignes en valeur, `categorie` en ligne. Vous obtenez
143, 112, 57, 57, 53, 34, 24. Le total du croisé doit redonner 480 au FCFA et au compteur près : c'est le contrôle
de cohérence, pas une formalité.

**Étape 6 — Les fréquences.** Divisez chaque effectif par 480 et multipliez par 100, une décimale. Le total des
pourcentages affichés doit faire 100,0 %.

**Étape 7 — Le contrôle par SQL.** Dans la base du socle (`sahel.duckdb`), ou directement sur le fichier :

```sql
SELECT categorie,
       COUNT(*)                                                   AS effectif,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)         AS freq_pct
FROM read_csv('01_socle_donnees/data/reference/ventes_magasin5_2025_ATTENDU.csv', sep=';')
GROUP BY categorie
ORDER BY effectif DESC;
```

Sept lignes de requête, les mêmes sept résultats. L'exercice ne consiste pas à choisir le bon outil : il consiste
à **ne pas avoir peur de vérifier avec deux**.

**Étape 8 — Les manquants, nommés.** `=NB.EUILL(F2:F481)` sur la colonne `client` renvoie 18 lignes vides ;
85 lignes portent la valeur `0` (le comptoir). Total : 103 lignes sans client identifié, soit 21,5 % de
l'échantillon. Écrivez cette phrase dans la fiche, avec son pourcentage : un lecteur qui l'apprend en annexe la
vit comme une cachisserie.

**Étape 9 — Ce que le tirage écrase.** Une ligne, à la fin de la fiche : « 40 lignes par mois : les volumes
relatifs des mois ne sont pas comparables sur cet extrait. » C'est la seule ligne que personne d'autre écrira à
votre place.

**Étape 10 — Dater et signer.** « Fiche établie le 17/09/2026 sur le fichier `ventes_magasin5_2025_ATTENDU.csv`,
480 lignes, empreinte non calculée. » La date et le nom du fichier sont ce qui rendra le document rejouable quand
le fichier aura changé de nom, ce qui arrivera.

---

## 8. Erreurs fréquentes

| Symptôme | Cause | Correction |
|---|---|---|
| Deux services publient des pourcentages différents sur « la même » données | l'individu n'est pas le même (lignes vs tickets vs clients) | nommer l'individu dans l'en-tête de chaque tableau ; le répéter dans la légende |
| Le total des pourcentages fait 99,6 % ou 100,4 % | arrondis cumulés, présentés sans mention | garder une décimale, additionner les valeurs affichées, mentionner l'arrondi si nécessaire |
| « La majorité des ventes sont des Matériaux » | modalité dominante confondue avec majorité absolue | exiger > 50 % pour « majorité » ; sinon écrire « première catégorie » |
| Un graphique en secteurs à 145 parts | cardinalité non consultée avant de choisir le visualisation | n'utiliser le camembert qu'à partir du moment où il y a moins de 6 modalités ; sinon un classement barres |
| Une conclusion sur « le magasin le plus performant » alors que l'extrait n'en contient qu'un | variable à cardinalité 1 prise pour une variable de comparaison | vérifier les cardinalités avant toute phrase comparative ; la fiche d'identité s'en charge |
| Des effectifs qui ne somment pas au total du fichier | lignes exclues silencieusement (filtre resté actif, en-têtes mal lus) | recalculer le total et l'afficher à côté de la somme des lignes du tableau |

---

## 9. Bonnes pratiques professionnelles

- Écrivez la **phrase d'identité** en tête de tout livrable : population, individu, période, source, mode de tirage. Cinq segments, une ligne et demie.
- Un pourcentage sans dénominateur est une opinion : affichez l'effectif à côté, toujours.
- Comptez les valeurs distinctes **avant** de commenter une comparaison : une cardinalité de 1 ferme la question.
- Dites ce que le tirage écrase, en une phrase, même si personne ne l'a demandée.
- Gardez les lignes « sans client » dans les effectifs, et nommez-les : les exclure change le dénominateur et donc tous les pourcentages — ce choix doit être écrit, pas subi.
- Vérifiez un résultat par un second outil au moins une fois par dossier, et notez dans le journal que vous l'avez fait.
- Datez la fiche, nommez le fichier. Une fiche sans date est une légende urbaine.

---

## 10. Exercice guidé — la fiche d'identité, ensemble, en 25 minutes

**Contexte.** Votre responsable vous demande de « préparer le terrain » avant l'arrivée du consultant qui
audite les pratiques de données du magasin. Il veut une page, pas un rapport.

**Étape 1 — Fixer l'objet.** Question posée : *de quoi parle-t-on ?* Réponse rédigée : « Des lignes de ticket
facturées au magasin 5 de Sahel Distribution SA sur l'année 2025, telles que la caisse les a enregistrées. »
Vous venez de nommer la population et l'individu. Notez-les dans le document, pas dans votre tête.

**Étape 2 — Compter.** Vous obtenez 480 lignes et 316 tickets. *Pourquoi les deux chiffres ?* Parce que la ligne
est ce que le fichier contient, le ticket ce que le client a vécu, et que le consultant demandera lequel des deux
a servi de base au calcul. Réponse écrite : « Effectif : 480 lignes de ticket ; 316 tickets ; 1,52 ligne par
ticket en moyenne. »

**Étape 3 — Cardinalités.** 7 catégories, 4 vendeurs, 145 produits, 372 clients distincts (hors vides), 6
modalités de remise, 1 magasin. *Que dit la dernière ?* Que cet extrait ne peut rien dire sur la comparaison entre
magasins — à écrire noir sur blanc, car c'est la question que le consultant posera en premier.

**Étape 4 — Fréquences.** Vous dressez le tableau des catégories (143, 112, 57, 57, 53, 34, 24 lignes), vous
ajoutez la colonne des pourcentages, vous vérifiez que le total tombe à 100,0 %. Vous ajoutez une ligne
« sans remise : 307 lignes, 64,0 % », parce que la remise est la variable qui fâche.

**Étape 5 — Les manquants.** 18 lignes sans client, 85 lignes au comptoir codées `0`. Décision écrite : elles
restent dans les effectifs (elles sont des ventes réelles), mais elles sortent de toute analyse par client — et
donc, cette analyse-là porte sur 377 lignes, pas 480.

**Étape 6 — La phrase de garde.** « Extrait construit à raison de 40 lignes par mois : les volumes mensuels ne
sont pas comparables entre eux sur ce fichier. » Cette phrase vaut à elle seule la fiche : elle désarme la
mauvaise question au lieu de la traiter.

*Résultat attendu :* une page de dix lignes, sans un seul calcul de moyenne. Le consultant gagnera vingt minutes,
vous en gagnerez trois semaines de crédibilité.

---

## 11. Exercices autonomes

**Exercice 1.1 (★) — Les cinq lignes.** Sur le fichier de 480 lignes, rédigez la phrase d'identité : population,
individu, échantillon, variables, tirage. *(attendu : 480 lignes, 316 tickets, 13 colonnes, 2025, 40 lignes par
mois après tri par date ; la phrase fait 4 à 6 lignes)*

**Exercice 1.2 (★) — Deux dénombrements, deux questions.** Calculez, en un tableur : le nombre de lignes, le
nombre de tickets, le nombre de tickets comportant au moins deux lignes, et leur part. *(attendu : 480 · 316 ·
104 · 32,9 %)*

**Exercice 1.3 (★) — Le tableau des catégories.** Effectifs et fréquences des 7 catégories, avec une décimale et
la ligne de total. *(attendu : 143 ; 112 ; 57 ; 57 ; 53 ; 34 ; 24 · 29,8 % ; 23,3 % ; 11,9 % ; 11,9 % ; 11,0 % ;
7,1 % ; 5,0 % · total 480 et 100,0 %)*

**Exercice 1.4 (★★) — La modalité qui interdit la conclusion.** Une phrase par variable, pour dire ce qu'elle
permet : `magasin` (1 modalité), `vendeur` (4), `categorie` (7), `produit` (145). *(attendu : pas de comparaison
possible entre magasins ; constat seulement sur 4 vendeurs ; répartitions et classements sur les catégories ;
liste ou top-N sur les produits, jamais un graphique en secteurs)*

**Exercice 1.5 (★★) — Le dénominateur qui bouge.** Calculez la part des lignes vendues sans remise, une fois sur
les 480 lignes, une fois sur les 377 lignes portant un client identifié. Commentez les deux chiffres en deux
phrases. *(attendu : 307 / 480 = 64,0 % · 307 / 377 ≈ 81,4 % ; le second chiffre parle des ventes identifiées,
pas de l'ensemble ; changer de dénominateur sans le dire fabrique un désaccord)*

---

## 12. Correction détaillée

**Exercice 1.1.** La phrase attendue tient en six segments : « Population : les lignes de ticket facturées au
magasin 5 de Sahel Distribution SA en 2025. Individu : la ligne de ticket. Échantillon : 480 lignes, soit
0,2 % des 240 000 lignes propres du socle. Variables : 13 colonnes, de `n_ticket` à `montant_ttc`. Tirage :
40 lignes par mois après tri par date, ce qui égalise les mois. Source : `ventes_magasin5_2025_ATTENDU.csv`,
fiche établie le 17/09/2026. » Ce qui est noté : la présence des cinq noms, et l'unité (lignes, pas ventes).

**Exercice 1.2.** Trois formules : `=NBVAL(A2:A481)` → 480 ; la formule de valeurs distinctes sur `n_ticket` →
316 ; `=NBVAL(A2:A481)/316` → 1,52. Pour les tickets multi-lignes, un tableau croisé de `n_ticket` en lignes avec
« nombre » en valeur, puis un comptage des clés dont l'effectif dépasse 1 → 104, soit 104 / 316 = 32,9 %. Le
piège classique : compter les lignes supplémentaires (480 − 316 = 164) au lieu des tickets, ou diviser 104 par 480 au lieu
de 316 — le dénominateur suit l'individu choisi, jamais la commodité : 104 tickets sur 316 ne se racontent pas « sur 480 ».

**Exercice 1.3.** Le tableau doit afficher, dans cet ordre décroissant : Matériaux 143 (29,8 %), Quincaillerie
112 (23,3 %), Consommables 57 (11,9 %), Plomberie 57 (11,9 %), Electricité 53 (11,0 %), Peinture 34 (7,1 %), Bois
& panneaux 24 (5,0 %), total 480 (100,0 %). Deux égalités à vérifier : 143 + 112 + 57 + 57 + 53 + 34 + 24 = 480
✔, et 29,8 + 23,3 + 11,9 + 11,9 + 11,0 + 7,1 + 5,0 = 100,0 ✔. À noter aussi : deux catégories sont à égalité
parfaite à 57 lignes — un classement qui les départagerait sur la deuxième décimale inventerait une hiérarchie.

**Exercice 1.4.** Attendu, une ligne par variable : `magasin` — une seule modalité, donc aucune conclusion
comparative possible sur cet extrait (la comparer supposerait d'ouvrir le fichier complet) ; `vendeur` — 4
modalités, un classement est descriptible mais instable (retirer un vendeur change tout) ; `categorie` — 7
modalités, répartitions et classements exploitables, graphique en barres horizontales ; `produit` — 145 modalités,
on liste, on ne figure pas, et l'on travaille en top-N avec la part restante explicite (« autres : X lignes »).

**Exercice 1.5.** 307 / 480 = 64,0 % ; 307 / 377 ≈ 81,4 %. Commentaire attendu : le premier chiffre décrit
*l'ensemble des ventes* ; le second ne décrit que *les ventes où l'on sait à qui*, et il est mécaniquement plus
élevé parce que le comptoir, où la remise est rare, a quitté le dénominateur. Un chiffre qui bouge de 17 points
par un changement de dénominateur doit être accompagné de son dénominateur à chaque fois qu'il est cité — sinon
c'est un argument, plus une mesure.

---

## 13. Mini-projet M02.P1 — « La fiche d'identité statistique du fichier complet » (50 min)

**Commande.** Établissez, pour le fichier `01_socle_donnees/data/reference/ventes_propres.csv` (240 000 lignes,
4 années, 6 magasins), la fiche d'identité statistique au format du chapitre : population, individu, période
couverte, variables et cardinalités, trois fréquences commentées, manquants nommés, tirage, date et source.

**Livrables numérotés.** (1) la fiche, une page ; (2) le tableau des effectifs et fréquences d'une variable au
choix ; (3) le script ou les formules utilisés, collés en fin de page ; (4) deux phrases sur ce que la fiche
empêche de conclure à tort.

**Barème (20 points, seuil 13).** Fiche complète, cinq rubriques (5) · effectifs et fréquences justes, total à
100,0 % (4) · cardinalités mesurées et non recopiées (3) · manquants chiffrés et nommés (3) · phrase sur le tirage
ou la couverture (2) · traçabilité des calculs (2) · style : une page, pas deux (1). Le tout en 50 minutes
chrono : si vous dépassez, votre tableau contient plus de lignes que nécessaire.

---

## 14. Résumé du chapitre

Statistiquement, un fichier ne dit rien de lui-même : il faut écrire ce qu'il représente. Cinq mots suffisent —
population, individu, échantillon, variable, modalité — et un calcul : l'effectif, puis sa fréquence. Les trois
quarts des disputes de chiffres naissent d'un individu mal nommé (lignes contre tickets contre clients), non d'une
formule ratée. La cardinalité se mesure avant de commenter : à 1 modalité, la comparaison est fermée ; à 145, le
graphique en secteurs est fermé. Les manquants restent dans le dénominateur tant qu'on ne l'écrit pas
autrement, et un pourcentage ne se cite jamais sans son dénominateur. Enfin, le mode de tirage s'énonce avec son
effet : ici, 40 lignes par mois signifient que les mois ne pèseront pas leur poids réel. Ce chapitre ne vous a
pas appris à calculer une moyenne : il vous a appris à ne pas en calculer une sur le mauvais objet, ce qui est
plus rare et plus utile.

---

## 15. À retenir

> **À retenir.**
> 1. **Nommer l'individu avant tout pourcentage** : 480 lignes, 316 tickets, 372 clients — trois chiffres, tous
>    justes, trois questions différentes.
> 2. **La population n'est pas le fichier** : l'extrait de 480 lignes couvre 0,2 % des 240 000 lignes propres, et
>    le dire est ce qui rend le chiffre défendable.
> 3. **Une fréquence = un effectif ÷ un dénominateur** : citez les deux, vérifiez que les pourcentages additionnés
>    retombent sur 100,0 %.
> 4. **La cardinalité commande** : à 1 modalité aucune comparaison, à 145 aucun camembert, à 7 toutes les
>    répartitions.
> 5. **Le tirage s'écrit avec son effet** : « 40 lignes par mois » interdit de conclure sur le poids des mois.

> **À retenir (le réflexe qui vaut une heure de réunion).** Une phrase d'identité en tête de chaque livrable :
> *de quoi, sur quoi, sur quelle période, extrait comment, source laquelle*. Elle ne coûte rien à écrire et rend
> le chiffre incontestable sur la forme — ce qui, dans une entreprise, est la moitié du travail.

---

## 16. Évaluation formative (auto-correction, 8 min)

1. Un fichier contient 480 lignes et 316 tickets. Que compte-t-on si l'on écrit « notre client moyen achète pour
   114 156 FCFA » ?
2. Vrai ou faux : « puisque `magasin` ne contient qu'une valeur dans l'extrait, on peut comparer le magasin 5 aux
   autres en divisant par cinq ».
3. Un tableau de fréquences affiche 99,6 % au total. Deux causes possibles ?
4. Sur 307 lignes sans remise sur 480, puis sur 377 lignes identifiées : pourquoi les deux pourcentages (64,0 %
   et 81,4 %) sont-ils tous les deux corrects, et lequel cite-t-on au directeur financier ?
5. Citez les cinq rubriques de la phrase d'identité, sans relire.

**Question ouverte.** Un collègue écrit : « 29,8 % de nos ventes concernent les Matériaux, c'est donc la
majorité de notre activité ». Reprenez la phrase en une ligne, en corrigeant ce qui doit l'être et en ajoutant ce
qui manque.

---

**Corrigé de l'évaluation formative.**

1. **Rien de proprement dit.** 114 156 FCFA est le montant *moyen par ticket* (moyenne des 316 tickets) : le
   chiffre est un panier moyen, pas un « client moyen ». L'individu est le ticket ; il faut le dire, sinon le
   lecteur sur-achète (il croit savoir ce qu'un client dépense alors qu'il lit ce qu'un ticket contient).
2. **Faux.** Diviser une valeur unique par cinq invente quatre magasins. Soit on ouvre le fichier complet (240 000
   lignes, 6 magasins), soit on écrit « sur le seul magasin 5 ».
3. **Arrondis cumulés** (le cas bénin : mentionner l'arrondi suffit) ou **lignes perdues dans le tableau**
   (modalité exclue, filtre resté actif, une catégorie absente du croisé) — la seconde cause est une erreur, la
   première une convention. On vérifie en additionnant les effectifs, pas les pourcentages : la somme doit faire 480.
4. Parce que les deux dénominateurs décrivent deux ensembles différents : *toutes les ventes*, et *les ventes où
   l'on sait à qui*. Au directeur financier, on cite le second **en nommant** le premier (« sur les 377 lignes
   identifiées, 81,4 % ; l'ensemble des lignes donne 64,0 % ») : un chiffre financier se discute sur ce qu'il
   couvre avant de se discuter sur sa valeur.
5. Population · individu · échantillon et période · variables et cardinalités · tirage et source (datés).
   *Question ouverte* — Réponse attendue : « les Matériaux représentent 143 lignes sur 480, soit 29,8 % : c'est la
   première catégorie, pas une majorité (qui exige plus de 50 %) ; le chiffre porte sur les lignes de l'extrait
   2025 du magasin 5, pas sur l'activité de l'entreprise ».
