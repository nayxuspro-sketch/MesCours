# Module M03.C06 — Rechercher et assembler : RECHERCHEV et ses quatre pièges, RECHERCHEX, INDEX/EQUIV, les fonctions de texte

**Outil de ce chapitre : le tableur seul, sur le classeur de l'atelier.** Durée indicative : 4 h. Niveau : N2.

> **L'idée du chapitre.** Une recherche n'est pas une formule, c'est une **clé**. Avant de taper
> `RECHERCHEV`, on répond à trois questions : qu'est-ce qui identifie une ligne sans ambiguïté, dans quelle
> colonne de la table de référence se trouve cette clé, et que doit rendre la cellule quand la clé n'y est pas.
> Les quatre pièges de `RECHERCHEV` — l'approximation par défaut, le premier match, l'interdiction de regarder à
> gauche, l'index de colonne figé — ne sont pas des coquetteries d'interface : chacun produit un **nombre faux sans
> message**, et sur l'extrait de l'atelier ils sont tous les quatre démontrables.

> **Base de travail.** Le classeur `01_socle_donnees/data/projection/m03_classeur_atelier.xlsx`, sur les feuilles
> `ventes` (le tableau `TableVentes`, 480 lignes), `ventes_brutes` (le fichier reçu, 489 lignes en texte), et les
> quatre tables de référence `clients` (371 lignes), `produits` (154 lignes), `vendeurs` (22 lignes),
> `magasins` (6 lignes). Les fiches 17 à 20 et 22 à 23 de la feuille `Calculs` sont celles de ce chapitre.
> Séparateur point-virgule, UTF-8, franc CFA (FCFA), virgule décimale, TVA 18 %. Chiffres cités :
> `01_socle_donnees/data/reference/chiffres_cites.md`, section M03. Copie de travail : `recherches_atelier`.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

1. **Choisir la clé** d'un rapprochement, et vérifier qu'elle est unique dans les deux tables avant de rechercher.
2. **Écrire** une `RECHERCHEV` exacte, et nommer ses quatre pièges avec, pour chacun, le symptôme visible.
3. **Écrire** la même recherche en `RECHERCHEX` et en `INDEX`/`EQUIV`, et dire laquelle porter dans un classeur
   destiné à Excel 2019 ou à LibreOffice Calc.
4. **Réparer une clé en texte** avec la famille des fonctions de texte : `SUPPRESPACE`, `SUBSTITUE`, `CNUM`,
   `GAUCHE`, `DROITE`, `STXT`, `NBCAR` — dans le bon ordre.
5. **Fabriquer une clé composite** avec `&`, `CONCAT` et `JOINDRE.TEXTE`, et savoir que le zéro de padding est un
   piège de texte, pas de nombre.
6. **Rejeter** `DECALER` et `INDIRECT` comme outils de construction, et les garder comme outils de lecture.

---

## 2. Pourquoi cette notion est importante

Un analyste qui ne sait pas rechercher recopie. Un analyste qui sait rechercher mais pas choisir sa clé produit des
chiffres faux qui ont l'air vrai. La seconde situation est la plus grave des deux, et l'atelier en donne une
mesure : joindre les ventes sur le seul numéro de ticket — ce qui semble naturel, puisque chaque ligne en porte un —
rend 24 915 054 FCFA de chiffre d'affaires là où le tableau en contient 36 073 185. Il manque `11 158 131` FCFA,
soit 30,9 % du total, parce que cent quatre tickets portent deux à quatre lignes et que `RECHERCHEV` s'arrête à la
première.

Autour de cette erreur centrale, trois raisons d'apprendre le chapitre :

1. **Les tables de référence sont le métier.** Un prix, un nom de client, une catégorie : l'information vit dans
   une table, le fichier de ventes ne porte que la clé. Rapprocher, c'est lire l'entreprise — les modules suivants
   refont la même opération en SQL puis en Python.
2. **Le `#N/A` est une information.** 103 lignes ne trouvent pas leur client : 85 comptoirs sans identifiant,
   18 cellules vides. Deux causes, deux traitements ; les noyer dans un 0 fabrique un faux rapport.
3. **La recherche se branche sur la propreté du texte.** `" 10857"` ne matche pas `10857`, `9` ne matche pas `09`.
   Les fonctions de texte ne décorent pas : elles rendent la recherche possible.

---

## 3. Explication simple

Imaginez un fichier de 480 lignes où chaque ligne dit : « ticket `T05-250101-075845`, client `10857`, 3 sacs de
plâtre, 56 658 FCFA ». Ces trois nombres ne disent pas **qui** est le client, **ce que** vaut le produit au
catalogue, **où** est le magasin. Pour le savoir, on va chercher dans une autre table, avec le numéro comme étiquette
— c'est la clé.

Une recherche, c'est une valeur à trouver, une plage où la trouver, une colonne où prendre la réponse.
`RECHERCHEV` exige que la plage commence par la colonne des clés et que la réponse soit **à droite** : c'est sa
limite, et la source de trois de ses quatre pièges. `RECHERCHEX` sépare « où je cherche » et « ce que je rapporte »,
et peut donc aller à gauche, prévoir un repli, et chercher depuis la fin.

Quand la clé est un texte sale, on la nettoie d'abord : `SUPPRESPACE` ôte les espaces de bord, `SUBSTITUE` remplace
le séparateur de milliers, `CNUM` convertit le résultat. Ces trois-là ne cherchent rien : elles rendent la recherche
possible.

> **Dans les faits.** Dans un fichier de pilotage transmis par un magasin, la colonne `client` est un nombre chez
> l'un, du texte chez l'autre, et le rapprochement marche chez le premier, échoue chez le second, sans erreur de
> connexion affichée. Les équipes qui ont appris ce chapitre commencent leurs classeurs par un contrôle de clé ;
> les autres commencent leurs réunions par « ce n'est pas possible, ton total est faux ».

---

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **Clé — key** | La valeur qui identifie une ligne dans les deux tables. | Une clé non unique dans la table de recherche renvoie un arbitraire. |
| **Table de référence — lookup table** | La table qui porte l'information qu'on veut ajouter. | Oublier qu'elle peut être triée, filtrée, ou périmée. |
| **Recherche exacte — exact match** | `FAUX` en 4ᵉ argument de `RECHERCHEV`, `0` en 5ᵉ de `RECHERCHEX`. | Omettre l'argument : on bascule en approximatif, silencieusement. |
| **Recherche approximative — approximate match** | Utile pour des tranches (grilles de tarifs), exige un tri croissant. | L'employer par paresse sur une table non triée. |
| **`#N/A` — not available** | « je n'ai pas trouvé », et donc tout ce qui dépend de moi non plus. | Le masquer par réflexe avant d'avoir compté les cas. |
| **Recherche à gauche — left lookup** | Renvoyer une colonne située **avant** la colonne de clé. | Vouloir le faire en `RECHERCHEV` avec un index négatif : impossible. |
| **Clé composite — composite key** | Clé fabriquée en collant deux colonnes (`magasin & "-" & mois`). | Le zéro non rempli : `"2025-9"` n'est pas `"2025-09"`. |
| **Formule volatile — volatile** | `DECALER`, `INDIRECT`, `ALEA` : recalculées à chaque frappe. | Bâtir un classeur de 240 000 lignes avec 20 000 `DECALER`. |

> **Définition.** Une **clé unique** est une valeur qui apparaît une fois et une seule dans la table où l'on
> cherche. `clients[id_client]` en est une : 371 lignes, 371 identifiants distincts. Un `n_ticket` ne l'est pas
> dans le tableau de ventes : 480 lignes, 316 tickets, et un ticket peut porter jusqu'à quatre lignes.

> **Définition.** Une **clé typée** est une clé du même type des deux côtés. `10857` (nombre) et `"10857"` (texte)
> sont deux clés différentes pour Excel : la seconde ne trouve jamais la première, et le symptôme est un `#N/A`
> propre, sans avertissement de format.

> **Définition.** Un **repli** est la valeur renvoyée quand la recherche échoue : le 4ᵉ argument de `RECHERCHEX`,
> contre une fonction `SIERREUR` autour de `RECHERCHEV`. La différence est de coût : le repli ne masque que le
> `#N/A`, `SIERREUR` masque aussi `#VALEUR!` et `#NOM?`, donc vos fautes de frappe.

> **Définition.** Une fonction de texte **découpante** (`GAUCHE`, `DROITE`, `STXT`) compte en caractères, pas en
> significations : elle ne sait pas que le 4ᵉ caractère est un tiret. Sauf si la longueur est garantie, on découpe
> à partir d'une borne trouvée (`TROUVE`, `CHERCHE`) ou depuis la fin (`DROITE`), jamais à partir d'un numéro chance.

---

## 5. Cours approfondi

![Le voyage d'une clé : ce que RECHERCHEV rate et ce que RECHERCHEX répare](../figures/M03_C06_recherches_assemblage.svg)

### 5.1 La clé d'abord, la formule ensuite

Le tableau `ventes` porte quatre colonnes qui peuvent servir de clé, et elles ne se valent pas :

| Colonne | Cardinalité sur l'extrait | Unique ? | Sert à |
|---|---|---|---|
| `n_ticket` | 316 valeurs pour 480 lignes | non | rapprocher les lignes **d'une même vente** |
| `client` | 462 valeurs renseignées, dont 85 à zéro | non | joindre la table `clients` |
| `produit` | libellés complets | non | joindre `produits` (mais sur 40 caractères) |
| la ligne elle-même | 480 lignes | oui | ne sert à rien : le numéro de ligne n'existe pas |

La bonne question n'est donc pas « quelle formule ? » mais « **à quel grain** je veux raisonner ? ». Au grain de la
ligne, il n'y a pas de clé dans le fichier : c'est pour cela que le module M02 ajoutait un identifiant de ligne en
base de données. Au grain du ticket, `n_ticket` est la bonne clé, et elle est **propre** ici : le numéro est fabriqué
à partir du nom de fichier, donc un ticket = une vente = une à quatre lignes. Vérifiez-le avant de vous en servir :
`=NB.SI(TableVentes[n_ticket];A2)` rend le nombre de lignes du ticket de la ligne courante, et le maximum est 4.

Le ticket encode deux choses que le tableur ne voit pas : `GAUCHE(A2;3)` rend le magasin (`T05`), et les six
caractères suivants la date `250101`. Contrôlée contre la colonne `date`, cette date encodée ne donne **aucune**
divergence sur les 480 lignes de l'extrait, ni sur `240 000` lignes de la population. Ce n'est pas un résultat à
exploiter, c'est un **contrôle de santé** : il prouve que les deux écritures du monde réel n'ont pas dérivé, ce qui est
exactement ce qui casse à un réimport. Le chapitre écrit ce contrôle deux fois — avec `STXT`, il passe ; en oubliant le
`0` des mois courts, il échoue sur les 360 lignes de janvier à septembre, et cette seconde écriture est celle que
produisent les gens qui n'ont pas lu ce chapitre.

> **À retenir.** Une clé se choisit au grain où l'on veut raisonner, et se vérifie en un compteur :
> `=NB.SI(colonne;valeur)` doit rendre 1 pour la table de référence, et ce que vous décidez pour le fichier de
> faits.

### 5.2 `RECHERCHEV` : quatre pièges, quatre symptômes mesurés

`=RECHERCHEV(valeur_cherchée;table;no_colonne;FAUX)` — anglais `VLOOKUP`. Quatre choses s'y passent mal si on ne
les décide pas.

**1. Le quatrième argument omis vaut `VAI`, pas `FAUX`.** Sans lui, la recherche est approximative : Excel prend la
plus grande valeur inférieure ou égale, et **exige** que la première colonne de la table soit triée. Ici le piège ne
mord pas — `clients[id_client]` est triée par construction, et la version fautive rend la bonne réponse sur les 377
lignes à identifiant valide, 0 divergence. Triez la même table par `nom` : 233 réponses changent ; par `ville` :
toutes. Le symptôme n'est donc pas une erreur, c'est un **résultat qui devient faux quand quelqu'un d'autre trie le
fichier**. Écrivez `FAUX` ; et si l'approximation est voulue (grille de tarifs, tranches de remise), consignez le
tri attendu dans la feuille.

**2. Elle s'arrête au premier match.** Sur une clé non unique, `RECHERCHEV` renvoie la première ligne trouvée — une
décision qu'elle ne vous demande pas. L'exemple du §2 vient de là : sommer le montant attaché à chaque ticket rend
24 915 054 FCFA au lieu de 36 073 185 FCFA. Le contrôle est un compteur, pas une recherche :
`=MAX(NB.SI(TableVentes[n_ticket];TableVentes[n_ticket]))` doit valoir 1, sinon vous ne cherchez pas au bon grain.

**3. Elle ne regarde pas à gauche.** La colonne de clé est la première de la plage, et l'index ne peut être que
supérieur. Dans `produits`, la désignation est en colonne B et l'`id_produit` en A : récupérer l'identifiant à partir
du libellé est **impossible** en `RECHERCHEV`, et aucun bricolage ne change cela — décaler la plage de colonne,
c'est changer l'index, et l'index 0 n'existe pas. Les issues sont `INDEX`/`EQUIV`, `RECHERCHEX`, ou une colonne
utilitaire dans la table.

**4. L'index de colonne est un nombre, pas un nom.** Pour le prix depuis `produits`, on écrit
`=RECHERCHEV(G2;produits!B:F;5;FAUX)` ; insérez une colonne en C et la formule rend le poids — un nombre, donc rien
d'affichant. Le remède est dans l'écriture : `=RECHERCHEX(G2;produits!designation;produits!prix_vente_ht;"—")` dans
un tableau, ou `=RECHERCHEV(G2;produits!B:F;EQUIV("prix_vente_ht";produits!B1:F1;0);FAUX)` quand la version bloque.

Ajoutez le cinquième, qui n'est pas un piège de la fonction mais du fichier : **le texte ne matche jamais le
nombre**. Sur `ventes_brutes`, la colonne `client` est du texte (471 cellules écrites, 18 vides) alors que
`clients[id_client]` est numérique : partie de la feuille sale, la même recherche échoue sur les 489 lignes. Un
`#N/A` intégral est plus rassurant qu'une réussite partielle — il dit que le problème est de type, pas de données.

> **Attention.** `=RECHERCHEV(1229678;ventes!G2:J481;4;FAUX)` — la fiche 17 de `Calculs` — rend `#N/A`, et ce
> n'est pas une formule cassée : on cherche un montant (nombre) dans une colonne de libellés (texte). Avant de
> corriger une `RECHERCHEV`, lisez les deux types, pas seulement les deux plages.

### 5.3 `RECHERCHEX` : la recherche qui pose les bonnes questions

`=RECHERCHEX(valeur;table_cherchée;table_résultat;[non_trouvée];[mode];[sens])` — anglais `XLOOKUP`, disponible
dans Microsoft 365, Excel 2021 et 2024, et dans LibreOffice Calc récent ; en Excel 2019, le nom renvoie `#NOM?`.
Six arguments dont trois sont optionnels, et les trois optionnels sont précisément ce que `RECHERCHEV` ne savait
pas faire :

| Argument | Écriture courante | Ce qu'il règle |
|---|---|---|
| `non_trouvée` | `"comptoir"`, `"—"` | le `#N/A` devient une réponse choisie |
| `mode` | `0` exact (défaut), `-1` exact sinon précédent, `2` jokers | l'approximation n'est plus implicite |
| `sens` | `1` depuis le début, `-1` depuis la fin | « la dernière ligne du ticket » devient une option |

La fiche 18 est une `RECHERCHEX` complète :
`=RECHERCHEX(ventes!M356;ventes!M2:M481;ventes!G2:G481;"non trouvé")` — chercher un montant, rapporter un libellé :
« Lame de lambris 4 m — réf 2 ». Le chemin est tordu à dessein (un montant n'est pas une clé) et montre que
`RECHERCHEX` n'a que faire de l'ordre des colonnes.

Pour les 103 lignes sans client, le repli seul ne suffit pas : il confondrait le comptoir (le client n'existe pas,
et c'est normal) avec la ligne mal renseignée (elle doit être corrigée). Deux replis distincts, un seul contrôle :

```
=SI(TableVentes[@client]="";"non saisi";RECHERCHEX([@client];clients[id_client];clients[nom];"comptoir"))
```

Le `SI` traite les 18 cellules vides, le repli les 85 zéros, et l'ordre compte : une cellule vide ne cherche pas
« rien » mais la valeur 0, et trouverait un client numéroté 0 si la table en contenait un — `clients` commence à
`125`, le prochain fichier ne vous doit rien.

> **Conseil professionnel.** Quand un classeur doit tourner chez des gens dont vous ne connaissez pas la version,
> écrivez la voie `INDEX`/`EQUIV` dans les cellules et la `RECHERCHEX` en commentaire de note. Un lecteur avec
> Microsoft 365 gagne du temps ; un lecteur avec 2019 n'a pas `#NOM?` en pleine réunion.

### 5.4 `INDEX` / `EQUIV` : la voie qui marche partout

Deux fonctions au lieu d'une : `EQUIV` (anglais `MATCH`) rend la **position**, `INDEX` rend la **valeur à cette
position**. `=INDEX(clients!B:B;EQUIV(F2;clients!A:A;0))` lit le nom du client de la ligne courante, quel que soit
l'ordre des colonnes, et fonctionne dans toutes les versions, Excel comme LibreOffice.

Trois écritures du troisième argument d'`EQUIV`, à connaître parce qu'elles reproduisent les pièges de §5.2 :

| Écriture | Cherche | Contrepartie |
|---|---|---|
| `EQUIV(v;p;0)` | correspondance exacte | `#N/A` si absent |
| `EQUIV(v;p;1)` | plus grand inférieur ou égal | exige un tri **croissant** |
| `EQUIV(v;p;-1)` | plus petit supérieur ou égal | exige un tri **décroissant** |

La fiche 20 du classeur isole le maillon : `=EQUIV(MAX(ventes!M2:M481);ventes!M2:M481;0)` rend **355** — la
position dans la plage, pas le numéro de ligne : la plage commence en `M2`, donc la ligne réelle est 356. C'est de
loin la source de décalage la plus fréquente en correction, et elle est silencieuse : un `INDEX` construit sur la
mauvaise plage rend le produit du voisin, pas une erreur. La fiche 19 enchaîne les deux et retrouve le même
libellé que `RECHERCHEX`.

Deux usages d'`INDEX` qui n'ont rien à voir avec la recherche, et qu'il faut savoir parce qu'ils remplacent
`DECALER` : `=INDEX(TableVentes[montant_ttc];EQUIV(A2;TableVentes[n_ticket];0)+1)` rend la **ligne suivante** d'un
ticket, et `=INDEX(A1:M1;EQUIV("remise";A1:M1;0))` rend un nom de colonne **par son titre** — c'est avec cela
qu'on écrit une `RECHERCHEV` qui ne casse plus quand une colonne s'insère. Enfin `EQUIV` accepte les jokers en mode 0 : `=NB.SI(TableVentes[produit];"*réf 2*")` compte 223 lignes sur 480 et
`EQUIV` avec la même écriture trouve la première — 77 des 154 libellés du catalogue finissent par `réf 2`, ce qui
explique le rapport et interdit d'en conclure quoi que ce soit sur les ventes.

> **À retenir.** `INDEX`/`EQUIV` n'est pas la voie des pauvres : c'est la voie où chaque pièce se vérifie
> séparément. La position d'abord — un nombre petit, entre 1 et la taille de la plage — puis la valeur.

### 5.5 Nettoyer la clé : `SUPPRESPACE`, `SUBSTITUE`, `CNUM`

Rien de ce qui précède ne fonctionne sur le fichier reçu, et c'est le point d'articulation du chapitre. La cellule
`ventes_brutes!M2` contient `56 658` : un nombre en apparence, du texte pour Excel. La fiche 22 le répare en une
formule : `=CNUM(SUBSTITUE(ventes_brutes!M2;" ";""))` → 56 658. Trois fonctions, trois rôles :

| Fonction | Rôle sur la clé | À ne pas faire |
|---|---|---|
| `SUPPRESPACE` (`TRIM`) | ôte les espaces de bord et réduit les doubles espaces internes | croire qu'elle retire les espaces insécables |
| `SUBSTITUE` (`SUBSTITUTE`) | remplace une chaîne précise : le séparateur de milliers, le point par la virgule | confondre avec `REMPLACE`, qui écrit à une position |
| `CNUM` (`VALUE`) | convertit en nombre, **après** nettoyage | l'employer seul : `=CNUM("56 658")` rend `#VALEUR!` |
| `GAUCHE` / `DROITE` / `STXT` | découpent : 3, 6, 17 caractères du ticket | découper à position fixe sur un libellé de longueur variable |
| `NBCAR` (`LEN`) | la seule qui dit si le découpage est licite | — |

Le cas réel est la clé `client` du fichier reçu : `" 10857 "` ne matche pas `10857`. La réparation se lit de
l'intérieur vers l'extérieur, `=RECHERCHEX(CNUM(SUPPRESPACE(ventes_brutes!F2));clients!A:A;clients!B:B;"—")`, 
et
se contrôle : `=NB(CNUM(SUPPRESPACE(ventes_brutes!F2:F490)))`, validée en `Ctrl` + `Maj` + `Entrée` hors 365, doit
rendre 471 — un de moins signale une valeur non numérique que la recherche aurait avalée sans rien dire.

Sur les libellés du catalogue — 154 lignes, toutes avec le tiret « — », 77 finissant par `réf 2` — extraire la
variante par `DROITE(A2;1)` marche ici et casse au premier libellé sans variante. La version qui tient est
`=SI(SIERREUR(TROUVE("réf ";A2);0)=0;"";STXT(A2;TROUVE("réf ";A2)+4;2))` — on cherche la borne, on découpe depuis
elle, et le découpage tolère une fin de chaîne courte. Retenez la règle : **tant que vous n'avez pas compté les longueurs, on découpe depuis une borne trouvée, jamais
depuis un rang**.

> **Attention.** `SIERREUR` autour d'une recherche ne répare rien : il rend indiscernables le client absent, la
> clé restée du texte, la table mal orthographiée et votre faute de frappe sur le nom de la fonction. Avant
> d'envelopper une recherche, comptez les échecs par cause — `=NB.SI(colonne_repli;"—")`, `=NB.VIDE(clé)`, et le
> nombre de clés non numériques — et n'écrivez le repli global qu'une fois cette répartition dans la feuille.

### 5.6 `DECALER` et `INDIRECT` : comprendre pour ne pas construire

`DECALER(réf;décal_lignes;décal_colonnes;[hauteur];[largeur])` (anglais `OFFSET`) renvoie une plage décalée ;
`INDIRECT("texte")` (même nom) renvoie la plage dont le nom est écrit dans ce texte. Elles sont pédagogiques parce
qu'elles donnent à voir ce que les autres recherches font en silence : `DECALER` **construit une plage à
l'exécution**, `INDIRECT` **construit une référence à partir d'un texte**.

Trois raisons de ne pas en faire des outils de recherche :

1. Ils sont **volatils** : recalculés à chaque modification du classeur, pas seulement quand leurs paramètres
   changent. Sur 480 lignes, rien ne se passe ; sur les `240 000` de la population, un classeur à vingt mille
   `DECALER` devient inutilisable, et la cause est invisible dans les formules.
2. `INDIRECT` ne vérifie rien : renommer un onglet ne casse pas la formule, elle rend `#REF!` à la première
   ouverture — souvent après l'envoi, le pire moment.
3. `FILTRE`, `UNIQUE` (C07) et Power Query (C08) les remplacent dans la quasi-totalité des cas d'atelier.

Ses deux usages légitimes : la **fenêtre glissante** d'un tableau de suivi
(`=MOYENNE(DECALER(Cellule;0;0;3;1))`, alors que deux `INDEX` bord à bord font la même chose sans volatilité), et
la liste déroulante dont le contenu dépend d'une autre cellule. Le critère tient en une phrase : si le classeur
recalcule souvent, la plage doit exister **avant** le calcul.

### 5.7 Assembler : `&`, `CONCAT`, `JOINDRE.TEXTE`

`&` colle. `CONCAT(a;b;…)` (anglais `CONCAT`, Excel 2019+) colle une plage entière. `JOINDRE.TEXTE(sép.;vrai;…)`
(anglais `TEXTJOIN`) colle avec séparateur, et c'est la seule des trois qui sache **ignorer les vides** — le
deuxième argument, `VRAI`, vaut « ne pas émettre de séparateur pour rien ».

L'usage n'est pas le joli libellé : c'est **fabriquer la clé**. La table `objectifs` du
classeur en porte un exemple, déjà construit : la colonne `annee_mois`, écrite `2023-01`, sert de clé de
rapprochement magasin × mois, et c'est le `SOMME.SI.ENS` de la fiche 28 qui la retrouve. Fabriquez-la à la main en
collant bêtement les colonnes (`=B2&"-"&C2`) et vous obtenez `2023-1` : la clé ne matche que sur 45 des 218
lignes de la table, et l'échec est maximal précisément sur les neuf premiers mois — ceux des soldes, des
réouvertures et de la rentrée, soit tout ce qui intéresse un direction commerciale. La bonne écriture passe par
`TEXTE` : `=B2&"-"&TEXTE(C2;"00")`, qui rend `2023-01` pour les 218 lignes.

`JOINDRE.TEXTE` brille quand une liste doit tenir dans une cellule : la fiche 23,
`=JOINDRE.TEXTE(", ";VRAI;UNIQUE(ventes!H2:H481))`, rend les sept catégories dans l'ordre du fichier — dont
`Electricité` **sans accent**, exactement comme dans la donnée, ce que doit aussi rendre un critère de recherche
(§5.4 de C05). Une liste recopiée à la main est une liste fausse.

> **Définition.** Le **padding** est l'ajout de zéros non significatifs pour que deux écritures d'un même nombre
> aient la même longueur de texte. En recherche, un mois ou un jour non paddé casse une clé composite ;
> `TEXTE(valeur;"00")` est le geste, et `NBCAR` en est le contrôle (2 caractères, pas 1).

> **Boîte à outils.** `=RECHERCHEV` · `=RECHERCHEX` · `=INDEX` · `=EQUIV` pour rapprocher ; `=CNUM` ·
> `=SUPPRESPACE` · `=SUBSTITUE` · `=ARRONDI` pour réparer avant de rapprocher ; `=GAUCHE` · `=DROITE` · `=STXT` ·
> `=NBCAR` · `=TROUVE` · `=CHERCHE` pour découper ; `&` · `=CONCAT` · `=JOINDRE.TEXTE` · `=TEXTE` pour assembler ;
> `=SIERREUR` pour un repli en 2019. À éviter : `=DECALER`, `=INDIRECT` comme fondation. Trois contrôles à poser
> dans tout classeur de recherche : `=MAX(NB.SI(clé))` sur la table de référence (= 1), `=NB.COUPLÉ` ou
> `=NB.SI` du taux de recouvrement de la clé, et le `=NBCAR` maximal de toute chaîne produite par une
> concaténation de liste.

---

## 6. Exemple concret : la jointure qui marchait trop bien

Une analyste doit ajouter le nom du client à chaque ligne de vente pour préparer un mailing. Elle ouvre
`clients`, voit la colonne A pleine d'identifiants triés, écrit `=RECHERCHEV(F2;clients!A:B;2)` — sans le `FAUX`,
parce que le classeur lui a toujours bien réussi — et obtient 480 noms. Elle croise sur les 377 lignes à clé
valide : tout tombe juste. Elle livre.

Trois jours plus tard, le commercial qui exploite la liste signale que les noms sont « parfois à côté ». Le
fichier n'a pas changé ; **le tri de la table `clients` a changé**, quelqu'un l'a rangée par ville pour un envoi
postal. La recherche approximative, qui ne disait rien sur une table triée, s'est mise à raisonner sur une table
désordonnée, et elle a produit des réponses **toutes fausses** : 377 sur 377, sans un `#N/A` pour avertir.

En parallèle, elle avait rapproché les ventes des tickets : 316 « clients mailing » au lieu de 480 lignes, ce qui
lui semblait une bonne nouvelle — elle croyait dédoublonner. C'était le piège 2 du §5.2, et le nom du destinataire
venait de la première ligne du ticket, qui n'est pas le client des trois autres.

L'autopsie tient en trois lignes : le `FAUX` manquait ; la clé de regroupement n'était pas la clé du fichier ; le
contrôle de recouvrement — 377 réussites sur 462 clés renseignées — n'avait pas été écrit, parce que la formule
« marchait ».

---

## 7. Démonstration pas à pas : la feuille de rapprochement

**Objectif.** Une feuille `Rapprochement` qui ajoute à chaque ligne de `ventes` le client, le magasin et le prix
catalogue, avec le taux de recouvrement affiché en tête.

| Étape | Formule à écrire dans `Rapprochement` | Ce qui doit se lire |
|---|---|---|
| 1 | `=RECHERCHEX(ventes!F2;clients!A:A;clients!B:B;"—comptoir")` en `B2`, étirée | 377 noms, 85 `—comptoir`, 18 `—comptoir` aussi |
| 2 | `=SI(ventes!F2="";"—non saisi";B2)` en `C2` | les 18 vides séparés des 85 zéros |
| 3 | `=RECHERCHEX(ventes!D2;magasins!A:A;magasins!B:B;"inconnu")` en `D2` | le nom long du magasin 5, 480 fois |
| 4 | `=RECHERCHEX(ventes!G2;produits!B:B;produits!F:F;"hors catalogue")` en `E2` | le prix HT, et **aucun** `hors catalogue` |
| 5 | `=NB(B2:B481)` et `=NBVAL(B2:B481)` en tête | 0 et 480 : des noms sont du texte, `NB` ne dit rien |
| 6 | `=NB.SI(B2:B481;"—comptoir")` | 85, avec la mention « 18 non saisis, cf. colonne C » |

**Démonstration chiffrée du §5.2, à faire une fois en classe.** En `G2`, la version fautive
`=RECHERCHEV(ventes!F2;clients!A:B;2)` ; en `H2`, `=SI(EXACT(B2;G2);"d'accord";"différent")` étirée. Les deux
colonnes disent « d'accord » 480 fois : l'approximation est invisible tant que `clients` est triée.
Triez la copie par `ville` et relisez : 377 mentions « différent », et 103 cellules en `#N/A` — l'absence reste
bruyante, la corruption du tri est silencieuse. C'est le geste qui fait comprendre le piège, et il ne coûte que deux tris.

**Barème de la démonstration (10 points).** Repli distinct pour vide et zéro (2) · recouvrement avec son
déno­minateur (2) · `produits` joint sur la désignation sans un « hors catalogue » (2) · contrôle `NB`/`NBVAL`
commenté (2) · expérience du tri menée en copie et consignée (2).

> **Contrôles qualité du chapitre.** (1) `=MAX(NB.SI(clients[id_client];…))` vaut 1 : la clé de la table de
> référence est unique. (2) Taux de recouvrement : 377 sur 462 clés renseignées, et les 85 manquants sont le
> comptoir, pas une anomalie. (3) `produits` ne manque aucun des libellés de l'extrait : 0 `hors catalogue` sur 480
> lignes. (4) Aucune formule du classeur de l'atelier n'emploie `DECALER` ni `INDIRECT` — vérifiez-le avec la boîte
> de dialogue Rechercher, c'est une ligne de votre rapport d'atelier.

---

## 8. Erreurs fréquentes

1. **Oublier `FAUX`** (ou `0`) en recherche exacte : 0 divergence sur la table triée, 233 sur 377 après un tri par
   nom, 377 après un tri par ville. Le symptôme est une dégradation différée, jamais une erreur.
2. **Chercher avec une clé non unique** : le premier match gagne, et sur `n_ticket` cela fait perdre
   `11 158 131` FCFA de chiffre d'affaires (30,9 % du total de l'extrait).
3. **Vouloir regarder à gauche en `RECHERCHEV`** avec un index négatif : la réponse est `INDEX`/`EQUIV` ou
   `RECHERCHEX`, pas un bricolage de `DECALER`.
4. **Compter les réussites avec `NB`** sur une colonne de noms : `NB` rend 0 là où il y a 480 réponses ; le compteur
   du texte est `NBVAL`.
5. **`SIERREUR` pour taire les 103 `#N/A` d'un coup** : plus rien ne distingue le comptoir de la ligne oubliée, et
   le fichier ne peut plus être réparé — seulement regretté.
6. **Concaténer une clé de date sans padding** : `=B2&"-"&C2` ne matche que 45 lignes sur 218 dans `objectifs`.
7. **Taper le critère de mémoire au lieu de le copier** : `RECHERCHEV("électricité";…)` rend `#N/A` alors que
   53 lignes portent `Electricité` sans accent — les comparaisons sont insensibles à la casse, sensibles aux
   accents. Et `SUPPRESPACE` ne suffit pas sur un fichier bourré d'espaces insécables : le détecteur est
   `=NBCAR(A2)` sur une cellule qui paraît propre.

---

## 9. Bonnes pratiques professionnelles

1. **Une colonne d'état par recherche.** La recherche proprement dite est dans `B`, l'interprétation (« comptoir »,
   « non saisi », « trouvé ») dans `C`. Sans cette séparation, un rapport est une boîte noire.
2. **Toujours le taux de recouvrement en tête de feuille** : « 377 sur 462 », pas « tout va bien ». C'est le seul
   chiffre qui permet à un relecteur de juger le reste sans refaire les formules.
3. **Un repli par cause.** Trois causes d'échec, trois textes ; un repli unique est un mensonge poli.
4. **Écrire la voie compatible, commenter la voie moderne** dans tout fichier livré hors de votre service.
5. **Nommer les plages de référence** (`clients!A:A` → `TableClients`) : la recherche devient lisible, et le
   chapitre C07 montrera que le nom protège aussi des tris et des filtres. Jamais de tri sur une table de référence
   dans le fichier de travail — triez une copie, ou ajoutez une colonne `rang_dorigine` avant.
6. **Contrôler les longueurs avant de découper** : `=MAX(NBCAR(colonne))` dit en une formule si `STXT` est licite.

---

## 10. Exercice guidé — la feuille client complétée (35 min, /10)

**Commande.** Dans `recherches_atelier`, produisez la feuille `Fiche client` qui, pour chaque ligne de
`TableVentes`, donne : ville du client, type de client, statut du vendeur, et le prix catalogue du produit — avec
un repli par cause et les quatre contrôles du chapitre.

| Étape | Geste | Ce qui doit se lire |
|---|---|---|
| 1 | `=RECHERCHEX([@client];clients!A:A;clients!D:D;"—")` | 377 villes, 103 `—` |
| 2 | Séparez le vide du zéro : `=SI([@client]="";"non saisi";étape 1)` | 18 lignes à « non saisi » |
| 3 | `=RECHERCHEV` équivalente avec `FAUX`, à côté | mêmes 377 réponses, et **le même repli** manquant |
| 4 | Vendeur : `=INDEX(vendeurs!E:E;EQUIV([@vendeur];vendeurs!B:B;0))` | 4 statuts, aucun `#N/A` |
| 5 | Prix catalogue : `=RECHERCHEX([@produit];produits!B:B;produits!F:F;"hors catalogue")` | 480 prix, 0 « hors catalogue » |
| 6 | Contrôles en tête : `=NBVAL`, `=NB.SI(plage;"—")`, `=MAX(NBCAR(…))` sur chaque colonne fabriquée | trois lignes de chiffres commentées |

**Démarrage.** À l'étape 1, n'élargissez pas la plage en vous promettant de décaler l'index : écrivez la colonne de
réponse en clair. À l'étape 4, `EQUIV` cherche un **nom** dans `vendeurs!B:B` : si deux vendeurs portaient le même,
la recherche deviendrait silencieusement arbitraire — d'où le contrôle d'unicité, écrit une fois en haut de la
feuille (`clients` : 371 lignes, 371 identifiants distincts ; `vendeurs` : 22 lignes, 22 noms distincts). À
l'étape 5, avoir 0 « hors catalogue » est un **résultat** : le fichier de ventes a été fabriqué depuis le catalogue,
et cela ne se reproduira pas au prochain import.

**Barème (10 points).** Quatre recherches justes (4) · repli par cause et non global (2) · contrôle d'unicité de
chaque table de référence écrit en tête (2) · comparaison écrite `RECHERCHEX` / `RECHERCHEV` en une phrase (1) ·
absence de `DECALER` et d'`INDIRECT` (1).

---

## 11. Exercices autonomes

**Exercice 6.1 (★) — Les deux écritures d'une même recherche.** Sur 20 lignes de `ventes`, écrivez la ville du
client en `RECHERCHEV` avec `FAUX`, en `RECHERCHEV` sans quatrième argument, et en `INDEX`/`EQUIV`. Triez la copie
de `clients` par `nom` et relisez les trois colonnes. Lequel de vos trois résultats vous a trahi, et par quel
signe ?

**Exercice 6.2 (★) — Le recouvrement avant le tableau.** Combien de lignes de `TableVentes[client]` ne trouvent
pas leur clé dans `clients` ? Décomposez : vides, zéros, identifiants absents. Écrivez les trois compteurs, puis la
phrase de trois lignes au responsable du magasin : le nombre, la cause, la demande.

**Exercice 6.3 (★★) — Le ticket comme clé, et pourquoi il résiste.** Construisez une colonne utilitaire qui
donne, pour chaque ligne, le **nombre de lignes du même ticket**, puis une seconde qui donne le montant du ticket
entier (`SOMME.SI` sur la clé). Vérifiez que la somme des montants de tickets, divisée par le nombre de tickets,
ne rend pas la moyenne de 75 152 FCFA, et expliquez au passage ce que vaudrait la moyenne des montants de ticket.

**Exercice 6.4 (★★) — Découper sans se faire avoir.** À partir de `n_ticket` seul, fabriquez la date au format
`AAAA-MM-JJ` avec `STXT` et `DATE`, le magasin avec `GAUCHE`, et comparez à la colonne `date`. Combien de divergences
sur 480 lignes ? Reprenez en lisant le mois **sans padding** : où partent janvier à septembre ?

**Exercice 6.5 (★★★) — La clé composite des objectifs.** Rejoignez `TableVentes` et `objectifs` sur
`magasin × mois` en écrivant la clé vous-même, naïvement (`=B2&"-"&C2`) puis avec `TEXTE` : donnez le nombre de
lignes jointes dans les deux cas, et dites où ajouter **une fois** la colonne que vous êtes tenté d'ajouter 480
fois.

**Exercice 6.6 (★★★) — Réparer le fichier reçu.** Sans ouvrir `ventes`, faites tourner sur `ventes_brutes` la
recherche de ville du client, d'abord brute puis avec `CNUM(SUPPRESPACE(…))`. Comptez les `#N/A` des deux versions
et dites pourquoi la première échoue partout — en nommant **les deux** types en présence.

---

## 12. Correction détaillée

**Exercice 6.1.** Les trois colonnes sont identiques tant que `clients` est triée par `id_client` : la version sans
quatrième argument est **approximative**, et sur une clé triée croissante elle retombe juste — 0 divergence sur les
377 lignes à clé valide. Après un tri par `nom`, une seule des trois bouge : 233 noms différents sur 377 ; les deux
écritures exactes, `FAUX` comme `EQUIV(…;0)`, gardent la bonne réponse. Le signe de trahison n'est pas une erreur,
c'est un résultat **qui a bougé sans que personne ne touche aux formules** — la définition même d'une fragilité.

**Exercice 6.2.** `=NB.VIDE(TableVentes[client])` rend 18, `=NB.SI(TableVentes[client];0)` rend 85 : voilà les 103 échecs. Les
réussites se comptent en colonne utilitaire — `=NB.SI(clients!A:A;[@client])` rendu 1 ou 0, dont la somme fait 377 —
et non en une matrice que personne ne relira : les 377 identifiants renseignés sont **tous** dans `clients`. Phrase
attendue :
« 480 lignes, 462 identifiants renseignés, 377 retrouvés dans le fichier clients ; 85 ventes sont des ventes
comptoir sans identifiant et 18 lignes n'en portent pas ; écrivez `COMPTOIR` plutôt que 0, et renseignez les 18 vides ». 

**Exercice 6.3.** `=NB.SI(TableVentes[n_ticket];A2)` vaut 1 pour les lignes seules et jusqu'à 4 sur les cent quatre
tickets multi-lignes ; `=SOMME.SI(TableVentes[n_ticket];A2;TableVentes[montant_ttc])` donne le montant du ticket, et
sa moyenne vaut 114 156 FCFA (316 tickets, 36 073 185 FCFA) — pas les 75 152 FCFA de la moyenne par ligne. Deux
questions, deux dénominateurs : « panier moyen 114 156 FCFA » se défend, « vente moyenne » avec le même chiffre non.

**Exercice 6.4.** `=DATE(2000+STXT(A2;5;2);STXT(A2;7;2);STXT(A2;9;2))` reconstruit la date depuis le ticket :
**aucune divergence** sur les 480 lignes, ni sur `240 000` en population. Mais si vous lisez le mois en `1` au lieu
de `01`, `DATE` digère le texte et la **clé texte** `AAAA-MM`, elle, ne matche plus : les 360 lignes de janvier à
septembre perdent leur correspondance. La leçon n'est pas `STXT`, c'est que le nombre et le texte ne se pardonnent
pas les mêmes choses.

**Exercice 6.5.** Clé naïve : 45 lignes jointes sur 218 — les seuls mois d'octobre à décembre, à deux chiffres.
Clé paddée `=B2&"-"&TEXTE(C2;"00")` : 218 sur 218. La colonne à ajouter **une fois** est déjà dans `objectifs`,
`annee_mois`, écrite `2023-01` : le travail de l'atelier est de l'utiliser, avec en tête le contrôle
`=NB.SI(objectifs!D:D;ANNEE(ventes!B2)&"-"&TEXTE(MOIS(ventes!B2);"00"))`. Conclusion à en tirer : quand la table de
référence porte la clé, le fichier de faits n'a pas à en fabriquer une.

**Exercice 6.6.** Sur `ventes_brutes!F2` brut : `#N/A` sur les 489 lignes, parce que la colonne est du texte
(471 cellules écrites, 18 vides) et que `clients[id_client]` est numérique — deux **types**, pas deux valeurs.
Avec `=CNUM(SUPPRESPACE(ventes_brutes!F2))`, les lignes identifiées retrouvent leur ville et les 18 vides tombent en
`#VALEUR!` sous `CNUM` — d'où le contrôle du vide **avant** la conversion, `=SI(F2="";"non saisi";RECHERCHEX(CNUM(SUPPRESPACE(F2));clients!A:A;clients!B:B;"comptoir"))`. Notez le
gain : la réparation n'a pas changé les données, elle a changé **le type**, et le taux de recouvrement est passé
de 0 à 377 sur 462.

---

## 13. Mini-projet M03.P1 — suite : le volet recherches (45 min)

**Commande.** Ajoutez à `recherches_atelier` une feuille `Enrichissement` qui fait du tableau `ventes` un jeu
prêt à agréger, et qui le prouve.

**Livrables numérotés.** (1) quatre colonnes enrichies (ville, type de client, statut du vendeur, prix catalogue),
écrites en `RECHERCHEX` **et** en `INDEX`/`EQUIV` côte à côte, avec une colonne `écart` entièrement vide ; (2) le
bloc de tête : unicité des trois clés de référence, taux de recouvrement par colonne, nombre de vides ; (3) les
colonnes `lignes_du_ticket` et `montant_ticket`, avec la note qui explique pourquoi on ne moyenne pas la seconde ;
(4) la clé composite mois de `objectifs`, comptée avant et après `TEXTE` (45 contre 218) ; (5) deux cents mots : ce
qui était du texte, ce qui est devenu typé, ce qui reste non joignable.

**Barème (20 points, seuil 13).** Colonnes justes et doublées de la voie 2019 (6) · contrôles de tête (5) ·
vide et zéro traités séparément (3) · clé composite paddée et démontrée (3) · page de notes (3).

---

## 14. Résumé du chapitre

Une recherche rapproche deux tables sur une clé, et la clé décide de tout : son **grain** (ligne ou ticket), son
**type** (nombre ou texte), son **unicité** (une ligne, ou un choix arbitraire). `RECHERCHEV` est
universelle et fragile : approximative par défaut, arrêtée au premier match, incapable de regarder à gauche, figée
sur un index de colonne. `RECHERCHEX` ferme trois de ces quatre portes et ajoute un repli typé par cause ;
`INDEX`/`EQUIV` fait partout le même travail et reste la voie des classeurs partagés. Les fonctions de texte ne
sont pas un à-côté : `SUPPRESPACE`, `SUBSTITUE` et `CNUM` rendent les clés joignables (fiche 22 : 56 658),
`GAUCHE`/`STXT`/`DROITE` les démontent, `&`, `CONCAT` et `JOINDRE.TEXTE` les reconstruisent — et le padding est la
seule manière d'avoir raison sur un mois court (45 lignes sur 218, sinon).

Trois réflexes : **compter avant de chercher** (377 sur 462, et 103 échecs à deux causes) ; **vérifier le type des
deux côtés** ; **ne jamais masquer un `#N/A` sans avoir dit lequel** — comptoir n'est pas non-saisi.

> **À retenir.** Le piège le plus coûteux de `RECHERCHEV` ne rend aucune erreur : 0 divergence sur la table triée,
> 233 sur 377 après un tri par nom, 377 après un tri par ville. Un résultat juste aujourd'hui n'est pas un résultat
> fiable.

1. **`RECHERCHEX(valeur;où;quoi;"repli";0;-1)`** dit en une ligne ce que `RECHERCHEV` + `SIERREUR` +
   `INDEX`/`EQUIV` disent en trois : le repli, l'exactitude, le sens de recherche. Écrivez la voie compatible dans
   les cellules, commentez la voie moderne.
2. Une clé de date fabriquée par concaténation s'écrit `=A&"-"&TEXTE(B;"00")`, jamais `=A&"-"&B` : le caractère
   perdu fait disparaître trois mois sur douze — 360 lignes de l'extrait.

---

## 15. À retenir

1. **Tester l'unicité de la clé de chaque table de référence** : `=MAX(NB.SI(produits!A:A;produits!A:A))` doit
   valoir 1 — formule matricielle sur Excel 2019 et 2021 (à valider en `Ctrl` + `Maj` + `Entrée`), naturelle sur
   Microsoft 365. Si le maximum dépasse 1, votre recherche renvoie un arbitraire et ne vous préviendra pas.
2. **Un repli par cause d'échec**, pas un repli global : `SI(vide)` avant la recherche, `non_trouvée` dedans, et
   jamais `SIERREUR` autour de tout pour faire taire la feuille.
3. **Réparer les types avant d'assembler les clés** : `=NB.SI(plage;0)` sur la colonne de départ, puis
   `CNUM(SUPPRESPACE(…))`, puis la recherche — dans cet ordre, et le taux de recouvrement comme preuve finale.

---

## 16. Évaluation formative (auto-correction, 10 min)

1. Une `RECHERCHEV` sans quatrième argument sur une table triée par sa clé : que se passe-t-il aujourd'hui, et après
   un tri par une autre colonne ?
2. Écrivez, sans fichier sous les yeux, la recherche du type de client d'une ligne de `TableVentes`, avec un repli
   distinct pour la cellule vide et pour l'identifiant absent, en une seule formule.
3. Pourquoi `=RECHERCHEV(libellé;produits!A:K;…)` ne peut-il pas rendre l'`id_produit`, et quelles écritures le
   peuvent ?
4. Un collègue joint les ventes aux tickets et trouve un chiffre d'affaires inférieur de 30,9 % au total du
   tableau. Donnez la cause, et le contrôle en une formule qui l'aurait montré avant le premier tableau de bord.
5. Dans `objectifs`, `annee_mois` vaut `2023-01`. Que donne une régénération par `=annee&"-"&mois`, et combien de
   lignes sur 218 survivent ?

**Question ouverte.** Vous livrez un classeur qui doit tourner en Microsoft 365, en Excel 2019 et dans LibreOffice
Calc, et être relu six mois plus tard par un inconnu. Décrivez votre politique de recherche : quelle fonction dans
les cellules, laquelle en note, quels contrôles en tête de feuille, et à quoi vous renoncez.

---

**Corrigé de l'évaluation formative.**

1. Rien aujourd'hui : l'approximation sur une clé triée croissante retombe juste (0 divergence sur les 377 lignes à
   clé valide). Après un tri par `nom`, la même formule rend 233 réponses fausses sur 377 ; après un tri par
   `ville`, 377. Le symptôme est un résultat **qui bouge sans cause**, pas une erreur.
2. `=SI(TableVentes[@client]="";"non saisi";RECHERCHEX([@client];clients[id_client];clients[type_client];"absent du fichier"))` —
   le contrôle du vide **avant** la recherche, le repli dedans, pas de `SIERREUR` autour.
3. Parce que `id_produit` est en colonne A et la désignation en B : `RECHERCHEV` ne renvoie que ce qui est **à
   droite** de sa colonne de clé, et un index 0 n'existe pas. Les deux issues :
   `=INDEX(produits!A:A;EQUIV(libellé;produits!B:B;0))` ou `=RECHERCHEX(libellé;produits!B:B;produits!A:A)`.
4. Le rapprochement s'est fait au grain du ticket alors que la donnée est au grain de la ligne : `RECHERCHEV`
   s'arrête au premier match et ne somme qu'une ligne sur cent quatre tickets multi-lignes. Contrôle :
   `=MAX(NB.SI(TableVentes[n_ticket];TableVentes[n_ticket]))` — s'il vaut plus de 1, la clé n'est pas une clé de
   ligne.
5. Elle devient `2023-1` pour les neuf premiers mois, donc injoignable : 45 lignes sur 218 se joignent (celles
   d'octobre à décembre), et la perte porte exactement sur les mois creux de l'année. Le remède est
   `TEXTE(mois;"00")`, et le contrôle est `=NBCAR(clé)` qui doit valoir 7 pour `AAAA-MM`.

**Question ouverte — attendus.** `INDEX`/`EQUIV` dans les cellules, `RECHERCHEX` en commentaire, contrôles
d'unicité et de recouvrement en tête, et renonciation assumée à `DECALER`, `INDIRECT` et aux macros enregistrées.
