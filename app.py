
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="Career Compass | AI Career Recommendation",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================================================
# 2. INITIALIZE SESSION STATE
# ==================================================
defaults = {
    "page": "welcome",
    "name": "",
    "profession": "Student",
    "other_role": "",
    "skill_scores": None,
    "results": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def go_to(page):
    st.session_state["page"] = page
    st.rerun()


# ==================================================
# 3. PROFESSIONAL DESIGN
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #0b1120, #111b35, #17122e);
    color: #f5f7ff;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    color: #ffffff;
    font-family: 'Space Grotesk', sans-serif;
}

.hero {
    background: linear-gradient(135deg, #18284b, #30235b);
    border: 1px solid #435783;
    border-radius: 24px;
    padding: 32px;
    margin-bottom: 22px;
}

.eyebrow {
    color: #76e5f4;
    letter-spacing: 2px;
    font-size: 12px;
    font-weight: 700;
}

.gradient {
    background: linear-gradient(90deg, #76e5f4, #c5a7ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.muted {
    color: #bdc9e2;
    line-height: 1.8;
}

.feature-card {
    background: #182440;
    border: 1px solid #344668;
    border-radius: 17px;
    padding: 20px;
    min-height: 155px;
    margin-bottom: 12px;
}

.career-card {
    background: #172440;
    border: 1px solid #3b4d70;
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0;
}

div.stButton > button {
    min-height: 45px;
    border-radius: 11px;
    font-weight: 600;
    border: 1px solid #455b83;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #635bdb, #8657d9);
    color: white;
    border: none;
}

div.stButton > button:hover {
    border-color: #76e5f4;
    color: #76e5f4;
}

div[data-testid="stForm"] {
    background: #151f38;
    border: 1px solid #344668;
    padding: 24px;
    border-radius: 18px;
}

.stProgress > div > div {
    background: linear-gradient(90deg, #7565ef, #76e5f4);
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# 4. LOAD TRAINED MODEL
# ==================================================
@st.cache_resource
def load_model():
    model_path = Path(__file__).parent / "career_model.joblib"

    if not model_path.exists():
        raise FileNotFoundError(
            "career_model.joblib must be in the same folder as app.py."
        )

    return joblib.load(model_path)


try:
    model = load_model()
except Exception as error:
    st.error("Unable to load the career prediction model.")
    st.write(
        "Check that career_model.joblib is uploaded to GitHub "
        "beside app.py and that requirements.txt is correct."
    )
    st.exception(error)
    st.stop()


# ==================================================
# 5. CAREER INFORMATION
# ==================================================
career_info = {
    "Data Scientist": {
        "icon": "📊",
        "description": "Analyses data and develops predictive models.",
        "skills": ["Python", "Maths", "DataAnalysis", "ProblemSolving"]
    },
    "Data Analyst": {
        "icon": "📈",
        "description": "Turns data into reports, charts and useful insights.",
        "skills": ["DataAnalysis", "Maths", "Python", "Communication"]
    },
    "Software Developer": {
        "icon": "💻",
        "description": "Builds and maintains applications and software.",
        "skills": ["Python", "ProblemSolving", "Maths"]
    },
    "Business Analyst": {
        "icon": "💼",
        "description": "Connects business needs with data-driven decisions.",
        "skills": ["Business", "Communication", "DataAnalysis"]
    },
    "UI UX Designer": {
        "icon": "🎨",
        "description": "Designs useful and user-friendly digital experiences.",
        "skills": ["Design", "Creativity", "Communication"]
    },
    "Digital Marketer": {
        "icon": "📣",
        "description": "Plans online marketing campaigns and studies audiences.",
        "skills": ["Communication", "Creativity", "Business"]
    },
    "Machine Learning Engineer": {
        "icon": "🤖",
        "description": "Builds systems that learn patterns from data.",
        "skills": ["Python", "Maths", "DataAnalysis", "ProblemSolving"]
    },
    "Cybersecurity Analyst": {
        "icon": "🛡️",
        "description": "Helps protect systems, networks and information.",
        "skills": ["ProblemSolving", "Python", "Maths"]
    }
}


def find_career_info(career):
    for label, info in career_info.items():
        if label.lower() == str(career).strip().lower():
            return info

    return {
        "icon": "✨",
        "description": (
            "Explore this career to learn about its responsibilities, "
            "qualifications and required skills."
        ),
        "skills": [
            "Python", "Communication", "ProblemSolving"
        ]
    }


# ==================================================
# 6. SIDEBAR
# ==================================================
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

    if st.button("🎯 My Results", use_container_width=True):
        if st.session_state["results"] is not None:
            go_to("results")
        else:
            st.warning("Complete the assessment to view results.")

    st.divider()
    st.caption("Discover your potential. Explore your future.")


# ==================================================
# 7. PAGE ONE: WELCOME
# ==================================================
if st.session_state["page"] == "welcome":

    left, right = st.columns([1.1, 0.9], gap="large")

    with left:
        st.markdown("""
        <div class="hero">
            <div class="eyebrow">AI-POWERED CAREER EXPLORATION</div>
            <h1 style="font-size:44px;line-height:1.15;">
                Discover Your<br>
                <span class="gradient">Career Direction.</span>
            </h1>
            <p class="muted">
                Your skills are the beginning of your story.
                Discover career possibilities, understand your strengths,
                and take your next step with confidence.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Your future starts here")
        st.markdown("""
        <p class="muted">
        Complete a simple profile, assess your skills, and explore
        three career options suggested by your trained machine-learning
        model.
        </p>
        """, unsafe_allow_html=True)

        if st.button(
            "🚀 Get Started",
            type="primary",
            use_container_width=True
        ):
            go_to("profile")

        st.caption("Simple assessment · Personalised results · Career exploration")

    with right:
        st.image(
            "https://images.unsplash.com/photo-1521737711867-e3b97375f902"
            "?auto=format&fit=crop&w=1000&q=85",
            use_container_width=True
        )

        st.markdown("""
        <div class="feature-card">
            <h3>🧭 Your Career Compass</h3>
            <p class="muted">
                Understand your current strengths, discover new
                possibilities, and identify skills you can develop.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Your journey in three steps")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="feature-card">
            <h3>01 👤 Profile</h3>
            <p>Enter your name and current role.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
            <h3>02 🧠 Assessment</h3>
            <p>Rate your skills from beginner to confident.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature-card">
            <h3>03 🎯 Results</h3>
            <p>Explore three career recommendations and explanations.</p>
        </div>
        """, unsafe_allow_html=True)

    st.caption(
        "This tool supports career exploration; it does not guarantee "
        "career success or employment."
    )


# ==================================================
# 8. PAGE TWO: USER PROFILE
# ==================================================
elif st.session_state["page"] == "profile":

    st.markdown("## 👤 Let's get to know you")
    st.markdown(
        '<p class="muted">Tell us a little about yourself before '
        'starting your assessment.</p>',
        unsafe_allow_html=True
    )

    with st.form("profile_form"):
        name = st.text_input(
            "Your name",
            value=st.session_state["name"],
            placeholder="Enter your name"
        )

        roles = [
            "Student",
            "Working Professional",
            "Job Seeker",
            "Entrepreneur",
            "Other"
        ]

        current_role = st.session_state["profession"]
        if current_role not in roles:
            current_role = "Other"

        profession = st.selectbox(
            "Your current role",
            roles,
            index=roles.index(current_role)
        )

        other_role = ""
        if profession == "Other":
            other_role = st.text_input(
                "Specify your role",
                value=st.session_state["other_role"]
            )

        submitted = st.form_submit_button(
            "Continue to Assessment →",
            type="primary",
            use_container_width=True
        )

        if submitted:
            if not name.strip():
                st.error("Please enter your name.")
            elif profession == "Other" and not other_role.strip():
                st.error("Please specify your role.")
            else:
                st.session_state["name"] = name.strip()
                st.session_state["profession"] = profession
                st.session_state["other_role"] = other_role.strip()
                go_to("assessment")

    if st.button("← Back to Home"):
        go_to("welcome")


# ==================================================
# 9. PAGE THREE: SKILL ASSESSMENT
# ==================================================
elif st.session_state["page"] == "assessment":

    name = st.session_state["name"] or "Explorer"

    st.markdown(f"## 🧠 {name}, discover your strengths")
    st.markdown("""
    <p class="muted">
    Rate each skill honestly. A rating of 0 means you are a beginner
    or have no experience, while 10 means you feel very confident.
    </p>
    """, unsafe_allow_html=True)

    # IMPORTANT:
    # These names must match the feature columns used to train the model.
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

    with st.form("assessment_form"):
        col1, col2 = st.columns(2)
        scores = {}

        for index, skill in enumerate(skill_names):
            target = col1 if index % 2 == 0 else col2

            with target:
                scores[skill] = st.slider(
                    skill_labels[skill],
                    min_value=0,
                    max_value=10,
                    value=5,
                    help="Rate your current skill from 0 to 10."
                )

        submitted = st.form_submit_button(
            "✨ Generate My Recommendations",
            type="primary",
            use_container_width=True
        )

        if submitted:
            try:
                # Match the exact feature names and order from training.
                feature_names = skill_names

                if hasattr(model, "feature_names_in_"):
                    feature_names = list(model.feature_names_in_)
                elif hasattr(model, "named_steps"):
                    final_estimator = list(model.named_steps.values())[-1]
                    if hasattr(final_estimator, "feature_names_in_"):
                        feature_names = list(
                            final_estimator.feature_names_in_
                        )

                missing = [
                    feature for feature in feature_names
                    if feature not in scores
                ]

                if missing:
                    st.error(
                        "The saved model expects different input features: "
                        + ", ".join(missing)
                        + ". Update skill_names to match your training data."
                    )
                elif not hasattr(model, "predict_proba"):
                    st.error(
                        "The saved model does not support predict_proba(). "
                        "Use a compatible classifier to rank recommendations."
                    )
                else:
                    input_data = pd.DataFrame([{
                        feature: scores[feature]
                        for feature in feature_names
                    }])

                    probabilities = model.predict_proba(input_data)[0]

                    if hasattr(model, "classes_"):
                        classes = model.classes_
                    elif hasattr(model, "named_steps"):
                        final_estimator = list(
                            model.named_steps.values()
                        )[-1]
                        classes = final_estimator.classes_
                    else:
                        raise ValueError(
                            "Unable to find the model's career labels."
                        )

                    # Rank the model's career classes by score.
                    ranked = np.argsort(probabilities)[::-1][:3]

                    results = []
                    for index in ranked:
                        results.append({
                            "career": str(classes[index]),
                            "score": float(probabilities[index]) * 100
                        })

                    st.session_state["skill_scores"] = scores
                    st.session_state["results"] = results

                    go_to("results")

            except Exception as error:
                st.error("Could not generate career recommendations.")
                st.exception(error)

    if st.button("← Back to Profile"):
        go_to("profile")


# ==================================================
# 10. PAGE FOUR: TOP 3 RECOMMENDATIONS
# ==================================================
elif st.session_state["page"] == "results":

    results = st.session_state["results"]
    scores = st.session_state["skill_scores"]

    if not results or not scores:
        st.warning("Please complete your skill assessment first.")
        if st.button("Start Assessment"):
            go_to("assessment")
        st.stop()

    name = st.session_state["name"] or "Explorer"

    st.markdown(f"## 🎯 Your Career Results, {name}")
    st.markdown("""
    <p class="muted">
    Explore the three careers ranked highest by your model.
    Each suggestion includes related skills and areas to develop.
    </p>
    """, unsafe_allow_html=True)

    best_career = results[0]["career"]
    best_info = find_career_info(best_career)

    st.markdown(f"""
    <div class="hero">
        <div class="eyebrow">YOUR TOP MODEL RECOMMENDATION</div>
        <h1>
            {best_info["icon"]}
            <span class="gradient">{best_career}</span>
        </h1>
        <p class="muted">{best_info["description"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🏆 Top 3 career recommendations")

    for rank, result in enumerate(results, start=1):
        career = result["career"]
        score = result["score"]
        info = find_career_info(career)
        related_skills = info["skills"]

        st.markdown(f"""
        <div class="career-card">
            <div class="eyebrow">RECOMMENDATION {rank}</div>
            <h2>{info["icon"]} {career}</h2>
            <p class="muted">{info["description"]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(
            max(0.0, min(score / 100.0, 1.0)),
            text=f"Model score: {score:.1f}%"
        )

        st.markdown("#### 💡 Why explore this career?")

        strong_skills = [
            skill for skill in related_skills
            if skill in scores and scores[skill] >= 7
        ]

        developing_skills = [
            skill for skill in related_skills
            if skill in scores and 4 <= scores[skill] < 7
        ]

        if strong_skills:
            st.write(
                "**Your stronger related self-ratings:** "
                + ", ".join(
                    f"{skill} ({scores[skill]}/10)"
                    for skill in strong_skills
                )
            )

        if developing_skills:
            st.write(
                "**Skills you can continue developing:** "
                + ", ".join(
                    f"{skill} ({scores[skill]}/10)"
                    for skill in developing_skills
                )
            )

        if not strong_skills and not developing_skills:
            st.write(
                "This is a career option suggested by the model. "
                "Explore its responsibilities and practise the relevant skills "
                "to decide whether it fits your interests."
            )

        st.write("**Related skills:** " + ", ".join(related_skills))
        st.divider()

    st.markdown("### 📊 Your skill assessment summary")

    skill_chart = pd.DataFrame({
        "Skill": list(scores.keys()),
        "Self-rating": list(scores.values())
    }).set_index("Skill")

    st.bar_chart(skill_chart, y="Self-rating")

    st.info(
        "How to interpret the results: The model score is the classifier's "
        "output for the supplied skills, not the probability of succeeding "
        "in that career. The explanations use manually defined career-skill "
        "associations and your self-ratings; they are not a direct explanation "
        "of the model's internal decisions."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Retake Assessment", use_container_width=True):
            st.session_state["results"] = None
            st.session_state["skill_scores"] = None
            go_to("assessment")

    with col2:
        if st.button("🏠 Back to Home", use_container_width=True):
            go_to("welcome")


# ==================================================
# 11. FOOTER
# ==================================================
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#9aabc9;'>"
    "CAREER COMPASS | AI CAREER RECOMMENDATION SYSTEM<br>"
    "Career exploration powered by machine learning"
    "</p>",
    unsafe_allow_html=True
)
