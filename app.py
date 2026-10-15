
# --------------------------------------------------
# LAST PAGE: TOP 3 CAREER RECOMMENDATIONS
# --------------------------------------------------
elif st.session_state["page"] == "results":

    st.title("🎯 Your Top 3 Career Recommendations")

    st.write(
        f"Hello, {st.session_state['name']}! "
        "Here are your career suggestions based on your skill assessment."
    )

    # Load the trained model
    model_path = Path(__file__).parent / "career_model.joblib"

    try:
        model = joblib.load(model_path)

        # Get the user's saved skill ratings
        scores = st.session_state.get("skill_scores")

        if not scores:
            st.warning("Please complete the skill assessment first.")
            if st.button("Go to Assessment"):
                st.session_state["page"] = "assessment"
                st.rerun()
            st.stop()

        # Build input using the same feature names and order
        # that were used during model training.
        input_data = pd.DataFrame([scores])

        if hasattr(model, "feature_names_in_"):
            input_data = input_data[list(model.feature_names_in_)]

        # Predict career recommendations
        if not hasattr(model, "predict_proba"):
            st.error(
                "Your saved model does not support ranked recommendations. "
                "Please use a classifier that supports predict_proba()."
            )
            st.stop()

        probabilities = model.predict_proba(input_data)[0]

        # Get career labels from the trained model
        if hasattr(model, "named_steps"):
            classifier = list(model.named_steps.values())[-1]
            career_labels = classifier.classes_
        else:
            career_labels = model.classes_

        # Sort from highest to lowest model score
        ranked_indices = np.argsort(probabilities)[::-1][:3]

        # Manually defined career-skill associations.
        # Update these names to match your dataset's career labels.
        career_skills = {
            "Data Scientist": [
                "Python", "Maths", "DataAnalysis", "ProblemSolving"
            ],
            "Data Analyst": [
                "DataAnalysis", "Maths", "Python", "Communication"
            ],
            "Software Developer": [
                "Python", "ProblemSolving", "Maths"
            ],
            "Business Analyst": [
                "Business", "Communication", "DataAnalysis"
            ],
            "UI UX Designer": [
                "Design", "Creativity", "Communication"
            ],
            "Digital Marketer": [
                "Communication", "Creativity", "Business"
            ],
            "Machine Learning Engineer": [
                "Python", "Maths", "DataAnalysis", "ProblemSolving"
            ],
            "Cybersecurity Analyst": [
                "ProblemSolving", "Python", "Maths"
            ]
        }

        career_descriptions = {
            "Data Scientist":
                "Analyses data and develops predictive models.",
            "Data Analyst":
                "Uses data, charts and reports to support decisions.",
            "Software Developer":
                "Builds and maintains applications and software.",
            "Business Analyst":
                "Connects business requirements with data-driven insights.",
            "UI UX Designer":
                "Designs user-friendly digital products and interfaces.",
            "Digital Marketer":
                "Plans online marketing campaigns and studies audiences.",
            "Machine Learning Engineer":
                "Builds systems that learn patterns from data.",
            "Cybersecurity Analyst":
                "Helps protect computer systems and information."
        }

        career_icons = {
            "Data Scientist": "📊",
            "Data Analyst": "📈",
            "Software Developer": "💻",
            "Business Analyst": "💼",
            "UI UX Designer": "🎨",
            "Digital Marketer": "📣",
            "Machine Learning Engineer": "🤖",
            "Cybersecurity Analyst": "🛡️"
        }

        st.markdown("---")

        for rank, idx in enumerate(ranked_indices, start=1):

            career = str(career_labels[idx])
            score = float(probabilities[idx]) * 100

            skills = career_skills.get(
                career,
                ["Python", "Communication", "ProblemSolving"]
            )

            description = career_descriptions.get(
                career,
                "Explore this career to learn about its responsibilities "
                "and required skills."
            )

            icon = career_icons.get(career, "✨")

            # Career card
            st.subheader(f"{rank}. {icon} {career}")
            st.write(description)

            st.progress(
                max(0.0, min(score / 100.0, 1.0)),
                text=f"Model score: {score:.1f}%"
            )

            # Explain the career using the user's skill ratings
            st.markdown("**💡 Why explore this career?**")

            strong_skills = [
                skill for skill in skills
                if skill in scores and scores[skill] >= 7
            ]

            developing_skills = [
                skill for skill in skills
                if skill in scores and 4 <= scores[skill] < 7
            ]

            if strong_skills:
                st.write(
                    "• Your strongest related self-ratings are: "
                    + ", ".join(
                        f"{skill} ({scores[skill]}/10)"
                        for skill in strong_skills
                    )
                    + "."
                )

            if developing_skills:
                st.write(
                    "• You have a developing foundation in: "
                    + ", ".join(
                        f"{skill} ({scores[skill]}/10)"
                        for skill in developing_skills
                    )
                    + "."
                )

            if not strong_skills and not developing_skills:
                st.write(
                    "• This career is an option to explore. "
                    "You can learn more about its required skills "
                    "and decide whether it interests you."
                )

            st.markdown("**📚 Skills related to this career**")
            st.write(", ".join(skills))

            st.markdown("---")

        st.subheader("📊 Your Skill Summary")

        skill_df = pd.DataFrame({
            "Skill": list(scores.keys()),
            "Self-Rating": list(scores.values())
        }).set_index("Skill")

        st.bar_chart(skill_df, y="Self-Rating")

        st.info(
            "Important: Model scores are the classifier's output scores, "
            "not guaranteed probabilities of career success. The reasons "
            "shown here are based on manually defined career-skill "
            "associations and your self-ratings; they do not explain "
            "the model's internal decision process."
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Retake Assessment", use_container_width=True):
                st.session_state["results"] = None
                st.session_state["skill_scores"] = None
                st.session_state["page"] = "assessment"
                st.rerun()

        with col2:
            if st.button("🏠 Back to Home", use_container_width=True):
                st.session_state["page"] = "welcome"
                st.rerun()

    except Exception as error:
        st.error("Unable to generate the top 3 recommendations.")
        st.code(str(error))
