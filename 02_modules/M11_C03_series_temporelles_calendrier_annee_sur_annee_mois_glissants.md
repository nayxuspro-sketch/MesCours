# Module M11.C03 — Le temps en SQL : table calendrier, année sur année, mois glissants, et le mois qui manque

**Outils : DuckDB 1.5.5 (exécuté), SQLite (contrôle croisé, exécuté), PostgreSQL et SQL Server (cités, non exécutés — règle §1.5).
Durée indicative : 4 h. Niveau : N3 → N4. Prérequis : M11.C01 et C02 (fenêtres, cadres, `LAG`) ;
M07.C02 (dates, `WHERE`), M07.C06 (`CASE`) ; M09.C03 (tendance, saisonnalité, bruit).**

> **L'idée du chapitre.** Comparer dans le temps a l'air simple — « cette année contre l'année dernière » —
> et c'est pourtant la famille de requêtes qui produit le plus de chiffres faux de toute la BI, parce que
> **le temps est incomplet** et que rien ne le signale : l'année en cours n'est pas finie, certains mois
> n'ont pas d'objectif, une moyenne mobile de douze mois calculée sur quatre mois reste une moyenne. Le
> socle du module donne à voir les trois cas d'un coup : **44** mois de ventes sans le moindre trou, mais
> **2** mois sans objectif (**magasin 4**, février et mars 2024) — et une comparaison naïve de 2026 à 2025
> qui publie **−28,9 %** là où la comparaison à périmètre égal (huit mois contre huit mois) publie
> **+15,4 %**. Ce chapitre apprend à écrire le temps **explicitement** : un calendrier, un périmètre, un
> compteur de fenêtre.

> **Matériel de l'atelier — DuckDB 1.5.5 · socle M11 (`03_exercices/dossier_M11/socle_m11.sql`, rejoué en
> 0,4 s).** Le socle contient une table `calendrier` (**1 339** jours, du 01/01/2023 au 31/08/2026, avec
> jours fériés et libellés), les **44** mois de ventes (**237 191** lignes nettes, **15 595 154 955** FCFA)
> et **218** lignes d'objectifs mensuels par magasin. Toutes les sorties publiées ici sont celles de
> l'atelier, exécutées le 24/09/2026.

---

## 1. Objectifs du chapitre

À la fin de ce chapitre, vous savez :

1. **Fabriquer un axe de temps complet** — avec `generate_series` ou une table calendrier — et **prouver**
   qu'il couvre la période du rapport.
2. **Détecter un trou de série** : distinguer un mois sans vente (qui n'existe pas toujours) d'un mois sans
   référence en face (objectif, budget, effectif), et le rendre visible par une jointure **externe**.
3. **Comparer deux périodes à périmètre égal** : dire explicitement quels mois sont comparés, et pourquoi
   la comparaison « année complète contre année en cours » est interdite.
4. **Calculer une moyenne mobile** de 3 et de 12 mois, avec le **cadre** qui convient, et **compter les
   lignes** de la fenêtre pour savoir si elle est complète.
5. **Lire la saison** du socle : jour de la semaine (rapport **3,2** entre le meilleur et le pire jour) et
   mois calendaire (rapport **1,65** entre mars et juillet), et s'en servir pour interpréter — pas pour
   excuser.

## 2. Pourquoi cette notion est importante

Une entreprise ne produit pas deux fois la même semaine. Le socle le montre sans ambiguïté : le lundi
rapporte **13 872 370** FCFA par jour de vente, le dimanche **4 322 830** — un rapport de **3,2**. Le mois
de mars vaut en moyenne **433 645 399** FCFA par mois, celui de juillet **262 079 192** — un rapport de
**1,65**. Autrement dit : **comparer deux mois sans regarder le mois**, c'est comparer deux calendriers
différents et appeler cela une tendance.

Par-dessus cette saison, la vraie difficulté est l'**incomplétude**. Trois situations, toutes présentes sur
le socle :

- **La période en cours n'est pas finie.** Les ventes s'arrêtent au 31/08/2026 : 2026 compte **8** mois,
  2025 en compte **12**. Comparer les deux totaux donne **−28,9 %** — une chute spectaculaire qui n'existe
  pas. À périmètre égal (janvier à août), la progression est de **+15,4 %**, cohérente avec les **+15,3 %**
  de 2025 et les **+18,8 %** de 2024 sur la même fenêtre.
- **La référence en face peut manquer.** Les objectifs couvrent **218** couples magasin-mois sur **220** :
  le magasin 4 n'a **pas d'objectif** pour février et mars 2024, alors qu'il y a réalisé **93 749 490** FCFA
  de ventes. Un rapport qui ne joint pas correctement publie soit une ligne à zéro (faux), soit rien du tout
  (invisible).
- **Une fenêtre peut être incomplète.** Une moyenne mobile de douze mois calculée sur un socle qui commence
  n'est complète qu'à partir du douzième mois. Sans compteur, janvier 2023 affiche « moyenne mobile 12 mois »
  d'un seul mois — et personne ne le voit.

## 3. Explication simple — l'agenda et les trous

Prenez un agenda papier de trois ans et demi. Vous y écrivez chaque soir le chiffre d'affaires du jour.

1. **Les pages existent même les jours sans écriture.** C'est tout l'intérêt d'un **calendrier** : il fournit
   les lignes que les ventes n'ont pas créées. Sans lui, un dimanche sans vente disparaît de la moyenne des
   dimanches — et la moyenne monte.
2. **Une page vide n'est pas un zéro.** Un jour sans vente vaut **0** FCFA ; un mois sans objectif vaut
   **inconnu**. Les deux se ressemblent dans un tableur et ne disent pas la même chose : le premier est une
   mesure, le second est une absence de mesure. La jointure externe (`LEFT JOIN`, `FULL OUTER JOIN`) est
   l'outil qui rend cette différence **visible**.
3. **Un agenda qui commence en janvier ne peut pas parler de décembre.** Toute comparaison « même mois,
   année précédente » a besoin de douze mois d'historique avant de pouvoir exister : sur le socle, seuls
  **32** des **44** mois ont un équivalent un an plus tôt. Les douze autres doivent afficher `NULL` et le
  dire.

## 4. Vocabulaire essentiel

| Terme (français) | Équivalent anglais | Définition en une phrase |
|---|---|---|
| **axe de temps** | *time axis* | La liste complète des périodes du rapport, y compris celles sans donnée. |
| **table calendrier** | *date dimension / calendar table* | La table qui contient une ligne par jour (ou par mois) avec ses attributs : année, mois, trimestre, jour férié. |
| **série fabriquée** | *generated series* | Un axe de temps produit par le moteur (`generate_series`) plutôt que lu dans une table. |
| **jointure externe** | *outer join* | Une jointure qui **conserve** les lignes sans correspondance (`LEFT`, `FULL OUTER`) : le seul moyen de voir un trou. |
| **trou de série** | *series gap* | Une période de l'axe sans donnée : soit une absence réelle (pas de vente), soit une absence de mesure (pas d'objectif). |
| **périmètre** | *scope / perimeter* | L'ensemble des lignes comparées ; deux périodes ne se comparent qu'à périmètre égal. |
| **période partielle** | *partial period* | Une période en cours (mois courant, année courante) : sa comparaison à une période complète est fausse par construction. |
| **année sur année** | *year over year* | Comparaison d'une période à la même période de l'année précédente (`LAG(ca, 12)` sur une série mensuelle). |
| **moyenne mobile** | *moving average* | Moyenne calculée sur une fenêtre qui avance (3 mois, 12 mois) : elle lisse le bruit sans supprimer la tendance. |
| **saison** | *seasonality* | La régularité calendaire d'une activité (jour de la semaine, mois, fêtes) : à connaître **avant** d'interpréter un écart. |

> **Définition.** Une **table calendrier** — *date dimension* — est la table de référence du temps : une
> ligne par jour (ici **1 339**), avec ses attributs calculés une fois pour toutes (année, mois, trimestre,
> libellé du jour, indicateur de férié). C'est **elle** qui rend les trous visibles : une jointure externe
> entre le calendrier et les ventes fait apparaître les jours sans vente, que les ventes seules ne peuvent
> pas montrer puisqu'elles ne contiennent que ce qui a eu lieu.

> **Définition.** Le **périmètre** — *scope* — d'une comparaison est l'ensemble des lignes effectivement
> comparables : mêmes mois, même nombre de jours, mêmes magasins, mêmes exclusions. « 2026 contre 2025 »
> n'est pas un périmètre : c'est une phrase incomplète. « janvier à août 2026 contre janvier à août 2025 »
> en est un.

## 5. Cours approfondi

### 5.1 Fabriquer l'axe du temps

Deux façons d'obtenir un axe complet, et elles doivent **concorder** :

```sql
-- 1. la série fabriquée par le moteur
SELECT COUNT(*) FROM generate_series(DATE '2023-01-01', DATE '2026-08-31', INTERVAL 1 DAY);
-- 2. la table de référence du socle
SELECT COUNT(*) FROM calendrier;
```

Les deux rendent **1 339**. Ce contrôle n'est pas une coquetterie : il vérifie que la table de référence et
la période réelle du socle parlent du même monde. Un écart signifie qu'un des deux est périmé — et c'est
exactement le genre d'écart qui fait publier un rapport sur une période que la base ne couvre plus.

Pour un rapport mensuel, on agrège les ventes **par mois** puis on joint le calendrier des mois — ou l'on
utilise directement `date_trunc('month', date_vente)` :

```sql
SELECT strftime(date_trunc('month', date_vente), '%Y-%m') AS mois, SUM(montant_ttc) AS ca
FROM ventes WHERE NOT est_retour GROUP BY 1 ORDER BY 1;
```

**44** lignes. Le socle n'a **aucun** mois sans vente : c'est une chance, et cela doit être vérifié, pas
supposé.

### 5.2 Le trou qu'on ne voit pas : l'objectif manquant

Les ventes couvrent les 44 mois ; les **objectifs** couvrent **218** couples magasin-mois sur les **220**
possibles (5 magasins × 44 mois). Deux lignes manquent : le **magasin 4** en **février** et **mars 2024**.

Une jointure **interne** ne les voit pas — elle ne garde que ce qui existe des deux côtés, donc elle
**supprime** silencieusement les deux mois. Une jointure **externe** les affiche :

```sql
WITH v AS (SELECT id_magasin, strftime(date_trunc('month', date_vente), '%Y-%m') am, SUM(montant_ttc) ca
           FROM ventes WHERE NOT est_retour GROUP BY 1, 2),
     o AS (SELECT id_magasin, annee_mois am, ca_objectif_ttc obj FROM objectif_mois)
SELECT COALESCE(v.id_magasin, o.id_magasin) AS magasin, COALESCE(v.am, o.am) AS mois,
       ROUND(v.ca) AS realise, o.obj AS objectif,
       CASE WHEN o.obj IS NULL THEN 'objectif manquant'
            WHEN v.ca IS NULL THEN 'vente manquante' ELSE 'complet' END AS etat
FROM v FULL OUTER JOIN o ON o.id_magasin = v.id_magasin AND o.am = v.am
WHERE o.obj IS NULL OR v.ca IS NULL;
```

```text
magasin | mois    | realise  | objectif | etat
4       | 2024-02 | 42514372 | NULL     | objectif manquant
4       | 2024-03 | 51235118 | NULL     | objectif manquant
```

**93 749 490** FCFA de ventes sans objectif en face. Le rapport de suivi a maintenant deux choix
intellectuellement honnêtes : exclure ces deux mois **en le disant**, ou les afficher avec un taux de
réalisation vide. Le choix malhonnête — et le plus fréquent — est de laisser la jointure interne les
supprimer, puis d'annoncer « 218 mois suivis, 100 % de couverture ».

> **Attention.** Une jointure interne sur une table de référence **réduit** le périmètre en silence. C'est
> le seul endroit du chapitre où la perte d'information ne produit ni `NULL`, ni erreur, ni ligne
> manquante : il n'y a simplement plus rien à voir. Règle de la maison : **toute jointure vers une table
> de référence se vérifie par un `COUNT(*)` avant et après.**

> **Définition.** Un **trou de série** — *series gap* — est une période de l'axe de temps pour laquelle
> il n'existe **aucune** donnée : soit parce que rien ne s'est produit (un dimanche sans vente), soit parce
> que la mesure n'a pas été faite (un mois sans objectif). La jointure externe les rend **visibles** ; c'est
> sa seule fonction, et c'est suffisant pour la justifier.

### 5.3 Année sur année : le périmètre d'abord

Le socle s'arrête au 31/08/2026. Deux lectures du même chiffre :

| Comparaison | Calcul | Résultat | Verdict |
|---|---|---|---|
| 2026 (8 mois) contre 2025 (12 mois) | 3 360 553 372 contre 4 724 700 286 | **−28,9 %** | faux |
| janvier—août 2026 contre janvier—août 2025 | 3 360 553 372 contre 2 913 055 394 | **+15,4 %** | défendable |

La même année, la même base, deux conclusions opposées. La première n'est pas une erreur de calcul : c'est
une erreur de **périmètre**. Elle est d'autant plus dangereuse qu'elle va dans le sens de la prudence
(« l'activité baisse »), donc personne ne la conteste.

La bonne écriture est une fonction du périmètre, pas du calendrier :

```sql
WITH m AS (SELECT YEAR(date_vente) an, MONTH(date_vente) mo, SUM(montant_ttc) ca
           FROM ventes WHERE NOT est_retour GROUP BY 1, 2)
SELECT an, ROUND(SUM(ca)) AS ca_total, ROUND(SUM(ca) FILTER (WHERE mo <= 8)) AS ca_8_mois
FROM m GROUP BY 1 ORDER BY 1;
```

```text
2023 | 3443581547 | 2127742355
2024 | 4066319750 | 2527257254
2025 | 4724700286 | 2913055394
2026 | 3360553372 | 3360553372
```

La colonne `ca_8_mois` aligne les quatre années sur la même fenêtre — **8,8 %**, **+15,3 %**, **+15,4 %** —
et cette fois 2026 se lit correctement. C'est aussi le contrôle que les trois croissances successives sont
**cohérentes** entre elles.

### 5.4 Moyennes mobiles : la fenêtre pleine et son compteur

Un mois isolé est bruité : sur le socle, la variation mensuelle va de **−12,3 %** à **+27,1 %** en cinq
mois, pour une tendance annuelle de **+16,8 %**. La moyenne mobile existe pour cela :

```sql
WITH m AS (SELECT date_trunc('month', date_vente) mm, SUM(montant_ttc) ca
           FROM ventes WHERE NOT est_retour GROUP BY 1)
SELECT strftime(mm, '%Y-%m') AS mois, ROUND(AVG(ca) OVER (ORDER BY mm
              ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)) AS moyenne_3_mois,
       COUNT(*) OVER (ORDER BY mm ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS lignes_3,
       ROUND(AVG(ca) OVER (ORDER BY mm
              ROWS BETWEEN 11 PRECEDING AND CURRENT ROW)) AS moyenne_12_mois,
       COUNT(*) OVER (ORDER BY mm ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) AS lignes_12
FROM m ORDER BY mm LIMIT 4;
```

```text
2023-01 | 284400304 | 1  | 284400304 | 1
2023-02 | 273791790 | 2  | 273791790 | 2
2023-03 | 293986146 | 3  | 293986146 | 3
2023-04 | 303978243 | 3  | 299083759 | 4
```

La cinquième colonne est la leçon : en janvier 2023, la « moyenne mobile de 12 mois » ne porte que sur
**1** mois ; en avril, sur **4**. Sans le compteur, ces valeurs s'affichent avec la même autorité que
celles des 32 mois complets — et la courbe a l'air de faire le travail pour lequel on l'a tracée.

> **Définition.** Le **cadre de fenêtre** — *window frame* — est la partie de la partition réellement prise
> en compte autour de la ligne courante. `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` désigne trois lignes ;
> `ROWS BETWEEN 11 PRECEDING AND CURRENT ROW` en désigne douze. Le cadre **ne s'étend pas au-delà** des
> lignes existantes : quand il n'y en a qu'une, il n'en prend qu'une.

### 5.5 La saison, à connaître avant d'interpréter

Deux saisons structurent le socle.

**Le jour de la semaine.** Le lundi rapporte **13 872 370** FCFA par jour de vente, le dimanche
**4 322 830** : rapport **3,2**. Un rapport hebdomadaire qui compare « ce lundi » à « ce samedi » mesure
le calendrier, pas l'activité. Le contrôle se fait avec le calendrier du socle :

```sql
SELECT c.libelle_jour, ROUND(SUM(v.montant_ttc) / COUNT(DISTINCT v.date_vente)) AS ca_par_jour
FROM ventes v JOIN calendrier c ON CAST(c.date AS DATE) = v.date_vente
WHERE NOT v.est_retour GROUP BY 1 ORDER BY ca_par_jour DESC;
```

**Le mois calendaire.** Mars vaut en moyenne **433 645 399** FCFA par mois, juillet **262 079 192** :
rapport **1,65**. Un premier trimestre et un troisième trimestre ne se comparent jamais directement.

> **Dans les faits.** L'écart saisonnier (**×1,65** sur le mois, **×3,2** sur le jour) est **plus grand**
> que la croissance annuelle du socle (**+16,8 %**). Autrement dit : sur cette activité, le calendrier pèse
> davantage que la tendance. Toute conclusion tirée d'un mois isolé, sans référence au même mois de l'année
> précédente, a plus de chances de décrire le calendrier que l'entreprise.

### 5.6 Le mois partiel : la dernière ligne du tableau

Un mois n'est comparable à un autre que s'il est **complet**. Août 2026 l'est : **5 022** lignes de vente
du 1er au 31, aucune journée manquante. Mais si le socle s'était arrêté au 15 août, le total du mois aurait
été **environ deux fois** plus petit — et la moyenne mobile de 3 mois, la variation annuelle et la
croissance du trimestre auraient toutes été fausses **en même temps**, sans qu'aucune ne signale l'autre.

> **Attention.** Le dernier point du graphique est presque toujours un mois **partiel**, et c'est celui
> qu'on regarde. Une moyenne mobile qui l'intègre baisse mécaniquement ; une variation annuelle qui l'utilise
> compare un bout de mois à un mois entier. La règle : le dernier point se publie **avec** son nombre de
> jours couverts, ou pas du tout — sur le socle, août 2026 est complet (**5 022** lignes du 1er au 31), donc
> publiable ; un mois arrêté au 15 ne l'aurait pas été.

Le contrôle de complétude coûte une ligne :

```sql
SELECT COUNT(*) AS jours_de_vente, MIN(date_vente), MAX(date_vente)
FROM ventes WHERE NOT est_retour AND date_vente >= DATE '2026-08-01';
```

> **À retenir.** Trois contrôles non négociables avant de publier une comparaison temporelle : la période
> est-elle **couverte** (calendrier), la référence est-elle **présente** (jointure externe), la fenêtre
> est-elle **pleine** (compteur de lignes). Les trois tiennent en trois colonnes, et les trois erreurs
> qu'ils évitent sont invisibles sans eux.

> **Conseil professionnel.** Construisez la table calendrier **une fois** pour tout le service, et non
> une fois par rapport. Elle se vérifie en trois lignes (la période couverte, le nombre de jours, la
> présence des fériés) et se réutilise partout : comparaisons inter-annuelles, moyennes mobiles, jours
> ouvrés, découpages trimestriels. Un rapport qui fabrique son propre axe de temps le fabrique
> différemment des autres — et deux rapports qui ne partagent pas leur calendrier ne se réconcilient
> jamais.

### 5.7 Ce que ce chapitre ne couvre pas

La **rétention** et les **cohortes** (le temps vu par client, et non par période) sont le sujet de C04. La
**prévision** (prolonger une série) appartient à M19. Ici, on ne fait que rendre le temps complet, comparable
et vérifiable.

## 6. Exemple concret — trois lectures de la même année

Un comité de direction demande « où en est l'année 2026 ? ». Le socle permet trois réponses, et une seule
est utilisable :

| Lecture | Requête | Résultat | Ce que ça vaut |
|---|---|---|---|
| Totale | `SUM(montant_ttc)` par année | **3 360 553 372** FCFA | un chiffre, pas une réponse |
| Naïve | 2026 contre 2025 complet | **−28,9 %** | faux (périmètre) |
| À périmètre égal | janvier—août 2026 contre janvier—août 2025 | **+15,4 %** | la réponse |

Et la réponse **s'accompagne** de sa saison : **+15,4 %** se compare à **+15,3 %** (2025) et **+18,8 %**
(2024) sur la même fenêtre de huit mois. La conclusion tenable est donc : « la progression à périmètre égal
est de **+15,4 %**, en très légère décélération par rapport aux **+18,8 %** de 2024 ». C'est une phrase qu'un
décideur peut utiliser — parce qu'elle dit ce qui est comparé.

## 7. Démonstration pas à pas — six étapes sur le socle

### 7.1 Étape 1 — compter l'axe du temps

```sql
SELECT COUNT(*) FROM generate_series(DATE '2023-01-01', DATE '2026-08-31', INTERVAL 1 DAY);
SELECT COUNT(*) FROM calendrier;
```

```text
1339
1339
```

### 7.2 Étape 2 — le CA mensuel, et la preuve qu'il n'y a pas de trou

44 lignes, du `2023-01` au `2026-08`, aucune manquante : la série mensuelle est **dense**.

### 7.3 Étape 3 — les objectifs, et leurs deux trous

C'est le `FULL OUTER JOIN` du §5.2 : **2** lignes d'état `objectif manquant`, magasin 4, février et mars
2024, pour **93 749 490** FCFA de ventes.

### 7.4 Étape 4 — année sur année à périmètre égal

Le tableau du §5.3 : **2 127 742 355** ; **2 527 257 254** ; **2 913 055 394** ; **3 360 553 372** FCFA sur
les huit premiers mois, soit **+18,8 %**, **+15,3 %** et **+15,4 %**.

### 7.5 Étape 5 — moyennes mobiles avec compteurs

Les trois derniers mois du socle, avec des fenêtres **complètes** :

```text
2026-06 | 351152152 | moyenne 3 mois : 423242990  | moyenne 12 mois : 421347035
2026-07 | 328841773 | moyenne 3 mois : 366577753  | moyenne 12 mois : 426175710
2026-08 | 368251515 | moyenne 3 mois : 349415147  | moyenne 12 mois : 431016522
```

La moyenne de 3 mois baisse (**423 242 990** → **349 415 147**) alors que la moyenne de 12 mois monte
(**421 347 035** → **431 016 522**) : le court terme et le long terme ne racontent pas la même chose, et
c'est normal. Une seule des deux courbes ne suffit jamais à décider.

### 7.6 Étape 6 — la saison, pour interpréter

Le jour (rapport **3,2**) et le mois (rapport **1,65**) du §5.5. À partir d'ici, chaque écart publié dans
le module est comparé **au même mois de l'année précédente**, jamais au mois d'avant.

## 8. Erreurs fréquentes

1. **Comparer une période partielle à une période complète.** 2026 compte **8** mois, 2025 en compte
   **12** : la comparaison directe publie **−28,9 %** au lieu de **+15,4 %** à périmètre égal. La faute est
   invisible parce qu'elle va dans le sens de la prudence.
2. **Joindre une table de référence en jointure interne.** Les **2** mois sans objectif du magasin 4
   disparaissent du rapport : **93 749 490** FCFA de ventes s'évaporent sans un message, et la couverture
   annoncée devient « 100 % ».
3. **Publier une moyenne mobile incomplète.** En janvier 2023, une moyenne de 12 mois porte sur **1** mois ;
   en avril, sur **4**. Sans la colonne `COUNT(*) OVER` (même cadre), la courbe est lisse et fausse sur les
   douze premiers points.
4. **Remplacer un `NULL` par zéro.** Un mois sans objectif n'est pas un mois d'objectif nul : publier `0`
   produit un taux de réalisation infini ou nul selon la formule. `NULL` signifie « inconnu » — et
   « inconnu », dans un rapport, se déclare.
5. **Comparer deux mois sans regarder la saison.** Mars (**433 645 399** FCFA par mois) contre juillet
   (**262 079 192**) donne **−40 %** sur un socle en croissance : l'écart est un écart de calendrier.

## 9. Bonnes pratiques professionnelles

1. **Vérifier la couverture de la période avant tout calcul.** Le `MIN`/`MAX` des dates, le nombre de
   jours ou de mois couverts, la comparaison au calendrier de référence : trois requêtes qui coûtent
   quelques secondes et qui conditionnent la validité de tout le reste.
2. **Écrire le périmètre dans le titre du rapport.** « Janvier—août 2026 contre janvier—août 2025 : +15,4 % »
   — le titre porte le périmètre, et personne ne peut plus confondre les deux lectures.
3. **Toujours joindre la saison à la comparaison.** Un écart annuel de **+15,4 %** se lit par rapport à la
   progression des années précédentes sur la même fenêtre (**+15,3 %**, **+18,8 %**), pas dans l'absolu.
4. **Compter les lignes de chaque fenêtre.** Un cadre (`ROWS BETWEEN …`) **et** un `COUNT(*) OVER` avec le
   même cadre : la valeur et sa fiabilité dans la même ligne de résultat.
5. **Déclarer les trous dans la note de méthode.** Deux mois sans objectif, douze mois sans antériorité :
   ce sont des informations sur la base, et elles doivent figurer dans le rapport — pas être lissées.

## 10. Exercice guidé

**Situation.** Le directeur général reçoit un rapport intitulé « **2026 : l'activité recule de 28,9 %** »,
qui compare le chiffre d'affaires 2026 au chiffre d'affaires 2025. Il appelle le service analyse, très
inquiet. Vous avez 15 minutes pour produire une réponse écrite avant son comité.

**Consigne.**

1. Reproduisez le chiffre du rapport. (2 pts)
2. Écrivez la comparaison à périmètre égal, avec le titre que vous proposeriez. (3 pts)
3. Ajoutez la référence des deux années précédentes sur la **même** fenêtre, et dites ce que la comparaison
   des trois progressions apporte. (3 pts)
4. Le DG demande : « pourquoi août 2026 peut-il être comparé à août 2025, alors qu'août 2025 avait
   **31** jours ? » Répondez en une phrase. (2 pts)
5. Citez la requête de contrôle qui prouve qu'aucun mois de ventes ne manque dans la base. (2 pts)

## 11. Exercices autonomes

**E1 — Le tableau de suivi des objectifs, trous compris (40 min).** Produisez, pour le magasin 4, un suivi
mensuel 2024 : réalisé, objectif, taux de réalisation, et une colonne `etat` qui distingue les trois cas
(complet, objectif manquant, vente manquante). Contrainte : la jointure sera **externe**, et le rapport
devra afficher les **2** mois sans objectif — pas les supprimer.

**E2 — Deux moyennes mobiles, une conclusion (35 min).** Pour le réseau entier, produisez la série mensuelle
avec la moyenne mobile de 3 mois et celle de 12 mois, **chacune accompagnée du nombre de lignes de sa
fenêtre**. Puis répondez en trois lignes : que disent les deux courbes sur le dernier trimestre, et pourquoi
ne disent-elles pas la même chose ?

## 12. Correction détaillée

**Exercice guidé.**

1. **Reproduire le chiffre.** `SELECT YEAR(date_vente), SUM(montant_ttc) … GROUP BY 1` donne
   **3 360 553 372** FCFA pour 2026 et **4 724 700 286** FCFA pour 2025, soit **−28,9 %**. Le calcul est
   juste ; la comparaison ne l'est pas.
2. **Le périmètre égal.** Même requête, avec `WHERE MONTH(date_vente) <= 8` avant d'agréger par année :
   **3 360 553 372** contre **2 913 055 394**, soit **+15,4 %**. Titre proposé : « **Janvier—août 2026
   contre janvier—août 2025 : +15,4 %** » — le périmètre est dans le titre, la question de périmètre est
   close.
3. **Les deux années de référence.** Sur la même fenêtre : **+18,8 %** (2024/2023) puis **+15,3 %**
   (2025/2024) puis **+15,4 %** (2026/2025). La progression est **stable**, très légèrement décélérante au
   milieu de la période. C'est le seul énoncé qui survive à une question du comité.
4. **Les 31 jours d'août.** Parce que la comparaison porte sur **les deux années au même mois**, donc sur
   deux mois d'août complets de 31 jours : la longueur du mois est identique des deux côtés, comme le
   nombre de jours fériés.
5. **Le contrôle de complétude.** `44` lignes mensuelles attendues entre `2023-01` et `2026-08` ; la requête
   `SELECT COUNT(DISTINCT date_trunc('month', date_vente)) FROM ventes WHERE NOT est_retour` en rend
   **44** — et le croisement avec le calendrier (1 339 jours) confirme la couverture.

**E1 (le suivi du magasin 4).** La structure attendue est le `FULL OUTER JOIN` du §5.2, avec le `CASE` à
trois états. Les deux lignes sans objectif portent **42 514 372** et **51 235 118** FCFA de réalisé, et le
taux de réalisation doit y être `NULL` — pas `0`, pas « 100 % ». Total des ventes sans objectif :
**93 749 490** FCFA.

**E2 (les deux mobiles).** Au dernier mois du socle, la moyenne de 3 mois vaut **349 415 147** FCFA et celle
de 12 mois **431 016 522** FCFA : la première baisse (elle a « oublié » un mois creux sorti du cadre), la
seconde monte (elle lisse l'année entière). Les deux sont justes ; la première décrit le trimestre, la
seconde la trajectoire. Un rapport qui n'en publie qu'une choisit à la place du lecteur — et le plus souvent
celle qui confirme ce qu'il espérait.

## 13. Mini-projet de chapitre

**La note de conjoncture d'un magasin, 2 pages.** Choisissez un magasin du réseau et produisez sa note de
conjoncture sur le dernier trimestre clos (juin—août 2026), avec le périmètre annoncé et la saison en regard.

**Livrables et barème.**

| Critère | Ce qui est vérifié | Points |
|---|---|---|
| Le tableau mensuel | mois, CA, cumul, moyenne mobile de 3 mois, **avec** le compteur de fenêtre | 6 |
| La comparaison annuelle | les trois mois contre les trois mêmes mois de 2025, variations exactes | 5 |
| Le contrôle de complétude | la requête de couverture (calendrier, 1 339 jours) et sa sortie | 4 |
| La conclusion | une phrase, périmètre annoncé, saison citée, et une limite | 3 |
| **Total** | | **18** |

## 14. Résumé du chapitre

Le temps en SQL se traite en trois gestes : **fabriquer** l'axe (calendrier ou `generate_series`, ici
**1 339** jours qui concordent), **joindre** les données à cet axe en **externe** pour que les trous
apparaissent (les **2** mois sans objectif du magasin 4, **93 749 490** FCFA de ventes sans référence), et
**compter** les lignes de chaque fenêtre pour savoir si elle est pleine. La comparaison temporelle exige un
**périmètre** explicite : 2026 contre 2025 vaut **−28,9 %** ; janvier—août contre janvier—août vaut
**+15,4 %** — même base, deux conclusions, une seule défendable. Les moyennes mobiles lissent le bruit
mensuel (**−12,3 %** à **+27,1 %** d'un mois sur l'autre) mais ne valent qu'avec leur compteur de lignes.
Enfin la **saison** doit être connue avant toute interprétation : **×3,2** entre le lundi et le dimanche,
**×1,65** entre mars et juillet — plus grand que la croissance annuelle du socle (**+16,8 %**), ce qui dit
l'essentiel : sur cette activité, le calendrier pèse plus que la tendance.

## 15. À retenir

1. **Un axe de temps complet est la condition de tout rapport temporel.** Sans calendrier, les périodes
   sans donnée n'existent pas — et l'absence se lit comme une absence de problème.
2. **Toute jointure vers une référence se fait en externe et se vérifie par un comptage.** La jointure
   interne supprime en silence.
3. **Aucune comparaison sans périmètre écrit.** « 2026 contre 2025 » n'est pas un périmètre ; « janvier—août
   contre janvier—août » en est un.
4. **Une fenêtre glissante se publie avec son compteur.** Une moyenne de 12 mois calculée sur 4 mois est une
   moyenne de 4 mois qui porte un mauvais nom.
5. **La saison se connaît avant l'interprétation.** Sur ce socle, le calendrier explique plus d'écart que la
   tendance.

> **À retenir.** Le chiffre qui résume le chapitre n'est pas
> **+15,4 %** : c'est la paire **−28,9 %** / **+15,4 %** — le même socle, la même année, la même question,
> et une phrase dans le titre qui décide laquelle des deux est publiée.

> **À retenir.** Un trou déclaré est une information ; un trou supprimé est une erreur. Les **2** mois du
> magasin 4 sont le seul endroit du socle où la réponse honnête est « je ne sais pas ».

## 16. Évaluation formative

Répondez sans machine, puis vérifiez avec l'atelier (5 minutes) :

1. Combien de jours comptent le calendrier du socle, et combien en rend `generate_series` sur la même
   période ?
2. Combien de mois de ventes manque-t-il sur le socle ? Combien de mois d'objectifs ?
3. Que publie la comparaison du total 2026 au total 2025, et que publie la comparaison à périmètre égal ?
4. Pourquoi une jointure interne sur `objectif_mois` est-elle dangereuse ici ?
5. Que signifie `lignes_12 = 4` en avril 2023 dans la requête de moyenne mobile ?
6. Quel rapport y a-t-il entre le lundi et le dimanche sur ce socle ?
7. Quel rapport entre mars et juillet, et que faut-il en conclure pour un rapport trimestriel ?
8. Combien de mois du socle ont un équivalent un an plus tôt ?
9. Quelle est la progression annuelle moyenne sur ces mois comparables ?
10. Que doit contenir le titre d'un rapport de comparaison temporelle ?

**Réponses.** 1. **1 339** et **1 339** : les deux axes concordent. 2. Aucun mois de ventes (**0** sur
**44**) ; **2** mois d'objectifs (**magasin 4**, février et mars 2024). 3. **−28,9 %** (2026 n'a que huit
mois) ; **+15,4 %** à périmètre égal. 4. Parce qu'elle **supprime** les deux mois sans objectif —
**93 749 490** FCFA de ventes — sans erreur ni `NULL`. 5. Que la « moyenne de 12 mois » ne porte que sur
**4** lignes : la fenêtre n'est pas pleine. 6. **3,2** (**13 872 370** contre **4 322 830** FCFA par jour
de vente). 7. **1,65** (**433 645 399** contre **262 079 192** FCFA par mois) : un premier trimestre ne se
compare pas à un troisième sans correction. 8. **32** des **44** mois. 9. **+16,8 %**. 10. Le **périmètre** :
« janvier—août 2026 contre janvier—août 2025 ».
