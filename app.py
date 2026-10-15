
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

st.set_page_config(
    page_title="AI Career Recommendation System",
    page_icon="🧭",
    layout="wide"
)

# IMPORTANT: Initialize state before checking the page
if "page" not in st.session_state:
    st.session_state["page"] = "welcome"

if "name" not in st.session_state:
    st.session_state["name"] = ""

if "profession" not in st.session_state:
    st.session_state["profession"] = "Student"

if "other_role" not in st.session_state:
    st.session_state["other_role"] = ""

if "results" not in st.session_state:
    st.session_state["results"] = None

if "skill_scores" not in st.session_state:
    st.session_state["skill_scores"] = None

# Your page conditions must come AFTER initialization
if st.session_state["page"] == "welcome":
    st.title("🧭 Career Compass")
    st.subheader("Discover Your Career Direction")
    st.write(
        "Explore career options based on your skills, strengths, "
        "and interests."
    )

    st.image(
        "https://images.unsplash.com/photo-1521737711867-e3b97375f902"
        "?auto=format&fit=crop&w=1200&q=85",
        use_container_width=True
    )

    if st.button("🚀 Get Started", type="primary"):
        st.session_state["page"] = "profile"
        st.rerun()

elif st.session_state["page"] == "profile":
    st.title("👤 Your Profile")

    with st.form("profile_form"):
        name = st.text_input("Enter your name")
        profession = st.selectbox(
            "Select your role",
            [
                "Student",
                "Working Professional",
                "Job Seeker",
                "Entrepreneur",
                "Other"
            ]
        )

        submitted = st.form_submit_button("Continue to Assessment")

        if submitted:
            if not name.strip():
                st.error("Please enter your name.")
            else:
                st.session_state["name"] = name.strip()
                st.session_state["profession"] = profession
                st.session_state["page"] = "assessment"
                st.rerun()

elif st.session_state["page"] == "assessment":
    st.title("🧠 Skill Assessment")
    st.write("Rate your current skills from 0 to 10.")

    with st.form("assessment_form"):
        python_score = st.slider("Python", 0, 10, 5)
        maths_score = st.slider("Mathematics", 0, 10, 5)
        communication_score = st.slider("Communication", 0, 10, 5)
        creativity_score = st.slider("Creativity", 0, 10, 5)
        business_score = st.slider("Business", 0, 10, 5)
        design_score = st.slider("Design", 0, 10, 5)
        problem_solving_score = st.slider("Problem Solving", 0, 10, 5)
        data_analysis_score = st.slider("Data Analysis", 0, 10, 5)

        submitted = st.form_submit_button("Generate Recommendations")

    if submitted:
        features = pd.DataFrame([{
            "Python": python_score,
            "Maths": maths_score,
            "Communication": communication_score,
            "Creativity": creativity_score,
            "Business": business_score,
            "Design": design_score,
            "ProblemSolving": problem_solving_score,
            "DataAnalysis": data_analysis_score
        }])

        try:
            model_path = Path(__file__).parent / "career_model.joblib"
            model = joblib.load(model_path)

            prediction = model.predict(features)[0]

            st.session_state["results"] = str(prediction)
            st.session_state["skill_scores"] = features.iloc[0].to_dict()
            st.session_state["page"] = "results"
            st.rerun()

        except Exception as error:
            st.error("Could not generate a prediction.")
            st.code(str(error))

elif st.session_state["page"] == "results":
    st.title("🎯 Your Career Recommendation")
    st.success(
        f"Hello, {st.session_state['name']}! "
        f"Your model's suggested career is: "
        f"{st.session_state['results']}"
    )

    st.write("Your skill ratings:")
    st.json(st.session_state["skill_scores"])

    if st.button("Retake Assessment"):
        st.session_state["page"] = "assessment"
        st.rerun()

    if st.button("Back to Home"):
        st.session_state["page"] = "welcome"
        st.rerun()
