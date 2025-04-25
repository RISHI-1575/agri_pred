import pandas as pd

def login(username, password, role):
    try:
        users = pd.read_csv("data/users.csv")
        user = users[
            (users["username"] == username) &
            (users["password"] == password) &
            (users["role"] == role)
        ]
        return not user.empty
    except:
        return False
