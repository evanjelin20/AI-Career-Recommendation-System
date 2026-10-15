
import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(
    page_title="AI Career Recommendation System",
    page_icon="🎓",
    layout="centered"
)

# Custom styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef4ff, #f9f5ff);
}
.main-title {
    text-align: center;
    color: #243b70;
    font-size: 38px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #555b70;
    font-size: 17px;
}
div.stButton > button {
    width: 100%;
    border-radius: 10px;
    font-weight: bold;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# Load trained model
@st.cache_resource
def load_model():
    return joblib.load("career_model.joblib")

try:
    model = load_model()
except Exception as e:
    st.error("Unable to load the trained model.")
    st.write("Check that career_model.joblib is in the same GitHub folder as app.py.")
    st.stop()

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "name" not in st.session_state:
    st.session_state.name = ""

if "profession" not in st.session_state:
    st.session_state.profession = ""

if "other_role" not in st.session_state:
    st.session_state.other_role = ""


# PAGE 1: WELCOME
if st.session_state.page == "welcome":

    st.write("")
    st.write("")

    st.markdown(
        '<div class="main-title">🎓 Welcome!</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI Career Recommendation System'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    st.image(
        "https://images.unsplash.com/photo-1521737711867-e3b97375f902"
        "?auto=format&fit=crop&w=1000&q=80",
        use_container_width=True
    )

    st.subheader("Discover Your Career Possibilities 🚀")

    st.write(
        "Explore potential career paths based on your skills, "
        "interests, and strengths."
    )

    st.info(
        "Tell us a little about yourself, complete a simple skill "
        "assessment, and explore your career recommendations."
    )

    if st.button("Get Started →", type="primary"):
        st.session_state.page = "profile"
        st.rerun()


# PAGE 2: USER DETAILS
elif st.session_state.page == "profile":

    st.title("👤 Tell Us About Yourself")
    st.write("Enter your details to personalize your experience.")

    name = st.text_input(
        "Your Name",
        value=st.session_state.name,
        placeholder="Enter your full name"
    )

    profession_options = [
        "Student",
        "Working Professional",
        "Job Seeker",
        "Entrepreneur",
        "Other"
    ]

    current_profession = st.session_state.profession
    default_index = (
        profession_options.index(current_profession)
        if current_profession in profession_options
        else 0
    )

    profession = st.selectbox(
        "Your Profession",
        profession_options,
        index=default_index
    )

    other_role = ""
    if profession == "Other":
        other_role = st.text_input(
            "Specify Your Role",
            value=st.session_state.other_role,
            placeholder="e.g., Freelancer, Career Changer"
        )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back"):
            st.session_state.page = "welcome"
            st.rerun()

    with col2:
        if st.button("Continue →", type="primary"):
            if not name.strip():
                st.warning("Please enter your name.")
            elif profession == "Other" and not other_role.strip():
                st.warning("Please specify your role.")
            else:
                st.session_state.name = name.strip()
                st.session_state.profession = profession
                st.session_state.other_role = other_role.strip()
                st.session_state.page = "assessment"
                st.rerun()


# PAGE 3: SKILL ASSESSMENT
elif st.session_state.page == "assessment":

    name = st.session_state.name
    profession = st.session_state.profession

    if profession == "Other":
        display_role = st.session_state.other_role
    else:
        display_role = profession

    st.title("🧠 Career Skill Assessment")

    st.write(f"Welcome, **{name}**! 👋")
    st.write(f"Your selected role: **{display_role}**")

    st.write(
        "Rate your current skills from 1 to 5. "
        "Choose the ratings that best reflect your abilities and interests."
    )

    with st.form("career_form"):

        python = st.slider("Python", 1, 5, 3)
        maths = st.slider("Mathematics", 1, 5, 3)
        communication = st.slider("Communication", 1, 5, 3)
        creativity = st.slider("Creativity", 1, 5, 3)
        business = st.slider("Business Interest", 1, 5, 3)
        design = st.slider("Design Interest", 1, 5, 3)
        problem = st.slider("Problem Solving", 1, 5, 3)
        data = st.slider("Data Analysis", 1, 5, 3)

        submit = st.form_submit_button(
            "✨ Recommend Careers",
            type="primary"
        )

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
            "Model Score (%)": np.round(
                probabilities[top] * 100, 1
            )
        })

        st.session_state.results = results

    if "results" in st.session_state:

        st.success(f"Here are your career suggestions, {name}! 🎉")

        st.subheader("🏆 Your Top 3 Career Recommendations")

        st.dataframe(
            st.session_state.results,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Download Results",
            data=st.session_state.results.to_csv(index=False),
            file_name=f"{name.replace(' ', '_')}_career_recommendations.csv",
            mime="text/csv"
        )

        st.caption(
            "These are demonstration predictions from a small sample "
            "dataset, not a validated career assessment."
        )

    st.write("")

    if st.button("← Back to Welcome Page"):
        st.session_state.page = "welcome"
        st.session_state.pop("results", None)
        st.rerun()
