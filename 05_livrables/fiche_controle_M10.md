# Fiche de contrôle — module M10 (Data visualization)

**Porte de validation §G.1 de l'architecture (contrôles Q1 à Q10) · passée le 24 septembre 2026 ·
10/10 au vert, zéro écart bloquant, trois nuances déclarées en fin de fiche (largeur d'une planche du
dossier corrigée par le contrôle automatique du projet ; quota de l'atelier à la limite ; statut
déclaré des outils).**

Cette fiche documente la livraison du module M10 — *Data visualization* — sept chapitres (N3, 30 h)
qui installent la **lecture** d'un graphique avant sa production : l'ordre perceptuel, la table des
16 graphiques, les couleurs et l'accessibilité, l'écriture (titres, axes, annotations), les 10 erreurs
avec leur effet **mesuré**, la séquence de trois écrans et la sortie (matplotlib, Excel, formats).
Elle ne raconte pas les intentions : chaque ligne donne la commande exécutée et ce qu'elle a rendu.

## 1. Les commandes de contrôle, et leur sortie réelle

| Commande | Sortie obtenue le 24 septembre 2026 |
|---|---|
| `python3 01_socle_donnees/scripts/autovalide.py M10 --strict` | `Résultat : OK (0 avertissement(s))` sur **9 fichiers** (C01 à C07 + projet + évaluation) |
| `python3 01_socle_donnees/scripts/chiffres_manuel.py M10` | **325 clés** `m10_*` / `m10p_*` / `m10e_*` (27 C01 + 19 C02 + 39 C03 + 32 C04 + 51 C05 + 44 C06 + 40 C07 + 21 projet + 13 évaluation + constantes) ; 2 exécutions successives : `diff` de `chiffres_cites.json` = **0 ligne** |
| `python3 tools/dossier_M10.py` | Dossier `03_exercices/dossier_M10/` régénéré (rapport **avant** : 5 SVG + `code_avant.py` + 2 pages de rapport ; rapport **après** : 5 SVG corrigés + `code_apres.py` ; `ATTENDU.json`) ; **`diff -rq` = 0** (byte-identique avant/après) ; aucune donnée créée : le dossier **rejoue le socle M09** |
| `python3 tools/figures_M10.py` (nouveau) | **7 planches rejouées, 7/7 déterministes, 7/7 citées** par leur chapitre : 643 × 484, 748 × 605, 643 × 408, 643 × 499, 718 × 567, 718 × 673, 718 × 537 px ; largeur maximale **748 px** (limite 776) ; poids total **731,3 Ko** |
| `python3 tools/controle_refonte_M10.py` (nouveau) | Dossier de référence : **`VERDICT : CONFORME`** — L1 filtres identiques, L2 écart **0,00** FCFA (total net = somme des catégories = somme des trimestres), L3 **5 + 5** SVG et **768 px** au maximum, L4 **6/6** titres qui affirment (contre **0/5** avant), **0** `twinx`, **0** échelle log, **1** annotation |
| `python3 tools/controle_refonte_M10.py --candidat /tmp/cand_ko` (copie falsifiée) | **`VERDICT : REJETÉE`** — `ECHEC : L2 : la règle du projet est violée — les totaux avant/après diffèrent : {'total_net_fcfa': (7876320164.91, 8012103456.12)}`. La copie avait des figures conformes : elle avait « amélioré » le CA de 136 M FCFA |
| `python3 tools/render.py "02_modules/M10_*.md" --join --out 05_livrables/M10.pdf` | PDF rendu : `05_livrables/M10.pdf` · **934 Ko** · **106 pages** (7 fichiers joints + couverture + sommaire) |
| `python3 tools/nb_pages.py 05_livrables/M10.pdf` | `106 pages` — confirmé par `pypdfium2` |
| `python3 tools/controle_pdf.py M10` | `M10 : 106 pages · figures : 7/7 vérifiées dans le PDF par leur libellé propre · glyphes : 32/32 composés · Défauts bloquants : 0` |
| `python3 tools/budget_pages.py --mesure` | `mesure M10 : 9 fichiers · 54 729 mots · budget 105 p. · composé 106 p. → dérive +1 % ; 15.4 p./chapitre (calibre 12.5)` ; budget additif et conforme à l'architecture (aucune erreur sur les 22 modules) |
| `python3 tools/outils_M10.py` (Excel **exécuté**) | Classeur écrit **puis relu** : `03_exercices/dossier_M10/exports/fil_rouge.xlsx` · **7,0 Ko** · **26** lignes · 1 graphique natif · écart relu **0,00** FCFA sur **24** valeurs ; exports matplotlib PNG 96 dpi (**23,4** Ko, 604 × 340 px), PNG 300 dpi (**96,1** Ko, 1 889 × 1 062 px), SVG (**12,9** Ko, 69 points tracés), PDF (**17,3** Ko) ; deux exécutions : **fichiers identiques** (y compris le classeur, horodatage figé) |
| Croisée socle ↔ dossier (contrôle de la fiche) | **11/11** concordances exactes entre `chiffres_manuel` et `ATTENDU.json` : total net **7 876 320 164,91** · ventes **50 008** · retours **208** · médiane **119 482** · queue **1 044** · corrélation **+0,35** · fenêtre tronquée **50** M · écart minimal **0,05** pt · totaux trimestriels **960 721 755** / **1 012 518 068** · masse **77,0** % |
| `python3 tools/poids.py` | `atelier : 127,0 Mo persistés sur 128 · 319 fichiers · marge +1,0 Mo` — après suppression des **7** sorties HTML intermédiaires (47,5 Mo rendus sans perte de source) |

**Le verdict le plus fort du module.** Un module de *visualisation* ne se juge pas sur ses figures,
mais sur ce qu'il **mesure** : les **7** planches passent la recette (déterminisme, largeur, citation),
les **10** erreurs sont chiffrées avec leur effet (**× 7,0** d'amplitude apparente pour **5,4 %** réels,
corrélation **affichée +0,35**, écart de **0,17°**, **5,4 %** de totaux masqués, masse de **42,1 %**
à **93,5 %** de largeur), et le projet possède un contrôle **automatique à 4 couches** qui accepte le
dossier de référence et **rejette** une copie falsifiée de 136 M FCFA. Le chiffre du graphique ne
change pas d'un outil à l'autre : la donnée est la même, seul le fichier change.

## 2. Les dix contrôles Q1 à Q10

### Q1 — Plan posé avant rédaction
- **Verdict : OK.** `05_livrables/plan_M10.md` (n° 21) précède la rédaction : 7 chapitres C01–C07
  (30 h, N3), budget **105** pages ± 15 % → **[89, 121]**, **7** figures (une par chapitre), la table
  des **16** graphiques en §1.7, le projet « La refonte » (**4** livrables /20, seuil **13**), la grille
  en **18** points et **4** familles, et les **7** étapes de production calquées sur M05–M09.

### Q2 — Socle de données reproductible
- **Verdict : OK.** Le module **ne crée aucune donnée** : il rejoue le socle M09. `tools/dossier_M10.py`
  régénère le dossier ; **`diff -rq` = 0** entre deux exécutions (5 SVG « avant », 5 SVG « après », les
  deux copies du script, les 2 pages du rapport, `ATTENDU.json`). Empreinte du socle déclarée :
  `b9a8d973119342ec`.

### Q3 — Chiffres cités traçables
- **Verdict : OK.** **325** clés `M10` dans `01_socle_donnees/data/reference/chiffres_cites.json`
  (1 755 clés au total, 11 sections). Tous les nombres ≥ 4 chiffres publiés dans les chapitres, le
  projet et l'évaluation viennent de ces clés — tables **non exemptées** (§B.4, R2) ; deux exécutions
  successives donnent un `diff` de **0 ligne**.
- La croisée socle ↔ dossier passe **11/11** (§1) : les mesures du chapitre C05 sur les défauts sont
  exactement celles de `ATTENDU.json`.

### Q4 — `autovalide.py --strict` 0 avertissement
- **Verdict : OK.** `Résultat : OK (0 avertissement(s))` sur les **9** fichiers du module.
- Effort réel : chaque chapitre a demandé **2 à 4** encadrés supplémentaires (`Définition`,
  `À retenir`, `Attention`) pour atteindre les seuils du §B.4 — C04 : **3** ajouts ; C05 : **4** ;
  C06 : **4** ; C07 : **4**. Aucune règle n'a été contournée : les encadrés ajoutés portent du fond
  (hauteur occupée, faux citable, densité d'un écran, résolution utile).

### Q5 — Figures SVG auditées
- **Verdict : OK.** `tools/figures_M10.py` (nouveau) rejoue les **7** planches : **7/7** déterministes
  (même empreinte sha256 après deux exécutions), **7/7** dans le format (largeur maximale **748** px
  pour une limite de **776**), **7/7** citées par leur chapitre avec un chemin `../figures/`.
  Poids total **731,3 Ko**, dont **433,7** Ko pour la planche des 16 graphiques (16 panneaux).

### Q6 — PDF budget pages respecté
- **Verdict : OK.** **106** pages composées pour un budget de **105** → dérive **+1 %**, très en deçà
  de la tolérance de 15 % (**[89, 121]**). Le détail : 7 chapitres (9 fichiers au total avec le projet
  et l'évaluation), **54 729** mots, **15,4** pages par chapitre pour un calibre de 12,5.

### Q7 — `controle_pdf.py` 0 défaut bloquant
- **Verdict : OK.** Les **7** planches sont retrouvées **dans** le PDF par un libellé propre à chacune
  (preuve que la composition n'a pas perdu les figures), et **32/32** glyphes des sources sont composés.
- Le contrôle a d'abord signalé **2** glyphes absents (`È` et `–`) : la cause était dans le **projet**
  (une citation du contrôle automatique écrite en capitales, et trois tirets demi-cadratins). Corrigé :
  message de l'outil reformulé sans `È`, tirets passés au cadratin `—`, PDF recomposé → **32/32**.

### Q8 — Moteurs exécutés
- **Verdict : OK.** **matplotlib 3.10.9** et **seaborn 0.13.2** produisent les **7** planches, les
  **10** figures du dossier de projet et les **4** exports du chapitre C07 ; **Excel est exécuté** via
  `openpyxl 3.1.5` : le classeur est **écrit**, son graphique natif est relié aux cellules, puis le
  classeur est **relu** et comparé au socle (**écart 0,00** FCFA sur **24** valeurs). Le déterminisme
  a été étendu au PNG, au PDF et au **classeur** (horodatage zip et `dcterms:modified` figés).

### Q9 — Power BI cité sans exécuté
- **Verdict : OK.** Power BI est présenté en **9** clics décrits, avec la mention **« cité, non
  exécuté »** dans le chapitre C07 **et** dans le livrable du mini-projet P7 ; aucun fichier `.pbix`,
  aucune capture, aucune mesure ne lui est attribuée. C'est la règle §1.5, appliquée comme en M05
  (Power Query) et en M07 (PostgreSQL).

### Q10 — Cohérence transverse
- **Verdict : OK.** Le même chiffre partout : **3 965,4** M FCFA de CA net 2026, **+1,4 %**,
  **77,0 %** des ventes pour **47,3 %** du CA, **1 044** ventes de plus de 500 000 FCFA pour **7,1 %**
  du CA, **208** retours (**0,4 %**), médiane **119 482**, totaux trimestriels de **960 721 755** à
  **1 012 518 068**. Le projet (P1 : 5 défauts mesurés), l'évaluation (quiz, « prédisez la mesure »,
  étude de cas) et les chapitres citent **les mêmes** valeurs, servies par un **socle unique**.
  Le contrôle automatique du projet compare les totaux déclarés : écart **0,00** FCFA exigé.

## 3. Nuances déclarées

1. **Un défaut réel trouvé par le contrôle du projet (corrigé, mesuré).** `g5_corrige.svg` du dossier
   faisait **806 px** de large, au-dessus de la limite de **776** px du module : le contrôle automatique
   l'a signalé (`ECHEC : L3 : figure(s) plus large(s) que 776 px`). Correctif : `figsize` ramené de
   8,4 à **8,0** pouces dans `tools/dossier_M10.py`, dossier régénéré, **`diff -rq` = 0** à la double
   exécution, `ATTENDU.json` **inchangé** (les mesures ne dépendent pas de la taille de la figure), et
   le contrôle repasse au vert avec **768 px** au maximum. Le contrôle sert donc aussi à l'auteur du
   manuel : c'est la première fois qu'un outil de validation d'exercice trouve un défaut dans le
   matériel livré.
2. **Le quota de l'atelier est à la limite (mesuré, action prise).** `tools/poids.py` annonçait
   **165,0 Mo** persistés pour un plafond de 128 (`marge -37,0 Mo`) : les **7** sorties HTML
   intermédiaires de composition (**47,5 Mo** au total, régénérables en 20 s par `render.py`) ont été
   supprimées, ramenant l'atelier à **127,0 Mo** et **319** fichiers. Les fichiers de données du socle
   (**27,2** Mo de `ventes_brutes.csv`, **26,8** Mo de `ventes_propres.csv`) et les dossiers
   d'exercices (**13,6** Mo M05, **11,8** Mo M07, **8,0** Mo M06) sont **conservés** : ils sont cités
   par leur nom dans **35** fichiers du manuel, et le contrôle `autovalide --strict` refuse leur
   absence (`fichier cité inexistant`). Conséquence : la marge restante est de **+1,0 Mo** ; toute
   nouvelle composition doit supprimer son HTML dans le même geste (ce que le PDF M10 fait : HTML
   supprimé juste après le rendu).
3. **Statut des outils déclaré dans les livrables eux-mêmes.** Le module exécute matplotlib, seaborn
   et Excel, et **cite** Power BI. La nuance ne porte pas sur la règle mais sur sa portée : le classeur
   Excel est **écrit, relu et comparé** au socle, mais son **rendu graphique** demande l'application
   Excel, qui n'est pas ouverte dans l'atelier. Le chapitre C07 le dit en clair : le fichier est
   vérifié, la capture ne l'est pas — et aucune capture n'est publiée.

## 4. Synthèse

**10 contrôles sur 10 au vert, 0 défaut bloquant, 3 nuances déclarées.** Le module M10 est livré
complet : **7** chapitres rédigés et poussés un par un (**7** commits, n° 24 à n° 31), **7** planches
exécutées et vérifiées (748 px au maximum, 731,3 Ko, déterminisme 7/7), **325** clés de chiffres
reproductibles (diff = 0), un dossier de projet régénéré byte-identique (rapport avant / après,
`ATTENDU.json`), un PDF de **106** pages dans le budget **[89, 121]**, un projet noté sur **20**
(seuil **13**) doté d'un contrôle automatique à **4** couches — **CONFORME** sur le dossier de
référence, **REJETÉE** sur une copie falsifiée —, une évaluation de **65** points dont un quiz de
**15** questions (dont **5** « prédisez l'effet »), **10** prédictions de mesure auto-corrigées et une
étude de cas « ce graphique a déclenché une décision fausse ». La phrase-clé du module — *« une erreur
n'est pas un péché, c'est une décision : elle est légitime si elle est déclarée »* — est tenue par les
faits : **10** erreurs chiffrées, **2** qu'aucune déclaration ne sauve (la 3D, la couleur à tout
faire), et un contrôle automatique qui ne juge pas le style, mais compare **deux nombres**.
