
import os
import html

import joblib
import numpy as np
import pandas as pd
import streamlit as st


# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="CareerPath | AI Career Recommendation",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

MODEL_PATH = "career_model.joblib"

FEATURES = [
    "Python",
    "Maths",
    "Communication",
    "Creativity",
    "Business",
    "Design",
    "ProblemSolving",
    "DataAnalysis"
]

CAREERS = {
    "Data Scientist": {
        "icon": "📊",
        "description": "Discover insights from data and develop predictive models.",
        "skills": ["Python", "Statistics", "SQL", "Machine Learning"],
        "improve": ["Learn pandas and NumPy", "Practice SQL", "Build data projects"]
    },
    "Software Developer": {
        "icon": "💻",
        "description": "Build, test, and maintain useful software applications.",
        "skills": ["Programming", "Problem Solving", "Java", "Git"],
        "improve": ["Practice coding", "Learn data structures", "Build applications"]
    },
    "Business Analyst": {
        "icon": "📈",
        "description": "Turn business requirements and data into actionable decisions.",
        "skills": ["Communication", "Excel", "SQL", "Critical Thinking"],
        "improve": ["Improve Excel skills", "Practice SQL", "Learn business analysis"]
    },
    "UI UX Designer": {
        "icon": "🎨",
        "description": "Create intuitive, accessible, and engaging user experiences.",
        "skills": ["Creativity", "Design", "Communication", "Figma"],
        "improve": ["Learn Figma", "Create wireframes", "Build a portfolio"]
    },
    "Digital Marketer": {
        "icon": "📱",
        "description": "Help businesses reach audiences through digital channels.",
        "skills": ["Communication", "Creativity", "SEO", "Analytics"],
        "improve": ["Learn SEO", "Plan content", "Study marketing analytics"]
    }
}


# =====================================================
# SESSION STATE
# =====================================================
defaults = {
    "page": "Welcome",
    "profile": {},
    "ratings": {feature: 5 for feature in FEATURES},
    "results": [],
    "method": "",
    "assessment_done": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def go_to(page):
    st.session_state.page = page
    st.rerun()


# =====================================================
# PROFESSIONAL DESIGN
# =====================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #F5F7FC;
    }

    [data-testid="stSidebar"] {
        background: #101C36;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF;
    }

    .brand {
        font-size: 27px;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -1px;
    }

    .brand span {
        color: #78A7FF;
    }

    .hero {
        background: linear-gradient(125deg, #122447 0%, #234C89 60%, #3977C8 100%);
        padding: 54px 42px;
        border-radius: 24px;
        color: white;
        margin-top: 12px;
        margin-bottom: 24px;
        border: 1px solid rgba(255,255,255,0.12);
    }

    .hero-tag {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 30px;
        background: rgba(255,255,255,0.13);
        color: #E4EDFF;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 22px;
    }

    .hero h1 {
        color: white;
        font-size: clamp(34px, 5vw, 54px);
        line-height: 1.15;
        letter-spacing: -2px;
        margin: 0 0 20px 0;
    }

    .hero p {
        color: #E1EAFB;
        font-size: 16px;
        line-height: 1.9;
        max-width: 650px;
    }

    .section-title {
        color: #172B4D;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.8px;
    }

    .section-subtitle {
        color: #64748B;
        font-size: 15px;
        line-height: 1.7;
    }

    .feature-card {
        background: white;
        border: 1px solid #E4EAF3;
        padding: 24px;
        border-radius: 18px;
        min-height: 175px;
        margin-bottom: 12px;
    }

    .feature-card h3 {
        color: #1E3763;
        font-size: 18px;
        margin-top: 12px;
    }

    .feature-card p {
        color: #64748B;
        line-height: 1.7;
        font-size: 14px;
    }

    .step-label {
        color: #356AC3;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.5px;
    }

    .career-card {
        background: white;
        border: 1px solid #E0E8F4;
        border-radius: 18px;
        padding: 24px;
        margin: 10px 0 18px 0;
    }

    .career-card h3 {
        color: #19345E;
        font-size: 22px;
    }

    .muted {
        color: #64748B;
        line-height: 1.7;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 44px;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #E4EAF3;
        padding: 18px;
        border-radius: 14px;
    }

    .footer {
        text-align: center;
        color: #8290A5;
        font-size: 12px;
        padding: 24px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================
# MODEL LOADING
# =====================================================
@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None

    try:
        return joblib.load(MODEL_PATH)
    except Exception:
        return None


model = load_model()


# =====================================================
# CAREER SCORING
# =====================================================
def fallback_recommendations(ratings):
    """Transparent skill-based scoring, not trained ML."""

    p = ratings["Python"]
    m = ratings["Maths"]
    c = ratings["Communication"]
    cr = ratings["Creativity"]
    b = ratings["Business"]
    d = ratings["Design"]
    ps = ratings["ProblemSolving"]
    da = ratings["DataAnalysis"]

    scores = {
        "Data Scientist":
            0.25*p + 0.25*m + 0.20*da + 0.20*ps + 0.10*cr,

        "Software Developer":
            0.35*p + 0.30*ps + 0.15*m + 0.10*cr + 0.10*da,

        "Business Analyst":
            0.25*c + 0.25*b + 0.20*da + 0.15*m + 0.15*ps,

        "UI UX Designer":
            0.35*d + 0.25*cr + 0.20*c + 0.10*ps + 0.10*b,

        "Digital Marketer":
            0.30*c + 0.25*cr + 0.25*b + 0.10*da + 0.10*d
    }

    total = sum(scores.values())

    if total == 0:
        return [
            {"career": career, "score": 20.0}
            for career in CAREERS
        ]

    results = [
        {
            "career": career,
            "score": round(score / total * 100, 2)
        }
        for career, score in scores.items()
    ]

    return sorted(results, key=lambda x: x["score"], reverse=True)


def recommend_careers(ratings):
    if model is None:
        return fallback_recommendations(ratings), "Skill-based scoring"

    input_df = pd.DataFrame(
        [[ratings[f] for f in FEATURES]],
        columns=FEATURES
    )

    try:
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_df)[0]

            results = [
                {
                    "career": str(career),
                    "score": round(float(probability) * 100, 2)
                }
                for career, probability in zip(
                    model.classes_, probabilities
                )
            ]

            if results:
                return sorted(
                    results, key=lambda x: x["score"], reverse=True
                ), "Trained ML model"

        prediction = model.predict(input_df)[0]

        return [
            {"career": str(prediction), "score": 100.0}
        ], "Trained ML model"

    except Exception:
        # Use a clear fallback instead of crashing the website.
        return fallback_recommendations(ratings), "Skill-based scoring"


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
with st.sidebar:
    st.markdown(
        '<div class="brand">Career<span>Path.</span></div>',
        unsafe_allow_html=True
    )

    st.caption("AI-POWERED CAREER EXPLORATION")
    st.divider()

    st.markdown("### Navigation")

    pages = ["Welcome", "Profile", "Assessment", "Results"]

    for page_name in pages:
        icon = {
            "Welcome": "🏠",
            "Profile": "👤",
            "Assessment": "📝",
            "Results": "📊"
        }[page_name]

        if st.button(
            f"{icon}  {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True,
            type="primary" if st.session_state.page == page_name else "secondary"
        ):
            go_to(page_name)

    st.divider()

    if st.session_state.profile.get("name"):
        st.markdown("### Current profile")
        st.write(st.session_state.profile["name"])
        st.caption(
            st.session_state.profile.get("status", "Not specified")
        )

    st.progress(
        {
            "Welcome": 0.0,
            "Profile": 0.25,
            "Assessment": 0.50,
            "Results": 1.0 if st.session_state.assessment_done else 0.50
        }[st.session_state.page]
    )

    st.caption("Your career journey, one step at a time.")


# =====================================================
# PAGE 1: WELCOME
# =====================================================
if st.session_state.page == "Welcome":

    st.markdown("""
    <div class="hero">
        <div class="hero-tag">✦ YOUR FUTURE STARTS HERE</div>
        <h1>Discover your potential.<br>Define your career.</h1>
        <p>
            Welcome to CareerPath, a career exploration platform that
            helps you understand your strengths, explore career options,
            and identify skills to develop for your future.
        </p>
    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 2, 1])

    with center:
        if st.button(
            "Get Started  →",
            type="primary",
            use_container_width=True
        ):
            go_to("Profile")

    st.write("")

    st.markdown(
        '<div class="section-title">A smarter way to explore careers</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="section-subtitle">'
        'A simple, guided journey to help you understand your strengths '
        'and plan your next steps.'
        '</p>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size:30px;">👤</div>
            <h3>01. Build your profile</h3>
            <p>Tell us about your education, current status, and career goals.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size:30px;">🧠</div>
            <h3>02. Assess your skills</h3>
            <p>Rate your strengths across technical, analytical, and creative skills.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature-card">
            <div style="font-size:30px;">🚀</div>
            <h3>03. Explore your future</h3>
            <p>Review career suggestions and discover skills worth developing.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    a, b, c = st.columns(3)
    a.metric("Career paths", "5")
    b.metric("Skill indicators", "8")
    c.metric("Assessment scale", "0–10")

    st.info(
        "Designed for students, graduates, job seekers, and people "
        "exploring their next career move."
    )

    st.markdown(
        '<div class="footer">CAREERPATH · CAREER EXPLORATION PLATFORM</div>',
        unsafe_allow_html=True
    )


# =====================================================
# PAGE 2: PROFILE
# =====================================================
elif st.session_state.page == "Profile":

    st.markdown(
        '<div class="step-label">STEP 01 OF 03</div>',
        unsafe_allow_html=True
    )
    st.title("👤 Your Profile")

    st.markdown(
        '<p class="section-subtitle">'
        'Help us understand your background and what you want to achieve.'
        '</p>',
        unsafe_allow_html=True
    )

    old = st.session_state.profile

    with st.form("profile_form"):

        name = st.text_input(
            "Full name *",
            value=old.get("name", ""),
            placeholder="Enter your name"
        )

        email = st.text_input(
            "Email (optional)",
            value=old.get("email", ""),
            placeholder="you@example.com"
        )

        col1, col2 = st.columns(2)

        with col1:
            status_options = [
                "Student",
                "Working Professional",
                "Job Seeker",
                "Entrepreneur",
                "Other"
            ]

            status = st.selectbox(
                "Current status",
                status_options,
                index=(
                    status_options.index(old["status"])
                    if old.get("status") in status_options else 0
                )
            )

            education = st.selectbox(
                "Education level",
                [
                    "Undergraduate",
                    "Diploma",
                    "Postgraduate",
                    "School Student",
                    "Graduate",
                    "Other"
                ],
                index=0
            )

        with col2:
            field = st.selectbox(
                "Field of study / work",
                [
                    "Artificial Intelligence & Data Science",
                    "Computer Science / IT",
                    "Engineering - Other",
                    "Business / Management",
                    "Arts / Science",
                    "Other"
                ],
                index=0
            )

            goal = st.selectbox(
                "Primary career goal",
                [
                    "Get a job",
                    "Explore career options",
                    "Improve my skills",
                    "Start a business",
                    "Change my career",
                    "Higher studies"
                ]
            )

        interests = st.multiselect(
            "Areas of interest",
            [
                "Technology",
                "Data and Analytics",
                "Business",
                "Design and Creativity",
                "Communication",
                "Research",
                "Entrepreneurship",
                "Marketing"
            ],
            default=old.get("interests", [])
        )

        submitted = st.form_submit_button(
            "Save Profile & Continue →",
            type="primary",
            use_container_width=True
        )

        if submitted:
            if not name.strip():
                st.error("Please enter your name.")
            else:
                st.session_state.profile = {
                    "name": name.strip(),
                    "email": email.strip(),
                    "status": status,
                    "education": education,
                    "field": field,
                    "goal": goal,
                    "interests": interests
                }

                go_to("Assessment")

    st.write("")

    left, right = st.columns(2)

    with left:
        if st.button("← Back to Welcome", use_container_width=True):
            go_to("Welcome")

    with right:
        if st.session_state.profile.get("name"):
            if st.button("Continue to Assessment →", use_container_width=True):
                go_to("Assessment")


# =====================================================
# PAGE 3: ASSESSMENT
# =====================================================
elif st.session_state.page == "Assessment":

    st.markdown(
        '<div class="step-label">STEP 02 OF 03</div>',
        unsafe_allow_html=True
    )

    st.title("📝 Skills Assessment")

    name = st.session_state.profile.get("name", "")

    if not name:
        st.warning("Please complete your profile before starting.")
        if st.button("Go to Profile", type="primary"):
            go_to("Profile")

    else:
        st.markdown(
            f"Welcome, **{html.escape(name)}**! Rate your current skills "
            "honestly. There are no right or wrong answers."
        )

        st.caption(
            "0 = Needs development · 5 = Intermediate · 10 = Very strong"
        )

        st.progress(0.67, text="Step 2: Skills assessment")

        with st.form("assessment_form"):

            st.markdown("### 💻 Technical skills")

            col1, col2 = st.columns(2)

            with col1:
                st.session_state.ratings["Python"] = st.slider(
                    "Python",
                    0, 10,
                    int(st.session_state.ratings["Python"])
                )

                st.session_state.ratings["DataAnalysis"] = st.slider(
                    "Data Analysis",
                    0, 10,
                    int(st.session_state.ratings["DataAnalysis"])
                )

            with col2:
                st.session_state.ratings["Maths"] = st.slider(
                    "Mathematics",
                    0, 10,
                    int(st.session_state.ratings["Maths"])
                )

                st.session_state.ratings["ProblemSolving"] = st.slider(
                    "Problem Solving",
                    0, 10,
                    int(st.session_state.ratings["ProblemSolving"])
                )

            st.divider()
            st.markdown("### 🎨 Professional skills")

            col3, col4 = st.columns(2)

            with col3:
                st.session_state.ratings["Communication"] = st.slider(
                    "Communication",
                    0, 10,
                    int(st.session_state.ratings["Communication"])
                )

                st.session_state.ratings["Creativity"] = st.slider(
                    "Creativity",
                    0, 10,
                    int(st.session_state.ratings["Creativity"])
                )

            with col4:
                st.session_state.ratings["Business"] = st.slider(
                    "Business Skills",
                    0, 10,
                    int(st.session_state.ratings["Business"])
                )

                st.session_state.ratings["Design"] = st.slider(
                    "Design Skills",
                    0, 10,
                    int(st.session_state.ratings["Design"])
                )

            st.write("")

            submit_assessment = st.form_submit_button(
                "Submit Assessment & View Results →",
                type="primary",
                use_container_width=True
            )

            if submit_assessment:
                results, method = recommend_careers(
                    st.session_state.ratings
                )

                if results:
                    st.session_state.results = results
                    st.session_state.method = method
                    st.session_state.assessment_done = True
                    go_to("Results")
                else:
                    st.error("Unable to generate recommendations.")

        st.write("")

        left, right = st.columns(2)

        with left:
            if st.button("← Back to Profile", use_container_width=True):
                go_to("Profile")

        with right:
            if st.button("Reset Ratings", use_container_width=True):
                st.session_state.ratings = {
                    feature: 5 for feature in FEATURES
                }
                st.rerun()


# =====================================================
# PAGE 4: RESULTS
# =====================================================
elif st.session_state.page == "Results":

    st.markdown(
        '<div class="step-label">STEP 03 OF 03</div>',
        unsafe_allow_html=True
    )

    st.title("🎯 Your Career Results")

    if not st.session_state.assessment_done or not st.session_state.results:
        st.info("Complete your skills assessment to see your results.")

        if st.button("Start Assessment →", type="primary"):
            go_to("Assessment")

    else:
        profile = st.session_state.profile
        results = st.session_state.results

        safe_name = html.escape(profile.get("name", "Student"))

        st.markdown(
            f"Hello, **{safe_name}**! Here are your highest-ranked "
            "career suggestions based on your assessment."
        )

        st.caption(
            f"Recommendation method: {st.session_state.method}. "
            "Treat these scores as guidance, not a guarantee of suitability."
        )

        top_results = results[:3]

        for rank, result in enumerate(top_results, start=1):

            career = result["career"]
            score = result["score"]

            details = CAREERS.get(
                career,
                {
                    "icon": "🌟",
                    "description": "Explore the requirements for this career.",
                    "skills": ["Research the role"],
                    "improve": ["Explore courses", "Build practical experience"]
                }
            )

            safe_career = html.escape(career)
            safe_description = html.escape(details["description"])

            st.markdown(
                f"""
                <div class="career-card">
                    <h3>{details["icon"]} #{rank} {safe_career}</h3>
                    <p class="muted">{safe_description}</p>
                    <strong>Relative score: {score:.2f}%</strong>
                </div>
                """,
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**💡 Related skills**")
                for skill in details["skills"]:
                    st.markdown(f"- {skill}")

            with col2:
                st.markdown("**📚 Areas to develop**")
                for skill in details["improve"]:
                    st.markdown(f"- {skill}")

        st.divider()

        st.subheader("📊 Your Skill Profile")

        skill_df = pd.DataFrame({
            "Skill": FEATURES,
            "Rating": [
                st.session_state.ratings[f] for f in FEATURES
            ]
        })

        # Compatible with Streamlit versions that do not support y_min/y_max.
        st.bar_chart(skill_df.set_index("Skill"))

        st.caption("Skill ratings use a scale from 0 to 10.")

        st.subheader("🏆 Complete Career Ranking")

        ranking_df = pd.DataFrame(results).rename(columns={
            "career": "Career",
            "score": "Relative Score (%)"
        })

        st.dataframe(
            ranking_df,
            use_container_width=True,
            hide_index=True
        )

        report = pd.DataFrame([{
            "Student": profile.get("name", ""),
            "Email": profile.get("email", ""),
            "Status": profile.get("status", ""),
            "Education": profile.get("education", ""),
            "Field": profile.get("field", ""),
            "Career Goal": profile.get("goal", ""),
            "Top Career": results[0]["career"],
            "Recommendation Method": st.session_state.method,
            **st.session_state.ratings
        }])

        st.download_button(
            "⬇️ Download Career Report (CSV)",
            data=report.to_csv(index=False).encode("utf-8"),
            file_name="career_report.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.write("")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("← Edit Assessment", use_container_width=True):
                go_to("Assessment")

        with col2:
            if st.button("Start New Assessment", use_container_width=True):
                st.session_state.ratings = {
                    feature: 5 for feature in FEATURES
                }
                st.session_state.results = []
                st.session_state.method = ""
                st.session_state.assessment_done = False
                go_to("Welcome")


# =====================================================
# FOOTER
# =====================================================
st.markdown(
    '<div class="footer">'
    'CAREERPATH © 2026 · AI CAREER RECOMMENDATION SYSTEM'
    '</div>',
    unsafe_allow_html=True
)
