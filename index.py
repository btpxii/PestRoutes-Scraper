import requests
import json
from config import *

def getStats():
    url = f"https://{SUBDOMAIN}.pestroutes.com/resources/mobile/salesroutes/leaderBoards.php"
    params = {
        "deviceToken": DEVICE_TOKEN,
        "mobileAuthentication": MOBILE_AUTH,
        "subdomain": SUBDOMAIN,
        "platform": "iOS",
        "version": "2.77",
        "devicePlatform": "iOS",
        "deviceVersion": "16.5",
        "deviceModel": "iPhone14,5",
        "appName": "salesroutes",
        "indicator": "1",
        "accountStatus": "0",
        "leaderID": "0",
        "teamID": "2",
        "officeID": "1"
    }

    res = requests.get(url, params=params)
    res = res.json()
    for rep in res["leaders"]:
        print(f"{rep['name']}: {rep['raw']}")