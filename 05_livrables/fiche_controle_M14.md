# Fiche de contrôle — module M14 (Power BI : de l'import à la publication)

**Porte de validation §G.1 de l'architecture (contrôles Q1 à Q10) · passée le 25 septembre 2026 ·
10/10 au vert, zéro écart bloquant, cinq nuances déclarées en fin de fiche (temps d'exécution
volatiles ; contrôle du PDF limité aux glyphes et aux libellés de planches ; budget estimé par les mots
d'un côté et lu dans le PDF de l'autre ; planches écrites sans accents ; outil non installable, donc
gestes documentés et non exécutés).**

Cette fiche documente la livraison du module M14 — *Power BI : de l'import à la publication* — huit
chapitres (N4, 30 h) qui transforment un modèle de **14** tables en un tableau de bord publié, avec
**11** mesures, **3** pages, **14** visuels, **4** signets, **6** rôles de sécurité et un dossier de
mise en production. Chaque ligne donne la commande exécutée et ce qu'elle a rendu.

## 1. Les commandes de contrôle, et leur sortie réelle

| Commande | Sortie obtenue le 25 septembre 2026 |
|---|---|
| `python3 01_socle_donnees/scripts/autovalide.py M14 --strict` | `Résultat : OK (0 avertissement(s))` sur **10** fichiers (C01 à C08 + projet + évaluation) |
| `python3 01_socle_donnees/scripts/chiffres_manuel.py M14` | **277** clés `m14_*` — dont C01 (licences et prix) **24** · C02 **17** · C03 **18** · C04 **20** · C05 **25** · C06 **37** · C07 **34** · C08 **26** · import **12** · valeurs du rapport **19** · grille **6** · évaluation **8** ; **3 003** clés au total pour le manuel |
| `python3 tools/mesures_M14.py` | **12** sections (écosystème, poids, modes, requêtes, contrôle croisé, modèle, DAX, visuels, filtres, publication, évaluation, grille, dossier) ; le contrôle croisé des **8** appariements M12 rend `0` écart ; les **12** valeurs du rapport sont identiques à celles du dossier |
| `python3 tools/dossier_M14.py --verifier` | `7` pièces sur `7` présentes : `modele_powerbi.md`, `retours_comite.md`, `rapport_avant.md`, `grille_conception_M14.md`, `connexion.py`, `modele_import/LISEZ_MOI.md`, `ATTENDU.json` |
| `python3 tools/figures_M14.py` | **4** planches produites, **4/4** citées par leur chapitre : C01 **609** px · C02 **609** px · C04 **638** px · C08 **681** px (limite **776**), **0** défaut de jeu de caractères, empreinte déterministe `3841e32e46d8d13c` |
| `python3 tools/render.py "0[234]_*/M14_*.md" --join --out 05_livrables/M14.pdf` | PDF rendu : `05_livrables/M14.pdf` · **844 Ko** · **116 pages** (**10** fichiers joints + couverture + sommaire), **22** signets |
| `python3 tools/controle_pdf.py M14` | `M14 : 116 pages · figures : 4/4 vérifiées dans le PDF par leur libellé propre · glyphes : 28/28 composés · Défauts bloquants : 0` |
| `python3 tools/budget_pages.py --mesure` | `mesure M14 : 10 fichiers · 52 649 mots · budget 117 p. · estimé 115 p. d'après les mots ; 13,1 p./chapitre (calibre 12,5)` — module composé **116 p.** pour **117 p.** (**− 0,9 %**, fourchette **[99, 135]**) |
| `python3 tools/poids.py` | `atelier : 125,3 Mo persistés sur 128 · 415 fichiers · marge +2,7 Mo` — dont **8,3 Mo** de source éditable ; le dossier M14 pèse **56 Ko** |
| `python3 -c "from pypdf import PdfReader; print(len(PdfReader('05_livrables/M14.pdf').pages))"` | `116` — confirme le contrôleur |

**Le verdict le plus fort du module.** Le mandat du premier projet exige « trois pages, quatorze
visuels, quatre segments, une page d'aide — et je veux pouvoir dire, pour chaque visuel, à quelle
décision il sert ». Ces exigences ne sont pas des intentions : le dossier du module les **mesure** —
**14** visuels répartis en **5 + 5 + 4**, **11** mesures dont **8** fonctions DAX, **6** rôles de
sécurité testés par compte, et un taux de rupture publié avec son périmètre (**7,29 %** avec le dépôt,
**6,03 %** à périmètre égal).

## 2. Les dix contrôles Q1 à Q10

### Q1 — Plan posé avant rédaction

Le plan du module est poussé avant le premier chapitre (n° **82**), le socle et le dossier sept jours
plus tard (n° **83**), puis les huit chapitres un par un (n° **84** à **90**). Le plan annonçait **8**
chapitres, **4** planches, **2** projets, une évaluation de **80** points et une grille enrichie de **6**
sous-questions : les quatre sont livrés, sans dérive de périmètre. La seule correction du plan porte sur
le compte des mesures — **10** lignes annoncées contre **11** mesurées —, tranchée en faveur de la mesure
au chapitre C04.

### Q2 — Socle reproductible et déclaré

Le socle n'est pas régénéré par ce module : il est **consommé** depuis M13, par `connexion.py`
(**3** `dirname`), et le module en déclare les exceptions là où elles comptent — la table de stock sans
magasin, le dépôt sans vente, les **2** relations inactives, les **7** cases vides de la matrice. Le
dossier M14 est régénérable : `dossier_M14.py --verifier` confirme ses **7** pièces, et `ATTENDU.json`
porte les **12** valeurs du rapport et les **15** compteurs du module, contrôlés contre l'instrument.

### Q3 — Chiffres sourcés dans le relevé

**277** clés `m14_*` pour **3 003** clés au total. Aucun nombre de quatre chiffres ou plus n'est écrit
sans exister sous la même graphie dans `chiffres_cites.json` : `--strict` est muet sur les **10**
fichiers. Les deux corrections de chiffres du module ont été faites dans le sens de la mesure : le piège
`annee_mois` du chapitre C04 — facteur **30,44** et non **44,0** —, et le facteur de stockage de la
marge du chapitre C05 — **1 558,4** —, tous deux retrouvés par l'instrument puis réécrits.

### Q4 — Gabarit des chapitres

Les **8** chapitres portent les **16** sections du gabarit, dans l'ordre, avec la ligne **Outils** en
tête et la déclaration §1.5. Les encadrés sont conformes à R8 dans les huit chapitres : **4** à **5**
« Définition », **2** « À retenir », **2** « Attention », **1** « Conseil professionnel », **1** à **2**
« Dans les faits », et l'encadré « Boîte à outils » là où une sous-section parle d'outil.

### Q5 — Exercices et corrigés

**41** exercices dans les huit chapitres — **5** par chapitre, **6** au chapitre C04 — et **41** reprises
au corrigé : **82** entêtes, aucun orphelin. Le projet ajoute **8** livrables (**4** pour P1, **4** pour
P2) et l'évaluation **4** exercices notés plus **15** questions de quiz. Aucun énoncé du module ne
reformule un énoncé d'un autre module.

### Q6 — Budget de pages respecté

**116** pages pour **117** attendues, soit **− 0,9 %**, dans la fourchette **[99, 135]** — le module le
plus proche de son budget depuis M07. Les **8** chapitres pèsent **52 030** mots, le projet **1 733** et
l'évaluation **3 536**, pour **57 399** mots au total. La lecture du PDF fait foi : `budget_pages.py`
estime **115** pages par les mots, `pypdf` en compte **116**.

### Q7 — Typographie et glyphes

**0** tiret demi-cadratin U+2013 dans les **10** fichiers, les **4** planches, l'instrument et le relevé ;
**28/28** glyphes composés dans le PDF ; **4/4** planches vérifiées par leur libellé propre ; les **4**
planches restent sous la limite de **776** px (maximum **681**). Les planches écrivent sans accents, par
contrainte de jeu de caractères, et les chapitres sont accentués normalement.

### Q8 — Anglicismes appariés

Les termes de la liste de contrôle employés par le module — *dashboard*, *drill*, *tooltip*,
*row-level security*, *workspace* — sont tous appariés à leur français dans le glossaire du module ou
dans le chapitre qui les introduit : « tableau de bord », « exploration », « info-bulle », « sécurité au
niveau des lignes », « espace de travail ». `--strict` ne relève aucun couple manquant.

### Q9 — Outils : exécuté contre cité

**DuckDB 1.5.5 est exécuté** : toutes les mesures des huit chapitres viennent de `mesures_M14.py`, y
compris les temps d'exécution (médianes de sept exécutions) et le scénario du total doublé. **Power BI
Desktop, le Service et Fabric sont cités** et non installés — la règle §1.5 est déclarée en tête de
chaque chapitre, et aucun geste de l'outil n'est présenté comme exécuté. **pandas** est disponible et non
requis.

### Q10 — Livrables du plan présents

Les pièces nommées du plan sont sur le dépôt : **8** chapitres, **1** projet à deux volets
(`03_exercices/M14_projet.md`), **1** évaluation (`04_evaluations/M14_evaluation.md`), **4** planches,
**1** dossier d'accompagnement à **7** pièces, **1** instrument (`tools/mesures_M14.py`), **1**
générateur de planches, **1** PDF de **116** pages et la présente fiche. `A_PRODURE` est vide : les
quatre planches annoncées sont produites.

## 3. Nuances déclarées

1. **Les temps d'exécution sont volatils, et cités comme tels.** Les clés `m14_c07_temps_*` et
   `m14_c07_temps_source_ms` changent d'une exécution à l'autre (**143** puis **150** ms pour la
   relecture du fichier source, **3** à **4** ms pour un panier filtré). Le chapitre C07 les cite comme
   des **médianes de sept exécutions**, et le relevé a été régénéré avant le push du chapitre.
2. **Le contrôle du PDF ne lit pas la prose.** `controle_pdf.py` vérifie la pagination, la présence des
   figures par leur libellé et la composition des glyphes ; il ne relit pas le texte. La relecture
   humaine a porté sur les **10** fichiers avant push.
3. **Le budget est estimé deux fois, et les deux lectures diffèrent d'une page.** Les mots donnent
   **115** pages, le PDF en compte **116** ; c'est le chiffre du PDF qui est retenu, lu par `pypdf`.
4. **Les planches s'écrivent sans accents.** Le jeu de caractères est latin-1 : les quatre planches
   écrivent `decision`, `lisibilite`, `modele`, pour rester extractibles du PDF composé.
5. **L'outil n'est pas installable, et le module ne le simule pas.** Aucune capture d'écran, aucun faux
   bouton : les gestes sont documentés pas à pas, et ce qui se mesure l'est en SQL — les onze mesures, le
   coût de stockage, les deux côtés d'un taux, la sécurité ligne à ligne, la taille du modèle face à la
   limite de licence.

## 4. Synthèse

| Contrôle | Verdict | Preuve la plus courte |
|---|---|---|
| Q1 plan | OK | plan n° **82**, socle n° **83**, huit chapitres poussés un par un (n° **84** à **90**) |
| Q2 socle | OK | `dossier_M14.py --verifier` : **7** pièces sur **7**, **12** valeurs et **15** compteurs |
| Q3 chiffres | OK | **277** clés `m14_*`, `--strict` muet sur **10** fichiers |
| Q4 gabarit | OK | **16** sections et les encadrés R8 dans les **8** chapitres |
| Q5 exercices | OK | **41** exercices, **41** repris au corrigé, **0** orphelin |
| Q6 budget | OK | **116** p. pour **117**, soit **− 0,9 %**, dans **[99, 135]** |
| Q7 typographie | OK | **0** U+2013, **28/28** glyphes, **4/4** figures, maximum **681** px |
| Q8 anglicismes | OK | aucun terme de la liste sans couple français |
| Q9 outils | OK | DuckDB **exécuté**, Power BI Desktop, Service et Fabric **cités** (§1.5) |
| Q10 livrables | OK | les pièces nommées du plan présentes, `A_PRODURE` vide |

**Verdict du module : 10/10 au vert, 0 écart bloquant, 5 nuances déclarées.** M14 est le premier module
de la phase 4 à tenir son budget à moins d'un pour cent près, tout en portant le dossier
d'accompagnement le plus complet du manuel (**7** pièces) et une grille de conception enrichie sans
changement de total. Il laisse M15 une frontière écrite — `ALL`, les fonctions temporelles, les
itérateurs —, ce qui est la meilleure façon de ne pas déborder sur le module suivant.
