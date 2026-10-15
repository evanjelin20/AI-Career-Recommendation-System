
import os
import html

import joblib
import numpy as np
import pandas as pd
import streamlit as st


# ==================================================
# PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="AI Career Recommendation System",
    page_icon="🎯",
    layout="wide"
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


# ==================================================
# CAREER INFORMATION
# ==================================================
CAREER_DETAILS = {
    "Data Scientist": {
        "icon": "📊",
        "description": "Analyze data and build predictive models.",
        "skills": ["Python", "Statistics", "SQL", "Machine Learning"],
        "develop": ["Learn pandas and NumPy", "Practice SQL", "Build ML projects"]
    },
    "Software Developer": {
        "icon": "💻",
        "description": "Develop and maintain software applications.",
        "skills": ["Python", "Java", "Problem Solving", "Git"],
        "develop": ["Practice coding", "Learn data structures", "Build applications"]
    },
    "Business Analyst": {
        "icon": "📈",
        "description": "Analyze business needs and support decisions.",
        "skills": ["Communication", "Excel", "SQL", "Critical Thinking"],
        "develop": ["Learn Excel", "Practice SQL", "Study business requirements"]
    },
    "UI UX Designer": {
        "icon": "🎨",
        "description": "Design useful, accessible digital experiences.",
        "skills": ["Creativity", "Design", "Communication", "Figma"],
        "develop": ["Learn Figma", "Create wireframes", "Build a portfolio"]
    },
    "Digital Marketer": {
        "icon": "📱",
        "description": "Promote products through digital channels.",
        "skills": ["Communication", "Creativity", "SEO", "Analytics"],
        "develop": ["Learn SEO", "Practice content planning", "Study campaign analytics"]
    }
}


# ==================================================
# CUSTOM STYLING
# ==================================================
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fb;
}

.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: 800;
    color: #243b64;
}

.subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 25px;
}

.career-card {
    background-color: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #dce3ef;
    margin: 10px 0;
}

.career-title {
    font-size: 23px;
    font-weight: bold;
    color: #243b64;
}

.career-score {
    font-size: 18px;
    color: #2563eb;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# LOAD TRAINED MODEL
# ==================================================
@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        return None

    try:
        return joblib.load(MODEL_PATH)
    except Exception:
        return None


model = load_model()


# ==================================================
# FALLBACK CAREER SCORING
# Used if no trained model is available.
# These are heuristic scores, not ML predictions.
# ==================================================
def calculate_scores(student):

    p = student["Python"]
    m = student["Maths"]
    c = student["Communication"]
    cr = student["Creativity"]
    b = student["Business"]
    d = student["Design"]
    ps = student["ProblemSolving"]
    da = student["DataAnalysis"]

    scores = {
        "Data Scientist":
            0.25 * p + 0.25 * m + 0.20 * da
            + 0.20 * ps + 0.10 * cr,

        "Software Developer":
            0.35 * p + 0.30 * ps + 0.15 * m
            + 0.10 * cr + 0.10 * da,

        "Business Analyst":
            0.25 * c + 0.25 * b + 0.20 * da
            + 0.15 * m + 0.15 * ps,

        "UI UX Designer":
            0.35 * d + 0.25 * cr + 0.20 * c
            + 0.10 * ps + 0.10 * b,

        "Digital Marketer":
            0.30 * c + 0.25 * cr + 0.25 * b
            + 0.10 * da + 0.10 * d
    }

    total = sum(scores.values())

    if total <= 0:
        return [
            {"career": career, "score": 20.0}
            for career in CAREER_DETAILS
        ]

    results = []

    for career, score in scores.items():
        results.append({
            "career": career,
            "score": round(score / total * 100, 2)
        })

    return sorted(
        results,
        key=lambda item: item["score"],
        reverse=True
    )


# ==================================================
# CAREER RECOMMENDATION FUNCTION
# ==================================================
def recommend_careers(student):

    if model is None:
        return calculate_scores(student), "Skill-based scoring"

    input_df = pd.DataFrame(
        [[student[f] for f in FEATURES]],
        columns=FEATURES
    )

    try:
        # Use the feature format expected by the trained model.
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(input_df)[0]
            classes = model.classes_

            results = [
                {
                    "career": str(career),
                    "score": round(float(probability) * 100, 2)
                }
                for career, probability in zip(classes, probabilities)
            ]

            if results:
                return sorted(
                    results,
                    key=lambda item: item["score"],
                    reverse=True
                ), "Trained ML model"

        # Support models that only implement predict().
        prediction = model.predict(input_df)[0]

        return [{
            "career": str(prediction),
            "score": 100.0
        }], "Trained ML model"

    except Exception:
        try:
            # Retry with a NumPy array for models requiring array input.
            input_array = np.array(
                [[student[f] for f in FEATURES]],
                dtype=float
            )

            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(input_array)[0]

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
                        results,
                        key=lambda item: item["score"],
                        reverse=True
                    ), "Trained ML model"

            prediction = model.predict(input_array)[0]

            return [{
                "career": str(prediction),
                "score": 100.0
            }], "Trained ML model"

        except Exception:
            return calculate_scores(student), "Skill-based scoring"


# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:

    st.title("🎯 Career Navigator")
    st.write("Explore careers based on your skills.")

    st.divider()

    student_name = st.text_input(
        "Student name",
        placeholder="Enter your name"
    )

    st.markdown("### Rate your skills")

    st.caption("0 = Beginner | 10 = Very strong")

    skill_values = {}

    for feature in FEATURES:
        skill_values[feature] = st.slider(
            feature,
            min_value=0,
            max_value=10,
            value=5,
            step=1
        )

    analyze = st.button(
        "🚀 Recommend Careers",
        type="primary",
        use_container_width=True
    )


# ==================================================
# MAIN PAGE
# ==================================================
st.markdown(
    '<div class="main-title">🎯 AI Career Recommendation System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Discover career paths that match your strengths and interests.'
    '</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

col1.metric("Career Options", len(CAREER_DETAILS))
col2.metric("Skills Evaluated", len(FEATURES))
col3.metric("Skill Rating", "0–10")

st.divider()

st.subheader("📋 About this system")

st.write(
    "Rate your skills in the sidebar and click **Recommend Careers** "
    "to see the highest-ranked careers, related skills, and areas to develop."
)

if model is None:
    st.info(
        "No compatible saved model was loaded. The app is using "
        "skill-based scoring. Add a compatible career_model.joblib "
        "file to use your trained model."
    )


# ==================================================
# DISPLAY RESULTS
# ==================================================
if analyze:

    student = {
        feature: int(skill_values[feature])
        for feature in FEATURES
    }

    results, method = recommend_careers(student)

    # Normalize DataFrame results, if a function returns one.
    if isinstance(results, pd.DataFrame):

        results = results.rename(columns={
            "Career": "career",
            "Score": "score",
            "Probability": "score"
        }).to_dict(orient="records")

    # Ensure that results are a list of dictionaries.
    if not isinstance(results, list):
        results = []

    valid_results = []

    for item in results:
        if isinstance(item, dict) and item.get("career") is not None:
            try:
                score = float(item.get("score", 0))
            except (TypeError, ValueError):
                score = 0.0

            valid_results.append({
                "career": str(item["career"]),
                "score": score
            })

    results = sorted(
        valid_results,
        key=lambda item: item["score"],
        reverse=True
    )

    if not results:
        st.error("No recommendations available. Please try again.")

    else:

        display_name = student_name.strip() or "Student"

        # Safe indexing after checking that results is not empty.
        best_career = results[0]["career"]

        st.success(f"Analysis completed for {display_name}!")

        st.markdown(f"## 🎯 Your Career Results, {display_name}")

        st.write(
            "Explore the three careers ranked highest by your model. "
            "Each suggestion includes related skills and areas to develop."
        )

        st.caption(f"Recommendation method: {method}")

        # ------------------------------------------
        # TOP THREE CAREERS
        # ------------------------------------------
        for rank, item in enumerate(results[:3], start=1):

            career = item["career"]
            score = item["score"]

            details = CAREER_DETAILS.get(
                career,
                {
                    "icon": "🌟",
                    "description": "Explore this career and its requirements.",
                    "skills": ["Research required skills"],
                    "develop": ["Take beginner courses", "Build practical projects"]
                }
            )

            icon = details["icon"]
            safe_career = html.escape(career)
            safe_description = html.escape(details["description"])

            st.markdown(
                f"""
                <div class="career-card">
                    <div class="career-title">
                        {icon} #{rank} {safe_career}
                    </div>
                    <p>{safe_description}</p>
                    <div class="career-score">
                        Relative score: {score:.2f}%
                    </div>
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

        # ------------------------------------------
        # SKILL PROFILE - COMPATIBLE CHART
        # ------------------------------------------
        st.subheader("📊 Your Skill Profile")

        skill_df = pd.DataFrame({
            "Skill": FEATURES,
            "Rating": [
                student[feature] for feature in FEATURES
            ]
        })

        # Do not use unsupported y_min or y_max arguments.
        st.bar_chart(
            skill_df.set_index("Skill")
        )

        st.caption("Each bar represents your rating for a skill out of 10.")

        # ------------------------------------------
        # COMPLETE CAREER RANKING
        # ------------------------------------------
        st.subheader("🏆 Complete Career Ranking")

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

        # ------------------------------------------
        # DOWNLOAD REPORT
        # ------------------------------------------
        report = pd.DataFrame([{
            "Student": display_name,
            "Top Career": best_career,
            "Recommendation Method": method,
            **student
        }])

        csv_data = report.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Career Report (CSV)",
            data=csv_data,
            file_name="career_recommendation_report.csv",
            mime="text/csv"
        )

else:
    st.info(
        "👈 Rate your skills in the sidebar and click "
        "**Recommend Careers** to view your results."
    )

    st.subheader("🌟 Explore Career Paths")

    cards = st.columns(3)

    for index, (career, details) in enumerate(CAREER_DETAILS.items()):
        with cards[index % 3]:
            st.markdown(f"### {details['icon']} {career}")
            st.write(details["description"])

st.divider()

st.caption(
    "AI Career Recommendation System | Educational project. "
    "Recommendations are guidance, not a guarantee of career success."
)
