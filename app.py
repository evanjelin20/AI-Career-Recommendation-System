
import os
import html
import joblib
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

PAGES = ["Welcome", "Profile", "Assessment", "Results"]

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

MODEL_PATH = "career_model.joblib"


# =====================================================
# CAREER DETAILS
# =====================================================

CAREERS = {
    "Data Scientist": {
        "icon": "📊",
        "description": "Analyze information, identify patterns and build predictive models.",
        "skills": ["Python", "SQL", "Statistics", "Machine Learning"],
        "improve": ["Practice Python", "Learn SQL", "Build data science projects"]
    },

    "Software Developer": {
        "icon": "💻",
        "description": "Design, develop and maintain software applications.",
        "skills": ["Python", "Java", "Problem Solving", "Git"],
        "improve": ["Learn data structures", "Practice coding", "Build applications"]
    },

    "Business Analyst": {
        "icon": "📈",
        "description": "Analyze business requirements and support better decisions.",
        "skills": ["Communication", "Excel", "SQL", "Business Analysis"],
        "improve": ["Improve Excel", "Practice SQL", "Learn business analytics"]
    },

    "UI UX Designer": {
        "icon": "🎨",
        "description": "Create attractive and user-friendly digital experiences.",
        "skills": ["Creativity", "Figma", "Design", "User Research"],
        "improve": ["Learn Figma", "Create wireframes", "Build a portfolio"]
    },

    "Digital Marketer": {
        "icon": "📱",
        "description": "Promote brands and products through digital marketing strategies.",
        "skills": ["Communication", "Creativity", "SEO", "Analytics"],
        "improve": ["Learn SEO", "Practice content planning", "Study marketing analytics"]
    }
}


# =====================================================
# SESSION STATE - FIXES NAVIGATION KEYERROR
# =====================================================

DEFAULTS = {
    "page": "Welcome",
    "profile": {},
    "ratings": {f: 5 for f in FEATURES},
    "results": [],
    "method": "",
    "assessment_done": False
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Normalize unexpected page values from previous app versions.
current_page = str(st.session_state.get("page", "Welcome")).strip().lower()

page_lookup = {p.lower(): p for p in PAGES}

st.session_state.page = page_lookup.get(current_page, "Welcome")

if not isinstance(st.session_state.profile, dict):
    st.session_state.profile = {}

if not isinstance(st.session_state.ratings, dict):
    st.session_state.ratings = {}

for feature in FEATURES:
    st.session_state.ratings.setdefault(feature, 5)


def navigate(page):
    if page in PAGES:
        st.session_state.page = page
    else:
        st.session_state.page = "Welcome"

    st.rerun()


# =====================================================
# PROFESSIONAL CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background: #F5F7FC;
}

.block-container {
    padding-top: 2rem;
    max-width: 1250px;
}

[data-testid="stSidebar"] {
    background: #14213D;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p {
    color: white;
}

.hero {
    background: linear-gradient(120deg, #14213D, #2356A0);
    border-radius: 24px;
    padding: 55px 45px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: clamp(32px, 5vw, 52px);
    font-weight: 800;
    line-height: 1.2;
}

.hero p {
    color: #DFE9FF;
    font-size: 17px;
    line-height: 1.8;
    max-width: 650px;
}

.hero-tag {
    display: inline-block;
    background: #FFFFFF20;
    color: white;
    padding: 8px 15px;
    border-radius: 30px;
    font-size: 13px;
    margin-bottom: 20px;
}

.feature-card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    min-height: 185px;
    margin-bottom: 15px;
}

.feature-card h3 {
    color: #17365D;
    font-size: 20px;
}

.feature-card p {
    color: #64748B;
    line-height: 1.7;
}

.career-card {
    background: white;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    margin: 15px 0;
}

.career-card h3 {
    color: #17365D;
}

.score {
    color: #2563EB;
    font-weight: bold;
    font-size: 18px;
}

.step-label {
    color: #2563EB;
    font-weight: 800;
    font-size: 13px;
    letter-spacing: 1px;
}

div.stButton > button {
    border-radius: 10px;
    min-height: 45px;
    font-weight: 600;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E2E8F0;
    padding: 16px;
    border-radius: 12px;
}

.footer {
    text-align: center;
    color: #64748B;
    font-size: 12px;
    padding: 30px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# MODEL LOADING
# =====================================================

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            return None

    return None


model = load_model()


# =====================================================
# FALLBACK RECOMMENDATION ENGINE
# =====================================================

def fallback_recommendations(r):

    p = r["Python"]
    m = r["Maths"]
    c = r["Communication"]
    cr = r["Creativity"]
    b = r["Business"]
    d = r["Design"]
    ps = r["ProblemSolving"]
    da = r["DataAnalysis"]

    scores = {
        "Data Scientist":
            .25*p + .25*m + .20*da + .20*ps + .10*cr,

        "Software Developer":
            .35*p + .30*ps + .15*m + .10*cr + .10*da,

        "Business Analyst":
            .25*c + .25*b + .20*da + .15*m + .15*ps,

        "UI UX Designer":
            .35*d + .25*cr + .20*c + .10*ps + .10*b,

        "Digital Marketer":
            .30*c + .25*cr + .25*b + .10*da + .10*d
    }

    total = sum(scores.values())

    if total <= 0:
        total = 1

    results = []

    for career, score in scores.items():
        results.append({
            "career": career,
            "score": round(score / total * 100, 2)
        })

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )


# =====================================================
# AI PREDICTION
# =====================================================

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
            classes = model.classes_

            results = []

            for career, probability in zip(classes, probabilities):
                results.append({
                    "career": str(career),
                    "score": round(float(probability) * 100, 2)
                })

            if results:
                results.sort(
                    key=lambda x: x["score"],
                    reverse=True
                )

                return results, "Trained ML model"

        prediction = model.predict(input_df)[0]

        return [
            {"career": str(prediction), "score": 100.0}
        ], "Trained ML model"

    except Exception:
        return fallback_recommendations(ratings), "Skill-based scoring"


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:

    st.title("🎯 CareerPath")
    st.caption("YOUR CAREER DISCOVERY PLATFORM")

    st.divider()

    for page in PAGES:

        icons = {
            "Welcome": "🏠",
            "Profile": "👤",
            "Assessment": "📝",
            "Results": "📊"
        }

        if st.button(
            f"{icons[page]}  {page}",
            key=f"nav_{page}",
            use_container_width=True,
            type="primary" if st.session_state.page == page else "secondary"
        ):
            navigate(page)

    st.divider()

    # SAFE PROGRESS - NO KEYERROR
    progress_values = {
        "Welcome": 0.0,
        "Profile": 0.25,
        "Assessment": 0.50,
        "Results": 1.0 if st.session_state.assessment_done else 0.50
    }

    progress = progress_values.get(
        st.session_state.page,
        0.0
    )

    st.progress(progress)

    st.caption("Complete your career journey.")

    if st.session_state.profile.get("name"):
        st.write("👤", st.session_state.profile["name"])


# =====================================================
# WELCOME PAGE
# =====================================================

if st.session_state.page == "Welcome":

    st.markdown("""
    <div class="hero">
        <div class="hero-tag">✦ AI-POWERED CAREER EXPLORATION</div>

        <h1>
            Discover Your Strengths.<br>
            Shape Your Future.
        </h1>

        <p>
            Your career journey starts with understanding yourself.
            Explore your skills, discover suitable career opportunities,
            and take confident steps toward your professional goals.
        </p>
    </div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1, 2, 1])

    with center:
        if st.button(
            "Get Started →",
            type="primary",
            use_container_width=True
        ):
            navigate("Profile")

    st.write("")

    st.header("Why Choose CareerPath?")

    st.write(
        "A guided platform designed to help students and job seekers "
        "explore career opportunities."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="feature-card">
            <h3>👤 Personal Profile</h3>
            <p>Create your profile and share your educational background,
            interests and professional goals.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
            <h3>🧠 Skill Assessment</h3>
            <p>Evaluate your technical, analytical and creative abilities
            through a simple assessment.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 Career Guidance</h3>
            <p>Discover career recommendations and understand the
            skills required for your next step.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.header("How It Works")

    col1, col2, col3 = st.columns(3)

    col1.info("**STEP 01**\n\nCreate your profile")
    col2.info("**STEP 02**\n\nComplete the assessment")
    col3.info("**STEP 03**\n\nExplore career results")

    st.divider()

    a, b, c = st.columns(3)

    a.metric("Career Paths", "5")
    b.metric("Skill Indicators", "8")
    c.metric("Assessment Scale", "0–10")

    st.write("")

    if st.button(
        "Start Your Career Journey →",
        type="primary",
        use_container_width=True
    ):
        navigate("Profile")


# =====================================================
# PROFILE PAGE
# =====================================================

elif st.session_state.page == "Profile":

    st.markdown(
        '<div class="step-label">STEP 01 OF 03</div>',
        unsafe_allow_html=True
    )

    st.title("👤 Create Your Profile")

    st.write(
        "Tell us about yourself before beginning your career assessment."
    )

    old = st.session_state.profile

    with st.form("profile_form"):

        name = st.text_input(
            "Full Name *",
            value=old.get("name", ""),
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email (Optional)",
            value=old.get("email", ""),
            placeholder="example@gmail.com"
        )

        col1, col2 = st.columns(2)

        status_options = [
            "Student",
            "Graduate",
            "Job Seeker",
            "Working Professional",
            "Other"
        ]

        education_options = [
            "School Student",
            "Diploma",
            "Undergraduate",
            "Postgraduate",
            "Graduate",
            "Other"
        ]

        field_options = [
            "Artificial Intelligence & Data Science",
            "Computer Science",
            "Information Technology",
            "Other Engineering",
            "Business / Management",
            "Arts / Science",
            "Other"
        ]

        goal_options = [
            "Explore Career Options",
            "Get a Job",
            "Improve My Skills",
            "Start a Business",
            "Higher Studies",
            "Career Change"
        ]

        def selected_index(options, previous):
            return options.index(previous) if previous in options else 0

        with col1:

            status = st.selectbox(
                "Current Status",
                status_options,
                index=selected_index(
                    status_options,
                    old.get("status")
                )
            )

            education = st.selectbox(
                "Education",
                education_options,
                index=selected_index(
                    education_options,
                    old.get("education")
                )
            )

        with col2:

            field = st.selectbox(
                "Field of Study",
                field_options,
                index=selected_index(
                    field_options,
                    old.get("field")
                )
            )

            goal = st.selectbox(
                "Career Goal",
                goal_options,
                index=selected_index(
                    goal_options,
                    old.get("goal")
                )
            )

        interest_options = [
            "Technology",
            "Data Analytics",
            "Business",
            "Design",
            "Communication",
            "Research",
            "Marketing",
            "Entrepreneurship"
        ]

        interests = st.multiselect(
            "Areas of Interest",
            interest_options,
            default=[
                x for x in old.get("interests", [])
                if x in interest_options
            ]
        )

        submit = st.form_submit_button(
            "Save Profile & Continue →",
            type="primary",
            use_container_width=True
        )

        if submit:

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

                navigate("Assessment")

    if st.button("← Back to Welcome"):
        navigate("Welcome")


# =====================================================
# ASSESSMENT PAGE
# =====================================================

elif st.session_state.page == "Assessment":

    st.markdown(
        '<div class="step-label">STEP 02 OF 03</div>',
        unsafe_allow_html=True
    )

    st.title("📝 Skills Assessment")

    if not st.session_state.profile.get("name"):

        st.warning("Please complete your profile first.")

        if st.button("Go to Profile", type="primary"):
            navigate("Profile")

    else:

        st.write(
            f"Welcome, **{st.session_state.profile['name']}**!"
        )

        st.write(
            "Rate your current skills from 0 to 10. "
            "There are no right or wrong answers."
        )

        st.progress(0.67)

        ratings = st.session_state.ratings.copy()

        with st.form("assessment_form"):

            st.subheader("💻 Technical & Analytical Skills")

            c1, c2 = st.columns(2)

            with c1:

                ratings["Python"] = st.slider(
                    "Python", 0, 10, int(ratings["Python"])
                )

                ratings["DataAnalysis"] = st.slider(
                    "Data Analysis", 0, 10, int(ratings["DataAnalysis"])
                )

            with c2:

                ratings["Maths"] = st.slider(
                    "Mathematics", 0, 10, int(ratings["Maths"])
                )

                ratings["ProblemSolving"] = st.slider(
                    "Problem Solving", 0, 10, int(ratings["ProblemSolving"])
                )

            st.divider()

            st.subheader("🎨 Creative & Professional Skills")

            c3, c4 = st.columns(2)

            with c3:

                ratings["Communication"] = st.slider(
                    "Communication", 0, 10, int(ratings["Communication"])
                )

                ratings["Creativity"] = st.slider(
                    "Creativity", 0, 10, int(ratings["Creativity"])
                )

            with c4:

                ratings["Business"] = st.slider(
                    "Business", 0, 10, int(ratings["Business"])
                )

                ratings["Design"] = st.slider(
                    "Design", 0, 10, int(ratings["Design"])
                )

            st.write("")

            submit = st.form_submit_button(
                "Submit Assessment & View Results →",
                type="primary",
                use_container_width=True
            )

            if submit:

                st.session_state.ratings = ratings

                results, method = recommend_careers(ratings)

                if isinstance(results, pd.DataFrame):
                    results = results.to_dict(orient="records")

                if not isinstance(results, list):
                    results = []

                results = [
                    item for item in results
                    if isinstance(item, dict)
                    and item.get("career") is not None
                ]

                if results:

                    st.session_state.results = results
                    st.session_state.method = method
                    st.session_state.assessment_done = True

                    navigate("Results")

                else:
                    st.error("Unable to generate recommendations.")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("← Back to Profile", use_container_width=True):
                navigate("Profile")

        with col2:
            if st.button("Reset Assessment", use_container_width=True):

                st.session_state.ratings = {
                    f: 5 for f in FEATURES
                }

                st.session_state.assessment_done = False
                st.session_state.results = []

                st.rerun()


# =====================================================
# RESULTS PAGE
# =====================================================

elif st.session_state.page == "Results":

    st.markdown(
        '<div class="step-label">STEP 03 OF 03</div>',
        unsafe_allow_html=True
    )

    st.title("🎯 Your Career Results")

    results = st.session_state.results

    if not st.session_state.assessment_done or not results:

        st.info("Complete your assessment to view your career results.")

        if st.button("Start Assessment →", type="primary"):
            navigate("Assessment")

    else:

        name = st.session_state.profile.get("name", "Student")

        st.success(f"Assessment completed for {name}!")

        st.write(
            "Explore your three highest-ranked career recommendations."
        )

        st.caption(
            f"Recommendation method: {st.session_state.method}. "
            "Scores are guidance, not guarantees of career suitability."
        )

        results = sorted(
            results,
            key=lambda x: float(x.get("score", 0)),
            reverse=True
        )

        best_career = results[0]["career"]

        st.subheader("🏆 Top Career Recommendations")

        for rank, result in enumerate(results[:3], start=1):

            career = result["career"]
            score = float(result.get("score", 0))

            details = CAREERS.get(
                career,
                {
                    "icon": "🌟",
                    "description": "Explore this career opportunity.",
                    "skills": ["Research this career"],
                    "improve": ["Explore relevant courses"]
                }
            )

            st.markdown(
                f"""
                <div class="career-card">
                    <h3>{details['icon']} #{rank} {html.escape(career)}</h3>
                    <p>{html.escape(details['description'])}</p>
                    <div class="score">Relative Score: {score:.2f}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            c1, c2 = st.columns(2)

            with c1:
                st.markdown("**💡 Related Skills**")

                for skill in details["skills"]:
                    st.write("•", skill)

            with c2:
                st.markdown("**📚 Areas to Develop**")

                for skill in details["improve"]:
                    st.write("•", skill)

            st.divider()

        # =================================================
        # SKILL PROFILE - TYPEERROR FIXED
        # =================================================

        st.subheader("📊 Your Skill Profile")

        skill_df = pd.DataFrame({
            "Skill": FEATURES,
            "Rating": [
                st.session_state.ratings[f]
                for f in FEATURES
            ]
        })

        st.bar_chart(
            skill_df.set_index("Skill")
        )

        st.caption("Skill ratings are measured on a scale of 0 to 10.")

        # =================================================
        # FULL RANKING
        # =================================================

        st.subheader("📈 Complete Career Ranking")

        ranking_df = pd.DataFrame(results)

        ranking_df = ranking_df.rename(columns={
            "career": "Career",
            "score": "Relative Score (%)"
        })

        st.dataframe(
            ranking_df,
            use_container_width=True,
            hide_index=True
        )

        # =================================================
        # DOWNLOAD REPORT
        # =================================================

        report = pd.DataFrame([{
            "Student": name,
            "Status": st.session_state.profile.get("status", ""),
            "Education": st.session_state.profile.get("education", ""),
            "Field": st.session_state.profile.get("field", ""),
            "Career Goal": st.session_state.profile.get("goal", ""),
            "Top Career": best_career,
            "Recommendation Method": st.session_state.method,
            **st.session_state.ratings
        }])

        st.download_button(
            "⬇️ Download Career Report",
            data=report.to_csv(index=False).encode("utf-8"),
            file_name="career_report.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.write("")

        c1, c2 = st.columns(2)

        with c1:
            if st.button("← Edit Assessment", use_container_width=True):
                navigate("Assessment")

        with c2:
            if st.button("Start New Assessment", use_container_width=True):

                st.session_state.profile = {}
                st.session_state.ratings = {
                    f: 5 for f in FEATURES
                }
                st.session_state.results = []
                st.session_state.method = ""
                st.session_state.assessment_done = False

                navigate("Welcome")


# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
    <div class="footer">
        CareerPath © 2026 | AI Career Recommendation System
        <p>Discover Your Strengths. Shape Your Future.</p>
    </div>
    """,
    unsafe_allow_html=True
)
