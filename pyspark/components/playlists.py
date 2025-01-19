import requests

# Get Access Tpken
with open("pyspark/token.txt", "r") as file:
    access_token = file.readline().strip()

print(access_token)

# Spotify API URL to get current user's playlists
url = "https://api.spotify.com/v1/me/playlists"

# Set up headers with the access token
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Send GET request to fetch playlists
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    playlists = response.json()
    print("Your Playlists:")
    for playlist in playlists['items']:
        print(f"Name: {playlist['name']}, ID: {playlist['id']}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
