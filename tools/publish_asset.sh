#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 5 ]]; then
  echo "usage: $0 <asset_id> <purpose> <tris> <tex> <tier>" >&2; exit 2
fi
ID="$1"; PURPOSE="$2"; TRIS="$3"; TEX="$4"; TIER="$5"
./tools/new_asset.sh "$ID" "$PURPOSE" "$TRIS" "$TEX" "$TIER"
. .venv/bin/activate
python tools/resolve_asset.py "$ID" > "kb/index/resolved/${ID}.json"
python tools/make_plan.py "kb/index/resolved/${ID}.json"
git add "kb/assets/${ID}" "kb/index/resolved/${ID}.json" "plans/${ID}.md"
git commit -m "Add ${ID} asset + pack + plan" || true
git push
echo "✅ Published ${ID}"
