import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Kinetic Gears",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        text-align: center;
        color: #64748B;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #0F172A;
        color: white;
        border-radius: 6px;
        padding: 0.5rem 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize authentication state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def login():
    st.markdown("<h2 class='main-title'>Kinetic Gears</h2>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Client & Internal Portal Access</p>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username / Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Log In")
        
        if submit:
            # Check credentials against Streamlit Secrets
            if username == st.secrets.get("ADMIN_USER", "admin") and password == st.secrets.get("ADMIN_PASSWORD", "gear123"):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("Invalid username or password.")

def dashboard():
    st.sidebar.title(f"Welcome, {st.session_state.get('username', 'User')}")
    if st.sidebar.button("Log Out"):
        st.session_state["authenticated"] = False
        st.rerun()
        
    st.title("Kinetic Gears Dashboard")
    st.write("Welcome to your workspace portal.")
    
    st.info("You are securely authenticated.")

# Render app based on auth status
if st.session_state["authenticated"]:
    dashboard()
else:
    login()
