# M01 — Bilan de compétences et auto-positionnement

> À remplir **à la main** (ou dans `journal.md` de votre cahier de l'apprenant) après le projet et l'évaluation. Ne sautez pas cette page : le parcours est conçu pour un autodidacte, et un autodidacte qui ne s'auto-évalue pas accumule des trous qui ne se voient qu'au module 12.

---

## 1. Je sais maintenant (vocabulaire — à cocher, et à définir de ma main)

Cochez seulement si vous pouvez **définir le mot en une phrase, sans jargon**, à quelqu'un qui ne travaille pas dans l'informatique.

| Terme | Je le définis sans aide | Ma phrase à moi |
|---|---|---|
| donnée · information · connaissance · décision | ☐ | |
| table · ligne · colonne · cellule · en-tête | ☐ | |
| grain d'une table | ☐ | |
| clé primaire · clé étrangère · valeur distincte | ☐ | |
| type de données · inférence de type | ☐ | |
| nombre stocké en texte | ☐ | |
| encodage · séparateur · décimale · chapeau | ☐ | |
| structuré · semi-structuré · non structuré | ☐ | |
| qualitatif (nominal, ordinal) · quantitatif (discret, continu) | ☐ | |
| échelle de mesure (nominale, ordinale, intervalle, ratio) | ☐ | |
| question analytique · critère de réussite · périmètre | ☐ | |
| métrique · indicateur (KPI) | ☐ | |
| source de vérité · jeu figé · empreinte (hash) | ☐ | |
| dictionnaire de données · journal de transformation · manifeste | ☐ | |
| cycle de vie d'une donnée · rétention · minimisation | ☐ | |

**Test de réalité.** Écrivez, sans regarder, ce que représentent : une ligne de `ventes_brutes.csv` (243 360 lignes) · une ligne de `objectifs_de_ca.csv` (218) · une ligne de `remises_manuelles.xlsx` (18 200) · une ligne de `dim_date.csv` (1 339). Quatre bonnes réponses = acquis. Trois ou moins = reprenez le chapitre C03, §5.2.

## 2. Je suis capable de (gestes professionnels)

Niveau d'autonomie : **A** = je le fais seul · **E** = je le fais avec la fiche sous les yeux · **N** = pas encore.

| Geste | A / E / N | Preuve chez moi (fichier ou capture) |
|---|---|---|
| Ranger un dossier de travail en six étapes numérotées, avec brut en lecture seule | ☐ | |
| Nommer un fichier selon `AAAA-MM-JJ_quoi_qui_etat.ext` | ☐ | |
| Vérifier qu'une sauvegarde se restaure réellement | ☐ | |
| Décrire une table inconnue en six phrases | ☐ | |
| Compter des lignes, des objets distincts, des valeurs manquantes dans un tableur | ☐ | |
| Détecter une colonne de montants stockée en texte avec deux formules | ☐ | |
| Convertir une colonne sans perte, avec contrôle avant/après | ☐ | |
| Réparer deux formats de date dans une même colonne, et prouver la réparation | ☐ | |
| Vérifier séparateur, encodage, décimale et chapeau d'un fichier plat | ☐ | |
| Classer une variable et dire quel calcul est licite | ☐ | |
| Rédiger un dictionnaire de colonnes avec la colonne « défauts connus » | ☐ | |
| Tenir un journal de transformation avec écarts chiffrés | ☐ | |
| Convertir une demande floue en question analytique à cinq composants | ☐ | |
| Choisir un outil (tableur · SQL · Python · Power BI) et justifier par volume, relecteur, rejouabilité | ☐ | |
| Rédiger une note de décision en six rubriques, limites comprises | ☐ | |

**Seuil de passage :** 11 gestes sur 15 en A ou E, dont obligatoirement « détecter une colonne texte », « question analytique à cinq composants » et « note en six rubriques ». Ces trois-là sont les prérequis réels du module 2.

## 3. Outils maîtrisés à la sortie du module

| Outil | Ce que je sais faire sans aide | Ce que je ne sais pas encore faire (et dans quel module ça s'apprend) |
|---|---|---|
| Explorateur / Finder | chemins, extensions, recherche, propriétés, lecture seule | scripts de renommage en masse (M08) |
| Tableur (Excel ou LibreOffice) | import assisté, `NB`, `NBVAL`, `CBI`/`VALUE`, `SUPPRESPACE`, tri, filtre, comptage de doublons, formules matricielles simples | tableaux croisés, Power Query, `RECHERCHEX` (M03-M06) |
| Éditeur de texte | lire un CSV, compter des lignes, repérer un encodage | écrire un parseur (M08, M20) |
| Terminal | `wc -l`, `head`, `cut`, `grep`, `file -i`, `md5sum`/`Get-FileHash` | automatiser une chaîne de traitement (M08, M24) |
| Power BI, SQL, Python | — je sais **quand** ils sont nécessaires et je le justifie | M07 (SQL), M08-M10 (Python), M13-M18 (Power BI) |

Cette colonne de droite est la plus utile : savoir nommer l'outil qui manque, avec la raison de son absence, est déjà une compétence d'architecte.

## 4. Niveau atteint

Le manuel utilise cinq niveaux, définis au §B.2 de l'architecture. En sortie de M01 :

| Niveau | Définition | Où j'en suis |
|---|---|---|
| **N1 — Literatie** | comprendre le vocabulaire, lire une donnée, savoir où elle est, formuler une question | ✔ objectif du module |
| N2 — Opérateur | produire des mesures justes dans un outil | M02-M06 |
| N3 — Analyste | mener une analyse complète et la défendre | M07-M12 |
| N4 — Concepteur | modéliser, industrialiser, administrer | M13-M21 |
| N5 — Référent | arbitrer, budgéter, transmettre | M22 et la pratique |

Auto-positionnement : placez-vous sur N1 avec un chiffre de 1 à 5 (1 = je découvre encore le vocabulaire, 5 = je peux l'expliquer à un collègue avec nos données à lui). Notez la date. Vous referez ce test à la fin de M06, de M12, de M18 et de M22 : **la progression du chiffre compte plus que le chiffre lui-même**.

## 5. Pour passer au module suivant

1. **Correction des exercices manqués.** Reprenez uniquement les énoncés où votre réponse diffère du corrigé sur un **nombre** (pas sur la formulation). Un écart de vocabulaire se corrige en écrivant la définition ; un écart de nombre se corrige en refaisant le calcul.
2. **Préparer M02.** Gardez sous la main le fichier `2025_ventes_M5_propre_v1.csv` que vous avez produit (480 lignes, 36 073 185 FCFA) : le module 2 part de **vos** colonnes nettoyées, et non d'un fichier fourni. Si vous ne l'avez pas, refaites-le : c'est le temps d'achat du module 2.
3. **Trois choses à savoir par cœur avant le premier chapitre de M02** : le grain du fichier (une ligne = un article d'un ticket) · la différence entre 489 lignes et 316 tickets · le fait que 0,74 % du total dépend du nettoyage. Sans ces trois repères, les statistiques du module 2 seront comprises trop tard.
4. **Le droit à l'erreur est organisé, pas négocié.** Toute erreur détectée après coup dans ce manuel est corrigée à la source et publiée en annexe « errata » (règle de production n° 7) : signalez-la, vous contribuez à l'ouvrage, et vous gardez la trace de votre contrôle dans votre journal — ce qui compte pour la soutenance du module 22.

## 6. Auto-questionnement dirigé (à écrire, 15 minutes)

1. Quel défaut du fichier de l'atelier m'a le plus surpris, et pourquoi ne l'avais-je pas vu ?
2. Quelle formule ou quel réflexe du module vais-je utiliser dès demain, même hors formation ?
3. Quel terme technique ai-je employé sans pouvoir le définir ? (→ à recopier dans `glossaire_personnel.md`)
4. Quelle demande professionnelle réelle, en attente chez moi, puis-je convertir en question analytique cette semaine ?
5. Ai-je écrit un journal de transformation qui permettrait à un inconnu de refaire mon travail ? Si non, qu'est-ce qui m'en a empêché — le temps, la méthode, ou la peur du regard ?

Ces cinq questions sont celles que poserait un enseignant en fin de module. Un enseignant, ici, n'existe pas : le cahier de l'apprenant le remplace, à condition de l'ouvrir.

---

**Contrôle de sortie du module (à cocher par l'apprenant, vérifié par la suite du parcours)**

- [ ] 7 chapitres lus et les 7 mini-projets rendus
- [ ] quiz ≥ 14/20 · projet M01.P complet et noté ≥ 13/20
- [ ] étude de cas rendue (cadrage de 5 demandes)
- [ ] fichier propre produit et total de contrôle = 36 073 185 FCFA
- [ ] dictionnaire de données avec colonne « défauts connus » remplie (65 · 486 · 18 · 7 · 9)
- [ ] journal de transformation ≥ 12 entrées, avec écarts chiffrés
