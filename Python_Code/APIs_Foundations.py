import requests

response = requests.get("https://randomuser.me/api/")
print(f'\n{response.text}\n')
