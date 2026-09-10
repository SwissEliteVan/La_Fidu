# -*- coding: utf-8 -*-
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "TOOLS"))
import next_prompt  # noqa: E402


class GeneratedSystemTests(unittest.TestCase):
    def test_manifest_counts(self):
        m = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(m["prompt_count"], m["category_count"] * 4)
        self.assertEqual(m["policy_profiles"], ["PRODUCTION", "STAGING", "POC"])

    def test_dag_has_no_cycle(self):
        g = json.loads((ROOT / "DEPENDENCY-GRAPH.json").read_text(encoding="utf-8"))
        self.assertEqual(g["cycles"], [])

    def test_next_prompt_support(self):
        self.assertTrue((ROOT / "TOOLS" / "next_prompt.py").exists())
        self.assertTrue((ROOT / "NEXT-PROMPT-RULES.md").exists())

    def test_git_confirmations(self):
        t = (ROOT / "TEMPLATES" / "GIT-INJECTION-TEMPLATE.md").read_text(encoding="utf-8")
        self.assertIn("git add -- <fichiers explicitement autorisés>", t)
        self.assertIn("Ne pas imposer `HEAD == origin/main` avant IA3", t)
        self.assertIn("Ne pas imposer `git fetch origin main` avant cette vérification initiale", t)


class RoutingTests(unittest.TestCase):
    """Règles de routage : WORKFLOW-RULES.md, GLOSSARY.md, NEXT-PROMPT-RULES.md."""

    @staticmethod
    def state(status=None, last_stage=None, **cycle):
        base = {"delta": {"relevant": False}, "last_completed_stage": last_stage,
                "revalidation_authorized_by_ia4": False}
        base.update(cycle)
        return {"status": status, "current_cycle": base}

    def test_refus_repart_de_ia1_quelle_que_soit_l_etape(self):
        for stage in next_prompt.STAGES:
            self.assertEqual(
                next_prompt.next_stage_for(self.state("REFUSÉ", stage)),
                "1-IA1-ANALYSE.md", stage)

    def test_bloque_ne_propose_aucune_etape(self):
        for stage in next_prompt.STAGES:
            self.assertIsNone(next_prompt.next_stage_for(self.state("BLOQUÉ", stage)), stage)

    def test_decision_en_attente_ne_propose_aucune_etape(self):
        self.assertIsNone(next_prompt.next_stage_for(
            self.state("EN_ATTENTE_DE_DÉCISION", "1-IA1-ANALYSE.md")))

    def test_cycle_normal_avance_d_une_etape(self):
        self.assertEqual(next_prompt.next_stage_for(self.state(None, None)), "1-IA1-ANALYSE.md")
        self.assertEqual(next_prompt.next_stage_for(self.state(None, "1-IA1-ANALYSE.md")),
                         "2-IA2-VERIFICATION.md")
        self.assertEqual(next_prompt.next_stage_for(self.state(None, "2-IA2-VERIFICATION.md")),
                         "3-IA3-EXECUTION.md")
        self.assertIsNone(next_prompt.next_stage_for(self.state(None, "4-IA4-CONTROLE.md")))

    def test_valide_ne_repart_que_sur_delta_autorise_par_ia4(self):
        self.assertIsNone(next_prompt.next_stage_for(self.state("VALIDÉ", "4-IA4-CONTROLE.md")))
        self.assertIsNone(next_prompt.next_stage_for(self.state(
            "VALIDÉ", "4-IA4-CONTROLE.md", delta={"relevant": True})))
        self.assertEqual(next_prompt.next_stage_for(self.state(
            "VALIDÉ", "4-IA4-CONTROLE.md", delta={"relevant": True},
            revalidation_authorized_by_ia4=True)), "1-IA1-ANALYSE.md")

    def test_gate_global_bloque_sur_applicabilite_non_decidee(self):
        category = {"slug": "53-FINAL-CLOSURE", "gate": "all_other_active_validated"}
        states = {"02-STACK": {"applicability": "TO_DEFINE", "status": None}}
        self.assertFalse(next_prompt.gate_ready(category, states))
        states = {"02-STACK": {"applicability": "ACTIVE", "status": "VALIDÉ"}}
        self.assertTrue(next_prompt.gate_ready(category, states))

    def test_dependance_na_satisfaite_to_define_non(self):
        state = {"dependencies": ["02-STACK"]}
        self.assertTrue(next_prompt.deps_ready(state, {"02-STACK": {"applicability": "N/A"}}))
        self.assertFalse(next_prompt.deps_ready(
            state, {"02-STACK": {"applicability": "TO_DEFINE", "status": None}}))


class StateSchemaTests(unittest.TestCase):
    SCHEMA = "2.2"

    def test_schema_version_et_bloc_git(self):
        manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
        for category in manifest["categories"]:
            path = ROOT / ".md-ai-system" / "state" / "{}.json".format(category["slug"])
            state = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(state["schema_version"], self.SCHEMA, category["slug"])
            self.assertEqual(sorted(state["current_cycle"]["git"]),
                             ["checked_at", "head_at_start", "remote_sha_at_start"])

    def test_empreintes_separees_du_runtime(self):
        manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
        self.assertTrue(manifest["runtime_files"])
        self.assertFalse([k for k in manifest["file_hashes"] if k.startswith(".md-ai-system/")])

    def test_politique_de_services_externes(self):
        config = json.loads((ROOT / ".md-ai-system" / "CONFIG.json").read_text(encoding="utf-8"))
        self.assertIn(config["deployment"]["external_services_policy"], ("deny", "allow_listed"))


class DoubleControlTests(unittest.TestCase):
    """AI-ROLES-RULES.md : IA2 != IA1, IA4 != IA3."""

    def setUp(self):
        import importlib
        self.mdai = importlib.import_module("mdai")

    @staticmethod
    def cycle(**providers):
        base = {"ia1": None, "ia2": None, "ia3": None, "ia4": None}
        for key, value in providers.items():
            base[key] = {"provider": value, "verdict": "ANALYSE", "ts": "", "summary": ""}
        return {"current_cycle": base}

    def config(self, **declared):
        return {"ai_roles": {"double_control": "required",
                             "independent_pairs": [["ia1", "ia2"], ["ia3", "ia4"]],
                             "declared_providers": declared or {}}}

    def test_meme_ia_pour_ia1_et_ia2_refuse(self):
        self.mdai.check_independence.forced = False
        with self.assertRaises(SystemExit):
            self.mdai.check_independence(self.config(), self.cycle(ia1="A"), 2, "A")

    def test_ia_differente_acceptee(self):
        self.mdai.check_independence.forced = False
        self.mdai.check_independence(self.config(), self.cycle(ia1="A"), 2, "B")

    def test_controle_sans_etape_produite_refuse(self):
        self.mdai.check_independence.forced = False
        with self.assertRaises(SystemExit):
            self.mdai.check_independence(self.config(), self.cycle(), 4, "B")

    def test_ia_non_declaree_refusee_sauf_force(self):
        config = self.config(ia2="B")
        self.mdai.check_independence.forced = False
        with self.assertRaises(SystemExit):
            self.mdai.check_independence(config, self.cycle(ia1="A"), 2, "C")
        self.mdai.check_independence.forced = True
        self.mdai.check_independence(config, self.cycle(ia1="A"), 2, "C")
        self.mdai.check_independence.forced = False

    def test_force_ne_contourne_jamais_l_independance(self):
        self.mdai.check_independence.forced = True
        with self.assertRaises(SystemExit):
            self.mdai.check_independence(self.config(), self.cycle(ia3="A"), 4, "A")
        self.mdai.check_independence.forced = False

    def test_config_projet_exige_le_double_controle(self):
        config = json.loads((ROOT / ".md-ai-system" / "CONFIG.json").read_text(encoding="utf-8"))
        self.assertEqual(config["ai_roles"]["double_control"], "required")
        self.assertIn(["ia1", "ia2"], config["ai_roles"]["independent_pairs"])
        self.assertIn(["ia3", "ia4"], config["ai_roles"]["independent_pairs"])


if __name__ == "__main__":
    unittest.main()
