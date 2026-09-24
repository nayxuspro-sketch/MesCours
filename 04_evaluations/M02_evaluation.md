# Évaluation M02 — « Statistiques descriptives et inférence »

**Module M02 · durée totale 2 h 45 · quatre épreuves · seuils : quiz 14/20, étude de cas 12/20, projet 13/20**

| Épreuve | Durée | Barème | Noté | Ce qui est attendu |
|---|---|---|---|---|
| A · Questions de récupération | 15 min | non noté | non | remettre à plat ce qui a été compris en cours de module |
| B · Quiz | 35 min | /20 | oui | vingt questions à réponse courte, une seule bonne réponse |
| C · Exercices pratiques | 55 min | /20 (auto-corrigé) | oui | deux séries menées jusqu'au chiffre, tableur ou Python |
| D · Étude de cas | 60 min | /20, seuil 12 | oui | un dossier de quatre pages, chiffré et prudent |

> Le score du module se lit ainsi : **B ≥ 14** et **D ≥ 12** ouvrent le module 3 ; le projet M02.P doit atteindre 13.
> Un candidat qui réussit B et échoue à D repasse uniquement D — l'écrit de connaissances ne remplace pas le travail
> sur les données.

---

## A · Questions de récupération (non notées)

À traiter à l'oral ou par écrit, sans document. Elles ne sont pas comptées ; elles servent à repérer ce qui n'est pas
assimilé avant de se tromper dans les épreuves notées.

1. Pourquoi la moyenne d'une distribution de paniers peut-elle être juste et inutilisable ?
2. Quelle différence de sens y a-t-il entre 150 000 FCFA « au 70ᵉ percentile » et « le 70ᵉ plus gros ticket » ?
3. Que devient un histogramme si la dernière classe est fermée à 150 000 alors que le maximum vaut 1 343 666 ?
4. Pourquoi dit-on d'un intervalle de confiance qu'il porte sur le paramètre et non sur les observations ?
5. Un p-valeur de 0,13 permet-il d'affirmer que deux vendeurs font le même chiffre ? Répondez en une phrase.
6. Pourquoi compare-t-on des moyennes de prix **par ligne** et non des chiffres d'affaires par vendeur ?
7. Qu'ajoute un test des rangs quand le test de Welch conclut déjà ?
8. Un échantillon de 385 personnes suffit pour une marge de 5 points. Un échantillon de 480 lignes donne-t-il une
   marge de 5 points sur un montant ? Expliquez.

---

## B · Quiz (20 questions · 20 points)

**Barème : 1 point par question, aucune soustraction de point pour une erreur de signe ou d'unité.** Les réponses
justifiées en une ligne peuvent rapporter un demi-point de bonus, plafonné à 20.

### Bloc 1 — Population, échantillon, biais (Q1 à Q5)

**Q1.** Un fichier contient 480 lignes issues des 40 premières lignes de chaque mois. On veut estimer le panier moyen
annuel. Ce que mesure avant tout le taux de 6,3 % :
a) la variance · b) la représentativité · c) le taux de remplissage · d) la précision

**Q2.** Le même échantillon ne contient que les jours 1 à 4 de chaque mois. On peut dire sans mesurer que la
moyenne :
a) est biaisée de 2 % · b) est biaisée vers le bas · c) est non représentative · d) est biaisée de 14 %

**Q3.** Trois modalités possibles pour le champ `magasin` alors qu'il y a cinq magasins. Le risque principal :
a) une clé orpheline · b) une valeur manquante · c) un type de donnée · d) une normalisation

**Q4.** Un champ de montants est vide sur 18 lignes, absent sur 103. La première décision statistique :
a) compléter par zéro · b) compléter par la moyenne · c) dire sur quelle population porte chaque chiffre · d) supprimer les 103 lignes

**Q5.** L'unité d'échantillonnage d'une étude de clientèle doit être :
a) la ligne de vente · b) le ticket · c) le jour · d) le client

### Bloc 2 — Centres (Q6 à Q8)

**Q6.** Sur un échantillon de 316 paniers, le plus gros vaut 1 343 666 FCFA. Passer de 316 à 315 paniers en
retirant ce maximum déplace surtout :
a) la médiane · b) le mode · c) la moyenne · d) l'écart interquartiles

**Q7.** Deux valeurs également fréquentes, deux modes donc, séparées de 1 463 FCFA. Le mode est ici :
a) inutilisable · b) une valeur de prix unitaire, pas de panier · c) un signal de palier tarifaire · d) une erreur de saisie

**Q8.** Moyenne 114 156, médiane 58 423 FCFA. Le chiffre qui dit « un client sur deux est en dessous » :
a) la moyenne · b) la médiane · c) le mode · d) le 75ᵉ percentile

### Bloc 3 — Dispersion et positions (Q9 à Q12)

**Q9.** Écart type 182 095 pour une moyenne de 114 156 FCFA. Le coefficient de variation vaut environ 159,5 % et
signale :
a) des données fausses · b) une dispersion supérieure à la moyenne, moyenne peu représentative · c) une erreur d'unité · d) une distribution normale

**Q10.** Premier quartile 20 635 FCFA, troisième 130 559 FCFA. La borne supérieure de Tukey vaut :
a) 130 559 + 1,5 × 109 924 · b) 1,5 × 130 559 · c) Q3 + 1,5 × Q1 · d) Q3 + 3 × IQR

**Q11.** Sur 316 tickets, 158 sont entre les quartiles — et non 158 comme l'annoncent 50 % des observations. L'écart
de 2 s'explique par :
a) une erreur de calcul · b) la convention de quantile, qui peut placer une valeur exactement sur un quartile · c) 2 aberrants · d) un arrondi de l'écart type

**Q12.** Le 90ᵉ percentile du montant par ligne vaut 234 518, 235 318, 236 118 ou 243 010 FCFA selon la méthode.
La bonne conduite :
a) publier la plus grande · b) publier celle du tableur · c) publier l'une et nommer la méthode · d) publier la moyenne des quatre

### Bloc 4 — Formes et liaisons (Q13 à Q16)

**Q13.** Asymétrie 3,84, excès de kurtosis 18,25. Le couple de qualificatifs exact :
a) symétrique pointue · b) à droite et pointue · c) à gauche et plate · d) normale et étroite

**Q14.** Le chiffre d'affaires est concentré : le dernier décile porte 47,5 % du total, et 1,6 % seulement est sous
le premier quartile. La première page du rapport devrait montrer :
a) un camembert par catégorie · b) une courbe cumulative · c) un nuage de points · d) un effectif par vendeur

**Q15.** La covariance entre `quantite` et `montant_ttc` vaut 857 634, en unités « pièces × FCFA ». Comment passe-t-on
de là au coefficient de Pearson ?
a) on divise la covariance par le produit des deux écarts types · b) on multiplie la covariance par les deux écarts types · c) on élève 0,712 au carré · d) on divise la covariance par l'écart interquartiles

**Q16.** Pente 12 237 FCFA par pièce, ordonnée -10 402 FCFA, coefficient 0,712. L'affirmation recevable :
a) doubler la quantité double le montant · b) une pièce supplémentaire accompagne en moyenne 12 237 FCFA de plus sur la ligne · c) 50,7 % du montant vient de la quantité, le reste est faux · d) la relation est causale

### Bloc 5 — Estimation et tests (Q17 à Q20)

**Q17.** Un intervalle [94 078 ; 134 234] FCFA sur le panier moyen. Le nombre 40 156 est :
a) l'erreur type · b) la marge d'erreur · c) la largeur de l'intervalle · d) la variance

**Q18.** Test de Welch entre deux vendeurs : t = 1,52, ddl 226,1, p = 0,13, IC [-8 279 ; 65 498]. La conclusion
écrite dans le rapport :
a) les vendeurs sont équivalents · b) l'écart est de 28 609 FCFA · c) aucun écart stable n'est établi sur cet extrait · d) le vendeur le plus performant est Bationo

**Q19.** Six comparaisons de paires sont menées, la plus petite p-valeur vaut 0,13, le seuil après correction 0,0083.
On conclut :
a) une comparaison est significative · b) aucune n'est significative au seuil corrigé, et l'étude manque de puissance · c) il faut publier la plus petite p · d) il faut augmenter alpha

**Q20.** Marge de détection de 52 956 FCFA par ligne à 80 % de puissance. Le même test au niveau ticket donne une
erreur type de 33 881 contre 18 821 : la raison est :
a) une erreur de formule · b) le passage de 234 à 107 observations, et le mélange de plusieurs vendeurs sur 84 tickets · c) des queues trop lourdes · d) un seuil mal choisi

---

## C · Exercices pratiques (2 séries · 55 min · auto-correction exigée)

Règles : une feuille de calcul ou un script par série ; tous les nombres doivent être retrouvables par une formule ou
une ligne de commande ; les arrondis sont affichés en fin de chaîne. Les corrigés de la partie C sont donnés à la fin
du document — l'auto-correction fait partie de l'épreuve, un candidat qui ne se corrige pas perd le point de méthode.

**E1 · Profil du magasin (30 min)**
1. E1.1 — effectif de lignes, effectif de tickets, moyenne et médiane du montant TTC par ligne, écart type.
2. E1.2 — trois premières et trois dernières lignes triées par `montant_ttc`, par ticket : le chiffre d'affaires est-il
   porté par les gros tickets ? Donnez le pourcentage du total détenu par les 32 plus gros tickets.
3. E1.3 — Q1, Q3, IQR, borne supérieure de Tukey, nombre d'observations hors borne, et ce que devient cette borne si
   l'on exclut les retours négatifs.

**E2 · Estimer et décider (25 min)**
1. E2.1 — intervalle à 95 % de la part de lignes avec remise dans l'échantillon (173 lignes sur 480), puis
   comparaison à la part observée dans la population de référence si vous y avez accès.
2. E2.2 — comparer le montant par ligne des deux vendeurs les plus fournis, au tableur **puis** en Python : moyenne,
   écart type, effectif, t, ddl, p, intervalle à 95 % de l'écart.
3. E2.3 — même comparaison par les rangs, puis par permutation (10 000 tirages, graine annoncée). Vous rédigez les
   trois p-valeurs et une phrase de décision unique.
4. E2.4 — avec 30 % de remise sur les 316 tickets, combien de tickets faudrait-il dans chaque groupe pour mettre en
   évidence un écart de 28 609 FCFA ?

---

## D · Étude de cas (20 points · seuil 12 · 60 min)

### Le dossier

Vous recevez un courriel du directeur commercial :

> « Bationo fait des paniers plus gros qu'Ilboudo : 90 963 contre 62 354 FCFA par ligne. C'est 46 % d'écart. Je
> veux deux choses : la preuve chiffrée, et si tu ne la trouves pas, dis-moi franchement que ces chiffres ne veulent
> rien dire. Et pendant que tu y es, est-ce que le magasin 5 vend plus cher que le magasin 1 ? »

Vous disposez de : l'extrait nettoyé de 480 lignes (316 tickets), le fichier de référence de 240 000 lignes, la table
`dim_date`, un tableur, Python si vous le souhaitez, et une demi-heure de calcul.

### Les quatre livrables demandés

1. **La preuve, ou son absence, sur les vendeurs** (6 pts) — au niveau ligne et au niveau ticket, avec les deux
   échantillons, l'écart estimé, l'intervalle, le test, le seuil corrigé si vous comparez plusieurs paires, et la
   marge de détection.
2. **La réponse sur les deux magasins** (6 pts) — périmètre et grain annoncés, les deux moyennes, les deux effectifs,
   l'écart, l'intervalle, le p, la décision.
3. **Une recommandation datée** (4 pts) — trois lignes maximum, qui ne dépasse pas ce que les pages précédentes
   établissent ; par exemple un plan de mesure (recalcul sur douze mois, effet de la couverture en jours, ce qu'il
   faudrait collecter).
4. **Un encadré « ce qui aurait changé ma réponse »** (4 pts) — trois contre-vérifications que vous auriez aimées et
   qui sont impossibles avec ces données (le client, le stock, la marge nette).

### Ce que le correcteur attend, ligne à ligne

| Livrable | Attendu | Point perdu si |
|---|---|---|
| 1 | écart 28 609 FCFA, t = 1,52, p = 0,13, IC [-8 279 ; 65 498], seuil corrigé 0,0083, MDE 52 956 ; version ticket écart 16 663 FCFA, p = 0,624 | le mot « équivalents » apparaît ; le grain n'est pas annoncé |
| 2 | magasins 1 et 5 sur 2025 au grain du ticket : 107 889 (14 463) et 116 886 FCFA (4 524), écart -8 997, t = -3,37, p = 0,000751, IC [-14 226 ; -3 767] → écart établi | le candidat compare des lignes sans le dire, ou omet les effectifs |
| 3 | décision de mesurer avant de gérer : pas de mutation, pas de prime sur cette base ; recalcul sur douze mois | la recommandation dépasse les chiffres |
| 4 | trois limites nommées, avec ce qu'il faudrait comme donnée pour chacune | limites rédigées en « il faudrait plus de données » |

**Total : 20 points. Seuil de passage : 12.**

---

## Corrigé

### B · Quiz — réponses et explications

| # | Réponse | Explication en une ligne |
|---|---|---|
| Q1 | b | le taux de 6,3 % est un taux de couverture : il mesure l'exposition à un biais, pas une variance |
| Q2 | c | le sens et l'amplitude du biais ne se devinent pas, ils se mesurent ; seul le caractère non représentatif est certain |
| Q3 | b | trois modalités sur cinq magasins : deux magasins sont absents du fichier, ce qui change le périmètre de la réponse |
| Q4 | c | avant de combler ou de supprimer, on écrit sur quoi porte chaque chiffre |
| Q5 | b | un client, un ticket : si l'unité est la ligne, les gros tickets comptent double |
| Q6 | c | la moyenne déplace tout le poids de l'observation extrême, la médiane presque rien |
| Q7 | c | deux modes serrés sur un champ de prix signalent un palier tarifaire, pas une erreur |
| Q8 | b | définition de la médiane ; 71,8 % des tickets sont sous la moyenne, ce que la moyenne ne dit pas |
| Q9 | b | un CV de 159,5 % est un signal de dispersion, pas une faute de calcul |
| Q10 | a | Q3 + 1,5 × IQR : 130 559 + 1,5 × 109 924, soit 295 445 FCFA |
| Q11 | b | 166 observations exactement à Q1, la frontière dépend de la convention retenue |
| Q12 | c | les méthodes diffèrent de 3,6 % sur cet extrait : on publie une valeur et on nomme la règle |
| Q13 | b | asymétrie positive et excursion marquée, jamais « normale » |
| Q14 | b | la concentration est une affaire de cumul ; le camembert ne la montre pas |
| Q15 | a | covariance sur produit des deux écarts types — c'est ce qui rend le nombre comparable d'un fichier à l'autre ; le carré du coefficient, 0,712², est le R² |
| Q16 | b | lecture de la pente, dans le domaine observé, sans causalité |
| Q17 | c | 40 156 est la largeur ; la marge est la moitié, 20 078 FCFA |
| Q18 | c | un intervalle qui contient zéro n'établit rien ; il n'innocente pas non plus |
| Q19 | b | 0,13 > 0,0083 : aucune comparaison ne passe, et la puissance était faible avant même de commencer |
| Q20 | b | moins d'observations et un effet partagé : deux raisons qui se cumulent |

Grille de conversion : 20/20 à 14/20 validé · 13/20 à 11/20 révisions ciblées sur les deux blocs manquants · 10/20
et moins reprendre le module.

### C · Exercices pratiques — corrigés

**E1.1** — 480 lignes, 316 tickets. Montant TTC par ligne : moyenne 75 152, médiane 37 966, écart type 143 915
FCFA. `=ECARTYPE.STANDARD(plage)` ou `df.montant_ttc.std()`.

**E1.2** — le total de l'extrait au grain du ticket vaut 36 073 185 FCFA. Les 32 plus gros tickets, soit 10,1 % des
316, en portent 17 139 852 FCFA : **47,5 %** du chiffre d'affaires pour un ticket sur dix. Les 31 tickets au-dessus
de 250 000 FCFA valent 16 903 734 FCFA, soit 46,9 %. Les neuf plus gros seulement suffisent à faire 24,0 % du
total (8 642 533 FCFA). Le chiffre d'affaires est donc bien porté par les gros tickets, et la moyenne du magasin
parle surtout d'eux.

**E1.3** — premier quartile 20 635, troisième 130 559, IQR 109 924, borne 295 445 FCFA, 25 tickets hors borne.
En excluant les 3 tickets de retour (montant négatif au niveau du ticket), la borne descend de 1 271 FCFA à
294 174 FCFA et le nombre de tickets hors borne **reste 25** : le nettoyage déplace la borne, il ne change pas le
verdict. C'est la réponse attendue — et elle vaut mieux que « la borne est une ligne de conduite », parce qu'elle est
mesurée des deux côtés.

**E2.1** — 173 sur 480, soit 36,0 % ; erreur type 2,2 points, marge 4,3 points, intervalle [31,7 ; 40,3] % — le
même calcul que M02.C07, exerc. 7.3. Dans la population de référence, la part de lignes avec remise se mesure par la
même formule sur 240 000 lignes : si les deux chiffres s'écartent de plus d'une dizaine de points, l'extrait n'est
plus neutre sur cette variable et la remarque va dans le rapport.

**E2.2** — Bationo : 90 963 FCFA de moyenne par ligne, 125 lignes. Ilboudo : 62 354 FCFA, 109 lignes. Écart
28 609 FCFA, erreur type 18 821, marge ±36 888, t = 1,52, ddl 226,1, p = 0,13, IC [-8 279 ; 65 498]. Au tableur
`=T.TEST(plage1;plage2;2;3)`, en Python `stats.ttest_ind(a, b, equal_var=False)` : les deux doivent rendre le même
p au millième près.

**E2.3** — permutation 10 000 tirages, graine annoncée : p = 0,1443 ; test des rangs : p = 0,0161. Phrase de décision
attendue : « avec 234 lignes, l'extrait ne permet d'établir aucun classement entre vendeurs ; le test des rangs
signale une différence de position qui résiste mal à la correction pour six comparaisons (seuil 0,0083) ».

**E2.4** — n = 412 lignes par groupe pour 80 % de puissance sur un écart de 28 609 FCFA avec 30 % de remise.
L'extrait en compte 125 et 109 : l'étude est en dessous d'un facteur quatre.

### D · Étude de cas — éléments de réponse attendus

**1.** Deux niveaux, deux chiffres, même conclusion. Niveau ligne : 234 observations, écart estimé 28 609 FCFA,
intervalle [-8 279 ; 65 498] FCFA, p = 0,13, seuil corrigé 0,0083 → non concluant. Niveau ticket : 107 observations,
écart 16 663 FCFA, erreur type 33 881, p = 0,624, intervalle [-49 743 ; 83 069] → non concluant, et il faut écrire
pourquoi l'intervalle gonfle : 30 % d'observations en moins, et 84 tickets sur 316 portent plusieurs vendeurs, donc
l'effet cherché est partagé. Marge de détection 52 956 FCFA : même une vraie différence de 20 000 FCFA n'aurait que
18,5 % de chances d'être détectée. Verdict à rendre : **classement non établi**, les 46 % du courriel sont un rapport
de moyennes, pas un effet démontré.

**2.** Périmètre : année 2025, magasin 1 contre magasin 5, grain du ticket, total des montants TTC par ticket dans
`ventes_propres`. Moyennes 107 889 FCFA (14 463 tickets) et 116 886 FCFA (4 524 tickets) ; médianes 65 313 et
68 160 FCFA. Écart -8 997 FCFA, erreur type 2 668, t = -3,37 sur 6 782,8 ddl, p = 0,000751, intervalle
[-14 226 ; -3 767] FCFA : zéro exclu, **écart établi** — le magasin 5 fait des paniers plus gros, d'environ 8 300 à
14 200 FCFA, soit 7,7 % à 13,2 % du panier moyen du magasin 1. La prudence à joindre : ce test porte sur la
population entière des deux magasins, l'extrait nettoyé n'y participe pas ; et rien ici n'explique l'écart (assortiment
ou clientèle, on ne sait pas).

**3.** Recommandation, modèle de rédaction : « aucune mesure individuelle ne se justifie sur cette base ; nous
proposons un recalcul sur douze mois complets au grain du ticket (14 463 et 4 524 tickets disponibles, seuil
d'observation 0,0083), et la collecte du rattachement client-ligne qui manque sur 21,5 % de l'effectif avant toute
comparaison de filets de clientèle ». Une ligne de date, une ligne de responsable, une ligne de revue.

**4.** Ce qui aurait changé la réponse : le panier par client et non par ticket (84 tickets multi-vendeurs, 103 lignes
sans client utile), la marge nette au lieu du chiffre d'affaires (le prix de revient est hors de ce fichier), et
l'écoulement du stock (sans lui, un gros mois peut être un transfert en magasin, pas une vente). Pour chacun : la
donnée à demander, et le test qui en découlerait.

### Total et décision d'orientation

| Composante | Score | Seuil | Statut |
|---|---|---|---|
| B · Quiz | ... /20 | 14 | bloquant |
| C · Exercices | ... /20 | indicatif (auto-correction menée = +0,5) | — |
| D · Étude de cas | ... /20 | 12 | bloquant |
| Projet M02.P | ... /20 | 13 | bloquant |

**Décision.** B et D au seuil, projet au seuil → module validé, passage en M03 (SQL : interroger la source). Quiz
seulement en dessous → trois jours pour reprendre C02 et C05, puis une nouvelle version de B. Étude de cas seulement
en dessous → nouvelle version de D sur le même dossier, avec un entretien de 15 minutes sur la lecture des
intervalles. Deux échecs → reprise du module, en commençant par les mini-projets P1 à P4.
