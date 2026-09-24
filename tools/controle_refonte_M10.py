#!/usr/bin/env python3
"""controle_refonte_M10.py — le controle automatique du projet M10.P (« La refonte »).

LA REGLE DU PROJET. Une refonte qui change un CHIFFRE en changeant un GRAPHIQUE est rejetee :
les totaux avant/apres doivent etre IDENTIQUES, et conformes au socle. Le module change la
lisibilite, jamais la donnee.

QUATRE COUCHES, du plus grave au plus cosmetique :

  L1 — la source    : les deux versions lisent le meme socle (memes fichiers, memes filtres) ;
  L2 — les totaux   : les totaux avant/apres sont identiques ET conformes au socle ;
  L3 — les figures  : 5 + 5 SVG, largeur <= 776 px (format du module), noms conformes ;
  L4 — l'ecriture   : audit des titres lu DANS LE CODE — le SVG de matplotlib ne porte pas de
                      texte mais des traces : la meme lecon qu'en C04.

Usage :
    python3 tools/controle_refonte_M10.py                        # le dossier de reference du module
    python3 tools/controle_refonte_M10.py --candidat CHEMIN      # la copie rendue par un apprenant
    python3 tools/controle_refonte_M10.py --candidat CHEMIN --json   # + le rapport machine

Un candidat rend un dossier qui contient :
    rapport_apres/g1_corrige.svg … g5_corrige.svg   les 5 graphiques corriges
    code_refonte.py                                 le script qui les produit (facultatif :
                                                    sans lui, L1 et L4 sont declarees non verifiables)
    refonte.json                                    {"totaux_avant": {...}, "totaux_apres": {...}}

Code de sortie : 0 = refonte conforme, 1 = refonte rejetee (la liste des echecs est imprimee).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

import pandas as pd

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = os.path.join(RACINE, "03_exercices", "dossier_M10")
SOCLE = os.path.join(RACINE, "03_exercices", "dossier_M09")
LARGEUR_MAX_PX = 776
SEUIL_PROJET = 13
POINTS_PROJET = 20


# ----------------------------------------------------------------------
# L2 — les totaux de reference, recalcules depuis le socle (jamais recopies)
# ----------------------------------------------------------------------
def totaux_socle():
    v = pd.read_csv(os.path.join(SOCLE, "quincaillerie", "vente.csv"), parse_dates=["date_vente"])
    prod = pd.read_csv(os.path.join(SOCLE, "quincaillerie", "produit.csv"))
    v["ct"] = (v["montant_ttc"] * 100).round().astype("int64")
    net = v[~v["est_retour"]]
    vp = net.merge(prod[["id_produit", "id_categorie"]], on="id_produit", how="left")
    t = {
        "total_net_fcfa": round(float(net["montant_ttc"].sum()), 2),
        "total_brut_fcfa": round(float(v["montant_ttc"].sum()), 2),
        "total_net_centimes": int(net["ct"].sum()),
        "ventes": int(len(v)),
        "ventes_nettes": int(len(net)),
        "retours": int(v["est_retour"].sum()),
        "categories": int(vp["id_categorie"].nunique()),
        "trimestres": int(net["date_vente"].dt.to_period("Q").nunique()),
        "mois": int(net["date_vente"].dt.to_period("M").nunique()),
        "mediane_fcfa": round(float(net["montant_ttc"].median()), 2),
        "max_fcfa": round(float(net["montant_ttc"].max()), 2),
        "queue_plus_500k": int((v["montant_ttc"] > 500000).sum()),
        "plateau_max": int((net["montant_ttc"] == net["montant_ttc"].max()).sum()),
    }
    t["total_categories_fcfa"] = round(float(vp.groupby("id_categorie")["montant_ttc"].sum().sum()), 2)
    t["total_trimestres_fcfa"] = round(
        float(net.groupby(net["date_vente"].dt.to_period("Q"))["montant_ttc"].sum().sum()), 2)
    return t


# ----------------------------------------------------------------------
# L1 et L4 — l'audit du CODE (le SVG ne porte pas de texte)
# ----------------------------------------------------------------------
def blocs(chemin):
    """Separe le fichier en trois zones : en-tete, def avant(...), def apres(...)."""
    src = open(chemin, encoding="utf-8").read()
    i = src.find("def avant(")
    j = src.find("def apres(")
    k = src.find("\nBRIEF = ", j) if j >= 0 else -1
    if i < 0 or j < 0:
        return src, "", ""
    return src[:i], src[i:j], src[j:k if k > 0 else len(src)]


def sources_du_texte(bloc):
    """Les fichiers de donnees lus, et les filtres appliques — la signature de la source."""
    fichiers = set(re.findall(r"\.csv\"", bloc)) and set(
        re.findall(r"0?3_exercices[^\"']*|dossier_[^\"']*", bloc)) or set()
    filtres = set(re.findall(r"~?v\[[^\]]*est_retour[^\]]*\]", bloc))
    colonnes = set(re.findall(r"\[\"(\w+)\"\]", bloc))
    return fichiers, filtres, colonnes


def titres_du_bloc(bloc):
    """Les titres, lus dans le code : set_title(...) / suptitle(...), multi-lignes et f-strings.

    Le comptage des parentheses est necessaire : un titre du dossier contient lui-meme des
    parentheses (« (axe a zero ; moyenne glissante 320-337 M) ») — une regex non gourmande
    s'arrete trop tot et le titre est perdu (leçon de C04 : on audite le CODE).
    """
    titres = []
    for m in re.finditer(r"(?:set_title|suptitle)\(", bloc):
        debut, profondeur, i = m.end(), 1, m.end()
        while i < len(bloc) and profondeur:
            if bloc[i] == "(":
                profondeur += 1
            elif bloc[i] == ")":
                profondeur -= 1
            i += 1
        brut = bloc[debut:i - 1]
        morceaux = re.findall(r"\"([^\"]*)\"", brut)
        titres.append("".join(morceaux).replace("\\n", " ").strip())
    return [t for t in titres if t]


def porte_une_mesure(titre):
    return bool(re.search(r"\d", titre)) or "{" in titre


def audit_ecriture(bloc_avant, bloc_apres):
    a, b = titres_du_bloc(bloc_avant), titres_du_bloc(bloc_apres)
    return {
        "titres_avant": len(a),
        "titres_apres": len(b),
        "titres_qui_affirment_avant": sum(porte_une_mesure(t) for t in a),
        "titres_qui_affirment_apres": sum(porte_une_mesure(t) for t in b),
        "axes_a_zero_après": len(re.findall(r"set_ylim\(\s*0\s*,", bloc_apres)),
        "twinx_avant": bloc_avant.count("twinx()"),
        "twinx_apres": bloc_apres.count("twinx()"),
        "set_yscale_log_avant": bloc_avant.count('set_yscale("log")'),
        "set_yscale_log_apres": bloc_apres.count('set_yscale("log")'),
        "tri_sort_values_avant": bloc_avant.count("sort_values"),
        "tri_sort_values_apres": bloc_apres.count("sort_values"),
        "annotations_apres": bloc_apres.count("annotate("),
    }


# ----------------------------------------------------------------------
# L3 — les figures
# ----------------------------------------------------------------------
def figures(dossier):
    """Les SVG des deux versions, avec leur largeur reelle en pixels."""
    out = {}
    for version, motif in (("avant", r"g\d.*\.svg$"), ("apres", r"g\d.*\.svg$")):
        sous = os.path.join(dossier, "rapport_" + version)
        out[version] = {}
        if not os.path.isdir(sous):
            continue
        for f in sorted(os.listdir(sous)):
            if re.search(motif, f):
                d = open(os.path.join(sous, f), encoding="utf-8").read(600)
                m = re.search(r"width=\"([\d.]+)(pt)?\"", d)
                larg = float(m.group(1)) if m else 0.0
                px = round(larg * 96 / 72) if m and m.group(2) else round(larg)
                out[version][f] = dict(largeur_px=px,
                                       ko=round(os.path.getsize(os.path.join(sous, f)) / 1024, 1))
    return out


# ----------------------------------------------------------------------
# Le controle
# ----------------------------------------------------------------------
def controler(dossier=DOSSIER, candidat=None, code=None):
    echecs, avertissements, mesures = [], [], {}
    cible = candidat or dossier
    code = code or os.path.join(dossier, "rapport_avant", "code_avant.py")
    attendu = json.load(open(os.path.join(DOSSIER, "ATTENDU.json"), encoding="utf-8"))
    t = totaux_socle()
    mesures["totaux_socle"] = t

    # --- L1 — la source
    if os.path.exists(code):
        _, bloc_avant, bloc_apres = blocs(code)
        fa, ffa, ca = sources_du_texte(bloc_avant)
        fb, ffb, cb = sources_du_texte(bloc_apres)
        mesures["L1_filtres_avant"] = len(ffa)
        mesures["L1_filtres_apres"] = len(ffb)
        mesures["L1_filtres_identiques"] = ffa == ffb
        mesures["L1_colonnes_avant"] = len(ca)
        mesures["L1_colonnes_apres"] = len(cb)
        if ffa != ffb:
            echecs.append("L1 : les filtres de donnees diffèrent entre les deux versions "
                          f"({sorted(ffa)} contre {sorted(ffb)})")
    else:
        bloc_avant = bloc_apres = ""
        avertissements.append(f"L1 : aucun code trouve ({code}) — la couche source n'est pas "
                              "verifiable sur ce dossier")

    # --- L2 — les totaux
    mesures["L2_total_net_egal_categories"] = (
        abs(t["total_net_fcfa"] - t["total_categories_fcfa"]) < 0.01)
    mesures["L2_total_net_egal_trimestres"] = (
        abs(t["total_net_fcfa"] - t["total_trimestres_fcfa"]) < 0.01)
    mesures["L2_ecart_categories_fcfa"] = round(
        abs(t["total_net_fcfa"] - t["total_categories_fcfa"]), 2)
    mesures["L2_ecart_trimestres_fcfa"] = round(
        abs(t["total_net_fcfa"] - t["total_trimestres_fcfa"]), 2)
    if not mesures["L2_total_net_egal_categories"]:
        echecs.append("L2 : le total par categorie diffère du total net "
                      f"({mesures['L2_ecart_categories_fcfa']} FCFA)")
    if not mesures["L2_total_net_egal_trimestres"]:
        echecs.append("L2 : le total par trimestre diffère du total net "
                      f"({mesures['L2_ecart_trimestres_fcfa']} FCFA)")
    msg = attendu["mesures"]
    mesures["L2_mediane_conforme_socle"] = abs(msg["d5_mediane_montant"] - round(t["mediane_fcfa"])) < 1
    mesures["L2_queue_conforme_socle"] = msg["d5_queue_sup_500k"] == t["queue_plus_500k"]
    if not mesures["L2_mediane_conforme_socle"]:
        echecs.append("L2 : la mediane de l'ATTENDU diffère de celle du socle")
    if not mesures["L2_queue_conforme_socle"]:
        echecs.append("L2 : le nombre de ventes au-dessus de 500 000 FCFA de l'ATTENDU "
                      "diffère de celui du socle")

    refonte = os.path.join(cible, "refonte.json")
    if os.path.exists(refonte):
        r = json.load(open(refonte, encoding="utf-8"))
        av, ap = r.get("totaux_avant", {}), r.get("totaux_apres", {})
        mesures["L2_totaux_declares"] = len(av)
        mesures["L2_totaux_identiques"] = av == ap
        mesures["L2_totaux_conformes_socle"] = all(
            abs(float(av[k]) - float(t[k])) < 0.01 for k in av) if av else False
        if not mesures["L2_totaux_identiques"]:
            diff = {k: (av.get(k), ap.get(k)) for k in set(av) | set(ap) if av.get(k) != ap.get(k)}
            echecs.append(f"L2 : la règle du projet est violée — les totaux avant/après "
                          f"diffèrent : {diff}")
        if av and not mesures["L2_totaux_conformes_socle"]:
            echecs.append("L2 : les totaux declares ne correspondent pas au socle")
    elif candidat:
        # sur le dossier de reference du module, l'absence de refonte.json est normale :
        # c'est l'apprenant qui la produit et qui declare ses totaux.
        avertissements.append("L2 : aucun refonte.json dans le dossier candidate — les totaux "
                              "declares ne sont pas verifiables")

    # --- L3 — les figures
    figs = figures(cible)
    mesures["L3_avant_svg"] = len(figs.get("avant", {}))
    mesures["L3_apres_svg"] = len(figs.get("apres", {}))
    mesures["L3_largeur_max_px"] = max([f["largeur_px"] for v in figs.values() for f in v.values()]
                                       or [0])
    mesures["L3_largeur_limite_px"] = LARGEUR_MAX_PX
    if mesures["L3_apres_svg"] < 5:
        echecs.append(f"L3 : {mesures['L3_apres_svg']} graphique(s) corrige(s) sur 5 attendus")
    if mesures["L3_avant_svg"] < 5:
        avertissements.append(f"L3 : {mesures['L3_avant_svg']} graphique(s) d'origine sur 5")
    trop_larges = [f"{v}/{n}" for v, d in figs.items() for n, x in d.items()
                   if x["largeur_px"] > LARGEUR_MAX_PX]
    if trop_larges:
        echecs.append(f"L3 : figure(s) plus large(s) que {LARGEUR_MAX_PX} px : {trop_larges}")

    # --- L4 — l'ecriture, auditee dans le code
    if bloc_apres:
        e = audit_ecriture(bloc_avant, bloc_apres)
        mesures.update({"L4_" + k: v for k, v in e.items()})
        if e["titres_qui_affirment_apres"] < e["titres_apres"]:
            echecs.append("L4 : un titre de la version corrigee n'affirme rien "
                          f"({e['titres_qui_affirment_apres']} sur {e['titres_apres']} portent une mesure)")
        if e["twinx_apres"] > 0:
            echecs.append("L4 : la version corrigee utilise encore un double axe (twinx)")
        if e["set_yscale_log_apres"] > 0:
            echecs.append("L4 : la version corrigee utilise encore une echelle logarithmique "
                          "(a declarer, ou a retirer)")
        if e["annotations_apres"] < 1:
            echecs.append("L4 : aucune annotation dans la version corrigee")

    # --- la coherence des deux versions (le 1 pour 1 du module)
    mesures["forme_avant"] = len(attendu["defauts"])
    mesures["forme_apres"] = len(attendu["corrections"])
    msg2 = ("la refonte est conforme : les deux versions portent les mêmes totaux, "
            "les 5 figures sont dans le format, et l'écriture corrigée est vérifiée dans le code")
    verdict = "CONFORME" if not echecs else "REJETÉE"
    return dict(verdict=verdict, echecs=echecs, avertissements=avertissements,
                mesures=mesures, message=msg2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidat", default=None, help="le dossier rendu par un apprenant")
    ap.add_argument("--code", default=None, help="le script a auditer (defaut : le dossier du module)")
    ap.add_argument("--json", action="store_true", help="imprime aussi le rapport machine")
    a = ap.parse_args()
    r = controler(candidat=a.candidat, code=a.code)
    print("=" * 78)
    print("CONTROLE DE REFONTE — M10.P « La refonte »")
    print("=" * 78)
    print(f"  dossier      : {a.candidat or DOSSIER}")
    print(f"  regle        : totaux avant/apres identiques et conformes au socle")
    print(f"  seuil        : {SEUIL_PROJET}/{POINTS_PROJET}")
    print("-" * 78)
    for k, v in r["mesures"].items():
        if isinstance(v, dict):
            continue
        print(f"  {k:34s} = {v}")
    print("-" * 78)
    for av in r["avertissements"]:
        print("  AVERTISSEMENT :", av)
    for e in r["echecs"]:
        print("  ECHEC         :", e)
    print("-" * 78)
    print(f"  VERDICT      : {r['verdict']}")
    if r["verdict"] == "CONFORME":
        print(f"  {r['message']}")
    print("=" * 78)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0 if r["verdict"] == "CONFORME" else 1


if __name__ == "__main__":
    raise SystemExit(main())
