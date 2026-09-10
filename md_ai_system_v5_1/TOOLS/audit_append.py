# -*- coding: utf-8 -*-
"""Ajoute une transition au journal d'audit .md-ai-system/AUDIT.jsonl.

Usage direct. En pratique, `TOOLS/mdai.py finish-stage` l'appelle pour toi.

Journal append-only : une transition = une ligne JSON. Aucune ligne n'est
modifiée ni supprimée. Le format est fixé par WORKFLOW-RULES.md.

Exemple :
  python TOOLS/audit_append.py --category 02-STACK --stage 4-IA4-CONTROLE.md \
      --mode NEW_WORK --actor IA4 --provider chatgpt --from-status null --to-status VALIDÉ \
      --commit a1b2c3d --summary "stack validée, tests réels passés"
"""
from __future__ import print_function
import argparse
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / ".md-ai-system" / "AUDIT.jsonl"
MANIFEST = ROOT / "MANIFEST.json"

FIELDS = ["ts", "category", "stage", "mode", "actor", "provider", "from_status",
          "to_status", "commit", "summary"]
STAGES = ["1-IA1-ANALYSE.md", "2-IA2-VERIFICATION.md", "3-IA3-EXECUTION.md",
          "4-IA4-CONTROLE.md", "—"]
ACTORS = ["IA1", "IA2", "IA3", "IA4", "HUMAIN", "OUTIL"]
MODES = ["NEW_WORK", "REVALIDATION", "CORRECTION"]
STATUSES = ["null", "VALIDÉ", "REFUSÉ", "BLOQUÉ", "EN_ATTENTE_DE_DÉCISION",
            "À_RÉÉVALUER", "EN_REVALIDATION", "TERMINÉ"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--category", required=True)
    parser.add_argument("--stage", required=True, choices=STAGES)
    parser.add_argument("--mode", required=True, choices=MODES)
    parser.add_argument("--actor", required=True, choices=ACTORS)
    parser.add_argument("--from-status", required=True, choices=STATUSES)
    parser.add_argument("--to-status", required=True, choices=STATUSES)
    parser.add_argument("--provider", default=None, help="IA ayant réalisé l'étape")
    parser.add_argument("--commit", default=None)
    parser.add_argument("--summary", required=True)
    args = parser.parse_args()

    slugs = {c["slug"] for c in json.loads(MANIFEST.read_text(encoding="utf-8"))["categories"]}
    if args.category not in slugs:
        raise SystemExit("Catégorie inconnue : {}".format(args.category))
    if not args.summary.strip():
        raise SystemExit("--summary ne peut pas être vide")

    record = {
        "ts": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "category": args.category,
        "stage": args.stage,
        "mode": args.mode,
        "actor": args.actor,
        "provider": args.provider,
        "from_status": None if args.from_status == "null" else args.from_status,
        "to_status": None if args.to_status == "null" else args.to_status,
        "commit": args.commit,
        "summary": args.summary.strip(),
    }
    line = json.dumps({k: record[k] for k in FIELDS}, ensure_ascii=False, sort_keys=True)
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
