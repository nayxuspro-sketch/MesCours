#!/usr/bin/env python3
"""Contrôle Q3 de la porte de module (§G.1) : tout le SQL publié est exécuté.

Le script lit les blocs ```sql des fichiers Markdown du module, dans l'ordre, et les
exécute dans une même session DuckDB. Si `03_exercices/dossier_{module}/commercial.duckdb`
(existe en M07) est présent, il sert de base de travail (lecture seule) ; sinon, session
mémoire vide. Il n'écrit aucune requête lui-même : c'est le texte du manuel qui est
testé, tel que l'apprenant le copie. Un bloc marqué d'un commentaire `-- ERREUR ATTENDUE`
est une démonstration d'erreur : le contrôleur exige que la requête **échoue** (et
compte l'échec comme un succès).

Usage : python3 tools/controle_sql.py M02 [--verif "SELECT ..." 316 114156]
"""
import argparse, glob, pathlib, re, sys

RACINE = pathlib.Path(__file__).resolve().parents[1]

def blocs_sql(fichiers):
    for f in fichiers:
        texte = pathlib.Path(f).read_text(encoding="utf-8").splitlines()
        i = 0
        while i < len(texte):
            j = i
            if texte[i].strip() == "```sql":
                j = i + 1
                while j < len(texte) and texte[j].strip() != "```":
                    j += 1
                yield pathlib.Path(f).name, i + 1, "\n".join(texte[i + 1:j])
            i = j + 1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("module")
    ap.add_argument("--verif", nargs=3, action="append", default=[],
                    help="requête · première valeur attendue · deuxième valeur attendue")
    a = ap.parse_args()
    fs = sorted(glob.glob(str(RACINE / "02_modules" / f"{a.module}_*.md")))
    if not fs:
        raise SystemExit("aucun fichier pour " + a.module)
    import duckdb
    # Base de travail du module (si présente) : lecture seule, tables réelles.
    dossier = RACINE / "03_exercices" / f"dossier_{a.module}"
    con = None
    for nom_base in ("commercial.duckdb", "base.duckdb"):
        p = dossier / nom_base
        if p.exists():
            con = duckdb.connect(str(p), read_only=True)
            print(f"Base chargée : {p.relative_to(RACINE)} (read-only)")
            break
    if con is None:
        con = duckdb.connect()
        print("Aucune base de module trouvée : session DuckDB mémoire vide.")
    ok = ko = 0
    for nom, ligne, sql in blocs_sql(fs):
        entete = f"{nom}:{ligne}"
        if re.search(r"[…]\|\.\.\.", sql):
            print(f"  ~  {entete}  (bloc abrégé, non exécuté)")
            continue
        erreur_attendue = "-- ERREUR ATTENDUE" in sql
        try:
            r = con.execute(sql)
            rows = r.fetchall()
            cols = [d[0] for d in (r.description or [])]
            if erreur_attendue:
                ko += 1
                print(f"  ✘  {entete}  (erreur attendue mais la requête a réussi)")
            else:
                ok += 1
                apercu = " | ".join(", ".join(str(v) for v in x) for x in rows[:3])
                print(f"  ✔  {entete}  {len(rows)} ligne(s)" + (f"  [{', '.join(cols[:5])}]  {apercu[:150]}" if rows else ""))
        except Exception as e:
            if erreur_attendue:
                ok += 1
                print(f"  ✔  {entete}  (erreur attendue obtenue : {str(e).splitlines()[0][:120]})")
            else:
                ko += 1
                print(f"  ✘  {entete}  {type(e).__name__}: {str(e)[:200]}")
    for req, v1, v2 in a.verif:
        try:
            got = con.execute(req).fetchone()
            def bon(a, b):
                try:
                    return abs(float(a) - float(str(b).replace("\u202f", "").replace(" ", ""))) < 0.51
                except Exception:
                    return str(a) == str(b)
            bons = [bon(got[0], v1), bon(got[1], v2)]
            print(f"  {'✔' if all(bons) else '✘'}  vérif {req[:60]}… → {got} (attendu ({v1}, {v2}))")
            ok += sum(bons); ko += 2 - sum(bons)
        except Exception as e:
            ko += 1
            print(f"  ✘  vérif {req[:60]}… → {type(e).__name__}: {str(e)[:120]}")
    print(f"SQL exécuté : {ok} réussite(s), {ko} échec(s)")
    return 1 if ko else 0

if __name__ == "__main__":
    sys.exit(main())
