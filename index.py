import requests
import time
import logging
from alert import alert
from config import SUBDOMAIN, DEVICE_TOKEN, MOBILE_AUTH, REPS

"""
TODO / Brainstorming
Error handling
EOD recap
Milestone tracking / incentive tracking
Deliver message via lights? text message? in-app feed message? something else?
"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s]: %(message)s')
# Create a stream handler for console output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
# Add the console handler to the logger
logger.addHandler(console_handler)


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
        logger.error(msg=f"Error updating stats: {e}")

    return stats

def main(reps: list, delay: int):
    stats = getStats(reps=reps) # get initial stats for comparison
    while True:
        logger.info(msg="Checking for updates...")
        newStats = getStats(reps=reps)
        if newStats != stats:
            for rep in newStats:
                if newStats[rep]['sales'] > stats[rep]['sales']:
                    alert(message=f"{rep} just got a sale, CV of ${newStats[rep]['rev'] - stats[rep]['rev']}",
                          logger=logger)
                elif newStats[rep]['sales'] < stats[rep]['sales']:
                    alert(message=f"{rep} just had a cancel",
                          logger=logger)
            stats = newStats

        time.sleep(delay)

main(reps=REPS, delay=10)