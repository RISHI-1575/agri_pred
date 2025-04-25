import streamlit as st
import pandas as pd

st.set_page_config(page_title="AgriPredict", layout="wide")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# File paths
user_file = "data/users.csv"

# Login and signup logic
def login(username, password, role):
    try:
        users_df = pd.read_csv(user_file)
        user_match = users_df[
            (users_df["username"] == username) & 
            (users_df["password"] == password) & 
            (users_df["role"] == role)
        ]
        return not user_match.empty
    except Exception as e:
        print("Error during login:", e)
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
                users_df = pd.read_csv(user_file)
                if new_username in users_df["username"].values:
                    st.error("⚠️ Username already exists. Please choose another.")
                elif not new_username or not new_password:
                    st.error("⚠️ Please fill in all fields.")
                else:
                    new_entry = pd.DataFrame([[new_username, new_password, new_role]], columns=["username", "password", "role"])
                    users_df = pd.concat([users_df, new_entry], ignore_index=True)
                    users_df.to_csv(user_file, index=False)
                    st.success("🎉 Account created! You can now log in.")
            except Exception as e:
                st.error(f"⚠️ Error during sign-up: {e}")
else:
    st.sidebar.title("📚 Navigation")
    st.sidebar.markdown(f"👤 Logged in as **{st.session_state.role.capitalize()}**")
    selected_page = st.sidebar.radio("Go to", ["Price Prediction", "Crop Recommendation", "Marketplace"])

    if selected_page == "Price Prediction":
        st.experimental_set_query_params(page="1_Price_Prediction")
        st.experimental_rerun()

    elif selected_page == "Crop Recommendation":
        st.experimental_set_query_params(page="2_Crop_Recommendation")
        st.experimental_rerun()

    elif selected_page == "Marketplace":
        st.experimental_set_query_params(page="3_Marketplace")
        st.experimental_rerun()
