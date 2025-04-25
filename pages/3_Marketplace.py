import streamlit as st
from utils.auth_utils import login

st.set_page_config(page_title="AgriPredict", layout="wide")

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Login UI
    st.title("🔐 Login to AgriPredict")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.radio("Login as", ["farmer", "company"])
    
    if st.button("Login"):
        if login(username, password, role):
            st.session_state.logged_in = True
            st.session_state.role = role
            st.success("✅ Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid credentials.")
else:
    # After login: show navigation
    st.sidebar.title("📚 Navigation")
    st.sidebar.markdown(f"👤 Logged in as **{st.session_state.role.capitalize()}**")
    selected_page = st.sidebar.radio("Go to", ["Price Prediction", "Marketplace"])

    if selected_page == "Price Prediction":
        st.switch_page("pages/1_Price_Prediction.py")
    elif selected_page == "Marketplace":
        st.switch_page("pages/2_Marketplace.py")
