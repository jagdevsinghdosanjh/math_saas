import streamlit as st

st.set_page_config(
    page_title="Math Hub – Research‑grade Math Workspace",
    page_icon="🧠",
    layout="wide"
)

# ---------- Custom CSS ----------
st.markdown("""
<style>
body {
    background-color: #050816;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 0rem;
}
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.nav-left {
    display: flex;
    align-items: baseline;
    gap: 0.4rem;
}
.brand-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #ffffff;
}
.brand-sub {
    font-size: 0.8rem;
    color: #9ca3af;
}
.nav-right {
    display: flex;
    gap: 1.5rem;
    font-size: 0.9rem;
    color: #e5e7eb;
}
.nav-link {
    cursor: pointer;
    opacity: 0.85;
}
.nav-link:hover {
    opacity: 1;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: #d1d5db;
    margin-top: 0.6rem;
}
.hero-tag {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 999px;
    font-size: 0.75rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    background: rgba(59,130,246,0.12);
    color: #93c5fd;
    border: 1px solid rgba(59,130,246,0.4);
}
.hero-card {
    background: radial-gradient(circle at top left, #1f2937 0, #020617 55%);
    border-radius: 1.2rem;
    padding: 1.4rem 1.6rem;
    border: 1px solid rgba(148,163,184,0.25);
    box-shadow: 0 18px 45px rgba(15,23,42,0.9);
}
.hero-metric-label {
    font-size: 0.75rem;
    color: #9ca3af;
}
.hero-metric-value {
    font-size: 1.1rem;
    font-weight: 600;
    color: #e5e7eb;
}
.cta-row {
    display: flex;
    gap: 0.8rem;
    margin-top: 1.2rem;
}
.cta-primary {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: #020617 !important;
    font-weight: 600;
}
.cta-secondary {
    border: 1px solid rgba(148,163,184,0.6);
    color: #e5e7eb !important;
    background: transparent;
}
.small-note {
    font-size: 0.75rem;
    color: #9ca3af;
    margin-top: 0.6rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- Top Nav ----------
with st.container():
    st.markdown('<div class="navbar">', unsafe_allow_html=True)
    col_nav_left, col_nav_right = st.columns([2, 3])

    with col_nav_left:
        st.markdown(
            """
            <div class="nav-left">
                <span class="brand-title">Math Hub</span>
                <span class="brand-sub">Research‑grade math workspace</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_nav_right:
        st.markdown(
            """
            <div class="nav-right">
                <span class="nav-link">Pricing</span>
                <span class="nav-link">Features</span>
                <span class="nav-link">Help</span>
                <span class="nav-link">Sign in</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")  # small spacer

# ---------- Hero Section ----------
col_left, col_right = st.columns([1.4, 1.1])

with col_left:
    st.markdown('<span class="hero-tag">For serious learners & educators</span>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">The research‑grade workspace<br>for school & competitive math.</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="hero-subtitle">
        Powered by structured chapter maps, daily math posts, and curated problem sets for Boards & JEE.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="cta-row">', unsafe_allow_html=True)
    col_cta1, col_cta2 = st.columns([1, 1])

    with col_cta1:
        student_click = st.button("Enter as Student", use_container_width=True, type="primary")
    with col_cta2:
        admin_click = st.button("Enter as Admin", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="small-note">No clutter. Just math, progress, and a clear path through your syllabus.</div>',
        unsafe_allow_html=True
    )

with col_right:
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    st.markdown("#### Today in Math Hub")
    st.markdown('<span class="hero-metric-label">Daily math post</span>', unsafe_allow_html=True)
    st.markdown('<div class="hero-metric-value">Vector Algebra · 3 curated problems</div>', unsafe_allow_html=True)
    st.write("")
    st.markdown('<span class="hero-metric-label">Active students</span>', unsafe_allow_html=True)
    st.markdown('<div class="hero-metric-value">128</div>', unsafe_allow_html=True)
    st.write("")
    st.markdown('<span class="hero-metric-label">Chapters mapped</span>', unsafe_allow_html=True)
    st.markdown('<div class="hero-metric-value">42 / 52</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Routing ----------
if "role" not in st.session_state:
    st.session_state.role = None

if student_click:
    st.session_state.role = "student"
if admin_click:
    st.session_state.role = "admin"

if st.session_state.role == "student":
    st.switch_page("pages/student_portal.py")  # adjust path to your file
elif st.session_state.role == "admin":
    st.switch_page("pages/admin_portal.py")    # adjust path to your file
