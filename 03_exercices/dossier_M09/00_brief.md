# Brief M09 — « 3 heures avec un fichier que personne n'a regardé »

Vous avez reçu **quatre jeux** dans `03_exercices/dossier_M09/` :

| Jeu | Contenu | Ce qu'on en sait |
|---|---|---|
| `quincaillerie/` | l'export CSV de la base des 5 magasins (M07/M08) | le fil rouge du parcours — vous en connaissez déjà les défauts et les totaux |
| `sante/` | un centre de santé : `consultation.csv`, `medicament.csv`, `stock_medicament.csv` | la direction veut savoir **quand le centre est saturé, quels médicaments manquent** |
| `scolaire/` | un établissement : `eleve.csv`, `note.csv`, `absence.csv` | la direction étudie **l'absentéisme et les résultats** d'une session |
| `projet/fichier_inconnu.csv` | un export brut d'un opérateur de mobile money, 6 mois | **personne ne l'a regardé** — le contexte est à découvrir dans le fichier |

Deux consignes avant d'explorer :

1. **Aucun jeu n'est propre par avance.** Les trois jeux satellites portent des défauts
   réels et comptables (manquants, doublons, valeurs impossibles) : l'étape 3 du
   protocole existe pour les trouver **avant** qu'ils ne faussent un chiffre.
2. **L'`ATTENDU.json` n'est pas un corrigé à recopier.** Il contient les mesures de
   référence (côté générateur) ; vous le consultez **après** avoir produit vos propres
   nombres, pour les comparer. Un candidat qui lit l'`ATTENDU` avant d'explorer n'a
   plus rien à rendre.

Le projet (M09.P) impose **3 heures, chronomètre en marche**, sur `fichier_inconnu.csv`
: fiche d'entrée (30 min), rapport des 10 étapes, 4 graphiques par question, note de
conclusions provisoires. À 3 h, on arrête et on rend ce qui est fait.
