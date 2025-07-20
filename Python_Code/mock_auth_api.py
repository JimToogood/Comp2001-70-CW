mock_users = {
    "tim@plymouth.ac.uk": {
        "password": "COMP2001!",
        "role": "admin"
    },
    "grace@plymouth.ac.uk": {
        "password": "ISAD123!",
        "role": "user"
    },
    "ada@plymouth.ac.uk": {
        "password": "insecurePassword",
        "role": "user"
    }
}

def authenticate(email, password):
    user = mock_users.get(email)

    if (user and user["password"] == password):
        return {"email": email, "role": user["role"]}
    
    return None
