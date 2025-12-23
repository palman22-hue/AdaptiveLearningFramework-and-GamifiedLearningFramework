class AdaptiveLearner:
    """
    Conceptuele klasse die de ALF-principes volgt:
    Fase 1: Diagnose
    Fase 2: Hypothese & Drill
    Fase 3: Validatie & Integratie
    """

    def __init__(self, topic: str):
        self.topic = topic
        self.history = []
        print(f"--- Adaptive Learner Initialized for: {topic} ---")

    # ---------- FASE 1: DIAGNOSE ----------

    def phase1_diagnose_isolate(self, question: str, student_input: str) -> dict:
        report = self._analyze_error(question, student_input)

        self.history.append({
            "phase": 1,
            "question": question,
            "student_input": student_input,
            "report": report,
        })

        print("\n[PHASE 1: DIAGNOSED]")
        print(f"Error Identified: {report['error_type']}")
        print(f"Details: {report['details']}")
        return report

    # ---------- FASE 2: HYPOTHESE & DRILL ----------

    def phase2_hypothesize_adapt(self, error_report: dict, student_hypothesis: str) -> dict:
        error_type = error_report.get("error_type", "Unknown")

        if "Operator" in error_type:
            explanation = "Error is due to confusing operations and ignoring exponents (order of operations)."
            drill_type = "operator"
        else:
            explanation = "Error seems conceptual; focus on the underlying formula."
            drill_type = "concept"

        print("\n[PHASE 2: EXPLAINED & ADAPTED]")
        print(f"Explanation: {explanation}")

        drill = self._create_drill(drill_type)

        self.history.append({
            "phase": 2,
            "student_hypothesis": student_hypothesis,
            "drill": drill,
        })

        return drill

    # ---------- FASE 3: VALIDATIE & INTEGRATIE ----------

    def phase3_validate_integrate(self, drill_result: dict):
        is_correct = drill_result.get("is_correct", False)

        if is_correct:
            print("\n[PHASE 3: VALIDATED]")
            print("Drill successful. Re-integrating skill with a complex problem...")
            final_test = self._create_final_test()
            self.history.append({
                "phase": 3,
                "drill_result": drill_result,
                "final_test": final_test,
            })
            return final_test

        print("\n[PHASE 3: FAILED VALIDATION]")
        print("Drill failed. Returning to Phase 2 for a new drill.")
        self.history.append({
            "phase": 3,
            "drill_result": drill_result,
            "final_test": None,
        })
        return None

    # ---------- INTERNE METHODEN ----------

    def _analyze_error(self, question: str, answer: str) -> dict:
        if "+" in answer and "x" not in answer and "squared" not in answer and "**2" not in answer:
            return {
                "error_type": "Incorrect Operator & Missing Exponent",
                "details": "Used '+' instead of '*' and failed to apply the square on velocity.",
                "correct_answer": "125 J",
            }
        return {
            "error_type": "Conceptual Confusion",
            "details": "Answer does not follow the expected structure for the formula.",
        }

    def _create_drill(self, drill_type: str) -> dict:
        if drill_type == "operator":
            return {
                "id": "drill_operator_1",
                "type": "order_of_operations",
                "prompt": "Compute 5 + 3 * 2 and (5 + 3) * 2. Explain why they differ.",
            }
        return {
            "id": "drill_concept_ke_formula_1",
            "type": "kinetic_energy_formula",
            "prompt": "Write the formula for kinetic energy and label each symbol.",
        }

    def _create_final_test(self) -> dict:
        return {
            "id": "final_ke_change_1",
            "type": "integration_problem",
            "prompt": (
                "A 5 kg object moves at 20 m/s and accelerates to 30 m/s.\n"
                "What is the change in kinetic energy?"
            ),
        }


# --------- VOORBEELD-GEBRUIK ---------

if __name__ == "__main__":
    learner = AdaptiveLearner("Kinetic Energy Formula")

    q_p1 = "E_k = 1/2 * m * v^2"
    a_p1 = "1 divided by 2 + 2,5kg multiplied by 10m/s"

    report = learner.phase1_diagnose_isolate(q_p1, a_p1)

    student_hyp = "I forgot order of operations and that velocity must be squared."
    drill = learner.phase2_hypothesize_adapt(report, student_hyp)
    print(f"\nGenerated Drill:\n{drill['prompt']}")

    drill_success = {"is_correct": True, "result": "125"}
    final_test = learner.phase3_validate_integrate(drill_success)

    if final_test:
        print("\nFinal Integration Test Generated:")
        print(final_test["prompt"])
