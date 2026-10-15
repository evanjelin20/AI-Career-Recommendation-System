
# --------------------------------------------------
# PROFESSIONAL WELCOME PAGE
# --------------------------------------------------
if st.session_state.page == "welcome":

    st.markdown("""
    <style>
    .welcome-hero {
        background: linear-gradient(135deg, #101a35, #25396a);
        padding: 36px 28px;
        border-radius: 22px;
        border: 1px solid #405582;
        margin-bottom: 24px;
    }
    .welcome-tag {
        color: #7ee7f5;
        letter-spacing: 2px;
        font-size: 12px;
        font-weight: 700;
    }
    .welcome-title {
        color: white;
        font-size: clamp(30px, 4vw, 48px);
        font-weight: 800;
        line-height: 1.15;
        margin: 16px 0;
    }
    .welcome-description {
        color: #d2dcf3;
        font-size: 16px;
        line-height: 1.8;
    }
    .feature-card {
        background: #172441;
        border: 1px solid #354769;
        padding: 20px;
        border-radius: 16px;
        min-height: 165px;
    }
    .feature-card p {
        color: #c4cfe5;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

    # Main hero section
    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        st.markdown("""
        <div class="welcome-hero">
            <div class="welcome-tag">AI-POWERED CAREER EXPLORATION</div>
            <div class="welcome-title">
                Discover Your<br>
                <span style="color:#7ee7f5;">Career Direction.</span>
            </div>
            <p class="welcome-description">
                Your skills are the beginning of your story.
                Discover career possibilities, understand your strengths,
                and take your next step with confidence.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Your future starts with one step")
        st.write(
            "Complete a short profile and skills assessment to explore "
            "career options suggested by our machine-learning model."
        )

        if st.button(
            "🚀  Get Started",
            type="primary",
            use_container_width=True
        ):
            st.session_state.page = "profile"
            st.rerun()

        st.caption("Free career exploration • Simple assessment • Instant results")

    with right:
        # Professional workplace photograph
        st.image(
            "https://images.unsplash.com/photo-1521737711867-e3b97375f902"
            "?auto=format&fit=crop&w=1000&q=85",
            caption="Explore your potential. Build your future.",
            use_container_width=True
        )

        st.markdown("""
        <div style="
            background:#172441;
            padding:18px;
            border-radius:15px;
            border:1px solid #354769;
            margin-top:8px;">
            <div style="color:#7ee7f5;font-weight:700;">
                YOUR PERSONAL CAREER COMPASS
            </div>
            <p style="color:#c4cfe5;line-height:1.7;margin-bottom:0;">
                Start with your strengths. Explore your options.
                Create a direction for your future.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Your journey, simplified")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>01 👤 Your Profile</h3>
            <p>Tell us your name and current role.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>02 🧠 Assessment</h3>
            <p>Rate your skills and strengths honestly.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>03 🎯 Career Results</h3>
            <p>Explore career suggestions and relevant skills.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    st.caption(
        "Note: Recommendations support career exploration; "
        "they do not guarantee employment or career success."
    )
