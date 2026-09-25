# Module M12.C05 — L'architecture BI de bout en bout

**Outils : DuckDB 1.5.5 (exécuté), pandas (exécuté), Excel (exécuté). Power BI (cité, non exécuté —
règle §1.5). Durée indicative : 5 h. Niveau : N3. Prérequis : M12.C01—C04, M09 (support), M11 (la
matière).**

> **L'idée du chapitre.** Un indicateur ne sort pas de nulle part : il traverse **sept** étages, de la
> source jusqu'au lecteur. Chaque étage a son métier, sa panne typique et son coût. Ce chapitre les
> nomme, les chiffre sur le socle — **240 000** lignes lues en **0,12** s, un socle rejoué en **0,70** s,
> une couche sémantique de **10** indicateurs et **70** cases — et raconte où le dossier raté a payé
> chaque étage sans le construire : **22** jours sur l'écran, **8** sur les sources.

![La chaîne BI en sept étages, de la source à la diffusion, avec la panne typique de chaque étage et les mesures du socle M12 (production : `tools/figures_M12.py`)](../figures/M12_C05_carte_des_sept_etages.svg)

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **nommer les sept étages** d'une chaîne décisionnelle et dire ce que chacun apporte, dans l'ordre :
   source, extraction, stockage, modèle, couche sémantique, visualisation, diffusion ;
2. **reconnaître la panne typique** de chaque étage, et savoir à quel étage un chiffre faux a été
   fabriqué ;
3. **chiffrer une chaîne simple** : volume des sources, temps d'extraction, temps de recalcul complet,
   nombre d'objets du modèle ;
4. **situer la frontière** entre ce qui appartient au module M12 (nommer les étages) et ce qui appartient
   à M13 (construire le modèle) et M14 (outiller la publication) ;
5. **répartir un budget de projet** entre les étages — et constater que le dossier raté a fait l'inverse
   de ce que la mesure recommande ;
6. **détecter les trois pannes qui coûtent le plus** : sources non fiables, couche sémantique absente,
   diffusion sans adoption.

---

## 2. Pourquoi cette notion est importante

Recopions la répartition réelle des **30** jours de travail du dossier raté, en face de ce que la mesure
recommande :

| Poste | Le dossier raté | Ce que dit la mesure |
|---|---|---|
| Reprise et nettoyage des sources | **8** jours | les sources portent **240 000** lignes, **2** prix manquants, **1** client sans fiche : c'est le socle de tout le reste |
| Conception et développement du tableau de bord | **22** jours | **41** indicateurs, **7** onglets, aucun responsable : de la production, pas de la définition |
| Formation | **1** heure, **12** participants, **250 000** FCFA | **14** destinataires, dont **4** ont ouvert le tableau de bord le premier jour |
| Maintenance annuelle | **1 200 000** FCFA | payée **11** semaines, puis résiliée |

Sur **7 940 000** FCFA dépensés, l'étage qui décide du sort de tous les autres — les **sources** — a reçu
**8** jours sur **30**. Et l'étage qui n'existe que si quelqu'un l'ouvre — la **diffusion** — a reçu
**1** heure de formation.

L'architecture n'est donc pas un sujet d'ingénieur : c'est le **plan de dépense** du projet. Nommer les
sept étages sert à savoir où mettre les semaines — et le dossier raté montre à quoi ressemble une
répartition qui ne tient pas.

> **À retenir.** Un dispositif BI ne se casse presque jamais au même endroit que celui où il a été
> construit : **22** jours passés sur l'écran n'ont pas racheté **8** jours de sources, et **1** heure de
> formation n'a pas racheté **14** lecteurs.

---

## 3. Explication simple — sept étages, deux sens

Pensez à un immeuble de sept étages.

- **Au sous-sol, les sources** : les fichiers des caisses, des achats, du stock. Ils existent déjà, ils
  ne nous attendent pas, et ils ne sont pas propres.
- **Au rez-de-chaussée, l'extraction** : on fait entrer les données, on les nettoie, on laisse une trace
  de ce qu'on a nettoyé.
- **Au premier, le stockage** : un endroit stable où les données vivent, qu'on peut rejouer.
- **Au deuxième, le modèle** : on dispose les données en tables qui se répondent — des faits et des
  dimensions.
- **Au troisième, la couche sémantique** : on écrit ce que chaque indicateur veut dire, une fois pour
  toutes.
- **Au quatrième, la visualisation** : on dessine ce qui doit être lu en dix secondes.
- **Au cinquième, la diffusion** : on livre à des gens qui décident — et on vérifie qu'ils l'ouvrent.

**Les données montent : elles entrent au sous-sol et grimpent étage par étage. La décision descend : un
directeur lit au cinquième étage et agit sur le magasin du sous-sol.** Toute la difficulté est là — les
deux flux ne se croisent jamais au même étage, et c'est pourtant la même chaîne.

---

## 4. Vocabulaire essentiel

> **Définition.** Une **chaîne de calcul** — *pipeline* — est la suite d'étapes qui transforme les
> sources brutes en indicateurs publiés : extraction, nettoyage, stockage, modélisation, définition,
> visualisation, diffusion. Une chaîne de calcul se juge à sa capacité à être **rejouée** à l'identique.

> **Définition.** Une **source de vérité** est l'endroit unique où une information est tenue à jour pour
> un usage donné. Sans source de vérité, deux services produisent deux chiffres — et les deux sont
> justes.

> **Définition.** La **gouvernance des données** désigne les règles explicites qui décident qui crée,
> qui modifie, qui valide et qui publie une donnée ou un indicateur. Elle se traduit par des noms, des
> droits et des définitions écrites.

> **Définition.** L'**adoption** est l'usage réel du dispositif par ses destinataires : nombre de
> lecteurs réguliers, fréquence d'ouverture, décisions citant le dispositif. Un tableau de bord livré et
> non ouvert n'a pas d'adoption, donc pas de valeur.

> **Définition.** La **diffusion** est le dernier étage : le choix du support, de la fréquence et du
> moment où l'indicateur atteint son lecteur — courriel, réunion, écran partagé — avec la personne qui
> répond du rendez-vous.

---

## 5. Cours approfondi

### 5.1 Étage 1 — les sources

**Ce que l'étage apporte** : la matière. Rien d'autre ne peut le remplacer ; c'est le seul étage dont
l'absence rend les six autres inutiles.

**Panne typique** : croire une source plus propre qu'elle n'est, ou combler un trou par une recopie. Le
socle du module en porte les marques, toutes mesurées : **2** prix manquants dans le référentiel
produits, **1** dépôt qui ne vend rien, **1** client hors référentiel qui pèse **18,3 %** du chiffre
d'affaires, **16** libellés de catégorie pour **7** familles réelles, un marqueur d'encodage en tête de
trois fichiers.

**Coût** : c'est l'étage qu'on sous-estime. Le dossier raté y a consacré **8** jours sur **30**, au titre
d'une « reprise et nettoyage des sources » facturée **1 640 000** FCFA — le poste le moins cher du devis,
et celui qui a décidé de l'échec.

> **Attention.** Un poste « sources » sous-doté ne se voit pas à la livraison : le tableau de bord
> s'affiche, les chiffres sont là, et c'est **plus tard** que le défaut remonte — une marge qui ne
> correspond pas, une catégorie en double, un client sans fiche qui pèse **18,3 %** du chiffre
> d'affaires. Les **8** jours sur **30** n'ont pas fait échouer le projet le jour de la livraison ; ils
> l'ont fait échouer **11** semaines plus tard, quand plus personne ne pouvait corriger l'étage 1.

### 5.2 Étage 2 — l'extraction

**Ce que l'étage apporte** : faire entrer les données et **laisser une trace** de ce qu'on leur a fait.
Sur le socle, l'extraction des **6** fichiers opérationnels prend **0,12** s, et la lecture des **240 000**
lignes de ventes **0,10** s : lire est rapide. Ce qui est lent, c'est de décider quoi faire des cas
particuliers.

**Panne typique** : nettoyer **sans écrire la règle**. Trois exemples du socle, chacun avec sa règle
explicite :

| Cas rencontré | Règle retenue | Ce que la règle évite |
|---|---|---|
| colonne de date contenant des vides | lire en texte, puis convertir explicitement | l'arrêt brutal du chargement, ou une date inventée |
| deux prix manquants au référentiel | médiane de la sous-catégorie, et mention de l'effet (**29,12 %** contre **29,07 %**) | une marge annoncée sans son approximation |
| marqueur d'encodage en tête de fichier | le déclarer à la lecture | une première colonne corrompue, donc une dimension fausse |

**Coût** : quelques minutes dans l'atelier, des semaines ailleurs. Une règle d'extraction non écrite se
repaie **à chaque nouveau fichier**.

### 5.3 Étage 3 — le stockage

**Ce que l'étage apporte** : un endroit stable, rejouable, où les données vivent entre deux usages. Sur
le socle, le choix est explicite : **aucun fichier de base versionné** (un fichier de base pèse au moins
**512** kilo-octets, et se périme) ; à la place, un **script** de **4 375** octets qui reconstruit les
**8** tables et la vue de marge à partir des sources, en **0,70** s.

**Panne typique** : le stock mort. Un répertoire de fichiers extraits à la main, sans script ni date :
personne ne peut le rejouer, ni savoir de quand il date. C'est le contraire d'un stockage.

**Coût** : près de zéro dans un atelier, très cher dans une entreprise. La règle opérationnelle : *si
vous ne pouvez pas reconstruire le stockage à partir des sources, vous ne stockez pas des données : vous
stockez une opinion.*

### 5.4 Étage 4 — le modèle

**Ce que l'étage apporte** : une forme qui rend les questions simples. Le socle compte **8** tables, **8**
clés uniques — donc huit grains prouvés — et **une** vue supplémentaire pour la marge. Le contrôle de
grain du C03 s'applique ici : chaque table répond à une question et une seule.

**Panne typique** : le **fan-out**, ou jointure à clé incomplète. Joindre les ventes aux ruptures sur le
produit **seul**, en oubliant le mois, multiplie les lignes par **15,9** et le chiffre d'affaires par
**15,8** — **246 567 448 121** FCFA au lieu de **15 595 154 955** — sans qu'aucune erreur ne s'affiche.

**Panne voisine** : mélanger les grains dans une même table, et devoir deviner, à chaque requête, ce que
représente une ligne. C'est la maladie dont le contrôle de clé unique est le vaccin.

**Coût** : une requête fausse coûte une correction ; un modèle faux coûte une **campagne** de corrections.
Sur le dossier raté, la discordance venait précisément de là : deux façons de relier les lignes, deux
chiffres.

### 5.5 Étage 5 — la couche sémantique

**Ce que l'étage apporte** : la définition unique. C'est l'étage que M12 passe son temps à préparer : les
**10** indicateurs du mandat, **7** champs par carte, **70** cases signées. La couche sémantique ne
calcule pas les chiffres : elle décide **quel calcul est le bon** et comment il s'appelle.

**Panne typique** : l'absence pure et simple. Quand elle manque, chaque utilisateur refait la définition
dans son outil, et l'on obtient ce que le socle permet de mesurer sans tricher : le même « taux de
retour » vaut **1,12 %** ou **1,91 %** selon le numérateur, le même panier moyen **107 396** FCFA par
ticket ou **65 749** par ligne, la même marge **29,12 %** hors taxes ou **24,67 %** toutes taxes
comprises.

**Coût** : c'est l'étage le moins cher à construire et le plus cher à omettre. **70** cases de carte
représentent quelques jours ; leur absence a coûté au dossier raté la question la plus importante posée
par sa direction — « où perdons-nous de la marge ? » — restée sans réponse.

### 5.6 Étage 6 — la visualisation

**Ce que l'étage apporte** : rendre le chiffre lisible en dix secondes. Deux principes, tous deux
mesurés ailleurs et vérifiés depuis :

1. **La forme de l'encodage décide de la lecture.** La hiérarchie des perceptions, établie par
   Cleveland et McGill en 1984, place la **position** et la **longueur** devant l'angle et la surface :
   les erreurs de lecture sont **40 à 250 %** plus grandes sur des longueurs comparées mal alignées que
   sur des positions communes, et le camembert est battu par des barres **37** fois sur **40**.
2. **Moins d'objets, plus de lecture.** Le dossier raté a livré **41** indicateurs sur **7** onglets ;
   l'atelier du module publie **2** planches pour **6** chapitres. La contrainte n'est pas esthétique :
   elle est imposée par le lecteur, qui ouvre le dispositif **4** fois le premier jour sur **14**
   destinataires.

**Panne typique** : l'axe tronqué, le camembert à douze parts, le tableau de 40 colonnes — trois façons
de faire dire à un graphique juste une chose fausse.

### 5.7 Étage 7 — la diffusion

**Ce que l'étage apporte** : l'usage. Un indicateur atteint son lecteur à une heure, sur un support, avec
une question à laquelle il répond. Le socle fournit la matière d'un calcul d'adoption : **14**
destinataires, **4** ouvertures le premier jour (**28,6 %** des destinataires), une moyenne quotidienne
qui tombe de **6** à **3** en une semaine — et l'abandon en **11** semaines.

**Panne typique** : confondre **livraison** et **diffusion**. Livrer, c'est envoyer une adresse ; diffuser,
c'est obtenir une lecture. La différence se mesure, et elle se voit dans les chiffres ci-dessus.

**Coût** : la formation d'**1** heure, **12** participants, **250 000** FCFA — et une maintenance de
**1 200 000** FCFA par an payée pour un dispositif que personne n'ouvrait. Le coût de la non-adoption
n'est pas la licence : c'est le projet entier.

> **Attention.** Livrer un lien n'est pas diffuser un indicateur. Les **14** destinataires du dossier
> raté avaient tous reçu l'adresse, et **4** l'ont ouverte : la livraison était parfaite, la diffusion
> nulle. Un dispositif se juge au nombre de décisions qu'il déclenche, pas au nombre de personnes qui
> peuvent y accéder.

### 5.8 Les sept étages en une table

| Étage | Ce qu'il apporte | Sa panne typique | Mesure du socle |
|---|---|---|---|
| 1. Sources | la matière | croire la source propre, combler un trou | **240 000** lignes, **2** prix manquants, **1** client hors référentiel (**18,3 %** du CA) |
| 2. Extraction | l'entrée, avec trace des règles | nettoyer sans écrire la règle | **6** fichiers lus en **0,12** s |
| 3. Stockage | un socle rejouable | le stock mort, non rejouable | **8** tables + **1** vue, script de **4 375** octets, rejoué en **0,70** s |
| 4. Modèle | des grains nets | la clé oubliée : × **15,8** de CA | **8** grains prouvés par **8** clés uniques |
| 5. Couche sémantique | la définition unique | aucune : chacun sa définition | **10** indicateurs, **70** cases, **6** définitions possibles du retour |
| 6. Visualisation | la lecture en dix secondes | l'axe tronqué, le camembert | **2** planches de moins de **776** pixels de large |
| 7. Diffusion | l'usage | livrer sans adopter | **4** ouvertures sur **14** destinataires, abandon en **11** semaines |

**Frontière de module.** C05 **nomme** les étages et leurs pannes ; M13 **construit** le modèle
proprement — schéma en étoile, clés, historisation ; M14 **outille** l'étage 6 et une partie du 5 dans un
outil de restitution ; M15 traitera la qualité et la gouvernance. Aucune capture d'outil ici : le module
M12 reste au niveau des fondamentaux.

---

## 6. Exemple concret — la chaîne du module M12, étage par étage

Le socle de ce module est lui-même une chaîne de calcul, et elle est entièrement mesurable :

| Étage | Ce qui existe dans l'atelier | Mesure |
|---|---|---|
| Sources | les ventes (**26,8** Mo, **240 001** lignes avec l'en-tête) et **6** fichiers opérationnels | **1,33** Mo de sources M12 |
| Extraction | un générateur déterministe, graine **46** | régénération complète en **0,70** s, écart **0** |
| Stockage | `socle_m12.sql` (**4 375** octets) : **8** tables, vues de ventes et de marge | aucun fichier de base |
| Modèle | **8** clés uniques, la vue `vente_marge` pour la marge par famille | grain prouvé table par table |
| Couche sémantique | les **10** cartes du mandat, **7** champs chacune | **239** clés de valeurs publiées dans le relevé du module |
| Visualisation | **2** planches | largeurs **623** et **625** pixels |
| Diffusion | le classeur et les PDF du module | **1** relevé recalculé en **13** s à chaque exécution |

Deux enseignements de ce tableau. D'abord, **la chaîne entière tient dans 1,33 Mo et se rejoue en moins
d'une seconde** : la simplicité n'est pas un luxe d'atelier, c'est ce qui permet de **vérifier** chaque
chiffre publié. Ensuite, le point de contrôle n'est pas l'écran : c'est le **relevé** — **239** valeurs
recalculées à chaque exécution, dont aucune n'est saisie à la main.

> **Dans les faits.** Les sept étages de ce module sont **exécutés**, pas décrits : `tools/dossier_M12.py`
> reconstruit les **6** sources en **0,70** s et contrôle l'écart avec le socle publié, `socle_m12.sql`
> redéclare les **8** tables, `tools/kpi_M12.py` recalcule les **10** cartes, et `tools/figures_M12.py`
> produit la planche de ce chapitre. Rejouer la chaîne complète prend **13** secondes : c'est le prix de
> la vérifiabilité, et il est dérisoire.

---

## 7. Démonstration pas à pas — suivre un chiffre dans les sept étages

Prenons la marge du module — **3 847 989 780** FCFA, soit **29,12 %** du chiffre d'affaires hors taxes —
et suivons-la de bas en haut, en notant à chaque étage ce qui pourrait la casser.

### 7.1 Étage 1 — la source

Le coût d'achat vient du référentiel produits, **154** lignes, dont **2** sans prix. **Panne** : recopier
le prix de la ligne voisine, et fabriquer une marge plausible.

### 7.2 Étage 2 — l'extraction

Les lignes de vente sont rapprochées du coût par produit. **Panne** : oublier que le référentiel porte un
prix unique alors que les prix de vente montent — d'où la règle d'extraction, publiée avec le chiffre.

### 7.3 Étage 3 — le stockage

Une vue `vente_marge` est construite une fois, et réutilisée par toutes les questions. **Panne** :
recalculer la marge dans chaque rapport, avec chaque fois une variante de la formule.

### 7.4 Étage 4 — le modèle

Le rattachement se fait au grain **ligne de vente × produit**. **Panne** : joindre sur le produit seul
avec une table qui contient plusieurs lignes par produit — le **× 15,8** du C03.

### 7.5 Étage 5 — la couche sémantique

La carte dit : « marge brute = ventes hors taxes moins coût standard × quantité ; base hors taxes ;
exclusions : aucune ». **Panne** : publier **29,12 %** sans dire la base, quand la même marge vaut
**24,67 %** toutes taxes comprises.

### 7.6 Étage 6 — la visualisation

La marge se lit par famille, en barres, sur **16** libellés qu'il faut d'abord replier en **7** familles
réelles. **Panne** : tracer les **16** libellés côte à côte, et faire croire à quatre familles de
peinture différentes.

### 7.7 Étage 7 — la diffusion

La marge part vers les acheteurs, avec le **contre-KPI** — le volume — et l'**action** si le seuil est
franchi. **Panne** : publier la marge seule ; la première décision prise sera d'augmenter les prix sans
regarder les volumes, ce que la mesure de 2023 à 2025 permet justement de surveiller.

**Conclusion de la démonstration** : le même chiffre était en danger **sept** fois. La différence entre
un dispositif qui tient et un dispositif qui s'effondre n'est pas la justesse du calcul — elle est dans
les règles écrites à chaque étage.

---

## 8. Erreurs fréquentes

1. **Ne voir que l'étage 6.** Le tableau de bord est la partie visible ; **22** jours sur **30** y ont été
   consacrés dans le dossier raté.
2. **Confondre source et extraction.** Une source se constate ; une extraction se **décide**, et sa règle
   s'écrit.
3. **Croire que le stockage est un répertoire.** Sans script, le répertoire n'est pas rejouable : ce n'est
   pas un stockage, c'est un historique.
4. **Laisser plusieurs grains dans une table.** Le contrôle de clé unique coûte une requête ; son absence
   coûte des mois.
5. **Faire l'économie de la couche sémantique.** Sans elle, **1,12 %** et **1,91 %** cohabitent.
6. **Multiplier les indicateurs pour couvrir les cas.** **41** indicateurs, **7** onglets, **4** lecteurs.
7. **Dessiner avant de savoir lire.** La position et la longueur se lisent mieux que l'angle et la
   surface, dans cet ordre.
8. **Livrer sans former.** **1** heure, **12** participants : la formation n'est pas un poste à rogner,
   c'est le seul étage qui produit de l'usage.
9. **Oublier la maintenance.** **1 200 000** FCFA par an : une chaîne sans entretien meurt de ses sources.
10. **Ne mesurer que la livraison.** On compte les indicateurs livrés, jamais les décisions prises ; les
    **4** ouvertures du premier jour disent pourtant tout.

---

## 9. Bonnes pratiques professionnelles

- **Parcourir les sept étages dans l'ordre** quand un chiffre est contesté : source, extraction,
  stockage, modèle, sémantique, visuel, diffusion. Le désaccord est presque toujours en amont du visuel.
- **Écrire une règle par cas particulier d'extraction** : date vide, prix manquant, catégorie en double.
- **Stocker en script**, pas en fichiers : le socle du module fait **4 375** octets et se rejoue en
  **0,70** s.
- **Prouver le grain de chaque table** avant de la publier.
- **Publier la définition avec le chiffre** : une carte de **7** champs par indicateur.
- **Chiffrer l'adoption** comme on chiffre la livraison : destinataires, ouvertures, questions posées.

> **Conseil professionnel.** Devant un projet BI, la question la plus utile n'est pas « quel outil ? »
> mais « combien de jours par étage ? ». Le dossier raté a répondu en mettant **22** jours sur l'écran et
> **8** sur les sources ; aucun outil n'aurait sauvé cette répartition.

---

## 10. Exercice guidé

**Énoncé.** On vous demande de reprendre le dossier raté pour une PME de distribution. Répartissez
**30** jours de travail sur les **7** étages et justifiez chaque poste par un risque mesurable.

**Étage 1 — sources (8 jours).** Le socle du module porte **2** prix manquants, **1** client hors
référentiel (**18,3 %** du CA) et **16** libellés pour **7** familles : nettoyer et documenter ces trois
points est un préalable à tout indicateur.

**Étage 2 — extraction (4 jours).** Une règle écrite par cas particulier, et un chargement reproductible
(les **6** fichiers se lisent en **0,12** s, la lenteur est ailleurs).

**Étage 3 — stockage (3 jours).** Un script, pas un répertoire : reconstruire le socle de zéro.

**Étage 4 — modèle (5 jours).** **8** tables, **8** grains prouvés, une table de faits de ventes, une
table de marge ; le contrôle avant/après jointure intégré.

**Étage 5 — couche sémantique (6 jours).** **10** cartes, **7** champs, **70** cases signées — c'est le
poste le plus rentable du projet, et le seul qui supprime les débats de définition.

**Étage 6 — visualisation (3 jours).** Un écran, **10** indicateurs, des barres et des positions plutôt
que des camemberts.

**Étage 7 — diffusion (1 jour + récurrence).** Une heure de formation **avant** la mise en ligne, puis un
rendez-vous mensuel où le dispositif est lu **en séance**, et un compteur d'ouvertures.

**Conclusion.** L'écran passe de **22** jours à **3**, et les définitions de **0** à **6** : le total est
le même, la répartition a changé — et avec elle, la probabilité d'usage.

---

## 11. Exercices autonomes

1. **Les sept étages.** Décrivez une chaîne décisionnelle que vous connaissez et nommez, pour chaque
   étage, ce qui existe et ce qui manque.
2. **Panorama des pannes.** Pour les **10** indicateurs du mandat, dites quel étage peut casser chacun
   d'eux, et par quel mécanisme.
3. **Stockage rejouable.** Chronométrez la reconstruction d'un jeu de données sur votre poste, et
   comparez avec le socle du module (**0,70** s pour **8** tables).
4. **Sémantique.** Prenez deux indicateurs de votre entourage et écrivez leurs cartes : si vous n'arrivez
   pas à remplir les **7** champs, notez précisément ce qui vous manque.
5. **Visualisation.** Sur un graphique existant, remplacez l'encodage par une position ou une longueur, et
   décrivez ce que devient la lecture.
6. **Adoption.** Sur le dossier raté, calculez le taux d'ouverture (**4** sur **14**) et proposez deux
   mesures de diffusion qui l'auraient changé.

---

## 12. Correction détaillée

**Exercice 1.** Attendu : une description où chaque étage est **nommé** et où l'absence est dite sans
détour — par exemple « la source existe mais personne ne documente la règle de nettoyage » (étage 2).

**Exercice 2.** La marge peut casser à l'étage 1 (coût absent), 5 (base non précisée : **29,12 %** ou
**24,67 %**) et 4 (jointure multipliée par **15,8**). Le taux de service peut casser à l'étage 5 en
choisissant les commandes **livrées** (**81,0 %**) plutôt que toutes les commandes (**78,2 %**). Le
taux de retour peut casser à l'étage 5 avec **1,12 %**, **1,16 %**, **1,17 %** ou **1,91 %**.

**Exercice 3.** Attendu : un temps comparable en ordre de grandeur, et surtout la capacité de le
**rejouer** deux fois avec le même résultat.

**Exercice 4.** Les champs les plus souvent impossibles à remplir sont le **responsable** et le
**seuil** : ce sont précisément ceux qui distinguent un indicateur d'un chiffre affiché.

**Exercice 5.** La position commune (barres alignées) remplace l'angle (camembert) : les erreurs de
lecture diminuent d'un facteur **40 à 250 %** selon l'étude de référence. Le classement lu change dans
la majorité des cas (**37** fois sur **40** dans l'expérience d'origine).

**Exercice 6.** Taux d'ouverture : **4** sur **14**, soit **28,6 %**. Deux mesures de diffusion : envoyer
le tableau de bord **avant** la réunion où il sera commenté, et remplacer l'accès libre par **une
question** à laquelle le dispositif répond à date fixe.

---

## 13. Mini-projet de chapitre

**« La carte des sept étages de votre organisation »** (2 h). Reprenez la trame de l'atelier et
remplissez-la pour un cas réel : sources disponibles et leurs défauts connus ; règles d'extraction
écrites ; mode de stockage et sa rejouabilité ; tables et grains ; définitions existantes ; écrans et
leur forme ; destinataires et fréquence. Chaque case non remplie est un **risque** : classez-les par coût
de correction, puis par coût d'absence. Ce document est la matière du livrable P3 du projet.

---

## 14. Résumé du chapitre

| Étage | Ce qu'il apporte | Sa panne | Mesure |
|---|---|---|---|
| 1. Sources | la matière | croire la source propre | **2** prix manquants, **1** client à **18,3 %** du CA |
| 2. Extraction | l'entrée et ses règles | nettoyer sans écrire | **0,12** s pour **6** fichiers |
| 3. Stockage | un socle rejouable | le stock mort | **0,70** s de reconstruction, **4 375** octets de script |
| 4. Modèle | des grains nets | la clé oubliée | × **15,8** de CA sans erreur du moteur |
| 5. Couche sémantique | la définition unique | l'absence | **10** KPI, **70** cases, **6** définitions du retour |
| 6. Visualisation | la lecture en dix secondes | l'axe tronqué | **2** planches sous **776** pixels |
| 7. Diffusion | l'usage | livrer sans adopter | **4** ouvertures sur **14**, abandon en **11** semaines |

## 15. À retenir

> **À retenir.** Une chaîne BI se conçoit **de bas en haut** et se lit **de haut en bas**. L'écran est le
> dernier étage, pas le premier poste de dépense : dans le dossier raté, **22** jours sur **30** y ont été
> consacrés, et le dispositif est mort en **11** semaines.

- **Sept étages, sept pannes** : sources, extraction, stockage, modèle, couche sémantique, visualisation,
  diffusion — chacune a sa mesure dans ce chapitre.
- **Le stockage se rejoue** : **8** tables reconstruites en **0,70** s par un script de **4 375** octets.
- **La couche sémantique est le meilleur rendement du projet** : **70** cases signées suppriment les
  débats de définition (**1,12 %** contre **1,91 %**).
- **La diffusion se mesure** : **4** ouvertures sur **14** destinataires, c'est un signal, pas un détail.

## 16. Évaluation formative

1. Citez les sept étages dans l'ordre, de la source à la diffusion.
2. Que se passe-t-il si l'étage 5 est absent, et comment le mesure-t-on sur le socle ?
3. Pourquoi dit-on que les données montent et que la décision descend ?
4. Quel étage a reçu **22** jours sur **30** dans le dossier raté, et qu'est-ce que cela a produit ?
5. Quelle est la panne typique de l'étage 4, et quel facteur de multiplication produit-elle ?
6. Pourquoi un répertoire de fichiers n'est-il pas un stockage ?
7. Que signifie « rejouable », et comment le vérifie-t-on sur le socle du module ?
8. Deux principes d'encodage visuel : lesquels, et dans quel ordre de performance ?
9. Qu'est-ce qui distingue la livraison de la diffusion, et comment la mesure-t-on ?
10. Le socle tient dans **1,33** Mo et se reconstruit en **0,70** s : en quoi est-ce un argument de
    fiabilité, et non de performance ?

**Corrigé :** 1. Sources, extraction, stockage, modèle, couche sémantique, visualisation, diffusion.
2. Chacun refait la définition : **1,12 %** ou **1,91 %** de taux de retour, **29,12 %** ou **24,67 %** de
marge, **107 396** ou **65 749** FCFA de panier. 3. Parce que la donnée entre au premier étage et que
l'action redescend du dernier : la corruption d'un étage bas ne se voit qu'en haut. 4. L'étage 6, la
visualisation : **41** indicateurs, **7** onglets, et un abandon en **11** semaines. 5. La jointure à clé
incomplète : × **15,9** de lignes, × **15,8** de chiffre d'affaires. 6. Parce qu'il n'est pas
reconstructible : sans script, personne ne sait ce qui a été fait aux lignes, ni quand.
7. Rejouable signifie que deux exécutions donnent le même résultat : le socle se régénère à l'identique
(écart **0**) en **0,70** s. 8. Position, puis longueur, devant angle et surface ; l'écart d'erreur de
lecture va de **40** à **250 %**. 9. La livraison envoie une adresse ; la diffusion obtient une lecture :
**4** ouvertures sur **14** destinataires le premier jour. 10. Parce qu'un socle petit et rapide se
**vérifie** : les **239** valeurs du module sont recalculées en **13** s, donc contrôlées à chaque
exécution, au lieu d'être crues sur parole.
