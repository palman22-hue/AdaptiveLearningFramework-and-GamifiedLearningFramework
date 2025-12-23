import json
import os

# ============================================================
# 1. PROBLEM BANK
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


problem_bank = ProblemBank()


# ============================================================
# 2. ADAPTIVE LEARNER (STATE MACHINE)
# ============================================================

class AdaptiveLearner:
    def __init__(self, problem_data):
        self.topic = problem_data["topic"]
        self.problem = problem_data
        self.history = []
        self.phase = 1
        self.last_report = None

    # -----------------------------
    # PHASE 1 — DIAGNOSE
    # -----------------------------
    def diagnose(self, student_input):
        for err in self.problem["common_errors"]:
            if err["pattern"].lower() in student_input.lower():
                self.last_report = err
                self.phase = 2
                return {
                    "status": "incorrect",
                    "error_type": err["pattern"],
                    "details": err["description"],
                    "drill": err["drill_prompt"]
                }

        # Geen match
        self.last_report = {
            "pattern": "unknown",
            "description": "Geen specifiek foutpatroon gevonden.",
            "drill_prompt": "Schrijf de formule opnieuw en leg elke stap uit."
        }

        self.phase = 2
        return {
            "status": "incorrect",
            "error_type": "unknown",
            "details": "Geen specifiek foutpatroon gevonden.",
            "drill": self.last_report["drill_prompt"]
        }

    # -----------------------------
    # PHASE 2 — DRILL
    # -----------------------------
    def drill(self, student_input):
        # Voor nu: alles goed
        self.phase = 3
        return {"is_correct": True}

    # -----------------------------
    # PHASE 3 — INTEGRATION TEST
    # -----------------------------
    def integration(self):
        self.phase = 1
        return self.problem["integration_test"]


# ============================================================
# 3. ADAPTIVE LEARNING FRAMEWORK (ENGINE)
# ============================================================

class AdaptiveLearningFramework:

    @staticmethod
    def initialize_learner(problem_data):
        return AdaptiveLearner(problem_data)

    @staticmethod
    def process_answer(learner, student_input):
        """
        Stuurt automatisch door de fases:
        diagnose → drill → integratie
        """

        if learner.phase == 1:
            return learner.diagnose(student_input)

        elif learner.phase == 2:
            drill_result = learner.drill(student_input)
            if drill_result["is_correct"]:
                return {
                    "status": "correct",
                    "integration": learner.integration()
                }
            else:
                return {
                    "status": "incorrect",
                    "drill": learner.last_report["drill_prompt"]
                }

        elif learner.phase == 3:
            return {
                "status": "correct",
                "integration": learner.integration()
            }
