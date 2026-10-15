
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
# CAREER INFORMATION
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
# SESSION STATE
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

page_lookup = {p.lower(): p for p in PAGES}

current_page = str(
    st.session_state.get("page", "Welcome")
).strip().lower()

st.session_state.page = page_lookup.get(
    current_page, "Welcome"
)

if not isinstance(st.session_state.profile, dict):
    st.session_state.profile = {}

if not isinstance(st.session_state.ratings, dict):
    st.session_state.ratings = {}

for feature in FEATURES:
    st.session_state.ratings.setdefault(feature, 5)


def navigate(page):
    st.session_state.page = page if page in PAGES else "Welcome"
    st.rerun()


def reset_assessment():
    st.session_state.ratings = {f: 5 for f in FEATURES}
    st.session_state.results = []
    st.session_state.method = ""
    st.session_state.assessment_done = False


# =====================================================
# CSS DESIGN
# =====================================================

st.markdown("""
<style>

.stApp {
    background: #F5F7FC;
    color: #14213D;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: #14213D;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #CBD5E1 !important;
}

[data-testid="stSidebar"] .stButton button {
    width: 100%;
    min-height: 48px;
    text-align: left;
    justify-content: flex-start;
    padding-left: 18px;
    font-size: 15px;
    font-weight: 600;
    border-radius: 10px;
}

[data-testid="stSidebar"] .stButton button[kind="secondary"] {
    background: #FFFFFF;
    color: #14213D !important;
    border: 1px solid #E2E8F0;
}

[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: #E54829;
    color: white !important;
    border: none;
}

[data-testid="stSidebar"] .stButton button p {
    color: inherit !important;
    font-weight: 600;
}

/* HERO SECTION */

.hero {
    background: linear-gradient(120deg, #14213D, #2356A0);
    border-radius: 24px;
    padding: 55px 45px;
    color: white;
    margin-bottom: 25px;
}

.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.13);
    color: white;
    padding: 8px 15px;
    border-radius: 30px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 20px;
}

.hero h1 {
    color: #FFFFFF !important;
    font-size: clamp(30px, 5vw, 52px);
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 20px;
}

.hero p {
    color: #DFE9FF !important;
    font-size: 17px;
    line-height: 1.8;
    max-width: 650px;
}

/* FEATURE CARDS */

.feature-card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    min-height: 190px;
    margin-bottom: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

.feature-card h3 {
    color: #17365D !important;
    font-size: 20px;
    margin-bottom: 15px;
}

.feature-card p {
    color: #64748B !important;
    line-height: 1.7;
}

/* CAREER CARDS */

.career-card {
    background: white;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #E2E8F0;
    margin: 15px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

.career-card h3 {
    color: #17365D !important;
    margin-bottom: 12px;
}

.career-card p {
    color: #64748B !important;
}

.score {
    color: #2563EB;
    font-weight: 700;
    font-size: 18px;
    margin-top: 12px;
}

.step-label {
    color: #2563EB;
    font-weight: 800;
    font-size: 13px;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

/* BUTTONS */

div.stButton > button,
div.stFormSubmitButton > button {
    border-radius: 10px;
    min-height: 45px;
    font-weight: 600;
}

div.stButton > button[kind="primary"],
div.stFormSubmitButton > button[kind="primary"] {
    background: #E54829;
    border-color: #E54829;
    color: white;
}

div.stButton > button[kind="primary"]:hover,
div.stFormSubmitButton > button[kind="primary"]:hover {
    background: #C8371B;
    border-color: #C8371B;
}

/* METRICS */

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E2E8F0;
    padding: 16px;
    border-radius: 12px;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #64748B;
    font-size: 12px;
    padding: 30px;
}

.footer p {
    color: #64748B;
}

/* MOBILE */

@media (max-width: 768px) {
    .hero {
        padding: 30px 22px;
    }

    .hero p {
        font-size: 15px;
    }

    .feature-card {
        min-height: auto;
    }
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
        if hasattr(model, "feature_names_in_"):
            expected = list(model.feature_names_in_)
            if set(expected) != set(FEATURES):
                raise ValueError("Model features do not match assessment.")
            input_df = input_df[expected]

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
            {
                "career": str(prediction),
                "score": 100.0
            }
        ], "Trained ML model"

    except Exception:
        return fallback_recommendations(ratings), "Skill-based scoring"


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🎯 CareerPath")
    st.caption("YOUR CAREER DISCOVERY PLATFORM")

    st.divider()

    icons = {
        "Welcome": "🏠",
        "Profile": "👤",
        "Assessment": "📝",
        "Results": "📊"
    }

    for page in PAGES:

        active = st.session_state.page == page

        if st.button(
            f"{icons[page]}  {page}",
            key=f"nav_{page}",
            use_container_width=True,
            type="primary" if active else "secondary"
        ):
            navigate(page)

    st.divider()

    progress_values = {
        "Welcome": 0.0,
        "Profile": 0.25,
        "Assessment": 0.50,
        "Results": 1.0 if st.session_state.assessment_done else 0.50
    }

    progress = progress_values.get(
        st.session_state.page, 0.0
    )

    st.progress(progress)

    st.caption("Complete your career journey.")

    if st.session_state.profile.get("name"):
        st.write(
            "👤 " + st.session_state.profile["name"]
        )


# =====================================================
# WELCOME PAGE
# =====================================================

if st.session_state.page == "Welcome":

    # FIX: HTML starts at the beginning of the line.
    # This prevents Markdown from displaying HTML as code.

    st.markdown("""
<div class="hero">
    <div class="hero-tag">✦ AI-POWERED CAREER EXPLORATION</div>
    <h1>Discover Your Strengths.<br>Shape Your Future.</h1>
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
    <p>
        Create your profile and share your educational background,
        interests and professional goals.
    </p>
</div>
""", unsafe_allow_html=True)

    with c2:
        st.markdown("""
<div class="feature-card">
    <h3>🧠 Skill Assessment</h3>
    <p>
        Evaluate your technical, analytical and creative abilities
        through a simple assessment.
    </p>
</div>
""", unsafe_allow_html=True)

    with c3:
        st.markdown("""
<div class="feature-card">
    <h3>🚀 Career Guidance</h3>
    <p>
        Discover career recommendations and understand the
        skills required for your next step.
    </p>
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

    def selected_index(options, previous):
        return options.index(previous) if previous in options else 0

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

        elif email.strip() and (
            "@" not in email or "." not in email.split("@")[-1]
        ):
            st.error("Please enter a valid email address.")

        else:

            new_profile = {
                "name": name.strip(),
                "email": email.strip(),
                "status": status,
                "education": education,
                "field": field,
                "goal": goal,
                "interests": interests
            }

            if new_profile != old:
                reset_assessment()

            st.session_state.profile = new_profile

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

        student_name = st.session_state.profile["name"]

        st.write(f"Welcome, **{student_name}**!")

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
                    "Python",
                    0, 10,
                    int(ratings["Python"])
                )

                ratings["DataAnalysis"] = st.slider(
                    "Data Analysis",
                    0, 10,
                    int(ratings["DataAnalysis"])
                )

            with c2:

                ratings["Maths"] = st.slider(
                    "Mathematics",
                    0, 10,
                    int(ratings["Maths"])
                )

                ratings["ProblemSolving"] = st.slider(
                    "Problem Solving",
                    0, 10,
                    int(ratings["ProblemSolving"])
                )

            st.divider()

            st.subheader("🎨 Creative & Professional Skills")

            c3, c4 = st.columns(2)

            with c3:

                ratings["Communication"] = st.slider(
                    "Communication",
                    0, 10,
                    int(ratings["Communication"])
                )

                ratings["Creativity"] = st.slider(
                    "Creativity",
                    0, 10,
                    int(ratings["Creativity"])
                )

            with c4:

                ratings["Business"] = st.slider(
                    "Business",
                    0, 10,
                    int(ratings["Business"])
                )

                ratings["Design"] = st.slider(
                    "Design",
                    0, 10,
                    int(ratings["Design"])
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
                and item.get("score") is not None
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
            if st.button(
                "← Back to Profile",
                use_container_width=True
            ):
                navigate("Profile")

        with col2:
            if st.button(
                "Reset Assessment",
                use_container_width=True
            ):
                reset_assessment()
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

        st.info(
            "Complete your assessment to view your career results."
        )

        if st.button("Start Assessment →", type="primary"):
            navigate("Assessment")

    else:

        name = st.session_state.profile.get(
            "name", "Student"
        )

        st.success(f"Assessment completed for {name}!")

        st.write(
            "Explore your three highest-ranked career recommendations."
        )

        st.caption(
            f"Recommendation method: {st.session_state.method}. "
            "Scores are guidance, not guarantees of career suitability."
        )

        # Convert scores safely into numbers.

        valid_results = []

        for item in results:
            try:
                career = str(item["career"])
                score = float(item["score"])

                if pd.notna(score):
                    valid_results.append({
                        "career": career,
                        "score": score
                    })

            except (ValueError, TypeError, KeyError):
                continue

        results = sorted(
            valid_results,
            key=lambda x: x["score"],
            reverse=True
        )

        if not results:
            st.error("No valid career results are available.")
            st.stop()

        best_career = results[0]["career"]

        st.subheader("🏆 Top Career Recommendations")

        for rank, result in enumerate(results[:3], start=1):

            career = result["career"]
            score = result["score"]

            details = CAREERS.get(
                career,
                {
                    "icon": "🌟",
                    "description": "Explore this career opportunity.",
                    "skills": ["Research this career"],
                    "improve": ["Explore relevant courses"]
                }
            )

            safe_career = html.escape(career)
            safe_description = html.escape(
                details["description"]
            )

            # HTML kept left-aligned to prevent code rendering.

            st.markdown(
                f"""
<div class="career-card">
    <h3>{details['icon']} #{rank} {safe_career}</h3>
    <p>{safe_description}</p>
    <div class="score">Relative Score: {score:.2f}%</div>
</div>
""",
                unsafe_allow_html=True
            )

            c1, c2 = st.columns(2)

            with c1:

                st.markdown("**💡 Related Skills**")

                for skill in details["skills"]:
                    st.write(f"• {skill}")

            with c2:

                st.markdown("**📚 Areas to Develop**")

                for skill in details["improve"]:
                    st.write(f"• {skill}")

            st.divider()

        # =================================================
        # SKILL PROFILE
        # =================================================

        st.subheader("📊 Your Skill Profile")

        skill_df = pd.DataFrame({
            "Skill": FEATURES,
            "Rating": [
                int(st.session_state.ratings.get(f, 5))
                for f in FEATURES
            ]
        })

        st.bar_chart(
            skill_df.set_index("Skill")
        )

        st.caption(
            "Skill ratings are measured on a scale of 0 to 10."
        )

        # =================================================
        # COMPLETE CAREER RANKING
        # =================================================

        st.subheader("📈 Complete Career Ranking")

        ranking_df = pd.DataFrame(results)

        ranking_df = ranking_df.rename(
            columns={
                "career": "Career",
                "score": "Relative Score (%)"
            }
        )

        st.dataframe(
            ranking_df,
            use_container_width=True,
            hide_index=True
        )

        # =================================================
        # DOWNLOAD CAREER REPORT
        # =================================================

        st.subheader("📥 Download Your Career Report")

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
            label="⬇️ Download Career Report",
            data=report.to_csv(index=False).encode("utf-8"),
            file_name="career_report.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.write("")

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "← Edit Assessment",
                use_container_width=True
            ):
                navigate("Assessment")

        with c2:

            if st.button(
                "Start New Assessment",
                use_container_width=True
            ):

                st.session_state.profile = {}

                reset_assessment()

                navigate("Welcome")


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown("""
<div class="footer">
    CareerPath © 2026 | AI Career Recommendation System
    <p>Discover Your Strengths. Shape Your Future.</p>
</div>
""", unsafe_allow_html=True)
