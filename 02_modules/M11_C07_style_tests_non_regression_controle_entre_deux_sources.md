# Module M11.C07 — La requête comme livrable : style, convention, tests de non-régression

**Outils : DuckDB 1.5.5 (exécuté), SQLite (contrôle croisé, exécuté), PostgreSQL et SQL Server (cités, non exécutés — règle §1.5.
Durée indicative : 3 h. Niveau : N3 → N4. Prérequis : M11.C01 à C06 ; M07.C08 (qualité, contrôles) ;
M05.C07 (documentation d'un classeur).**

> **L'idée du chapitre.** Une requête juste qu'on ne peut pas relire est une requête qu'on ne peut pas
> corriger. Ce dernier chapitre du module traite les requêtes comme des **livrables** : un en-tête qui dit
> la question métier, un nommage qui se relit six mois plus tard, et des **tests de non-régression** qui
> refusent qu'un chiffre publié change sans que personne ne s'en aperçoive. Le module en fournit la preuve
> la plus concrète : `tools/controle_sql_M11.py` rejoue **18** requêtes et confronte chaque résultat au
> fichier publié — **18** contrôles, **18** accords. Et il porte un avertissement : un test qui **réécrit**
> la requête ne teste plus la même chose. Sur le socle, un classement des clients par nombre de tickets
> classé en ordre croissant au lieu de décroissant donne **23 497** au lieu de **23 444** — même données,
> même requête « à peu près », deux chiffres.

> **Matériel de l'atelier — DuckDB 1.5.5 · socle M11 (`03_exercices/dossier_M11/socle_m11.sql`) ·
> instrument `tools/controle_sql_M11.py`.** Les chiffres de chapitre sont ceux du module, gelés dans
> `chiffres_cites.json` ; les sorties montrées sont celles de l'atelier, exécutées le **24/09/2026**.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **Écrire un en-tête de requête** qui porte la question métier, le périmètre, la date et l'auteur.
2. **Nommer** les étapes, les alias et les colonnes de sortie pour qu'une relecture soit possible.
3. **Appliquer les conventions du manuel** : mots-clés en majuscules, une requête pour une question, pas de
   `SELECT *`, unités déclarées, apostrophes échappées.
4. **Écrire un test de non-régression** qui rejoue une requête et compare son résultat à une valeur publiée.
5. **Construire un contrôle croisé** entre deux sources indépendantes, et **expliquer un écart** au lieu de
   le masquer.
6. **Rejouer une requête à l'identique** dans un test — et savoir ce qu'on mesure quand on la réécrit.
7. **Livrer un rapport SQL** : requêtes, tests, note de méthode, et la liste de ce qui n'a pas été vérifié.

## 2. Pourquoi cette notion est importante

Le module M11 publie **12** rapports, **20** requêtes de référence et **18** requêtes auto-testées. Chaque
chiffre de ces rapports se retrouve un jour dans une réunion, puis dans un budget. Le mode de défaillance
n'est pas l'erreur grossière : c'est le chiffre qui change **sans que personne ne le remarque** — un libellé
corrigé dans le référentiel, une ligne de retour ajoutée, un filtre déplacé d'une clause à l'autre.

Les tests de non-régression existent pour cela, et ils coûtent étonnamment peu : **18** requêtes rejouées,
comparées à un fichier publié, un verdict par ligne et un code de sortie. Le jour où un chiffre bouge, la
cause est identifiée en une minute au lieu d'une réunion.

Le chapitre porte aussi un piège de méthode, mesuré sur le socle. Un contrôle sur le nombre de tickets par
client donne **23 444** si la requête source classe en ordre **décroissant** — et **23 497** si le test la
classe en ordre **croissant**. Personne n'a touché aux données : c'est le test qui a changé de question. Un
test de non-régression qui ne rejoue pas la requête **à l'identique** ne protège rien ; il fabrique des
alertes.

## 3. Explication simple — la fiche de recette et le contrôle qualité

**Une requête livrée, c'est une fiche de recette.** En haut : le nom du plat, pour combien de personnes
(le périmètre), la date, qui l'a écrite. Ensuite les étapes, numérotées et nommées. En bas : ce qui peut
rater. Une requête sans en-tête oblige le suivant à deviner la question — et à la deviner faux.

**Un test de non-régression, c'est le contrôle qualité du rayon.** On ne regoûte pas le plat chaque matin ;
on vérifie que l'étiquette dit la même chose que le contenu. Sur le module : **18** étiquettes, **18**
contenus, et l'accord est vérifié à chaque exécution.

**Un contrôle croisé, c'est peser la farine sur deux balances.** Deux instruments différents, la même
grandeur : si les deux donnent **15 595 154 955** FCFA, on avance ; s'ils diffèrent, on cherche **lequel** a
bougé avant de publier. Le module compare ainsi une mesure DuckDB et une mesure pandas.

## 4. Vocabulaire essentiel

| Terme (français) | Équivalent anglais | Définition en une phrase |
|---|---|---|
| **en-tête de requête** | *query header* | Le bloc de commentaires qui précède une requête : question, périmètre, source, date, auteur. |
| **convention de nommage** | *naming convention* | Les règles partagées sur les noms de tables, de colonnes et d'étapes intermédiaires. |
| **test de non-régression** | *regression test* | Un test qui rejoue une requête et compare son résultat à une valeur attendue. |
| **valeur attendue** | *expected value* | La valeur publiée à laquelle le test compare le résultat — ici, celle du fichier `chiffres_cites.json`. |
| **contrôle croisé** | *cross-check* | La vérification d'une même grandeur par deux chemins indépendants (deux moteurs, deux méthodes). |
| **code de sortie** | *exit code* | Le signal rendu par un contrôle : zéro si tout passe, non nul sinon — c'est ce qui l'automatise. |
| **jeu de tests** | *test set* | L'ensemble des contrôles d'un module ; ici, **18** requêtes rejouées. |
| **requête à l'identique** | *verbatim replay* | La règle d'or d'un test : rejouer exactement la requête publiée, sans la réécrire. |
| **écart expliqué** | *explained gap* | La différence entre deux socles, documentée (périmètre, période, retours) et jamais additionnée. |

> **Définition.** Un **test de non-régression** est un contrôle qui rejoue une requête **publiée** et
> compare son résultat à une **valeur attendue**. Sa valeur n'est pas de trouver des erreurs : elle est de
> **signaler un changement**. Un test qui échoue ne dit pas « le rapport est faux », il dit « quelque chose a
> bougé, et il faut savoir quoi avant de livrer ». C'est une alerte, pas un verdict.

> **Définition.** Un **contrôle croisé** vérifie une même grandeur par deux chemins **indépendants** :
> deux moteurs (DuckDB et SQLite), deux outils (SQL et pandas), ou deux socles (le socle M11 et celui de
> M09). Il porte une conclusion plus forte qu'un simple test, à une condition : les deux chemins ne doivent
> pas partager la même source d'erreur.

> **Définition.** Le **code de sortie** d'un contrôle est le signal qu'il rend au système : zéro si tous les
> contrôles passent, non nul sinon. C'est ce détail — et non l'affichage — qui rend un jeu de tests
> utilisable dans une chaîne automatique : un rapport qui se construit sans que les contrôles aient tourné
> n'est pas un rapport vérifié.

## 5. Cours approfondi

### 5.1 L'en-tête de requête : la question avant le code

Le manuel impose un en-tête court, en commentaires, à toute requête livrée :

```sql
-- Q07 · Part du chiffre d'affaires des 10 % de clients les plus gros
-- Périmètre : ventes nettes (retours exclus), 01/01/2023 au 31/08/2026, 5 magasins, client 0 inclus
-- Source   : 03_exercices/dossier_M11/socle_m11.sql (vue ventes)
-- Sortie   : une ligne par centile, plus la part cumulée
-- Publié   : 38,1 % (voir chiffres_cites.json, clé m11_concentration_top10_pct)
```

Ces cinq lignes répondent aux cinq questions qu'un relecteur se pose — et elles sont aussi ce dont un test
de non-régression a besoin pour vérifier la **bonne** valeur : une requête sans périmètre écrit ne permet
pas de savoir si les **38,1 %** publiés et les **24,2 %** hors client non identifié parlent du même ensemble.

> **Conseil professionnel.** Écrivez l'en-tête **avant** la requête, pas après. Tant que le périmètre n'est
> pas rédigé, la requête n'est pas finie : c'est en écrivant la ligne « Périmètre » qu'on découvre qu'on
> hésite entre ventes brutes et ventes nettes — et cette hésitation est exactement ce qui fait publier deux
> chiffres différents du même indicateur.

### 5.2 Nommer : les étapes, les alias, les colonnes

Trois règles, et elles suffisent :

1. **Une étape, un nom qui dit son rôle.** `nets`, `ca_mois`, `rang_magasin` — jamais `tmp1`, `tmp2`, `t3`.
2. **Un alias qui se lit à voix haute.** `SUM(montant_ttc) AS ca_net`, et non `AS s`. Une colonne de sortie
   est lue par quelqu'un qui n'a pas écrit la requête.
3. **Un nom de colonne de sortie en français**, comme le reste du manuel : `part_pct`, `rang`, `mois`.

> **Attention.** Un alias muet est un défaut de livraison, pas un détail esthétique. `SELECT COUNT(*) AS n1,
> SUM(x) AS s` sort une table publiée avec deux colonnes nommées `n1` et `s` : l'analyste qui reçoit ce
> fichier doit revenir demander ce que contiennent les colonnes — et il posera la question à quelqu'un qui
> ne se souvient plus.

### 5.3 Un style qui se relit

Les conventions du manuel, appliquées dans tous les chapitres du module :

| Règle | Exemple |
|---|---|
| Mots-clés en majuscules, identifiants en minuscules | `SELECT id_magasin FROM ventes WHERE NOT est_retour` |
| Une requête par question ; une question par requête | Le titre de l'en-tête est une phrase, pas un thème |
| Pas de `SELECT *` dans un rapport | colonnes nommées (C06 : **581** ms contre **96** ms) |
| Alias de table courts mais lisibles | `ventes v JOIN magasin m USING (id_magasin)` |
| Unités écrites dans le nom de la colonne | `ca_net_fcfa`, `part_pct`, `duree_jours` |
| Apostrophes échappées dans les filtres | `mode_paiement = 'Créance 30 j'` — et non des guillemets doubles |
| Découpage en CTE plutôt qu'en requêtes imbriquées | une étape nommée par intention (C05) |

### 5.4 Les trois tests de non-régression du module

Le module en compte **3**, et chacun protège autre chose :

| Test | Ce qu'il protège | Instrument |
|---|---|---|
| Rejeu des **18** requêtes de référence contre les valeurs publiées | les chiffres du module | `tools/controle_sql_M11.py` |
| Comparaison de deux relevés du socle | la stabilité du fichier de valeurs | `chiffres_manuel.py M11` (deux exécutions, `diff` = 0 ligne) |
| Comparaison des deux socles (M11 et M09) | le périmètre des rapports | rapport R12 du projet |

Le premier est exécuté ici, dans son intégralité :

```text
=== controle SQL M11 : 18 requetes, une source par cote ===
  cote SQL   : socle_m11.sql rejoue par DuckDB 1.5.5
  cote publie: chiffres_cites.json (265 cles M11)

  | 1 | m11_lignes                | 240000     | 240000           | OK |
  | 2 | m11_lignes_hors_retours   | 237191     | 237191           | OK |
  | 3 | m11_retours               | 2809       | 2809             | OK |
  | 4 | m11_tickets               | 145212     | 145212           | OK |
  | 5 | m11_clients_vente         | 23497      | 23497            | OK |
  | 6 | m11_magasins              | 5          | 5                | OK |
  | 7 | m11_produits              | 154        | 154              | OK |
  | 8 | m11_ca_2023               | 3443581547 | 3 443 581 547 FCFA | OK |
  | 9 | m11_ca_8_mois_2026        | 3360553372 | 3 360 553 372 FCFA | OK |
  |10 | m11_client0_lignes        | 42658      | 42658            | OK |
  |11 | m11_client0_ca            | 2852612447 | 2 852 612 447 FCFA | OK |
  |12 | m11_c02_max_rank          | 23444      | 23444            | OK |
  |13 | m11_c02_max_dense_rank    | 21         | 21               | OK |
  |14 | m11_c03_ratio_saison      | 1.65       | 1.65             | OK |
  |15 | m11_c04_rfm_blocs         | 7833       | 7 833 / 7 832 / 7 832 | OK |
  |16 | m11_c04_oneshot           | 64         | 64               | OK |
  |17 | m11_c05_grouping_sets_lignes | 47      | 47               | OK |
  |18 | m11_calendrier_jours      | 1339       | 1339             | OK |

  18 controles sur 18 : OK — le socle et le fichier publie disent la meme chose.
```

Ce tableau est un **contrôle croisé**, au sens strict : le côté gauche est une requête exécutée à
l'instant, le côté droit un fichier écrit plus tôt — parfois par une autre exécution, parfois sur une autre
machine (le fichier de valeurs a été produit par `chiffres_manuel.py`). Les deux chemins ne partagent ni le
moment, ni le code : c'est ce qui donne sa valeur à l'accord.

> **Définition.** La **valeur attendue** d'un test est la valeur **publiée** — ici, celle du fichier
> `chiffres_cites.json` — et non la valeur qu'on vient de lire à l'écran. C'est cette distinction qui fait
> la force du contrôle : le test ne compare pas le socle à lui-même, il compare le socle **aujourd'hui** à ce
> que le module affirmait **avant**. Sans valeur attendue écrite quelque part, un test ne peut que constater
> que « ça tourne ».

### 5.5 Le contrôle entre deux sources : expliquer un écart, jamais l'additionner

Le module travaille sur **2** socles. Le socle M11 — celui des chapitres — compte **240 000** lignes de
ventes. Le socle de M07/M09, construit pour la quincaillerie, en compte **50 008** et affiche
**7 908 259 732** FCFA bruts, **7 876 320 165** hors retours. Les additionner n'aurait aucun sens : ils ne
mesurent ni la même période, ni le même périmètre.

Le rapport R12 du projet fait le contraire : il **confronte** les deux et **explique** l'écart — lignes,
retours, magasins, période. C'est le troisième test du module, et le plus formateur : il n'y a pas de
« bonne » réponse à trouver, il y a une différence à documenter. Un rapport qui publie un écart sans
l'expliquer laisse à son lecteur le soin d'imaginer une erreur — et le lecteur imaginera la pire.

### 5.6 Un test rejoue la requête à l'identique

Voici la même question posée à deux ordres de tri près :

```sql
-- version publiée (ordre décroissant) : rang maximum 23444
WITH c AS (SELECT id_client, COUNT(DISTINCT id_ticket) t FROM ventes WHERE NOT est_retour GROUP BY 1),
     r AS (SELECT RANK() OVER (ORDER BY t DESC) rk FROM c) SELECT MAX(rk) FROM r;
-- version « équivalente » écrite dans un test (ordre croissant) : rang maximum 23497
WITH c AS (SELECT id_client, COUNT(DISTINCT id_ticket) t FROM ventes WHERE NOT est_retour GROUP BY 1),
     r AS (SELECT RANK() OVER (ORDER BY t) rk FROM c) SELECT MAX(rk) FROM r;
```

**23 444** contre **23 497**. La première valeur est celle que le module publie (avec **21** comme plus
grand `DENSE_RANK`), la seconde est le nombre de clients — un résultat qui a l'air correct et qui ne répond
pas à la question posée. Un test qui aurait « réécrit proprement » la requête aurait donc signalé un écart
inexistant, ou pire : validé **23 497** et fait diverger le module de son propre fichier.

> **Attention.** Un test de non-régression recopie la requête **caractère pour caractère** — ordre de tri,
> filtre de retour, périmètre, jointure. Toute « amélioration » du texte dans un test est une nouvelle
> requête, donc un nouveau résultat : ce n'est plus un test, c'est une source de bruit. Le corollaire est
> agréable : quand un test échoue, la première chose à vérifier n'est pas la donnée, c'est **la requête du
> test**.

> **Dans les faits.** Le contrôle du module n'a pas seulement validé **18** chiffres : il en a **corrigé**
> un. Le contrôle du client **0** a d'abord compté **43 161** lignes, là où le module publie **42 658** —
> l'écart venait de la requête de contrôle, qui comptait aussi les lignes de retour, alors que la valeur
> publiée est en ventes nettes. La donnée était bonne, la mesure était fausse : c'est exactement ce qu'un
> contrôle croisé doit détecter, et il vaut mieux qu'il le fasse sur un contrôle que sur un rapport.

### 5.7 Ce que ce chapitre ne couvre pas

Les tests d'**intégration** et la chaîne d'automatisation (exécuter les contrôles à chaque modification,
refuser la livraison en cas d'échec, notifier l'équipe) relèvent de l'ingénierie et non de l'analyse : ils
sont cités ici et traités dans l'option M17. Le principe utile à retenir reste accessible : un contrôle qui
ne s'exécute pas tout seul finira par ne plus s'exécuter du tout.

## 6. Exemple concret — la revue d'un rapport avant envoi

Un rapport est prêt. La revue tient en dix minutes et cinq questions, dans cet ordre :

| # | Question | Réponse attendue |
|---|---|---|
| 1 | L'en-tête dit-il la question, le périmètre et la source ? | cinq lignes, pas zéro |
| 2 | Les colonnes de sortie portent-elles leurs unités ? | `ca_net_fcfa`, `part_pct` |
| 3 | Reste-t-il un `SELECT *` ? | non (C06 : **581** ms contre **96** ms) |
| 4 | Les classements ont-ils une clé de départage ? | oui (C04 : **3 316** clients à **8** tickets) |
| 5 | Les chiffres publiés passent-ils les contrôles ? | **18** sur **18** |

Cinq questions, une seule exige un outil, et aucune ne demande de relire la logique métier : c'est le
propre d'une revue utile.

## 7. Démonstration pas à pas — cinq étapes sur le socle

### 7.1 Étape 1 — écrire l'en-tête

La question, le périmètre, la source, la sortie, la valeur publiée : cinq lignes avant la première ligne de
SQL. Sur le socle, la question la plus sensible du module — la concentration — porte deux valeurs selon le
traitement du client non identifié (**38,1 %** ou **24,2 %**) : sans en-tête, on ne sait pas laquelle est
publiée.

### 7.2 Étape 2 — nommer les étapes

La CTE `c` (le client et son nombre de tickets) et la CTE `r` (le rang) du §5.6 : deux étapes, deux noms,
et une requête qui se relit.

### 7.3 Étape 3 — rejouer les 18 contrôles

`python3 tools/controle_sql_M11.py` : **18** contrôles, **18** accords, code de sortie nul. Le tableau du
§5.4 est la sortie réelle de l'atelier.

### 7.4 Étape 4 — comparer les deux socles

**240 000** lignes contre **50 008**, **15 595 154 955** FCFA contre **7 908 259 732** bruts : l'écart
s'explique (période, périmètre, retours) et ne s'additionne pas.

### 7.5 Étape 5 — documenter ce qui n'a pas été testé

PostgreSQL, SQL Server, les partitions, la montée en charge : **cités**, non exécutés. Une note de méthode
qui ne dit que ce qui marche est une publicité, pas une méthode.

## 8. Erreurs fréquentes

1. **Publier une requête sans en-tête.** Le relecteur ne peut ni vérifier le périmètre ni reproduire le
   chiffre (**38,1 %** ou **24,2 %** selon le traitement du client non identifié).
2. **Réécrire la requête dans le test.** **23 444** contre **23 497** pour un ordre de tri inversé : le test
   signale alors un écart qui n'existe pas, et la confiance dans les contrôles en sort abîmée.
3. **Additionner deux socles.** **240 000** lignes et **50 008** lignes ne mesurent pas la même chose : un
   total commun n'a aucun sens, et il est impossible à défendre.
4. **Chercher les erreurs, pas les changements.** Un test de non-régression ne dit pas « c'est faux » : il
   dit « quelque chose a bougé ». Confondre les deux fait ignorer les alertes utiles.
5. **Laisser un contrôle sans code de sortie.** Un contrôle qui affiche « OK » sans rendre de code ne
   s'intègre à rien : il dépend d'un humain qui le lance et qui lit.
6. **Publier des alias muets.** `n1`, `s`, `col3` : le rapport est juste et inutilisable.

## 9. Bonnes pratiques professionnelles

1. **L'en-tête d'abord.** Cinq lignes : question, périmètre, source, sortie, valeur publiée.
2. **Un test recopie la requête à l'identique.** Aucune reformulation, aucun « nettoyage » : le test est un
   témoin, pas une réécriture.
3. **Comparer plutôt qu'additionner.** Deux socles se confrontent et s'expliquent (rapport R12) ; ils ne se
   somment jamais.
4. **Rendre un code de sortie.** Un jeu de tests s'utilise dans une chaîne automatique ou ne sert à rien.
5. **Documenter ce qui n'a pas été vérifié.** Moteurs cités, partitions citées, mesures non faites : la même
   honnêteté que pour les chiffres (§1.5).

## 10. Exercice guidé

**Situation.** Vous reprenez une requête écrite par un collègue : elle calcule la part du chiffre d'affaires
des **10 %** de clients les plus gros, sans en-tête, avec des alias `a`, `b`, `c`, et un `SELECT *` dans une
CTE intermédiaire. Elle donne **38,1 %**.

**Consigne.**

1. Écrivez l'en-tête complet de la requête, périmètre compris. (3 pts)
2. Renommez les étapes et les colonnes de sortie, et justifiez deux de vos choix. (2 pts)
3. Écrivez le contrôle de non-régression associé à cette requête, dans l'esprit de
   `tools/controle_sql_M11.py`. (3 pts)
4. Le même calcul hors client non identifié donne **24,2 %** : comment l'en-tête doit-il le dire, et
   pourquoi ? (2 pts)

## 11. Exercices autonomes

**E1 — Cinq requêtes, cinq en-têtes (40 min).** Reprenez cinq requêtes des chapitres C01 à C06 (celles que
vous avez écrites aux exercices) et ajoutez-leur un en-tête complet. Puis relisez-les une par une et notez
ce que l'en-tête vous a obligé à préciser que la requête laissait implicite.

**E2 — Le jeu de tests d'un rapport (40 min).** Choisissez un des **12** rapports du projet, listez les
valeurs qu'il publie, et écrivez pour chacune un contrôle : la requête rejouée à l'identique, la clé de la
valeur attendue, et ce que l'échec signifierait. Terminez par la phrase qui doit figurer dans la note de
méthode, et par celle qui dit ce que vous n'avez pas testé.

## 12. Correction détaillée

**Exercice guidé.**

1. **L'en-tête.** Question : « part du chiffre d'affaires net des 10 % de clients les plus gros ».
   Périmètre : ventes nettes (retours exclus), 01/01/2023 au 31/08/2026, **5** magasins, **client 0
   inclus**. Source : `socle_m11.sql`. Sortie : une ligne par centile, avec part cumulée. Publié :
   **38,1 %** (`m11_concentration_top10_pct`).
2. **Les noms.** `clients_ca` (le chiffre d'affaires par client) et `deciles` (le découpage en centiles) au
   lieu de `a` et `b` : le nom dit ce que contient l'étape, et la relecture ne demande plus de reconstruire
   le raisonnement. Les colonnes de sortie portent leurs unités : `ca_net_fcfa`, `part_pct`.
3. **Le contrôle.** Rejeu de la requête **à l'identique**, comparaison à la clé publiée, verdict par ligne,
   code de sortie non nul en cas d'écart — la structure de `tools/controle_sql_M11.py` (qui en compte
   **18**).
4. **Le client non identifié.** L'en-tête doit dire que le client **0** est inclus — et donner la valeur
   hors client non identifié (**24,2 %**) dans la note, puisque le retrait est une décision de périmètre :
   sans cette phrase, deux services publieront deux chiffres différents du même indicateur.

**E1 (les en-têtes).** Les points que l'en-tête fait apparaître sont toujours les mêmes : le **périmètre**
(retours inclus ou non), le **grain** (client, ticket, ligne), la **période**, et le **traitement des cas
particuliers** (client **0**, magasin sans objectif, cohorte incomplète). C'est la liste des quatre erreurs
les plus fréquentes du module, et l'en-tête les rend visibles **avant** la publication.

**E2 (le jeu de tests).** Un bon jeu de tests couvre trois natures de valeurs : un **volume** (les
**240 000** lignes, les **145 212** tickets), un **total** (**15 595 154 955** FCFA, **3 443 581 547** pour
2023) et un **taux** (**38,1 %**, **15,8 %** de rétention à M+1). Trois natures, trois façons de casser :
un volume qui bouge signale un changement de filtre ou de source, un total un changement de périmètre, un
taux un changement de dénominateur. Et la phrase de méthode : « les contrôles rejouent les requêtes
publiées à l'identique ; les moteurs cités et non exécutés ne sont pas testés ».

## 13. Mini-projet de chapitre

**La remise en forme d'un rapport existant, 2 pages.** Prenez l'un des **12** rapports du projet de module,
réécrivez-le selon les conventions du chapitre (en-tête, nommage, colonnes nommées) et livrez son jeu de
tests.

**Livrables et barème.**

| Critère | Ce qui est vérifié | Points |
|---|---|---|
| L'en-tête | question, périmètre, source, sortie, valeur publiée | 5 |
| Le style | étapes nommées, alias lisibles, unités dans les noms, aucun `SELECT *` | 4 |
| Les tests | requêtes rejouées **à l'identique**, valeurs attendues citées, code de sortie | 6 |
| La note de méthode | ce qui est vérifié, ce qui ne l'est pas, et la limite du rapport | 3 |
| **Total** | | **18** |

## 14. Résumé du chapitre

Une requête livrée sans en-tête est une requête qu'on ne peut pas vérifier : cinq lignes — question,
périmètre, source, sortie, valeur publiée — suffisent à la rendre reproductible. Le style n'est pas une
coquetterie : les étapes nommées, les alias lisibles et les unités dans les noms de colonnes font la
différence entre un rapport qu'on relit et un rapport qu'on refait. Les **3** tests de non-régression du
module couvrent les chiffres (**18** contrôles rejoués contre le fichier publié), la stabilité du fichier de
valeurs (deux relevés, `diff` = 0 ligne) et le périmètre des rapports (comparaison des deux socles,
**240 000** lignes contre **50 008**). Deux règles portent tout le reste : un test recopie la requête **à
l'identique** — l'ordre de tri inversé donne **23 497** au lieu de **23 444**, et ce n'est pas une erreur de
donnée mais une erreur de test — et un contrôle qui ne rend pas de **code de sortie** ne sert à rien.

## 15. À retenir

1. **L'en-tête d'abord** : la question, le périmètre, la source, la sortie, la valeur publiée.
2. **Un nom dit un rôle.** `clients_ca`, `rang_magasin`, jamais `tmp`, `t3`, `n1`.
3. **Un test rejoue la requête à l'identique.** Réécrire la requête du test, c'est changer de question.
4. **Un test signale un changement, il ne prouve pas une erreur.** C'est une alerte, pas un verdict.
5. **Deux socles se comparent, ils ne s'additionnent pas** : **240 000** lignes contre **50 008**.
6. **Un contrôle rend un code de sortie**, sinon il dépend d'un humain qui se souvienne de le lancer.
7. **La note de méthode dit aussi ce qui n'a pas été testé.**

> **À retenir.** Le chiffre qui résume le chapitre est une paire : **23 444** / **23 497**. Même requête,
> même socle, même question — à un ordre de tri près. Un test qui n'aurait pas recopié la requête publiée
> aurait signalé une fausse alerte, ou validé un chiffre faux. C'est le seul chapitre du module où la
> rigueur porte sur **le contrôle lui-même**.

> **À retenir.** **18** contrôles, **18** accords, et un code de sortie nul : voilà à quoi ressemble un
> module qu'on peut livrer. Le jour où l'un des **18** passe au rouge, on saura **quoi** regarder — et
> c'est tout ce qu'on demande à un test.

## 16. Évaluation formative

Répondez sans machine, puis vérifiez avec l'atelier (5 minutes) :

1. Que contient l'en-tête d'une requête livrée, et pourquoi le périmètre y figure-t-il en premier ?
2. Combien de tests de non-régression compte le module, et que protège chacun ?
3. Combien de contrôles rejoue `tools/controle_sql_M11.py`, et contre quelle source ?
4. Que donne le rang maximum des clients par nombre de tickets en ordre décroissant, et en ordre croissant ?
5. Pourquoi un test de non-régression ne doit-il jamais réécrire la requête qu'il rejoue ?
6. Que fait un contrôle croisé de plus qu'un simple test, et à quelle condition ?
7. Combien de lignes comptent les deux socles du module, et pourquoi ne pas les additionner ?
8. Pourquoi un contrôle doit-il rendre un code de sortie ?
9. Citez trois natures de valeurs qu'un jeu de tests doit couvrir.
10. Que doit dire la note de méthode d'un rapport, en plus de ce qu'il vérifie ?

**Réponses.** 1. Question, périmètre, source, sortie, valeur publiée — le périmètre d'abord, parce que c'est
lui qui décide de la valeur publiée (**38,1 %** ou **24,2 %** selon le client non identifié). 2. **3** : les
chiffres du module, la stabilité du fichier de valeurs, et le périmètre des rapports entre les deux socles.
3. **18** contrôles, contre les valeurs publiées de `chiffres_cites.json` (côté SQL : le socle rejoué).
4. **23 444** en ordre décroissant, **23 497** en ordre croissant. 5. Parce que toute réécriture est une
autre requête : on testerait un résultat qui n'a jamais été publié. 6. Il vérifie une même grandeur par deux
chemins indépendants — à condition que les deux ne partagent pas la même source d'erreur (ici : une requête
exécutée contre un fichier écrit plus tôt). 7. **240 000** lignes et **50 008** : périodes, périmètres et
retours différents — les additionner produirait un total indéfendable. 8. Pour pouvoir l'enchaîner dans un
traitement automatique, sans dépendre d'un humain qui lit la sortie. 9. Un volume, un total, un taux.
10. Ce qui n'a **pas** été vérifié ou exécuté (moteurs cités, partitions, montée en charge).
