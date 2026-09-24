# Épreuve de validation de palier P1 — « Du fichier reçu à la conclusion tenable »

**Fin du palier P1 (dernier module : M03) · 90 min en temps limité · noté /20, seuil 14 ·
conditions d'entrée au palier P2 · épreuve mixte : lecture des données, calculs statistiques,
formules de classeur, et une question de décision.**

| Partie | Durée | Barème | Ce qui est mesuré |
|---|---|---|---|
| 1 · Lire et cadrer (M01) | 20 min | /5 | la forme du fichier, les variables avec leur unité, ce que le fichier peut répondre et ce qu'il ne peut pas |
| 2 · Statistiques descriptives (M02) | 25 min | /5 | moyenne contre médiane, dispersion, aberrant, corrélation — et l'interprétation de chaque chiffre |
| 3 · Formules et classeur (M03) | 20 min | /4 | la formule unique recopiable, la référence structurée, le total qui ne trompe pas |
| 4 · Pièges et biais (M01 + M02) | 15 min | /3 | l'échantillon, l'erreur d'échantillonnage, la taille nécessaire |
| 5 · Question de décision (M01 + M02 + M03) | 10 min | /3 | trancher, avec les chiffres qui soutiennent la décision **et** sa limite |

> **Règle de l'épreuve.** Une réponse **sans son chiffre** ne compte pas ; un chiffre **sans sa
> limite** ne compte qu'à moitié. Tous les nombres de l'énoncé et du corrigé sont mesurés sur les
> socles livrés (`data/projection/ventes_magasin5_2025.csv`, `data/reference/` et `data/projection/m03_classeur_atelier.xlsx`)
> et sourcés dans `01_socle_donnees/data/reference/chiffres_cites.json`.

> **Note de méthode, déclarée.** L'architecture décrit l'épreuve de palier comme un mélange de
> « requêtes, formules, code et une question de décision » (§B.6). Cette description vaut pour les
> paliers suivants : au **P1**, ni SQL ni Python ne sont encore enseignés (ils arrivent en M05 à M08).
> L'épreuve du P1 mesure donc le mix réellement acquis : **lecture des données (M01), calculs et
> interprétation statistique (M02), formules et classeur (M03)**, plus la question de décision. Le
> mélange complet (requêtes + code) est celui du **P2**, dont l'épreuve existe déjà
> (`04_evaluations/P2_epreuve_validation.md`).

---

## Matériel de l'épreuve

| Élément | Chemin | Ce que c'est |
|---|---|---|
| Le fichier reçu | `01_socle_donnees/data/projection/ventes_magasin5_2025.csv` | l'extrait de M01 : **489** lignes × **13** colonnes, magasin 5, année 2025 |
| Le classeur d'atelier | `01_socle_donnees/data/projection/m03_classeur_atelier.xlsx` | le classeur de M03, sur le même extrait |
| Les référentiels propres | `01_socle_donnees/data/reference/` | produits, clients, magasins, vendeurs, vérité terrain |
| Les chiffres cités | `01_socle_donnees/data/reference/chiffres_cites.json` | les valeurs de référence (sections `M01`, `M02`, `M03`) |

**Calculatrice autorisée. Tableur autorisé. Aucun accès réseau.** Les formules demandées sont
écrites **au clavier** (pas de clic), et les requêtes n'existent pas encore à ce palier : c'est une
épreuve de compréhension, pas de syntaxe.

---

## Partie 1 · Lire et cadrer (20 min · 5 points)

**Q1.1 (1,5 pt).** Donnez la **forme** du fichier reçu (lignes × colonnes) et le **grain** de la
table : une ligne représente quoi, exactement ? Combien de tickets distincts le fichier contient-il,
et quel est le **nombre maximal de lignes rattachées à un même ticket** ?

**Q1.2 (1,5 pt).** Trois colonnes arrivent en **texte** alors qu'elles devraient être numériques ou
datées. Lesquelles, et comment le savez-vous **sans ouvrir le fichier à la main** (citez le contrôle
que vous faites et ce qu'il rend) ?

**Q1.3 (1 pt).** Écrivez **trois** questions que ce fichier peut répondre, et **deux** qu'il ne peut
pas — en donnant, pour chaque question impossible, la **variable manquante** qui l'empêche.

**Q1.4 (1 pt).** Le fichier reçu contient **9** lignes en double et **18** clients sans identifiant.
Dans quel ordre traitez-vous ces deux défauts, et pourquoi cet ordre change le total ?

## Partie 2 · Statistiques descriptives (25 min · 5 points)

Sur les **316** tickets de l'extrait, le panier (montant d'un ticket) donne : moyenne **114 156**
FCFA, médiane **58 423** FCFA, écart-type **182 095** FCFA, minimum **−150 804** FCFA, maximum
**1 343 666** FCFA.

**Q2.1 (1,5 pt).** Calculez le **coefficient de variation** et expliquez ce qu'il dit de la
distribution, en une phrase. Pourquoi l'**écart-type seul** ne suffit-il pas ?

**Q2.2 (1,5 pt).** La moyenne vaut presque **le double** de la médiane. Donnez la mesure de forme
qui l'explique (nom et valeur), puis **la part** des tickets situés **sous la moyenne** — et
concluez en une phrase sur ce que « panier moyen » signifie ici.

**Q2.3 (1 pt).** Calculez la **borne haute** de la règle de l'écart interquartile (Q3 + 1,5 × IQR)
avec les valeurs du fichier, donnez le nombre de tickets au-dessus, et dites pourquoi on ne les
supprime pas.

**Q2.4 (1 pt).** La corrélation entre la quantité et le montant d'une ligne vaut **0,712**, celle de
Spearman **0,641**, et le r² **50,7 %**. Traduisez les **trois** en une phrase chacun, sans dire
« corrélation » deux fois de la même façon, et dites ce que le r² permet de prédire.

## Partie 3 · Formules et classeur (20 min · 4 points)

Le classeur `m03_classeur_atelier.xlsx` contient l'extrait nettoyé : **480** lignes de ventes
(colonne A à M), un tableau structuré nommé `TableVentes`, et la colonne `montant_ttc` en M.

**Q3.1 (1,5 pt).** Écrivez la **formule unique** qui calcule le montant TTC de la ligne 2 dans un
tableau dont les colonnes sont `quantite` (I), `prix_unitaire_ht` (J) et `remise` (K), sachant que
le taux de TVA est **19 %** et qu'il n'est pas dans le tableau. La formule doit être **recopiable**
vers le bas sans qu'on écrive une seule référence en dur.

**Q3.2 (1 pt).** Écrivez la formule qui donne le **CA total** du tableau sans passer par le pied de
tableau, et expliquez en une phrase pourquoi on ne somme **jamais** la ligne de total.

**Q3.3 (1 pt).** Le plus gros montant de ligne du fichier vaut **1 229 678** FCFA et se trouve à la
ligne **356**. Écrivez la formule (ou la démarche) qui **retrouve** automatiquement cette ligne, et
dites ce qu'on vérifie ensuite sur cette ligne avant de publier le chiffre.

**Q3.4 (0,5 pt).** Le total du classeur affiche **36 357 118** FCFA alors que le fichier brut donnait
**36 339 317** FCFA. Expliquez l'écart par la **définition** des deux périmètres (et non par une
erreur de calcul).

## Partie 4 · Pièges et biais (15 min · 3 points)

L'extrait **n'est pas** l'ensemble des ventes : il représente **6,3 %** des lignes et **7,0 %** des
tickets de la population. Sur cette population, la moyenne du panier est **116 886** FCFA et la
médiane **68 160** FCFA.

**Q4.1 (1 pt).** L'extrait donne une moyenne de **114 156** FCFA et une médiane de **58 423** FCFA.
Comparez aux valeurs de la population : de quel pourcentage la moyenne s'écarte-t-elle, et de quel
pourcentage la médiane ? Que retient-on de la comparaison des deux écarts ?

**Q4.2 (1 pt).** L'extrait ne couvre que les jours **1 à 4** de chaque mois, soit **2** à **4** jours
par mois. Nommez le **mécanisme de biais** en jeu (M02) et proposez **le** contrôle qui le détecte
avant tout calcul — celui que vous auriez dû faire en premier.

**Q4.3 (1 pt).** Pour mesurer une proportion avec une marge de **5** points, le calcul donne
**385** tickets. L'extrait en contient **316**. Écrivez ce que vous faites de ce constat : la
question est-elle de conclure « l'extrait ne suffit pas », ou de préciser **ce que** l'extrait ne
permet pas de conclure ?

## Partie 5 · Question de décision (10 min · 3 points)

Le comptable de l'enseigne affirme : « **Les remises coûtent cher : elles portent sur 173 lignes et
12 198 008 FCFA de chiffre d'affaires — il faut les supprimer.** » Vous disposez des chiffres
suivants sur l'extrait : CA des lignes positives **36 357 118** FCFA, **173** lignes avec remise,
**12 198 008** FCFA de CA sur ces lignes, modalités de remise observées : 0 %, 3 %, 4 %, 7 %, 8 %,
11 %.

**Q5.1 (2 pts).** Tranchez : la phrase du comptable est-elle soutenable en l'état ? Donnez **deux**
chiffres qui l'affaiblissent (dont un que vous calculez) et une phrase de conclusion.

**Q5.2 (1 pt).** Écrivez la **limite** de votre propre conclusion en une phrase, et **le chiffre
supplémentaire** qu'il faudrait pour aller plus loin (nommez-le : il manque une variable, pas un
calcul).

---

## Corrigé

### Partie 1

**Q1.1.** **489** lignes × **13** colonnes (`m01_petit_lignes`, `m01_petit_colonnes`) ; le grain est
**la ligne de vente** (un produit, une quantité, un prix), pas le ticket : **316** tickets distincts
(`m01_petit_valeurs_uniques["n_ticket"]`), soit **1,52** ligne par ticket en moyenne, **104** tickets
à plusieurs lignes (**32,9 %**) et jusqu'à **4** lignes pour un même ticket (`m02_c01_lignes_par_ticket`,
`m02_c01_tickets_multi_lignes`, `m02_c01_pct_tickets_multi`, `m02_c01_max_lignes_par_ticket`). La
leçon : **un fichier ne contient pas « des ventes » par défaut — il contient des lignes**, et le
compte change selon le grain qu'on choisit.

**Q1.2.** **`date`**, **`heure`** et **`montant_ttc`** arrivent en texte (`m01_petit_types_inferes_par_pandas` :
`object`). Le contrôle : l'**inférence de types** du fichier (`dtypes`) — trois colonnes sortent en
`object` au lieu de `datetime64` et `float64`. Les conséquences mesurées : **65** dates écrites de
plusieurs façons (`m01_petit_dates_mixtes`) et **486** montants en texte (`m01_petit_montants_texte`),
qui rendent tout calcul faux **silencieusement** si on somme des chaînes.

**Q1.3.** Trois questions **répondables** : (a) quelle catégorie porte le plus de lignes ?
(7 modalités, `Matériaux` **146** lignes, `m01_petit_categories`) ; (b) quel jour et à quelle heure
vend-on ? (heures de **07:01** à **18:57**, **31** jours distincts, `m01_petit_heure_min`,
`m01_petit_jours_distincts`) ; (c) quel vendeur réalise le plus gros CA ? (**4** vendeurs,
`m01_petit_vendeur_distincts`). Deux questions **impossibles** : le **taux de marge** — la variable
manquante est le **coût d'achat** ; la **comparaison entre magasins** — la variable manquante est le
**magasin** (une seule valeur : le magasin 5, `m01_petit_valeurs_uniques["magasin"] = 1`).

**Q1.4.** On traite les **doublons d'abord**, les clients manquants ensuite. Raison : **9** lignes
sont des copies exactes (`m01_petit_lignes_en_double`) ; les garder **gonfle le total** — la preuve
mesurée est que la somme des trois premiers mois double presque (**36 339 317** contre **72 678 634**,
`m01_petit_double_total_brut`). L'identifiant client manquant (**18** lignes, `m01_petit_clients_manquants`)
ne change **aucun total** : il empêche seulement une analyse par client. L'ordre des deux gestes n'est
donc pas indifférent : on retire ce qui fausse les montants avant de qualifier ce qui gêne l'analyse.

### Partie 2

**Q2.1.** Le coefficient de variation vaut **159,5 %** (`m02_panier_cv_pct`) : l'écart-type représente
une fois et demie la moyenne. L'écart-type seul (**182 095** FCFA, `m02_panier_ecart_type`) ne dit rien
parce qu'il n'a pas d'échelle de comparaison : c'est le **rapport** à la moyenne qui permet de dire
« cette distribution est très dispersée » — au-delà de 30 à 40 %, on n'a plus affaire à une population
homogène, mais à un mélange de populations.

**Q2.2.** La mesure de forme est l'**asymétrie**, qui vaut **3,84** (`m02_panier_asymetrie`) : une
distribution fortement étalée vers la droite. La part des tickets **sous la moyenne** est de **71,8 %**
(**227** tickets sur 316, `m02_c02_pct_tickets_sous_la_moyenne`, `m02_c02_tickets_sous_la_moyenne`).
Conclusion : « panier moyen » désigne ici un **montant qu'aucun client ne paie** — la majorité des
tickets est **sous** lui, et il est tiré par quelques très gros paniers (maximum **1 343 666** FCFA,
`m02_panier_max`). Le chiffre à publier pour décrire le client typique est la **médiane**, **58 423**
FCFA (`m02_panier_mediane`).

**Q2.3.** Borne haute : Q3 **130 559** + 1,5 × écart interquartile **109 924** = **295 445** FCFA
(`m02_panier_seuil_iqr`), au-dessus de laquelle on compte **25** tickets (`m02_panier_nb_aberrants_iqr`).
On ne les supprime pas : leur montant est **légal, daté et rattaché à un client** — et, comme ils
portent une part importante du CA, les retirer ferait baisser le total du fichier d'un montant réel.
Un point aberrant se **signale** (et se vérifie), il ne se supprime que s'il est **impossible**
(quantité négative, montant hors borne métier).

**Q2.4.** **Pearson = 0,712** (`m02_panier_corr_quantite_montant`) : la relation est **linéaire et
forte** — plus on vend d'unités, plus le montant de la ligne monte. **Spearman = 0,641**
(`m02_c06_corr_spearman`) : le **rang** est conservé — les grosses quantités sont presque toujours
dans les lignes les plus élevées, même quand la relation n'est pas parfaitement proportionnelle.
**r² = 50,7 %** (`m02_c06_r2_pct`) : **la moitié** de la variation du montant s'explique par la
quantité ; l'autre moitié vient d'ailleurs (le prix unitaire, la catégorie, la remise). C'est le r²
qui autorise une prédiction — et qui limite sa précision.

### Partie 3

**Q3.1.** `=[@quantite]*[@prix_unitaire_ht]*(1-0,19)…` **non** : la remise **ne se retire pas de la
TVA**, elle se retire du HT. La formule juste est
`=[@quantite]*[@prix_unitaire_ht]*(1-[@remise])*(1+0,19)`. Les **références structurées**
(`[@colonne]`) remplacent l'adresse de cellule : la formule se recopie **toute seule** sur les
**480** lignes, et reste juste si on insère une colonne. Le taux **19 %** est la seule constante
écrite en dur — c'est accepté ici parce qu'il est dans la consigne ; en production, il vit dans une
cellule nommée.

**Q3.2.** `=SOMME(TableVentes[montant_ttc])` — ou, si le total est hors du tableau,
`=SOMME(M2:M481)`. On ne somme **jamais** la ligne de total parce qu'elle est **dans** la plage :
la somme se compterait elle-même, et le total doublerait — l'erreur classique qui produit un CA de
**72 678 634** FCFA au lieu de **36 339 317** (`m01_petit_double_total_brut`).

**Q3.3.** `=INDEX(TableVentes[montant_ttc];EQUIV(MAX(TableVentes[montant_ttc]);TableVentes[montant_ttc];0))`
— ou, plus simple, un tri décroissant suivi de la première ligne, ou un filtre automatique.
Le plus gros montant de ligne vaut **1 229 678** FCFA (`m03_plus_gros_montant_ligne`) et se trouve en
**M356** (**Lame de lambris 4 m — réf 2**, `m03_produit_du_plus_gros_montant`). Avant de publier, on
vérifie sur cette ligne : la **quantité** (une quantité géante signale une saisie en unités au lieu de
paquets), le **prix unitaire** (comparé au référentiel, dont **120** produits ont plusieurs prix dans
l'extrait, `m03_produits_plusieurs_prix_dans_extrait`), et la **remise**.

**Q3.4.** Les deux totaux ne mesurent pas la même chose : **36 357 118** FCFA est le CA des **lignes
positives** (`m03_ca_lignes_positives`), quand **36 339 317** FCFA est le total **brut** du fichier de
M01 (`m01_petit_total_ttc_brut_valeur`). L'écart — **266 132** FCFA (`m01_petit_ecart_nettoyage_valeur`)
— n'est pas une erreur : il contient les **8** lignes de retour (montants négatifs, minimum
**−150 804** FCFA, `m03_min_ligne`) et les corrections de type. Règle du palier : **un écart entre
deux totaux s'explique par la définition des périmètres**, jamais par « le tableur se trompe ».

### Partie 4

**Q4.1.** Moyenne de l'extrait **114 156** contre **116 886** dans la population : **−2,3 %**
(`m02_c07_ecart_moyenne_pop_pct`). Médiane **58 423** contre **68 160** : **−14,3 %**
(`m02_c07_ecart_mediane_pop_pct`). Ce que la comparaison apprend : **l'erreur n'est pas la même selon
le paramètre** — la moyenne est robuste au plan de sondage, la **médiane** ne l'est pas. Un extrait
qui « tombe bien » sur la moyenne peut se tromper de **14 %** sur la valeur qui décrit le client
typique. Conclusion : on ne contrôle pas un échantillon sur **un** chiffre, mais sur **tous** ceux
qu'on publiera.

**Q4.2.** Le mécanisme est un **biais de sélection de période** : l'extrait ne contient que les jours
**1 à 4** de chaque mois (`m02_c07_jours_du_mois`), soit **2** à **4** jours par mois
(`m02_c07_jours_par_mois_min`, `m02_c07_jours_par_mois_max`) sur **12** mois
(`m02_c07_mois_couverts` = couverture annuelle, mais partielle en jours). Le contrôle à faire **avant
tout calcul** : compter les **jours distincts par mois** et les comparer aux jours ouvrés du mois ;
c'est-à-dire vérifier la **couverture temporelle**, pas le volume. Le biais est mesurable : les jours
de début de mois ne portent pas le même panier que les autres (**109 109** contre **118 243** FCFA
de moyenne, `m02_c07_pop_moy_jours_debut`, `m02_c07_pop_moy_autres_jours`).

**Q4.3.** Le constat n'est ni « l'extrait ne suffit pas » ni « il faut 385 tickets » : c'est une
**précision** énoncée. Avec **316** tickets, la marge est plus large que **5** points : un intervalle
de confiance à 95 % sur la proportion de tickets à plusieurs lignes donne **[27,7 ; 38,1]** points
(`m02_c07_ic95_prop_multi`), soit une largeur de **10,4** points environ — trop large pour trancher un
écart de **5** points. Ce que l'extrait ne permet **pas** de conclure : « la proportion a changé de
plus de 5 points ». Ce qu'il permet : situer cette proportion **entre un quart et deux cinquièmes**
des tickets. C'est le passage du chiffre à l'**affirmation tenable**.

### Partie 5

**Q5.1.** La phrase du comptable n'est **pas soutenable** en l'état, pour deux raisons mesurables.
(a) Les **173** lignes avec remise (`m03_lignes_avec_remise`) portent **12 198 008** FCFA de CA
(`m03_ca_lignes_avec_remise`), soit **33,6 %** du CA des lignes positives : supprimer la remise
n'est pas « économiser 12,2 M FCFA », c'est **retirer un tiers du chiffre d'affaires** — et la remise
n'est que la partie visible de ce CA. (b) La remise observée est **modeste** : **6** modalités, de
**0 %** à **11 %** (`m01_petit_remise_modalites`), et la corrélation entre remise et montant est
quasi **nulle** : **−0,031** (`m02_c06_corr_remise_montant`). Autrement dit : **on ne démontre pas
que la remise fait vendre plus**, mais on ne démontre pas non plus qu'elle coûte : le fichier ne
contient **pas** le coût d'achat. Conclusion tenable : « la remise représente un tiers du CA observé
et jusqu'à 11 % du montant ; son effet sur le volume **ne se mesure pas** avec ce fichier ».

**Q5.2.** La limite : l'extrait ne couvre que **6,3 %** des lignes et les **4** premiers jours de
chaque mois (`m02_c07_part_extrait_lignes_pct`, `m02_c07_jours_du_mois`) — aucune conclusion sur
l'année entière n'est donc tenable. Le chiffre qui manque n'est pas un calcul : c'est une
**variable**, le **coût d'achat** (ou la marge unitaire), qui seule permettrait de trancher entre
« remise consentie » et « marge abandonnée ». *(Variante acceptée : la **remise accordée** par
produit, pour distinguer remise tarifaire et remise commerciale.)*

---

## Barème détaillé, et ce qui fait la différence

| Partie | Détail | Points |
|---|---|---|
| 1 · Lire et cadrer | forme **et** grain (**489** × **13**, **316** tickets, jusqu'à **4** lignes) · les 3 colonnes en texte avec le contrôle qui le montre · 3 questions possibles + 2 impossibles **avec la variable manquante** · l'ordre doublons → manquants justifié | /5 |
| 2 · Statistiques | CV **159,5 %** et sa lecture · asymétrie **3,84** + **71,8 %** sous la moyenne · borne **295 445** FCFA et **25** tickets non supprimés · les trois lectures (Pearson, Spearman, r²) | /5 |
| 3 · Formules | formule unique **références structurées** (remise correctement placée) · total sans le pied · formule de recherche du max en **M356** + les contrôles avant publication · écart **266 132** FCFA expliqué par les périmètres | /4 |
| 4 · Pièges | **−2,3 %** contre **−14,3 %** et ce qu'on en retient · biais de sélection de période + contrôle de couverture · **316** contre **385** : énoncer une **précision**, pas un refus | /3 |
| 5 · Décision | deux chiffres qui affaiblissent la phrase (dont un calculé : **33,6 %**), conclusion **tenable** · limite écrite + la **variable** manquante nommée | /3 |
| **Total** | | **/20** |
| **Seuil** | conditions d'entrée au palier P2 | **14/20** |

**Les quatre erreurs qui coûtent le plus de points** (et le chiffre qui les contrôle) :

1. **Confondre la ligne et le ticket** : publier « le panier moyen est de **75 152** FCFA par ligne »
   comme s'il s'agissait d'un ticket, alors que le ticket se compte en **316** unités et non en **480**
   lignes (`m03_moyenne_ligne` contre `m02_panier_moyenne`).
2. **Publier la moyenne seule** : **71,8 %** des tickets sont **sous** la moyenne — un chiffre qui
   n'est pas faux mais qui décrit un client qui n'existe pas.
3. **Confondre écart et erreur** : **266 132** FCFA d'écart entre deux totaux s'expliquent par les
   périmètres (retours et corrections), pas par un tableur fautif.
4. **Répondre par un refus** à la question « l'échantillon suffit-il ? » : la bonne réponse est une
   **précision** (intervalle **[27,7 ; 38,1]** sur la proportion), pas un abandon.

> **Ce que cette épreuve valide, en une phrase.** Que vous savez passer d'un fichier reçu à une
> **affirmation tenable** : un chiffre **mesuré**, une **interprétation** juste du chiffre, et une
> **limite** écrite. C'est exactement ce que le palier P2 exigera ensuite avec SQL et Python — la
> syntaxe change, la discipline ne change pas.
