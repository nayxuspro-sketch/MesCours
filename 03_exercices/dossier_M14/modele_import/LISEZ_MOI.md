# Les fichiers d'import du rapport M14

**Ces fichiers ne sont pas versionnés.** Le dossier contient **12** tables et **29,3** Mo, dont

**240 000** lignes de ventes : l'atelier vit sous un quota de **128** Mo, et un fichier d'import se
régénère, il ne se stocke pas.

## Les produire

```bash
python3 tools/mesures_M14.py --export                  # écrit dans /tmp/m14_import
python3 tools/mesures_M14.py --export --ou chemin/dir  # écrit ailleurs
```

## Ce que vous obtenez

| Table | Nature | Ce qu'elle porte |
|---|---|---|
| `dim_client.csv` | dimension | **23 913** clients, **8** attributs |
| `dim_produit.csv` | dimension | **154** produits, **11** attributs |
| `dim_magasin.csv` | dimension | **6** points de vente, dont **1** dépôt sans vente |
| `dim_vendeur.csv` | dimension | **22** vendeurs |
| `dim_date.csv` | dimension de temps | **1 339** jours, **15** attributs |
| `fait_ventes.csv` | fait | **240 000** lignes au grain du ticket, **17** colonnes |
| `fait_commandes.csv` | fait | **9 000** commandes, **3** dates |
| `fait_encaissements.csv` | fait | **9 000** factures |
| `fait_ruptures.csv` | fait | **2 428** couples produit-magasin-mois |
| `fait_stock_mensuel.csv` | fait | **6 776** lignes produit-mois |
| `fait_objectifs.csv` | fait | **218** objectifs magasin-mois |
| `fait_logistique.csv` | fait | **264** lignes magasin-mois |

## Dans Power BI

`Accueil > Obtenir les données > Texte/CSV`, un fichier à la fois — ou
`Obtenir les données > Dossier` pour les importer d'un coup, et c'est l'occasion d'écrire le

**paramètre** de chemin du geste n° **15**.

Le format est prévu pour l'import : **UTF-8 avec BOM**, séparateur virgule, en-têtes sur la
première ligne, dates au format ISO. Les **2** prix manquants du référentiel produit
(identifiants `62` et `149`) sont **vides**, et c'est voulu : le module apprend à traiter un
manquant, pas à le masquer.

## La règle du dossier

Un rapport qui dépend d'un fichier doit **savoir d'où il vient**. Écrivez, dans la page d'aide
du rapport : le chemin source, la date de l'extraction, la personne qui la produit, et ce qui
se passe si elle manque.
