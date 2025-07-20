import requests

auth_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

credentials = {
    "email": "tim@plymouth.ac.uk",
    "password": "COMP2001!"
}

response = requests.post(auth_url, json=credentials)

if response.status_code == 200:
    try:
        json_response = response.json()
        print("\nAuthenticated successfully:", json_response)

    except requests.JSONDecodeError:
        print("\nResponse is not valid JSON. Raw response content:")
        print(response.text)
else:
    print(f"\nAuthentication failed with status code {response.status_code}\n")
    print("Response content:", response.text)
