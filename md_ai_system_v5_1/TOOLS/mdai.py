# -*- coding: utf-8 -*-
"""Commande unique du système MD AI.

Automatise ce qui devait être fait à la main : mise à jour d'état, journal
d'audit, index, vue, calcul du prompt suivant, contrôle du double contrôle par
deux IA différentes.

Sous-commandes :
  init           configure profil de rigueur, hébergement et IA par étape
  check          prérequis + cohérence interne du système
  status         avancement lisible + prochaine étape
  next           prochain prompt et IA attendue
  git-snapshot   enregistre l'état Git de début de cycle
  finish-stage   enregistre le résultat d'une étape et enchaîne tout le reste
  set            applicabilité, statut, blocages, delta, revalidation
  promote        passe de POC à STAGING ou PRODUCTION, avec revalidation
  explain        explique l'état d'une catégorie en langage simple
  unblock        lève un blocage

Aucune commande n'invente de valeur : ce qui n'est pas fourni reste vide.
"""
from __future__ import print_function
import argparse
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECT = ROOT.parent
STATE_DIR = ROOT / ".md-ai-system" / "state"
CONFIG = ROOT / ".md-ai-system" / "CONFIG.json"
AUDIT = ROOT / ".md-ai-system" / "AUDIT.jsonl"
MANIFEST = ROOT / "MANIFEST.json"

sys.path.insert(0, str(ROOT / "TOOLS"))
import next_prompt  # noqa: E402
import state_index  # noqa: E402
import state_overview  # noqa: E402

STAGES = next_prompt.STAGES
STAGE_KEYS = ["ia1", "ia2", "ia3", "ia4"]
POLICIES = ["PRODUCTION", "STAGING", "POC"]
NEUTRAL = {"ANALYSE", "EXÉCUTÉ"}
CARRIED = {"BLOQUÉ", "EN_ATTENTE_DE_DÉCISION", "À_RÉÉVALUER", "EN_REVALIDATION"}
VERDICTS = {
    1: ["ANALYSE", "BLOQUÉ", "EN_ATTENTE_DE_DÉCISION", "À_RÉÉVALUER", "EN_REVALIDATION"],
    2: ["VALIDÉ", "REFUSÉ", "BLOQUÉ", "EN_ATTENTE_DE_DÉCISION", "À_RÉÉVALUER", "EN_REVALIDATION"],
    3: ["EXÉCUTÉ", "BLOQUÉ", "EN_ATTENTE_DE_DÉCISION", "À_RÉÉVALUER", "EN_REVALIDATION"],
    4: ["VALIDÉ", "REFUSÉ", "BLOQUÉ", "EN_ATTENTE_DE_DÉCISION", "À_RÉÉVALUER", "EN_REVALIDATION"],
}


def now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def dump(path, data):
    Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def state_path(category):
    path = STATE_DIR / "{}.json".format(category)
    if not path.exists():
        raise SystemExit("Catégorie inconnue : {}".format(category))
    return path


def fail(message):
    raise SystemExit("STOP — {}".format(message))


def audit(category, stage, mode, actor, provider, from_status, to_status, commit, summary):
    record = {
        "ts": now(), "category": category, "stage": stage, "mode": mode, "actor": actor,
        "provider": provider, "from_status": from_status, "to_status": to_status,
        "commit": commit, "summary": summary,
    }
    with AUDIT.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def refresh():
    """Régénère l'index et la vue humaine, sans bruit sur la sortie."""
    dump(state_index.OUT, state_index.build())
    stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")
    try:
        state_overview.main()
    finally:
        sys.stdout.close()
        sys.stdout = stdout


def show_next():
    rel, reason = next_prompt.resolve()
    if rel is None:
        print("NEXT_PROMPT_PATH: NONE")
        print("NEXT_PROMPT_TO_SEND: NONE")
        print("NEXT_PROMPT_REASON: {}".format(reason))
        print("NEXT_PROMPT_AI: SANS_OBJET")
        return
    provider = next_prompt.expected_ai(rel.rsplit("/", 1)[1])
    print("NEXT_PROMPT_PATH: {}".format(rel))
    print("NEXT_PROMPT_TO_SEND: Exécute le prompt `{}` en le lisant directement dans le workspace VS Code.".format(rel))
    print("NEXT_PROMPT_REASON: {}".format(reason))
    print("NEXT_PROMPT_AI: {}".format(provider or "NON_DÉCLARÉ"))


# ----------------------------------------------------------------- init


def cmd_init(args):
    config = load(CONFIG)
    if args.policy:
        config["policy_profile"] = args.policy
    if args.hosting:
        config.setdefault("deployment", {})["hosting_target"] = args.hosting
    if args.hosting_plan:
        config.setdefault("deployment", {})["hosting_plan"] = args.hosting_plan
    if args.external_services:
        config.setdefault("deployment", {})["external_services_policy"] = args.external_services
    roles = config.setdefault("ai_roles", {})
    declared = roles.setdefault("declared_providers", {k: None for k in STAGE_KEYS})
    for key, value in zip(STAGE_KEYS, [args.ia1, args.ia2, args.ia3, args.ia4]):
        if value:
            declared[key] = value
    dump(CONFIG, config)

    missing = []
    if not config.get("policy_profile"):
        missing.append("policy_profile (PRODUCTION, STAGING ou POC)")
    if not (config.get("deployment") or {}).get("hosting_target"):
        missing.append("deployment.hosting_target")
    if roles.get("double_control") == "required":
        for pair in roles.get("independent_pairs", []):
            a, b = declared.get(pair[0]), declared.get(pair[1])
            if not a or not b:
                missing.append("ai_roles.declared_providers.{} et .{}".format(*pair))
            elif a == b:
                fail("{} et {} doivent être deux IA différentes (double contrôle).".format(*pair))
    print("Configuration écrite dans {}".format(CONFIG))
    if missing:
        print("À COMPLÉTER : " + " ; ".join(missing))
    else:
        print("Configuration complète.")
    return 0


# ---------------------------------------------------------------- check


def git(*args, **kwargs):
    cwd = kwargs.pop("cwd", PROJECT)
    try:
        out = subprocess.run(["git"] + list(args), cwd=str(cwd),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        return None
    return out.stdout.decode("utf-8", "replace").strip() if out.returncode == 0 else None


def cmd_check(args):
    print("# PRÉREQUIS")
    print("- Python : {}.{}.{}".format(*sys.version_info[:3]))
    version = git("--version")
    print("- Git : {}".format(version or "ABSENT"))
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    print("- Branche courante : {}".format(branch or "—"))
    dirty = git("status", "--porcelain")
    print("- Working tree : {}".format("propre" if dirty == "" else "MODIFICATIONS EN COURS"))
    config = load(CONFIG)
    roles = config.get("ai_roles") or {}
    print("- POLICY_PROFILE : {}".format(config.get("policy_profile") or "NON CONFIGURÉ"))
    print("- Hébergement : {}".format((config.get("deployment") or {}).get("hosting_target") or "NON CONFIGURÉ"))
    print("- IA déclarées : {}".format(roles.get("declared_providers") or "aucune"))
    print("")
    return subprocess.call([sys.executable, str(ROOT / "TOOLS" / "validate_system.py")])


# --------------------------------------------------------------- status


def cmd_status(args):
    manifest = load(MANIFEST)
    counts = {}
    blocked, pending, refused = [], [], []
    for c in manifest["categories"]:
        s = load(state_path(c["slug"]))
        app = s.get("applicability")
        key = app if app != "ACTIVE" else (s.get("status") or "À FAIRE")
        counts[key] = counts.get(key, 0) + 1
        if app == "ACTIVE":
            if s.get("status") == "BLOQUÉ":
                blocked.append(c["slug"])
            elif s.get("status") == "EN_ATTENTE_DE_DÉCISION":
                pending.append(c["slug"])
            elif s.get("status") == "REFUSÉ":
                refused.append(c["slug"])
    print("# AVANCEMENT")
    for key in sorted(counts):
        print("- {} : {}".format(key, counts[key]))
    for label, items in [("Bloquées", blocked), ("En attente de décision", pending),
                         ("Refusées", refused)]:
        if items:
            print("- {} : {}".format(label, ", ".join(items)))
    print("")
    show_next()
    return 0


def cmd_next(args):
    show_next()
    return 0


# --------------------------------------------------------- git-snapshot


def cmd_git_snapshot(args):
    path = state_path(args.category)
    state = load(path)
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    dirty = git("status", "--porcelain")
    head = git("rev-parse", "HEAD")
    remote = git("ls-remote", "origin", "refs/heads/main")
    if branch is None or head is None:
        fail("dépôt Git illisible depuis {}".format(PROJECT))
    if branch != "main" and not args.allow_any_branch:
        fail("branche courante '{}' : le système travaille uniquement sur main.".format(branch))
    if dirty:
        fail("working tree non propre : modification humaine ou travail en cours détecté.")
    if "\n" in (remote or "") or not remote:
        remote_sha = None
    else:
        remote_sha = remote.split()[0]
    state["current_cycle"]["git"] = {
        "checked_at": now(), "head_at_start": head, "remote_sha_at_start": remote_sha}
    dump(path, state)
    print("GIT_HEAD: {}".format(head))
    print("GIT_REMOTE_MAIN: {}".format(remote_sha or "INCONNU"))
    print("GIT_BRANCH: {}".format(branch))
    print("Enregistré dans {}".format(path.name))
    return 0


# --------------------------------------------------------- finish-stage


def check_independence(config, state, stage_number, provider):
    roles = config.get("ai_roles") or {}
    if roles.get("double_control") != "required":
        return
    key = STAGE_KEYS[stage_number - 1]
    declared = roles.get("declared_providers") or {}
    if declared.get(key) and declared[key] != provider and not getattr(check_independence, "forced", False):
        fail("étape {} attendue depuis '{}', reçue depuis '{}'.".format(
            key.upper(), declared[key], provider))
    for pair in roles.get("independent_pairs", []):
        if key != pair[1]:
            continue
        other = (state["current_cycle"].get(pair[0]) or {}).get("provider")
        if other is None:
            fail("{} n'a pas été enregistrée : impossible de contrôler l'indépendance du double contrôle.".format(pair[0].upper()))
        if other == provider:
            fail("double contrôle invalide : {} et {} ont été faites par la même IA ('{}').".format(
                pair[0].upper(), pair[1].upper(), provider))


def cmd_finish_stage(args):
    path = state_path(args.category)
    state = load(path)
    config = load(CONFIG)
    stage_number = args.stage
    stage_name = STAGES[stage_number - 1]
    verdict = args.verdict
    if verdict not in VERDICTS[stage_number]:
        fail("verdict '{}' non autorisé pour IA{} ({}).".format(
            verdict, stage_number, ", ".join(VERDICTS[stage_number])))
    if state.get("applicability") != "ACTIVE":
        fail("catégorie {} : applicabilité '{}' — seules les catégories ACTIVE exécutent IA1→IA4.".format(
            args.category, state.get("applicability")))

    cycle = state["current_cycle"]
    previous_status = state.get("status")

    if stage_number == 1:
        mode = args.mode or (
            "CORRECTION" if previous_status == "REFUSÉ"
            else "REVALIDATION" if state.get("last_validation") else "NEW_WORK")
        cycle["mode"] = mode
        for key in STAGE_KEYS:
            cycle[key] = None
        cycle["last_completed_stage"] = None
        cycle["git"] = {"checked_at": None, "head_at_start": None, "remote_sha_at_start": None}
        if previous_status in ("REFUSÉ", "À_RÉÉVALUER", "BLOQUÉ"):
            state["status"] = None
    check_independence.forced = args.force
    check_independence(config, state, stage_number, args.ai)

    cycle[STAGE_KEYS[stage_number - 1]] = {
        "provider": args.ai, "verdict": verdict, "ts": now(),
        "summary": args.summary.strip(),
    }
    cycle["last_completed_stage"] = stage_name

    if verdict in CARRIED:
        state["status"] = verdict
    elif verdict == "REFUSÉ":
        state["status"] = "REFUSÉ"
        cycle["mode"] = "CORRECTION"
    elif verdict == "VALIDÉ" and stage_number == 4:
        if not args.commit and (config.get("policy_profile") != "POC"):
            fail("IA4 VALIDÉ exige --commit (commit de validation) hors profil POC.")
        state["status"] = "VALIDÉ"
        state["validation_commit"] = args.commit
        state["last_validation"] = {"commit": args.commit, "ts": now(),
                                    "summary": args.summary.strip()}
        cycle["delta"] = {"from_commit": args.commit, "relevant": False, "summary": "",
                          "to_commit": None}
        cycle["revalidation_authorized_by_ia4"] = False
    elif verdict in NEUTRAL or (verdict == "VALIDÉ" and stage_number == 2):
        if state.get("status") in ("REFUSÉ", "BLOQUÉ"):
            state["status"] = None

    if args.blocker:
        state["open_blockers"] = sorted(set(state.get("open_blockers") or []) | {args.blocker})
    elif verdict not in ("BLOQUÉ", "EN_ATTENTE_DE_DÉCISION"):
        state["open_blockers"] = []

    dump(path, state)
    audit(args.category, stage_name, cycle["mode"], "IA{}".format(stage_number), args.ai,
          previous_status, state.get("status"), args.commit, args.summary.strip())
    refresh()
    print("Étape IA{} enregistrée pour {} — verdict {} (IA : {}).".format(
        stage_number, args.category, verdict, args.ai))
    print("STATUT_CATÉGORIE: {}".format(state.get("status") or "—"))
    print("")
    show_next()
    return 0


# ------------------------------------------------------------------ set


def cmd_set(args):
    path = state_path(args.category)
    state = load(path)
    previous = state.get("status")
    changed = []
    if args.applicability:
        if args.applicability != "N/A" and not args.reason and not state.get("activation_reason"):
            fail("--reason est obligatoire pour justifier une applicabilité.")
        if args.applicability == "N/A":
            state["status"] = None
        state["applicability"] = args.applicability
        state["applicability_scope"] = (
            load(CONFIG).get("policy_profile") if args.policy_scoped else None)
        if args.reason:
            state["activation_reason"] = args.reason
        changed.append("applicabilité={}{}".format(
            args.applicability, " (liée au profil courant)" if args.policy_scoped else ""))
    if args.status:
        state["status"] = None if args.status == "null" else args.status
        changed.append("statut={}".format(args.status))
    if args.add_blocker:
        state["open_blockers"] = sorted(set(state.get("open_blockers") or []) | {args.add_blocker})
        changed.append("blocage ajouté")
    if args.clear_blockers:
        state["open_blockers"] = []
        changed.append("blocages effacés")
    if args.delta_summary:
        state["current_cycle"]["delta"] = {
            "from_commit": (state.get("last_validation") or {}).get("commit"),
            "to_commit": args.delta_to_commit, "relevant": True,
            "summary": args.delta_summary}
        changed.append("delta pertinent enregistré")
    if args.authorize_revalidation:
        if not (state["current_cycle"].get("delta") or {}).get("relevant"):
            fail("aucun delta pertinent enregistré : rien à revalider.")
        state["current_cycle"]["revalidation_authorized_by_ia4"] = True
        changed.append("revalidation autorisée par IA4")
    if not changed:
        fail("aucune modification demandée.")
    dump(path, state)
    audit(args.category, "—", state["current_cycle"].get("mode") or "NEW_WORK",
          args.actor, None, previous, state.get("status"), None,
          args.reason or "; ".join(changed))
    refresh()
    print("{} : {}".format(args.category, " ; ".join(changed)))
    print("")
    show_next()
    return 0


def cmd_unblock(args):
    path = state_path(args.category)
    state = load(path)
    if state.get("status") not in ("BLOQUÉ", "EN_ATTENTE_DE_DÉCISION"):
        fail("{} n'est ni BLOQUÉ ni EN_ATTENTE_DE_DÉCISION.".format(args.category))
    previous = state["status"]
    state["status"] = "À_RÉÉVALUER" if state.get("last_validation") else None
    state["open_blockers"] = []
    dump(path, state)
    audit(args.category, "—", state["current_cycle"].get("mode") or "NEW_WORK", args.actor,
          None, previous, state.get("status"), None, args.reason)
    refresh()
    print("{} : blocage levé ({} → {}).".format(args.category, previous, state.get("status") or "null"))
    print("")
    show_next()
    return 0


# -------------------------------------------------------------- promote


def cmd_promote(args):
    config = load(CONFIG)
    current = config.get("policy_profile")
    if current == args.to:
        fail("le projet est déjà en {}.".format(args.to))
    if current is None:
        fail("aucun POLICY_PROFILE configuré : rien à promouvoir.")
    manifest = load(MANIFEST)
    reopened, revalidate = [], []
    for c in manifest["categories"]:
        path = state_path(c["slug"])
        state = load(path)
        touched = False
        if state.get("applicability") == "N/A" and state.get("applicability_scope") == current:
            state["applicability"] = "TO_DEFINE"
            state["applicability_scope"] = None
            state["activation_reason"] = "à redécider après promotion {} → {}".format(current, args.to)
            reopened.append(c["slug"])
            touched = True
        if state.get("status") == "VALIDÉ":
            state["status"] = "À_RÉÉVALUER"
            state["current_cycle"]["mode"] = "REVALIDATION"
            state["current_cycle"]["delta"] = {
                "from_commit": (state.get("last_validation") or {}).get("commit"),
                "to_commit": None, "relevant": True,
                "summary": "promotion {} → {} : contrôles du nouveau profil à appliquer".format(current, args.to)}
            state["current_cycle"]["revalidation_authorized_by_ia4"] = True
            revalidate.append(c["slug"])
            touched = True
        if touched:
            dump(path, state)
            audit(c["slug"], "—", state["current_cycle"].get("mode") or "REVALIDATION", "OUTIL",
                  None, "VALIDÉ" if c["slug"] in revalidate else None, state.get("status"), None,
                  "promotion {} → {}".format(current, args.to))
    config["policy_profile"] = args.to
    dump(CONFIG, config)
    refresh()
    print("POLICY_PROFILE : {} → {}".format(current, args.to))
    print("Catégories à redécider : {}".format(", ".join(reopened) or "aucune"))
    print("Catégories à revalider : {}".format(", ".join(revalidate) or "aucune"))
    print("La dernière validation de chaque catégorie est conservée.")
    print("")
    show_next()
    return 0


# -------------------------------------------------------------- explain


def cmd_explain(args):
    state = load(state_path(args.category))
    cycle = state.get("current_cycle") or {}
    app = state.get("applicability")
    status = state.get("status")
    print("# {}".format(args.category))
    print("")
    if app == "N/A":
        print("Cette catégorie ne concerne pas ton projet. Motif : {}".format(
            state.get("activation_reason") or "non documenté"))
        return 0
    if app == "TO_DEFINE":
        print("On n'a pas encore décidé si cette catégorie s'applique à ton projet.")
        print("Rien ne peut être clôturé tant qu'il en reste. C'est la catégorie")
        print("01-PROJECT-PROFILE-APPLICABILITY qui tranche.")
        return 0
    explanations = {
        None: "Le travail n'a pas encore commencé, ou un cycle est en cours.",
        "VALIDÉ": "Contrôlée et validée par IA4. Elle ne repartira que si un changement pertinent est enregistré et autorisé.",
        "REFUSÉ": "IA2 ou IA4 a refusé : un écart réel subsiste ou une preuve manque. Le cycle repart de l'analyse (IA1), en correction.",
        "BLOQUÉ": "Un obstacle réel empêche d'avancer. Aucune étape n'est proposée ici ; les autres branches continuent. Il faut lever le blocage : mdai unblock.",
        "EN_ATTENTE_DE_DÉCISION": "Le système attend une décision de ta part. Les autres branches continuent.",
        "À_RÉÉVALUER": "Elle était validée, un changement impose un nouveau contrôle. La validation précédente est conservée.",
        "EN_REVALIDATION": "Le nouveau contrôle est en cours.",
    }
    print(explanations.get(status, "Statut : {}".format(status)))
    print("")
    print("- Dernière étape terminée : {}".format(cycle.get("last_completed_stage") or "aucune"))
    print("- Mode de travail : {}".format(cycle.get("mode") or "—"))
    for key in STAGE_KEYS:
        entry = cycle.get(key)
        if entry:
            print("- {} : {} par {} — {}".format(key.upper(), entry.get("verdict"),
                                                 entry.get("provider"), entry.get("summary") or ""))
    if state.get("open_blockers"):
        print("- Blocages ouverts : {}".format("; ".join(state["open_blockers"])))
    if state.get("last_validation"):
        print("- Dernière validation : commit {}".format(state["last_validation"].get("commit")))
    if state.get("dependencies"):
        print("- Dépend de : {}".format(", ".join(state["dependencies"])))
    print("")
    show_next()
    return 0


# ----------------------------------------------------------------- main


def build_parser():
    parser = argparse.ArgumentParser(prog="mdai", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("init", help="configure le projet")
    p.add_argument("--policy", choices=POLICIES)
    p.add_argument("--hosting")
    p.add_argument("--hosting-plan")
    p.add_argument("--external-services", choices=["deny", "allow_listed"])
    for key in STAGE_KEYS:
        p.add_argument("--{}".format(key), help="IA chargée de {}".format(key.upper()))
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("check", help="prérequis + cohérence du système")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("status", help="avancement + prochaine étape")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("next", help="prochain prompt et IA attendue")
    p.set_defaults(func=cmd_next)

    p = sub.add_parser("git-snapshot", help="enregistre l'état Git de début de cycle")
    p.add_argument("--category", required=True)
    p.add_argument("--allow-any-branch", action="store_true")
    p.set_defaults(func=cmd_git_snapshot)

    p = sub.add_parser("finish-stage", help="enregistre une étape et enchaîne le reste")
    p.add_argument("--category", required=True)
    p.add_argument("--stage", required=True, type=int, choices=[1, 2, 3, 4])
    p.add_argument("--ai", required=True, help="IA ayant réalisé l'étape")
    p.add_argument("--verdict", required=True)
    p.add_argument("--summary", required=True)
    p.add_argument("--commit")
    p.add_argument("--mode", choices=["NEW_WORK", "REVALIDATION", "CORRECTION"])
    p.add_argument("--blocker")
    p.add_argument("--force", action="store_true",
                   help="passe outre l'IA déclarée, jamais l'indépendance du double contrôle")
    p.set_defaults(func=cmd_finish_stage)

    p = sub.add_parser("set", help="applicabilité, statut, blocages, delta")
    p.add_argument("--category", required=True)
    p.add_argument("--applicability", choices=["ACTIVE", "N/A", "TO_DEFINE"])
    p.add_argument("--status", choices=["null", "VALIDÉ", "REFUSÉ", "BLOQUÉ",
                                        "EN_ATTENTE_DE_DÉCISION", "À_RÉÉVALUER", "EN_REVALIDATION"])
    p.add_argument("--reason")
    p.add_argument("--add-blocker")
    p.add_argument("--clear-blockers", action="store_true")
    p.add_argument("--policy-scoped", action="store_true",
                   help="l'applicabilité ne vaut que pour le profil de rigueur courant")
    p.add_argument("--delta-summary")
    p.add_argument("--delta-to-commit")
    p.add_argument("--authorize-revalidation", action="store_true")
    p.add_argument("--actor", default="IA1", choices=["IA1", "IA2", "IA3", "IA4", "HUMAIN", "OUTIL"])
    p.set_defaults(func=cmd_set)

    p = sub.add_parser("promote", help="passe le projet d'un profil de rigueur au suivant")
    p.add_argument("--to", required=True, choices=POLICIES)
    p.set_defaults(func=cmd_promote)

    p = sub.add_parser("explain", help="explique en langage simple l'état d'une catégorie")
    p.add_argument("--category", required=True)
    p.set_defaults(func=cmd_explain)

    p = sub.add_parser("unblock", help="lève un blocage")
    p.add_argument("--category", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--actor", default="HUMAIN", choices=["IA1", "IA2", "IA3", "IA4", "HUMAIN", "OUTIL"])
    p.set_defaults(func=cmd_unblock)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        os._exit(0)
