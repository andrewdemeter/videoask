import requests

# Assign variables

token = ""
question_id = ""
organization_id = ""

# Set headers for both API calls

headers = {
  "Authorization": f"Bearer {token}",
  "organization-id": f"{organization_id}"
}

# Retrieve media_id

url = f"https://api.videoask.com/questions/{question_id}"

response = requests.request("GET", url, headers=headers)
json_response = response.json()

media_id = json_response["media_id"]

# Retrieve transcription

url = f"https://api.videoask.com/media/{media_id}"

response = requests.request("GET", url, headers=headers)
json_response = response.json()

transcription = json_response["transcription"]
print(transcription)
