import requests
from functools import wraps
from flask import request, jsonify, g


# Decorator function for header_handler
def require_auth(func):
    @wraps(func)
    def header_handler(*args, **kwargs):
        header = request.headers.get("user-credentials")

        if not header:
            return (jsonify({"error": "Missing user credentials"}), 401)     # 401 = Unauthorised status code

        try:
            email, password = header.split("::")
        except ValueError:
            return (jsonify({"error": "Invalid user credentials format"}), 400)     # 400 = Bad Request status code

        output = check_auth_server(email, password)

        if output == "Verified":
            g.current_user_email = email
            return func(*args, **kwargs)
        else:
            return (jsonify({"error": output}), 403)    # 403 = Forbidden status code
    
    return header_handler


def check_auth_server(email, password):
    auth_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

    credentials = {
        "email": email,
        "password": password
    }

    # Connect to auth server
    response = requests.post(auth_url, json=credentials)

    if response.status_code == 200:     # 200 = OK status code
        try:
            json_response = response.json()
            
            # If account is verified
            if json_response == ["Verified", "True"]:
                return "Verified"
            # If account is not verified
            else:
                return "Verification failed"

        except Exception as error:
            return f"Auth server error: {error}"
    else:
        return "Failed to connect to auth server"
