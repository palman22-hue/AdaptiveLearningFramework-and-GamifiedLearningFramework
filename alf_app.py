import streamlit as st
from ALFFramework.engine import AdaptiveLearningFramework, ProblemBank

# ---------------------------------------------------------
# 1. LANGUAGE SETUP (ALWAYS AVAILABLE)
# ---------------------------------------------------------
if "language" not in st.session_state:
    st.session_state["language"] = "English"

st.session_state["language"] = st.sidebar.selectbox(
    "Language",
    ["English", "Nederlands"],
    index=0
)

language = st.session_state["language"]

# ---------------------------------------------------------
# 2. EXPLANATION RENDERING
# ---------------------------------------------------------
def render_explanation(explanation_data, language):
    if not explanation_data:
        st.info("No explanation available." if language == "English" else "Geen uitleg beschikbaar.")
        return

    st.subheader("Explanation" if language == "English" else "Uitleg")

    for concept in explanation_data.get("concepts", []):
        symbol = concept.get("symbol", "")
        meaning = concept.get("meaning", "")

        st.markdown(f"**{symbol}**")
        st.write(meaning)
        st.markdown("---")

# ---------------------------------------------------------
# 3. LOAD ENGINE (engine loads its own ProblemBank)
# ---------------------------------------------------------
alf = AdaptiveLearningFramework()
problem_bank = alf.problem_bank

# ---------------------------------------------------------
# 4. TOPIC SELECTION
# ---------------------------------------------------------
topics = problem_bank.get_topics()

selected_topic = st.sidebar.selectbox(
    "Choose a topic" if language == "English" else "Kies een onderwerp",
    topics
)

# Initialize learner when topic changes
if "current_topic" not in st.session_state or st.session_state["current_topic"] != selected_topic:
    st.session_state["current_topic"] = selected_topic
    st.session_state["learner"] = alf.initialize_learner(selected_topic)

learner = st.session_state["learner"]
problem_data = learner.problem_data

# ---------------------------------------------------------
# 5. DISPLAY QUESTION
# ---------------------------------------------------------
st.title("Adaptive Learning Framework")

st.write(problem_data["question"])

# ---------------------------------------------------------
# 6. EXPLAIN BUTTON
# ---------------------------------------------------------
if st.button("Explain" if language == "English" else "Leg uit"):
    render_explanation(problem_data.get("explanation"), language)

# ---------------------------------------------------------
# 7. USER INPUT
# ---------------------------------------------------------
user_answer = st.text_input(
    "Your answer" if language == "English" else "Jouw antwoord"
)

if st.button("Submit"):
    result = alf.process_answer(learner, user_answer)

    st.write(result["message"])

    # If integration test is triggered
    if result.get("integration_test"):
        st.subheader("Integration Test" if language == "English" else "Integratietest")
        st.write(result["integration_test"]["prompt"])