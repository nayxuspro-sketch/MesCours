# Fiche de contrôle — module M03 (Excel pour l'analyse de données)

**Porte de validation §G.1 de l'architecture (contrôles Q1 à Q10) · passée le 18 septembre 2026 · 9/10 au vert,
un contrôle ouvert (Q10) et cinq écarts déclarés en fin de fiche.**

Comme les deux précédentes, cette fiche ne raconte pas les intentions : chaque ligne donne la commande exécutée et
ce qu'elle a rendu. Deux défauts y ont été trouvés, dans l'ordre où ils sont listés plus bas — un dans le classeur
livré, un dans le contrôleur qui devait le garder. Les deux sont corrigés dans le dépôt.

## 1. Les commandes de contrôle, et leur sortie réelle

| Commande | Sortie obtenue le 18 septembre 2026 |
|---|---|
| `python3 01_socle_donnees/scripts/autovalide.py M03 --strict` | `Résultat : OK (0 avertissement(s))` sur **10 fichiers** (8 chapitres + `M03_projet.md` + `M03_evaluation.md`) |
| `python3 01_socle_donnees/scripts/chiffres_manuel.py M01 M02 M03` (deux exécutions) | 71 clés pour M01, 406 pour M02, **138 pour M03** ; `diff` du `chiffres_cites.json` publié entre les deux passages = **0 ligne** → les chiffres cités sont reproductibles |
| `python3 tools/controle_formules.py` | classeur recalculé en 4,0 s par `formulas` · **123 contrôles conformes, 0 écart** · « aucune cellule de contrôle ne doit être une erreur » ✔ · 28 fiches de la feuille `Calculs` |
| `python3 tools/controle_sql.py M03` | `SQL exécuté : 0 réussite(s), 0 échec(s)` — **aucun bloc SQL n'est publié dans M03**, rien à exécuter (le SQL s'enseigne en M05 en miroir et en M07) |
| `python3 tools/controle_python.py M03` | `Python publié : 0 bloc(s) exécuté(s), 0 fragment(s) à nom non résolu, 0 défaut(s)` — pareil : M03 n'enseigne pas Python |
| `python3 tools/figures_M03.py` | 9 figures régénérées ; largeur contrôlée à la génération (`largeur ok`, extension maximale estimée 764 px pour `M03_C08_tcd_et_modele.svg`, 746 px pour `M03_C08_chemin_donnees.svg`) |
| `python3 tools/budget_pages.py --mesure` | M03 : 10 fichiers · 60 526 mots · budget 117 p. · composé **121 p.** → dérive **+3 %** ; 14,7 p./chapitre (calibre 12,5) · verdict : `budget additif et conforme à l'architecture` |
| `python3 tools/nb_pages.py 05_livrables/M01.pdf … M03.pdf` | **110** · **113** · **121** pages composées |
| `python3 tools/controle_pdf.py M01 M02 M03` (outil ajouté à cette fiche) | figures retrouvées dans le PDF rendu : 7/7, 4/4, **9/9** ; glyphes composés : 55/55, 47/47, **37/37** ; `Défauts bloquants : 0` |
| lecture directe du classeur (`openpyxl`, `data_only`) | 11 feuilles ; `ventes` `A1:N481` avec 480 montants numériques ; `ventes_brutes` `A1:M490` entièrement texte ; `Calculs` `A1:G29` = 28 fiches ; `TCD` 7 rayons ; `Mensuel` 12 mois + total |

**Le contrôle croisé le plus fort de la série.** Le total de référence du module — `36 073 185` FCFA — est produit
par quatre chemins indépendants : la clé publiée `m03_ca_attendu` du générateur, le recalcul par `formulas` de la
formule `=SUM(ventes!M2:M481)` stockée dans la feuille `Calculs`, la somme des cellules lues dans le fichier par
`openpyxl`, et un `pandas` sur `ventes_magasin5_2025_ATTENDU.csv`. Les quatre tombent sur le même nombre, et la
colonne `contrôle` du classeur affiche `ok` sur la ligne. C'est ce nombre — et non un total recopié — qui apparaît
dans le corrigé du projet et dans celui de l'évaluation.

**Deux défauts trouvés en passant cette fiche, et ce qu'ils étaient.**

1. **Dans le classeur livré.** La fiche 3 de `Calculs` annonçait `=NB(ventes_brutes!M2:M490)` → 3 et la fiche 4
   `=SOMME(…)` → 2 444 FCFA. Ces deux nombres sont vrais du **CSV reçu** (trois montants saisis sans séparateur de
   milliers, lignes 88, 179 et 236) ; ils sont faux du **classeur**, dont la feuille `ventes_brutes` est écrite
   entièrement en texte — donc Excel et LibreOffice y rendent 0 et 0, et la colonne `contrôle` aurait affiché
   « à revoir » sur la feuille même dont le rôle est de dire « ok ». Le générateur calcule maintenant les deux
   valeurs attendues à partir de ce qu'il écrit (`nb_brut`, `somme_brut`), et le chiffre du CSV passe dans le
   commentaire de la fiche, qui renvoie à C02 §5.1. Aucun énoncé du manuel ne citait les anciennes valeurs : la
   prose de C05 §5.6 (« `SOMME` rend 0, `MOYENNE` rend `#DIV/0!`, … ») était juste, l'auto-contrôle du fichier non.
2. **Dans le contrôleur.** `formulas` convertit « 1234 » stocké en chaîne là où Excel ne le convertit pas : la ligne
   passait donc pour la mauvaise raison, et le défaut ci-dessus ne pouvait pas être vu par elle. Les deux lignes qui
   portent sur la feuille de preuve sont désormais comparées aux **types réellement stockés dans le fichier**, et la
   divergence des moteurs est imprimée plutôt que masquée — c'est pourtant le sujet de C05 §5.6 (`NB.SI` convertit,
   `NB` ne convertit pas).

## 2. Les dix contrôles, un par un

| # | Contrôle (critère de passage) | Verdict | Preuve |
|---|---|---|---|
| Q1 | 16/16 blocs du gabarit, 100 % des objectifs du module portés et prouvés | ✔ 8 chapitres sur 8 | R1 d'`autovalide.py` (présence **et ordre** des seize blocs) rendu muet en mode strict sur les 10 fichiers. Portée des objectifs : se déplacer sans risque → C01-C02 ; structurer et trier → C03 ; formules et erreurs → C04 ; agréger honnêtement → C05 ; assembler → C06 ; dates et matricielles → C07 ; TCD, modèle, protection → C08. Le livrable visé par l'architecture (« classeur de gestion TCD/DASH complet », compétence 5) est produit par `M03_projet.md` : 6 livrables sur 20, seuil 13 |
| Q2 | 0 violation de progressivité (aucune notion employée avant d'avoir été enseignée) | ✔ | Power Query et le modèle relationnel ne sont qu'**annoncés** en C08 (chapitre M05 et M06) ; `SOMME.SI.ENS` est enseigné en C05 avant la grille mensuelle de C07 ; les références structurées en C03 avant les colonnes calculées de C06 ; le TCD en C08 §5.1 avant la mesure DAX §5.6. Trois références inter-modules fausses ont été trouvées et corrigées à cette occasion : SQL attribué à « M04 » (2 endroits dans C08, 1 dans l'évaluation) alors que M04 est la qualité et la documentation — renvoi désormais à M05 en miroir et M07 ; et « Power BI (M13) » en M01.C05, corrigé en M14 |
| Q3 | 100 % d'exécution sans erreur (SQL, Python, formules) | ✔ 123/123 | `controle_formules.py` : 123 contrôles conformes, 0 écart, sur un classeur recalculé ligne à ligne ; SQL et Python : 0 bloc publié dans M03, donc rien qui puisse casser. Excel et LibreOffice ne s'exécutent pas ici : chaque valeur que le chapitre affirme est recalculée en pandas par le générateur, publiée dans `chiffres_cites.json`, et reprise dans la feuille `Calculs` avec sa colonne `contrôle` |
| Q4 | écart 0 avec `verites_terrain.csv`, joints sans perte | ✔ | 138 clés M03, deux exécutions identiques au `diff` près ; les quatre chemins du total de référence concordent (§ 1) ; la moyenne par ligne (75 152), par ticket (114 156), par jour ouvré (150 305) et par jour couru (107 361) sont les quatre valeurs que C07 et le corrigé de l'évaluation citent, toutes descendues du même tableau. Le défaut de la fiche 3 de `Calculs` a été trouvé **à** cette étape, pas après |
| Q5 | 100 % des énoncés corrigés, avec le résultat intermédiaire | ✔ | R5 muet en strict : chaque « Exercice c.n » des huit chapitres est repris dans le bloc « Correction détaillée » du même fichier ; le projet a ses 6 livrables corrigés avec les nombres attendus ; l'évaluation a ses quatre épreuves corrigées (A non notée 9 questions, B quiz 15 questions /15 seuil 11, C 4 exercices /20, D étude de cas /20 seuil 12) avec la table de décision de passage |
| Q6 | 0 contradiction, une seule définition par terme | ✔ corrigé | Scan des 10 fichiers : **33 encadrés Définition**, 42 termes en gras à l'intérieur, **un seul** défini deux fois — « colonne calculée », en C03 pour le tableau et en C08 pour le modèle. Le second encadré dit maintenant la différence de mécanique (propagée à la saisie là-bas, recalculée à l'actualisation ici) et renvoie à C03, au lieu de redéfinir le mot comme s'il était nouveau |
| Q7 | 100 % des termes non communs définis au premier emploi | ✔ | R7 (couple « français — *english* » exigé à chaque anglicisme, mots doublés, idéogrammes) muet en strict. Scan indépendant des 10 fichiers : aucun caractère hors latin-1 en dehors du petit jeu de la maison (`→` 115 fois, `★` 75, `−` 24, exposants `ᵉ` 18 et `ʳ` 7), et trois glyphes que M01/M02 n'employaient pas — `↑` `↓` `▼`, 13 occurrences, pour le sens d'un tri et le triangle d'un filtre ; `controle_pdf.py` prouve qu'ils sont composés dans le PDF (37/37). Un doublon signalé par le scan a été écarté parce que faux (« vous vous postez ») |
| Q8 | 100 % des affirmations d'outil datées ou marquées « à vérifier » | ✔ | Chaque affirmation d'indisponibilité nomme la version **et** son symptôme (C06 l. 186 : « dans Microsoft 365, Excel 2021 et 2024, et dans LibreOffice Calc récent ; en Excel 2019, le nom renvoie `#NOM?` »), et 13 mentions « à vérifier / vérifié » sont réparties sur six chapitres, dont les trois points qui peuvent bouger sur un poste réel : nom non traduit d'une fonction, disponibilité selon la licence, séparateur de décimales. La date de vérification est portée par cette fiche (18 septembre 2026) et non par le chapitre — c'est déjà l'usage de M01 et M02 (`grep septembre 2026 02_modules/M0[12]_*.md` : 0) |
| Q9 | tables de plus de 6 colonnes doublées d'une version courte, aucune information par la seule couleur | ✔ corrigé | Scan programmé des 10 fichiers : largeur **maximale observée 7 colonnes**, un seul tableau concerné — la table des quatre arrondis de C04 §5.6 (ticket, quantité, prix, remise, produit brut, enregistré, `ARRONDI`). Elle a reçu sa « version alternative pour un petit écran », deux phrases qui tiennent tout son contenu, comme les deux tables de sept colonnes de M01 (C05 §5.2 et C06 §5.2) que le même scan retrouvé confirme doublées. Le scan imprime la largeur maximale et pas seulement les dépassements : sa première mouture, dont la classe de caractères lisait `:-|` comme une plage, ne matchait aucune ligne de séparateurs et annonçait « 0 tableau de 7 colonnes » — un faux négatif parfait. Aucune information portée par la couleur seule : chaque mise en forme conditionnelle est écrite avec sa formule et son effet en toutes lettres (C02 §5.6 : « 489 cellules allumées ; 486 après un import qui en a converti trois »), et les ✔/✘ des tableaux sont des glyphes (37/37 composés dans le PDF), pas des teintes |
| Q10 | ≤ 5 passages à relire par chapitre | **écart ouvert** | Voir § 3, point 1. Ce qui a été fait : trois passes de resserrement sur C08 (52 631 → 45 672 caractères, 16 blocs et 20 tableaux intacts, les nombres inchangés), une relecture ligne à ligne avec onze corrections de contenu (dont `#VALUE!` → `#N/A` dans un corrigé, et un jour férié tombant un jour de fermeture), et les scannages qui attrapent les accidents d'écriture |

## 3. Écarts ouverts

1. **Q10, test de lecture « débutant simulé ».** Il se conduit à la relecture complète d'un module d'une traite, ce
   que la production en cours ne permet pas de déclarer tenu — comme pour M01 et M02. Programmé à l'étape 4, sur le
   texte assemblé, module par module.
2. **Glossaire et index FR/EN (étape 4).** La non-redondance est contrôlée *dans* M03 (33 encadrés, un doublon
   traité ci-dessus) ; elle n'est pas encore contrôlée *entre* M01, M02 et M03, le glossaire n'existant pas avant
   l'assemblage.
3. **Pagination des signets.** `nb_pages.py` annonce pour M03 un `/Count` de 225 pour 121 pages réelles (M01 : 208
   pour 110 ; M02 : 233 pour 113). Le désaccord est le même sur les trois modules, il touche la table des matières
   interne du PDF et non la pagination imprimée : à trancher à l'assemblage, pas module par module.
4. **Calibre.** M03 est le plus dense des trois modules en mots (60 526 sur ses 10 fichiers, contre 55 264 pour M02
   et 50 280 pour M01), soit 14,7 pages par chapitre à la conversion mots→pages, dans la fourchette maison 10-16. La composition réelle
   tient pourtant le budget : 121 pages pour 117 prévues (+3 %), comme M01 (+5 %) et M02 (−3 %). Si l'étape 4 doit
   revenir au calibre 12,5, les deux coupes naturelles sont C01 §5.5-5.6 (l'anatomie de l'écran) et C08 §5.8 (le
   tableur comme environnement) — décision reportée, pas un défaut.
5. **Ce que cet atelier ne peut pas exécuter : Excel, LibreOffice, Power BI.** Aucun contenu DAX au-delà du
   vocabulaire de C08 §5.6, aucune requête Power Query (M05), et toute affirmation sur le comportement d'une formule
   est doublée d'un calcul en pandas ou de la colonne `contrôle` du classeur. Le classeur de correction n'existe pas
   et n'est promis nulle part : la réparation passe par la feuille `Calculs` et par le corrigé du projet.

## 4. Ce que la fiche change à la production

Quatre règles, applicables dès M04 :

- **Une valeur attendue se mesure sur le fichier livré, pas sur sa source.** Un auto-contrôle d'un classeur doit
  être vrai *dans* ce classeur. Le générateur de M03 déduit maintenant les deux lignes litigieuses de ce qu'il écrit
  lui-même : si une version future du fichier contient de vrais nombres dans `ventes_brutes`, l'attente suivra toute
  seule.
- **Un moteur de recalcul tolérant n'est pas l'outil enseigné.** `formulas` convertit du texte numérique, Excel ne
  le convertit pas. Là où les deux divergent, `controle_formules.py` compare aux types stockés dans le fichier et
  affiche la divergence — une tolérance d'implémentation ne doit jamais devenir une preuve.
- **Une mesure qui tombe en estimation sans le dire est une mesure fausse.** `budget_pages.py` écrivait
  « composé 133 p. » alors qu'il n'avait pas lu le PDF (`pypdfium2` absent) et annonçait pour M03 une dérive de
  +14 %. Le script dit maintenant « estimé … PDF non lu (installer `pypdfium2`) » ; avec la dépendance, la dérive
  mesurée est **+3 %**. Le +14 % cité oralement avant cette fiche était l'artefact, pas le module.
- **Un scan qui ne matche rien est un scan qui ment poliment.** Celui des largeurs de tableaux annonçait zéro
  dépassement parce qu'aucune ligne de séparateurs ne passait sa regex. Un verdict « 0 » venu d'un motif
  inexistant et un verdict « 0 » venu d'un corpus conforme se ressemblent : depuis, le contrôle imprime la
  largeur maximale observée, qui trancherait.
- **Un contrôle qui lit le fichier rendu est le seul qui prouve l'impression.** `tools/controle_pdf.py`, écrit pour
  cette fiche, vérifie dans le PDF que chaque figure des sources y a son libellé propre (le SVG est composé en
  XObjects vectoriels : 11 011 XObjects et 0 objet `/Image` dans `M03.pdf`, donc compter les images ne prouvait
  rien) et que chaque glyphe non ASCII des sources ressort du texte extrait.
