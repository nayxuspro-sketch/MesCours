# Évaluation M13 — « Modélisation des données »

**7 chapitres · 30 h · niveau 3 vers niveau 4 · 75 points au total · durée conseillée : 3 h.**
**Barème d'ensemble : quiz **15** questions (**20** points, seuil **11** sur **20**) ; deux exercices de
normalisation (**20** points) ; étude de cas (**30** points, seuil **18**) ; auto-test de contrôle du
modèle (**5** points) — soit **75** points, seuil de réussite **48**.**

**Ce que l'évaluation vérifie.** Que vous savez **relier** des entités, **normaliser** un tableau sans
le mutiler, **choisir** un grain, **dater** ce qu'un modèle doit conserver, et **prouver** qu'un modèle
est juste. Les requêtes sont courtes ; les décisions et les preuves sont l'essentiel.

---

## A · Questions de récupération (non notées)

1. Quelles sont les **4** anomalies que la normalisation évite ?
2. Qu'est-ce que le **grain** d'une table, et quelle requête le prouve ?
3. Quelles mesures sont additives, semi-additives, non additives ? Donnez un exemple du socle pour
   chacune.
4. Qu'est-ce qu'un changement lent de type 2, et que faut-il ajouter à **chaque** jointure ?
5. Pourquoi un modèle porte-t-il **une seule** table de dates ?

---

## B · Quiz (15 questions · 20 points)

*Les questions 1 à 10 valent 1 point ; les questions 11 à 15 valent 2 points. Seuil : **11** points sur
**20**.*

### Bloc 1 — Définir (Q1 à Q5)

**Q1.** Une relation plusieurs à plusieurs entre deux entités se résout par :
a) une colonne supplémentaire dans l'une des deux tables ;
b) une troisième table qui porte les deux clés ;
c) la suppression de l'une des deux tables.

**Q2.** La troisième forme normale interdit :
a) les colonnes calculées ;
b) les attributs qui ne dépendent pas de la clé ;
c) les tables de plus de dix colonnes.

**Q3.** Le grain d'une table de faits est :
a) le nombre de lignes qu'elle contient ;
b) ce que représente **une** ligne, écrit en une phrase ;
c) la liste de ses clés étrangères.

**Q4.** Une mesure semi-additive est additive :
a) dans le temps mais pas dans l'espace ;
b) dans l'espace mais pas dans le temps ;
c) ni dans l'espace ni dans le temps.

**Q5.** Le type 3 d'un changement lent garde :
a) toutes les versions horodatées ;
b) une colonne qui porte la valeur précédente ;
c) aucune trace, la valeur est écrasée.

### Bloc 2 — Mesurer (Q6 à Q10)

**Q6.** Le socle compte **240 000** lignes de vente pour **146 161** tickets. La moyenne de lignes par
ticket vaut environ :
a) 0,61 ;
b) 1,64 ;
c) 2,40.

**Q7.** Un modèle affiche **31 298 080 184** FCFA là où la recette vaut **15 595 154 955** FCFA. Le
facteur vaut :
a) 2,01 ;
b) 1,43 ;
c) 0,50.

**Q8.** Le chiffre d'affaires du premier trimestre, lu sur un fait de ventes, est une mesure :
a) non additive ;
b) semi-additive ;
c) additive.

**Q9.** Le socle compte **18** jours fériés travaillés. Où cette information se lit-elle ?
a) dans le fait de ventes ;
b) dans la dimension de temps ;
c) dans la dimension des magasins.

**Q10.** Un rapport par catégorie affiche **16** lignes là où le référentiel compte **7** familles. La
cause la plus probable est :
a) une jointure manquante dans la requête ;
b) des libellés repris tels quels du fichier source ;
c) un filtre de période mal borné.

### Bloc 3 — Modéliser (Q11 à Q15, 2 points chacune)

**Q11.** Un rapport par segment donne **15 595 154 955** FCFA au total, mais deux segments sont faux de
**102 917 580** FCFA. Quelle conclusion ?
a) le rapport est globalement bon ;
b) un contrôle de total ne valide pas la répartition ;
c) la clé de segment est dupliquée.

**Q12.** Pourquoi une table de pont ne doit-elle porter **aucun** montant ?
a) parce qu'elle n'a pas de clé ;
b) parce que son montant serait répété autant de fois que l'objet a de liens ;
c) parce que le moteur refuse les sommes sur une table de pont.

**Q13.** Le calendrier du socle s'arrête au 2026-08-31 et **46** commandes sont livrées en
septembre. La correction juste est :
a) filtrer la période du rapport ;
b) prolonger le calendrier ;
c) joindre en interne sur la date de livraison.

**Q14.** Le chiffre d'affaires 2026 est comparé à celui de 2025 : **− 28,9 %**. Que faut-il faire ?
a) publier le chiffre tel quel, il est mesuré ;
b) borner les deux années au même mois de fin ;
c) remplacer la comparaison par un cumul depuis janvier.

**Q15.** Un modèle déclare **0** clé primaire et **0** clé étrangère. Que peut-on en conclure ?
a) le modèle est faux ;
b) l'unicité et les liens ne sont pas garantis par la base, donc ils doivent être contrôlés à
   l'exécution ;
c) le modèle ne peut pas être chargé.

---

## C · Deux exercices de normalisation (20 points)

### N1 — Normaliser une table plate en 3FN (10 points)

Voici un extrait de commandes tel qu'il arrive d'un fichier bureautique.

| id_commande | date_commande | id_client | nom_client | ville_client | id_produit | designation | categorie | quantite | prix_unitaire |
|---|---|---|---|---|---|---|---|---|---|
| 1041 | 2026-03-02 | 208 | Diallo | Kaya | 12 | Panneau bois | Panels | 4 | 5 415 |
| 1041 | 2026-03-02 | 208 | Diallo | Kaya | 31 | Colle forte | Quincaillerie | 2 | 2 300 |
| 1042 | 2026-03-05 | 208 | Diallo | Kaya | 12 | Panneau bois | Panels | 6 | 5 415 |
| 1043 | 2026-03-05 | 415 | Sawadogo | Koudougou | 7 | Tuyau PVC | Plomberie | 12 | 1 850 |
| 1044 | 2026-03-09 | 415 | Sawadogo | Koudougou | 12 | Panneau bois | Panels | 3 | 5 415 |
| 1045 | 2026-03-09 | 901 | Nikiema | Ouagadougou | 31 | Colle forte | Quincaillerie | 5 | 2 300 |
| 1046 | 2026-03-12 | 901 | Nikiema | Ouagadougou | 7 | Tuyau PVC | Plomberie | 8 | 1 850 |
| 1047 | 2026-03-12 | 901 | Nikiema | Ouagadougou | 12 | Panneau bois | Panels | 1 | 5 415 |
| 1048 | 2026-03-15 | 208 | Diallo | Kaya | 7 | Tuyau PVC | Plomberie | 20 | 1 850 |
| 1049 | 2026-03-15 | 415 | Sawadogo | Koudougou | 31 | Colle forte | Quincaillerie | 4 | 2 300 |
| 1050 | 2026-03-18 | 901 | Nikiema | Ouagadougou | 7 | Tuyau PVC | Plomberie | 15 | 1 850 |
| 1051 | 2026-03-18 | 208 | Diallo | Kaya | 12 | Panneau bois | Panels | 9 | 5 415 |

**Travail demandé.**

1. Écrivez le ou les défauts de cette table, dans l'ordre des formes normales : ce qui viole la
   première, la deuxième, la troisième.
2. Proposez le modèle normalisé : nommez chaque table, écrivez sa clé et son grain.
3. Nommez les **4** anomalies que cette organisation évite, et donnez pour chacune un exemple
   **pris dans ce tableau**.
4. Le prix unitaire du produit 12 est le même sur les cinq lignes : dites où il doit vivre, et ce
   qu'un changement de tarif implique dans les deux organisations.

**Barème.** Défauts identifiés : **3** points. Modèle proposé, clés et grains : **4** points.
Quatre anomalies nommées et illustrées : **2** points. Emplacement du tarif et conséquence : **1**
point.

### N2 — Dénormaliser volontairement, et le chiffrer (10 points)

Un rapport doit afficher le chiffre d'affaires par famille de produits. Dans le modèle en étoile du
socle, la famille vit dans une table de famille séparée : la requête coûte **2** jointures de plus
qu'une lecture directe.

**Travail demandé.**

1. Écrivez les deux variantes : celle qui garde la table de familles séparée, et celle qui recopie la
   famille dans la dimension produit.
2. Chiffrez le coût de la dénormalisation : combien de fois la famille est-elle écrite dans chaque
   variante, sur les **154** produits et les **7** familles ?
3. Vérifiez que les deux variantes rendent le **même** résultat, et donnez la valeur de la famille
   Matériaux lue dans le modèle du socle.
4. Rédigez en cinq lignes la justification que vous donneriez à un responsable : ce que la
   dénormalisation fait gagner, ce qu'elle fait perdre, et ce qu'elle **ne change pas**.

**Barème.** Deux variantes écrites : **3** points. Chiffrage des occurrences : **3** points.
Égalité des résultats vérifiée et valeur donnée : **2** points. Justification écrite : **2** points.

---

## D · Étude de cas — « trois tableaux reliés donnent un chiffre d'affaires faux de 40 % » (30 points · seuil 18)

### La commande

Un distributeur de matériaux vous appelle. Son contrôle de gestion a additionné trois extraits — les
ventes, les commandes fournisseurs et les encaissements — dans un même rapport, en les reliant par le
magasin. Le rapport annonce **22 305 610 960** FCFA de chiffre d'affaires, là où la comptabilité en
attend **15 595 154 955** FCFA. Le directeur financier a arrêté de publier le rapport, et
votre commande tient en trois phrases : « dites-nous ce qui s'est passé, corrigez-le, et prouvez-moi
que le nouveau chiffre est le bon ».

Vous disposez du socle de Sahel Distribution, qui reproduit exactement ce cas : un fait de ventes, un
fait de commandes, un fait d'encaissements, et des rapports fautifs qui s'exécutent sans erreur.

### Le résultat attendu (à retrouver, pas à recopier)

| Étape | Ce que vous devez produire |
|---|---|
| Diagnostic | ce que fait chaque modèle fautif, et pourquoi il s'exécute sans erreur |
| Mesure | le chiffre annoncé par chacun, l'écart en pourcentage, et le facteur de la jointure la plus violente |
| Correction | la requête juste, et le chiffre de référence du socle |
| Preuve | les **4** contrôles de recette exécutés, dont le total |
| Rédaction | une note de **10** lignes pour le directeur financier, sans jargon, avec le chiffre juste |

### Barème de l'étude de cas

| Élément | Points |
|---|---|
| Diagnostic des trois modèles fautifs, dont la cause de chacun | **10** |
| Mesure : trois chiffres, trois écarts, le facteur de la jointure | **8** |
| Correction : la requête juste et le chiffre de référence | **6** |
| Preuve : les **4** contrôles exécutés et leur sortie | **4** |
| Note au directeur financier | **2** |
| **Total** | **30** |

---

## E · Auto-test de contrôle du modèle (5 points)

Écrivez les **12** requêtes suivantes, exécutez-les sur le socle, et rendez leur sortie. Chaque
requête juste vaut **0,4** point, l'ensemble étant arrondi à **5** points sur **12**.

| N° | Contrôle demandé |
|---|---|
| 1 | le nombre de lignes et le nombre de valeurs distinctes de la clé des clients |
| 2 | la même paire de comptages sur la clé des ventes |
| 3 | le nombre de lignes du fait de ventes, comparé à sa source |
| 4 | le nombre d'orphelins de la clé produit, par jointure externe |
| 5 | le nombre d'orphelins de la clé client, la ligne inconnue mise à part |
| 6 | le chiffre d'affaires net, et le chiffre d'affaires toutes lignes |
| 7 | le total des objectifs, et sa part dans le chiffre d'affaires net |
| 8 | le nombre de jours du calendrier sans aucune vente |
| 9 | le nombre de dates de livraison absentes du calendrier |
| 10 | le nombre de versions de la dimension client historisée |
| 11 | le nombre de ventes rattachées au client non identifié |
| 12 | le nombre de caractères de noms de clients recopiés dans la table plate, comparé au même texte rangé dans la dimension |

---

## Correction détaillée

### A · Réponses de récupération

1. Insertion, mise à jour, suppression, redondance.
2. Ce que représente une ligne, écrit en une phrase ; il se prouve en comparant le nombre de valeurs
   distinctes de la clé au nombre de lignes.
3. Additive : le chiffre d'affaires (**15 595 154 955** FCFA). Semi-additive : le stock, additif dans
   l'espace et pas dans le temps (**6 776** lignes mensuelles). Non additive : une moyenne, comme le
   délai de livraison moyen (**6,66** jours).
4. Une nouvelle version à chaque changement, avec une période de validité ; chaque jointure doit porter
   la clause de date qui lit la version en vigueur **au moment du fait**.
5. Pour que toutes les lectures du temps soient comparables, et parce que la définition du trimestre,
   de la semaine ou de l'exercice doit vivre à un seul endroit.

### B · Corrigé du quiz

| Q | Réponse | Le point à retenir |
|---|---|---|
| 1 | **b** | une relation plusieurs à plusieurs exige une table intermédiaire, jamais une colonne de plus |
| 2 | **b** | la troisième forme normale traque la dépendance transitive, pas la taille des tables |
| 3 | **b** | le grain se décrit avant de se compter |
| 4 | **b** | le stock monte et descend dans l'espace, pas dans le temps |
| 5 | **b** | le type 3 garde une valeur d'avant, ce qui suffit rarement |
| 6 | **b** | **240 000** ÷ **146 161** = **1,64** ligne par ticket |
| 7 | **a** | **31 298 080 184** ÷ **15 595 154 955** = **2,01** : le montant répété par la table de pont |
| 8 | **c** | un trimestre est la somme de ses mois, donc additif |
| 9 | **b** | le statut de férié vit dans la dimension de temps, jamais dans le fait |
| 10 | **b** | **16** libellés pour **7** familles : le référentiel n'a pas été appliqué |
| 11 | **b** | un total juste autorise une répartition fausse de **102 917 580** FCFA |
| 12 | **b** | le pont relie, il ne porte pas de montant : **2,01** fois le chiffre d'affaires sinon |
| 13 | **b** | la date hors calendrier se corrige dans le calendrier, pas dans la requête |
| 14 | **b** | **− 28,9 %** contre **+ 15,4 %** : **44,3** points d'écart pour une borne |
| 15 | **b** | sans contrainte déclarée, la garantie vit dans le contrôle, et un contrôle s'exécute |

### C · Corrigé des exercices de normalisation

**N1.** La table viole la première forme normale par ses groupes qui se répètent dans la colonne
désignation, la deuxième par la dépendance du nom et de la ville du client à l'identifiant de
commande autant qu'à celui du client, et la troisième par la catégorie qui dépend de la désignation
et non de la ligne de commande. Le modèle attendu compte quatre tables : `commande` (clé identifiant de
commande, **11** lignes distinctes), `ligne_commande` (clé commande et produit, grain : une ligne de
commande, **12** lignes), `client` (clé identifiant de client, **3** lignes) et `produit` (clé
identifiant de produit, **3** lignes). Les quatre anomalies se lisent dans le tableau : l'insertion
d'un nouveau client exige une commande (anomalie d'insertion) ; changer la ville de Diallo demande de
modifier **5** lignes (mise à jour) ; supprimer les quatre commandes de Nikiema efface le client
(suppression) ; et « Kaya » est écrit **5** fois (redondance). Le prix unitaire appartient à la table des produits :
dans la table plate, un changement de tarif oblige à réécrire toutes les lignes du produit, ce qui a
produit exactement les **616** versions de tarifs du socle.

**N2.** La variante en flocon joint la table des familles pour atteindre le libellé ; la variante
dénormalisée le lit directement dans la dimension produit. La famille est écrite **7** fois dans la
table des familles et **154** fois dans la dimension produit, soit une par produit. Les deux
variantes rendent le **même** résultat : la famille Matériaux vaut **3 535 582 421** FCFA dans le
modèle du socle. La justification attendue : la dénormalisation fait gagner deux jointures et rend la
famille lisible sans détour ; elle fait perdre un point de mise à jour unique, puisqu'un renommage de
famille touche **154** lignes au lieu de **7** ; elle ne change **rien** au chiffre d'affaires, ni au
grain, ni aux contrôles.

### D · Corrigé de l'étude de cas

**Diagnostic.** Trois causes, toutes silencieuses. La première additionne deux tables qui portent
toutes les deux un montant, sans vérifier qu'elles parlent du même fait. La deuxième y ajoute les
encaissements, troisième comptage du même argent. La troisième joint les ventes à la logistique sur
le seul magasin, si bien que chaque ligne de vente rencontre les **44** mois d'historique du magasin
et se répète. Aucune de ces trois requêtes ne produit d'erreur : elles sont syntaxiquement justes.

**Mesure.** Sur le socle, les trois modèles rendent **22 305 610 960** FCFA (**+ 43,0 %**),
**29 474 916 530** FCFA (**+ 89,0 %**) et **686 186 818 020** FCFA, soit **44** fois le chiffre juste.
Le facteur de la jointure sur le magasin vaut **44**, ce qui s'entend : un magasin a **44** mois
d'historique dans le fait de logistique. L'écart annoncé par le contrôle de gestion, environ **40 %**,
correspond au premier de ces trois cas.

**Correction.** La requête juste lit un seul fait, au bon grain, avec son filtre de retours :
`SELECT SUM(montant_ttc) FROM fait_ventes WHERE est_retour = 0`, et rend **15 595 154 955** FCFA. Le
chiffre d'affaires toutes lignes vaut **15 419 985 157** FCFA : l'écart de **175 169 798** FCFA est
exactement le montant des **2 809** retours, qu'il ne faut pas oublier de filtrer.

**Preuve.** Les **4** contrôles du chapitre C07 : unicité sur les **14** tables, grain sur les **7**
faits, **12** clés étrangères sans orphelin, et la recette au franc près. Un modèle de **14** tables
dont le total tombe juste est un modèle qu'on peut publier.

**Note au directeur financier, dix lignes.** Les trois extraits ne pouvaient pas s'additionner : les
ventes, les commandes et les encaissements décrivent trois moments du même argent. Le rapport
comptait donc une partie de l'activité deux fois et l'autre trois fois, et la jointure par magasin
multipliait chaque ligne par les **44** mois d'historique. Le chiffre juste est **15 595 154 955**
FCFA pour l'exercice, hors retours ; toutes lignes comprises, il vaut **15 419 985 157** FCFA, la
différence étant les **2 809** retours de l'année. Nous avons ajouté **4** contrôles qui s'exécutent à
chaque chargement et refusent la publication en cas d'écart : le total, le grain, les liens et
l'unicité des clés. Aucun rapport ne sortira désormais sans eux.

### E · Corrigé de l'auto-test

| N° | Réponse |
|---|---|
| 1 | **23 913** lignes, **23 913** valeurs distinctes |
| 2 | **240 000** lignes, **240 000** valeurs distinctes : la clé de vente est unique |
| 3 | **240 000** lignes des deux côtés |
| 4 | **0** orphelin |
| 5 | **0** orphelin, hors les **43 161** ventes de la ligne déclarée |
| 6 | **15 595 154 955** FCFA hors retours, **15 419 985 157** FCFA toutes lignes |
| 7 | **6 685 260 000** FCFA, soit **42,9 %** du chiffre d'affaires net |
| 8 | **0** jour |
| 9 | **13** dates, pour **46** commandes et **32 772 075** FCFA |
| 10 | **24 893** versions, pour **900** clients ayant une histoire |
| 11 | **43 161** ventes, **2 852 612 447** FCFA |
| 12 | **2 826 394** caractères recopiés, contre **239 599** dans la dimension |

---

**Rappel du barème d'ensemble :** quiz **20** pts (seuil **11**) + normalisation **20** pts + étude de
cas **30** pts (seuil **18**) + auto-test **5** pts = **75** points, **seuil de réussite 48**.

**Pour aller plus loin.** Le projet **M13.P** « Le modèle de Sahel Distribution » (**20** points,
seuil **13**) demande les quatre livrables du module : modèle conceptuel et logique, script
exécutable avec ses **4** contrôles, revue en **15** points, et note de choix de **3** pages. C'est la
**4**ᵉ pièce du dossier de portfolio, après les rapports SQL de M11 et la carte de **10** indicateurs
de M12.
