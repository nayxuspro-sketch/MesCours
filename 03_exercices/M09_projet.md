# Projet M09.P — « 3 heures avec un fichier que personne n'a regardé »

**Module M09 · projet noté sur 20 · seuil 13 · durée imposée 3 h (chronomètre en marche) · rendu : 4 livrables**

> **Ce que le projet évalue.** Non pas « ce que vous avez trouvé », mais **ce que vous
> pouvez affirmer** : un rapport de 10 étapes à 80 % avec ses limites honnêtes passe ;
> une exploration à 100 % sans structure ne passe pas. Le fichier est un export brut
> d'un opérateur de **mobile money** (6 mois, 10 014 lignes × 10 colonnes) dont le
> contexte est à découvrir **dans** le fichier — personne ne vous en dit plus que ce
> qu'il contient.

---

## 1. Énoncé

### Le matériel

| Élément | Chemin | Ce que c'est |
|---|---|---|
| Fichier de travail | `03_exercices/dossier_M09/projet/fichier_inconnu.csv` | 10 014 lignes × 10 colonnes, période 2026-01-01 → 2026-06-30, **personne ne l'a regardé** |
| Brief du dossier | `03_exercices/dossier_M09/00_brief.md` | ce qui est remis à l'apprenant : les 4 jeux, et la règle de l'`ATTENDU` |
| Résultats attendus | `03_exercices/dossier_M09/ATTENDU.json` | les mesures de référence (section `projet`) — **à consulter après**, jamais avant |
| Les 6 chapitres | `02_modules/M09_C01…C06` | le protocole en 10 étapes, l'audit, la décomposition, la preuve, la corrélation, la note d'EDA |
| Référence des chiffres | `01_socle_donnees/data/reference/chiffres_cites.json` | clés `m09p_p_*` : tout chiffre publié vient de là |

### La règle du chronomètre

**3 h, pas 3 h 30.** À la 3ᵉ heure, on **arrête** et on rend ce qui est fait. La fiche
d'entrée se remplit dans les **30 premières minutes** (C01) : un candidat qui explore
45 minutes « pour voir » avant d'écrire une ligne a déjà perdu la moitié de P1.
L'exploration **sans méthode** est la faute que le projet punit ; l'arrêt **avec** des
conclusions provisoires est la compétence qu'il note.

### Les 4 livrables et ce qu'ils notent

| # | Livrable | Ce que ça mobilise | Points |
|---|---|---|---|
| **P1** | **La fiche d'entrée** (complétée dans les 30 min) : forme du fichier, variables (nom, unité, type, origine), **3 questions que le fichier peut répondre** et **2 qu'il ne peut pas** | C01 | /4 |
| **P2** | **Le rapport d'EDA** : les 10 étapes du protocole, **chaque étape** en une question + sa réponse chiffrée (sortie imprimée) ; les défauts du fichier chiffrés **avec leur définition exacte** | C01–C04 | /6 |
| **P3** | **Les 4 graphiques** qui répondent aux 4 questions les plus importantes du rapport — chacun légendé : **question** dans le titre, **source**, **n**, **axe déclaré** s'il n'est pas à zéro | C06 | /5 |
| **P4** | **La note de conclusions provisoires** (1 page) : ce que le fichier **suggère**, chaque affirmation avec sa **source** et sa **limite** ; la corrélation n'est **jamais** présentée comme une cause | C05, C06 | /5 |
| | **Total** | | **/20** |
| | **Seuil de validation** | | **13/20** |

## 2. Grille de notation détaillée (/20)

| Livrable | Détail | Points |
|---|---|---|
| **P1** | Fiche d'entrée **complète et datée** : forme (lignes × colonnes), les 10 variables avec unité et origine, 3 questions **répondables** (formulées), 2 questions **non répondables** avec la raison (*variable absente*, *période trop courte*, *pas d'intervention*) ; rendue **dans les 30 minutes** | /4 |
| **P2** | Les **10 étapes présentes**, chacune en question + réponse chiffrée ; les **4 défauts** du fichier chiffrés **avec leur définition exacte** (doublons sur `tx_ref`, montants négatifs, montants hors borne, commissions manquantes) ; les **6 graphies de statut** normalisées avant tout calcul de taux | /6 |
| **P3** | 4 graphiques **qui répondent à une question écrite dans le titre**, `matplotlib`/`seaborn` exécutés, légende (source, n), axe déclaré si non zéro, **pas** de graphique « pour voir » | /5 |
| **P4** | 1 page, chaque affirmation = phrase + **source** (sortie re-jouable) + **limite** remplie (taille d'échantillon, période, variables manquantes) ; **aucune** causalité affirmée | /5 |
| **Total** | | **/20** |

**Les 4 points qui se perdent le plus souvent** (et le chiffre qui les contrôle) :

1. compter les lignes **avant** de dédoublonner → 10 014 lignes affichées au lieu de
   10 000 transactions distinctes ;
2. calculer un taux de succès **sans normaliser les statuts** → six graphies
   (`OK`, `ok`, `Reussie`, `REUSSI`, `Echouee`, `echec`) et un taux faux ;
3. publier un montant moyen **sans exclure les valeurs impossibles** → la moyenne est
   tirée par deux lignes aberrantes ;
4. conclure « les agents X font mieux » **sans les tailles** → 20 agents, des volumes
   très inégaux.

## 3. Corrigé-type (sorties réelles, exécutées le 20/09/2026)

```python
import pandas as pd
d = pd.read_csv("03_exercices/dossier_M09/projet/fichier_inconnu.csv")

print(d.shape)                       # (10014, 10)
print(d["tx_ref"].duplicated().sum())  # 14  -> doublons sur la clé de transaction
d2 = d.drop_duplicates(subset="tx_ref")
print(d2.shape)                      # (10000, 10) : 10 000 transactions distinctes

print(d2["statut"].value_counts().to_dict())
# {'Reussie': 2082, 'ok': 2043, 'OK': 2037, 'REUSSI': 1962, 'echec': 981, 'Echouee': 909}
norm = (d2["statut"].str.strip().str.lower()
        .map(lambda s: "succes" if s in ("ok", "reussie", "reussi") else "echec"))
print(norm.value_counts().to_dict())  # {'succes': 8115, 'echec': 1885}
print(round(100 * norm.eq("succes").mean(), 2))   # 81.15  (taux de succès, %)

print(int((d2["montant_xof"] < 0).sum()))         # 5   (min -4 555)
print(int((d2["montant_xof"] > 1_000_000).sum())) # 2   (max 1 000 000 000)
print(int(d2["commission"].isna().sum()))         # 29
print(d2["agent_code"].nunique())                 # 20
print(d2["canal"].value_counts().to_dict())       # {'Agent': 4971, 'USSD': 4009, 'app': 1020}
print(d2["type_op"].value_counts().to_dict())     # {'in': 5847, 'out': 4153}
print(d2["date_op"].min(), "->", d2["date_op"].max())   # 2026-01-01 -> 2026-06-30
```

**La lecture P4 (la note de conclusions provisoires)** — quatre affirmations, chacune
avec sa source et sa limite :

1. « **Huit transactions sur dix réussissent** (81.15 %), stable sur les 6 mois. »
   *Source : normalisation des 6 graphies + `value_counts` (exécuté).* *Limite : les
   1890 échecs ne portent **pas** de code de motif — on ne sait pas **pourquoi** elles
   échouent ; ne pas confondre taux d'échec et cause d'échec.*
2. « La **moyenne des montants ne veut rien dire** tant que les extrêmes sont dans le
   fichier : 203 506 XOF sur le fichier reçu contre 3 790 XOF sur les 9 993 lignes
   valides, pour une médiane de 2 503 XOF — 2 lignes à 1 000 000 000 XOF et 5 lignes
   négatives (de -685 à -4 555) font tout l'écart. » *Source : bornes métier, médiane
   vs moyenne (exécuté).* *Limite : la borne haute est **à confirmer avec l'exploitant**
   — on exclut ces lignes du calcul et on l'écrit, on ne les corrige pas.*
3. « Le **canal Agent** domine (4971 transactions) devant l'USSD (4009) et l'application
   (1020). » *Source : `value_counts` (exécuté).* *Limite : 6 mois seulement, et
   `agent_code` est un **code** : 20 agents, mais aucune information sur la zone, le
   point de vente ou le type de clientèle — pas de lecture géographique possible.*
4. « Les **29 commissions manquantes** (0.29 % des lignes) se concentrent sur un seul
   canal : à signaler, pas à combler. » *Source : `isna().sum()` par canal (exécuté).*
   *Limite : un manquant **déclaré** n'est pas un manquant corrigé ; inventer la
   commission (taux moyen) fabriquerait un chiffre que personne ne peut vérifier.*

## 4. Les contrôles de fiabilité (rappel et vérification)

| Contrôle | Défaut / écart | La leçon | Chiffre de contrôle |
|---|---|---|---|
| **D1** | 14 doublons sur `tx_ref` | dédoublonner sur la **clé de transaction**, pas sur la ligne entière | 10 014 → 10 000 |
| **D2** | 6 graphies de statut (`OK`, `ok`, `Reussie`, `REUSSI`, `Echouee`, `echec`) | normaliser **avant** de compter : le taux se calcule sur la valeur normalisée | 8 115 succès / 1 885 échecs (81.15 %) |
| **D3** | 5 montants négatifs + 2 montants à 1 000 000 000 XOF | borner **avec le métier**, exclure en le déclarant, jamais « corriger » une valeur qu'on ne peut pas vérifier | 9 993 lignes exploitables |
| **D4** | 29 commissions manquantes (0.29 %) | un manquant se **signale** ; l'inventer fabrique un chiffre invérifiable | 29 sur 10 000 |
| **Centimes** | publier un volume en float sur des montants à 9 chiffres | additionner en **entiers** (centimes), diviser une fois après l'agrégat | volume valide 37 874 954 XOF, moyenne valide 3 790 XOF (`m09p_p_montant_total_valides`) |

> **Le contrôle final du projet.** Relisez P4 à voix haute : chaque phrase doit pouvoir
> être suivie de « … et sa limite est que … ». Si la limite reste vide, l'affirmation
> **déborde** de ce que le fichier dit : on la recule (ou on la retire). C'est
> exactement ce que note l'épreuve de palier **P2** — produire des chiffres justes
> **et** en tirer des conclusions provisoires honnêtes.
