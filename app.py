
# --------------------------------------------------
# PAGE 1: INTERACTIVE WELCOME PAGE
# --------------------------------------------------
if st.session_state.page == "welcome":

    # Hero section
    st.markdown("""
    <div style="
        background: linear-gradient(120deg, #172554, #4f46e5, #7c3aed);
        padding: 42px 25px;
        border-radius: 22px;
        text-align: center;
        color: white;
    ">
        <div style="font-size: 55px;">🎓</div>
        <h1 style="color: white; font-size: 38px;">
            Discover Your Career Path
        </h1>
        <p style="font-size: 17px;">
            Your skills. Your interests. Your future.
        </p>
        <p>
            Explore career possibilities with our Machine Learning demo.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # Interactive call to action
    st.subheader("🚀 Start Your Career Journey")
    st.write(
        "Answer a few questions about yourself and your skills "
        "to explore potential career options."
    )

    if st.button(
        "✨ Get Started",
        type="primary",
        use_container_width=True
    ):
        st.session_state.page = "profile"
        st.rerun()

    st.write("")
    st.divider()

    # Clickable career exploration cards
    st.subheader("💼 Explore Career Paths")
    st.write("Select a career area to learn more.")

    career_info = {
        "📊 Data & Analytics": (
            "Data Analyst",
            "Explore data, identify patterns, and prepare reports."
        ),
        "🤖 AI & Machine Learning": (
            "AI Engineer",
            "Explore intelligent applications and machine learning."
        ),
        "💻 Software Development": (
            "Software Developer",
            "Build, test, and maintain software applications."
        ),
        "🎨 Design & Creativity": (
            "UI/UX Designer",
            "Design useful and user-friendly digital experiences."
        )
    }

    col1, col2 = st.columns(2)

    for index, (label, info) in enumerate(career_info.items()):
        with (col1 if index % 2 == 0 else col2):
            with st.container(border=True):
                st.markdown(f"### {label}")
                st.write(info[1])

                if st.button(
                    "Explore this area",
                    key=f"explore_{index}",
                    use_container_width=True
                ):
                    st.session_state.selected_career = info[0]

    # Show selected career details
    if st.session_state.get("selected_career"):
        selected = st.session_state.selected_career
        st.success(f"You selected: {selected}")
        st.write(
            "Complete the skill assessment to explore career "
            "recommendations tailored to your ratings."
        )

        if st.button("Start Assessment →", key="explore_start"):
            st.session_state.page = "profile"
            st.rerun()

    st.divider()

    # Interactive skill preview
    st.subheader("🧠 Try a Quick Skill Preview")
    st.write("Adjust the slider to see how a skill rating works.")

    preview_skill = st.selectbox(
        "Choose a skill",
        [
            "Python",
            "Mathematics",
            "Communication",
            "Creativity",
            "Problem Solving",
            "Data Analysis"
        ]
    )

    preview_rating = st.slider(
        f"Your {preview_skill} rating",
        min_value=1,
        max_value=5,
        value=3,
        key="homepage_preview_rating"
    )

    st.progress(preview_rating / 5)

    rating_messages = {
        1: "🌱 Beginner — a skill you can start developing.",
        2: "📘 Learning — you are building your foundation.",
        3: "👍 Intermediate — you have some confidence in this skill.",
        4: "⭐ Strong — this is one of your stronger areas.",
        5: "🏆 Very strong — you rate yourself highly in this skill."
    }

    st.info(rating_messages[preview_rating])

    st.caption(
        "This preview is for exploration only. It does not generate "
        "a prediction or change your trained model."
    )

    st.divider()

    # How it works
    st.subheader("⚙️ How It Works")

    with st.expander("Step 1 — Create Your Profile"):
        st.write(
            "Enter your name and select Student, Working Professional, "
            "Job Seeker, Entrepreneur, or specify another role."
        )

    with st.expander("Step 2 — Rate Your Skills"):
        st.write(
            "Rate eight skills from 1 to 5, including Python, "
            "Mathematics, Communication, and Data Analysis."
        )

    with st.expander("Step 3 — View Your Recommendations"):
        st.write(
            "View the top three model predictions, read the career "
            "descriptions and explanations, and download your results."
        )

    # Final call to action
    st.markdown("""
    <div style="
        background-color: #eef2ff;
        padding: 22px;
        border-radius: 16px;
        text-align: center;
    ">
        <h3 style="color: #243b70;">
            Your Next Step Starts Here!
        </h3>
        <p>Explore your strengths and discover new possibilities.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "Start My Career Assessment 🚀",
        type="primary",
        use_container_width=True
    ):
        st.session_state.page = "profile"
        st.rerun()

    st.write("")
    st.caption(
        "AI Career Recommendation System | Built with Python, "
        "Scikit-learn and Streamlit"
    )
