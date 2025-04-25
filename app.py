import streamlit as st
from utils.auth_utils import validate_login, register_user

st.set_page_config(page_title="AgriPredict", layout="wide")

# Ensure session state is initialized
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

st.title("🌱 Welcome to AgriPredict")

if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔒 Login", "📝 Sign Up"])

    # Login Tab
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        role = st.radio("Login as", ["farmer", "company"], key="login_role")

        if st.button("Login"):
            if validate_login(username, password, role):
                # Update session state
                st.session_state.logged_in = True
                st.session_state.role = role
                st.success("✅ Logged in successfully!")

                # Debugging information
                st.write("Session state updated. Rerunning app...")

                # Safely rerun the app
                st.experimental_rerun()
            else:
                st.error("❌ Invalid credentials. Please check your username, password, and role.")

    # Signup Tab
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
else:
    # Sidebar navigation
    st.sidebar.title("📚 Navigation")
    st.sidebar.markdown(f"👤 Logged in as **{st.session_state.role.capitalize()}**")
    selected_page = st.sidebar.radio("Go to", ["Price Prediction", "Crop Recommendation", "Marketplace"])

    # Debugging information
    st.write(f"Session state: {st.session_state}")

    if selected_page == "Price Prediction":
        st.write("Redirecting to Price Prediction...")
    elif selected_page == "Crop Recommendation":
        st.write("Redirecting to Crop Recommendation...")
    elif selected_page == "Marketplace":
        st.write("Redirecting to Marketplace...")
