# Plan M08 — Python pour l'analyse de données

**Module M08 · 8 chapitres · 30 h · niveau N2 → N3 (N3 en devenir) · prérequis M04, M05.C04 (ou grande
aisance Excel), M07 (le parallèle SQL/pandas est utilisé volontairement comme accélérateur d'apprentissage).**

> **L'idée du module.** Le SGBD a montré en M07 qu'une même question se pose en une ligne — mais chaque
> question exige une requête, et l'analyseur qui n'a pas de Python reste prisonnier de ce que le SGBD sait
> faire. M08 fait passer l'apprenant de *« je sais poser une question au SGBD »* à *« je sais écrire un
> script qui importe, audite, nettoie, calcule et exporte — et que je relancerai sans douleur le mois
> prochain »*. Les **8 chapitres** couvrent l'environnement (C01), les fondations sans données (C02), le
> contrôle du flux (C03), les structures de données (C04), l'organisation en fonctions et la lecture des
> erreurs (C05), NumPy utile et suffisant (C06), pandas I (C07) et pandas II (C08). Le **projet M08.P**
> ferme le module : « le script qui fait le travail de trois matinées » — analyse complète d'un jeu inconnu
> en une seule exécution, 2ᵉ pièce du portfolio. La **transition** finale annonce M09 (EDA) : *« Vous savez
> produire des chiffres par trois chemins. Rien ne garantit encore qu'ils racontent une histoire vraie. »*

## 1. Cadrage

### 1.1 Position dans l'architecture

- **Phase** 2 — Maîtrise opérationnelle (palier P2), dernier module du palier avant l'épreuve de validation P2.
- **Après** M07 (SQL), **avant** M09 (EDA), M14 (Power BI), M17 (automatisation), M21 (fil rouge en Python).
- **Prérequis** :
  - **M04** — qualité et conventions (nommage des variables, fichiers, documentation) ; **indispensable**.
  - **M05.C04** — l'apprenant a déjà *vu* du pandas en M05 (comparatif trois moteurs) ; ou grande aisance Excel.
  - **M07** — le parallèle SQL/pandas est l'accélérateur du module : chaque notion pandas est montrée **côte
    à côte** avec son équivalent SQL que l'apprenant maîtrise déjà.
- **Verrouillé** par M09 (EDA en pandas), M14 (Power Query/DAX se comprennent mieux avec Python),
  M17 (automatisation), M21 (fil rouge).

### 1.2 Huit compétences de sortie (la matrice de couverture)

1. **Installer sans stress** Python, `pip`, un environnement virtuel, VS Code et Jupyter — et exécuter son
   premier script, en expliquant chaque couche (interpréteur, paquet, environnement, noyau).
2. **Manipuler les fondations** : variables, les 5 types de base (`int`, `float`, `str`, `bool`, et la
   liste de C04), opérateurs, `input`/`print`, commentaires — et **lire une erreur** (nom, ligne, cause).
3. **Décider et répéter** : `if/elif/else`, boucles `for`/`while`, `break`/`continue`, et écrire une
   compréhension de liste quand elle reste lisible.
4. **Ranger les données** : listes, tuples, chaînes, **dictionnaires**, ensembles — et choisir le bon
   contenant pour la bonne question métier.
5. **Organiser le code** : fonctions (arguments positionnels/nommés/par défaut), portée, docstring,
   modules et paquets, `try/except` — et **lire une traceback** de haut en bas.
6. **Vectoriser** avec NumPy : tableaux, opérations élément par élément, statistiques, `np.nan`,
   `np.where`, broadcasting — et comprendre pourquoi une boucle lente devient une ligne.
7. **Pandas I** : `Series`/`DataFrame`, `read_csv`/`read_excel`, `loc`/`iloc`, filtres, nouvelles
   colonnes, `describe`, valeurs manquantes — avec l'équivalent SQL à chaque bloc.
8. **Pandas II** : `groupby`/`agg`/`transform`, `merge`, `pivot_table`, dates et périodes, `apply`,
   export Excel avec mise en forme — et assembler le script de bout en bout.

### 1.3 Fait du socle (mesurés le 19/09/2026)

- **Environnement d'écriture** (règle du dépôt, inchangée) : **Python 3.13.14, pandas 2.2.3, numpy
  2.3.5**. Les sorties publiées dans les chapitres sont produites sous cet environnement.
- **Version de référence ciblée par l'apprenant** : **pandas 3.x** (sorti en janvier 2026 : type texte
  dédié `str`, *copy-on-write* par défaut, alias de périodes supprimés). **Décision de conception
  importante (architecture §M08)** : le manuel enseigne les patterns **valides en pandas 2.3 et 3.x**,
  signale explicitement les **12 écritures obsolètes** à ne plus reproduire (liste en §1.7) et fournit
  une annexe « migration » en C08. Un manuel qui ignorerait pandas 3 serait faux dès sa parution.
- **Fait mesuré le 19/09/2026** (preuve que la distinction n'est pas cosmétique) : sur le socle M01/M03,
  `pandas 3.0.6` change 4 valeurs de vérité terrain par rapport à `pandas 2.2.3` — cellules vides du
  fichier clients `103 → 85`, modalités brutes `373 → 372`, cellules texte du fichier attendu `7 → 0`,
  lignes client champ vide `18 → 0` — et le dtype texte passe de `object` à `str`. Ces 4 écarts,
  sourcés (`m08p_pd3_*`), sont l'exemple fil rouge de l'annexe migration et du sujet E4 (« ce script
  tourne mais ses chiffres sont faux »).
- **Deuxième fait mesuré le 19/09/2026** (la leçon des centimes) : `montant_ttc` est un **DOUBLE** dans
  la base M07. La somme float dérive selon le moteur : la somme **Decimal exacte** des 50 008 montants
  vaut 7 908 259 732,20 FCFA, DuckDB renvoie 7 908 259 730,56… (ROUND = 7 908 259 731, la valeur
  publiée M07), l'addition en **centimes entiers** (int64) renvoie 7 908 259 732. Écart mesuré :
  1 à 2 FCFA sur 7,9 milliards — négligeable en métier, visible en audit. La vérification croisée
  SQL/pandas est donc **exacte pour les comptages** et à **± 2 FCFA pour les totaux monétaires**
  (écarts mesurés sourcés `m08p_ecart_somme_float_*`) ; le chapitre C08 enseigne l'addition en
  centimes et le projet M08.P accepte ± 2 FCFA sur les totaux (exact sur les comptages).
- **Socle M08** (à ouvrir en étape 2) : la base commerciale M07, **re-exportée en 8 CSV** par
  `tools/dossier_M08.py` (déterministe : il ne génère rien, il **exporte** la base figée, empreinte
  `df9333ff…a1dde`) dans `03_exercices/dossier_M08/` :
  1. `ventes.csv` — 50 008 lignes × 13 col (le jeu principal, avec ses 8 doublons, 208 lignes
     `est_retour` dont 200 retours uniques après dédoublonnage, le vice des 21 406 dates
     `date_vente > date_limite_remise` et les 15 deadlines aberrantes : l'audit du projet a de
     vrais défauts à trouver).
  2. `clients.csv` (1 200 l.), `produits.csv` (380 l.), `categories.csv` (8 l.), `magasins.csv` (5 l.),
     `modes_paiement.csv` (5 l.), `regles_tva.csv` (2 l.).
  3. `objectif_magasin.csv` — **0 ligne, en-tête seul** : table vide (une table peut n'avoir aucune
     ligne ; impossible à montrer dans Excel, trivial en CSV).
  4. `00_brief.md` — le brief : « vous avez reçu l'export de la chaîne, voici les 8 fichiers ; la vue
     mensuelle n'est pas exportée, elle se reconstruit (C08) ».
  5. `ATTENDU.json` — ~ 35 clés `m08p_*` (formes, audit, indicateurs ; les réponses pandas du projet).
- **Le fil rouge du module** : **les mêmes chiffres, trois chemins** — Excel (M05), SQL (M07), pandas
  (M08). Chaque bloc de code pandas est suivi de son **équivalent SQL M07** côte à côte ; chaque
  indicateur du projet est déjà connu de l'apprenant (Q01-Q30 de M07.P), ce qui transforme le projet en
  **vérification croisée** plutôt qu'en devinette.
- **Règle d'exécution** : tout Python est **exécuté** (règle 2 du README) — chaque bloc de code a sa
  **sortie réelle imprimée** (jamais « le résultat est… » sans le texte de sortie), avec une
  interprétation en une phrase et l'équivalent SQL. Les 4 écarts pandas 2.2/3.0 cités plus haut sont
  mesurés, pas illustrés.

### 1.4 Le projet M08.P — « Le script qui fait le travail de trois matinées »

- **Énoncé.** L'apprenant reçoit le dossier M08 (8 CSV, dont un vide) et doit écrire **un seul script
  commenté** (`analyse_commerciale.py`) qui, exécuté d'une traite, produit : (1) l'**import** des 8 CSV
  avec contrôle des formes ; (2) l'**audit** (doublons, retours, dates inversées, valeurs manquantes,
  table vide) avec un rapport imprimé ; (3) le **nettoyage** (dédoublonnage, exclusion des retours des
  indicateurs) ; (4) les **indicateurs** (CA brut / CA propre / panier moyen / CA par magasin / par
  catégorie / par mois — les 30 questions M07 reformulées en pandas) ; (5) **4 graphiques** (CA mensuel,
  CA par magasin, répartition par catégorie, histogramme des montants) ; (6) l'**export** d'un classeur
  de synthèse `synthese_commerciale.xlsx` (4 feuilles : audit, indicateurs, par magasin, par mois).
- **Livrables** (grille /20, seuil 13) :
  - **E1 — Le script commenté** (8 points) — 6 sections numérotées, chaque section avec un en-tête de
    2 lignes, aucune valeur en dur (tout est calculé), `if __name__ == "__main__":`.
  - **E2 — Le rapport d'audit imprimé** (4 points) — les 4 défauts du socle chiffrés avec leur
    définition exacte (8 doublons → 50 000 uniques ; 208 retours en brut / 200 après dédoublonnage ;
    21 406 dates sous la condition naïve + 15 deadlines aberrantes ; 0 valeur manquante, 1 table
    vide), avec la **méthode** qui les a trouvés.
  - **E3 — Le classeur de synthèse** (4 points) — 4 feuilles, **comptages identiques** au corrigé
    M07.P et **totaux monétaires à ± 2 FCFA** (la dérive float, mesurée et documentée dans le
    rapport d'audit), feuilles nommées, pas de cellule en dur.
  - **E4 — La note « ce qui a failli tourner en boucle »** (4 points) — 1 page : les 2-3 blocs où
    l'apprenant a hésité entre une boucle et une vectorisation, et pourquoi la version vectorisée gagne
    (mesure de temps fournie).

### 1.5 Évaluation M08

- **Quiz** 15 Q (dont 5 « **lisez ce court programme et prédisez la sortie** » — objectif pédagogique :
  lire du code autant qu'en écrire).
- **5 exercices** (à rendre : un script court chacun) + **E4 « ce script tourne mais ses chiffres sont
  faux »** : l'apprenant reçoit un script correct en syntaxe qui produit 3 chiffres faux (doublons
  comptés, retours inclus, division par zéro masquée) et doit les localiser et corriger.
- **~ 15 exercices « prédisez la sortie »** auto-validés par `tools/controle_exos_M08.py` — chaque
  exercice a une sortie attendue mesurée (`m08p_*` / sorties littérales), le script compare la sortie
  réelle à la sortie attendue.
- **Étude de cas** — « le script du stagiaire » : un notebook livré avec 3 erreurs typées
  (`NameError`, `KeyError`, `SettingWithCopyWarning` muet sous copy-on-write) et un chiffre qui ne
  correspond pas au total M07 ; l'apprenant diagnostique et corrige, en commentant chaque traceback.
- **Corrigés** avec les **messages d'erreur commentés** : apprendre à lire une traceback est un objectif
  à part entière (traité en C05 §12-13, réutilisé dans tous les corrigés).

### 1.6 Règles d'exécution (cadence héritée de M06/M07)

- **Tout Python est exécuté** avant publication (règle 2 du dépôt) ; les **4 écarts pandas 2.2/3.0** du
  §1.3 sont mesurés sous les deux versions le 19/09/2026 et sourcés.
- **DuckDB** (exécuté) et **SQLite** (exécuté) restent disponibles pour les équivalents SQL ; **PostgreSQL
  cité sans exécuté** (règle §1.5 héritée de M06 — l'exécution PostgreSQL revient en M11).
- Chaque chiffre ≥ 4 chiffres cité dans un .md est **sourcé dans `chiffres_cites.json`** (les `m08_*` /
  `m08p_*`, ou les clés des modules précédents — le contrôle R2 lit **toutes** les sections du JSON) ou
  reformulé.
- **Patterns 2.3/3.x** : tout code publié est **exécuté sous pandas 2.2.3** (environnement d'écriture)
  et **testé sous pandas 3.0.6** (version de référence) — les deux sorties sont identiques, sinon un
  encadré « Dans les faits » le signale.

### 1.7 Les 12 écritures obsolètes (liste de référence — détaillée en C08 §13 + annexe migration)

| # | Écriture (2.x) | Pourquoi c'est fini | Écriture enseignée |
|---|---|---|---|
| 1 | `df.append(ligne)` | supprimée en 2.0 | `pd.concat([df, nouvelle_ligne])` |
| 2 | `inplace=True` | sans effet utile sous copy-on-write (3.x) | réassigner : `df = df.drop(…)` |
| 3 | `df[masque]["col"] = valeur` (affectation chaînée) | silencieux ou muet sous CoW | `df.loc[masque, "col"] = valeur` |
| 4 | Alias de périodes `'M'`, `'H'`, `'S'` | supprimés en 3.0 (ambigus : fin de mois vs millier) | `'ME'`, `'h'`, `'s'` |
| 5 | `Series.iteritems()` | supprimée en 2.0 | `Series.items()` |
| 6 | `DataFrame.applymap(f)` | dépréciée en 2.1 | `DataFrame.map(f)` |
| 7 | `fillna(method="ffill")` | dépréciée en 2.1 | `ffill()` / `bfill()` directs |
| 8 | `reindex_axis` / `swapaxes` | supprimées en 2.0 | `reindex` / `transpose` |
| 9 | `mad()` (écart moyen absolu) | supprimée en 2.0 | `numpy` : `(x - x.mean()).abs().mean()` |
| 10 | Compter une cellule texte vide comme non-vide | changement de sémantique NaN/chaîne en 3.0 (écarts §1.3) | normaliser **avant** de compter |
| 11 | `dtype object` pour le texte | remplacé par le type dédié `str` en 3.0 | ne pas brancher sur le dtype : brancher sur la valeur |
| 12 | Modifier une vue/une tranche en croyant modifier la mère | copy-on-write par défaut en 3.0 (plus de `SettingWithCopyWarning` : le changement est **silencieusement perdu** dans certains cas) | copier explicitement : `tranche = df[masque].copy()` |

## 2. Vocabulaire du module (à définir au premier emploi)

| Français — English | Première définition | Piège à éviter |
|---|---|---|
| **interpréteur** | le programme qui **lit et exécute** le Python ligne à ligne (ce qu'Excel fait pour les formules, ce que le SGBD fait pour le SQL). | croire que Python « compile » en local : le `.pyc` est un cache, pas une traduction. |
| **paquet** — *package* | un **bloc de code réutilisable** installé séparément (`pandas`, `numpy`), via `pip`. | confondre paquet et module : un paquet contient des modules. |
| **environnement virtuel** — *virtualenv* | une **copie isolée** de Python + ses paquets pour un projet, qui ne touche pas le reste du système. | installer `pip install` dans le Python système : le projet de demain casse celui d'aujourd'hui. |
| **noyau** — *kernel* | le **moteur d'exécution** derrière un notebook Jupyter, qui exécute les cellules dans un état mémorisé. | croire qu'une cellule « voit » ce que la cellule suivante a fait : seul l'ordre d'**exécution** compte, pas l'ordre d'écriture. |
| **variable** | un **nom pointant vers une valeur** (pas une boîte contenant la valeur). | dire « la variable contient le nombre » : elle pointe vers l'objet ; rebaptiser ne duplique pas. |
| **type** — *type* | la **famille de valeurs** qui autorise des opérations (`int`, `float`, `str`, `bool`, `list`…). | croire que `1` et `1.0` et `"1"` sont la même valeur : trois objets, trois types, trois comportements. |
| **boucle** — *loop* | un bloc **répété** tant qu'une condition le permet (`for`, `while`). | la boucle `while` sans condition d'arrêt : la boucle infinie. |
| **dictionnaire** — *dict* | une collection **clé → valeur** (un index par clé, pas par position). | chercher une clé absente sans `get` : `KeyError` — ou pire, la créer vide par accident. |
| **fonction** — *function* | un **bloc nommé** qui reçoit des entrées, calcule, et renvoie une sortie. | une fonction qui `print` au lieu de `return` : impossible à réutiliser. |
| **exception** — *exception* | une **erreur signalée** à l'exécution (`ValueError`, `KeyError`…), interceptable avec `try/except`. | `except:` tout nu : il avale toutes les erreurs, y compris celles qu'il faut voir. |
| **tableau** (NumPy) — *array* | une collection **contiguë et homogène** de nombres, calculée en bloc (pas un par un). | utiliser une liste Python pour un calcul massif : 10 à 100 × plus lent. |
| **vectorisation** | calculer **sur tout le tableau d'un coup**, au lieu d'une boucle par élément. | « vectoriser » un truc qui a de la mémoire d'étape : certains calculs restent des boucles (et c'est normal). |
| **DataFrame** | un **tableau à deux dimensions** avec colonnes nommées (une table SQL en Python), le cœur de pandas. | le manipuler ligne par ligne avec une boucle : c'est exactement ce qu'il faut éviter. |
| **Série** — *Series* | une **colonne** de DataFrame (un index + des valeurs), le cousin 1-D du DataFrame. | confondre l'**index** (l'étiquette des lignes) et la **première colonne** : ce n'est pas la même chose. |
| **traceback** — *traceback* | le **rapport d'erreur** Python : la pile d'appels du haut (cause) vers le bas (où ça a explosé). | lire la traceback de bas en haut : la **dernière ligne** dit l'erreur, la **première** dit pourquoi. |
| **groupby** | la méthode pandas qui **regroupe les lignes** partageant une clé — l'équivalent de `GROUP BY` SQL. | croire qu'on peut agréger « tout » d'un coup : `groupby` renvoie un objet qu'il faut ensuite agréger. |
| **merge** | la méthode pandas qui **joint deux DataFrames** sur des colonnes — l'équivalent de `JOIN` SQL. | un `merge` sans clé commune explicite : il joint sur l'intersection des noms, souvent au pire endroit. |

## 3. Découpage en 8 chapitres

### C01 — Installer sans stress : Python, `pip`, environnements virtuels, VS Code et Jupyter, exécuter son premier script

- **Objectif.** L'apprenant installe la chaîne complète **sans casser son système**, et exécute son
  premier script en comprenant les 4 couches (système → Python → paquet → projet).
- **Plan sommaire** :
  1. Ce qu'on installe et pourquoi : le **runtime** (Python 3.13), le **gestionnaire de paquets**
     (`pip`), l'**outil de projet** (VS Code), le **carnet** (Jupyter) — les 4 couches, 4 rôles.
  2. L'installation Windows-first (le profil du lecteur) : l'installeur officiel, la case
     **« Add to PATH »** (le piège n° 1), la vérification `python --version` / `pip --version`.
  3. `pip install pandas numpy` — lire la sortie d'installation (« Successfully installed … »).
  4. L'**environnement virtuel** : `python -m venv .venv`, l'activer (Windows : `.venv\Scripts\activate`),
     pourquoi (le projet de demain ne casse pas celui d'aujourd'hui), `requirements.txt` pour figer.
  5. VS Code : ouvrir un dossier, le terminal intégré, exécuter `python premier.py`.
  6. **Jupyter** : `jupyter lab`, une cellule, l'exécution par cellule, le **noyau** et son état
     mémorisé (réinitialiser le noyau, l'ordre d'exécution ≠ ordre d'écriture).
  7. **Son premier script** : `premier.py` — 3 lignes (`print`, `input`, une variable), exécuté dans
     VS Code **et** dans une cellule Jupyter ; les deux sorties sont publiées.
  8. Les 5 erreurs d'installation les plus courantes (`python n'est pas reconnu`, `pip` installe
     dans le mauvais Python, le venv n'est pas activé, le portier antivirus, le notebook qui ne voit
     pas les paquets du terminal).
- **Livrables spécifiques** : 1 figure SVG « les 4 couches de l'environnement Python » (système →
  runtime → paquet → projet, avec `pip` et le venv comme parois).

### C02 — Les fondations sans données : variables, types, opérateurs, entrées/sorties, commentaires, erreurs

- **Objectif.** L'apprenant écrit et **lit** des programmes simples, et lit une erreur sans paniquer.
- **Plan sommaire** :
  1. La variable : un nom pointant vers une valeur (`prix = 1500`), le rebaptisage, le `TypeError`
     quand on mélange des types.
  2. Les 5 types de base : `int`, `float`, `str`, `bool` + l'aperçu des conteneurs (C04) ; `type(x)`
     et les conversions (`int("1500")`, `float("1500,50")` → `ValueError` : la virgule).
  3. Les opérateurs : arithmétiques (`+ - * / // % **`), de comparaison (`==`, `!=`, `<`, `<=`, …),
     les 3 opérateurs booléens (`and`, `or`, `not`) — **et le parallèle `AND`/`OR` de M07**.
  4. `input()` (toujours un `str` !) et `print()` (séparateur, `end`) ; l'exemple métier : lire un
     montant et le convertir.
  5. Les commentaires : `#` en ligne, docstring (aperçu, développée en C05) — commenter **pourquoi**,
     pas **quoi** (règle M04).
  6. **Lire une erreur** : l'anatomie d'une `SyntaxError` / `NameError` / `ValueError` (le message,
     la ligne, la fleche) — 3 erreurs réelles exécutées, sorties publiées.
  7. Le `None` et les `bool` qui surprennent (`0`, `""`, `[]` sont « faux » en condition).
  8. **Exercice fil rouge** : un mini « calculateur de remise » — lire 2 entrées, calculer, afficher
     ; 3 variantes (le montant en lettres avec une virgule, le client absent, la remise > 100 %).
- **Livrables spécifiques** : 1 figure SVG « les 5 types × 4 opérations » (tableau-matrice).

### C03 — Décider et répéter : `if/elif/else`, boucles `for`/`while`, `break`/`continue`, compréhensions

- **Objectif.** L'apprenant fait le flux : décider, répéter, s'arrêter — et sait quand une
  compréhension vaut mieux qu'une boucle.
- **Plan sommaire** :
  1. `if/elif/else` : l'échelle de décision (le `CASE WHEN` de M06 en Python), l'indentation **est**
     la syntaxe.
  2. La boucle `for` : parcourir une liste (les 5 magasins), `range(10)`, `enumerate` (l'index **et**
     la valeur).
  3. La boucle `while` : « tant que » (le solde d'un crédit) — et la boucle infinie (l'exemple exécuté
     qui bloque, et le `break` qui sauve).
  4. `break` / `continue` : sortir, passer à la suite — les 2 usages métiers (arrêter au premier
     dépassement ; ignorer les lignes pourries).
  5. **Les compréhensions** : `[expr for x in it if cond]` — la liste en une ligne, lisible ;
     **la règle des 2 niveaux** : au-delà, c'est une boucle.
  6. Le `zip` : parcourir 2 listes en parallèle (magasins + objectifs) — l'équivalent d'un `CROSS JOIN`
     propre.
  7. **Le parallèle SQL** : `for`/`while` = ce que le SGBD fait pour vous (pas de boucle dans une
     requête) ; quand Python gagne (le traitement hors table).
  8. **Exercice fil rouge** : le « contrôle qualité express » — parcourir 10 montants, compter les
     anomalies, arrêter au 3ᵉ dépassement, imprimer le rapport.
- **Livrables spécifiques** : 1 figure SVG « décider et répéter » (l'échelle `if` + la boucle, avec
  les issues `break`/`continue`).

### C04 — Ranger : listes, tuples, chaînes, **dictionnaires**, ensembles, index, tris

- **Objectif.** L'apprenant choisit le bon contenant pour la bonne question, et indexe sans erreur.
- **Plan sommaire** :
  1. La **liste** : ordonnée, mutable, dupliquable ; `append`, `extend`, l'index négatif (`-1`), la
     tranche `[2:5]`.
  2. Le **tuple** : immuable (une clé de dictionnaire, un résultat multi-valeurs) ; quand choisir
     tuple plutôt que liste.
  3. La **chaîne** : immuable ; les tranches, les méthodes (`split`, `strip`, `replace`, `startswith`),
     les f-strings (`f"CA {ca:,.0f} FCFA"` — le formatage des montants, règle M01).
  4. **Le dictionnaire** : clé → valeur ; `d["ville"]`, `d.get("ville", "inconnu")`, `in d` teste les
     **clés** ; le dictionnaire de compteurs (le `GROUP BY` avant pandas).
  5. L'**ensemble** (`set`) : les valeurs uniques ; `len(set(villes))` = `COUNT(DISTINCT ville)` ;
     l'intersection (les clients des 2 magasins).
  6. Les index et les tranches : `l[0]`, `l[-1]`, `l[::2]` — l'index hors plage (`IndexError`, la
     ligne `n` a l'index `n-1`).
  7. Les tris : `sorted(l)` (ne modifie pas), `l.sort(reverse=True)`, trier des dictionnaires par
     valeur (`sorted(d.items(), key=…)` — le **top N** en une ligne).
  8. **Exercice fil rouge** : les 5 magasins en 4 contenants (liste de noms, tuple de coordonnées,
     dictionnaire ville→magasin, ensemble de villes) — et répondre à 5 questions métier avec le bon
     contenant pour chacune.
- **Livrables spécifiques** : 1 figure SVG « les 5 conteneurs » (5 cases, chacune avec sa question
  métier et son opérateur signature).

### C05 — Organiser : fonctions, arguments, portée, docstring, modules et paquets, `try/except`, fichiers CSV/Excel/JSON

- **Objectif.** L'apprenant découpe son script en fonctions testables, lit une traceback de haut en
  bas, et écrit/lit des fichiers.
- **Plan sommaire** :
  1. La fonction : `def`, `return` (pas `print` !) ; la fonction sans `return` renvoie `None` (le
     piège exécuté).
  2. Les arguments : positionnels, nommés (`calculer_remise(montant, taux=0.10)`), par défaut — et
     **l'argument par défaut mutable** (le piège `def f(x, acc=[])`).
  3. La **portée** : locale / globale ; `global` (à éviter) ; la variable de boucle qui « fuite »
     (elle existe après la boucle).
  4. La **docstring** : la convention (`"""Quoi, entrées, sorties, exemple"""`), le contrôle
     `help(f)` — la règle M04 reprise en Python.
  5. **Modules et paquets** : `import pandas as pd`, `from numpy import where`, le `import` en tête
     de fichier (règle), ce qu'on met dans son propre module.
  6. **`try/except`** : intercepter l'attendu (`ValueError` sur un montant en lettres), **spécifier**
     l'exception (jamais `except:` tout nu), le `else` et le `finally` (en 1 paragraphe, pour la suite).
  7. **Lire une traceback** : les 3 couches (la pile d'appels, la ligne fautive, le type d'erreur) —
     3 tracebacks réelles exécutées et annotées ligne à ligne (`NameError`, `KeyError`,
     `FileNotFoundError`).
  8. **Les fichiers** : ouvrir un CSV avec `open` (encodage `utf-8-sig`, le BOM — rappel M01), le
     `csv` standard, `json.load`/`json.dump`, et l'aperçu `pandas.read_csv` (C07).
  9. **Exercice fil rouge** : le « nettoyeur de montants » — une fonction qui reçoit une chaîne de
     montant (`"15 000,50"`, `"15000.50"`, `"N/C"`) et renvoie un `float` ou `None`, avec `try/except`
     et docstring ; 6 cas de test exécutés.
- **Livrables spécifiques** : 1 figure SVG « lire une traceback » (la pile d'appels annotée, du haut
  vers le bas).

### C06 — NumPy utile et suffisant : tableaux, vecteurisation, statistiques, `nan`, `where`, broadcasting

- **Objectif.** L'apprenant calcule **en bloc** sur des tableaux de nombres, et comprend pourquoi la
  boucle de C03 devient une ligne.
- **Plan sommaire** :
  1. Le tableau NumPy : `np.array([...])`, homogène, contigu, `dtype` — la différence avec une liste
     (la taille en microsecondes, mesurée).
  2. **La vecteurisation** : `montants * 1.19` = tout le tableau multiplié ; `np.sum`, `np.mean`,
     `np.median`, `np.std` — et le **parallèle SQL** (`SUM`, `AVG` sur la colonne).
  3. Les statistiques : `np.min`/`np.max`/`np.percentile`, le quartile (le Q1 de M02 en NumPy).
  4. **`np.nan`** : le nombre qui « n'a pas de valeur » ; `np.isnan`, pourquoi `nan + 1 = nan`
     (l'absence se propage), `np.nansum`/`np.nanmean` — le pont vers les `NULL` de M06/M07.
  5. **`np.where`** : `np.where(montants > 100000, "gros", "normal")` — le `CASE WHEN` de M06 en
     tableau.
  6. **Broadcasting** : `montants - moyennes_par_magasin` (une ligne de 5 valeurs soustraite d'un
     tableau de 50 000) — la règle de forme en 1 figure.
  7. La mesure : la boucle `for` de C03 sur 50 000 montants vs la ligne vectorisée — le **temps mesuré**
     publié (les deux sorties, le rapport).
  8. **Exercice fil rouge** : les 50 000 montants du socle (importés d'un CSV avec `np.loadtxt` en
     1 ligne) — CA total, panier moyen, le 95ᵉ percentile, les montants « gros » : 4 calculs, 0 boucle.
- **Livrables spécifiques** : 1 figure SVG « boucle vs vecteur » (les deux chemins, avec le rapport de
  vitesse mesuré).

### C07 — pandas I : `Series`, `DataFrame`, `read_csv`/`read_excel`, sélection `loc`/`iloc`, filtres, nouvelles colonnes, `describe`, valeurs manquantes

- **Objectif.** L'apprenant importe le dossier M08, et sait sélectionner, filtrer, décrire, et compter
  les valeurs manquantes — chaque bloc avec son équivalent SQL.
- **Plan sommaire** :
  1. `import pandas as pd` : ce que c'est (une bibliothèque, pas un langage) ; la **Série** (une
     colonne : index + valeurs) et le **DataFrame** (un tableau de colonnes) — les 2 objets du module.
  2. **`read_csv`** : `pd.read_csv("ventes.csv")`, `head()`, `shape`, `dtypes`, `info()` — l'import
     des 8 CSV du dossier M08, **sorties réelles publiées** (50 008 × 13, 1 200 × 5, …).
  3. L'**index** : ce n'est pas une colonne ; `reset_index`, quand l'index porte un sens (les dates,
     C08).
  4. **`loc`** (par nom) vs **`iloc`** (par position) : `df.loc[masque, "col"]`, `df.iloc[0:5, 1:3]` —
     le tableau de 4 cas (ligne/colonne × nom/position).
  5. **Les filtres** : `df[df["est_retour"] == False]`, les opérateurs vectoriels (`&`/`|`/`~`,
     parenthèses obligatoires) — **le parallèle `WHERE`** en tableau côte à côte.
  6. **Les nouvelles colonnes** : `df["ca_ht"] = df["montant_ttc"] / (1 + df["taux_tva"])` — le
     `SELECT montant, montant / (1 + taux) AS ca_ht` ; `assign` pour la chaîne lisible.
  7. **`describe()`** : la carte d'identité statistique (les 8 statistiques de M02), `count()` par
     colonne.
  8. **Les valeurs manquantes** : `isna()`, `isna().sum()`, `dropna()` vs `fillna()` — **l'audit du
     dossier M08** : le socle n'en a pas (mesuré), mais `objectif_magasin` est vide (0 ligne) : ce que
     `read_csv` en fait, et le `KeyError` quand on l'indexe.
  9. Les **12 écritures obsolètes** (1ʳᵉ salve, 4 d'entre elles) : `inplace`, l'affectation chaînée,
     `fillna(method=…)`, `append` — avec l'encadré « Dans les faits » sur les 4 écarts 2.2/3.0 mesurés.
  10. **Exercice fil rouge** : l'audit complet du dossier M08 en 8 lignes — formes, doublons, retours,
      dates inversées, table vide — chaque résultat **identique** à son équivalent SQL M07 (côté à
      côte).
- **Livrables spécifiques** : 1 figure SVG « `loc` vs `iloc` : le tableau 4 cas » (grille 2×2 sur un
  DataFrame 5×4 annoté).

### C08 — pandas II : `groupby`/`agg`/`transform`, `merge`, `pivot_table`, dates, périodes, `apply`, export Excel avec mise en forme

- **Objectif.** L'apprenant agrège, joint, pivote, et assemble le script de bout en bout — en
  reconstruisant en pandas **tout ce que M07 faisait en SQL**.
- **Plan sommaire** :
  1. **`groupby`** : `g = df.groupby("id_magasin")`, `g["montant_ttc"].agg(["sum","count","mean"])` —
     **le `GROUP BY` de M07** en 1 ligne, sortie réelle (les 5 magasins, CA 1 564 937 883 à
     1 596 813 264, top magasin 4).
  2. **`transform`** : la moyenne **par groupe** remise sur chaque ligne (le « delta vs la moyenne de
     son magasin ») — ce que `GROUP BY` ne fait pas.
  3. **`merge`** : `ventes.merge(magasins, on="id_magasin")` — **le `JOIN` de M07** ; `how="left"`
     (le piège : 0 ligne perdue, et l'`objectif_magasin` vide → tout en `NaN`, **mesuré**).
  4. **`pivot_table`** : CA par magasin × mois (la vue `v_ca_mensuel_magasin` **reconstruite** —
     120 lignes, le plus gros mois 78 965 529) — la vue SQL que l'apprenant a apprise en C08 de M07,
     recréée ici sans SQL.
  5. **Les dates** : `pd.to_datetime`, `dt.year`/`dt.month`/`dt.day_name()`, le CA par mois — le
     `EXTRACT` de M07 ; les périodes (`resample("ME")` — l'**alias `'M'` est mort**, §1.7 n° 4).
  6. **`apply`** : la fonction de C05 sur une colonne (« netoyer de montant ») — et **quand ne pas
     l'utiliser** (la vectorisation d'abord).
  7. **L'export Excel** : `df.to_excel("synthese.xlsx", sheet_name="…")`, un classeur multi-feuilles
     (`ExcelWriter`), la mise en forme minimale (largeurs, nombres) — le livrable E3 du projet.
  8. **L'annexe migration pandas 2.3 → 3.x** : les 12 écritures obsolètes (§1.7) détaillées avec le
     code avant/après, et les 4 écarts mesurés (§1.3) commentés — « votre script de 2026 tournera en
     2028 » est l'objectif.
  9. **Le script de bout en bout** : les 6 sections du projet M08.P assemblées (import → audit →
     nettoyage → indicateurs → graphiques → export), exécuté d'une traite, sorties publiées.
  10. **Exercice fil rouge** : les 30 questions M07.P réécrites en pandas — 10 d'entre elles exécutées
      et comparées au corrigé SQL (0 écart), 9 affichées avec le parallèle côte à côte.
- **Livrables spécifiques** : 1 figure SVG « `GROUP BY` SQL ↔ `groupby` pandas » (le même pipeline,
  deux syntaxes, une même sortie).

## 4. Budget pages

| Chapitre | Pages (calibre 12,5) | Estimé |
|---|---|---|
| C01 Installer sans stress | 12 | 11-14 |
| C02 Les fondations sans données | 12 | 11-14 |
| C03 Décider et répéter | 12 | 11-14 |
| C04 Ranger | 12 | 11-14 |
| C05 Organiser (fonctions, erreurs, fichiers) | 13 | 11-14 |
| C06 NumPy utile et suffisant | 12 | 11-14 |
| C07 pandas I | 13 | 11-14 |
| C08 pandas II + annexe migration | 13 | 12-15 |
| Appareil (couverture, TOC, projet, évaluation) | 17 | 15-20 |
| **Total** | **116** | budget module ≈ 117 p. |

Budget §F.4 = 117 p., tolérance ±15 % = **[99, 135] p.** Si dérive : coupes naturelles en C02
(l'aperçu des conteneurs raccourci au profit de C04), C05 (`else`/`finally` réduit à 1 phrase),
C08 (les 9 exercices affichés ramenés à 6).

## 5. Chiffres cibles (à mesurer dans `chiffres_manuel.py M08`)

- **Formes des 8 CSV** : `ventes` 50 008 × 13, `client` 1 200 × 5, `produit` 380 × 6, `categorie`
  8 × 3, `magasin` 5 × 6, `mode_paiement` 5 × 4, `regle_tva` 2 × 2, `objectif_magasin` **0** × 4.
- **Audit pandas** (doit redonner les défauts M07, vérification croisée ; chaque définition est
  précise, c'est elle qui fait le chapitre) :
  - doublons exacts (12 colonnes métier — toutes sauf `id_vente`) : **8** → 50 000 ventes uniques ;
  - retours : **208** lignes `est_retour = True` en brut, **200** après dédoublonnage (les 8
    doublons sont des copies de lignes retours — la leçon M08 : **l'ordre des opérations** de
    l'audit, et l'objet de l'exercice E4 « les chiffres sont faux ») ;
  - dates : **21 406** lignes sous la condition naïve `date_vente > date_limite_remise` (le « vice
    caché » documenté en M07 C02 : deadline fixée au 15 du mois, ventes réparties sur le mois) +
    **15** deadlines aberrantes tombant au **20** du mois (18 en brut dont 3 doublons) ;
  - valeurs manquantes : **0** ; table vide : `objectif_magasin` (**0** ligne).
- **Indicateurs** (côté pandas, addition en centimes — doivent redonner M07.P à ± 2 FCFA près) :
  CA brut 7 908 259 732 (DuckDB : 7 908 259 731), CA propre 7 876 320 164 (DuckDB : 7 876 320 163),
  panier moyen 158 140 (158 159 sans retours), 2025 = 24 920 ventes / 3 925 215 672 FCFA
  (DuckDB : 3 925 215 671), 2026 = 25 088 / 3 983 044 059 (DuckDB : 3 983 044 060), plus gros mois
  78 965 529 (magasin 3, 2025-08, vue sans retours — identique des deux côtés), top magasin 4
  (1 596 813 264 — identique des deux côtés).
- **Empreinte** du dossier M08 : sha256 des 8 CSV concaténés (à fixer à l'étape 2 ; le dossier
  dérive de la base M07 figée, empreinte `df9333ff…a1dde` — il est stable par construction).
- **Écarts pandas 2.2.3 / 3.0.6** (mesurés le 19/09/2026, sourcés `m08p_pd3_*`) : cellules vides
  clients 103 → 85, modalités brutes 373 → 372, cellules texte attendu 7 → 0, lignes client champ
  vide 18 → 0, dtype texte `object` → `str`.
- **Reproductibilité** : 2 exécutions successives de `chiffres_manuel.py M08` → diff = 0.

## 6. Risques et parades

| Risque | Parade |
|---|---|
| L'apprenant installe mal et bloque avant la ligne 1 (PATH, venv, antivirus) | C01 §8 : les 5 erreurs d'installation avec la sortie exacte observée et le remède ; l'encadré « Dans les faits » signale ce que l'atelier ne peut pas exécuter (l'installeur Windows). |
| Confondre `loc`/`iloc`, ou l'affectation chaînée (le piège n° 1 de pandas) | Figure C07 (tableau 4 cas), l'encadré §1.7 n° 3 avec le cas muet sous copy-on-write, et un exercice dédié où les deux écritures donnent des résultats **différents mesurés**. |
| Écrire du pandas en boucle (l'anti-pattern total) | C06 §7 : la mesure de temps publiée (boucle vs vectorisé sur 50 000 valeurs) ; C08 §6 : la règle « vectoriser d'abord, `apply` ensuite ». |
| Les 12 écritures obsolètes noient le message | Elles n'apparaissent **qu'en C07 §9 (4) et C08 §8 (12)** ; le reste du module ne produit que des patterns 2.3/3.x valides — l'annexe est un repère, pas une leçon. |
| L'apprenant sur pandas 3.x voit des sorties différentes du manuel | §1.6 : tout code testé sous les deux versions ; chaque écart a son encadré « Dans les faits » ; l'annexe migration donne la correspondance complète (les 4 écarts mesurés sont l'exemple). |
| Le parallèle SQL/pandas dérive en « traduction mot à mot » | C08 §10 : le parallèle est montré, puis **cassé à dessein** sur 2 cas où pandas fait mieux (le `transform`, le pivot) — « traduire, puis choisir ». |

## 7. Étapes de production (calque M05/M06/M07)

1. **Étape 1 — Plan** (ce document) ✅.
2. **Étape 2 — Socle** : `tools/dossier_M08.py` (export déterministe de la base M07 figée → 8 CSV +
   brief + `ATTENDU.json` ~ 35 clés `m08p_*`) + `chiffres_manuel.py M08()` (~ 35 clés, mesurées en
   pandas sur les CSV — la vérification croisée SQL/pandas est le socle du module).
3. **Étape 3 — Rédaction** : 8 chapitres, cadence 1 push par chapitre validé `--strict`.
4. **Étape 4 — Figures** : `tools/figures_M08.py` (8 planches SVG, extension ≤ 776 px, jeu latin-1
   étendu).
5. **Étape 5 — PDF** : `tools/render.py --join "02_modules/M08_*.md"` → `M08.pdf` (budget 117 p.
   ±15 %).
6. **Étape 6 — Fiche de contrôle** : `05_livrables/fiche_controle_M08.md` Q1-Q10.
7. **Étape 7 — P2** : `03_exercices/M08_projet.md` (4 livrables /20 seuil 13) +
   `04_evaluations/M08_evaluation.md` (15 Q quiz + ~ 15 exercices « prédisez la sortie » auto-validés
   + 5 exercices rendus + E4 + étude de cas) + `README.md` (mise à jour) + push final.
