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
for i in range (50):
    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN,
    }
    
    files = {
            "country": "es",
            "operation": "sale",
            "propertyType":"homes",
            "center":'40.475897,-3.680078',
            # "center":'40.450494,-3.712827',
            "distance":"15000"
        }
    
    response = requests.post("http://api.idealista.com/3.5/es/search", headers=headers, data=files)
    
    # Test
    print(response.status_code)
    print(response.text)
    print(ACCESS_TOKEN)
    
    import json
    
    y = json.loads(response.text)
    print (y['elementList'][0])
    
    pisos =[]
    
    for item in range (len(y['elementList'])):
    
        flat = (y['elementList'][item])
        if 'parkingSpace' in flat:        
            flat['parkingIncludedInprice'] = flat['parkingSpace']['isParkingSpaceIncludedInPrice']
            flat['parkingSpace'] = flat['parkingSpace']['hasParkingSpace']
        pisos.append(flat)
        
    import csv
    
    
    import pandas as pd
    pisos_df = pd.DataFrame(pisos)
    pisos_df.to_csv('pisosDFJaime.csv', index=False, header=True)
    
    
