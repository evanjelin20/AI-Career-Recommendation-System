
     
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="AI Career Recommendation System",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef4ff, #f9f5ff);
}
.main-title {
    text-align: center;
    color: #243b70;
    font-size: 40px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #555b70;
    font-size: 18px;
}
div.stButton > button {
    border-radius: 10px;
    font-weight: bold;
    min-height: 42px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD TRAINED MODEL
# --------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load("career_model.joblib")


try:
    model = load_model()
except Exception as error:
    st.error("Unable to load the trained model.")
    st.info(
        "Check that career_model.joblib is in the same "
        "GitHub folder as app.py."
    )
    st.stop()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "name" not in st.session_state:
    st.session_state.name = ""

if "profession" not in st.session_state:
    st.session_state.profession = "Student"

if "other_role" not in st.session_state:
    st.session_state.other_role = ""

if "results" not in st.session_state:
    st.session_state.results = None


# --------------------------------------------------
# CAREER EXPLANATION CONFIGURATION
# --------------------------------------------------
career_skills = {
    "Data Scientist": [
        "Python", "Maths", "Data Analysis", "Problem Solving"
    ],
    "Data Analyst": [
        "Data Analysis", "Maths", "Python", "Problem Solving"
    ],
    "Software Developer": [
        "Python", "Problem Solving", "Maths"
    ],
    "Business Analyst": [
        "Business Interest", "Communication", "Data Analysis"
    ],
    "AI Engineer": [
        "Python", "Maths", "Problem Solving", "Data Analysis"
    ],
    "Web Developer": [
        "Python", "Creativity", "Problem Solving"
    ],
    "UI/UX Designer": [
        "Design Interest", "Creativity", "Communication"
    ],
    "Graphic Designer": [
        "Design Interest", "Creativity"
    ],
    "Business Manager": [
        "Business Interest", "Communication"
    ]
}

career_descriptions = {
    "Data Scientist":
        "Analyzes data and builds models to identify patterns and support decisions.",
    "Data Analyst":
        "Studies data, prepares reports, and finds useful business insights.",
    "Software Developer":
        "Designs, develops, tests, and maintains software applications.",
    "Business Analyst":
        "Studies business needs and uses data to suggest improvements.",
    "AI Engineer":
        "Develops and integrates artificial intelligence solutions.",
    "Web Developer":
        "Builds and maintains websites and web applications.",
    "UI/UX Designer":
        "Designs user-friendly digital experiences and interfaces.",
    "Graphic Designer":
        "Creates visual designs for communication and branding.",
    "Business Manager":
        "Coordinates business activities, people, and organizational goals."
}


# --------------------------------------------------
# PAGE 1: WELCOME PAGE
# --------------------------------------------------
if st.session_state.page == "welcome":

    st.write("")
    st.markdown(
        '<div class="main-title">🎓 AI Career Recommendation System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Discover career possibilities based on your skills and interests'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    left, right = st.columns([1, 1])

    with left:
        st.subheader("🚀 Welcome to Your Career Journey!")

        st.write(
            "Not sure which career path to explore? "
            "This application helps you discover potential careers "
            "based on your self-rated skills and interests."
        )

        st.markdown("""
        **What you can do here:**

        - 👤 Enter your personal profile
        - 🎯 Select your profession
        - 🧠 Rate your skills from 1 to 5
        - 🏆 Explore your top 3 career suggestions
        - 💡 Understand why each career was suggested
        - 📥 Download your results
        """)

        if st.button("Get Started →", type="primary",
                     use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()

    with right:
        st.markdown("""
        <div style="
            background-color: white;
            padding: 35px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        ">
            <div style="font-size: 85px;">🎯</div>
            <h2 style="color:#243b70;">Find Your Direction</h2>
            <p style="color:#555;">
            Understand your strengths and explore possible
            career paths with a machine learning demonstration.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.caption("AI-powered demonstration • Learn • Explore • Grow")


# --------------------------------------------------
# PAGE 2: USER PROFILE
# --------------------------------------------------
elif st.session_state.page == "profile":

    st.title("👤 Tell Us About Yourself")
    st.write("Enter your details to personalize your experience.")

    with st.form("profile_form"):

        name = st.text_input(
            "Your Name",
            value=st.session_state.name,
            placeholder="Enter your name"
        )

        profession_options = [
            "Student",
            "Working Professional",
            "Job Seeker",
            "Entrepreneur",
            "Other"
        ]

        profession = st.selectbox(
            "Choose Your Profession",
            profession_options,
            index=(
                profession_options.index(st.session_state.profession)
                if st.session_state.profession in profession_options
                else 0
            )
        )

        other_role = ""
        if profession == "Other":
            other_role = st.text_input(
                "Specify Your Role",
                value=st.session_state.other_role,
                placeholder="e.g. Freelancer, Teacher, Career Changer"
            )

        continue_clicked = st.form_submit_button(
            "Continue to Skill Assessment →",
            type="primary",
            use_container_width=True
        )

    if continue_clicked:
        if not name.strip():
            st.warning("Please enter your name.")
        elif profession == "Other" and not other_role.strip():
            st.warning("Please specify your role.")
        else:
            st.session_state.name = name.strip()
            st.session_state.profession = profession
            st.session_state.other_role = other_role.strip()
            st.session_state.results = None
            st.session_state.page = "assessment"
            st.rerun()

    if st.button("← Back to Welcome"):
        st.session_state.page = "welcome"
        st.rerun()


# --------------------------------------------------
# PAGE 3: SKILL ASSESSMENT AND RESULTS
# --------------------------------------------------
elif st.session_state.page == "assessment":

    name = st.session_state.name

    if st.session_state.profession == "Other":
        display_role = st.session_state.other_role
    else:
        display_role = st.session_state.profession

    st.title("🧠 Career Skill Assessment")
    st.write(f"Welcome, **{name}**! 👋")
    st.write(f"**Your profession:** {display_role}")

    st.info(
        "Rate your current skills from 1 (beginner/low) "
        "to 5 (strong/high). Answer honestly for more useful suggestions."
    )

    # SKILL INPUT FORM
    with st.form("career_form"):

        st.subheader("Rate Your Skills")

        col1, col2 = st.columns(2)

        with col1:
            python = st.slider("Python", 1, 5, 3)
            maths = st.slider("Mathematics", 1, 5, 3)
            communication = st.slider("Communication", 1, 5, 3)
            creativity = st.slider("Creativity", 1, 5, 3)

        with col2:
            business = st.slider("Business Interest", 1, 5, 3)
            design = st.slider("Design Interest", 1, 5, 3)
            problem = st.slider("Problem Solving", 1, 5, 3)
            data = st.slider("Data Analysis", 1, 5, 3)

        submit = st.form_submit_button(
            "✨ Recommend My Careers",
            type="primary",
            use_container_width=True
        )

    # GENERATE PREDICTIONS
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

        try:
            probabilities = model.predict_proba(student)[0]
            classes = model.named_steps["classifier"].classes_

            top_indices = np.argsort(probabilities)[::-1][:3]

            skill_values = {
                "Python": python,
                "Maths": maths,
                "Communication": communication,
                "Creativity": creativity,
                "Business Interest": business,
                "Design Interest": design,
                "Problem Solving": problem,
                "Data Analysis": data
            }

            result_rows = []

            for idx in top_indices:

                career = str(classes[idx])

                relevant_skills = career_skills.get(
                    career,
                    [
                        "Python",
                        "Problem Solving",
                        "Communication"
                    ]
                )

                strong_skills = [
                    skill for skill in relevant_skills
                    if skill_values[skill] >= 4
                ]

                if strong_skills:
                    reason = (
                        "You rated yourself highly in "
                        + ", ".join(strong_skills)
                        + ". These skills are relevant to this career."
                    )
                else:
                    best_skill = max(
                        relevant_skills,
                        key=lambda skill: skill_values[skill]
                    )

                    reason = (
                        f"Your highest-rated skill among those listed "
                        f"for this career is {best_skill} "
                        f"({skill_values[best_skill]}/5). "
                        "Developing the other relevant skills may help."
                    )

                description = career_descriptions.get(
                    career,
                    "Explore the responsibilities and required skills "
                    "for this career to see whether it interests you."
                )

                result_rows.append({
                    "Career": career,
                    "Model Score (%)": round(
                        float(probabilities[idx]) * 100, 1
                    ),
                    "Career Overview": description,
                    "Why Recommended": reason
                })

            st.session_state.results = pd.DataFrame(result_rows)

        except Exception as error:
            st.error(
                "An error occurred while generating recommendations."
            )
            st.code(str(error))

    # DISPLAY RESULTS
    if st.session_state.results is not None:

        st.divider()
        st.header(f"🏆 Career Recommendations for {name}")

        st.write(
            "These are the top three predictions from the trained model. "
            "Review the reasons and career descriptions below."
        )

        for i, row in st.session_state.results.iterrows():

            with st.container(border=True):

                st.subheader(f"{i + 1}. {row['Career']}")

                st.metric(
                    "Model Score",
                    f"{row['Model Score (%)']:.1f}%"
                )

                st.markdown("**💼 About This Career**")
                st.write(row["Career Overview"])

                st.markdown("**💡 Why Was This Career Recommended?**")
                st.write(row["Why Recommended"])

        st.subheader("📊 Results Summary")

        st.dataframe(
            st.session_state.results,
            use_container_width=True,
            hide_index=True
        )

        csv_data = st.session_state.results.to_csv(index=False)

        st.download_button(
            "📥 Download Career Report",
            data=csv_data,
            file_name=(
                f"{name.replace(' ', '_')}_career_recommendations.csv"
            ),
            mime="text/csv",
            use_container_width=True
        )

        st.caption(
            "Important: This is a demonstration project using a small "
            "sample dataset. Model scores are not guaranteed probabilities "
            "of job success, and recommendations are not a validated "
            "career assessment."
        )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Edit Profile", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()

    with col2:
        if st.button("Start New Assessment", use_container_width=True):
            st.session_state.results = None
            st.session_state.page = "assessment"
            st.rerun()
