# Module M12.C06 — Réussir le projet BI

**Outils : DuckDB 1.5.5 (exécuté), pandas (exécuté), Excel (exécuté). Power BI (cité, non exécuté —
règle §1.5). Durée indicative : 5 h. Niveau : N3. Prérequis : M12.C01—C05.**

> **L'idée du chapitre.** Un projet BI ne réussit pas parce que les chiffres sont justes : il réussit
> parce que quelqu'un **décide** avec lui. Ce chapitre referme le module en partant de l'échec — le
> dossier du projet raté — pour en tirer **10** causes vérifiables, une méthode de conduite, un cahier
> des charges utile et une recette de réception. Les chiffres qui l'accompagnent sont ceux du dossier :
> **7 940 000** FCFA dépensés pour **41** indicateurs, **4** lecteurs sur **14**, **11** semaines de vie
> — et, en face, les **10** cartes du mandat de reprise.

![Les dix couples indicateur / contre-KPI du mandat de reprise, chacun avec sa mesure (production : `tools/figures_M12.py`)](../figures/M12_C06_matrice_des_dix_couples.svg)

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **citer les dix causes d'échec** d'un projet décisionnel et **reconnaître chacune** dans le dossier du
   projet raté, avec sa mesure ;
2. **distinguer les parties prenantes** : qui commande, qui lit, qui défend, qui maintient — et pourquoi
   l'absence du dernier rôle tue le dispositif ;
3. **rédiger un cahier des charges utile**, en posant les **6** questions que le prestataire du dossier
   n'a jamais posées, et en plafonnant le nombre d'indicateurs ;
4. **conduire un projet** par étapes mesurables : sources, définitions, écran, formation, recette, revue
   d'usage ;
5. **mesurer l'adoption** comme on mesure la livraison : destinataires, ouvertures, décisions, coût par
   lecteur (**1 985 000** FCFA dans le dossier raté) ;
6. **organiser la maintenance et la gouvernance** : un budget par an (**1 200 000** FCFA), un
   responsable par indicateur, une revue qui retire ce qui n'est plus lu.

---

## 2. Pourquoi cette notion est importante

Un projet décisionnel échoue rarement par erreur de calcul. Il échoue parce que personne ne s'en sert.
Le dossier du projet raté en donne la décomposition exacte, et chaque ligne est un chiffre mesurable :

| Ce qui a été livré | Ce qui s'est passé | Le chiffre |
|---|---|---|
| **41** indicateurs sur **7** onglets | personne ne sait lesquels comptent | **10** KPI demandés à la reprise |
| une commande floue, acceptée sans discussion | **6** questions jamais posées | — |
| **3** sources discordantes, **2** débats non tranchés | le CA a deux valeurs, la marge aussi | **2 809** lignes de retour en cause |
| **14** destinataires | **4** ouvrent le premier jour | **28,6 %** |
| **1** heure de formation, **12** participants | la moyenne d'ouvertures tombe de **6** à **3** | en une semaine |
| **1 200 000** FCFA de maintenance par an | contrat résilié | au bout de **11** semaines |
| **22** jours sur l'écran, **8** sur les sources | la question de la direction reste sans réponse | « où perdons-nous de la marge ? » |

Le mandat de reprise tient donc en deux exigences, et ce chapitre les traite : **au plus 10 indicateurs**,
chacun avec sa carte — et **une réponse** à la seule question qui compte : *que fait-on quand c'est
rouge ?*

> **À retenir.** La réussite d'un dispositif décisionnel se mesure à l'extérieur de lui : au nombre de
> décisions qu'il déclenche. Un dispositif lu par **4** personnes sur **14** n'est pas un échec technique :
> c'est un échec de **projet** — commande, conduite, formation et maintenance.

---

## 3. Explication simple — la maison et ses habitants

Un projet BI ressemble à une maison construite pour un client qu'on n'a jamais questionné sur sa façon de
vivre. On peut livrer de beaux murs, une plomberie impeccable : si la famille entre par la porte de
service et fait la cuisine dans le salon, la maison est ratée — et ce n'est pas la faute du maçon.

Quatre questions séparent une maison ratée d'une maison habitée :

- **Qui va y vivre ?** — les destinataires, avec leur rôle et leur niveau de lecture.
- **Qu'y fera-t-on ?** — les décisions, pas les fonctions : commander, relancer, arbitrer.
- **Quand ?** — la fréquence réelle de ces décisions, jour, semaine, mois.
- **Qui s'en occupe ?** — celui qui répare la fuite, c'est-à-dire le responsable de la maintenance.

Le dossier du projet raté a répondu aux quatre à l'envers : des destinataires définis par une liste
d'adresses, des indicateurs définis par ce qui était calculable, une fréquence quotidienne pour tout, et
aucun responsable.

---

## 4. Vocabulaire essentiel

> **Définition.** Un **cahier des charges** est l'écrit qui fixe, avant le début des travaux, les
> décisions à éclairer, les destinataires, la fréquence, les définitions attendues, les critères de
> réception et le budget de maintenance. Un cahier des charges sans critère de réception n'engage que le
> client.

> **Définition.** Le **commanditaire** — *sponsor* — est la personne qui finance le dispositif, le
> défend dans l'organisation et arbitre les désaccords. Sans commanditaire identifié, le premier débat de
> définition fait tomber le projet.

> **Définition.** Une **partie prenante** est toute personne qui influe sur le projet ou le subit :
> destinataires, producteurs de données, informaticiens, comptables, contrôleurs. Chacune a besoin d'un
> rôle écrit : qui décide, qui valide, qui consulte.

> **Définition.** La **recette** — *réception* — est l'étape où le commanditaire vérifie le dispositif
> contre les critères du cahier des charges : chaque indicateur existe, sa valeur est reproductible, sa
> définition est publiée, son responsable est nommé, son seuil déclenche une action.

> **Définition.** La **maintenance** couvre deux activités distinctes : la **maintenance corrective**, qui
> répare (**1 200 000** FCFA par an dans le dossier raté, soit **23 077** FCFA par semaine), et la
> **maintenance évolutive**, qui retire ce qui n'est plus lu et ajoute ce qui manque.

---

## 5. Cours approfondi

### 5.1 Les dix causes d'échec, toutes visibles dans le dossier

| # | Cause d'échec | Le symptôme mesuré | Détectée **avant** la livraison par |
|---|---|---|---|
| 1 | **Commande floue** | « il doit contenir tout » : **41** indicateurs, **7** onglets | la question « quelles **10** décisions voulez-vous éclairer ? » |
| 2 | **Aucun commanditaire actif** | **6** questions jamais posées, dont « qui décide avec ce chiffre ? » | le nom de la personne qui arbitre en réunion |
| 3 | **Sources non fiables ou non documentées** | **3** sources discordantes, **2** débats non tranchés | la liste des cas particuliers par source, écrite |
| 4 | **Définitions non écrites** | deux CA, deux marges : **29,12 %** ou **24,67 %** | la carte de définition remplie avant l'écran |
| 5 | **Trop d'indicateurs** | **41** indicateurs, **10** souhaitables | le plafond inscrit au cahier des charges |
| 6 | **Aucun responsable par indicateur** | personne ne tranche les **2** questions | **10** noms sur **10** cartes |
| 7 | **Aucun seuil relié à une action** | « que fait-on si la rupture dépasse le seuil ? » resté sans réponse | la colonne « action si rouge » remplie |
| 8 | **Adoption supposée** | **4** ouvertures sur **14** destinataires, puis **6** puis **3** par jour | la mesure d'usage à J+7 et J+30, et une formation **avant** la mise en ligne |
| 9 | **Maintenance non financée ou non attribuée** | **1 200 000** FCFA/an, contrat résilié en **11** semaines | le responsable de maintenance nommé, avec son budget de **23 077** FCFA par semaine |
| 10 | **Écran construit avant la couche sémantique** | **22** jours sur l'écran, **8** sur les sources | l'ordre d'exécution inscrit au planning |

**Ces dix causes ne sont pas indépendantes** : les causes 1, 2 et 6 sont un même problème — le projet a
été traité comme une commande de logiciel au lieu d'un projet de **décision**. Les autres en découlent.

> **Attention.** Aucune de ces causes ne se voit à la livraison. Le jour de la mise en ligne, les **41**
> indicateurs s'affichent, les totaux tombent juste et le prestataire est payé : le défaut n'apparaîtra
> qu'à la première réunion où deux chiffres se contrediront, ou à la deuxième semaine où les ouvertures
> tomberont de **6** à **3**. Une recette qui se limite à « est-ce que ça s'affiche ? » ne détecte
> aucune des dix.

### 5.2 Les parties prenantes et leurs rôles

Quatre rôles, et le dossier raté permet de voir ce qui arrive quand l'un manque :

| Rôle | Ce qu'il fait | Dans le dossier raté | Conséquence |
|---|---|---|---|
| **Commanditaire** | finance, défend, arbitre | absent au moment des **2** débats | chaque service garde son chiffre |
| **Producteur de données** | tient la source et ses règles | **8** jours sur **30**, sans documentation publiée | les défauts remontent **11** semaines plus tard |
| **Destinataire** | décide avec l'indicateur | **14** personnes, dont **4** lecteurs le premier jour | l'usage ne vient pas |
| **Responsable de maintenance** | corrige, retire, complète | non nommé, contrat résilié | le dispositif meurt de ses sources |

La règle qui en découle tient en une ligne : **chaque rôle a un nom avant le premier jour de
développement**, pas à la livraison.

### 5.3 Le cahier des charges utile, en six questions

Le dossier du projet raté liste lui-même les **6** questions que le prestataire n'a jamais posées. Elles
forment le squelette d'un cahier des charges :

1. Qui décide avec ce chiffre, et **quand** ?
2. Que fera-t-on **différemment** si le chiffre est mauvais ?
3. Quelle est **déjà** la réponse des gens à cette question, et où la lisent-ils aujourd'hui ?
4. Qui est **responsable** de la définition de chaque indicateur ?
5. Combien de temps par jour le lecteur accepte-t-il d'y consacrer ?
6. Que se passe-t-il le **8** du mois, quand la donnée arrive en retard ?

À ces six questions, la reprise ajoute trois plafonds mesurables : **10** indicateurs au maximum, **7**
champs par carte, et **une** action par seuil. Trois plafonds, et le projet devient vérifiable.

### 5.4 La conduite : l'ordre des étapes fait le projet

Le dossier raté a exécuté le projet dans l'ordre inverse de la chaîne des sept étages (C05) : écran
d'abord, définitions jamais. La conduite recommandée inverse la dépense :

| Étape | Livrable | Le dossier raté | La reprise |
|---|---|---|---|
| 1. Cadrage | **6** questions, liste des décisions, plafond d'indicateurs | absent | **1** page signée |
| 2. Sources | cas particuliers documentés, règles d'extraction | **8** jours, non publiés | **8** jours, publiés |
| 3. Définitions | **10** cartes, **70** cases | absent | **6** jours |
| 4. Calcul | socle rejouable, contrôle de grain | non rejouable | **0,70** s de reconstruction |
| 5. Écran | **10** indicateurs, **1** page | **22** jours, **7** onglets | **3** jours |
| 6. Formation et recette | usage mesuré à J+7 et J+30 | **1** heure, **12** participants | **1** heure **avant** la mise en ligne |
| 7. Revue d'usage | retrait de ce qui n'est pas lu | jamais | trimestrielle, avec le commanditaire |

### 5.5 L'adoption : la mesurer pour la piloter

L'adoption est une grandeur, pas une impression : le dossier du projet raté permet de la calculer
entièrement.

| Indicateur d'adoption | Valeur du dossier raté | Lecture |
|---|---|---|
| destinataires | **14** | la cible n'est pas « tout le monde », c'est ceux qui décident |
| lecteurs le premier jour | **4** (**28,6 %**) | un dispositif qui démarre sous un tiers des destinataires ne démarre pas |
| moyenne quotidienne, semaine 1 | **6** | l'intérêt initial existe |
| moyenne quotidienne, semaine 2 | **3** | il divise par deux en une semaine : c'est le signal d'alarme |
| coût par lecteur du premier jour | **1 985 000** FCFA | le prix réel d'un écran sans formation |
| durée de vie | **11** semaines | pour **7 940 000** FCFA engagés |

**La seule mesure qui compte** est la dernière colonne : ce que l'usage a coûté. Un dispositif peu
coûteux et très lu est une réussite ; un dispositif cher et peu lu est un échec, quels que soient la
qualité des chiffres.

> **Attention.** Un indicateur d'adoption ne se mesure pas une fois, à la livraison, mais **deux fois** :
> à J+7 et à J+30. Le dossier raté aurait été sauvé par cette seule discipline — la chute de **6** à
> **3** ouvertures quotidiennes était visible dès la deuxième semaine, alors qu'il restait **9** semaines
> de maintenance à décider.

### 5.6 La maintenance et la gouvernance

Un dispositif décisionnel se dégrade : les sources changent, les rôles bougent, les questions évoluent.
Trois règles suffisent à tenir :

1. **Un responsable par indicateur**, nommé sur la carte (C04). C'est lui qui signale la donnée en retard
   le **8** du mois.
2. **Un budget de maintenance annuel**, avec son ordre de grandeur : **1 200 000** FCFA par an dans le
   dossier raté, soit **23 077** FCFA par semaine — un montant modeste, et un contrat pourtant résilié
   faute d'usage.
3. **Une revue trimestrielle d'usage** : on regarde ce qui est lu, on **retire** ce qui ne l'est pas, on
   ajoute une question si elle revient trois fois en réunion. Un dispositif qui ne retire jamais rien
   finit à **41** indicateurs.

### 5.7 L'économie réelle d'un projet décisionnel

Ramener le budget au livrable et à l'usage change la lecture d'un projet :

| Rapport | Valeur | Ce qu'il dit |
|---|---|---|
| budget ÷ indicateurs livrés | **193 659** FCFA par indicateur | **41** indicateurs à ce prix : la production n'était pas le problème |
| budget ÷ KPI du mandat | **794 000** FCFA par KPI | le même budget, bien ciblé, finance **10** indicateurs complets |
| budget ÷ lecteurs du 1er jour | **1 985 000** FCFA par lecteur | l'adoption est le vrai poste de dépense |
| maintenance par semaine | **23 077** FCFA | l'entretien coûtait moins cher qu'un jour de prestation |
| répartition de la dépense | **61,1 %** conception, **20,7 %** sources, **3,1 %** formation, **15,1 %** maintenance | la formation, qui produit l'usage, est le poste le plus petit |

Le dernier rapport est le plus instructif : **3,1 %** du budget pour la seule activité qui produit des
lecteurs. Une reprise sérieuse commence par rééquilibrer cette ligne-là.

### 5.8 Détecter les causes d'échec avant la livraison

La recette se prépare **avant** la mise en ligne, avec une liste de vérifications qui tient sur une page :

1. chaque indicateur a sa **carte** complète (**7** champs, pas **6**) ;
2. chaque carte a un **responsable** nommé, une fonction, pas un service ;
3. chaque seuil a une **action** écrite, avec volume et destinataire ;
4. chaque indicateur sensible a son **contre-KPI** publié à côté ;
5. le **grain** est prouvé pour chaque table du modèle ;
6. les **cas particuliers** d'extraction sont documentés ;
7. le dispositif se **rejoue** : deux exécutions donnent le même résultat ;
8. les **destinataires** sont nommés, avec leur décision et leur fréquence ;
9. la **formation** a eu lieu **avant** la mise en ligne ;
10. la **maintenance** a un nom, un budget et un rythme de revue.

C'est le même genre de contrôle que celui que le module s'applique à lui-même : l'atelier M12 vérifie à
chaque exécution que ses **255** valeurs publiées se recalculent à l'identique, que ses **10** cartes
tiennent, et que ses **2** planches restent déterministes.

> **Dans les faits.** La recette de ce module est **automatique** : `01_socle_donnees/scripts/autovalide.py`
> contrôle huit règles — gabarit des seize blocs, origine de chaque nombre cité, existence des figures et
> des chemins, présence du corrigé de chaque exercice, cohérence des barèmes, anglicismes, fréquence des
> encadrés — et le module M12 s'y présente avec **6** chapitres validés **sans avertissement**. Une
> recette qui ne se rejoue pas à chaque modification n'est pas une recette : c'est une signature.

---

## 6. Exemple concret — la reprise, chiffrée de bout en bout

Voici comment se présente la reprise du dispositif raté, budget inchangé :

| Poste de la reprise | Jours | Ce qu'on y gagne |
|---|---|---|
| Sources : cas particuliers, règles, qualité | **8** | plus de défaut découvert en **11** semaines |
| Définitions : **10** cartes, **70** cases | **6** | les **2** débats de définition disparaissent |
| Calcul : socle rejouable, contrôle de grain | **4** | aucune mesure contestée sans rejeu |
| Écran : **10** indicateurs, **1** page | **3** | **41** indicateurs en moins, **7** onglets en moins |
| Formation et recette | **2** | **14** destinataires formés **avant** l'ouverture |
| Revue d'usage trimestrielle | récurrent | un dispositif qui se retire au lieu de mourir |
| Maintenance | récurrente | **23 077** FCFA par semaine, avec un nom dessus |

**Le total de la reprise tient en 23 jours, contre 30 au dossier raté : c'est la répartition qui a
changé.** L'écran passe de **22** jours à **3**, et les définitions de zéro à **6**. Ce déplacement de
quelques jours est la différence entre **41** indicateurs abandonnés et **10** indicateurs utilisés.

---

## 7. Démonstration pas à pas — six étapes de reprise

### 7.1 Étape 1 — diagnostiquer avec des chiffres

Reprendre les **41** indicateurs, les **7** onglets, les **14** destinataires et les **4** ouvertures, et
en tirer un constat mesuré : **193 659** FCFA par indicateur livré, **1 985 000** FCFA par lecteur du
premier jour, **11** semaines de vie. Un diagnostic sans chiffres est un avis.

### 7.2 Étape 2 — choisir 10 décisions

Partir des décisions, pas des données : commander, relancer, arbitrer les prix, surveiller les ruptures,
décider d'un réassort. Les **10** indicateurs du mandat en découlent, et le **8** du mois reste la date
de publication.

### 7.3 Étape 3 — remplir les 70 cases

Chaque indicateur reçoit sa carte : formule, source, granularité, fréquence, responsable, seuil,
contre-KPI. C'est le livrable P2 du projet, et le seul document que la direction signera.

### 7.4 Étape 4 — construire un socle rejouable

Un script, pas un répertoire : **8** tables, **8** grains prouvés, une vue de marge, et un contrôle de
lignes avant/après chaque jointure — la protection contre le **× 15,8**.

### 7.5 Étape 5 — un écran, une page, une action par seuil

Dix indicateurs, leurs contre-KPI, et la réponse à la question du mandat : *que fait-on quand c'est
rouge ?* — avec un volume, un destinataire et une échéance, comme les **1 155** factures de plus de
**90** jours.

### 7.6 Étape 6 — mesurer l'usage à J+7 et à J+30

Deux chiffres, relevés et publiés : combien de destinataires ont ouvert, combien de décisions citent le
dispositif. Sans cette mesure, on retombe sur **6** puis **3** ouvertures par jour — et sur une
résiliation au bout de **11** semaines.

---

## 8. Erreurs fréquentes

1. **Commencer par l'outil.** L'outil est l'étage 6 ; le projet commence aux étages 1 et 5.
2. **Accepter une commande sans décisions.** « Tout » se traduit en **41** indicateurs, jamais en usage.
3. **Ne pas nommer de commanditaire.** Les **2** débats de définition n'ont pas été tranchés : personne
   n'en avait le pouvoir.
4. **Compter les indicateurs livrés comme un résultat.** **41** livrés, **4** lecteurs : le ratio dit
   tout.
5. **Former après la mise en ligne.** **1** heure de formation pour **14** destinataires, et **4**
   ouvertures le premier jour.
6. **Supposer que l'adoption suivra.** La moyenne quotidienne passe de **6** à **3** en une semaine : le
   signal était visible avant l'abandon.
7. **Oublier le responsable de maintenance.** Sans nom, la première source cassée tue le dispositif.
8. **Confondre maintenance corrective et évolutive.** La première répare (**23 077** FCFA par semaine) ;
   la seconde retire ce qui n'est plus lu.
9. **Ne jamais retirer d'indicateur.** Un dispositif qui n'oublie rien finit illisible.
10. **Croire qu'un échec est technique.** Celui-ci est un échec de projet : **3,1 %** du budget pour la
    formation, **0** nom sur les définitions.

---

## 9. Bonnes pratiques professionnelles

- **Écrire le cahier des charges en questions de décision**, avec les **6** questions du §5.3 et trois
  plafonds : **10** indicateurs, **7** champs, **1** action par seuil.
- **Nommer les quatre rôles avant le premier jour** : commanditaire, producteur de données, destinataire,
  responsable de maintenance.
- **Faire signer les cartes** par les responsables, pas par les informaticiens.
- **Mesurer l'usage à J+7 et J+30**, et publier la mesure comme n'importe quel indicateur.
- **Recetter avant d'ouvrir** : les **10** vérifications du §5.8, sur une page.
- **Fixer la revue trimestrielle** : ce qui n'est pas lu se retire.

> **Conseil professionnel.** Avant de lancer un dispositif, faites l'exercice inverse de celui du
> prestataire du dossier : demandez à chaque futur destinataire **quelle décision** il prendra avec quel
> indicateur, à quelle date, et avec quelle action si la valeur est mauvaise. Si trois personnes
> répondent « je ne sais pas », le projet n'est pas prêt — et il vaut mieux le savoir **30** jours avant
> qu'après **11** semaines.

---

## 10. Exercice guidé

**Énoncé.** Rédigez le cahier des charges de la reprise du dossier raté, en une page, avec des critères
de réception vérifiables.

**Étape 1 — les décisions.** Lister les décisions à éclairer : réassort, relance des impayés, arbitrage
des prix, contrôle des retours, arbitrage logistique. Chaque décision donne **1** ou **2** indicateurs :
le total tient dans **10**.

**Étape 2 — les destinataires.** Nommer les personnes et leur décision, pas les services : **14**
destinataires identifiés, dont **10** lecteurs attendus (contre **4** dans le dossier raté).

**Étape 3 — les définitions.** Fixer **10** cartes de **7** champs, avec les points de choix explicites :
taux de retour sur lignes (**1,17 %**) ou sur tickets (**1,91 %**) ; taux de service sur commandes
livrées (**81,0 %**) ou toutes commandes (**78,2 %**) ; marge hors taxes (**29,12 %**) ou toutes taxes
comprises (**24,67 %**).

**Étape 4 — les critères de réception.** Dix vérifications du §5.8, dont trois mesurables : le socle se
rejoue à l'identique en **0,70** s ; les **255** valeurs publiées se recalculent ; chaque seuil a son
action.

**Étape 5 — l'usage.** Objectif d'adoption : **10** lecteurs sur **14** à J+30, mesuré et publié. Le
dossier raté en comptait **4** à J+1.

**Étape 6 — l'entretien.** Un responsable nommé, **23 077** FCFA par semaine de maintenance, une revue
trimestrielle qui retire les indicateurs non lus.

---

## 11. Exercices autonomes

1. **Dix causes.** Reprenez les **10** causes du §5.1 et dites, pour chacune, le signal **mesurable** qui
   l'aurait détectée avant la livraison.
2. **Rôles.** Attribuez les **4** rôles du §5.2 à des fonctions d'une entreprise que vous connaissez, et
   notez lequel manque aujourd'hui.
3. **Cahier des charges.** Écrivez les **6** questions et répondez-y pour un dispositif réel.
4. **Adoption.** Calculez le taux d'ouverture (**4** sur **14**) et proposez le protocole de mesure à
   J+7 et J+30.
5. **Économie.** Calculez le coût par indicateur (**193 659** FCFA) et le coût par lecteur (**1 985 000**
   FCFA) du dossier raté, puis refaites le calcul pour un dispositif de **10** indicateurs lu par **10**
   personnes.
6. **Recette.** Rédigez la page de recette du §5.8 en la transformant en liste cochable, avec la preuve
   attendue pour chaque ligne.

---

## 12. Correction détaillée

**Exercice 1.** Par exemple : cause 1 se détecte par le nombre de décisions listées (s'il est inférieur
à **10**, la commande est floue) ; cause 8 par la mesure d'ouverture à J+7 ; cause 9 par l'existence d'un
nom et d'un budget (**23 077** FCFA par semaine).

**Exercice 2.** Attendu : une attribution nominative, avec le constat des rôles absents — le plus souvent
le **commanditaire** et le **responsable de maintenance**.

**Exercice 3.** Les réponses doivent tenir en une ligne chacune et désigner une personne, une date et une
action : c'est le test de validité.

**Exercice 4.** **28,6 %** d'ouverture le premier jour. Protocole : comptage des ouvertures uniques par
destinataire à J+7 et J+30, avec un seuil d'alerte à **60 %** et une relance individuelle en dessous.

**Exercice 5.** **41** indicateurs donnent **193 659** FCFA par indicateur et **1 985 000** FCFA par
lecteur ; **10** indicateurs pour **10** lecteurs donnent, à budget constant, **794 000** FCFA par
indicateur et **794 000** FCFA par lecteur — soit **2,5** fois moins par lecteur.

**Exercice 6.** Attendu : chaque ligne associée à une **preuve** (une capture ne compte pas : on attend
un rejeu, un contrôle de valeur, un nom, une date).

---

## 13. Mini-projet de chapitre

**« La note de reprise en une page »** (2 h). Rédigez la note qui accompagne le livrable P3 du projet :
constat chiffré du dispositif en place (**41** indicateurs, **4** lecteurs, **11** semaines), les **10**
indicateurs retenus, la répartition des **30** jours, les critères de réception, l'objectif d'adoption et
le nom du responsable de maintenance. Une page, pas deux : c'est l'exercice de concision qui prépare le
livrable du projet.

---

## 14. Résumé du chapitre

| Notion | Ce qu'il faut retenir |
|---|---|
| Les 10 causes | commande floue, pas de commanditaire, sources non documentées, définitions non écrites, trop d'indicateurs, pas de responsable, pas d'action, adoption supposée, maintenance non financée, écran d'abord |
| Cahier des charges | **6** questions, **3** plafonds : **10** indicateurs, **7** champs, **1** action par seuil |
| Rôles | commanditaire, producteur de données, destinataire, responsable de maintenance — nommés avant le premier jour |
| Adoption | **4** lecteurs sur **14** (**28,6 %**), **6** puis **3** ouvertures par jour, **1 985 000** FCFA par lecteur |
| Économie | **193 659** FCFA par indicateur livré, **794 000** par KPI bien ciblé, **3,1 %** du budget pour la formation |
| Maintenance | **1 200 000** FCFA par an, **23 077** par semaine, avec un nom dessus |
| Recette | **10** vérifications sur une page, dont le rejeu du socle en **0,70** s |

## 15. À retenir

> **À retenir.** Un projet décisionnel réussit quand la dépense suit la chaîne : **sources**,
> **définitions**, **écran**, **formation**, **entretien**. Le dossier raté a fait l'inverse — **61,1 %**
> pour la conception, **3,1 %** pour la formation — et il a payé **1 985 000** FCFA par lecteur du premier
> jour.

- **Les dix causes se détectent avant la livraison**, avec une page de recette et des chiffres.
- **L'adoption se mesure** : destinataires, ouvertures à J+7 et J+30, décisions citant le dispositif.
- **La maintenance a un nom et un budget** : sans eux, la première source cassée emporte tout.
- **Retirer est un acte de pilotage** : un dispositif qui n'oublie rien finit à **41** indicateurs.

## 16. Évaluation formative

1. Citez quatre des dix causes d'échec et leur symptôme mesuré.
2. Pourquoi la commande « il doit contenir tout » est-elle dangereuse, et par quel plafond la corrige-t-on ?
3. Quels sont les quatre rôles d'un projet décisionnel ?
4. Que mesure-t-on pour savoir si un dispositif est adopté ?
5. Comment calcule-t-on le coût par lecteur du dossier raté, et que vaut-il ?
6. Pourquoi la formation est-elle un poste de dépense rentable, alors qu'elle ne produit aucun indicateur ?
7. Qu'est-ce que la maintenance évolutive, et en quoi diffère-t-elle de la corrective ?
8. Citez trois des dix vérifications de recette.
9. Que signifie « le socle se rejoue » et comment le vérifie-t-on ?
10. Sur le mandat de reprise, pourquoi **10** indicateurs valent-ils mieux que **41** ?

**Corrigé :** 1. Par exemple : commande floue (**41** indicateurs) ; adoption supposée (**4** ouvertures
sur **14**) ; pas de responsable (aucun nom sur les cartes) ; écran d'abord (**22** jours sur **30**).
2. Parce qu'elle transforme un projet de décision en production de rapports : le plafond de **10**
indicateurs, avec **7** champs chacun, la rend vérifiable. 3. Commanditaire, producteur de données,
destinataire, responsable de maintenance. 4. Les destinataires, les ouvertures à J+7 et J+30, et les
décisions qui citent le dispositif. 5. **7 940 000** FCFA divisés par **4** lecteurs du premier jour =
**1 985 000** FCFA par lecteur. 6. Parce qu'elle produit des **lecteurs**, et que sans lecteur le
dispositif n'a aucune valeur, quel que soit le nombre d'indicateurs livrés. 7. La corrective répare
(**1 200 000** FCFA par an, **23 077** par semaine) ; l'évolutive retire ce qui n'est pas lu et ajoute
les questions récurrentes. 8. Par exemple : carte complète (**7** champs), responsable nommé, seuil avec
action écrite. 9. Deux exécutions produisent le même résultat : sur le socle, écarts nuls en **0,70** s
de reconstruction. 10. Parce que l'usage décide : **10** indicateurs lus par **10** personnes valent
mieux que **41** indicateurs lus par **4** — le budget est comparable, la dépense par lecteur ne l'est
pas.
