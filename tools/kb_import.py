#!/usr/bin/env python3
import json, sys
from pathlib import Path
from jsonschema import validate, RefResolver

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "kb" / "schemas"
OUT_RULES = ROOT / "kb" / "rules"
OUT_PROCS = ROOT / "kb" / "procedures"
OUT_CHECKS = ROOT / "kb" / "checklists"
INDEX_DIR = ROOT / "kb" / "index"

def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main(bundle_path: str):
    with open(bundle_path, "r", encoding="utf-8") as f:
        bundle = json.load(f)

    with open(SCHEMAS / "bundle.schema.json","r") as f:
        bundle_schema = json.load(f)
    resolver = RefResolver(base_uri=f"file://{SCHEMAS.as_posix()}/", referrer=bundle_schema)
    validate(instance=bundle, schema=bundle_schema, resolver=resolver)

    for r in bundle["rules"]:
        parts = r["rule_ref"].split(":")
        path = OUT_RULES.joinpath(*parts, r["version"] + ".json")
        write_json(path, r)

    for p in bundle["procedures"]:
        path = OUT_PROCS / p["id"] / (p["version"] + ".json")
        write_json(path, p)

    for c in bundle["checklists"]:
        path = OUT_CHECKS / c["stage"] / (c["version"] + ".json")
        write_json(path, c)

    manifest = {
        "rules": [r["rule_ref"] + "@" + r["version"] for r in bundle["rules"]],
        "procedures": [p["id"] + "@" + p["version"] for p in bundle["procedures"]],
        "checklists": [c["stage"] + "@" + c["version"] for c in bundle["checklists"]],
        "meta": bundle.get("meta", {})
    }
    write_json(INDEX_DIR / "manifest.json", manifest)

    roblox_rules = [r for r in bundle["rules"] if r["category"] in ["export","roblox","performance"]]
    write_json(INDEX_DIR / "by_engine" / "roblox.json", roblox_rules)

    export_rules = [r for r in bundle["rules"] if r["category"] == "export"]
    write_json(INDEX_DIR / "by_category" / "export.json", export_rules)

    print("Import OK")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: kb_import.py kb/bundles/kb_bundle_v1.json", file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1])
