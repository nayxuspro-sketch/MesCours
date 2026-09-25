# M14 — Le rapport que le client ne comprend pas (étude de cas)

**Le contexte.** Un consultant a livré ce rapport il y a trois mois. Il fonctionne : les chiffres sont justes, l'actualisation passe, rien ne plante. Le client l'a ouvert **quatre** fois le premier mois, puis plus. Son courriel tient en une ligne : « je ne comprends pas d'où sortent vos chiffres ». Vous avez **8** pages sous les yeux ; voici ce qu'elles contiennent, honnêtement décrites.
| Page | Titre | Ce qu'elle contient |
|---|---|---|
| **P1** | Vue générale | **12** visuels répartis sur l'écran, dont **3** graphiques à deux axes, une jauge sans cible, et deux cartes qui affichent le même indicateur calculé de deux façons différentes (**15 595 154 955** FCFA avec les retours, **15 419 985 157** FCFA sans). Aucun sous-titre ne dit laquelle est laquelle. |
| **P2** | Détail par magasin | un tableau de **6** lignes et **18** colonnes, sans tri, dont **4** colonnes de montants dont l'unité n'est écrite nulle part. Le total de la colonne ne correspond pas à la carte de la page P1. |
| **P3** | Détail par produit | **154** lignes, triées par ordre alphabétique, avec les **16** libellés de familles tels qu'ils sortent du fichier source — alors que le référentiel en compte **7**. |
| **P4** | Tendances | une courbe du chiffre d'affaires mensuel sur **44** mois, sans repère, dont le dernier point est un mois incomplet : la courbe « s'effondre » de **28,9 %** en fin de période. |
| **P5** | Clients | une carte de **23 913** clients, un camembert à **5** parts, et un classement des **10** premiers clients par chiffre d'affaires — sans dire si les retours sont déduits. |
| **P6** | Ruptures | un tableau de **2 428** lignes sans total, et un chiffre en rouge en haut à droite (**7,29 %**) que personne n'a expliqué. |
| **P7** | Objectifs | l'objectif du mois saisi à la main dans un classeur, collé dans un visuel texte. La somme annoncée est celle de **12** mois.
 |
| **P8** | Aide | vide. Le titre est là, les définitions ne le sont pas. |

**Ce qui est vrai dans ce rapport.** Les chiffres de la carte P1 sont justes : ce sont deux définitions défendables du même indicateur, et **175 169 798** FCFA les séparent — l'écart exact des retours. Les **16** libellés de P3 sont ceux du fichier source : c'est le défaut que M13 a corrigé par un modèle, pas par une requête. La baisse de **28,9 %** de P4 est un effet de bord : le mois en cours est incomplet, et la comparaison honnête donne **+ 15,4 %**.

**Votre travail.**

1. Passez la **grille de conception en 18 points** sur les **8** pages, en gardant la **preuve** de chaque réponse (une phrase par point, pas une note).
2. Nommez les **trois** défauts qui expliquent le plus grand nombre d'incompréhensions, et dites pour chacun s'il se corrige dans le **modèle**, dans le **visuel** ou dans la **définition**.
3. Refaites la **page P1** : **5** visuels au maximum, chaque chiffre portant son unité, sa période et sa définition. Les trois valeurs à faire apparaître sont celles du fichier `ATTENDU.json`.
4. Écrivez la **page P8**, l'aide à la lecture, en **10** lignes : ce que chaque indicateur compte, ce qu'il exclut, et la fraîcheur de la donnée.
