import pandas as pd
import os

# File path to the user data CSV file
USER_FILE = "data/users.csv"

def load_users():
    """
    Load the users' data from the CSV file.
    Returns a pandas DataFrame of user credentials.
    """
    try:
        # Check if the file exists
        if not os.path.exists(USER_FILE):
            # Create an empty DataFrame with required columns if file doesn't exist
            users_df = pd.DataFrame(columns=["username", "password", "role"])
            users_df.to_csv(USER_FILE, index=False)
        else:
            # Load the existing user data
            users_df = pd.read_csv(USER_FILE)
        return users_df
    except Exception as e:
        print("Error loading users:", e)
        return pd.DataFrame(columns=["username", "password", "role"])

def save_users(users_df):
    """
    Save the updated users' DataFrame to the CSV file.
    """
    try:
        users_df.to_csv(USER_FILE, index=False)
    except Exception as e:
        print("Error saving users:", e)

def validate_login(username, password, role):
    """
    Validate user login credentials.
    Returns True if the user is authenticated, otherwise False.
    """
    users = load_users()
    print("DEBUG: Loaded users data:")
    print(users)
    print(f"DEBUG: Attempting login with - Username: {username}, Password: {password}, Role: {role}")
    
    user_match = users[
        (users["username"] == username) &
        (users["password"] == password) &
        (users["role"] == role)
    ]
    
    if not user_match.empty:
        print("DEBUG: Login successful!")
        return True
    else:
        print("DEBUG: Login failed.")
        return False

def register_user(username, password, role):
    """
    Register a new user.
    Returns a message indicating success or failure.
    """
    users = load_users()

    if username in users["username"].values:
        return "⚠️ Username already exists. Please choose another."
    elif not username or not password:
        return "⚠️ Please fill in all fields."
    else:
        new_entry = pd.DataFrame([[username, password, role]], columns=["username", "password", "role"])
        users = pd.concat([users, new_entry], ignore_index=True)
        save_users(users)
        return "🎉 Account created! You can now log in."
