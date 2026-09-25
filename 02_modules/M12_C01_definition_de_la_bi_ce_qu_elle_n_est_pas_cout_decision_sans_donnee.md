# Module M12.C01 — Qu'est-ce que la BI, et ce qu'elle n'est pas

**Outils : DuckDB 1.5.5 (exécuté), pandas (contrôle croisé, exécuté), Excel (exécuté). Power BI
(cité, non exécuté — règle §1.5). Durée indicative : 5 h. Niveau : N3. Prérequis : M09 (questions
métier), M10 (support), M11 (la matière : des requêtes fiables).**

> **L'idée du chapitre.** La Business Intelligence n'est pas une collection de graphiques, ni un
> logiciel, ni un projet informatique : c'est l'**organisation qui fait qu'un chiffre arrive devant
> celui qui doit décider, à temps, avec une définition unique, et suivi d'une action décidée
> d'avance**. Ce chapitre installe cette définition et la met immédiatement à l'épreuve du socle :
> **41** indicateurs livrés, **4** personnes qui les ouvrent le premier jour, **11** semaines plus
> tard un contrat résilié. Le module entier part de cet échec mesuré — parce qu'on apprend mieux une
> discipline par ce qu'elle rate que par ce qu'elle promet.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **définir** la Business Intelligence, et la distinguer de quatre choses avec lesquelles on la
   confond tous les jours (le graphique, le logiciel, le rapport figé, l'intelligence artificielle) ;
2. **situer** la place de chacun dans une chaîne qui va de la donnée brute à la décision, et nommer
   ce que chaque maillon ajoute ;
3. **chiffrer le coût d'une décision sans donnée** — retardée, fausse, ou jamais prise — sur un cas
   réel du socle, plutôt que sur une généralité ;
4. **estimer l'économie d'un dispositif BI** dans une PME : ce qu'il coûte, ce qu'il rapporte, et
   pourquoi son coût visible n'est jamais son vrai coût ;
5. **citer les trois questions de cadrage** sans lesquelles aucun dispositif ne tient (quelle
   décision, qui décide, que fait-on si c'est rouge) et repérer les cinq signaux d'un échec
   annoncé.

---

## 2. Pourquoi cette notion est importante

Vous savez produire des chiffres justes depuis M11. C'est nécessaire et ce n'est pas suffisant : sur
le socle du module, **15 595 154 955** FCFA de ventes ont été enregistrés, **2 428** couples
produit-magasin-mois sont passés en rupture, **1 202 550 590** FCFA de factures restent ouvertes —
et **aucun** de ces trois nombres, à lui seul, n'a jamais fait prendre une bonne décision.

La raison est simple et brutale : **une décision ne consomme pas des chiffres, elle consomme des
écarts**. « Nous avons vendu 15 595 154 955 FCFA » n'appelle aucune action ; « nous avons vendu
**1,12 %** de moins que ce que nos propres définitions appellent le chiffre d'affaires » appelle une
réunion. La BI est la discipline qui fabrique systématiquement ce deuxième type de phrase — et qui
organise l'entreprise pour qu'il arrive à l'heure.

> **Attention.** Un chiffre juste publié au mauvais grain, à la mauvaise fréquence, ou sans
> responsable, produit exactement le même effet qu'un chiffre faux : il ne change rien. C'est la
> découverte la plus coûteuse de ce module, et le dossier du projet raté la démontre sur **11**
> semaines.

> **À retenir.** La BI ne se juge pas au nombre de chiffres publiés, mais au nombre de **décisions**
> qu'elle rend possibles : **41** indicateurs pour **10** décisions réclamées, dans le dossier du
> projet, c'est trente et un chiffres de trop.

---

## 3. Explication simple — le tableau de bord du camion

Prenez un camion de livraison. Il possède **beaucoup** de mesures : température moteur, pression des
pneus, niveau de carburant, vitesse, charge, usure des freins, pression d'huile, tension de la
batterie. Le constructeur n'affiche pas tout devant le conducteur : il en garde une poignée, choisie
selon **une seule règle** — *est-ce que cette aiguille peut changer une action pendant que je
conduis ?* La température d'huile qui monte : je m'arrête. La pression d'un pneu : je ralentis.
Le kilométrage : il déclenche un entretien, pas une action immédiate. L'usure des freins : elle
se planifie.

Le reste des mesures existe : elles vivent dans le calculateur, lues par le garagiste, au moment où
quelqu'un en a besoin.

Un dispositif de BI fonctionne exactement comme ce tableau de bord, et échoue exactement comme un
tableau de bord qui afficherait les **41** mesures du camion en même temps, sur **7** écrans, sans
dire laquelle impose quoi. Le conducteur poserait son regard ailleurs — c'est ce qui est arrivé au
dispositif du dossier : **14** destinataires, **4** ouvertures le premier jour, **3** la deuxième
semaine.

---

## 4. Vocabulaire essentiel

> **Définition.** La **Business Intelligence** (BI) est l'ensemble organisé des moyens — données,
> définitions, modèles, outils, responsabilités — qui permet à une organisation de **décider avec des
> chiffres partagés** : les mêmes définitions pour tous, disponibles au bon moment, avec une action
> décidée d'avance quand ils passent un seuil.

> **Définition.** Un **indicateur clé** — KPI, *Key Performance Indicators* — est une mesure
> **choisie** pour suivre une performance et **déclencher une décision**. Ce qui le distingue d'une
> simple mesure tient là, et nulle part ailleurs : *à qui sert-il, pour décider quoi ?*

> **Définition.** Une **décision fondée sur les données** — *data-driven* — est prise en s'appuyant
> sur des mesures définies **avant** la décision, et vérifiables **après**. Sans la seconde partie,
> l'expression n'est qu'une façon de parler.

> **Définition.** La **couche sémantique** — *semantic layer* — est l'endroit — table, vue, modèle —
> où les définitions d'indicateurs sont **écrites une fois** pour toute l'organisation. C'est la
> version industrielle de la carte de définition du chapitre C04.

**Le vocabulaire minimal de la chaîne**, dans l'ordre : *donnée* (un enregistrement), *information*
(une mise en relation — « ce magasin vend 3,06 fois plus que le plus petit »), *connaissance*
(une règle — « nos ruptures se concentrent sur les produits à rotation rapide »), *décision*
(un engagement — « nous portons le stock de ces 23 références à deux mois »).

---

## 5. Cours approfondi

### 5.1 Ce que la BI n'est pas — cinq confusions qui coûtent

| Ce qu'on croit | Ce que c'est en réalité | Le coût mesuré de la confusion |
|---|---|---|
| « de la belle visualisation » | une **définition** partagée, souvent invisible sur l'écran | le dispositif à **41** indicateurs était lisible ; il était indéfini |
| « un projet informatique » | un **projet métier** que l'informatique outille | **2** définitions du CA coexistaient sans arbitrage |
| « un rapport figé » | un **service** mis à jour, corrigé, retiré | la maintenance résiliée (**1 200 000** FCFA/an) a tué l'usage |
| « de l'intelligence artificielle » | de la **définition** et de la **discipline** | aucune décision n'est prise par un modèle dans ce module |
| « toutes nos données » | les **quelques** mesures qui changent une action | **41** indicateurs pour **14** lecteurs, dont **4** le premier jour |

### 5.2 La chaîne de la donnée à la décision, maillon par maillon

```
   source          →   extraction      →   stockage       →   modèle
   (le fait)           (le transport)      (la mémoire)       (la structure)

   →   couche sémantique   →   visualisation   →   diffusion   →   décision
       (les définitions)       (la lecture)        (l'accès)       (l'action)
```

Chaque maillon **ajoute** quelque chose, et chaque maillon **peut** casser le résultat :
une extraction qui perd les retours fabrique les **175 169 798** FCFA d'écart du §7.2 ; un modèle qui
double les lignes double les totaux ; une visualisation sans unité fait lire des milliers comme des
millions ; une diffusion sans responsable produit des chiffres que personne ne défend.

**Le maillon invisible** — et c'est celui de M12 — est la **couche sémantique** : celle où « chiffre
d'affaires » veut dire une chose précise. Aucun outil ne l'invente à votre place.

### 5.3 Le coût d'une décision sans donnée : trois formes

| Forme | Ce qui se passe | Mesure sur le socle |
|---|---|---|
| **Décision retardée** | on attend d'être sûr, l'occasion passe | **13 129** jours de rupture cumulés avant réaction |
| **Décision fausse** | on décide sur un indicateur mal défini | rotation lue **0,78** au lieu de **9,42** tours : on stocke au lieu de déstocker |
| **Non-décision** | personne ne sait que faire si c'est rouge | **1 272** factures ouvertes, **1 202 550 590** FCFA, aucun seuil associé à une action |

La troisième est la plus chère et la moins visible. Elle ne produit aucune erreur : elle produit un
**silence**.

> **Attention.** Ne pas décider est une décision — elle est simplement prise sans vous. **1 272**
> factures restent ouvertes pour **1 202 550 590** FCFA non pas parce que personne ne sait les
> relancer, mais parce que personne n'a écrit **qui** devait le faire à partir de quel seuil. Le dossier du projet raté la décrit en une ligne — le seuil de rupture n'a jamais été
relié à une action — et c'est la raison pour laquelle le mandat de reprise exige une page intitulée
« que fait-on quand c'est rouge ? ».

### 5.4 L'économie réelle d'un dispositif BI dans une PME

Le dossier du projet fournit le chiffrage : **7 940 000** FCFA la première année, dont **1 640 000**
pour la seule reprise des sources et **1 200 000** de maintenance — pour un dispositif abandonné en
**11** semaines. Trois enseignements d'économie, tous vérifiables :

1. **Le coût dominant n'est pas l'outil, c'est la matière.** La reprise des sources pèse plus de
   **20 %** du projet ; un projet qui la sous-estime livre un tableau de bord qui calcule juste sur
   des données fausses.
2. **Le retour ne vient jamais du nombre d'indicateurs.** Ici **41** indicateurs pour **10**
   décisions réclamées au mandat de reprise : tout ce qui dépasse la décision est du coût pur.
3. **Un dispositif non maintenu meurt vite.** **4** ouvertures le premier jour, **3** trois semaines
   plus tard : la courbe d'adoption se lit comme un indicateur, et c'est le seul qui compte.

> **Dans les faits.** L'atelier de ce manuel applique la règle à lui-même : les dix indicateurs du
> module sont recalculés par un script (`tools/kpi_M12.py`) à chaque relevé de chiffres, et le
> contrôle croisé côte pandas vérifie que le CA net vaut bien **15 595 154 955** FCFA des deux
> côtés. Une définition qui ne se vérifie pas toute seule finit par diverger.

### 5.5 Qui fait de la BI dans une PME

| Rôle | Ce qu'il décide | Ce qu'on lui doit |
|---|---|---|
| Direction | les priorités et les arbitrages de définition | **une** carte de définition, pas un catalogue |
| Responsable métier | l'action quand l'indicateur passe au rouge | un seuil **et** une action, écrits |
| Analyste BI | la justesse, la fraîcheur, la documentation | le droit de refuser un indicateur indéfini |
| Informatique | les accès, les flux, la sécurité | des définitions stables, pas des demandes quotidiennes |

La ligne la plus mal comprise est la dernière : **l'analyste doit pouvoir refuser**. Un indicateur
sans définition écrite et sans responsable produira, le jour du désaccord, deux chiffres et zéro
décision — exactement le scénario des **3** sources discordantes du dossier.

### 5.6 Les trois questions de cadrage

1. **Quelle décision ?** — « la direction veut tout suivre » n'est pas une décision. « Nous devons
   décider chaque mois quelles références porter à deux mois de stock » en est une.
2. **Qui décide, et quand ?** — un indicateur sans nom de responsable et sans rendez-vous est un
   objet décoratif.
3. **Que fait-on si c'est rouge ?** — la question qui distingue un dispositif vivant d'un dispositif
   abandonné. Elle se répond **avant** la livraison, en une phrase par indicateur.

### 5.7 Les cinq signaux d'un échec annoncé

| Signal | Seuil d'alerte observé | Ce qu'il annonce |
|---|---|---|
| Adoption | moins de la moitié des destinataires ouvrent dans la semaine | le dispositif n'est pas attendu |
| Définitions | un même indicateur a **2** valeurs en réunion | la couche sémantique n'existe pas |
| Décisions | aucun seuil relié à une action | les alertes seront ignorées |
| Périmètre | plus de **10** indicateurs pour une équipe | la priorité n'a pas été choisie |
| Maintenance | personne ne sait qui corrige une définition | l'abandon est daté |

### 5.8 Quatre façons de rater la couche sémantique

La couche sémantique est le seul maillon du §5.2 qu'aucun outil ne fournit. Quatre échecs typiques,
tous observables dans la semaine qui suit la mise en service :

| Échec | Ce qu'on voit | Ce qu'il faut faire |
|---|---|---|
| **Deux définitions, deux fichiers** | le CA « compta » et le CA « du tableau de bord » diffèrent de **175 169 798** FCFA | écrire **une** définition, publier l'autre comme un indicateur distinct et nommé |
| **Le grain implicite** | le panier moyen vaut **107 396** FCFA ou **65 749** FCFA selon qu'on divise par les tickets ou les lignes | nommer le dénominateur dans le titre de l'indicateur |
| **La convention tacite** | les retours comptés en négatif dans un onglet, exclus dans l'autre | figer la convention dans la carte de définition (C04) |
| **La mise à jour sans date** | deux lecteurs comparent des chiffres de deux jours différents | dater chaque bloc de résultats, à l'écran |

**La règle qui les prévient toutes.** Une définition est complète quand un lecteur qui n'a pas écrit
l'indicateur peut le recalculer sans vous appeler — même critère que les rapports de M11, appliqué
aux définitions.

### 5.9 Ce que ce chapitre ne couvre pas

Le **vocabulaire exact** des données (métrique, dimension, fait, grain) est le chapitre C03 ; la
**fabrication** d'un indicateur — les six critères, la carte de définition, le contre-KPI — est le
chapitre C04 ; l'**architecture** détaillée (sept étages, leurs pannes, leurs coûts) est le C05 ; la
**conduite de projet** et les dix causes d'échec sont le C06. Ce chapitre-ci tient volontairement une
seule question : *pourquoi la BI existe, et à quoi on reconnaît qu'elle n'y est pas encore ?*

---

## 6. Exemple concret — une décision de réassort, avec et sans BI

Le magasin de Kaya doit décider, pour le mois qui vient, quelles références porter à deux mois de
stock. Voici les trois façons de décider, et ce que chacune coûte sur le socle.

**Sans tableau de bord.** Le responsable regarde les rayons et commande ce qui manque. Ce qui manque,
il ne le voit qu'au moment où le client le demande : le socle compte **2 428** ruptures et
**13 129** jours de rupture. Le manque à gagner **estimé** — car une rupture ne se mesure pas, elle
s'estime — vaut **169 386 812** FCFA.

**Avec un chiffre, mal défini.** On lui donne « la rotation de stock ». L'indicateur est calculé en
divisant les ventes de douze mois par la **somme** des douze stocks mensuels : **0,78** tour par an.
Conclusion, mécanique : « notre stock ne tourne pas, arrêtons de commander ». Or la même donnée, avec
le bon dénominateur — la **moyenne** mensuelle du stock — donne **9,42** tours par an, couverture
**1,27** mois, c'est-à-dire un stock **sain**. Un chiffre mal défini fait prendre la décision exacte
inverse de celle qu'il fallait.

**Avec un indicateur défini.** « Rotation de stock : quantités vendues sur douze mois glissants
divisées par le stock moyen mensuel de la même période ; cible **9,42** tours ; seuil d'alerte en
dessous de **7** ; responsable : le responsable d'approvisionnement ; action si rouge : révision du
plan de réassort sous cinq jours ouvrés ; contre-KPI : taux de rupture. » Cette phrase — et non la
requête — est ce que M12 apprend à écrire. Elle a trois vertus : elle rend le chiffre reproductible,
elle rend la décision obligatoire, et elle empêche de « gagner » la rotation en laissant mourir le
service client.

---

## 7. Démonstration pas à pas — six étapes sur le socle

Tout se rejoue avec `03_exercices/dossier_M12/connexion.py` (socle de M11 + les cinq tables
opérationnelles).

### 7.1 Étape 1 — le total de contrôle

```sql
SELECT ROUND(SUM(montant_ttc)) AS ca_net
FROM ventes
WHERE est_retour = 0;
```

**15 595 154 955** FCFA. C'est le total de référence du module : tout indicateur qui parle de chiffre
d'affaires doit retomber dessus, ou dire pourquoi il ne le fait pas.

### 7.2 Étape 2 — la même question, deux définitions

```sql
SELECT ROUND(SUM(montant_ttc)) AS ca_toutes_lignes FROM ventes;
```

**15 419 985 157** FCFA. L'écart avec l'étape 1 vaut **175 169 798** FCFA, soit **1,12 %** : les
lignes de retour, négatives, sont comptées. Aucune des deux valeurs n'est fausse — la première parle
d'activité nette, la seconde de flux de caisse. Ce qui est faux, c'est de les **mélanger** dans un
même rapport : c'est exactement la première discorde du dossier du projet raté.

### 7.3 Étape 3 — l'indicateur qui décide, et son denominateur

```sql
SELECT ROUND(SUM(v.quantite) / AVG(stock_du_mois), 2) AS rotation
FROM ventes v,
     (SELECT mois, SUM(stock_moyen_unites) AS stock_du_mois
      FROM stock_mensuel GROUP BY 1) s
WHERE v.est_retour = 0
  AND v.date_vente >= DATE '2025-09-01' AND v.date_vente < DATE '2026-09-01'
  AND s.mois >= '2025-09' AND s.mois < '2026-09';
```

**9,42** tours par an. Remplacez `AVG(stock_du_mois)` par `SUM(stock_moyen_unites)` : **0,78**. Une
requête qui **ne lève aucune erreur** peut diviser un indicateur par douze — et faire stocker quand
il fallait déstocker.

### 7.4 Étape 4 — le dénominateur d'un taux, et les commandes qui disparaissent

```sql
SELECT
  COUNT(*) FILTER (WHERE statut = 'livree')                                  AS livrees,
  COUNT(*) FILTER (WHERE statut = 'livree' AND date_livraison <= date_promisee) AS a_lheure,
  COUNT(*)                                                                   AS commandes
FROM commande;
```

**8 681** livrées, **7 035** à l'heure, **9 000** commandes. Le taux de service vaut donc **81,0 %**
des livrées ou **78,2 %** des commandes, selon ce qu'on met au dénominateur — et **319** commandes
annulées décident à elles seules du chiffre publié. Deux conventions, une seule à écrire, et le mot
« annulée » à ne pas cacher sous le tapis.

### 7.5 Étape 5 — ce qu'une donnée manquante fait à un indicateur

```sql
SELECT ROUND(SUM(marge_fcfa) / SUM(montant_ht) * 100, 2) AS taux_marge
FROM vente_marge WHERE est_retour = 0;
```

**29,12 %** — alors que le référentiel annonce une marge cible de **18** à **24 %** par rayon. Deux
causes, toutes deux mesurables : deux produits du référentiel n'ont **pas de prix de vente** (écart de
**0,05** point selon qu'on les écarte ou qu'on reconstitue leur prix), et surtout les prix de vente du
socle ont monté de **25,0 %** entre 2023 (**8 219** FCFA de prix unitaire moyen) et 2026 (**10 271**
FCFA), quand le référentiel porte un prix unique. Publier « 29,12 % de marge » sans cette phrase fait
croire à une performance qui n'existe pas.

### 7.6 Étape 6 — écrire la décision, pas le chiffre

| Indicateur | Valeur | Seuil | Action si dépassé | Contre-KPI |
|---|---|---|---|---|
| Rotation | **9,42** tours | < **7** | révision du réassort en 5 jours | taux de rupture |
| Taux de rupture | **7,29 %** | > **10 %** | arbitrage de stock par rayon | rotation |
| Taux de service | **78,2 %** | < **85 %** | revue des tournées le vendredi | coût logistique unitaire |
| Recouvrement à échéance | **74,0 %** | < **80 %** | relance au 5ᵉ jour de retard | CA net |

C'est ce tableau — six colonnes, quatre lignes — que le mandat de reprise réclame, et c'est lui que
le projet M12.P vous fera produire sur dix indicateurs.

### 7.7 Étape 7 — mesurer l'adoption, c'est-à-dire la seule chose qui compte

Un dispositif se juge sur des ouvertures, pas sur des indicateurs. Le dossier du projet fournit trois
mesures qui suffisent à dater l'abandon :

| Semaine | Destinataires | Ouvertures quotidiennes moyennes | Lecture |
|---|---|---|---|
| 1 | **14** | **6** | quatre personnes l'ont ouvert le premier jour, puis le soufflé retombe |
| 2 | **14** | **3** | le dispositif n'est pas dans le rituel de travail |
| 3 → 11 | **14** | non mesurée | personne ne sait plus qui l'ouvre : l'abandon est consommé |

**La leçon de méthode.** L'ouverture n'est pas un indicateur « technique » réservé à l'informatique :
c'est le seul indicateur qui mesure la **valeur** du dispositif. Un rapport jamais ouvert coûte
exactement ce qu'a coûté celui-ci — **7 940 000** FCFA la première année — et rapporte zéro décision.
La première carte de définition qu'un analyste doit écrire n'est donc pas celle du chiffre
d'affaires : c'est celle de l'usage (« nombre de lecteurs actifs par semaine », seuil, action).

---

## 8. Erreurs fréquentes

1. **Confondre l'outil et la discipline.** Acheter une licence ne crée aucune définition.
2. **Croire qu'un indicateur est neutre.** Toute mesure **pousse** un comportement : la rotation
   pousse à déstocker, la disponibilité pousse à surstocker. D'où le contre-KPI (C04).
3. **Publier un chiffre sans son périmètre.** CA net ou toutes lignes : **1,12 %** d'écart.
4. **Mélanger deux dénominateurs** dans une même série : **81,0 %** et **78,2 %** ne se comparent pas.
5. **Laisser une donnée manquante en silence.** **2** produits sans prix suffisent à rendre une marge
   inexplicable.
6. **Multiplier les indicateurs.** **41** indicateurs, **4** lecteurs le premier jour.
7. **Confondre estimation et mesure.** Les **169 386 812** FCFA de CA perdu sont une **estimation** :
   publiés comme une mesure, ils détruisent la confiance dans tout le reste du tableau.
8. **Ne pas dater la donnée.** Un chiffre de la veille et un chiffre du mois se ressemblent.
9. **Croire que l'adoption est acquise.** Elle se mesure (**4** ouvertures le premier jour) et se
   travaille.
10. **Ne pas écrire l'action.** Un seuil sans action est un ornement — le dossier du projet en
    contient **41**.

---

## 9. Bonnes pratiques professionnelles

- **Écrire la décision avant l'indicateur.** Si vous ne pouvez pas nommer la décision, vous n'avez
  pas besoin de l'indicateur.
- **Une définition, un endroit.** La couche sémantique est la version outillée de la carte de
  définition : une seule vérité, écrite.
- **Toujours le contre-KPI.** Aucun indicateur seul : chaque couple protège l'organisation d'un
  effet pervers (§C04).
- **Distinguer mesure et estimation** dans le titre même de l'indicateur (« CA perdu estimé »).
- **Compter les lecteurs, pas les indicateurs.** L'adoption est l'indicateur de l'indicateur.

> **Conseil professionnel.** Quand on vous demande un indicateur, posez les trois questions du §5.6
> **avant** d'écrire la requête, et notez les réponses : elles constituent la carte de définition.
> Un analyste qui accepte de produire un chiffre sans ces réponses signe, à retardement, un projet
> abandonné — **7 940 000** FCFA d'exemple dans ce module.

---

## 10. Exercice guidé

**Énoncé.** Le responsable logistique demande « le coût de la logistique ». Produisez l'indicateur
complet : valeur, définition, granularité, seuil, action, contre-KPI.

**Étape 1 — mesurer.** `SELECT SUM(cout_total_fcfa), SUM(colis) FROM logistique;` donne
**172 710 030** FCFA pour **52 596** colis.

**Étape 2 — choisir la forme de l'indicateur.** Un coût total n'appelle aucune action ; un coût
unitaire, si : **3 284** FCFA par colis (**249** FCFA au kilo).

**Étape 3 — nommer le piège.** **8 766** colis sont facturés au **dépôt central**, qui n'a **aucune
vente** : un coût unitaire calculé sur l'ensemble du réseau mélange deux activités.

**Étape 4 — écrire la fiche.** Formule, source (`logistique_mensuelle.csv`), granularité
(mois × magasin), fréquence (mensuelle), responsable (responsable logistique), seuil (**> 3 700**
FCFA par colis), action (revue des tournées et du taux de remplissage), contre-KPI (**taux de
service** : on ne remplit pas un camion en livrant en retard).

---

## 11. Exercices autonomes

1. **Le coût d'une décision retardée.** Chiffrez ce que représentent les **13 129** jours de rupture
   en jours-magasin et en FCFA estimés, puis écrivez la phrase que vous diriez à la direction — en
   distinguant mesure et estimation.
2. **Deux définitions du CA.** Construisez le tableau des deux totaux (net et toutes lignes), calculez
   l'écart en FCFA et en pourcentage, et expliquez en trois lignes laquelle vous publieriez dans un
   rapport destiné à la direction financière.
3. **Le dénominateur du taux de service.** Calculez les deux taux (**81,0 %** et **78,2 %**), puis
   écrivez celle des deux définitions qui a votre préférence, et ce qu'elle cache.
4. **Le magasin sans vente.** Le dépôt central porte **8 766** colis et aucune vente. Proposez deux
   traitements possibles (l'exclure, ou lui affecter les ventes qu'il sert) et les conséquences de
   chacun sur le coût logistique unitaire.
5. **Votre propre disposition.** Prenez un dispositif que vous connaissez (vos tableaux Excel) et
   remplissez les cinq signaux du §5.7 : combien sont déjà au rouge ?

---

## 12. Correction détaillée

**Exercice 1.** Les **13 129** jours de rupture cumulés correspondent au total des jours pendant
lesquels un couple produit-magasin-mois n'était pas servable. En FCFA : **169 386 812** FCFA
**estimés**. La phrase attendue : « nous estimons à **169 386 812** FCFA le chiffre d'affaires perdu
pour cause de rupture sur la période — c'est une estimation calculée à partir du rythme de vente des
jours précédents, pas une mesure ; la mesure, elle, est le nombre de jours : **13 129**. »

**Exercice 2.** Net : **15 595 154 955** FCFA ; toutes lignes : **15 419 985 157** FCFA ; écart
**175 169 798** FCFA, soit **1,12 %**. Pour la direction financière, on publie le **net** — et on
écrit que les retours sont exclus, parce que c'est la définition qui se rapproche de la facturation.

**Exercice 3.** **81,0 %** des commandes livrées à l'heure (**7 035** sur **8 681**) ; **78,2 %** des
commandes reçues (**7 035** sur **9 000**). La seconde définition, plus sévère, a l'avantage d'être
celle que le client perçoit : une commande annulée est un échec, même si elle n'est pas « en retard ».
Le risque de la seconde : elle mélange deux causes d'échec (retard et annulation), qu'il faut alors
suivre séparément.

**Exercice 4.** *Exclure le dépôt* : le coût unitaire porte sur les **43 830** colis des magasins et
grimpe mécaniquement, mais il mesure la livraison client. *Lui affecter les ventes* : on obtient un
coût logistique global par activité, au prix d'une clé de répartition — donc d'une convention à
écrire. Dans les deux cas, la règle du module tient : la convention se **déclare**.

**Exercice 5.** Attendu : au moins deux signaux au rouge dans la plupart des cas — les définitions
multiples (deux versions d'un même chiffre dans deux fichiers) et l'absence de seuil relié à une
action. C'est le diagnostic que le projet M12.P demande de mener, chiffres à l'appui.

---

## 13. Mini-projet de chapitre

**« Radiographie d'un dispositif »** (2 h). Choisissez un ensemble de tableaux de suivi existant
(vos fichiers, ou les **7** onglets du dossier du projet raté). Produisez une page A4 qui contient :
(1) le nombre d'indicateurs et de lecteurs réels ; (2) les définitions divergentes, chiffrées ;
(3) les seuils qui n'ont pas d'action associée ; (4) les **3** questions de cadrage posées puis
répondues ; (5) une recommandation en trois lignes — réduire, redéfinir, ou arrêter. La règle de
notation : chaque affirmation porte une mesure.

---

## 14. Résumé du chapitre

| Notion | Ce qu'il faut retenir |
|---|---|
| Définition de la BI | des définitions partagées + le bon moment + une action décidée d'avance |
| Les 5 confusions | graphique, informatique, rapport figé, IA, « toutes les données » |
| La chaîne | source → extraction → stockage → modèle → couche sémantique → visualisation → diffusion → décision |
| Les 3 coûts | décision retardée (**13 129** jours), décision fausse (**0,78** contre **9,42** tours), non-décision (**1 202 550 590** FCFA d'encours) |
| L'économie | **7 940 000** FCFA pour **41** indicateurs et **4** lecteurs : la matière et la décision manquaient |
| Les 3 questions de cadrage | quelle décision · qui décide et quand · que fait-on si c'est rouge |
| Les 5 signaux d'échec | adoption, définitions, décisions, périmètre, maintenance |

## 15. À retenir

> **À retenir.** Une mesure se constate, un indicateur se **choisit** : s'il ne déclenche aucune
> décision, c'est une mesure de plus — et le coût d'un indicateur inutile est exactement celui de
> l'indicateur utile, plus l'attention qu'il consomme.

- **La BI n'est pas ce qu'on affiche, c'est ce qui est décidé.** Un dispositif dont personne ne peut
  citer une décision n'est pas un dispositif.
- **Une mesure, un indicateur, un contre-indicateur** : trois mots, trois responsabilités.
- **Le dénominateur est un choix**, et un choix non écrit devient une dispute (**81,0 %** ou
  **78,2 %** ; **9,42** ou **0,78**).
- **Estimation n'est pas mesure** : l'écrire protège tout le reste du rapport.
- **L'adoption se mesure** : **4** ouvertures le premier jour annonçaient l'abandon de la onzième
  semaine.

## 16. Évaluation formative

1. En une phrase, qu'est-ce qui distingue une mesure d'un indicateur ?
2. Citez trois choses que la BI n'est pas, et le coût mesuré de chacune.
3. Que vaut l'écart entre le CA net et le CA de toutes les lignes ? Exprimez-le deux fois.
4. Pourquoi **0,78** et **9,42** décrivent-ils le même stock ?
5. Que décide le mot « annulée » dans un taux de service ?
6. Qu'est-ce qu'une couche sémantique, et pourquoi aucun outil ne la remplace ?
7. Quelles sont les trois questions de cadrage, dans l'ordre ?
8. Quels sont les deux signaux d'échec les plus précoces, et comment les mesure-t-on ?
9. Pourquoi publie-t-on « CA perdu **estimé** » et pas « CA perdu » ?
10. Écrivez la fiche complète d'un indicateur de votre choix, en six lignes, sur le socle du module.

**Corrigé :** 1. Le KPI est *choisi* pour déclencher une décision, la mesure est *constatée*.
2. Graphique (les **41** indicateurs étaient lisibles), projet informatique (**2** définitions sans
arbitrage), rapport figé (maintenance résiliée, **1 200 000** FCFA/an). 3. **175 169 798** FCFA, soit
**1,12 %**. 4. La première divise par la **somme** des douze stocks, la seconde par leur **moyenne**
mensuelle. 5. Elle fait passer le taux de **81,0 %** (dénominateur : livrées) à **78,2 %**
(dénominateur : commandes). 6. L'endroit où les définitions sont écrites une fois ; aucun outil ne
choisit à votre place ce que « chiffre d'affaires » veut dire. 7. Quelle décision · qui décide et
quand · que fait-on si c'est rouge. 8. L'adoption (ouvertures par semaine) et les définitions
divergentes (**2** valeurs en réunion). 9. Parce que **169 386 812** FCFA vient d'une reconstitution
du rythme de vente, pas d'un enregistrement. 10. Réponse libre, notée sur la présence des six
rubriques : formule, source, granularité, fréquence, responsable, seuil + action + contre-KPI.
