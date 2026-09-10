# -*- coding: utf-8 -*-
"""Vérifie la cohérence interne du système MD AI.

Ne modifie rien. Sort en code 1 si un contrôle échoue.

Contrôles :
  1. comptes du manifeste ;
  2. présence des 216 prompts, absence de prompt orphelin ;
  3. graphe de dépendances == manifeste, absence de cycle (recalculée) ;
  4. EXECUTION-MATRIX.md == manifeste ;
  5. READING-ORDER.md == manifeste ;
  6. états par catégorie : dépendances, applicabilité, vocabulaire de statut ;
  7. STATE.json == projection des états par catégorie ;
  8. empreintes SNAPSHOTS.json des prompts ;
  9. empreintes MANIFEST.json des fichiers système immuables ;
 10. références de chemins système résolvables ;
 11. cohérence CONFIG / contraintes de déploiement ;
 12. cohérence des schema_version ;
 13. format du journal d'audit ;
 14. schéma des décisions verrouillées ;
 15. double contrôle par deux IA différentes.

Les fichiers d'exécution changent par construction pendant un projet : ils sont
listés dans MANIFEST.runtime_files, sans empreinte.
"""
from __future__ import print_function
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STAGES = ["1-IA1-ANALYSE.md", "2-IA2-VERIFICATION.md", "3-IA3-EXECUTION.md", "4-IA4-CONTROLE.md"]
APPLICABILITIES = {"ACTIVE", "N/A", "TO_DEFINE"}
CATEGORY_STATUSES = {
    None, "VALIDÉ", "REFUSÉ", "BLOQUÉ", "EN_ATTENTE_DE_DÉCISION",
    "À_RÉÉVALUER", "EN_REVALIDATION", "TERMINÉ",
}
MODES = {None, "NEW_WORK", "REVALIDATION", "CORRECTION"}
RUNTIME_PREFIX = ".md-ai-system/"
REF_PREFIXES = ("PROMPTS/", "TEMPLATES/", "TOOLS/", "TESTS/")
SCHEMA_VERSION = "2.2"
AUDIT_FIELDS = ["ts", "category", "stage", "mode", "actor", "provider", "from_status",
                "to_status", "commit", "summary"]
AUDIT_ACTORS = {"IA1", "IA2", "IA3", "IA4", "HUMAIN", "OUTIL"}
DECISION_FIELDS = ["id", "decision", "scope", "state", "tests", "validation_commit",
                   "known_limitations", "locked_by", "locked_at"]

failures = []
checks = []


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def text(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def report(name, ok, detail=""):
    checks.append((name, ok, detail))
    if not ok:
        failures.append("{}: {}".format(name, detail))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_counts(manifest):
    ok = (
        manifest["category_count"] == len(manifest["categories"])
        and manifest["prompt_count"] == manifest["category_count"] * len(STAGES)
        and manifest["operational_category_count_excluding_start"] == manifest["category_count"] - 1
    )
    report("1. comptes du manifeste", ok, "category_count/prompt_count incohérents")


def check_prompts(slugs):
    missing = []
    for slug in slugs:
        for stage in STAGES:
            if not (ROOT / "PROMPTS" / slug / stage).exists():
                missing.append("{}/{}".format(slug, stage))
    extra = sorted(
        str(p.relative_to(ROOT)) for p in (ROOT / "PROMPTS").glob("*/*")
        if p.parent.name not in slugs or p.name not in STAGES
    )
    report("2. prompts présents", not missing and not extra,
           "manquants={} inattendus={}".format(missing[:5], extra[:5]))


def check_graph(manifest, deps):
    graph = load("DEPENDENCY-GRAPH.json")
    nodes = set(graph["nodes"] if isinstance(graph["nodes"][0], str) else [n["id"] for n in graph["nodes"]])
    edges = {}
    for e in graph["edges"]:
        src = e.get("from") or e.get("source")
        dst = e.get("to") or e.get("target")
        edges.setdefault(dst, set()).add(src)
    same = nodes == set(deps) and all(edges.get(s, set()) == set(deps[s]) for s in deps)
    report("3a. graphe == manifeste", same, "arêtes ou nœuds divergents")

    color = {}

    def visit(node):
        color[node] = 1
        for parent in deps.get(node, []):
            if color.get(parent) == 1:
                return True
            if color.get(parent, 0) == 0 and visit(parent):
                return True
        color[node] = 2
        return False

    cycle = any(visit(s) for s in deps if color.get(s, 0) == 0)
    report("3b. absence de cycle", not cycle and graph["cycles"] == [], "cycle détecté")


def check_matrix(manifest, deps):
    rows = re.findall(r"^\| *(\d+) \| `([^`]+)` \| ([^|]*)\| ([^|]*)\| ([^|]*)\|", text("EXECUTION-MATRIX.md"), re.M)
    seen = {}
    for prio, slug, dep_col, gate, profiles in rows:
        seen[slug] = {
            "execution_priority": int(prio),
            "depends_on": sorted(x.strip().strip("`") for x in dep_col.split(",") if x.strip() not in ("", "—")),
            "gate": gate.strip(),
            "project_profiles": [x.strip() for x in profiles.split(",") if x.strip()],
        }
    problems = []
    for c in manifest["categories"]:
        row = seen.get(c["slug"])
        if not row:
            problems.append(c["slug"])
            continue
        if (row["execution_priority"] != c["execution_priority"]
                or row["depends_on"] != sorted(c["depends_on"])
                or row["gate"] != c["gate"]
                or row["project_profiles"] != c["project_profiles"]):
            problems.append(c["slug"])
    report("4. EXECUTION-MATRIX == manifeste", not problems, "divergences: {}".format(problems[:5]))


def check_reading_order(manifest):
    rows = re.findall(r"^\d+\. `([^`]+)` — (.+)$", text("READING-ORDER.md"), re.M)
    by_slug = {c["slug"]: c for c in manifest["categories"]}
    problems = []
    for index, (slug, title) in enumerate(rows):
        c = by_slug.get(slug)
        if not c or c["reading_order"] != index or c["title"] != title.strip():
            problems.append(slug)
    if len(rows) != len(by_slug):
        problems.append("nombre de lignes")
    report("5. READING-ORDER == manifeste", not problems, "divergences: {}".format(problems[:5]))


def check_states(manifest, deps):
    problems = []
    for c in manifest["categories"]:
        slug = c["slug"]
        path = ROOT / ".md-ai-system" / "state" / "{}.json".format(slug)
        if not path.exists():
            problems.append("{}: état absent".format(slug))
            continue
        s = json.loads(path.read_text(encoding="utf-8"))
        cycle = s.get("current_cycle") or {}
        if s.get("category") != slug:
            problems.append("{}: champ category".format(slug))
        if sorted(s.get("dependencies", [])) != sorted(deps[slug]):
            problems.append("{}: dépendances".format(slug))
        if s.get("applicability") not in APPLICABILITIES:
            problems.append("{}: applicabilité '{}'".format(slug, s.get("applicability")))
        if s.get("status") not in CATEGORY_STATUSES:
            problems.append("{}: statut '{}' hors vocabulaire".format(slug, s.get("status")))
        if cycle.get("mode") not in MODES:
            problems.append("{}: mode '{}'".format(slug, cycle.get("mode")))
        if s.get("status") == "VALIDÉ" and not s.get("last_validation"):
            problems.append("{}: VALIDÉ sans last_validation".format(slug))
        if s.get("applicability") == "N/A" and s.get("status") is not None:
            problems.append("{}: N/A avec un statut".format(slug))
        if set(cycle.get("git") or {}) != {"head_at_start", "remote_sha_at_start", "checked_at"}:
            problems.append("{}: bloc current_cycle.git absent ou incomplet".format(slug))
    report("6. états par catégorie", not problems, "; ".join(problems[:5]))


def check_index(manifest):
    index = load(".md-ai-system/STATE.json")["categories"]
    problems = []
    for c in manifest["categories"]:
        slug = c["slug"]
        s = json.loads((ROOT / ".md-ai-system" / "state" / "{}.json".format(slug)).read_text(encoding="utf-8"))
        row = index.get(slug)
        if not row:
            problems.append(slug)
            continue
        if row.get("applicability") != s.get("applicability") or row.get("status") != s.get("status"):
            problems.append(slug)
    report("7. STATE.json == états par catégorie", not problems,
           "désynchronisé: {} (corriger avec TOOLS/state_index.py)".format(problems[:5]))


def check_snapshots():
    snap = load("SNAPSHOTS.json")["prompt_sha256"]
    bad = [rel for rel, digest in snap.items()
           if not (ROOT / rel).exists() or sha256(ROOT / rel) != digest]
    report("8. empreintes des prompts", not bad, "modifiés hors build: {}".format(bad[:5]))


def check_file_hashes(manifest):
    bad, absent, leaked = [], [], []
    for rel, digest in manifest.get("file_hashes", {}).items():
        if rel.startswith(RUNTIME_PREFIX):
            leaked.append(rel)
            continue
        path = ROOT / rel
        if not path.exists():
            absent.append(rel)
        elif sha256(path) != digest:
            bad.append(rel)
    missing_runtime = [rel for rel in manifest.get("runtime_files", []) if not (ROOT / rel).exists()]
    report("9. empreintes des fichiers système", not bad and not absent and not leaked and not missing_runtime,
           "modifiés={} absents={} runtime dans file_hashes={} runtime manquants={}".format(
               bad[:5], absent[:5], leaked[:3], missing_runtime[:3]))


def check_schema_versions(manifest):
    files = ["MANIFEST.json", "DEPENDENCY-GRAPH.json", "SNAPSHOTS.json",
             "TEMPLATES/CONFIG-TEMPLATE.json", ".md-ai-system/CONFIG.json",
             ".md-ai-system/STATE.json", ".md-ai-system/DECISIONS.json"]
    bad = [f for f in files if load(f).get("schema_version") != SCHEMA_VERSION]
    bad += ["state/{}.json".format(c["slug"]) for c in manifest["categories"]
            if json.loads((ROOT / ".md-ai-system" / "state" / "{}.json".format(c["slug"]))
                          .read_text(encoding="utf-8")).get("schema_version") != SCHEMA_VERSION]
    report("12. schema_version cohérents", not bad,
           "attendu {} — divergents: {}".format(SCHEMA_VERSION, bad[:5]))


def check_audit(slugs):
    path = ROOT / ".md-ai-system" / "AUDIT.jsonl"
    problems = []
    if path.exists():
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except ValueError:
                problems.append("ligne {}: JSON invalide".format(number))
                continue
            if sorted(record) != sorted(AUDIT_FIELDS):
                problems.append("ligne {}: champs {}".format(number, sorted(record)))
                continue
            if record["category"] not in slugs:
                problems.append("ligne {}: catégorie inconnue".format(number))
            if record["actor"] not in AUDIT_ACTORS:
                problems.append("ligne {}: actor '{}'".format(number, record["actor"]))
            if record["from_status"] not in CATEGORY_STATUSES or record["to_status"] not in CATEGORY_STATUSES:
                problems.append("ligne {}: statut hors vocabulaire".format(number))
            if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", record["ts"] or ""):
                problems.append("ligne {}: ts non UTC ISO".format(number))
            if not (record["summary"] or "").strip():
                problems.append("ligne {}: summary vide".format(number))
    report("13. journal d'audit", not problems, "; ".join(problems[:5]))


def check_decisions():
    data = load(".md-ai-system/DECISIONS.json")
    problems = []
    if data.get("decision_fields") != DECISION_FIELDS:
        problems.append("decision_fields non conforme")
    for entry in data.get("locked_decisions", []):
        label = entry.get("id", "<sans id>")
        if sorted(entry) != sorted(DECISION_FIELDS):
            problems.append("{}: champs incomplets".format(label))
            continue
        if entry["state"] not in ("VALIDÉ", "REFUSÉ", "BLOQUÉ", "EN_ATTENTE_DE_DÉCISION"):
            problems.append("{}: state '{}'".format(label, entry["state"]))
        if entry["locked_by"] not in ("IA4", "HUMAIN"):
            problems.append("{}: locked_by '{}'".format(label, entry["locked_by"]))
    ids = [e.get("id") for e in data.get("locked_decisions", [])]
    if len(ids) != len(set(ids)):
        problems.append("identifiants dupliqués")
    report("14. décisions verrouillées", not problems, "; ".join(problems[:5]))


def check_references():
    bad = []
    for path in sorted(ROOT.rglob("*.md")):
        rel_file = path.relative_to(ROOT)
        if str(rel_file).startswith(RUNTIME_PREFIX):
            continue
        for ref in set(re.findall(r"`([A-Za-z0-9_.\-/]+\.(?:md|json|py|jsonl))`", path.read_text(encoding="utf-8"))):
            if ref.startswith(REF_PREFIXES) and not (ROOT / ref).exists():
                bad.append("{} -> {}".format(rel_file, ref))
    report("10. références de chemins système", not bad, "; ".join(sorted(bad)[:5]))


def check_deployment():
    config = load(".md-ai-system/CONFIG.json")
    template = load("TEMPLATES/CONFIG-TEMPLATE.json")
    problems = []
    if set(template) - set(config):
        problems.append("blocs manquants: {}".format(sorted(set(template) - set(config))))
    dep = config.get("deployment") or {}
    if set(template.get("deployment", {})) - set(dep):
        problems.append("bloc deployment incomplet")
    if set(template.get("ai_roles", {})) - set(config.get("ai_roles") or {}):
        problems.append("bloc ai_roles incomplet")
    if dep.get("external_services_policy") not in ("deny", "allow_listed"):
        problems.append("external_services_policy invalide")
    if dep.get("external_services_policy") == "deny" and dep.get("allowed_external_services"):
        problems.append("dérogations déclarées alors que la politique est deny")
    if config.get("policy_profile") not in (None, "PRODUCTION", "STAGING", "POC"):
        problems.append("policy_profile invalide")
    report("11. CONFIG / contraintes de déploiement", not problems, "; ".join(problems))


def check_double_control(manifest):
    config = load(".md-ai-system/CONFIG.json")
    roles = config.get("ai_roles") or {}
    problems = []
    if roles.get("double_control") not in ("required", "degraded"):
        problems.append("ai_roles.double_control absent ou invalide")
    pairs = roles.get("independent_pairs") or []
    if roles.get("double_control") == "required" and not pairs:
        problems.append("aucune paire indépendante déclarée")
    for c in manifest["categories"]:
        state = json.loads((ROOT / ".md-ai-system" / "state" / "{}.json".format(c["slug"]))
                           .read_text(encoding="utf-8"))
        cycle = state.get("current_cycle") or {}
        for produced, controlled in pairs:
            a, b = cycle.get(produced) or {}, cycle.get(controlled) or {}
            if not b:
                continue
            if not a:
                problems.append("{}: {} enregistrée sans {}".format(c["slug"], controlled.upper(), produced.upper()))
            elif a.get("provider") and a.get("provider") == b.get("provider"):
                problems.append("{}: {} et {} par la même IA '{}'".format(
                    c["slug"], produced.upper(), controlled.upper(), a.get("provider")))
            elif roles.get("double_control") == "required" and not (a.get("provider") and b.get("provider")):
                problems.append("{}: fournisseur d'IA non enregistré".format(c["slug"]))
    report("15. double contrôle par deux IA", not problems, "; ".join(problems[:5]))


def main():
    manifest = load("MANIFEST.json")
    deps = {c["slug"]: c["depends_on"] for c in manifest["categories"]}
    slugs = set(deps)

    check_counts(manifest)
    check_prompts(slugs)
    check_graph(manifest, deps)
    check_matrix(manifest, deps)
    check_reading_order(manifest)
    check_states(manifest, deps)
    check_index(manifest)
    check_snapshots()
    check_file_hashes(manifest)
    check_references()
    check_deployment()
    check_schema_versions(manifest)
    check_audit(slugs)
    check_decisions()
    check_double_control(manifest)

    print("# VALIDATION SYSTÈME")
    print("")
    for name, ok, detail in checks:
        print("- {} : {}{}".format(name, "PASS" if ok else "FAIL", "" if ok else " — " + detail))
    print("")
    print("RESULTAT: {}".format("PASS" if not failures else "FAIL"))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
