import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def login_page():
    """Show login/signup page."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: #09090d; }
    #MainMenu, footer, header { visibility: hidden; }
    .auth-container {
        max-width: 420px;
        margin: 0 auto;
        padding: 2rem;
    }
    .auth-logo {
        text-align: center;
        margin-bottom: 2rem;
    }
    .auth-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #a5b4fc 50%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .auth-sub {
        color: #52525b;
        text-align: center;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }
    .stTextInput input {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.09) !important;
        border-radius: 10px !important;
        color: #fff !important;
        padding: 0.8rem 1rem !important;
    }
    .stTextInput input:focus {
        border-color: rgba(99,102,241,0.5) !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
    }
    .stTextInput label { color: #71717a !important; font-size: 0.85rem !important; }
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.7rem !important;
        width: 100% !important;
        transition: all 0.3s !important;
        box-shadow: 0 4px 20px rgba(99,102,241,0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(99,102,241,0.5) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 5px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 8px !important;
        color: #52525b !important;
        font-weight: 500 !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99,102,241,0.15) !important;
        color: #a5b4fc !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Logo + Title
        st.markdown("""
        <div class='auth-logo'>
            <div style='width:56px;height:56px;border-radius:16px;background:linear-gradient(135deg,#6366f1,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:1.8rem;font-weight:900;color:#fff;margin:0 auto 1rem auto;'>◆</div>
        </div>
        <div class='auth-title'>Nexus HQ</div>
        <div class='auth-sub'>Your AI Company Command Center</div>
        """, unsafe_allow_html=True)

        # Login / Signup tabs
        tab1, tab2 = st.tabs(["🔑  Sign In", "✨  Create Account"])

        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="you@example.com", key="login_email")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Sign In →", key="login_btn", use_container_width=True):
                if email and password:
                    try:
                        response = supabase.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })
                        st.session_state.user = response.user
                        st.session_state.access_token = response.session.access_token
                        st.success("✅ Welcome back!")
                        st.rerun()
                    except Exception as e:
                        st.error("❌ Invalid email or password")
                else:
                    st.warning("Please enter email and password")

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            new_email = st.text_input("Email", placeholder="you@example.com", key="signup_email")
            new_password = st.text_input("Password", type="password", placeholder="Min 6 characters", key="signup_password")
            new_name = st.text_input("Your Name", placeholder="Divyansh", key="signup_name")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Create Account →", key="signup_btn", use_container_width=True):
                if new_email and new_password and new_name:
                    if len(new_password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        try:
                            response = supabase.auth.sign_up({
                                "email": new_email,
                                "password": new_password,
                            })
                            st.session_state.user = response.user
                            st.session_state.user_name = new_name
                            st.session_state.access_token = response.session.access_token
                            st.success("✅ Account created! Welcome to Nexus HQ!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Signup failed: {str(e)}")
                else:
                    st.warning("Please fill all fields")

def logout():
    """Log out current user."""
    try:
        supabase.auth.sign_out()
    except:
        pass
    st.session_state.user = None
    st.session_state.access_token = None
    st.rerun()

def get_current_user():
    """Get current logged in user."""
    return st.session_state.get("user", None)