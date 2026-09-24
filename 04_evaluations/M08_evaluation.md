# Évaluation M08 — « Python pour l'analyse de données »

**Module M08 · durée totale 3 h 10 · cinq épreuves · seuils : quiz 11/15, exercices 11/15, étude de cas 12/20, projet 13/20**

| Épreuve | Durée | Barème | Noté | Ce qui est attendu |
|---|---|---|---|---|
| A · Questions de récupération | 10 min | non noté | non | vérifier qu'on a lu les huit chapitres avant de se tromper cher |
| B · Quiz | 25 min | /15 | oui | quinze questions à réponse unique, cinq blocs, dont **5 « prédisez la sortie »** |
| C · Exercices « prédisez la sortie » | 30 min | /15 (auto-corrigé) | oui | quinze valeurs en pandas, auto-validés par `tools/controle_exos_M08.py` |
| D · Exercices à rendre + E4 | 45 min | /20 | oui | cinq scripts courts (5 × /2) + « ce script tourne mais ses chiffres sont faux » (/10) |
| E · Étude de cas — « Le script du stagiaire » | 75 min | /20, seuil 12 | oui | diagnostiquer et corriger, en commentant chaque message d'erreur |

> Le score du module se lit ainsi : **B ≥ 11** et **C ≥ 11** et **E ≥ 12** valident le
> module ; le projet M08.P doit atteindre 13/20. Un candidat qui réussit B et échoue à E
> repasse uniquement E : savoir lire un `groupby` ne dispense pas de savoir lire une
> traceback qui dit que votre nombre est faux. Tout nombre de cette évaluation est mesuré
> sur le socle livré (`03_exercices/dossier_M08/`, 8 CSV, réexport déterministe de la base
> M07 figée, empreinte dossier `b9a8d973119342ec…`) ; les corrections le citent avec leur
> clé `m08_*` / `m08p_*` dans `chiffres_cites.json`.

---

## A · Questions de récupération (non notées)

À traiter sans document, en une ou deux phrases chacune. Elles ne sont pas comptées ; elles
servent à repérer ce qui n'est pas assimilé avant de perdre des points sur un détail.

1. Citez les **4 couches** de l'environnement Python (C01), et dites ce qu'isole un
   `venv` — et pourquoi le script du projet M08.P doit tourner « sur la machine du
   collègue ».
2. Pourquoi `0.1 + 0.2` ne vaut pas `0.3` en Python (C02), et quelle est la conséquence
   pour des montants en FCFA (l'ordre des opérations de l'addition) ?
3. Quand choisir `for`, quand choisir `while` (C03) ? À quoi servent `break` et
   `continue` ?
4. Liste, tuple, dictionnaire, ensemble : lequel pour chacune de ces questions métier —
   « combien de fois », « dans quel ordre », « quelle valeur pour cette clé », « y a-t-il
   un doublon ? » (C04) ?
5. On vous donne une traceback de 30 lignes : par où commencez-vous la lecture (C05) ?
   Et quel bloc d'un `try/except/finally` s'exécute **toujours** ?
6. Pourquoi `np.where` gagne-t-il contre une boucle `for` sur 50 000 valeurs (C06) ?
   Que vaut une cellule « pas de valeur » dans un tableau NumPy ?
7. `loc` et `iloc` : qui parle en **libellés**, qui parle en **positions** (C07) ?
   Que renvoie `describe()` sur une colonne de montants ?
8. Pourquoi somme-t-on en **centimes entiers** avant de diviser (C08) ? Et pourquoi
   `resample("M")` lève-t-il une erreur sous pandas 3.x, et quelle est l'écriture vivante ?

---

## B · Quiz (15 questions · 15 points)

**Barème : 1 point par question, une seule bonne réponse. Les réponses justifiées en une
ligne rapportent un demi-point de bonus, plafonné à 15.**

### Bloc 1 — Environnement et types (C01—C02) (Q1 à Q3)

**Q1. (prédisez la sortie)** Que renvoie `print(0.1 + 0.2)` ?
a) `0.3` · b) **`0.30000000000000004`** · c) `TypeError` · d) `0.29999999999999998` arrondi à `0.3`.

**Q2.** Un environnement virtuel (`venv`) isole : a) le système d'exploitation · b) **les
paquets d'un projet (site-packages) du reste de la machine** · c) le navigateur · d) le
compte utilisateur.

**Q3.** `x = "15"` puis `x + 5` : a) renvoie `20` (conversion implicite) · b) **lève
`TypeError: unsupported operand type(s) for +: 'str' and 'int'`** · c) renvoie `"155"` ·
d) renvoie `None`.

### Bloc 2 — Contrôle du flux et conteneurs (C03—C04) (Q4 à Q6)

**Q4.** Dans une boucle `for`, `break` : a) saute une itération · b) **quitte la boucle
entièrement** · c) relance la boucle · d) est une erreur de syntaxe.

**Q5. (prédisez la sortie)** Que renvoie `print([x for x in range(1, 10) if x % 3 == 0])` ?
a) `[1, 2, 3, 4, 5, 6, 7, 8, 9]` · b) `[0, 3, 6, 9]` · c) **`[3, 6, 9]`** · d) `9`.

**Q6.** Un **dictionnaire** sert à : a) garder un ordre fixe · b) **récupérer une valeur
par clé** · c) supprimer les doublons · d) trier des nombres.

### Bloc 3 — Organiser le code (C05) (Q7 à Q9)

**Q7.** Dans un `try/except/finally`, le bloc qui s'exécute **toujours** (erreur ou non)
est : a) `try` · b) `except` · c) **`finally`** · d) aucun.

**Q8. (prédisez la sortie)**
```python
def remise(prix, pct=10):
    return prix * (1 - pct / 100)

print(remise(1500))
```
a) `1500` · b) `135.0` · c) **`1350.0`** · d) `TypeError`.

**Q9.** Une traceback se lit : a) de bas en haut, en s'arrêtant au message final · b)
**de haut en bas pour comprendre la chaîne d'appels, et la dernière ligne porte le nom de
l'erreur et la cause** · c) au hasard · d) uniquement par le code d'erreur.

### Bloc 4 — Vecteurisation et lecture (C06—C07) (Q10 à Q12)

**Q10.** `np.where(condition, a, b)` : a) lance une boucle interne · b) **construit un
tableau en choisissant `a` ou `b` élément par élément, sans boucle Python** · c) filtre
une colonne · d) trie un tableau.

**Q11.** `df.loc` et `df.iloc` : a) sont interchangeables · b) **`loc` sélectionne par
libellés (index/noms), `iloc` par positions entières** · c) `loc` ne fonctionne que sur
les entiers · d) `iloc` ne fonctionne que sur les chaînes.

**Q12. (prédisez la sortie)** Sur le socle du module, que renvoie
`pd.read_csv("03_exercices/dossier_M08/vente.csv").shape` ?
a) `(50000, 13)` · b) **`(50008, 13)`** · c) `(50008, 12)` · d) `(50000, 12)`.

### Bloc 5 — Agréger et livrer (C08) (Q13 à Q15)

**Q13.** Diviser chaque ligne en FCFA **avant** de sommer, au lieu de sommer en centimes
puis diviser : a) ne change rien · b) **perd les centimes de chaque ligne (le plus gros
mois du socle sort à 228 FCFA de son total exact)** · c) donne un résultat plus précis ·
d) lève une erreur.

**Q14. (prédisez la sortie)**
```python
v = pd.read_csv("03_exercices/dossier_M08/vente.csv")
print(v.groupby("id_magasin")["id_vente"].count().tolist())
```
a) `[9942, 9873, 10033, 10061, 10099]` · b) **`[10099, 10033, 9873, 10061, 9942]`** ·
c) `[1200, 1200, 1200, 1200, 1200]` · d) une erreur (5 magasins, 1 200 clients).

**Q15.** `v.merge(obj, on="id_magasin", how="left")` avec `obj` **vide** (0 ligne) :
a) renvoie 0 ligne · b) **renvoie 50 008 lignes avec toute la colonne `ca_objectif_ttc`
en `NaN` — un signal à lire, pas un bug** · c) lève `KeyError` · d) renvoie 50 008 lignes
complètes par duplication.

---

## C · Exercices « prédisez la sortie » (15 exercices · 15 points · auto-corrigés)

**Consigne.** Sur le dossier `03_exercices/dossier_M08/` (les 8 CSV), produire le résultat
de chaque bloc. 1 point par réponse exacte. Les 15 blocs de référence et leurs valeurs
attendues sont auto-validés par `python3 tools/controle_exos_M08.py` — exécutez-le pour
vérifier vos réponses ; il rapporte chaque valeur obtenue. Les valeurs attendues sont
mesurées sur le socle livré, jamais déduites (cf. `chiffres_cites.json`, clés
`m08_*` / `m08p_*`).

| # | Bloc (code de référence) | Résultat attendu |
|---|---|---|
| C01 | `len(v)` | **50 008** |
| C02 | `int((v["montant_ttc"] * 100).round().astype("int64").sum()) // 100` (CA brut, centimes) | **7 908 259 732** |
| C03 | `v.drop_duplicates(subset=[c for c in v.columns if c != "id_vente"]).shape[0]` | **50 000** |
| C04 | `int(v["est_retour"].sum())` | **208** |
| C05 | CA propre en centimes, retours exclus | **7 876 320 164** |
| C06 | Panier moyen, arrondi (CA brut en centimes ÷ 50 008) | **158 140** |
| C07 | CA du top magasin, en centimes | **1 596 813 264** |
| C08 | `int((pd.to_datetime(v["date_vente"]).dt.dayofweek == 6).sum())` | **7 136** |
| C09 | `v.merge(o, on="id_magasin", how="left").shape` | **`(50008, 16)`** |
| C10 | Nombre de cellules `NaN` de `ca_objectif_ttc` après ce merge | **50 008** |
| C11 | Nombre de groupes de la vue mensuelle (sans retours, magasin × année-mois) | **120** |
| C12 | Plus gros mois de la vue, en centimes | **78 965 529** |
| C13 | `int(v["date_vente"].str.startswith("2025").sum())` | **24 920** |
| C14 | `int(v["date_vente"].str.startswith("2026").sum())` | **25 088** |
| C15 | `int((v["montant_ttc"] > 100000).sum())` | **28 065** |

> **Lecture des C02/C05.** Le canon du module est l'**addition en centimes entiers** côté
> pandas : C02 = `m08p_ca_brut`, C05 = `m08p_ca_sans_retours`. Le côté SQL de la croisée
> (DuckDB, somme `float`) donne 7 908 259 731 et 7 876 320 163 — l'écart de 1 FCFA est la
> dérive mesurée et sourcée (`m08p_ecart_somme_float_*`), pas un piège d'énoncé : un
> candidat qui livre 7 908 259 731 **en le signalant** garde son point.

---

## D · Exercices à rendre (5 scripts courts · 5 × /2) + E4 « ce script tourne mais ses chiffres sont faux » (/10)

### D1 — Les deadlines impossibles (C03, C07) — /2

Filtrer les ventes dont la `date_limite_remise` tombe au **20 du mois** (les deadlines
aberrantes du socle : la remise est fixée au 15). Produire, sur 3 lignes : le nombre de
lignes en **brut**, le nombre après dédoublonnage (12 colonnes métier), et la **première**
date de vente parmi ces lignes (triées par `id_vente`).

**Sortie attendue :**
```text
18
15
2025-01-10
```
*La 3ᵉ ligne se lit « la plus ancienne vente concernée est du 10 janvier 2025 » — la date
seule ne vaut rien sans sa question.*

### D2 — La fonction des centimes (C05) — /2

Écrire `en_centimes(montant: float) -> int` qui convertit un montant en FCFA en **centimes
entiers** avec un arrondi juste (pas de troncature float). Deux tests obligatoires :
`en_centimes(0.1 + 0.2)` doit valoir **30** (et non 29 — c'est le piège
`0.1 + 0.2 = 0.30000000000000004`), et `en_centimes(15000.5)` doit valoir **1 500 050**.
Appliquer la fonction à la colonne `montant_ttc` et imprimer la somme des centimes.

**Sortie attendue (les 3 lignes) :**
```text
30
1500050
790825973220
```
*La 3ᵉ ligne : la somme des centimes du CA brut, **avant** le `// 100` — ce n'est pas
exactement 100 fois le C02 : il reste 20 centimes (`m08p_ca_brut_centimes`) qui font que
`790825973220 // 100 = 7908259732`.*

### D3 — Les 4 tranches de montants (C06) — /2

Classer les 50 008 montants en 4 tranches avec `np.where` (sans boucle) :
**50 000 et moins**, **plus de 50 000 jusqu'à 100 000**, **plus de 100 000 jusqu'à
200 000**, **plus de 200 000** FCFA, et imprimer le nombre
de ventes par tranche, dans cet ordre.

**Sortie attendue :**
```text
0-50k      12753
50-100k     9190
100-200k   12319
200k+      15746
```
*La somme des 4 effectifs redonne 50 008 — le contrôle total du C04, en tranches.*

### D4 — L'année 2025 du magasin 4 (C07) — /2

Filtrer les ventes du **magasin 4** en **2025**, **sans retours**, ajouter une colonne
`mois`, et imprimer le CA mensuel en centimes (12 lignes, mois triés). C'est l'exercice
guidé du chapitre C08 §10, à refaire de mémoire.

**Sortie attendue :**
```text
01    64948883
02    76403254
03    61294111
04    62254879
05    63589011
06    61805710
07    64979650
08    65368579
09    75836578
10    68271344
11    64272077
12    66454383
```
*Le plus fort mois est **02** (76 403 254 FCFA) ; la somme des 12 valeurs est le total
2025 du magasin 4 : 795 478 466 FCFA (`m08p_mag4_2025_total`).*

### D5 — Le classeur en deux feuilles (C08) — /2

Construire un classeur Excel avec **deux feuilles nommées** : `vue_mensuelle` (les 120
lignes de la vue M07 sans retours : `id_magasin`, `mois`, `ca_fcfa` en centimes) et
`top_magasin` (5 lignes : `id_magasin`, `ca_fcfa`). Recharger le classeur avec
`sheet_name=None` et imprimer la forme de chaque feuille.

**Sortie attendue :**
```text
{'vue_mensuelle': (120, 3), 'top_magasin': (5, 2)}
```
*Le rechargement par nom est la garantie : une feuille sans nom ne se retrouve pas.*

---

### E4 — « Ce script tourne mais ses chiffres sont faux » (/10)

Le stagiaire livre ce script. **Il s'exécute sans lever d'erreur.** Trois de ses chiffres
sont faux — localisez-les, expliquez chacun en une phrase, et corrigez.

```python
"""analyse_synthese.py (v0 du stagiaire) — résumé mensuel du mois écoulé.
Le script s'exécute sans lever d'erreur. Trois chiffres sont faux.
"""
import pandas as pd

D = "03_exercices/dossier_M08"
v = pd.read_csv(D + "/vente.csv")

# 1. Volume : combien de ventes ?
ventes = len(v)

# 2. CA propre (retours exclus), en FCFA
centimes = (v["montant_ttc"] * 100).round().astype("int64")
ca_propre = int(centimes.sum()) // 100

# 3. Panier moyen des « méga-ventes » (1 000 000 FCFA et plus)
mega = v[v["montant_ttc"] >= 1000000]
try:
    panier_mega = int(centimes[v["montant_ttc"] >= 1000000].sum()) // len(mega)
except ZeroDivisionError:
    panier_mega = 0

print("ventes =", ventes)
print("ca_propre =", ca_propre)
print("panier_mega =", panier_mega)
```

**Sortie réelle (exécutée le 20/09/2026) :**
```text
ventes = 50008
ca_propre = 7908259732
panier_mega = 0
```

| # | Ce qui est faux | Le bon chiffre | La faute (à expliquer) |
|---|---|---|---|
| 1 | `ventes = 50008` présenté comme le volume de ventes | **50 000** (`m08p_ventes_uniques`) | **doublons comptés** : le socle porte 8 doublons exacts (12 colonnes métier) — `len(v)` compte les lignes brutes, pas les ventes |
| 2 | `ca_propre = 7908259732` présenté comme le CA **propre** | **7 876 320 164** (`m08p_ca_sans_retours`) | **retours inclus** : le filtre `~v["est_retour"]` est absent — 208 retours à montant positif gonflent le CA de 31 939 568 FCFA (`m08p_ecart_ca_retours`) ; le chiffre affiché est le CA **brut** |
| 3 | `panier_mega = 0` | **l'indicateur n'existe pas** — aucune vente ≥ 1 000 000 FCFA (le montant max du socle est 594 363 FCFA, `m08p_max_montant`) | **division par zéro masquée** : `len(mega)` vaut 0, le `except ZeroDivisionError` renvoie silencieusement `0` — un « 0 » qui ressemble à un chiffre, alors que la question est vide. Remède : vérifier le dénominateur **avant** de diviser, et dire « aucune vente » au lieu d'écrire 0 |

**Barème E4 : 3 × /3** (localisation + bonne explication de chaque faute) **+ /1** pour
les trois corrections effectivement réexécutées (les 3 sorties corrigées :
`ventes = 50000`, `ca_propre = 7876320164`, `panier_mega : aucune vente ≥ 1 000 000 FCFA`).

> **L'esprit de E4.** C'est le piège le plus rare et le plus cher de tous : un script
> **sans erreur** qui **produit**. Les 8 chapitres apprennent à lire les erreurs ; E4
> apprend à se méfier des sorties qui sont trop propres.

---

## E · Étude de cas — « Le script du stagiaire » (75 min · /20, seuil 12)

**Consigne.** Le stagiaire livre `ca_magasin4_2025.py`, ci-dessous, pour produire le CA du
magasin 4 en 2025 (sans retours), mois par mois, + total de l'année + panier moyen.
Le script **échoue à l'exécution** (trois messages d'erreur, à faire apparaître les uns
après les autres en corrigeant au fil de l'eau) et **son total, quand il s'affiche, ne
correspond pas** au total attendu. Le candidat rend le script corrigé + un paragraphe par
erreur (ce qu'elle dit, pourquoi elle est là, ce qui a été changé). Barème :

| Point | Contenu | Points |
|---|---|---|
| E1 | `NameError` : identifier la variable inconnue et la cause (typo) | /4 |
| E2 | `KeyError` : identifier la colonne inexistante et la colonne juste | /4 |
| E3 | Le total qui ne correspond pas : trouver la ligne qui **ne fait rien** (l'affectation sur la vue) et expliquer pourquoi le filtre retours n'a pas eu d'effet | /6 |
| E4 | Les sorties corrigées : les 12 valeurs mensuelles, le total 795 478 466 FCFA, le panier 157 426 FCFA | /4 |
| E5 | Qualité : un paragraphe par erreur, chaque message d'erreur **cité** et commenté | /2 |

**Le script livré :**
```python
"""ca_magasin4_2025.py (livré par le stagiaire)
Objectif : CA du magasin 4 en 2025, sans retours, mois par mois,
+ total de l'année + panier moyen.
"""
import pandas as pd

D = "03_exercices/dossier_M08"
v = pd.read_csv(D + "/vente.csv")

masque = (v2["id_magasin"] == 4) & (v2["date_vente"].str.startswith("2025"))
vue = v2[masque]
vue["est_retour"] = 0

vue["mois"] = vue["date_vente"].str[5:7]
ca_cents = (vue["montant_ttc"] * 100).round().astype("int64")
mensuel = ca_cents.groupby(vue["mois"]).sum() // 100
print("CA mensuel magasin 4 (2025)")
print(mensuel.to_string())

total_2025 = int(ca_cents.sum()) // 100
print("total_2025 =", total_2025)

panier = int(v["montant_ht"].sum()) // 100
print("panier =", panier)
```

### Les trois exécutions, sorties réelles (exécutées le 20/09/2026)

**1ᵉ run — le premier mur :**
```text
Traceback (most recent call last):
  File "ca_magasin4_2025.py", line 10, in <module>
    masque = (v2["id_magasin"] == 4) & (v2["date_vente"].str.startswith("2025"))
              ^^
NameError: name 'v2' is not defined. Did you mean: 'v' ?
```
*(pandas 2.2.3 ; sous 3.x le message est le même, avec ou sans la suggestion.)*

**2ᵉ run — après correction du `NameError` uniquement : les chiffres s'affichent, puis le
deuxième mur :**
```text
SettingWithCopyWarning:
A value is trying to be set on a copy of a slice from a DataFrame.
Try using .loc[row_indexer,col_indexer] = value instead
  vue["est_retour"] = 0
SettingWithCopyWarning:
...
  vue["mois"] = vue["date_vente"].str[5:7]
CA mensuel magasin 4 (2025)
mois
01    65140834
02    76403254
03    61404369
04    62560349
05    63589011
06    62223329
07    64979650
08    65653426
09    75944225
10    68968410
11    64272077
12    66454383
total_2025 = 797593323
Traceback (most recent call last):
  File "ca_magasin4_2025.py", line 23, in <module>
    panier = int(v["montant_ht"].sum()) // 100
KeyError: 'montant_ht'
```
*(Le `total_2025 = 797593323` qui s'affiche **avant** le `KeyError` est déjà faux : il
inclut les 11 retours du magasin 4 en 2025. Le bon total est 795 478 466 — l'écart de
2 114 857 FCFA est le CA de ces retours. Les avertissements sont déjà le signal de la
ligne qui ne fait rien.)*

**Run corrigé — les sorties attendues :**
```text
CA mensuel magasin 4 (2025, sans retours)
mois
01    64948883
02    76403254
03    61294111
04    62254879
05    63589011
06    61805710
07    64979650
08    65368579
09    75836578
10    68271344
11    64272077
12    66454383
total_2025 = 795478466
panier = 157426
```

**Critères de passage de l'étude de cas (12/20) :** E1 + E2 sans faute, E3 avec la
**bonne** explication (l'affectation sur la vue ne modifie pas le parent — le filtre
retours s'applique donc à la population non nettoyée), et E4 avec le total 795 478 466.

> **L'esprit de l'étude.** Le `NameError` et le `KeyError` sont faciles — Python les
> donne. Le total qui ne correspond pas est le vrai exercice : rien ne crie, deux
> avertissements murmurent, et un chiffre d'écart de 2 114 857 FCFA attend dans la
> sortie. C'est la compétence du module : **un chiffre sans sa vérification n'est pas un
> chiffre, c'est une hypothèse**.

---

## Corrigés ligne à ligne

### B · Quiz — réponses

| Q | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Réponse | b | b | b | b | c | b | c | c | b | b | b | b | b | b | b |

Justifications en une ligne (bonus) :
- Q1 : les décimales binaire ne représentent pas 0,1 exactement — `0.1 + 0.2` renvoie
  `0.30000000000000004` ; d'où les centimes entiers (C02, C08).
- Q3 : Python ne convertit pas implicatement `str + int` — l'erreur est le message, le
  type est la cause.
- Q8 : argument par défaut `pct=10` — `1500 * (1 - 0.1) = 1350.0` (`m08p_demo_prix`,
  `m08p_demo_prix_net`).
- Q12 : le socle a 50 008 **lignes** (8 doublons inclus) et 13 colonnes — la forme est
  brute, pas dédoublonnée.
- Q13 : diviser par ligne arrondit chaque ligne — les centimes perdus ne se retrouvent
  pas (le plus gros mois sort à 228 FCFA de son total).
- Q15 : un `merge` gauche avec table vide garde toutes les lignes de gauche, colonnes
  droites en `NaN` — c'est le signal « pas de données d'objectif », pas un bug.

### C · Exercices — valeurs de référence (clés de traçabilité)

| # | Valeur | Clé `chiffres_cites.json` |
|---|---|---|
| C01 | 50 008 | `m08p_ventes_lignes` |
| C02 | 7 908 259 732 | `m08p_ca_brut` |
| C03 | 50 000 | `m08p_ventes_uniques` |
| C04 | 208 | `m08p_retours_brut` |
| C05 | 7 876 320 164 | `m08p_ca_sans_retours` |
| C06 | 158 140 | `m08p_panier_moyen` |
| C07 | 1 596 813 264 | `m08p_ca_top_magasin` |
| C08 | 7 136 | `m08p_ventes_dimanches` |
| C09 | (50008, 16) | `m08p_ventes_lignes` × `m08p_merge_colonnes` |
| C10 | 50 008 | `m08p_ventes_lignes` |
| C11 | 120 | `m08p_vue_lignes` |
| C12 | 78 965 529 | `m08p_plus_gros_mois_ca` |
| C13 | 24 920 | `m08p_nb_ventes_2025` |
| C14 | 25 088 | `m08p_nb_ventes_2026` |
| C15 | 28 065 | `m08p_ventes_gros_100k` |

### D · Exercices rendus — sorties de référence

| # | Sortie attendue | Clés |
|---|---|---|
| D1 | 18 / 15 / 2025-01-10 | `m08p_deadlines_jour_20_brut`, `m08p_deadlines_jour_20` |
| D2 | 30 / 1 500 050 / 790 825 973 200 | `m08p_demo_float_add`, `m08p_ca_brut` × 100 |
| D3 | 12 753 / 9 190 / 12 319 / 15 746 | `m08p_tranche_0_50k`, `m08p_tranche_50_100k`, `m08p_tranche_100_200k`, `m08p_tranche_200k` |
| D4 | les 12 valeurs mensuelles ; total 795 478 466 ; mois fort 02 (76 403 254) | `m08p_mag4_2025_total`, `m08p_mag4_2025_mois_fort` |
| D5 | `{'vue_mensuelle': (120, 3), 'top_magasin': (5, 2)}` | `m08p_vue_lignes`, `m08p_magasins_lignes` |

### E4 — Les trois corrections

```python
# 1. Volume : dedoublonner avant de compter (12 colonnes métier)
ventes = v.drop_duplicates(subset=[c for c in v.columns if c != "id_vente"]).shape[0]

# 2. CA propre : exclure les retours AVANT de sommer
centimes = (v.loc[~v["est_retour"], "montant_ttc"] * 100).round().astype("int64")
ca_propre = int(centimes.sum()) // 100

# 3. Dénominateur vérifié avant la division — « aucune vente » au lieu de 0
mega = v[v["montant_ttc"] >= 1000000]
if len(mega) == 0:
    print("panier_mega : aucune vente >= 1000000 FCFA")
else:
    panier_mega = int(centimes[v["montant_ttc"] >= 1000000].sum()) // len(mega)
```

**Sorties corrigées (exécutées le 20/09/2026) :**
```text
ventes = 50000
ca_propre = 7876320164
panier_mega : aucune vente >= 1000000 FCFA
```

### E · Étude de cas — points de repère du corrigé

- **E1** : `v2` n'est jamais défini — la typo du `NameError` ; le message de pandas
  2.2.3 le dit lui-même : `Did you mean: 'v' ?`. Correction : `v` partout (2 lignes).
- **E2** : `montant_ht` n'existe pas — la colonne s'appelle `montant_ttc` (13 colonnes,
  pas de HT dans le socle). Correction : `v["montant_ttc"]` — mais attention : le panier
  doit être calculé sur la **population propre** (magasin 4, 2025, sans retours), pas sur
  tout le socle.
- **E3** : `vue = v[masque]` renvoie une vue/copie — `vue["est_retour"] = 0` s'écrit sur
  la vue **sans rien modifier dans `v`** (les `SettingWithCopyWarning` du 2ᵉ run sont le
  signal ; sous pandas 3.x, la même écriture est **silencieuse** — pire encore). Le
  filtre « sans retours » du script s'applique à `vue` **après** que le drapeau a été
  remis à zéro… ou plutôt pas du tout : le mensuel est construit sur **toutes** les
  lignes du magasin 4 en 2025, retours compris → total 797 593 323 au lieu de
  795 478 466 (11 retours, 2 114 857 FCFA). Correction : `vue = vue[~vue["est_retour"]]`
  **avant** de compter.
- **E4** : les 12 valeurs du run corrigé, total 795 478 466, panier 157 426
  (= 795 478 466 // 5 053 ventes propres, `m08p_mag4_2025_ventes`).
- **E5** : chaque paragraphe cite le message (`NameError`, `KeyError`,
  `SettingWithCopyWarning`) et dit **ce qui a été changé** — pas « j'ai corrigé », mais
  « la ligne 12 `vue["est_retour"] = 0` ne modifie pas le parent ; remplacée par
  `vue = vue[~vue["est_retour"]]` avant l'agrégat ».
