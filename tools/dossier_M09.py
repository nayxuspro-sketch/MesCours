#!/usr/bin/env python3
"""
dossier_M09.py — socle du module M09 « Analyse exploratoire de données (EDA) ».

Trois jeux contrastés + le fichier du projet, tous générés de façon **déterministe**
(graine 45, aucun tirage, aucune date système) :

  - quincaillerie/  — réexport de la base M07 figée (comme le dossier M08, même
                      empreinte `b9a8d973…`) : le fil rouge, dont les totaux doivent
                      redonner M07/M08 au FCFA près ;
  - sante/          — un centre de santé : consultations (730 jours), médicaments
                      essentiels et stock quotidien, **ruptures** ;
  - scolaire/       — un établissement : 400 élèves, notes (5 matières × 3 trimestres),
                      absentéisme corrélé (mais non causal) aux résultats ;
  - projet/         — `fichier_inconnu.csv` : un export brut volontairement sale
                      (statuts en 6 graphies, doublons, montants impossibles, colonne
                      inutile) — le « fichier que personne n'a regardé » du M09.P.

Chaque jeu porte des **défauts plantés et comptables** (4 par jeu pour sante et
scolaire, 4 pour le projet) ; leurs comptes exacts sont dans `ATTENDU.json`, et
`chiffres_manuel.py M09` les re-mesure côté pandas — toute divergence lève une erreur
(même principe de croisée que M08).

Usage : python3 tools/dossier_M09.py
Sorties : 03_exercices/dossier_M09/ (voir l'arborescence ci-dessus) + 00_brief.md
Déterminisme : 2 exécutions → diff = 0 ; empreinte sha256 imprimée et dans ATTENDU.
"""
import hashlib
import json
import os

import numpy as np
import pandas as pd

HERE = os.path.abspath(os.path.dirname(__file__))
RACINE = os.path.abspath(os.path.join(HERE, ".."))
SRC_M07 = os.path.join(RACINE, "03_exercices", "dossier_M07")
OUT = os.path.join(RACINE, "03_exercices", "dossier_M09")
SEED = 45

# ----------------------------------------------------------------------------
# Jeu 1 — quincaillerie : réexport déterministe de la base M07 figée
# ----------------------------------------------------------------------------
QUINCAILLERIE_TABLES = ["vente", "client", "produit", "categorie", "magasin",
                        "mode_paiement", "regle_tva", "objectif_magasin"]


def export_quincaillerie():
    import duckdb
    out = os.path.join(OUT, "quincaillerie")
    os.makedirs(out, exist_ok=True)
    con = duckdb.connect(os.path.join(SRC_M07, "commercial.duckdb"), read_only=True)
    empreinte = hashlib.sha256()
    formes = {}
    for table in QUINCAILLERIE_TABLES:
        df = con.execute(f"SELECT * FROM {table}").fetchdf()
        chemin = os.path.join(out, table + ".csv")
        df.to_csv(chemin, index=False, encoding="utf-8")
        formes[table] = [int(len(df)), int(df.shape[1])]
        with open(chemin, "rb") as fh:
            empreinte.update(fh.read())
    con.close()
    return formes, empreinte.hexdigest()[:16] + "…"


# ----------------------------------------------------------------------------
# Jeu 2 — centre de santé
# ----------------------------------------------------------------------------
MOTIFS = ["paludisme", "diarrhee", "fievre", "toux", "suivi_grossesse",
          "vaccination", "maladie_chronique", "autre"]
TRANCHES = ["0-4", "5-14", "15-34", "35-59", "60+"]
# (id, nom, categorie, seuil_alerte)
MEDICAMENTS = [
    ("M01", "Paracétamol", "analgésique", 500),
    ("M02", "Amoxicilline", "antibiotique", 300),
    ("M03", "Artemésine-luméfantrine", "antipaludique", 400),
    ("M04", "SRO (réhydratation orale)", "anti-diarrhéique", 250),
    ("M05", "Métronidazole", "antibiotique", 200),
    ("M06", "Vitamine A", "complément", 300),
    ("M07", "Insuline", "chronique", 80),
    ("M08", "Amlodipine", "chronique", 150),
    ("M09", "Sulfadoxine-pyriméthamine", "antipaludique", 350),
    ("M10", "Ceftriaxone (injectable)", "antibiotique", 120),
    ("M11", "Ocytocine", "obstétrique", 100),
    ("M12", "Cotrimoxazole", "antibiotique", 280),
]
DEMANDE_MED = {"M01": 9, "M02": 6, "M03": 7, "M04": 5, "M05": 4, "M06": 4,
               "M07": 2, "M08": 3, "M09": 5, "M10": 3, "M11": 2, "M12": 3}
STOCK_INITIAL = {"M01": 800, "M02": 500, "M03": 650, "M04": 450, "M05": 380,
                 "M06": 520, "M07": 150, "M08": 300, "M09": 600, "M10": 240,
                 "M11": 190, "M12": 480}
# Ruptures plantées : (medicament, debut, fin) — jours consécutifs à stock 0
RUPTURES = [("M01", "2025-07-14", "2025-07-16"),
            ("M02", "2026-03-02", "2026-03-06"),
            ("M04", "2026-08-10", "2026-08-11")]
# Défauts plantés (comptes exacts dans ATTENDU)
SANTE_MANQUANTS_MOTIF = 23
SANTE_DOUBLONS_STOCK = 7
SANTE_DATE_FUTURE = "2027-01-05"          # 1 consultation, après le « aujourd'hui » du jeu
SANTE_STOCK_NEGATIFS = [("M05", "2025-04-18", -1), ("M07", "2025-10-09", -3),
                        ("M10", "2026-05-21", -2), ("M12", "2026-11-03", -12)]


def generer_sante(rng):
    out = os.path.join(OUT, "sante")
    os.makedirs(out, exist_ok=True)
    jours = pd.date_range("2025-01-01", "2026-12-31")

    # ---- consultations ----
    poids_jour = [1.4, 1.25, 1.2, 1.15, 1.2, 0.7, 0.15]          # lun → dim
    base = 24
    nb_par_jour = []
    for j in jours:
        mois_w = 1.15 if j.month in (6, 7, 8, 9) else (1.08 if j.month in (12, 1) else 1.0)
        bruit = rng.uniform(0.85, 1.15)
        nb_par_jour.append(int(round(base * poids_jour[j.dayofweek] * mois_w * bruit)))
    nb_cons = sum(nb_par_jour)
    idc = np.arange(1, nb_cons + 1)
    dates = np.array([j.strftime("%Y-%m-%d") for j in jours])
    rep = np.repeat(dates, np.array(nb_par_jour))
    heures = rng.choice(["08:00", "09:00", "10:00", "11:00", "12:00", "13:00",
                         "14:00", "15:00", "16:00", "17:00"], size=nb_cons,
                       p=[0.09, 0.12, 0.12, 0.11, 0.05, 0.06, 0.11, 0.11, 0.11, 0.12])
    patients = rng.integers(1, 1501, size=nb_cons)
    motifs = np.array(MOTIFS)[rng.integers(0, len(MOTIFS), size=nb_cons)]
    tranches = np.array(TRANCHES)[rng.choice(len(TRANCHES), size=nb_cons,
                                             p=[0.24, 0.2, 0.26, 0.22, 0.08])]
    agents = rng.integers(1, 7, size=nb_cons)
    df = pd.DataFrame({
        "id_consultation": [f"C{i:06d}" for i in idc],
        "date_consultation": rep, "heure": heures,
        "id_patient": [f"P{p:04d}" for p in patients],
        "motif": motifs, "tranche_age": tranches,
        "id_agent": agents,
    })
    # D2.1 — 23 motifs manquants (indices fixes, tirés par la graine puis triés)
    idx_manq = np.sort(rng.choice(nb_cons, SANTE_MANQUANTS_MOTIF, replace=False))
    df.loc[idx_manq, "motif"] = ""
    # D2.3 — 1 consultation datée dans le futur
    df.loc[0, "date_consultation"] = SANTE_DATE_FUTURE
    df.to_csv(os.path.join(out, "consultation.csv"), index=False, encoding="utf-8")

    # ---- stock des médicaments (flux quotidien cohérent) ----
    lignes_stock = []
    for mid, _nom, _cat, _seuil in MEDICAMENTS:
        stock = STOCK_INITIAL[mid]
        demande = DEMANDE_MED[mid]
        for j in jours:
            sortie = rng.poisson(demande)
            entree = rng.poisson(13 * demande + 8) if j.day % 14 == (int(mid[1:]) % 14) else 0
            stock = stock + entree - sortie
            lignes_stock.append([j.strftime("%Y-%m-%d"), mid, int(entree), int(sortie), int(stock)])
    stk = pd.DataFrame(lignes_stock, columns=["date", "id_medicament", "entree", "sortie", "stock_fin"])
    # Ruptures plantées : le jour `deb`, la sortie épuise le stock (stock_fin = 0),
    # le stock reste à 0 jusqu'à `fin` inclus (aucun flux), la livraison du jour
    # suivant restaure. Les recurrences `stock = prev + entree - sortie` restent
    # cohérentes sur toute la série.
    for mid, deb, fin in RUPTURES:
        veille = (pd.Timestamp(deb) - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        stock_veille = int(stk.loc[(stk["id_medicament"] == mid) & (stk["date"] == veille),
                                   "stock_fin"].iloc[0])
        md = (stk["id_medicament"] == mid) & (stk["date"] == deb)
        stk.loc[md, "sortie"] = stock_veille + int(stk.loc[md, "entree"].iloc[0])
        stk.loc[md, "stock_fin"] = 0
        mw = ((stk["id_medicament"] == mid) & (stk["date"] > deb) & (stk["date"] <= fin))
        stk.loc[mw, ["entree", "sortie", "stock_fin"]] = 0
        apres = (pd.Timestamp(fin) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
        ma = (stk["id_medicament"] == mid) & (stk["date"] == apres)
        stk.loc[ma, "entree"] = max(int(stk.loc[ma, "entree"].iloc[0]), 3 * DEMANDE_MED[mid] + 50)
        stk.loc[ma, "stock_fin"] = int(stk.loc[ma, "entree"].iloc[0]) - int(stk.loc[ma, "sortie"].iloc[0])
    # D2.4 — 4 stocks négatifs (incohérents par construction : défaut de saisie)
    for mid, date, valeur in SANTE_STOCK_NEGATIFS:
        m = (stk["id_medicament"] == mid) & (stk["date"] == date)
        stk.loc[m, "stock_fin"] = valeur
    # D2.2 — 7 doublons exacts de lignes stock (lignes tirées, hors fenêtres)
    hors = ~stk["stock_fin"].isna()
    idx_disp = np.where(hors)[0]
    idx_dbl = np.sort(rng.choice(idx_disp, SANTE_DOUBLONS_STOCK, replace=False))
    stk = pd.concat([stk, stk.iloc[idx_dbl]], ignore_index=True)
    stk = stk.sort_values(["id_medicament", "date"]).reset_index(drop=True)
    stk.to_csv(os.path.join(out, "stock_medicament.csv"), index=False, encoding="utf-8")

    med = pd.DataFrame(MEDICAMENTS, columns=["id_medicament", "nom", "categorie", "seuil_alerte"])
    med.to_csv(os.path.join(out, "medicament.csv"), index=False, encoding="utf-8")

    # ---- mesures pour ATTENDU (côté générateur) ----
    dfc = pd.read_csv(os.path.join(out, "consultation.csv"))
    st = pd.read_csv(os.path.join(out, "stock_medicament.csv"))
    par_jour = dfc.groupby("date_consultation").size()
    defauts = {
        "manquants_motif": int(dfc["motif"].isna().sum()),
        "doublons_stock": int(st.duplicated().sum()),
        "consultations_date_future": int((dfc["date_consultation"] > "2026-12-31").sum()),
        "stocks_negatifs": int((st["stock_fin"] < 0).sum()),
    }
    a = {
        "formes": {
            "consultation": [int(len(dfc)), int(dfc.shape[1])],
            "medicament": [int(len(med)), int(med.shape[1])],
            "stock_medicament": [int(len(st)), int(st.shape[1])],
        },
        "periode": ["2025-01-01", "2026-12-31"],
        "n_consultations_brut": int(len(dfc)),
        "defauts": defauts,
        "median_consultations_par_jour": float(par_jour.median()),
        "moyenne_consultations_par_jour": round(float(par_jour.mean()), 2),
        "pic_mois": par_jour.groupby(par_jour.index.str[:7]).sum().idxmax(),
        "creux_midi": int((dfc["heure"] == "12:00").sum()),
        "jours_consultes": int(par_jour.shape[0]),
        "n_patients_distincts": int(dfc["id_patient"].nunique()),
    }
    for mid, deb, fin in RUPTURES:
        m = (st["id_medicament"] == mid) & (st["stock_fin"] == 0)
        a[f"rupture_{mid}_jours"] = int(m.sum())
    a["rupture_la_plus_longue"] = max(
        int((st[st["id_medicament"] == mid]["stock_fin"] == 0).sum()) for mid, _, _ in RUPTURES)
    mrg = st.merge(med, on="id_medicament")
    a["jours_sous_seuil_alerte"] = int((mrg["stock_fin"] < mrg["seuil_alerte"]).sum())
    return a


# ----------------------------------------------------------------------------
# Jeu 3 — établissement scolaire
# ----------------------------------------------------------------------------
MATIERES = ["maths", "francais", "sciences", "anglais", "histoire_geographie"]
CLASSES = [("5e", 110), ("4e", 105), ("3e", 100), ("2nde", 85)]
T1, T2, T3 = ("2025-09-01", "2025-11-30"), ("2025-12-01", "2026-02-28"), ("2026-03-01", "2026-06-30")
FERIES = ["2025-11-01", "2025-12-25", "2025-12-26", "2026-01-01"]
SCOL_DOUBLONS_ELEVES = 2
SCOL_NOTES_HORS_BORNES = 6
SCOL_ABSENCES_FERIES = 4
SCOL_ABSENTS_NOTES = 3


def generer_scolaire(rng):
    out = os.path.join(OUT, "scolaire")
    os.makedirs(out, exist_ok=True)
    n_eleves = sum(n for _, n in CLASSES)
    ids = [f"E{i + 1:04d}" for i in range(n_eleves)]
    classes = []
    for classe, n in CLASSES:
        classes += [classe] * n
    sexes = np.array(["M", "F"])[rng.choice(2, size=n_eleves, p=[0.52, 0.48])]
    df_e = pd.DataFrame({"id_eleve": ids, "sexe": sexes, "classe": classes})
    # D3.2 — 2 doublons d'élèves (E0107 en conflit de sexe, E0233 identique)
    d107 = df_e[df_e["id_eleve"] == "E0107"].iloc[0]
    d107_b = d107.copy()
    d107_b["sexe"] = "F" if d107["sexe"] == "M" else "M"
    df_e = pd.concat([df_e, pd.DataFrame([d107_b, df_e[df_e["id_eleve"] == "E0233"].iloc[0]])],
                     ignore_index=True)
    df_e.to_csv(os.path.join(out, "eleve.csv"), index=False, encoding="utf-8")

    # capacité latente + effet classe + niveau matière
    a_i = rng.normal(0, 1, n_eleves)
    c_j = {classe: rng.normal(0, 0.6) for classe, _ in CLASSES}
    s_k = {m: rng.normal(0, 0.8) for m in MATIERES}
    lignes = []
    for i, eid in enumerate(ids):
        for tr in (1, 2, 3):
            for k, mat in enumerate(MATIERES):
                note = 10.5 + 2.2 * a_i[i] + 1.2 * c_j[df_e.iloc[i]["classe"]] + \
                    0.8 * s_k[mat] + rng.normal(0, 1.2)
                lignes.append([f"N{i:04d}{tr}{k}", eid, mat, round(float(np.clip(note, 0, 20)), 2), tr])
    df_n = pd.DataFrame(lignes, columns=["id_note", "id_eleve", "matiere", "note", "trimestre"])
    # D3.1 — 6 notes hors bornes (22,5 × 2 ; 25,0 ; -1,5 ; -0,5 ; -3)
    idx_n = np.sort(rng.choice(len(df_n), SCOL_NOTES_HORS_BORNES, replace=False))
    valeurs = [22.5, 22.5, 25.0, -1.5, -0.5, -3.0]
    for idx, val in zip(idx_n, valeurs):
        df_n.loc[idx, "note"] = val
    df_n.to_csv(os.path.join(out, "note.csv"), index=False, encoding="utf-8")

    # ---- absences : propension élevée chez les élèves en difficulté (confond) ----
    # calendrier scolaire = jours ouvrés SANS jours fériés (sinon les absences
    # naturelles tombent sur les fériés et le défaut planté n'est plus comptable)
    jours_scol = pd.bdate_range("2025-09-01", "2026-06-30")
    jours_scol = jours_scol[~jours_scol.strftime("%Y-%m-%d").isin(FERIES)]
    # propension quotidienne d'absence : lognormale légère (σ 0.6), ×2 pour les
    # élèves en difficulté (confond), facteur classe, plafond 0.04/j (sinon la
    # queue produit des « 29 absences au trimestre » irréalistes et masque le
    # défaut planté)
    p_i = np.exp(rng.normal(-4.3, 0.6, n_eleves))
    p_i[a_i < -0.8] *= 2.0
    # effet classe : la 4e est la classe la plus absente (facteur 1.4)
    fact_classe = {"5e": 0.9, "4e": 1.4, "3e": 1.0, "2nde": 0.8}
    p_i = p_i * np.array([fact_classe[c] for c in classes])
    p_i = np.clip(p_i, 1e-4, 0.04)
    evts = []
    n_id = 0
    for i, eid in enumerate(ids):
        n_ev = rng.poisson(p_i[i] * len(jours_scol))
        for _ in range(n_ev):
            j = jours_scol[rng.integers(0, len(jours_scol))]
            tardif = rng.random() < 0.25
            n_id += 1
            evts.append([f"A{n_id:06d}", eid, j.strftime("%Y-%m-%d"),
                         "tardif" if tardif else "absence", 0 if tardif else 1])
    df_a = pd.DataFrame(evts, columns=["id_absence", "id_eleve", "date", "type", "duree_jours"])
    # D3.4 — 3 élèves absents (≥ 12 absences) en T2 mais notés en T2 ; le critère
    # « ≥ 10 absences en T2 » les isole proprement (le naturel plafonne à ~6)
    idx_abs = np.where(a_i < -1.1)[0][:SCOL_ABSENTS_NOTES]
    jours_t2 = pd.bdate_range(*T2)
    jours_t2 = jours_t2[~jours_t2.strftime("%Y-%m-%d").isin(FERIES)]
    for i in idx_abs:
        for _ in range(12):
            n_id += 1
            j = jours_t2[rng.integers(0, len(jours_t2))]
            evts.append([f"A{n_id:06d}", ids[i], j.strftime("%Y-%m-%d"), "absence", 1])
    df_a = pd.DataFrame(evts, columns=["id_absence", "id_eleve", "date", "type", "duree_jours"])
    # D3.3 — 4 absences datées un jour férié
    for f in FERIES:
        n_id += 1
        j = pd.Timestamp(f)
        evts.append([f"A{n_id:06d}", ids[int(rng.integers(0, n_eleves))], f, "absence", 1])
    df_a = pd.DataFrame(evts, columns=["id_absence", "id_eleve", "date", "type", "duree_jours"])
    df_a.to_csv(os.path.join(out, "absence.csv"), index=False, encoding="utf-8")

    # ---- mesures pour ATTENDU (côté générateur) ----
    e2 = pd.read_csv(os.path.join(out, "eleve.csv"))
    n2 = pd.read_csv(os.path.join(out, "note.csv"))
    a2 = pd.read_csv(os.path.join(out, "absence.csv"))
    # « absentéisme » = jours réellement absents (type absence, durée 1 j ; les
    # retards comptent 0 j)
    abs_par_eleve = a2.groupby("id_eleve")["duree_jours"].sum()
    notes_p = n2[(n2["note"] >= 0) & (n2["note"] <= 20)]
    taux = abs_par_eleve.reindex(ids, fill_value=0)
    corr = float(notes_p.groupby("id_eleve")["note"].mean().corr(
        taux.reindex(notes_p.groupby("id_eleve")["note"].mean().index)))
    seg = [int((taux < 2).sum()), int(((taux >= 2) & (taux < 6)).sum()), int((taux >= 6).sum())]
    classe_map = df_e.drop_duplicates("id_eleve").set_index("id_eleve")["classe"]
    classe_map = classe_map.reindex(taux.index)
    a = {
        "formes": {
            "eleve": [int(len(e2)), int(e2.shape[1])],
            "note": [int(len(n2)), int(n2.shape[1])],
            "absence": [int(len(a2)), int(a2.shape[1])],
        },
        "periode": ["2025-09-01", "2026-06-30"],
        "n_eleves_declares": int(len(e2)),
        "n_eleves_distincts": int(e2["id_eleve"].nunique()),
        "defauts": {
            "notes_hors_bornes": int(((n2["note"] < 0) | (n2["note"] > 20)).sum()),
            "doublons_eleves": int(e2.duplicated(subset=["id_eleve"]).sum()),
            "absences_jour_ferie": int(a2["date"].isin(FERIES).sum()),
            "absents_not_t2": SCOL_ABSENTS_NOTES,
        },
        "correlation_absent_notes": round(corr, 3),
        "segments_absences": seg,
        "taux_absence_par_classe": {
            c: round(float(taux[classe_map == c].mean()), 2)
            for c in [cl for cl, _ in CLASSES]
        },
        "classe_la_plus_absente": max(
            [cl for cl, _ in CLASSES],
            key=lambda c: float(taux[classe_map == c].mean()),
        ),
        "n_absences_brut": int(len(a2)),
    }
    return a


# ----------------------------------------------------------------------------
# Fichier projet — « le fichier que personne n'a regardé »
# ----------------------------------------------------------------------------
PROJET_STATUTS_OK = ["OK", "ok", "Reussie", "REUSSI"]
PROJET_STATUTS_KO = ["Echouee", "echec"]
PROJET_DOUBLONS = 14
PROJET_MONTANTS_NEGATIFS = 5
PROJET_MONTANTS_ENORMES = 2
PROJET_COMMISSIONS_MANQUANTES = 30


def generer_projet(rng):
    out = os.path.join(OUT, "projet")
    os.makedirs(out, exist_ok=True)
    n = 10000
    jours = pd.date_range("2026-01-01", "2026-06-30")
    dates = np.array([j.strftime("%Y-%m-%d") for j in jours])
    w = np.array([1.5, 1.1, 1.05, 1.05, 1.2, 0.7, 0.15])[jours.dayofweek]
    w = w / w.sum()
    rep = dates[np.sort(rng.choice(len(jours), size=n, p=w))]
    agents = np.array([f"AG{a:02d}" for a in rng.integers(1, 21, size=n)])
    types = np.array(["in", "out"])[rng.choice(2, size=n, p=[0.58, 0.42])]
    statuts = np.where(rng.random(n) < 0.82, 0, 1)
    ok_idx = rng.integers(0, len(PROJET_STATUTS_OK), size=n)
    ko_idx = rng.integers(0, len(PROJET_STATUTS_KO), size=n)
    stat_label = np.where(statuts == 0,
                          np.array(PROJET_STATUTS_OK)[ok_idx],
                          np.array(PROJET_STATUTS_KO)[ko_idx])
    montants = np.round(np.exp(rng.normal(np.log(2500), 0.9, size=n))).astype(int)
    montants = np.clip(montants, 100, 150000)
    comm = np.where(types == "in", np.round(montants * 0.025), np.round(montants * 0.01))
    canaux = np.array(["USSD", "Agent", "app"])[rng.choice(3, size=n, p=[0.4, 0.5, 0.1])]
    def tel(r):
        n1 = str(rng.integers(70, 80)) + str(rng.integers(0, 10))
        reste = str(rng.integers(0, 10000000)).zfill(7)
        r = rng.random()
        if r < 0.4:
            return f"+226 {n1} {reste[:2]} {reste[2:4]} {reste[4:]}"
        if r < 0.8:
            return f"{n1} {reste[:2]} {reste[2:4]} {reste[4:]}"
        return n1 + reste
    tels = np.array([tel(i) for i in range(n)])
    df = pd.DataFrame({
        "tx_ref": [f"TX{i + 1:07d}" for i in range(n)],
        "agent_code": agents, "client_phone": tels, "montant_xof": montants,
        "type_op": types, "statut": stat_label, "date_op": rep,
        "commission": comm, "canal": canaux,
        "id_export": np.arange(1, n + 1),
    })
    # défauts plantés
    idx_dbl = np.sort(rng.choice(n, PROJET_DOUBLONS, replace=False))
    df = pd.concat([df, df.iloc[idx_dbl]], ignore_index=True)
    idx_neg = np.sort(rng.choice(len(df) - n, PROJET_MONTANTS_NEGATIFS, replace=False))
    df.loc[idx_neg, "montant_xof"] = -rng.integers(500, 5000, size=PROJET_MONTANTS_NEGATIFS)
    idx_eno = np.sort(rng.choice(np.setdiff1d(np.arange(len(df) - n), idx_neg),
                                 PROJET_MONTANTS_ENORMES, replace=False))
    df.loc[idx_eno, "montant_xof"] = 1000000000
    idx_com = np.sort(rng.choice(len(df), PROJET_COMMISSIONS_MANQUANTES, replace=False))
    df.loc[idx_com, "commission"] = np.nan          # écrit comme champ vide dans le CSV
    df.to_csv(os.path.join(out, "fichier_inconnu.csv"), index=False, encoding="utf-8")

    d = pd.read_csv(os.path.join(out, "fichier_inconnu.csv"), dtype=str)
    ok = d["statut"].isin(PROJET_STATUTS_OK).sum()
    a = {
        "formes": {"fichier_inconnu": [int(len(d)), int(d.shape[1])]},
        "periode": ["2026-01-01", "2026-06-30"],
        "defauts": {
            "doublons_tx_ref": int(d.duplicated(subset=["tx_ref"]).sum()),
            "montants_negatifs": int((d["montant_xof"].astype(int) < 0).sum()),
            "montants_enormes": int((d["montant_xof"].astype(int) >= 100000000).sum()),
            "commissions_manquantes": int(d["commission"].isna().sum()),
        },
        "statuts_bruts": {s: int((d["statut"] == s).sum()) for s in
                          PROJET_STATUTS_OK + PROJET_STATUTS_KO},
        "succes_normalises": int(ok),
        "ecchecs_normalises": int(len(d) - ok),
        "n_agents": int(d["agent_code"].nunique()),
    }
    return a


# ----------------------------------------------------------------------------
def main():
    os.makedirs(OUT, exist_ok=True)
    rng = np.random.default_rng(SEED)
    formes_q, empreinte_q = export_quincaillerie()
    sante = generer_sante(rng)
    scolaire = generer_scolaire(rng)
    projet = generer_projet(rng)

    # empreinte du dossier (ordre des fichiers fixé)
    h = hashlib.sha256()
    ordre = []
    for sous in ["quincaillerie", "sante", "scolaire", "projet"]:
        dossier = os.path.join(OUT, sous)
        for nom in sorted(os.listdir(dossier)):
            ordre.append(f"{sous}/{nom}")
            with open(os.path.join(dossier, nom), "rb") as fh:
                h.update(fh.read())
    empreinte = h.hexdigest()

    attendu = {
        "graine": SEED,
        "quincaillerie": {
            "formes": formes_q,
            "empreinte": empreinte_q,
            "note": "réexport de la base M07 figée — mêmes totaux que M07/M08 (CA brut "
                    "7 908 259 732 FCFA, CA propre 7 876 320 164 FCFA, plus gros mois "
                    "78 965 529 FCFA : magasin 3, 2025-08, vue sans retours)",
        },
        "sante": sante,
        "scolaire": scolaire,
        "projet": projet,
        "empreinte_dossier": empreinte,
    }
    json.dump(attendu, open(os.path.join(OUT, "ATTENDU.json"), "w"),
              indent=2, ensure_ascii=False)

    brief = f"""# Brief M09 — « 3 heures avec un fichier que personne n'a regardé »

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
"""
    open(os.path.join(OUT, "00_brief.md"), "w", encoding="utf-8").write(brief)

    print("dossier_M09 (graine", SEED, ")")
    for sous, a in [("sante", sante), ("scolaire", scolaire), ("projet", projet)]:
        for k, v in a["formes"].items():
            print(f"  {sous}/{k}.csv : {v[0]:,} l. × {v[1]} col")
    print("  sante défauts :", sante["defauts"])
    print("  scolaire défauts :", scolaire["defauts"])
    print("  projet défauts :", projet["defauts"])
    print("  corrélation absences×notes (scolaire) :", scolaire["correlation_absent_notes"])
    print("  ruptures (jours) :", {f"{m}": a for m, _, _ in RUPTURES for a in [sante[f"rupture_{m}_jours"]]})
    print("empreinte dossier :", empreinte[:16] + "…")


if __name__ == "__main__":
    main()
