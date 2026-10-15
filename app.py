
import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="AI Career Recommendation", page_icon="🎓")

@st.cache_resource
def load_model():
    return joblib.load("career_model.joblib")

model = load_model()

st.title("AI Career Recommendation System")
st.write("Rate your skills from 1 to 5.")

with st.form("career_form"):
    python = st.slider("Python", 1, 5, 3)
    maths = st.slider("Maths", 1, 5, 3)
    communication = st.slider("Communication", 1, 5, 3)
    creativity = st.slider("Creativity", 1, 5, 3)
    business = st.slider("Business Interest", 1, 5, 3)
    design = st.slider("Design Interest", 1, 5, 3)
    problem = st.slider("Problem Solving", 1, 5, 3)
    data = st.slider("Data Analysis", 1, 5, 3)

    submit = st.form_submit_button("Recommend Careers")

if submit:
    student = pd.DataFrame([{
        "Python": python,
        "Maths": maths,
        "Communication": communication,
        "Creativity": creativity,
        "Business": business,
        "Design": design,
        "ProblemSolving": problem,
        "DataAnalysis": data
    }])

    probabilities = model.predict_proba(student)[0]
    classes = model.named_steps["classifier"].classes_
    top = np.argsort(probabilities)[::-1][:3]

    results = pd.DataFrame({
        "Career": classes[top],
        "Model Score (%)": np.round(probabilities[top] * 100, 1)
    })

    st.subheader("Top 3 Career Recommendations")
    st.dataframe(results, use_container_width=True)

    st.download_button(
        "Download Results",
        results.to_csv(index=False),
        "career_recommendations.csv",
        "text/csv"
    )
