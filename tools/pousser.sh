#!/usr/bin/env bash
# Pousse vers nayxuspro-sketch/MesCours en AJOUT SEUL, selon la procedure mise au point
# apres l'incident PATCH_11 (le force-push ecraserait le disque incomplet).
#
#   bash tools/pousser.sh <jeton> "<message de commit>" <chemin> [<chemin> ...]
#
# Le jeton n'est jamais ecrit dans un fichier : il est passe en argument, teste par
# l'API avant tout, et n'apparait que dans l'URL de push (le remote enregistre sans
# identifiants echoue avec « could not read Username »).
set -euo pipefail

JETON="${1:?usage : pousser.sh <jeton> \"<message>\" <chemin> [<chemin> ...]}"; shift
MESSAGE="${1:?message de commit manquant}"; shift
if [ "$#" -lt 1 ]; then echo "aucun chemin nomme : rien a pousser"; exit 1; fi

RACINE="$(cd "$(dirname "$0")/.." && pwd)"; cd "$RACINE"

# 1. le jeton est teste AVANT tout (lecon PATCH_1)
CODE=$(curl -s -o /dev/null -w '%{http_code}' -H "Authorization: token ${JETON}" \
       https://api.github.com/user)
PAGE=$(curl -s -o /dev/null -w '%{http_code}' -H "Authorization: token ${JETON}" \
       "https://github.com/nayxuspro-sketch/MesCours.git/info/refs?service=git-receive-pack" \
       -u "x-access-token:${JETON}")
echo "jeton : API /user -> ${CODE} · droit d'ecriture annonce -> ${PAGE}"
if [ "${CODE}" != "200" ]; then echo "jeton refuse par l'API : push annule"; exit 2; fi

# 2. reprise du remote a l'identique, puis ajout seul (lecon PATCH_11)
rm -rf .git
git init -q -b main
git config user.name "nayxuspro-sketch"
git config user.email "nayxuspro-sketch@users.noreply.github.com"
git fetch -q --depth 1 https://github.com/nayxuspro-sketch/MesCours.git main
git update-ref refs/heads/main FETCH_HEAD
git read-tree main
echo "arbre local aligne sur $(git rev-parse --short HEAD)"

# 3. seuls les chemins nommes sont indexes : jamais « git add -A » (les PDF deplaces
#    vers /tmp apparaissent en « D » et seraient supprimes du remote)
for CHEMIN in "$@"; do
  if [ ! -e "${CHEMIN}" ]; then echo "chemin absent, push annule : ${CHEMIN}"; exit 3; fi
done
git add "$@"
git commit -q -m "${MESSAGE}"

# 4. push avec le jeton dans l'URL
git push -q "https://${JETON}@github.com/nayxuspro-sketch/MesCours.git" main
echo "push OK : $(git rev-parse --short HEAD)"

# 5. bundle AVANT la suppression de .git (lecon PATCH_2)
BUNDLE="/tmp/mesCours_$(git rev-parse --short HEAD).bundle"
git bundle create "${BUNDLE}" main >/dev/null 2>&1
git bundle verify "${BUNDLE}" 2>&1 | head -1
git ls-remote https://github.com/nayxuspro-sketch/MesCours.git main | cut -c1-12

# 6. .git local supprime apres chaque push (regle de cadence)
rm -rf .git
echo ".git supprime · bundle : ${BUNDLE}"
