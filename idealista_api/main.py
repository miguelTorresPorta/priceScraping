import config as cfg
import requests

def get_access_token():
    import base64

    auth = "Basic " + (base64.b64encode(bytes(str(cfg.API_CREDENTIALS["api_key"] + ":" + cfg.API_CREDENTIALS["secret"]), "utf-8"))).decode("utf-8")

    headers = {
        "Host": "api.idealista.com",
        "User-Agent": cfg.USER_AGENT,
        "Authorization": auth,
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "read",
    }

    response = requests.post("https://api.idealista.com/oauth/token", headers=headers, data=data)

    if response.status_code == 200:
        print("Access token successfully acquired")
        return (response.json())["access_token"]

    else:
        print("Access token could not be obtained.")
        print("Error:", response.status_code)
     
ACCESS_TOKEN = get_access_token()

################################################################################

headers = {
    "Host": "api.idealista.com",
    "User-Agent": cfg.USER_AGENT,
    "Authorization": "Bearer " + ACCESS_TOKEN,
    "Content-Type": "multipart/form-data",
}

files = {
    "center": (None, "40.430,-3.702"),
    "propertyType": (None, "homes"),
    "distance": (None, "15000"),
    "operation": (None, "sale"),
}

response = requests.post("http://api.idealista.com/3.5/es/search", headers=headers, data=files)

# Test
print(response.status_code)
print(response.text)
print(ACCESS_TOKEN)