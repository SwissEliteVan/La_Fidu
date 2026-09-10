# -*- coding: utf-8 -*-
from __future__ import print_function
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "MANIFEST.json"
STATE_DIR = ROOT / ".md-ai-system" / "state"
STAGES = ["1-IA1-ANALYSE.md", "2-IA2-VERIFICATION.md", "3-IA3-EXECUTION.md", "4-IA4-CONTROLE.md"]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def stage_index(name):
    if not name:
        return -1
    try:
        return STAGES.index(name)
    except ValueError:
        return -1


def deps_ready(state, states):
    for dep in state.get("dependencies", []):
        ds = states.get(dep)
        if not ds:
            return False
        if ds.get("applicability") == "N/A":
            continue
        if ds.get("applicability") != "ACTIVE":
            return False
        if ds.get("status") != "VALIDÉ":
            return False
    return True


def gate_ready(category, states):
    gate = category.get("gate", "normal")
    if gate == "normal":
        return True
    current = category["slug"]
    for slug, other in states.items():
        if slug == current:
            continue
        if gate == "all_active_except_source_and_final_validated" and slug in ("52-SOURCE-OF-TRUTH-LOCK", "53-FINAL-CLOSURE"):
            continue
        if other.get("applicability") == "TO_DEFINE":
            return False
        if other.get("applicability") == "ACTIVE" and other.get("status") != "VALIDÉ":
            return False
    return True


def next_stage_for(state):
    """Étape suivante pour une catégorie, ou None si elle n'est pas exécutable.

    Règles (WORKFLOW-RULES.md, GLOSSARY.md) :
      - VALIDÉ : rien, sauf delta pertinent explicitement autorisé par IA4 ;
      - BLOQUÉ / EN_ATTENTE_DE_DÉCISION : rien tant que l'obstacle subsiste ;
      - REFUSÉ : nouveau cycle depuis IA1, en mode CORRECTION, jamais IA3 ;
      - À_RÉÉVALUER : nouveau cycle depuis IA1 ;
      - sinon : étape suivante du cycle courant.
    """
    status = state.get("status")
    cycle = state.get("current_cycle") or {}
    if status == "VALIDÉ":
        delta = cycle.get("delta") or {}
        if not delta.get("relevant"):
            return None
        if not cycle.get("revalidation_authorized_by_ia4"):
            return None
        return STAGES[0]
    if status in ("EN_ATTENTE_DE_DÉCISION", "BLOQUÉ"):
        return None
    if status in ("À_RÉÉVALUER", "REFUSÉ"):
        return STAGES[0]
    last = cycle.get("last_completed_stage")
    idx = stage_index(last)
    if idx < 0:
        return STAGES[0]
    if idx + 1 < len(STAGES):
        return STAGES[idx + 1]
    return None


def no_candidate_reason(manifest, states):
    """Explique précisément pourquoi aucun prompt n'est exécutable."""
    to_define, pending, blocked, refused, active = [], [], [], [], []
    for c in manifest["categories"]:
        s = states.get(c["slug"]) or {}
        app = s.get("applicability")
        status = s.get("status")
        if app == "TO_DEFINE":
            to_define.append(c["slug"])
        elif app == "ACTIVE":
            active.append(c["slug"])
            if status == "EN_ATTENTE_DE_DÉCISION":
                pending.append(c["slug"])
            elif status == "BLOQUÉ":
                blocked.append(c["slug"])
            elif status == "REFUSÉ":
                refused.append(c["slug"])

    if not to_define and active and all(
        (states.get(slug) or {}).get("status") == "VALIDÉ" for slug in active
    ):
        return "Projet TERMINÉ : toutes les catégories ACTIVE sont VALIDÉES, aucune applicabilité TO_DEFINE, aucune décision en attente."
    parts = []
    if to_define:
        parts.append("applicabilité TO_DEFINE à décider ({})".format(summarize(to_define)))
    if pending:
        parts.append("décision humaine en attente ({})".format(summarize(pending)))
    if blocked:
        parts.append("blocage réel à lever ({})".format(summarize(blocked)))
    if refused:
        parts.append("refus à corriger ({})".format(summarize(refused)))
    if not parts:
        parts.append("aucune branche exécutable ; vérifier les dépendances et les gates")
    return "Aucun prompt exécutable : " + " ; ".join(parts) + "."


def summarize(slugs, limit=3):
    shown = ", ".join(slugs[:limit])
    return shown if len(slugs) <= limit else "{} et {} autres".format(shown, len(slugs) - limit)


def expected_ai(stage):
    """Fournisseur d'IA déclaré pour cette étape, ou None."""
    config_path = ROOT / ".md-ai-system" / "CONFIG.json"
    if not config_path.exists():
        return None
    roles = (load(config_path).get("ai_roles") or {}).get("declared_providers") or {}
    idx = stage_index(stage)
    return roles.get("ia{}".format(idx + 1)) if idx >= 0 else None


def resolve():
    """Retourne (chemin relatif du prompt ou None, raison)."""
    manifest = load(MANIFEST_PATH)
    states = {}
    for path in STATE_DIR.glob("*.json"):
        s = load(path)
        states[s["category"]] = s

    candidates = []
    for c in manifest["categories"]:
        s = states.get(c["slug"])
        if not s or s.get("applicability") != "ACTIVE":
            continue
        if not deps_ready(s, states):
            continue
        if not gate_ready(c, states):
            continue
        stage = next_stage_for(s)
        if stage:
            engaged = 0 if (s.get("current_cycle") or {}).get("last_completed_stage") else 1
            candidates.append((engaged, c["execution_priority"], c, stage))

    if not candidates:
        return None, no_candidate_reason(manifest, states)

    candidates.sort(key=lambda x: (x[0], x[1]))
    _, _, c, stage = candidates[0]
    rel = "PROMPTS/{}/{}".format(c["slug"], stage)
    if not (ROOT / rel).exists():
        raise SystemExit("Prompt introuvable: {}".format(ROOT / rel))
    return rel, "prochaine étape exécutable selon l'état courant, le DAG et la priorité d'exécution."


def main():
    rel, reason = resolve()
    if rel is None:
        print("NEXT_PROMPT_PATH: NONE")
        print("NEXT_PROMPT_TO_SEND: NONE")
        print("NEXT_PROMPT_REASON: {}".format(reason))
        print("NEXT_PROMPT_AI: SANS_OBJET")
        return
    provider = expected_ai(rel.rsplit("/", 1)[1])
    print("NEXT_PROMPT_PATH: {}".format(rel))
    print("NEXT_PROMPT_TO_SEND: Exécute le prompt `{}` en le lisant directement dans le workspace VS Code.".format(rel))
    print("NEXT_PROMPT_REASON: {}".format(reason))
    print("NEXT_PROMPT_AI: {}".format(provider or "NON_DÉCLARÉ"))


if __name__ == "__main__":
    main()
