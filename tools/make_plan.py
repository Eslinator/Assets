#!/usr/bin/env python3
import json, sys, pathlib
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "plans"

def h1(x): return f"# {x}\n\n"
def h2(x): return f"## {x}\n\n"
def li(x): return f"- {x}\n"

# Map common Unicode glyphs to ASCII-safe equivalents
ASCII_MAP = {
    0x2014: "-",   # em dash —
    0x2013: "-",   # en dash –
    0x2212: "-",   # minus −
    0x2264: "<=",  # ≤
    0x2265: ">=",  # ≥
    0x00B1: "+/-", # ±
    0x00A0: " ",   # nbsp
    0x00A7: "Sec " # §
}
def ascii_safe(s: str) -> str:
    return s.translate(ASCII_MAP)

def main(resolved_path: str):
    p = pathlib.Path(resolved_path)
    data = json.loads(p.read_text("utf-8"))
    asset = data["asset_spec"]["data"]
    rules = [r["data"] for r in data["rules"]]
    procs = [pr["data"] for pr in data["procedures"]]
    checks = [c["data"] for c in data["checklists"]]

    name = asset["asset_id"]
    out = []
    out.append(h1(f"Build Plan - {name}"))
    out.append(li(f"Purpose: {asset.get('purpose','')}"))
    out.append(li(f"Hero tier: {asset.get('hero_tier','')}"))
    out.append(li(f"Targets: {', '.join(asset.get('target_engine',[]))}"))
    tex_str = ", ".join([f"{t['map']} {t['size_px']}px" for t in asset['budgets'].get('textures', [])])
    out.append(li(f"Budget: <= {asset['budgets']['tris_max']} tris; textures: {tex_str}"))
    out.append("\n")

    # Constraints
    out.append(h2("Constraints (sorted by severity)"))
    sev_order = {"blocker":0,"warn":1,"advice":2}
    for r in sorted(rules, key=lambda x: sev_order.get(x.get("severity","warn"), 9)):
        s = r.get("statement","")
        units = f" [{r['units']}]" if r.get("units") else ""
        out.append(li(f"{r['severity'].upper()}: {s}{units} (ref: {r['rule_ref']})"))
    out.append("\n")

    # Build plan by phase
    out.append(h2("Blender Build Plan (phase order)"))
    phase_order = {"blockout":0,"model":1,"uv":2,"bake":3,"texture":4,"export":5,"qa":6}
    for pr in sorted(procs, key=lambda x: phase_order.get(x.get("phase","zz"), 99)):
        out.append(f"### {pr['phase'].upper()} - {pr['id']}\n\n")
        for s in pr.get("steps", []):
            out.append(li(s))
        if pr.get("metrics"):
            metrics_str = ", ".join([f"{m['name']}={m['target']} {m['unit']}" for m in pr["metrics"]])
            out.append(f"\n**Metrics:** {metrics_str}\n")
        if pr.get("DoD"):
            out.append(f"**Definition of Done:** {pr['DoD']}\n\n")

    # Checklists
    out.append(h2("Checklists"))
    for chk in checks:
        title = chk['stage'].replace('_',' ').title()
        out.append(f"### {title}\n\n")
        for item in chk.get("items", []):
            out.append(li(item))
        out.append("\n")

    # Sources
    out.append(h2("Provenance"))
    for s in asset.get("sources", []):
        out.append(li(f"{s['title']} - {s['url']}"))
    out.append("\n")

    # Write ASCII-safe content
    OUT.mkdir(parents=True, exist_ok=True)
    outfile = OUT / f"{name}.md"
    content = "".join(out)
    outfile.write_text(ascii_safe(content), encoding="utf-8")
    print(f"Wrote {outfile}")

if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("usage: make_plan.py <resolved_pack.json>", file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1])
