# 💡 AdaptiveLearner – ALF-Inspired Mini Tutor

![alt text](image.png)

## 🎯 Project Overzicht

De `AdaptiveLearner` is een **conceptuele Python-klasse** die de logica van een adaptief leerframework implementeert. Het hoofddoel is om de inefficiëntie van traditioneel leren aan te pakken door elke studentfout direct om te zetten in een gerichte, leerzame oefening.

De kern van de `AdaptiveLearner` is de gestructureerde, **drie-fasen leerlus** (geïnspireerd door het Adaptive Learning and Feedback (ALF) Framework):

1.  **Phase 1:** Diagnose & Isolate (Foutisolatie)
2.  **Phase 2:** Hypothesize & Adapt (Drill-generatie)
3.  **Phase 3:** Validate & Integrate (Kennisintegratie)

De huidige implementatie richt zich op de **kinetische energie formule** ($E_k = \frac{1}{2}mv^2$), maar het onderliggende patroon is algemeen en kan worden toegepast op elk technisch of conceptueel onderwerp.

🔗 Live Demo: Test het ALF/GEAR Framework direct in uw browser via de Google Colab Notebook: https://colab.research.google.com/drive/1NCitFl4TUaE5bap72ekAWHhjYzSRsR2N?usp=sharing

---

## ✨ Features

* **State Tracking:** Houdt een specifiek `topic` en een gedetailleerde `history` van alle interacties bij.
* **Precise Diagnosis (Phase 1):** Analyseert de studentinvoer en labelt het fouttype (bijvoorbeeld `Incorrect Operator & Missing Exponent` vs. `Conceptual Confusion`).
* **Targeted Drills (Phase 2):** Gebruikt het fouttype én de vrije-tekst `student_hypothesis` om een uiterst gerichte oefening te genereren.
* **Adaptive Progression (Phase 3):** Bepaalt op basis van het drill-resultaat of de leerling doorstroomt naar een complexe **Integratie-opgave** of terug moet voor een herhaalde drill.
* **CLI Functionality:** Bevat een eenvoudige `if __name__ == "__main__":` lus voor gebruik als een tekst-gebaseerde tutor via de commandoregel.

---

## 💻 Code Overzicht

### Class Initialisatie

```python
learner = AdaptiveLearner("Kinetic Energy Formula")