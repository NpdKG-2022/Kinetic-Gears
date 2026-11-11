import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Kinetic Gears | Login",
    page_icon="⚙️",
    layout="wide"
)

# Custom CSS matching the image layout & styling
st.markdown("""
    <style>
    /* Full height setup & background gradient / split styling */
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Main container flex alignment */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Left Hero / Industrial Branding Section */
    .hero-container {
        padding: 3rem 2rem;
        color: #FFFFFF;
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 0.5rem;
        letter-spacing: 1px;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        color: #94A3B8;
        margin-bottom: 1.5rem;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.1);
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        width: fit-content;
    }

    /* Right Login Card Panel */
    .login-card {
        background-color: #F8FAFC;
        padding: 2.5rem 2rem;
        border-radius: 24px;
        box-shadow: 0px 20px 40px rgba(0, 0, 0, 0.4);
        border: 1px solid #E2E8F0;
        margin-top: 1rem;
    }

    .card-header {
        text-align: center;
        color: #0F172A;
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .card-divider {
        display: flex;
        align-items: center;
        text-align: center;
        color: #64748B;
        font-size: 0.9rem;
        margin: 1rem 0 1.5rem 0;
    }
    .card-divider::before, .card-divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #CBD5E1;
    }
    .card-divider::before { margin-right: .5em; }
    .card-divider::after { margin-left: .5em; }

    /* Customizing Streamlit Input Boxes */
    .stTextInput > div > div > input {
        background-color: #F1F5F9 !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        color: #0F172A !important;
        padding: 0.6rem 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0284C7 !important;
        box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.2) !important;
    }

    /* Primary Submit Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(180deg, #00529B 0%, #003366 100%) !important;
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 0.68rem 1rem !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0, 51, 102, 0.3) !important;
        transition: all 0.2s ease-in-out;
    }
    
    .stButton > button:hover {
        background: linear-gradient(180deg, #0066C0 0%, #004080 100%) !important;
        transform: translateY(-1px);
    }

    /* Links & Options */
    .forgot-link {
        text-align: right;
        font-size: 0.85rem;
        margin-top: -0.5rem;
    }
    .forgot-link a {
        color: #0284C7;
        text-decoration: none;
        font-weight: 500;
    }
    .forgot-link a:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# Authentication state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login_page():
    col1, col2 = st.columns([1.2, 1], gap="large")

    # Left Column - Industrial / Machining Visual Side
    with col1:
        st.markdown("""
            <div class="hero-container">
                <div class="hero-badge">⚙️ High Precision Engineering</div>
                <h1 class="hero-title">Kinetic Gears</h1>
                <p class="hero-subtitle">Machined Components & Industrial Manufacturing Platform</p>
            </div>
        """, unsafe_allow_html=True)

    # Right Column - Styled White Card Form
    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # Logo / Icon Top Header
        st.markdown("""
            <div style="text-align: center; margin-bottom: 0.5rem;">
                <span style="font-size: 3.2rem;">⚙️</span>
                <div style="font-weight: 800; font-size: 1.3rem; color: #003366; tracking: 0.5px;">
                    KINETIC GEARS
                </div>
            </div>
            <div class="card-divider">User Login</div>
        """, unsafe_allow_html=True)

        # Login Form
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("User ID", placeholder="Enter your User ID")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            c1, c2 = st.columns(2)
            with c1:
                remember_me = st.checkbox("Remember Me")
            with c2:
                st.markdown('<div class="forgot-link"><a href="#">Forgot Password?</a></div>', unsafe_allow_html=True)

            submit = st.form_submit_button("➔  Login")

            if submit:
                # Check credentials using secrets or default fallback
                valid_user = st.secrets.get("ADMIN_USER", "admin")
                valid_pass = st.secrets.get("ADMIN_PASSWORD", "gear123")
                
                if username == valid_user and password == valid_pass:
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.rerun()
                else:
                    st.error("Invalid User ID or Password")

        st.markdown('</div>', unsafe_allow_html=True)

def dashboard_page():
    st.sidebar.markdown(f"### ⚙️ Kinetic Gears")
    st.sidebar.write(f"Logged in as: **{st.session_state.get('username')}**")
    
    if st.sidebar.button("Log Out"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.title("Kinetic Gears Dashboard")
    st.success("Successfully logged into the manufacturing management workspace.")

# Render page according to session status
if st.session_state["authenticated"]:
    dashboard_page()
else:
    login_page()
