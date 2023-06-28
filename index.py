import requests
import time
import logging
from datetime import datetime
from alert import discordWebhook
from config import SUBDOMAIN, DEVICE_TOKEN, MOBILE_AUTH

"""
TODO / Brainstorming
Error handling
EOD recap
Milestone tracking / incentive tracking
Deliver message via lights? text message? in-app feed message? something else?
"""

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s]: %(message)s',
)

def getStats(reps: list):
    stats = {}
    url = f"https://{SUBDOMAIN}.pestroutes.com/resources/mobile/salesroutes/leaderBoards.php"
    params = {
        "deviceToken": DEVICE_TOKEN,
        "mobileAuthentication": MOBILE_AUTH,
        "indicator": "1",
        "accountStatus": "0", # zero is sold, 1 is serviced
        "teamID": "2",
        "dateHelper": "6" # today: 0, yesterday: 1, this week: 2, last week: 3, this month: 4, last month: 5, this year: 6
    }
    try:
        r = requests.get(url, params=params)
        if r.status_code == 200:
            data = r.json()
            stats = {rep['name']: {'sales': rep['raw'], 'rev': float(rep['helper'].get('soldRevenue', 0))}
                     for rep in data['leaders']
                     if rep['name'] in reps}
                    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error updating stats: {e}")

    return stats

def main(reps: list, delay: int):
    # get initial stats for comparison
    stats = getStats(reps=reps)
    discordWebhook(message="TEST", timestamp=datetime.utcnow(), logger=logging)
    time.sleep(delay)

    while True:
        newStats = getStats(reps=reps)
        if newStats != stats:
            for rep in newStats:
                if newStats[rep]['sales'] > stats[rep]['sales']:
                    message = f"{rep} just got a sale, CV of ${newStats[rep]['rev'] - stats[rep]['rev']}"
                elif newStats[rep]['sales'] < stats[rep]['sales']:
                    message = f"{rep} just had a cancel"
                logging.info(message)
                discordWebhook(message=message, timestamp=datetime.utcnow(), logger=logging)
            stats = newStats

        time.sleep(delay)

main(reps=["Anna Jorgensen", "Sam Jorgensen", "Ellie  Jorgensen", "Charlotte Jorgensen", "Nick Hortin", "Adam  Forsloff ", "Os Hansen"], delay=10)