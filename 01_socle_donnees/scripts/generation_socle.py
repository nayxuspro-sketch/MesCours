#!/usr/bin/env python3
"""
La Voie des Données — générateur du socle de données du fil rouge « Sahel Distribution SA ».

Produit, de façon déterministe (même graine = mêmes fichiers, donc les chiffres cités
dans le manuel restent vrais) :

  data/brut/       les fichiers tels qu'un analyste les reçoit (avec leurs défauts)
  data/reference/  la version propre + la vérité terrain + le dictionnaire des données
  data/projection/ les extraits utilisés par les premiers modules (M01 : 480 lignes)
  data/sahel.duckdb la base DuckDB prête (couche brute + couche propre + vue de contrôle)

Usage :  python3 generation_socle.py [--quick]
"""
from __future__ import annotations
import argparse, json, os, random, shutil, sqlite3, sys
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
BRUT = os.path.join(ROOT, "data", "brut")
REF = os.path.join(ROOT, "data", "reference")
PROJ = os.path.join(ROOT, "data", "projection")
SEED = 20260917
TVA = 0.18
DEBUT, FIN = date(2023, 1, 1), date(2026, 8, 31)

CATALOGUE = [
    # (catégorie, sous-catégorie, [designations], unité, prix moyen HT, poids unitaire kg, fournisseur)
    ("Matériaux", "Ciment & liants", ["Ciment CPJ45 50 kg", "Ciment CPJ35 50 kg", "Chaux aérienne 25 kg",
        "Plâtre de construction 25 kg", "Colle à carrelage 25 kg", "Enduit de lissage 20 kg"], "sac", 4300, 50, "CIMAF Sahel"),
    ("Matériaux", "Agglomérés & briques", ["Parpaing 15 aggloméré", "Brique de terre cuite", "Carreau de pavement 40x40",
        "Hourdis creux 12", "Pavé autobloquant"], "unité", 850, 3.2, "Matériaux Kaboré"),
    ("Matériaux", "Sable & gravier", ["Sable de rivière (m3)", "Gravier 15/25 (m3)", "Tout-venant (m3)"], "m3", 18500, 1600, "Carrière Nakosin"),
    ("Quincaillerie", "Fixations", ["Vis à bois 4x40 (boîte)", "Cheville nylon 8 mm (sachet)", "Pointe 100 mm (kg)",
        "Boulon HM 10x40 (boîte)", "Écrou hexagonal 10 (sachet)", "Fer à béton 8 mm (barre)", "Fil de fer recuit (kg)"], "unité", 1450, 0.4, "Sahel Quincaillerie"),
    ("Quincaillerie", "Outillage", ["Marteau de menuisier", "Scie égoïne 500 mm", "Clé plate 13", "Tournevis cruciforme PH2",
        "Mètre ruban 5 m", "Pince coupante 200 mm", "Niveau à bulle 600 mm", "Meuleuse 125 mm", "Perforateur 800 W"], "unité", 6200, 1.1, "Outil Pro SA"),
    ("Plomberie", "Tubes & raccords", ["Tube PVC évacuation 100 mm (ml)", "Tube PER 16x2 (rouleau)", "Raccord laiton 20/27",
        "Coude PVC 90° 100", "Té fonte 100", "Mastic d'étanchéité"], "unité", 2750, 0.9, "Hydro Ouest"),
    ("Plomberie", "Appareils & robinetterie", ["Robinet mitigeur évier", "Chasse d'eau 6 L", "Douche de toilettes",
        "Ballon d'eau chaude 50 L", "Lavabo céramique", "WC complet avec abattant"], "unité", 21500, 8.5, "Hydro Ouest"),
    ("Electricité", "Câblage & protection", ["Câble 2x1,5 (rouleau 100 m)", "Câble 3x2,5 (rouleau 100 m)", "Disjoncteur 16 A",
        "Disjoncteur différentiel 30 mA", "Tableau 18 modules", "Douille E27 avec cordon", "Passe-câble étanche"], "unité", 9800, 2.3, "Élec-Faso"),
    ("Electricité", "Éclairage & énergie solaire", ["Ampoule LED 9 W", "Panneau solaire 100 W", "Batterie à décharge lente 120 Ah",
        "Régulateur de charge 10 A", "Lampe solaire murale", "Projecteur LED 30 W", "Lampe torche rechargeable"], "unité", 12400, 1.6, "Solaire Sahel SARL"),
    ("Peinture", "Peintures & enduits", ["Peinture acrylique blanc 10 L", "Peinture glycéro 1 L", "Enduit de rebouchage 5 kg",
        "Vernis marin 1 L", "Antirouille rouge brique 1 L", "Peinture toiture 25 kg", "Diluant nitro 5 L"], "litre", 3600, 1.15, "Peinture Saaba"),
    ("Bois & panneaux", "Panels & lames", ["Panneau contreplaqué 15 mm", "Panneau MDF 12 mm", "Lame de lambris 4 m",
        "Plaque de plâtre 13 mm", "Baguette de finition 2,4 m"], "unité", 11800, 12.4, "Boissonnerie de Koudougou"),
    ("Consommables", "Divers chantier", ["Bêche à manche bois", "Pelle carrée", "Brouette 90 L", "Sac de transport 100 kg",
        "Brouette en kit", "Échelle aluminium 4 marches", "Gants anti-coupure (paire)", "Lunettes de protection", "Casque de chantier"], "unité", 5400, 0.7, "EPI Faso"),
]
CATS_POIDS = [
    ("Matériaux", .30), ("Quincaillerie", .22), ("Plomberie", .12), ("Electricité", .11),
    ("Peinture", .06), ("Bois & panneaux", .07), ("Consommables", .12),
]

VILLES = [("Ouagadougou", "Centre", 0.44), ("Bobo-Dioulasso", "Hauts-Bassins", 0.22), ("Koudougou", "Centre-Ouest", 0.13),
          ("Kaya", "Centre-Nord", 0.10), ("Ziniaré", "Plateau-Central", 0.11)]
TYPES_CLIENT = ([["Particulier", 0.52], ["Professionnel", 0.31], ["Entreprise", 0.12], ["Administration", 0.05]])
MODES = ["Espèces", "Chèque", "Virement", "Mobile Money", "Créance 30 j"]
QUALITE = ["Magasin", "Livraison", "Téléphone"]


class Rand:
    """Adaptateur : les générateurs du socle écrivent r.random(), r.randint(a, b), r.choice(seq, p=...),
    r.normal(), r.lognormal() — le tout sur un tirage numpy reproductible (même graine = mêmes fichiers)."""

    def __init__(self, seed):
        self.g = np.random.default_rng(seed)
        self.r = random.Random(seed)

    def random(self, n=None):
        return float(self.g.random()) if n is None else self.g.random(n)

    def randint(self, a, b):
        return int(self.g.integers(a, b + 1))

    def integers(self, a, b, size=None):
        return self.g.integers(a, b, size=size)

    def choice(self, seq, p=None, size=None, replace=True):
        lst = list(seq)
        if p is not None:
            w = np.asarray(p, dtype=float)
            w = w / w.sum()
            return self.g.choice(np.asarray(lst, dtype=object), size=size, p=w, replace=replace)
        if size is None:
            return self.r.choice(lst)
        if replace is False:
            return self.r.sample(lst, size)
        return self.g.choice(np.asarray(lst, dtype=object), size=size)

    def lognormal(self, mu=0.0, sigma=1.0, size=None):
        return self.g.lognormal(mu, sigma, size)

    def normal(self, mu=0.0, sigma=1.0, size=None):
        return self.g.normal(mu, sigma, size)


def rng():
    return Rand(SEED)


def dim_date():
    jours = pd.date_range(DEBUT, FIN, freq="D")
    d = pd.DataFrame({"date": jours})
    d["annee"] = d["date"].dt.year
    d["mois"] = d["date"].dt.month
    d["libelle_mois"] = d["date"].dt.strftime("%Y-%m")
    d["trimestre"] = d["date"].dt.quarter
    d["semaine_iso"] = d["date"].dt.isocalendar().week.astype(int)
    d["jour_semaine"] = d["date"].dt.dayofweek
    d["libelle_jour"] = d["date"].dt.strftime("%A")
    d["est_dimanche"] = (d["jour_semaine"] == 6).astype(int)
    d["est_ferie"] = 0
    d["evenement"] = ""
    # Fêtes *fixes* uniquement, volontairement incomplètes : construire un calendrier juste
    # (jours fériés mobiles, semaines commerciales) est un exercice de M11.C03.
    feries = {(1, 1): "Nouvel An", (5, 1): "Fête du Travail", (8, 5): "Anniversaire de la Révolution",
              (12, 11): "Fête nationale", (12, 25): "Noël"}
    for (mo, jo), nom in feries.items():
        mask = (d["date"].dt.month == mo) & (d["date"].dt.day == jo)
        d.loc[mask, "est_ferie"] = 1
        d.loc[mask, "evenement"] = nom
    d["annee_mois"] = d["annee"].astype(str) + "-" + d["mois"].astype(str).str.zfill(2)
    return d


def magasins():
    rows = [
        dict(id_magasin=1, nom="Sahel Distribution — Ouaga 2000", ville="Ouagadougou", quartier="Ouaga 2000",
             region="Centre", type_magasin="Magasin", surface_m2=1450, responsable="A. Zongo", ouverture="2016-03-01"),
        dict(id_magasin=2, nom="Sahel Distribution — Gounghin", ville="Ouagadougou", quartier="Gounghin",
             region="Centre", type_magasin="Magasin", surface_m2=900, responsable="F. Kaboré", ouverture="2018-09-15"),
        dict(id_magasin=3, nom="Sahel Distribution — Bobo Kibidwé", ville="Bobo-Dioulasso", quartier="Kibidwé",
             region="Hauts-Bassins", type_magasin="Magasin", surface_m2=1100, responsable="S. Sanou", ouverture="2017-06-01"),
        dict(id_magasin=4, nom="Sahel Distribution — Koudougou Centre", ville="Koudougou", quartier="Pole",
             region="Centre-Ouest", type_magasin="Magasin", surface_m2=650, responsable="R. Ouédraogo", ouverture="2020-02-10"),
        dict(id_magasin=5, nom="Sahel Distribution — Kaya Marché", ville="Kaya", quartier="Marché",
             region="Centre-Nord", type_magasin="Magasin", surface_m2=520, responsable="I. Traoré", ouverture="2021-11-05"),
        dict(id_magasin=6, nom="Dépôt central — Zogona", ville="Ouagadougou", quartier="Zogona",
             region="Centre", type_magasin="Dépôt", surface_m2=3200, responsable="M. Compaoré", ouverture="2015-01-12"),
    ]
    return pd.DataFrame(rows)


def produits(r):
    pid, rows = 0, []
    for cat, sous, noms, unite, pmoy, poids, four in CATALOGUE:
        for nom in noms:
            for variante in range(1, 3):  # deux marques/gammes par famille -> ~ 2 refs
                pid += 1
                base = pmoy * (0.62 + 0.9 * r.random()) * (1.10 if variante == 2 else 1.0)
                pu = int(round(base / 25) * 25)
                rows.append(dict(id_produit=pid, designation=f"{nom} — réf {variante}", categorie=cat,
                                 sous_categorie=sous, unite=unite, prix_vente_ht=pu,
                                 poids_unite_kg=round(poids * (0.5 + r.random()), 2),
                                 fournisseur=four, reference_fournisseur=f"{cat[:3].upper()}-{pid:04d}",
                                 tva=round(TVA, 2), actif=1 if r.random() > 0.03 else 0))
    df = pd.DataFrame(rows)
    return df


def vendeurs(r, mags):
    pren = ["Awa", "Issa", "Fatoumata", "Boureima", "Salif", "Mariam", "Karim", "Rasmata", "Adama", "Safiatou",
            "Boukary", "Alizéta", "Wendpanga", "Salamatu", "Norgho", "Kadidiatou", "Etienne", "Rokia", "Moussa",
            "Aïssata", "Blaise", "Nafissatou"]
    nom = ["Zongo", "Kaboré", "Sanou", "Ouédraogo", "Traoré", "Compaoré", "Sawadogo", "Diallo", "Bationo",
           "Nikiéma", "Ouattara", "Tapsoba", "Kabré", "Sankara", "Bonkoum", "Yaro", "Guigma", "Kinda", "Ilboudo",
           "Barry", "Dicko", "Zoungrana"]
    rows = []
    for i, (p, n) in enumerate(zip(pren, nom), start=1):
        mag = [m for m in mags["id_magasin"] if m != 6][i % 5]
        rows.append(dict(id_vendeur=i, nom_complet=f"{p} {n}", id_magasin=mag,
                         date_embauche=str((datetime(2016, 1, 1) + timedelta(days=r.randint(0, 3200))).date()),
                         statut="Titulaire" if r.random() > 0.18 else "CDD",
                         secteur_vente="Comptoir" if r.random() > 0.4 else "Itinérant"))
    return pd.DataFrame(rows)


def clients(r, n=23500):
    villes = np.array([v for v, _, _ in VILLES]); poids = np.array([p for _, _, p in VILLES])
    types, tpoids = zip(*TYPES_CLIENT)
    rows = []
    for i in range(1, n + 1):
        v = str(r.choice(villes, p=poids))
        t = str(r.choice(types, p=tpoids))
        creation = (datetime(2016, 1, 1) + timedelta(days=r.randint(0, 3800))).date()
        rows.append(dict(id_client=i,
                         nom=(f"Menage {i:05d}" if t == "Particulier" else
                              f"{r.choice(['Ets', 'SARL', 'Societe', 'Chantiers'])} {r.choice(nom_surname(r))}"),
                         type_client=t, ville=v, region=dict((a, b) for a, b, _ in VILLES)[v],
                         telephone=f"+226 {r.randint(70,79)} {r.randint(10,99)} {r.randint(10,99)} {r.randint(10,99)} {r.randint(10,99)}",
                         email=(f"contact{i}@{r.choice(['gmail.com','yahoo.fr','outlook.fr','entreprise.bf'])}"
                                if t != "Particulier" and r.random() > 0.35 else ""),
                         date_creation=str(creation),
                         segment=r.choice(["Or", "Argent", "Standard"], p=[0.12, 0.28, 0.60]),
                         conditions_paiement=r.choice(["Comptant", "30 j", "60 j"], p=[0.6, 0.3, 0.1]),
                         plafond_credit=r.choice([0, 250000, 500000, 1500000, 5000000],
                                                 p=[0.45, 0.2, 0.2, 0.12, 0.03])))
    return pd.DataFrame(rows)


def nom_surname(r):
    return r.choice(["Zongo", "Kaboré", "Sanou", "Ouédraogo", "Traoré", "Compaoré", "Sawadogo", "Diallo",
                     "Bationo", "Nikiéma", "Ouattara", "Tapsoba", "Kabré", "Sankara", "Yaro", "Zoungrana"])


def ventes(g, nb, cli, prod, mags, vds, dim):
    """Couche propre (sans défauts) du fait « ventes », vectorisée : ~240 000 lignes en quelques secondes.

    La génération est volontairement pilotée par des règles de gestion explicites (saisonnalité,
    mix produit, remises par segment, retours, prix qui suit l'année) : c'est ce qui permet au manuel
    d'affirmer des chiffres et de les défendre.
    """
    jours = dim["date"].to_numpy()
    mois = dim["date"].dt.month.to_numpy()
    jd = dim["date"].dt.dayofweek.to_numpy()
    annees = dim["date"].dt.year.to_numpy()
    mois_w = np.array([.95, 1.0, 1.18, 1.14, .92, .78, .72, .80, 1.02, 1.22, 1.20, 1.16])
    jour_w = np.array([1.12, 1.08, 1.02, .96, 1.00, 1.05, .35])
    annee_gross = {a: 1.0 + 0.085 * (a - int(annees.min())) for a in set(annees.tolist())}
    poids_jour = mois_w[mois - 1] * jour_w[jd] * np.array([annee_gross[a] for a in annees])
    poids_jour = poids_jour / poids_jour.sum()
    idx_jour = g.choice(len(jours), size=nb, p=poids_jour)

    ids_par_cat = {c[0]: prod.loc[prod.categorie == c[0], "id_produit"].to_numpy()
                   for c in CATS_POIDS if (prod.categorie == c[0]).any()}
    noms_cats = np.array(list(ids_par_cat))
    wcat = np.array([dict(CATS_POIDS)[c] for c in noms_cats], dtype=float)
    cat_pick = g.choice(noms_cats, size=nb, p=wcat / wcat.sum())
    pid = np.array([int(g.choice(ids_par_cat[c])) for c in cat_pick])

    prix = prod.set_index("id_produit")["prix_vente_ht"].to_dict()
    poids = prod.set_index("id_produit")["poids_unite_kg"].to_dict()
    unite = prod.set_index("id_produit")["unite"].to_dict()
    annee_row = annees[idx_jour]
    pu = np.array([prix[p] for p in pid], dtype=float) * np.array([annee_gross[a] for a in annee_row])
    pu = (np.round(pu * (0.97 + 0.06 * g.random(nb)) / 25) * 25).astype(int)

    u = np.array([unite[p] for p in pid])
    q = np.empty(nb, dtype=int)
    for cible, mu, sig, maxi in [(u == "sac", 1.9, .7, 400), (u == "m3", 1.2, .6, 60),
                                 (u == "litre", 2.3, .8, 200), (u == "unité", 1.4, .9, 250),
                                 (u == "carton", 1.6, .8, 150)]:
        n = int(cible.sum())
        if n:
            q[cible] = np.minimum(maxi, np.maximum(1, np.round(g.lognormal(mu, sig, n)))).astype(int)
    mags_w = np.array([.34, .22, .20, .13, .11])
    mag = g.choice(np.array([1, 2, 3, 4, 5]), size=nb, p=mags_w / mags_w.sum())

    segment = cli.set_index("id_client")["segment"].to_dict()
    ncli = len(segment)
    cid = np.where(g.random(nb) > 0.18, g.integers(1, ncli + 1, nb), 0)
    seg = np.array([segment.get(int(c), "Standard") for c in cid])
    remise = np.select([seg == "Or", seg == "Argent"], [.08, .04], default=0.0)
    remise = np.round(np.minimum(remise + np.where(g.random(nb) < .05, .03, 0.0) * np.where(cid > 0, 1, 0), .25), 3)

    par_magasin = vds.groupby("id_magasin")["id_vendeur"].apply(list).to_dict()
    vd = np.array([int(g.choice(par_magasin[int(m)])) for m in mag])

    ht = np.round(q * pu * (1 - remise)).astype(int)
    tva = np.round(ht * TVA).astype(int)
    ttc = ht + tva
    retour = (g.random(nb) < .012)
    sign = np.where(retour, -1, 1)
    poids_kg = np.round(np.array([poids[p] for p in pid], dtype=float) * q, 2) * sign
    dts = pd.Series(pd.to_datetime(jours[idx_jour]))
    tid = np.arange(1, nb + 1)
    df = pd.DataFrame(dict(
        id_vente=tid,
        id_ticket=tid.copy(),  # remplacé plus bas par un vrai numéro de ticket multi-lignes
        date_vente=dts,
        heure=[f"{h:02d}:{mi:02d}" for h, mi in zip(g.integers(7, 19, nb), g.integers(0, 60, nb))],
        id_magasin=mag, id_vendeur=vd, id_client=cid, id_produit=pid,
        quantite=q * sign, prix_unitaire_ht=pu, taux_remise=remise,
        montant_ht=ht * sign, montant_tva=tva * sign, montant_ttc=ttc * sign,
        mode_paiement=g.choice(MODES, nb, p=[.34, .18, .14, .26, .08]),
        canal=g.choice(QUALITE, nb, p=[.66, .24, .10]),
        est_retour=retour.astype(int), poids_kg=poids_kg,
        mois=dts.dt.month.to_numpy(), annee=dts.dt.year.to_numpy()))
    df = df.sort_values(["date_vente", "id_magasin", "id_vente"], kind="mergesort").reset_index(drop=True)
    df["id_ticket"] = numeros_de_ticket(df, seed=SEED + 3)
    return df


def numeros_de_ticket(df, seed=1):
    """Regroupe les lignes en tickets réels (1 à 5 lignes par ticket), puis fabrique le numéro.

    Sans cette étape, chaque ligne serait son propre ticket : COUNT(*) et COUNT(DISTINCT id_ticket)
    donneraient le même résultat et l'exercice « une vente n'est pas une ligne » tomberait à plat.
    """
    g = np.random.default_rng(seed)
    lab = np.empty(len(df), dtype=np.int64)
    pos = 0
    n_ticket = 0
    for (_d, _m), grp in df.groupby(["date_vente", "id_magasin"], sort=False):
        n = len(grp)
        k = int(max(1, min(n, round(n / float(g.integers(1, 4))))))  # 1 à 3 lignes en moyenne
        tailles = np.full(k, n // k)
        tailles[: n % k] += 1
        lab[pos:pos + n] = np.repeat(np.arange(k), tailles) + n_ticket
        n_ticket += k
        pos += n
    mag = df["id_magasin"].to_numpy()
    jcle = df["date_vente"].dt.strftime("%y%m%d").to_numpy()
    return np.array([f"T{int(a):02d}-{b}-{c % 1000000:06d}" for a, b, c in zip(mag, jcle, lab)])


def injecter_defauts(brut: pd.DataFrame, prod: pd.DataFrame, cli: pd.DataFrame, r):
    """Retourne (brut_avec_defauts, prod_sale, cli_sale, rapport_du_plan_d_injection).
    Le rapport du plan d injection ne sert plus de corrigé : depuis la correction du 18/09/2026,
    le corrigé est mesuré sur les fichiers livrés (bloc « corrigé enseignant » de main).
    Il reste l histoire du point 12 de M04.C01 et de l exercice E4 de l évaluation."""
    d = brut.copy()
    rapport = {}
    # 1. montants écrits en texte (espace mille + suffixe) sur ~1,4 % des lignes
    d["montant_ttc"] = d["montant_ttc"].astype(object)
    idx = r.choice(d.index, size=int(len(d) * 0.014), replace=False)
    d.loc[idx, "montant_ttc"] = [f"{int(v):,}".replace(",", " ") + " FCFA" for v in d.loc[idx, "montant_ttc"]]
    rapport["montants_en_texte"] = len(idx)
    # 2. dates dans deux formats différents sur ~1,1 % des lignes
    idx2 = r.choice(d.index, size=int(len(d) * 0.011), replace=False)
    d.loc[idx2, "date_vente"] = pd.to_datetime(d.loc[idx2, "date_vente"]).dt.strftime("%d/%m/%Y")
    rapport["dates_format_mixte"] = len(idx2)
    # 3. doublons exacts (ticket ressaisi) ~ 1,4 %
    n_dup = int(len(d) * 0.014)
    dup = d.sample(n_dup, random_state=SEED).copy()
    dup["id_vente"] = np.arange(d["id_vente"].max() + 1, d["id_vente"].max() + 1 + n_dup)
    d = pd.concat([d, dup], ignore_index=True)
    rapport["lignes_en_double"] = n_dup
    # 4. remises aberrantes (saisie en points de pourcentage au lieu d'une proportion) ~ 0,4 %
    idx3 = r.choice(d.index, size=int(len(d) * 0.004), replace=False)
    d["taux_remise"] = d["taux_remise"].astype(object)
    d.loc[idx3, "taux_remise"] = list(r.choice([12.0, 18.0, 25.0, 30.0], size=len(idx3)))
    rapport["remises_aberrantes"] = len(idx3)
    # 5. clients inconnus (id absent de la table clients) ~ 0,2 %
    idx4 = r.choice(d.index, size=int(len(d) * 0.002), replace=False)
    d.loc[idx4, "id_client"] = r.integers(900001, 900901, size=len(idx4))
    rapport["clients_non_referentes"] = len(idx4)
    # 6. produits orthographiés / catégories à 4 écritures
    prod2 = prod.copy()
    variantes = {"Électricité": ["Electricité", "ELECTRICITE", "Électricité ", "Electricité"],
                 "Matériaux": ["Materiaux", "MATÉRIAUX", "Matériaux ", "materiaux"],
                 "Quincaillerie": ["Quincaillerie", "QUINCAILLERIE", "Quincaillerie ", "quincaillerie"],
                 "Peinture": ["Peinture", "PEINTURE", "Peintures", "peinture"]}
    prod2["categorie"] = [variantes.get(c, [c] * 4)[r.randint(0, 3)] for c in prod2["categorie"]]
    prod2.loc[prod2.sample(2, random_state=SEED).index, "prix_vente_ht"] = np.nan
    prod2.loc[prod2.sample(6, random_state=SEED).index, "poids_unite_kg"] = -1
    rapport["produits_categorie_heteroclite"] = int((prod2["categorie"] != prod["categorie"]).sum())
    # 7. villes manquantes chez les clients (8 %)
    cli2 = cli.copy()
    miss = r.choice(cli2.index, size=int(len(cli2) * 0.08), replace=False)
    cli2.loc[miss, "ville"] = np.nan
    # 8. doublons quasi-exacts de clients (412) : même foyer, orthographe/espaces différents
    dupc = cli2.head(412).copy()
    dupc["id_client"] = cli2["id_client"].max() + np.arange(1, 413)
    dupc["nom"] = ["  " + n.upper().replace("  ", " ") + " " for n in dupc["nom"]]
    dupc["telephone"] = [t.replace(" ", "") for t in dupc["telephone"]]
    cli2 = pd.concat([cli2, dupc], ignore_index=True)
    rapport["clients_manquants_ville"] = len(miss)
    rapport["doublons_quasi_clients"] = 412
    return d, prod2, cli2, rapport


def targets(r, dim):
    am = dim[["annee", "mois"]].drop_duplicates()
    rows = []
    for mag in [1, 2, 3, 4, 5]:
        base = {1: 48e6, 2: 31e6, 3: 27e6, 4: 18e6, 5: 14e6}[mag]
        for _, a in am.iterrows():
            croissance = 1 + 0.085 * (a.annee - 2023)
            saison = {1: .95, 2: 1.0, 3: 1.18, 4: 1.14, 5: .92, 6: .78, 7: .72, 8: .8, 9: 1.02, 10: 1.22, 11: 1.2, 12: 1.16}[a.mois]
            rows.append(dict(id_magasin=mag, annee=int(a.annee), mois=int(a.mois),
                             annee_mois=f"{a.annee}-{a.mois:02d}",
                             ca_objectif_ttc=int(round(base * croissance * saison / 1e4) * 1e4),
                             marge_objectif_pct=round(0.185 + 0.02 * r.random(), 3)))
    df = pd.DataFrame(rows)
    # 2 mois manquants volontairement (exercice M04.C04 : « le total du tableau ne colle pas »)
    df = df.drop(df[(df.id_magasin == 4) & (df.annee_mois.isin(["2024-02", "2024-03"]))].index)
    return df.reset_index(drop=True)


def stocks(r, prod, mags, dim, nb=60000):
    jours = dim["date"].dt.date.tolist()
    pid = prod["id_produit"].values
    prix = dict(zip(prod["id_produit"], prod["prix_vente_ht"]))
    rows = []
    seen = set()
    while len(rows) < nb:
        d = r.choice(jours); p = int(r.choice(pid)); m = int(r.choice([1, 2, 3, 4, 5, 6]))
        key = (d, p, m)
        if key in seen:
            continue
        seen.add(key)
        theo = int(max(0, round(r.lognormal(3.1, 1.0))))
        ecart = int(round(theo * r.normal(0, 0.06)))
        rows.append(dict(date=d, id_produit=p, id_magasin=m, qte_theorique=theo,
                         qte_physique=max(0, theo + ecart), seuil_alerte=int(theo * 0.25),
                         valeur_stock_ht=int(max(0, theo + ecart) * prix[p])))
    df = pd.DataFrame(rows)
    # trous de série (ruptures de relevés) et valeurs négatives
    df.loc[r.choice(df.index, size=int(len(df) * 0.03), replace=False), "qte_physique"] = -1
    return df


def couts_achat(r, prod):
    rows = []
    for p, pu, four in zip(prod["id_produit"], prod["prix_vente_ht"], prod["fournisseur"]):
        t = DEBUT
        marge = 0.62 + 0.12 * r.random()
        while t <= FIN:
            t2 = min((pd.Timestamp(t) + pd.DateOffset(months=4)).date(), FIN)
            rows.append(dict(id_produit=int(p), date_debut=str(t), date_fin=str(t2),
                             pu_achat_ht=int(round(pu * (1 - marge) / 25) * 25), fournisseur=four))
            t = (pd.Timestamp(t2) + timedelta(days=1)).date()
            marge = min(0.82, max(0.5, marge + r.normal(0, 0.03)))
    return pd.DataFrame(rows)


def remises_manuel(r, cli, dim):
    am = dim.groupby(["annee", "mois"]).size().reset_index()[["annee", "mois"]]
    rows = []
    ech = r.choice(cli["id_client"].values, size=1400, replace=False)
    for c in ech:
        for a in am.sample(13, random_state=r.randint(0, 10**6)).itertuples():
            rows.append(dict(id_client=int(c), annee=int(a.annee), mois=int(a.mois),
                             annee_mois=f"{a.annee}-{a.mois:02d}",
                             remise_consentie_montant=int(round(r.lognormal(11.3, 0.8), -3)),
                             motif=r.choice(["Volume mensuel", "Litige qualité", "Fidélité", "Relance paiement", "Cadeau commercial"]),
                             saisi_par=r.choice(["Assistante commerciale", "Directeur magasin", "Itinérant"])))
    return pd.DataFrame(rows)


def ecrire_fournisseur_defectueux(prod, r, n=42):
    """Fichier 'export du fournisseur' : séparateur point-virgule, encodage Windows, 3 lignes de chapeau,
    nombre avec virgule décimale -> l'exercice du module 1."""
    entetes = ["export genere depuis ELODIE v3", f"edition le {date.today():%d/%m/%Y}", "peinture saaba sarl — tarif 2026"]
    cols = "code_article;libelle;conditionnement;prix_unitaire;unite_mesure;tva"
    lignes = []
    art = prod[prod.categorie.isin(["Peinture", "Plomberie"])].head(n)
    for i, p in enumerate(art.itertuples(), start=1):
        lignes.append(f"{'PS-' + str(i).zfill(3)};{p.designation.replace(';', ',')};10 L;{p.prix_vente_ht},{r.randint(0,99)};litre;0,18")
    os.makedirs(BRUT, exist_ok=True)
    chemin = os.path.join(BRUT, "tarif_fournisseur_peinture.csv")
    with open(chemin, "w", encoding="cp1252", newline="") as f:
        f.write("\n".join(entetes) + "\n" + cols + "\n" + "\n".join(lignes) + "\n")
    return chemin


def main(quick=False):
    for d in (BRUT, REF, PROJ):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d, exist_ok=True)
    r = rng()
    dim = dim_date()
    mags = magasins()
    prod = produits(r)
    vds = vendeurs(r, mags)
    cli = clients(r, 3000 if quick else 23500)
    nbv = 20000 if quick else 240000
    ventes_propres = ventes(np.random.default_rng(SEED + 1), nbv, cli, prod, mags, vds, dim)
    brut, prod_sale, cli_sale, rapport = injecter_defauts(ventes_propres, prod, cli, Rand(SEED + 2))

    tgt = targets(r, dim)
    stk = stocks(r, prod, mags, dim, 4000 if quick else 60000)
    couts = couts_achat(r, prod)
    remises = remises_manuel(r, cli, dim)

    # ---------------- fichiers bruts (ce que reçoit l'analyste) ----------------
    brut_ventes = brut.copy()
    # on écrit le brut TEL QUEL : les dates au format mixte et les montants en texte sont l'objet de
    # l'exercice (le corriger soi-même produirait un fichier "propre" et tuerait l'apprentissage)
    brut_ventes["date_vente"] = brut_ventes["date_vente"].astype(str).str.slice(0, 10)
    brut_ventes.loc[brut_ventes["date_vente"].str.contains("00:00:00"), "date_vente"] = (
        pd.to_datetime(brut_ventes.loc[brut_ventes["date_vente"].str.contains("00:00:00"), "date_vente"])
        .dt.strftime("%d/%m/%Y"))
    brut_ventes.to_csv(os.path.join(BRUT, "ventes_brutes.csv"), index=False, encoding="utf-8-sig")
    prod_sale.to_csv(os.path.join(BRUT, "produits.csv"), index=False, encoding="utf-8-sig")
    cli_sale.to_csv(os.path.join(BRUT, "clients.csv"), index=False, encoding="utf-8-sig")
    mags.to_csv(os.path.join(BRUT, "magasins.csv"), index=False, encoding="utf-8-sig")
    vds.to_csv(os.path.join(BRUT, "vendeurs.csv"), index=False, encoding="utf-8-sig")
    tgt.to_csv(os.path.join(BRUT, "objectifs_de_ca.csv"), sep=";", index=False, encoding="cp1252")
    stk.to_csv(os.path.join(BRUT, "stocks_quotidiens.csv"), index=False)
    couts.to_csv(os.path.join(BRUT, "couts_achat.csv"), index=False)
    remises.to_excel(os.path.join(BRUT, "remises_manuelles.xlsx"), index=False, engine="openpyxl")
    ecrire_fournisseur_defectueux(prod, r)

    # ---------------- référence (corrigés, vérité terrain) ----------------
    ventes_propres.to_csv(os.path.join(REF, "ventes_propres.csv"), index=False)
    prod.to_csv(os.path.join(REF, "produits_propres.csv"), index=False)
    cli.to_csv(os.path.join(REF, "clients_propres.csv"), index=False)
    dim.to_csv(os.path.join(REF, "dim_date.csv"), index=False)
    verites = []
    for mag, g in ventes_propres.groupby("id_magasin"):
        verites.append(dict(niveau="magasin", cle=int(mag), nb_lignes=len(g),
                            ca_ttc=int(g.montant_ttc.sum()), marge_estimee_ht=int(g.montant_ht.sum())))
    for an, g in ventes_propres.groupby(ventes_propres.date_vente.dt.year):
        verites.append(dict(niveau="annee", cle=int(an), nb_lignes=len(g), ca_ttc=int(g.montant_ttc.sum()),
                            marge_estimee_ht=int(g.montant_ht.sum())))
    for (am), g in ventes_propres.groupby(ventes_propres.date_vente.dt.strftime("%Y-%m")):
        verites.append(dict(niveau="mois", cle=am, nb_lignes=len(g), ca_ttc=int(g.montant_ttc.sum()),
                            marge_estimee_ht=int(g.montant_ht.sum())))
    for cat, g in ventes_propres.merge(prod[["id_produit", "categorie"]], on="id_produit").groupby("categorie"):
        verites.append(dict(niveau="categorie", cle=cat, nb_lignes=len(g), ca_ttc=int(g.montant_ttc.sum()),
                            marge_estimee_ht=int(g.montant_ht.sum())))
    verites.append(dict(niveau="total", cle="toutes_ventes", nb_lignes=len(ventes_propres),
                        ca_ttc=int(ventes_propres.montant_ttc.sum()),
                        marge_estimee_ht=int(ventes_propres.montant_ht.sum())))
    pd.DataFrame(verites).to_csv(os.path.join(REF, "verites_terrain.csv"), index=False)
    # ---------------- corrigé enseignant : mesuré sur les fichiers LIVRÉS ----------------
    # La première version de ce socle recopiait ici le plan d'injection (le `rapport`
    # retourné par injecter_defauts) : faux sur trois lignes - 3 360 montants texte au lieu
    # de 3 421 (les doublons recopient les montants texte), 2 640 dates mixtes qui ne
    # survivent pas à l'écriture, 1 880 villes au lieu de 1 911. M04 en fait l'objet d'étude
    # du point 12 (C01) et de l'exercice E4 (évaluation) ; la version du socle livrée dans
    # l'atelier conserve cette clé d'origine, c'est voulu. Correction apportée au générateur
    # le 18/09/2026 : à la prochaine régénération, le corrigé se recompte après l'écriture,
    # jamais d'après le plan.
    b_lu = pd.read_csv(os.path.join(BRUT, "ventes_brutes.csv"), dtype=str, keep_default_na=False,
                       encoding="utf-8-sig")
    c_lu = pd.read_csv(os.path.join(BRUT, "clients.csv"), dtype=str, keep_default_na=False,
                       encoding="utf-8-sig")
    p_lu = pd.read_csv(os.path.join(BRUT, "produits.csv"), dtype=str, keep_default_na=False,
                       encoding="utf-8-sig")
    dic_lu = pd.read_csv(os.path.join(REF, "dictionnaire_produits.csv"), dtype=str,
                         keep_default_na=False, encoding="utf-8-sig")
    ttc_lu = pd.to_numeric(b_lu["montant_ttc"], errors="coerce")
    rapport = {
        "montants_en_texte": int((ttc_lu.isna() & (b_lu["montant_ttc"].str.strip() != "")).sum()),
        "dates_format_mixte": int((~b_lu["date_vente"].str.match(r"^\d{4}-\d{2}-\d{2}$")).sum()),
        "lignes_en_double": int(len(b_lu) - len(ventes_propres)),
        "remises_aberrantes": int((pd.to_numeric(b_lu["taux_remise"], errors="coerce") > 1).sum()),
        "clients_non_referentes": int((~b_lu["id_client"].isin(set(c_lu["id_client"]))
                                       & (b_lu["id_client"].str.strip() != "0")
                                       & (b_lu["id_client"].str.strip() != "")).sum()),
        # même définition que m04_produits_categorie_heteroclite dans chiffres_manuel.py :
        # hors des sept catégories canoniques, pas « hors des modalités du dictionnaire »
        "produits_categorie_heteroclite": int((~p_lu["categorie"].astype(str).str.strip().isin(
            ["Bois & panneaux", "Consommables", "Electricité", "Matériaux", "Peinture",
             "Plomberie", "Quincaillerie"])).sum()),
        "clients_manquants_ville": int((c_lu["ville"].str.strip() == "").sum()),
        "doublons_quasi_clients": int(len(c_lu) - len(cli)),
        "lignes_brutes": int(len(b_lu)),
        "lignes_propres": int(len(ventes_propres)),
    }
    json.dump(rapport, open(os.path.join(REF, "rapport_defauts.json"), "w"), indent=2, ensure_ascii=False)

    # ---------------- projection : les petits fichiers des premiers modules ----------------
    petit = ventes_propres[ventes_propres.date_vente.dt.year == 2025].copy()
    mag5 = petit[petit.id_magasin == 5].sort_values(["date_vente", "id_ticket", "id_vente"])
    # échantillon de 480 lignes pour le projet M01, avec ses défauts
    # on prend ~40 lignes par mois pour couvrir l'année entière (sinon l'échantillon ne
    # contient que janvier et l'analyse saisonnière tombe à plat)
    base = (pd.concat([g.head(40) for _, g in mag5.groupby(mag5["date_vente"].dt.month, sort=True)])
             .sort_values(["date_vente", "id_ticket"]).copy())
    echant = base.copy()
    echant["id_magasin"] = "Magasin 5 — Kaya Marché"
    base["id_magasin"] = "Magasin 5 — Kaya Marché"
    echant["montant_ttc"] = echant["montant_ttc"].astype(object)
    dates_iso = echant["date_vente"].dt.strftime("%Y-%m-%d").to_numpy()
    bascule = np.random.default_rng(SEED + 5).choice(len(dates_iso), size=64, replace=False)
    for i_pos in bascule:  # 64 lignes sur 480 saisies à la main au format français
        aa, mm, jj = dates_iso[i_pos].split("-")   # l'écriture manuelle francophone est jour/mois/année
        dates_iso[i_pos] = f"{jj}/{mm}/{aa}"
    echant["date_vente"] = dates_iso
    echant["montant_ttc"] = [f"{int(v):,}".replace(",", " ") for v in echant["montant_ttc"]]
    rr = np.random.default_rng(SEED + 7)
    idx = rr.choice(echant.index[:480], size=18, replace=False)
    echant.loc[idx, "id_client"] = np.nan
    # un identifiant client s'écrit en entier : sans ce cast, le NaN fait basculer la colonne en
    # float64 et l'énoncé afficherait « 10857.0 », que l'attendu ne contiendrait jamais
    echant["id_client"] = echant["id_client"].astype("Int64")
    idx2 = rr.choice(echant.index[:480], size=7, replace=False)
    echant.loc[idx2, "quantite"] = [int(v) * 1000 for v in echant.loc[idx2, "quantite"]]
    idx3 = rr.choice(echant.index[5:], size=9, replace=False)
    echant = pd.concat([echant, echant.loc[idx3]]).sort_index()
    echant["id_magasin"] = "Magasin 5 — Kaya Marché"
    def en_format_projet(f):
        """Même mise en page (13 colonnes, en-têtes français) pour l'énoncé et pour le corrigé."""
        dates = f.date_vente.dt.strftime("%Y-%m-%d") if hasattr(f.date_vente, "dt") else f.date_vente
        return pd.DataFrame({"n_ticket": f.id_ticket, "date": dates, "heure": f.heure, "magasin": f.id_magasin,
                             "vendeur": f.id_vendeur.map(dict(zip(vds.id_vendeur, vds.nom_complet))),
                             "client": f.id_client,
                             "produit": f.id_produit.map(dict(zip(prod.id_produit, prod.designation))),
                             "categorie": f.id_produit.map(dict(zip(prod.id_produit, prod.categorie))),
                             "quantite": f.quantite, "prix_unitaire_ht": f.prix_unitaire_ht,
                             "remise": f.taux_remise, "montant_ht": f.montant_ht})
    # l'énoncé : le fichier tel qu'il est reçu (489 lignes, avec ses défauts)
    out = en_format_projet(echant)
    out["montant_ttc"] = echant.montant_ttc.to_numpy()   # déjà au format texte avec espace de milliers
    out.to_csv(os.path.join(PROJ, "ventes_magasin5_2025.csv"), index=False, encoding="utf-8-sig", sep=";", na_rep="")
    # ATTENDU = l'énoncé NETTOYÉ, pas l'extrait propre d'origine : on défait exactement les
    # défauts injectés et rien d'autre. Un apprenant qui obéit aux consignes (dont « ne pas
    # remplir les clients vides ») doit retrouver le fichier cellule pour cellule.
    propre = echant.sort_index()
    propre = propre[~propre.index.duplicated(keep="first")]            # 9 lignes de doublon retirées → 480
    propre = propre.copy()
    propre.loc[propre.index.isin(idx2), "quantite"] = (propre.loc[propre.index.isin(idx2), "quantite"].astype("int64") // 1000)
    propre["date_vente"] = pd.to_datetime(propre["date_vente"], dayfirst=True, format="mixed").dt.strftime("%Y-%m-%d")
    ttc_net = pd.to_numeric(propre["montant_ttc"].astype(str).str.replace("\u00a0", "").str.replace(" ", ""), errors="raise")
    attendu = en_format_projet(propre)
    attendu["montant_ttc"] = [str(int(v)) for v in ttc_net]            # corrigé : nombre simple, sans espace
    attendu.to_csv(os.path.join(REF, "ventes_magasin5_2025_ATTENDU.csv"), index=False,
                   encoding="utf-8-sig", sep=";", na_rep="")
    assert len(attendu) == 480, f"ATTENDU à {len(attendu)} lignes au lieu de 480"

    # ---------------- base DuckDB ----------------
    try:
        import duckdb
        dbp = os.path.join(ROOT, "data", "sahel.duckdb")
        if os.path.exists(dbp):
            os.remove(dbp)
        con = duckdb.connect(dbp)
        con.execute("CREATE SCHEMA brut"); con.execute("CREATE SCHEMA propre")
        for t, f in [("brut.ventes", os.path.join(BRUT, "ventes_brutes.csv")),
                     ("brut.produits", os.path.join(BRUT, "produits.csv")),
                     ("brut.clients", os.path.join(BRUT, "clients.csv")),
                     ("brut.magasins", os.path.join(BRUT, "magasins.csv")),
                     ("brut.vendeurs", os.path.join(BRUT, "vendeurs.csv")),
                     ("brut.objectifs", os.path.join(BRUT, "objectifs_de_ca.csv")),
                     ("brut.stocks", os.path.join(BRUT, "stocks_quotidiens.csv")),
                     ("brut.couts_achat", os.path.join(BRUT, "couts_achat.csv")),
                     ("propre.ventes", os.path.join(REF, "ventes_propres.csv")),
                     ("propre.produits", os.path.join(REF, "produits_propres.csv")),
                     ("propre.clients", os.path.join(REF, "clients_propres.csv")),
                     ("propre.dim_date", os.path.join(REF, "dim_date.csv")),
                     ("propre.verites_terrain", os.path.join(REF, "verites_terrain.csv"))]:
            try:
                con.execute(f"CREATE OR REPLACE TABLE {t} AS SELECT * FROM read_csv_auto('{f}', header=true)")
            except Exception as e:
                con.execute(f"CREATE OR REPLACE TABLE {t} AS SELECT * FROM read_csv('{f}', header=true, all_varchar=true)")
                print("  (lecture brute pour", t, ")", str(e)[:80])
        con.execute("""CREATE OR REPLACE VIEW controle_totaux AS
                       SELECT 'propre' AS couche, count(*) AS lignes, sum(montant_ttc) AS ca_ttc FROM propre.ventes
                       UNION ALL SELECT 'brut', count(*), NULL FROM brut.ventes""")
        con.close()
        print("base DuckDB :", dbp)
    except Exception as e:
        print("DuckDB non disponible :", e)

    # ---------------- notices ----------------
    with open(os.path.join(REF, "NOTICE.md"), "w", encoding="utf-8") as f:
        f.write(f"""# Sahel Distribution SA — socle de données du manuel

Généré par `generation_socle.py` (graine {SEED}) le {date.today():%d/%m/%Y}. Toute réexécution produit
des fichiers identiques : les chiffres cités dans le manuel restent valables.

## Le scénario
Grossiste en matériaux et quincaillerie. 5 magasins + 1 dépôt central, 3 ans et 8 mois d'historique
({DEBUT} → {FIN}), un système de caisse (export CSV), un fichier d'objectifs tenu par la direction,
un relevé de stocks tenu par le magasinier, et un fichier de remises tenu à la main par une assistante.
L'enjeu du parcours : *le directeur général attribue la baisse de marge aux prix de vente ; l'analyse
devra montrer le rôle du mélange de produits, des remises et des ruptures.*

## Les tables
| table | fichier | grain | lignes (brut / propre) |
|---|---|---|---|
| ventes | `brut/ventes_brutes.csv` | 1 ligne = 1 article d'un ticket | {len(brut)} / {len(ventes_propres)} |
| clients | `brut/clients.csv` | 1 ligne = 1 client | {len(cli_sale)} / {len(cli)} |
| produits | `brut/produits.csv` | 1 ligne = 1 référence | {len(prod_sale)} / {len(prod)} |
| magasins | `brut/magasins.csv` | 1 ligne = 1 point de vente | {len(mags)} |
| vendeurs | `brut/vendeurs.csv` | 1 ligne = 1 salarié en vente | {len(vds)} |
| objectifs | `brut/objectifs_de_ca.csv` | 1 ligne = 1 magasin × 1 mois | {len(tgt)} |
| stocks | `brut/stocks_quotidiens.csv` | 1 ligne = 1 produit × 1 dépôt × 1 jour | {len(stk)} |
| coûts d'achat | `brut/couts_achat.csv` | 1 ligne = 1 produit × 1 période de prix | {len(couts)} |
| remises manuelles | `brut/remises_manuelles.xlsx` | 1 ligne = 1 client × 1 mois | {len(remises)} |
| calendrier | `reference/dim_date.csv` | 1 ligne = 1 jour | {len(dim)} |

## Défauts volontairement injectés (corrigé enseignant : `rapport_defauts.json`)
{json.dumps(rapport, indent=2, ensure_ascii=False)}

## Règles de gestion (à connaître avant de calculer)
- TVA 18 % ; `montant_ttc = round(montant_ht × 1,18)`, arrondi à l'entier en FCFA.
- `remise` est une proportion (0,08 = 8 %). Les valeurs supérieures à 1 sont une erreur de saisie en points de %.
- Une ligne avec `est_retour = 1` est une marchandise reprise : quantités et montants sont négatifs.
- `id_client = 0` = vente au comptoir sans identification (ce n'est pas une donnée manquante à « remplir »).
- 2026 est une année partielle (janv. → août) : ne jamais comparer 2026 à 2025 en annuel sans le dire.

## Ce qui n'est PAS dans le jeu (et pourquoi c'est utile)
Aucune table de coûts de structure (loyer, salaires, transport) : la **marge brute** est calculable, la
**marge nette** ne l'est pas. Le manuel s'en sert pour enseigner la limite d'un indicateur.
""")
    prod.to_csv(os.path.join(REF, "dictionnaire_produits.csv"), index=False)
    stats = dict(lignes_brutes=len(brut), lignes_propres=len(ventes_propres), ca_ttc_pleine=int(ventes_propres.montant_ttc.sum()),
                 ca_par_annee={int(k): int(v) for k, v in ventes_propres.groupby(ventes_propres.date_vente.dt.year).montant_ttc.sum().items()},
                 fichiers=len(os.listdir(BRUT)) + len(os.listdir(REF)) + len(os.listdir(PROJ)))
    json.dump(stats, open(os.path.join(REF, "stats_generation.json"), "w"), indent=2, ensure_ascii=False)
    print(json.dumps(stats, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="version réduite (20 k lignes) pour un test rapide")
    a = ap.parse_args()
    main(quick=a.quick)
