# Projet M02.P — « Profil statistique du magasin 5 »

**Module M02 · projet de fin de module · 6 h · à rendre avant le module 3 · barème /20, seuil de passage 13/20**

> **Le cadre réel.** Vous êtes toujours chez *Sahel Distribution SA*. Le directeur a maintenant une phrase pour vous :
> « je ne veux pas votre moyenne, je veux la vérité du magasin ». Derrière cette phrase maladroite se trouve
> exactement le travail du module 2 : dire ce que vaut chaque indicateur, comment il a été calculé, ce qu'il dit, ce
> qu'il ne dit pas, et ce que l'extrait permet ou non d'affirmer. Vous rendez six pages, pas une.

> **Note de cohérence.** Le plan validé annonçait « Profil statistique de la Boutique Kwame, 1 500 ventes ». Le
> socle de données réel de la formation fournit un autre volume — 480 lignes et 316 tickets une fois nettoyés, pour
> le magasin 5 sur 2025 — et c'est sur lui que portent les livrables, afin que chaque chiffre du corrigé soit
> vérifiable. Le livrable, le barème et les exigences de preuve sont inchangés.

---

## 1. Énoncé

### Le matériel

| Élément | Chemin | Ce que c'est |
|---|---|---|
| Fichier de travail | `01_socle_donnees/data/reference/ventes_magasin5_2025_ATTENDU.csv` | le fichier **nettoyé** au projet M01 : 480 lignes × 13 variables, 316 tickets |
| Population de référence | `01_socle_donnees/data/reference/ventes_propres.csv` | toutes les ventes propres, 240 000 lignes ; le magasin 5 sur 2025 y tient 7 676 lignes et 4 524 tickets |
| Contrôle des chiffres | `01_socle_donnees/data/reference/chiffres_cites.md` | à utiliser **après** chaque calcul, pour vérifier — pas pour remplir |
| Outils | tableur (Excel ou LibreOffice) + Python si vous l'avez | le tableur est obligatoire au moins une fois, Python sert de contrôle |

### Les six livrables

**L1 — Page d'identité statistique** (1 page). Population visée, unité sondée, effectifs (480 lignes, 316 tickets,
7 676 lignes et 4 524 tickets en face), taux de représentation, règle d'extraction reconstituée, liste des variables
par nature (quantitatives discrètes / continues / nominales / ordinales), et les trois questions du module auxquelles
le fichier peut répondre. Une ligne par rubrique, aucune phrase de remplissage.

**L2 — Page des centres et de la dispersion** (1 page, prolongement de M02.P1 et M02.P2). Cinq indicateurs, chacun
au format *valeur · calcul · ce que ça dit · ce que ça ne dit pas* : moyenne, médiane, mode, écart type, écart
interquartiles. Vous ajoutez le coefficient de variation et vous expliquez ce qu'il fait saliver.

**L3 — Page des positions et de la forme** (1 page). Premier et troisième quartiles, trois percentiles choisis parmi
dix, quatre-vingts, quatre-vingt-quinze ; bornes de Tukey et nombre d'observations hors borne ; histogramme commenté
(classes, effectifs par classe, part du chiffre d'affaires par classe) ; asymétrie et excursion des valeurs.

**L4 — Page des liaisons** (1 page). Trois liaisons au choix, chacune avec covariance ou coefficient, effectif,
grain, carré du coefficient, droite de régression si elle a un sens, et une ligne « ce que la liaison ne dit pas ».
Vous menez en plus **un** contrôle de confusion et vous donnez les deux chiffres, avant et après.

**L5 — Page d'incertitude et de décision** (1 page). Intervalle à 95 % du panier moyen et de la médiane, biais de
l'extrait chiffré, un test de comparaison entre deux vendeurs conduit **au tableur puis vérifié en Python**, le même
test entre le magasin 1 et le magasin 5 sur l'année 2025, et la marge de détection de votre étude. Un paragraphe de
décision, une phrase de prudence.

**L6 — Anomalies et conclusion** (1 page). **Trois anomalies chiffrées** au choix (doublons, quantités hors échelle,
dates manuscrites, clients non renseignés, retours négatifs, tickets aberrants), chacune en quatre lignes : ce qui
est observé, combien, ce que ça change au chiffre, ce qui a été fait. Puis la **conclusion en cinq lignes**, qui dit
ce que l'entreprise peut décider avec ce profil, et ce qu'elle ne peut pas.

### Contraintes de rendu

1. Un seul document PDF de six pages, nommé `2026-MM-JJ_projet_M02_P_votre_nom.pdf`, plus le classeur de travail et,
   si vous en avez utilisé, les scripts.
2. Chaque page porte en pied de page : l'effectif utilisé, le grain, le nom du fichier et la date de lecture.
3. Tout nombre affiché doit être accompagné de son moyen de preuve à portée de main : capture de la formule, ligne de
   commande, ou extrait du script. Un chiffre sans méthode est compté comme faux, même juste.
4. Précision : montants en entiers de FCFA, coefficients à trois décimales, pourcentages à une décimale. Aucun
   arrondi « de présentation » non signalé.
5. Les comparaisons multiples (plus de deux groupes) doivent annoncer le nombre de tests et le seuil employé.
6. **Interdits** : recopier une valeur depuis `chiffres_cites.md` sans le calcul correspondant ; mélanger dans une
   même page un total au niveau ligne et un total au niveau ticket sans écrire lequel est lequel ; publier un test
   sans son intervalle ; conclure à l'absence de différence sur un p supérieur au seuil.

---

## 2. Barème détaillé

| # | Critère | Pts | Ce qui fait perdre les points |
|---|---|---|---|
| 1 | L1 : identité statistique exacte, règle d'extraction reconstituée | 3 | taux de représentation absent ; unité sondée confondue avec le nombre de lignes |
| 2 | L2 : cinq indicateurs justes, avec le « ce que ça ne dit pas » | 3 | mode unique annoncé alors qu'il y en a deux ; moyenne seule présentée comme « le panier type » |
| 3 | L3 : positions et forme, histogramme commenté | 4 | classes fermées qui avalent les retours négatifs ; bornes de Tukey calculées sur le mauvais effectif |
| 4 | L4 : liaisons chiffrées et contrôle de confusion mené | 3 | R² publié sans r, ou sans l'effectif ; pente extrapolée hors domaine |
| 5 | L5 : intervalles, tests exécutés aux deux outils, marge de détection | 4 | test exécuté sans grain déclaré ; p lu comme probabilité que H0 soit vraie ; bootstrap sans graine |
| 6 | L6 : trois anomalies chiffrées, conclusion honnête, journal | 3 | anomalie racontée et pas comptée ; conclusion qui généralise au-delà du périmètre |
| | **Total** | **20** | seuil de passage en M03 : **13** |

---

## 3. Correction pas à pas (corrigé enseignant)

Ce corrigé est rédigé comme un compte-rendu de travail. Les valeurs sont celles produites par les fichiers livrés du
socle ; si votre fichier diffère, régénérez-le (`python3 01_socle_donnees/scripts/generation_socle.py`) avant de
vous comparer.

### 3.1 — L1 : l'identité statistique, telle qu'elle doit être rendue

| Rubrique | Réponse attendue |
|---|---|
| Population visée | les tickets du magasin 5 sur l'année 2025 : 4 524 tickets, 7 676 lignes |
| Échantillon réellement utilisé | 316 tickets, 480 lignes — soit 7,0 % des tickets et 6,3 % des lignes |
| Règle d'extraction | les 40 premières lignes de chaque mois, triées par date : les jours 1 à 4 seulement |
| Unité sondée à retenir | le **ticket** pour toute question de clientèle, la **ligne** pour toute question de produit |
| Variables quantitatives | `quantite` (discrète), `prix_unitaire_ht`, `remise`, `montant_ht`, `montant_ttc` (continues au sens du métier : montants entiers en FCFA) |
| Variables nominales | `magasin`, `vendeur`, `produit`, `categorie` ; `client` est un identifiant, pas une quantité |
| Questions ouvertes au fichier | panier moyen et sa dispersion, structure par catégorie, liaisons quantité-montant, comparaison de vendeurs |
| Question fermée | la marge nette, la satisfaction client, l'effet d'une promotion : aucune de ces trois n'est répondable ici |

Le correcteur vérifie en priorité la troisième ligne : un candidat qui écrit « 480 lignes prises au hasard » a perdu
le fil du module, un candidat qui écrit « les 40 premières lignes de chaque mois » a compris M02.C07.

### 3.2 — L2 : centres et dispersion

| Indicateur | Valeur | Calcul | Ce que ça dit | Ce que ça ne dit pas |
|---|---|---|---|---|
| Moyenne du panier | 114 156 FCFA | somme de 36 073 185 FCFA sur 316 tickets | la masse d'affaires par ticket | 71,8 % des tickets sont **sous** cette valeur |
| Médiane | 58 423 FCFA | `=MEDIANE()` sur les 316 totaux | la moitié des tickets est en dessous | ce que font les 25 plus gros tickets |
| Modes | 6 797 et 8 260 FCFA | valeurs les plus fréquentes, deux ex-æquo | deux tailles de ticket reviennent souvent | rien sur les gros paniers, qui sont justement l'enjeu |
| Écart type | 182 095 FCFA | `=ECARTYPE.STANDARD()` | la dispersion est supérieure à la moyenne | la dispersion est tirée par la queue de droite |
| Écart interquartiles | 109 924 FCFA | 130 559 moins 20 635 | la moitié centrale s'étale sur cette plage | le chiffre d'affaires total |
| Coefficient de variation | 159,5 % | écart type sur moyenne | aucune moyenne ne représente ce fichier à elle seule | — |

Phrase à exiger en pied de page : « le ratio moyenne sur médiane vaut 1,95 : la moyenne est à peu près le double de
la médiane, ce qui signe une distribution étirée à droite, pas une augmentation générale des paniers ».

### 3.3 — L3 : positions et forme

Premier quartile 20 635 FCFA, troisième 130 559 FCFA, P10 = 7 390, P80 = 165 177, P90 = 235 318,
P95 = 435 984 FCFA ; minimum -150 804, maximum 1 343 666, étendue 1 494 470 FCFA. Bornes de Tukey : borne
supérieure 130 559 + 1,5 × 109 924, soit 295 445 FCFA, avec 25 tickets au-delà.

L'histogramme attendu compte **sept** classes, la première et la dernière ouvertes, avec 3, 133, 84, 25, 23, 17 et
31 tickets. Deux pièges de fabrication, à commenter :

1. borné à 150 000 FCFA, l'histogramme écrase la moitié du chiffre d'affaires dans la dernière classe ; six classes
   fermées font disparaître les trois tickets négatifs, qui sont pourtant la preuve qu'il y a des retours ;
2. la classe 0 à 50 000 FCFA pèse 42,1 % des effectifs et 7,3 % du chiffre d'affaires : les deux lecture doivent
   apparaître, sinon le graphique raconte « un magasin de petits clients » alors que le dernier décile porte 47,5 %
   du chiffre d'affaires.

Asymétrie 3,84, excès de kurtosis 18,25, 307 valeurs de panier distinctes sur 316 : le vocabulaire à vérifier dans
la copie est celui-là, et le mot « normale » n'y a pas sa place.

### 3.4 — L4 : liaisons

Le couple attendu, parce qu'il est instructif sans être trivial : `quantite` et `montant_ttc` au niveau ligne.
Covariance 857 634, coefficient de Pearson 0,712, Spearman 0,641, R² 50,7 %, pente 12 237 FCFA par pièce, ordonnée
à l'origine -10 402 FCFA. Contrôle exigé : la droite au point moyen rend 75 257 FCFA contre 75 152 FCFA observés —
l'écart est un arrondi d'affichage, et le candidat qui écrit ce contrôle gagne le point de méthode.

Le contrôle de confusion attendu : l'écart de panier moyen entre le premier et le dernier vendeur vaut 34 014 FCFA
toutes catégories confondues ; recompté à catégorie contenue, il remonte à 57 346 FCFA en moyenne (17 433 FCFA au
moins en Quincaillerie, 173 167 FCFA au plus en Electricité). La phrase de conclusion juste est : « à catégorie de
produits égale, les écarts entre vendeurs ne se résorbent pas — ils s'agrandissent. Le portefeuille de produits
n'explique donc pas le classement, et il ne l'innocente pas non plus. »

### 3.5 — L5 : incertitude, tests, décision

| Objet | Valeur attendue | Vérification demandée |
|---|---|---|
| Intervalle à 95 % du panier moyen | [94 078 ; 134 234] FCFA, largeur 40 156 | erreur type 10 244 FCFA retrouvée par 182 095 sur racine de 316 |
| Biais de l'extrait | -2,3 % sur la moyenne, **-14,3 %** sur la médiane | médiane des jours 1 à 4 dans la population : 58 424 FCFA |
| Bootstrap de la médiane | [52 318 ; 64 632] FCFA | 2 000 tirages, graine 20260917 |
| Valeur de population du panier moyen | 116 886 FCFA | elle est bien dans l'intervalle : la couverture est vérifiée |
| Comparaison Bationo / Ilboudo, au niveau ligne | écart 28 609 FCFA, t = 1,52, p = 0,13, IC [-8 279 ; 65 498] | tableur `=T.TEST(tab1;tab2;2;3)` puis `scipy.stats.ttest_ind(..., equal_var=False)` |
| Contrôle par permutation | p = 0,1443 | 10 000 redistributions, graine annoncée |
| Test des rangs sur le même couple | p = 0,0161 | publié avec la mention du seuil corrigé 0,0083 : non concluant après correction |
| Comparaison magasin 1 / magasin 5, sur 2025 au grain du ticket | écart -8 997 FCFA, t = -3,37, ddl 6 782,8, p = 0,000751, IC [-14 226 ; -3 767] | 14 463 tickets contre 4 524 ; moyennes 107 889 et 116 886 FCFA |
| Marge de détection de l'étude vendeurs | 52 956 FCFA par ligne à 80 % de puissance | 412 lignes par groupe auraient été nécessaires |

Les deux derniers blocs sont le cœur du livrable : le premier montre un **écart établi** (intervalle excluant zéro,
avec 14 463 et 4 524 tickets), le second montre que le même dispositif, ramené à 125 et 109 lignes, ne voit rien de
stable. Le correcteur attend la phrase qui relie les deux : « la différence entre magasins est mesurable, la
différence entre vendeurs non, et la raison est l'effectif, pas la volonté ».

Une exécution au tableur doit laisser voir : la colonne des totaux par ticket (`=SOMME.SI()`), les quatre cellules
`MOYENNE`, `NB`, `ECARTYPE.STANDARD`, puis la formule de l'erreur type et la marge. Un candidat qui rend uniquement
le p Python perd le point de méthode demandé.

### 3.6 — L6 : les trois anomalies, écrites comme attendu

1. **Neuf lignes en double** dans le fichier reçu : 36 339 317 - 36 073 185 = 266 132 FCFA comptés en trop, soit
   +0,74 % de chiffre d'affaires si on ne les retire pas. Elles ont été retirées au projet M01 et ne réapparaissent
   nulle part dans ce livrable.
2. **Sept quantités hors échelle** : maximum 14 000 pièces dans le fichier reçu, 68 une fois l'unité corrigée. Sans
   correction, la quantité moyenne serait fausse d'un facteur qui déforme la pente de la droite quantité-montant.
3. **Cent trois lignes sans client exploitable** (dont 18 sans identifiant renseigné), soit 21,5 % de l'effectif :
   toute statistique de clientèle est donc calculée sur un périmètre de fait, et le taux est à rappeler à chaque
   fois — c'est le seul des trois défauts qui ne se répare pas en nettoyant.

Conclusion en cinq lignes, modèle : *le magasin 5 sur 2025, dans l'extrait disponible, fait un panier moyen de
114 156 FCFA, intervalle [94 078 ; 134 234], et un demi-ticket type à 58 423 FCFA. La masse d'affaires est
concentrée : le dernier décile porte 47,5 % du chiffre d'affaires. Aucun classement de vendeurs n'est établi par ces
données, et l'extrait sous-estime la médiane annuelle de 14,3 % du fait de sa couverture en jours. La liaison
quantité-montant est forte (0,712) mais explique la moitié du phénomène, pas l'autre. Nous recommandons un recalcul
sur les douze mois complets avant toute décision d'assortiment.*

---

## 4. Grille d'auto-évaluation avant rendu

Répondez par oui ou non ; trois « non » = ne rendez pas, reprenez la page concernée.

| # | Question | Si non |
|---|---|---|
| 1 | Chaque page indique-t-elle effectif, grain, fichier et date de lecture ? | pied de page manquant, point perdu |
| 2 | Ai-je écrit la règle d'extraction et son effet chiffré (médiane -14,3 %) ? | reprendre M02.C07 §5.3 |
| 3 | Moyenne et médiane sont-elles données ensemble, avec le ratio commenté ? | reprendre M02.C02 |
| 4 | L'histogramme a-t-il sept classes, les deux extrêmes ouvertes ? | reprendre M02.C05 §5.2 |
| 5 | Ai-je distingué effectif et chiffre d'affaires par classe ? | reprendre M02.C05 §5.4 |
| 6 | Chaque coefficient publié porte-t-il son effectif, son grain et son carré ? | reprendre M02.C06 §9 |
| 7 | Le contrôle de confusion est-il chiffré avant/après ? | reprendre M02.C06 §5.6 |
| 8 | Chaque intervalle est-il accompagné de son erreur type et du nombre de tirages quand il vient d'un bootstrap ? | reprendre M02.C07 §5.5-5.6 |
| 9 | Chaque test annonce-t-il sa question, son grain, son seuil et le nombre de comparaisons ? | reprendre M02.C08 §5.1-5.2 |
| 10 | Ai-je écrit « non établi » là où j'ai été tenté d'écrire « identique » ? | reprendre M02.C08 §5.3 |
| 11 | Les trois anomalies sont-elles comptées, pas racontées ? | reprendre M01 (doublons) et M02.C01 |
| 12 | Un tiers peut-il rejouer mes calculs sans moi (scripts, formules, graine) ? | joindre le classeur et les scripts |

---

## 5. Ce que le correcteur regardera en premier

1. **Le pied de page de la page 2.** Effectif, grain, fichier : trois indications qui, si elles manquent, décrètent
   que le module n'a pas été travaillé mais lu.
2. **La présence de deux chiffres là où un seul suffirait.** Moyenne *et* médiane, r *et* R², p *et* intervalle,
   écart avant *et* après contrôle : le module 2 se joue là, pas dans la justesse arithmétique.
3. **La mention du biais de couverture.** Une seule page, même mal mise en forme, qui écrit « jours 1 à 4 » et
   « -14,3 % » vaut plus que six pages impeccables qui l'ignorent.
4. **La discipline sur les comparaisons.** Six comparaisons annoncées comme telles avec un seuil corrigé, c'est un
   comportement professionnel, pas une coquetterie technique.
5. **La conclusion.** Cinq lignes qui disent ce que l'on peut décider — et ce que l'on ne peut pas — sont la vraie
   livraison du module. Une conclusion qui promet une action non fondée sur les pages précédentes fait perdre le point
   entier.
