import streamlit as st
import csv
import os

st.set_page_config(page_title="AgriPredict", layout="wide")

# Ensure users.csv exists
user_file = "data/users.csv"
if not os.path.exists(user_file):
    os.makedirs("data", exist_ok=True)
    with open(user_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["username", "password", "role"])

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# Login logic
def login(username, password, role):
    try:
        # Load the users.csv file
        with open(user_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username and row["password"] == password and row["role"] == role:
                    return True
        return False
    except Exception as e:
        print("Error during login:", e)  # Debugging: Print any errors
        return False

if not st.session_state.logged_in:
    st.title("🌱 Welcome to AgriPredict")

    tab1, tab2 = st.tabs(["🔒 Login", "📝 Sign Up"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        role = st.radio("Login as", ["farmer", "company"], key="login_role")

        if st.button("Login"):
            if login(username, password, role):
                st.session_state.logged_in = True
                st.session_state.role = role
                st.success("✅ Logged in successfully!")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid credentials. Please check your username, password, and role.")

    with tab2:
        new_username = st.text_input("Choose a Username", key="signup_user")
        new_password = st.text_input("Choose a Password", type="password", key="signup_pass")
        new_role = st.radio("Register as", ["farmer", "company"], key="signup_role")

        if st.button("Sign Up"):
            try:
                if not new_username or not new_password:
                    st.error("⚠️ Please fill in all fields.")
                else:
                    with open(user_file, mode="r") as file:
                        reader = csv.DictReader(file)
                        if any(row["username"] == new_username for row in reader):
                            st.error("⚠️ Username already exists. Please choose another.")
                            return

                    with open(user_file, mode="a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([new_username, new_password, new_role])
                    st.success("🎉 Account created! You can now log in.")
            except Exception as e:
                st.error(f"⚠️ Error during sign-up: {e}")
else:
    # After login: show navigation
    st.sidebar.title("📚 Navigation")
    st.sidebar.markdown(f"👤 Logged in as **{st.session_state.role.capitalize()}**")
    selected_page = st.sidebar.radio("Go to", ["Price Prediction", "Marketplace"])

    if selected_page == "Price Prediction":
        st.experimental_set_query_params(page="1_Price_Prediction")
        st.write("🚧 Redirecting to Price Prediction...")
        st.experimental_rerun()

    elif selected_page == "Marketplace":
        st.experimental_set_query_params(page="2_Marketplace")
        st.write("🚧 Redirecting to Marketplace...")
        st.experimental_rerun()

# Protect other pages (e.g., Price Prediction and Marketplace)
if "page" in st.query_params:
    page = st.query_params["page"][0]
    if not st.session_state.logged_in:
        st.error("❌ You must be logged in to access this page.")
    elif page == "1_Price_Prediction":
        # Price Prediction Page Code
        st.title("📈 Price Prediction")
        st.write("Welcome to the price prediction page.")
    elif page == "2_Marketplace":
        # Marketplace Page Code
        st.title("🛒 Marketplace")
        st.write("Welcome to the marketplace page.")
