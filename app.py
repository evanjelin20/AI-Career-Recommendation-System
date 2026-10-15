
        
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="AI Career Recommendation System",
    page_icon="🎓",
    layout="wide"
)

# ==================================================
# 2. SESSION STATE INITIALIZATION
# Must run before accessing session_state.page
# ==================================================
defaults = {
    "page": "welcome",
    "name": "",
    "profession": "Student",
    "other_role": "",
    "results": None,
    "selected_career": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==================================================
# 3. CUSTOM CSS
# ==================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef4ff, #faf5ff);
}
.block-container {
    padding-top: 2rem;
}
.hero {
    background: linear-gradient(120deg, #172554, #4338ca, #7e22ce);
    padding: 42px 24px;
    border-radius: 22px;
    color: white;
    text-align: center;
}
.hero h1 {
    color: white;
    font-size: 38px;
}
.hero p {
    color: white;
    font-size: 18px;
}
div.stButton > button {
    border-radius: 10px;
    min-height: 42px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# 4. LOAD TRAINED MODEL
# ==================================================
@st.cache_resource
def load_model():
    return joblib.load("career_model.joblib")


try:
    model = load_model()
except Exception as error:
    st.error("Unable to load the machine learning model.")
    st.write(
        "Make sure career_model.joblib is uploaded to the "
        "same GitHub folder as app.py."
    )
    st.stop()


# ==================================================
# 5. CAREER INFORMATION
# Use the exact career labels from the trained model
# ==================================================
career_skills = {
    "Data Scientist": [
        "Python", "Maths", "Data Analysis", "Problem Solving"
    ],
    "Software Developer": [
        "Python", "Problem Solving", "Maths"
    ],
    "Business Analyst": [
        "Business Interest", "Communication", "Data Analysis"
    ],
    "UI UX Designer": [
        "Design Interest", "Creativity", "Communication"
    ],
    "Digital Marketer": [
        "Communication", "Creativity", "Business Interest"
    ]
}

career_descriptions = {
    "Data Scientist":
        "Uses data, statistics, and machine learning to discover patterns "
        "and support decision-making.",
    "Software Developer":
        "Designs, develops, tests, and maintains software applications.",
    "Business Analyst":
        "Studies business requirements and analyzes information to "
        "identify improvements.",
    "UI UX Designer":
        "Designs user interfaces and improves the experience of using "
        "websites and applications.",
    "Digital Marketer":
        "Promotes products or services through digital channels and "
        "uses audience insights to improve campaigns."
}


# ==================================================
# 6. PAGE 1 - INTERACTIVE WELCOME PAGE
# ==================================================
if st.session_state.page == "welcome":

    st.markdown("""
    <div class="hero">
        <div style="font-size:65px;">🎓</div>
        <h1>AI Career Recommendation System</h1>
        <p>Your Skills. Your Interests. Your Future.</p>
        <p>
        Explore career possibilities with a machine learning
        recommendation demo.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    left, right = st.columns([1.2, 1])

    with left:
        st.header("Discover Your Potential 🚀")
        st.write(
            "Not sure which career to explore? Start by telling us "
            "about yourself and rating your skills."
        )

        st.markdown("""
        - 👤 Personalised welcome
        - 🎯 Profession selection
        - 🧠 Interactive skill assessment
        - 🏆 Top three career suggestions
        - 💡 Reasons behind each suggestion
        - 📥 Downloadable career report
        """)

        if st.button(
            "Get Started →",
            type="primary",
            use_container_width=True
        ):
            st.session_state.page = "profile"
            st.rerun()

    with right:
        st.subheader("✨ Your Journey")

        st.markdown("""
        <div style="
            background:white;
            padding:22px;
            border-radius:16px;
            border-left:5px solid #6366f1;
        ">
            <h3>01 · Create Your Profile</h3>
            <p>Tell us your name and current role.</p>
            <h3>02 · Rate Your Skills</h3>
            <p>Rate eight skills on a scale of 1 to 5.</p>
            <h3>03 · Explore Careers</h3>
            <p>Review career suggestions and explanations.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Interactive career cards
    st.header("💼 Explore Career Areas")
    st.write("Click a card to learn about that career.")

    career_cards = [
        (
            "📊 Data Science",
            "Data Scientist",
            "Analyze data, find patterns, and develop predictive models."
        ),
        (
            "💻 Software Development",
            "Software Developer",
            "Build and maintain applications and software systems."
        ),
        (
            "📈 Business Analysis",
            "Business Analyst",
            "Understand business needs and use data to solve problems."
        ),
        (
            "🎨 UI/UX Design",
            "UI UX Designer",
            "Create intuitive and user-friendly digital experiences."
        ),
        (
            "📱 Digital Marketing",
            "Digital Marketer",
            "Explore digital campaigns, communication, and creativity."
        )
    ]

    columns = st.columns(3)

    for i, (title, career, description) in enumerate(career_cards):
        with columns[i % 3]:
            with st.container(border=True):
                st.subheader(title)
                st.write(description)

                if st.button(
                    "Explore",
                    key=f"career_card_{i}",
                    use_container_width=True
                ):
                    st.session_state.selected_career = career

    if st.session_state.selected_career:
        selected = st.session_state.selected_career

        st.success(f"Selected career to explore: {selected}")
        st.write(career_descriptions[selected])

        if st.button("Start My Assessment →", type="primary"):
            st.session_state.page = "profile"
            st.rerun()

    st.divider()

    # Interactive skill preview
    st.header("🧠 Try a Skill Preview")

    preview_skill = st.selectbox(
        "Choose a skill",
        [
            "Python",
            "Maths",
            "Communication",
            "Creativity",
            "Business Interest",
            "Design Interest",
            "Problem Solving",
            "Data Analysis"
        ]
    )

    preview_rating = st.slider(
        f"Rate your {preview_skill}",
        min_value=1,
        max_value=5,
        value=3,
        key="preview_rating"
    )

    st.progress(preview_rating / 5)

    preview_messages = {
        1: "🌱 Beginner: an opportunity to learn and improve.",
        2: "📘 Developing: you are building your foundation.",
        3: "👍 Intermediate: keep practising this skill.",
        4: "⭐ Strong: you rate yourself highly in this area.",
        5: "🏆 Very strong: you rate this as one of your strengths."
    }

    st.info(preview_messages[preview_rating])

    st.caption(
        "This preview is only for exploration. It does not affect "
        "your actual career prediction."
    )

    st.divider()

    with st.expander("ℹ️ About This Project"):
        st.write(
            "This project uses a Random Forest classification model "
            "trained on a small demonstration dataset. It is intended "
            "for learning and exploration, not professional career advice."
        )

    if st.button(
        "Begin Career Assessment 🚀",
        type="primary",
        use_container_width=True
    ):
        st.session_state.page = "profile"
        st.rerun()

    st.caption(
        "Built using Python, Pandas, NumPy, Scikit-learn and Streamlit."
    )


# ==================================================
# 7. PAGE 2 - USER PROFILE
# ==================================================
elif st.session_state.page == "profile":

    st.title("👤 Tell Us About Yourself")
    st.write("Your details will personalize the application experience.")

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
                placeholder="e.g. Teacher, Freelancer, Career Changer"
            )

        continue_clicked = st.form_submit_button(
            "Continue to Assessment →",
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


# ==================================================
# 8. PAGE 3 - SKILL ASSESSMENT
# ==================================================
elif st.session_state.page == "assessment":

    name = st.session_state.name

    if st.session_state.profession == "Other":
        role = st.session_state.other_role
    else:
        role = st.session_state.profession

    st.title("🧠 Career Skill Assessment")
    st.write(f"Welcome, **{name}**! 👋")
    st.write(f"**Your profession:** {role}")

    st.info(
        "Rate your current skills from 1 (beginner/low) to 5 "
        "(strong/high). Choose ratings that reflect your own assessment."
    )

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

    # Generate career predictions
    if submit:

        # Feature names and order must match training
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
                    ["Python", "Problem Solving", "Communication"]
                )

                strong_skills = [
                    skill for skill in relevant_skills
                    if skill_values[skill] >= 4
                ]

                if strong_skills:
                    reason = (
                        "You rated yourself highly in "
                        + ", ".join(strong_skills)
                        + ". These skills are relevant to exploring "
                        + career + "."
                    )
                else:
                    best_skill = max(
                        relevant_skills,
                        key=lambda skill: skill_values[skill]
                    )

                    reason = (
                        f"Among the skills associated with this career, "
                        f"your highest rating was {best_skill} "
                        f"({skill_values[best_skill]}/5). "
                        "You could continue developing the other skills."
                    )

                result_rows.append({
                    "Career": career,
                    "Model Score (%)": round(
                        float(probabilities[idx]) * 100, 1
                    ),
                    "Career Overview": career_descriptions.get(
                        career,
                        "Explore this career's responsibilities and "
                        "required skills."
                    ),
                    "Why Recommended": reason
                })

            st.session_state.results = pd.DataFrame(result_rows)

        except Exception as error:
            st.error("Unable to generate career recommendations.")
            st.write("Check that the model and feature columns match.")
            st.code(str(error))

    # ==================================================
    # 9. DISPLAY CAREER RESULTS
    # ==================================================
    if st.session_state.results is not None:

        st.divider()
        st.header(f"🏆 Career Recommendations for {name}")

        st.write(
            "Review the top three model predictions, career descriptions, "
            "and skill-based explanations."
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

        st.download_button(
            "📥 Download Career Report",
            data=st.session_state.results.to_csv(index=False),
            file_name=(
                f"{name.replace(' ', '_')}_career_recommendations.csv"
            ),
            mime="text/csv",
            use_container_width=True
        )

        st.caption(
            "Important: This project uses a small demonstration dataset. "
            "Model scores are not probabilities of getting a job. "
            "Recommendations are not a validated career assessment."
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Edit Profile", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()

    with col2:
        if st.button("🔄 Start New Assessment",
                     use_container_width=True):
            st.session_state.results = None
            st.session_state.page = "assessment"
            st.rerun()
