# Module M14.C03 — Transformer avec Power Query : les quinze gestes

**Outils : DuckDB 1.5.5 (exécuté) ; pandas (non requis). Power BI Desktop et son éditeur de requête
sont *cités* — l'outil n'est pas installé dans cet atelier (règle §1.5). Tout ce qui peut être mesuré
l'est en SQL, et l'est à chaque exécution de `tools/mesures_M14.py`.**

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **exécuter les quinze gestes** de l'éditeur de requête dans l'ordre où ils se présentent — de la
   source au paramètre — et savoir lesquels sont **irréversibles** pour la suite du modèle ;
2. **convertir des types sans casser le rapport** : un montant lu comme du texte, une date lue comme
   un nombre, un vide devenu zéro — trois défauts que le socle porte et que le chapitre chiffre ;
3. **nettoyer des libellés** au bon endroit : **16** écritures de familles pour **7** familles, dont
   **12** lignes qui portent un espace en trop, et la règle qui évite de refaire le travail à chaque
   rapport ;
4. **regrouper au bon grain** : **240 000** lignes de vente groupées par produit, magasin et mois
   donnent **33 323** lignes — **7,2** fois moins, et un grain écrit noir sur blanc dans la requête ;
5. **nommer ses étapes et son travail**, et reconnaître les trois défauts de requête qui coûtent des
   performances sans jamais lever d'erreur.

---

## 2. Pourquoi cette notion est importante

Power Query n'est pas un nettoyeur de fichiers : c'est le **journal** de la fabrication de la donnée.
Chaque geste y est écrit, ordonné, rejouable, et lisible par quelqu'un d'autre — à condition d'avoir
été nommé. C'est la différence entre un rapport qui se répare en cinq minutes et un rapport qu'on
refait parce que personne ne sait ce qui a été fait.

Le chapitre précédent a fait entrer la donnée ; celui-ci la rend **utilisable**. Trois enjeux, tous
mesurés sur le fil rouge.

**Le premier est la conversion.** Une colonne de montants lue comme du texte ne s'additionne pas ; une
colonne de dates lue comme du texte ne se compare pas ; un vide converti en zéro fait baisser une
moyenne sans prévenir. Sur le socle, les **2** prix manquants — les produits d'identifiants `62` et
`149` — sont **vides**, et c'est volontaire : un rapport qui les traite mal affiche des erreurs ou
des totaux faux.

**Le deuxième est le nettoyage des libellés.** Le référentiel du fil rouge écrit la même famille de
quatre façons : **16** libellés source pour **7** familles réelles, et **12** lignes qui portent un
espace en trop en fin de valeur. Sans nettoyage, un rapport par famille affiche **16** lignes au lieu
de **7**, et la famille la plus grosse du réseau — Matériaux — arrive en cinquième position au lieu de
la première, parce que son montant est partagé entre quatre écritures.

**Le troisième est le grain du regroupement.** Grouper **240 000** lignes de vente par produit,
magasin et mois fabrique une table de **33 323** lignes que le rapport lit **7,2** fois plus vite — et
surtout, ce regroupement **écrit** le grain dans la requête. Une table dont le grain est écrit ne peut
plus être additionnée par erreur avec une table dont le grain diffère : c'est la leçon de M13, portée
dans l'outil.

---

## 3. Explication simple — la cuisine et la fiche recette

Cuisiner pour dix personnes et servir un dessert ressemblent à deux activités différentes ; en
réalité, ce sont deux temps d'un même travail, et la différence tient dans une fiche.

La **préparation** se fait en gestes : laver, éplucher, couper, doser, assaisonner. Personne ne mange
à ce moment-là, et pourtant c'est là que se décide le goût. La **fiche recette** note chaque geste dans
l'ordre, avec sa quantité, pour que le plat puisse être refait demain par quelqu'un d'autre.

L'éditeur de requête est exactement cela, et il a une qualité que la cuisine n'a pas : chaque geste
est **conservé** et peut être **rejoué**. La requête du rapport n'est pas une photo du fichier après
nettoyage, c'est la liste des opérations qui produisent cette photo. Le jour où le fichier source
change, on corrige un geste, pas le résultat.

Trois conséquences pratiques, qui organisent tout le chapitre.

**Un geste mal placé coûte à chaque exécution.** Filtrer après avoir converti toute une colonne, c'est
laver dix kilos de légumes pour n'en cuisiner qu'un : l'outil a travaillé pour rien, et il le refera à
chaque actualisation.

**Un geste non nommé est un geste perdu.** « Personnalisée1 » ne dit rien à personne, y compris à vous
dans trois mois. « Prix — conversion en nombre, vide conservé » se relit.

**Un geste irréversible se décide une fois.** Supprimer une colonne, agréger, dépivoter : ces gestes
changent la nature de la table. Les faire trop tôt ferme des portes ; les faire trop tard alourdit tout
ce qui suit.

---

## 4. Vocabulaire essentiel

| Terme | Ce qu'il désigne exactement | Où il se règle |
|---|---|---|
| **Étape** | une opération enregistrée dans la requête, avec son nom | volet des étapes |
| **Type** | la nature d'une colonne : texte, entier, décimal, date, booléen | en-tête de colonne |
| **Locale** | la convention de date et de nombre du fichier : jour/mois ou mois/jour, virgule ou point | paramètres du fichier |
| **Colonne conditionnelle** | une colonne calculée par des cas | onglet ajouter une colonne |
| **Colonne personnalisée** | une colonne calculée par une expression | onglet ajouter une colonne |
| **Dépivoter** | transformer des colonnes en lignes | onglet transformer |
| **Regrouper** | agréger des lignes selon une clé | onglet transformer |
| **Fusionner** | joindre deux requêtes selon une clé | onglet accueil |
| **Requête de référence** | une requête qui part d'une autre sans la modifier | clic droit |
| **Paramètre** | une valeur nommée réutilisée dans les requêtes | gestionnaire de paramètres |
| **Fonction** | une requête transformée en règle appliquée à chaque élément | clic droit sur une requête |
| **Étape orpheline** | une étape qui ne sert à rien et que rien ne justifie | à supprimer |

> **Définition.** Une **étape** est une opération enregistrée dans la requête : elle a un nom, une
> position et un effet. La liste des étapes est le vrai contenu d'une requête — le tableau qu'on voit à
> l'écran n'en est que le résultat. C'est pour cela qu'une requête se relit, se corrige et se
> documente, alors qu'un fichier nettoyé à la main ne se relit pas.

> **Définition.** La **locale** est la convention d'écriture des dates et des nombres du fichier
> source. Un fichier américain écrit le mois avant le jour et le point avant les décimales ; un fichier
> francophone fait l'inverse. Une locale mal déclarée transforme le 3 avril en 4 mars, sans erreur,
> sans avertissement, et avec des ventes déplacées d'un mois dans tous les rapports.

> **Définition.** **Dépivoter** (*unpivot*) consiste à transformer des colonnes en lignes : un tableau
> qui porte douze colonnes de mois devient un tableau de deux colonnes — le mois et la valeur. La
> table obtenue est plus longue et beaucoup plus utile : elle se filtre, se groupe et se compare comme
> n'importe quelle table, alors que la version en colonnes ne se lit qu'à l'œil.

> **Définition.** **Regrouper** consiste à remplacer un ensemble de lignes par une ligne par clé, avec
> des agrégats. C'est le geste qui **réduit** le volume et qui **fixe le grain** : après un
> regroupement par produit, magasin et mois, chaque ligne représente un produit, un magasin et un mois,
> et le nom de la requête doit le dire.

> **Définition.** Une **requête de référence** est une requête qui part du résultat d'une autre sans la
> modifier. Elle évite le défaut classique : deux requêtes qui refont les mêmes étapes de nettoyage et
> qui finissent par diverger. On nettoie une fois, on référence deux fois.

> **Attention.** Ne confondez pas **fusionner** et **ajouter**. Fusionner joint deux tables côte à
> côte, selon une clé commune, et change le nombre de lignes si la clé n'est pas unique ;
> ajouter empile deux tables de même structure, et additionne les lignes. Une fusion faite sur une clé
> non unique multiplie les lignes — c'est le mécanisme que M13 a mesuré : **44** fois le chiffre
> d'affaires sur une jointure trop large.

> **Attention.** Un type déclaré trop tôt casse la requête : si vous convertissez une colonne en
> nombre avant d'avoir traité ses vides et ses textes parasites, l'étape échoue sur la première ligne
> fautive — et l'outil refusera de rafraîchir le rapport, pas seulement la ligne. Convertissez après
> avoir nettoyé, pas avant.

> **Dans les faits.** Trois gestes de ce chapitre portent l'essentiel du gain : le **nettoyage des
> libellés** (**16** écritures ramenées à **7** familles, **12** lignes corrigées), le **regroupement**
> (**240 000** lignes vers **33 323**, **7,2** fois moins) et le **retrait des colonnes inutiles**
> (**6** colonnes sur **17**, **37,5 %** du poids de la table mesuré au chapitre précédent).

---

## 5. Cours approfondi

### 5.1 Les quinze gestes, dans l'ordre où ils arrivent

| # | Geste | Ce qu'il fait sur le fil rouge | Réversible ? |
|---|---|---|---|
| 1 | Source | ouvrir un fichier, un dossier ou une base | oui |
| 2 | Promouvoir les en-têtes | la première ligne devient le nom des colonnes | oui |
| 3 | Modifier le type | entiers, décimaux, dates, texte, booléens | oui |
| 4 | Remplacer les valeurs | les écritures multiples d'une même famille | oui |
| 5 | Colonne conditionnelle | le drapeau de retour, la classe de panier | oui |
| 6 | Fractionner une colonne | `annee_mois` devient une année et un mois | oui |
| 7 | Colonne personnalisée | le premier jour du mois, la date fiscale | oui |
| 8 | Supprimer des colonnes | les **6** colonnes que le rapport ne lit pas | **non** |
| 9 | Renommer | des noms lisibles, et identiques d'une requête à l'autre | oui |
| 10 | Filtrer les lignes | écarter les statuts annulés, les lignes vides | **non** |
| 11 | Dépivoter | les **12** colonnes de mois deviennent **12** lignes | **non** |
| 12 | Regrouper | le fait mensuel fabriqué depuis les lignes de vente | **non** |
| 13 | Fusionner | le coût d'achat entre dans le référentiel produit | **non** |
| 14 | Ajouter | empiler deux extractions d'années successives | oui |
| 15 | Paramètre et fonction | le chemin devient un paramètre, le dossier une fonction | oui |

Six gestes sur quinze sont **irréversibles dans la pratique** : on peut toujours revenir en arrière
dans la liste des étapes, mais une fois que les tables suivantes sont construites sur le résultat, la
décision est prise. C'est pourquoi ils se décident en connaissance de cause — et jamais « pour voir ».

### 5.2 Convertir les types sans casser le rapport

Le socle porte exactement les trois cas qui font échouer une conversion.

| Cas | Ce que porte le socle | Ce qui se passe sans traitement | Le geste juste |
|---|---|---|---|
| Prix manquants | **2** produits sans prix de vente (identifiants `62` et `149`) | une erreur de conversion, ou un zéro silencieux | conserver le vide, et l'expliquer dans la page d'aide |
| Textes dans une colonne de nombres | une valeur écrite avec une espace, ou un tiret | l'étape échoue, et le rapport ne s'actualise plus | nettoyer avant de convertir |
| Dates en texte | les **1 339** jours du calendrier, écrits au format international | un tri alphabétique, et un ordre faux | déclarer le type de date **avec** sa locale |
| Espaces parasites | **12** lignes de libellés en portent un en fin de valeur | **2** familles de plus que la réalité | nettoyer, puis vérifier le nombre de valeurs distinctes |

**La règle des trois temps :** *nettoyer*, *convertir*, *vérifier*. Le troisième temps est celui qu'on
saute, et c'est le seul qui prouve quelque chose : après conversion, on compte les valeurs distinctes
d'une colonne de libellés (**7** familles, pas **16**), on regarde le minimum et le maximum d'une
colonne de dates (**2023-01-01** à **2026-08-31**), et l'on vérifie qu'un montant total ne change pas
d'un iota.

### 5.3 Le nettoyage des libellés, au bon endroit

Le défaut du fil rouge est celui de toutes les organisations : la même réalité écrite de plusieurs
façons. Sur le socle, la famille **Matériaux** apparaît sous quatre écritures, dont une avec un espace
en trop ; au total, **16** libellés source pour **7** familles réelles, et **12** lignes à corriger.

Trois endroits possibles pour corriger, et un seul qui tient :

| Endroit | Ce que cela donne | Verdict |
|---|---|---|
| Dans chaque rapport, à chaque visuel | le même nettoyage refait vingt fois, et divergent à la troisième | à éviter |
| Dans la requête, au moment de l'import | un seul endroit, rejoué à chaque actualisation | **le bon** |
| Dans le référentiel, à la source | la correction la plus durable, mais elle ne dépend pas de vous | à demander |

La bonne pratique professionnelle tient en deux lignes : **corriger dans la requête**, et **écrire une
demande de correction à la source** pour que le nettoyage finisse par devenir inutile. Tant que la
source n'est pas corrigée, la requête porte la cicatrice — et c'est très bien ainsi, à condition qu'elle
soit nommée.

**Le test qui prouve que le nettoyage a marché** tient en un comptage : après remplacement et
suppression des espaces, une colonne de familles doit rendre **7** valeurs distinctes. Si elle en rend
**8**, il reste une écriture non traitée — et un rapport qui affiche une famille fantôme.

### 5.4 Regrouper au bon grain, et l'écrire

Le regroupement est le geste le plus utile et le plus dangereux du chapitre. Utile, parce qu'il
**réduit** le volume : **240 000** lignes de vente groupées par produit, magasin et mois donnent
**33 323** lignes, soit **7,2** fois moins. Dangereux, parce qu'il **change le grain**, et qu'un
rapport qui somme ensuite cette table avec un fait au grain du ticket compte deux fois.

Trois règles, qui viennent directement de M13.

1. **Le nom de la requête porte le grain.** « Ventes par produit, magasin et mois » se relit ;
   « Ventes_groupées » ne dit rien.
2. **On ne regroupe que ce qu'on ne redescendra pas.** Un rapport qui a besoin du détail d'un ticket ne
   doit pas lire une table mensuelle : deux tables, deux usages, et une règle de non-addition écrite.
3. **Le regroupement n'est pas une optimisation, c'est une décision de modèle.** Sur le fil rouge, le
   rapport mensuel lit **33 323** lignes au lieu de **240 000** : c'est agréable, mais le vrai gain est
   ailleurs — le grain est **écrit**, donc vérifiable.

### 5.5 Les trois défauts de requête qui coûtent sans se plaindre

| Défaut | Ce qu'il coûte | Comment le voir |
|---|---|---|
| Convertir avant de filtrer | l'outil traite **240 000** lignes pour en garder **237 191** | les étapes de filtre sont **après** les étapes de conversion |
| Laisser un tri en fin de requête | un tri qui ne sert à aucun visuel, refait à chaque actualisation | une étape de tri qui n'est utilisée par aucune page |
| Empiler deux requêtes qui lisent la même source | la source est lue deux fois, et les deux copies divergent | deux requêtes dont la première étape est identique |

Ces trois défauts ont une propriété commune : **aucun ne casse le rapport**. Le rapport s'affiche,
les chiffres sont justes, et le temps d'actualisation double. C'est exactement le genre de problème qui
ne se corrige jamais, faute d'être vu — sauf si on le cherche.

**Le contrôle en une minute.** Ouvrez la liste des étapes de chaque requête et comptez : les étapes de
filtre viennent-elles avant les conversions ? Y a-t-il un tri que rien n'utilise ? Deux requêtes
commencent-elles par la même source ? Trois questions, trois réponses, et un modèle plus rapide.

### 5.6 Nommer, documenter, transmettre

La valeur d'une requête se mesure à la facilité avec laquelle quelqu'un d'autre la reprend. Trois
pratiques, héritées du SQL de M11 et applicables ici mot pour mot.

- **Nommer les étapes** : « prix — conversion en nombre, vide conservé » plutôt que « Type modifié ».
- **Nommer les requêtes** : par ce qu'elles portent, pas par leur origine (« Ventes par produit et
  mois », pas « Export_2026_v3 »).
- **Laisser une requête de référence** pour la documentation : une requête qui n'alimente rien et qui
  porte les contrôles — nombre de lignes, valeurs distinctes des libellés, bornes de dates. Elle ne
  coûte rien à l'actualisation, et elle prouve que le nettoyage a fonctionné.

> **Conseil professionnel.** Écrivez le journal de requête **pendant** que vous faites les gestes, pas
> après. Trois colonnes suffisent : l'étape, son effet, et la raison pour laquelle elle est là. Le
> journal se relit en cinq minutes et remplace une réunion d'une heure au premier incident.

> **À retenir.** Le nombre d'étapes d'une requête n'est pas une qualité, et sa brièveté n'en est pas
> une non plus : ce qui compte est que chaque étape soit **nécessaire** et **nommée**. Une requête de
> vingt étapes nommées se relit ; une requête de cinq étapes dont trois s'appellent « Personnalisée »
> se refait.

---

## 6. Exemple concret — la requête du fil rouge, geste par geste

**La situation.** Le rapport lit le fait de ventes et le référentiel produit. Deux requêtes, quinze
gestes, et un objectif : que le rapport par famille affiche **7** lignes justes au lieu de **16**
lignes fausses.

| Geste | Requête des ventes | Requête des produits |
|---|---|---|
| Source | le fichier d'export, séparateur virgule, en-tête en première ligne | le fichier du référentiel |
| En-têtes | rien à faire : ils sont propres | rien à faire |
| Types | date, entiers, décimaux, booléen de retour | prix en décimal, texte ailleurs |
| Remplacer | — | les **4** écritures de la famille Matériaux |
| Conditionnelle | la classe de panier (petit, moyen, grand) | l'indicateur d'activité |
| Fractionner | — | — |
| Personnalisée | le premier jour du mois | — |
| Supprimer | les **6** colonnes inutilisées | aucune |
| Renommer | `montant_ttc`, `date_vente`, `est_retour` | `famille`, `prix_vente_ht` |
| Filtrer | écarter les lignes sans date | — |
| Dépivoter | — | — |
| Regrouper | la table mensuelle : **33 323** lignes | — |
| Fusionner | — | le coût d'achat, pour la marge |
| Ajouter | — | — |
| Paramètre | le chemin du dossier | le chemin du référentiel |

**Le résultat, mesuré.** Après nettoyage, la colonne des familles rend **7** valeurs distinctes pour
**154** produits, et **0** orphelin à la fusion avec les coûts : chaque produit du référentiel trouve
son coût. Le rapport par famille affiche alors **7** lignes, et la famille Matériaux arrive à sa place
— la première — au lieu de la cinquième qu'elle occupait quand son montant était partagé entre quatre
écritures.

**Ce que le socle apporte à cet exemple.** Les trois défauts de conversion y sont présents et nommés :
**2** prix manquants (identifiants `62` et `149`), des libellés avec espace final (**12** lignes), et
un calendrier de **1 339** jours écrit en texte. La requête qui les traite est la même que celle du
projet : elle est écrite dans le dossier du module, et elle se rejoue.

---

## 7. Démonstration pas à pas — les gestes, dans l'outil

> **Boîte à outils.** Ce chapitre utilise **six** gestes de l'éditeur de requête — promouvoir les
> en-têtes, modifier le type, remplacer des valeurs, regrouper par, fusionner, et transformer une
> requête en paramètre. Les cinq premiers transforment la donnée ; le sixième rend le travail
> réutilisable. Aucun des six ne s'exécute dans cet atelier : ils se décrivent ici et se rejouent dans
> l'outil.

**Avertissement d'exécution.** Ces gestes n'ont pas été exécutés dans l'atelier (règle §1.5). Les
valeurs de contrôle sont, elles, mesurées.

**Étape 1 — Ouvrir la requête et lire ses étapes.**

1. Dans **Accueil**, choisissez **Transformer les données** plutôt que **Charger** : vous entrez dans
   l'éditeur, où les gestes se voient.
2. Le volet de droite liste les étapes déjà écrites — promotion des en-têtes, modification de type.
   Renommez-les en français et par leur effet avant d'ajouter quoi que ce soit.

**Étape 2 — Convertir proprement.**

1. Traitez les vides **avant** la conversion : sur une colonne de prix, remplacez les vides par une
   valeur décidée — et notez la décision.
2. Déclarez ensuite le type, avec la **locale** du fichier. Un fichier international écrit
   l'année d'abord : c'est le cas des exports du socle.
3. Vérifiez : une colonne de dates doit montrer une borne basse au **2023-01-01** et une borne haute au
   **2026-08-31**. Si les bornes sont absurdes, la locale ou le type sont faux.

**Étape 3 — Nettoyer les libellés.**

1. Sur la colonne des familles, commencez par supprimer les espaces de début et de fin : **12** lignes
   du socle en portent un.
2. Remplacez ensuite les écritures multiples par la forme officielle : quatre écritures de Matériaux
   deviennent une.
3. **Contrôlez par un comptage** : la colonne doit rendre **7** valeurs distinctes. Tant qu'elle en
   rend davantage, le nettoyage est incomplet.

**Étape 4 — Regrouper, et nommer le grain.**

1. Sur la requête des ventes, ouvrez **Regrouper par** : produit, magasin, mois en clé ; somme des
   quantités et des montants en agrégats.
2. Renommez la requête d'après ce qu'elle porte : « Ventes par produit, magasin et mois ».
3. Contrôlez : **240 000** lignes deviennent **33 323**. Écrivez ce nombre dans le dossier du rapport —
   c'est le grain, et il ne se devine pas.

**Étape 5 — Fusionner, et vérifier l'intégrité.**

1. Fusionnez le référentiel produit avec le fichier des coûts, sur l'identifiant de produit.
2. Choisissez la jointure qui **garde toutes les lignes de gauche**, puis comptez : le référentiel
   compte **154** produits avant comme après, et **0** ligne de coût reste orpheline.
3. Si le nombre de lignes change, la fusion est fautive : c'est le seul contrôle qui la démasque.

---

## 8. Erreurs fréquentes

| Erreur | Ce qui se passe | Le réflexe juste |
|---|---|---|
| convertir avant de nettoyer | l'étape échoue au premier texte parasite | nettoyer, convertir, vérifier |
| oublier la locale | des ventes changent de mois sans erreur | déclarer la locale avec le type |
| laisser un espace en fin de libellé | une famille fantôme apparaît dans les rapports | espace de début et de fin, puis comptage |
| remplacer des libellés dans les visuels | le même nettoyage refait vingt fois | corriger dans la requête |
| regrouper sans écrire le grain | la table est additionnée à un fait plus fin | nommer la requête d'après son grain |
| fusionner sur une clé non unique | les lignes se multiplient, le total explose | vérifier le nombre de lignes après fusion |
| trier en fin de requête | un tri refait à chaque actualisation, pour rien | trier dans le visuel, pas dans la requête |
| empiler deux requêtes sur la même source | la source est lue deux fois | une requête de base, deux références |

---

## 9. Bonnes pratiques professionnelles

1. **Nommez chaque étape par son effet**, en français : la liste des étapes est le seul document qui
   survit à votre départ.
2. **Nettoyez une fois, référencez ensuite.** Une requête de base, des requêtes de référence : jamais
   deux nettoyages parallèles.
3. **Comptez après chaque nettoyage.** Valeurs distinctes des familles, bornes de dates, nombre de
   lignes après fusion : trois comptages qui valent mieux qu'une relecture.
4. **Filtrez le plus tôt possible.** Traiter **240 000** lignes pour en garder **237 191** se paie à
   chaque actualisation.
5. **Un paramètre par chemin, une fonction par dossier.** Le rapport doit survivre au déménagement de
   ses sources.
6. **Gardez une requête de contrôle** qui n'alimente rien et qui porte les comptages : elle documente
   le modèle en s'exécutant.

---

## 10. Exercice guidé

**Énoncé.** La requête des produits du fil rouge rend **16** valeurs distinctes de familles, et la
famille Matériaux se classe cinquième. Corrigez la requête, prouvez la correction, et expliquez ce qui
change dans le rapport.

**Étape 1 — constater.** Comptez les valeurs distinctes : **16** pour **7** familles réelles, et
**12** lignes portent un espace en fin de valeur.

**Étape 2 — nettoyer.** Supprimez les espaces de début et de fin, puis ramenez les quatre écritures de
Matériaux à une seule. Rejouez le comptage : **7** valeurs distinctes.

**Étape 3 — mesurer l'effet.** Avant nettoyage, la famille Matériaux apparaît en **4** lignes distinctes
et se classe **5**ᵉ ; après, elle forme une seule ligne et reprend sa place de première famille du
réseau, avec **3 535 582 421** FCFA.

**Étape 4 — écrire la demande de correction.** Rédigez en trois lignes la demande au propriétaire du
référentiel, pour que le nettoyage devienne inutile à la source.

**Attendu.** Un comptage avant (**16**), un comptage après (**7**), la position corrigée de Matériaux,
et une demande écrite — pas une plainte.

---

## 11. Exercices autonomes

**Exercice 3.1.** Classez les quinze gestes en deux colonnes : ceux qui changent le **grain** et ceux
qui ne le changent pas. Expliquez en une phrase la conséquence de votre classement.

**Exercice 3.2.** Le socle porte **2** prix manquants, sur les produits d'identifiants `62` et `149`.
Écrivez les trois façons de les traiter — remplacer par zéro, remplacer par la médiane, conserver le
vide — et dites laquelle vous retenez pour un rapport de marge, et pourquoi.

**Exercice 3.3.** Un rapport affiche **8** lignes de familles au lieu de **7**. Écrivez le contrôle
qui prouve qu'il en manque une, puis le geste qui la corrige.

**Exercice 3.4.** Le regroupement fait passer les ventes de **240 000** à **33 323** lignes. Expliquez
ce que le rapport gagne, et ce qu'il perd — puis dites dans quel cas vous refuseriez ce regroupement.

**Exercice 3.5.** Reprenez les trois défauts de requête du chapitre et, pour chacun, écrivez la
question que vous poseriez en relisant la requête d'un collègue.

---

## 12. Correction détaillée

**Exercice 3.1.** Changent le grain : supprimer des colonnes (la table perd des attributs, pas des
lignes, mais son usage change), filtrer des lignes, dépivoter, regrouper, fusionner. Ne le changent pas :
la source, les en-têtes, les types, les remplacements, les colonnes calculées, le fractionnement, le
renommage, l'ajout, les paramètres. La conséquence est directe : les gestes de la première colonne se
décident **une fois**, en connaissance de cause, et se documentent dans le dossier du rapport.

**Exercice 3.2.** Remplacer par zéro fait baisser la marge sans qu'aucun signal ne l'indique : le coût
d'achat nul rend le produit faussement rentable. Remplacer par la médiane des autres produits est
défendable, et c'est ce que fait le socle pour reconstituer une marge de contrôle — mais la valeur
obtenue doit être **déclarée** comme estimée. Conserver le vide oblige le rapport à traiter le cas : le
produit apparaît sans marge, et l'absence se voit. Pour un rapport de marge, on garde le vide **et** on
le compte : **2** produits sur **154**, soit **1,3 %** du catalogue, et la page d'aide le dit.

**Exercice 3.3.** Le contrôle : compter les valeurs distinctes de la colonne des familles et les
comparer aux **7** familles du référentiel. Si le compte rend **8**, chercher la valeur en trop par une
requête qui liste les familles et leur nombre de produits : celle qui n'en porte qu'un petit nombre est
la candidate. Le geste : supprimer les espaces de début et de fin, puis remplacer l'écriture
différente par la forme officielle — le cas du socle se corrige exactement ainsi, avec **12** lignes
concernées.

**Exercice 3.4.** Le rapport gagne un facteur **7,2** sur la lecture de la table (**240 000** lignes
contre **33 323**), et surtout un grain **écrit** dans la requête, donc vérifiable. Il perd l'accès au
détail : plus de ticket, plus de vendeur, plus de ligne. On refuse ce regroupement dès qu'une page
affiche un détail — l'exploration par clic d'un magasin vers ses ventes, par exemple, exige le grain
du ticket.

**Exercice 3.5.** Pour la conversion avant filtrage : « les étapes de filtre viennent-elles avant les
conversions ? » Pour le tri inutile : « quel visuel utilise ce tri ? » Pour les deux requêtes sur la
même source : « pourquoi ces deux requêtes ne partent-elles pas d'une requête de référence ? » Trois
questions, posées en relecture, évitent les trois défauts — et se posent en cinq minutes.

---

## 13. Mini-projet de chapitre — le journal de requête

**Énoncé.** Produisez le **journal de requête** du rapport : pour chacune des deux requêtes
principales, la liste numérotée des étapes, avec pour chaque étape son effet, et pour les six gestes
irréversibles, la décision prise et sa raison.

**Barème indicatif** : la liste des étapes, nommées par leur effet (**6** points) · les **6** gestes
irréversibles identifiés avec leur raison (**6** points) · les trois comptages de contrôle (familles,
dates, lignes après fusion) écrits avec leur valeur (**4** points) · la demande de correction à la
source, en trois lignes (**2** points) · sur **18** points.

> **Pourquoi ce mini-projet.** Parce qu'une requête sans journal est une requête qu'on n'ose pas
> toucher. Le journal transforme un enchaînement de gestes en document de travail — et c'est exactement
> ce qu'un collègue vous demandera le jour où la source changera de format.

---

## 14. Résumé du chapitre

| Notion | Mesure du module | Ce qu'elle enseigne |
|---|---|---|
| Gestes | **15**, dont **6** irréversibles | les gestes irréversibles se décident une fois |
| Libellés source | **16** pour **7** familles, **12** lignes à corriger | le référentiel n'est pas le rapport |
| Effet du nettoyage | Matériaux de la 5ᵉ à la 1ʳᵉ place | un libellé faux change un classement |
| Prix manquants | **2** produits sur **154** (**1,3 %**) | un vide se traite, il ne se remplace pas au hasard |
| Regroupement | **240 000** vers **33 323** lignes (**7,2** fois moins) | regrouper, c'est écrire le grain |
| Fusion | **154** produits, **0** orphelin | une fusion se contrôle par un comptage de lignes |
| Défauts de requête | **3**, aucun ne casse le rapport | ce qui ne casse rien ne se corrige jamais tout seul |
| Colonnes retirées | **6** sur **17**, **37,5 %** du poids | le nettoyage est aussi une performance |

**Instrument.** `python3 tools/mesures_M14.py` recalcule les **16** libellés, les **7** familles, les
**12** lignes à corriger, le regroupement (**240 000** vers **33 323**), l'intégrité de la fusion et les
trois comptages de contrôle. Les gestes, eux, se rejouent devant votre écran.

**Le module en une ligne.** Trois chapitres ont posé l'outil, sa licence et ses sources ; celui-ci a
transformé la donnée — types, libellés, grain, fusion — et il a montré que le nettoyage n'est pas une
corvée mais une **preuve** : un comptage avant, un comptage après, et un rapport qui cesse de mentir.

---

## 15. À retenir

1. **Nettoyer, convertir, vérifier** — dans cet ordre, jamais autrement. Sur le fil rouge, la
   vérification tient en trois comptages : **7** familles, des dates de **2023-01-01** à **2026-08-31**,
   **0** orphelin après fusion.
2. **Regrouper écrit le grain.** **240 000** lignes vers **33 323** : le gain de lecture est agréable,
   mais la vraie valeur est que le grain devient **vérifiable** — et qu'on ne l'additionne plus par
   erreur avec un fait plus fin.
3. **Les défauts de requête ne se plaignent pas.** Convertir avant de filtrer, trier pour rien, lire
   deux fois la même source : trois défauts qui laissent le rapport juste et le rendent lent.

> **À retenir.** Une requête est un **document**, pas une manipulation. Elle se relit, se nomme et se
> transmet ; elle porte ses comptages de contrôle et ses décisions. Six ans après votre départ, ce
> document sera encore la seule chose qui explique pourquoi la famille Matériaux s'appelle ainsi — et
> c'est exactement ce qu'on attend d'un travail professionnel.

---

## 16. Évaluation formative

1. Citez cinq des quinze gestes de l'éditeur, et dites lesquels changent le grain.
2. Pourquoi faut-il nettoyer **avant** de convertir un type ?
3. Le socle porte **16** libellés de familles pour **7** familles. Combien de lignes doivent être
   corrigées, et que se passe-t-il si on ne le fait pas ?
4. Que se passe-t-il si la locale d'un fichier de dates est mal déclarée ?
5. Combien de lignes le regroupement produit-il, et pourquoi ce nombre compte-t-il ?
6. Quelle est la différence entre fusionner et ajouter ?
7. Comment contrôle-t-on qu'une fusion n'a pas multiplié les lignes ?
8. Citez les trois défauts de requête du chapitre et ce qu'ils coûtent.
9. Que fait une requête de référence, et quel défaut évite-t-elle ?
10. Pourquoi la demande de correction à la source est-elle un livrable, et pas une plainte ?

**Corrigé.** 1. Source, promotion des en-têtes, modification de type, remplacement de valeurs, colonne
conditionnelle, regroupement, fusion, dépivotage, paramètre — changent le grain : dépivoter, regrouper,
fusionner, filtrer, supprimer des colonnes. 2. Parce qu'une conversion échoue sur la première valeur
fautive, et qu'elle bloque l'actualisation du rapport entier. 3. **12** lignes portent un espace final ;
sans correction, le rapport affiche **16** familles et la plus grosse du réseau se classe cinquième,
son montant étant partagé entre quatre écritures. 4. Les dates se décalent sans erreur : le 3 avril
devient le 4 mars, et toutes les comparaisons mensuelles sont fausses. 5. **33 323** lignes, soit
**7,2** fois moins que **240 000** ; ce nombre est le grain de la table, et il doit être écrit. 6.
Fusionner joint deux tables selon une clé et **change le nombre de lignes** si la clé n'est pas unique ;
ajouter empile deux tables de même structure et additionne les lignes sans multiplier. 7. En comparant
le nombre de lignes avant et après : le référentiel du fil rouge compte **154** produits avant et
après, avec **0** orphelin. 8. Convertir avant de filtrer (l'outil traite **240 000** lignes pour en
garder **237 191**), trier sans usage, lire deux fois la même source. 9. Elle part du résultat d'une
autre requête sans la modifier, et évite deux nettoyages parallèles qui finissent par diverger. 10.
Parce qu'une file de demandes de correction finit par supprimer le nettoyage : la requête porte une
cicatrice tant que la source n'est pas propre, et le livrable est ce qui la rendra inutile.
