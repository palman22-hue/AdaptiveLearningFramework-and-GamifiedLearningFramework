from AdaptiveLearner import AdaptiveLearner

learner = AdaptiveLearner("Kinetic Energy Formula")

question = "E_k = 1/2 * m * v^2"
student_input = input("Jouw antwoord: ")

report = learner.phase1_diagnose_isolate(question, student_input)

hyp = input("Waarom denk je dat dit fout was? ")
drill = learner.phase2_hypothesize_adapt(report, hyp)

print("\nDRILL:")
print(drill["prompt"])

correct = input("Heb je de drill goed opgelost? (y/n): ")
drill_result = {"is_correct": correct.lower().startswith("y")}

final_test = learner.phase3_validate_integrate(drill_result)

if final_test:
    print("\nFINAL TEST:")
    print(final_test["prompt"])