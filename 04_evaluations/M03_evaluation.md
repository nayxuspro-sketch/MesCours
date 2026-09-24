# Évaluation M03 — « Excel, du clic à la méthode »

**Module M03 · durée totale 2 h 30 · quatre épreuves · seuils : quiz 11/15, étude de cas 12/20, projet 13/20**

| Épreuve | Durée | Barème | Noté | Ce qui est attendu |
|---|---|---|---|---|
| A · Questions de récupération | 15 min | non noté | non | vérifier qu'on a lu les huit chapitres avant de se tromper cher |
| B · Quiz | 25 min | /15 | oui | quinze questions à réponse unique, dont trois sur l'identification d'une erreur affichée |
| C · Exercices pratiques | 50 min | /20 (auto-corrigé) | oui | quatre exercices menés jusqu'au chiffre sur le classeur de l'atelier |
| D · Étude de cas | 60 min | /20, seuil 12 | oui | un dossier en quatre pages : un tableau de bord à déclarer pilotable ou non |

> Le score du module se lit ainsi : **B ≥ 11** et **D ≥ 12** ouvrent le module 4 ; le projet M03.P doit atteindre 13.
> Un candidat qui réussit B et échoue à D repasse uniquement D : savoir ce que fait `FIN.MOIS` ne dispense pas de
> dire ce que vaut le ratio affiché dans un comité.

---

## A · Questions de récupération (non notées)

À traiter sans document, en une phrase chacune. Elles ne sont pas comptées ; elles servent à repérer ce qui n'est pas
assimilé avant de perdre des points sur un détail de syntaxe.

1. Pourquoi `=SOMME()` sur une colonne de montants stockés en texte rend-il 0 au lieu d'une erreur, et pourquoi est-ce
   plus grave ?
2. Que devient `=DATE(25;1;1)`, et quel est le réglage qui rend ce piège impossible ?
3. Une date « 15/03/2025 » dans une cellule : citez deux tests qui disent s'il s'agit d'un nombre ou d'un texte.
4. Pourquoi un `RECHERCHEV` est-il plus dangereux qu'un `INDEX`/`EQUIV` quand on insère une colonne, et que répond
   `RECHERCHEX` à ce problème ?
5. Un TCD affiche un total inférieur à la somme de la colonne source : listez trois causes, pas une.
6. Que signifie `#PROPAGATION!`, et pourquoi n'est-ce pas une erreur de formule ?
7. Pourquoi un segment ne change-t-il rien à une cellule `=SOMME(...)` écrite à côté du TCD ?
8. « 75 152 FCFA par ligne » et « 114 156 FCFA par ticket » : lequel répondre à « combien vend-on par ticket » ?
9. Qu'est-ce qu'une macro enregistrée ne sait pas faire, et que sait faire une requête Power Query à sa place ?

---

## B · Quiz (15 questions · 15 points)

**Barème : 1 point par question, une seule bonne réponse. Les réponses justifiées en une ligne rapportent un
demi-point de bonus, plafonné à 15.**

### Bloc 1 — Types, formats, saisie (Q1 à Q4)

**Q1.** Un montant est saisi `1 234,56` (espace de milliers) dans une cellule au format Standard. Ce que la cellule
contient :
a) le nombre 1234,56 · b) le texte `1 234,56` · c) le nombre 1,23456 · d) une erreur immédiate

**Q2.** Quatre montants sur 489 sont lus comme des nombres et le reste comme du texte dans le fichier reçu. Pour
récupérer la valeur d'une cellule texte `1229678`, l'écriture correcte est :
a) `=CNUM(A1)*1` · b) `=A1&""` · c) `=CNUM(SUBSTITUE(A1;" ";""))` · d) `=ARRONDI(A1;0)`

**Q3.** Le format « Monétaire » avec le code FCFA diffère du format « Comptabilité » en ce que :
a) rien, ce sont deux noms du même format · b) la colonne des symboles reste alignée en comptabilité, pas en monétaire
· c) le comptable interdit les négatifs · d) le monétaire arrondit à l'unité

**Q4.** Une validation des données en liste refuse une valeur saisie. Le message par défaut :
a) bloque et propose la liste · b) bloque sans explication · c) avertit mais accepte · d) convertit la valeur

### Bloc 2 — Adresses et erreurs affichées (Q5 à Q8)

**Q5.** Une nouvelle colonne est ajoutée **dans** `TableVentes` avec la formule
`=SOMME(TableVentes[montant_ttc])`. Ce qui s'affiche :
a) 36 073 185 dans chaque cellule, sans erreur · b) une référence circulaire refusée · c) `#VALUE!` en tête de
colonne · d) 0 sur les lignes dont la catégorie est vide

**Q6.** Une cellule affiche `#N/A`. Parmi ces quatre situations, laquelle ne peut **pas** en être la cause ?
a) la clé cherchée n'existe pas dans la table · b) la clé porte un espace invisible en trop · c) le numéro de colonne
rendu par `RECHERCHEV` dépasse la largeur de la plage · d) la valeur renvoyée contient elle-même `#N/A`

**Q7.** Une formule matricielle dynamique renvoie `#PROPAGATION!`. La correction est :
a) valider en `Ctrl` + `Maj` + `Entrée` · b) libérer les cellules de la zone d'arrivée, hors du tableau structuré
· c) convertir la date en nombre · d) ajouter un troisième argument à `RECHERCHEX`

**Q8.** `=FILTRE(…)` rendu sur un poste en Excel 2019 affiche :
a) `#VALEUR!` · b) `#NOM?` · c) `#PROPAGATION!` · d) la première ligne du tableau seulement

### Bloc 3 — Agrégats, critères, dates (Q9 à Q12)

**Q9.** `=NB(TableVentes[date])` vaut 480, `=MOIS(TableVentes[date])` sur une cellule de la même colonne rend
`#VALEUR!`. L'explication cohérente :
a) la colonne est un mélange de dates et de texte, `=NB()` ignore le texte · b) `MOIS` n'existe pas en français
· c) la cellule appelée contient un nombre trop grand · d) le tableau est trié

**Q10.** Pour isoler le mois de février 2024 dans un `SOMME.SI.ENS` sans écrire le 29 ou le 28, on pose :
a) `">="&DATE(2024;2;1)` et `"<"&DATE(2024;3;1)` · b) `">="&DATE(2024;2;1)` et `"<=29/02/2024"` · c)
`MOIS(plage)=2` · d) `">="&DATE(2024;2;1)` et `"<="&FIN.MOIS(DATE(2024;2;1);1)`

**Q11.** `=FIN.MOIS(DATE(2025;2;1);0)` rend `45716` affiché tel quel. Ce qu'il faut faire :
a) rien, c'est le 28 février en série de dates · b) formater la cellule en date · c) ajouter 1 · d) passer par `DATEVAL`

**Q12.** Sur la période du 01/01/2025 au 02/12/2025, `=NB.JOURS.OUVRES(début;fin)` rend 240. Le chiffre devient faux
dès que :
a) l'entreprise travaille le samedi · b) des jours fériés sont chômés et non passés en troisième argument · c) la
période traverse deux années · d) l'intervalle inclut le 29 février

### Bloc 4 — Recherche, assemblage, TCD (Q13 à Q15)

**Q13.** 103 lignes de l'extrait portent un `client` absent du référentiel (85 au comptoir `0`, 18 vides). Un
`RECHERCHEX` sur ces lignes avec le quatrième argument omis renvoie :
a) 0 · b) une erreur `#N/A`, propagée aux calculs qui lisent la cellule · c) la ligne précédente · d) le texte
introuvable entre guillemets

**Q14.** Un TCD construit sur une **plage** `A1:M481` puis 20 lignes ajoutées au tableau source : à l'actualisation,
le TCD rend :
a) 500 lignes · b) 480 lignes : la plage ne s'est pas étendue · c) une erreur de source · d) 480 lignes et un
avertissement rouge

**Q15.** Dans un TCD, « Nombre » sur le champ `client` et une mesure `=DISTINCTCOUNT(ventes[client])` dans le modèle :
a) les deux rendent 480 · b) 480 d'un côté, 372 de l'autre · c) 372 des deux côtés · d) le second exige Excel 2019

---

## C · Exercices pratiques (4 exercices · 20 points)

**Matériel autorisé : le classeur `m03_classeur_atelier.xlsx` et les CSV du socle. Barème : 12 points sur E1 à E3,
8 points sur E4 ; la restitution des formules fait partie du point, pas une annexe.**

| # | Exercice | Pts |
|---|---|---|
| E1 | Formats, types, validation : rendre la colonne montant et la colonne date utilisables | 4 |
| E2 | Agrégations à critères et TCD : retrouver six chiffres, en expliquer un | 4 |
| E3 | Recherches et jointures : le référentiel, les 103 orphelins, la clé composée | 4 |
| E4 | Le classeur aux trois chiffres faux : diagnostiquer et corriger | 8 |
| | **Total** | **20** |

**E1 (4 pts).** Sur `ventes_brutes` : convertissez `montant_ttc` en nombre et `date` en série de dates, en écrivant
une formule par ligne (voie accessible) puis la requête Power Query équivalente (voie moderne). Contrôles exigés :
compte numérique 480, `MAX(date) - MIN(date)` = 335 jours, somme 36 073 185 FCFA. Ajoutez une validation des données
qui refuse une quantité supérieure à 500 et expliquez pourquoi la borne est 500 et non 68.

**E2 (4 pts).** Sans TCD, puis avec un TCD, retrouvez : le CA de la catégorie Plomberie, le nombre de lignes
remisées en Peinture, la moyenne par ligne d'Electricité, la part du CA de Bois & panneaux, le CA de mai, le CA de
décembre. Six valeurs, une formule chacune. Expliquez en trois lignes pourquoi la « moyenne des moyennes par
catégorie » n'est pas la moyenne par ligne, chiffres à l'appui.

**E3 (4 pts).** Rapportez à chaque ligne de l'extrait la catégorie du produit, le segment du client et la ville du
magasin, d'abord avec `RECHERCHEV`, puis avec `RECHERCHEX`, puis avec une relation du modèle de données. Contrôles :
les lignes sans client utile doivent être comptées et nommées ; la jointure aux objectifs se fait sur une clé
composée que vous fabriquez ; un test doit montrer ce qui casse si une colonne est insérée dans le référentiel.

**E4 (8 pts) — le classeur aux trois chiffres faux.** Un analyste a rendu le classeur ci-dessous ; il est
interne, propre, et contient trois chiffres faux.

| Ce que rend le classeur | Contexte affiché | Ce que le fichier contient |
|---|---|---|
| Chiffre d'affaires 2025 : **36 339 317 FCFA** | `=SOMME(ventes!M2:M490)` sur la feuille reçue | 489 lignes, dont neuf doublons de ticket |
| Panier moyen : **98 281 FCFA** | `=MOYENNE()` sur une colonne de moyennes par catégorie | la moyenne par ligne vaut 75 152, le panier par ticket 114 156 |
| Clients servis : **480** | `=NBVAL()` sur la colonne client du tableau de lignes | 316 tickets, 372 clients distincts |
| Réalisation décembre : **27,9 %** | ratio du CA de décembre sur l'objectif mensuel | pas faux, mais lu à tort comme une performance |

Pour chacun des trois premiers : expliquez la cause, écrivez la formule de contrôle qui l'aurait révélée, et donnez
la valeur attendue. Pour le quatrième : dites en deux lignes pourquoi ce n'est pas une erreur de calcul et ce qu'il
faut écrire sous le graphique. Bonus (non compté) : la mise en forme conditionnelle qui aurait alerté sur le premier.

---

## D · Étude de cas — « Le tableau de bord du magasin 5 est-il pilotable ? » (20 points, seuil 12)

**Le dossier.** Le responsable régional transmet un classeur qu'il utilise chaque lundi, et un courriel de trois
lignes : « Le magasin 5 est à 18,2 % de son objectif annuel en 2025. Décembre est à 27,9 %, octobre à 14,1 %.
Je félicite en décembre, je recadre en octobre. Dis-moi si le fichier tient la route avant que j'envoie ça. »

Le classeur reçu contient : une feuille `Données` (480 lignes, collées depuis un CSV, montants et dates en texte,
triest effectués à la main), une feuille `Calculs` (neuf colonnes utilitaires dont trois `RECHERCHEV` sur des
plages `A:F` figées, une moyenne glissante `=MOYENNE(B2:B13)` recopiée depuis la ligne 2), une feuille `Pilotage`
(deux TCD pointant sur la plage `Données!A1:M481`, un segment connecté à un seul TCD, un graphique en camembert de
sept parts, un ratio en colonne `=C2/D2` sans test de dénominateur), et une macro `Reparer` enregistrée qui supprime
des lignes et met en forme douze cellules. Le fichier est `.xlsx`, non protégé, et un onglet caché porte une copie
des montants en dur.

**Questions, à traiter dans cet ordre, en quatre pages maximum.**

**1.** Le chiffre de 18,2 % est-il exact, et dit-il ce que le responsable croit ? Reprenez les deux nombres (CA de
l'extrait, objectif du magasin 5 sur 2025), refaites la division, et énoncez ce que mesure ce ratio compte tenu de la
couverture réelle des lignes. Donnez les deux ratios mensuels cités, et la phrase qui doit accompagner le graphique.

**2.** Que devient ce pilotage sur la population entière des ventes (pas l'extrait) ? Chiffrez le CA annuel du
magasin 5, son ratio à l'objectif, et l'étendue des ratios magasin-mois observés dans le fichier d'objectifs. Concluez
sur la comparabilité des magasins : ce que la table d'objectifs permet et ne permet pas d'affirmer.

**3.** Listez, dans l'ordre de gravité, les sept défauts du classeur qui empêchent de le déclarer pilotable, et pour
chacun la correction au format d'une ligne de procédure (quoi faire, dans quel outil, quel contrôle à l'appui).
Trois défauts au moins doivent concerner ce qui casse à l'actualisation, pas la présentation.

**4.** Rédigez la réponse au courriel, en six lignes, avec les deux chiffres à ne pas envoyer tels quels et la
proposition de dispositif : ce qui reste dans le tableur, ce qui passe par une requête, ce qui est à sortir d'Excel.
Vous indiquez en une phrase ce que vous écrivez au sujet de la macro `Reparer`.

### Éléments de réponse attendus

**1.** Le ratio est arithmétiquement juste : 36 073 185 FCFA sur 198 030 000 FCFA d'objectif, soit 18,2 %. Il ne dit
rien d'une performance annuelle : l'extrait ne couvre que les jours 1 à 4 de chaque mois, à raison de 40 lignes par
mois, et 103 lignes sur 480 portent un client qu'on ne peut pas relier au référentiel. Les ratios mensuels cités
(14,1 % en octobre, 27,9 % en décembre) comparent la même tranche de quatre jours à un mois de cible : la mention à
écrire sous le graphique est celle de la feuille `Mensuel` du classeur d'atelier — le ratio mesure un extrait, pas
l'année. Une réponse qui corrige le pourcentage sans corriger l'échelle est comptée à moitié.

**2.** Sur la population : 528 792 330 FCFA de chiffre d'affaires pour le magasin 5 en 2025, soit 267,0 % de
l'objectif — un ratio supérieur à 100 % qui, lui non plus, ne veut rien dire tant que la table d'objectifs n'a pas
été lue (218 lignes, un objectif par magasin et par mois, des trous : deux mois de l'extrait sont sans cible). Les
ratios magasin-mois s'étagent de 1,62 à 3,27 (médiane 2,31), soit un facteur deux entre le meilleur et le pire
magasin sur cette base : la comparaison brute des pourcentages de réalisation est donc **un classement des objectifs,
pas des résultats**, tant que le mode de construction de la cible n'est pas connu. Ce qu'il faut demander : la
méthode d'élaboration des objectifs et le taux d'ouverture mensuel par magasin.

**3. Les sept défauts, dans l'ordre où ils font perdre confiance.** (a) TCD pointant sur une plage figée : à
l'actualisation, les lignes 482 à 500 restent dehors, silencieusement ; correction = sourcer sur le tableau structuré,
contrôle = total du TCD contre somme du tableau. (b) Les montants en texte : `=SOMME()` sur la feuille reçue rend
36 339 317 FCFA au lieu de 36 073 185, et sur une plage entièrement texte elle rend 0 sans erreur ; correction =
conversion dans la requête, contrôle = `=NB(colonne)` attendu 480. (c) Dates en texte avec deux écritures : le
regroupement par mois produit 36 groupes au lieu de 12, le tri alphabétique masque l'erreur ; correction = colonne
date typée et `mois` calculé. (d) `RECHERCHEV` sur plages figées : une colonne insérée dans le référentiel et les
numéros d'index décalent les libellés, sans erreur affichée ; correction = `RECHERCHEX` ou relation du modèle.
(e) Moyenne glissante `=MOYENNE(B2:B13)` recopiée depuis la ligne 2 : les onze premiers points ne sont pas des
moyennes à douze mois ; correction = garde-fou `=SI(NB(...)=12;...)` et deux premières cellules laissées vides.
(f) Ratio `=C2/D2` sans test de dénominateur : deux lignes de l'extrait n'ont pas de cible, le classeur affiche
`#DIV/0!` et le camembert ampute les parts ; correction = `SIERREUR` avec un libellé, plus une ligne « cible absente »
dans la note. (g) Macro `Reparer` qui supprime des lignes : non annulable, adressée en dur, silencieuse si la forme
change, et `.xlsm` refusé par beaucoup de postes ; correction = remplacer par une étape de requête, et ne garder la
macro que pour l'export. Le segment connecté à un seul TCD, le graphique en camembert de sept parts voisines et la
feuille cachée en dur sont trois défauts de plus, comptés comme secondaires.

**4.** Modèle de réponse : « le fichier est exact dans ses calculs, faux dans ce qu'il autorise à conclure. 18,2 %
n'est pas une réalisation annuelle mais le poids de quatre jours par mois rapportés à une cible mensuelle ; décembre à
27,9 % et octobre à 14,1 % ne se comparent pas non plus. Je propose : nettoyage par requête (six étapes, rejouées),
TCD sur le modèle de données, un segment connecté aux deux tableaux, un avis de prudence sur le ratio tant que la
fabrication des objectifs n'est pas connue. La macro `Reparer` doit être retirée du circuit : elle détruit des lignes
sans trace et ne sera pas utilisable sur les postes du service. » Toute recommandation de sanction ou de félicitation
maintenue sur ces bases fait perdre le point de conclusion.

---

## Corrigé du quiz (B)

| Q | Réponse | Une ligne de justification |
|---|---|---|
| 1 | b | l'espace de milliers non reconnu à la saisie laisse du texte ; le format ne convertit rien |
| 2 | c | `SUBSTITUE` retire l'espace, `CNUM` convertit ; b) fabrique du texte, d) convertit 0 |
| 3 | b | la comptabilité aligne symboles et décimales sur une colonne dédiée |
| 4 | a | le message par défaut bloque et propose la liste autorisée |
| 5 | a | la formule se recopie sur les 480 lignes : chaque cellule est juste, la colonne sommée vaut `17 315 128 800` FCFA, un chiffre sans sens et sans erreur |
| 6 | c | un index hors plage se signale `#REF!` ; les trois autres produisent bien un `#N/A` |
| 7 | b | `#PROPAGATION!` = la zone d'arrivée est occupée, y compris par un tableau structuré |
| 8 | b | les dynamiques sont en 365, 2021 et 2024 : en 2019, `#NOM?` |
| 9 | a | `=NB()` ignore le texte et compte les nombres : un mélange de types, pas une absence de dates |
| 10 | a | borne basse inclusive, haute exclusive, aucune mention du 29 |
| 11 | b | `FIN.MOIS` rend un nombre ; c'est le format date qui l'affiche en jour |
| 12 | b | sans troisième argument, les fériés comptent comme travaillés |
| 13 | b | `#N/A` propagé : c'est le quatrième argument (valeur si non trouvée) qui manque |
| 14 | b | la plage ne s'étend pas ; 480 lignes, sans un mot |
| 15 | b | « Nombre » compte des lignes ; le distinct exige le modèle de données |

**Seuils de lecture du quiz.** 13 et plus : les mécanismes sont acquis. 11-12 : le candidat confond encore types et
formats, reprendre C02 et C07. 10 et moins : reprendre C02, C03, C04 en mini-projets, puis une nouvelle version de B.
Les questions 6, 10 et 15 sont éliminatoires dans ma pratique : un analyste qui ne sait pas ce que fait une borne de
période écrira un faux chiffre, et un faux chiffre signé, c'est tout le module.

## Éléments de corrigé des exercices (C)

**E1.** Quatre formules de contrôle, dans cet ordre : `=NB(ventes[montant_ttc])` → 480 ; `=MAX(date)-MIN(date)` → 335
jours (et 0 si la colonne est restée texte) ; `=SOMME(ventes[montant_ttc])` → 36 073 185 FCFA ;
`=MAX(quantite)` → 68 après correction d'unité contre 14 000 dans le fichier reçu. La borne 500 se justifie par
l'échelle du métier : 7 lignes dépassaient 500 pièces, toutes issues d'un oubli de conversion d'unité, et non parce
que 68 serait un plafond physique — la formulation juste est « seuil d'alerte, pas seuil de vérité ».

**E2.** Plomberie 8 754 982 FCFA ; Peinture 8 lignes remisées ; Electricité 119 088 FCFA par ligne ; Bois & panneaux
13,4 % du CA ; mai 1 258 801 FCFA ; décembre 5 292 517 FCFA. L'explication attendue : la moyenne des sept moyennes
de catégories vaut 98 281 FCFA, la moyenne des 480 lignes 75 152 FCFA, et l'écart vient de la taille des groupes —
chaque catégorie ne pèse pas le même nombre de lignes. En tableur : `=MOYENNE(plage_de_ca)/NB(plage)` n'est pas la
moyenne des `=MOYENNE.SI.ENS(...)`, et le TCD qui agrège une colonne de moyennes reproduit exactement l'erreur.

**E3.** Trois valeurs de contrôle : les lignes rapportées (480), les 103 lignes sans client exploitable — dont 85
au client comptoir `0` et 18 au champ vide — et la clé `annee_mois` qui joint à 218 lignes d'objectifs, deux lignes
de l'extrait restant sans cible. La voie `RECHERCHEV` casse si on insère une colonne dans `produits` (les index de
retour décalent, sans erreur) ; `RECHERCHEX` ne casse pas (il recherche la valeur de la clé, pas une position) ; la
relation du modèle ne casse pas non plus et supprime trois colonnes de recopie.

**E4.** (i) 36 339 317 : neuf lignes en double, l'écart de 266 132 FCFA se lit en comparant à `=SOMME` sur le
fichier nettoyé — la formule de contrôle est `=SOMME(ventes!M:M)-SOMME(Données!M:M)`, attendu 0.
(ii) 98 281 : une moyenne appliquée à des moyennes, la valeur par ligne est 75 152 et le panier par ticket 114 156 ;
contrôle = `=SOMME(ca)/NB(lignes)`. (iii) 480 : un `NBVAL` sur une colonne de lignes de vente, qui compte 480 lignes
pour 316 tickets et 372 clients distincts ; contrôle = le nombre distincts via le modèle, ou une colonne
`=1/NB.SI()` sommée. (iv) 27,9 % : juste, mais rapporté à quatre jours de vente sur un mois de cible — la correction
est éditoriale, pas arithmétique, et c'est la raison pour laquelle le barème la compte à part. Les trois premiers
valent 2 points chacun (1 pour la cause, 1 pour la formule de contrôle), le quatrième 2 points, la ligne de mise en
forme conditionnelle 0,5 point de bonus.

## Total et décision d'orientation

| Composante | Score | Seuil | Statut |
|---|---|---|---|
| B · Quiz | ... /15 | 11 | bloquant |
| C · Exercices | ... /20 | indicatif (démarche restituée = +0,5) | — |
| D · Étude de cas | ... /20 | 12 | bloquant |
| Projet M03.P | ... /20 | 13 | bloquant |

**Décision.** B, C et D au seuil, projet au seuil → module validé, passage en M04 (qualité, préparation et
documentation des données, où le nettoyage devient une trace écrite ; le SQL en miroir s'ouvre en M05). Quiz seulement en dessous → deux jours pour reprendre C02, C04 et C07,
puis une nouvelle version de B. Étude de cas seulement en dessous → nouvelle version de D sur le même dossier, avec un
entretien de quinze minutes sur l'échelle de l'extrait. Deux échecs → reprise du module en commençant par les six
exercices autonomes de C08, puis le projet.
