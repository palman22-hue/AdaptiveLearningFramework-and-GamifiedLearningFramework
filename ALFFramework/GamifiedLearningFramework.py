if __name__ == "__main__":
    learner = AdaptiveLearner("Kinetic Energy Formula")

    while True:
        print("\n--- NEW CYCLE (type 'quit' to stop) ---")
        student_answer = input("Your answer to E_k = 1/2 * m * v^2: ")

        if student_answer.lower().strip() in {"quit", "exit"}:
            print("Exiting tutor. Goodbye.")
            break

        report = learner.phase1_diagnose_isolate(
            "E_k = 1/2 * m * v^2",
            student_answer
        )

        hypothesis = input("Why do you think this was wrong? ")
        drill = learner.phase2_hypothesize_adapt(report, hypothesis)
        print(f"\nDRILL:\n{drill['prompt']}")

        drill_input = input("\nDid you solve this drill correctly? (y/n): ")
        drill_result = {"is_correct": drill_input.lower().startswith("y")}
        final_test = learner.phase3_validate_integrate(drill_result)

        if final_test:
            print("\nFINAL TEST:")
            print(final_test["prompt"])
