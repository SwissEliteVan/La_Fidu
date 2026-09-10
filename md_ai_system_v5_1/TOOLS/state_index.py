# -*- coding: utf-8 -*-
"""Régénère l'index global .md-ai-system/STATE.json depuis les états par catégorie.

L'état atomique par catégorie (.md-ai-system/state/<CATEGORY>.json) est la source
de vérité. STATE.json en est une projection : il ne doit jamais être édité à la
main ni diverger.
"""
from __future__ import print_function
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "MANIFEST.json"
STATE_DIR = ROOT / ".md-ai-system" / "state"
OUT = ROOT / ".md-ai-system" / "STATE.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build():
    manifest = load(MANIFEST)
    schema_version = manifest.get("schema_version", "2.0")
    categories = {}
    missing = []
    for c in manifest["categories"]:
        slug = c["slug"]
        path = STATE_DIR / "{}.json".format(slug)
        if not path.exists():
            missing.append(slug)
            continue
        s = load(path)
        categories[slug] = {
            "applicability": s.get("applicability", "TO_DEFINE"),
            "state_file": "state/{}.json".format(slug),
            "status": s.get("status"),
            "validation_commit": (s.get("last_validation") or {}).get("commit")
            or s.get("validation_commit"),
        }
    if missing:
        raise SystemExit("État manquant pour : {}".format(", ".join(missing)))
    return {"categories": categories, "schema_version": schema_version}


def main():
    payload = build()
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    previous = OUT.read_text(encoding="utf-8") if OUT.exists() else None
    OUT.write_text(text, encoding="utf-8")
    print("{} ({})".format(OUT, "inchangé" if previous == text else "mis à jour"))


if __name__ == "__main__":
    main()
