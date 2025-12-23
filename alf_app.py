import streamlit as st
from ALFFramework import ProblemBank, AdaptiveLearner

bank = ProblemBank()
problem = bank.get("Kinetic Energy")
topics = list(bank.problems.keys())
selected_topic = st.selectbox("Kies een onderwerp:", topics)
problem = bank.get(selected_topic)


# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Adaptive Learning Framework",
    page_icon="🎓",
    layout="centered"
)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("""
<div style="text-align:center; padding: 10px 0;">
    <h1 style="margin-bottom:0;">🎓 Adaptive Learning Framework</h1>
    <p style="color:#666; font-size:18px; margin-top:5px;">
        Diagnose → Hypothese → Drill → Integratie
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# INITIALIZE LEARNER
# -------------------------------
if "learner" not in st.session_state:
    st.session_state.learner = AdaptiveLearner("Kinetic Energy")

learner = st.session_state.learner

# -------------------------------
# PHASE 1 — DIAGNOSE
# -------------------------------
st.markdown("## 🔍 Fase 1: Diagnose")

question = learner.problem["question"]


with st.container():
    st.markdown("""
    <div style="padding: 15px; border-radius: 10px; background-color: #f0f2f6;">
        <b>Vraag:</b> E<sub>k</sub> = 1/2 · m · v²  
        <br><br>
        Vul jouw antwoord hieronder in:
    </div>
    """, unsafe_allow_html=True)

student_input = st.text_input("Jouw antwoord:")

if st.button("Diagnose uitvoeren"):
    report = learner.phase1_diagnose_isolate(student_input)
    st.session_state.report = report

# -------------------------------
# SHOW DIAGNOSE RESULT
# -------------------------------
if "report" in st.session_state:
    report = st.session_state.report

    st.markdown("### 📋 Diagnose Resultaat")

    st.markdown(f"""
    <div style="padding: 15px; border-radius: 10px; background-color: #e8f4ff;">
        <p><b>Fouttype:</b> {report['error_type']}</p>
        <p><b>Details:</b> {report['details']}</p>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------
    # PHASE 2 — HYPOTHESIS & DRILL
    # -------------------------------
    st.markdown("## 🧩 Fase 2: Hypothese & Drill")

    hyp = st.text_input("Waarom denk je dat dit fout was?")

    if st.button("Genereer Drill"):
        drill = learner.phase2_hypothesize_adapt(report, hyp)
        st.session_state.drill = drill

# -------------------------------
# SHOW DRILL
# -------------------------------
if "drill" in st.session_state:
    drill = st.session_state.drill

    st.markdown("### 📝 Drill")

    st.markdown(f"""
    <div style="padding: 15px; border-radius: 10px; background-color: #fff7e6;">
        <p>{drill['prompt']}</p>
    </div>
    """, unsafe_allow_html=True)

    correct = st.checkbox("Ik heb de drill correct opgelost")

    if st.button("Valideer"):
        drill_result = {"is_correct": correct}
        final_test = learner.phase3_validate_integrate(drill_result)
        st.session_state.final_test = final_test

# -------------------------------
# PHASE 3 — FINAL TEST
# -------------------------------
if "final_test" in st.session_state and st.session_state.final_test:
    final_test = st.session_state.final_test

    st.markdown("## 🚀 Fase 3: Integratie Test")

    st.markdown(f"""
    <div style="padding: 15px; border-radius: 10px; background-color: #e9ffe8;">
        <p>{final_test['prompt']}</p>
    </div>
    """, unsafe_allow_html=True)
