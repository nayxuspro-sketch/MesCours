# Fiche de contrôle — modules M01 et M02

**Porte de validation §G.1 de l'architecture (contrôles Q1 à Q10) · passée le 18 septembre 2026 · 10/10 au vert
sauf un écart ouvert, déclaré en fin de fiche.**

Cette fiche est le document exigé par l'architecture (« fiche de contrôle Q1–Q10 publiée avec le module »). Elle ne
raconte pas les intentions : chaque ligne donne la commande exécutée et ce qu'elle a rendu.

## 1. Les commandes de contrôle, et leur sortie réelle

| Commande | Sortie obtenue le 18 septembre 2026 |
|---|---|
| `python3 01_socle_donnees/scripts/autovalide.py M01 --strict` | `Résultat : OK (0 avertissement(s))` sur 11 fichiers |
| `python3 01_socle_donnees/scripts/autovalide.py M02 --strict` | `Résultat : OK (0 avertissement(s))` sur 10 fichiers |
| `python3 01_socle_donnees/scripts/chiffres_manuel.py M01 M02` (deux exécutions à vide) | 71 clés pour M01, 406 pour M02 ; `diff` du fichier publié = 0 ligne entre les deux passages → les chiffres cités sont reproductibles |
| `python3 tools/controle_sql.py M02` | **9 blocs SQL publiés exécutés, 0 échec**, plus 2 contrôles croisés (`SELECT COUNT(*), ROUND(AVG(panier)) FROM paniers` → 316 et 114 156, les deux nombres annoncés au C02) — DuckDB 1.5.5, session ouverte à la racine du dépôt |
| `python3 tools/controle_sql.py M01` | 0 bloc — aucun SQL n'est publié dans M01, rien à exécuter |
| `python3 tools/controle_python.py M02` | **5 blocs publiés exécutés, 0 défaut** (Python 3.13, pandas, SciPy) |
| `python3 tools/controle_python.py M01` | 0 bloc, même raison |
| `python3 tools/budget_pages.py --mesure` | M01 : 50 164 mots, budget 105 p., dérive **+5 %** · M02 : 55 264 mots, budget 117 p., dérive **+3 %** → « budget additif et conforme à l'architecture » |
| `python3 tools/nb_pages.py 05_livrables/M01.pdf 05_livrables/M02.pdf` | **110** et **113** pages composées |
| `select couche, lignes, ca_ttc from controle_totaux` (base `01_socle_donnees/data/sahel.duckdb`) | `propre 240 000 · 15 419 985 157` et `brut 243 360` — c'est l'assiette sur laquelle les deux modules écrivent |

**Contrôle croisé jugé le plus fort de la série.** Le total du chiffre d'affaires de l'extrait est produit par deux
chemins indépendants : la clé `c02_total_propre` du générateur (36 073 185 FCFA) et la requête `SELECT SUM(montant_ttc)
FROM read_csv(…)` exécutée par le contrôleur SQL sur le fichier lu sur disque (36 073 185 FCFA). Les deux nombres sont
ceux qui apparaissent dans le corrigé du projet.

## 2. Les dix contrôles, un par un

| # | Contrôle (critère de passage) | M01 | M02 | Preuve |
|---|---|---|---|---|
| Q1 | 16/16 blocs, 100 % des objectifs du module portés et prouvés | ✔ 8 fichiers sur 8 | ✔ 8 fichiers sur 8 | R1 d'`autovalide.py` (présence **et ordre** des seize blocs). Portée des objectifs de M02 : décrire → C02-C05 et mini-projets P1-P2 ; relier → C06 et P3 ; inférer et décider → C07-C08, P4, et la page L5 du projet noté |
| Q2 | 0 violation (aucune notion utilisée sans avoir été enseignée) | ✔ | ✔ | Deux violations trouvées et corrigées le 18 septembre : (a) les blocs SQL de C03, C04, C05 et C06 interrogeaient les relations `paniers` et `lignes_ventes` que rien ne créait — un `CREATE OR REPLACE VIEW` est maintenant publié au C02, § « Pour la suite du module » ; (b) le bloc de C04 utilisait `NTILE(10) … GROUP BY ALL`, refusé par DuckDB (`Cannot group on a window clause`) — la fenêtre et l'agrégation sont désormais dans deux étapes, et le chapitre explique pourquoi |
| Q3 | 100 % d'exécution sans erreur (SQL, Python, formules) | ✔ (0 bloc publié) | ✔ 14/14 (9 SQL + 5 Python) | Sorties ci-dessus, § 1. Trois défauts trouvés à cette occasion dans M02 et corrigés : le bloc de simulation de C07 lisait `donnees/reference/…`, chemin qui n'existe pas dans le dépôt (remplacé par le chemin réel du fichier) ; la requête `NTILE` de C04 ; les vues manquantes. Les formules de tableur ne peuvent pas s'exécuter ici (ni Excel, ni LibreOffice dans l'environnement) : les **noms** de fonctions ont été vérifiés le 17 septembre sur la documentation de l'éditeur (les fonctions statistiques récentes ne sont pas traduites en français, les héritées le sont), et les valeurs qu'elles doivent rendre sont recalculées en pandas/DuckDB dans chaque chapitre |
| Q4 | écart 0 avec `verites_terrain.csv`, joints sans perte | ✔ | ✔ | `chiffres_manuel.py` relu deux fois sans dérive (71 et 406 clés) ; les totaux du module descendent de la même lecture que la table `controle_totaux` (240 000 lignes propres, 15 419 985 157 FCFA) ; les mesures ajoutées pour le corrigé de l'évaluation (concentration du chiffre d'affaires, effet du retrait des retours) ont été prises sur le fichier avant publication ; la vérification a invalidé une phrase déjà écrite du corrigé, réécrite avec les nombres mesurés |
| Q5 | 100 % des énoncés corrigés, avec le résultat intermédiaire | ✔ 37/37 | ✔ 40/40 | R5 d'`autovalide.py` : chaque « Exercice c.n » est repris dans le bloc « Correction détaillée » du même chapitre, plus la correction de l'exercice guidé noté sur 10 |
| Q6 | 0 contradiction, une seule définition par terme | ✔ (dans le module) | ✔ (dans le module) | 40 encadrés Définition par module, aucun terme défini deux fois avec un contenu différent à l'intérieur du module ; le contrôle **inter-modules** du glossaire est reporté à l'étape 4 (assemblage), la ligne « écart ouvert » le dit |
| Q7 | 100 % des termes non communs définis au premier emploi | ✔ | ✔ | R7 (couple « français — *english* » exigé à chaque anglicisme, mots doublés, idéogrammes) rendu muet en mode strict. Scan indépendant du 18 septembre sur les 21 fichiers des deux modules : aucun caractère hors latin-1 typographique, un seul doublon signalé et écarté parce que faux (« vous vous postez ») |
| Q8 | 100 % des affirmations d'outil datées ou marquées « à vérifier » | ✔ | ✔ | Toutes les assertions de version des deux modules portent leur date de vérification (17 septembre 2026) ; pour les quatre fonctions de test statistique au tableur, le manuel donne le nom non traduit, le nom hérité traduit, et la mention explicite « à vérifier dans l'assistant de fonction » |
| Q9 | conforme (tables de plus de 6 colonnes avec version alternative, pas d'information par la seule couleur) | ✔ corrigé | ✔ | M02 : 0 tableau de 7 colonnes et plus. M01 : deux tables de 7 colonnes (C05 §5.2, C06 §5.2) portaient l'information sans équivalent court — une « version alternative pour un petit écran » est ajoutée sous chacune le 18 septembre, qui redit le tableau en deux phrases. Aucune information portée par la couleur seule : les encadrés se distinguent par leur titre, les ✔/✘ des tableaux sont des glyphes et non des couleurs |
| Q10 | ≤ 5 passages à relire par module | **écart ouvert** | **écart ouvert** | Voir § 3 |

## 3. Écarts ouverts, publiés ici comme l'exige la porte de module

1. **Q10, test de lecture « débutant simulé ».** Ce contrôle se conduit à la relecture complète d'un module d'une
   traite, ce que la production en cours ne permet pas encore de déclarer tenu. Ce qui a été fait : trois passages
   relus et resserrés sur M02.C08 (l'intervalle qui n'est pas un verdict, l'exercice 8.4 réécrit après mesure, la
   hiérarchie de vendeurs qui n'existe pas), et les scannage qui attrapent les accidents d'écriture (mots doublés,
   caractères parasites, phrases coupées — c'est comme cela qu'a été trouvé et réparé le « d'êtreAbsent » de C07).
   Le test complet est programmé à l'étape 4, sur le texte assemblé, module par module.
2. **Glossaire et index FR/EN (étape 4).** Le contrôle de non-redondance est fait *dans* chaque module ; il n'est pas
   encore fait *entre* modules, parce que le glossaire n'existe pas encore. Aucun terme n'est redéfini ailleurs que
   dans un encadré Définition, ce qui rendra le contrôle mécaniquement possible à l'assemblage.
3. **Ce que cet atelier ne peut pas exécuter : Excel, Power BI, Tableau.** La règle de production l'impose, la fiche
   le rappelle : pour M01 et M02, aucun contenu DAX ni aucune manipulation Power BI n'est publié (ils commencent en
   M08 et M10), et les formules de tableur sont toutes doublées d'un calcul exécuté en SQL ou en Python.

## 4. Ce que la fiche change à la production

Trois choses, à appliquer dès M03 :

- **Un bloc SQL publié sans sa vue est un défaut.** Le contrôleur `tools/controle_sql.py` exécute les chapitres dans
  l'ordre de lecture, dans une seule session : un bloc qui ne passe pas parce qu'une relation manque est signalé.
  Règle de rédaction : *toute relation nommée dans un bloc est créée dans un bloc publié antérieur*.
- **Un nombre cité dans un corrigé est un nombre mesuré.** La concentration du chiffre d'affaires du corrigé de
  l'évaluation M02 (les 32 plus gros tickets, les neuf plus gros, l'effet du retrait des retours sur la borne de
  Tukey) a été écrite de mémoire, puis mesurée : cinq des six nombres n'existaient pas dans le fichier, et le
  dernier changeait le verdict — la borne après retrait des retours ne descend que de 1 271 FCFA et laisse 25
  tickets hors borne, pas 24. Les clés `c05_ca_top32_tickets`,
  `c05_ca_top9_tickets`, `c05_ca_tickets_sup250k`, `c03_borne_hors_tickets_negatifs`,
  `c03_ecart_borne_apres_retrait_negatifs`, `c05_ca_extrait_tickets` portent maintenant ces mesures dans
  `chiffres_cites.{json,md}`, et le contrôle R6 les exige ailleurs dans le manuel.
- **Un écart de format se ferme à la source.** Les deux tableaux de sept colonnes de M01 n'ont pas été réduits au
  scalpel ni supprimés : ils ont reçu une version courte, qui vaut aussi bien pour l'imprimé que pour le téléphone.
