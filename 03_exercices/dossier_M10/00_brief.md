# Brief M10 — « La refonte »

Vous recevez un **rapport commercial** d'une enseigne de quincaillerie (5 magasins, 24 mois,
50 008 ventes). Ce rapport n'est pas faux : **ses chiffres sont justes**. Ce sont ses
**graphiques** qui font lire autre chose que ce que les données disent.

| Dossier | Contenu |
|---|---|
| `rapport_avant/` | les **5 graphiques** du rapport, tels qu'ils ont été publiés (et le code qui les produit) |
| `rapport_avant/rapport_avant.md` | les **2 pages** du rapport : ce que la direction en a retenu |
| `rapport_apres/` | les 5 graphiques **corrigés** — à ne consulter qu'après avoir proposé les vôtres |
| `ATTENDU.json` | les mesures des défauts (à comparer à vos propres mesures, **pas à recopier**) |

**Ce qu'on vous demande (`M10.P — La refonte`) :**

1. **Diagnostiquer** chaque graphique : nommer le défaut, **mesurer** l'écart qu'il crée entre
   ce que l'œil lit et ce que les données disent, et dire **quelle décision il ferait prendre à tort**.
2. **Corriger** : le bon graphique pour la question, titre qui affirme, axes honnêtes, annotation
   du chiffre clé, couleur justifiée.
3. **Produire deux versions du même constat** : une version **direction** (1 écran, l'idée et la
   décision) et une version **équipe opérationnelle** (le détail et les libellés exacts).
4. **Auto-évaluer** votre refonte avec la **grille de conception en 18 points**, puis la faire
   relire par un pair.

**La règle du projet.** Une refonte qui change un **chiffre** en changeant un **graphique** est
rejetée : les totaux avant/après doivent être **identiques** (contrôle automatique). Le module
change la **lisibilité**, jamais la donnée.
