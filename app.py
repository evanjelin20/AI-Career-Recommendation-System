
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Career Compass | AI Career Guide",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# 2. INITIALIZE SESSION STATE FIRST
# --------------------------------------------------
defaults = {
    "page": "welcome",
    "name": "",
    "profession": "Student",
    "other_role": "",
    "selected_career": None,
    "results": None,
    "skill_scores": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------------------------------
# 3. CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

.stApp {
    background: linear-gradient(145deg, #0b1020 0%, #111a32 55%, #15102a 100%);
    color: #f5f7ff;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1150px;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
    color: #ffffff;
}

.hero {
    padding: 42px 32px;
    border-radius: 25px;
    background: linear-gradient(120deg, #171f3b, #25204b 65%, #12384a);
    border: 1px solid rgba(135, 157, 255, 0.25);
    text-align: center;
    margin-bottom: 25px;
}

.hero-icon {
    font-size: 56px;
    margin-bottom: 8px;
}

.eyebrow {
    color: #67e8f9;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.hero h1 {
    font-size: clamp(32px, 5vw, 54px);
    line-height: 1.12;
    margin: 15px 0;
}

.gradient-text {
    background: linear-gradient(90deg, #67e8f9, #b7a5ff, #f0abfc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #c8d1e8;
    max-width: 650px;
    margin: 0 auto;
    line-height: 1.8;
}

.panel {
    background: rgba(24, 34, 61, 0.78);
    border: 1px solid rgba(148, 163, 184, 0.2);
    padding: 23px;
    border-radius: 19px;
    margin-bottom: 15px;
}

.small-label {
    color: #9aa9c9;
    font-size: 13px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.metric {
    color: #67e8f9;
    font-size: 28px;
    font-weight: 700;
}

.step {
    background: #17213b;
    border: 1px solid #354467;
    border-radius: 15px;
    padding: 18px;
    min-height: 135px;
}

.step-number {
    color: #67e8f9;
    font-size: 13px;
    font-weight: 700;
}

.muted {
    color: #b8c4dc;
    line-height: 1.65;
}

div.stButton > button {
    border-radius: 12px;
    min-height: 45px;
    font-weight: 600;
    border: 1px solid #52638d;
    transition: 0.2s ease;
}

div.stButton > button:hover {
    border-color: #67e8f9;
    color: #67e8f9;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    border: none;
    color: white;
}

div[data-testid="stForm"] {
    background: rgba(24, 34, 61, 0.7);
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #354467;
}

div[data-testid="stSlider"] {
    padding-bottom: 8px;
}

.stProgress > div > div {
    background: linear-gradient(90deg, #6366f1, #67e8f9);
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 4. LOAD TRAINED MODEL
# --------------------------------------------------
@st.cache_resource
def load_model():
    model_path = Path(__file__).parent / "career_model.joblib"
    if not model_path.exists():
        raise FileNotFoundError(
            "career_model.joblib was not found in the project folder."
        )
    return joblib.load(model_path)

try:
    model = load_model()
except Exception as error:
    st.error("Unable to load the trained career prediction model.")
    st.info(
        "Check that career_model.joblib exists in the same GitHub folder "
        "as app.py and that requirements.txt contains the required libraries."
    )
    st.exception(error)
    st.stop()

# --------------------------------------------------
# 5. CAREER INFORMATION
# --------------------------------------------------
career_information = {
    "Data Scientist": {
        "icon": "📊",
        "description": "Explore data, discover patterns and build predictive models.",
        "skills": ["Python", "Maths", "DataAnalysis", "ProblemSolving"]
    },
    "Data Analyst": {
        "icon": "📈",
        "description": "Turn raw data into useful reports, charts and insights.",
        "skills": ["DataAnalysis", "Maths", "Communication", "Python"]
    },
    "Software Developer": {
        "icon": "💻",
        "description": "Build, test and maintain websites, apps and software.",
        "skills": ["Python", "ProblemSolving", "Maths"]
    },
    "Business Analyst": {
        "icon": "💼",
        "description": "Understand business needs and support decisions with data.",
        "skills": ["Business", "Communication", "DataAnalysis"]
    },
    "UI UX Designer": {
        "icon": "🎨",
        "description": "Design clear, attractive and user-friendly digital experiences.",
        "skills": ["Design", "Creativity", "Communication"]
    },
    "Digital Marketer": {
        "icon": "📣",
        "description": "Plan digital campaigns and understand customer engagement.",
        "skills": ["Communication", "Creativity", "Business"]
    },
    "Machine Learning Engineer": {
        "icon": "🤖",
        "description": "Develop software that learns patterns from data.",
        "skills": ["Python", "Maths", "DataAnalysis", "ProblemSolving"]
    },
    "Cybersecurity Analyst": {
        "icon": "🛡️",
        "description": "Help protect systems, networks and information.",
        "skills": ["ProblemSolving", "Python", "Maths"]
    }
}

# These are simple, manually defined explanations.
# They are NOT explanations of the model's internal decision process.
def get_career_info(career):
    for known_career, info in career_information.items():
        if known_career.lower() == str(career).lower():
            return info

    return {
        "icon": "✨",
        "description": (
            "Explore this career by researching its responsibilities, "
            "required qualifications and practical skills."
        ),
        "skills": ["Python", "Communication", "ProblemSolving"]
    }


def get_reasons(career, scores):
    info = get_career_info(career)
    relevant_skills = info["skills"]

    ranked_skills = sorted(
        relevant_skills,
        key=lambda skill: scores.get(skill, 0),
        reverse=True
    )

    reasons = []
    for skill in ranked_skills[:3]:
        score = scores.get(skill, 0)
        if score >= 7:
            reasons.append(
                f"Your self-rating in {skill} is strong ({score}/10)."
            )
        elif score >= 4:
            reasons.append(
                f"You have a developing foundation in {skill} ({score}/10)."
            )

    if not reasons:
        reasons.append(
            "Use this recommendation as a starting point for exploring "
            "your interests and developing relevant skills."
        )

    return reasons


# --------------------------------------------------
# 6. HELPER FUNCTIONS
# --------------------------------------------------
def go_to(page):
    st.session_state.page = page
    st.rerun()


def get_model_classes():
    if hasattr(model, "named_steps"):
        final_estimator = list(model.named_steps.values())[-1]
        if hasattr(final_estimator, "classes_"):
            return final_estimator.classes_

    if hasattr(model, "classes_"):
        return model.classes_

    return None


# --------------------------------------------------
# 7. SIDEBAR NAVIGATION
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 🧭 Career Compass")
    st.caption("AI Career Recommendation System")
    st.divider()

    if st.button("🏠 Home", use_container_width=True):
        go_to("welcome")

    if st.button("👤 My Profile", use_container_width=True):
        go_to("profile")

    if st.button("🧠 Skill Assessment", use_container_width=True):
        go_to("assessment")

    if st.button("✨ My Results", use_container_width=True):
        if st.session_state.results is None:
            st.warning("Complete the skill assessment first.")
        else:
            go_to("results")

    st.divider()
    st.caption("Discover possibilities. Build your future.")

# --------------------------------------------------
# 8. WELCOME PAGE
# --------------------------------------------------
if st.session_state.page == "welcome":

    st.markdown("""
    <div class="hero">
        <div class="hero-icon">🧭</div>
        <div class="eyebrow">Your future, your direction</div>
        <h1>Find Your <span class="gradient-text">Career Compass</span></h1>
        <p>
            Discover career possibilities that connect with your skills,
            interests and strengths. Take a short assessment and explore
            where your next chapter could begin.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ✨ A smarter way to explore your future")
    st.markdown(
        '<p class="muted">Your career journey does not need to start with '
        'guesswork. Start by understanding your current strengths.</p>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="panel">
            <div style="font-size:32px;">🧠</div>
            <h3>Know Your Skills</h3>
            <p class="muted">
                Rate your abilities in programming, communication,
                creativity, business and more.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="panel">
            <div style="font-size:32px;">🎯</div>
            <h3>Explore Careers</h3>
            <p class="muted">
                Get career suggestions from your trained machine-learning
                model and explore relevant skills.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="panel">
            <div style="font-size:32px;">🚀</div>
            <h3>Plan Your Next Step</h3>
            <p class="muted">
                Use your results to decide which skills to practise
                and which careers to research.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🌟 Career worlds to explore")

    career_cols = st.columns(4)
    featured_careers = [
        ("📊", "Data & Analytics"),
        ("💻", "Software & Tech"),
        ("🎨", "Design & Creativity"),
        ("💼", "Business & Strategy")
    ]

    for col, item in zip(career_cols, featured_careers):
        with col:
            st.markdown(f"""
            <div class="step">
                <div style="font-size:30px;">{item[0]}</div>
                <h4>{item[1]}</h4>
                <p class="muted">Discover related opportunities.</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### 🗺️ Your journey in 3 steps")

    step1, step2, step3 = st.columns(3)

    with step1:
        st.markdown("""
        <div class="step">
            <div class="step-number">STEP 01</div>
            <h4>Introduce Yourself</h4>
            <p class="muted">Tell us a little about your current role.</p>
        </div>
        """, unsafe_allow_html=True)

    with step2:
        st.markdown("""
        <div class="step">
            <div class="step-number">STEP 02</div>
            <h4>Rate Your Skills</h4>
            <p class="muted">Answer a few quick self-assessment questions.</p>
        </div>
        """, unsafe_allow_html=True)

    with step3:
        st.markdown("""
        <div class="step">
            <div class="step-number">STEP 03</div>
            <h4>Explore Your Results</h4>
            <p class="muted">Review suggested careers and skill areas.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    left, center, right = st.columns([1, 2, 1])
    with center:
        if st.button(
            "🚀  START MY CAREER JOURNEY",
            type="primary",
            use_container_width=True
        ):
            go_to("profile")

    st.caption(
        "Note: This is an educational career-exploration tool, "
        "not a guarantee of career success or job placement."
    )

# --------------------------------------------------
# 9. PROFILE PAGE
# --------------------------------------------------
elif st.session_state.page == "profile":

    st.markdown("## 👤 Let's get to know you")
    st.markdown(
        '<p class="muted">A few details will help personalise your '
        'career exploration experience.</p>',
        unsafe_allow_html=True
    )

    with st.form("profile_form"):
        name = st.text_input(
            "What should we call you?",
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

        current_profession = st.session_state.profession
        if current_profession not in profession_options:
            current_profession = "Other"

        profession = st.selectbox(
            "Which best describes you?",
            profession_options,
            index=profession_options.index(current_profession)
        )

        other_role = ""
        if profession == "Other":
            other_role = st.text_input(
                "Please specify your role",
                value=st.session_state.other_role,
                placeholder="Enter your role"
            )

        submitted = st.form_submit_button(
            "Continue to Skill Assessment →",
            type="primary",
            use_container_width=True
        )

        if submitted:
            if not name.strip():
                st.error("Please enter your name.")
            elif profession == "Other" and not other_role.strip():
                st.error("Please specify your role.")
            else:
                st.session_state.name = name.strip()
                st.session_state.profession = profession
                st.session_state.other_role = other_role.strip()
                go_to("assessment")

    if st.button("← Back to Home"):
        go_to("welcome")

# --------------------------------------------------
# 10. SKILL ASSESSMENT PAGE
# --------------------------------------------------
elif st.session_state.page == "assessment":

    display_name = st.session_state.name or "Explorer"

    st.markdown(f"## 🧠 {display_name}, let's map your strengths")
    st.markdown(
        '<p class="muted">Rate each skill from 0 to 10 based on your '
        'current self-assessment. There are no right or wrong answers.</p>',
        unsafe_allow_html=True
    )

    # IMPORTANT:
    # These feature names must match the columns used to train your model.
    skill_names = [
        "Python",
        "Maths",
        "Communication",
        "Creativity",
        "Business",
        "Design",
        "ProblemSolving",
        "DataAnalysis"
    ]

    skill_labels = {
        "Python": "💻 Python Programming",
        "Maths": "🔢 Mathematics",
        "Communication": "💬 Communication",
        "Creativity": "🎨 Creativity",
        "Business": "💼 Business Interest",
        "Design": "🖌️ Design Interest",
        "ProblemSolving": "🧩 Problem Solving",
        "DataAnalysis": "📊 Data Analysis"
    }

    with st.form("skills_form"):
        st.markdown("### Rate your current skills")

        col1, col2 = st.columns(2)
        scores = {}

        for index, skill in enumerate(skill_names):
            target_col = col1 if index % 2 == 0 else col2

            with target_col:
                scores[skill] = st.slider(
                    skill_labels[skill],
                    min_value=0,
                    max_value=10,
                    value=5,
                    key=f"skill_{skill}",
                    help="0 = Beginner, 10 = Very confident"
                )

        submitted = st.form_submit_button(
            "✨ Generate My Career Recommendations",
            type="primary",
            use_container_width=True
        )

        if submitted:
            try:
                # Keep the same feature order used by the training dataset.
                feature_names = skill_names

                if hasattr(model, "feature_names_in_"):
                    feature_names = list(model.feature_names_in_)
                elif hasattr(model, "named_steps"):
                    final_estimator = list(model.named_steps.values())[-1]
                    if hasattr(final_estimator, "feature_names_in_"):
                        feature_names = list(final_estimator.feature_names_in_)

                missing_features = [
                    feature for feature in feature_names
                    if feature not in scores
                ]

                if missing_features:
                    st.error(
                        "The model expects different input columns: "
                        + ", ".join(missing_features)
                    )
                    st.info(
                        "Update skill_names to match the exact columns "
                        "used when training career_model.joblib."
                    )
                else:
                    input_data = pd.DataFrame([{
                        feature: scores[feature]
                        for feature in feature_names
                    }])

                    predicted = model.predict(input_data)[0]

                    if hasattr(model, "predict_proba"):
                        probabilities = model.predict_proba(input_data)[0]
                        classes = get_model_classes()

                        if classes is not None:
                            ranked_indices = np.argsort(probabilities)[::-1]
                            recommendations = [
                                {
                                    "career": str(classes[index]),
                                    "score": float(probabilities[index]) * 100
                                }
                                for index in ranked_indices[:3]
                            ]
                        else:
                            recommendations = [{
                                "career": str(predicted),
                                "score": 100.0
                            }]
                    else:
                        recommendations = [{
                            "career": str(predicted),
                            "score": 100.0
                        }]

                    st.session_state.skill_scores = scores
                    st.session_state.results = recommendations
                    go_to("results")

            except Exception as error:
                st.error("Unable to generate recommendations.")
                st.exception(error)

    if st.button("← Back to Profile"):
        go_to("profile")

# --------------------------------------------------
# 11. RESULTS PAGE
# --------------------------------------------------
elif st.session_state.page == "results":

    recommendations = st.session_state.results
    scores = st.session_state.skill_scores

    if not recommendations or not scores:
        st.warning("Please complete the skill assessment first.")
        if st.button("Start Assessment"):
            go_to("assessment")
        st.stop()

    name = st.session_state.name or "Explorer"

    st.markdown(f"## ✨ Your Career Compass, {name}")
    st.markdown(
        '<p class="muted">Here are the career categories suggested by '
        'your model. Use them as starting points for further research.</p>',
        unsafe_allow_html=True
    )

    best = recommendations[0]
    best_info = get_career_info(best["career"])

    st.markdown(f"""
    <div class="hero">
        <div class="hero-icon">{best_info["icon"]}</div>
        <div class="eyebrow">Your top model recommendation</div>
        <h1><span class="gradient-text">{best["career"]}</span></h1>
        <p>{best_info["description"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🏆 Your top recommendations")

    for index, recommendation in enumerate(recommendations, start=1):
        career = recommendation["career"]
        info = get_career_info(career)
        score = recommendation["score"]

        st.markdown(f"""
        <div class="panel">
            <div class="small-label">RECOMMENDATION {index}</div>
            <h3>{info["icon"]} {career}</h3>
            <p class="muted">{info["description"]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(
            max(0.0, min(float(score) / 100.0, 1.0)),
            text=f"Model score: {score:.1f}%"
        )

        st.markdown("**Why explore this career?**")
        for reason in get_reasons(career, scores):
            st.markdown(f"- {reason}")

        with st.expander(f"Skills to explore for {career}"):
            for skill in info["skills"]:
                st.write(
                    f"• {skill}: your self-rating is "
                    f"{scores.get(skill, 0)}/10"
                )

    st.divider()
    st.markdown("### 📊 Your skill snapshot")

    chart_data = pd.DataFrame({
        "Skill": list(scores.keys()),
        "Self-rating": list(scores.values())
    }).set_index("Skill")

    st.bar_chart(chart_data, y="Self-rating")

    st.info(
        "Important: Model scores represent the model's relative output "
        "for the supplied input, not the probability that you will succeed "
        "in a career. The explanations above use manually selected skill "
        "associations and are not model feature-attribution results."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🔄 Retake Assessment",
            use_container_width=True
        ):
            st.session_state.results = None
            st.session_state.skill_scores = None
            go_to("assessment")

    with col2:
        if st.button(
            "🏠 Back to Home",
            use_container_width=True
        ):
            go_to("welcome")

# --------------------------------------------------
# 12. FOOTER
# --------------------------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#9aa9c9;'>"
    "CAREER COMPASS · AI CAREER RECOMMENDATION SYSTEM<br>"
    "Built for career exploration and educational purposes"
    "</p>",
    unsafe_allow_html=True
)
