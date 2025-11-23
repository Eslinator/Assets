#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 4 ]]; then
  echo "usage: $0 <asset_id> <purpose> <tris_max> <tex_size_px> [hero|mid|background]" >&2
  exit 2
fi

ASSET_ID="$1"
PURPOSE="$2"
TRIS_MAX="$3"
TEX="$4"
HERO_TIER="${5:-mid}"

ASSET_DIR="kb/assets/${ASSET_ID}"
mkdir -p "${ASSET_DIR}"

cat > "${ASSET_DIR}/1.0.0.json" <<JSON
{
  "type": "asset_spec",
  "version": "1.0.0",
  "asset_id": "${ASSET_ID}",
  "purpose": "${PURPOSE}",
  "hero_tier": "${HERO_TIER}",
  "target_engine": ["Roblox","Unreal"],
  "budgets": {
    "tris_max": ${TRIS_MAX},
    "textures": [
      {"map":"ORM","size_px":${TEX}},
      {"map":"Normal","size_px":${TEX}},
      {"map":"BaseColor","size_px":${TEX}}
    ]
  },
  "lod_plan": [{"name":"HIGH"},{"name":"MED"},{"name":"LOW"}],
  "constraints": [
    {"rule_ref":"OPT:ROBLOX:MESHPART_TRIS_MAX","severity":"blocker"},
    {"rule_ref":"EXPORT:AXIS:NEG_Z_FWD_Y_UP","severity":"blocker"},
    {"rule_ref":"LOD:PRESENT_HIGH_MED_LOW","severity":"blocker"}
  ],
  "scale_units": {"m_per_unit":1.0,"roblox_stud_per_m":3.571},
  "sources": [
    {"url":"/mnt/data/unknown-unknowns-2025.md","title":"Unknown Unknowns 2025"},
    {"url":"/mnt/data/paas-validation-principles.md","title":"PaaS Validation Principles"}
  ]
}
JSON

echo "created ${ASSET_DIR}/1.0.0.json"
