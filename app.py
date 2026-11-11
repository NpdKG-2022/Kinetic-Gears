import streamlit as st
import base64

# --- Page Configuration ---
st.set_page_config(
    page_title="Kinetic Gears Portal | Secure Login", 
    page_icon="⚙️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Helper Function: Convert Local Image to Base64 ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Ensure this matches the exact filename of the image you uploaded to GitHub
IMG_FILENAME = "background_login.png" 

try:
    img_base64 = get_base64_of_bin_file(IMG_FILENAME)
except FileNotFoundError:
    st.error(f"Error: Required background image '{IMG_FILENAME}' not found in your repository.")
    st.stop()

# --- Custom Styling & Layout ---
st.markdown(
    f"""
    <style>
    /* 1. Set the background image on the main container */
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: local;
    }}

    /* 2. Hide default Streamlit Header and Footer */
    [data-testid="stHeader"], [data-testid="stFooter"] {{
        visibility: hidden;
        height: 0%;
        position: fixed;
    }}

    /* 3. Style input fields */
    .stTextInput>div>div>input {{
        color: #0F172A;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 8px;
        border: 1px solid #CBD5E1;
    }}

    /* 4. Login Form Card Wrapper */
    .login-box {{
        background-color: rgba(248, 250, 252, 0.92);
        padding: 35px;
        border-radius: 20px;
        width: 100%;
        max-width: 420px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        border: 1px solid #E2E8F0;
        margin: 0 auto;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Authentication State Management ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def check_login():
    # Use Streamlit Secrets in production for secure authentication
    valid_user = st.secrets.get("ADMIN_USER", "admin")
    valid_pass = st.secrets.get("ADMIN_PASSWORD", "gear123")
    
    if st.session_state.get("username_input") == valid_user and st.session_state.get("password_input") == valid_pass:
        st.session_state['logged_in'] = True
        st.rerun()
    else:
        st.error("Invalid User ID or Password.")

# --- Render Application Views ---
if st.session_state['logged_in']:
    # Restore header visibility for dashboard view
    st.markdown("""<style>[data-testid="stHeader"] {visibility: visible; height: auto;}</style>""", unsafe_allow_html=True)
    
    st.sidebar.markdown("### ⚙️ Kinetic Gears")
    st.sidebar.write(f"Logged in as: **{st.secrets.get('ADMIN_USER', 'admin')}**")
    
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.rerun()

    st.title("Kinetic Gears Dashboard")
    st.success("Successfully logged into the precision manufacturing platform workspace.")

else:
    # Spacer to align the form position vertically with your background image layout
    st.write("")
    st.write("")
    st.write("")

    # Create columns to shift the login card to the right side matching your graphic
    col1, col_center, col2 = st.columns([1.2, 1, 0.3])

    with col_center:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        
        st.markdown("""
            <div style="text-align: center; margin-bottom: 1rem;">
                <span style="font-size: 2.8rem;">⚙️</span>
                <div style="font-weight: 800; font-size: 1.2rem; color: #003366; letter-spacing: 0.5px;">
                    KINETIC GEARS
                </div>
                <div style="font-size: 0.8rem; color: #64748B; margin-top: 2px;">Precision Manufacturing Portal</div>
            </div>
            <div style="border-bottom: 1px solid #CBD5E1; margin-bottom: 1.5rem;"></div>
        """, unsafe_allow_html=True)
        
        # Form inputs
        st.text_input("User ID", key="username_input", placeholder="Enter your User ID")
        st.text_input("Password", type="password", key="password_input", placeholder="Enter your password")
        
        c1, c2 = st.columns(2)
        with c1:
            st.checkbox("REMEMBER ME")
        with c2:
            st.markdown("<div style='text-align: right; font-size: 0.8rem; margin-top: 5px;'><a href='#' style='color: #0284C7; text-decoration: none;'>FORGOT PASSWORD?</a></div>", unsafe_allow_html=True)
        
        st.write("")
        st.button("LOGIN", on_click=check_login, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
