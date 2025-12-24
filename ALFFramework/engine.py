import json
import os

# ---------------------------------------------------------
# PROBLEM BANK
# ---------------------------------------------------------
class ProblemBank:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.problems = self.load_all_problems()

    def load_all_problems(self):
        problems = {}
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".json"):
                path = os.path.join(self.folder_path, filename)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    topic = data.get("topic", filename.replace(".json", ""))
                    problems[topic] = data
        return problems

    def get_topics(self):
        return list(self.problems.keys())

    def get_problem(self, topic):
        return self.problems.get(topic)


# ---------------------------------------------------------
# ADAPTIVE LEARNER
# ---------------------------------------------------------
class AdaptiveLearner:
    def __init__(self, topic, problem_data):
        self.topic = topic
        self.problem_data = problem_data
        self.phase = "diagnosis"
        self.last_error = None


# ---------------------------------------------------------
# ADAPTIVE LEARNING FRAMEWORK
# ---------------------------------------------------------
class AdaptiveLearningFramework:
    def __init__(self):
        # IMPORTANT: This is what your UI expects
        self.problem_bank = ProblemBank("problems")

    def initialize_learner(self, topic):
        problem_data = self.problem_bank.get_problem(topic)
        return AdaptiveLearner(topic, problem_data)

    def process_answer(self, learner, user_answer):
        # Very simplified logic — your version may be more complex
        correct = learner.problem_data["correct_answer"]

        if learner.phase == "diagnosis":
            if user_answer.strip() == correct:
                learner.phase = "integration"
                return {
                    "message": "Correct!",
                    "integration_test": learner.problem_data.get("integration_test")
                }
            else:
                learner.last_error = "generic_error"
                return {"message": "Incorrect. Try again."}

        elif learner.phase == "integration":
            if user_answer.strip() == correct:
                return {"message": "Integration complete!"}
            else:
                return {"message": "Incorrect. Try again."}
