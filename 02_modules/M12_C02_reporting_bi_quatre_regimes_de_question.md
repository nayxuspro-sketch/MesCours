# Module M12.C02 — Reporting, BI, et les quatre régimes de question

**Outils : DuckDB 1.5.5 (exécuté), pandas (contrôle croisé, exécuté), Excel (exécuté). Power BI
(cité, non exécuté — règle §1.5). Durée indicative : 5 h. Niveau : N3. Prérequis : M12.C01 (ce
qu'est la BI), M09 (questions métier), M11 (agrégats et fenêtres).**

> **L'idée du chapitre.** Un rapport périodique et un dispositif de BI ne diffèrent ni par l'outil,
> ni par le prix : ils diffèrent par **le type de question auquel ils répondent**. « Combien avons-nous
> vendu ? » se satisfait d'un rapport mensuel ; « pourquoi la marge baisse-t-elle ? » exige de
> l'exploration ; « que se passera-t-il en décembre ? » exige une projection — et une **erreur
> constatée** ; « qui relancer, et quand ? » exige une **file d'action**. Ce chapitre classe les
> quatre régimes, montre comment les reconnaître dans une demande, et mesure les quatre sur le socle
> plutôt que de les décrire.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **distinguer** reporting, BI, entrepôt de données, lac de données et service en autonomie — par ce qu'ils
   permettent de faire, et non par leur définition marketing ;
2. **classer** une demande dans l'un des **4** régimes de question (quoi, pourquoi, quoi demain, que
   faire) et en déduire la réponse technique **et** le rythme de publication ;
3. **reconnaître** les quatre propriétés d'un dispositif de BI — périodicité, exploration,
   interactivité, gouvernance — et dire laquelle manque à un rapport donné ;
4. **construire une projection honnête** sans modèle statistique, et **publier son erreur** plutôt que
   sa confiance : trois méthodes, mesurées sur **8** mois du socle ;
5. **transformer un constat en file d'action** : seuil, montant, liste, responsable — l'étape que
   **41** indicateurs du dossier du projet n'ont jamais franchie.

---

## 2. Pourquoi cette notion est importante

La confusion entre reporting et BI coûte cher d'une manière précise : elle fait **financer un rapport
périodique en croyant acheter un dispositif d'exploration**. Le dossier du projet raté en est
l'illustration exacte — **41** indicateurs répartis en **7** onglets, aucun d'eux explorable, et une
question de direction (« où perdons-nous de la marge ? ») qui n'a jamais reçu de réponse alors que
toutes les données nécessaires étaient présentes.

Une entreprise qui ne distingue pas les deux se retrouve avec un dispositif qui répond chaque mois à
la question de la semaine dernière, et reste muet sur celle du jour. Ce chapitre donne le critère de
tri : **quel régime de question votre demande occupe-t-elle ?** — et, selon la réponse, trois choses
changent : le rythme, le droit à l'erreur, et la personne à qui l'on s'adresse.

> **À retenir.** Le reporting **réduit** l'incertitude (que s'est-il passé ?) ; la BI **déplace** la
> question (pourquoi, et que faire ?). Un rapport qui ne réduit ni ne déplace n'occupe aucun des deux
> rôles : il décore.

---

## 3. Explication simple — la météo et le climat

Un bulletin météo et une étude climatique manipulent les mêmes données de température. Ils ne rendent
pas le même service.

Le **bulletin météo** paraît à heure fixe, répond toujours à la même question (« quel temps demain ? »),
se trompe parfois, et personne ne lui reproche de ne pas expliquer **pourquoi**. Il **réduit
l'incertitude de la journée**.

L'**étude climatique** ne paraît pas tous les matins ; elle explore, compare des zones, cherche des
tendances sur trente ans, et donne des **fourchettes**, pas des certitudes. Elle ne sert pas à sortir
le parapluie, elle sert à décider d'un investissement.

Un dispositif d'entreprise a besoin des deux, et meurt de les confondre : un rapport périodique qui
prétend expliquer devient illisible ; une exploration qui prétend donner une réponse quotidienne
devient inutile. Ce que le chapitre ajoute, c'est **le nom des régimes** et **la preuve chiffrée**
qu'on peut tirer de chacun sur le socle du module.

---

## 4. Vocabulaire essentiel

> **Définition.** Le **reporting** est la production périodique de résultats standardisés, à
> définition figée, destinés à être **lus** — tableau de bord mensuel, état des ventes, balance âgée.
> Son critère de réussite est la régularité et la comparabilité, pas l'explication.

> **Définition.** La **BI** (Business Intelligence) est l'ensemble des moyens qui permettent
> d'**explorer** les données pour répondre à des questions non prévues à l'avance, gouvernées par des
> définitions partagées. Son critère de réussite est le nombre de questions nouvelles qu'un
> responsable peut poser **sans demander un nouveau rapport**.

> **Définition.** Un **entrepôt de données** — *data warehouse* — est un stockage structuré,
> historisé et modélisé (M13), alimenté par les sources opérationnelles, dans lequel la BI vient lire.
> Un **lac de données** — *data lake* — conserve les fichiers bruts, souvent hétérogènes, sans schéma
> imposé : il stocke ce qu'on ne sait pas encore modéliser.

> **Définition.** Le **service en autonomie** — *self-service* — désigne le fait de laisser un utilisateur métier construire ses
> propres vues à partir d'une couche sémantique gouvernée. Il ne supprime pas la gouvernance : il la
> déplace vers les **définitions**, qu'il rend d'autant plus nécessaires.

> **Définition.** Les **quatre régimes de question** sont le descriptif (« que s'est-il passé ? »), le
> **diagnostique** (« pourquoi ? »), le **prédictif** (« que se passera-t-il ? ») et le **prescriptif**
> (« que faire ? »). Ce ne sont pas des niveaux de maturité : ce sont **quatre besoins différents**,
> qui coexistent dans la même entreprise le même jour.

---

## 5. Cours approfondi

### 5.1 Reporting et BI : ce qui les sépare vraiment

| Critère | Reporting | BI |
|---|---|---|
| Question de départ | figée à la conception | posée par l'utilisateur, dans l'instant |
| Forme de la réponse | tableau, courbe, chiffre unique | exploration, comparaison, puis décision |
| Rythme | périodique (jour, semaine, mois) | à la demande |
| Définition des indicateurs | implicite, dans le code du rapport | **écrite**, gouvernée (C04) |
| Coût dominant | la production et la distribution | la **matière** (sources, définitions) |
| Signe vital | paraît à l'heure | **est ouvert** et fait poser des questions |

Le tableau ci-dessus se lit dans les deux sens : un rapport mensuel peut être excellent, et un
dispositif de BI peut échouer. Ce qui les distingue n'est pas la modernité, c'est la **question
servie**.

### 5.2 Les quatre régimes, et la technique que chacun réclame

| Régime | Question type | Réponse technique | Le piège propre au régime |
|---|---|---|---|
| **Descriptif** — *quoi* | « combien, quand, où ? » | agrégats, filtres, séries (M07, M11) | croire que le chiffre répond à la question suivante |
| **Diagnostique** — *pourquoi* | « d'où vient cet écart ? » | comparaison, décomposition, drill-down | expliquer une corrélation et l'appeler cause |
| **Prédictif** — *quoi demain* | « que va-t-il se passer ? » | projection simple **déclarée**, saisonnalité | ne pas publier l'erreur de la méthode |
| **Prescriptif** — *que faire* | « qui, quand, à partir de quel seuil ? » | seuils, files d'action, priorisation | produire une alerte sans responsable |

> **Attention.** Un rapport qui **mélange** les quatre régimes dans un même écran fait exactement ce
> qu'a fait le dispositif abandonné : il affiche un « CA du jour » (descriptif), un « taux de rupture »
> (diagnostique en apparence), une « cible » (prédictive non dite) et un feu tricolore **sans action**
> (prescriptif vide). Quatre régimes, aucune réponse : les **14** destinataires ont cessé d'ouvrir.

### 5.3 Le régime descriptif, mesuré — la notion de tranche

Décrire, c'est choisir des **tranches** lisibles. Sur le socle, le même total se lit dans :

| Tranche | Nombre de tranches disponibles | Ce que la tranche permet de dire |
|---|---|---|
| Mois | **44** | la saison, la tendance longue |
| Magasin × mois | **220** | quel point de vente décroche, et quand |
| Magasin × mois × famille | **3 515** cellules | quelle famille décroche, et où |
| Produits | **154** produits servis | quelle référence porte le mouvement |

Le premier chiffre du module, **15 595 154 955** FCFA, est un total ; les tranches ci-dessus sont ce
qui le rend **exploitable**. Un rapport figé n'affiche qu'une tranche — et c'est là toute sa limite,
pas dans son outil.

### 5.4 Le rythme fait partie de l'indicateur

Le socle montre à quel point la **périodicité** change la lecture d'un même chiffre :

- le **lundi** pèse **2 663 495 054** FCFA de chiffre d'affaires, le **dimanche** **829 983 276** —
  un rapport hebdomadaire publié le dimanche soir compare donc le meilleur jour de la semaine au pire,
  chaque semaine ;
- **17,8 %** du chiffre d'affaires d'un mois est réalisé après le **25** : un rapport mensuel publié le
  1ᵉʳ du mois suivant, avec les données arrêtées au 25, manque près d'un cinquième de l'activité — et
  ne le dit jamais ;
- la première tranche temporelle du socle (**284 400 304** FCFA en janvier 2023) et la dernière
  (**368 251 515** FCFA en août 2026) ne se comparent que parce que la **même** tranche est utilisée
  des deux côtés.

**La règle** : la périodicité d'un rapport est une **définition** — elle aussi — et elle s'écrit dans
son en-tête, au même titre que le périmètre.

> **Attention.** Un rapport est arrêté à une date, et cette date n'est pas la fin du mois. Sans la
> mention « données arrêtées au 25 », les **17,8 %** d'activité réalisée après le 25 disparaissent de
> la lecture — et avec eux, la comparabilité d'un mois à l'autre.

### 5.5 Le régime diagnostique : relier un écart à une cause mesurée

Diagnostiquer n'est pas commenter. Le socle en donne un cas net : la marge brute ressort à **29,12 %**
alors que le référentiel annonce des cibles de **18** à **24 %** par rayon.

Trois explications possibles, toutes vérifiables :

1. « nous vendons mieux » — à écarter : aucune décision commerciale n'a changé dans le socle ;
2. « nos coûts d'achat ont baissé » — à écarter : le coût standard est **figé** dans le référentiel ;
3. « nos prix de vente ont monté plus vite que le référentiel ne le dit » — **vérifiée** : entre 2023
   et 2026, le prix unitaire moyen des ventes est passé de **8 219** à **10 271** FCFA, soit
   **25,0 %**, quand le référentiel porte un prix unique.

Le diagnostic tient en une phrase vérifiable. C'est ce qui le distingue d'un commentaire — et c'est ce
que le projet M12.P vous demandera de produire pour **10** indicateurs.

### 5.6 Le régime prédictif sans modèle : trois projections, une erreur publiée

Beaucoup de projets appellent « prédictif » ce qui n'est qu'une **reconduction**. Le module assume
l'inverse : une projection **simple**, **déclarée**, avec son erreur **constatée**, vaut mieux qu'un
modèle que personne ne peut auditer. Trois méthodes, testées sur les **8** mois de 2026 du socle :

| Méthode | Règle | Erreur moyenne constatée (MAPE) |
|---|---|---|
| Reconduire le mois précédent | « décembre vaudra novembre » | **12,2 %** |
| Reconduire l'an dernier | « décembre vaudra décembre N-1 » | **13,5 %** |
| Moyenne des 12 derniers mois | « chaque mois vaut la moyenne » | **14,3 %** |

Trois enseignements, tous contre-intuitifs :

1. la méthode **la plus simple gagne** sur cette série — la saisonnalité du socle n'est pas assez
   régulière pour battre la simple reconduction ;
2. aucune méthode ne descend sous **12 %** d'erreur : un dispositif qui promet « la prévision du mois »
   à 3 % près doit **prouver** sa méthode, sinon il vend une croyance ;
3. l'erreur se **publie** avec la prévision : « 368 251 515 FCFA ± 12 % » n'est pas la même phrase que
   « 368 251 515 FCFA ».

### 5.7 Le régime prescriptif : transformer un constat en file d'action

Le socle fournit **1 202 550 590** FCFA d'encours ouvert. Ce chiffre est descriptif. Ce qui en fait une
prescription, c'est la **balance âgée** et la **file** qu'elle dessine :

| Tranche d'ancienneté | Factures | Montant | Ce qu'on en fait |
|---|---|---|---|
| 0 à 30 jours | **71** | **70 049 670** FCFA | rien : c'est le délai normal |
| 31 à 60 jours | **30** | **26 248 320** FCFA | rappel automatique |
| 61 à 90 jours | **16** | **14 913 570** FCFA | appel du commercial |
| **plus de 90 jours** | **1 155** | **1 091 339 030** FCFA | **contentieux / plan d'apurement** |

La file prescriptive est la dernière ligne : **1 155** factures, **1 091 339 030** FCFA, soit **90,8 %**
de l'encours ouvert. Et la mesure qui la rend exécutable existe déjà dans le socle : parmi les factures
payées **en retard**, **1 068** l'ont été avec un retard **médian de 5 jours**. Autrement dit, le retard
« normal » se règle en une semaine ; ce qui reste au-delà de **90** jours n'est plus un retard, c'est
un **impayé** — et c'est un autre métier, avec un autre responsable.

> **Dans les faits.** L'atelier du manuel applique la même règle à ses propres mesures : la balance
> âgée ci-dessus est recalculée à chaque relevé par `tools/kpi_M12.py`, et ses quatre tranches
> s'additionnent exactement à l'encours ouvert du module (**1 202 550 590** FCFA). Une répartition dont
> les tranches ne retombent pas sur le total est le premier signe d'un indicateur mal découpé.

### 5.8 Périodicité, exploration, interactivité, gouvernance : les quatre propriétés

| Propriété | La question qu'elle règle | Ce qui la mesure | Où elle a manqué au projet |
|---|---|---|---|
| **Périodicité** | à quelle fréquence, avec quel délai ? | date de publication vs date des données | aucune fréquence annoncée par indicateur |
| **Exploration** | peut-on descendre d'un total à sa cause ? | nombre de tranches accessibles sans nouvelle demande | **7** onglets figés, aucune descente |
| **Interactivité** | qui peut filtrer quoi, et à quel coût ? | temps de réponse et droits d'accès | filtres présents, **mais** définitions non filtrées |
| **Gouvernance** | qui décide de la définition, et où est-elle écrite ? | existence d'une carte de définition | **2** versions du CA, **3** sources discordantes |

Les quatre propriétés se lisent dans cet ordre, et la dernière **conditionne** les trois premières :
une exploration rapide sur des définitions flottantes produit des décisions rapides et fausses.

### 5.9 Ce que ce chapitre ne couvre pas

Les **critères de fabrication** d'un indicateur (les six critères, la carte de définition, le
contre-KPI) sont le chapitre C04 ; la **couche sémantique** et l'architecture complète sont le C05 ;
la **conduite** d'un projet d'exploration — adoption, formation, maintenance — est le C06 ; les
méthodes de prévision proprement dites, avec leur validation, appartiennent à M19. Ce chapitre-ci ne
promet aucune prédiction : il apprend à **ranger les questions** et à refuser celles qu'on ne peut pas
servir honnêtement.

---

## 6. Exemple concret — la même demande, quatre réponses

Un directeur régional écrit : « Je veux savoir où nous perdons de l'argent. »

**Régime descriptif.** On lui livre la marge par magasin et par famille : **29,12 %** au global, et les
tranches qui baissent. Il sait **où** — il ne sait pas **pourquoi**.

**Régime diagnostique.** On décompose l'écart : prix de vente (**+25,0 %** de 2023 à 2026), coût
standard figé, remises par famille, et l'effet des **2** produits sans prix au référentiel. La réponse
tient en une phrase, et elle nomme une **cause** : l'écart vient des prix, pas d'une dérive de coût.

**Régime prédictif.** On projette la marge des trois prochains mois avec la méthode la plus simple,
**12,2 %** d'erreur annoncée. Le directeur sait ce qu'il peut en faire : anticiper une tendance, pas
décider un investissement.

**Régime prescriptif.** On livre la file d'action : les familles à marge basse **et** à volume élevé,
triées par montant, avec un seuil (« en dessous de **20 %** de marge sur plus de **500 000** FCFA
mensuels »), un responsable (chef de rayon) et un délai (revue d'assortiment du mois).

**La leçon.** La demande initiale était floue ; elle contenait les quatre régimes. Un analyste qui
répond aux quatre d'un coup produit un écran illisible ; un analyste qui refuse les trois premiers
pour ne servir que le quatrième produit une décision. **L'ordre de service est un choix
professionnel**, et c'est le cœur de ce chapitre.

---

## 7. Démonstration pas à pas — quatre régimes sur le socle

Tout se rejoue avec `03_exercices/dossier_M12/connexion.py`.

### 7.1 Étape 1 — descriptif : le total, puis les tranches

```sql
SELECT strftime(date_vente, '%Y-%m') AS mois, ROUND(SUM(montant_ttc)) AS ca
FROM ventes WHERE est_retour = 0 GROUP BY 1 ORDER BY 1;
```

**44** lignes, de **284 400 304** FCFA (janvier 2023) à **368 251 515** FCFA (août 2026). Un total
unique (**15 595 154 955** FCFA) ne décide rien ; la série, elle, commence à parler.

### 7.2 Étape 2 — descriptif fin : la tranche qui change la lecture

```sql
SELECT strftime(date_vente, '%w') AS jour, ROUND(SUM(montant_ttc)) AS ca
FROM ventes WHERE est_retour = 0 GROUP BY 1 ORDER BY 1;
```

Lundi **2 663 495 054** FCFA, dimanche **829 983 276** FCFA : un rapport hebdomadaire « semaine du
dimanche au samedi » et un rapport « du lundi au dimanche » ne racontent pas la même histoire, avec
**× 3,21** d'écart entre le meilleur et le pire jour.

### 7.3 Étape 3 — diagnostique : de l'écart à la cause

```sql
SELECT year(date_vente) AS annee, ROUND(AVG(prix_unitaire_ht)) AS prix_moyen
FROM ventes WHERE est_retour = 0 GROUP BY 1 ORDER BY 1;
```

La hausse de **8 219** à **10 271** FCFA (**+25,0 %**) explique la marge apparente de **29,12 %**
face à une cible de **18** à **24 %**. Le diagnostic s'arrête quand la cause est **mesurée**, pas quand
elle est plausible.

### 7.4 Étape 4 — prédictif : trois méthodes, une erreur publiée

| Méthode | Règle appliquée à septembre 2026 | Erreur constatée sur 2026 |
|---|---|---|
| Reconduction du mois précédent | août **368 251 515** FCFA | **12,2 %** |
| Reconduction de l'an dernier | septembre 2025 | **13,5 %** |
| Moyenne des 12 derniers mois | moyenne glissante | **14,3 %** |

On publie la projection **avec** son erreur : c'est la seule façon d'être honnête sans modèle.

### 7.5 Étape 5 — prescriptif : la file, pas l'alerte

```sql
SELECT CASE WHEN date_diff('day', date_echeance, DATE '2026-08-31') <= 30 THEN '0-30 j'
            WHEN date_diff('day', date_echeance, DATE '2026-08-31') <= 60 THEN '31-60 j'
            WHEN date_diff('day', date_echeance, DATE '2026-08-31') <= 90 THEN '61-90 j'
            ELSE 'plus de 90 j' END AS tranche,
       COUNT(*) AS factures, ROUND(SUM(montant_ttc)) AS montant
FROM encaissement WHERE date_encaissement IS NULL GROUP BY 1 ORDER BY 1;
```

Quatre lignes, dont la dernière porte **1 155** factures et **1 091 339 030** FCFA : la file de
contentieux, **90,8 %** de l'encours. C'est une **liste de travail**, pas une alerte.

### 7.6 Étape 6 — l'arbitrage entre régimes

| Demande reçue | Régime | Livrable | Délai |
|---|---|---|---|
| « le CA du mois » | descriptif | rapport périodique | automatique |
| « d'où vient la baisse de marge ? » | diagnostique | note d'une page, cause mesurée | quelques jours |
| « la prévision de décembre » | prédictif | fourchette ± erreur publiée | quelques jours |
| « que fait-on des impayés ? » | prescriptif | file de relance priorisée | un jour |

Ce tableau est ce que le module appelle **un catalogue de services** : il dit à l'entreprise ce qu'elle
peut demander, et à quel prix en délai. Il remplace avantageusement une liste de **41** indicateurs.

---

## 8. Erreurs fréquentes

1. **Appeler « BI » un rapport périodique.** Le critère est l'exploration, pas le nom.
2. **Promettre du prédictif sans publier l'erreur.** Sur ce socle, la meilleure méthode simple se
   trompe de **12,2 %**.
3. **Confondre corrélation et cause** dans le diagnostic : la marge monte **et** les prix montent —
   c'est la seconde qui explique la première, et les deux sont mesurées.
4. **Publier une alerte sans responsable.** Le dossier du projet contient **41** seuils, **0** action.
5. **Ignorer la périodicité des données.** **17,8 %** du mois se réalise après le **25**.
6. **Comparer deux tranches de tailles différentes** : lundi contre dimanche, **× 3,21**.
7. **Confondre lac et entrepôt.** Stocker brut ne dispense pas de définir — cela déplace seulement le
   travail plus loin.
8. **Croire que le service en autonomie supprime la gouvernance.** Il l'exige : sans définitions, il produit
   **2** versions de chaque chiffre, à la vitesse de l'utilisateur.
9. **Répondre aux quatre régimes dans un même écran.** Sept onglets, quatre besoins, aucune réponse.
10. **Oublier de dater les données.** Un bulletin sans date n'est pas un bulletin.

---

## 9. Bonnes pratiques professionnelles

- **Trier la demande avant de l'instruire.** Une question = un régime = un livrable = un délai.
- **Publier une fourchette, jamais une promesse.** Une projection s'écrit « ± **12 %** », pas « exacte ».
- **Mesurer la cause avant de la nommer**, et s'arrêter quand elle est mesurée.
- **Transformer tout constat chiffré en file d'action** : seuil, montant, liste, responsable, délai.
- **Dater les tranches** et écrire la périodicité dans l'en-tête du rapport.

> **Conseil professionnel.** Quand une direction demande « un tableau de bord avec tout », répondez par
> le tableau des quatre régimes du §7.6 : il montre que « tout » signifie quatre livrables différents,
> dont trois ne sont pas des écrans. C'est la réponse qui a manqué au prestataire du dossier — et qui
> lui a coûté **7 940 000** FCFA de dispositif abandonné.

---

## 10. Exercice guidé

**Énoncé.** Classez ces quatre demandes dans les régimes, et dites pour chacune ce que vous livrez :
(a) « combien de ruptures cette semaine ? » ; (b) « pourquoi Kaya rompt-il plus que les autres ? » ;
(c) « allons-nous rompre la semaine prochaine ? » ; (d) « quelles références faut-il réapprovisionner
en priorité ? ».

**Étape 1 — classer.** (a) descriptif, (b) diagnostique, (c) prédictif, (d) prescriptif.

**Étape 2 — chiffrer le contexte.** Le socle compte **2 428** ruptures sur **33 296** couples servis
(**7,29 %**), **13 129** jours de rupture et **169 386 812** FCFA **estimés** de chiffre d'affaires
perdu.

**Étape 3 — choisir le livrable.** (a) un rapport hebdomadaire ; (b) une note comparant Kaya aux
autres magasins, par famille et par rotation ; (c) une projection **avec** son erreur publiée ;
(d) une file triée par couple (jours × rotation), avec un seuil et un responsable.

**Étape 4 — nommer la limite.** Pour (c), rappelez que la meilleure projection simple du socle se
trompe de **12,2 %** : la file de (d) vaut mieux qu'une prévision trop fine.

---

## 11. Exercices autonomes

1. **Tranches.** Combien de cellules magasin-mois-famille le socle permet-il (**3 515**), et combien
   de questions vos tableaux de suivi habituels en rendent-ils accessibles sans travail manuel ?
2. **Périodicité.** Un rapport mensuel est arrêté au **25**. Quelle part de l'activité manque-t-il, et
   comment l'écrire dans son en-tête ?
3. **Diagnostic guidé.** La marge ressort à **29,12 %** pour une cible de **18** à **24 %** : proposez
   trois causes possibles, puis écartez-en deux par la mesure.
4. **Prévision honnête.** Choisissez un mois de 2026 et appliquez les trois méthodes du §5.6 ;
   publiez votre erreur en pourcentage.
5. **File d'action.** Construisez la balance âgée des **9 000** factures, puis écrivez la file de
   relance avec seuil, montant, responsable et délai.
6. **Le régime oublié.** Reprenez les **7** onglets du dossier du projet et dites, pour chacun, le
   régime qu'il prétend servir et celui qu'il sert réellement.

---

## 12. Correction détaillée

**Exercice 1.** **3 515** cellules (magasin × mois × famille) contre **220** couples magasin-mois :
la même donnée multiplie par seize le nombre de questions accessibles. Un rapport figé en ouvre une.

**Exercice 2.** **17,8 %** du chiffre d'affaires mensuel se réalise après le **25**. L'en-tête attendu :
« données arrêtées au 25 du mois, soit environ **82 %** du mois ; le complément est intégré au rapport
du mois suivant. »

**Exercice 3.** Causes plausibles : (1) hausse des prix de vente, (2) baisse des coûts d'achat,
(3) erreur de calcul. On écarte (2) — le coût standard est **figé** — et (3) — le contrôle croisé
côté pandas retrouve **15 595 154 955** FCFA. Reste (1), mesurée : **8 219** → **10 271** FCFA
(**+25,0 %**).

**Exercice 4.** Exemple sur août 2026 : reconduction du mois précédent (juillet) ; reconduction d'août
2025 ; moyenne des douze derniers mois. L'erreur publiée doit être celle de la méthode, mesurée sur
**8** mois : **12,2 %**, **13,5 %** ou **14,3 %** selon la méthode choisie.

**Exercice 5.** Balance âgée : **71** factures (**70 049 670** FCFA) en 0-30 jours, **30**
(**26 248 320**) en 31-60, **16** (**14 913 570**) en 61-90, **1 155** (**1 091 339 030**) au-delà de
90 jours. File de relance : les **1 155** factures de plus de 90 jours (**90,8 %** de l'encours),
responsable : responsable recouvrement, délai : revue hebdomadaire du lundi.

**Exercice 6.** Attendu, onglet par onglet : « Activité » sert le descriptif ; « Écarts » prétend le
prescriptif mais n'a pas d'action ; « Ruptures » prétend le diagnostique mais ne montre que des
comptages ; « Livraisons » et « Encaissements » servent le descriptif ; « Logistique » sert le
descriptif ; le tableau de bord, dans son ensemble, **ne sert aucun des quatre régimes** : il les
juxtapose.

---

## 13. Mini-projet de chapitre

**« Le catalogue de services d'un analyste »** (2 h). Produisez, pour une entreprise que vous
connaissez, une page qui contient : (1) les **8** questions les plus souvent posées, classées par
régime ; (2) pour chacune, le livrable, le délai et le responsable ; (3) les **3** questions auxquelles
vous refusez de répondre, et pourquoi (méthode indisponible, donnée absente, définition non
gouvernée) ; (4) la question de direction que votre catalogue ne sert pas encore, et le moyen de la
servir. Règle de notation : chaque affirmation chiffrée, chaque refus argumenté.

---

## 14. Résumé du chapitre

| Notion | Ce qu'il faut retenir |
|---|---|
| Reporting vs BI | la question servie, pas l'outil : figée et périodique contre exploratoire et gouvernée |
| Les 4 régimes | descriptif (quoi), diagnostique (pourquoi), prédictif (quoi demain), prescriptif (que faire) |
| Descriptif | **44** mois, **220** couples magasin-mois, **3 515** cellules : la tranche fait la valeur |
| Diagnostique | **29,12 %** de marge pour une cible de **18** à **24 %** : la cause mesurée est le prix (**+25,0 %**) |
| Prédictif | trois méthodes simples, erreurs **12,2 %**, **13,5 %**, **14,3 %** : on publie l'erreur |
| Prescriptif | **1 155** factures de plus de 90 jours, **1 091 339 030** FCFA, **90,8 %** de l'encours |
| Les 4 propriétés | périodicité, exploration, interactivité, gouvernance — la dernière conditionne les autres |

## 15. À retenir

> **À retenir.** Un rapport qui répond à une question qu'on ne se pose plus est un coût ; un dispositif
> qui répond à quatre régimes à la fois est un brouillard. Le travail de l'analyste commence par le
> **tri** de la demande.

- **La périodicité est une définition** : données arrêtées au **25**, c'est **17,8 %** de mois absent.
- **Une prévision sans erreur publiée n'est pas une prévision**, c'est une opinion — ici **12,2 %**
  au mieux.
- **Une alerte sans file d'action est un ornement** : le dossier du projet en aligne **41**.
- **Comprendre n'est pas décrire** : le diagnostic s'arrête quand la cause est **mesurée**.

## 16. Évaluation formative

1. Citez deux différences de fond entre reporting et BI, autres que l'outil.
2. Nommez les quatre régimes et la question type de chacun.
3. Que signifie « tranche » en descriptif, et combien le socle en offre-t-il (magasin × mois × famille) ?
4. Pourquoi la périodicité d'arrêt des données doit-elle figurer dans l'en-tête d'un rapport ?
5. Quelle est la cause mesurée du taux de marge apparent de **29,12 %** ?
6. Quelle méthode de projection se trompe le moins sur ce socle, et de combien ?
7. Qu'est-ce qu'une file d'action, et qu'est-ce qui la distingue d'une alerte ?
8. Quel est le montant de l'encours de plus de 90 jours, et sa part dans l'encours total ?
9. Pourquoi le service en autonomie rend-il la gouvernance **plus** nécessaire ?
10. Parmi les quatre propriétés du §5.8, laquelle conditionne les trois autres, et pourquoi ?

**Corrigé :** 1. La définition des indicateurs (implicite contre écrite) et le signe vital (paraître à
l'heure contre être ouvert). 2. Descriptif (« que s'est-il passé ? »), diagnostique (« pourquoi ? »),
prédictif (« que se passera-t-il ? »), prescriptif (« que faire ? »). 3. Une découpe lisible des
données ; **3 515** cellules. 4. Parce que **17,8 %** du mois se réalise après le **25** : sans cette
mention, le lecteur croit lire le mois entier. 5. La hausse des prix de vente unitaires, de **8 219** à
**10 271** FCFA (**+25,0 %**) entre 2023 et 2026, pour un coût standard figé. 6. La reconduction du
mois précédent, avec **12,2 %** d'erreur moyenne sur **8** mois. 7. Une liste de travail priorisée avec
seuil, montant, responsable et délai ; l'alerte ne dit pas qui agit. 8. **1 091 339 030** FCFA de
**1 202 550 590**, soit **90,8 %**. 9. Parce qu'il multiplie les producteurs de chiffres : sans
définitions écrites, chacun obtient la sienne. 10. La gouvernance : elle fixe le sens des chiffres que
les trois autres propriétés diffusent.
