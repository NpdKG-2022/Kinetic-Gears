import streamlit as st
import base64
import random

# --- Page Configuration ---
st.set_page_config(
    page_title="Kinetic Gears", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Helper Function: Load Background & Logo Images ---
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

IMG_FILENAME = "background_login.png" 
LOGO_FILENAME = "KG-Logo.png"

img_base64 = get_base64_of_bin_file(IMG_FILENAME)
logo_base64 = get_base64_of_bin_file(LOGO_FILENAME)

if not img_base64:
    st.error(f"Error: Required background image '{IMG_FILENAME}' not found in your GitHub repository.")
    st.stop()

st.markdown(
    f"""
    <style>
    /* 1. Full-screen background image setup */
    .stApp {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* 2. Hide default Streamlit headers */
    [data-testid="stHeader"], [data-testid="stFooter"] {{
        visibility: hidden;
        height: 0%;
        position: fixed;
    }}

    /* 3. Transparent login container without background card or borders */
    .login-container {{
        background: transparent !important;
        padding: 1.5rem;
        width: 100%;
        max-width: 480px;
        margin: 0 auto;
    }}

    /* 4. Customizing text input fields to mimic clean bordered design */
    .stTextInput > div > div > input {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        color: #0F172A !important;
        padding: 0.6rem 1rem !important;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: #0284C7 !important;
        box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.2) !important;
    }}

    /* 5. Customizing the Login Submit Button */
    .stButton > button {{
        width: 100%;
        background: linear-gradient(180deg, #004080 0%, #002244 100%) !important;
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        padding: 0.7rem 1rem !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0, 34, 68, 0.3) !important;
        transition: all 0.2s ease-in-out;
    }}
    .stButton > button:hover {{
        background: linear-gradient(180deg, #0059b3 0%, #003366 100%) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Authentication Logic ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def check_login():
    valid_user = st.secrets.get("ADMIN_USER", "admin")
    valid_pass = st.secrets.get("ADMIN_PASSWORD", "admin1234")

    # Validate CAPTCHA
    try:
        user_captcha_ans = int(st.session_state.get("captcha_input", "").strip())
    except ValueError:
        user_captcha_ans = -99999

    if user_captcha_ans != st.session_state.get("captcha_ans"):
        st.error("Incorrect CAPTCHA answer.")
        # Reset captcha on failure
        for key in ["captcha_num1", "captcha_num2", "captcha_op", "captcha_ans"]:
            if key in st.session_state:
                del st.session_state[key]
        return
    
    if st.session_state.get("username_input") == valid_user and st.session_state.get("password_input") == valid_pass:
        st.session_state['logged_in'] = True
        # Clear captcha state on successful login
        for key in ["captcha_num1", "captcha_num2", "captcha_op", "captcha_ans"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    else:
        st.error("Invalid User ID or Password.")

# --- Application Views ---
if st.session_state['logged_in']:
    st.markdown("""<style>[data-testid="stHeader"] {visibility: visible; height: auto;}</style>""", unsafe_allow_html=True)
    st.sidebar.markdown("### Kinetic Gears")
    st.sidebar.write(f"Logged in as: **{st.secrets.get('ADMIN_USER', 'admin')}**")
    
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.rerun()

    st.title("Kinetic Gears Dashboard")
    st.success("Successfully logged in.")

else:
    # --- Initialize CAPTCHA state ---
    if "captcha_num1" not in st.session_state:
        op = random.choice(["+", "-", "*", "/"])
        if op == "+":
            n1 = random.randint(10, 99)
            n2 = random.randint(1, 99)
            ans = n1 + n2
        elif op == "-":
            n1 = random.randint(10, 99)
            n2 = random.randint(1, n1)  # ensure non-negative result
            ans = n1 - n2
        elif op == "*":
            n1 = random.randint(2, 9)
            n2 = random.randint(2, 9)
            ans = n1 * n2
        else: # division '/'
            # ensure clean integer division
            n2 = random.randint(2, 9)
            ans = random.randint(2, 9)
            n1 = n2 * ans
        
        st.session_state["captcha_num1"] = n1
        st.session_state["captcha_num2"] = n2
        st.session_state["captcha_op"] = op
        st.session_state["captcha_ans"] = ans
        
    # Vertical spacing to align the transparent form on the right side
    st.write("")
    st.write("")

    # Create layout columns
    col1, col_center, col2 = st.columns([1.25, 1, 0.15])

    with col_center:
        st.markdown('<div class="login-container" style="margin-top: -60px;">', unsafe_allow_html=True)
        
        # Render Logo naturally without circle wrapper or borders
        if logo_base64:
            st.markdown(
                f'<div style="text-align: center; margin-bottom: 10px;"><img src="data:image/png;base64,{logo_base64}" style="width: 150px; height: auto; object-fit: contain;" /></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown('<div style="text-align: center; font-size: 3rem; margin-bottom: 10px;">⚙️</div>', unsafe_allow_html=True)
        
        # Header Titles and Divider
        st.markdown("""
            <div style="text-align: center; margin-bottom: 0.5rem;">
                <div style="font-weight: 800; font-size: 2.0rem; color: #FFFFFF; letter-spacing: 0.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">
                    KINETIC GEARS
                </div>
                <div style="font-size: 1.25rem; color: #E2E8F0; margin-top: 2px; text-shadow: 0 1px 3px rgba(0,0,0,0.5);">
                    Login, Solve Maths and enjoy working !
                </div>
            </div>
            
            <div style="display: flex; align-items: center; text-align: center; color: #CBD5E1; font-weight: 600; font-size: 0.95rem; margin: 1.2rem 0 1.5rem 0;">
                <div style="flex: 1; border-bottom: 1px solid rgba(255,255,255,0.3);"></div>
                <span style="padding: 0 10px;">User Login</span>
                <div style="flex: 1; border-bottom: 1px solid rgba(255,255,255,0.3);"></div>
            </div>
        """, unsafe_allow_html=True)
        
        # Form Container for Inputs
        with st.form("login_form"):
            st.text_input("User ID", key="username_input", placeholder="👤  User ID")
            st.text_input("Password", type="password", key="password_input", placeholder="🔒  Password")

            # --- CAPTCHA Input Field ---
            captcha_label = f"Solve: {st.session_state['captcha_num1']} {st.session_state['captcha_op']} {st.session_state['captcha_num2']} = ?"
            st.text_input(captcha_label, key="captcha_input", placeholder="Enter number answer")
            
            st.write("")
            submit_btn = st.form_submit_button("➔   Let's Work")
            
            if submit_btn:
                check_login()

        st.markdown('</div>', unsafe_allow_html=True)
