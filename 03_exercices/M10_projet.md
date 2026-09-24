# Projet M10.P — « La refonte »

**Module M10 · projet noté sur 20 · seuil 13 · durée imposée 4 h (chronomètre en marche) ·
rendu : 4 livrables.**

> **Ce que le projet évalue.** Non pas « le plus beau graphique », mais **la refonte mesurée** :
> vous recevez un rapport dont **les chiffres sont justes** et dont les **5 graphiques** font lire
> autre chose que ce que les données disent. Vous devez **nommer** chaque défaut, **mesurer** l'écart
> qu'il crée, **corriger** la figure — puis **prouver** que votre correction n'a pas touché à la
> donnée. La règle du projet est la règle du module : **une refonte qui change un chiffre est
> rejetée** ; les totaux avant/après sont contrôlés automatiquement par
> `tools/controle_refonte_M10.py`, en **4** couches.

---

## 1. Énoncé

### Le matériel

| Élément | Chemin | Ce que c'est |
|---|---|---|
| Le rapport à refondre | `03_exercices/dossier_M10/rapport_avant/` | **5** graphiques publiés (`g1_axe_tronque.svg` … `g5_log_surcharge.svg`) + `code_avant.py` qui les produit |
| Les 2 pages du rapport | `03_exercices/dossier_M10/rapport_avant/rapport_avant.md` | ce que la direction en a retenu — les affirmations à vérifier |
| Le brief | `03_exercices/dossier_M10/00_brief.md` | la commande, en une page |
| Les 5 corrigés (à ne pas lire avant) | `03_exercices/dossier_M10/rapport_apres/` | `g1_corrige.svg` … `g5_corrige.svg` + `code_apres.py` |
| Les mesures de référence | `03_exercices/dossier_M10/ATTENDU.json` | les défauts et leurs mesures (`d1_*` à `d5_*`) — **à comparer à vos mesures, jamais à recopier** |
| Le contrôle automatique | `tools/controle_refonte_M10.py` | vérifie la règle des totaux identiques, couche par couche |
| Les 7 chapitres | `02_modules/M10_C01…C07` | perception, table des 16 graphiques, couleurs, écriture, les 10 erreurs, la séquence, les outils |
| Référence des chiffres | `01_socle_donnees/data/reference/chiffres_cites.json` | clés `m10p_*` : tout chiffre publié dans ce projet vient de là |

### La règle du projet : les totaux avant/après sont identiques

C'est **le** point du barème qui élimine. Un candidat qui « améliore » la courbe en lissant, qui
retire les retours « pour nettoyer », ou qui regroupe des catégories pour rendre un camembert
lisible, change la donnée — et la refonte est rejetée, même si la figure est plus belle.
Sur le fil rouge, les totaux de contrôle sont : **7 876 320 164,91** FCFA de CA net, **50 008**
ventes dont **208** retours, **1 044** ventes de plus de 500 000 FCFA, une médiane de
**119 482** FCFA. Le contrôle recalcule ces valeurs depuis le socle (il ne les recopie pas) et
vérifie que la somme par catégorie et la somme par trimestre retombent sur le même total net,
à **0,00** FCFA près.

### Les 4 livrables et ce qu'ils notent

| # | Livrable | Ce que ça mobilise | Points |
|---|---|---|---|
| **P1** | **Le diagnostic des 5 défauts** : pour chaque graphique, le défaut **nommé** (liste du C05), **mesuré** (l'écart entre ce que l'œil lit et ce que les données disent), et la **décision fausse** qu'il ferait prendre | C05 | /5 |
| **P2** | **Les 5 graphiques corrigés** : le bon graphique pour la question, titre qui affirme, axe honnête, annotation du chiffre clé, couleur justifiée | C01—C04 | /6 |
| **P3** | **Les deux versions du constat** : direction (1 écran, l'idée et la décision) et équipe opérationnelle (le détail, les libellés exacts) — **sans contradiction de chiffres** entre les deux | C06 | /5 |
| **P4** | **La grille visuelle en 18 points, auto-évaluée**, puis revue par un pair : deux notes, et l'écart commenté | la grille du module | /4 |
| | **Total** | | **/20** |
| | **Seuil de validation** | | **13/20** |

## 2. Grille de notation détaillée (/20)

| Livrable | Détail | Points |
|---|---|---|
| **P1** | Les **5** défauts **nommés** (axe tronqué, double axe, camembert surchargé, cumul à 100 %, échelle log surprise) ; chacun avec **sa mesure** (pas un adjectif) ; la décision fausse rédigée en une phrase ; et la mention de la **déclaration** qui rendrait l'usage légitime — ou la raison pour laquelle aucune ne suffit | /5 |
| **P2** | Les **5** figures corrigées : titre qui **affirme** (il porte un chiffre), axe à zéro **ou** troncature déclarée, annotation du chiffre clé, couleur justifiée (une couleur, un rôle), ordre trié quand il s'agit d'un classement ; largeur ≤ **776** px (format du module) | /6 |
| **P3** | **2** versions : direction (1 écran, la hiérarchie met l'idée principale en tête) et équipe (le détail, les libellés, les ordres de grandeur) ; **aucun** chiffre contradictoire entre les deux versions (le contrôle compare les totaux déclarés) | /5 |
| **P4** | La grille en **18** points remplie par l'auteur, les **4** familles notées (décision servie, justesse, lisibilité, utilisation), puis la note du pair ; l'écart entre les deux notes est **commenté** (l'écart non commenté ne rapporte pas) | /4 |
| **Total** | | **/20** |

**Les 4 points qui se perdent le plus souvent** (et la mesure qui les contrôle) :

1. **Le diagnostic sans mesure** : « l'axe est tronqué » ne vaut pas un point ; « l'axe occupe
   82,4 % de sa hauteur pour une variation réelle de 5,4 %, soit une amplitude apparente × 7,0 »
   en vaut trois. Le contrôle relit d'ailleurs les **titres dans le code**, pas dans l'image (un
   SVG de matplotlib ne contient pas de texte).
2. **La correction qui change la question** : remplacer un camembert à 8 parts par un camembert à
   4 parts ne change pas la question, seulement la gêne. Passer à des barres triées **la change** —
   et c'est légitime si la question est un classement (C01).
3. **Le double axe conservé** « pour ne pas refaire la figure » : c'est un échec de la couche L4
   (le contrôle refuse tout `twinx` dans la version corrigée).
4. **Les deux versions qui ne disent pas la même chose** : 3 965,4 M d'un côté, 3 969 M de l'autre.
   Un écart de 4 M FCFA entre la note de direction et le tableau d'équipe décrédibilise l'analyse
   entière — le contrôle compare les totaux déclarés et refuse l'écart.

## 3. Corrigé-type (sorties réelles, exécutées dans l'atelier)

### 3.1 Le contrôle automatique, sur le dossier de référence

```text
$ python3 tools/controle_refonte_M10.py
==============================================================================
CONTROLE DE REFONTE — M10.P « La refonte »
==============================================================================
  dossier      : 03_exercices/dossier_M10
  regle        : totaux avant/apres identiques et conformes au socle
  seuil        : 13/20
------------------------------------------------------------------------------
  L1_filtres_avant                   = 1
  L1_filtres_apres                   = 1
  L1_filtres_identiques              = True
  L2_total_net_egal_categories       = True
  L2_total_net_egal_trimestres       = True
  L2_ecart_categories_fcfa           = 0.0
  L2_ecart_trimestres_fcfa           = 0.0
  L3_avant_svg                       = 5
  L3_apres_svg                       = 5
  L3_largeur_max_px                  = 768
  L3_largeur_limite_px               = 776
  L4_titres_avant                    = 5
  L4_titres_apres                    = 6
  L4_titres_qui_affirment_avant      = 0
  L4_titres_qui_affirment_apres      = 6
  L4_twinx_avant                     = 1
  L4_twinx_apres                     = 0
  L4_set_yscale_log_avant            = 1
  L4_set_yscale_log_apres            = 0
  L4_annotations_apres               = 1
------------------------------------------------------------------------------
  VERDICT      : CONFORME
==============================================================================
```

Ce que ces lignes disent, en clair : la version corrigée **lit la même source** (mêmes fichiers,
mêmes filtres), elle **retombe sur les mêmes totaux** (écart **0,00** FCFA sur la somme par
catégorie comme sur la somme par trimestre), ses **5** figures tiennent dans le format
(**768** px au maximum, sous la limite de **776**), et son **écriture** est vérifiée **dans le
code** : **6** titres qui affirment sur **6**, plus aucun `twinx`, plus aucune échelle
logarithmique non déclarée, une annotation du chiffre clé. Les titres « avant » portaient une
mesure **0** fois sur 5.

### 3.2 Le contrôle sur une copie falsifiée (le cas qui doit être rejeté)

```text
$ python3 tools/controle_refonte_M10.py --candidat /tmp/cand_ko --code /tmp/cand_ko/code_refonte.py
------------------------------------------------------------------------------
  AVERTISSEMENT : L3 : 0 graphique(s) d'origine sur 5
  ECHEC         : L2 : la règle du projet est violée — les totaux avant/après diffèrent :
                  {'total_net_fcfa': (7876320164.91, 8012103456.12)}
------------------------------------------------------------------------------
  VERDICT      : REJETÉE
==============================================================================
```

La copie avait pourtant des figures correctes, dans le bon format. Elle a **« amélioré » le CA de
136 M FCFA** en refaisant les graphiques : c'est exactement ce que le projet refuse. Le contrôle
n'a pas jugé le style : il a comparé deux nombres.

### 3.3 Le contenu attendu du livrable P1, ligne par ligne

| Graphique | Défaut (C05) | La mesure | La décision fausse possible |
|---|---|---|---|
| `g1_axe_tronque` | n° 1, axe tronqué | fenêtre 300-350 M : **82,4 %** de hauteur occupée pour une variation réelle de **5,4 %** → amplitude apparente **× 7,0** | « l'activité s'envole, réorganisons l'équipe » |
| `g2_double_axe` | n° 2, double axe | corrélation **affichée** r = **+0,35** entre le CA et les retours (4 à 16 retours par mois, **24** mois) | « les retours suivent l'activité : il faut renforcer les contrôles les mois de pointe » |
| `g3_camembert` | n° 4, camembert surchargé | **8** parts, écart minimal **0,05** pt = **0,17°** ; lisible jusqu'à **3** parts | « voici notre classement de catégories » sur des parts indiscernables |
| `g4_cumul_pourcent` | n° 5, cumul de pourcentages | totaux trimestriels de **960 721 755** à **1 012 518 068** FCFA (**5,4 %**) masqués par des parts qui ne bougent que de **1,9** point | « le mix est stable, rien à faire » |
| `g5_log_surcharge` | n° 10, échelle log surprise | la masse (**77,0 %** des ventes sous 250 000 FCFA) occupe **42,1 %** de la largeur en linéaire et **93,5 %** en log ; la queue (**1 044** ventes) passe de **15,9 %** à **1,3 %** | « les montants sont homogènes » : la queue, qui porte **7,1 %** du CA, disparaît |

### 3.4 Ce qu'un livrable P2 conforme contient

Pour chaque figure : **un** titre qui affirme (il contient un chiffre), l'axe déclaré, **une**
annotation, une couleur par rôle, et l'ordre adapté à la question. Les cinq corrections du dossier
de référence, à comparer aux vôtres : axe à zéro + annotation « la moyenne glissante reste entre
**320** et **337** M » ; deux petits multiples (une échelle chacun) avec la corrélation annoncée
dans le titre ; barres **triées** avec les valeurs absolues écrites ; volumes **absolus** par
trimestre avec la ligne de moyenne ; histogramme **linéaire annoncé** et **zoom séparé** sur la
queue.

## 4. Les contrôles de fiabilité (rappel et vérification)

| Contrôle | Comment il se fait | Ce qu'il attrape |
|---|---|---|
| **Totaux identiques** | `tools/controle_refonte_M10.py`, couche **L2** : comparaison des totaux déclarés et des sommes par catégorie et par trimestre | une refonte qui change la donnée (lissage, filtre, regroupement) |
| **Même source** | couche **L1** : les deux versions lisent les mêmes fichiers avec les mêmes filtres | un « nettoyage » silencieux des retours |
| **Format** | couche **L3** : **5 + 5** SVG, largeur ≤ **776** px | une figure qui ne rentre pas dans la page composée |
| **Écriture** | couche **L4** : audit **du code** — titres, axes, `twinx`, échelle log, annotations | une figure « corrigée » qui garde son défaut structurel |
| **Grille en 18 points** | **P4**, auto-évaluation puis relecture par un pair | l'écart entre ce que l'auteur croit avoir fait et ce qu'un lecteur voit |

> **Le réflexe du module, à garder après ce projet.** Avant de publier une figure, une seule
> question : *« qu'est-ce que quelqu'un pourrait dire de faux devant ce graphique ? »* Si la phrase
> existe, la figure n'est pas prête — soit on la corrige, soit on **écrit la déclaration** qui rend
> la phrase impossible (C05).

## 5. Comment rendre

| Fichier | Contenu attendu |
|---|---|
| `rapport_apres/g1_corrige.svg` … `g5_corrige.svg` | les 5 figures corrigées, au format du module |
| `code_refonte.py` | le script qui produit les 5 figures (facultatif : sans lui, les couches L1 et L4 sont déclarées non vérifiables) |
| `refonte.json` | `{"totaux_avant": {…}, "totaux_apres": {…}}` : les totaux que vous avez mesurés dans les deux versions (les clés du socle : `total_net_fcfa`, `ventes`, `retours`, `mediane_fcfa`, `queue_plus_500k`) |
| `diagnostic.md` | le livrable P1, sous forme de tableau (graphique, défaut, mesure, décision fausse, déclaration) |
| `versions/` | les deux versions de P3 : un dossier par version, avec la figure et son titre |
| `grille.md` | la grille en **18** points remplie deux fois (auteur, pair) et l'écart commenté |

**Ce qui n'est pas accepté** : une refonte sans mesure, une correction qui change un total, une
figure dont le titre n'affirme rien, deux versions qui se contredisent, et un dossier dont les
figures dépassent la largeur du format.
