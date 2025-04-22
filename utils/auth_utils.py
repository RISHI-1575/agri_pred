def login(username, password, role):
    users = {
        "farmer1": {"password": "1234", "role": "farmer"},
        "company1": {"password": "admin", "role": "company"}
    }
    return users.get(username, {}).get("password") == password and users.get(username, {}).get("role") == role