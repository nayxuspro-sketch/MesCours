# Projet M03.P — « Le classeur de pilotage de Sahel Distribution »

**Module M03 · projet de fin de module · 6 h · à rendre avant le module 4 · barème /20, seuil de passage 13/20**

> **Le cadre réel.** Vous êtes chez *Sahel Distribution SA*, et c'est la première fois qu'on vous demande un
> **classeur** plutôt qu'un rapport. Le directeur commercial a dit : « je veux ouvrir le fichier le lundi matin,
> changer le mois, et que tout bouge ». Cette phrase contient tout le module : une donnée nettoyée par une méthode
> écrite, des calculs qui survivent à l'actualisation, un tableau de bord qui ne ment pas sur son échelle, et une
> forme qui permet à quelqu'un d'autre de rouvrir le fichier sans vous appeler. **C'est la première pièce de votre
> portfolio : elle sera relue par un recruteur, pas seulement par moi.**

> **Note de cohérence.** Le plan validé décrit « un fichier de ventes + un fichier de cibles, classeur à trois
> feuilles : données préparées, calculs, tableau de bord ». Le socle de la formation fournit exactement ces deux
> entrées — `ventes_brutes.csv` (489 lignes énoncées) et `objectifs_de_ca.csv` (218 lignes jointes) — et le classeur
> d'entraînement du module, `m03_classeur_atelier.xlsx`, en présente une version disséquée en onze feuilles. Vous
> rendez, vous, **trois feuilles de rendu** ; les annexes sont admises, pas comptées. Les chiffres de ce corrigé sont
> ceux du socle livré, vérifiables ligne à ligne.

---

## 1. Énoncé

### Le matériel

| Élément | Chemin | Ce que c'est |
|---|---|---|
| Fichier de ventes brut | `01_socle_donnees/data/brut/ventes_brutes.csv` | le fichier reçu : 489 lignes énoncées, montants en texte, dates en deux écritures |
| Fichier nettoyé de contrôle | `01_socle_donnees/data/reference/ventes_magasin5_2025_ATTENDU.csv` | ce que la préparation doit produire : 480 lignes, 316 tickets |
| Cibles commerciales | `01_socle_donnees/data/brut/objectifs_de_ca.csv` | 218 lignes magasin × année × mois, 198 030 000 FCFA sur le magasin 5 en 2025 |
| Référentiels | `01_socle_donnees/data/brut/produits.csv`, `clients.csv`, `magasins.csv` | les dimensions du modèle |
| Classeur de référence | `01_socle_donnees/data/projection/m03_classeur_atelier.xlsx` | la version d'enseignement : 11 feuilles, 28 fiches de fonction, une grille mensuelle, une grille croisée |
| Contrôle des chiffres | `01_socle_donnees/data/reference/chiffres_cites.md` | à utiliser **après** le calcul, jamais comme source de copie |
| Outils | un tableur (Excel 2021+ ou LibreOffice Calc), Power Query et le modèle de données si votre poste les a | sinon : la voie accessible, et vous l'écrivez |

### Les six livrables

**L1 — Feuille `Données`** (la préparation, par requête). Une requête nommée, de six étapes au minimum, qui part du
CSV brut et rend 480 lignes × 16 colonnes : types corrigés, séparateur décimal des remises, dates reconstituées dans
les deux écritures, doublons traités à la règle « une ligne par ticket et par produit », quantité filtrée, colonne
`est_retour` ajoutée, plus deux colonnes de jointure `mois` et `annee_mois`. Le chemin du fichier source passe par
un paramètre ou une cellule nommée, jamais par un chemin tapé dans l'étape.

**L2 — Feuille `Calculs`** (les fiches de fonction). **Huit fiches au format du module** — nom et version · syntaxe ·
rôle de chaque argument · exemple chiffré sur le jeu de l'atelier · cas réel d'entreprise · erreur fréquente et son
symptôme — dont trois au choix hors de la liste d'office (`SOMME.SI.ENS`, `NB.SI.ENS`, `RECHERCHEX`, `INDEX`/`EQUIV`,
`FIN.MOIS`, `NB.JOURS.OUVRES`, `FILTRE` étant imposées). Chaque fiche occupe une ligne du tableau de bord des fiches
et sa formule doit être **exécutée dans la feuille**, pas décrite.

**L3 — Feuille `Pilotage`** (le tableau de bord). Un tableau croisé dynamique par catégorie (lignes, CA, moyenne,
part en % du total général), un second par mois avec les jours ouvrés, **quatre graphiques** (classement en barres,
évolution en courbes avec moyenne glissante à trois mois, parts, et un quatrième au choix argumenté), **trois
segments** (ville, catégorie, mois) connectés aux deux TCD, et le ratio `CA / objectif`. Aucune valeur tapée à la
main dans cette feuille.

**L4 — Formatage, noms, protection.** Formats monétaires FCFA à zéro décimale, pourcentages à une décimale, dates en
`JJ/MM/AAAA` ; **cinq noms** au minimum (`Debut_periode`, `Fin_periode`, `req_ventes_nettoyees`, `TCD_ca_categorie`,
`Controle_total`) ; protection de la feuille `Pilotage` avec saisie dégagée là où elle est prévue et TCD autorisés ;
structure du classeur verrouillée ; le tout ouvrant sur `Pilotage`.

**L5 — Note de cadrage** (2 pages, PDF). Ce que le classeur mesure, ce qu'il ne mesure pas, et pourquoi. Trois
rubriques obligatoires : **l'échelle** (l'extrait ne couvre que les jours 1 à 4 de chaque mois), **le dénominateur**
(CA par ligne, par ticket, par jour ouvré : les trois, avec les chiffres), **la voie** (ce qui est écrit en fonction
dynamique et ce qui ne l'est pas, et sur quel poste ça casse). Vous y joignez la **procédure d'actualisation** en
cinq lignes max, écrite pour quelqu'un qui ne vous connaît pas.

**L6 — Le dossier de rejouabilité.** Un classeur vierge de vos feuilles de résultat, reconstruit en une seule
actualisation depuis le CSV, avec l'état des contrôles à l'appui : la page d'un tableur montrant `Controle_total` à 0,
le compte de lignes de la requête, et le message exact renvoyé si le fichier source a bougé. C'est la partie que le
correcteur exécute en premier ; elle vaut même si le reste est imparfait.

### Contraintes de rendu

1. Deux fichiers : `2026-MM-JJ_projet_M03_P_votre_nom.xlsx` et `2026-MM-JJ_projet_M03_P_note.pdf`. Le classeur est
   ouvert sur `Pilotage`, zoom 100 %, aucune sélection en cours.
2. Aucune valeur saisie dans `Pilotage` : tout vient d'un TCD, d'une mesure, ou d'une formule qui lit la feuille
   `Données`. Aucun chiffre recopié depuis `chiffres_cites.md` sans son calcul à portée de clic.
3. Chaque cellule de contrôle est écrite en équation visible (`=total_TCD - total_source`, attendu 0), pas en
   commentaire « vérifié ».
4. Les graphiques portent un titre qui dit la granularité et la période, et une source en légende.
5. Si votre poste n'a ni Power Query ni modèle de données (LibreOffice, Excel pour Mac, Excel 2019 sans add-in) :
   vous livrez la voie accessible **et** vous écrivez en L5 ce que la voie moderne aurait changé. Le barème ne
   sanctionne pas l'outil, il sanctionne le silence sur l'outil.
6. **Interdits** : macro enregistrée en guise de nettoyage ; mise en forme conditionnelle qui colore un chiffre que
   rien ne contrôle ; format date appliqué à une colonne de texte sans conversion ; TCD pointant sur une plage figée ;
   mot de passe présenté comme une confidentialité.

---

## 2. Barème détaillé

| # | Critère | Pts | Ce qui fait perdre les points |
|---|---|---|---|
| 1 | L1 : requête en six étapes, paramétrée, rendant 480 lignes justes | 4 | doublons traités sur le ticket seul ; étapes anonymes ; chemin absolu en dur |
| 2 | L2 : huit fiches exécutées, au format imposé, avec leur erreur fréquente | 4 | fiche descriptive sans formule ; exemple hors jeu de l'atelier ; « cas réel » rédigé en généralité |
| 3 | L3 : deux TCD, quatre graphiques, trois segments, ratio à l'objectif | 5 | segments connectés à un seul TCD ; parts calculées à la main ; graphique héritant d'un filtre caché |
| 4 | L4 : formats, cinq noms, protection utilisable | 2 | TCD inactualisable sous protection ; formats FCFA absents ; aucune plage nommée |
| 5 | L5 : note de cadrage — échelle, dénominateur, voie | 3 | « 27,9 % » écrit sans dire que décembre n'a que quatre jours dans l'extrait |
| 6 | L6 : dossier de rejouabilité et contrôles à zéro | 2 | contrôle annoncé mais non écrit ; actualisation qui ne repart pas du CSV |
| | **Total** | **20** | seuil de passage en M04 : **13** |

---

## 3. Correction pas à pas (corrigé enseignant)

Ce corrigé est un compte-rendu d'exécution. Les valeurs sont celles du socle livré ; si votre fichier diffère,
régénérez le socle avant de vous comparer. Le correcteur ouvre d'abord le classeur, jamais la note.

### 3.1 — L1 : la préparation attendue, étape par étape

| # | Étape de requête | Ce qu'elle doit produire, chiffré |
|---|---|---|
| 1 | *Source* (chemin lu dans un paramètre) | 489 lignes lues, 13 colonnes, types non figés |
| 2 | *Remplacer* `.` par `,` puis *Charger le type* sur les montants | 486 des 489 montants arrivaient en texte, 3 seulement en nombre |
| 3 | *Analyser les dates* : 424 en `AAAA-MM-JJ`, 65 en `JJ/MM/AAAA` | une colonne date typée, amplitude du 01/01/2025 au 02/12/2025 |
| 4 | *Doublons* sur `n_ticket` + `produit`, après tri | 12 lignes retirées, 481 978 FCFA ; la variante sur le ticket seul retire 173 lignes et 11 424 263 FCFA — erreur de lot complète |
| 5 | *Filtrer* `quantite` ≤ 500 | 7 lignes hors échelle, maximum reçu 14 000 contre 68 après correction d'unité |
| 6 | *Colonne personnalisée* `est_retour` | 8 lignes vraies à VRAI, 283 933 FCFA retirés du CA s'ils sont exclus à tort |
| 7 | *Colonnes de jointure* `mois` et `annee_mois` | 12 valeurs de mois, une clé texte unique par ligne d'objectif |

Le chargement attendu est **connexion uniquement + ajout au modèle de données**, avec une table visible dans
`Données` pour l'œil : 480 lignes × 16 colonnes. Le total de contrôle, `=SOMME(Données[montant_ttc])`, doit rendre
36 073 185 FCFA, soit exactement la somme du fichier nettoyé. Un candidat qui a 36 339 317 FCFA n'a pas retiré les
doublons : l'écart est de 266 132 FCFA, et il est écrit dans le corrigé de M01.C06.

Deux points de discrimination, visibles sans ouvrir la note :

1. **la colonne `categorie` provient-elle d'une jointure ou d'une recopie ?** Le livrable attendu la tire de
   `produits` par relation (ou par `RECHERCHEX` dans la voie accessible), pas d'un collage depuis le CSV reçu — la
   preuve est dans l'en-tête de la table : `produits` amène le libellé, pas la vente.
2. **les 103 lignes de client introuvable sont-elles nommées ?** 85 portent le client comptoir `0`, 18 n'ont rien :
   la préparation correcte crée une valeur lisible (« comptoir » ou « non renseigné ») plutôt que de laisser un TCD
   afficher un blanc en tête de classement.

### 3.2 — L2 : ce que rendent les fiches exécutées dans `Calculs`

Les huit valeurs de contrôle ci-dessous sont celles que la feuille de l'atelier affiche ; le candidat doit les
retrouver, pas les recopier.

| Fonction | Valeur attendue sur l'atelier | Détail de contrôle |
|---|---|---|
| `SOMME` | 36 073 185 FCFA | sur `montant_ttc`, 480 lignes |
| `MOYENNE` | 75 152 FCFA | par **ligne**, à ne pas confondre avec le panier |
| `MEDIANE` | 37 966 FCFA | la moitié des lignes est en dessous |
| `ECARTYPE.STANDARD` | 143 915 FCFA | supérieur à la moyenne : aucune moyenne ne représente ce fichier |
| `MAX` / `MIN` | 1 229 678 / −150 804 FCFA | le minimum est un retour, pas une erreur de signe |
| `QUARTILE.INC` (1, 3) | 12 950 / 74 234 FCFA | la moitié centrale tient sur `61 284` FCFA |
| `NB.JOURS.OUVRES` | 240 jours | du 01/01/2025 au 02/12/2025, fériés non retirés |
| `SOMME.SI.ENS` / ratio | 18,2 % | 36 073 185 FCFA sur 198 030 000 FCFA d'objectif magasin 5 |

La fiche la plus ratée est `NB.SI`/`NB` sur une colonne texte : le candidat qui compte les montants du fichier reçu
avec `=NB()` obtient 0, et beaucoup écrivent dans la fiche « 0 montants, donc un fichier vide ». Le symptôme à
documenter est l'inverse : `=SOMME()` sur la même plage rend 0 sans erreur, ce qui est précisément le piège traité en
M03.C05. La fiche la mieux notée est celle qui montre un `RECHERCHEX` échouant sur une clé avec espace invisible, et
sa correction par `SUPPRESPACE` — trois lignes, un cas réel, un symptôme.

### 3.3 — L3 : le tableau de bord, avec ses nombres

Le TCD par catégorie doit rendre, dans cet ordre de classement :

| catégorie | lignes | CA (FCFA) | moyenne par ligne | part | lignes remisées |
|---|---|---|---|---|---|
| Plomberie | 57 | 8 754 982 | 153 596 | 24,3 % | 22 |
| Matériaux | 143 | 6 519 357 | 45 590 | 18,1 % | 49 |
| Electricité | 53 | 6 311 645 | 119 088 | 17,5 % | 21 |
| Bois & panneaux | 24 | 4 844 758 | 201 865 | 13,4 % | 10 |
| Quincaillerie | 112 | 4 203 121 | 37 528 | 11,7 % | 45 |
| Peinture | 34 | 2 938 358 | 86 422 | 8,1 % | 8 |
| Consommables | 57 | 2 500 964 | 43 877 | 6,9 % | 18 |
| **Total** | **480** | **36 073 185** | **75 152** | **100,0 %** | **173** |

Vérifications que le correcteur fait au clavier, dans l'ordre : la ligne de total contre `=SOMME(Données[montant_ttc])`
(égalité exigée) ; les lignes 480 contre le compte du tableau ; la part sommant à 100,0 % quand aucun segment n'est
cliqué ; la colonne « moyenne par ligne » recalculée en `CA / lignes` catégorie par catégorie, et **non** comme la
moyenne des sept moyennes — la seconde écriture vaut 98 281 FCFA et fait perdre le point de L3 en entier, parce
qu'elle se présente joliment.

Le TCD par mois, lui, attend douze lignes de 40 lignes chacune (la régularité est celle de l'extrait, pas du
magasin) et un CA qui court de 1 258 801 FCFA (mai) à 5 292 517 FCFA (décembre). Les quatre graphiques attendus :
barres horizontales du classement par CA, courbe du CA mensuel avec la glissante à trois mois en deuxième série,
barres empilées ou camembert **avec la mention que deux parts voisinent à 0,6 point** (18,1 % et 17,5 %) si le
candidat a choisi le camembert, et un quatrième au choix — le top 5 des produits est l'option la plus tenue :

| produit | CA (FCFA) | lignes |
|---|---|---|
| Robinet mitigeur évier — réf 1 | 1 976 000 | 14 |
| Robinet mitigeur évier — réf 2 | 1 794 026 | 13 |
| Lame de lambris 4 m — réf 2 | 1 529 811 | 11 |
| Lavabo céramique — réf 1 | 1 485 299 | 10 |
| Régulateur de charge 10 A — réf 1 | 1 369 527 | 12 |

Les trois segments (ville, catégorie, mois) doivent être connectés aux **deux** TCD : c'est le réglage
« Connexions de rapports », et c'est le point de barème le plus souvent perdu en L3, parce qu'il est invisible
jusqu'à ce qu'on clique. Le ratio `CA / objectif` attend 18,2 % sur l'année de l'extrait, et les valeurs mensuelles
les plus hautes autour de 27,9 % en décembre contre 14,1 % en octobre : le bon rendu écrit à côté, dans la même
zone, que ce ratio rapporte quatre jours de vente à un mois de cible.

### 3.4 — L4 : noms, formats, protection

Cinq noms au minimum, et deux sont contrôlés par le correcteur par leur **usage** : `Debut_periode` et
`Fin_periode` doivent apparaître dans les critères des `SOMME.SI.ENS` et dans la source des segments de chronologie ;
si les dates des graphiques sont figées en dur, le point n'est pas acquis même si les noms existent. `Controle_total`
désigne la cellule d'égalité (attendu 0), et `TCD_ca_categorie` la plage du TCD — utile pour l'export et pour la
mise en forme conditionnelle, qui ne doit colorer aucun chiffre non contrôlé.

Protection : la feuille `Pilotage` est verrouillée, **les segments restent utilisables**, l'onglet *Données →
Actualiser tout* fonctionne, la structure du classeur empêche de supprimer `Calculs`. Trois formats à vérifier à
l'œil : montants sans décimale avec le code FCFA, parts à une décimale, `JJ/MM/AAAA` aux deux bornes de période. Le
classeur s'ouvre sur `Pilotage` (dernière feuille active enregistrée, ou macro d'ouverture — ici admise, parce
qu'elle ne touche pas à la donnée).

### 3.5 — L5 : la note, et les trois phrases qui font la différence

1. **L'échelle.** « Le fichier d'entraînement couvre les jours 1 à 4 de chaque mois de 2025 : 25,6 % des lignes
   tombent un samedi ou un dimanche, 40 lignes par mois exactement, 240 jours ouvrés sur 336 jours courus. Aucune
   saisonnalité ne peut être affirmée sur cette base, et le ratio à l'objectif non plus. » Le correcteur cherche la
   mention des quatre jours : sans elle, deux points sont perdus, avec elle le reste se discute.
2. **Le dénominateur.** 75 152 FCFA par ligne, 114 156 FCFA par ticket, 150 305 FCFA par jour ouvré, 107 361 FCFA
   par jour couru : quatre chiffres justes, et la note doit dire lequel elle affiche et pourquoi. La mention « par
   jour travaillé » sans précision des week-ends (`9 730 140` FCFA de CA, 27,0 % de la masse) est comptée comme une
   absence.
3. **La voie.** Ce qui est écrit en fonctions dynamiques (`FILTRE`, `UNIQUE`, `TRIERPAR`, `SEQUENCE`, `LET`), ce qui
   est en voie accessible, et ce qui se passe sur les postes du service : `#NOM?` en Excel 2019 pour les dynamiques,
   pas de propagation sur LibreOffice 24.8 et antérieurs sans pré-allocation de la plage, pas de modèle de données
   sur Excel pour Mac (donc pas de « Nombre distincts »), pas de segments du tout dans Calc. Le correcteur attend la
   phrase qui dit lequel des deux il a livré et pourquoi, pas une liste d'excuses.

### 3.6 — L6 : la rejouabilité, testée comme elle le sera

Le correcteur fait ceci, en trois minutes : il ouvre le classeur, supprime la feuille `Données` et les TCD, clique
*Données → Actualiser tout*, puis vérifie quatre nombres — 480 lignes, 36 073 185 FCFA, 12 mois, 0 à la cellule de
contrôle. Quatre défauts type, et leur traduction en points :

| Défaut observé | Diagnostic | Conséquence au barème |
|---|---|---|
| l'actualisation redemande le chemin du fichier | paramètre absent, chemin en dur dans l'étape *Source* | L1 amputé de 2 pts, L6 de 1 |
| le TCD revient vide | la source pointait une plage supprimée avec la feuille | L6 à 0, L3 plafonné à 2 |
| le total revient à 36 339 317 FCFA | les doublons étaient retirés à la main dans la feuille, pas dans la requête | L1 à 1, L6 à 1 |
| le ratio d'objectif passe à « #DIV/0! » | la jointure `annee_mois` a été perdue en rechargeant le CSV | L3 à 2, L5 amendée |

Un dossier qui montre le message d'erreur attendu quand le fichier source a bougé (« chemin introuvable », avec la
correction en deux lignes) vaut le point entier de L6 : c'est la seule preuve que le livrable est compris et pas
seulement produit.

---

## 4. Grille d'auto-évaluation avant rendu

Répondez par oui ou non ; trois « non » = ne rendez pas, reprenez la feuille concernée.

| # | Question | Si non |
|---|---|---|
| 1 | La requête repart-elle bien du CSV brut et rend-elle 480 lignes ? | reprendre M03.C08 §5.5 |
| 2 | Les doublons sont-ils retirés sur `n_ticket` **et** `produit`, après un tri explicite ? | reprendre M03.C03 §5.4 et M03.C08 ex. 8.4 |
| 3 | Les montants sont-ils numériques dans la table finale (`=NB()` = 480) ? | reprendre M03.C02 §5.2 |
| 4 | La colonne date est-elle une série, pas du texte (`=MOIS()` fonctionne) ? | reprendre M03.C07 §5.1 |
| 5 | Les huit fiches sont-elles exécutées, pas décrites ? | reprendre le format de fiche, §3 des chapitres |
| 6 | Chaque TCD affiche-t-il un total égal à la somme de la colonne source ? | reprendre M03.C08 §5.1 |
| 7 | Les trois segments sont-ils connectés aux deux TCD ? | reprendre M03.C08 §5.3 |
| 8 | Le graphique reprend-il les filtres cachés du TCD au moment de sa création ? | reprendre M03.C08 §5.4 |
| 9 | Les parts sont-elles en « Total général en % » et non calculées à la main ? | reprendre M03.C08 §5.1 |
| 10 | Le ratio à l'objectif est-il accompagné de la mention d'échelle ? | reprendre M03.C07 §6 |
| 11 | La protection laisse-t-elle actualiser et cliquer ? | reprendre M03.C08 §5.8 |
| 12 | Un autre poste peut-il ouvrir le classeur sans `#NOM?` ni plage vide ? | écrire la voie alternative, M03.C07 §5.7 |

---

## 5. Ce que le correcteur regardera en premier

1. **Le compte de lignes de la requête, à l'étape 4.** 480, pas 468 ni 316 : c'est la ligne qui dit si le doublon a
   été compris comme un défaut de fichier ou comme une règle métier.
2. **La cellule de contrôle.** `Controle_total` doit être une formule, pas un 0 écrit. Un zéro tapé est un aveu, pas
   une preuve.
3. **Le segment qui ne fait rien.** Premier clic sur un segment : si un seul des deux TCD bouge, le candidat n'a pas
   ouvert « Connexions de rapports », et le tableau de bord est décoratif.
4. **La phrase d'échelle.** Dans la note ou sous le graphique, « les jours 1 à 4 de chaque mois » doit se lire. C'est
   le seul endroit du projet où l'honnêteté du module M02 est vérifiable dans un livrable Excel.
5. **La liste des voies.** Un classeur qui n'utilise que des fonctions que deux postes sur cinq peuvent exécuter n'est
   pas un livrable, c'est une démonstration. À l'inverse, un classeur 100 % accessible avec une ligne qui dit ce que
   `FILTRE` aurait économisé est noté comme un travail de professionnel.
