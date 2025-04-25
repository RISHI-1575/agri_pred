import streamlit as st
from utils.auth_utils import validate_login, register_user
from utils.price_prediction import get_price_prediction
from utils.crop_recommendation import recommend_crops
from utils.marketplace import get_marketplace_items

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

# Access Control
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
            if validate_login(username, password, role):
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
            message = register_user(new_username, new_password, new_role)
            if "🎉" in message:
                st.success(message)
            else:
                st.error(message)

else:
    # Main App Page (Post-Login)
    st.sidebar.title("📚 Navigation")
    st.sidebar.markdown(f"👤 Logged in as **{st.session_state.role.capitalize()}**")

    # Sidebar Navigation
    selected_page = st.sidebar.radio(
        "Go to",
        ["Price Prediction", "Crop Recommendation", "Marketplace"],
        key="navigation"
    )

    # Logout Button
    if st.sidebar.button("Logout"):
        # Reset session state and navigate back to login
        st.session_state.logged_in = False
        st.session_state.role = None
        set_page("login")

    # Main Content Based on Navigation
    if selected_page == "Price Prediction":
        st.title("📈 Crop Price Prediction")
        # Crop Price Prediction Logic
        crop = st.selectbox("Select Crop", ["Wheat", "Rice", "Maize"])
        city = st.text_input("Enter City")
        if st.button("Predict Price"):
            if crop and city:
                prediction = get_price_prediction(crop, city)
                st.success(f"The predicted price for {crop} in {city} is ₹{prediction}/kg.")
            else:
                st.error("Please enter both crop and city.")

    elif selected_page == "Crop Recommendation":
        st.title("🌾 Crop Recommendation")
        # Crop Recommendation Logic
        soil_type = st.selectbox("Select Soil Type", ["Clay", "Sandy", "Silt", "Loam"])
        rainfall = st.number_input("Enter Average Rainfall (mm)", min_value=0)
        if st.button("Recommend Crops"):
            if soil_type and rainfall:
                recommendations = recommend_crops(soil_type, rainfall)
                st.success(f"Recommended crops for {soil_type} soil and {rainfall}mm rainfall: {', '.join(recommendations)}")
            else:
                st.error("Please enter valid soil type and rainfall.")

    elif selected_page == "Marketplace":
        st.title("🛒 Marketplace")
        # Marketplace Logic
        items = get_marketplace_items()
        if items:
            for item in items:
                st.write(f"**{item['name']}** - ₹{item['price']}/kg")
                st.write(f"Seller: {item['seller']}")
        else:
            st.info("No items available in the marketplace.")
