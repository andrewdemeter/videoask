import json
import requests

# Assign your variables
token = ""
organization_id = ""
file_path = ""  # e.g. /Users/Andrew/Downloads/team.csv

# Create a dictionary that will store emails, folder names, and folder IDs
email_name_id = {}

# Read emails and folder names from the CSV file
file = open(file_path, "r")

# Add each email and folder name to the dictionary
for line in file:
    split_line = line.rstrip("\n").split(",", 2)
    email = split_line[0]
    folder_name = split_line[1]
    email_name_id[email] = [folder_name]

# Set headers for both API calls
headers = {
    "Authorization": f"Bearer {token}",
    "organization-id": f"{organization_id}",
    "content-type": "application/json"
}

# Fetch all folder names and folder IDs from VideoAsk
response = requests.request("GET", "https://api.videoask.com/folders", headers=headers)
json_response = response.json()

# Iterate through each folder and add relevant folder IDs to the dictionary
for folder in json_response["results"]:
    for email, folder_name in email_name_id.items():
        folder_name = str(folder_name)[2:-2]  # Strip list formatting
        if folder_name == folder["name"]:
            email_name_id[email] = [folder["name"], folder["folder_id"]]

# Invite each team member to their corresponding folder
for email, folder in email_name_id.items():
    url = f"https://api.videoask.com/organizations/{organization_id}/invitations"

    payload = json.dumps({
        "email": email,
        "role": "member",
        "permissions": {
            "default": None,
            "folders": {
                folder[1]: "read/write"
            }
        }
    })

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
