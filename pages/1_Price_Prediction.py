import streamlit as st
import os

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
    """
    Updates session state to navigate to the specified page.
    """
    st.session_state.current_page = page_name

# Restrict Access to Pages
if not st.session_state.logged_in:
    # Login and Sign-Up Page
    st.title("🌱 Welcome to AgriPredict")

    tab1, tab2 = st.tabs(["🔒 Login", "📝 Sign Up"])

    # Login Tab
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        role = st.radio("Login as", ["farmer", "company"], key="login_role")

        if st.button("Login"):
            # Mock validation (replace with real validation)
            if username == "user" and password == "pass":
                # Update session state and navigate to the main app
                st.session_state.logged_in = True
                st.session_state.role = role
                st.success("✅ Logged in successfully!")
                set_page("main")  # Navigate to the main page
            else:
                st.error("❌ Invalid credentials. Please check your username, password, and role.")

    # Sign-Up Tab
    with tab2:
        new_username = st.text_input("Choose a Username", key="signup_user")
        new_password = st.text_input("Choose a Password", type="password", key="signup_pass")
        new_role = st.radio("Register as", ["farmer", "company"], key="signup_role")

        if st.button("Sign Up"):
            # Mock registration logic
            st.success("🎉 Successfully signed up! Please log in to continue.")
else:
    # Main App Page (Post-Login)
    st.sidebar.title("📚 Navigation")
    st.sidebar.markdown(f"👤 Logged in as **{st.session_state.role.capitalize()}**")

    # Sidebar Navigation
    # Dynamically load pages from the `pages` folder
    pages_dir = "pages"
    available_pages = [f for f in os.listdir(pages_dir) if f.endswith(".py") and f != "__init__.py"]
    selected_page = st.sidebar.radio(
        "Go to",
        ["Home"] + [page.replace("_", " ").replace(".py", "") for page in available_pages]
    )

    # Logout Button
    if st.sidebar.button("Logout"):
        # Reset session state and navigate back to login
        st.session_state.logged_in = False
        st.session_state.role = None
        set_page("login")

    # Main Content Based on Navigation
    if selected_page == "Home":
        st.title("Welcome to AgriPredict!")
        st.write("Select a feature from the sidebar to get started.")
    else:
        # Dynamically load the selected page
        page_file = selected_page.replace(" ", "_") + ".py"
        page_path = os.path.join(pages_dir, page_file)
        if os.path.exists(page_path):
            exec(open(page_path).read())
        else:
            st.error("The selected page could not be found.")
