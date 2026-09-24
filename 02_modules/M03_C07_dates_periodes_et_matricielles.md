# Module M03.C07 — Dates, durées, périodes, puis les fonctions matricielles : `FIN.MOIS`, `NB.JOURS.OUVRES`, `FILTRE`, `TRIERPAR`, `LET`

**Outil de ce chapitre : le tableur seul, sur le classeur de l'atelier.** Durée indicative : 4 h. Niveau : N2.

> **L'idée du chapitre.** Une date n'est pas un texte qui ressemble à une date : c'est **un nombre de jours**, et
> toute l'analyse temporelle sort de là. Ce chapitre fait trois choses dans cet ordre : apprendre à lire les dates
> que le fichier contient (une colonne en contient trois sortes), construire les bornes de période sans jamais
> taper un jour au clavier, puis — parce que le calendrier une fois posé il faut le parcourir — les fonctions
> matricielles qui renvoient un tableau au lieu d'une cellule, avec la **règle de la fiche double** : chaque geste
> est écrit deux fois, une fois dans la voie moderne, une fois dans la voie que tout le monde peut relire.

> **Base de travail.** Le classeur `01_socle_donnees/data/projection/m03_classeur_atelier.xlsx` : `ventes` (le
> tableau `TableVentes`, 480 lignes, dates typées), `ventes_brutes` (le fichier reçu, dates en texte), `Mensuel`
> (la grille de 12 mois que ce chapitre démonte pierre par pierre) et les fiches 24, 25 et 28 de `Calculs`.
> Séparateur point-virgule, UTF-8, franc CFA (FCFA), virgule décimale, TVA 18 %. Chiffres cités :
> `01_socle_donnees/data/reference/chiffres_cites.md`, section M03. Copie de travail : `calendrier_atelier`.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous saurez :

1. **Distinguer** la date-série (un nombre), la date-texte et l'heure, et diagnostiquer une colonne qui mélange les
   trois — 424 dates en format international, 65 en `JJ/MM/AAAA` dans le fichier reçu, 36 groupes là où il y a 12 mois.
2. **Écrire** les bornes de période sans littéral : `DATE(2025;n;1)`, `FIN.MOIS`, `MOIS.DECALER`, et la borne
   haute exclusive qui ne double-compte pas le 1ᵉʳ du mois suivant.
3. **Calculer** des durées : `DATEDIF` et ses six unités, `NB.JOURS.OUVRES` et ses jours fériés, `SERIE.JOUR.OUVRE`
   pour projeter une échéance.
4. **Nommer le dénominateur temporel** de tout ratio : 240 jours ouvrés ou 336 jours courus ne donnent pas le même
   chiffre, et aucun des deux n'est une moyenne de vente.
5. **Lire et écrire** `FILTRE`, `UNIQUE`, `TRIER`, `TRIERPAR`, `SEQUENCE`, `LET`, et prévoir `#PROPAGATION!`.
6. **Appliquer la fiche double** : une voie moderne, une voie Excel 2021 / LibreOffice, et savoir laquelle mettre
   dans le classeur livré.

---

## 2. Pourquoi cette notion est importante

Le trimestre dernier, un tableau de bord annonçait « 27,9 % de l'objectif atteint en décembre ». C'était faux deux
fois : le pourcentage était celui de **quatre jours de vente** rapportés à un mois complet — l'extrait de l'atelier
ne contient que les jours 1 à 4 de chaque mois, 256 lignes au 1ᵉ, 163 au 2, 55 au 3, 6 au 4 — et le dénominateur,
lui, était mensuel. Personne n'a vérifié l'échelle, parce que le nombre avait l'air raisonnable.

Trois raisons de prendre le calendrier au sérieux :

1. **Le temps est le seul axe que toutes les demandes contiennent.** « Par mois », « en glissant sur trois mois »,
   « en jours ouvrés », « depuis le début de l'année » : quatre questions, quatre écritures, et une seule
   (la première) se code sans réflexion.
2. **Les dates sont le type le plus fréquemment raté à l'import.** Le module C02 l'a montré pour les montants ;
   pour les dates le défaut est pire, parce qu'une date-texte se trie alphabétiquement sans rien afficher, et se
   groupe en 36 classes là où il y a 12 mois.
3. **Les fonctions dynamiques ont changé ce qu'on peut exiger d'une feuille** — et un classeur qui n'utilise
   qu'elles est un classeur que la moitié de l'entreprise ne pourra pas rouvrir.

---

## 3. Explication simple

Dans un tableur, une date est un compteur de jours. `01/01/1900` porte le numéro 1, `02/01/1900` le numéro 2 ; une
date de 2025 est donc un nombre de l'ordre de 45 000. Le format `JJ/MM/AAAA` n'est qu'un habillement :
c'est ce qui rend `=B2+1` possible (le lendemain), et ce qui rend `=MOIS(B2)` impossible si `B2` contient le
**texte** `01/01/2025`. L'heure est la partie décimale du même nombre : 0,5 vaut midi.

Une période, c'est deux bornes. La règle qui évite tous les débats : **inclusif en bas, exclusif en haut**.
Janvier 2025 = « à partir du 1ᵉʳ janvier, avant le 1ᵉʳ février ». On ne touche jamais au dernier jour du mois,
donc on ne se demande plus s'il a 28, 29, 30 ou 31 jours.

Les fonctions matricielles dynamiques, elles, répondent à une autre limite : une formule ne peut-elle rendre
qu'une cellule ? Non. `=FILTRE(…)` rend un tableau de 12 lignes qui se **propage** (l'anglais *spill*) dans les
cellules d'à côté. Si la place est prise, Excel dit `#PROPAGATION!` — c'est la nouvelle erreur à connaître, et sa
correction est toujours la même : libérer la zone.

> **Dans les faits.** Dans un fichier d'atelier comme dans beaucoup de exports d'ERP, la colonne date contient
> deux écritures : le format international `AAAA-MM-JJ` pour la plupart des lignes, le format local `JJ/MM/AAAA`
> pour les autres — 424 et 65 ici. Le tableur ne devine pas : il prend ce qu'on lui donne, et une partie de la
> colonne reste du texte. Le premier réflexe du chapitre est donc un compteur, pas une formule de calcul.

---

## 4. Vocabulaire essentiel

| Français — English | Définition simple | Piège à éviter |
|---|---|---|
| **Série de dates — date serial** | Le nombre de jours depuis l'origine du tableur. | Comparer une série à du texte : la condition ne matche pas. |
| **Système 1904 — 1904 date system** | Origine alternative (Mac ancien) : même affichage, numéros décalés de `1 462` jours. | Ouvrir un fichier 1904 et recopier des nombres bruts. |
| **Borne exclusive — exclusive bound** | `<DATE(2025;2;1)` plutôt que `<=FIN.MOIS(...)`. | Traiter février 2024 sans le 29 par un `<=28`. |
| **Jour ouvré — business day** | Lundi à vendredi, sauf jours fériés listés. | Oublier le troisième argument et appeler ça « jours travaillés ». |
| **Glissement — rolling window** | Moyenne sur les n dernières périodes. | Moyenne des trois premiers mois étiquetée « glissante » en janvier. |
| **Propagation — spill** | Le déploiement d'un résultat multi-cellules dans la grille. | Écrire une formule dynamique **dans** un tableau structuré : non pris en charge. |
| **`#PROPAGATION!` — #SPILL!** | La zone d'arrivée est occupée. | Croire que la formule est fausse : c'est la place qui manque. |
| **Plage propagée — spill range** | La référence `F2#` désigne tout le bloc. | Recopier le résultat au lieu de le référencer. |

> **Définition.** Une **période ancrée** est une période définie par une formule qui la recalcule
> (`=DATE(ANNEE(AUJOURDHUI());1;1)`), par opposition à une période tapée à la main (`>=01/01/2025`). Une feuille
> vivante n'a aucune date littérale dans ses critères.

> **Définition.** Une **fonction matricielle dynamique** est une fonction dont le résultat est un tableau de taille
> variable : `FILTRE`, `UNIQUE`, `TRIER`, `TRIERPAR`, `SEQUENCE`, `TABLEAU.ALEA`. Elle existe en Microsoft 365,
> Excel 2021 et 2024, et dans LibreOffice Calc depuis la version 24.8 — mais Calc ne propage pas : il faut
> pré-allouer la plage et valider en `Ctrl` + `Maj` + `Entrée`.

> **Définition.** `LET(nom1;valeur1;…;calcul)` attache des noms intermédiaires dans une formule. Ce n'est pas du
> confort : une plage nommée **localement** n'est évaluée qu'une fois, donc la formule se relit sans se
> redémontrer, et le tableur ne repart pas la calculer trois fois.

> **Définition.** Un **décalage d'échelle** est l'écart entre la période mesurée et la période dénominateur. Le
> ratio de l'atelier (18,2 % de l'objectif annuel) compare quatre jours par mois à douze mois : il mesure un extrait,
> pas une performance.

---

## 5. Cours approfondi

![Le calendrier de l'extrait, et les deux voies pour le calculer](../figures/M03_C07_dates_periodes.svg)

### 5.1 Lire ce que la colonne date contient vraiment

Avant toute formule de période, trois compteurs sur la colonne :

| Contrôle | Formule | Attendu sur `ventes` | Attendu sur `ventes_brutes` |
|---|---|---|---|
| les dates typées | `=NB(TableVentes[date])` | 480 | 0 |
| les valeurs non typées | `=NBVAL(ventes_brutes!B2:B490)-NB(ventes_brutes!B2:B490)` | — | 489 |
| l'amplitude réelle | `=MAX(date)-MIN(date)` | 335 jours | 0 : rien à sommer |
| les bornes | `=MIN(date)` et `=MAX(date)` | 01/01/2025 · 02/12/2025 | idem, en texte |

Le premier point qui surprend : `=MAX(ventes_brutes!B2:B490)` rend 0, pas `#VALEUR!` — sur une plage de texte, les
agrégats numériques rendent 0 (le chapitre C05 l'a établi pour les montants, la leçon est identique ici). Le second
: dans le fichier reçu, la date est **texte** pour 424 lignes au format international et pour 65 lignes au format
`JJ/MM/AAAA` ; aucune n'est une série. Grouper dessus produit `m03_groupes_texte_pour_12_mois` = 36 classes au lieu
de 12, parce que la chaîne `15/03/2025` et la chaîne `2025-03-15` ne sont pas le même texte.

Le nettoyage, en une formule par ligne : `=DATEVAL(SUPPRESPACE(B2))` fait le travail quand le texte est dans **le
format reconnu par le système**, et c'est le point sensible : `DATEVAL` lit `2025-03-15` partout, mais
`15/03/2025` seulement si vos paramètres régionaux placent le jour en premier. La voie robuste passe par le
découpage, comme au chapitre précédent : `=DATE(CNUM(STXT(B2;7;4));CNUM(STXT(B2;4;2));CNUM(STXT(B2;1;2)))` pour un
`JJ/MM/AAAA`, et les mêmes positions décalées pour l'écriture internationale. Écrivez les deux, comparez les
sommes : si les deux rendent la même date, la colonne est saine.

> **À retenir.** `=MOIS(B2)` sur une date texte ne rend pas une erreur de format, il rend `#VALEUR!` — et
> `=NB.SI(colonne;Mois5)` ne rend rien du tout. Le seul contrôle qui ferme la question est `=NB(colonne)` : 480 si
> la colonne est typée, 0 si elle ne l'est pas.

### 5.2 Extraire le temps : la famille qui lit dans la série

| Fonction | Syntaxe FR | Ce qu'elle rend sur le 15/03/2025 |
|---|---|---|
| `ANNEE` / `MOIS` / `JOUR` | `=MOIS(B2)` | 2025 · 3 · 15 |
| `JOURSEM` (WEEKDAY) | `=JOURSEM(B2;2)` | 6 — le 15/03/2025 est un samedi, lundi = 1 |
| `NO.SEMAINE` (WEEKNUM) | `=NO.SEMAINE(B2;2)` | 11 — semaine de l'année, semaines luso-isolées |
| `NO.SEMAINE.ISO` | `=NO.SEMAINE.ISO(B2)` | 11 — la norme européenne, à préférer en reporting |
| `HEURE` / `MINUTE` | `=HEURE(C2)` | sur la colonne `heure` de l'atelier |
| `TEXTE` | `=TEXTE(B2;"aaaam-mmm")` | « 2025-mar » — l'étiquette de regroupement |

Les types de `JOURSEM` et `NO.SEMAINE` méritent la ligne de note dans la fiche : sans deuxième argument,
`JOURSEM` compte **dimanche = 1**, ce qui place le dimanche dans le premier jour de la semaine et le week-end de
l'entreprise à cheval sur deux bornes. Avec `2`, lundi = 1 et le test du week-end devient `=JOURSEM(B2;2)>5`. Sur
l'extrait, ce test attrape 91 lignes du samedi et 32 du dimanche, soit 123 lignes sur 480 — 25,6 % du fichier, mais `9 730 140` FCFA
sur 36 073 185, soit 27,0 % du chiffre d'affaires. C'est une information de calendrier, pas une anomalie : mais
elle interdit d'appeler « CA par jour travaillé » un chiffre calculé sur les seuls jours ouvrés, comme on le verra
en §5.4.

Le regroupement mensuel propre ne passe **pas** par `MOIS` seule : `=MOIS(B2)` rend 3 pour mars 2025 comme pour
mars 2024, et une colonne qui perd l'année est une colonne qui agrége deux années sans prévenir. Trois écritures,
dans l'ordre de préférence :

1. `=FIN.MOIS(B2;-1)+1` — **le premier jour du mois** de la ligne, en nombre, donc triable, comparables, joignable ;
2. `=DATE(ANNEE(B2);MOIS(B2);1)` — le même résultat, plus lisible pour un non-initié ;
3. `=TEXTE(B2;"AAAA-MM")` — l'étiquette pour le titre de colonne, jamais pour la jointure (c'est du texte).

La première a ma préférence parce qu'elle survit aux années : `FIN.MOIS` connaît les mois de 28, 29, 30 et 31
jours, `DATE(…;MOIS(…)+1;1)` aussi, mais `=B2-JOUR(B2)+1` (l'écriture « arithmétique » qu'on voit partout) casse
sur février bissextile et mérite d'être bannie d'un manuel.

### 5.3 Bornes, durées, `DATEDIF`

Les trois fonctions de bornes, avec leur usage dans le classeur :

- `FIN.MOIS(dates;mois)` renvoie le dernier jour du mois décalé de `mois` — le second argument **accepte le
  nombre de mois, pas de jours**, ce qui le rend supérieur à tout ajout arithmétique : `=FIN.MOIS(A2;0)` est la fin
  du mois courant, `=FIN.MOIS(A2;1)` celle du suivant. La feuille `Mensuel` s'en sert comme borne haute.
- `MOIS.DECALER(dates;mois)` (`EDATE`) décale d'un même jour de mois en mois, en écrasant les jours inexistants :
  `=MOIS.DECALER(DATE(2025;1;31);1)` rend le 28 février 2025, pas le 3 mars — comportement juste pour une échéance,
  piégeux pour un anniversaire.
- `DATEDIF(début;fin;unité)` calcule un âge. Les six unités : `Y` années complètes, `M` mois complets, `D` jours,
  `MD` jours restants après le dernier mois complet, `YM` mois restants après la dernière année, `YD` jours
  restants hors années complètes. Sur l'extrait, `=DATEDIF(MIN(TableVentes[date]);MAX(TableVentes[date]);"m")` rend
  11 mois et l'amplitude est de 335 jours — deux réponses également justes à « quelle durée couvre le fichier ? »,
  et c'est la raison pour laquelle on cite l'unité dans le commentaire.

Une bizarrerie assumée : `DATE` normalise les arguments hors plage. `=DATE(2025;13;1)` est le 1ᵉʳ janvier **2026**,
`=DATE(2025;1;32)` le 1ᵉʳ février, `=DATE(2025;n;0)` le dernier jour du mois précédent. La feuille `Mensuel` en
profite avec élégance : sa borne haute s'écrit `DATE(2025;$A2+1;1)` pour le mois 12 aussi, sans test d'année
suivante. Retenez l'inverse aussi : pour une année, écrivez `DATE(2025;1;0)` et non `DATE(2024;12;31)` — le
premier dit « fin de 2024 » sans connaître le calendrier.

Attention aux deux chiffres : la règle documentée de `DATE` est que si l'année est comprise entre 0 et 1899, Excel
ajoute cette valeur à 1900 — `=DATE(108;1;2)` renvoie le 2 janvier 2008. Un `=DATE(GAUCHE(A2;2);…)` qui lit « 25 »
dans un ticket tombe donc en 1925, silencieusement. Écrivez quatre chiffres, toujours.

### 5.4 `NB.JOURS.OUVRES` : le dénominateur du temps travaillé

`=NB.JOURS.OUVRES(début;fin;[fériés])` compte les lundis à vendredis de l'intervalle, **bornes incluses**. Fiche 24
du classeur : `=NB.JOURS.OUVRES(DATE(2025;1;1);DATE(2025;12;2))` → 240. Trois choses à savoir :

1. Sans troisième argument, **aucun jour férié n'est retiré**. Le chiffre s'appelle alors « jours de semaine », pas
   « jours travaillés ». Dans l'atelier, c'est exact — il n'y a pas de table de fériés — mais un fichier de
   l'entreprise en porte une, et l'oublier gonfle le dénominateur d'une quinzaine de jours par an, soit environ 6 %
   de sur- ou sous-évaluation du rythme quotidien selon le sens du ratio.
2. Le troisième argument accepte une plage de dates **ou une plage nommée** ; mettez la liste des fériés dans une
   feuille `Calendrier` et nommez-la `Jours_fériés`, sinon chaque année il faudra réécrire les douze formules.
3. `SERIE.JOUR.OUVRE(date;n;[fériés])` est l'inverse : il projette l'échéance `n` jours ouvrés plus loin, et c'est
   ce qu'on attend pour une date de livraison, pas `=date+n`.

À quelle sauce le dénominateur change le récit ? Le chiffre d'affaires de l'extrait est de 36 073 185 FCFA :

| Dénominateur | Nombre | CA par unité |
|---|---|---|
| lignes de vente | 480 | 75 152 FCFA |
| tickets | 316 | 114 156 FCFA |
| jours ouvrés (lun→ven, 01/01→02/12) | 240 | 150 305 FCFA |
| jours calendaires courus | 336 | 107 361 FCFA |
| mois couverts | 12 | 3 006 099 FCFA |

Quatre nombres justes. Un rapport qui en cite un sans dire lequel est invérifiable — et le quatrième, celui qui
semble le plus « naturel », est le seul qui ignore que 123 lignes sont tombées un samedi ou un dimanche.
`AUJOURDHUI()` et `MAINTENANT()` complètent le jeu : la première ne rend **rien d'autre** qu'un numéro de jour
courant (et change à chaque ouverture, donc ne la mettez jamais dans une cellule de contrôle attendue), la seconde
porte la partie décimale de l'heure.

> **Attention.** Un ratio temporel recalculé avec `AUJOURDHUI()` dans le dénominateur change de valeur tout seul
> entre la livraison et la réunion. Deux règles : les feuilles de contrôle figent la borne (`=DATE(2025;12;31)`)
> et la date d'arrêté est écrite dans une cellule nommée, consultée par les formules, jamais recopiée dans
> chacune.

### 5.5 La grille mensuelle de l'atelier, démontée

La feuille `Mensuel` est un modèle du genre, et elle tient en six formules répétées douze fois. Colonne A : le
numéro de mois (1 à 12). Les autres :

```
B2  =SOMME.SI.ENS(ventes!M2:M481;ventes!B2:B481;">="&DATE(2025;$A2;1);ventes!B2:B481;"<"&DATE(2025;$A2+1;1))
C2  =NB.SI.ENS(ventes!B2:B481;">="&DATE(2025;$A2;1);ventes!B2:B481;"<"&DATE(2025;$A2+1;1))
D2  =SOMME.SI.ENS(objectifs!E2:E219;objectifs!A2:A219;5;objectifs!B2:B219;2025;objectifs!C2:C219;$A2)
E2  =SIERREUR(B2/D2;"objectif absent")
F2  =NB.JOURS.OUVRES(DATE(2025;$A2;1);FIN.MOIS(DATE(2025;$A2;1);0))
```

Quatre décisions de style valent le détour, et ce sont les vôtres à partir de maintenant :

- **la borne haute est exclusive** (`"<"&DATE(2025;$A2+1;1)`) : aucun 31/01 oublié, aucun 01/02 compté deux fois,
  et le mois 12 ne demande pas de trait d'esprit puisque `DATE(2025;13;1)` est janvier 2026 ;
- **le critère est construit, jamais tapé** : la concaténation `">="&DATE(...)` produit le nombre au bon format,
  alors que le littéral `">=01/01/2025"` dépend des réglages régionaux du poste ;
- **`SIERREUR` encadre le ratio, pas la somme** : une division par un objectif absent donne « objectif absent »,
  tandis qu'un CA manquant doit rester visible ;
- **les jours ouvrés sont dans la grille** (colonne F, 20 à 23 selon les mois, 240 au total sur la période de
  l'extrait) : le ratio `B/F` est calculable en un glisser, et c'est le seul chiffre de la feuille qui se compare
  d'un mois à l'autre sans biais de longueur.

### 5.6 Lisser : la moyenne glissante, et ce qu'elle cache

Sur les douze CA mensuels (`1 258 801` FCFA au plus bas en mai, `5 292 517` au plus haut en décembre — un rapport de
4,2 entre les deux, ce qui rend la lecture ligne à ligne impossible), la moyenne glissante sur trois mois s'écrit
en `C4` de la copie de la grille, étirée vers le bas :

| mois | CA mensuel | lignes | ouvrés | CA par jour ouvré | glissant 3 mois |
|---|---|---|---|---|---|
| 1 | 2 051 424 | 40 | 23 | `89 192` | — |
| 5 | 1 258 801 | 40 | 22 | `57 218` | 2 540 138 |
| 10 | 2 808 078 | 40 | 23 | `122 090` | 3 106 116 |
| 12 | 5 292 517 | 40 | 23 | `230 109` | 3 627 210 |

Trois remarques qui valent plus que la formule. Un : les deux premiers mois n'ont pas de glissante —
`=MOYENNE(B2:B4)` en `C2` avale les cases vides et rend une moyenne sur un ou deux mois étiquetée « trois mois » ;
le garde-fou est `=SI(NB(B2:B4)=3;MOYENNE(B2:B4);"")`. Deux : la glissante **ne corrige pas l'échelle** — ici elle
lisserait douze mois construits sur quatre jours chacun, ce qui est une régularité d'échantillon, pas de saison ;
le commentaire à écrire dans la feuille est celui du classeur lui-même : l'extrait ne couvre que les jours 1 à 4
de chaque mois, donc aucun ratio mensuel de ce fichier ne mesure une performance annuelle. Trois : sur un vrai
fichier, on lisse en **jours ouvrés** et non en lignes, sinon un mois de 23 jours ouvrés semble battre un mois de
20 jours de 15 % sans avoir rien vendu de plus.

### 5.7 Les fonctions dynamiques, en fiches doubles

Cinq fonctions, chacune avec son écriture accessible. La règle du classeur : la voie du milieu est **dans les
cellules**, la voie moderne **en commentaire de note**, sauf dans un classeur dont vous contrôlez la distribution.

| Tâche | voie moderne (365 · 2021 · 2024 · LibreOffice 24.8+) | voie accessible (tous, y compris 2019) |
|---|---|---|
| les lignes d'un mois | `=FILTRE(TableVentes!A2:M481;MOIS(TableVentes!B2:B481)=12;"aucune ligne")` | un filtre sur la colonne `mois` de la §5.2, ou `=SOMME.SI.ENS` si seul le total intéresse |
| les valeurs présentes | `=UNIQUE(TableVentes[categorie])` | `=JOINDRE.TEXTE(", ";VRAI;…)` de la fiche 23, ou une colonne triée-puis-dédupliquée |
| le top 5 par CA | `=TRIER(FILTRE(…);3;-1;VRAI)` | `=GRANDE.VALEUR` ×5 sur la grille par catégorie, ou le tri d'un TCD (chapitre C08) |
| un calendrier de 12 lignes | `=DATE(2025;SEQUENCE(12);1)` | douze cellules recopiées, `=A2+1` interdit : `=DATE(2025;MOIS(A2)+1;1)` |
| trier par une autre colonne | `=TRIERPAR(plage;TableVentes[montant_ttc];-1)` | la colonne utilitaire `rang` + un tri manuel, consigné |
| éviter de tout répéter | `=LET(ca;SOMME.SI.ENS(…);nb;NB.SI.ENS(…);ca/nb)` | une ligne d'aide dans la grille, et la division en colonne séparée |

Deux contraintes d'environnement, toutes deux documentées par l'aide de Microsoft, à connaître avant d'écrire :
une formule à propagation **ne peut pas vivre dans un tableau structuré** — chez vous, `TableVentes` est un
tableau : écrivez `FILTRE`/`UNIQUE` dans la grille libre à côté, jamais dans une colonne du tableau ; et si la zone
d'arrivée est occupée — y compris par des cellules fusionnées ou une mise en forme résiduelle — Excel rend
`#PROPAGATION!`. La correction n'est pas une réécriture : c'est un ménage. Enfin, la référence `=F2#` (le dièse de
plage propagée) est le moyen propre de chaîner un `FILTRE` vers un `=SOMME` ; elle n'existe ni en 2019 ni dans
Calc, ce qui est la vraie raison d'écrire la voie du milieu en regard.

> **Attention.** Ces deux contraintes vont dans la fiche d'en-tête du classeur, pas dans la légende du graphique :
> les dynamiques exigent Microsoft 365, Excel 2021 ou 2024 (en 2019 : `#NOM?` cellule par cellule), et LibreOffice
> les connaît depuis 24.8 sans les propager — plage pré-allouée, validation en `Ctrl` + `Maj` + `Entrée`.

`LET` mérite un mot, parce qu'on le sous-estime : dans la voie « ca/nb », il **nomme** les deux agrégats, et un
dénominateur nommé se relit et se discute — sans même parler des recalculs évités.

> **Conseil professionnel.** Écrivez la voie moderne dans une feuille de bac à sable, vérifiez qu'elle rend bien le
> même nombre que la voie accessible sur les douze mois, puis livrez l'accessible et gardez la moderne en note. Le
> gain de temps est à vous, le risque de `#NOM?` ne l'est pas.

### 5.8 Cinq fiches de fonction du chapitre

Format du module : nom et version · syntaxe · arguments · exemple sur le jeu de l'atelier · cas réel · erreur
fréquente et symptôme. Version abrégée ici, la fiche complète étant à rédiger dans votre classeur.

| Fonction | Version | Exemple sur l'atelier | Erreur fréquente, symptôme |
|---|---|---|---|
| `FIN.MOIS` (`EOMONTH`) | toutes | `=FIN.MOIS(DATE(2025;2;1);0)` → 28/02/2025 | le résultat est un nombre : sans format date, la cellule affiche 45716 |
| `MOIS.DECALER` (`EDATE`) | toutes | `=MOIS.DECALER(A2;3)` | confondre avec `+3` : l'un décale de 3 mois, l'autre de 3 jours |
| `DATEDIF` | toutes (non listée dans l'assistant) | `=DATEDIF(MIN(date);MAX(date);"m")` → 11 | unité `M` vs nombre de mois civils : 11 contre 12, selon les bornes |
| `NB.JOURS.OUVRES` (`NETWORKDAYS`) | 2010+ | fiche 24 → 240 | troisième argument oublié : les fériés comptent comme travaillés |
| `FILTRE` | 365 · 2021 · 2024 · LO 24.8+ | 40 lignes de décembre en une formule | écrit dans le tableau structuré, ou zone occupée → `#PROPAGATION!` |

---

## 6. Exemple concret : le décembre qui écrasait les autres

Décembre affiche 5 292 517 FCFA, le plus haut des douze mois, contre 1 258 801 en mai. Le commentaire du
tableau de bord, écrit par quelqu'un qui n'avait pas lu ce chapitre : « +320 % en décembre, effet fêtes ». Deux
vérifications démontent la phrase.

La première est de longueur : les jours ouvrés vont de 20 à 23 selon le mois, décembre en compte 23, mai 22. En
CA par jour ouvré, décembre passe de `230 109` à comparer à `57 218` pour mai — l'écart reste massif (×4), mais il
n'est plus de 320 % : il est de 302 %. L'effet de longueur était réel et minime ; la mention du dénominateur, elle,
est passée d'aucune à obligatoire.

La seconde est d'échelle : dans ce fichier, un mois, c'est quatre jours. Le ratio au objectif de décembre (27,9 %
contre 14,1 % en octobre) ne dit pas que le magasin a fait 28 % de son mois en une semaine — il dit que
l'échantillon de quatre jours de décembre pèse ce poids-là. La note du classeur `Mensuel` le dit elle-même, et
c'est la seule fois du manuel où je vous demande de recopier une phrase d'un fichier : elle est courte, et elle est
exacte. Le vrai écart se lit à l'échelle de la population entière, où le rapport CA/objectif s'étage de 1,62 à
3,27 selon le magasin-mois.

Ce qu'il fallait produire, et ce que produit la §7 : une colonne de jours ouvrés, un ratio sur ce dénominateur, et
une ligne d'échelle (« extrait : jours 1 à 4 de chaque mois ») sous le titre du graphique.

---

## 7. Démonstration pas à pas : la grille de rythme mensuel

**Objectif.** Une feuille `Rythme` qui, pour les douze mois, rend CA, lignes, jours ouvrés, CA par jour ouvré, et
la glissante à trois mois — dans la voie accessible, avec la voie moderne en vis-à-vis.

| Étape | Formule | Ce qui doit se lire |
|---|---|---|
| 1 | `=DATE(2025;SEQUENCE(12);1)` en `A2` (hors tableau, à gauche de la zone libre) | 12 premiers du mois, de janvier à décembre 2025 |
| 2 | `=DATE(ANNEE($A2);MOIS($A2);1)` en `A2`, recopiée | même colonne, voie 2019 : la comparaison des deux est le contrôle |
| 3 | `=SOMME.SI.ENS(TableVentes[montant_ttc];TableVentes[date];">="&$A2;TableVentes[date];"<"&FIN.MOIS($A2;0)+1)` | douze CA, dont 2 051 424 en janvier ; la somme = 36 073 185 FCFA |
| 4 | `=NB.JOURS.OUVRES($A2;FIN.MOIS($A2;0))` | 20 à 23, total 261 sur l'année pleine |
| 5 | `=SI(B2>0;B2/D2;"")` | un rythme par mois, aucun `#DIV/0!` |
| 6 | `=SI(NB(B2:B4)=3;MOYENNE(B2:B4);"")` | deux cellules vides, dix glissantes |

**Contrôles qualité du chapitre.** (1) La colonne A est une série de dates, pas du texte : `=NB(Rythme!A2:A13)` → 12.
(2) L'étape 3 ferme sur le total du tableau, ni plus ni moins : 36 073 185 FCFA. (3) Le total des jours ouvrés de la
colonne D vaut 261 pour l'année, et 240 pour la période réellement couverte par l'extrait (fiche 24) — les deux
nombres sont justes, ils ne répondent pas à la même question, et c'est le commentaire qui tranche. (4) Les douze
CA mensuels recopiés à côté de `m03_ca_par_mois` se religne-à-religne à l'unité près.

**Barème de la démonstration (10 points).** Colonnes A doublées voie moderne/accessible et concordantes (2) ·
bornes exclusives aux douze lignes (2) · jours ouvrés et rythme calculés (3) · glissante gardée-foutie (1) ·
note d'échelle « quatre jours par mois » écrite sous le titre (2).

---

## 8. Erreurs fréquentes

1. **Compter sur `=NB(colonne date)` sans l'avoir fait.** Une date texte n'est pas une date : 489 lignes en texte
   rendent 0, et `=MOIS(…)` rend `#VALEUR!` sur la moitié de la colonne sans que le tri n'avertisse.
2. **Comparer à un littéral de date.** `">=01/01/2025"` dépend du poste, et `=B2="01/01/2025"` est une comparaison de
   texte : la même donnée, deux réponses selon la machine. Construire, toujours : `">="&DATE(2025;1;1)`.
3. **Oublier le 29 février.** Un `<=FIN.MOIS()` écrit à la main sur février rend 2024 orphelin de son dernier jour ;
   `MOIS.DECALER` et la borne exclusive ne connaissent pas ce problème.
4. **Appeler « jours travaillés » un `NB.JOURS.OUVRES` sans fériés.** Le troisième argument n'est pas optionnel en
   entreprise, il est optionnel en syntaxe.
5. **Retirer le week-end du dénominateur en gardant les ventes du week-end.** 123 lignes sur 480 sont tombées un
   samedi ou un dimanche : diviser le CA total par les seuls jours ouvrés produit un rythme surévalué d'autant.
6. **Moyenne glissante sans garde-fou.** `=MOYENNE(B2:B4)` en haut de la colonne rend un chiffre sur deux points :
   `SI(NB(…)=3;…)` est la ligne qui manque.
7. **Écrire une formule dynamique dans le tableau structuré.** Elle ne se propage pas, et le message est
   `#PROPAGATION!` là où l'on cherchait une erreur de formule.
8. **Livrer un classeur 365 à une salle en 2019.** `FILTRE`, `UNIQUE`, `TRIERPAR` rendent `#NOM?` cellule par
   cellule : la fiche double n'est pas une politesse, c'est une assurance.
9. **Figer une période avec `AUJOURDHUI()` dans une cellule de contrôle.** Le contrôle change d'attendu tous les
   matins ; la borne d'arrêté se nomme, elle ne se devine pas.

---

## 9. Bonnes pratiques professionnelles

1. **Une feuille `Calendrier`** avec une ligne par jour de la période analysée : date, mois, mois-étiquette,
   numéro de semaine ISO, jour ouvré, jour férié. C'est la table qui rend toutes les autres simples, et elle
   s'écrit en une `SEQUENCE` en trente secondes.
2. **Jamais de date littérale dans un critère.** Une cellule `!Calendrier!B2` nommée `Debut_periode`, et les
   formules qui la pointent.
3. **Toujours le dénominateur temporel écrit à côté du ratio** : « CA par jour ouvré », pas « CA moyen ».
4. **Glissante et brut côte à côte**, jamais l'une pour masquer l'autre ; le graphique montre les deux courbes.
5. **La voie accessible dans les cellules livrées**, la voie moderne en note et dans votre feuille de bac à sable.
6. **Un contrôle de fermeture temporelle** : la somme des CA mensuels égale le CA du tableau, et le total des
   lignes par mois égale 480. En dessous de cette égalité, aucune analyse de saisonnalité n'est présentable.
7. **Format date explicite** partout où une formule a arithmétiquement touché une date : `FIN.MOIS` rend un
   numéro, et un numéro de série dans un commentaire de graphique fait fuir un comité.

---

## 10. Exercice guidé — la grille de rythme (40 min, /10)

**Commande.** Construisez `Rythme` en partant de zéro, dans les deux voies, et joignez-y le ratio à l'objectif.

| Étape | Geste | Ce qui doit se lire |
|---|---|---|
| 1 | 12 premiers de mois, `SEQUENCE` puis voie 2019 | douze premiers de mois identiques, à un jour près : zéro écart |
| 2 | CA mensuel par `SOMME.SI.ENS` à bornes `$A2` / `FIN.MOIS($A2;0)+1` | douze nombres, total 36 073 185 FCFA |
| 3 | Jours ouvrés par mois | 20 à 23, total annuel 261 |
| 4 | CA par jour ouvré, et son ratio à l'objectif (`objectifs` sur `magasin × mois`) | douze ratios ; décembre en tête |
| 5 | Glissante 3 mois avec garde-fou | deux vides en tête, dix valeurs |
| 6 | `FILTRE` des lignes de décembre **hors tableau**, et son `=SOMME` chaîné par `#` | 40 lignes, même total qu'à l'étape 2 |

**Démarrage.** À l'étape 1, ne recopiez pas les dates : la colonne doit venir d'une formule, sinon le jour où le
périmètre change en janvier 2026 vous aurez douze lignes à retaper et une à oublier. À l'étape 4, le ratio à
l'objectif se fait par `SOMME.SI.ENS` sur `objectifs` (magasin 5, année 2025, mois = `MOIS($A2)`) et non par
`RECHERCHEX` sur une clé texte : la clé de la table d'objectifs est `annee_mois`, fabriquée au chapitre C06, et
`MOIS($A2)` rend un nombre — si vous préférez joindre sur la clé, fabriquez-la des deux côtés avec `TEXTE`, ou
la jointure ne matchera pas : `MOIS($A2)` est un nombre, la clé est une chaîne. À l'étape 6, déplacez le point d'insertion **à droite du tableau** : dans une colonne de
`TableVentes`, la propagation est refusée, et vous perdrez dix minutes à croire que `FILTRE` est cassé.

**Barème (10 points).** Deux voies concordantes démontrées (3) · bornes exclusives et critères construits (2) ·
jours ouvrés et ratio justes (2) · glissante avec garde-fou (1) · `FILTRE` hors tableau et total chaîné identique (1) ·
note d'échelle de l'extrait (1).

---

## 11. Exercices autonomes

**Exercice 7.1 (★) — Le recensement de colonne.** Sur `ventes_brutes` puis sur `ventes`, comptez les dates typées,
les dates en texte, les deux formats textuels distincts, et l'amplitude rendue par `MAX-MIN` dans chaque cas.
Concluez : que vaut `=MAX(ventes_brutes!B2:B490)` et pourquoi ce n'est pas une erreur.

**Exercice 7.2 (★) — Le week-end dans le dénominateur.** Calculez le CA par jour ouvré (a) en divisant le CA total
par les 240 jours ouvrés, (b) en retirant d'abord les 123 lignes de week-end puis en divisant par 240. Donnez les
deux nombres, l'écart en pourcentage, et la phrase qui dit lequel des deux répond à « combien vend-on par jour de
travail », compte tenu du fait que ces 123 lignes ne sont pas marginales.

**Exercice 7.3 (★★) — Le calendrier en une formule.** Construisez une feuille `Calendrier` couvrant l'année 2025
avec `SEQUENCE` (voie 2019 : recopie incrémentée), puis ajoutez mois, mois-étiquette, semaine ISO, jour
ouvré et un drapeau « ouvré et dans l'extrait ». Contrôlez : le compte des ouvrés doit se raccorder aux 240 de la
fiche 24, et le total des lignes de l'extrait doit retomber sur 480 en croisant `NB.SI.ENS`.

**Exercice 7.4 (★★) — La glissante honnête.** Reprenez la grille mensuelle, calculez la glissante à trois mois
en (a) ignorant les mois incomplets, (b) en moyenne mobile **par jour ouvré**. Les deux séries ne racontent pas la
même histoire : dites laquelle conserve l'ordre des mois, et ce que l'autre invente.

**Exercice 7.5 (★★★) — `DATEDIF` aux six unités.** Sur les bornes de l'extrait, calculez `Y`, `M`, `D`, `YM`, `MD`,
`YD`, puis le nombre de mois civils couverts (`=MOIS(MAX)-MOIS(MIN)+12*(ANNEE(MAX)-ANNEE(MIN))+1`). Expliquez
pourquoi deux de ces six nombres sont également justes et inutilisables sans la mention de l'unité, et lequel
correspond au « 335 jours » de la fiche 25.

**Exercice 7.6 (★★★) — La double fiche.** Pour chacune des six tâches du tableau de §5.7, écrivez les deux voies,
vérifiez l'égalité des résultats, et consignez la version qui entre dans le classeur livré avec une ligne de
justification. Vous devez obtenir six égalités : si l'une manque, cherchez du côté de `FIN.MOIS` (nombre vs date)
et de la borne exclusive.

---

## 12. Correction détaillée

**Exercice 7.1.** `ventes` : 480 typées, 0 texte, amplitude 335 jours (nombre). `ventes_brutes` : 0 typée, 489 en
texte, dont 424 en `AAAA-MM-JJ` et 65 en `JJ/MM/AAAA`, et `MAX` rend **0** parce que le maximum d'une plage sans
nombre est 0 en l'absence d'erreur — c'est le comportement établi au chapitre C05 pour les montants, et il est ici
plus coûteux : une date à 0 s'affiche 00/01/1900, un format date caché, et l'amplitude devient une donnée fausse
au lieu d'un zéro visible.

**Exercice 7.2.** (a) 36 073 185 ÷ 240 = `150 305` FCFA par jour ouvré, week-ends compris dans le numérateur.
(b) le week-end pèse `9 730 140` FCFA ; le numérateur tombe à `26 343 045`, le rythme à `109 763` — un écart de
27,0 %, pas une nuance. Réponse attendue : « combien vend-on par jour de travail » se répond avec (b) **à condition
de retirer aussi les 104 samedis et dimanches de 2025 du dénominateur** (261 ouvrés sur l'année, mais le week-end
n'en est pas un ici) ; sinon on compare un numérateur réduit à un dénominateur inchangé. La discipline est
d'énoncer les deux dans la légende et de n'en choisir qu'un, une fois pour toutes, à l'échelle de l'entreprise.

**Exercice 7.3.** `=DATE(2025;1;1)+SEQUENCE(366)-1` (ou `=DATE(2024;12;31)+SEQUENCE(366)` si vous voulez que le
29 février 2024 soit exclu — 2025 ne l'est pas, il a 365 jours : le test utile est donc 365 lignes, pas 366, et
vérifiez le compte avant d'écrire la formule). Les contrôles qui doivent tomber : ouvrés = 261 sur l'année, 240 entre le 01/01 et le
02/12 (fiche 24) ; croisement avec l'extrait par `=NB.SI.ENS(TableVentes[date];">="&A2;TableVentes[date];"<"&A2+1)`
somme sur la colonne = 480 lignes réparties sur 31 jours distincts.

**Exercice 7.4.** (a) garde-fou `SI(NB(…)=3;…)` : deux cellules vides, dix valeurs comprises entre `1 992 788` et
`3 627 210` FCFA. (b) la glissante sur le rythme par jour ouvré déplace les pics — un mois court bien rempli passe
devant un mois long à rythme égal. Réponse attendue : la série (a) conserve l'ordre d'importance des mois mais
confond longueur et performance ; la série (b) compare ce qui est comparable mais **inventerait** une saisonnalité
si on l'appliquait à notre extrait, où chaque mois ne compte que quatre jours. D'où la règle : on ne lisse pas
pour faire joli, on lisse après avoir égalisé la longueur.

**Exercice 7.5.** `Y` = 0, `M` = 11, `D` = 335, `YM` = 11, `MD` = 1, `YD` = 335, mois civils = 12. Deux d'entre
eux répondent à « quelle durée ? » selon qu'on compte en mois **complets** (11) ou en mois **touchés** (12) —
c'est l'écart entre `DATEDIF` et le comptage par `MOIS`, et le seul remède est d'écrire l'unité dans le
commentaire. Le nombre qui correspond à la fiche 25 est `D`, 335.

**Exercice 7.6.** Les six égalités attendues : 12 mois de CA, 7 catégories listées, top 5 par CA, calendrier de
12 lignes, tri par montant, et CA moyen d'un mois. Les deux rupteurs classiques : `FIN.MOIS` sans format date (un
nombre de 45 000 dans une comparaison de texte), et la borne `<=FIN.MOIS()` qui ampute les mois de 31
jours — l'atelier écrit `<FIN.MOIS()+1`.

---

## 13. Mini-projet M03.P1 — suite : le volet calendrier (45 min)

**Commande.** Ajoutez à `calendrier_atelier` la feuille `Calendrier` et la feuille `Rythme`, et faites-les
travailler ensemble dans le tableau de bord du projet.

**Livrables numérotés.** (1) `Calendrier` : une ligne par jour de l'année couverte, avec date, mois,
mois-étiquette, semaine ISO, ouvré, férié (vide assumé, documenté) et le drapeau « dans l'extrait » ; (2) `Rythme` :
les douze mois en CA, lignes, ouvrés, CA par jour ouvré, glissante à trois mois, ratio à l'objectif, chaque colonne
portant sa voie accessible et sa voie moderne avec la cellule de contrôle d'égalité ; (3) le bloc d'échelle : trois
lignes qui disent ce que l'extrait couvre (jours 1 à 4), ce que le ratio mesure, et ce qu'il ne mesure pas ; (4) un
`FILTRE` de démonstration hors tableau, chaîné par `#` vers un total, avec sa variante `SOMME.SI.ENS` en vis-à-vis ;
(5) la fiche de fonction de `NB.JOURS.OUVRES` au format du module (six rubriques).

**Barème (20 points, seuil 13).** `Calendrier` juste et contrôlée (5) · `Rythme` en double voie avec égalités
vérifiées (6) · bloc d'échelle qui se lit sans ouvrir une formule (4) · `FILTRE` proprement chaîné (3) · fiche de
fonction complète (2).

---

## 14. Résumé du chapitre

Une date est un nombre de jours : tout ce qui suit en découle — comparer, borner, découper, moyenne. Trois gestes
 ferment la question du typage (`=NB(colonne)`, les deux formats textuels repérés par `NBCAR`, l'amplitude), un seul
ferme celle de la période : borne basse inclusive, borne haute exclusive, construites avec `DATE`/`FIN.MOIS`, jamais
tapées. Les durées se disent avec leur unité (`DATEDIF` rend 11 mois là où l'amplitude rend 335 jours, et les deux
sont vrais), et le rythme se nomme : 75 152 FCFA par ligne, 114 156 par ticket, 150 305 par jour ouvré, 107 361 par
jour couru — un chiffre sans dénominateur temporel est une opinion.

Les fonctions dynamiques changent la fabrique de la grille, pas la nature de la donnée : `FILTRE`, `UNIQUE`,
`TRIER`, `TRIERPAR`, `SEQUENCE`, `LET` sont en 365, 2021 et 2024, connues de LibreOffice 24.8 et plus sans
propagation, absentes de 2019, refusées dans un tableau structuré, et punies de `#PROPAGATION!` dès que la zone
d'arrivée est prise. La fiche double — accessible en cellules, moderne en note — est la seule politique qui rend un
classeur lisible par toute la salle.

> **À retenir.** Deux chiffres de rythme sur le même fichier : 150 305 FCFA par jour ouvré, 107 361 par jour
> couru. Aucun n'est faux, les deux sont incomplets tant que la légende ne dit pas si les 123 lignes de week-end
> sont dans le numérateur.

> **À retenir.** `=DATE(2025;$A2+1;1)` est la borne haute du mois 12 sans cas particulier : `DATE` normalise
> l'année suivante. C'est la différence entre une formule qui tient douze mois et une formule qui tient douze ans.

---

## 15. À retenir

1. **Trois compteurs avant toute analyse de période** : `=NB(colonne date)`, `=MAX-MIN`, `=NB.SI.ENS` du nombre de
   lignes par mois. S'ils ne tombent pas d'accord, ne calculatez rien.
2. **Bornes construites, jamais tapées** : `">="&DATE(2025;n;1)` et `"<"&FIN.MOIS(…;0)+1`. Le littéral dépend du
   poste, la formule dépend du calendrier — seule la seconde est la même partout.
3. **Une période doit dire son échelle.** Un extrait de quatre jours par mois rapporté à un objectif annuel est un
   taux d'échantillon, pas un taux de réalisation : écrivez-le sous le graphique, pas dans votre tête.

---

## 16. Évaluation formative (auto-correction, 10 min)

1. Une colonne date contient 489 cellules, `=NB(colonne)` rend 0, `=MAX(colonne)` rend 0. Que concluez-vous, et que
   faites-vous en premier ?
2. Écrivez les bornes de mars 2024 d'un `SOMME.SI.ENS` qui compte le 29 février de l'année d'avant et n'oublie
   aucun 31 — sans taper un seul jour en dur.
3. Pourquoi `=NB.JOURS.OUVRES(début;fin)` seul est-il un mauvais dénominateur pour un commerce ouvert le samedi, et
   que faut-il écrire à côté du chiffre ?
4. Un classeur livré contient `=FILTRE(…)` dans une colonne de `TableVentes`. Il rend `#PROPAGATION!` chez vous et
   `#NOM?` chez un collègue en 2019. Expliquez les deux messages, et corrigez les deux.
5. Le commentaire dit « glissante à trois mois » alors que la formule est `=MOYENNE(B2:B4)` recopiée depuis la
   première ligne. Quel est le défaut, et quel est le garde-fou en une formule ?

**Question ouverte.** Vous devez livrer une revue annuelle qui compare douze magasins sur des périodes de longueurs
différentes (certains ouverts en cours d'année, tous avec des jours fériés locaux distincts). Écrivez la politique
de calendrier que vous imposez : quelles colonnes dans la table de dates, quel dénominateur retenu, ce que vous
refusez d'afficher, et comment la voie accessible et la voie moderne cohabitent dans le classeur.

---

**Corrigé de l'évaluation formative.**

1. Aucune date n'est typée : la colonne est entièrement du texte (424 en `AAAA-MM-JJ`, 65 en `JJ/MM/AAAA` dans
   l'énoncé reçu). Premier geste : le compteur de conversion — une colonne utilitaire
   `=DATEVAL(SUPPRESPACE(B2))` testée sur les deux formats, puis comparaison des sommes — pas un graphique.
2. `=SOMME.SI.ENS(TableVentes[montant_ttc];TableVentes[date];">="&DATE(2024;3;1);TableVentes[date];"<"&DATE(2024;4;1))` :
   le 29 février 2024 est attrapé par le chemin précédent (borne haute exclusive sur mars), et mars 2024 a 31 jours
   — la borne `+1` sur le mois suivant n'a jamais à le savoir. Écrire `<=31/03/2024` reproduirait le problème sur
   février.
3. Parce que le numérateur contient les ventes du week-end et pas le dénominateur : le rythme est sur-évalué (ici
   de 27,0 % entre les deux écritures du calcul : `9 730 140` FCFA de ventes de week-end ne se retranchent pas en
douceur). À écrire à côté : « jours ouvrés lun→ven, fériés non retirés ; 123 lignes de week-end incluses dans le CA ».
4. `#PROPAGATION!` : la formule est dans un tableau structuré, où la propagation n'est pas prise en charge — on la
   déplace dans la grille libre à droite du tableau. `#NOM?` : la fonction n'existe pas en 2019 — on la remplace
   par la voie `SOMME.SI.ENS`/filtre, et on garde `FILTRE` en note.
5. Le défaut : en `C2` et `C3`, la moyenne porte sur deux et trois cellules dont certaines vides, donc « trois
   mois » veut dire un ou deux mois. Garde-fou : `=SI(NB(B2:B4)=3;MOYENNE(B2:B4);"")`.

**Question ouverte — attendus.** Une table de dates avec une ligne par jour, le drapeau ouvré par magasin (et non
un), la liste des fériés par site, un dénominateur unique annoncé dans le titre (« CA par jour ouvré du site »), le
refus explicite des parts de chiffre d'affaires entre magasins ouverts à des dates différentes, et la voie
accessible dans les cellules livrées.
