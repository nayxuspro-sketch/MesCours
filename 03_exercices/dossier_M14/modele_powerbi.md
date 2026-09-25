# M14 — Le modèle à construire dans Power BI

**Ce que vous montez, dans l'ordre.** Le modèle est celui de M13, importé tel quel : **12** tables du rapport, **12** relations actives, **2** relations inactives, **10** mesures, **3** pages et **14** visuels. Aucune capture d'écran : chaque geste est décrit par son libellé, son emplacement et son effet vérifiable.

**Déclaration d'exécution (§1.5).** Power BI Desktop n'est pas installé dans l'atelier : rien de ce document n'a été exécuté dans l'outil. Ce qui **est** mesuré, c'est ce que le rapport doit afficher : les **10** valeurs du fichier `ATTENDU.json`, calculées en SQL sur le modèle de M13.

## 1. Les 12 relations à déclarer
| # | Table de faits | Colonne | Dimension | Colonne | Cardinalité | Sens du filtre |
|---|---|---|---|---|---|---|
| 1 | `fait_ventes` | `id_magasin` | `dim_magasin` | `id_magasin` | plusieurs à un | dimension vers le fait |
| 2 | `fait_ventes` | `id_produit` | `dim_produit` | `id_produit` | plusieurs à un | dimension vers le fait |
| 3 | `fait_ventes` | `id_client` | `dim_client` | `id_client` | plusieurs à un | dimension vers le fait |
| 4 | `fait_ventes` | `id_vendeur` | `dim_vendeur` | `id_vendeur` | plusieurs à un | dimension vers le fait |
| 5 | `fait_ventes` | `date_vente` | `dim_date` | `date` | plusieurs à un | dimension vers le fait |
| 6 | `fait_commandes` | `id_magasin` | `dim_magasin` | `id_magasin` | plusieurs à un | dimension vers le fait |
| 7 | `fait_commandes` | `id_client` | `dim_client` | `id_client` | plusieurs à un | dimension vers le fait |
| 8 | `fait_commandes` | `date_commande` | `dim_date` | `date` | plusieurs à un | dimension vers le fait |
| 9 | `fait_encaissements` | `id_client` | `dim_client` | `id_client` | plusieurs à un | dimension vers le fait |
| 10 | `fait_encaissements` | `date_facture` | `dim_date` | `date` | plusieurs à un | dimension vers le fait |
| 11 | `fait_ruptures` | `id_produit` | `dim_produit` | `id_produit` | plusieurs à un | dimension vers le fait |
| 12 | `fait_ruptures` | `id_magasin` | `dim_magasin` | `id_magasin` | plusieurs à un | dimension vers le fait |

**Ce que le contrôle dit de ces relations** : les **12** colonnes de dimension sont **uniques** dans leur table (`dim_client` : 23 913 valeurs distinctes de clé pour 23 913 lignes · `dim_produit` : 154 valeurs distinctes de clé pour 154 lignes · `dim_magasin` : 6 valeurs distinctes de clé pour 6 lignes · `dim_vendeur` : 22 valeurs distinctes de clé pour 22 lignes · `dim_date` : 1 339 valeurs distinctes de clé pour 1 339 lignes). Une relation plusieurs à un n'a que cette condition à remplir, et elle suffit à garantir qu'aucune ligne ne se multiplie.

## 2. Les 2 relations inactives, et pourquoi
| Table de faits | Colonne | Dimension | Raison |
|---|---|---|---|
| `fait_commandes` | `date_promisee` | `dim_date` | la date promise : elle sert au taux de service, et s'active dans la mesure, jamais dans le filtre du rapport |
| `fait_commandes` | `date_livraison` | `dim_date` | la date de livraison : candidate naturelle, mais le rapport se lit par date de commande — la livraison est une information de suivi |

**La règle.** `fait_commandes` porte **trois** dates et il n'existe qu'**une** table de dates : une seule relation peut porter le filtre du rapport. Les deux autres restent **inactives** — elles existent, elles ne filtrent pas — et s'activent dans une mesure précise. Ce n'est pas un défaut : c'est la seule façon d'avoir trois temps dans un même fait.

**Le piège à ne pas commettre.** Ne reliez **jamais** un fait à la table de dates par une colonne non unique, comme `annee_mois` : elle apparaît **44** fois dans le calendrier (une fois par mois), le filtre se propage à ces **44** lignes, chaque ligne de vente se répète et le chiffre d'affaires est multiplié. C'est la faute que M13 a mesurée : un facteur **44,0** sur une jointure trop large.

## 3. Les 15 gestes de Power Query
| # | Geste | Porte sur | Ce qu'il fait sur le fil rouge |
|---|---|---|---|
| 1 | **Source** | CSV | ouvrir le fichier, délimiteur virgule, encodage UTF-8 avec BOM |
| 2 | **Promouvoir les en-têtes** | Table | la première ligne devient le nom des colonnes |
| 3 | **Modifier le type** | Type | types explicites : entiers, décimaux, dates, texte |
| 4 | **Remplacer les valeurs** | Valeur | les libellés de familles écrits de quatre façons |
| 5 | **Colonne conditionnelle** | Colonne | le drapeau de retour et le canal de vente |
| 6 | **Fractionner la colonne** | Colonne | `annee_mois` devient une année et un mois |
| 7 | **Colonne personnalisée** | Colonne | `date_mois` = premier jour du mois, pour la table de dates |
| 8 | **Supprimer les colonnes** | Colonne | les colonnes techniques qui ne servent à aucune page |
| 9 | **Renommer** | Colonne | des noms lisibles : `montant_ttc`, pas `mt_ttc_calc_2` |
| 10 | **Filtrer les lignes** | Ligne | retirer les statuts annulés de la requête des commandes |
| 11 | **Dépivoter les colonnes** | Colonne | les douze mois en colonnes deviennent deux colonnes |
| 12 | **Regrouper les lignes** | Ligne | fabriquer le fait mensuel à partir des lignes de vente |
| 13 | **Fusionner les requêtes** | Requête | le coût d'achat entre dans le référentiel produit |
| 14 | **Ajouter les requêtes** | Requête | empiler deux extractions d'années successives |
| 15 | **Paramètre et fonction** | Requête | le chemin du dossier devient un paramètre, la requête une fonction |

**Deux consignes de méthode.** (1) **Nommez chaque étape** : une étape laissée « Personnalisée1 » est une étape que personne ne pourra relire dans six mois. (2) **Une requête qui commence par un filtre** traite moins de lignes qu'une requête qui convertit tout avant de filtrer : l'ordre des étapes change le temps d'actualisation, pas seulement l'élégance.

## 4. Les 10 mesures, avec leur code
| Mesure | Code DAX | Ce qu'elle rend | Définition écrite |
|---|---|---|---|
| **[CA net]** | `CALCULATE(SUM(fait_ventes[montant_ttc]), fait_ventes[est_retour] = 0)` | le chiffre d'affaires hors retours | somme des montants TTC des lignes de vente, retours exclus |
| **[CA HT]** | `CALCULATE(SUM(fait_ventes[montant_ht]), fait_ventes[est_retour] = 0)` | le chiffre d'affaires hors taxes, retours exclus | somme des montants HT, retours exclus : c'est le dénominateur de la marge |
| **[Coût HT]** | `CALCULATE(SUMX(fait_ventes, fait_ventes[quantite] * RELATED(dim_produit[cout_unitaire_ht])), fait_ventes[est_retour] = 0)` | le coût d'achat des marchandises vendues | quantité vendue multipliée par le coût standard du produit, porté par la dimension |
| **[Marge brute]** | `[CA HT] - [Coût HT]` | la marge en valeur | chiffre d'affaires HT moins coût standard des marchandises vendues |
| **[Taux de marge %]** | `DIVIDE([Marge brute], [CA HT])` | la marge en pourcentage | marge brute divisée par le chiffre d'affaires HT : DIVIDE rend un vide au lieu d'une erreur |
| **[Panier moyen]** | `DIVIDE([CA net], DISTINCTCOUNT(fait_ventes[id_ticket]))` | le panier moyen par ticket | chiffre d'affaires net divisé par le nombre de tickets distincts — pas par le nombre de lignes |
| **[Taux de rupture %]** | `DIVIDE(COUNTROWS(fait_ruptures), [Couples servis])` | la part des couples produit-magasin-mois en rupture | couples servis ayant connu au moins un jour de rupture, sur les couples réellement servis |
| **[Taux de retour lignes %]** | `DIVIDE(CALCULATE(COUNTROWS(fait_ventes), fait_ventes[est_retour] = 1), COUNTROWS(fait_ventes))` | la part des lignes de retour | lignes de retour divisées par toutes les lignes : la mesure logistique du retour |
| **[Taux de service %]** | `DIVIDE([Commandes à l'heure], CALCULATE(COUNTROWS(fait_commandes), fait_commandes[statut] = "livree"))` | la part des commandes livrées à la date promise | commandes livrées au plus tard à la date promise, sur les commandes livrées |
| **[Encours client]** | `CALCULATE(SUM(fait_encaissements[montant_ttc]), ISBLANK(fait_encaissements[date_encaissement]))` | le montant des factures non encaissées | montant des factures dont la date d'encaissement est vide : l'encours ouvert |
| **[Coût logistique par colis]** | `DIVIDE(SUM(fait_logistique[cout_total]), SUM(fait_logistique[colis]))` | le coût moyen d'un colis | coût logistique total divisé par le nombre de colis : l'unité est dans le nom |

**Trois avertissements, payés d'avance.**

1. **`DIVIDE` plutôt que `/`** : `DIVIDE` rend un vide au lieu d'une erreur quand le dénominateur est nul, et un rapport qui affiche des erreurs perd la confiance de son lecteur en une seconde.
2. **`RELATED` apparaît une fois** dans ce module, dans `[Coût HT]`, parce que le coût vit dans la dimension produit et pas dans le fait. M15 consacre un chapitre entier à ces fonctions d'itinéraire : ici, une seule ligne suffit.
3. **La part du réseau (Ouaga 2000 : 34,1 % des 15 595 154 955 FCFA) s'affiche par un graphique**, pas par une mesure : un pourcentage du total demande `ALL`, qui est du ressort de M15. Un module qui enseigne `ALL` trop tôt fabrique des mesures que l'apprenant ne sait pas relire.
## 5. Les 3 pages et les 14 visuels
| Page | Visuels | Contenu |
|---|---|---|
| **Direction** | 5 | carte du CA net · jauge de l'objectif atteint · barres du CA par magasin, ordonnées · courbe du CA mensuel · carte du taux de marge |
| **Commercial** | 5 | matrice magasin × famille · barres du panier moyen par magasin · courbe des retours par mois · segment des familles · carte du taux de retour |
| **Approvisionnement** | 4 | carte du taux de rupture · barres des ruptures par famille · nuage couverture × rotation · matrice des ruptures par magasin et mois |
| **Détail** | 2 | détail magasin et détail produit, ouverts par exploration |
| **Aide** | 0 | aucune donnée : les définitions, les exclusions, la fraîcheur |

**Les 4 segments de la page Direction** : période, magasin, famille de produits, segment de client. Ils sont **synchronisés** avec les deux pages de détail, jamais avec la page d'aide.

## 6. Les 4 signets
| # | Signet | Ce qu'il montre |
|---|---|---|
| 1 | **Vue d'ensemble** | les quatre visuels de la page Direction, sans filtre de magasin |
| 2 | **Focus magasin** | le même écran filtré sur le magasin choisi dans le segment |
| 3 | **Détail produit** | l'exploration par clic ouverte depuis la matrice des familles |
| 4 | **Aide à la lecture** | la page qui porte les définitions, les exclusions et la fraîcheur |

## 7. La sécurité et l'actualisation, à documenter dans le dossier

- **Sécurité au niveau des lignes** : le retour n° **2** du comité (« je ne dois voir que mon magasin ») se traite par un rôle qui filtre `dim_magasin` sur l'utilisateur connecté — et par rien d'autre : un filtre posé dans chaque mesure se contourne en changeant de page. Le socle compte **6** magasins, dont **1** dépôt sans vente.
- **Actualisation planifiée** : fréquence, mode (Import), passerelle ou absence de passerelle, qui la surveille et qui prévient en cas d'échec. Un rapport qui se rafraîchit mal sans que personne ne le sache est pire qu'un rapport manuel.
- **Les 7 tests avant mise en production** : les totaux aux trois niveaux, le grain affiché, les vides expliqués, les dates cohérentes, les deux définitions d'un même indicateur, l'ouverture en moins de **3** secondes, et la relecture par un pair avec la grille en **18** points.
