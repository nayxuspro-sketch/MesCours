# Plan M09 — Analyse exploratoire de données (EDA)

**Module M09 · 6 chapitres · 30 h · niveau N3 · prérequis M02 (statistiques) et M08 (pandas) ; M05/M07 utiles.**

> **L'idée du module.** M08 a appris à produire des chiffres par trois chemins ; M09 apprend
> à **poser les bonnes questions** à un jeu de données qu'on ne connaît pas, et à n'affirmer
> que des conclusions **provisoires, correctement exprimées**. Le fil conducteur est un
> **protocole en 10 étapes** (inspecter, comprendre les variables, détecter les problèmes,
> premières statistiques, tendances, anomalies, relations, hypothèses, visualisations,
> conclusions provisoires) appliqué **trois fois** sur trois jeux contrastés : les ventes de
> la quincaillerie (fil rouge M07/M08), un **centre de santé** (fréquentation, ruptures de
> médicaments essentiels) et un **établissement scolaire** (résultats, absentéisme). Le
> **projet M09.P** impose un chronomètre — « 3 heures avec un fichier que personne n'a
> regardé » : c'est la condition pour apprendre à ne pas explorer sans fin. La **transition**
> finale annonce M10 (visualisation) : *« Vos résultats sont justes. S'ils sont illisibles,
> ils ne serviront à rien. »*

## 1. Cadrage

### 1.1 Position dans l'architecture

- **Phase** 2 — Maîtrise opérationnelle (palier P2), **dernier module du palier** avant
  l'épreuve de validation P2 ; **avant** M10 (visualisation), M14 (Power BI), M17
  (automatisation), M21 (fil rouge en Python).
- **Après** M08 (pandas : l'apprenant sait lire, nettoyer, agréger, exporter).
- **Prérequis** :
  - **M02** — les statistiques descriptives (moyenne, médiane, quartiles, écart-type,
    percentile) ; **indispensable** : toute la mesure de M09 est descriptive.
  - **M08** — pandas (le module est en pandas de bout en bout, `matplotlib`/`seaborn` pour
    l'exploration visuelle) ; le parallèle SQL sert d'accélérateur là où M07 a posé la
    requête équivalente (tendances, anomalies).
  - **M05/M07** utiles — le parallèle trois moteurs et la base de la quincaillerie.
- **Verrouillé** par M10 (on ne peut pas choisir un graphique par question si on ne sait pas
  poser la question), M14 (l'exploration précède le modèle), M17, M21.

### 1.2 Six compétences de sortie (la matrice de couverture)

1. **Inspecter sans se fier** : forme, types, premières lignes, doublons possibles — et
   produire la **« fiche d'entrée »** d'une analyse (variables, unités, sources, questions
   autorisées) en 30 minutes.
2. **Détecter les problèmes avant de mesurer** : doublons, manquants, valeurs impossibles —
   et savoir qu'un audit qui ne trouve **rien** est suspect, pas réconfortant.
3. **Résumer par variable** : les statistiques descriptives juste nécessaires (médiane vs
   moyenne, quartiles, extrêmes), chacune rattachée à une question métier.
4. **Lire les tendances** : séries temporelles simples, saisonnalité, comparaisons de
   périodes — et dire ce qui est **structurel** et ce qui est **bruit**.
5. **Traiter les anomalies** : ce qui est inhabituel, **comment le prouver** (position dans
   la distribution, répétition, cohérence avec le métier), et quoi en conclure — ni
   supprimer à l'aveugle, ni ignorer.
6. **Relier et conclure provisoirement** : corrélation vs causalité, segments, comparaison
   de groupes, les pièges d'inférence — et écrire une **conclusion provisoire** qui dit ses
   limites.

### 1.3 Fait du socle (à mesurer à l'étape 2 — `chiffres_manuel.py M09`)

- **Jeu 1 — la quincaillerie (fil rouge)** : réexport **déterministe** de la base M07 figée
  (comme le dossier M08 : `vente.csv` 50 008 lignes, 4 défauts connus, empreinte
  `b9a8d973119342ec…`) — le module doit **redonner les mêmes totaux** que M07/M08
  (CA propre 7 876 320 164 FCFA, plus gros mois 78 965 529 FCFA) : la constance du
  socle est le premier contrôle du protocole.
- **Jeu 2 — le centre de santé (à générer, `tools/dossier_M09.py`, graine 45)** :
  fréquentation du centre (consultations par jour, par motif, par tranche d'âge) + stocks de
  médicaments essentiels (entrées/sorties, seuil d'alerte, **ruptures**). Défauts plantés
  **et chiffrés** au moment de la génération (manquants sur les motifs, doublons sur les
  sorties de stock, une date dans le futur, un stock négatif) — chacun avec sa définition
  exacte dans le brief, comme en M04/M07.
- **Jeu 3 — l'établissement scolaire (à générer, graine 45)** : résultats d'une session
  (notes par matière, par élève) + **absentéisme** (retardes/absences par période). Défauts
  plantés et chiffrés (notes hors bornes, doublon d'élève, absence datée un jour férié,
  élève absent mais noté).
- **Fichier du projet M09.P — « le fichier que personne n'a regardé » (à générer, graine
  45)** : un export brut volontairement sale (en-tête mal nommé, mélange de séparateurs,
  colonnes inutiles, doublons, valeurs incohérentes) — l'apprenant a **3 heures,
  chronomètre en marche**.
- **Reproductibilité** : 2 exécutions successives de `chiffres_manuel.py M09` → diff = 0 ;
  `tools/dossier_M09.py` → diff = 0 sur les 3 jeux + le fichier projet.

### 1.4 Le projet M09.P — « 3 heures avec un fichier que personne n'a regardé »

- **Énoncé.** L'apprenant reçoit `fichier_inconnu.csv` (un export brut, 10 000 lignes
  environ, d'un contexte qu'il découvre **dans** le fichier). Chronomètre imposé : **3 h**.
  Le protocole en 10 étapes est autorisé (encouragé) ; l'exploration sans méthode est la
  faute que le projet punit.
- **Livrables** (grille /20, seuil 13) :
  - **P1 — La fiche d'entrée** (4 points) — complétée dans les 30 premières minutes :
    forme, variables (nom, unité, type, origine), 3 questions que le fichier **peut**
    répondre et 2 questions qu'il **ne peut pas** répondre.
  - **P2 — Le rapport d'EDA** (6 points) — les 10 étapes du protocole, chaque étape en
    une question + sa réponse chiffrée (sorties imprimées) ; les défauts trouvés chiffrés
    avec leur définition exacte.
  - **P3 — Les 4 graphiques** (5 points) — 4 graphiques (`matplotlib`/`seaborn`) qui
    **répondent** aux 4 questions les plus importantes du rapport (pas 4 jolis graphiques
    sans question) ; chaque graphique légendé : question + source + ce qu'on doit retenir.
  - **P4 — La note de conclusions provisoires** (5 points) — 1 page : ce que les données
    suggèrent, formulé **provisoirement** (chacun de ses affirmations porte sa limite :
    taille d'échantillon, période, variables manquantes) ; la corrélation n'est jamais
    présentée comme cause.
- **Règle du chronomètre.** À 3 h, on arrête et on rend ce qui est fait : un rapport de
  10 étapes à 80 % avec les limites honnêtes passe ; une exploration à 100 % sans
  structure ne passe pas. C'est la compétence du module : **s'arrêter** avec des
  conclusions provisoires, pas explorer jusqu'à n'en plus avoir.

### 1.5 Évaluation M09

- **Quiz** 15 Q (dont 5 « prédisez la sortie » — la sortie d'un bloc pandas court).
- **Étude de cas notée sur la qualité des questions** : sur un jeu fourni (le centre de
  santé, variant non vu), le candidat doit d'abord **poser** les 5 questions les plus
  pertinentes (notées pour leur pertinence métier, leur formulation falsifiable, et ce que
  le jeu peut ou ne peut pas répondre), puis y répondre. Une bonne question mal répondue
  vaut plus qu'une mauvaise question bien répondue — c'est l'inverse de M07/M08,
  délibérément.
- **Corrigés** : valeurs mesurées sur le socle (clés `m09_*` / `m09p_*`), chaque réponse
  annotée avec la question qui la motivait et son piège classique.
- **Épreuves de palier P2** : l'épreuve de validation P2 s'appuie sur M08 + M09 (produire
  des chiffres justes **et** en tirer des conclusions provisoires honnêtes).

### 1.6 Règles d'exécution (cadence héritée de M06—M08)

- **1 push par chapitre validé `--strict`** ; push forcé autorisé ; `.git` local supprimé
  après chaque push (bundle de secours avant) ; token GitHub ré-testé via curl avant
  chaque push.
- **Chiffres** : toute valeur ≥ 4 chiffres citée dans les `.md` est sourcée dans
  `chiffres_cites.json` (section M09, clés `m09_*`/`m09p_*`) ou reformulée ; les sorties
  publiées sont exécutées avant publication, jamais déduites.
- **Figures** : 6 planches SVG (une par chapitre), extension ≤ 776 px, jeu latin-1 étendu
  `set("é·èà—'\"«»→ê…×î←Éùç▼ô°\xa0§¹²³")`, embarquées dans les `.md` par
  `![…](../figures/…)` (convention M08), vérifiées par `controle_pdf.py`.
- **Moteurs** (règle §1.5) : DuckDB et SQLite **exécutés** quand le parallèle est montré
  (tendances/anomalies comparées aux requêtes M07) ; PostgreSQL **cité sans exécuté**.
- **Environnements** : écriture sous Python 3.13 / pandas **2.2.3** / matplotlib 3.10.9 /
  seaborn 0.13.2 ; le comportement pandas 3.x (venv 3.0.6) est cité pour les points de
  divergence (CoW, `resample`), sans en faire le sujet du module.
- **Typographie** : chaque glyphe utilisé dans un `.md` doit être composé dans le PDF
  (police DejaVuSerif latin-1 ; les ordinaux `ᵉ`/`ʳᵉ` passent — vérifié M07/M08).

### 1.7 Les 10 étapes du protocole (liste de référence — le fil du module)

| # | Étape | Question posée | Outil principal |
|---|---|---|---|
| 1 | **Inspecter** | « Qu'est-ce que j'ai entre les mains ? » | `shape`, `dtypes`, `head()`, `info()` |
| 2 | **Comprendre les variables** | « Que veut dire chaque colonne, en quelle unité, d'où vient-elle ? » | la **fiche d'entrée** (tableau variable → sens/unité/source) |
| 3 | **Détecter les problèmes** | « Y a-t-il des doublons, des manquants, des valeurs impossibles ? » | `duplicated()`, `isna()`, bornes métier |
| 4 | **Premières statistiques** | « Quelle est la forme de chaque variable clé ? » | `describe()`, médiane/quartiles, `value_counts()` |
| 5 | **Tendances** | « Ça monte, ça descend, ça cycle ? » | séries temporelles simples, `resample`, comparaisons de périodes |
| 6 | **Anomalies** | « Qu'est-ce qui est inhabituel, et comment le **prouver** ? » | position dans la distribution (quartiles, iqr), récurrence, cohérence métier |
| 7 | **Relations** | « Les variables bougent-elles ensemble ? » | corrélation, tableaux croisés, segments |
| 8 | **Hypothèses** | « Que puis-je affirmer, et sous quelle condition ? » | formulation falsifiable, contre-exemples dans les données |
| 9 | **Visualisations** | « Quel graphique répond à la question ? » | `matplotlib`/`seaborn` : courbe, barres, boxplot, histogramme, nuage |
| 10 | **Conclusions provisoires** | « Que dis-je, et quelles sont mes limites ? » | la **note d'EDA** : affirmation + limite, page par page |

> **Le protocole est un contrat, pas une check-list.** Une étape peut être vide (« aucune
> anomalie détectée — et voici les 3 contrôles que j'ai faits pour l'affirmer »), mais
> **jamais passée** : une étape sautée sans explication est un défaut du rapport, comme une
> requête SQL non exécutée l'est en M07.

## 2. Vocabulaire du module (à définir au premier emploi)

- **analyse exploratoire de données** — *exploratory data analysis (EDA)* — l'examen
  systématique d'un jeu de données inconnu pour en dégager des structures, des problèmes
  et des pistes, **avant** de modéliser.
- **fiche d'entrée** — le document de cadrage d'une analyse : variables, unités, sources,
  questions autorisées, durée prévue.
- **anomalie** — *anomalie / outlier* — une observation qui s'écarte de la distribution ;
  se prouve (position, récurrence, métier) avant d'être traitée.
- **point aberrant** — *outlier* — synonyme chiffré : la position dans la distribution
  (ex. au-delà de Q3 + 1,5 × iqr) le définit.
- **saisonnalité** — *saisonnalité* — la variation régulière et prévisible liée au cycle
  (saison, jour de semaine, mois).
- **corrélation** — *corrélation* — la mesure d'association entre deux variables ;
  **n'est jamais une causalité** (le piège du module).
- **biais de sélection** — *biais d'échantillonnage* — l'écart entre la population étudiée
  et la population visée, hérité de la façon dont les données ont été collectées.
- **conclusion provisoire** — une affirmation posée **avec** ses limites (période,
  échantillon, variables absentes), révisable aux données suivantes.
- **iqr** — *interquartile range* — Q3 − Q1 ; la largeur du « cœur » de la distribution,
  indépendante des extrêmes.
- **tableau croisé** — *tableau de contingence* — la fréquence d'un couple de modalités
  (ex. matière × trimestre).

## 3. Découpage en 6 chapitres

> **Rythme commun** (gabarit §B.3, 24 titres) : objectifs · pourquoi c'est important ·
> explication simple · vocabulaire · cours approfondi · exemple concret (fil rouge) ·
> démo pas à pas · erreurs fréquentes · bonnes pratiques · exercice guidé (/10) · exercices
> autonomes · correction détaillée · mini-projet · boîte à outils · résumé · à retenir ·
> évaluation formative. Le **fil rouge** du chapitre est toujours l'un des 3 jeux ; les
> jeux 2 et 3 y apparaissent pour la première fois en C02 (centre de santé) et C05
> (scolaire), puis sont rejoués par l'apprenant sur une variante (règle « 3 études de cas
> complètes et contrastées »).

### C01 — Le protocole en 10 étapes, la « fiche d'entrée » et le temps à y consacrer (5 h)

- **Étapes du protocole : 1—2** (inspecter, comprendre les variables).
- **Contenu** : pourquoi on explore (le jeu inconnu, la question métier, le livrable
  provisoire) ; les 10 étapes comme contrat ; inspecter sans se fier (`shape`, `dtypes`,
  `head`, `info` — et pourquoi `head(5)` peut mentir) ; la **fiche d'entrée** (tableau
  variable → sens / unité / source / question autorisée) ; **le temps** : 30 minutes
  maximum à l'entrée, et pourquoi (le chronomètre du projet) ; les limites d'un fichier
  (ce qu'il peut / ne peut pas répondre).
- **Fil rouge** : la quincaillerie — la fiche d'entrée des 13 colonnes de `vente.csv`
  (récapitule M07/M08, y compris les unités FCFA et la convention des dates).
- **Figure** : les 10 étapes en chaîne (étape → question → outil), avec les 3 jeux comme
  3 trajets.
- **Ancres projet/évaluation** : P1 (la fiche d'entrée dans les 30 premières minutes).

### C02 — Audit et premières statistiques, cadrage des hypothèses (5 h)

- **Étapes du protocole : 3—4** (problèmes, statistiques).
- **Contenu** : les 3 familles de défauts (doublons, manquants, valeurs impossibles) et
  les contrôles qui les trouvent ; **l'audit vide est suspect** (le contrôle du contrôle :
  quoi vérifier quand `isna().sum() == 0` partout) ; les statistiques juste nécessaires
  (médiane vs moyenne sur une distribution asymétrique, quartiles, iqr, extrêmes) ;
  `describe()` lu colonne par colonne ; **cadrer une hypothèse** : la formuler
  falsifiable (« si c'est un problème de saison, les 4 étés doivent ressembler plus entre
  eux qu'à leurs hivers ») avant de la tester.
- **Jeu 2 intro** : le **centre de santé** arrive ici — audit (manquants sur les motifs,
  doublons sur les sorties de stock, une date dans le futur, un stock négatif — les 4
  défauts plantés) puis statistiques (fréquentation : médiane vs moyenne des
  consultations/jour).
- **Figures** : la matrice « famille de défaut → contrôle → exemple chiffré ».
- **Ancres** : P2 (les défauts du rapport chiffrés avec leur définition exacte) ; le
  parallèle SQL (M07 : `COUNT(*)` vs `COUNT(DISTINCT)`) pour le dédoublonnage.

### C03 — Tendances : séries temporelles simples, saisonnalité, comparaisons de périodes (5 h)

- **Étape du protocole : 5** (tendances).
- **Contenu** : la série simple en pandas (`set_index` + `resample` — le rappel `'ME'` de
  M08) ; décomposer **tendance / saisonnalité / bruit** à l'œil et au chiffre (moyennes
  glissantes simples, même mois sur N années) ; comparer des périodes **à taille égale**
  (le piège : 2025 vs 2026 incomplets, la période partielle qui ment) ; saisonnalité du
  jour de semaine (le rappel `dayofweek == 6` de M08) ; dire **structurel vs bruit**
  (l'amplitude vs la variabilité résiduelle).
- **Fil rouge** : la quincaillerie — les 120 mois de la vue mensuelle (M07/M08), la
  saisonnalité des fêtes de fin d'année, la comparaison 2025 vs 2026 **à mois égal**.
- **Jeu 2** : la fréquentation du centre de santé — le pic de saison (grippe/pluie),
  la journée type (creux de midi), la rupture de stock qui **coupe** une tendance
  (tendance interrompue ≠ tendance retombée).
- **Figures** : la décomposition tendance/saisonnalité/bruit sur un exemple chiffré.
- **Ancres** : P3 (le graphique « ça monte, ça descend, ça cycle ? ») ; le parallèle SQL
  (`GROUP BY mois` de M07 vs `resample` pandas — même nombre, deux écritures).

### C04 — Anomalies et raretés : ce qui est inhabituel, comment le prouver, quoi en conclure (5 h)

- **Étape du protocole : 6** (anomalies).
- **Contenu** : définir l'anomalie **avant** de la chercher (seuil par iqr, par borne
  métier, par comparaison à la période) ; **prouver** (position dans la distribution +
  récurrence + cohérence métier) — l'anomalie non prouvée est un soupçon ; les 3 décisions
  après détection (corriger, exclure **en le documentant**, garder **en le signalant**) —
  jamais supprimer silencieusement ; les anomalies **structurelles** (le stock négatif qui
  révèle un défaut de saisie, pas une erreur) ; les rares qui ne sont pas des anomalies
  (le gros client n'est pas un bug — le top 1 de M07 est un client, pas un défaut).
- **Fil rouge** : la quincaillerie — les 8 doublons (anomalie structurelle révélée par
  l'audit), les montants > 100 000 FCFA (rares mais légitimes), le plus gros mois
  78 965 529 (pic expliqué, pas écarté).
- **Jeu 2** : les ruptures de médicaments essentiels (l'anomalie qui **compte** : une
  rupture de paracétamol 3 jours est un signal métier, pas un chiffre à corriger) et la
  date dans le futur (défaut de saisie prouvé par le métier, pas par la statistique).
- **Figures** : la boîte à outils de preuve (iqr / borne métier / récurrence / métier)
  avec les 4 cas du socle.
- **Ancres** : P2 (chaque anomalie du rapport porte sa preuve) ; E4 de l'évaluation
  (« l'anomalie qu'il ne fallait pas corriger »).

### C05 — Relations et hypothèses : corrélation, segments, comparaison de groupes, pièges d'inférence (5 h)

- **Étapes du protocole : 7—8** (relations, hypothèses).
- **Contenu** : la corrélation de Pearson en une ligne (`corr()`) **et ses limites**
  (linéarité, valeur extrême qui tire le coefficient) ; la corrélation **n'est pas** la
  causalité — les 3 fausses causes du module (troisièmes variables, régression vers la
  moyenne, sens inversé) ; les tableaux croisés (`crosstab`) ; les segments (trancher les
  clients par CA — le rappel `np.where` de M08) ; la comparaison de groupes (médiane par
  groupe + taille des groupes — le petit groupe qui ment) ; **formuler l'hypothèse**
  falsifiable et la tester sur les données (l'étape 8 est une discipline d'écriture, pas
  de calcul).
- **Jeu 3 intro** : l'**établissement scolaire** arrive ici — absentéisme × résultats :
  la corrélation (négative, forte) **et** le piège (l'absentéisme et la difficulté
  co-vus, mais le fichier ne dit pas lequel cause l'autre — la limite est **dans** la
  conclusion) ; segments d'élèves par niveau d'absentéisme.
- **Fil rouge** : la quincaillerie — CA × remises (corrélation faible, et ce que ça
  suggère), panier moyen par mode de paiement (comparaison de groupes à taille inégale).
- **Figures** : les 3 fausses causes, chacune avec son contre-exemple chiffré du socle.
- **Ancres** : P2/P4 (l'hypothèse du rapport + sa formulation provisoire) ; l'étude de cas
  de l'évaluation (poser les questions **avant** de répondre).

### C06 — Visualisations d'exploration et conclusions provisoires, note d'EDA (5 h)

- **Étapes du protocole : 9—10** (visualisations, premières conclusions).
- **Contenu** : choisir le graphique **par question** (courbe = évolution, barres =
  comparaison, boxplot = dispersion par groupe, histogramme = forme, nuage = association —
  le préambule de M10, en version exploration) ; les 5 erreurs d'exploration (l'axe qui
  ne part pas à zéro **sans le dire**, le graphique sans question, la couleur qui porte
  une info non mentionnée, l'échelle logarithmique surprise, le nuage sans taille
  d'échantillon) ; `matplotlib` (4 graphiques du projet) + `seaborn` (`boxplot`,
  `heatmap` des tableaux croisés) ; la **note d'EDA** : 1 page par jeu, chaque affirmation
  porte sa source (sortie) et sa **limite** ; lire une note d'EDA écrite par quelqu'un
  d'autre (l'exercice de rétro-lecture).
- **Fil rouge** : la note d'EDA de la quincaillerie **complète** (les 3 jeux y reviennent
  chacun en un paragraphe) — le livrable de fin de module.
- **Figures** : la table question → graphique (les 5 questions du module → les 5
  graphiques qui y répondent, chacun exécuté sur le socle).
- **Ancres** : P3 + P4 (les 4 graphiques + la note) ; la transition vers M10
  (« vos résultats sont justes ; s'ils sont illisibles, ils ne serviront à rien »).

## 4. Budget pages

| Chapitre | Pages (calibre 12,5) | Estimé |
|---|---|---|
| C01 Le protocole en 10 étapes, fiche d'entrée | 13 | 12-14 |
| C02 Audit et premières statistiques | 14 | 13-15 |
| C03 Tendances | 14 | 13-15 |
| C04 Anomalies et raretés | 14 | 13-15 |
| C05 Relations et hypothèses | 14 | 13-15 |
| C06 Visualisations et note d'EDA | 14 | 13-15 |
| Appareil (couverture, TOC, projet, évaluation) | 17 | 15-20 |
| **Total** | **92,5** | budget module ≈ **93 p.** |

Budget §F.4 = **6 × 12,5 + 17 = 92,5 p.**, tolérance ±15 % = **[79, 106] p.**
(`tools/budget_pages.py`). Si dérive : coupes naturelles en C02 (la démo SQL de
dédoublonnage ramenée à 1 requête), C03 (les moyennes glissantes réduites au principe),
C05 (un des 3 pièges d'inférence raboté à 2 lignes — les 3 restent nommés).

## 5. Chiffres cibles (à mesurer dans `chiffres_manuel.py M09`)

- **Jeu 1 (quincaillerie)** : redonne les totaux M07/M08 — 50 008 ventes, 8 doublons,
  208/200 retours, 21 406 dates sous la condition naïve, 15 deadlines au 20, 0 manquant,
  1 table vide ; CA propre 7 876 320 164 FCFA, plus gros mois 78 965 529 FCFA,
  dimanches 7 136, vue mensuelle 120 lignes.
- **Jeu 2 (centre de santé)** : formes (consultations, médicaments, seuils), les 4 défauts
  plantés chiffrés, fréquentation (médiane vs moyenne consultations/jour, pic de saison
  identifié, creux de midi), ruptures (nb de jours de rupture par médicament essentiel,
  la plus longue), stock négatif (nb d'occurrences, la date).
- **Jeu 3 (scolaire)** : formes (élèves, notes, absences), les défauts plantés chiffrés,
  corrélation absentéisme × moyenne générale (valeur mesurée + sa lecture « corrélation
  ≠ causalité »), segments d'élèves par niveau d'absentéisme (tailles des 3-4 segments),
  la matière la plus absente.
- **Fichier projet** : forme brute (lignes, colonnes), les défauts plantés chiffrés, les
  3 questions « autorisées » de la fiche d'entrée modèle et les 2 « interdites ».
- **Empreintes** : sha256 des 3 jeux + du fichier projet (fixées à l'étape 2).
- **Reproductibilité** : 2 exécutions successives → diff = 0.

## 6. Risques et parades

| Risque | Parade |
|---|---|
| L'apprenant explore « pour voir » et n'a plus de structure à 2 h 30/3 | Le chronomètre du projet + la fiche d'entrée (30 min) + le protocole comme contrat : une étape sautée = défaut de rapport (C01 §8, P2). |
| Confondre corrélation et causalité (le piège n° 1 du module) | C05 §5 : les 3 fausses causes avec contre-exemple **chiffré** du socle ; la note d'EDA (C06) interdit l'affirmation causale sans l'encadré « corrélation, pas causalité » ; l'évaluation le note. |
| Supprimer les anomalies à l'aveugle | C04 : la règle « prouver avant de traiter » ; les 3 décisions (corriger / exclure en documentant / garder en signalant) ; le jeu 2 porte une anomalie **qui compte** (rupture) — la corriger serait une erreur métier, notée comme telle. |
| Les 3 jeux noient le fil rouge | La quincaillerie est présente dans **les 6 chapitres** ; les jeux 2 et 3 arrivent chacun en un chapitre (C02, C05) et reviennent en C06 (note d'EDA) ; le chapitre type annonce son jeu en page 1. |
| `seaborn` inconnu, `matplotlib` minimal (M08 n'a fait que 4 graphiques de base) | C06 §5 : les 2 APIs sur **les mêmes données** (le même boxplot en `matplotlib` pur puis en `seaborn`), avec les sorties réelles ; les graphiques du projet utilisent `matplotlib` (dépendance minimale) — `seaborn` est l'option confort, documentée. |
| La comparaison de périodes ment (période partielle) | C03 §5 : le 2026 incomplet du socle (la base s'arrête à 2026-12-28) est le contre-exemple **chiffré** : comparer 2025 et 2026 « en tout » est une erreur, à mois égal c'est une mesure — le parallèle M07 (24 mois). |

## 7. Étapes de production (calque M05—M08)

1. **Étape 1 — Plan** (ce document).
2. **Étape 2 — Socle** : `tools/dossier_M09.py` (graine 45, déterministe) : réexport
   quincaillerie (empreinte M07/M08) + génération centre de santé (4 défauts plantés) +
   établissement scolaire (4 défauts plantés) + fichier projet « inconnu » ; `ATTENDU.json`
   (~ 30 clés `m09p_*` par jeu) + `chiffres_manuel.py M09()` (~ 90 clés, mesurées en pandas,
   2 runs diff = 0).
3. **Étape 3 — Rédaction** : 6 chapitres, cadence **1 push par chapitre validé `--strict`**
   (8 chapitres M08 → 6 ici : 6 pushes).
4. **Étape 4 — Figures** : `tools/figures_M09.py` (6 planches SVG, extension ≤ 776 px,
   jeu latin-1 étendu, embarquées).
5. **Étape 5 — PDF** : `tools/render.py --join "02_modules/M09_*.md"` → `M09.pdf`
   (budget 92,5 p. ±15 % = [79, 106]) + `tools/controle_pdf.py M09`.
6. **Étape 6 — Fiche de contrôle** : `05_livrables/fiche_controle_M09.md` Q1-Q10.
7. **Étape 7 — Projet + évaluation** : `03_exercices/M09_projet.md` (4 livrables /20 seuil
   13) + `04_evaluations/M09_evaluation.md` (quiz 15 Q + étude de cas « qualité des
   questions » + corrigés) + `tools/controle_exos_M09.py` (auto-validation) +
   `README.md` (mise à jour) + push final.
