# -*- coding: utf-8 -*-
from __future__ import print_function
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = ROOT / ".md-ai-system" / "state"
OUT = ROOT / ".md-ai-system" / "STATE-OVERVIEW.md"
MANIFEST = ROOT / "MANIFEST.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def computed_display(state, states):
    app = state.get("applicability")
    if app == "N/A":
        return "N/A"
    if app != "ACTIVE":
        return app or "TO_DEFINE"
    status = state.get("status")
    if status:
        return status
    for dep in state.get("dependencies", []):
        ds = states.get(dep, {})
        if ds.get("applicability") == "ACTIVE" and ds.get("status") != "VALIDÉ":
            return "BLOQUÉ"
    return "À FAIRE"


def main():
    manifest = load(MANIFEST)
    states = {}
    for path in STATE_DIR.glob("*.json"):
        s = load(path)
        states[s["category"]] = s
    lines = ["# STATE OVERVIEW", "", "Vue générée depuis les JSON. Ne pas éditer manuellement.", "", "| Priorité | Catégorie | Applicabilité | Statut | Mode | Dernière validation | Blocages |", "|---:|---|---|---|---|---|---|"]
    for c in sorted(manifest["categories"], key=lambda x: x["execution_priority"]):
        s = states.get(c["slug"], {})
        last = s.get("last_validation") or {}
        cycle = s.get("current_cycle") or {}
        blockers = "; ".join(s.get("open_blockers") or []) or "—"
        lines.append("| {p} | `{slug}` | {app} | {status} | {mode} | {commit} | {blockers} |".format(
            p=c["execution_priority"], slug=c["slug"], app=s.get("applicability", "TO_DEFINE"),
            status=computed_display(s, states), mode=cycle.get("mode", "—"),
            commit=last.get("commit") or s.get("validation_commit") or "—", blockers=blockers))
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(str(OUT))


if __name__ == "__main__":
    main()
