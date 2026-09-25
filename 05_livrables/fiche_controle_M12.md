# Fiche de contrôle — module M12 (Fondamentaux de la Business Intelligence)

**Porte de validation §G.1 de l'architecture (contrôles Q1 à Q10) · passée le 25 septembre 2026 ·
10/10 au vert, zéro écart bloquant, quatre nuances déclarées en fin de fiche (outil de restitution cité
et non exécuté ; planches lues en SVG et contrôlées par leur libellé dans le PDF ; deux réconciliations
de chiffres assumées en cours de route ; devise FCFA conservée du fil rouge).**

Cette fiche documente la livraison du module M12 — *Fondamentaux de la Business Intelligence* — six
chapitres (N3, 30 h) qui apprennent à **choisir** un indicateur, à **écrire** sa définition, à **poser**
son seuil et à **trouver** son contre-KPI. Elle ne raconte pas les intentions : chaque ligne donne la
commande exécutée et ce qu'elle a rendu.

## 1. Les commandes de contrôle, et leur sortie réelle

| Commande | Sortie obtenue le 25 septembre 2026 |
|---|---|
| `python3 01_socle_donnees/scripts/autovalide.py M12 --strict` | `Résultat : OK (0 avertissement(s))` sur **8 fichiers** (C01 à C06 + projet + évaluation) |
| `python3 01_socle_donnees/scripts/chiffres_manuel.py M12` | **255 clés** `m12_*` ; deux exécutions successives : `diff` de `chiffres_cites.json` = **0 ligne** → reproductible ; **2 332** clés au total pour le manuel |
| `python3 tools/dossier_M12.py` | Socle régénéré : **6** CSV + `socle_m12.sql` (**4 375** octets, `sha256[:16]` = `fe5b6bfc5eb74cd8`) ; `ATTENDU.json` **identique** avant/après ; `ruptures.csv` **inchangé** au caractère près ; génération complète en **0,70** s ; `aucun fichier .duckdb : le socle est un script, il ne pèse rien en dépôt` |
| `python3 tools/kpi_M12.py` | Les **10** KPI, les **4** régimes de question, le vocabulaire du grain et les **6** critères d'un KPI imprimés en console, chacun **avec sa définition au-dessus du chiffre** : CA net **15 595 154 955** FCFA · marge **29,12 %** · rupture **7,29 %** · rotation **9,42** tours · panier **107 396** FCFA · retour **1,17 %** · service **81,0 %** / **78,2 %** · recouvrement **74,0 %** · logistique **3 284** FCFA · part interne **60,8 %** / **39,2 %** |
| `python3 tools/figures_M12.py` | **2** planches produites, **2/2** déterministes (deux productions, même empreinte), **2/2** citées par leur chapitre : `M12_C05_carte_des_sept_etages.svg` **623 px** et `M12_C06_matrice_des_dix_couples.svg` **625 px** (limite 776) ; texte réel dans le SVG (`svg.fonttype = none`) ; **aucun chiffre écrit en dur** (tous lus dans `chiffres_cites.json`) |
| `python3 tools/render.py "0[234]_*/M12_*.md" --join --out 05_livrables/M12.pdf` | PDF rendu : `05_livrables/M12.pdf` · **586 Ko** · **82 pages** (**8** fichiers joints — les **6** chapitres, le projet et l'évaluation — + couverture + sommaire) |
| `python3 tools/controle_pdf.py M12` | `M12 : 82 pages · figures : 2/2 vérifiées dans le PDF par leur libellé propre · glyphes : 31/31 composés · Défauts bloquants : 0` |
| `python3 tools/budget_pages.py --mesure` | `M12 : 8 fichiers · 32 214 mots · budget 92 p.` — module composé **82 p.** pour **92 p.** (**−10,9 %**, dans la fourchette **[78, 106]**) ; l'estimation par les mots donnait **71 p.** : seul le PDF fait foi |
| `python3 tools/render.py "03_exercices/M12_projet.md" --out /tmp/projet_M12.pdf` puis `"04_evaluations/M12_evaluation.md"` | projet **6 p.** · évaluation **7 p.** |
| `python3 tools/poids.py` | `atelier : 122,3 Mo persistés sur 128 · 358 fichiers · marge +5,7 Mo` — le socle M12 pèse **1,33 Mo** (six CSV déterministes) et **aucun** fichier de base |
| `python3 -c "from pypdf import PdfReader; print(len(PdfReader('05_livrables/M12.pdf').pages))"` | `82` — confirme le contrôleur |
| `python3 -c "import hashlib; ..."` sur `socle_m12.sql` | **4 375** octets, empreinte `fe5b6bfc5eb74cd8` — publiée ici pour qu'un tiers puisse comparer |

**Le verdict le plus fort du module.** Le mandat exige « pas plus de **10** indicateurs, chacun avec sa
définition écrite, son responsable, sa fréquence, son seuil et son contre-indicateur ». Ces exigences ne
sont pas des intentions de cours : elles sont **mesurées** dans le chapitre C04 — **7** champs × **10**
KPI = **70** cases à remplir, contre **41** indicateurs sans carte au dossier raté —, et **5** des **10**
critères de réussite portent une valeur recalculable à chaque exécution.

## 2. Les dix contrôles Q1 à Q10

### Q1 — Plan posé avant rédaction
- **Verdict : OK.** `05_livrables/plan_M12.md` poussé **avant** le socle et la rédaction (push n° **46**) :
  **6** chapitres (C01 → C06, **30** h, N3), budget **92** p. [**78**, **106**], projet « Le tableau de bord
  que personne n'ouvrait » — **4** livrables notés **6 + 8 + 4 + 2 = 20** points, seuil **13** —,
  évaluation (quiz **15** Q, seuil **11**, **2** exercices de rédaction de KPI, étude de cas **30** pts
  seuil **18**), **2** figures, les **10** couples indicateur / contre-KPI du §1.7.
- **Preuve :** plan poussé au n° **46**, socle et instruments au n° **47**, puis C01 n° **48**, C02 n° **49**,
  C03 n° **50**, C04 n° **52**, C05 n° **55**, C06 n° **57** — un push par chapitre validé, sans exception.

### Q2 — Socle reproductible et déclaré
- **Verdict : OK.** `tools/dossier_M12.py` (graine **46**) reconstruit **6** CSV + `socle_m12.sql` +
  `connexion.py` + `ATTENDU.json` + `etude_avant.md` ; deux générations successives donnent des fichiers
  identiques (`ruptures.csv` vérifié au caractère près) ; `ATTENDU.json` inchangé.
- **Preuve :** **1,33 Mo** de sources, **0,70** s de génération, **8** tables et **1** vue, `sha256[:16]` du
  socle `fe5b6bfc5eb74cd8`. Sources ajoutées par M12 : coût d'achat (**154** lignes), stock mensuel
  (**6 776**), ruptures (**2 428**), commandes (**9 000**), encaissements (**9 000**), logistique (**264**).

### Q3 — Chiffres sourcés dans le relevé
- **Verdict : OK.** Les **255** clés `m12_*` couvrent les **10** KPI, les **4** régimes de question, le
  vocabulaire du grain (grain, additivité, fan-out), les **6** critères d'un KPI et l'économie du projet.
  `autovalide --strict` refuse tout nombre de quatre chiffres ou plus introuvable dans ce relevé.
- **Réserves déclarées :** les clés de texte sont écrites **sans accents** (contrainte du relevé JSON), et
  les identifiants de ticket sont cités en `code inline`.

### Q4 — Gabarit des chapitres
- **Verdict : OK.** Les **6** chapitres portent les **16** blocs du gabarit, dans l'ordre, et la fréquence
  des encadrés est respectée : **5** « Définition », **2** « À retenir », **2** « Attention », **1**
  « Conseil professionnel », **1** « Dans les faits » par chapitre.
- **Piège évité, documenté :** un encadré rédigé `> **Définition — X.**` ne compte **pas** dans le contrôle
  R8, qui n'accepte que la forme `> **Définition.**` ; cette forme est désormais écrite **dès la
  rédaction**, comme l'impose PATCH_13.

### Q5 — Exercices et corrigés
- **Verdict : OK.** Chaque chapitre a son exercice guidé, ses **6** exercices autonomes et leur
  **correction détaillée** ; le contrôle R5 vérifie la reprise de chaque énoncé dans le corrigé.
- **Preuve :** le contrôle passe sur les **8** fichiers, y compris le projet et l'évaluation (quiz **15**
  Q avec corrigé, **2** exercices de rédaction avec barème, étude de cas avec son barème de **30** points
  et son seuil de **18**).

### Q6 — Budget de pages respecté
- **Verdict : OK.** **82** pages composées pour **92** pages de budget (**−10,9 %**), dans la fourchette
  autorisée [**78**, **106**] ; chapitres, projet (**6** p.) et évaluation (**7** p.) sont joints dans le
  même PDF, couverture et sommaire compris.
- **Nuance :** l'estimation par les mots donnait **71** pages — l'instrument de mesure par les mots
  sous-estime les modules à tableaux ; **seul le PDF fait foi**, comme l'a montré M11 (**93** estimées,
  **97** réelles).

### Q7 — Typographie et glyphes
- **Verdict : OK.** `controle_pdf.py` compose **31/31** glyphes du corpus dans le PDF ; le tiret
  demi-cadratin U+2013 est **absent** des **8** fichiers (contrôle : `0` occurrence) et l'écriture emploie
  le tiret cadratin U+2014 et le signe moins U+2212.
- **Preuve :** les deux planches SVG sont écrites en texte réel (`svg.fonttype = none`), donc vérifiables
  dans le PDF par leur libellé propre — contrôle rendu : **2/2**.

### Q8 — Anglicismes appariés
- **Verdict : OK.** Les termes anglais employés portent leur couple français : *pipeline* → **chaîne de
  calcul**, *sponsor* → **commanditaire**, *semantic layer* → **couche sémantique**, *data warehouse* →
  **entrepôt de données**, *data lake* → **lac de données**, *KPI* → **indicateur clé**, *self-service* →
  **service en autonomie**, *pipeline* reposé en C05 sous forme appariée.
- **Nuance :** le contrôle a d'abord refusé « gouvernance de la donnée » employé seul (terme suivi dans la
  liste du jargon) ; la rédaction a été corrigée en « gouvernance des données », sans perte de sens.

### Q9 — Outils : exécuté contre cité
- **Verdict : OK.** **DuckDB 1.5.5**, **pandas** et **Excel** sont **exécutés** ; **Power BI** et les
  tableurs d'entreprise sont **cités, jamais exécutés** (règle §1.5), et la fiche le déclare comme le fait
  la fiche M11 pour PostgreSQL et SQL Server.
- **Preuve :** `m12_outils_executes` et `m12_outils_cites` figurent dans le relevé ; aucune capture d'outil
  de restitution n'apparaît dans le module.

### Q10 — Livrables du plan présents
- **Verdict : OK.** Les **25** livrables du plan existent sous leur nom exact : **6** chapitres, le projet,
  l'évaluation, la fiche, le plan, le PDF, les **2** figures, les instruments (`tools/dossier_M12.py`,
  `tools/kpi_M12.py`, `tools/figures_M12.py`), le dossier complet (**10** fichiers), et les documents
  d'état (`README.md`, `05_livrables/etat_avancement.md`, `05_livrables/journal_pushs.md`).
- **Preuve :** contrôle d'existence nommée par `ls`, un nom par ligne, exécuté avant ce document (PATCH_6).

## 3. Nuances déclarées

1. **L'outil de restitution est cité, pas exécuté.** Power BI appartient au module M14 ; M12 reste aux
   fondamentaux et le déclare deux fois (plan §6, fiche Q9).
2. **Les planches sont contrôlées par leur libellé dans le PDF.** `pypdfium2` n'étant pas installé, la
   vérification visuelle automatique passe par le texte SVG composé dans le PDF, plus le contrôle de largeur
   et de déterminisme côté production.
3. **Deux réconciliations de chiffres, assumées et publiées.** (a) l'`ATTENDU.json` du générateur portait
   **169 386 796** FCFA là où le CSV et les KPI mesurent **169 386 812** : l'écart de **16** FCFA venait de
   l'arrondi appliqué après coup au lieu d'être appliqué à la ligne écrite, défaut de la famille PATCH_15 ;
   le générateur arrondit désormais **comme le fichier**, et les trois sources concordent. (b) le libellé
   `k10_premier_magasin` désignait le premier magasin de la liste alphabétique par ville ; il désigne
   maintenant le premier magasin **du réseau** (Ouaga 2000, **34,1 %**), la part de marché interne étant
   mesurée là où elle existe vraiment (Ouagadougou : **60,8 %** / **39,2 %**) — leçon PATCH_17.
4. **La devise du fil rouge est conservée.** Le module raisonne en francs CFA, comme M01 à M11 ; la note
   d'échelle du manuel (**0,4 M€** = **260 000** FCFA ; **0,8 €** pour **5 M€**) figure dans C01 et permet
   la transposition.

## 4. Synthèse

| Contrôle | Verdict | Preuve principale |
|---|---|---|
| Q1 plan | OK | plan poussé n° **46**, avant socle et rédaction |
| Q2 socle | OK | régénération **0,70** s, écart **0**, `fe5b6bfc5eb74cd8` |
| Q3 chiffres | OK | **255** clés `m12_*`, `diff` = **0** entre deux relevés |
| Q4 gabarit | OK | **16** blocs × **6** chapitres, encadrés conformes |
| Q5 exercices | OK | R5 au vert, corrigés présents (dont quiz **15** Q) |
| Q6 budget | OK | **82** p. pour **92**, soit **−10,9 %** |
| Q7 typographie | OK | **31/31** glyphes, **0** U+2013, **2/2** figures |
| Q8 anglicismes | OK | couples français — anglais, y compris *pipeline* |
| Q9 outils | OK | DuckDB/pandas/Excel exécutés, Power BI cité |
| Q10 livrables | OK | **25** livrables nommés, contrôle `ls` passé |

**Verdict de la porte : 10/10 au vert.** Le module M12 est validé pour publication — **6** chapitres,
**35 712** mots, **82** pages, **255** valeurs publiées et recalculées, le document signature du manuel
(la carte de définition de **10** KPI) prêt à être réutilisé par M13, M14, M15 et M21.
