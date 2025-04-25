import streamlit as st
from utils.auth_utils import validate_login, register_user

st.set_page_config(page_title="AgriPredict", layout="wide")

# Ensure session state is initialized
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"  # Default to login page

# Page Navigation Logic
def set_page(page_name):
    st.session_state.current_page = page_name

# Login and Sign-Up Page
if st.session_state.current_page == "login":
    st.title("🌱 Welcome to AgriPredict")

    tab1, tab2 = st.tabs(["🔒 Login", "📝 Sign Up"])

    # Login Tab
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        role = st.radio("Login as", ["farmer", "company"], key="login_role")

        if st.button("Login"):
            if validate_login(username, password, role):
                # Update session state and navigate to the main app
                st.session_state.logged_in = True
                st.session_state.role = role
                st.success("✅ Logged in successfully!")
                set_page("main")  # Redirect to the main app page
            else:
                st.error("❌ Invalid credentials. Please check your username, password, and role.")

    # Sign-Up Tab
    with tab2:
        new_username = st.text_input("Choose a Username", key="signup_user")
        new_password = st.text_input("Choose a Password", type="password", key="signup_pass")
        new_role = st.radio("Register as", ["farmer", "company"], key="signup_role")

        if st.button("Sign Up"):
            message = register_user(new_username, new_password, new_role)
            if "🎉" in message:
                st.success(message)
            else:
                st.error(message)

# Main App Page (Post-Login)
elif st.session_state.current_page == "main":
    st.sidebar.title("📚 Navigation")
    st.sidebar.markdown(f"👤 Logged in as **{st.session_state.role.capitalize()}**")
    selected_page = st.sidebar.radio("Go to", ["Price Prediction", "Crop Recommendation", "Marketplace"])

    if st.sidebar.button("Logout"):
        # Reset session state and navigate back to login
        st.session_state.logged_in = False
        st.session_state.role = None
        set_page("login")

    if selected_page == "Price Prediction":
        st.write("Redirecting to Price Prediction...")
    elif selected_page == "Crop Recommendation":
        st.write("Redirecting to Crop Recommendation...")
    elif selected_page == "Marketplace":
        st.write("Redirecting to Marketplace...")
