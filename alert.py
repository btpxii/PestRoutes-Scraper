import requests
import json
from config import WEBHOOK
from datetime import datetime

def discordWebhook(message, logger):
    data = {
        "username": "PestRoutes Monitor",
        "avatar_url": "https://play-lh.googleusercontent.com/4iNHH0LNRGdjJSTT5XJUYPsiIYWDBbessRGVN3pTb5lWAhNOV6KwNe2GJp8IQ8TkpKc",
        "embeds": [{
            "title": message,
            "footer": {"text": f"GitHub: btpxii | [ {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} UTC ]"},
            "color": 0x00af86
        }]
    }
    res = requests.post(WEBHOOK, data=json.dumps(data), headers={"Content-Type": "application/json"})
    if res.status_code != 204:
        logger.error(msg=f"Webhook failed, status code {res.status_code}")

def alert(message, logger):
    discordWebhook(message=message, logger=logger)
    logger.info(msg=message)