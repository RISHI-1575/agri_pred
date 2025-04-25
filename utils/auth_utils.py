import pandas as pd

# File path to the user data CSV file
USER_FILE = "data/users.csv"

def load_users():
    """
    Load the users' data from the CSV file.
    Returns a pandas DataFrame of user credentials.
    """
    try:
        return pd.read_csv(USER_FILE)
    except FileNotFoundError:
        # If user file doesn't exist, create an empty DataFrame with required columns
        return pd.DataFrame(columns=["username", "password", "role"])

def save_users(users_df):
    """
    Save the updated users' DataFrame to the CSV file.
    """
    users_df.to_csv(USER_FILE, index=False)

def validate_login(username, password, role):
    """
    Validate user login credentials.
    Returns True if the user is authenticated, otherwise False.
    """
    users = load_users()
    user_match = users[
        (users["username"] == username) &
        (users["password"] == password) &
        (users["role"] == role)
    ]
    return not user_match.empty  # True if match found, False otherwise

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
