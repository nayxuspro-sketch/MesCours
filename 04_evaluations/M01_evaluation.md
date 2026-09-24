# Évaluation du module M01 — récupération, quiz, exercices, étude de cas, corrigés

**Durée totale conseillée : 2 h 30 · Deux notes indépendantes, ni l'une ni l'autre négociable : quiz sur 20 (seuil de passage 14/20) et étude de cas sur 20 (seuil 12) · Le projet de module est noté séparément, sur 20, seuil 13 (`03_exercices/M01_projet.md`)**

Le module est validé quand les trois notes sont au seuil. Chaque instrument répond à une question différente, et c'est pour cela qu'ils ne se compensent pas : le quiz dit si vous savez, les exercices si vous savez faire, l'étude de cas si vous savez cadrer avant de faire, le projet si vous savez livrer.

| Instrument (barèmes du manuel, partie B.6 de l'architecture) | Barème | Durée | Ce qui est vérifié |
|---|---|---|---|
| A. Récupération — 7 questions | non noté, auto-corrigé | 15 min | la mémoire des sept chapitres, sans relire |
| B. Quiz — 15 questions | **/20**, seuil 14/20 | 30 min | le vocabulaire, les types, la structure d'une table |
| C. Exercices pratiques — 4 exercices | auto-correction par résultat attendu chiffré | 45 min | le geste : compter, convertir, contrôler |
| D. Étude de cas — 5 demandes | grille à 5 critères, **/20**, seuil 12 | 60 min | le cadrage, avant tout calcul |

Matériel autorisé : le fichier `ventes_magasin5_2025.csv` (489 lignes), `tarif_fournisseur_peinture.csv`, un tableur, un éditeur de texte. Matériel interdit : le corrigé, les notes du projet M01.P (l'évaluation sert à vérifier que le savoir est **en vous**, pas dans votre dossier).

---

## A. Questions de récupération (non notées, à traiter avant le quiz)

Répondez en une phrase, sans relire. Toute réponse hésitante = relecture ciblée du chapitre indiqué.

1. Que représente une ligne du fichier de l'atelier ? *( C03 · un article d'un ticket, pas une vente )*
2. Quelle est la différence entre un format et un type ? *( C04 · l'apparence vs la nature de la valeur, donc ses opérations permises )*
3. Combien de lignes a le fichier, et combien de tickets ? *( C03 · 489 et 316 )*
4. Que fait `=NB()` que `=NBVAL()` ne fait pas ? *( C04 · il ignore le texte : la différence des deux mesure les montants mal typés )*
5. Un fichier en `;` encodé en Windows-1252 est-il cassé ? *( C05 · non : il est lisible, c'est la lecture qui est mal réglée )*
6. Citez les trois documents qui rendent un chiffre défendable dans trois ans. *( C06 · dictionnaire de données, journal de transformation, manifeste d'archivage )*
7. Quels sont les cinq composants d'une question analytique ? *( C02/C07 · objet, unité + définition, comparaison, périmètre, critère de réussite )*

---

## B. Quiz — 15 questions, noté sur 20

**Barème : 10 questions à 1 point (Q3, Q5, Q6, Q7, Q8, Q10, Q12, Q13, Q14, Q15) et 5 items-piège à 2 points (Q1, Q2, Q4, Q9, Q11), où la justification écrite est exigée : 10 × 1 + 5 × 2 = 20.** Une réponse juste sans justification sur un item-piège vaut 1 point sur 2 ; une justification sans réponse vaut 0. Les items-piège ne testent pas la mémoire des mots mais la frontière entre eux. Répondez par Vrai/Faux ou choisissez l'option ; le corrigé commenté suit immédiatement, à ne consulter qu'après avoir tout traité.

### Frontières du vocabulaire (Q1 à Q4)

**Q1.** « Une donnée est une information. » Vrai ou faux ?

**Q2.** « Une colonne `id_client` remplie de nombres est une variable quantitative. » Vrai ou faux ?

**Q3.** « Un CSV ne contient pas de types de données. » Vrai ou faux ?

**Q4.** « Une fois formatée en date, une cellule contient une date. » Vrai ou faux ?

### Structure et lecture d'une table (Q5 à Q9)

**Q5.** Sur le fichier de l'atelier, combien de tickets distincts pour 489 lignes ?
 a) 489  b) 480  c) 316  d) 145

**Q6.** Quelle colonne, à elle seule, peut servir de clé primaire de ce fichier ?
 a) `n_ticket`  b) `produit`  c) `date`  d) aucune

**Q7.** Vous voulez compter « le nombre d'articles facturés » et « le nombre de ventes ». Quelle paire de comptages ?
 a) lignes, tickets distincts  b) tickets distincts, lignes  c) clients distincts, produits distincts  d) montants distincts, lignes

**Q8.** Le fichier `ventes_propres.csv` du socle contient :
 a) 243 360 lignes  b) 240 000 lignes  c) 489 lignes  d) 1 339 lignes

**Q9.** Un tableau croisé affiche un total exactement double du total de la colonne. Cause la plus probable :
 a) une ligne de sous-total importée comme donnée  b) un encodage différent  c) des dates au format français  d) un identifiant client en texte

### Types, formats, encodages (Q10 à Q13)

**Q10.** Combien de lignes de `montant_ttc`, dans le fichier de l'atelier, ne sont pas des nombres ?
 a) 0  b) 3  c) 486  d) 489

**Q11.** Après nettoyage complet, le CA TTC de l'extrait passe de 36 339 317 à 36 073 185 FCFA. Cet écart de 266 132 FCFA provient de :
 a) lignes en double  b) retours négatifs  c) TVA mal appliquée  d) arrondis successifs

**Q12.** Le fichier du fournisseur compte 42 lignes. Combien de références ?
 a) 42  b) 41  c) 38  d) 39

**Q13.** Un fichier dont les accents s'affichent `Ã©` a été :
 a) corrompu par l'e-mail  b) écrit en UTF-8 et lu en Windows-1252 (ou l'inverse)  c) enregistré au format XLS  d) tronqué

### Posture et méthode (Q14 et Q15)

**Q14.** Le directeur demande « est-ce que ça marche bien ? ». La **première** action correcte est :
 a) charger le fichier dans le tableur  b) construire un graphique de CA mensuel  c) demander quelle décision dépend de la réponse  d) proposer Power BI

**Q15.** Sur un échantillon de 480 lignes représentant 40 lignes par mois, vous affirmez « décembre est le meilleur mois de 2025 au magasin 5, la preuve d'une forte saisonnalité ». Ce raisonnement est :
 a) correct, le chiffre est exact  b) incorrect : l'extrait n'est pas la population, et un classement sur échantillon ne prouve pas une saisonnalité  c) correct si le total de contrôle est bon  d) incorrect, car il faudrait inclure 2026

---

## C. Exercices pratiques (4) — séries E1 et E2, auto-correction

Ces quatre exercices ne sont pas notés au quiz : ils sont **validés par le résultat attendu**, parce que dans le métier un résultat ne se discute pas, il se vérifie. Traitez les quatre, comparez vos chiffres à l'attendu, puis lisez le corrigé. Un attendu manqué de peu n'est pas un demi-exercice réussi : cherchez l'écart, c'est là qu'est l'apprentissage.

**Exercice C.1 (série E1).** Ouvrez `ventes_magasin5_2025.csv` dans un éditeur de texte. Notez : le séparateur, le nombre de colonnes de la ligne d'en-tête, le contenu de la ligne 2 en trois mots, et une anomalie visible **sans calculer**. *(attendu : `;` · 13 · ticket, date, montant en texte · par exemple l'espace dans `56 658` ou la date `12/01/2025`)*

**Exercice C.2 (série E1).** Dans le tableur, importez avec toutes les colonnes en texte, puis donnez, par trois formules : le nombre de lignes de données, le nombre de valeurs numériques de `montant_ttc`, le nombre de lignes dont `date` contient un `/`. *(attendu : `=NBVAL(A2:A490)` = 489 · `=NB(M2:M490)` = 3 · `=NB.SI(B:B;"?*/*/*")` = 65)*

**Exercice C.3 (série E2).** Produisez le fichier nettoyé attendu : 480 lignes, dates en ISO, `montant_ttc` en nombre, `quantite` rétablie sur les 7 lignes aberrantes (÷ 1 000), `client` conservé tel quel, y compris les 18 vides et les `0` de comptoir. Donnez le total de contrôle. *(attendu : 36 073 185 FCFA ; la comparaison avec `ventes_magasin5_2025_ATTENDU.csv` est le contrôle de forme)*

**Exercice C.4 (série E2).** Convertissez le fichier du fournisseur en un tableau propre de 38 lignes × 6 colonnes, prix en nombre, TVA conservée. Donnez le prix moyen et le prix maximal. *(attendu : 11 155 FCFA en moyenne, 34 826 FCFA au maximum, TVA 0,18 sur toutes les lignes ; encodage cp1252, 3 lignes de chapeau ignorées, virgule décimale traitée)*

---

## D. Étude de cas — « Le patron veut savoir des choses » (20 points, seuil 12)

**Contexte.** Samedi matin, marché de Kaya. Le directeur de Sahel Distribution SA vous retient trente secondes près du parking et dit, d'un trait, les cinq phrases ci-dessous. Vous n'avez ni base, ni tableau de bord, ni temps : vous avez un carnet. Consignez, pour **chacune** des cinq demandes, la décision visée et la question analytique complète (objet, unité + définition, comparaison, périmètre, critère de réussite), ainsi que la ou les tables à ouvrir et **ce qui manquera** dans le jeu de données pour y répondre.

1. « Les prix de la concurrence, il faut qu'on s'aligne, tu crois qu'on est trop chers ? »
2. « Bationo, il vend trop bien, faut le augmenter — ou pas. Regarde. »
3. « On m'a dit qu'en janvier on ne vend rien, et moi je trouve qu'en janvier ça bosse. »
4. « Si on fermait le dépôt le dimanche, ça changerait quoi ? »
5. « Le magasin 5, il me plaît. Combien il rapporte ? »

**Contraintes de rendu.** Cinq blocs de six lignes maximum, format imposé :

```
[n°] Demande (verbatim, 1 ligne)
     Décision visée · Destinataire · Échéance                 (1 ligne)
     Question analytique                                       (1-2 lignes)
     Tables et colonnes à ouvrir                                (1 ligne)
     Manquant / limite qui empêche de conclure                  (1 ligne)
     Outil choisi + motif en 4 mots                             (1 ligne)
```

**Grille de notation — 5 critères, 4 points par demande (5 × 4 = 20 points, seuil de validation 12).** Pour chaque demande : question analytique comportant les cinq composants (1,5) · décision, destinataire et échéance nommés (1) · limite réellement limitée et non générique (0,5) · choix d'outil justifié par une contrainte et non par un goût (1). Un bloc qui répond à la place de cadrer est noté 0 : on ne demande pas ici le chiffre, on demande la question. Le dixième point de la grille est un point de **cohérence d'ensemble** : les cinq demandes doivent se ressembler (même gabarit, mêmes colonnes appelées), parce qu'un cadrage qui change de forme d'un dossier à l'autre n'est pas un cadrage, c'est une humeur du moment.

---

## Corrigé de l'évaluation (à consulter après traitement complet)

### B. Quiz — réponses et explications

**Q1 — Faux.** Une donnée est un fait brut ; elle devient information quand elle est replacée (quoi, qui, quand, unité). `56 658` n'est pas un chiffre d'affaires ; « 56 658 FCFA TTC, ligne 1 du ticket du 01/01/2025, magasin 5 » en est une. *Le piège est réel : dans le langage courant, les deux mots sont interchangeables ; dans le métier, non.*

**Q2 — Faux.** C'est un **identifiant**, donc une valeur nominale : le calculer, le moyener, le trier par ordre numérique n'a aucun sens. Le test : « une soustraction a-t-elle un sens ? » `10 857 − 3 312` ne veut rien dire.

**Q3 — Vrai.** Un CSV est du texte ; le type apparaît quand un outil le déclare ou le devine. C'est pourquoi les identifiants doivent être explicitement lus comme texte (et pourquoi le `075845` final du ticket `T05-250101-075845` deviendrait `75845` si un tableur le lisait comme un nombre).

**Q4 — Faux.** Le format change l'affichage, pas la nature de la valeur. Une cellule affichant `12/01/2025` peut contenir le texte « 12/01/2025 » (et refuser tout calcul de mois) ou le nombre 45669 (le douzième jour de l'année 2025 compté depuis l'origine du tableur, qui est le 00/01/1900 : une vraie date, stockée en numéro de série). Le contrôle : `=ESTNUM()` puis `=ESTDATE()`.

**Q5 — c) 316.** 480 lignes propres pour 316 tickets ; 489 est le nombre de lignes de l'énoncé, 145 le nombre de produits distincts.

**Q6 — d) aucune.** `n_ticket` se répète (1 à 4 lignes) ; `produit` et `date` aussi. L'unicité demande le couple (`n_ticket`, `produit`).

**Q7 — a).** Les lignes = les articles facturés, les tickets distincts = les ventes. Confondre les deux surestime le nombre de ventes de 55 % sur ce fichier.

**Q8 — b) 240 000 lignes.** `ventes_brutes.csv` en contient 243 360 ; 489 est l'extrait de l'atelier, 1 339 la table `dim_date`.

**Q9 — a).** Un sous-total importé comme donnée double exactement le total. Les autres options changent l'affichage ou la ponctuation, pas la somme. Vérification : compter les lignes dont la colonne-clé est vide.

**Q10 — c) 486** sur 489 (3 valeurs seulement sont numériques). Le diagnostic complet : `=NB()` = 3, `=NBVAL()` = 489, la soustraction donne le nombre de défauts.

**Q11 — a).** Les 9 lignes en double injectées par l'export de la caisse. Le calcul : 36 339 317 − 36 073 185 = 266 132 FCFA, soit +0,74 % de surévaluation si l'on ne nettoie rien. La TVA, les retours et les arrondis sont cohérents dans ce fichier.

**Q12 — c) 38** (42 lignes − 3 de chapeau − 1 d'en-tête). Un candidat qui répond 42 a importé le document, pas les données.

**Q13 — b.** Le fichier est intact, la lecture est mal réglée. Réflexe : changer l'encodage **à l'import**, jamais réenregistrer le brut.

**Q14 — c).** Avant l'outil et avant le graphique : la décision. Un tableau de bord sans décision associée ne sera pas ouvert après deux semaines.

**Q15 — b).** Le chiffre est exact (décembre 5 292 517 FCFA, mai 1 258 801, ratio 4,2), l'inférence ne l'est pas : l'extrait contient 40 lignes par mois, tous les mois ne sont donc pas représentés proportionnellement à leur activité réelle. Réponse d'analyste : « sur cet extrait, décembre domine ; pour conclure sur la saisonnalité, il faut le fichier complet du magasin ».

**Seuil et rythme.** 12 bonnes réponses sur 15 = 6/8 (correctif : 14/20 au total de l'évaluation, pas au quiz seul si l'étude de cas est pleine). Un score ≤ 8 sur 15 indique une relecture ciblée : Q1-Q4 ratées → C02 ; Q5-Q9 → C03 ; Q10-Q13 → C04-C05 ; Q14-Q15 → C06-C07.

### C. Exercices — corrigés détaillés

**C.1.** Séparateur `;` · 13 colonnes · ligne 2 = « ticket T05-250101-075845, Plâtre de construction 25 kg — réf 1, 11 unités, montant en texte `56 658` » · anomalie sans calcul : le `0.0` du client de la ligne 3 (comptoir), ou l'espace de milliers dans `51 802`, ou une date `12/01/2025` ailleurs. Sont également recevables : les lignes en double visibles au tri sur `n_ticket`, et le libellé « … — réf 1 » (deux informations dans une cellule). *Ce qui ne l'est pas : « il y a des erreurs » (non localisé).*

**C.2.** Les trois formules, et la logique derrière :

```
=NBVAL(A2:A490)          → 489     lignes de données (contrôle de l'import : pas de ligne perdue)
=NB(M2:M490)             → 3       montants réellement numériques
=NB.SI(B2:B490;"?*/*/*")  → 65       dates écrites en JJ/MM/AAAA
```

Le correcteur vérifie la **cohérence des trois** : 489 = 480 + 9 (doublons) et 486 = 489 − 3 (montants texte). Un candidat qui obtient 488 lignes a mal importé (première ligne utilisée comme en-tête ou ligne vide finale).

**C.3.** Recettes, dans l'ordre : (1) import en texte · (2) `ttc_num = CBI(SUPPRESPACE(SUBSTITUE(colonne;" ";"")))`, contrôle `=NB(colonne d'erreurs)` = 0 · (3) tri sur toutes les colonnes puis suppression des doublons stricts → 480 lignes · (4) détection des dates par le 5ᵉ caractère et reconstruction en ISO des 65 lignes concernées · (5) quantités > 500 divisées par 1 000 (7 lignes, max 14 000 → 14) · (6) `client` laissé en l'état, avec une note : 18 vides, et les `0` = comptoir · (7) total : **36 073 185 FCFA**.
Comparaison finale : `=SOMME` du fichier attendu (même fichier, 480 lignes) — égalité demandée à 0 FCFA près, non négociable : si l'écart n'est pas nul, une ligne a été supprimée à tort (le cas habituel : les 7 lignes de quantité, traitées en correction au lieu d'un marquage).

**C.4.** Import : `;`, encodage Windows-1252, 3 lignes sautées, colonne `prix_unitaire` en texte puis `SUBSTITUE(cellule;".";"")` et remplacement de la virgule par le point avant conversion → 38 lignes, 6 colonnes. Moyenne **11 155 FCFA**, maximum **34 826 FCFA**, TVA 0,18 partout. Contrôles demandés : nombre de lignes (38), aucune valeur nulle, et `prix × 1,18` cohérent avec une grille interne si l'apprenant la consulte (bonus de méthode, pas de résultat).

### D. Étude de cas — cinq cadrages attendus

Les cinq réponses ci-dessous sont des **modèles de rendu**, pas des réponses uniques : un candidat peut formuler autrement, à condition de conserver les cinq composants et la limite. Les numéros de lignes et de colonnes cités existent dans le socle fourni.

**1. « On est trop chers ? »**
*Décision* : réviser la grille avant la campagne de décembre (direction commerciale, arbitrage avant le 30/11). *Question analytique* : « Entre 2023 et 2025, le prix moyen HT des 154 références a-t-il évolué moins vite que leur coût d'achat HT (`couts_achat.csv`, 1 694 lignes), et dans quelle proportion l'écart de marge brute s'explique par la remise plutôt que par le prix ? » *Tables* : `ventes`, `produits`, `couts_achat`. *Manquant* : **le prix des concurrents** — aucune donnée externe dans le jeu ; seule une étude terrain (20 références relevées au marché) le fournirait, à chiffrer comme tâche distincte. *Outil* : SQL ou tableur selon le volume ; motif : « calcul de taux sur 240 000 lignes ».
Le point de lucidité attendu : dire que « trop cher » ne se mesure pas **dans ces données**, et proposer le relevé terrain comme complétement — c'est ce qui distingue un cadrage d'une promesse.

**2. « Bationo vend trop bien, faut l'augmenter ? »**
*Décision* : politique de prime, direction générale, avant le prochain trimestre. *Question analytique* : « Sur 2025 (extrait magasin 5), le CA TTC et le **nombre de tickets distincts** par vendeur placent-ils A. Bationo en tête après retrait des 9 doublons, et cet écart tient-il au panier moyen (114 156 FCFA) ou au volume de tickets ? » *Tables* : `ventes`, `vendeurs.csv` (22). *Manquant* : `vendeur` n'existe que sur l'extrait du magasin 5 (4 vendeurs sur 22) ; la comparaison à l'ensemble des vendeurs suppose le fichier complet ; et une prime se discute avec la **marge**, non le CA — la marge nette n'est pas calculable (aucun coût de structure). *Outil* : tableur, motif : « échantillon, un seul chiffre à défendre ».
Rendu attendu : sur l'extrait, Bationo = 11 370 350 FCFA (31,5 % du total), devant Sankara 9 423 281, Ouédraogo 8 483 019, Ilboudo 6 796 535 FCFA — et la phrase qui dit que ce n'est **pas** une preuve de performance sans le fichier complet ni la marge.

**3. « En janvier, on ne vend rien / ça bosse. »**
*Décision* : caler les congés et les tournées du premier mois. *Question analytique* : « Sur l'année 2025, le CA de janvier (2 051 424 FCFA sur l'extrait) est-il dans le bas de la distribution des douze mois, et l'écart s'explique-t-il par le nombre de jours ouverts ou par le CA par jour ? » *Tables* : `ventes`, `dim_date.csv` (1 339 lignes, 12 colonnes, drapeaux dimanche/férié). *Manquant* : les jours d'ouverture réels ne sont pas dans le jeu (`dim_date` donne les dimanches et les fêtes, pas les fermetures exceptionnelles) ; et l'extrait ne contient que 40 lignes par mois. *Outil* : tableur, motif : « 12 lignes, un graphique suffit ».
Le point de méthode attendu : distinguer « peu de lignes » de « peu de ventes » — sur un extrait mensuel fixe, la question devient un ratio, plus un total.

**4. « Fermer le dépôt le dimanche ? »**
*Décision* : horaires d'exploitation, direction + exploitation, effet au 1ᵉʳ janvier. *Question analytique* : « Un dimanche sur deux dans l'extrait des ventes : combien de tickets et quel CA sont réalisés un dimanche par le dépôt (`id_magasin = 6`) et par les magasins qu'il approvisionne ? » *Tables* : `ventes`, `dim_date` (colonne `est_dimanche`), `magasins` (6 lignes). *Manquant* : le jeu ne contient **pas** de flux physique dépôt → magasins (les transferts ne sont pas saisis), donc l'impact sur les ruptures est inconnu ; et `stocks_quotidiens.csv` couvre 60 000 lignes d'extrait, pas le champ complet. *Outil* : SQL, motif : « compte sur un gros fichier + jointure calendrier ».
Rendu attendu : poser la question du **coût évité** (indisponible dans le jeu) autant que du chiffre d'affaires perdu — un cadrage qui ne voit que le CA est incomplet.

**5. « Le magasin 5, combien il rapporte ? »**
*Décision* : arbitrer un investissement dans ce point de vente. *Question analytique* : « Que vaut le CA TTC 2025 du magasin 5 sur le fichier complet (à distinguer des 36 073 185 FCFA de l'extrait), et quelle **marge brute** — somme de (prix de vente − coût d'achat) par ligne — en FCFA et en pourcentage ? » *Tables* : `ventes_propres.csv` (240 000 lignes), `couts_achat.csv`, `magasins.csv`. *Manquant* : marge **nette** impossible (loyer, salaires, transport absents) ; `objectifs_de_ca.csv` compte 218 lignes, donc des mois sans cible. *Outil* : SQL ou Python, motif : « jointure sur 240 000 lignes et contrôle de totaux ».
Le point le plus noté : le candidat qui **refuse** le mot « rapporte » sans le définir (CA ? marge brute ? marge nette ?) et demande la décision cachée derrière.

### Total et décision d'orientation

**Trois seuils, trois décisions.**
- **Quiz : 14/20 minimum.** En dessous, ne passez pas en M02 : les statistiques appliquées (M02) reposent mot pour mot sur la distinction type/format et sur le vocabulaire donnée-information. Reprenez C02 (frontières du vocabulaire) et C04 (types, formats), puis re-passez le quiz en entier — pas seulement les items ratés, parce que la mémoire des réponses fausses fausse la seconde tentative.
- **Étude de cas : 12/20 minimum.** En dessous, le savoir est là mais le réflexe professionnel non : refaites les cinq demandes du projet M01.P qui portent sur le cadrage, et l'exercice guidé de C07, puis re-passez cette seule partie.
- **Projet : 13/20 minimum** (barème dans `03_exercices/M01_projet.md`). Un projet non rendu ne se compense par aucune note.

Entre 14 et 16 au quiz avec l'étude de cas réussie, passez en M02 en reprenant C04 avant son deuxième chapitre : les statistiques vous sembleraient obscures pour de mauvaises raisons. Cette règle de remédiation est la même pour les 21 modules suivants ; c'est l'une des rares choses du parcours qui ne se négocie pas.
