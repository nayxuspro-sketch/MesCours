# Sahel Distribution SA — socle de données du manuel

Généré par `generation_socle.py` (graine 20260917) le 17/09/2026. Toute réexécution produit
des fichiers identiques : les chiffres cités dans le manuel restent valables.

## Le scénario
Grossiste en matériaux et quincaillerie. 5 magasins + 1 dépôt central, 3 ans et 8 mois d'historique
(2023-01-01 → 2026-08-31), un système de caisse (export CSV), un fichier d'objectifs tenu par la direction,
un relevé de stocks tenu par le magasinier, et un fichier de remises tenu à la main par une assistante.
L'enjeu du parcours : *le directeur général attribue la baisse de marge aux prix de vente ; l'analyse
devra montrer le rôle du mélange de produits, des remises et des ruptures.*

## Les tables
| table | fichier | grain | lignes (brut / propre) |
|---|---|---|---|
| ventes | `brut/ventes_brutes.csv` | 1 ligne = 1 article d'un ticket | 243360 / 240000 |
| clients | `brut/clients.csv` | 1 ligne = 1 client | 23912 / 23500 |
| produits | `brut/produits.csv` | 1 ligne = 1 référence | 154 / 154 |
| magasins | `brut/magasins.csv` | 1 ligne = 1 point de vente | 6 |
| vendeurs | `brut/vendeurs.csv` | 1 ligne = 1 salarié en vente | 22 |
| objectifs | `brut/objectifs_de_ca.csv` | 1 ligne = 1 magasin × 1 mois | 218 |
| stocks | `brut/stocks_quotidiens.csv` | 1 ligne = 1 produit × 1 dépôt × 1 jour | 60000 |
| coûts d'achat | `brut/couts_achat.csv` | 1 ligne = 1 produit × 1 période de prix | 1694 |
| remises manuelles | `brut/remises_manuelles.xlsx` | 1 ligne = 1 client × 1 mois | 18200 |
| calendrier | `reference/dim_date.csv` | 1 ligne = 1 jour | 1339 |

## Défauts volontairement injectés (corrigé enseignant : `rapport_defauts.json`)
{
  "montants_en_texte": 3360,
  "dates_format_mixte": 2640,
  "lignes_en_double": 3360,
  "remises_aberrantes": 973,
  "clients_non_referentes": 486,
  "produits_categorie_heteroclite": 61,
  "clients_manquants_ville": 1880,
  "doublons_quasi_clients": 412
}

## Règles de gestion (à connaître avant de calculer)
- TVA 18 % ; `montant_ttc = round(montant_ht × 1,18)`, arrondi à l'entier en FCFA.
- `remise` est une proportion (0,08 = 8 %). Les valeurs supérieures à 1 sont une erreur de saisie en points de %.
- Une ligne avec `est_retour = 1` est une marchandise reprise : quantités et montants sont négatifs.
- `id_client = 0` = vente au comptoir sans identification (ce n'est pas une donnée manquante à « remplir »).
- 2026 est une année partielle (janv. → août) : ne jamais comparer 2026 à 2025 en annuel sans le dire.

## L'extrait des modules M01 et M02
- `projection/ventes_magasin5_2025.csv` = **les 40 premières lignes de chaque mois** du magasin 5 en 2025, triées par
  date : 489 lignes avec les défauts, 480 une fois nettoyé. Conséquence pédagogique assumée : l'extrait ne contient
  que les jours 1 à 4 de chaque mois (31 dates distinctes), ce qui enseigne le **biais de couverture** en M02.C07.
- Défauts présents dans cet extrait : 65 dates écrites à la main au format JJ/MM/AAAA, 18 lignes sans identifiant
  client, 7 quantités multipliées par 1000, 9 lignes en double. Le fichier corrigé de référence est
  `reference/ventes_magasin5_2025_ATTENDU.csv` (480 lignes), obtenu en défaisant exactement ces défauts.

## Ce qui n'est PAS dans le jeu (et pourquoi c'est utile)
Aucune table de coûts de structure (loyer, salaires, transport) : la **marge brute** est calculable, la
**marge nette** ne l'est pas. Le manuel s'en sert pour enseigner la limite d'un indicateur.
