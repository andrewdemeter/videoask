import requests
from flask import Flask, request

# Assign variables
client_id = ""
client_secret = ""

scope = "openid%20profile%20email%20offline_access"
callback_url = ""  # e.g. https://example.com/success
authentication_url = f"https://auth.videoask.com/authorize?response_type=code&audience=https://api.videoask.com/&client_id={client_id}&scope={scope}&redirect_uri={callback_url}"

# Create Flask app
app = Flask(__name__)


# Create login page
@app.route("/login")
def login():
    return f"<a href=\"{authentication_url}\">Log in to VideoAsk</a>"


# Create success page
@app.route("/success")
def success():

    # Fetch authorization code from URL
    code = request.args.get("code")

    url = "https://auth.videoask.com/oauth/token"

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": callback_url
    }

    # Use authorization code to generate access and refresh tokens
    response = requests.request("POST", url, data=payload)
    json_response = response.json()

    access_token = json_response["access_token"]
    refresh_token = json_response["refresh_token"]

    return f"<p>Your access token is {access_token}<br><br>Your refresh token is {refresh_token}</p>"


# Run the Flask app
if __name__ == "__main__":
    app.run()
