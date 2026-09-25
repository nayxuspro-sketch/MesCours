# Architecture pédagogique complète
## Formation professionnelle en Analyse de données appliquée & Business Intelligence
### Document de référence — Étape 1 du protocole de production

| | |
|---|---|
| **Nature du document** | Architecture pédagogique (plan directeur de production) |
| **Statut** | V1.0 — soumis à validation avant rédaction des modules |
| **Date d'établissement** | 17 septembre 2026 |
| **Périmètre** | 22 modules obligatoires + 3 modules de spécialisation, **143 chapitres**, 180 exercices corrigés (190 avec les options), 30 projets, 28 épreuves évaluées |
| **Destinataire** | Apprenant solo, débutant absolu, francophone (Afrique de l'Ouest), autodidacte encadré |
| **Livrable final prévu** | Manuel professionnel A4, mise en page éditeur, PDF prêt à imprimer |

> **Note de méthode.** Ce document est le *seul* qui est produit à l'étape 1, conformément à votre consigne : « Commence par présenter l'architecture pédagogique complète de la formation, avant de commencer la rédaction des chapitres. » Aucun contenu pédagogique définitif n'est encore rédigé : tout ce qui suit est un **contrat de production**, c'est-à-dire la promesse détaillée et vérifiable de ce que contiendra le manuel. À chaque étape ultérieure, vous pourrez comparer le module livré à la ligne correspondante de ce document.

---

# PARTIE A — FONDEMENTS DU PROJET

## A.1. Positionnement du manuel

**Ce que le manuel est.** Un parcours autodidacte complet, de zéro à l'embauche, en analyse de données et Business Intelligence. Il remplit simultanément six fonctions que vous avez explicitement demandées :

| Fonction | Ce que cela implique concrètement dans le manuel |
|---|---|
| **Cours** | Chaque notion est définie, expliquée intuitivement, mise en formule et interprétée. Aucun prérequis implicite. |
| **Tutoriel** | Chaque opération est détaillée clic par clic, ligne de code par ligne de code, avec l'écran ou le résultat attendu. |
| **Cahier d'exercices** | 180 exercices progressifs, chacun avec objectif, outil, données, consigne, compétence évaluée, corrigé pas à pas. |
| **Guide pratique** | Bonnes pratiques, nommage, documentation, contrôle qualité, pièges réels, checklists utilisables au travail. |
| **Parcours professionnel** | Feuille de route débutant → Data Analyst junior → confirmé → BI Analyst → BI Developer, avec critères de passage objectivés. |
| **Portfolio** | 14 projets "vitrine" construits, documentés et présentables, issus directement des modules. |

**Ce que le manuel n'est pas.**
1. **Pas une encyclopédie d'outils.** Vous l'exigez (§6) : seuls sont enseignés les outils réellement utiles sur le marché francophone ouest-africain. Les autres sont *mentionnés* avec une raison de les ignorer ou de les adopter plus tard.
2. **Pas un catalogue de concepts.** Chaque notion sans application professionnelle identifiable a été supprimée de la conception.
3. **Pas un substitut de données d'entreprise réelles.** Le manuel fournit des données *réalistes* et explique comment transposer la méthode à vos données propres ; il ne prétend pas remplacer une immersion en entreprise.
4. **Pas une préparation certifiante formelle.** Il prépare aux entretiens et aux tests techniques ; les certifications officielles font l'objet du module M20, avec recommandations argumentées et non avec promesse de réussite.

**Promesse centrale, formulée en une phrase :**
> *À la fin du manuel, vous êtes capable de recevoir un fichier de données brutes et douteux, d'en faire un tableau de bord fiable dont on peut débattre les chiffres en réunion de direction, et de défendre oralement les trois décisions que ces chiffres suggèrent.*

---

## A.2. Public cible et hypothèses de conception

| Élément | Hypothèse retenue | Conséquence sur la conception |
|---|---|---|
| Niveau de départ | Aucune notion en informatique, statistiques, programmation, BI | Un chapitre 0 de alphabétisation bureautique (M01) avant tout outil d'analyse ; définition systématique du vocabulaire |
| Matériel | Ordinateur portable Windows, 8 Go de RAM minimum, connexion internet intermittente | Windows-first ; tous les fichiers livrés en local ; installations possibles hors-ligne signalées ; outils gratuits uniquement |
| Temps disponible | À définir par vous (§ H.2) ; conception sur une base de **10 h/semaine** | Chaque module = ~25 à 30 h, soit 10 h/semaine pendant 3 semaines ; découpage en séances de 90 min autonome |
| Langue | Français de travail ; documentation technique en anglais | Systématique : *terme français — Terme anglais* au premier emploi ; phrases courtes ; pas d'idiomes |
| Contexte économique | Burkina Faso / UEMOA : PME, grande distribution, banques et assurance, télécom, ONG, administration, agriculture | Tous les jeux de données, scénarios, monnaies (FCFA), organisations et cas métier ancrés dans cette réalité, sans jamais sacrifier la généralité de la méthode |
| Contraintes structurelles réelles | Coût des licences, énergie instable, volume de données souvent faible à moyen, Excel encore dominant, forte demande de compétences Power BI | Ordre d'apprentissage optimisé : **Excel d'abord** (immédiatement rentable et utile), SQL et Power BI en force principale, Python en accélérateur |
| Objectif de sortie | Emploi ou promotion, en local ou en remote international | Parcours orienté production de livrables présentables dès le module 4 ; module emploi (M20) avec CV, portfolio, tests techniques, soutenance |

---

## A.3. Réponse à vos 20 objectifs de sortie (matrice de couverture)

Vos 20 objectifs de la section §2 du cahier des charges, chacun **affecté à des modules porteurs** et **prouvé par un livrable**. Le principe : aucun objectif n'est revendiqué par un seul module (fragile), aucun module n'existe sans porter au moins un objectif.

| # | Objectif de fin de formation | Modules porteurs (principal en gras) | Preuve de maîtrise |
|---|---|---|---|
| 1 | Comprendre les données et leur structure | **M01**, M12, M13 | Quiz M01 + fiche de lecture d'un fichier inconnu (1 page) |
| 2 | Collecter et organiser des données | M01, **M04**, M13 | Formulaire + plan de collecte livré, M04.P |
| 3 | Nettoyer et préparer des données | **M05**, M03 (Power Query), M08 (pandas) | Script M05 (3 langages) + rapport qualité chiffré |
| 4 | Appliquer les statistiques nécessaires | **M02** | Étude statistique guidée M02.P |
| 5 | Analyser des données avec Excel | **M03** | Classeur de gestion TCD/DASH complet M03.P |
| 6 | Interroger des bases avec SQL | **M07** | 40 requêtes validées + cas d'audit M07.P |
| 7 | Utiliser Python pour l'analyse | **M08** | Notebook d'analyse reproductible M08.P |
| 8 | Utiliser les outils modernes de BI | M10, **M14**, M16 | Dashboard publié M14.P + comparatif d'outils argumenté |
| 9 | Construire des modèles de données fiables | M13, **M10**, M14 | Schéma en étoile documenté + modèle Power BI validé |
| 10 | Créer des indicateurs et KPI pertinents | **M10**, M18 | **Carte de définition des métriques** (artefact signature du manuel) |
| 11 | Concevoir des tableaux de bord professionnels | M09, M10, **M14** | Dashboard validé par la grille de conception §E.7 |
| 12 | Utiliser Power BI à un niveau avancé | **M14**, **M15** | Projet BI avancé complet M14.P2 + mesures DAX documentées |
| 13 | Automatiser analyses et reportings | M03 (Power Query), **M17**, M08 | Chaîne automatisée rejouable en 1 clic |
| 14 | Interpréter correctement les résultats | M02, M11, **M19** | Note d'interprétation avec limites et biais énoncés |
| 15 | Présenter les résultats à un décideur | **M19** | Soutenance filmée/enregistrée de 8 min + deck |
| 16 | Transformer des données brutes en aide à la décision | **Transversal** — validé par le projet final M21 | Livrable de mission complet (voir M21) |
| 17 | Réaliser des projets complets de bout en bout | M21, M18, M06 | 8 projets fil rouge + 6 projets sectoriels |
| 18 | Constituer un portfolio professionnel | **M20** (continuum dès M03) | 14 fiches de projet publiables |
| 19 | Travailler sur des données réelles d'entreprise | M05, M18, **M21** | Données volontairement "sales" + données ouvertes réelles |
| 20 | Connaître les bonnes pratiques des pros de la Data/BI | **M04** + transversal permanent | Checklist de qualité appliquée à chaque rendu |

**Contrôle de cohérence :** les 20 objectifs sont couverts, 20/20. Aucun module des 20 obligatoires n'est orphelin d'un objectif (vérification §G.1).

---

# PARTIE B — LE SYSTÈME PÉDAGOGIQUE

## B.1. Les six niveaux et leurs portes d'entrée

Le cahier des charges impose la progression *Débutant absolu → Débutant → Intermédiaire → Avancé → Professionnel → Expert*. Je la rends **décidable** : chaque niveau a un critère objectif, vérifiable par un artefact, pas par une impression.

| Niveau | Nom | Définition opératoire | Portes (artefacts exigés pour passer) | Modules |
|---|---|---|---|---|
| **N0** | Débutant absolu | Ne sait pas ce qu'est un classeur, une cellule, un fichier CSV, une moyenne | Ouvrir un fichier, le décrire oralement en 5 phrases, dire ce qu'on voudrait en savoir | M01 |
| **N1** | Débutant | Lit des données simples, calcule des résumé, comprend le vocabulaire de base | 8/10 au quiz M02 ; tableau croisé dynamique produit sans aide ; définition correcte de 30 termes du glossaire de base | M01 → M03 |
| **N2** | Intermédiaire | Prépare seul une donnée et répond à une question métier simple avec Excel, SQL ou Python selon le cas | M05 : nettoyage livré avec rapport qualité ; M07 : 30 requêtes justes sur 35 ; M08 : notebook exécuté de bout en bout sans erreur | M04 → M08 |
| **N3** | Avancé | Conçoit une analyse complète et un tableau de bord, argumente ses choix | M11 : 25 requêtes de niveau 3 correctes ; M14 : dashboard respectant intégralement la grille de conception ; DAX sans colonne calculée pour un ratio | M09 → M15 |
| **N4** | Professionnel | Livre un système de BI exploitable par d'autres, automatisé et documenté, et soutient ses conclusions | M21 : mission complète validée par la grille de soutenance (≥ 16/20) ; chaîne de mise à jour reproductible ; 3 fiches portfolio publiables | M16 → M21 |
| **N5** | Expert | Choix d'architecture et de méthode assumés, cadrage de l'incertain, encadrement, capacité à concevoir le parcours d'un autre | Projet d'extension libre à M22 validé en auto-évaluation argumentée ; production d'un module de formation pour un tiers ; analyse critique d'un modèle prédictif | M19 approfondi + M22 |

**Règle de non-avancement.** Un niveau n'est pas validé par la lecture ; il est validé par l'artefact. Le manuel prévoit pour chaque porte une *procédure de rattrapage* : 3 exercices ciblés identifiés au lieu de reprendre tout le module.

---

## B.2. Les douze principes pédagogiques appliqués

Vos principes du §3 sont reformulés en règles de rédaction contraignantes, que je m'applique et que vous pourrez vérifier dans chaque chapitre.

| # | Principe | Règle de rédaction vérifiable |
|---|---|---|
| P1 | Ne jamais supposer un terme connu | Tout terme non commun à un lycéen est défini à son **premier** emploi, dans un encadré, avec l'équivalent anglais |
| P2 | Expliquer avant de manipuler | Aucun clic n'est demandé avant la phrase « *à quoi ça sert et pourquoi* » |
| P3 | Six questions par notion | Définition simple · utilité · importance · exemple concret · contexte d'usage · outil |
| P4 | Un exemple chiffré minimum | Toute formule est suivie d'un calcul à la main sur au plus 8 lignes de données |
| P5 | Montrer l'opération | Après toute explication : la marche à suivre littérale (Excel : chemins de menus ; SQL : requête entière ; Python : bloc exécuté + sortie) |
| P6 | Anticiper l'erreur | Chaque notion difficile est suivie de l'erreur la plus fréquente et de son symptôme visible |
| P7 | Progression par charge cognitive | 1 nouvelle notion majeure + max 2 secondaires par chapitre ; jamais 2 nouveaux langages dans la même séance |
| P8 | Réactivation espacée | Chaque module commence par 5 questions de rappel des modules antérieurs (méthode des « 5 minutes de récupération ») |
| P9 | Manipuler des données sales | 100 % des jeux de données du parcours contiennent des défauts réels, jamais un jeu parfait |
| P10 | Décider, pas seulement calculer | Chaque module se termine par une question de décision : « *que ferait le responsable avec ce résultat ?* » |
| P11 | Justesse technique | Tout code, toute requête, toute formule est exécuté dans un environnement réel avant publication (voir §G.2) |
| P12 | Accessibilité matérielle et économique | Aucun outil payant exigé pour terminer la formation, y compris les modules Tableau et Power BI (voir C.4) |

**Exemple d'application de P1–P6 (extrait témoin, ton et granulométrie attendus) :**

> **Table de faits — Fact table — Encadré n°1 du chapitre M10.C04**
> *Définition simple.* Une table de faits est la table qui contient **les événements** que l'entreprise veut mesurer : une vente, un paiement, une consultation, une livraison. Une ligne = un événement. Elle ne contient presque que des nombres à additionner (la quantité, le montant) et des références vers les "autour" de l'événement (le client, le produit, la date).
> *Utilité.* Elle répond à la question « *combien* ». Les tables de dimensions répondent à « *qui, quoi, où, quand* ».
> *Pourquoi c'est important.* Un tableau de bord qui rame, ou qui donne un chiffre faux quand on ajoute un filtre, vient presque toujours d'une table de faits mal conçue (par exemple une ligne qui mélange deux événements).
> *Exemple concret.* À la quincaillerie **Sahel Distribution**, la table `ventes` compte 24 000 lignes : une par ligne de ticket de caisse. Une ligne dit : « magasin 3, ticket 11 902, ciment de 50 kg, 12 sacs, à 4 200 FCFA le sac, le 12 mars 2025 ».
> *Contexte d'usage.* Dès que vous voulez calculer un chiffre d'affaires, une marge, une quantité vendue.
> *Outil.* Power BI : c'est la table que vous marquez "Table de faits" dans le modèle. Excel : votre TCD se construit dessus. SQL : `SUM(montant)` se fait sur cette table.

---

## B.3. Gabarit de chapitre (16 blocs) — normalisé et chiffré

Chaque chapitre du manuel suit votre structure en 16 points. Pour éviter que ce gabarit ne devienne un carcan verbeux, chaque bloc a une **durée de rédaction cible** et une **règle de compression** : les blocs sont obligatoires, mais leur format est adaptatif (un paragraphe suffit si c'est suffisant).

| Bloc | Contenu | Longueur cible | Règle de compression |
|---|---|---|---|
| 1 | Objectifs du chapitre (« à la fin, vous saurez… », 3 à 5 verbes d'action) | 5 lignes | — |
| 2 | Pourquoi cette notion est importante (situations professionnelles réelles) | 1/2 p. | — |
| 3 | Explication simple (analogie du quotidien, pas de jargon) | 1/2 – 1 p. | — |
| 4 | Vocabulaire essentiel (tableau : *Français — English — définition — piège*) | 1 tableau | ≤ 10 termes |
| 5 | Cours approfondi (mécanique, cas limites, variantes) | 2 – 4 p. | — |
| 6 | Exemple concret (données chiffrées du fil rouge) | 1 p. | — |
| 7 | Démonstration pas à pas (captures à insérer : légende + contenu exact ; ou listing complet exécuté) | 1 – 3 p. | une étape = une action |
| 8 | Erreurs fréquentes (symptôme → cause → correction) | 1 tableau de 3 à 6 lignes | — |
| 9 | Bonnes pratiques professionnelles | 5 à 10 puces | format checklist |
| 10 | Exercice guidé (fait ensemble, corrigé en continu dans le texte) | 1 – 2 p. | — |
| 11 | Exercices autonomes (3 à 6, difficulty balisée ★ à ★★★) | 1/2 p. | — |
| 12 | Correction détaillée (étapes, raisonnement, résultat intermédiaire) | 1 – 3 p. | jamais le seul résultat final |
| 13 | Mini-projet (livrable réel, 30 à 60 min) | 1/2 p. | 1 par module minimum (souvent 1 par chapitre-pivot) |
| 14 | Résumé du chapitre (schéma de synthèse + texte) | 1/2 p. | 10 lignes max |
| 15 | Ce qu'il faut retenir (encadré « À retenir », 5 points) | 1 encadré | — |
| 16 | Évaluation formative du chapitre (5 questions + corrigé, auto-correction) | 1/2 p. | QCM + une question ouverte |

Chapitre-type = **6 à 14 pages A4**. **Calibre en vigueur (mesuré sur M01, achevé et autovalidé le 17 septembre 2026) : 12,5 pages par chapitre**, décomposées en **7 pages de matière** (blocs 1 à 9 et 14 à 16) et **5,5 pages d'exercices embarqués** (blocs 10 à 13 : exercice guidé, exercices autonomes, correction détaillée, mini-projet) — les mesures réelles de M01 donnent 12,3 pages en moyenne sur ses sept chapitres, de 11 à 14 pages. Le budget total, additionné module par module au §F.4, donne **≈ 2455 pages** en manuel intégral, **≈ 1692** en tome unique condensé, **747** dès la fin de M07 en parution progressive. Chaque ligne du budget se recompose par `chapitres × 12,5 + 17 pages d'appareil de module` : aucun total n'est posé « à l'œil », et le calcul se refait avec `tools/budget_pages.py`.

---

## B.4. Les six encadrés de mise en page pédagogique

| Encadré | Usage | Fréquence cible | Code couleur du PDF |
|---|---|---|---|
| **Définition** | Premier emploi d'un terme : *Français — English — sens simple* | 4 à 8 par chapitre | Bandeau bleu clair |
| **À retenir** | L'essentiel non négociable du chapitre/module | 2 à 4 par chapitre | Bandeau vert, icône ★ |
| **Attention** | Erreur fréquente, coût réel de l'erreur, contre-exemple | 2 à 5 par chapitre | Bandeau ambre, icône ⚠ |
| **Conseil professionnel** | Ce que font les analystes en entreprise, les usages, les raccourcis propres | 1 à 3 par chapitre | Bandeau gris, icône 💼 |
| **Dans les faits** | Chiffre, ordre de grandeur, cas réel d'entreprise locale ou internationale | 1 à 2 par chapitre | Encadré fin, sans fond |
| **Boîte à outils** | Où cliquer, quelle fonction, quelle ligne de commande, quelle doc officielle | 1 par section-outil | Cadre pointillé, monospace |

Toutes les formules sont centrées et numérotées (équation 3.2 = module 3, équation 2). Tout listing est numéroté avec le langage indiqué, et **testé** (§G.2).

---

## B.5. Chaîne de difficulté des exercices (7 familles)

Votre §7 demande sept types d'exercices. Ils sont appliqués comme un **cycle systématique** dans chaque module, et non répartis au hasard : la répétition du même cycle est ce qui produit l'automatisme professionnel.

| Famille | Rôle pédagogique | Forme du corrigé | Occurrences visées |
|---|---|---|---|
| **E1 — Très simple** | Créer la réussite, ancrer le vocabulaire et le geste | Copie littérale commentée | **46** (un par chapitre environ) |
| **E2 — Application directe** | Reproduire avec des données différentes | Déroulé complet | **48** |
| **E3 — Réflexion** | Choisir un outil, une visualisation, une formule et le justifier | Argumentaire avec critères de décision | **24** |
| **E4 — Correction d'erreurs** | Diagnostiquer un fichier, une requête, une formule, un dashboard défectueux | Analyse de symptôme → cause → remède | **20** (le format le plus formateur) |
| **E5 — Analyse** | Répondre à une question métier ouverte avec les moyens du chapitre | Chemin complet + conclusion chiffrée | **24** |
| **E6 — Mise en situation professionnelle** | Briefing de client interne, contrainte de délai, livrable défini | Livrable complet + note d'intention | **13** (les modules où une commande réelle a du sens ; le projet, lui, est bien 1 par module) |
| **E7 — Difficulté progressive / défi** | Dépassement, optionnel, non bloquant | Piste de résolution + solution | **5** (réservés aux modules techniques, pour ne pas alourdir les fondamentaux) |

Format d'énoncé obligatoire (une fiche par exercice, conforme à votre §7) :

> **Exercice M07.E12 — « Le chiffre que le directeur conteste »**
> **Outil recommandé :** SQL (DuckDB/PostgreSQL) + Excel pour la vérification
> **Objectif :** reproduire un contrôle de cohérence entre deux niveaux d'agrégation
> **Données utilisées :** `sahel_ventes`, `sahel_dim_magasin` (module M21, 24 000 lignes)
> **Travail demandé :** 1) calculer le CA mensuel par magasin ; 2) retrouver un écart de 3 % signalé par le directeur ; 3) conclure sur la cause la plus probable et la vérifier.
> **Compétence évaluée :** fiabilité du résultat, jointure, agrégation, esprit critique
> **Temps indicatif :** 45 min — **Difficulté :** ★★☆☆☆ (E6)
> **Correction :** pages 742–745 (déroulé complet, requêtes commentées, deux causes écartées par une requête dédiée)

---

## B.6. Système d'évaluation du manuel

Votre §9 exige, par module : quiz de 10–20 questions, 2 à 5 exercices pratiques, une étude de cas, un projet, avec corrigés détaillés. C'est le socle ; j'ajoute **la mécanique qui fait que le système tient sans enseignant humain**.

| Instrument | Fréquence | Rôle | Barème |
|---|---|---|---|
| **Récupération** (5 questions, début de module) | 22 | Activer les prérequis | non noté, auto-corrigé |
| **Quiz de module** | 22 (un par module, 15–20 questions) | Vérifier la compréhension, y compris les items de type vrai-faux-piègeux | /20, seuil de passage **14/20** |
| **Exercices pratiques corrigés** | 2 à 5 par module | Vérifier le geste | auto-correction par résultat attendu chiffré |
| **Étude de cas** | 1 par module (sauf M21, projet final) | Vérifier le raisonnement et la décision | grille 5 critères / 20, seuil 12 |
| **Projet de module** | 22 au total (2 pour M14 ; 3 pistes au choix en M18) | Vérifier la production | grille projet / 20, seuil 13 |
| **Épreuve de validation de palier** | 4 (fin de P1, P2, P4, P5) | Conditions d'entrée au palier suivant : 90 min en temps limité, mélange de requêtes, de formules, de code et une question de décision | /20, seuil 14 |
| **Soutenance** | 2 (M19 et M21) | Vérifier la communication, l'unique compétence qu'aucun QCM ne mesure | grille 20 points (structure 5, clarté 4, rigueur des chiffres 4, recommandations 4, réponse aux objections 3), seuil 16 |

**Correction automatisée disponible (différenciation forte de ce manuel).** Pour les exercices SQL et Python, chaque chapitre fournit un **script d'auto-validation** que l'apprenant exécute lui-même : il compare son résultat au résultat attendu et obtient « validé / non validé + quel test a échoué ». Le corrigé écrit reste intégralement fourni. Cela rend l'auto-formation réellement vérifiable, au lieu de reposer sur l'impression d'avoir compris.

---

# PARTIE C — L'ARCHITECTURE DE LA FORMATION

## C.1. Vue d'ensemble : 6 phases, 22 modules + 3 de spécialisation, 143 chapitres

```
PHASE 0  CULTURE NUMÉRIQUE & POSTURE PROFESSIONNELLE         [N0 → N1]   30 h   ·  1 module   ·   7 chap.
   M01  Lire les données, comprendre le métier de l'analyse (7 chap.)

PHASE 1  FONDATIONS ANALYTIQUES                               [N1 → N2]   60 h   ·  2 modules  ·  16 chap.
   M02  Statistiques appliquées, depuis zéro            (8 chap. · vos 23 notions)
   M03  Excel pour l'analyse de données                  (8 chap.)

PHASE 2  MAÎTRISE OPÉRATIONNELLE                              [N2 → N3]  180 h   ·  6 modules  ·  38 chap.
   M04  Qualité, préparation et documentation des données(6 chap.)
   M05  Chaîne de transformation : Power Query, SQL, pandas (5 chap. · vos 12 opérations)
   M06  Bases de données relationnelles : comprendre      (5 chap.)
   M07  SQL : interroger, agréger, rejoindre               (8 chap.)
   M08  Python pour l'analyse de données                   (8 chap.)
   M09  Analyse exploratoire de données — EDA              (6 chap.)

PHASE 3  COMMUNICATION ANALYTIQUE                              [N3]      30 h   ·  1 module   ·   7 chap.
   M10  Data visualization                                (7 chap.)

PHASE 4  BUSINESS INTELLIGENCE                                [N3 → N4]  150 h   ·  5 modules  ·  35 chap.
   M11  SQL avancé pour la BI                            (7 chap.)
   M12  Fondamentaux de la Business Intelligence          (6 chap.)
   M13  Modélisation des données                          (7 chap.)
   M14  Power BI, de l'import à la publication            (8 chap.)
   M15  DAX pour la BI                                    (7 chap.)

PHASE 5  PERFORMANCE ET AUTONOMIE PROFESSIONNELLE               [N4]     120 h   ·  4 modules  ·  24 chap.
   M16  Tableau et autres outils BI                       (5 chap.)
   M17  Automatisation du reporting                       (6 chap.)
   M18  Analyses sectorielles                              (7 chap.)
   M19  Analyse avancée : prévision, segmentation, scoring (6 chap.)

PHASE 6  PROFESSIONNALISATION                                 [N4 → N5]   90 h   ·  3 modules  ·  16 chap.
   M20  Data storytelling & communication décideur         (6 chap.)
   M21  Projets professionnels complets (7 projets + final)(6 chap.)
   M22  Portfolio, emploi, feuille de route                (4 chap.)
────────────────────────────────────────────────────────────────────────────
SPÉCIALISATION (après N4, au choix)                                      50 h   ·  3 modules  ·  14 chap.
   M23  R pour l'analyse de données                        (5 chap.)
   M24  Data engineering appliqué : ETL/ELT, DuckDB, orchestration (5 chap.)
   M25  Données ouvertes, géomatique et cartographie décisionnelle (4 chap.)

TOTAL parcours de base  = 660 h (22 modules × 30 h)  →  10 h/semaine ≈ 15 mois  ;  20 h/semaine ≈ 7,5 mois
TOTAL avec spécialisations = 710 h (M23–M25 : 50 h de plus)
```

**Ce qui a été changé par rapport à votre plan de 18 modules, et pourquoi** (votre §5 autorisait explicitement : « Construis et, si nécessaire, améliore »).

| # | Transformation | Justification pédagogique ou de marché |
|---|---|---|
| 1 | Votre **Module 1 est scindé** : un volet « savoirs de base sur la donnée » (M01) et un volet « métier, organisation, méthodes de travail » (intégré à M01 + M04) | Pour un débutant absolu, « qu'est-ce qu'un fichier CSV » et « qu'est-ce que le rôle d'un BI Analyst » ne relèvent pas du même effort d'abstraction ; et les exigences de votre §12 (bonnes pratiques) avaient besoin d'un logement, sinon elles ne sont jamais enseignées vraiment |
| 2 | Ajout de **M04** (qualité, documentation, reproductibilité, sécurité) | C'est l'exigence la plus rentable en entretien et celle que tous les débutants ignorent ; elle doit être enseignée *avant* la chaîne d'outils, pas à la fin |
| 3 | Votre **Module 4 est scindé** : M04 (la discipline de la qualité) + M05 (la mise en œuvre comparative Power Query / SQL / pandas) | Votre §4 demandait « explique quel outil choisir selon la taille et la nature des données » : cette comparaison ne s'apprend pas en même temps que le nettoyage, elle s'apprend *après*, comme méta-compétence |
| 4 | Votre **Module 5 est scindé** : M06 (comprendre les bases relationnelles) + M07 (SQL 1) + **M11** (SQL avancé pour la BI) | Le §5 du cahier des charges réunissait 21 notions SQL dont les fonctions de fenêtre ; pour un vrai débutant, c'est deux apprentissages séparés par les statistiques et le nettoyage. Séparer évite le surchargement, et M11 permet de traiter les fenêtres *avec* l'objectif BI qui leur donne un sens |
| 5 | Ajout de **M22** distinct des projets (M21) | Un portfolio et une stratégie d'emploi ne sont pas des compétences de données : elles demandent leurs propres chapitres, sinon elles restent à l'état de conseil |
| 6 | Vos modules 16 et 17 permutés et **le storytelling déplacé en phase 6** (M20) | Vous placiez la communication après la prédiction ; or la communication est ce qui rend employable *avant* d'être prédictif, et elle se pratique mieux quand tous les livrables existent déjà à montrer |
| 7 | Power BI et DAX maintenus séparés (M14 / M15), DAX enseigné **en trois temps** | Votre plan le prévoyait : c'est pédagogiquement juste. Le DAX est introduit à dose contrôlée dans M14 (mesures simples), théorisé en M15 (contextes), réinvesti en M21. Cette règle est explicitement écrite en M15.C01 |
| 8 | Création des **3 modules de spécialisation optionnels** | R est explicitement conditionné dans votre §1 (« lorsque son utilisation est pertinente ») : l'option plutôt que l'obligation est la réponse exacte à votre consigne. Idem pour le data engineering (vos §1 mentionnent ETL/ELT et les bases de données) et la cartographie, très utile dans les secteurs agricole, santé et humanitaire de la zone |

## C.2. Cartographie de l'acquisition des 20 objectifs de sortie

```
                         M01  M02  M03  M04  M05  M06  M07  M08  M09  M10  M11  M12  M13  M14  M15  M16  M17  M18  M19  M20  M21  M22
O01 structure donnée     ██   ·    ·    ·    ·    ▒▒   ·    ▒▒   ██   ·    ·    ·    ▒▒   ·    ·    ·    ·    ·    ·    ·    ▒▒   ·
O02 collecter/organiser  ██   ·    ▒▒   ██   ▒▒   ·    ·    ▒▒   ·    ·    ·    ▒▒   ██   ▒▒   ·    ·    ▒▒   ██   ·    ·    ██   ·
O03 nettoyer/préparer    ·    ▒▒   ██   ██   ██   ·    ▒▒   ██   ██   ·    ▒▒   ·    ·    ██   ·    ·    ▒▒   ·    ▒▒   ·    ██   ·
O04 statistiques         ·    ██   ▒▒   ▒▒   ·    ·    ▒▒   ██   ██   ▒▒   ▒▒   ·    ·    ▒▒   ▒▒   ·    ·    ██   ██   ▒▒   ▒▒   ·
O05 Excel                ·    ▒▒   ██   ▒▒   ██   ·    ·    ·    ▒▒   ▒▒   ·    ▒▒   ·    ▒▒   ·    ▒▒   ██   ▒▒   ·    ·    ██   ·
O06 SQL                  ·    ·    ·    ·    ██   ▒▒   ██   ·    ·    ·    ██   ▒▒   ██   ▒▒   ·    ▒▒   ▒▒   ██   ▒▒   ·    ██   ·
O07 Python               ·    ·    ·    ·    ▒▒   ·    ·    ██   ██   ██   ·    ·    ·    ·    ·    ▒▒   ██   ██   ██   ▒▒   ██   ·
O08 outils BI modernes   ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ·    ██   ▒▒   ██   ██   ██   ▒▒   ▒▒   ▒▒   ▒▒   ██   ▒▒
O09 modèles fiables      ·    ·    ·    ▒▒   ·    ██   ▒▒   ·    ·    ·    ▒▒   ██   ██   ██   ▒▒   ▒▒   ▒▒   ▒▒   ·    ·    ██   ·
O10 KPI                  ·    ▒▒   ▒▒   ·    ·    ·    ██   ·    ▒▒   ·    ██   ██   ▒▒   ██   ██   ▒▒   ▒▒   ██   ▒▒   ██   ██   ·
O11 tableaux de bord     ·    ·    ▒▒   ·    ·    ·    ·    ▒▒   ▒▒   ██   ·    ██   ▒▒   ██   ██   ██   ██   ▒▒   ·    ██   ██   ·
O12 Power BI avancé      ·    ·    ·    ·    ▒▒   ·    ·    ·    ·    ·    ▒▒   ▒▒   ▒▒   ██   ██   ▒▒   ██   ▒▒   ▒▒   ▒▒   ██   ·
O13 automatisation       ·    ·    ▒▒   ▒▒   ▒▒   ·    ▒▒   ██   ·    ·    ·    ▒▒   ·    ██   ·    ▒▒   ██   ·    ▒▒   ·    ██   ▒▒
O14 interpréter          ·    ██   ▒▒   ▒▒   ·    ·    ▒▒   ██   ██   ██   ▒▒   ██   ·    ▒▒   ▒▒   ·    ·    ██   ██   ██   ██   ·
O15 présenter/réunir     ▒▒   ·    ▒▒   ▒▒   ·    ·    ·    ▒▒   ▒▒   ██   ·    ▒▒   ·    ▒▒   ·    ▒▒   ▒▒   ▒▒   ▒▒   ██   ██   ▒▒
O16 brut → décision      ██   ▒▒   ▒▒   ██   ██   ·    ▒▒   ▒▒   ██   ██   ▒▒   ██   ▒▒   ██   ▒▒   ▒▒   ██   ██   ██   ██   ██   ▒▒
O17 projets complets     ·    ·    ▒▒   ▒▒   ▒▒   ·    ▒▒   ▒▒   ██   ▒▒   ▒▒   ▒▒   ▒▒   ██   ▒▒   ▒▒   ██   ██   ██   ██   ██   ▒▒
O18 portfolio            ·    ·    ▒▒   ▒▒   ·    ·    ▒▒   ▒▒   ▒▒   ▒▒   ·    ·    ·    ▒▒   ·    ▒▒   ·    ▒▒   ▒▒   ▒▒   ██   ██
O19 données réelles      ██   ▒▒   ██   ██   ██   ▒▒   ██   ██   ██   ▒▒   ██   ▒▒   ▒▒   ██   ▒▒   ▒▒   ██   ██   ██   ▒▒   ██   ▒▒
O20 bonnes pratiques     ·    ▒▒   ▒▒   ██   ██   ▒▒   ██   ██   ▒▒   ▒▒   ██   ██   ██   ██   ██   ▒▒   ██   ▒▒   ▒▒   ▒▒   ██   ██

██ = objectif construit/atteint dans le module     ▒▒ = entretenu, réinvesti     · = non concerné
```

**Lecture utile :** Excel n'est pas un tremplin jeté après le module 3 ; il reste entretenu jusqu'au projet final (le réflexe « je vérifie dans Excel ce que le dashboard affirme » est une compétence professionnelle réelle et rare). Python n'intervient pas avant M08, conformément à votre consigne de ne pas commencer par lui.

## C.3. Tableau de progression par module

| Module | Titre | Chap. | H | Niveau sortie | Outil principal | Projet de module | Évaluation | Palier |
|---|---|---|---|---|---|---|---|---|
| M01 | Lire les données, comprendre le métier | 7 | 30 | N0 → N1 | Explorateur de fichiers, Excel (lecture), LibreOffice | Analyser un petit fichier de ventes | Quiz 15 Q | P0 |
| M02 | Statistiques appliquées, depuis zéro | 8 | 30 | N1 | Calculette, Excel, Python (contrôle) | Profil statistique d'une boutique | Quiz 20 Q + étude de cas | P1 |
| M03 | Excel pour l'analyse de données | 8 | 30 | N1 → N2 | Excel 365 / 2021, LibreOffice Calc | Classeur de pilotage commercial | Quiz 15 Q + 4 exos + projet | P1 |
| M04 | Qualité, préparation, documentation | 6 | 30 | N2 | Excel, Power Query, conventions | Dossier de données propre + README | Quiz 15 Q + grille qualité | P1 |
| M05 | Chaîne de transformation (M/Q → SQL → pandas) | 5 | 30 | N2 | Power Query, DuckDB, pandas | Un nettoyage, trois outils, un rapport | Quiz 15 Q + comparatif | P1 |
| M06 | Bases de données relationnelles | 5 | 30 | N2 | SQLite/DuckDB, dbdiagram.io, PostgreSQL | Concevoir la base de la quincaillerie | Quiz 15 Q + schéma | P2 |
| M07 | SQL : interroger, agréger, rejoindre | 8 | 30 | N2 → N3 | DuckDB (CLI + Python), PostgreSQL, DBeaver | 30 questions métier en SQL | Quiz 20 Q + 35 requêtes | P2 |
| M08 | Python pour l'analyse de données | 8 | 30 | N2 → N3 | Python 3.13, Jupyter, pandas | Analyse complète d'un jeu inconnu | Quiz 15 Q + notebook | P2 |
| M09 | Analyse exploratoire (EDA) | 6 | 30 | N3 | pandas + matplotlib/seaborn + Excel | EDA guidée puis autonome | Quiz 15 Q + étude | P2 |
| M10 | Data visualization | 7 | 30 | N3 | matplotlib, Excel, Power BI | Refonte de 5 mauvais graphiques | Quiz 15 Q + grille visuelle | P3 |
| M11 | SQL avancé pour la BI | 7 | 30 | N3 | DuckDB, PostgreSQL, SQL Server | Analyses de cohortes et classements | Quiz 20 Q + cas | P4 (errata 24/09/2026) |
| M12 | Fondamentaux de la Business Intelligence | 6 | 30 | N3 | tous, vue d'ensemble | Chaîne brut → décision documentée | Quiz 15 Q + carte KPI | P4 (errata 24/09/2026) |
| M13 | Modélisation des données | 7 | 30 | N3 → N4 | dbdiagram, Power Pivot, SQL | Modèle en étoile + MCD complet | Quiz 15 Q + modèle | P4 |
| M14 | Power BI, de l'import à la publication | 8 | 30 | N4 | Power BI Desktop | Dashboard commercial pro (2 versions) | Quiz 15 Q + validation dashboard | P4 |
| M15 | DAX pour la BI | 7 | 30 | N4 | Power BI, DAX, Tabular Editor (lecture) | Bibliothèque de 40 mesures | Quiz 20 Q + mesures | P4 |
| M16 | Tableau et autres outils BI | 5 | 30 | N4 | Tableau Desktop Free, Looker Studio | Même dashboard dans 3 outils + arbitrage | Étude comparative notée | P4 |
| M17 | Automatisation du reporting | 6 | 30 | N4 | Power Query, Python, Power BI, tâches planifiées | Rapport hebdo sans intervention | Quiz 15 Q + démo de bout en bout | P4 |
| M18 | Analyses sectorielles | 7 | 30 | N4 | selon secteur | Un dossier sectoriel au choix | Étude de cas sectorielle | P4 |
| M19 | Analyse avancée : prévision, segmentation, scoring | 6 | 30 | N4 (+) | Python (scikit-learn), Excel | Prévision + segmentation commentées | Quiz 15 Q + rapport d'incertitude | P4 |
| M20 | Data storytelling & communication | 6 | 30 | N4 → N5 | PowerPoint/Slides, Power BI, Canva | Soutenance de 8 min + deck | Grille de soutenance /20 | P4 |
| M21 | Projets professionnels complets | 6 | 30 | N4 → N5 | tout le socle, en autonomie | 7 projets + **mission finale** | Grille mission /40 | P5 |
| M22 | Portfolio, emploi, feuille de route | 4 | 30 | N5 | GitHub, LinkedIn, PDF | Portfolio v1 + CV + lettre | Revue de portfolio notée | P5 |
| M23 | *R pour l'analyse* (option) | 5 | 15 | N4 | R, RStudio/Posit, dplyr, ggplot2 | Équivalent M09 en R | Quiz 12 Q | — |
| M24 | *Data engineering appliqué* (option) | 5 | 20 | N4 → N5 | DuckDB, dbt-core, Airflow Lite/Prefect, Git | Pipeline ETL/ELT versionné | Projet + revue de code | — |
| M25 | *Données ouvertes & cartographie* (option) | 4 | 15 | N4 | Python (geopandas), QGIS, Power BI carte | Atlas décisionnel d'une région | Atlas + note | — |

**Palier et phase — errata du 24 septembre 2026 (clôture de M11).** Ce tableau sert deux axes qu'il
ne faut pas confondre : la **phase** d'un module (bloc de progression, donnée par le §C.1, qui **fait
foi**) et le **palier** qu'il prépare (niveau de validation clos par une épreuve, §B.6 : 4 épreuves,
fin de P1, P2, P4 et P5). Les lignes **M11** et **M12** portaient le palier *P3*, hérité du premier
jet, alors que le §C.1 place **M11 à M15** en **phase 4** : le palier est corrigé en *P4*. La
**phase 3** (M10) reste *P3* ; en cas d'écart entre ce tableau et le §C.1, le **§C.1 fait foi**, et
c'est lui qui décide du rangement des modules dans les phases.

**Totaux vérifiés (le détail chapitre par chapitre de la partie D est le décompte de référence) :**

| agrégat | valeur | contrôle |
|---|---|---|
| Modules obligatoires | **22** (M01 → M22, dont 3 de la phase 6) | lignes M01 → M22 du tableau ci-dessus |
| Modules de spécialisation | **3** (M23–M25) | hors périmètre obligatoire |
| Sous-total modules obligatoires par phase | 1 · 2 · 6 · 1 · 5 · 4 · 3 = **22** | colonnes du tableau de la phase C.1 |
| Chapitres rédigés | **143** | somme de la colonne « Chap. » : 7+8+8+6+5+5+8+8+6+7+7+6+7+8+7+5+6+7+6+6+6+4 = **143** |
| Heures du parcours de base | **660 h** | somme de la colonne « H » : 22 modules × 30 h |
| Pages du manuel final | **≈ 2455** (intégral) / **≈ 1692** (condensé) / **747** (à la fin de M07) | budget module par module, §F.4, recomposé par `chap. × 12,5 + 17 d'appareil de module`, calibre mesuré sur M01 |
| Exercices / projets / évaluations | **180 / 32 / 23** | §E.4, §E.3, §B.6 |
| Options M23–M25 | 14 chapitres · 50 h · 226 p. | si activées : **157 chapitres · 710 h · 2681 p.**

---

# PARTIE D — PROGRAMME DÉTAILLÉ MODULE PAR MODULE

*Chaque module : objectifs · prérequis · chapitres (compétence visée par chapitre) · outils · projet · évaluation · acquis · transition. Les durées sont indicatives pour 10 h/semaine.*

## PHASE 0 — CULTURE NUMÉRIQUE & POSTURE PROFESSIONNELLE

### M01 — Lire les données et comprendre le métier de l'analyse — 7 chap. · 30 h
**Objectifs.** (1) Distinguer donnée, information, connaissance et décision. (2) Reconnaître la structure d'un fichier tabulaire sans l'ouvrir dans un logiciel spécialisé. (3) Employer correctement le vocabulaire de base (ligne, colonne, variable, observation, identifiant, type). (4) Situer le rôle d'un Data Analyst, d'un BI Analyst, d'un Data Scientist et d'un Data Engineer. (5) Décrire le cycle complet d'une analyse et savoir formuler une question analytique.
**Prérequis.** Aucun. Savoir allumer un ordinateur et utiliser une souris suffit ; le chapitre 1 prend en charge le reste.
**Notions abordées.** vos §MODULE 1, intégrales, plus : formats de fichiers, séparateurs, encodage de caractères, chemins de fichiers, notion de schéma, question analytique, cadrage d'une demande.

| Chap. | Titre | Compétence visée | Outil | H |
|---|---|---|---|---|
| M01.C01 | Se repérer dans un ordinateur de travail : dossiers, fichiers, extensions, chemins, sauvegardes | Ne plus jamais perdre un fichier ; comprendre `C:\Users\...\Documents` | Explorateur Windows | 4 |
| M01.C02 | Donnée, information, connaissance, décision | Formuler la différence avec des exemples de son propre environnement | — (papier) | 3 |
| M01.C03 | La table : lignes, colonnes, cellules, en-têtes, identifiants | Lire une table et la décrire en langage clair | Excel / LibreOffice | 5 |
| M01.C04 | Types de données et ce qu'ils autorisent (texte, nombre, date, booléen, montant) | Détecter une colonne "nombre stocké en texte" et expliquer le dégât | Excel | 5 |
| M01.C05 | Données structurées, semi-structurées, non structurées ; qualitatives et quantitatives | Classer 20 exemples réels | Excel, éditeur de texte | 4 |
| M01.C06 | Le cycle de vie d'une donnée : naissance, stockage, transformation, usage, archivage, suppression | Retracer le cycle d'une ligne de vente de sa caisse au rapport annuel | — (schéma) | 4 |
| M01.C07 | Les métiers de la donnée, la chaîne de valeur, et l'anatomie d'une analyse | Écrire une question analytique correcte à partir d'une demande floue | traitement de texte | 5 |

**Exemples pratiques.** Le ticket de caisse d'une quincaillerie de Ouagadougou décortiqué ; un relevé d'électricité ; un carnet de stocks écrit à la main ; un fichier de 12 000 lignes livré par un fournisseur et « qui ne marche pas » (le grand classique du point-virgule et du CSV).
**Projet M01.P — « Un petit fichier de ventes, une première fois ».** 489 lignes de ventes d'un magasin (dont 9 en trop, à découvrir). Livrables : (1) fiche d'identité du fichier (colonnes, types, bornes, anomalies perçues) ; (2) trois questions que l'on peut lui poser ; (3) une réponse chiffrée obtenue sans autre outil que le tri/filtre Excel ; (4) une page « ce que je ne sais pas encore faire ».
**Évaluation.** Quiz de 15 questions (dont 4 pièges de vocabulaire : « *une donnée est une information* — vrai/faux ») ; 4 exercices E1/E2 ; étude de cas « Le patron veut savoir des choses » (cadrage de 5 demandes en questions analytiques) ; corrigés en 9 pages.
**Compétences acquises.** Vocabulaire fondamental ; hygiène de fichiers ; lecture d'un fichier tabulaire ; question analytique cadrée. **Niveau : N1.**
**Transition.** « Vous savez lire une donnée. Vous ne savez pas encore la résumer honnêtement. Le module 2 vous donne les outils du résumé : sans lui, tout le reste du parcours produirait des chiffres faux avec assurance. »

## PHASE 1 — FONDATIONS ANALYTIQUES

### M02 — Statistiques appliquées, depuis zéro — 8 chap. · 30 h
**Objectifs.** (1) Calculer et surtout *interpréter* les indicateurs de position et de dispersion. (2) Choisir moyenne ou médiane selon la forme des données. (3) Détecter une valeur aberrante et décider quoi en faire. (4) Lire une distribution. (5) Comprendre la corrélation **et son principal malentendu : la causalité**. (6) Evaluer la solidité d'un résultat sur échantillon (intervalle de confiance, test simple) et expliquer l'incertitude à un non-statisticien.
**Prérequis.** M01 (table, types, colonnes). Arithmétique de base. Aucune autre statistique.
**Vos 23 notions statistiques** sont intégralement couvertes, chacune en 7 temps (définition simple, explication intuitive, formule, exemple numérique, interprétation, usage professionnel, exercice).

| Chap. | Titre | Vos notions couvertes | H |
|---|---|---|---|
| M02.C01 | Population, échantillon, individu, variable, modalité, fréquence | population · échantillon · variable · fréquence | 4 |
| M02.C02 | Centres : moyenne, médiane, mode ; minimum, maximum, étendue | moyenne · médiane · mode · min · max · étendue | 4 |
| M02.C03 | Dispersion : variance, écart-type, coefficient de variation, IQR | variance · écart-type | 4 |
| M02.C04 | Positions : quartiles, déciles, percentiles, lecture du boxplot | quartiles · percentiles | 3 |
| M02.C05 | Formes : distribution, histogramme, asymétrie, valeurs extrêmes | distribution | 4 |
| M02.C06 | Relations : covariance, corrélation, causalité, paradoxes usuels | corrélation · covariance | 4 |
| M02.C07 | Hasard et incertitude : probabilités de base, échantillonnage, biais | probabilités de base · échantillonnage | 4 |
| M02.C08 | Décider avec incertitude : intervalle de confiance, tests (t-test, chi²), interprétation et limites | intervalles de confiance · tests statistiques · interprétation statistique | 3 |

**Démonstrations phares.** (a) Le même tableau de ventes (extrait nettoyé de 480 lignes, 316 tickets) donne un panier de **114 156 FCFA en moyenne** et de **58 423 FCFA en médiane** — 71,8 % des tickets sont sous la moyenne : pourquoi, et lequel montrer au directeur ? *(chiffres mesurés par `scripts/chiffres_manuel.py`, bloc M02 ; les valeurs annoncées ici avant rédaction étaient des ordres de grandeur provisoires)* (b) Un t-test entre deux magasins, exécuté en Excel *puis* vérifié en Python, avec l'interprétation en français. (c) La corrélation trompeuse entre ventes de parapluies et accidents de moto en saison des pluies.
**Projet M02.P — « Profil statistique de la Boutique Kwame ».** 1 500 ventes. Livrable : une page par indicateur (valeur, calcul, ce que ça dit, ce que ça ne dit pas) + 3 anomalies chiffrées + conclusion en 5 lignes.
**Évaluation.** Quiz 20 Q (calcul mental + interprétation) ; 5 exercices pratiques dont un E4 « ce tableau de statistiques contient 3 erreurs » ; étude de cas « le rapport mensuel contredit la médiane » ; corrigés pas à pas avec les calculs intermédiaires.
**Compétences acquises.** Mesurer un phénomène, résumer honnêtement, repérer l'abus de moyenne, douter utilement. **Niveau : N1 → N2.**
**Transition.** « Les statistiques vous disent *quoi* mesurer. Il faut maintenant un instrument. Votre premier instrument est le logiciel que votre futur employeur a déjà installé : Excel. »

### M03 — Excel pour l'analyse de données — 8 chap. · 30 h
**Objectifs.** (1) Maîtriser l'interface et la mécanique des formules. (2) Construire 15 fonctions-clés du métier d'analyste avec leur syntaxe, exemples, cas réels et erreurs. (3) Produire des tableaux croisés dynamiques et des graphiques fiables. (4) Préparer et charger des données avec Power Query. (5) Construire un modèle de données avec Power Pivot et des mesures DAX minimales.
**Prérequis.** M01.C01–C04 ; M02 (pour les TCD statistiques).
**Version de référence.** Excel pour Microsoft 365 (canal courant, septembre 2026), avec équivalents pour Excel 2021/2019 et LibreOffice Calc. Les fonctions récentes non disponibles en 2019 sont signalées par un pictogramme de version ; le manuel n'emploie aucune fonction qui n'existerait pas en 2021 sans le dire.

| Chap. | Titre | Contenu contractuel (vos §Module 3) | H |
|---|---|---|---|
| M03.C01 | Interface, classeur/feuille/cellule, plage, navigation, sélection rapide | interface · feuilles · cellules · lignes · colonnes | 3 |
| M03.C02 | Formats et saisie intelligente : monétaire FCFA, dates, texte vs nombre, validation de données, mise en forme conditionnelle | formats | 4 |
| M03.C03 | Le tableau structuré `Ctrl+L`, tri, filtres, rechercher, supprimer les doublons | tableaux · tri · filtres | 4 |
| M03.C04 | La formule : référence relative/absolue/mixte, `=`, erreurs `#VALUE!`, `#N/A`, `#DIV/0!`, `#RÉF!` | formules · références relatives et absolues | 4 |
| M03.C05 | Boîte à fonctions d'agrégation et conditionnelle : SOMME, MOYENNE, NB, NBVAL, MAX/MIN, MEDIANE, QUARTILE.INC, SOMME.SI.ENS, NB.SI.ENS, MOYENNE.SI.ENS | fonctions statistiques · fonctions conditionnelles | 4 |
| M03.C06 | Rechercher et assembler : RECHERCHEV (et ses 4 pièges), **RECHERCHEX**, INDEX/EQUIV, DECALER/INDIRECT (comprendre, éviter), CONCAT/JOINDRE.TEXTE, GAUCHE/DROITE/SUBSTITE/EFFACERE/STXT, NBCAR | fonctions de recherche · fonctions texte | 4 |
| M03.C07 | Dates, durées, périodes : `DATE`, `AUJOURDHUI`, `MOIS`, `ANNEE`, `JOUR`, `FIN.MOIS`, `DATEDIF`, `NB.JOURS.OUVRES`, moyenne glissante ; puis les fonctions matricielles dynamiques `FILTRE`, `TRIBY`, `UNIQUE`, `LET`, `SÉQUENCE` — **exigées par Microsoft 365 seulement**, d'où la règle de la fiche double : la voie moderne, plus la variante accessible à Excel 2021 et à LibreOffice | fonctions date · fonctions dynamiques | 4 |
| M03.C08 | TCD, segments, graphiques, Power Query, Power Pivot, DAX de survie, protections, automatisation (enregistrements de macro → limites, Python dans Excel) | TCD · graphiques · segments · Power Query · Power Pivot · modèle de données · DAX · automatisation | 3 (hors exercices) |

**Fiches de fonction (26 au total), format imposé par votre §3 :** nom et version · syntaxe (avec les noms anglais entre parenthèses, car beaucoup d'installations sont en anglais) · explication de chaque argument · exemple sur le jeu du fil rouge · cas réel d'entreprise · erreur fréquente et son symptôme · exercice. Exemple du contrat de fiche pour `RECHERCHEX` : 1 page, 4 pièges listés (valeurs multiples, ordre des colonnes, textes avec espaces invisibles, `#N/A` propagé), 2 exercices, corrigé.
**Projet M03.P — « Le classeur de pilotage de Sahel Distribution ».** Un fichier de ventes + un fichier de targets : classeur à 3 feuilles (données préparées, calculs, tableau de bord TCD + 4 graphiques + 3 segments), formaté, protégé, nommé, documenté. **C'est la 1re pièce du portfolio.**
**Évaluation.** Quiz 15 Q (dont reconnaître la bonne formule d'une erreur affichée) ; 4 exercices pratiques dont un E4 « ce classeur donne 3 chiffres faux, trouvez pourquoi » ; étude de cas commerciale ; corrigés.
**Compétences acquises.** Excel du niveau *utiliseur expert local*, premier artefact professionnel présentable. **Niveau : N2.**
**Transition.** « Excel est votre instrument de travail, pas votre méthode. La méthode, la voici : avant de calculer quoi que ce soit, il faut rendre la donnée digne de confiance. »

## PHASE 2 — MAÎTRISE OPÉRATIONNELLE

### M04 — Qualité, préparation et documentation des données — 6 chap. · 30 h
**Objectifs.** (1) Diagnostiquer un jeu de données avec une grille reproductible. (2) Décider, traiter et **documenter** chaque défaut. (3) Normaliser, standardiser, créer des variables. (4) Contrôler la qualité après transformation (et prouver qu'on n'a pas cassé les totaux). (5) Instaurer les réflexes pro : arborescence, nommage, README, journal de transformation, confidentialité, versionnage.
**Prérequis.** M02, M03 (C01–C06).
**C'est le module qui absorbe vos exigences §4 « Nettoyage et préparation » (volet discipline) et §12 « Bonnes pratiques professionnelles ».**

| Chap. | Titre | Compétence visée | H |
|---|---|---|---|
| M04.C01 | Le diagnostic en 12 points : complétude, unicité, validité, cohérence, exactitude, actualité, conformité | Exécuter un diagnostic en 45 min sur un fichier inconnu | 6 |
| M04.C02 | Données manquantes : 5 mécanismes d'absence, 5 traitements (ignorer, signaler, imputer, supprimer, modéliser), choix argumentés | Justifier son traitement de l'absence au lieu de le subir | 5 |
| M04.C03 | Doublons et identifiants : vrai vs faux doublon, clé candidate, fusion de fichiers mal appariés | Résoudre un "dé-duplication" avec dictionnaire de correspondance | 5 |
| M04.C04 | Valeurs aberrantes et incohérences : seuils métier, IQR, z-score, règles croisées, erreurs de saisie, formats et unités | Écrire une règle de contrôle réutilisable | 5 |
| M04.C05 | Normalisation et transformations : casse, accents, espaces, majuscules, formats de date locaux, devises, pourcentages, découpage/fusion de colonnes | Rendre deux fichiers comparables | 4 |
| M04.C06 | Documentation, nommage, reproductibilité, contrôle de cohérence final, confidentialité et sécurité (données personnelles, RGPD/loi locale, anonymisation) | Produire un README et un dossier de données recevables | 5 |

**Projet M04.P — « Le dossier de données ».** Un zip livré volontairement pourri (7 défauts de natures différentes, dont 2 qui fausseront vos totaux si vous les traitez à la va-vite). Livrable : `ventes_propres.csv` + `README.md` + `journal_des_transformations.md` + `rapport_qualite.md` (tableau des défauts : comptés, traités, restants).
**Évaluation.** Quiz 15 Q ; 3 exercices dont un E4 ; étude de cas « le stock indiqué est-il crédible ? » ; grille qualité à cocher notée sur 20 ; corrigés détaillés avec les mauvais choix commentés.
**Compétences acquises.** La compétence la plus demandée du métier, la moins enseignée en ligne. **Niveau : N2.**
**Transition.** « Vous savez dire *ce qui ne va pas*. Reste à le faire, efficacement, et à choisir l'outil. »

### M05 — Chaîne de préparation : Power Query, SQL, pandas en miroir — 5 chap. · 30 h
**Objectifs.** (1) Réaliser le même nettoyage dans trois outils et comparer coût/bénéfice. (2) Choisir l'outil selon la volumétrie, la nature et l'interlocuteur. (3) Maîtriser les primitives communes : importer, pivoter/dépivoter, fusionner (jointure), agréger, créer une colonne, charger.
**Prérequis.** M04. Réponse explicite à votre consigne : « Explique quel outil choisir selon la taille et la nature des données. »

| Chap. | Titre | Contenu | H |
|---|---|---|---|
| M05.C01 | Le langage commun des transformations : 10 opérations, leurs noms dans chaque outil | tableau de correspondance *Power Query — SQL — pandas — Excel* | 5 |
| M05.C02 | Power Query : source, étapes, types, dépivotage, fusion, agrégation, requêtes paramétrées, M sans complexe | le ETL du pauvre, le plus rentable du parcours | 7 |
| M05.C03 | SQL pour transformer : `INSERT…SELECT`, `CREATE TABLE AS`, `WITH`, nettoyage dans la requête, chargement en base | préparation reproductible côté base | 7 |
| M05.C04 | pandas pour transformer : chaîne de transformations, `pipe`, `assign`, `query`, `melt`/`pivot`, `merge`, `groupby` | préparation scriptée, versionnable | 7 |
| M05.C05 | Arbitrer : tableau de décision « taille du fichier × fréquence × compétences de l'équipe × gouvernance → outil », et le cas des 1 million de lignes | dire « non » à Excel ou « pas encore » à Python | 4 |

**Cas comparé fil rouge.** 1 fichier → 3 méthodes → 3 livrables → 1 verdict documenté (temps passé, robustesse à l'arrivée du fichier du mois suivant, lisibilité pour un collègue).
**Projet M05.P — « Trois chemins, une même table propre ».** 120 000 lignes, 9 défauts. Livrables : requête Power Query, script SQL, notebook pandas, tous produisant un `df_final` identique **au centime près** (contrôle automatisé fourni).
**Évaluation.** Quiz 15 Q ; 2 exercices par outil ; étude de cas « on me donne 8 Go de logs » ; corrigés.
**Niveau : N2.** **Transition.** « Tout cela suppose que la donnée est quelque part. Le plus souvent, elle est dans une base de données — et la clé d'entrée s'appelle SQL. »

### M06 — Bases de données relationnelles : comprendre avant de requêter — 5 chap. · 30 h
**Objectifs.** (1) Comprendre ce qu'est une base et un SGBD, ce qu'ils résolvent, et ce qu'ils coûtent. (2) Passer d'un tableur à un schéma relationnel. (3) Clé primaire, clé étrangère, contraintes, intégrité référentielle. (4) Créer, alimenter et interroger une base réelle. (5) Choisir PostgreSQL, SQLite, DuckDB, MySQL, SQL Server selon la situation.
**Prérequis.** M01.C03, M04.

| Chap. | Titre | Notions | H |
|---|---|---|---|
| M06.C01 | Pourquoi une base et pas un classeur Excel : redondance, anomalie de mise à jour, concurrence, volumétrie, sécurité | base de données · SGBD | 5 |
| M06.C02 | Table, colonne, ligne, schéma, type, contrainte, valeur nulle (et `NULL` ≠ 0 ≠ vide) | table · colonne · ligne · schéma | 6 |
| M06.C03 | Clés et relations : primaire, étrangère, candidate, composite, 1-1, 1-N, N-M + table de jointure | clé primaire · clé étrangère · relation | 7 |
| M06.C04 | Installer et vivre avec DuckDB / SQLite / PostgreSQL : créer, insérer, importer un CSV, se connecter avec un client graphique | SGBD en pratique | 7 |
| M06.C05 | Les autres mondes : NoSQL (document, clé-valeur), datalake, entrepôt, lac, ce qui importe pour un analyste | paysage, vocabulaire d'entretien | 5 |

**Projet M06.P — « La base de la quincaillerie ».** À partir d'un export de caisse unique et dénormalisé (1 table de 42 colonnes), concevoir et créer 7 tables reliées, avec contraintes, importer 24 000 ventes, et prouver par 3 requêtes de contrôle que l'intégrité tient.
**Évaluation.** Quiz 15 Q ; 2 exercices de modélisation papier ; étude de cas « l'école veut tout dans une seule feuille » ; corrigés.
**Niveau : N2.** **Transition.** « La base existe. Apprenons à lui parler. »

### M07 — SQL : interroger, agréger, rejoindre — 8 chap. · 30 h
**Objectifs.** Écrire, en autonomie, toute requête SQL de niveau analyste : filtrer, agréger, grouper, trier, rejoindre, imbriquer, comparer. Lire et corriger la requête d'un autre.
**Prérequis.** M06 (indispensable), M02 (agrégats), M04 (qualité des résultats).
**Dialecte de référence.** ANSI SQL avec DuckDB/PostgreSQL ; les écarts SQL Server et MySQL sont signalés dans des encadrés — un professionnel rencontre les trois.

| Chap. | Titre | Vos mots-clés | H |
|---|---|---|---|
| M07.C01 | Le premier contact : `SELECT`, `FROM`, alias, `DISTINCT`, `LIMIT`, l'ordre réel d'exécution (la clé de tout) | SELECT · DISTINCT · LIMIT | 4 |
| M07.C02 | Filtrer : `WHERE`, opérateurs, `IN`, `BETWEEN`, `LIKE`, `IS NULL`, dates, priorités logiques | WHERE | 4 |
| M07.C03 | Trier, limiter, paginer : `ORDER BY`, multi-clés, tri par alias, première/dernière valeur par groupe | ORDER BY | 3 |
| M07.C04 | Agréger : `COUNT`/`COUNT(*)`/`COUNT(DISTINCT)`, `SUM`, `AVG`, `MIN`, `MAX`, `NULL` et moyennes, `ROUND` | fonctions d'agrégation | 4 |
| M07.C05 | Résumer par groupe : `GROUP BY`, ce qui est autorisé dans `SELECT`, `HAVING` vs `WHERE`, comptages conditionnels | GROUP BY · HAVING | 4 |
| M07.C06 | Catégoriser en SQL : `CASE` simple et recherché, entonnoirs, tranches de prix, `COALESCE`, `NULLIF` | CASE | 3 |
| M07.C07 | Joindre : `INNER`, `LEFT`/`RIGHT`, `FULL`, `CROSS`, auto-jointure, jointure multiple, les 4 symptômes de l'explosion de lignes, `UNION` | JOIN | 5 |
| M07.C08 | Structurer : sous-requêtes (scalaire, `IN`, `FROM`), CTE (`WITH`), vues, `EXISTS` vs `IN`, style et lisibilité | sous-requêtes · CTE · vues · bonnes pratiques | 4 |

**Le « pourquoi » imposé par votre §3, exemple :** la fiche `GROUP BY` du manuel commence par « *GROUP BY permet de regrouper les lignes qui partagent une caractéristique afin de produire un résumé. Une entreprise a 10 000 ventes individuelles ; GROUP BY calcule le chiffre d'affaires par ville* », puis montre l'exécution sur `sahel_ventes`, puis **les 5 erreurs de débutant** (colonne non agrégée non regroupée, `HAVING` avec une colonne brute, comptage d'une jointure multiple qui double les lignes, `DISTINCT` utilisé pour masquer un mauvais `JOIN`, `GROUP BY` sur une date minute par minute).
**Optimisation** : son traitement est délibérément limité à un chapitre de *sensibilisation* dans M11 (`EXPLAIN`, index, colonnes inutiles), parce que l'optimisation suppose un SGBD administré qu'un débutant n'a pas ; c'est une amélioration assumée de votre §5, détaillée en §H.3.
**Projet M07.P — « La base commerciale d'une chaîne de 5 magasins ».** 30 questions métier croissantes, dont 6 "pièges de fiabilité" où la réponse juste exige de repérer un doublon. Livrable : un fichier `.sql` commenté + une note de 1 page « les trois questions que je ne peux pas trancher ».
**Évaluation.** Quiz 20 Q ; 35 exercices de requêtes auto-validés par script ; étude de cas d'audit (« le directeur financier conteste le total mars ») ; corrigés ligne à ligne.
**Compétences acquises.** SQL de niveau analyste, base du métier. **Niveau : N2 → N3.**
**Transition.** « SQL vous donne le chiffre. Python vous donne la méthode, la vitesse, et la capacité de refaire tout cela en une seconde le mois prochain. »

### M08 — Python pour l'analyse de données — 8 chap. · 30 h
**Objectifs.** (1) Comprendre la programmation sans bagage : ce qu'est un langage, un interpréteur, un environnement, un paquet. (2) Manipuler les structures et écrire les 6 constructions de contrôle. (3) Maîtriser pandas pour importer, nettoyer, filtrer, agréger, joindre. (4) Produire des graphiques et des statistiques. (5) Écrire un script réutilisable et reproductible.
**Prérequis.** M04, M05.C04 (ou grande aisance Excel), M07 (le parallèle SQL/pandas est utilisé volontairement comme accélérateur d'apprentissage).
**Version de référence.** Python 3.13+, pandas **3.x** (sorti en janvier 2026, avec le type texte dédié, le comportement *copy-on-write* et les changements d'API qui en découlent). **Décision de conception importante :** le manuel enseigne les patterns valides en pandas 2.3 *et* 3.x, signale explicitement les 12 écritures obsolètes à ne plus reproduire (dont les alias de périodes, les usages de `inplace`, les affectations chaînées), et fournit une annexe « migration ». Un manuel qui ignorerait pandas 3 serait faux dès sa parution — cf. §F.2 et §G.4.

| Chap. | Titre | Contenu | H |
|---|---|---|---|
| M08.C01 | Installer sans stress : Python, `pip`, environnements virtuels / uv, VS Code et Jupyter, exécuter son premier script | installation · environnement | 4 |
| M08.C02 | Les fondations sans données : variables, types, opérateurs, entrées/sorties, commentaires, erreurs | variables · types | 4 |
| M08.C03 | Décider et répéter : `if/elif/else`, boucles `for`/`while`, `break`/`continue`, compréhensions | conditions · boucles | 4 |
| M08.C04 | Ranger : listes, tuples, chaînes, **dictionnaires**, ensembles, index, tris | listes · dictionnaires | 3 |
| M08.C05 | Organiser : fonctions, arguments par défaut/nommés, portée, docstring, modules et paquets, exceptions `try/except`, fichiers CSV/Excel/JSON | fonctions · fichiers · exceptions · modules | 5 |
| M08.C06 | NumPy utile et suffisant : tableaux, vecteurisation, statistiques, `nan`, conditions `where`, broadcasting | NumPy | 3 |
| M08.C07 | pandas I : `Series`, `DataFrame`, `read_csv`/`read_excel`, sélection `loc`/`iloc`, filtres, nouvelles colonnes, `describe`, valeurs manquantes | importation · nettoyage · filtrage | 5 |
| M08.C08 | pandas II : `groupby`/`agg`/`transform`, `merge`, `pivot_table`, dates, périodes, `apply`, export Excel avec mise en forme | regroupement · jointures · statistiques · automatisation | 3 (hors exercices) |

**Contrat pédagogique.** Chaque notion = une question métier du fil rouge + un bloc de code + sa **sortie réelle imprimée** (jamais « le résultat est… » sans le texte de sortie). Exemple : `df.groupby("magasin")["montant"].agg(["sum","count","mean"]).round(0)`, avec le `DataFrame` tel qu'il s'affiche, puis l'interprétation en une phrase, puis l'équivalent SQL côte à côte.
**Projet M08.P — « Le script qui fait le travail de trois matinées ».** Analyse complète d'un jeu inconnu : import → audit → nettoyage → indicateurs → 4 graphiques → export d'un classeur de synthèse, le tout dans un script commenté exécuté d'une traite. **2e pièce du portfolio.**
**Évaluation.** Quiz 15 Q (dont lire et prédire la sortie d'un court programme) ; 5 exercices ; un E4 « ce script tourne mais ses chiffres sont faux » ; étude de cas ; corrigés avec les messages d'erreur commentés (apprendre à lire une traceback est un objectif pédagogique à part entière, traité en M08.C05).
**Niveau : N3 en devenir.** **Transition.** « Vous savez produire des chiffres par trois chemins. Rien ne garantit encore qu'ils racontent une histoire vraie. »

### M09 — Analyse exploratoire de données (EDA) — 6 chap. · 30 h
**Objectifs.** Appliquer une méthode de 10 étapes (exactement votre liste §MODULE 7) à un jeu de données inconnu, et en tirer des conclusions provisoires correctement exprimées.
**Prérequis.** M02 (statistiques), M08 (pandas) ; M05/M07 utiles.

| Chap. | Titre | Vos 10 étapes | H |
|---|---|---|---|
| M09.C01 | Le protocole en 10 étapes, la « fiche d'entrée » d'une analyse et le temps à y consacrer | étapes 1–2 (inspecter, comprendre les variables) | 5 |
| M09.C02 | Audit et premières statistiques, cadrage des hypothèses | 3–4 (problèmes, statistiques) | 5 |
| M09.C03 | Tendances : séries temporelles simples, saisonnalité, comparaisons de périodes | 5 (tendances) | 5 |
| M09.C04 | Anomalies et raretés : ce qui est inhabituel, comment le prouver, quoi en conclure | 6 (anomalies) | 5 |
| M09.C05 | Relations et hypothèses : corrélation, segments, comparaison de groupes, pièges d'inférence | 7–8 (relations, hypothèses) | 5 |
| M09.C06 | Visualisations d'exploration et conclusions provisoires, note d'EDA | 9–10 (visualisations, premières conclusions) | 5 |

**3 études de cas complètes et contrastées.** (1) Ventes d'une quincaillerie (fil rouge) ; (2) données d'un centre de santé (fréquentation, ruptures de stock de médicaments essentiels) ; (3) résultats scolaires d'un établissement avec absentéisme. Chacune conduite pas à pas, puis rejouée par l'apprenant sur une variante.
**Projet M09.P — « 3 heures avec un fichier que personne n'a regardé ».** Chronomètre imposé : c'est la condition pour apprendre à ne pas explorer sans fin.
**Évaluation.** Quiz 15 Q ; étude de cas notée sur la qualité des *questions* posées autant que des réponses ; corrigés. **Niveau : N3.**
**Transition.** « Vos résultats sont justes. S'ils sont illisibles, ils ne serviront à rien. »

## PHASE 3 — COMMUNICATION ANALYTIQUE

### M10 — Data visualization — 7 chap. · 30 h
**Objectifs.** (1) Choisir un graphique par **question**, pas par esthétisme. (2) Appliquer les principes de perception. (3) Construire un titre, des axes, une légende, une annotation qui font gagner du temps au lecteur. (4) Éliminer les 10 erreurs qui faussent ou noient le message. (5) Structurer un récit visuel pour décideur.
**Prérequis.** M09 ; notions de couleurs et de mise en page sans prérequis graphique.

| Chap. | Titre | Contenu (vos §MODULE 8) | H |
|---|---|---|---|
| M10.C01 | Comment l'œil lit un graphique : l'ordre perceptuel (position > longueur > angle > surface > couleur), ce que ça prescrit | perception visuelle | 4 |
| M10.C02 | Le tableau de correspondance question → graphique : les 11 graphiques de votre liste, et 5 autres utiles | choix du graphique ; histogramme, barres, courbe, camembert, nuage, boxplot, heatmap, carte, waterfall, funnel, combiné | 6 |
| M10.C03 | Couleurs, palettes, accessibilité (daltonisme, contraste), FCFA et formats numériques, culture locale des couleurs | couleurs | 4 |
| M10.C04 | Titres qui parlent, axes honnêtes, légendes, annotations, ordre des barres, hiérarchie visuelle | titres · axes · légendes · annotations | 4 |
| M10.C05 | Les erreurs qui tuent la crédibilité : ax truncated, double axe, 3D, camemberts, cumul de %, couleurs signifiant tout et rien, surcharge | erreurs fréquentes | 4 |
| M10.C06 | Storytelling visuel : composer une séquence, enchaîner écran → insight → décision | storytelling | 4 |
| M10.C07 | Mettre en œuvre : graphiques Excel, matplotlib/seaborn, Power BI, choix du support et de la résolution | transformation en livrable clair pour un décideur | 4 |

**Projet M10.P — « La refonte ».** 5 graphiques volontairement ratés d'un rapport existant sont fournis : les corriger, en expliquer chaque choix, et produire une version « direction » + une version « équipe opérationnelle » du même constat. **3e pièce du portfolio.**
**Évaluation.** Quiz 15 Q ; 3 exercices de choix argumentés (E3) ; étude de cas « ce graphique a déclenché une décision fausse » ; **grille d'évaluation visuelle en 18 points** utilisée ensuite dans tous les dashboards du parcours. **Niveau : N3.**
**Transition.** « Le graphique est la partie visible. Derrière, il y a une organisation, un modèle, des KPI, des décisions : c'est la Business Intelligence. »

## PHASE 4 — BUSINESS INTELLIGENCE

### M11 — SQL avancé pour la BI — 7 chap. · 30 h
**Objectifs.** Écrire les requêtes qui font la différence entre un débutant et un professionnel : fenêtres, cohortes, cumuls, classements, écarts, récapitulatifs multi-niveaux, et comprendre ce qui rend une requête lente.
**Prérequis.** M07 (tout), M06.C04, M02.

| Chap. | Titre | Contenu | H |
|---|---|---|---|
| M11.C01 | Fonctions de fenêtre, le concept : `OVER`, `PARTITION BY`, `ORDER BY`, et la différence avec `GROUP BY` | fonctions de fenêtre | 5 |
| M11.C02 | Rang, cumuls, décalages : `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`, `SUM() OVER`, `LAG`, `LEAD`, écarts et variations en % | top N par groupe, running totals, M-1 | 5 |
| M11.C03 | Séries temporelles en SQL : dates partielles, `date_trunc`, calendrier, comparaisons année sur année, mois glissants, absence de ventes | time intelligence avant l'heure | 4 |
| M11.C04 | Cohortes, rétenzione et récurrence : première/derière achat, panier, fréquence, RFM simplifié | analyses de fidélité | 4 |
| M11.C05 | Requêtes avancées : CTE récursives, `PIVOT`, `UNNEST`, `QUALIFY` (DuckDB), agrégats conditionnels, `GROUPING SETS`/`ROLLUP`/`CUBE` | tableaux croisés en SQL | 4 |
| M11.C06 | Vues, vues matérialisées, index, `EXPLAIN`, requêtes lentes, le coût des `SELECT *`, partitions : ce qu'un analyste doit savoir | optimisation de requêtes | 5 |
| M11.C07 | Style, lisibilité, conventions, tests de non-régression sur des requêtes, contrôle de cohérence entre 2 sources | bonnes pratiques SQL | 3 |

**Projet M11.P — « Les 12 rapports SQL de la cellule commerciale ».** Chaque rapport est une requête autonome, versionnée, testée (total contrôlé contre la source), commentée en français. Un livrable directement montrable en entretien.
**Évaluation.** Quiz 20 Q ; 5 exercices dont deux E4 sur requêtes erronées ; étude de cas « les 10 % de clients qui font 60 % du CA » ; 18 requêtes de validation auto-testées. **Niveau : N3.**
**Transition.** « Vous savez produire des chiffres fiables. La BI commence quand un responsable accepte de décider avec. »

### M12 — Fondamentaux de la Business Intelligence — 6 chap. · 30 h
**Objectifs.** (1) Définir la BI, sa place, ses acteurs, son économie réelle dans une PME. (2) Distinguer reporting, BI, data warehouse, data lake, self-service. (3) Concevoir un KPI, et une **carte de définition** qui empêche les débats de chiffres en réunion. (4) Comprendre l'architecture complète de la donnée au tableau de bord. (5) Réussir ou éviter l'échec typique d'un projet BI.
**Prérequis.** M09 (questions métier), M10 (support). Aucune compétence technique nouvelle.

| Chap. | Titre | Contenu (vos §MODULE 9) | H |
|---|---|---|---|
| M12.C01 | Définition de la BI, ce qu'elle n'est pas, la décision fondée sur les données, le coût d'une décision sans donnée | définition · rôle · data-driven | 5 |
| M12.C02 | Reporting vs BI : périodicité, exploration, interactivité, gouvernance ; les 4 régimes de question (quoi, pourquoi, quoi demain, que faire) | différence reporting/BI ; analyses descriptive, diagnostique, prédictive, prescriptive | 5 |
| M12.C03 | Métriques, dimensions, faits, granularité : le vocabulaire exact, et la différence entre indicateur opérationnel, tactique, stratégique | métriques · dimensions · faits · indicateurs | 5 |
| M12.C04 | Concevoir un KPI : la règle des 6 critères, la **carte de définition**, le contre-KPI, les effets pervers (un KPI mal choisi détruit ce qu'on veut protéger) | KPI | 5 |
| M12.C05 | L'architecture BI complète de bout en bout : source → extraction → stockage → modèle → semantic layer → visualisation → diffusion ; données brutes → préparation → modèle → KPI → tableau de bord → décision (votre exemple complet) | architecture BI | 5 |
| M12.C06 | Réussir le projet BI : parties prenantes, cahier des charges, conduite, adoption, maintenance ; les 10 causes d'échec et comment les détecter | gestion · adoption | 5 |

**Projet M12.P — « Le tableau de bord que personne n'ouvrait ».** Étude d'un dispositif réel raté (fourni en 12 pages) ; diagnostic puis plan de reprise. Livrable : une **carte de définition de 10 KPI** du commerce de gros (CA, marge brute, taux de rupture, rotation de stock, panier moyen, taux de retour, taux de service, taux de recouvrement, coût logistique unitaire, part de marché interne), chacun avec formule, source, granularité, fréquence, responsable, seuil d'alerte, contre-KPI. Ce livrable est réutilisé intégralement dans M13, M14, M15, M21. **C'est le document signature du manuel.**
**Évaluation.** Quiz 15 Q ; 2 exercices de rédaction de KPI ; étude de cas « la direction veut un dashboard, elle a déjà tort de le vouloir comme ça » ; corrigés. **Niveau : N3.**
**Transition.** « Un bon KPI sur un mauvais modèle donne un mauvais tableau de bord, vite. Le modèle décide de tout. »

### M13 — Modélisation des données — 7 chap. · 30 h
**Objectifs.** (1) Concevoir un modèle du simple au complexe. (2) Normaliser et dénormaliser en connaissance de cause. (3) Construire un modèle en étoile et un modèle en flocon pour la BI. (4) Préparer une table calendrier correcte. (5) Reconnaître les modèles qui font des faux totaux.
**Prérequis.** M06, M12, M11 (jointures et agrégats).

| Chap. | Titre | Contenu (vos §MODULE 10) | H |
|---|---|---|---|
| M13.C01 | Modéliser : entités, attributs, relations, cardinalités ; modèle conceptuel, logique, physique ; le passage du tableur au modèle | MCD · MLD · MPD · entités · attributs · relations · cardinalités | 5 |
| M13.C02 | Normaliser 1FN → 3FN → FNSI, et les 4 anomalies évitées ; quand ne pas normaliser | normalisation · dénormalisation | 5 |
| M13.C03 | La dimension analytique : granularité, additionnabilité, faits sans additive ; le théorème du « ne jamais mélanger les grains » | table de faits · grain | 5 |
| M13.C04 | Le schéma en étoile : dimensions conformed, attributs de dimensions, hiérarchies, lenteurs de changement (SCD type 0/1/2/3) avec exemples clients et prix | schéma en étoile · dimensions · SCD | 5 |
| M13.C05 | Le schéma en flocon et ses variantes (fact-table multiple, bridge table pour N-M, junk dimension) ; quand dénormaliser exprès pour Power BI | modèle en flocon | 4 |
| M13.C06 | Temps et calendrier : `dim_date`, années fiscales, semaines commerciales, jours fériés locaux, la règle « une seule table date par modèle » | calendrier | 3 |
| M13.C07 | Qualité du modèle, documentation du schéma, impacts sur les performances et sur la justesse des DAX, revue de modèle avec une grille de 15 points | contrôle qualité du modèle | 3 |

**Illustrations prévues (vos §18).** 9 diagrammas à produire : (1) ticket de caisse → table plate → étoile, en 3 panneaux ; (2) anomalie de mise à jour avant/après normalisation ; (3) les 4 types de SCD dessinés sur la frise d'un changement de prix ; (4) étoile vs flocon côte à côte sur le même besoin ; (5) les 3 modes d'additionnabilité d'un fait ; (6) explosion de lignes illustrée sur 6 lignes de données ; (7) grain d'un fait et ses conséquences ; (8) architecture complète d'un SI décisionnel de PME ; (9) revue de modèle annotée « 5 défauts à trouver ».
**Projet M13.P — « Le modèle de Sahel Distribution ».** Livrable : MCD + MLD + script de création SQL + modèle Power BI importé + document de 3 pages justifiant chaque choix. **4e pièce du portfolio.**
**Évaluation.** Quiz 15 Q ; 2 exercices de normalisation ; étude de cas « 3 tableaux reliés donnent un CA faux de 40 % » ; corrigés. **Niveau : N3 → N4.**
**Transition.** « Le modèle est bon. Il faut maintenant l'outil qui le fait vivre devant les utilisateurs : Power BI. »

### M14 — Power BI : de l'import à la publication — 8 chap. · 30 h
**Objectifs.** Construire, seul, un dispositif complet et propre : import, Power Query, modèle, mesures, pages, filtres, navigation, publication, actualisation, gouvernance minimale.
**Prérequis.** M05.C02 (Power Query), M13 (modèle), M12 (KPI), M10 (visuel).
**État de l'art pris en compte (septembre 2026).** Power BI Desktop reste **gratuit** pour créer localement ; **le partage nécessite une licence** : Pro ou Premium Per User par utilisateur, ou une capacité Microsoft Fabric **F64 ou plus** pour que des utilisateurs en licence gratuite consultent — les SKUs capacity « P » de l'ancienne offre Premium ne sont plus commercialisés. Power BI s'inscrit dans la plateforme **Microsoft Fabric** (Data Factory, Synapse, OneLake) : le manuel l'explique en M12.C05 et M17, sans exiger de licence pour apprendre. Fonctions récentes enseignées là où elles ont du sens : édition des modèles sémantiques dans le service et vue TMDL (disponibles en GA), **fonctions utilisateur DAX (UDF)** et **calendriers améliorés** (Enhanced DAX Time Intelligence), Direct Lake — chacune signalée comme « récent : vérifiez la disponibilité dans votre version », avec la marche à suivre pour activer une fonction en aperçu. Le rapport paginé sur site relève désormais de **Power BI Report Server**, qui a absorbé SSRS (cf. §C.4).

| Chap. | Titre | Contenu (vos §MODULE 11) | H |
|---|---|---|---|
| M14.C01 | Installer, comprendre l'écosystème Desktop / Service / Fabric / Mobile, créer un compte, ce qui est gratuit et ce qui ne l'est pas, les alternatives si l'organisation n'a pas de licence | installation · interface · licences | 4 |
| M14.C02 | Obtenir la donnée : import, connecteurs, modes Import/DirectQuery/Live connection/Direct Lake, sources Excel/CSV/SQL/folders, la stratégie du cache | importation · actualisation | 4 |
| M14.C03 | Transformer avec Power Query dans Power BI : les 15 gestes, types, colonne conditionnelle, paramètres et fonctions, requêtes combinées, M utile, performances | Power Query · nettoyage · transformation | 4 |
| M14.C04 | Modéliser dans Power BI : relations, cardinalité, direction du filtrage, dates marquées, intégrité, le message « ambiguïté » et comment le guérir | relations · modèle de données | 4 |
| M14.C05 | Mesures vs colonnes calculées, le premier DAX de survie, `DIVIDE`, formatage, hiérarchie de l'ordre d'affichage, traductions | mesures · colonnes calculées · DAX (initiation) | 4 |
| M14.C06 | Construire les visuels : KPI carte, jauge, matrice, graphiques, mise en page, navigation, panneau de signets, boutons, volets, accessibilité, thèmes et charte graphique | visualisations · KPI | 4 |
| M14.C07 | Faire parler le rapport : filtres (page/visuel/au niveau), segments, synchronisation, interactions, drill-down, drill-through, info-bulles personnalisées, infobulle de synthèse, Q&A | filtres · segments · interactions · drill-down · drill-through · bookmarks | 4 |
| M14.C08 | Publier et faire vivre : espace de travail, application, partage et permissions, actualisation planifiée, passerelle, jeux de données réutilisables, sécurité au niveau des lignes, alertes, tests avant mise en production | publication · partage · actualisation · bonnes pratiques | 2 |

**Deux projets, comme promis :**
- **M14.P1 — « Dashboard commercial professionnel »** : à partir des 5 magasins du fil rouge, 3 pages (Direction, Commercial, Approvisionnement), 14 visuels, 4 segments, 2 pages de détail, 1 page d'aide à la lecture du dashboard, thème personnalisé, 10 mesures, actualisation automatisée documentée. Validé par la **grille de conception en 18 points** héritée de M10 et enrichie (performance, cohérence des totaux, accessibilité, légende, granularité, gestion des vides).
- **M14.P2 — « Version 2, après les retours des utilisateurs »** : le manuel fournit les 11 retours d'un faux comité ; l'apprenant doit arbitrer, prioriser et justifier ses refus. C'est l'exercice le plus proche de la réalité professionnelle du module.
**Évaluation.** Quiz 15 Q ; 3 exercices pratiques (dont un E4 « ce dashboard affiche un total double ») ; étude de cas « le client ne comprend pas le dashboard » ; corrigés ; validation par grille auto.
**Niveau : N4.** **Transition.** « Vos mesures sont simples. Dès qu'il y a une date, un filtre, un pourcentage, le DAX simple devient faux. Le module suivant est celui qui sépare les tableaux de bord crédibles des tableaux de bord qui font perdre leur temps aux gens. »

### M15 — DAX pour la BI — 7 chap. · 30 h
**Objectifs.** Comprendre les **contextes** (la seule chose qu'il faille vraiment comprendre en DAX), puis construire des mesures correctes pour les cas réels : ratios, comparaisons temporelles, cumuls, pourcentages du total, top N, KPI conditionnels.
**Prérequis.** M14.C04–C05, M13.
**Promesse de progressivité (votre §MODULE 12) :** aucune mesure n'est écrite avec une fonction non encore expliquée. Les 15 fonctions enseignées sont un **socle** : `SUM`, `SUMX`, `COUNTROWS`, `COUNT`, `DISTINCTCOUNT`, `DIVIDE`, `CALCULATE`, `FILTER`, `ALL`, `ALLEXCEPT`, `RELATED`, `RELATEDTABLE`, `VAR`/`RETURN`, `SELECTEDVALUE`, `IF`/`SWITCH`. Les fonctions temporelles (`TOTALYTD`, `SAMEPERIODLASTYEAR`, `DATEADD`, `PARALLELPERIOD`, `DATESYTD`) sont introduites *après* `CALCULATE` et `FILTER`, jamais avant, parce que leur compréhension dépend du contexte de filtre.

| Chap. | Titre | Notions clés | H |
|---|---|---|---|
| M15.C01 | Deux façons de calculer : mesure ou colonne ? Et le contexte de ligne et le contexte de filtre, enfin expliqués avec de la poussière | contexte de ligne · contexte de filtre · mesures · colonnes calculées | 5 |
| M15.C02 | Agréger et itérer : `SUM` vs `SUMX`, `COUNTROWS`, `DISTINCTCOUNT`, `AVERAGEX`, `MAXX`, le piège des moyennes de moyennes | SUM · SUMX · COUNT · DISTINCTCOUNT | 4 |
| M15.C03 | `CALCULATE`, le cœur du langage : modifier le contexte de filtre, `FILTER`, `ALL`, `ALLEXCEPT`, `KEEPFILTERS`, les variables | CALCULATE · FILTER · ALL | 5 |
| M15.C04 | Naviguer dans le modèle : `RELATED`, `RELATEDTABLE`, le filtrage croisé, `USERELATIONSHIP`, les messages d'erreur fréquents | RELATED | 4 |
| M15.C05 | Le temps : la table calendrier, cumuls, comparaisons, glissants, jours ouvrés, et les nouveautés calendriers améliorées | fonctions temporelles · comparaison avec période précédente · cumul | 4 |
| M15.C06 | Les patterns de la mesure d'affaires : ratio, part du total, variation %, top N, seuils conditionnels, `SWITCH`, tri dynamique, info-bulle, KPI à 3 états | pourcentages · ratios · KPI complexes | 4 |
| M15.C07 | Bien écrire, mesurer, documenter : nommage `[CA brut]`, formatage, performance (`Performance Analyzer`, `DAX Studio` en lecture), colonnes calculées à éviter, UDF et groupes de calcul pour industrialiser, revue de mesures | bonnes pratiques | 4 |

**Chaque fonction = un cas professionnel réel** (votre §MODULE 12). Exemple du contrat : `DISTINCTCOUNT` enseigné par le problème « combien de clients ont réellement acheté en mars, alors que 4 100 lignes de vente ? » ; `ALL` enseigné par le besoin « afficher la part de chaque magasin dans le CA **de la sélection en cours** » avec les deux versions du dénominateur et le résultat différent affiché.
**Projet M15.P — « La bibliothèque de mesures ».** 40 mesures livrées, chacune avec : définition métier, code DAX, exemple de contexte de filtre, test de non-régression, niveau de difficulté. **C'est l'artefact qui, seul, prouve un niveau DAX professionnel** en entretien.
**Évaluation.** Quiz 20 Q (dont prédire le résultat d'une mesure selon le contexte, format qui correspond le mieux à l'entreprise) ; 4 exercices ; étude de cas « la mesure `Marge` est juste dans la matrice et fausse sur la carte » ; 12 mesures corrigées ligne par ligne. **Niveau : N4.**
**Transition.** « Power BI est l'outil dominant en francophonie, mais ce n'est pas le seul, et un professionnel sait dire pourquoi il a choisi. »

## PHASE 5 — PERFORMANCE ET AUTONOMIE PROFESSIONNELLE

### M16 — Tableau et autres outils BI — 5 chap. · 30 h
**Objectifs.** (1) Choisir un outil pour une raison, pas par mode. (2) Produire un dashboard Tableau comparable à celui de Power BI et en dire les différences. (3) Connaître le marché et ses évolutions récentes, y compris les gratuités utiles.
**Prérequis.** M10, M14 (la comparaison n'a de sens qu'avec un point de référence).

| Chap. | Titre | Contenu (vos §MODULE 13) | H |
|---|---|---|---|
| M16.C01 | Panorama honnête : ce qu'est un outil de BI, les 6 critères de comparaison (sources, modèle, calcul, collaboration, coût, compétences requises) | caractéristiques · cas d'utilisation | 5 |
| M16.C02 | Tableau : interface, sources, calculs (tablecalcs, LOD), feuilles, histoires, dashboards, performances ; **l'état réel de l'accès gratuit en 2026** (voir C.4) | forces · limites · difficulté | 7 |
| M16.C03 | Les autres : Looker Studio (Google), Qlik Sense, Superset, Metabase, Mode, Power BI Report Server, les outils open source ; à qui ils conviennent | marché | 5 |
| M16.C04 | Le match décisif : Excel vs Power BI vs Tableau vs Looker Studio vs SQL vs Python vs R — tableau complet, et surtout : « si tu dois faire cette tâche, utilise cet outil **parce que…** », 22 situations tranchées | complémentarité · arbitrage | 7 |
| M16.C05 | Produire le même livrable dans 3 outils, mesurer le temps, arbitrer pour une PME de 40 personnes au budget contraint | expérience comparée | 6 |

**Projet M16.P — « Recommandation d'outillage ».** Dossier d'aide à la décision de 4 pages pour un directeur général, avec scénarios, coûts, compétences à recruter, risques de dépendance fournisseur, et recommandation assumée. Livrable typique d'un consultant BI junior.
**Évaluation.** Quiz 15 Q ; étude comparative notée par grille ; corrigés argumentés (plusieurs réponses possibles, critères de réussite définis). **Niveau : N4.**
**Transition.** « Un outil choisi est une promesse de maintenance. Automatisons-la. »

### M17 — Automatisation du reporting — 6 chap. · 30 h
**Objectifs.** (1) Cartographier un processus manuel et décider quoi automatiser (et quoi ne surtout pas). (2) Automatiser de bout en bout : import, nettoyage, calculs, génération, export, diffusion. (3) Choisir l'approche selon le niveau de l'organisation. (4) Rendre un pipeline robuste, surveillé et documenté.
**Prérequis.** M05, M08, M14, M15.

| Chap. | Titre | Contenu (vos §MODULE 14) | H |
|---|---|---|---|
| M17.C01 | Cartographier et chiffrer un processus manuel : les 5 candidats à l'automatisation, le seuil de rentabilité, le "ne pas automatiser l'erreur" | méthode | 5 |
| M17.C02 | Automatiser dans Excel : Power Query comme usine, requêtes paramétrées, actualisation à l'ouverture, feuilles de collecte, modèles protégés, rapport mensuel en 3 clics | Excel / Power Query | 5 |
| M17.C03 | Automatiser en Python : boucle sur dossiers, scripts de génération, `openpyxl`/`xlsxwriter`, exports PDF, envoi par courriel, planificateur de tâches Windows / cron | Python · SQL | 5 |
| M17.C04 | Automatiser dans Power BI : actualisation planifiée, passerelle, paramètres, alertes sur cartes, abonnements par courriel, déploiement, Fabric Data Factory et pipelines quand l'organisation les a | Power BI | 5 |
| M17.C05 | Robustesse : journalisation, gestion des pannes et du fichier manquant, contrôles automatiques de cohérence, notifications en cas d'échec, reprise, "le lundi à 7 h" | fiabilité | 5 |
| M17.C06 | Industrialiser : versionnage Git du code et des requêtes, README technique, transfert à un collègue, document d'exploitation, coût de maintenance | gouvernance | 5 |

**Projet M17.P — « Le rapport hebdomadaire qui se fait seul ».** À partir d'un dossier où tombent chaque lundi 5 fichiers CSV : le pipeline doit détecter le fichier manquant, contrôler 6 règles, régénérer un classeur et un PDF, écrire un journal, prévenir par courriel en cas d'anomalie. **Testé et rejoué devant vous** (auto-démonstration avec les scripts fournis).
**Évaluation.** Quiz 15 Q ; 3 exercices ; étude de cas « le rapport se trompe depuis 3 mois, personne n'a remarqué » ; corrigés. **Niveau : N4.**
**Transition.** « Vous êtes opérationnel sur un métier générique. Regardons comment cela se passe métier par métier. »

### M18 — Analyses sectorielles — 7 chap. · 30 h
**Objectifs.** Pour chaque domaine, vos 7 rubriques (§MODULE 15) : données disponibles, questions métier, KPI, analyses possibles, outils adaptés, exemple, projet.
**Prérequis.** M09, M10, M12, M14.

| Chap. | Secteurs traités | Points d'entrée typiques |
|---|---|---|
| M18.C01 | **Commerce, grande distribution, PME de négoce** | CA, marge, rotation, rupture, panier, promotions, fidélité, Assortiment |
| M18.C02 | **Finance, banque, assurance, microfinance** | risque, NPL, scoring, solvabilité, conformité, rentabilité par produit/agence |
| M18.C03 | **Marketing et digital** | campagnes, coût par acquisition, entonnoir, rétention, ROI, attribution, réseaux sociaux |
| M18.C04 | **Ressources humaines** | effectifs, absentéisme, turnover, masse salariale, recrutement, formation, climat |
| M18.C05 | **Stocks, logistique, production, qualité** | couverture, taux de service, écarts d'inventaire, rendement, TRS, rebuts, délais |
| M18.C06 | **Santé, éducation, administration, secteur humanitaire** | fréquentation, indicateurs de santé publique, résultats scolaires, files d'attente, indicateurs de projet/ONG, redevabilité bailleurs |
| M18.C07 | **Agriculture, élevage, environnement** | rendements, prix de marché, pluviométrie, cheptel, saisonnalité, analyse de projets |

**Chaque fiche sectorielle = 6 à 9 pages** avec : 1 schéma du système d'information source, 1 dictionnaire de données, 1 tableau de 12 KPI avec définitions, 1 analyse complète conduite de bout en bout (données fournies), 1 dashboard ou classeur, 1 projet noté, 1 « ce qui trompe les analystes dans ce secteur ».
**Choix de conception.** Les secteurs sont groupés en 7 chapitres plutôt que 12 : les logique de commerce/stock/production partagent 70 % des KPI ; les séparer produirait la redondance que votre §23 interdit. La couverture des 12 secteurs de votre liste est **totale** dans le contenu, seule l'articulation change — voir §H.3.
**Projet M18.P.** Au choix, 3 pistes (commerce, banque/microfinance, santé/ONG) : dossier analytique sectoriel complet, avec données fournies et grille de notation par critères sectoriels. **4e–5e pièces du portfolio.**
**Évaluation.** Quiz par fiche ; étude de cas sectorielle ; corrigés. **Niveau : N4.**
**Transition.** « Vous répondez aux questions posées. Le niveau supérieur consiste à répondre à celles qu'on n'ose pas poser : *que va-t-il se passer ?* »

### M19 — Analyse avancée : de la description à la prédiction — 6 chap. · 30 h
**Objectifs.** (1) Marquer clairement la frontière Data Analysis → BI → Data Science → Machine Learning (votre exigence explicite). (2) Construire une prévision défendable avec des méthodes simples et une validation honnête. (3) Segmenter et scorer. (4) Détecter des anomalies. (5) **Communiquer l'incertitude** — ce qui distingue le praticien responsable.
**Prérequis.** M02, M08, M09. Aucun prérequis en mathématiques supérieures : tout est reconstruit intuitivement.

| Chap. | Titre | Contenu (vos §MODULE 16) | H |
|---|---|---|---|
| M19.C01 | La frontière : analyse descriptive, diagnostique, prédictive, prescriptive ; ce que la BI fait déjà bien ; décider si vous avez besoin de "prédire" | frontière DA/BI/DS/ML | 4 |
| M19.C02 | Séries temporelles et prévisions : composantes, lissage, moyenne mobile, décomposition, Holt, projection naïve comme étalon, validation (train/test, erreurs MAE/RMPE/MAPE), intervalles | séries temporelles · prévisions | 6 |
| M19.C03 | Régression linéaire simple et multiple pour expliquer, avec diagnostics accessibles, et les 6 avertissements nécessaires | régression | 5 |
| M19.C04 | Classification et scoring : seuils, matrice de confusion, précision/rappel, scorecard pondéré simple, cas du défaut de paiement en microfinance | classification · scoring | 5 |
| M19.C05 | Segmentation et clustering : K-means et RFM comparés, décrire les groupes, les utiliser opérationnellement, pièges | segmentation · clustering | 5 |
| M19.C06 | Détection d'anomalies, introduction au ML et ce qu'il faut savoir de plus tard : arbre, validation croisée, biais/variance, surapprentissage, équité, quand un Data Scientist est nécessaire et comment travailler avec lui | détection d'anomalies · introduction au ML | 5 |

**Règle de rigueur imposée.** Chaque méthode est présentée avec : ce qu'elle promet, ce dont elle a besoin, comment la tester, **comment elle ment**, et la phrase type à dire au décideur. Exemple : aucune prévision du manuel n'est publiée sans son intervalle et sans la comparaison à la projection naïve.
**Projet M19.P — « Prévoir le trimestre prochain et le défendre ».** Prévision de ventes à 12 semaines + segmentation de clients + note de 2 pages sur l'incertitude ; l'apprenant doit aussi produire la page « pourquoi je me tromperai ».
**Évaluation.** Quiz 15 Q ; 3 exercices ; étude de cas « le modèle disait vrai en atelier, faux en production » ; corrigés. **Niveau : N4(+).**
**Transition.** « La meilleure analyse du monde ne change rien si personne n'y adhère. Le module suivant est peut-être celui qui augmentera le plus votre valeur sur le marché. »

## PHASE 6 — PROFESSIONNALISATION

### M20 — Data storytelling et communication — 6 chap. · 30 h
**Objectifs.** (1) Construire le récit d'un résultat. (2) Choisir les 3 chiffres qui comptent. (3) Ne pas surcharger. (4) Recommander sans déformer. (5) Présenter à quatre publics distincts (directeur, responsable, client, équipe, public non technique).
**Prérequis.** M10 (visuel), M12 (KPI), M02 (honnêteté statistique).

| Chap. | Titre | Contenu (vos §MODULE 17) | H |
|---|---|---|---|
| M20.C01 | Avant le support : analyser l'audience, la décision attendue, le niveau de conflit possible ; la note de cadrage | présentation d'un résultat | 5 |
| M20.C02 | La structure narrative : situation–complication–question–réponse ; le pyramide inversée ; le hook de 20 secondes ; 4 plans-types (revue mensuelle, alerte, opportunité, bilan de projet) | construire une histoire | 5 |
| M20.C03 | Le deck : 12 diapositives, une idée par diapositive, titres affirmatifs, le chiffre unique, les 3 exemples complets de présentations professionnelles annotées | exemples de présentations | 5 |
| M20.C04 | Choisir les indicateurs à montrer et éviter la surcharge : la règle du « que doit faire le lecteur ? », l'écran de synthèse, l'annexe comme sas de sécurité | indicateurs importants · surcharge | 5 |
| M20.C05 | Recommander sans déformer : le langage de la prudence, séparer fait / inférence / opinion, assumer les limites, les 9 formulations professionnelles, gérer la question qui démonte l'analyse | recommandation fondée sans déformation | 5 |
| M20.C06 | La soutenance : préparer, chronométrer, gérer le direct, le distanciel, l'improvisation d'un graphique, le compte rendu écrit post-réunion | mise en pratique | 5 |

**3 présentations professionnelles complètes** en annexe de module (structure, diapositives reproduites, commentaire marginal de l'auteur, ce qui aurait pu être fait autrement) : (1) revue mensuelle de direction commerciale ; (2) alerte sur une rupture de stock critique en pharmacie hospitalière ; (3) restitution d'un audit de données à une ONG.
**Projet M20.P — « 8 minutes devant le comité de direction ».** L'apprenant choisit un de ses livrables de M17/M18/M19, produit 6 diapositives + un script + un enregistrement de 8 min, et s'auto-évalue avec la grille de soutenance (20 points) ; une version « auto-évaluation par un tiers » est fournie pour être donnée à un ami ou collègue non expert. **6e pièce du portfolio.**
**Évaluation.** Quiz 15 Q de reformulation (réécrire un titre de diapositive), 3 exercices, grille de soutenance /20, corrigés exemplaires. **Niveau : N4 → N5.**
**Transition.** « Il reste une chose à prouver : que vous savez le faire seul, sur un vrai dossier, du début à la fin. »

### M21 — Projets professionnels complets (7 + final) — 6 chap. · 30 h d'accompagnement + ~40 h de travail projet
**Objectifs.** Mener seul, de la commande à la soutenance, les huit projets qui constituent la preuve de niveau N4.

| Chap. | Titre | Contenu | H |
|---|---|---|---|
| M21.C01 | Projets 1 et 2 : la vente, du tableur au classeur piloté | P1 débutant (Excel seul) puis P2 intermédiaire (Power Query) ; grille de réussite commune | 5 |
| M21.C02 | Projets 3 et 4 : la base et le script | P3 SQL (25 questions) et P4 Python (EDA complète), avec auto-validation | 6 |
| M21.C03 | Projets 5 et 6 : le dashboard et le système complet | P5 Power BI puis P6 chaîne base → SQL → ETL → modèle → DAX → dashboard | 8 |
| M21.C04 | Projet 7 : l'audit d'un dispositif existant | reprendre un existant bancal fourni, diagnostiquer, remédier, chiffrer | 4 |
| M21.C05 | La mission finale : cadrage, méthode, journal de bord | comment travailler 25 h en autonomie sur une commande réelle | 3 |
| M21.C06 | La mission finale : rendus, soutenance et corrigés exemplaires | les livrables attendus, la grille /40, les 6 rendus exemplaires annotés | 4 |

**Vos 8 projets sont conservés tels quels**, enrichis d'un livrable et d'une grille de réussite ; leur difficulté progresse réellement et ils s'additionnent (les artefacts de l'un servent à l'autre) :

| # | Votre intitulé | Module correspondant | Livrable attendu | Outils | Grille |
|---|---|---|---|---|---|
| P1 | Analyse simple des ventes d'une petite entreprise | M21.C01 (niveau débutant) | Note de 1 page + 3 graphiques | Excel | /20 |
| P2 | Analyse commerciale avec Excel et Power Query | M21.C01 (intermédiaire) | Classeur automatisé + 5 insights | Excel + Power Query | /20 |
| P3 | Analyse d'une base de données de ventes | M21.C02 (SQL) | 25 requêtes commentées + note | DuckDB/PostgreSQL | /20 |
| P4 | Analyse exploratoire complète d'un jeu de données | M21.C02 (Python) | Notebook de 30 cellules + rapport | pandas | /20 |
| P5 | Tableau de bord commercial professionnel | M21.C03 (Power BI) | `.pbix` 3 pages + 12 mesures + thème | Power BI | /20 |
| P6 | BI avancée : base → SQL → ETL → modèle → DAX → Power BI → dashboard | M21.C03 (BI avancée) | Chaîne complète, scriptée, rejouable | PostgreSQL + Power Query/M + DAX + Power BI | /25 |
| P7 *(ajout)* | Mission de conseil : l'audit d'un dispositif existant | M21.C04 | Rapport d'audit + plan de remédiation chiffré | tout | /20 |
| **Final** | **Mission de Data Analyst / BI Analyst** | **M21.C05–C06** | **Dossier de mission complet** | **tout, en autonomie** | **/40** |

**Le projet final — « La mission Sahel Distribution ».** Cahier des charges de 6 pages simulant une commande réelle (commanditaire : directeur général ; contexte de conflit interne ; contraintes de délai et d'accès ; données livrées volontairement lacunaires et **incohérentes entre deux systèmes**, avec un choix d'arbitrage à assumer). Livrables exigés, tous notés : (1) note de cadrage et plan de travail ; (2) dossier de données documenté ; (3) modèle dimensionnel ; (4) couche SQL/Power Query ; (5) bibliothèque de mesures ; (6) tableau de bord ; (7) note analytique de 2 pages avec 3 recommandations ; (8) deck de soutenance de 8 min ; (9) journal de bord de l'analyse. Grille en 40 points, critères publiés en amont dans le manuel, avec auto-évaluation puis évaluation par un pair.
**M21.C04** fournit aussi 2 projets "reprise" (reprendre un dispositif bancal fourni et le corriger) et les barèmes détaillés ; **M21.C06** fournit les *corrigés intégraux* des 8 projets sous forme de rendus exemplaires annotés — c'est là que se joue l'auto-formation, et c'est ce qui rend le module 21 le plus long à produire de tout le parcours.

### M22 — Portfolio, emploi, feuille de route — 4 chap. · 30 h
**Objectifs.** (1) Transformer les rendus du parcours en portfolio. (2) Se positionner. (3) Passer les entretiens et les tests techniques. (4) Planifier les 24 mois suivants.

| Chap. | Titre | Contenu |
|---|---|---|
| M22.C01 | Le portfolio, méthode et 14 fiches : 3 Excel + 3 SQL + 3 Python + 3 Power BI + 2 BI complets (votre §15), comment présenter chaque projet (contexte → question → démarche → résultat chiffré → décision → code/sources), les formats de publication (GitHub, PDF, site, Power BI web, Tableau), les erreurs qui décrédibilisent | §15 |
| M22.C02 | Se vendre : CV orienté résultats chiffrés, lettre, profil LinkedIn, GitHub, tarification et freelancing local, portfolio en ligne, ce que regardent réellement les recruteurs sur la zone UEMOA et en remote | insertion |
| M22.C03 | Entretien et tests techniques : 60 questions types avec réponses commentées, tests SQL en direct, étude de cas Excel, exercice Power BI, négociation, et la question « parlez-moi d'un résultat que vous avez dû corriger » | recrutement |
| M22.C04 | Feuille de route et certifications : **Débutant → Data Analyst junior → Data Analyst confirmé → BI Analyst → BI Developer/spécialiste BI**, avec pour chaque palier compétences, outils, projets, portfolio, compétences métier, erreurs à éviter ; les certifications utiles et leur rentabilité réelle (PL-300 Power BI Data Analyst, et alternatives), les communautés, les 12 prochains mois, la suite (Data Engineering, Data Science, Product Analytics) | §14 + documentation continue |

**Évaluation.** Portfolio v1 (14 fiches, 4 d'entre elles issues de vos travaux antérieurs) + CV + lettre + une simulation d'entretien écrite (20 questions répondues) ; grille de revue notée /20. **Niveau visé : N5 en construction.**

## MODULES DE SPÉCIALISATION (optionnels, après le palier P4)

### M23 — R pour l'analyse de données — 5 chap. · 15 h
Traitement honnête de votre « R lorsque son utilisation est pertinente » : **quand R est le bon choix** (statistique inférentielle, bio/santé publique, analyse de données agricoles, travaux académiques, publications) et quand il ne l'est pas (BI d'entreprise en francophonie, où Power BI et SQL dominent). Contenu : installation R/RStudio-Posit, vecteurs et data frames, `dplyr`/`tidyr`/`readr`, `ggplot2`, tests statistiques, `tidymodels` en survol, et **l'équivalence systématique pandas ↔ R** chapitre par chapitre (chaque exercice pandas du module M08/M09 est refait en R). Projet : refaire l'EDA de M09 en R et comparer.
### M24 — Data engineering appliqué : ETL/ELT, DuckDB, orchestration — 5 chap. · 20 h
Pour passer de « analyste qui produit » à « analyste qui conçoit la chaîne » : ingestion de fichiers et d'API, stockage de fichiers (parquet, delta), DuckDB comme entrepôt local, transformations avec dbt-core, incrementalité, tests de données (null/unique/referential/freshness), orchestration (Prefect ou tâches planifiées), Git et revues de code, déploiement sur un petit serveur. Projet : le pipeline complet du fil rouge, versionné, testé, documenté, rejouable par un collègue.
### M25 — Données ouvertes, géomatique et cartographie décisionnelle — 4 chap. · 15 h
Comment trouver, lire et citer des données ouvertes réelles (instituts nationaux de statistique de la zone — **INSD au Burkina, insd.bf** ; ANSD au Sénégal ; INStaD en Côte d'Ivoire —, BCEAO, Banque mondiale / World Bank Open Data, HDX et ReliefWeb pour l'humanitaire, FAO/FAOSTAT et les relevés de prix des marchés agricoles, OpenStreetMap), les nettoyer, les joindre, les cartographier (`geopandas`, QGIS, Power BI carte avec formes personnalisées), et les intégrer à une analyse métier. Projet : atlas décisionnel d'une région sur un thème au choix (prix agricoles, couverture sanitaire, résultats scolaires).

## C.4. Référentiel des outils enseignés (votre §6, tableau complet)

| Outil | Fonction principale | Niveau où il est enseigné | Cas d'utilisation concret | Avantages | Limites | Décision du manuel |
|---|---|---|---|---|---|---|
| **Excel / LibreOffice Calc** | Tableur : calcul, tableaux croisés, graphiques, petite analyse | M01, M03, entretenu jusqu'à M21 | Tout : le langage universel de l'entreprise, la vérification rapide, le livrable que le manager rouvrira | Ubiquitaire, gratuit d'accès, TCD très efficaces, Power Query surprenant de puissance | 30–100 k lignes avec confort, peu de gouvernance, versions non vérifiables, erreurs de formules invisibles | **Colonne vertébrale du début** ; jamais présenté comme "petit outil" |
| **Power Query (M)** | Préparation et transformation reproductibles | M03.C08, M05.C02, M14.C03, M17.C02 | Import multi-fichiers, nettoyage hebdo, fusion de fichiers du même dossier | Pas de code, rejouable, gratuit dans Excel, le meilleur ROI horaire du parcours | Moins souple que pandas pour le sale travail, limité hors écosystème Microsoft | **Obligatoire** ; le plus rentable pour un analyste de PME |
| **Power Pivot / DAX** | Modèle de données et mesures dans Excel | M03.C08, préparatoire à M15 | Besoin d'un modèle en étoile sans Power BI : chiffres fiables et partagés dans un classeur | Gratuit dès qu'Excel est là, aucun serveur, les mêmes mesures réutilisables dans Power BI | Courbe raide, peu d'aide francophone, contexte de filtre exigeant, modèle limité en taille | **Enseigné comme passerelle** vers M13/M15, pas comme fin en soi |
| **SQL** (DuckDB, SQLite, PostgreSQL) | Interroger et transformer des jeux structurés | M06, M07, M11, M05.C03, M21.P3 | Toute base de l'entreprise, les 5 millions de lignes, les requêtes de contrôle, l'automatisation légère | Compétence n°1 demandée en annonce, universel, performant, vérifiable | Ne couvre ni la préparation sauvage, ni la visualisation | **Pilier n°1 du parcours** (avec Power BI) |
| **Python** (pandas, matplotlib, seaborn, scikit-learn) | Analyse, automatisation, modélisation | M05.C04, M08, M09, M17, M19, M25 | Nettoyage difficile, EDA, séries longues, scripts, prévisions, pipeline | Gratuit, polyvalent, réutilisable, versionnable | Demande de l'abstraction ; inutile si tout tient dans une base + Power BI | **Pilier n°2**, introduit après Excel et le nettoyage |
| **Jupyter / VS Code** | Environnement d'exécution et d'édition | M08.C01 | Travailler, documenter, partager son analyse en cours | Gratuit, reproductible, pédagogique (texte + code + sortie) | Piège du notebook non linéaire (run dans le désordre) — traité explicitement | **Obligatoire**, avec contre-mesure "noyauter puis exécuter dans l'ordre" enseignée |
| **Power BI** | BI : modèle, mesure, dashboard, diffusion | M14, M15, M17, M21 | Le dashboard professionnel, la gouvernance, l'abonnement courriel, la sécurité par ligne | Écosystème Excel/Power Query/DAX, coût d'entrée nul en création, marché francophone favorable | Partage payant (licence Pro/PPU par utilisateur, ou capacité Fabric F64+ pour des lecteurs gratuits) ; Desktop Windows uniquement ; DAX déroutant | **Outil BI principal du manuel** ; alternatives fournies pour les contraintes de licence et de matériel |
| **Tableau** | BI et visualisation exploratoire | M16.C02, M16.C05 | Analyse visuelle rapide, data art, storytelling par "stories" | Excellent pour l'exploration visuelle, calculs et LOD puissants | Coût des licences Creator ; **à vérifier au moment de la rédaction** : depuis 2026, des sources professionnelles rapportent l'existence d'une *Tableau Desktop Free Edition* (analyse locale complète, tous connecteurs, sans publication vers Server/Cloud/Public) en complément de Tableau Public (fichiers uniquement, 15 M lignes, tout est public). **Le manuel signalera cette information comme à confirmer sur le site officiel et fournira un plan B open source** | **Présenté, comparé, pratiqué** via les versions gratuites ; jamais imposé |
| **Looker Studio** | Rapports web légers et gratuits | M16.C03, M17 | Reporting digital marketing, tableau de bord Google Sheets/GA4, partage gratuit en URL | Gratuit par utilisateur (Pro payant ≈ 9 $/utilisateur/mois pour la gestion d'équipe), natif avec l'écosystème Google | Gouvernance, sécurité par ligne et performances limitées, peu d'usage en entreprise de la zone | **Mentionné utilement** pour ONG, startups, marketing |
| **Open source BI** (Metabase, Superset, Lightdash) | Dashboards hébergés sans licence | M16.C03, M24 | ONG, administrations, projets avec données sensibles sur serveur local | Zéro coût de licence, déployable, simples | Nécessitent un hébergement et une maintenance, moins "cliquables" pour l'utilisateur final | **Solutions de repli recommandées** quand Power BI n'est pas finançable |
| **Power BI Report Server / SSRS** | Rapports paginés imprimables sur site | M16.C03 (mention) | Le relevé mensuel de 40 lignes imprimables, la facture, le rapport réglementaire | Pixel-perfect, diffusion planifiée | Contexte de licences SQL Server ; **SSRS 2022 est la dernière version de SSRS, SQL Server 2025 est livré sans SSRS et l'on-premises reporting converge vers PBIRS** (support sécurité SSRS jusqu'au 11 janvier 2033) | **Une fiche explicative, pas un apprentissage** |
| **R** | Statistique, modélisation, publication | M23 (option) | Analyse académique, santé, agronomie | Richesse statistique inégalée, gratuit | Peu demandé dans la BI d'entreprise francophone | **Option assumée**, position argumentée en M23.C01 |
| **Git / GitHub** | Versionnage, publication, collaboration | M04.C06, M17.C06, M21, M22 | Suivre ses scripts et rendre son travail vérifiable | Gratuit, standard, base de l'employabilité | Effet d'intimidation initial | **Enseigné de façon minimale et progressive**, pas en module isolé |
| **dbdiagram / Draw.io** | Schémas de données et flux | M06, M13, M20 | Les 9 diagrammes d'un dossier d'analyse | Gratuit, rapide, export propre | Peu de gouvernance | **Obligatoire** (les diagrammes sont des livrables) |

**Outils volontairement exclus**, avec la raison écrite dans le manuel (votre §6 « Évite d'accumuler des logiciels sans nécessité ») : Alteryx, KNIME (redondants avec Power Query/pandas pour un débutant), QlikView (parcours de maintenance), Apache Spark/PySpark (inutile en dessous de quelques centaines de millions de lignes — une fiche de "quand y venir" en M24.C04), Power Apps, les outils de BI chinois/indiens, les solutions no-code dashboard (superficielles en entretien), tout outil nécessitant une licence à plus de 20 $/mois pour apprendre.

## C.5. Référentiel de l'état de l'art (à jour au 17 septembre 2026)

| Sujet | État retenu dans le manuel | Référence à re-vérifier au moment de la rédaction |
|---|---|---|
| **Power BI licences** | Desktop gratuit pour créer ; publier/partager → **Pro** ou **Premium Per User** (les anciens SKUs Premium "P" par capacité ne sont plus commercialisés) ; les lecteurs n'ont pas de licence payante **à partir d'une capacité Microsoft Fabric F64** | Microsoft Fabric / Power BI pricing page |
| **Fonctions récentes Power BI** | Édition des modèles sémantiques dans le service (GA), vue TMDL (GA), UDF DAX (aperçu sept. 2025 → GA en juin 2026 selon les sources), calendriers améliorés / Enhanced DAX Time Intelligence (aperçu), Direct Lake | Power BI release notes mensuelles |
| **pandas** | **3.x** courant (3.0 paru le 21 janvier 2026) : type texte dédié par défaut, copy-on-write, suppression d'API dépréciées. Écritures 2.x à corriger signalées | pandas documentation « What's new » |
| **PostgreSQL** | Version 18 en production (sortie sept. 2025 ; nouvelle sous-couche d'entrées/sorties asynchrones), support jusqu'en novembre 2030 ; la 14 arrive en fin de support le 12/11/2026 | postgresql.org/versioning |
| **DuckDB** | v1.x (utilisé comme moteur SQL local du parcours : zéro installation serveur, lit CSV/Parquet directement) | duckdb.org |
| **Tableau** | Existence rapportée d'un **Desktop Free Edition** (mars 2026) à confirmer ; Tableau Public : 15 M lignes/fichier, tout est public, connecteurs limités | tableau.com/products |
| **Looker Studio** | Gratuit par utilisateur ; Pro ≈ 9 $/utilisateur/mois ; pas de sécurité par ligne dans la version gratuite | Google Looker Studio |
| **SSRS** | SSRS 2022 = dernière version ; SQL Server 2025 livré sans SSRS ; reports paginés sur site = Power BI Report Server ; sécurité SSRS maintenue jusqu'au 11/01/2033 | Microsoft Learn, Reporting Services consolidation FAQ |
| **Excel** | Microsoft 365 courant ; fonction Python dans Excel disponible ; **`RECHERCHEX` (XLOOKUP) existe dès Excel 2021 en licence perpétuelle, alors que les fonctions matricielles dynamiques `FILTRE`, `TRIBY`, `UNIQUE`, `LET`, `SÉQUENCE` exigent Microsoft 365** ; côté LibreOffice, ces fonctions sont intégrées nativement **depuis la version 24.8** (la version installée est donc à vérifier), mais **Power Query et Power Pivot n'existent pas** dans LibreOffice | Microsoft Support ; notes de version LibreOffice |

> **Règle de rédaction n°1 du projet** : toute affirmation relative à une version, une licence ou une disponibilité de fonctionnalité porte une date de vérification en note de bas de page du manuel, et figure dans cette table. Un manuel daté est un manuel honnête ; un manuel qui ne date pas ment sans le savoir.

---

# PARTIE E — LES RESSOURCES PÉDAGOGIQUES

## E.1. Le fil rouge : « Sahel Distribution SA »

**Pourquoi un fil rouge.** Votre §11 demande des situations professionnelles réalistes plutôt que des exemples artificiels. Un fil rouge unique permet à l'apprenant de **connaître les données par cœur à partir du module 6**, ce qui est précisément ce qui arrive en entreprise : la difficulté cesse d'être la donnée et devient l'analyse. Un fil rouge unique évite aussi 20 jeux de données à maintenir et 20 sources d'incohérence (§23).

**La scénario.** *Sahel Distribution SA*, distributeur grossiste de matériaux et de quincaillerie, 5 magasins et 1 dépôt, 23 500 clients, 154 références, 22 vendeurs, 3 ans et 8 mois d'historique (2023-01-01 → 2026-08-31), un système de caisse, un fichier Excel de suivi des remises tenu par une assistante, un relevé de stocks tenu par le magasinier. **Les chiffres de ce paragraphe sont ceux des fichiers réellement livrés dans `01_socle_donnees/data/` ; ils sont produits par `scripts/chiffres_manuel.py` (clé `structure`) et ne sont jamais recopiés de mémoire.** Enjeu fil rouge, constant : *le directeur général pense que la marge baisse à cause des prix ; l'analyse montrera que c'est surtout le mix produit et les ruptures.*

| Table | Grain | Taille | Utilisée dans | Défauts volontairement injectés |
|---|---|---|---|---|
| `magasins` | 1 par magasin | **6** (5 magasins + 1 dépôt) | M06, M13, M14 | — |
| `vendeurs` | 1 par salarié en vente | **22** | M03, M12 | — |
| `clients` | 1 par client | **23 912 brut / 23 500 propre** | M03, M06, M08, M11 | 1 880 villes manquantes (8 %), 412 doublons quasi-exacts, 3 formats de téléphone |
| `produits` | 1 par référence | **154** | M02 → M14 | 61 lignes à catégorie orthographiée de travers, 2 prix nuls, 6 poids incohérents |
| `ventes` (fait) | 1 par ligne de ticket | **243 360 brut / 240 000 propre** · 20 colonnes · 28,5 Mo | tous | 3 360 lignes en double, 3 360 montants en texte, 2 640 dates au format mixte, 486 clients non référentés, 973 remises aberrantes |
| `objectifs` | 1 par magasin × mois | **218** | M03, M12, M14 | 2 mois manquants |
| `stocks` | 1 par produit × dépôt × jour | **60 000** (extrait d'un champ théorique de 1,1 M) | M05, M11, M19 | trous de série, valeurs négatives |
| `couts_achat` | 1 par produit × période de prix | **1 694** | M13 (SCD type 2), M15 | changements de prix en cours de mois |
| `dim_date` | 1 par jour | **1 339** (2023-01-01 → 2026-08-31) | M11, M15 | à construire soi-même (exercice) |
| `remises_manuelles` | 1 par client × mois | **18 200** (fichier `.xlsx`) | M04, M05 | fusion avec les ventes : le cauchemar pédagogique parfait |

Le jeu complet est fourni en **CSV/Excel + base DuckDB prête** avec dictionnaire de données, générateur reproductible, et un fichier `verites_terrain.csv` (les vrais totaux de référence, pour auto-validation) — c'est ce qui rend possible la correction automatique (§B.6). Trois extraits de différentes tailles (489 lignes → 240 k lignes → le champ complet des stocks) permettent aux modules de débuter sans écraser un ordinateur à 8 Go.

## E.2. Les jeux de données satellites (7)

| Jeu | Origine | Usage | Pourquoi ce choix |
|---|---|---|---|
| `sante_centre_c` | Synthétique réaliste, inspirée des formats DHIS2 | M09, M18.C06, M20 | Fréquentation, ruptures de médicaments, files d'attente : typique des données que rencontrera un analyste d'ONG ou de ministère |
| `ecole_resultats` | Synthétique inspiré de SchoolData-format | M02, M09, M16 | Absentéisme, résultats par classe, genre, redoublement : statistiques accessibles sans polémique |
| `agri_prix_marche` | Données de prix de marché réelles (céréales : mil, sorgho, maïs), agrégées et citées | M09, M19, M25, M18.C07 | Saisonnalité, prévision, agriculture, région : directement utile au contexte burkinabè |
| `banque_microfinance` | Synthétique conforme au format type d'un portefeuille de crédit | M18.C02, M19 | NPL, scoring, taux de recouvrement, cohorte de prêt : le secteur qui recrute |
| `rh_effectifs` | Synthétique de paie et SIRH | M03, M18.C04, M11 | Turnover, absentéisme, masse salariale, fenêtres SQL parfaites |
| `energie_reseau` | Synthétique de relevés de consommation | M19, M25 | Prévision, détection d'anomalies de compteur |
| `transport_urbain` | Synthétique de courses de motos-taxi / bus | M08, M09, M10 | Données horaires, heatmap, cartes, forte volumétrie légère |

**Tous les jeux sont livrés avec** : dictionnaire des colonnes, 5 questions métier prêtes, défauts connus et documentés, vérité terrain, et un fichier `NOTICE.md`. Aucune donnée personnelle réelle n'est utilisée : les données sont synthétiques et le manuel explique explicitement ce choix en M04.C06 (confidentialité).

## E.3. Les 30 projets du parcours de base (21 en M01–M20, 8 en M21 dont la mission finale, 1 portfolio en M22) + 3 en options

Chaque projet suit le contrat unique : **commanditaire · contexte · données fournies · livrables numérotés · contraintes (délai, format, outil imposé ou interdit) · critères de réussite explicites · corrigé exemplaire annoté · auto-évaluation**. Les projets 1 à 12 sont guidés (une fiche d'étapes), 13 à 24 semi-guidés (objectifs sans étapes), 25 à 32 en autonomie (commande seule, comme en entreprise). Les projets sont **cumulatifs par conception** : M14.P réutilise la carte de KPI de M12.P et le modèle de M13.P ; M21.P6 est la chaîne complète des modules 4 à 17. C'est cette cumulativité qui fait la différence entre 32 exercices et une formation.

## E.4. Les 180 exercices : répartition

| Phase | Modules | E1 | E2 | E3 | E4 | E5 | E6 | E7 | **Total** |
|---|---|---|---|---|---|---|---|---|---|
| P0–P1 | M01–M03 (3) | 10 | 10 | 4 | 4 | 4 | 3 | 2 | **37** |
| P2 | M04–M09 (6) | 14 | 14 | 6 | 6 | 7 | 3 | 1 | **51** |
| P3–P4 | M10–M15 (6) | 12 | 14 | 7 | 6 | 7 | 4 | 1 | **51** |
| P5–P6 | M16–M22 (7) | 10 | 10 | 7 | 4 | 6 | 3 | 1 | **41** |
| **Parcours de base** | 22 modules | **46** | **48** | **24** | **20** | **24** | **13** | **5** | **180** |
| Options M23–M25 | 3 modules | 3 | 3 | 1 | 1 | 1 | — | 1 | **10** |

**Contrôle arithmétique (à refaire à chaque révision) :** lignes `37 + 51 + 51 + 41 = 180` ; colonnes `46 + 48 + 24 + 20 + 24 + 13 + 5 = 180`. Soit **190 exercices** avec les modules d'option. Les « occurrences visées » du §B.5 sont ces mêmes nombres : ce ne sont pas des estimations.

## E.5. Le « Cahier de l'apprenant » : l'espace de travail intégré à l'architecture

| Élément | Description | Où |
|---|---|---|
| `journal.md` | Un paragraphe par séance : ce que j'ai fait, ce qui bloque, ce que je referai différemment | Modèle fourni M01, usage obligatoire jusqu'à M22 |
| `glossaire_personnel.md` | 3 à 5 termes nouveaux par chapitre, avec sa phrase à lui | Construit en continu — **le manuel en fournit 620, l'apprenant en écrit 260** |
| `erreurs.md` | Journal des bugs, messages d'erreur, erreurs de formule rencontrés et leur solution | Anti-répétition, base des 60 questions d'entretien de M22.C03 |
| `carnet_projets/` | Un dossier par projet : README, données, code, livrables, auto-évaluation | Devient directement le portfolio de M22 |
| `checklists/` | 9 checklists imprimables (qualité de donnée, préparation d'un dashboard, revue de modèle, avant soutenance, mise en production d'un rapport…) | Annexes du manuel, reproductibles autorisées |

**Pourquoi c'est dans l'architecture et pas dans un conseil final.** Un autodidacte sans enseignant n'a pas de mémoire de travail externe. Le cahier de l'apprenant est le tuteur ; c'est la contrepartie structurelle de l'absence de classe.

## E.6. Règles de production des contenus techniques (applicables dès l'étape 2)

| Contenu | Règle | Preuve exigée dans le chapitre |
|---|---|---|
| SQL | Exécuté sur DuckDB 1.5 et revérifié sur PostgreSQL 18 ; requêtes en ANSI SQL, écarts dialectaux signalés en encadré | Bloc de sortie réel + n° de version |
| Python | Exécuté sous Python 3.13 / pandas 3.x, reproductible par script | Sortie console ou output notebook réel |
| Formules Excel | Testées dans une feuille de calcul générée (openpyxl) ; noms français **et** anglais donnés | Capture du résultat + fichier `.xlsx` disponible |
| DAX | Écrit selon la sémantique vérifiée sur modèle réel quand c'est possible, sinon **explicitement signalé comme non exécuté**, avec les 3 points à tester manuellement | Mention de statut |
| Power BI (clics) | Chemins de menu, boîtes de dialogue, captures à insérer **avec contenu de l'écran décrit précisément** ; toute dépendance à une option "fonctionnalité en aperçu" signalée | Légende + contenu attendu |
| Chiffres et statistiques | Toujours recalculés depuis le jeu de données, jamais inventés ; toute donnée externe sourcée avec date | Référence interne au `verites_terrain.csv` |

## E.7. Grille de conception des tableaux de bord (utilisée 4 fois : M10, M14, M17, M21)

**18 points** — errata du 24 septembre 2026 : le texte annonçait « 20 points, 4 points par famille » (4 × 4 = **16**, incohérent) ; le module M10 et le module M14 disent **18** points, la répartition retenue est **4 / 5 / 5 / 4** — dans **4 familles** : **1. Décision servie** (le dashboard répond à une décision nommée) · **2. Justesse** (totaux cohérents aux 3 niveaux, granularité affichée, vides expliqués, dates cohérentes) · **3. Lisibilité** (hiérarchie, 5 secondes pour le chiffre principal, pas de double axe inutile, ordre des barres, contraste, accessibilité) · **4. Utilisation** (segments, drill-down, page d'aide, performance < 3 s, responsive, nommage, documentation). Le manuel fournit la version auto-évaluée et la version revue par un pair.

---

# PARTIE F — LE LIVRABLE FINAL

## F.1. Propositions de titre (10), choix argumenté

| # | Titre | Positionnement | Note d'adéquation |
|---|---|---|---|
| 1 | **La Voie des Données** — Analyse de données et Business Intelligence, du débutant absolu à l'expert | Progression, cheminement, sérieux éditorial ; se prononce bien en français comme à l'international | 19/20 |
| 2 | **De la Donnée à la Décision** — Manuel complet d'analyse de données et de Business Intelligence | Exactement votre thème (transformer des données brutes en aide à la décision) ; un peu descriptif | 18/20 |
| 3 | **Données en Décisions** — Le manuel d'analyse de données et de BI, du zéro à l'expertise | Formule courte, mémorisable, mais syntaxiquement forcée | 15/20 |
| 4 | **Décider avec les Données** — Le parcours complet de l'analyste, d'Excel à Power BI | Très bon pour le décideur, moins pour l'aspect technique | 16/20 |
| 5 | **Le Manuel d'Analyse de Données & de Business Intelligence** — 22 modules pour passer de zéro à l'expertise | Sobre, institutionnel, excellent en librairie, peu évocateur | 17/20 |
| 6 | **Data & Décision** — Le parcours complet de l'analyste et du praticien de la BI | Moderne, un brin générique | 14/20 |
| 7 | **Du Tableau Brut au Tableau de Bord** — Manuel d'analyse de données appliquée et de Business Intelligence | Jeu de mots exact et très mémorable (le filetage Excel → Power BI) ; un peu long | 18/20 |
| 8 | **L'Intelligence des Données** — De l'analyse descriptive à la décision | Élégant, mais ambigu avec « intelligence artificielle » en 2026 | 13/20 |
| 9 | **Le Métier de l'Analyse** — Données, statistiques, SQL, Power BI : du débutant absolu au professionnel | Très orienté employabilité, un peu sec | 16/20 |
| 10 | **Lire les Données, Éclairer les Décisions** — Formation complète d'analyse de données et de Business Intelligence | Poétique et exact, un peu mou pour un titre principal | 15/20 |

**Titre officiel retenu :**

> # **La Voie des Données**
> ## Analyse de données appliquée & Business Intelligence
> ### Le manuel complet du débutant absolu à l'expert — Excel · SQL · Python · Power BI
> *Édition 2026 — 22 modules · 143 chapitres · 180 exercices corrigés · 30 projets · ≈ 2455 pages*

**Justification du choix.** « La Voie » est le seul titre qui porte vos trois exigences simultanées sans les trahir : la **progression** (votre exigence centrale du §2, six niveaux, sans condescendance), la **transformation** (la donnée suit un chemin, du brut au décidé, §16) et la **durée** (une voie suppose de la constance, ce qui prépare le lecteur à 660 heures). Elle reste sobre et crédible sur un CV comme en librairie professionnelle, ne promet ni magie ni certification, et fonctionne comme une marque pour les modules de spécialisation ultérieurs (*La Voie des Données — Data Engineering*, *— Data Science*, *— Gestion de la donnée*). Le sous-titre, lui, fait le travail de référencement : il dit exactement ce qu'il y a dedans, ce que recherchent vos 10 premiers lecteurs.

**Alternative recommandée en cas de préférence plus descriptive :** n°2, *De la Donnée à la Décision*, avec le même sous-titre technique.

## F.2. Constitution du manuel (vos 20 rubriques, §20, intégralement servies)

| # | Votre rubrique | Traitement retenu | Volume estimé |
|---|---|---|---|
| 1 | Couverture | A4, 3 volets possibles : fond nuit-deep (#0F2A43), titre en serif, motif de données vectoriel (nuage → courbe → damier de tableau de bord), bandeau « Édition 2026 », dos + 4ᵉ de couverture avec promesse et sommaire des 6 phases | 2 p. |
| 2 | Page de titre | Titre, sous-titre, édition, date, mention de version, avertissement sur la fraîcheur des informations logicielles | 1 p. |
| 3 | Préface | À qui s'adresse ce manuel, ce qu'il exige, ce qu'il ne promet pas, comment le lire (3 stratégies : 10 h/sem · immersion · module par module) | 3 p. |
| 4 | Objectifs de la formation | Les 20 objectifs + la matrice de couverture (§A.3) | 4 p. |
| 5 | Parcours pédagogique | Les 6 niveaux et leurs portes, les 12 principes, le gabarit de chapitre, le cahier de l'apprenant, la méthode de travail | 9 p. |
| 6 | Sommaire | Détaillé à 3 niveaux (module → chapitre → section), paginé, à leaders pointillés, cliquable dans le PDF (généré automatiquement : voir §F.3) | 20 p. |
| 7–8 | Modules et chapitres | 22 modules × 4 à 8 chapitres = **143 chapitres rédigés** | **2 226 p.** (1 792 de chapitres à 12,5 p., dont énoncés et corrigés embarqués + 374 d'appareil de module + 60 de rendus annotés en M21) |
| 9 | Exemples | ~1 100 exemples concrets, tous chiffrés, issus du fil rouge ou des jeux satellites | intégrés |
| 10 | Exercices | 190 énoncés (180 de base + 10 d'options), format fiche, en fin de chapitre | **embarqués** : les 5,5 p. d'exercices par chapitre (787 p. au total) sont comptés dans les 12,5 p. du §F.4 |
| 11 | Corrigés | Corrigés détaillés pas à pas (démarche, résultat intermédiaire, résultat vérifié), dans le bloc 12 de chaque chapitre ; le format A les regroupera en tome 2 | inclus dans les 5,5 p. d'exercices |
| 12 | Projets | 30 projets (33 avec les options) : fiche de commande, livrables numérotés, grille, rendu exemplaire annoté ; la mission finale occupe à elle seule ≈ 130 p. | inclus dans 7–8 |
| 13 | Évaluations | 22 quiz de module (≈ 330 questions), 4 épreuves de palier, 2 soutenances, 23 grilles | inclus dans 7–8 |
| 14 | Corrigés des évaluations | Pour chaque question : la réponse, pourquoi, et l'erreur classique associée | inclus dans 7–8 |
| 15 | Glossaire | 620 termes, format imposé (*Terme — Définition simple — Explication — Exemple*), 3 index (français, anglais, fonctions et mots-clés) | **80 p.** |
| 16 | Feuille de route professionnelle | Débutant → junior → confirmé → BI Analyst → BI Developer, avec le détail de M22.C04 | 14 p. |
| 17 | Portfolio | 14 fiches de projet + modèles de présentation + critères de relecture | 12 p. |
| 18 | Ressources complémentaires | Documentation officielle par outil (liens précis), données ouvertes, livres, communautés, avec avis critique | 8 p. |
| 19 | Bibliographie / webographie | ≈ 90 références, format normalisé, **date de dernière consultation** pour chaque ressource en ligne | 8 p. |
| 20 | Conclusion générale | Ce que vous savez faire, les 5 erreurs qui restent, les 6 mois suivants, la posture professionnelle | 8 p. |
| — | Annexes | Raccourcis Excel, antisèches SQL et DAX, 9 checklists, dictionnaire de données du fil rouge, scripts d'auto-validation, note de licence, errata | **60 p.** |
| | **Total** | | **2 455 p.** | (= 39 d'ouverture + 2226 de modules + 190 d'appareil de fin, contrôlé ci-dessous)

**Contrôle de cohérence des volumes (à refaire à chaque révision).** Lignes 1 à 6 : `2 + 1 + 3 + 4 + 9 + 20 = 39 p.` d'appareil d'ouverture. Lignes 7–8 : **2 226 p.** (additionnées module par module au §F.4). Lignes 9 à 14 : **0 p. de plus**, elles décrivent du contenu déjà compté en 7–8. Lignes 15 à 20 et annexes : `80 + 14 + 12 + 8 + 8 + 8 + 60 = 190 p.` Total : **39 + 2 226 + 190 = 2 455 p.**, ce qui est bien le budget du §F.4 (`1 792 de chapitres + 434 d'appareil de module + 229 d'appareil du livre = 2 455`). Ce contrôle se relance avec `python3 tools/budget_pages.py` : il compare chaque ligne du §F.4 au calcul et échoue si une colonne ne tombe pas juste.

**Structure interne type d'un module dans le manuel :**
`page d'ouverture (titre, promesse, carte des chapitres, prérequis, durée, outils, livrable final du module)` → `chapitres 1..n (gabarit 16 blocs)` → `projet du module` → `évaluation (récupération, quiz, exercices, étude de cas, corrigés)` → `bilan de compétences ("Je sais maintenant / Je suis capable de / Outils maîtrisés / Niveau atteint / Pour passer au module suivant" — votre §10)` → `auto-positionnement sur la grille des niveaux`.

## F.3. Chaîne de production documentaire et mise en page (votre §22)

**Méthode retenue : une source unique, deux rendus.** Le contenu est écrit en Markdown structuré (un fichier par chapitre, numérotés `Mxx_Cxx_titre.md`) puis **composé** vers le PDF par un moteur typographique, avec un gabarit CSS/LaTeX commun. Conséquences : (a) cohérence graphique garantie sur 1 100 pages parce qu'elle est *programmatique* et non manuelle ; (b) corrections de forme en un point ; (c) une version web HTML lisible sur téléphone en bonus naturel, ce que vous demandiez (« agréable à lire sur ordinateur, tablette, téléphone, et en imprimé »).

| Élément de mise en page | Exécution |
|---|---|
| Format | **A4 (210 × 297 mm)**, marges intérieures élargies pour la reliure (18/22/20/20 mm), grille de 1 colonne, corps de texte 10 pt |
| Typographie | Titres en serif éditoriale (ex. Source Serif / Charter), texte en serif lisible (ex. EB Garamond / Source Serif), code en **JetBrains Mono** avec accents et FCFA, tableaux en sans-serif condensée. Hiérarchie : Module (24 pt) > Chapitre (18 pt) > Section (13 pt) > Sous-section (11 pt) > corps 10 pt, interligne 1.32 |
| En-têtes / pieds | En-tête : *nom du module* à gauche, *titre du chapitre* à droite, filet ; pied : n° de page extérieur, *La Voie des Données* centré, date d'édition intérieure. Pages de début de module sans en-tête |
| Pagination | Recto/verso, numéro continu depuis la préface en chiffres romains, corps en arabes ; les 6 premières pages non numérotées |
| Tableaux | Règles horizontales seulement, en-tête répété si le tableau change de page, alignement des nombres à droite et sur la virgule, légende numérotée (`Tableau 12-3`) |
| Encadrés | Les 6 types §B.4, largeur de cadre égale, coins non arrondis, icône unique |
| Code | Blocs à filet gauche, numéro de listing (`Listing 8-4 · pandas — agrégation par magasin`), langage indiqué, surlignage des 3 lignes à retenir, jamais de code coupé en milieu de ligne |
| Schémas et figures | **Tous générés en SVG/HTML intégrés** (diagrammes d'architecture, modèles de données, flux ETL, exemples de dashboards en wireframe annoté, mini-graphiques d'exemple) : nets à l'impression 300 ppp et lisibles sur téléphone. Les captures d'écran sont laissées en **emplacements réservés** avec légende, contenu exact décrit et zone à encadrer — choix assumé, détaillé §H.3 |
| Graphiques | Conçus selon M10 (ils s'enseignent eux-mêmes), palettes accessibles, valeurs affichées sur les barres, pas de 3D, formats FCFA localisés |
| Sommaire | À 3 niveaux, lignes de conduite, hyperliens internes + signets PDF + table des matières cliquable |
| Qualité impression | Export 300 ppp, aplats en RVB→CMJN ou PDF/X, tests de contraste AA, vérification des veuves et orphelines sur les encadrés |
| Confort numérique | Deux exports : (1) PDF A4 pour lecture et impression ; (2) **PDF A5/recto ou version HTML** pour téléphone, avec police plus grande et tableaux à défilement horizontal ; liens internes actifs dans tous les cas |

## F.4. Budget de pages et de production, module par module

**Règle de calibrage (unique et vérifiable) :** `pages d'un module = chapitres × 7 + pages d'énoncés d'exercices + pages de corrigés et d'évaluations`. Le chiffre « 7 » est le calibre retenu par chapitre : les 16 blocs du gabarit §B.3 tenus serrés (0,5 p. d'objectifs, 1 p. de cours profond par notion, 1 p. de démonstration, 0,5 p. d'erreurs et de bonnes pratiques, énoncés comptés à part, 0,5 p. de résumé). Les colonnes s'additionnent ; aucune ligne n'est posée « à l'œil ».

| Module | Chap. | Chapitres × 12,5 p. | Appareil de module | **Pages** | Séances de production | Priorité |
|---|---|---|---|---|---|---|
| M01 | 7 | 88 | 17 | **105** | 2 | Immédiate (après validation) |
| M02 | 8 | 100 | 17 | **117** | 3 | Immédiate |
| M03 | 8 | 100 | 17 | **117** | 3 | Immédiate |
| M04 | 6 | 75 | 17 | **92** | 2 | Haute |
| M05 | 5 | 63 | 17 | **80** | 2 | Haute |
| M06 | 5 | 63 | 17 | **80** | 2 | Haute |
| M07 | 8 | 100 | 17 | **117** | 3 | Haute |
| M08 | 8 | 100 | 17 | **117** | 3 | Haute |
| M09 | 6 | 75 | 17 | **92** | 2 | Haute |
| M10 | 7 | 88 | 17 | **105** | 2 | Moyenne |
| M11 | 7 | 88 | 17 | **105** | 2 | Moyenne |
| M12 | 6 | 75 | 17 | **92** | 2 | Haute |
| M13 | 7 | 88 | 17 | **105** | 2 | Haute |
| M14 | 8 | 100 | 17 | **117** | 3 | Haute |
| M15 | 7 | 88 | 17 | **105** | 3 | Haute |
| M16 | 5 | 63 | 17 | **80** | 2 | Moyenne |
| M17 | 6 | 75 | 17 | **92** | 2 | Moyenne |
| M18 | 7 | 88 | 17 | **105** | 3 | Moyenne |
| M19 | 6 | 75 | 17 | **92** | 3 | Moyenne |
| M20 | 6 | 75 | 17 | **92** | 2 | Moyenne |
| M21 | 6 | 75 | 77 | **152** | 5 | Dernière, la plus lourde (rendus exemplaires annotés) |
| M22 | 4 | 50 | 17 | **67** | 2 | Dernière |
| **Sous-total des 22 modules obligatoires** | **143** | **1 792** | **434** | **2 226** | **55** | |
| Pages d'appareil (couverture 2, titre 1, préface 3, objectifs 4, parcours 9, sommaire 20) | — | — | — | 39 | — | |
| Glossaire (620 termes) + 3 index | — | — | — | 80 | 2 | |
| Feuille de route, portfolio, ressources, bibliographie, conclusion | — | — | — | 50 | 1 | |
| Annexes (antisèches, checklists, dictionnaire du fil rouge, errata) | — | — | — | 60 | 1 | |
| **MANUEL COMPLET** | **143 chap.** | | | **2 455 p.** (2 226 + 229 d'appareil) | **≈ 60 séances** (55 modules + 5 assemblage) | |
| Options M23–M25 | 14 | 175 | 51 | **226** | 3 | si activées : **157 chap. · 2681 p.** |

> **Mesure M01 et décision de calibrage (17 septembre 2026).** Le module M01, rédigé, autovalidé et composé, fait
> **103 pages de contenu** (110 avec la couverture et la table des matières) : 86 pages pour ses sept chapitres —
> de 11 à 14 pages chacun, 42 044 mots, 88 encadrés, 37 exercices autonomes tous corrigés —, 3 pages d'ouverture,
> 3 de bilan de compétences, 5 de projet, 6 d'évaluation. Le budget antérieur (7 pages par chapitre, énoncés et
> corrigés comptés « à part », 71 pages pour M01) sous-estimait le module de 45 %, parce que le §B.3 place les blocs
> 10 à 13 *dans* le fichier de chapitre et que la règle « aucun chiffre inventé » ajoute les tables de bornes, de
> contrôles et de résultats attendus. **Décision actée : le contenu n'est pas sacrifié au format.** Le calibre est
> rebasé à **12,5 pages par chapitre**, le budget §F.4 est recalculé en conséquence (**≈ 2455 pages** en intégral,
> **747** à la fin de M07, **≈ 1692** en condensé), et chaque module suivant est mesuré à la même aune par
> `tools/budget_pages.py`. Un chapitre qui descend sous 10 pages signale un bloc 5 ou 12 bâclé ; un chapitre qui
> dépasse 16 pages signale un cours qui raconte au lieu de faire faire : les deux sont des défauts, pas des vertus.
>
> **Mesure M02 (18 septembre 2026).** Huit chapitres, **94 pages** (de 11 à 13 par chapitre), 49 149 mots, 97 encadrés,
> 40 exercices autonomes tous corrigés, 4 mini-projets, plus 6 pages de projet et 6 d'évaluation : **113 pages** avec
> la couverture et la table des matières, pour un budget additif de 117 (−3 %, dans la tolérance de ±15 %). La
> densité mesurée passe à 488 mots par page (457 à M01) sans que la matière baisse : ce sont les tableaux de bornes,
> de contrôles et de sorties de calcul qui remplacent de la prose. Les chiffres annoncés (143 chapitres, 2 455 pages)
> restent donc valables ; aucune ligne de §F.4 n'est rebasée à ce stade.
> 

### Les trois formats d'édition — décision à prendre **avant** la rédaction

Produire ≈ 2455 pages d'un bloc est possible mais lent ; ce qui compte, c'est que l'apprenant puisse **pratiquer tôt**. Trois formats, même contenu de base :

| Format | Volume | Ce qui change | Pour qui | Délai relatif |
|---|---|---|---|---|
| **A — Manuel de référence, 2 tomes** | T1 ≈ 1363 p. (M01–M13 : 1324 p. de modules + 39 p. d'appareil d'ouverture) · T2 ≈ 1092 p. (M14–M22 : 902 p. + 190 p. d'appareil de fin) — total 2455 p. | rien n'est amputé ; les corrigés sont dans un tome séparé pour préserver la lecture active | vous voulez LE manuel unique, imprimable, et une valeur de référence durable | 100 % |
| **B — Tome unique condensé** | ≈ 1692 p. | matière ramenée à 5 p. et exercices embarqués à 4 p. par chapitre (9 p./chapitre, 1 287 p.), appareil de module réduit à 8 p. (176 p.), corrigés en clé commentée, appareil + glossaire de 420 termes (229 p.) | un seul livre à porter, plus digeste ; la profondeur des corrigés baisse d'environ 35 % | ~70 % |
| **C — Parution progressive, module à module** | **747 p.** à l'achèvement de M01–M07 (N2 atteint : 105 + 117 + 117 + 92 + 80 + 80 + 117 + 39 d'ouverture = 747), puis les modules suivants publiés au rythme de leur achèvement | chaque module livré est utilisable immédiatement (PDF daté, numéroté) ; l'assemblage final reste possible en format A | **recommandé** : vous travaillez dans le manuel pendant qu'il s'écrit, et vous arbitrerez le volume final avec de l'expérience | 100 % au total, mais 40 % utiles dès le 3ᵉ lot |

> **Recommandation de production : format C, avec verrou de bascule en A.** Le format C sert votre objectif réel — apprendre, pas accumuler des pages — et il permet de corriger la maquette sur les 300 premières pages avant d'en engager 1 600. Le tome T2 du format A est alors produit gratuitement à la fin, puisque les corrigés existent déjà en fichier source. Un format « B » ultérieur (sélection des 8 modules essentiels, ~450 p.) reste envisageable comme version découverte, sans reprise du texte.

Les jeux de données, le moteur d'auto-validation et les gabarits de figures sont produits **une fois, avant le premier module** (ils alimentent M01 à M21) : prérequis technique de l'étape 2, ≈ 1,5 séance.

## G.1. Porte de validation de module (appliquée à chaque module, votre §Étape 3)

| # | Contrôle | Méthode | Critère de passage |
|---|---|---|---|
| Q1 | Cohérence pédagogique | Les 16 blocs présents · chaque objectif du module est porté par au moins un chapitre et prouvé par un exercice ou le projet | 16/16 blocs, 100 % |
| Q2 | Progression réelle | Une notion nouvelle par bloc majeur ; aucune fonction non enseignée utilisée dans un exemple ou un corrigé | 0 violation |
| Q3 | Validité technique | SQL exécuté · Python exécuté · formules Excel recalculées dans un classeur généré · chiffres recalculés depuis les CSV | 100 % d'exécution sans erreur |
| Q4 | Cohérence des données | Totaux du module = totaux du `verites_terrain.csv` · joints sans perte ni explosion · types stables | écart 0 |
| Q5 | Exercices ↔ corrigés | Chaque énoncé a une correction complète et reproductible, avec le résultat intermédiaire | 100 % |
| Q6 | Redondance et contradiction | Recherche croisée des définitions et des chiffres dans tous les modules déjà écrits (le glossaire est la source unique des définitions) | 0 contradiction, 1 seule définition par terme |
| Q7 | Vocabulaire | Tout terme non commun défini au premier emploi, ajouté au glossaire et à l'index FR/EN | 100 % |
| Q8 | Fraîcheur outil | Table C.5 consultée ; mention de version ou mention "à vérifier" | 100 % des claims outillés |
| Q9 | Accessibilité | Confort sur téléphone (pas de tableau de plus de 6 colonnes sans version alternative), contraste, pas d'information portée par la seule couleur | conforme |
| Q10 | Test de lecture | Une relecture "débutant simulé" : 10 passages où le lecteur doit relire = correction | ≤ 5 passages à relire par module |

Un module n'est déclaré terminé qu'avec les 10 contrôles au vert ; sinon la liste des écarts ouverts est publiée en début de module suivant (transparence de production, qui est aussi un objet pédagogique sur la qualité).

## G.2. Exécution réelle : ce qui a été vérifié dans cet environnement

| Capacité | État vérifié le 17/09/2026 | Usage dans le projet |
|---|---|---|
| Python 3.13 + pandas 2.2.3 (env.), numpy, matplotlib, seaborn, plotly, scikit-learn, openpyxl, python-docx | disponibles | Exécution de tout code enseigné, génération des jeux de données et des classeurs |
| **DuckDB 1.5.5** | installé et fonctionnel | Validation SQL réelle (M06, M07, M11, M05.C03) |
| `sqlite3` | disponible | Base de secours pour les exercices |
| Génération PDF (moteur HTML/CSS ou LaTeX) | à installer au moment de l'assemblage (étape 5) | Composition du manuel |
| Pas de licence | Excel, Power BI, Tableau ne peuvent pas s'exécuter ici | **Limitation assumée** : les contenus de ces outils sont rédigés par menus/émoticônes décrits, captures à insérer, et DAX/Power Query **signalés comme non exécutés** avec points de contrôle manuels. Toute la logique chiffrée qui les sous-tend est, elle, exécutée en SQL/pandas sur les mêmes données |

## G.3. Registre des risques du projet (et leur parade, intégrée à la conception)

| Risque | Probabilité | Impact | Parade intégrée |
|---|---|---|---|
| Obsolescence logicielle du manuel | Élevée (Power BI monthly, pandas 3, licences Tableau) | Fort | Table C.5 avec date de vérification · préférence pour les concepts stables (jointure, grain, agrégation, contexte de filtre) sur les raccourcis d'interface · annexe « points de rupture » et fichier `errata` |
| Code enseigné non exécutable | Moyenne | Fort | Règle Q3 : rien n'est publié sans exécution ; environnement contrôlé documenté en G.2 |
| Dérive vers une encyclopédie illisible | Élevée (22 modules, ≈ 2455 p.) | Moyen | Budget de pages par module (F.4) et règle de compression du gabarit (B.3) ; « pas de notion sans application » (A.1) |
| Redondance entre modules (votre §23) | Moyenne | Moyen | Glossaire comme source unique de définition · 20 objectifs matricés (C.2) · 1 seul enseignement *initial* par notion, les autres en réinvestissement explicite |
| Incohérence des jeux de données entre modules | Moyenne | Fort | Générateur unique versionné + vérité terrain + contrôle automatique à chaque module (Q4) |
| Frustration sur les licences (Power BI/Tableau) | Moyenne | Moyen | Plan B gratuit validé pour chaque projet : Power BI Desktop suffit jusqu'au partage, Looker Studio/Metabase/Tableau Free selon l'état du moment, et tous les livrables portables en PDF |
| Énergie/connexion instables | Moyenne | Moyen | Tout est réversible hors-ligne : jeux de données, bases, scripts et docs locales ; aucune dépendance à un service cloud pour apprendre |
| Surcharge de l'apprenant (abandon, le vrai risque n°1 d'un autodidacte) | Élevée | Fort | Séances de 90 min · réussite obligatoire en E1 avant toute difficulté · portes de niveau non punitives avec rattrapage ciblé · journal de bord · 3 rythmes de lecture possibles |

## G.4. Contrôle qualité transversal (votre §23) — ce qui sera vérifié à l'étape 4, pas seulement par module

Progression des difficultés (graphe de prérequis, absence de cycle et d'à-peu-près) · cohérence des exemples (le fil rouge ne contredit jamais ses propres chiffres) · validité des formules statistiques (recalculées) · validité des requêtes SQL et du code Python (exécutés) · cohérence exercices/corrigés · absence de chapitre redondant (audit croisé des 143 titres et des 620 définitions) · actualité des outils (table C.5) · cohérence des projets (chaque projet utilise au moins un livrable d'un module antérieur). **Toute erreur détectée est corrigée à la source et l'errata est publié dans le manuel** : c'est aussi une leçon de méthode, et le manuel l'assume comme telle.

---

# PARTIE H — PROTOCOLE DE PRODUCTION ET VALIDATION

## H.1. Étapes et livrables, conformes à votre §25

| Étape | Livrable | Format | Critère d'achèvement |
|---|---|---|---|
| **1** | **Cette architecture** (8 parties, 143 chapitres planifiés, référentiels chiffrés) | Markdown + PDF lisible | ✔ produite ; **en attente de votre validation** |
| **1.5** | Socle technique : générateur des 9 tables du fil rouge + 7 jeux satellites, vérité terrain, base DuckDB, scripts d'auto-validation, gabarits SVG, CSS de mise en page | dépôt de fichiers dans `formation-data-bi/` | Totaux cohérents, scripts exécutés, contrôle Q4 au vert |
| **2** | Modules rédigés, **par lots de 2 à 3 modules** (phase = unité de livraison) | Markdown par chapitre | chaque module passe les 10 contrôles G.1 |
| **3** | Vérification pédagogique et technique de module | fiche de contrôle Q1–Q10 publiée avec le module | 10/10 au vert |
| **4** | Assemblage : glossaire unifié, index, sommaire, corrections croisées | document consolidé | G.4 complet, 0 contradiction |
| **5** | Composition du manuel : couverture, A4, pagination, encadrés, figures | PDF + HTML | test de lecture sur A4, A5 et téléphone |
| **6** | Revue finale de livraison | rapport de revue + errata | 1 relecture technique complète + relecture "débutant simulé" |

**Granularité de livraison proposée pour l'étape 2 :** par phase (6 lots) plutôt que module par module, pour trois raisons : (a) un module seul ne permet pas de vérifier les liens entre modules, qui est justement le point faible des formations produites par morceaux ; (b) les corrigés et le glossaire se déduisent mieux d'un ensemble ; (c) cela représente 2 à 4 tours de production par lot, soit ~13 lots au total. Si vous préférez le module par module pour un contrôle plus fin, l'architecture ne change pas, seul le rythme.

## H.2. Quatre décisions à prendre avant de rédiger (à réponse courte)

1. **Rythme de rédaction.** (a) 1 module par tour de conversation, le plus fin et le plus lent ; (b) **1 phase par tour** (recommandé) : 2–3 modules complets avec exercices, corrigés, projet, évaluation et fiche de contrôle ; (c) gros volumes, plus rapide mais plus difficile à relire d'un trait.
2. **Poids des exercices.** (a) 180 exercices + tous les corrigés (recommandé, c'est ce qui rend l'auto-formation possible) ; (b) 180 énoncés, corrigés par module à la demande ; (c) concentré sur les projets (moins d'exercices, plus de cas).
3. **Format d'édition.** (a) **A — deux tomes**, ≈ 2455 p., tout est développé ; (b) **B — tome unique condensé**, ≈ 1692 p. ; (c) **C — parution progressive** (recommandé) : vous pratiquez dès le module 1, assemblage intégral en fin de parcours ; (d) **B+C** : parution progressive en version condensée, puis tome intégral à la demande.  
4. **Fichiers de travail.** (a) je dépose aussi les vrais fichiers dans le workspace (CSV, `.db`, notebooks, classeurs) : vous pouvez pratiquer immédiatement — **fortement recommandé** ; (b) le manuel seul, avec les données reproduites en tableaux dans le texte.

## H.3. Quatre écarts assumés par rapport au cahier des charges, à valider explicitement

| # | Votre texte | Ce que je propose | Pourquoi |
|---|---|---|---|
| 1 | « des captures d'écran à insérer » | Emplacements réservés + description exacte de l'écran + exercices de reproduction | Je ne peux pas exécuter Excel/Power BI ici. Une capture inventée serait une tromperie. Alternative possible : je produis des **wireframes SVG fidèles** (mêmes libellés de menus, mêmes fenêtres, mêmes valeurs affichées), imprimables, qui enseignent le geste sans simuler une capture réelle |
| 2 | SQL : « optimisation de requêtes » en module 5 | Déplacé en M11.C06 (après les fenêtres) et partiellement en M24 | Un débutant sans serveur administré ne peut pas mesurer un plan d'exécution ; enseigné trop tôt, ce n'est que du vocabulaire |
| 3 | 12 secteurs d'activité en un module | 7 chapitres sectoriels couvrant les 12 secteurs | 12 chapitres séparés = ~35 % de contenu redondant, ce que votre §23 interdit. La couverture reste complète, seule la découpe change |
| 4 | Un module 1 très riche (7 rubriques conceptuelles + 6 rôles métier) | M01 recentré sur la lecture des données ; les rôles métiers et la chaîne de valeur déplacés aux chapitres 6–7 et approfondis en M12/M22 | Les distinctions Data Analyst/BI/Data Scientist/Data Engineer s'apprécient quand on a pratiqué les trois outils ; à J+3, elles ne sont que des mots. Elles sont donc présentées tôt **en survol**, approfondies en M01.C07, puis stabilisées en M12 et M22 |

## H.4. Points ouverts (questions à vous poser maintenant)

1. Validation de l'architecture, avec les 4 écarts de H.3 ?
2. H.2 (1) (2) (3) (4) : rythme, poids des exercices, format d'édition, dépôt de fichiers ?
3. Contexte à privilégier pour les exemples : **commerce/grossiste** (fil rouge actuel), **banque/microfinance**, **ONG/humanitaire**, **administration**, ou **agriculture** ? Le fil rouge peut être remplacé avant la production du socle sans rien casser.
4. Faut-il un **module de préparation aux certifications** (PL-300 et consorts) développé, ou la mention stratégique de M22.C04 suffit-elle ?
5. **Certifications.** faut-il développer un module de préparation aux certifications (PL-300 et concurrentes) ou en garder la seule analyse stratégique en M22.C04 ?
6. **Options.** faut-il ajouter **R** (M23) et **Data engineering** (M24) au socle dès le départ plutôt qu'en option ?

---

## H.5. Journal des arbitrages de l'étape 1 (traçabilité de production)

Parce que le §12 du cahier des charges impose traçabilité et documentation, chaque décision de conception est consignée ici avec sa raison. Ce journal sera tenu à jour à chaque lot de production et publié en annexe du manuel.

| # | Décision | Alternative écartée | Raison |
|---|---|---|---|
| D01 | 22 modules obligatoires au lieu des 18 du cahier des charges, plus 3 options | garder le découpage du cahier des charges | absorber §12 (qualité) et §14–15 (emploi) sinon jamais enseignés ; scinder SQL en 3 volets pour la charge cognitive |
| D02 | Excel avant statistiques-outil, SQL/Python ensuite | commencer par Python (plus « pro ») | votre consigne explicite ; et Excel est le seul outil déjà présent chez l'employeur visé |
| D03 | Nettoyage scindé en discipline (M04) + mise en œuvre comparative (M05) | un seul module « nettoyage » | la comparaison d'outils est une méta-compétence : elle s'acquiert après avoir fait le geste trois fois |
| D04 | Auto-validation exécutable des exercices SQL/Python | correction seulement rédigée | sans elle, l'autodidacte ne sait pas s'il a raison ; c'est le point de rupture n°1 des formations en autonomie |
| D05 | Corrigés dans un tome/clé séparé | corrigé immédiatement après l'énoncé | la lecture active se casse si la réponse est à la page suivante |
| D06 | Un fil rouge unique + 7 jeux satellites | 20 jeux de données indépendants | maîtrise réelle de la donnée, et une seule source de cohérence à contrôler (§G.4) |
| D07 | Wireframes SVG produits par mes soins au lieu de captures simulées | captures inventées | une capture d'un écran que je n'ai pas vu est une erreur factuelle, pas une approximation |
| D08 | DAX enseigné trois fois (M03.C08 → M14.C05 → M15) | un seul module DAX | le contexte de filtre ne se comprend qu'en revenant sur des modèles de plus en plus riches |
| D09 | Calibre **12,5 p./chapitre** (7 de matière + 5,5 d'exercices embarqués), budget additionné (2 455 p.), **rebasé sur la mesure de M01 du 17/09/2026** | volume laissé « au sentiment », ou calibre théorique que la rédaction réelle ne respecte pas | un budget non additif est un budget non tenable ; un calibre non mesuré est un calibre décoratif ; et il permet l'arbitrage des formats A/B/C |
| D10 | R, data engineering et cartographie en options | modules obligatoires | votre §1 conditionnait R à sa pertinence ; imposer les trois alourdirait de 30 % pour un bénéfice d'emploi marginal en BI d'entreprise |
| D11 | pandas 3.x comme référence, avec annexe de migration | rester sur pandas 2.x (encore très répandu) | 3.0 est sorti le 21/01/2026 et une écriture dépréciée apprise aujourd'hui sera un réflexe faux demain |
| D12 | Titre « La Voie des Données » | « Du Tableau Brut au Tableau de Bord » (n°7, 18/20) | plus court, plus mémorable, et il porte la progression sans promettre de certification |

---

## Fin de l'Étape 1 — Résumé d'une page

- **22 modules + 3 options, 143 chapitres, 6 phases, 6 niveaux, 660 h**, 180 exercices (190 avec les options), 30 projets, 28 épreuves évaluées, 620 termes de glossaire, **≈ 2 455 pages** en manuel intégral (trois formats d'édition chiffrés au §F.4, calibre mesuré sur M01) ; **747 pages utilisables dès la fin de M07**.
- Progression **fondations → Excel → qualité → SQL → Python → EDA → visualisation → BI → modélisation → Power BI → DAX → outils → automatisation → secteurs → prédictif → communication → projets → emploi**. Rien de technique avant la culture de la donnée ; Python après SQL ; DAX enseigné trois fois ; le nettoyage enseigné comme une discipline et non comme une tâche.
- Deux innovations structurantes : **l'auto-validation exécutable** (le débutant autodidacte peut vérifier seul qu'il a juste) et le **livrable signature** (la carte de définition des KPI, réutilisée de M12 à M21), qui fait du manuel un ensemble au lieu d'une suite.
- Chaque affirmation technique sera exécutée avant publication ; chaque donnée chiffrée recalculée depuis un générateur unique ; chaque fait logiciel daté.
- **Titre proposé et retenu : *La Voie des Données*.**
- **État : prêt à entrer en Étape 1.5 (socle technique de données et de gabarits) dès votre validation, puis à dérouler les modules, phase par phase.**
