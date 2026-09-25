# Évaluation M12 — « Fondamentaux de la Business Intelligence »

**6 chapitres · 30 h · niveau 3 · 70 points au total · durée conseillée : 2 h 30.**
**Barème d'ensemble : quiz **15** questions (**20** points, seuil **11** sur **15**) ; deux exercices de
rédaction de KPI (**20** points) ; étude de cas (**30** points, seuil **18**) — soit **70** points,
seuil de réussite **45**.**

**Ce que l'évaluation vérifie.** Que vous savez **choisir** un indicateur, **écrire** sa définition,
**poser** son seuil, **trouver** son contre-KPI et **dire** ce qui se passe quand il passe au rouge. Les
calculs sont courts ; les définitions et les décisions sont l'essentiel.

---

## A · Questions de récupération (non notées)

1. Quels sont les **4** régimes de question, et lequel déclenche une action ?
2. Que signifie le **grain** d'une table, et comment le prouve-t-on ?
3. Quels sont les **7** champs d'une carte de définition ?
4. Dans quel ordre montent les **7** étages de la chaîne BI ?
5. Qu'est-ce qu'un contre-KPI ?

---

## B · Quiz (15 questions · 20 points)

*Les questions 1 à 10 valent 1 point ; les questions 11 à 15 valent 2 points (elles demandent un
raisonnement). Seuil : **11** points sur **15** questions traitées.*

### Bloc 1 — Définir (Q1 à Q5)

**Q1.** Un indicateur clé se distingue d'une métrique par : (a) sa précision, (b) sa carte de définition
et son responsable, (c) sa fréquence de calcul, (d) son coût de production.

**Q2.** Le même « taux de retour » peut valoir, sur le même socle : **1,12 %**, **1,16 %**, **1,17 %**,
**1,91 %**. Ces écarts viennent : (a) d'erreurs de calcul, (b) d'un choix de numérateur et de
dénominateur, (c) de la qualité des sources, (d) de la période observée.

**Q3.** La marge brute du socle vaut **29,12 %** : ce chiffre est rapporté : (a) au chiffre d'affaires
toutes taxes comprises, (b) au chiffre d'affaires hors taxes, (c) aux achats, (d) au chiffre d'affaires
brut.

**Q4.** Une carte de définition compte **7** champs. Lequel manque le plus souvent dans la pratique ?
(a) la formule, (b) la source, (c) le responsable et le seuil, (d) la granularité.

**Q5.** Le contre-KPI d'un taux de rupture élevé est : (a) le taux de service, (b) la rotation de stock,
(c) le panier moyen, (d) le taux de recouvrement.

### Bloc 2 — Mesurer (Q6 à Q10)

**Q6.** Le socle compte **2 428** ruptures pour **33 296** couples produit-magasin-mois servis. Le taux de
rupture vaut : (a) **7,29 %**, (b) **12,1 %**, (c) **0,73 %**, (d) **242,8 %**.

**Q7.** Additionner les stocks des **44** mois donne **2 034 733** unités, contre **45 882** au dernier
mois. Cela montre qu'un stock est : (a) additif, (b) semi-additif, (c) non additif, (d) constant.

**Q8.** Le taux de service vaut **81,0 %** sur les commandes livrées et **78,2 %** sur toutes les
commandes. L'écart s'explique par : (a) les retours, (b) les **319** commandes annulées, (c) les jours
fériés, (d) les prix manquants.

**Q9.** Posé à **1,5** mois de couverture, un seuil d'alerte met en alerte **5 126** lignes sur **6 776**.
Ce seuil est : (a) excellent, (b) trop sensible pour être utile, (c) insuffisant, (d) impossible à
calculer.

**Q10.** Le coût logistique unitaire du socle vaut **3 284** FCFA par colis ; sur les seuls magasins,
**3 281** FCFA. L'écart vient : (a) des **8 766** colis du dépôt, qui ne vend rien, (b) des taxes,
(c) du carburant, (d) des retours.

### Bloc 3 — Décider (Q11 à Q15, 2 points chacune)

**Q11.** La direction annonce : « la rotation doit passer de **9,42** à **12** tours ». Quelles
conséquences mesurables attendez-vous, et quel indicateur le prouvera ?

**Q12.** Un indicateur de part de marché interne montre qu'un magasin gagne **2** points face à son voisin
de la même ville. Pourquoi faut-il un contre-KPI, et lequel ?

**Q13.** Le taux de recouvrement est de **74 %** et l'encours échu de plus de **90** jours pèse
**1 091 339 030** FCFA. Rédigez l'action associée au seuil, avec un volume et un délai.

**Q14.** Un prestataire propose **40** indicateurs « pour être complet ». Rédigez en trois phrases
l'argumentaire de refus, en vous appuyant sur les chiffres du dossier du projet raté.

**Q15.** Deux personnes justes se contredisent : l'une annonce **23 497** clients, l'autre **188 886**.
Expliquez, puis dites quelle phrase de définition empêche le débat.

---

## C · Exercices de rédaction de KPI (20 points · 2 exercices · PATCH_8 : les énoncés reformulent, ils ne
recopient jamais un exercice du cours)

### R1 — Le taux de rupture (10 points de rédaction)

**Énoncé.** Rédigez la carte de définition complète du **taux de rupture** du réseau de distribution, en
vous appuyant sur le socle fourni.

**Attendu, dans cet ordre :**

1. **la formule**, avec le numérateur et le dénominateur écrits en toutes lettres, et la précision du
   périmètre retenu (les couples réellement servis, pas le catalogue entier) ;
2. **les deux versions concurrentes** que vous avez écartées, avec leur valeur mesurée et la raison de
   votre choix ;
3. **la source** exacte et ses limites connues ;
4. **la granularité** et **la fréquence**, avec la date d'arrêté des données ;
5. **le responsable**, nommé par fonction ;
6. **le seuil d'alerte**, accompagné du nombre de produits qu'il met en alerte ;
7. **le contre-KPI**, avec sa valeur mesurée ;
8. **l'action si rouge**, avec un volume et un délai.

**Barème.** 8 points pour les champs 1 à 7 (1 par champ, 2 pour la formule) ; 2 points pour la cohérence
d'ensemble. Un seuil sans action mesurée ne compte pas.

### R2 — La part des clients non identifiés (10 points)

**Énoncé.** Le service commercial veut suivre la part des ventes réalisées sans identification du client.
Rédigez la carte complète du KPI correspondant.

**Attendu.** La carte complète (les **7** champs), la **valeur actuelle mesurée** sur le socle, **le choix
argumenté** entre la part des lignes et la part du chiffre d'affaires, et un **contre-KPI** qui empêche
d'améliorer l'indicateur en créant des fiches en doublon.

**Barème.** 7 points pour les **7** champs ; 2 points pour la justification du choix de définition ; 1
point pour la pertinence du contre-KPI.

---

## D · Étude de cas — « la direction veut un tableau de bord, elle a déjà tort de le vouloir comme ça » (30 points · seuil 18)

### La commande

> « Nous voulons **un** tableau de bord, pour **tout** : le chiffre d'affaires, la marge, les stocks, les
> ruptures, les livraisons, les impayés et la logistique, avec les comparaisons avec l'an dernier. Les
> directeurs l'ouvriront tous les matins. »

Trois questions vous sont posées par la direction, qui attend une réponse écrite.

**Question 1 (10 points) — Reformulez la commande.** Écrivez la commande telle que vous l'acceptez : les
décisions à éclairer, les destinataires, la fréquence de publication, et le nombre maximal d'indicateurs.
Justifiez chaque élément par un chiffre du socle ou du dossier.

**Question 2 (12 points) — Choisissez cinq indicateurs, pas plus.** Sélectionnez au plus **5** indicateurs
parmi les **10** du mandat de reprise, donnez pour chacun sa valeur actuelle mesurée, son seuil et son
contre-KPI. Puis expliquez, en une phrase par indicateur écarté, pourquoi il ne fait pas partie des cinq.

**Question 3 (8 points) — Rédigez la phrase de refus argumenté.** En trois phrases maximum, refusez les
deux demandes suivantes sans perdre le client : « toutes les mailles, tous les jours » et « le même
tableau de bord pour tout le monde ». Chaque phrase doit contenir un argument **mesuré**.

### Le résultat attendu (à retrouver, pas à recopier)

- **La fréquence quotidienne** se justifie sur **2** ou **3** indicateurs au maximum (ruptures,
  encaissements du jour) ; les autres se lisent au mois.
- **Les 5 indicateurs** doivent inclure au moins un indicateur de marge ou de prix, un indicateur de stock
  ou de rupture, et un indicateur de trésorerie — sinon la direction ne peut pas arbitrer.
- **Le refus argumenté** s'appuie sur des ordres de grandeur du socle : **41** indicateurs livrés pour
  **4** lecteurs sur **14** ; une marge qui vaut **29,12 %** ou **24,67 %** selon la base ; un panier moyen
  de **107 396** FCFA par ticket ou **65 749** par ligne.

### Barème de l'étude de cas

| Élément | Points |
|---|---|
| Q1 : commande reformulée, complète et justifiée | **10** |
| Q2 : cinq indicateurs, valeurs mesurées, seuils, contre-KPI, écartés justifiés | **12** |
| Q3 : refus argumenté, chiffré, courtois | **8** |
| **Total** | **30** |

**Seuil de l'étude de cas : 18 points sur 30.**

---

## Correction détaillée

### A · Réponses de récupération

1. Descriptif, diagnostique, prédictif, prescriptif — le prescriptif, seul, déclenche une action.
2. Ce que représente une ligne ; on le prouve par une clé dont le nombre de valeurs distinctes égale le
   nombre de lignes.
3. Formule, source, granularité, fréquence, responsable, seuil d'alerte, contre-KPI.
4. Sources, extraction, stockage, modèle, couche sémantique, visualisation, diffusion.
5. L'indicateur qui mesure ce qu'on dégrade en améliorant le premier ; il se publie à côté de lui.

### B · Corrigé du quiz

| Q | Réponse | Le point à retenir |
|---|---|---|
| 1 | **b** | une métrique se calcule ; un KPI se définit et s'attribue |
| 2 | **b** | **1,12 %** en valeur, **1,91 %** en tickets : cinq définitions, toutes justes |
| 3 | **b** | la même marge vaut **24,67 %** toute taxe comprise |
| 4 | **c** | le responsable et le seuil sont les deux champs qu'on saute |
| 5 | **b** | stocker plus réduit la rupture et dégrade la rotation (**9,42** tours) |
| 6 | **a** | **2 428** ÷ **33 296** |
| 7 | **b** | semi-additif : additif dans l'espace, jamais dans le temps |
| 8 | **b** | les **319** commandes annulées sortent du premier dénominateur |
| 9 | **b** | à **1,5** mois, **75,6 %** des lignes s'allument : le seuil ne discrimine plus |
| 10 | **a** | les **8 766** colis du dépôt, qui ne vend rien, sortent du second calcul |
| 11 | 2 pts | réduire la couverture (**1,27** mois) augmente les produits sous **1** mois (**50** aujourd'hui) et pousse la rupture (**7,29 %**) : à surveiller par le taux de rupture par famille |
| 12 | 2 pts | le gain d'un magasin est la perte de l'autre dans la même ville (**60,8 %** / **39,2 %** à Ouagadougou) : le contre-KPI est le CA du **réseau** |
| 13 | 2 pts | relancer les **1 155** factures de plus de **90** jours sous quinzaine, liste par ordre de montant, responsable du recouvrement |
| 14 | 2 pts | **41** indicateurs pour **4** lecteurs sur **14** et **11** semaines de vie : le plafond de **10** indicateurs documentés est un choix d'usage, pas de confort |
| 15 | 2 pts | **23 497** clients distincts ; **188 886** est la **somme** des clients par produit (un client achète **8,04** produits en moyenne) : la phrase « les comptages distincts ne s'additionnent pas » clôt le débat |

### C · Corrigé des exercices de rédaction

**R1 — le taux de rupture.** Formule retenue : couples produit-magasin-mois **en rupture** ÷ couples
produit-magasin-mois **servis**, soit **2 428** ÷ **33 296** = **7,29 %**. Version écartée n° 1 : la part
des jours de rupture sur les jours ouvrés (**13 129** jours cumulés), qui mesure la durée et non la
couverture. Version écartée n° 2 : le taux calculé sur le catalogue entier, qui mesurerait l'assortiment.
Granularité produit × magasin × mois ; fréquence mensuelle, données arrêtées au dernier jour du mois ;
responsable : direction des opérations ; seuil : plus de **10 %** des couples servis, ce qui met en alerte
les produits les plus touchés ; contre-KPI : rotation (**9,42** tours) et couverture (**1,27** mois) ;
action si rouge : revue des 20 produits les plus touchés avec les achats sous cinq jours, sur la base du
coût estimé de **169 386 812** FCFA.

**R2 — la part des clients non identifiés.** Formule : part du **chiffre d'affaires** réalisé sur des
lignes sans identifiant client, soit **18,3 %** et **2 852 612 447** FCFA. Le choix de la part du chiffre
d'affaires est justifié : la part des lignes mesurerait la saisie au comptoir, pas la connaissance de la
clientèle. Granularité magasin × mois ; fréquence mensuelle ; responsable : qualité de la donnée ; seuil :
**15 %** ; contre-KPI : nombre de fiches clients créées et taux de doublons — sans lui, l'indicateur
s'améliore en polluant le référentiel ; action si rouge : contrôle de saisie par magasin, sur la liste des
tickets concernés.

### D · Corrigé de l'étude de cas

**Q1 — la commande reformulée.** Attendu : **un** écran, **5** à **10** décisions explicites, des
destinataires nommés, une fréquence par indicateur (mensuelle pour la plupart, quotidienne pour les
ruptures et les encaissements), et un plafond d'indicateurs assumé. La justification s'appuie sur le
dossier raté : **41** indicateurs, **4** lecteurs sur **14**, **11** semaines.

**Q2 — cinq indicateurs.** Une sélection défendable : **CA net** (**15 595 154 955** FCFA ; contre-KPI :
taux de retour **1,17 %**), **marge brute** (**29,12 %** hors taxes ; contre-KPI : volume, recette
unitaire × **1,174** pour des unités × **1,169**), **taux de rupture** (**7,29 %** ; contre-KPI :
rotation **9,42** tours), **taux de recouvrement** (**74,0 %** ; contre-KPI : CA net), **coût logistique
unitaire** (**3 284** FCFA par colis ; contre-KPI : taux de service **81,0 %**). Les indicateurs écartés
se justifient un par un : rotation (redondante avec la rupture, publiée en contre-KPI), panier moyen
(utile au mois, pas au jour), part de marché interne (mesure interne, pas d'action), taux de retour
(suivi en contre-KPI du CA).

**Q3 — la phrase de refus.** Attendu : trois phrases, chacune avec un argument chiffré. Par exemple :
« Tous les jours et à toutes les mailles supposent de lire **2 428** couples de rupture par mois : nous
publions au jour les ruptures et au mois les sept autres indicateurs, ce qui couvre **100 %** des
décisions recensées. » ; « Le même tableau pour tous a produit **14** destinataires et **4** lecteurs :
nous préparons deux vues, une de pilotage (5 indicateurs, mensuelle) et une d'action (ruptures et
encaissements, quotidienne). » ; « Chaque définition supplémentaire coûte un débat non tranché — la marge
vaut **29,12 %** ou **24,67 %** selon la base : nous écrivons les définitions avant l'écran. »

---

**Rappel du barème d'ensemble :** quiz **20** pts (seuil **11** sur **15**) + rédaction de KPI **20** pts
+ étude de cas **30** pts (**seuil 18**) = **70** points, **seuil de réussite 45**.
