import requests
import json
from config import WEBHOOK

def discordWebhook(message, timestamp, logger):
    data = {
        "username": "PestRoutes Monitor",
        "avatar_url": "https://food.fnr.sndimg.com/content/dam/images/food/fullset/2022/02/16/0/FNM_030122-Homemade-Bagels_s4x3.jpg",
        "embeds": [{
            "title": message,
            "footer": {"text": f"GitHub: btpxii | [ {timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} UTC ]"},
        }]
    }
    res = requests.post(WEBHOOK, data=json.dumps(data), headers={"Content-Type": "application/json"})
    if res.status_code != 204:
        logger.error(msg=f"Webhook failed, status code {res.status_code}")