# Fiche de contrôle — module M13 (Modélisation des données)

**Porte de validation §G.1 de l'architecture (contrôles Q1 à Q10) · passée le 25 septembre 2026 ·
10/10 au vert, zéro écart bloquant, cinq nuances déclarées en fin de fiche (durées de lecture
volatiles et réalignées ; contrôle du PDF limité aux glyphes et aux libellés de planches ; budget
estimé par les mots faute de lecteur PDF dans l'atelier ; planches écrites sans accents ; exceptions
du socle déclarées et non corrigées).**

Cette fiche documente la livraison du module M13 — *Modélisation des données* — sept chapitres
(N3 → N4, 30 h) qui transforment un fichier plat de **240 000** lignes en un modèle de **14** tables
dont la recette est prouvée. Elle ne raconte pas les intentions : chaque ligne donne la commande
exécutée et ce qu'elle a rendu.

## 1. Les commandes de contrôle, et leur sortie réelle

| Commande | Sortie obtenue le 25 septembre 2026 |
|---|---|
| `python3 01_socle_donnees/scripts/autovalide.py M13 --strict` | `Résultat : OK (0 avertissement(s))` sur **9** fichiers (C01 à C07 + projet + évaluation) |
| `python3 01_socle_donnees/scripts/chiffres_manuel.py M13` | **394** clés `m13_*` : C01 **44** · C02 **22** · C03 **37** · C04 **27** · C05 **35** · C06 **94** · C07 **34** ; **2 726** clés au total pour le manuel |
| `python3 tools/modele_M13.py` | Les **4** contrôles au vert : unicité **14** tables sur **14** · grain **7** faits sur **7** · **12** clés étrangères, **0** orphelin · recette **15 595 154 955** FCFA par le modèle et par la source, `identiques` |
| `python3 tools/figures_M13.py --toutes` | **3** planches produites, **3/3** citées par leur chapitre : `M13_C03_grain_et_explosion.svg` **623** px · `M13_C04_frise_scd.svg` **668** px · `M13_C07_grille_revue.svg` **609** px (limite **776**) — empreinte déterministe `c2a252ef871ea6cb` |
| `python3 tools/render.py "0[234]_*/M13_*.md" --join --out 05_livrables/M13.pdf` | PDF rendu : `05_livrables/M13.pdf` · **774 Ko** · **107 pages** (**9** fichiers joints — les **7** chapitres, le projet et l'évaluation — + couverture + sommaire), **20** signets |
| `python3 tools/controle_pdf.py M13` | `M13 : 107 pages · figures : 3/3 vérifiées dans le PDF par leur libellé propre · glyphes : 27/27 composés · Défauts bloquants : 0` |
| `python3 tools/budget_pages.py --mesure` | `mesure M13 : 9 fichiers · 47 245 mots · budget 105 p. · estimé 104 p. d'après les mots ; 13,4 p./chapitre (calibre 12,5)` — module composé **107 p.** pour **105 p.** (**+ 1,9 %**, fourchette **[89, 121]**) |
| `python3 tools/render.py "03_exercices/M13_projet.md" --out /tmp/projet_M13.pdf` puis `"04_evaluations/M13_evaluation.md"` | projet **6 p.** · évaluation **9 p.** |
| `python3 tools/dossier_M13.py` | Socle reconstruit à l'identique : `socle_m13.sql` **17 776** o, `sha256[:16]` = `739e4ba68297bff8` ; empreintes identiques avant et après réexécution (`mouvements_clients.csv` `4a01740221f4`, `tarifs_produits.csv` `2209e17f525e`, `ATTENDU.json` `37b55d851f9d`) ; **1 120** mouvements (SCD2 **980** / SCD1 **140**), **616** tarifs, **7** familles |
| `python3 tools/poids.py` | `atelier : 124,0 Mo persistés sur 128 · 390 fichiers · marge +4,0 Mo` — dont **7,7 Mo** de source éditable ; le socle M13 ne pèse **77 Ko** de CSV, **aucun** fichier de base |
| `python3 -c "from pypdf import PdfReader; print(len(PdfReader('05_livrables/M13.pdf').pages))"` | `107` — confirme le contrôleur |

**Le verdict le plus fort du module.** Le mandat du projet exige « un modèle, pas un fichier ; une
table par sujet ; des clés déclarées ; et la preuve que le total est le même qu'avant ». Ces
exigences ne sont pas des intentions de cours : le modèle du fil rouge les **mesure** dans la section
**16** de son instrument — **14** tables sur **14** à clé unique, **7** faits sur **7** au grain de
leur source, **12** clés étrangères sans orphelin et la recette au franc près sur
**15 595 154 955** FCFA.

## 2. Les dix contrôles Q1 à Q10

### Q1 — Plan posé avant rédaction
- **Verdict : OK.** `05_livrables/plan_M13.md` poussé **avant** le socle et la rédaction (push
  n° **58**) : **7** chapitres (C01 → C07, **30** h, N3 → N4), budget **105** p. [**89**, **121**],
  projet « Le modèle de Sahel Distribution » — **4** livrables notés **6 + 6 + 5 + 3 = 20** points,
  seuil **13** —, évaluation (quiz **15** Q, seuil **11**, **2** exercices de normalisation, étude de
  cas **30** pts seuil **18**, auto-test **5** pts), **3** planches, les **8** décisions de
  modélisation du fil rouge.
- **Preuve :** plan n° **58**, socle et instrument n° **59**, puis C01 n° **61**, C02 n° **63**,
  C03 n° **69**, C04 n° **72**, C05 n° **74**, C06 n° **77**, C07 n° **78** — un push par chapitre
  validé, sans exception.

### Q2 — Socle reproductible et déclaré
- **Verdict : OK.** `tools/dossier_M13.py` reconstruit **8** fichiers dans `03_exercices/dossier_M13/`
  (socle SQL, connexion, modèle fautif, deux CSV de versions, table plate, revue de modèle, attendus).
  Deux exécutions successives donnent des empreintes **identiques** ; `ATTENDU.json` est inchangé.
- **Preuve :** `socle_m13.sql` **17 776** o, `sha256[:16]` `739e4ba68297bff8` ; **12** tables
  (**5** dimensions, **7** faits) ; **2** dimensions historisées bâties **en SQL** (**24 892** versions
  de clients, **616** versions de produits) ; génération en moins d'une seconde ; aucun fichier de base
  dans le dépôt — le socle est un script.

### Q3 — Chiffres sourcés dans le relevé
- **Verdict : OK.** Les **394** clés `m13_*` couvrent les quatre contrôles, la normalisation, le
  grain, l'étoile et les changements lents, le flocon, le temps et le calendrier, la revue. Le
  chapitre C06 a lui seul **94** clés, parce que le calendrier se mesure dans les deux sens.
- **Preuve :** `autovalide M13 --strict` refuse tout nombre de quatre chiffres ou plus introuvable
  dans le relevé ; **0** avertissement sur **9** fichiers. La règle de
  production a été tenue à chaque fois : une valeur nouvelle s'ajoute d'abord à l'instrument, puis au
  relevé, puis au chapitre. Un nombre écrit par erreur dans le chapitre C07 a été remplacé par sa
  mesure (**8,5 %** au lieu d'un **13,8 %** non mesuré), et un signe moins perdu dans le chapitre C06
  a été restauré avant la composition du PDF.

### Q4 — Gabarit des chapitres
- **Verdict : OK.** Les **7** chapitres portent **16** sections dans l'ordre imposé (`blocs_manquants`
  muet sur les sept) et respectent R8 : **Définition** de **5** à **6** par chapitre, **À retenir** de **2**
  à **3**, **Attention** de **2** à **3**, **Dans les faits** **1**, **Conseil professionnel** de **1**
  à **2**.
- **Preuve :** comptage des encadrés avant `--strict`, par le script d'autovalidation ; taille des
  chapitres entre **5 577** et **7 154** mots, soit **13,4** p. par chapitre pour un calibre de
  **12,5**.

### Q5 — Exercices et corrigés
- **Verdict : OK.** **33** exercices autonomes dans les **7** chapitres (C01 **4**, C02 **4**, C03 à
  C07 **5** chacun), **33** repris dans le corrigé, **0** énoncé sans reprise. Le projet, lui, est un
  livrable noté, et l'évaluation porte **12** requêtes d'auto-test.
- **Preuve :** contrôle R5 de l'autovalidation, qui compare chaque libellé d'exercice à sa reprise
  dans la section « Correction détaillée » ; les **10** exercices de C05 et de C06 se recopient et
  s'exécutent sur le socle, les autres demandent une preuve écrite.

### Q6 — Budget de pages respecté
- **Verdict : OK.** Module composé **107 p.** pour un budget de **105 p.**, soit **+ 1,9 %**, dans la
  fourchette **[89, 121]**. C'est la plus petite dérive de la phase 4 : **M11** était à − 8 % et
  **M12** à − 10,9 %.
- **Preuve :** `budget_pages.py --mesure` donne **47 245** mots et **13,4** p. par chapitre (calibre
  **12,5**) ; le PDF composé en fait **107**. L'estimation par les mots annonçait **104** p. : seul le
  PDF fait foi, et l'atelier ne sait pas le lire faute de `pypdfium2` (nuance 3).

### Q7 — Typographie et glyphes
- **Verdict : OK.** **0** occurrence de U+2013 et de U+2019 dans les **9** fichiers du module ; **27**
  glyphes composés sur **27** au contrôle du PDF ; les **3** planches sont citées par leur chapitre et
  retrouvées dans le PDF par leur **libellé propre**, pas par leur nom de fichier.
- **Preuve :** `controle_pdf.py M13` → `figures : 3/3 vérifiées dans le PDF par leur libellé propre ·
  glyphes : 27/27 composés · Défauts bloquants : 0`. Les planches obéissent au jeu **latin-1** et
  n'emploient ni accent ni tiret cadratin dans leur texte (nuance 4).

### Q8 — Anglicismes appariés
- **Verdict : OK.** Aucun terme de la liste `JARGON` de l'autovalidation (`dataframe`, `dashboard`,
  `dataset`, `pipeline`, `self-service`, `KPI`, `gouvernance de la donnée`) n'apparaît sans son couple
  français dans le module : le vocabulaire employé est « table de faits », « dimension », « table de
  pont », « dimension déchet », « calendrier », « tableau de bord ».
- **Preuve :** R7 muet sur les **9** fichiers ; le seul terme anglais conservé est `left join`, écrit
  en `code inline` avec sa traduction « jointure externe gauche » dans la même phrase.

### Q9 — Outils : exécuté contre cité
- **Verdict : OK.** Chaque chapitre déclare son régime d'exécution en tête de fichier : **DuckDB
  1.5.5 exécuté**, **pandas exécuté** (contrôle croisé des comptages), **PostgreSQL et Power BI cités
  et non exécutés** (règle §1.5). Les **7** chapitres portent la déclaration ; les **5** qui ne
  l'avaient pas l'ont reçue à la clôture.
- **Preuve :** le socle est ouvert par `03_exercices/dossier_M13/connexion.py` (DuckDB en mémoire) ;
  les **4** contrôles de l'instrument, les **5** exercices de C05 et les **5** exercices de C06 ont été
  **recopiés et exécutés** pendant la rédaction, et rendent les valeurs annoncées.

### Q10 — Livrables du plan présents
- **Verdict : OK.** Les **9** livrables nommés du plan existent et sont poussés : **7** chapitres,
  `05_livrables/M13.pdf`, `05_livrables/fiche_controle_M13.md`, `03_exercices/M13_projet.md`,
  `04_evaluations/M13_evaluation.md`, les **3** planches dans `figures/`, le socle
  `03_exercices/dossier_M13/` (**8** fichiers), l'instrument `tools/modele_M13.py` et
  `tools/figures_M13.py`.
- **Preuve :** vérification nommée, fichier par fichier, sur le dépôt distant après le push de
  clôture ; les **8** totaux de contrôle annoncés dans le projet sont ceux du socle.

## 3. Nuances déclarées

1. **Les durées de lecture sont volatiles.** Les clés `m13_c02_temps_*`, `m13_c04_temps_*` et
   `m13_c05_temps_*` changent d'une exécution à l'autre (mesuré : **2/3** puis **3/4** puis **3/3**
   ms pour l'étoile et le flocon ; **7/14** ms pour courant et historisé au dernier passage de C04).
   Les trois chapitres ont été **vérifiés un par un contre le relevé** à la clôture
   (**6** / **3** ms en C02, **7** / **14** ms en C04, **3** / **3** ms en C05) et chacun écrit que le
   chiffre cité est une **médiane de sept exécutions**.
2. **Le contrôle du PDF ne lit pas le contenu.** `controle_pdf.py` vérifie la pagination, la présence
   des figures par leur libellé et la composition des glyphes ; il ne relit pas la prose. La
   relecture du texte reste humaine, et elle a porté sur les **9** fichiers avant push.
3. **Le budget de pages est estimé par les mots.** `budget_pages.py --mesure` ne sait pas ouvrir un
   PDF dans cet atelier (`pypdfium2` absent) : il donne **104** p. estimées là où le PDF composé en
   compte **107**. Le chiffre retenu est celui du PDF, lu par `pypdf`.
4. **Les planches s'écrivent sans accents.** Le jeu de caractères des figures est latin-1 et le
   texte est volontairement sans accent (`modele`, `annees`, `feries`) pour rester extractible du
   PDF composé. Les chapitres, eux, sont accentués normalement.
5. **Les exceptions du socle sont déclarées, pas corrigées.** Le client absent du référentiel reçoit
   une ligne « client non identifié » (**43 161** ventes, **2 852 612 447** FCFA) ; deux prix sont
   manquants dans le fichier produits ; aucun jour du calendrier ne porte zéro vente, ce qui est une
   propriété du socle et non une règle générale. Ces trois points sont écrits dans les chapitres
   concernés et repris dans la grille de revue.

## 4. Synthèse

| Contrôle | Verdict | Preuve la plus courte |
|---|---|---|
| Q1 plan | OK | plan n° **58**, socle n° **59**, sept chapitres poussés un par un |
| Q2 socle | OK | empreintes identiques avant et après réexécution du générateur |
| Q3 chiffres | OK | **394** clés `m13_*`, `--strict` muet sur **9** fichiers |
| Q4 gabarit | OK | **16** sections et les **5** encadrés R8 dans les **7** chapitres |
| Q5 exercices | OK | **33** exercices, **33** repris au corrigé, **0** orphelin |
| Q6 budget | OK | **107** p. pour **105**, soit **+ 1,9 %**, dans **[89, 121]** |
| Q7 typographie | OK | **0** U+2013, **0** U+2019, **27/27** glyphes, **3/3** figures |
| Q8 anglicismes | OK | aucun terme de la liste `JARGON` sans couple français |
| Q9 outils | OK | DuckDB et pandas **exécutés**, PostgreSQL et Power BI **cités** |
| Q10 livrables | OK | les **9** pièces nommées du plan présentes sur le dépôt |

**Verdict du module : 10/10 au vert, 0 écart bloquant, 5 nuances déclarées.** M13 est le premier
module de la phase 4 dont le PDF dépasse légèrement son budget : **107** pages pour **105**, ce qui
tient au fait que le module porte **47 245** mots, le plus long de la phase 4. La dérive reste très
inférieure à la tolérance de **15 %**, et les trois modules suivants garderont la marge comme
indicateur plutôt que le calibre fixe.
