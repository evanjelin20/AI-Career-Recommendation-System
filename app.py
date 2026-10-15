
# ==================================================
# PAGE 1 - CAREER COMPASS: CREATIVE WELCOME PAGE
# ==================================================
if st.session_state.page == "welcome":

    # Premium visual styling
    st.markdown("""
    <style>
    .stApp {
        background:
            radial-gradient(ellipse at 10% 5%,
            rgba(91, 75, 210, 0.20), transparent 40%),
            radial-gradient(ellipse at 90% 30%,
            rgba(0, 210, 220, 0.10), transparent 35%),
            #080d1b;
        color: #f4f7ff;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
    }

    .brand {
        color: #b8c4ff;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
    }

    .hero-title {
        color: #ffffff;
        font-size: clamp(38px, 5vw, 66px);
        line-height: 1.08;
        font-weight: 850;
        letter-spacing: -2px;
        margin-top: 20px;
        margin-bottom: 18px;
    }

    .gradient-text {
        background: linear-gradient(90deg, #a5b4fc, #67e8f9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        color: #b7c1d8;
        font-size: 17px;
        line-height: 1.8;
        max-width: 680px;
    }

    .eyebrow {
        display: inline-block;
        color: #c4b5fd;
        border: 1px solid rgba(167,139,250,0.4);
        background: rgba(139,92,246,0.12);
        border-radius: 50px;
        padding: 8px 14px;
        font-size: 12px;
        letter-spacing: 1px;
    }

    .orbit-card {
        background: linear-gradient(145deg,
            rgba(30,41,80,0.95),
            rgba(15,23,42,0.95));
        border: 1px solid rgba(148,163,184,0.25);
        border-radius: 26px;
        padding: 28px;
        text-align: center;
        box-shadow: 0 15px 50px rgba(0,0,0,0.25);
    }

    .orbit {
        width: 185px;
        height: 185px;
        margin: 12px auto 25px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 65px;
        background:
            radial-gradient(circle,
            #263b78 0%,
            #151c42 55%,
            #101629 72%);
        border: 1px solid #7184ff;
        box-shadow:
            0 0 25px rgba(99,102,241,0.4),
            inset 0 0 25px rgba(103,232,249,0.12);
        animation: float 4s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }

    .orbit-heading {
        color: white;
        font-size: 22px;
        font-weight: 750;
    }

    .muted {
        color: #a9b5cf;
        font-size: 14px;
        line-height: 1.7;
    }

    .section-heading {
        color: white;
        font-size: 27px;
        font-weight: 750;
        margin-bottom: 5px;
    }

    .career-card {
        min-height: 195px;
        padding: 23px 20px;
        border-radius: 19px;
        border: 1px solid rgba(148,163,184,0.23);
        background: linear-gradient(145deg,
            rgba(26,36,66,0.95),
            rgba(13,20,38,0.98));
        transition: transform 0.2s, border-color 0.2s;
    }

    .career-card:hover {
        transform: translateY(-5px);
        border-color: #818cf8;
    }

    .career-icon {
        font-size: 31px;
        margin-bottom: 12px;
    }

    .career-title {
        color: #f5f7ff;
        font-size: 17px;
        font-weight: 750;
        margin-bottom: 8px;
    }

    .career-desc {
        color: #a9b5cf;
        font-size: 13px;
        line-height: 1.7;
    }

    .step-card {
        background: rgba(24,34,61,0.8);
        border: 1px solid rgba(148,163,184,0.2);
        padding: 19px;
        border-radius: 16px;
        min-height: 135px;
    }

    .step-number {
        color: #67e8f9;
        font-size: 12px;
        letter-spacing: 2px;
        font-weight: 800;
    }

    .step-title {
        color: white;
        font-size: 16px;
        font-weight: 750;
        margin-top: 8px;
    }

    .step-desc {
        color: #a9b5cf;
        font-size: 13px;
        line-height: 1.6;
        margin-top: 7px;
    }

    /* Improve contrast of common Streamlit elements */
    [data-testid="stMarkdownContainer"] p {
        line-height: 1.7;
    }

    div.stButton > button {
        border-radius: 11px;
        min-height: 46px;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

    # TOP BRAND BAR
    brand_left, brand_right = st.columns([2, 1])

    with brand_left:
        st.markdown(
            '<div class="brand">✦ CAREER COMPASS</div>',
            unsafe_allow_html=True
        )

    with brand_right:
        st.markdown(
            '<div style="text-align:right;color:#a9b5cf;'
            'font-size:12px;padding-top:5px;">'
            'DISCOVER · EXPLORE · GROW</div>',
            unsafe_allow_html=True
        )

    st.write("")
    st.write("")

    # HERO SECTION
    hero_left, hero_right = st.columns([1.35, 1], gap="large")

    with hero_left:

        st.markdown(
            '<div class="eyebrow">✦ YOUR PERSONAL CAREER EXPLORER</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="hero-title">'
            'Your future.<br>'
            'Your strengths.<br>'
            '<span class="gradient-text">Your direction.</span>'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="hero-description">'
            'Discover career possibilities that connect with your '
            'skills and interests. Take a simple assessment and explore '
            'new directions for your future.'
            '</div>',
            unsafe_allow_html=True
        )

        st.write("")
        st.write("")

        if st.button(
            "✦  Discover My Career Path  →",
            type="primary",
            use_container_width=True
        ):
            st.session_state.page = "profile"
            st.rerun()

        st.caption(
            "A few simple steps to explore your possibilities."
        )

    with hero_right:

        st.markdown("""
        <div class="orbit-card">
            <div style="color:#a5b4fc;font-size:12px;
                        letter-spacing:3px;font-weight:700;">
                YOUR NEXT CHAPTER
            </div>
            <div class="orbit">🧭</div>
            <div class="orbit-heading">Find Your Direction</div>
            <p class="muted">
                Understand your strengths.<br>
                Explore different career possibilities.<br>
                Take your next step with confidence.
            </p>
            <div style="color:#67e8f9;font-size:12px;
                        letter-spacing:2px;">
                YOUR JOURNEY STARTS HERE ✦
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # QUICK HIGHLIGHT STRIP
    st.markdown("""
    <div style="
        display:flex;
        flex-wrap:wrap;
        gap:12px;
        justify-content:space-between;
        background:rgba(30,41,80,0.48);
        border:1px solid rgba(148,163,184,0.18);
        border-radius:16px;
        padding:20px;
    ">
        <div>🧠 <b>Skill-based exploration</b></div>
        <div>🎯 <b>Personalized experience</b></div>
        <div>💡 <b>Career explanations</b></div>
        <div>📥 <b>Downloadable report</b></div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # INTERACTIVE CAREER EXPLORER
    st.markdown(
        '<div class="section-heading">Explore Your Possibilities</div>'
        '<div class="muted">Choose an area that catches your interest.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    career_cards = [
        (
            "📊",
            "Data & Analytics",
            "Explore insights, patterns, reporting, and data-driven decisions.",
            "Data Analyst"
        ),
        (
            "🤖",
            "AI & Intelligence",
            "Explore machine learning, intelligent systems, and automation.",
            "Data Scientist"
        ),
        (
            "💻",
            "Software & Development",
            "Explore programming, application development, and problem-solving.",
            "Software Developer"
        ),
        (
            "📈",
            "Business & Strategy",
            "Explore business problems, communication, and analysis.",
            "Business Analyst"
        ),
        (
            "🎨",
            "Design & Creativity",
            "Explore visual thinking and user-friendly digital experiences.",
            "UI UX Designer"
        ),
        (
            "🚀",
            "Digital & Innovation",
            "Explore creativity, communication, and digital opportunities.",
            "Digital Marketer"
        )
    ]

    columns = st.columns(3)

    for i, (emoji, title, description, career) in enumerate(career_cards):

        with columns[i % 3]:

            st.markdown(
                f"""
                <div class="career-card">
                    <div class="career-icon">{emoji}</div>
                    <div class="career-title">{title}</div>
                    <div class="career-desc">{description}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                f"Explore {title} →",
                key=f"compass_career_{i}",
                use_container_width=True
            ):
                st.session_state.selected_career = career

    # Display selected career
    selected = st.session_state.get("selected_career")

    if selected:

        st.write("")

        st.markdown(
            f'<div class="section-heading">'
            f'Your selected interest: {selected}</div>',
            unsafe_allow_html=True
        )

        st.write(
            "Great choice! Complete the assessment to explore the "
            "model's career recommendations based on your skill ratings."
        )

        if st.button(
            "Continue with My Assessment →",
            type="primary",
            use_container_width=True
        ):
            st.session_state.page = "profile"
            st.rerun()

    st.write("")
    st.write("")

    # INTERACTIVE SKILL PREVIEW
    st.markdown(
        '<div class="section-heading">A Little Preview of You</div>'
        '<div class="muted">'
        'Try rating a skill and see how the assessment scale works.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    preview_left, preview_right = st.columns([1, 1], gap="large")

    with preview_left:

        preview_skill = st.selectbox(
            "Choose a skill to preview",
            [
                "Python",
                "Mathematics",
                "Communication",
                "Creativity",
                "Business Interest",
                "Design Interest",
                "Problem Solving",
                "Data Analysis"
            ],
            key="compass_preview_skill"
        )

        preview_rating = st.slider(
            "Adjust your self-rating",
            min_value=1,
            max_value=5,
            value=3,
            key="compass_preview_rating"
        )

    with preview_right:

        st.markdown(
            '<div class="step-card">'
            '<div class="step-number">YOUR SKILL SNAPSHOT</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="hero-title" style="font-size:42px;'
            f'margin-top:8px;">{preview_rating}<span '
            f'class="gradient-text">/5</span></div>',
            unsafe_allow_html=True
        )

        preview_messages = {
            1: "A starting point — you can develop this skill further.",
            2: "Building your foundation through practice.",
            3: "A developing skill with room to grow.",
            4: "A strength you rate highly.",
            5: "One of your strongest self-rated skills."
        }

        st.write(f"**{preview_skill}**")
        st.write(preview_messages[preview_rating])
        st.progress(preview_rating / 5)

        st.markdown("</div>", unsafe_allow_html=True)

    st.caption(
        "This preview is for exploration only. It does not affect "
        "your actual model prediction."
    )

    st.write("")
    st.write("")

    # HOW IT WORKS
    st.markdown(
        '<div class="section-heading">Your Journey in 3 Steps</div>'
        '<div class="muted">Simple to begin. Easy to explore.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    step_columns = st.columns(3)

    steps = [
        (
            "01",
            "Create Your Profile",
            "Enter your name and choose your current profession."
        ),
        (
            "02",
            "Discover Your Skills",
            "Rate eight skills based on your own assessment."
        ),
        (
            "03",
            "Explore Your Results",
            "Review the top three predictions and their explanations."
        )
    ]

    for col, (number, title, description) in zip(step_columns, steps):

        with col:
            st.markdown(
                f"""
                <div class="step-card">
                    <div class="step-number">STEP {number}</div>
                    <div class="step-title">{title}</div>
                    <div class="step-desc">{description}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")
    st.write("")

    # FINAL CALL TO ACTION
    st.markdown("""
    <div style="
        background:linear-gradient(120deg,#312e81,#4338ca,#164e63);
        border:1px solid rgba(165,180,252,0.35);
        border-radius:22px;
        padding:30px 20px;
        text-align:center;
    ">
        <div style="font-size:35px;">✨</div>
        <h2 style="color:white;">Ready to Explore What's Possible?</h2>
        <p style="color:#dbeafe;">
            Your next career idea could begin with one small step.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.button(
        "Start My Journey  ✦",
        type="primary",
        use_container_width=True
    ):
        st.session_state.page = "profile"
        st.rerun()

    st.write("")
    st.divider()

    st.markdown(
        '<div style="text-align:center;color:#94a3b8;'
        'font-size:12px;">'
        'CAREER COMPASS · AI CAREER RECOMMENDATION SYSTEM<br>'
        'Built with Python · Scikit-learn · Streamlit'
        '</div>',
        unsafe_allow_html=True
    )
