import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Access secrets
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Spotify API Token URL
url = "https://accounts.spotify.com/api/token"

# Headers and body for the POST request
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
}

# Sending the POST request
response = requests.post(url, headers=headers, data=data)

# Checking the response status
if response.status_code == 200:
    # Access token
    access_token = response.json().get("access_token")
    print(f"Access Token: {access_token}")
else:
    access_token = ""
    print(f"Error: {response.status_code}")
    print(response.json())

with open("pyspark/token.txt", "w") as file:
    file.write(f"{access_token}")
