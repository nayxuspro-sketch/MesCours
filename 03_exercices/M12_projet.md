# Projet M12.P — « Le tableau de bord que personne n'ouvrait »

**Module : M12 — Fondamentaux de la Business Intelligence · 4 livrables · 20 points · seuil de réussite
13 · environ 10 h de travail.**

**Le mandat.** Une PME de distribution a payé **7 940 000** FCFA pour un tableau de bord de **41**
indicateurs répartis en **7** onglets. Onze semaines plus tard, le contrat de maintenance est résilié :
**14** personnes avaient reçu l'adresse, **4** l'ont ouverte le premier jour. La direction vous mandate
pour **diagnostiquer** ce dispositif et **proposer une reprise**. Sa consigne, textuelle : « pas plus de
**10** indicateurs, chacun avec sa définition écrite, son responsable, sa fréquence, son seuil et son
contre-indicateur. Et une réponse à la seule question qui compte : que fait-on quand il passe au
rouge ? »

## 1. Énoncé

### Le matériel fourni

Tout est dans `03_exercices/dossier_M12/` :

| Pièce | Contenu |
|---|---|
| `etude_avant.md` | les **12** pages du dossier : commande, devis, liste des **41** indicateurs, démarrage, sources de la discorde, coût de l'abandon, questions jamais posées, mandat de reprise |
| `socle_m12.sql` | le socle : **8** tables (ventes, commande, encaissement, stock mensuel, ruptures, logistique, produit, magasin) et la vue de marge |
| `connexion.py` | l'ouverture de la base, identique à celle des chapitres |
| `ATTENDU.json` | les mesures de référence du socle, pour vérifier vos calculs |
| 6 fichiers `.csv` | les cinq sources opérationnelles ajoutées par M12 : coût d'achat, stock, ruptures, commandes, encaissements, logistique |

**Règle du mandat : un diagnostic qui ne mesure rien est un avis.** Chaque affirmation de votre dossier
doit porter un chiffre, et chaque chiffre doit se recalculer avec les fichiers fournis.

### Les six totaux de contrôle

Avant de commencer, vérifiez que votre socle répond :

| Contrôle | Valeur attendue |
|---|---|
| lignes de vente | **240 000** dont **237 191** hors retours |
| chiffre d'affaires net | **15 595 154 955** FCFA (brut : **15 419 985 157**) |
| clients | **23 497** pour **145 212** tickets |
| marge brute | **3 847 989 780** FCFA, soit **29,12 %** hors taxes |
| ruptures | **2 428** couples produit-magasin-mois, **13 129** jours |
| encours | **1 202 550 590** FCFA sur **1 272** factures ouvertes |

Si l'un de ces six contrôles ne tombe pas juste, ne poursuivez pas : reprenez le socle (§7).

## 2. Les dix indicateurs imposés (le catalogue du mandat)

La reprise doit couvrir ces **10** indicateurs, ni plus ni moins :

1. chiffre d'affaires net
2. marge brute
3. taux de rupture
4. rotation de stock
5. panier moyen
6. taux de retour
7. taux de service
8. taux de recouvrement
9. coût logistique unitaire
10. part de marché interne

Chacun doit être livré avec sa **carte de définition** complète : **7** champs, soit **70** cases à
remplir. Une case vide compte comme une case fausse.

## 3. Les 4 livrables

### P1 — Le diagnostic mesuré (6 points)

**Format : 3 pages maximum, plus un tableau de mesures.** Le diagnostic répond, chiffres en main, à six
questions :

1. **Combien a coûté le dispositif ?** Ventilez les **7 940 000** FCFA par poste et calculez le coût par
   indicateur livré, le coût par KPI du mandat et le coût par lecteur du premier jour.
2. **Pourquoi les chiffres se contredisaient-ils ?** Reprenez les **3** sources de la discorde —
   CA net contre CA brut, deux coûts d'achat, deux dénominateurs du panier moyen — et donnez, pour
   chacune, les deux valeurs mesurées sur le socle.
3. **Que valait la couche sémantique ?** Montrez, sur un indicateur au choix, que le socle permet
   plusieurs définitions défendables, et mesurez-les.
4. **Pourquoi les gens ont-ils cessé de l'ouvrir ?** Mesurez l'adoption : destinataires, ouvertures,
   évolution hebdomadaire, et la chute de la deuxième semaine.
5. **Quels étages de la chaîne ont été construits, et lesquels ont été sautés ?** Situez les **7** étages
   et donnez la mesure du socle pour chacun.
6. **Quelles causes d'échec retrouvez-vous ?** Citez-en au moins cinq parmi les **10** du cours, chacune
   avec son symptôme mesuré.

**Ce qui fait la note** : chaque affirmation porte un chiffre recalculable ; aucune cause n'est affirmée
sans mesure ; le coût par lecteur est calculé et interprété.

### P2 — La carte de définition de 10 KPI (8 points)

**Format : 10 fiches.** C'est le livrable central du module, et le document que la direction signera. Pour
chacun des **10** indicateurs du §2, remplissez les **7** champs :

| Champ | Exigence |
|---|---|
| **Formule** | numérateur, dénominateur, base de calcul, exclusions — sans ambiguïté |
| **Source** | la table et le fichier exacts, avec les cas particuliers connus |
| **Granularité** | ce que représente une ligne du résultat |
| **Fréquence** | quand l'indicateur est juste, et à quelle date il est arrêté |
| **Responsable** | une fonction nommée, pas un service |
| **Seuil d'alerte** | une valeur, et la mesure de ce qu'elle déclenche |
| **Contre-KPI** | l'indicateur publié à côté, avec sa valeur actuelle |

Deux exigences de fond :

- **chaque valeur actuelle est mesurée sur le socle** (tableau récapitulatif de vos **10** valeurs, avec
  la requête ou le script qui les produit) ;
- **au moins trois cartes justifient un choix de définition** en comparant deux versions mesurées — par
  exemple CA net (**15 595 154 955** FCFA) contre CA brut (**15 419 985 157**), ou taux de service sur
  commandes livrées (**81,0 %**) contre toutes commandes (**78,2 %**).

**Ce qui fait la note** : les 7 champs sont remplis pour les 10 indicateurs ; les valeurs sont mesurées et
reproductibles ; les choix de définition sont argumentés par des chiffres ; un contre-KPI accompagne
chaque indicateur et sa valeur est donnée.

### P3 — Le plan de reprise (4 points)

**Format : 2 pages, dont un tableau de charges.** Reprenez le budget du dispositif raté et proposez une
répartition des **30** jours entre les étages de la chaîne (sources, extraction, stockage, modèle,
sémantique, écran, diffusion), en justifiant chaque poste par un risque mesuré. Le plan doit préciser :

- **ce qu'on arrête** : au moins trois pratiques du dossier (par exemple la publication d'indicateurs sans
  responsable, la définition locale du CA, l'onglet « Écarts » sans cible) ;
- **ce qu'on garde** malgré l'échec : au moins une chose utile du dispositif précédent ;
- **le calendrier** : nombre de semaines, jalons, et la date de la première revue d'usage ;
- **les destinataires** : qui reçoit quoi, à quelle fréquence, et l'objectif d'adoption chiffré à J+30.

**Ce qui fait la note** : la répartition est argumentée ; les charges sont cohérentes avec le total ;
l'objectif d'adoption est chiffré et mesurable.

### P4 — La page « que fait-on quand c'est rouge ? » (2 points)

**Format : 1 page.** C'est la réponse à la seule question laissée sans réponse par le dispositif
précédent. Pour les **10** indicateurs, une ligne par indicateur, avec quatre colonnes : le seuil, l'action
exacte, la personne qui la déclenche, le délai. Les actions doivent avoir un **volume** : une liste de
produits, un nombre de factures, un montant — jamais « surveiller » ou « relancer si nécessaire ».

**Ce qui fait la note** : les dix seuils ont une action ; les actions ont un volume et un destinataire ;
la page tient en une page.

## 4. Barème

| Livrable | Points | Seuil de détail |
|---|---|---|
| **P1** Diagnostic mesuré | **6** | 1 point par question, si la réponse est chiffrée et recalculable |
| **P2** Carte de 10 KPI | **8** | 0,8 point par indicateur, dont 0,5 pour la complétude des **7** champs et 0,3 pour la cohérence des valeurs |
| **P3** Plan de reprise | **4** | 1 point par exigence : arrêts, conservation, calendrier, adoption |
| **P4** Page « c'est rouge » | **2** | 0,2 point par indicateur, si le seuil **et** l'action sont complets |
| **Total** | **20** | **seuil de réussite : 13** |

**Ce que le barème sanctionne** : un chiffre repris du dossier sans être recalculé (**−1** par chiffre) ; une
carte de définition incomplète (**−0,3** par champ vide) ; une action sans volume (**−0,2**) ; un
contre-KPI absent ou décoratif (**−0,3**).

## 5. Ce qui fait rejeter un livrable

1. **Un diagnostic sans mesure** : les affirmations du dossier ne portent pas de chiffre vérifiable.
2. **Des cartes recopiées des chapitres** : les valeurs doivent être **mesurées** sur le socle, pas
   reprises du cours.
3. **Des définitions ambiguës** : « taux de retour » sans préciser numérateur ni dénominateur.
4. **Un seul indicateur sans responsable** : **10** indicateurs, **10** fonctions nommées.
5. **Des seuils sans action** ou des actions sans volume.
6. **Une page P4 qui dépasse une page** : l'exercice porte sur la concision autant que sur le fond.
7. **Un contre-KPI décoratif** : il doit être mesuré sur le socle, avec sa valeur actuelle.
8. **Plus de 10 indicateurs** : le mandat est un plafond, pas une suggestion.

## 6. Déroulé conseillé (4 séances, environ 10 h)

| Séance | Durée | Travail | Livrable visé |
|---|---|---|---|
| 1 | 2 h | lecture du dossier, contrôle des six totaux, premiers calculs du diagnostic | P1 (questions 1 à 3) |
| 2 | 3 h | rédaction des cartes de définition, mesure des valeurs actuelles, choix de définition argumentés | P2 (indicateurs 1 à 6) |
| 3 | 3 h | fin des cartes, seuils éprouvés par la mesure, contre-KPI mesurés | P2 (indicateurs 7 à 10) |
| 4 | 2 h | plan de reprise, répartition des jours, page « c'est rouge », relecture | P3 et P4 |

## 7. Comment vous corriger vous-même

1. **Les six totaux** du §1 tombent juste, et votre socle se reconstruit à l'identique deux fois de suite.
2. **Chaque chiffre du diagnostic** se recalcule : aucun n'est recopié du dossier.
3. **Chaque carte a 7 champs** : comptez-les ; s'il en manque un, la carte n'est pas finie.
4. **Chaque seuil a été essayé** : vous savez dire combien de lignes il met en alerte.
5. **Chaque contre-KPI a une valeur mesurée** et une phrase expliquant ce qu'il protège.
6. **La page P4 tient en une page** et chaque action porte un volume, une personne et un délai.
7. **L'objectif d'adoption est chiffré** et comparable aux **4** lecteurs sur **14** du dispositif
   précédent.

**Le test final.** Faites lire votre P2 par quelqu'un qui ne connaît pas le dossier : s'il peut recalculer
un indicateur et dire qui l'améliore ou le dégrade, la carte est bonne. S'il pose une question sur une
définition, elle est incomplète.
