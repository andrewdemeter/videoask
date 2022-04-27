import redis
import requests

redis_host = ""
redis_port = ""
client_id = ""
client_secret = ""
refresh_token = ""

# Connect to Redis
r = redis.Redis(host=redis_host, port=redis_port)

# Check if access token exists in Redis cache
access_token = r.get("access_token")

# If access token exists in cache
if access_token is not None:
    access_token = str(r.get("access_token"), "utf-8")
    print(f"Access token is still valid: {access_token}")

# If access token doesn't exist in cache
else:
    print("Generating new access token...")

    body = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    response = requests.request("POST", "https://auth.videoask.com/oauth/token", data=body)
    json_response = response.json()
    access_token = json_response['access_token']

    # Store new access token in cache for 24 hours (milliseconds equivalent)
    r.psetex("access_token", 86400000, access_token)
    access_token = str(r.get("access_token"), "utf-8")
    print(f"Access token has been added to cache: {access_token}")
    