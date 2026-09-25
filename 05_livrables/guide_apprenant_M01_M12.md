# Guide de l'apprenant — *La Voie des Données*, modules M01 à M12

**Ce guide dit comment se servir du manuel.** Il n'enseigne rien lui-même : il vous dit quoi lire,
dans quel ordre, quoi produire, comment vous êtes corrigé, et où sont les fichiers.

Tous les nombres cités ici sont **mesurés** sur le dépôt et consignés dans
`05_livrables/kit_M01_M12.json` — la source est nommée à chaque fois, rien n'est de mémoire.

---

## 1. Ce que vous avez entre les mains

Douze modules, un seul cas fil rouge : **Sahel Distribution**, un distributeur de quincaillerie
et de matériaux, avec ses 240 000 lignes de ventes, ses clients, ses produits, ses magasins, ses
objectifs. Le même jeu de données du premier chapitre de M01 au dernier de M12 — vous ne
recommencez jamais à zéro.

| Ce que vous avez | Combien | Où |
|---|---|---|
| Modules terminés | 12 | `La_Voie_des_Donnees_M01-M12.pdf` |
| Chapitres rédigés | 81 | les douze modules du livre |
| Heures de programme | 360 | 30 heures par module |
| Pages de cours | 1 207 | les douze modules du livre |
| Mots de cours | 509 252 | les 81 chapitres |
| Exercices autonomes | 366 | section 11 de chaque chapitre |
| Projets de module | 12 | partie II du livre, premier cahier |
| Évaluations de module | 12 | partie II du livre, second cahier |
| Planches | 69 | affichées dans les chapitres |
| Dossiers d'exercices prêts à ouvrir | 10 | `03_exercices/dossier_MXX/` |
| Notions indexées | 488 | partie III du livre |

Le livre assemblé compte **1 395 pages** : les douze modules, puis les cahiers, puis l'appareil.
Le reste du manuel (M13 à M22) est en cours d'écriture ; ce guide ne couvre que ce qui est écrit.

**Une précision qui compte.** Chaque exercice autonome du manuel est repris au corrigé, et c'est
**vérifié** : le contrôle « exercices sans reprise au corrigé » du kit renvoie **0** sur les 366.
Vous pouvez donc travailler seul de bout en bout.

---

## 2. Comment lire, dans quel ordre

Les modules s'enchaînent : chacun suppose le précédent. La colonne « prérequis » de l'index est
sérieuse — commencer M08 sans M05 et M07 coûte deux fois plus de temps qu'il n'en faut.

| Bloc | Modules | Ce que vous y gagnez |
|---|---|---|
| Fondations | M01 à M04 | Lire une donnée, la décrire, la préparer, la documenter |
| Outillage | M05 à M08 | Transformer avec trois moteurs, puis parler SQL et Python |
| Analyse | M09 et M10 | Explorer, conclure prudemment, écrire un graphique honnête |
| Décision | M11 et M12 | Répondre par des requêtes difficiles, définir des indicateurs |

**Le rythme d'un chapitre**, et c'est le même partout :

1. lisez §1 à §5 (objectifs, pourquoi, explication simple, vocabulaire, cours) — 40 minutes ;
2. faites l'**exercice guidé** (§10) en même temps que le pas à pas du §9 — 30 minutes ;
3. faites les **exercices autonomes** (§11) sans regarder la suite — 45 minutes ;
4. **comparez** avec la correction détaillée (§12) et notez la cause de chaque écart — 20 minutes ;
5. écrivez **trois lignes** : ce que vous savez faire maintenant, ce qui reste flou, la question à
   poser. Ces trois lignes sont votre carnet de bord.

Un chapitre demande environ **2 heures de lecture et 2 heures de pratique**. À 6 heures par
semaine, comptez un module toutes les six semaines — et un peu plus vite sur les modules courts.

---

## 3. Les quatre encadrés, et ce qu'ils vous demandent

Le manuel balise chaque chapitre avec les mêmes repères. Ils ne sont pas décoratifs.

- **Définition.** Le mot exact, celui que vous écrirez dans une note professionnelle. Chaque
  chapitre en porte au moins quatre.
- **Attention.** L'erreur qui coûte cher, celle qu'on retrouve en vrai. Au moins deux par chapitre.
- **Dans les faits.** L'ordre de grandeur mesuré sur le fil rouge. Au moins un par chapitre.
- **À retenir.** Ce qu'il faut savoir par cœur pour passer au chapitre suivant. Au moins deux.

L'appareil du livre, dans la partie III, donne l'**index des notions** (488 entrées, avec les
chapitres où chaque terme est traité), le **glossaire** (la première phrase de chaque définition du
manuel), l'**index des planches**, celui des **instruments** et celui des **jeux de données**.

---

## 4. Ce que vous produisez

Chaque module se termine par un projet noté, et chaque projet nourrit **une** pièce de portfolio.
Douze modules, douze pièces — c'est ce que vous montrerez en entretien, pas vos notes.

Un projet de module tient en général en quatre à six heures de travail et se remet sous forme de
fichiers. Trois règles, toujours les mêmes :

- **le périmètre est déclaré** : ce que votre livrable couvre, ce qu'il ne couvre pas ;
- **aucun chiffre sans source** : la table ou le fichier d'où il vient, et la requête ou la formule
  qui le calcule ;
- **le geste se rejoue** : un lecteur doit pouvoir refaire votre travail sur les mêmes fichiers.

Les douze projets sont réunis au **premier cahier** de la partie II, avec leurs livrables et leur
barème. Ils totalisent 67 516 mots avec les évaluations, dans un seul document.

---

## 5. Comment vous êtes corrigé

Chaque module a son évaluation, au **second cahier** de la partie II. La **structure** est stable —
une épreuve de récupération (quiz), des exercices d'application, une étude de cas, parfois un
auto-test — et le **barème**, lui, est propre à chaque module. Les voici, tels qu'ils sont annoncés
en tête de chaque évaluation :

| Module | Ce que l'évaluation note | Seuils annoncés |
|---|---|---|
| **M01** et **M02** | quiz sur 20, étude de cas sur 20 | 14/20 et 12/20 (projet 13/20) |
| **M03** | quiz sur 15, étude de cas sur 20 | 11/15 et 12/20 (projet 13/20) |
| **M04**, **M05**, **M06** | quiz sur 15, exercices sur 20, étude de cas sur 20 | 11/15, 14/20 et 12/20 |
| **M07** | quiz sur 20, exercices sur 35, étude de cas sur 20 | 13/20, 28/35 et 12/20 |
| **M08** et **M09** | quiz sur 15, exercices sur 15, étude de cas sur 20 | 11/15, 11/15 et 12/20 (projet 13/20) |
| **M10** | quiz sur 20, « prédisez la mesure » sur 10, exercices sur 20, étude de cas sur 20 | 14/20 et 12/20 — **65 points** au total |
| **M11** | quiz sur 20, exercices sur 20, auto-test sur 10, étude de cas sur 20 | 14/20 et 12/20 — **70 points** au total |
| **M12** | quiz sur 20 (15 questions), exercices sur 20, étude de cas sur 30 | 11/15 et 18/30 — **70 points** au total |

Deux règles traversent tous les modules. **L'étude de cas porte toujours son propre seuil** — 12 sur 20
dans onze modules sur douze, 18 sur 30 en M12 : un raisonnement juste mais non chiffré ne la valide
pas.
Et le **projet de module est noté séparément** de l'évaluation, sur 20, seuil 13 : il ne rattrape pas
un quiz manqué, et un quiz réussi ne remplace pas un livrable absent.

**Comment se corriger soi-même, sans se mentir.** Le corrigé donne les valeurs attendues et, plus
utile, l'**écart toléré** : un résultat à 2 % du bon n'est pas faux, un raisonnement qui ne dit pas
où il prend son chiffre l'est. Quand votre résultat diffère, cherchez d'abord la cause — filtre
oublié, jointure qui multiplie, arrondi trop tôt — puis écrivez-la dans votre carnet. Les six
erreurs les plus fréquentes sont listées à la fin de chaque correction détaillée.

---

## 6. Les fichiers, et comment les ouvrir

| Ce que vous cherchez | Où c'est | Comment on l'ouvre |
|---|---|---|
| Un jeu de données d'exercice | `03_exercices/dossier_MXX/` | `python3 connexion.py` dans le dossier |
| Le socle complet du fil rouge | `01_socle_donnees/data/` | DuckDB ou SQLite, jamais Excel |
| Tous les chiffres cités, par module | `01_socle_donnees/data/reference/chiffres_cites.json` | un éditeur de texte |
| Le recalcul des chiffres du manuel | `01_socle_donnees/scripts/chiffres_manuel.py` | `python3 chiffres_manuel.py M12` |
| Le contrôle qualité du texte | `01_socle_donnees/scripts/autovalide.py` | `python3 autovalide.py M12 --strict` |

**Avant le premier exercice**, installez l'environnement une seule fois :

```bash
python3 -m venv .venv
source .venv/bin/activate        # sous Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

Puis ouvrez le dossier du module et lancez `connexion.py` : il ouvre la base DuckDB du chapitre et
affiche les tables disponibles. Tout le manuel tourne avec des outils **gratuits** : DuckDB, SQLite,
Python, pandas, Excel. Les outils commerciaux (Power BI, Tableau, SQL Server, PostgreSQL) sont
cités, jamais nécessaires pour faire les exercices — et les chapitres qui les présentent disent
explicitement ce qui est **exécuté** et ce qui est **cité sans exécution**.

---

## 7. Les cinq règles du manuel

Elles ne sont pas des principes affichés : elles sont contrôlées par les scripts du dépôt.

1. **Un chiffre a une source.** Tout nombre de quatre chiffres et plus, dans le texte, vient d'un
   calcul enregistré. Le relevé du manuel en compte 2 499, tous recalculables.
2. **Une affirmation se mesure.** Quand un chapitre dit qu'une méthode coûte plus cher ou va plus
   vite, il donne la mesure, et le libellé colle à la mesure.
3. **Le périmètre est écrit.** Ce qui est fait, ce qui n'est pas fait — les trois modules M14, M16
   et M17 sont documentés pas à pas **et déclarés non exécutés** ici.
4. **Les choses portent leur nom.** « Tableau de bord » plutôt que *dashboard*, « chaîne de calcul »
   plutôt que *pipeline* ; chaque terme anglais est accompagné de son équivalent français.
5. **Le travail se relit.** Un chiffre recopié à la main est un chiffre qui mentira un jour : c'est
   pourquoi l'index, le glossaire et ce guide sont **générés** depuis les fichiers du manuel.

---

## 8. Par où continuer

Le manuel n'est pas fini : **22 modules** sont prévus, dont **12 sont écrits**. La suite dans
l'ordre, et ce qu'elle vous apportera :

- **M13, Modélisation des données** (en cours) — concevoir le schéma qui rend les indicateurs de
  M12 calculables sans erreur ; c'est la quatrième pièce de votre portfolio ;
- **M14 et M15** — Power BI puis DAX, documentés pas à pas ;
- **M16 à M19** — Tableau, automatisation du reporting, analyses sectorielles, prévision,
  segmentation, scoring, jusqu'à la soutenance ;
- **M20 à M22** — dire ce que les chiffres veulent dire, mener un projet complet, puis le portfolio
  et la recherche d'emploi.

D'ici là, tout ce dont vous avez besoin pour travailler **est dans le livre**. Si un exercice
résiste plus de quarante minutes, la bonne réponse n'est pas de chercher plus longtemps : c'est de
lire la correction, puis de refaire l'exercice deux jours plus tard, cahier fermé.

---

*Guide de l'apprenant, édition du 25 septembre 2026 — pour les modules M01 à M12. Sources des
nombres : `05_livrables/kit_M01_M12.json` (mesures du kit), `05_livrables/index_glossaire_M01_M12.md`
(index et glossaire), `01_socle_donnees/data/reference/chiffres_cites.json` (relevé des chiffres
cités dans le manuel).*
