#!/usr/bin/env python3
import json, sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "kb"

def latest_version_file(dirpath: Path):
    vers = []
    for p in dirpath.glob("*.json"):
        m = re.match(r"(\d+)\.(\d+)\.(\d+)\.json$", p.name)
        if m:
            vers.append((tuple(map(int, m.groups())), p))
    if not vers:
        return None
    return sorted(vers)[-1][1]

def load_asset_spec(asset_id: str):
    aset_dir = KB / "assets" / asset_id
    if not aset_dir.exists():
        sys.exit(f"ERR: asset not found: {aset_dir}")
    f = latest_version_file(aset_dir)
    if not f:
        sys.exit(f"ERR: no versioned spec in {aset_dir}")
    with open(f, "r", encoding="utf-8") as fh:
        spec = json.load(fh)
    return spec, f

def load_rule(rule_ref: str):
    parts = rule_ref.split(":")
    rule_dir = KB / "rules" / Path(*parts)
    f = latest_version_file(rule_dir)
    if not f:
        sys.exit(f"ERR: rule not found: {rule_dir}")
    with open(f, "r", encoding="utf-8") as fh:
        rule = json.load(fh)
    return rule, f

def load_all_procedures():
    out = []
    for proc_dir in (KB / "procedures").iterdir():
        if not proc_dir.is_dir(): continue
        f = latest_version_file(proc_dir)
        if f:
            with open(f, "r", encoding="utf-8") as fh:
                out.append((json.load(fh), f))
    return out

def load_all_checklists():
    out = []
    for stage_dir in (KB / "checklists").iterdir():
        if not stage_dir.is_dir(): continue
        f = latest_version_file(stage_dir)
        if f:
            with open(f, "r", encoding="utf-8") as fh:
                out.append((json.load(fh), f))
    return out

def main(asset_id: str):
    asset, asset_path = load_asset_spec(asset_id)
    # Resolve rules referenced by constraints
    rules = []
    for c in asset.get("constraints", []):
        rule, rpath = load_rule(c["rule_ref"])
        rules.append({"path": str(rpath), "data": rule})

    # Pull in all procedures & checklists (simple v1 strategy)
    procs = [{"path": str(p), "data": d} for (d, p) in load_all_procedures()]
    checks = [{"path": str(p), "data": d} for (d, p) in load_all_checklists()]

    resolved = {
        "resolved_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "asset_spec": {"path": str(asset_path), "data": asset},
        "rules": rules,
        "procedures": procs,
        "checklists": checks
    }
    json.dump(resolved, sys.stdout, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: resolve_asset.py <asset_id>", file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1])
