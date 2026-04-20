#!/bin/bash
# Copie site/ vers le miroir Documents/GitHub/caswingue-v3/ prêt à push.
# Usage: npm run deploy:local
set -e

SRC="/Users/mathieuvirondaud/claude/golf/ça_swingue_3/site"
DST="/Users/mathieuvirondaud/Documents/GitHub/caswingue-v3"

if [ ! -d "$DST" ]; then
  echo "❌ $DST n'existe pas encore."
  echo "   Clone d'abord : gh repo clone caswingue-v3 $DST"
  echo "   ou : git clone https://github.com/virondaud/caswingue-v3.git $DST"
  exit 1
fi

# Build + integrity
cd "$(dirname "$0")/.."
npm run build

# Sync (rsync pour ne copier que les diffs)
rsync -a --delete \
  --exclude='.git' \
  --exclude='.DS_Store' \
  --exclude='node_modules' \
  "$SRC/" "$DST/"

# Copier integrity.json à la racine
cp "$SRC/integrity.json" "$DST/integrity.json" 2>/dev/null || true

echo ""
echo "✅ Synchronisation OK. À pousser :"
echo "   cd $DST"
echo "   git add -A && git commit -m 'msg' && git push"
