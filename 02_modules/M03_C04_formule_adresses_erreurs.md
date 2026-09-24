# Module M03.C04 — La formule : références relatives, absolues, mixtes, et les sept erreurs

**Outil de ce chapitre : le tableur seul, sur le classeur de l'atelier.** Durée indicative : 4 h. Niveau : N2.

> **L'idée du chapitre.** Une formule n'est pas un calcul, c'est un **déplacement**. Vous écrivez une phrase pour une
> ligne, le tableur la rejoue sur les 479 autres, et c'est ce jeu qui marche ou qui casse. Le chapitre tient donc à
> deux questions : *qu'est-ce qui bouge quand je recopie ?* et *qu'est-ce que cette erreur est en train de me dire ?*

> **Base de travail.** Le classeur `01_socle_donnees/data/projection/m03_classeur_atelier.xlsx`, et deux de ses
> feuilles : `ventes` (480 lignes, colonne N = montant hors taxes recalculé) et **`Calculs`** — 28 fiches de formules,
> une par ligne, avec la valeur attendue, la valeur rendue et un contrôle automatique. Le fichier reçu
> `01_socle_donnees/data/projection/ventes_magasin5_2025.csv` sert de terrain de chasse aux erreurs. Séparateur
> point-virgule, UTF-8, franc CFA (FCFA), virgule décimale, TVA 18 %. Chiffres cités :
> `01_socle_donnees/data/reference/chiffres_cites.md`, section M03. On travaille dans une copie du classeur nommée
> `formules_atelier` : la feuille `Calculs` se lit, elle ne se corrige pas.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

1. **Écrire** une formule lisible : opérateurs, ordre de calcul, parenthèses — et prévoir ce qu'elle vaudra ligne 481.
2. **Distinguer** référence relative, absolue et mixte, et choisir la bonne à la seule lecture du besoin.
3. **Lire** une erreur au lieu de la masquer : `#VALEUR!`, `#N/A`, `#DIV/0!`, `#RÉF!`, `#NOM?`, `#NULL!`, `####`.
4. **Comprendre la propagation** : une cellule fausse en contamine cinquante, et `SIERREUR` n'est pas un pansement.
5. **Arrondir au bon endroit** : dans la valeur ou dans l'affichage, mais pas les deux — et dire pourquoi le total du
   classeur bouge de 4 FCFA selon ce choix.
6. **Faire parler le classeur d'atelier** : ses 640 cellules à formule, ses noms stockés en anglais, son auto-contrôle.

---

## 2. Pourquoi cette notion est importante

**Situation 1 — le taux qui ne bouge pas d'un cheveu.** Une facturière calcule le TTC sur 480 lignes avec
`=L2*1,18`, le taux étant écrit dans la formule. Le taux change au 1ᵉʳ septembre : elle corrige la ligne 2, recopie —
les lignes déjà relues et verrouillées en haut du fichier restent à l'ancien taux, et le total ne le dit pas. La
formule juste est `=L2*TauxTVA`, avec le taux dans une cellule nommée : une saisie, 480 lignes à jour, zéro report.

**Situation 2 — l'erreur qui n'en est pas une.** Le tableau de bord affiche `#DIV/0!` en face d'un vendeur. Ce n'est
pas une panne : c'est la réponse exacte à une question mal posée — ce vendeur n'a aucune ligne dans la période
filtrée. Le masquer par un `SIERREUR(…;"")` transforme un diagnostic en mensonge : le tableau devient propre, et le
trou devient invisible au comité.

**Situation 3 — la suppression qui a tout emporté.** Une colonne « heure », jugée inutile, est supprimée. Les
formules qui lisaient `K2:K481` ne disparaissent pas : elles deviennent `#RÉF!`, y compris celles que personne ne
regardait, dans `TCD` et dans `Mensuel`. Le tableur n'a pas cassé le calcul, il a dit très clairement qu'on lui avait
retiré sa matière — et personne n'a lu.

> **Dans les faits.** Le contrôle de qualité d'un classeur de gestion commence par deux gestes de dix secondes :
> `Ctrl` + `'` pour afficher toutes les formules de la feuille, et une recherche de `#` dans le classeur entier. Ils
> trouvent plus de défauts que leur réputation ne le laisse croire, parce qu'ils portent sur tout — y compris les
> cellules que personne n'ouvre jamais.

---

## 3. Explication simple

Une formule est une phrase : un signe égal, des références, des opérateurs, des fonctions. Elle ne stocke pas un
résultat, elle stocke une **instruction de calcul**, et le résultat est recalculé à chaque changement.

Quand vous recopiez une formule, le tableur ne copie pas le texte : il le **translate**. `=L2*1,18` recopié une ligne
plus bas devient `=L3*1,18`. C'est la référence **relative** : elle désigne un décalage, pas une adresse. Le signe `$`
fixe un bord : `$L$2` ne bouge jamais (absolue), `L$2` fige la ligne et laisse la colonne voyager (mixte). La touche
`F4` fait tourner les trois écritures dans l'ordre.

D'où la règle du module, déjà entrevue au chapitre précédent : **ce qui sert de règle se fixe, ce qui se répète se
laisse relatif**. Le taux de TVA est une règle → absolue. La ligne de vente est un calcul → relatif.

Les erreurs, elles, ne sont pas des pannes : ce sont des messages. Sept formes, sept causes distinctes. Savoir les
lire divise par dix le temps de diagnostic ; les masquer le multiplie par cent.

---

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **Référence relative — relative reference** | `L2` : un décalage depuis la cellule de la formule. | Recopier la référence d'une règle : chaque ligne prend son propre décalage. |
| **Référence absolue — absolute reference** | `$L$2` : adresse figée, insensible au report. | Figer ce qui doit bouger : 480 lignes avec le même montant. |
| **Référence mixte — mixed reference** | `L$2` ou `$L2` : un seul bord figé. | Ne pas la connaître : elle règle d'un coup les tableaux à double sens. |
| **Report — fill** | Glisser la poignée, double-clic, `Ctrl` + `D`, ou *Accueil → Modifier → Remplir*. | Reporter 480 lignes d'une formule fausse à la ligne 2. |
| **Référence structurée — structured reference** | `TableVentes[montant_ttc]`, `[@quantite]`. | Écrire un `[@…]` hors du tableau : `#VALEUR!`. |
| **Référence circulaire — circular reference** | Une formule qui se lit elle-même, directement ou par chaîne. | Ignorer l'avertissement d'ouverture et valider des valeurs figées. |
| **Propagation d'erreur — error propagation** | Toute fonction recevant une erreur la renvoie. | Entourer la chaîne entière de `SIERREUR` et perdre l'adresse du défaut. |
| **Fonction volatile — volatile function** | Recalculée à chaque frappe (`AUJOURDHUI`, `DECALER`, `INDIRECT`). | En parsemer 480 lignes et attendre la réactivité d'une application. |

> **Définition.** Le **maillage** d'une formule est l'ensemble des cellules qu'elle lit. Deux formules qui se
> recouvrent sans le savoir — la colonne enregistrée `montant_ht` et la colonne N qui la recalcule — produisent un
> **écart de contrôle** : 4 FCFA ici. Un maillage documenté rend l'écart explicable ; un maillage implicite le rend
> suspect, et un écart suspect se paie en demi-journée de réunion.

> **Définition.** Le **sens du report** est la direction où le décalage s'applique : vers le bas pour une colonne de
> lignes, vers la droite pour une ligne de mois. Une référence mixte `L$2` se comporte comme une ordonnée : la ligne
> est commune à toute la grille, la colonne suit le déplacement. C'est elle qui écrit une grille mensuelle en une
> seule saisie au lieu de quarante-huit.

---

## 5. Cours approfondi

![Ce qui bouge quand on recopie, et ce que disent les sept erreurs](../figures/M03_C04_adresses_erreurs.svg)

### 5.1 Les opérateurs, et l'ordre qui les range

Six familles, un ordre : `^` d'abord, puis `*` et `/`, puis `+` et `-` ; les comparaisons (`=`, `<>`, `>=`) et la
concaténation `&` viennent après ; le texte se compare par ordre alphabétique, pas par longueur. Quatre tests à faire
vous-même dans une cellule libre :

- `=2+3*4` rend 14, `=(2+3)*4` rend 20 : la parenthèse n'est pas une précaution, c'est la ponctuation du calcul.
- `=1/2` rend 0,5 — si la cellule affiche `0`, le format masque les décimales et la valeur est juste : on regarde la
  barre de formule, pas la grille.
- `="11"&" mois"` rend `11 mois`, c'est-à-dire un **texte** : toute formule qui le somme rendra `#VALEUR!`.
- `=-2^2` rend −4 quand `=(-2)^2` rend 4 : l'exposant s'attache au nombre, pas au signe.

> **Définition.** L'**ordre de priorité** est la convention qui range les opérateurs : puissances, puis
> multiplications et divisions, puis additions et soustractions, puis comparaisons et concaténation. Un tableur ne
> « calcule pas de gauche à droite » : il applique cette hiérarchie, et rien d'autre. Écrire `=1-2*3` rend −5 ;
> écrire `=(1-2)*3` rend −3. Les parenthèses ne clarifient pas, elles **décident**.

Le pourcentage est un diviseur : taper `18` puis appliquer `0,0 %` vaut `0,18`, pas 18. Les remises du fichier reçu,
écrites `0.03`, sont exactement ce malentendu — à l'envers, et multiplié à 489 lignes.

### 5.2 Relative, absolue, mixte : ce qui bouge, ce qui reste

La figure se lit en trois colonnes : `=B2*$B$1` recopiée vers le bas devient `=B3*$B$1` — la donnée suit le
déplacement, la règle reste. Quatre situations de gestion, quatre écritures :

| Besoin | Écriture | Pourquoi |
|---|---|---|
| Taux de TVA commun à 480 lignes | `=L2*TauxTVA` | une règle, saisie une fois, nommée une fois |
| Grille de mois en tête de colonne | `=B$1*$Q2` | la ligne 1 porte les mois, la colonne Q porte les lignes |
| Total d'une colonne du tableau | `=SOMME(TableVentes[montant_ttc])` | le nom remplace l'adresse et survit aux lignes nouvelles |
| Somme d'une fenêtre fixe, lignes 40 à 80 | `=SOMME($L$40:$L$80)` | figée, sinon le report déplace la fenêtre et le total |

`F4` fait tourner `L2 → $L$2 → L$2 → $L2` dans cet ordre : on n'écrit jamais les `$` à la main, on les fait tourner —
et l'on vérifie ensuite dans la barre de formule, pas dans le résultat. Une référence construite avec `LIGNE()`,
`COLONNE()` ou `EQUIV()` ne se reporte pas « mal » : elle rend sa propre position. C'est le principe de la colonne de
rang `=LIGNE()-1`, qui numérote les lignes sans les compter à la main — et qui cesse de le faire dès qu'on la
convertit en valeurs.

### 5.3 Ce que le fichier stocke, ce que vous lisez

La feuille `Calculs` porte deux colonnes qui disent tout : « Fonction (telle que l'affiche Excel FR) » et « Formule,
telle qu'elle est stockée ». La fiche 22 s'intitule *Réparer une cellule* et son contenu stocké est
`VALUE(SUBSTITUTE(ventes_brutes!M2," ",""))`. Le fichier écrit les noms de fonction en **anglais** et sépare les
arguments par des **virgules** ; l'interface française affiche les noms traduits et des points-virgules. Trois
conséquences de travail :

1. Une formule venue d'un classeur anglophone s'affiche traduite chez vous : le fichier voyage mieux que la
   documentation. C'est pour cela qu'une fiche de formules cite le **nom français en toutes lettres**, jamais une
   capture d'écran.
2. Une fonction inconnue du tableur ne se traduit pas : `TEXTJOIN` ou `UNIQUE` sur une version ancienne rendent
   `#NOM?` — et la fiche 23 de `Calculs`, qui les emploie toutes les deux, est précisément réservée à Microsoft 365
   (règle de la fiche double, §5.8).
3. `Ctrl` + `'` bascule l'affichage des formules. Le geste de l'auditeur : il révèle d'un écran les 480 formules de la
   colonne N de `ventes`, les recopies incohérentes, et les nombres tapés à la place d'un calcul — le défaut le plus
   coûteux du tableur en entreprise, parce qu'il a l'air exact.

> **À retenir.** Un `=` n'engage pas le même calcul selon la cellule où il se trouve : la même formule, reportée, est
> une autre formule. On ne valide jamais la ligne 2 seule — on regarde une ligne au milieu, une ligne de retour (les
> montants négatifs existent ici), et la dernière ligne du fichier.

### 5.4 Les sept erreurs, une cause chacune

- **`#VALEUR!` — le type ne convient pas.** `=CNUM("56 658")`, ou une multiplication qui touche du texte. Les 486
  montants texte du fichier reçu la produisent à chaque tentative de calcul direct. Le remède est la conversion
  (chapitre C02), pas la conversion de l'erreur en 0.
- **`#N/A` — la clé est absente.** `=RECHERCHEV(1229678;ventes!G2:J481;4;FAUX)`, la fiche 17 de `Calculs`, cherche un
  *montant* dans une colonne de *produits*. `#N/A` ne dit pas « la formule est fausse » : il dit « ici, rien ne
  correspond ». C'est souvent le résultat exact d'une question juste posée sur un périmètre trop court.
- **`#DIV/0!` — dénominateur nul.** Une moyenne sur une sélection vide, un objectif absent, un taux de réalisation
  sur un magasin sans ligne. Le classeur connaît le cas : deux ventes de l'extrait n'ont pas d'objectif.
- **`#RÉF!` — la plage n'existe plus.** Suppression d'une ligne ou d'une colonne référencée. La formule n'est pas
  réparable en l'état : on la réécrit, ou on restaure la version d'avant — d'où la copie de travail du chapitre C01.
- **`#NOM?` — le nom est inconnu.** Fonction d'une version plus récente, faute de frappe, ou référence structurée
  écrite hors du tableau.
- **`#NULL!` — intersection vide.** Un espace au lieu d'un point-virgule : `=SOMME(L2:L10 M2:M10)` demande
  l'intersection de deux plages qui ne se touchent pas.
- **`####` — ce n'est pas une erreur.** La colonne est trop étroite pour l'affichage, la valeur est juste :
  double-clic sur le bord de la colonne et elle réapparaît. C'est la seule des sept qui ne dise rien du calcul.

> **Définition.** Une erreur de tableur est une **valeur réservée**, qui se propage comme les autres le long du
> maillage — mais que `SOMME`, `MOYENNE`, `NB` et les filtres **ignorent en silence**. C'est cette asymétrie qui rend
> une feuille fausse et pourtant muette : `=SOMME(M2:M481)` sur une colonne contenant dix `#VALEUR!` ne rend pas une
> erreur, il rend un total amputé.

### 5.5 Propager, attraper, compter : trois gestes différents

`SIERREUR(x;"rien")` renvoie le second argument dès que `x` est une erreur — n'importe laquelle. C'est un cache, pas
un contrôle. Trois écritures, par ordre de mérite :

1. **Attraper la seule erreur attendue** : `=SI.NON.DISP(RECHERCHEV(…);"absent du fichier")` — en français la
   fonction `IFNA` s'appelle `SI.NON.DISP`, et elle ne prend que deux arguments : la valeur, ce qu'on affiche à la
   place si c'est `#N/A`. Sur un rapprochement de clients, `#N/A` devient un libellé lisible, `#VALEUR!` continue de
   crier. La voie universelle, à connaître parce qu'elle marche aussi dans les versions anciennes :
   `=SI(ESTNA(RECHERCHEV(…));"absent du fichier";RECHERCHEV(…))`.
2. **Prévenir plutôt qu'attraper** : `=SI(ESTNUM(M2);M2*1,18;"montant non numérique")`. La colonne de statut du
   chapitre C02 est de cette famille — elle dit ce qu'elle voit au lieu de faire disparaître.
3. **Compter les erreurs au lieu de les afficher** : `=SOMME(ESTERREUR(plage)*1)`, en validation matricielle
   (`Ctrl` + `Maj` + `Entrée` sur Excel 2021). Attention aux deux voisines : `ESTERREUR` (anglais `ISERROR`) capte
   toutes les erreurs, `ESTERR` (`ISERR`) **rate `#N/A`** — la seconde est donc le mauvais outil pour un compteur. Le
   test ne dépend pas de la langue, alors que chercher le texte `#VALEUR!` dans un `NB.SI` dépend de l'affichage :
   c'est la recette qui marche chez le voisin et pas chez vous. Un nombre d'erreurs se suit d'un import à l'autre :
   une baisse est une amélioration, une hausse non commentée est une alerte.

La fiche 26 de `Calculs` montre le geste et son prix : `=SIERREUR(1/0;"rien à afficher")` rend le texte attendu — et
rendrait la même chose pour un `#RÉF!` ou un `#NOM?` logé dans une cellule d'à côté. La fiche 17, elle, laisse son
`#N/A` remonter **jusque dans son propre contrôle** : la colonne *contrôle* de cette ligne tombe en `#N/A` à son tour,
parce que `EXACT` propage. Tout le chapitre est dans cette case : une erreur attrapée trop tôt devient une erreur qui
ne dit plus où elle est.

### 5.6 Arrondir : dans la valeur, ou dans l'affichage — mais pas les deux

`ARRONDI(x;0)` modifie la valeur stockée ; le format ne modifie que son image. Le classeur d'atelier permet de mesurer
l'écart, parce qu'il contient à la fois un `montant_ht` **enregistré** par la caisse et une colonne N qui le
**recalcule** : `=ARRONDI(I2*J2*(1-K2);0)`. L'écart des deux totaux est de 4 FCFA sur 30 570 491 FCFA — et ce n'est
pas une faute. Sept lignes de l'extrait ont un produit qui tombe à un demi-franc (six au test strict, la septième à
un cheveu près, ce qui est déjà une leçon) ; sur quatre d'entre elles, la règle d'arrondi choisie change le franc :

| Ticket | Quantité | Prix HT | Remise | Produit brut | Enregistré | Avec `ARRONDI` |
|---|---|---|---|---|---|---|
| T05-250702-096500 | 2 | 9 725 | 11 % | 17 310,5 | 17 310 | 17 311 |
| T05-250703-096586 | 2 | 26 625 | 7 % | 49 522,5 | 49 522 | 49 523 |
| T05-250801-099095 | 2 | 6 225 | 7 % | 11 578,5 | 11 578 | 11 579 |
| T05-251002-105562 | 18 | 5 025 | 3 % | 87 736,5 | 87 736 | 87 737 |

**Version alternative pour un petit écran** — ce tableau de sept colonnes tient en deux phrases. Sur les quatre
lignes, le produit brut finit en `,5` : la caisse a retenu l'entier pair juste en dessous, `ARRONDI` retient
l'entier au-dessus. Le paragraphe qui suit dit laquelle des deux règles votre fichier doit suivre, et pourquoi.

Un franc sur une ligne, quatre sur le fichier : la caisse applique **l'arrondi bancaire** (à mi-chemin, on va vers
le pair — 15 856,5 devient 15 856), Excel `ARRONDI` applique l'arrondi usuel (à mi-chemin, on s'éloigne de zéro — il
devient 15 857). Reproduire l'arrondi bancaire dans une colonne de contrôle donne le total enregistré à zéro franc
près : la preuve que l'écart de 4 FCFA vient de la règle, pas des données. Trois règles de métier. Un **montant destiné à être facturé**
s'arrondit dans la valeur, parce que le total doit se recomposer depuis les lignes. Une **statistique** ne s'arrondit
jamais avant agrégation — arrondir 480 montants puis faire la moyenne déplace le résultat, et le module M02 a montré
de combien. Et **la règle s'écrit** : une ligne dans `Aidez-moi`, sinon un relecteur perdra une heure à chercher une
faute inexistante. Notez que **sans aucun arrondi**, l'écart est de 2 FCFA, pas de 0 : les deux totaux ne coïncident
pas non plus.

### 5.7 Ce qui casse une référence, ce qui ne la casse pas

| Geste | Effet sur la formule |
|---|---|
| Insérer une ligne au milieu de la plage sommée | la plage s'étend, la formule suit — il n'y a rien à faire |
| Supprimer une ligne de la plage | la plage se réduit, `=SOMME(L2:L479)` |
| Supprimer la colonne référencée | `#RÉF!`, et la formule est à réécrire |
| Couper-coller une cellule référencée | les formules qui la lisaient sont réécrites vers la nouvelle adresse |
| Coller une valeur par-dessus une formule | la formule disparaît, sans trace dans le fichier |
| Masquer des lignes | aucun effet sur `SOMME`, effet total sur `SOUS.TOTAL` |
| Trier | aucun effet sur les références, effet fâcheux sur un maillage mal figé |

La colonne de rang (`=LIGNE()-1`) ne survivra pas à une suppression de ligne si on l'a convertie en valeurs ; la
colonne `n_ticket` lue dans le fichier, si. Un numéro de ligne est une **position**, un identifiant est une
**donnée** : la première se recalcule, la seconde se protège. C'est la différence qui explique qu'un même fichier
donne deux historiques différents selon la personne qui l'a ouvert.

> **Attention.** Coller en valeurs sur une colonne de calcul supprime le calcul **sans laisser de trace** :
> la cellule ne se distingue plus d'une saisie manuelle, ni à l'écran, ni dans le fichier. Sur 480 lignes, l'accident
> est invisible au moment où il se produit et irréversible à la relecture. Deux protections valent le coup : garder la
> colonne source à côté (c'est ce que fait le classeur avec `ventes_brutes`), et noter dans `Aidez-moi` quelles
> colonnes sont calculées — la liste tient en quatre lignes.

### 5.8 La règle de la fiche double, et les deux silences du tableur

Deux fonctions citées ici n'existent pas partout : `TEXTJOIN` et `UNIQUE` (fiche 23), comme `FILTRE`, `TRIBY` et
`SÉQUENCE` au chapitre C07 — Microsoft 365 requis. LibreOffice Calc 24.8 a rattrapé une partie du retard, les
versions plus anciennes non. La règle du manuel est donc la **fiche double** : la voie moderne, puis la variante
accessible à Excel 2021 et à Calc, avec le nom de la fonction écrit en toutes lettres. Livrer
`=JOINDRE.TEXTE(", ";VRAI;UNIQUE(ventes!H2:H481))` sans sa variante, c'est un classeur qui rendra `#NOM?` sur le
poste de la direction, et une réunion pour rien.

Deux silences, pour finir. Le tableur **ne prévient pas** quand une formule ne couvre pas toute la plage :
`=SOMME(L2:L480)` posé à la ligne 481 rend un total amputé d'une ligne, et rien ne clignote — le seul contrôle est la
barre d'état, pas la cellule. Il **recalcule sans mesurer** non plus : `AUJOURDHUI()`, `DECALER`, `INDIRECT` sont
volatiles, recalculées à chaque frappe ; multipliées par 480 lignes, elles transforment un classeur léger en fichier
lent — d'où le « comprendre, éviter » du programme.

> **Attention.** `=SOMME(ventes!L2:L480)` et `=SOMME(TableVentes[montant_ttc])` peuvent cohabiter, donner deux
> nombres différents, et s'afficher toutes les deux sans le moindre avertissement. Le tableur ne compare pas les
> maillages, il les exécute. Une cellule de contrôle par table, qui confronte les deux écritures, coûte dix secondes
> et ferme ce risque pour de bon.

> **Boîte à outils.** `F4` faire tourner les `$` · `Ctrl` + `'` afficher (et recacher) les formules de la feuille ·
> `F2` éditer une cellule sans perdre sa formule · `Maj` + `Flèches` pendant l'édition pour étendre une référence ·
> `Ctrl` + `D` remplir vers le bas, *Accueil → Modifier → Remplir → Vers la droite* pour l'autre sens ·
> `Ctrl` + `Entrée` valider sans descendre · *Création de tableau → Tableau → Sélection → Sélection du tableau* pour
> vérifier la portée · `Ctrl` + `F` sur `#`, dans le classeur entier, pour lister les erreurs ·
> *Formules → Vérification des formules → Espion de formule* pour remonter une chaîne cellule par cellule. Dans
> LibreOffice Calc, `F4` alterne les `$` de la même façon, l'affichage des formules est dans *Affichage → Afficher
> les formules* (pas de raccourci par défaut), et *Outils → Contenu des cellules → Précédents / Dépendants* remplace
> l'espion.

---

## 6. Exemple concret : la ligne 2, de la saisie au total

Ligne 2 de `ventes` : quantité `11`, prix unitaire HT `4 500`, remise `0,03`, montant HT enregistré `48 015`, montant
TTC enregistré `56 658`. La chaîne complète :

- `11 × 4 500 = 49 500` — le brut ;
- `49 500 × (1 − 0,03) = 48 015` — le net de remise, entier ici, aucun arrondi nécessaire ;
- `48 015 × 1,18 = 56 657,7` — le TTC **avant** arrondi. Formaté sans décimale, le tableur affiche `56 658` alors que
  la valeur stockée reste `56 657,7` ;
- `=ARRONDI(48015*1,18;0)` rend `56 658` dans la **valeur**, et le total de la colonne se recompose dès lors ligne par
  ligne.

Sur cette ligne, les deux écritures donnent le même affichage. Sur les lignes à demi-franc du §5.6, elles donnent un
total différent de 4 FCFA. C'est toute la démonstration : le format n'est pas un choix cosmétique tant qu'on n'a pas
dit **où** l'arrondi se produit — et c'est pourquoi la colonne N du classeur ne se contente pas d'être jolie, elle
recalcule, et son écart avec la colonne enregistrée est la mesure du travail.

## 7. Démonstration pas à pas : lire, reproduire, casser, réparer

Sept étapes dans la copie `formules_atelier`.

**1. Lire une fiche.** Fiche 5 de `Calculs` : `=SOMME(ventes!M2:M481)` doit rendre 36 073 185. La colonne
*Ce que la formule rend* recalcule, la colonne *contrôle* compare avec `=SI(EXACT(D6;E6);"ok";"à revoir")`. Le
classeur s'auto-auditte sur 28 lignes, en vingt secondes, sans macro : c'est la pratique à copier dans vos fichiers.

**2. Reproduire la fiche 22.** Sur une copie de `ventes_brutes`, en colonne P : `=CNUM(SUBSTITUE(M2;" ";""))`,
reportée jusqu'en `P490` — le double-clic sur la poignée suffit, la plage est contiguë. Retirez le `SUBSTITUE` :
trois lignes passent, 486 rendent `#VALEUR!`. Le compteur de valeurs numériques passe de 489 à 3, et le report n'y
est pour rien : c'est l'ancre qui a été juste, la conversion qui était fausse.

**3. Trier la référence, pas le nombre.** Écrivez `1,18` en `Q1`, nommez la cellule `TauxTVA`. En `Q2` :
`=ARRONDI(L2*TauxTVA;0)`, reportée sur les 480 lignes. Retirez le nom, laissez `L2*1,18`, re-reportez, puis corrigez
seulement la ligne 2 : le total ne bouge presque pas, et 479 lignes sont fausses. C'est l'expérience la plus courte
du chapitre et la plus probante.

**4. Fabriquer les trois erreurs utiles.** `=M2*2` sur la feuille brute (`#VALEUR!` : du texte) ;
`=RECHERCHEV(1229678;ventes!G2:G481;1;FAUX)` (`#N/A` : la clé n'est pas dans cette colonne) ;
`=MOYENNE.SI.ENS(ventes!M2:M481;ventes!E2:E481;"Vendeur inconnu")` (`#DIV/0!` : personne ne correspond). Notez en
face de chacune la phrase de ce qu'elle dit — pas ce qu'il faudrait faire.

**5. Les compter.** En `U1` : `=SOMME(ESTERREUR(Q2:Q481)*1)` en validation matricielle. Le nombre doit descendre à 0
quand les formules sont correctes, et monter dès qu'une conversion est retirée. Le comparateur de texte `NB.SI` n'est
pas utilisé ici, parce qu'il dépend de la langue d'affichage — §5.5, point 3.

**6. Faire un `#RÉF!` exprès.** Supprimez la colonne P construite à l'étape 2 : les cellules qui la lisaient deviennent
`=ARRONDI(#RÉF!*TauxTVA;0)`. Annulez avec `Ctrl` + `Z` **avant d'enregistrer** — après, il n'y a plus d'annulation.
Reconstruire la colonne prend deux minutes ; la retrouver dans un classeur de 480 lignes prend une matinée.

**7. Écrire la règle d'arrondi** dans `Aidez-moi` : « montants arrondis à l'unité ; le recalcul de la colonne N
diffère du montant enregistré de 4 FCFA, sur 4 lignes nées d'un produit à demi-franc » — et la colonne d'écart
`=ARRONDI(I2*J2*(1-K2);0)-L2`, qui rend la phrase vérifiable ligne par ligne.

**Contrôles qualité du chapitre.**

| # | Contrôle | Seuil | Résultat attendu | Si échec |
|---|---|---|---|---|
| 1 | Fiche 5 de `Calculs`, valeur rendue | ±1 FCFA | 36 073 185 FCFA | plage tronquée en 480, ou feuille mal lue |
| 2 | Colonne *contrôle* des 28 fiches | deux nombres | 27 « ok », 1 en `#N/A` propagé | `SIERREUR` posé sur le contrôle au lieu de la formule |
| 3 | Report de `=ARRONDI(L2*TauxTVA;0)` | compteur | 480 lignes non nulles | 1 juste et 479 fausses : nom ou `$` oubliés |
| 4 | Somme de la colonne d'écart N − L | ±1 FCFA | 4 FCFA (2 FCFA sans arrondi) | arrondi appliqué deux fois, ou jamais |
| 5 | Cellules en erreur de la colonne P | deux nombres | 0 avec `SUBSTITUE`, 486 sans | conversion partielle non détectée |

## 8. Erreurs fréquentes

1. **Figer la mauvaise dimension.** `=$L2` au lieu de `$L$2` dans une grille de mois : la moitié des cellules pointe
   hors de la plage, et le résultat reste plausible sur la première ligne — précisément celle que vous avez vérifiée.
2. **Valider une formule sur une seule ligne.** Le report est un déplacement : l'erreur d'ancre apparaît en bas de
   plage, et sur une ligne de retour si les montants peuvent être négatifs.
3. **Utiliser `SIERREUR` comme nettoyant.** Le classeur devient présentable, les 486 textes deviennent invisibles, et
   le total amputé reste roi. D'abord `ESTNUM` et une colonne de statut ; le silence, seulement s'il est choisi.
4. **Recopier une formule depuis une documentation étrangère.** Les noms changent, la virgule change de sens : on
   recopie la formule **telle que le fichier la stocke** (feuille `Calculs`, colonne C), pas une capture.
5. **Écraser une formule par une valeur sans le dire.** Un collage spécial trop large et le calcul disparaît sans
   trace. Le classeur de référence garde donc ses colonnes brutes (`ventes_brutes`) à côté des recalculs (N).
6. **Chercher `#` dans une seule feuille.** Les erreurs vivent souvent dans l'onglet que personne n'ouvre — `Mensuel`,
   ou la ligne de total masquée d'un tableau.

## 9. Bonnes pratiques professionnelles

1. **Une cellule d'hypothèse par taux, nommée et documentée** : `TauxTVA`, `ObjectifMensuel`, `SeuilAnomalie`. Le nom
   rend la formule auto-explicative et le changement d'hypothèse traçable — `Q1` ne l'est pas.
2. **Les formules de contrôle à côté des données, pas dedans.** Une colonne qui compare l'enregistré et le recalculé
   ne pollue pas la ligne de total, se filtre, et se compte.
3. **`Ctrl` + `'` avant chaque envoi**, puis une recherche de `#` sur le classeur : trente secondes, la moitié des
   retours en moins.
4. **La fiche double systématique** pour toute fonction version-dépendante : voie moderne, variante 2021/Calc, nom
   écrit en toutes lettres.
5. **Un commentaire sur les trois cellules qui coûtent cher** : la règle d'arrondi, le dénominateur d'une moyenne, le
   périmètre d'un filtre. Le destinataire ne rouvrira pas le chapitre, il rouvrira le classeur.

> **Conseil professionnel.** Ne dites jamais « le tableur a fait une erreur ». Il a exécuté. Formulez en revue :
> « la plage de somme s'arrête en `L480`, la ligne 481 est hors périmètre » — une adresse et une cause. C'est la
> différence entre un collègue qui corrige et un collègue qui se sent accusé et rouvre le fichier sans le regarder.

## 10. Exercice guidé — la chaîne de calcul, de la cellule au contrôle (35 min, /10)

**Commande.** Dans `formules_atelier`, reconstruisez la chaîne du montant hors taxes sur la feuille `ventes` (480
lignes), et rendez son écart mesurable.

| Étape | Geste | Ce qui doit se lire |
|---|---|---|
| 1 | `1,18` en `Q1`, nommée `TauxTVA` via la zone de nom | `TauxTVA` dans *Gestion des noms* |
| 2 | `=ARRONDI(I2*J2*(1-K2);0)` en `R2`, report | 480 valeurs, total 30 570 495 FCFA |
| 3 | `=R2-L2` en `S2`, report, format nombre | somme des écarts : 4 FCFA |
| 4 | Compteur `=SOMME(ESTERREUR(R2:S481)*1)` | 0 |
| 5 | Retirer `ARRONDI` à l'étape 2 | somme des écarts : 2 FCFA |
| 6 | Retirer les `$` d'une référence de règle (test en `T2` avec `=R2*Q1`) | 1 ligne juste, 479 à 0 |
| 7 | Taux porté à `1,19`, recopie du nom seulement | total TTC recalculé, 480 lignes à jour |

**Démarrage.** Les étapes 2, 3 et 5 sont le cœur : même données, trois règles d'arrondi, trois totaux. Notez-les dans
cet ordre avant toute explication. Le total attendu à l'étape 2 n'est pas celui de la colonne enregistrée : la caisse
a arrondi une fois, votre `ARRONDI` une autre, et l'écart de 4 FCFA est le résultat prévu, pas une faute. À l'étape 6,
écrivez la phrase de ce que vous voyez — c'est elle, et non le chiffre, qui prouve que vous avez compris le report.

**Barème (10 points).** Nom de plage posé et réellement utilisé dans une formule (2) · colonne recalculée juste sur
les 480 lignes (2) · les trois totaux notés, et l'écart de 4 FCFA expliqué par les lignes à demi-franc (3) ·
démonstration de la casse par retrait du `$`, chiffres à l'appui (2) · deux lignes écrites dans `Aidez-moi` (1).

## 11. Exercices autonomes

**Exercice 4.1 (★) — Les six écritures d'une adresse.** Dans une feuille libre, placez un taux en `B1`, une donnée en
`B2`, et écrivez en `C2` la formule `=B2*$B$1`. Reportez-la cinq lignes plus bas, puis trois colonnes vers la droite.
Notez ce que deviennent les deux références dans chaque cas, puis réécrivez la formule en `=$B2` et en `=B$2` et
recommencez. Concluez en une phrase.

**Exercice 4.2 (★) — Ce qui se propage.** Fabriquez une chaîne de trois cellules : une division par zéro, une cellule
qui l'additionne, une `=SOMME()` des deux. Ajoutez un compteur d'erreurs. Dites, pour chacune des quatre cellules, si
l'erreur est visible, propagée, ignorée ou comptée — et concluez sur ce que voit un lecteur du tableau de bord.

**Exercice 4.3 (★★) — La moyenne qui n'existe pas.** Calculez la moyenne des montants par vendeur de deux façons :
`=SOMME.SI.ENS(...)/NB.SI.ENS(...)` puis `=MOYENNE.SI.ENS(...)`. Faites disparaître un vendeur du périmètre avec un
filtre, puis avec une condition impossible. Laquelle des deux formules tombe en `#DIV/0!`, l'autre rend-elle la même
chose, et que faudrait-il écrire pour que ce soit dit en français et non en code d'erreur ?

**Exercice 4.4 (★★) — Les lignes à demi-franc, une par une.** Isolez les lignes de `ventes` dont le produit
`quantite × prix × (1 − remise)` tombe à un demi-franc. Pour chacune, calculez le résultat avec `ARRONDI`, avec
`ARRONDI.INF`, avec `ARRONDI.SUP`, et sans arrondi. Dressez le tableau, retrouvez les 4 FCFA, et écrivez la ligne de
fiche qui rend l'écart **prévu** et non plus suspect.

**Exercice 4.5 (★★) — Le classeur sans `#NOM?`.** Reprenez la fiche 23 de `Calculs` (`TEXTJOIN` + `UNIQUE`) et
écrivez sa variante compatible : un tri de la colonne des catégories, une colonne indicatrice
`=SI(NB.SI($H$2:H2;H2)=1;1;0)`, puis une concaténation par `&` sur les lignes retenues. Contrôlez que les deux voies
rendent les mêmes 7 libellés, dans le même ordre que la cellule `Calculs!E24`.

## 12. Correction détaillée

**Exercice 4.1.** Vers le bas : `=B3*$B$1`, `=B4*$B$1` — la ligne suit, la règle reste. Vers la droite :
`=C2*$B$1`, `=D2*$B$1` — la colonne suit, la règle reste. En `=$B2` : vers le bas, `=$B3`, donc la **colonne** est
figée et la ligne voyage ; en `=B$2`, vers la droite, `=C$2`. Règle attendue : « le `$` fige ce qui vient après lui —
la partie qui le porte ne bouge pas ».

**Exercice 4.2.** Cellule 1 : `#DIV/0!` visible. Cellule 2 : la même erreur, propagée (une addition ne sait pas
faire autrement). `SOMME` des deux : l'erreur est **ignorée**, le total rendu est celui de ce qui restait, sans un
mot. Compteur : 1. Conclusion attendue : les fonctions d'agrégation ignorent les erreurs comme elles ignorent le
texte — seul un compteur les rend visibles, donc seul un compteur vaut veille.

**Exercice 4.3.** Les deux écritures tombent en `#DIV/0!`, parce que `MOYENNE.SI.ENS` cache le même dénominateur.
Écrire `=SI(NB.SI.ENS(ventes!E2:E481;Q1)=0;"aucune ligne dans le périmètre";MOYENNE.SI.ENS(...))` rend le fait
lisible. Le vendeur mobile est celui de la ligne 481 du prochain import, jamais celui que l'on teste — d'où la
nécessité d'un message rédigé plutôt que d'un code.

**Exercice 4.4.** Quatre lignes divergent entre l'arrondi usuel et celui de la caisse, une cinquième touche le
demi-franc à un cheveu près et ne bouge pas, deux restent d'accord. Les quatre règles ne donnent pas le même total :

| Règle appliquée aux 480 lignes | Total de la colonne | Écart avec le fichier |
|---|---|---|
| aucune (le produit brut) | 30 570 493 | +2 |
| `ARRONDI` (usuel) | 30 570 495 | +4 |
| `ARRONDI.INF` | 30 570 487 | −4 |
| `ARRONDI.SUP` | 30 570 500 | +9 |
| arrondi bancaire, celui de la caisse | **30 570 491** | 0 |

Treize lignes de l'extrait ont un produit non entier, et seule la cinquième ligne du tableau reproduit le fichier à
zéro franc près : l'écart n'est donc pas une faute de saisie, c'est une convention. Phrase attendue : « un franc d'écart sur une ligne n'est pas une erreur : c'est la ligne où le produit tombait exactement à
un demi-franc ; la règle retenue est l'arrondi au franc le plus proche, elle est écrite ici, et l'écart total attendu
est de 4 FCFA ».

**Exercice 4.5.** La voie compatible tient en trois colonnes et un tri, contre une formule de 40 caractères pour la
voie 365. Les deux rendent les sept catégories dans l'ordre de la donnée, tel que `Calculs!E24` l'affiche.
Conclusion attendue : la variante est laide et verbeuse, mais elle s'ouvre sur un poste de 2021 — c'est exactement
pourquoi le manuel impose la fiche double.

## 13. Mini-projet M03.P1 — suite : le volet formules et cohérence (45 min)

**Commande.** Ajoutez au classeur de l'atelier un onglet `Mes fiches` calqué sur `Calculs`, et la colonne de contrôle
annoncée par ce chapitre.

**Livrables numérotés.** (1) dix fiches sur le modèle à six colonnes (nom français, formule stockée, valeur
attendue, valeur rendue, contrôle automatique, motif), au moins une par famille : agrégat, conditionnelle, recherche,
texte, date ; (2) la chaîne de calcul du montant en quatre colonnes (quantité, prix, remise, net arrondi) avec le
taux en cellule nommée ; (3) la colonne d'écart enregistré/recalculé et sa ligne de total, avec l'écart expliqué en
une phrase chiffrée ; (4) un inventaire d'erreurs par feuille et par type, `=SOMME(ESTERREUR(plage)*1)`, sur `ventes`,
`ventes_brutes` et `objectifs` ; (5) la fiche double de la fonction la plus récente que vous ayez employée, avec son
alternative 2021/Calc.

**Barème (20 points, seuil 13).** Fiches conformes au modèle, colonne de contrôle à « ok » (5) · chaîne de calcul avec
nom de plage et ancre justes (4) · écart chiffré et commenté (4) · inventaire d'erreurs complet et non masqué (4) ·
fiche double rédigée (3).

## 14. Résumé du chapitre

Une formule est un déplacement, pas un calcul : `F4` décide de ce qui suit le report et de ce qui reste, et c'est la
seule question à trancher avant d'étendre une ligne sur 480. Les opérateurs ont un ordre, la parenthèse est leur
ponctuation, le pourcentage est un diviseur. Le fichier stocke des noms anglais et des virgules, l'interface affiche
du français et des points-virgules : d'où une fiche de formules écrite en noms, jamais en captures.

Les sept erreurs sont sept causes : le type (`#VALEUR!`), la clé absente (`#N/A`), le dénominateur (`#DIV/0!`),
l'adresse disparue (`#RÉF!`), le nom inconnu (`#NOM?`), l'intersection vide (`#NULL!`), et la colonne trop étroite
(`####`, qui n'est pas une erreur). Elles se propagent le long du maillage, mais les fonctions d'agrégation les
ignorent en silence — c'est ce silence qui fabrique des totaux faux et présentables. `SIERREUR` ne répare pas, il fait
taire : `SI.NON.DISP`, `ESTNUM` et un compteur `ESTERREUR` rendent la feuille lisible sans la rendre muette.

Reste l'arrondi, qui est un choix de valeur et non d'affichage. Le classeur le mesure : 4 FCFA entre la colonne
enregistrée et la colonne recalculée, 4 lignes où la règle change le franc, 2 FCFA si l'on n'arrondit pas du tout.
Cinq lignes de documentation, une colonne d'écart, et le doute devient preuve.

## 15. À retenir

> **À retenir.** Le report translate les références relatives. Une formule juste à la ligne 2 peut être fausse à la
> ligne 480 : on valide en bas de plage, et sur une ligne à montant négatif.

> **À retenir.** `#N/A` est une réponse, `#RÉF!` est une amputation, `####` n'est pas une erreur. Les traduire avant
> de les masquer est le travail ; les masquer est le dégât.

> **À retenir.** Une erreur se propage dans les formules mais disparaît dans les agrégats : un total peut être faux
> sans afficher la moindre erreur. Un compteur d'erreurs par feuille est la seule veille qui tienne.

1. Une règle commune vit dans une cellule **nommée** ; un taux recopié dans 480 formules est un taux qu'on ne
   corrigera jamais 480 fois.
2. `Ctrl` + `'` avant d'envoyer, `Ctrl` + `F` sur `#` dans tout le classeur : trente secondes, la moitié des retours.
3. L'arrondi se choisit pour les montants facturés, se refuse dans les statistiques — et s'écrit toujours.
4. Toute fonction version-dépendante vient avec sa variante documentée : c'est ce qui permet à un poste d'agence de
   lire le fichier.
5. On ne supprime pas une colonne référencée : on la renomme, on la masque, on la documente.

## 16. Évaluation formative (auto-correction, 10 min)

1. Que devient `=B2*$B$1` recopié deux lignes vers le bas, puis trois colonnes vers la droite ? Écrivez les deux
   résultats.
2. Une cellule affiche `####`. Que vérifiez-vous d'abord, et pourquoi ce n'est pas une erreur de calcul ?
3. Pourquoi `=SIERREUR(RECHERCHEV(…);"0")` est-il trois fois sur quatre un mauvais choix, et que mettez-vous à la
   place ?
4. Sur la fiche 5 de `Calculs`, la plage est `ventes!M2:M481`. Si vous l'écrivez `ventes!M2:M480`, que rend la
   colonne de contrôle de la ligne, et pourquoi cet enchaînement est-il plus dangereux qu'une erreur affichée ?
5. Le total de la colonne enregistrée et celui de la colonne recalculée diffèrent de 4 FCFA. Citez les trois nombres
   qui prouvent que ce n'est pas une faute, et la ligne de documentation qui les rend prévisibles.

**Question ouverte.** Un classeur de 480 lignes contient 479 formules identiques et une différente. Quel raccourci,
quel geste, quelle colonne de contrôle permettent de trouver la dissidente sans lire 480 lignes ?

---

**Corrigé de l'évaluation formative.**

1. Vers le bas : `=B4*$B$1`. Vers la droite, en partant de `C2` : `=E2*$B$1`. Dans les deux sens, la référence
   relative suit le déplacement et `$B$1` ne bronche pas — c'est le `$` qui décide, pas la direction.
2. La largeur de colonne. `####` signifie « l'affichage ne tient pas », non « le calcul échoue » : double-clic sur le
   bord de la colonne, la valeur réapparaît, inchangée.
3. Parce qu'il avale toutes les erreurs, `#RÉF!` et `#NOM?` compris, et retourne un 0 ou un texte qui a l'air propre.
   On met un `SI.NON.DISP` ciblé sur `#N/A` seul, ou un test `ESTNUM` en colonne de statut, qui dit ce qu'il voit sans
   rien faire disparaître.
4. Le contrôle rend « à revoir » : une valeur plausible, égale au total amputé de la dernière ligne. C'est plus
   dangereux qu'une erreur affichée parce que le défaut est un **périmètre**, pas une syntaxe — la formule est
   parfaite, elle ne lit que 479 lignes, et rien à l'écran ne le signale.
5. Six lignes dont le produit tombe exactement à un demi-franc (sept au sens large) ; quatre où la règle d'arrondi
   change le franc ; écart de 4 FCFA avec `ARRONDI`, de 2 FCFA sans arrondi. La ligne de fiche : « montants arrondis à
   l'unité au plus proche ; écart attendu de 4 FCFA entre montant enregistré et recalculé, vérifié par la colonne
   d'écart ».
   *Question ouverte* — Réponse attendue : `Ctrl` + `'` affiche les formules et la dissidente se voit à l'œil ; en
   contrôle, une colonne `=SI(EXACT(T2;T3);"";"formule différente")` la repère ligne à ligne. Le vrai remède est
   structurel : la formule doit être **une colonne calculée du tableau**, donc identique par construction sur 480
   lignes.

---

**Suite du module.** Le chapitre C05 ouvre la boîte à fonctions : les agrégats (`SOMME`, `MOYENNE`, `NB`, `MAX`,
`MEDIANE`, `QUARTILE.INC`) et leurs cousins conditionnels (`SOMME.SI.ENS`, `NB.SI.ENS`, `MOYENNE.SI.ENS`) — ceux qui
répondent à « combien, pour qui ? » sans avoir à construire un tableau croisé.
