import streamlit as st
from database import DatabaseHandler


def show_login_page(db_handler: DatabaseHandler):
    """
    Display login page
    
    Args:
        db_handler: Database handler instance
    """
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1>🤖 Aurion AI Assistant</h1>
        <h3>Login to Continue</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            login_button = st.form_submit_button("🔐 Login", use_container_width=True)
        
        if login_button:
            if email and password:
                with st.spinner("Logging in..."):
                    result = db_handler.login_user(email, password)
                    
                    if result['success']:
                        # Store user data in session state
                        st.session_state.authenticated = True
                        st.session_state.user = result['user']
                        st.success(f"✅ Welcome back, {result['user']['name']}!")
                        st.rerun()
                    else:
                        st.error(f"❌ {result['message']}")
            else:
                st.error("⚠️ Please enter both email and password")
    
    # Link to signup
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("📝 Create New Account", use_container_width=True):
            st.session_state.show_signup = True
            st.rerun()


def show_signup_page(db_handler: DatabaseHandler):
    """
    Display signup page
    
    Args:
        db_handler: Database handler instance
    """
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1>🤖 Aurion AI Assistant</h1>
        <h3>Create Your Account</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Signup form
    with st.form("signup_form"):
        name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="At least 6 characters")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            signup_button = st.form_submit_button("✅ Sign Up", use_container_width=True)
        
        if signup_button:
            # Validate inputs
            if not name or not email or not password or not confirm_password:
                st.error("⚠️ All fields are required")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            elif len(password) < 6:
                st.error("⚠️ Password must be at least 6 characters")
            else:
                with st.spinner("Creating account..."):
                    result = db_handler.register_user(name, email, password)
                    
                    if result['success']:
                        st.success("✅ Account created successfully! Please login.")
                        st.session_state.show_signup = False
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ {result['message']}")
    
    # Link back to login
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔙 Back to Login", use_container_width=True):
            st.session_state.show_signup = False
            st.rerun()


def show_profile_sidebar(db_handler: DatabaseHandler):
    """
    Display user profile in sidebar
    
    Args:
        db_handler: Database handler instance
    """
    if 'user' in st.session_state and st.session_state.user:
        user = st.session_state.user
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 👤 User Profile")
        st.sidebar.markdown(f"**Name:** {user['name']}")
        st.sidebar.markdown(f"**Email:** {user['email']}")
        
        st.sidebar.markdown("---")
        
        # Logout button
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            # Clear session state
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.current_conversation_id = None
            st.success("Logged out successfully!")
            st.rerun()


def check_authentication():
    """
    Check if user is authenticated
    
    Returns:
        bool: True if authenticated, False otherwise
    """
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    return st.session_state.authenticated


def initialize_auth_state():
    """Initialize authentication-related session state"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False