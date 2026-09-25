# Revue de modele — « cinq defauts a trouver » (chapitre C07)

**Le modele ci-dessous est celui d'un stagiaire. Il produit des totaux, il s'ouvre, il a l'air
correct. Il porte cinq defauts qui font des faux totaux — et deux d'entre eux ne se voient pas a
l'oeil nu.**

```sql
CREATE TABLE vente (
    id_vente     INTEGER,
    date_vente   DATE,
    mois         VARCHAR,
    id_magasin   INTEGER,
    id_client    INTEGER,
    nom_client   VARCHAR,
    ville_client VARCHAR,
    id_produit   INTEGER,
    designation  VARCHAR,
    categorie    VARCHAR,
    quantite     DOUBLE,
    montant_ttc  DOUBLE,
    ca_objectif  DOUBLE
);

CREATE TABLE magasin (
    id_magasin INTEGER,
    nom        VARCHAR,
    ville      VARCHAR
);
```

**Defaut 1 — les attributs du client sont dans la table des ventes.** Le nom, la ville et le
segment du client sont recopies sur chaque ligne. Une adresse change : il faut mettre a jour
**240 000** lignes, et oublier une ligne suffit a creer deux villes pour un client. *Correction :
une dimension client, une ligne par client, une cle etrangere dans les faits.*

**Defaut 2 — `mois` est un texte, et `date_vente` est une date : le modele a deux temps.** Les deux
colonnes disent la meme chose autrement, et elles finiront par se contredire (un mois corrige dans
l'une, pas dans l'autre). *Correction : une seule table de dates, et une cle de date dans les faits.*

**Defaut 3 — `ca_objectif` est pose sur la ligne de vente.** L'objectif est un fait au grain
magasin x mois (**218** lignes) ; pose sur **240 000** lignes de vente, il est repete et se somme
avec les ventes : le total du modele vaut alors le chiffre d'affaires **plus 42,9 % d'objectifs**.
*Correction : une table de faits `fait_objectifs` au bon grain, jointe par la cle (magasin, mois).*

**Defaut 4 — aucune cle primaire, aucune cle etrangere.** Rien n'empeche d'ecrire une vente pour un
produit qui n'existe pas, ni le meme identifiant deux fois. *Correction : cles declarees, contrôles
d'unicite et d'orphelins a chaque chargement.*

**Defaut 5 — la categorie est recopiee telle quelle depuis le fichier d'origine.** Elle porte
**16** libelles pour **7** familles : tout tableau par categorie est faux, sans qu'aucune requete ne
soit fausse. *Correction : la correspondance appartient au referentiel, pas a la requete.*

**La grille de revue en 15 points du chapitre C07 reprend chacun de ces defauts**, et les transforme
en questions fermees dont la reponse est une preuve : une requete, un compte, ou un nom.
