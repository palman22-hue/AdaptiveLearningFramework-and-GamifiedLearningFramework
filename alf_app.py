import streamlit as st
import json
import os
from engine import AdaptiveLearningFramework   # <-- BELANGRIJK

# -----------------------------
# LANGUAGE SYSTEM
# -----------------------------

LANGUAGES = {
    "English": "en",
    "Nederlands": "nl"
}

TEXT = {
    "en": {
        "title": "Adaptive Learning Framework",
        "choose_topic": "Choose a topic:",
        "your_answer": "Your answer:",
        "submit": "Submit",
        "correct": "Correct!",
        "incorrect": "Incorrect.",
        "drill_question": "Drill question:",
        "integration_test": "Integration test:"
    },
    "nl": {
        "title": "Adaptief Leerframework",
        "choose_topic": "Kies een onderwerp:",
        "your_answer": "Jouw antwoord:",
        "submit": "Versturen",
        "correct": "Goed!",
        "incorrect": "Fout.",
        "drill_question": "Drill vraag:",
        "integration_test": "Integratietest:"
    }
}

# -----------------------------
# SESSION INIT
# -----------------------------

if "language" not in st.session_state:
    st.session_state.language = "English"

if "learner" not in st.session_state:
    st.session_state.learner = None

# -----------------------------
# LANGUAGE SELECTOR
# -----------------------------

st.session_state.language = st.sidebar.selectbox(
    "Language / Taal",
    list(LANGUAGES.keys())
)

lang = LANGUAGES[st.session_state.language]
T = TEXT[lang]

# -----------------------------
# LOAD TOPICS
# -----------------------------

problem_dir = "problems"
topics = [f.replace(".json", "") for f in os.listdir(problem_dir) if f.endswith(".json")]

st.title(T["title"])

# -----------------------------
# TOPIC SELECTOR
# -----------------------------

selected_topic = st.selectbox(T["choose_topic"], topics)

if selected_topic:
    json_path = os.path.join(problem_dir, selected_topic + ".json")
    with open(json_path, "r", encoding="utf-8") as f:
        problem_data = json.load(f)

    if (
        st.session_state.learner is None
        or st.session_state.learner.topic != problem_data["topic"]
    ):
        st.session_state.learner = AdaptiveLearningFramework.initialize_learner(problem_data)

# -----------------------------
# MAIN UI
# -----------------------------

user_answer = st.text_input(T["your_answer"])

if st.button(T["submit"]):
    result = AdaptiveLearningFramework.process_answer(
        st.session_state.learner,
        user_answer
    )

    if result["status"] == "correct":
        st.success(T["correct"])
    else:
        st.error(T["incorrect"])

    if "drill" in result:
        st.subheader(T["drill_question"])
        st.write(result["drill"])

    if "integration" in result:
        st.subheader(T["integration_test"])
        st.write(result["integration"])
