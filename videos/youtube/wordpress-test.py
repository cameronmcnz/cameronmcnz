import requests
from requests.auth import HTTPBasicAuth

BASE = "https://itknowledgeexchange.techtarget.com/wp-json/wp/v2"
USER = "Cameron McKenzie"
APP_PASSWORD = "app-password"

# who am I?
r = requests.get(f"{BASE}/users/me", auth=HTTPBasicAuth(USER, APP_PASSWORD))
print("me:", r.status_code, r.json() if r.ok else r.text)

# create draft post
payload = {
    "title": "API test post",
    "content": "Hello from the API",
    "status": "draft"
}
r = requests.post(f"{BASE}/posts", json=payload, auth=HTTPBasicAuth(USER, APP_PASSWORD))
print("create:", r.status_code, r.json() if r.ok else r.text)
