#!/usr/bin/env python3
"""Auto-validation des 35 exercices de l'évaluation M07 (épreuve C).

Chaque exercice est une requête SQL exécutée sur la base du module
(`03_exercices/dossier_M07/commercial.duckdb`, lecture seule) et comparée à une
valeur attendue mesurée sur le socle (jamais déduite). Le candidat remplit les
35 réponses ; le contrôleur vérifie.

Usage : python3 tools/controle_exos_M07.py
Sortie : une ligne par exercice (✔/✘ + valeur obtenue) + bilan.
"""
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parents[1]
BD = RACINE / "03_exercices" / "dossier_M07" / "commercial.duckdb"

# (code, libellé, requête, valeur attendue, tolérance absolue)
EXOS = [
    ("E01", "Nombre de ventes", "SELECT COUNT(*) FROM vente", 50008, 0.5),
    ("E02", "CA brut total (FCFA, arrondi)", "SELECT ROUND(SUM(montant_ttc)) FROM vente", 7908259731, 0.5),
    ("E03", "Produits actifs", "SELECT COUNT(*) FROM produit WHERE actif = TRUE", 362, 0.5),
    ("E04", "Clients d'Ouagadougou", "SELECT COUNT(*) FROM client WHERE ville = 'Ouagadougou'", 512, 0.5),
    ("E05", "Ventes un dimanche", "SELECT COUNT(*) FROM vente WHERE EXTRACT(DOW FROM date_vente) = 0", 7136, 0.5),
    ("E06", "Panier moyen (toutes ventes, arrondi)", "SELECT ROUND(AVG(montant_ttc)) FROM vente", 158140, 0.5),
    ("E07", "Montant maximum (FCFA)", "SELECT ROUND(MAX(montant_ttc)) FROM vente", 594363, 0.5),
    ("E08", "Montant minimum (FCFA, arrondi)", "SELECT ROUND(MIN(montant_ttc)) FROM vente", 763, 0.5),
    ("E09", "Top magasin par CA (id)", "SELECT id_magasin FROM vente GROUP BY 1 ORDER BY SUM(montant_ttc) DESC LIMIT 1", 4, 0.5),
    ("E10", "CA du top magasin (FCFA)", "SELECT ROUND(SUM(montant_ttc)) FROM vente WHERE id_magasin = 4", 1596813264, 0.5),
    ("E11", "Ventes de 2025", "SELECT COUNT(*) FROM vente WHERE EXTRACT(YEAR FROM date_vente) = 2025", 24920, 0.5),
    ("E12", "CA de 2026 (FCFA)", "SELECT ROUND(SUM(montant_ttc)) FROM vente WHERE EXTRACT(YEAR FROM date_vente) = 2026", 3983044060, 0.5),
    ("E13", "Ventes en Espèces (mode 1)", "SELECT COUNT(*) FROM vente WHERE id_mode = 1", 20175, 0.5),
    ("E14", "CA Carte Bancaire (mode 2, FCFA)", "SELECT ROUND(SUM(montant_ttc)) FROM vente WHERE id_mode = 2", 1944001846, 0.5),
    ("E15", "Catégories (> id) avec plus de 6500 ventes",
     "SELECT COUNT(*) FROM (SELECT p.id_categorie FROM vente v JOIN produit p ON p.id_produit = v.id_produit GROUP BY 1 HAVING COUNT(*) > 6500) t", 4, 0.5),
    ("E16", "Ventes de la catégorie Decoration (id 7)",
     "SELECT COUNT(*) FROM vente v JOIN produit p ON p.id_produit = v.id_produit WHERE p.id_categorie = 7", 6798, 0.5),
    ("E17", "Clients avec plafond > 100 000", "SELECT COUNT(*) FROM client WHERE plafond_credit > 100000", 490, 0.5),
    ("E18", "Clients particuliers", "SELECT COUNT(*) FROM client WHERE type_client = 'particulier'", 850, 0.5),
    ("E19", "CA des clients entreprises (FCFA)",
     "SELECT ROUND(SUM(v.montant_ttc)) FROM vente v JOIN client c ON c.id_client = v.id_client WHERE c.type_client = 'entreprise'", 1482606616, 0.5),
    ("E20", "Clients de Koudougou", "SELECT COUNT(*) FROM client WHERE ville = 'Koudougou'", 247, 0.5),
    ("E21", "Ventes de 200 000 FCFA et plus", "SELECT COUNT(*) FROM vente WHERE montant_ttc >= 200000", 15746, 0.5),
    ("E22", "Ventes de moins de 50 000 FCFA", "SELECT COUNT(*) FROM vente WHERE montant_ttc < 50000", 12753, 0.5),
    ("E23", "Ventes du magasin 4 en 2026",
     "SELECT COUNT(*) FROM vente WHERE id_magasin = 4 AND EXTRACT(YEAR FROM date_vente) = 2026", 4997, 0.5),
    ("E24", "CA des produits inactifs (FCFA)",
     "SELECT ROUND(SUM(v.montant_ttc)) FROM vente v JOIN produit p ON p.id_produit = v.id_produit WHERE p.actif = FALSE", 471206245, 0.5),
    ("E25", "CA du meilleur client (FCFA)",
     "SELECT ROUND(SUM(montant_ttc)) FROM vente GROUP BY id_client ORDER BY SUM(montant_ttc) DESC LIMIT 1", 11561026, 0.5),
    ("E26", "Ventes des clients de Bobo-Dioulasso",
     "SELECT COUNT(*) FROM vente v JOIN client c ON c.id_client = v.id_client WHERE c.ville = 'Bobo-Dioulasso'", 18364, 0.5),
    ("E27", "Ventes uniques (dedoublonnage complet, 12 colonnes)",
     "SELECT COUNT(*) FROM (SELECT DISTINCT id_client, id_produit, id_magasin, id_mode, date_vente, date_limite_remise, quantite, prix_unitaire_ht, taux_tva, montant_ttc, montant_remise, est_retour FROM vente) t", 50000, 0.5),
    ("E28", "Ventes uniques (proxy 5 colonnes — piège P1)",
     "SELECT COUNT(*) FROM (SELECT DISTINCT id_client, id_produit, id_magasin, date_vente, montant_ttc FROM vente) t", 49999, 0.5),
    ("E29", "Couples client x produit distincts (piège P5)",
     "SELECT COUNT(*) FROM (SELECT DISTINCT id_client, id_produit FROM vente) t", 47359, 0.5),
    ("E30", "Ventes Bobo x rayon Bricolage (4 jointures, piège P4)",
     "SELECT COUNT(*) FROM vente v JOIN client c ON c.id_client = v.id_client JOIN produit p ON p.id_produit = v.id_produit JOIN categorie cat ON cat.id_categorie = p.id_categorie WHERE c.ville = 'Bobo-Dioulasso' AND cat.rayon = 'Bricolage'", 4568, 0.5),
    ("E31", "Clients ayant acheté les 2 produits les plus chers (P6)",
     "SELECT COUNT(*) FROM client c WHERE NOT EXISTS (SELECT 1 FROM (SELECT id_produit FROM vente ORDER BY montant_ttc DESC LIMIT 2) top WHERE NOT EXISTS (SELECT 1 FROM vente v WHERE v.id_client = c.id_client AND v.id_produit = top.id_produit))", 119, 0.5),
    ("E32", "Lignes de la vue v_ca_mensuel_magasin", "SELECT COUNT(*) FROM v_ca_mensuel_magasin", 120, 0.5),
    ("E33", "Plus gros mois de la vue (FCFA, arrondi)", "SELECT ROUND(MAX(ca_ttc)) FROM v_ca_mensuel_magasin", 78965529, 0.5),
    ("E34", "Ventes au-dessus du panier moyen",
     "SELECT COUNT(*) FROM vente WHERE montant_ttc > (SELECT AVG(montant_ttc) FROM vente)", 20289, 0.5),
    ("E35", "Produits au-dessus du prix moyen de leur rayon",
     "SELECT COUNT(*) FROM produit p WHERE p.prix_vente_ht > (SELECT AVG(prix_vente_ht) FROM produit p2 WHERE p2.id_categorie = p.id_categorie)", 190, 0.5),
]


def main():
    import duckdb
    if not BD.exists():
        raise SystemExit(f"base absente : {BD}")
    con = duckdb.connect(str(BD), read_only=True)
    ok = ko = 0
    print(f"=== Auto-validation M07 · {len(EXOS)} exercices (base commercial.duckdb, read-only) ===")
    for code, lib, sql, attendu, tol in EXOS:
        try:
            got = con.execute(sql).fetchone()[0]
            try:
                diff = abs(float(got) - float(attendu))
            except Exception:
                diff = 0 if got == attendu else float("inf")
            if diff <= tol:
                ok += 1
                print(f"  ✔  {code}  {lib}  →  {got}")
            else:
                ko += 1
                print(f"  ✘  {code}  {lib}  →  {got}  (attendu {attendu})")
        except Exception as e:
            ko += 1
            print(f"  ✘  {code}  {lib}  ERREUR : {str(e).splitlines()[0][:120]}")
    con.close()
    print(f"Bilan : {ok}/{len(EXOS)} réponses conformes" + (f" · {ko} à revoir" if ko else " · tout est vert"))
    return 1 if ko else 0


if __name__ == "__main__":
    sys.exit(main())
