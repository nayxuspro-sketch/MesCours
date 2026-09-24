# Brief M08 — « Le script qui fait le travail de trois matinées »

Vous avez reçu l'export CSV de la base commerciale de la chaîne de 5 magasins (la même base
que le module M07, que vous avez interrogée en SQL). Huit fichiers, un par table :

| Fichier | Lignes | Rôle |
|---|---|---|
| `vente.csv` | 50,008 | les ventes (le jeu principal) |
| `client.csv` | 1,200 | la clientèle |
| `produit.csv` | 380 | le catalogue |
| `categorie.csv` | 8 | les rayons et sous-catégories |
| `magasin.csv` | 5 | les 5 magasins |
| `mode_paiement.csv` | 5 | les 5 modes de paiement |
| `regle_tva.csv` | 2 | le taux par année fiscale |
| `objectif_magasin.csv` | 0 | **vide** — la direction n'a pas saisi les objectifs |

Deux consignes de lecture avant de toucher Python :

1. **Rien n'est « propre par avance ».** Ce fichier a été exporté par un stagiaire qui ne sait pas
   ce qu'il a dupliqué : l'audit (section 2 du projet) a de vrais défauts à trouver — des doublons,
   des retours comptés en positif, des dates impossibles, et une table vide.
2. **La vue mensuelle n'est pas exportée.** En SQL, `v_ca_mensuel_magasin` existe dans la base ;
   ici, elle est à **reconstruire** avec `pivot_table` (C08). Ce n'est pas une perte : c'est
   l'exercice.

Votre script devra finir par produire un classeur `synthese_commerciale.xlsx` dont les chiffres
sont **vérifiables** : vous connaissez déjà les réponses au SQL de M07.P. Zéro écart, c'est la
preuve que les deux chemins disent la même chose.
