import json
import requests

# Assign variables

api_token = ""
question_id = ""
organization_id = ""
thumbnail_file_path = ""

# Set headers for VideoAsk API calls

videoask_headers = {
    'Authorization': f'Bearer {api_token}',
    'content-type': 'application/json',
    'organization_id': organization_id
}

# Get Media ID of first question

response = requests.request("GET", f"https://api.videoask.com/questions/{question_id}", headers=videoask_headers)
json_response = response.json()
media_id = json_response['media_id']

# Generate thumbnail upload URL

payload = json.dumps({
    'extension': 'jpeg'
})

response = requests.request("POST", f"https://api.videoask.com/media/{media_id}/thumbnail-upload-url", headers=videoask_headers, data=payload)
json_response = response.json()
presigned_thumbnail_url = json_response['presigned_thumbnail_url']
thumbnail_object_key = json_response['thumbnail_object_key']

# Read and upload binary contents of image file

file = open(thumbnail_file_path, "rb")
file_contents = file.read()
file.close()

aws_headers = {
    'content-type': 'image/jpeg'
}

requests.request("PUT", presigned_thumbnail_url, headers=aws_headers, data=file_contents)

# Confirm uploaded thumbnail

payload = json.dumps({
    'thumbnail_object_key': thumbnail_object_key
})

requests.request("POST", f"https://api.videoask.com/media/{media_id}/confirm-thumbnail", headers=videoask_headers, data=payload)