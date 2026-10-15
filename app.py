
import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="AI Career Recommendation System",
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

CAREER_DETAILS = {
    "Data Scientist": {
        "description": "Analyze data and build predictive models to solve business problems.",
        "skills": ["Python", "Statistics", "SQL", "Machine Learning", "Data Visualization"],
        "develop": ["Practice pandas and NumPy", "Learn SQL", "Build ML projects"],
        "icon": "📊"
    },
    "Software Developer": {
        "description": "Design, develop, test, and maintain software applications.",
        "skills": ["Programming", "Problem Solving", "Java", "Python", "Git"],
        "develop": ["Practice coding problems", "Learn data structures", "Build applications"],
        "icon": "💻"
    },
    "Business Analyst": {
        "description": "Understand business requirements and turn information into useful decisions.",
        "skills": ["Communication", "SQL", "Excel", "Business Analysis", "Critical Thinking"],
        "develop": ["Improve Excel skills", "Practice SQL queries", "Learn requirement gathering"],
        "icon": "📈"
    },
    "UI UX Designer": {
        "description": "Create user-friendly digital products and engaging user experiences.",
        "skills": ["Creativity", "UI Design", "UX Research", "Wireframing", "Figma"],
        "develop": ["Learn Figma", "Create wireframes", "Build a design portfolio"],
        "icon": "🎨"
    },
    "Digital Marketer": {
        "description": "Promote products and services using digital channels and marketing strategies.",
        "skills": ["Communication", "Creativity", "SEO", "Content Strategy", "Analytics"],
        "develop": ["Learn SEO basics", "Practice content planning", "Study campaign analytics"],
        "icon": "📱"
    }
}

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fb;
    }

    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #243b64;
        text-align: center;
        margin-bottom: 8px;
    }

    .subtitle {
        color: #64748b;
        text-align: center;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .career-card {
        background: white;
        padding: 22px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        margin-bottom: 18px;
    }

    .career-heading {
        font-size: 23px;
        font-weight: 700;
        color: #243b64;
    }

    .score {
        color: #2563eb;
        font-weight: 700;
        font-size: 18px;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        min-height: 45px;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# MODEL LOADING
# --------------------------------------------------
@st.cache_resource
def load_model():
    """Load the saved model. Return None if it cannot be loaded."""
    if not os.path.exists(MODEL_PATH):
        return None

    try:
        return joblib.load(MODEL_PATH)
    except Exception:
        return None


model = load_model()


# --------------------------------------------------
# CAREER SCORING FALLBACK
# Used when the saved ML model is unavailable.
# These are heuristic scores, not trained ML predictions.
# --------------------------------------------------
def calculate_fallback_scores(student):
    python = student["Python"]
    maths = student["Maths"]
    communication = student["Communication"]
    creativity = student["Creativity"]
    business = student["Business"]
    design = student["Design"]
    problem_solving = student["ProblemSolving"]
    data_analysis = student["DataAnalysis"]

    scores = {
        "Data Scientist": (
            0.25 * python
            + 0.25 * maths
            + 0.20 * data_analysis
            + 0.20 * problem_solving
            + 0.10 * creativity
        ),
        "Software Developer": (
            0.35 * python
            + 0.30 * problem_solving
            + 0.15 * maths
            + 0.10 * creativity
            + 0.10 * data_analysis
        ),
        "Business Analyst": (
            0.25 * communication
            + 0.25 * business
            + 0.20 * data_analysis
            + 0.15 * maths
            + 0.15 * problem_solving
        ),
        "UI UX Designer": (
            0.35 * design
            + 0.25 * creativity
            + 0.20 * communication
            + 0.10 * problem_solving
            + 0.10 * business
        ),
        "Digital Marketer": (
            0.30 * communication
            + 0.25 * creativity
            + 0.25 * business
            + 0.10 * data_analysis
            + 0.10 * design
        )
    }

    # Convert scores to a relative percentage distribution.
    total = sum(max(score, 0) for score in scores.values())

    if total <= 0:
        return [
            {"career": career, "score": 20.0}
            for career in CAREER_DETAILS
        ]

    return [
        {
            "career": career,
            "score": round(max(score, 0) / total * 100, 2)
        }
        for career, score in scores.items()
    ]


# --------------------------------------------------
# GENERATE CAREER RECOMMENDATIONS
# --------------------------------------------------
def recommend_careers(student):
    if model is None:
        return calculate_fallback_scores(student), "skill-based fallback"

    try:
        # Preserve feature names for models trained using DataFrames.
        input_df = pd.DataFrame(
            [[student[feature] for feature in FEATURES]],
            columns=FEATURES
        )

        probabilities = model.predict_proba(input_df)[0]
        classes = list(model.classes_)

        if len(probabilities) != len(classes):
            raise ValueError("Prediction output does not match model classes.")

        results = []

        for career, probability in zip(classes, probabilities):
            results.append({
                "career": str(career),
                "score": round(float(probability) * 100, 2)
            })

        results.sort(key=lambda item: item["score"], reverse=True)

        if not results:
            raise ValueError("The model returned no career results.")

        return results, "trained ML model"

    except Exception as error:
        # A model may have been trained with a different input format.
        try:
            input_array = np.array(
                [[student[feature] for feature in FEATURES]],
                dtype=float
            )

            probabilities = model.predict_proba(input_array)[0]
            classes = list(model.classes_)

            results = [
                {
                    "career": str(career),
                    "score": round(float(probability) * 100, 2)
                }
                for career, probability in zip(classes, probabilities)
            ]

            results.sort(key=lambda item: item["score"], reverse=True)

            if results:
                return results, "trained ML model"

        except Exception:
            pass

        st.warning(
            "The saved model could not process these inputs. "
            "Showing skill-based recommendations instead."
        )
        return calculate_fallback_scores(student), "skill-based fallback"


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.title("🎯 Career Navigator")
    st.write("Discover career paths based on your skills.")

    st.divider()

    student_name = st.text_input(
        "Student name",
        value="",
        placeholder="Enter your name"
    )

    st.caption("Rate each skill from 0 to 10.")
    st.caption("0 = Beginner | 10 = Very strong")

    st.divider()

    st.markdown("### Your skill ratings")

    skill_values = {}

    for feature in FEATURES:
        skill_values[feature] = st.slider(
            feature,
            min_value=0,
            max_value=10,
            value=5,
            step=1,
            key=f"skill_{feature}"
        )

    st.divider()

    analyze = st.button(
        "🚀 Recommend Careers",
        type="primary",
        use_container_width=True
    )


# --------------------------------------------------
# MAIN PAGE
# --------------------------------------------------
st.markdown(
    '<div class="main-title">🎯 AI Career Recommendation System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Discover career paths that align with your skills, interests, '
    'and strengths.'
    '</div>',
    unsafe_allow_html=True
)

# Welcome section
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Career Options", len(CAREER_DETAILS))

with col2:
    st.metric("Skills Evaluated", len(FEATURES))

with col3:
    st.metric("Rating Scale", "0–10")

st.divider()

st.subheader("📋 About this system")
st.write(
    "Rate your skills in the sidebar and click **Recommend Careers**. "
    "The application ranks suitable career options and suggests skills "
    "you can develop next."
)

if model is None:
    st.info(
        "No usable saved model was loaded. The app will use a transparent, "
        "skill-based scoring method. To use trained ML predictions, add a "
        "compatible career_model.joblib file."
    )

# --------------------------------------------------
# RESULTS
# --------------------------------------------------
if analyze:

    student = {
        feature: int(skill_values[feature])
        for feature in FEATURES
    }

    results, method = recommend_careers(student)

    # Critical fix: normalize and validate results before indexing.
    if isinstance(results, pd.DataFrame):
        # Support a DataFrame with Career/Score or career/score columns.
        results = results.rename(columns={
            "Career": "career",
            "Score": "score",
            "Probability": "score"
        }).to_dict(orient="records")

    if not isinstance(results, list):
        st.error("Career results are in an unsupported format.")
        st.stop()

    results = [
        item for item in results
        if isinstance(item, dict) and item.get("career") is not None
    ]

    if not results:
        st.error(
            "No career recommendations were generated. "
            "Please check your model and try again."
        )
        st.stop()

    results.sort(
        key=lambda item: float(item.get("score", 0)),
        reverse=True
    )

    # Avoid the original error:
    # results[0]["career"] when results is empty or incorrectly structured.
    best_career = results[0]["career"]

    display_name = student_name.strip() or "Student"

    st.success(f"Analysis completed for {display_name}!")

    st.markdown(
        f"## 🎯 Your Career Results, {display_name}"
    )

    st.write(
        "Explore the three careers ranked highest by your model. "
        "Each suggestion includes related skills and areas to develop."
    )

    st.caption(
        "Recommendation method: " + method +
        ". These results are guidance, not a guarantee of career success."
    )

    # Top three recommendations
    top_results = results[:3]

    for rank, item in enumerate(top_results, start=1):

        career = item["career"]

        try:
            score = float(item.get("score", 0))
        except (TypeError, ValueError):
            score = 0.0

        details = CAREER_DETAILS.get(
            career,
            {
                "description": "Explore this career and its requirements.",
                "skills": ["Research the required skills"],
                "develop": ["Explore beginner courses", "Build practical projects"],
                "icon": "🌟"
            }
        )

        st.markdown(
            f"""
            <div class="career-card">
                <div class="career-heading">
                    {details["icon"]} #{rank} {career}
                </div>
                <p>{details["description"]}</p>
                <div class="score">Relative score: {score:.2f}%</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        left, right = st.columns(2)

        with left:
            st.markdown("**💡 Related skills**")
            for skill in details["skills"]:
                st.markdown(f"- {skill}")

        with right:
            st.markdown("**📚 Areas to develop**")
            for skill in details["develop"]:
                st.markdown(f"- {skill}")

        st.divider()

    # Skill profile
    st.subheader("📊 Your Skill Profile")

    skill_df = pd.DataFrame({
        "Skill": FEATURES,
        "Rating": [student[feature] for feature in FEATURES]
    })

    st.bar_chart(
        skill_df.set_index("Skill"),
        y="Rating",
        y_min=0,
        y_max=10
    )

    # Full career ranking
    st.subheader("🏆 Complete Career Ranking")

    ranking_df = pd.DataFrame(results)
    ranking_df = ranking_df.rename(columns={
        "career": "Career",
        "score": "Score (%)"
    })

    st.dataframe(
        ranking_df,
        use_container_width=True,
        hide_index=True
    )

    # Download report
    report_df = pd.DataFrame([{
        "Student": display_name,
        "Top Career": best_career,
        "Recommendation Method": method,
        **student
    }])

    st.download_button(
        label="⬇️ Download Career Report (CSV)",
        data=report_df.to_csv(index=False).encode("utf-8"),
        file_name="career_recommendation_report.csv",
        mime="text/csv"
    )

else:
    st.info(
        "👈 Rate your skills in the sidebar and click "
        "**Recommend Careers** to view your results."
    )

    st.markdown("### 🌟 Available career paths")

    columns = st.columns(3)

    for index, (career, details) in enumerate(CAREER_DETAILS.items()):
        with columns[index % 3]:
            st.markdown(f"#### {details['icon']} {career}")
            st.write(details["description"])

st.divider()

st.caption(
    "AI Career Recommendation System | Educational project | "
    "Recommendations should be considered alongside your interests "
    "and career research."
)
