import json
import os

# ============================================================
# 1. PROBLEM BANK (laadt alle JSON-problemen)
# ============================================================

class ProblemBank:
    def __init__(self, folder="problems"):
        self.folder = folder
        self.problems = self._load_all()

    def _load_all(self):
        problems = {}
        if not os.path.exists(self.folder):
            print(f"[WARNING] Problem folder '{self.folder}' not found.")
            return problems

        for file in os.listdir(self.folder):
            if file.endswith(".json"):
                path = os.path.join(self.folder, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        problems[data["topic"]] = data
                except Exception as e:
                    print(f"[ERROR] Failed to load {file}: {e}")

        return problems

    def get(self, topic):
        return self.problems.get(topic)


# Maak één globale problem bank
problem_bank = ProblemBank()


# ============================================================
# 2. ADAPTIVE LEARNER (maakt gebruik van JSON-problemen)
# ============================================================

class AdaptiveLearner:
    def __init__(self, topic):
        self.topic = topic
        self.problem = problem_bank.get(topic)
        self.history = []

        if not self.problem:
            raise ValueError(f"Topic '{topic}' bestaat niet in problems/ folder.")

        print(f"--- Adaptive Learner Initialized for: {topic} ---")

    # --------------------------------------------------------
    # FASE 1: DIAGNOSE
    # --------------------------------------------------------
    def phase1_diagnose_isolate(self, student_input: str) -> dict:
        question = self.problem["question"]

        # Zoek naar foutpatronen
        for err in self.problem["common_errors"]:
            pattern = err["pattern"].lower()
            if pattern in student_input.lower():
                report = {
                    "error_type": err["pattern"],
                    "details": err["description"],
                    "drill_prompt": err["drill_prompt"]
                }
                self.history.append({"phase": 1, "report": report})
                return report

        # Geen match → generieke fout
        report = {
            "error_type": "unknown",
            "details": "Geen specifiek foutpatroon gevonden.",
            "drill_prompt": "Schrijf de formule opnieuw en leg elke stap uit."
        }
        self.history.append({"phase": 1, "report": report})
        return report

    # --------------------------------------------------------
    # FASE 2: HYPOTHESE & DRILL
    # --------------------------------------------------------
    def phase2_hypothesize_adapt(self, report: dict, student_hypothesis: str) -> dict:
        drill = {
            "prompt": report["drill_prompt"]
        }

        self.history.append({
            "phase": 2,
            "hypothesis": student_hypothesis,
            "drill": drill
        })

        return drill

    # --------------------------------------------------------
    # FASE 3: VALIDATIE & INTEGRATIE
    # --------------------------------------------------------
    def phase3_validate_integrate(self, drill_result: dict):
        if drill_result.get("is_correct"):
            final_test = self.problem["integration_test"]
            self.history.append({
                "phase": 3,
                "drill_result": drill_result,
                "final_test": final_test
            })
            return final_test

        # Fout → terug naar fase 2
        self.history.append({
            "phase": 3,
            "drill_result": drill_result,
            "final_test": None
        })
        return None
