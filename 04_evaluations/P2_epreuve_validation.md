# Épreuve de validation de palier P2 — « Du chiffre juste à la conclusion honnête »

**Fin du palier P2 (dernier module : M09) · 90 min en temps limité · noté /20, seuil 14 · conditions d'entrée au palier P3 · épreuve mixte : requêtes, formules, code, et une question de décision.**

| Partie | Durée | Barème | Ce qui est mesuré |
|---|---|---|---|
| 1 · Requêtes (M06–M07) | 20 min | /5 | écrire et **exécuter** la requête qui répond à la question, avec sa vue intermédiaire |
| 2 · Formules et tableau (M03) | 15 min | /3 | la formule unique recopiée, la plage nommée, le total qui ne trompe pas |
| 3 · Code pandas (M08) | 25 min | /5 | lire un script, prédire sa sortie, corriger une erreur de valeur |
| 4 · EDA (M09) | 20 min | /4 | les 10 étapes, la preuve d'une anomalie, la phrase et sa limite |
| 5 · Question de décision (M08 + M09) | 10 min | /3 | trancher, avec les chiffres qui soutiennent la décision **et** sa limite |

> **Règle de l'épreuve.** Une réponse **sans son chiffre** ne compte pas ; un chiffre **sans sa
> limite** ne compte qu'à moitié. Les deux compétences du palier se mesurent ensemble : produire
> des chiffres justes (M08) **et** en tirer des conclusions provisoires honnêtes (M09). Tous les
> nombres de l'énoncé et du corrigé sont mesurés sur les socles livrés (`dossier_M07`,
> `dossier_M08`, `dossier_M09`) et sourcés dans `chiffres_cites.json`.

---

## Partie 1 · Requêtes (5 points)

Sur `commercial.duckdb` (socle M07) : la table `vente` porte 50 008 lignes, dont 8 doublons et
208 retours.

**Q1.1 (1 pt).** Écrire la requête qui donne le **CA propre** (retours exclus) des 5 magasins, en
**centimes entiers**, et donner le total en FCFA.

**Q1.2 (1 pt).** Écrire la requête qui donne le **plus gros mois** de la vue `v_ca_mensuel_magasin`
— et dire pourquoi la jointure de la vue ne gonfle **pas** le total.

**Q1.3 (1.5 pt).** Écrire la requête qui compte les ventes **par mode de paiement** et les trie par
effectif décroissant ; expliquer en une phrase pourquoi les tailles (de 2 552 à 20 175) comptent
autant que les paniers.

**Q1.4 (1.5 pt).** Une erreur classique : `COUNT(*)` sur une jointure `vente × produit × client ×
magasin` donne un total **plus grand** que 50 008. Donner la requête **fausse**, le résultat
qu'elle produit, la requête **juste** et le résultat juste.

## Partie 2 · Formules et tableau (3 points)

**Q2.1 (1 pt).** Écrire la formule **unique** (recopiable) qui calcule le montant TTC de la ligne 2
d'un tableau de ventes (quantité × prix unitaire HT × 1,19), en colonne `E`, sachant que le tableau
s'appelle `TableVentes` et que les colonnes sont `quantite` (B), `prix_unitaire_ht` (C) et
`taux_tva` (D).

**Q2.2 (1 pt).** Écrire la formule qui donne le CA total du tableau **sans** le total de pied de
tableau, et expliquer pourquoi on ne somme **jamais** la colonne de total.

**Q2.3 (1 pt).** Le tableur affiche 78 965 301 FCFA là où le socle mesure **78 965 529** : quelle
est la cause **exacte**, et quelle est la règle qui l'évite ?

## Partie 3 · Code pandas (5 points)

```python
import pandas as pd
v = pd.read_csv("03_exercices/dossier_M08/vente.csv", parse_dates=["date_vente"])
ct = (v["montant_ttc"] * 100).round().astype("int64")
print(ct.sum() // 100)
print(int((pd.to_datetime(v["date_vente"]).dt.dayofweek == 6).sum()))
print(v.groupby("id_mode")["montant_ttc"].mean().round(0).to_dict())
print(round(v["montant_remise"].corr(v["montant_ttc"]), 3))
```

**Q3.1 (2 pts).** **Prédisez** les quatre sorties, puis dites laquelle est un **piège de lecture**
(et de quel type).

**Q3.2 (1.5 pt).** Un stagiaire remplace la première ligne par
`print(v["montant_ttc"].sum())` : que change-t-il exactement, et pourquoi le total devient-il faux ?

**Q3.3 (1.5 pt).** Le stagiaire calcule ensuite le taux de remise avec
`v["montant_remise"] / v["montant_ttc"]` et trouve une corrélation de **0.001**, alors qu'en FCFA
il trouvait **0.552**. Expliquer les deux valeurs en une phrase chacune.

## Partie 4 · EDA (4 points)

**Q4.1 (1.5 pt).** Citer les **10 étapes** du protocole, puis dire ce qu'on écrit dans une étape
qui ne trouve rien.

**Q4.2 (1.5 pt).** Sur `dossier_M09/sante/stock_medicament.csv`, 4 lignes portent un stock de fin
**négatif** (jusqu'à -12). Donner les **deux** témoins qui permettent d'affirmer que c'est un
défaut, et la décision qui en découle **avec sa ligne de rapport**.

**Q4.3 (1 pt).** La corrélation entre absentéisme et résultats vaut **-0.232** (n = 400). Écrire la
phrase publiée, **avec ses quatre chiffres**.

## Partie 5 · Question de décision (3 points)

**Q5.** Le directeur commercial vous demande : « **doit-on ouvrir un sixième magasin ?** » Les
chiffres du fil rouge : CA mensuel stable (307 à 348 M FCFA, moyenne glissante 3 mois dans une
bande de 320 à 337 M), 5 magasins, 1 200 clients, 20 175 ventes sur le mode de paiement le plus
fréquent, top 10 % des clients = **13.8 %** du CA. **Tranchez** (1 pt), donnez les **deux chiffres**
qui soutiennent votre décision (1 pt), et la **limite** qui pourrait l'inverser (1 pt).

---

## Corrigé

### Partie 1

**Q1.1.** `SELECT SUM(CAST(ROUND(montant_ttc * 100) AS BIGINT)) FROM vente WHERE NOT est_retour;`
→ **787 632 016 400** centimes = **7 876 320 164 FCFA** (clé `m08p_ca_sans_retours`). Sans le
`WHERE`, on obtient 7 908 259 732 FCFA — l'écart (31 939 568 FCFA) **est** le montant des retours.

**Q1.2.** `SELECT magasin, mois, ca FROM v_ca_mensuel_magasin ORDER BY ca DESC LIMIT 1;` → le plus
gros mois : magasin **3**, **2025-08**, **78 965 529 FCFA** (`m08p_plus_gros_mois_ca`). La vue ne
gonfle pas le total parce que la jointure est **étoile** (plusieurs tables côté « 1 », une seule
côté « plusieurs ») : chaque ligne de vente reste **une** ligne — une jointure qui multiplie serait
une jointure mal faite, et le compte le dirait.

**Q1.3.** `SELECT id_mode, COUNT(*) n, AVG(montant_ttc) panier FROM vente GROUP BY id_mode ORDER BY
n DESC;` → 20 175 / 12 366 / 12 322 / 2 593 / 2 552 ventes (`m09p_q_ventes_par_mode`). Les tailles
comptent autant que les paniers parce qu'un panier moyen sur 2 552 ventes n'a pas la même précision
que sur 20 175 : les écarts de 2.4 % entre modes sont **du bruit de taille**, pas un comportement.

**Q1.4.** La requête fausse joint les 4 tables **sans agrégat ni `DISTINCT`** :
`SELECT COUNT(*) FROM vente v JOIN produit p ON … JOIN client c ON … JOIN magasin m ON …;` →
compte **> 50 008** (chaque vente répétée par les lignes correspondantes des tables jointes). La
requête juste : `SELECT COUNT(*) FROM vente;` → **50 008** (ou `COUNT(DISTINCT id_vente)` après
jointure). **La leçon** : on compte sur la table **de faits**, jamais après une jointure qui n'a pas
été vérifiée par le compte.

### Partie 2

**Q2.1.** `=[@quantite]*[@prix_unitaire_ht]*(1+[@taux_tva])` — les références **structurées** du
tableau `TableVentes` : la formule se recopie seule sur les 50 008 lignes et reste juste si on
ajoute une ligne.

**Q2.2.** `=SOMME(TableVentes[montant_ttc])` : elle somme la **colonne du tableau**, dont la
portée suit les lignes ajoutées ; le total de pied de tableau, lui, est **une cellule** — le sommer
avec la colonne compterait les lignes **deux fois**.

**Q2.3.** La cause est l'addition **ligne par ligne de valeurs arrondies** (chaque ligne divisée
avant la somme) : les centimes de chaque ligne sont perdus. La règle : additionner en **centimes
entiers**, diviser **une seule fois** après l'agrégat — l'écart de 228 FCFA est exactement ce que la
règle récupère.

### Partie 3

**Q3.1.** Sorties : (1) **7 908 259 732** FCFA — le CA **brut**, retours **inclus** (« le total qui
sourit ») ; (2) **7 136** ventes du dimanche (`m08p_q_dimanches`) ; (3) les **5** paniers moyens par
mode, de **156 150** à **159 959** FCFA ; (4) **0.552**. Le **piège de lecture** est la sortie (1) :
c'est un total **juste** et une réponse **fausse** — le script n'a pas filtré les retours.

**Q3.2.** `v["montant_ttc"].sum()` additionne des `float` : le total devient **7 908 259 731** (un
FCFA de moins) au lieu de 7 908 259 732 — la **dérive float** de la somme, mesurée et documentée. Le
total est faux **au sens strict** du palier : on additionne en centimes entiers.

**Q3.3.** En FCFA, la remise **suit mécaniquement** le montant (une grosse vente porte une grosse
remise en valeur) : **0.552** est un effet de **scale**. En **taux** (remise / montant), le lien
disparaît : **0.001** — la politique de remise ne dépend pas de la taille du panier.

### Partie 4

**Q4.1.** Inspecter, comprendre les variables, détecter les problèmes, premières statistiques,
tendances, anomalies, relations, hypothèses, visualisations, conclusions provisoires. Une étape qui
ne trouve rien s'**écrit vide** : « aucune anomalie détectée, et voici les 3 contrôles faits pour
l'affirmer » — le silence est le seul défaut du rapport.

**Q4.2.** **Témoin métier** : une borne qu'aucun inventaire réel ne franchit (un stock ne peut pas
être négatif) — il parle **seul**. **Témoin de récurrence** : hier + entrées - sorties = aujourd'hui
donne, pour la ligne à -12, un stock d'entrée de **545** : la ligne est **condamnée** par le calcul.
**Décision** : **corriger** (les 4 négatifs deviennent 411, 253, 278, 545) ; **ligne de rapport** :
« 4 stocks négatifs (-1, -3, -2, -12) corrigés par récurrence : la valeur d'entrée était déductible
du flux ; correction tracée, source à confirmer. »

**Q4.3.** « L'absentéisme et les résultats sont **associés négativement** (−0.232), **n = 400**
élèves, **contrôle** par bandes de niveau initial (−0.145 / −0.085 / +0.163 : le lien s'effondre),
**limite** : corrélation sans causalité, sens non départagé, une seule session. »

### Partie 5

**Décision (1 pt)** : **non** — ne pas ouvrir sur ces chiffres. **Les deux chiffres (1 pt)** : le CA
est **plat** sur 24 mois (moyenne glissante 3 mois entre **320** et **337** M FCFA — la dérive la
plus forte à mois égal est de **+1.6 %**), et la clientèle est **plate** (le top 10 % des 1 200
clients pèse **13.8 %** du CA : pas de concentration qui signalerait une demande insatisfaite).
**La limite qui pourrait inverser la décision (1 pt)** : le fichier ne porte **ni la zone de
chalandise, ni la file d'attente, ni les ventes perdues** — un sixième magasin se décide sur des
données que ces 5 magasins **ne contiennent pas** (le socle s'arrête au 2026-12-28, décembre 2026
partiel : la tendance de fin d'année n'est pas lisible). La bonne réponse au directeur est donc :
« aucune ouverture sur ces chiffres — ce qu'il faut aller chercher, c'est la demande non servie ».

---

> **Seuil de passage.** 14/20. En dessous de 12, le palier P2 est à reprendre en entier (M08 et M09) :
> la compétence du palier est **l'honnêteté du chiffre**, pas la vitesse du calcul.
