import requests
import time
import logging
from alert import alert
from config import SUBDOMAIN, DEVICE_TOKEN, MOBILE_AUTH, REPS

"""
TODO / Brainstorming
Write logs to file
EOD recap
Milestone tracking / incentive tracking
Deliver message via lights? text message? in-app feed message? something else?
"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s]: %(message)s')

# Create a stream handler for console output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Create a file handler for writing logs to a file
file_handler = logging.FileHandler('logs.txt')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def getStats(reps: list):
    stats = {}
    url = f"https://{SUBDOMAIN}.pestroutes.com/resources/mobile/salesroutes/leaderBoards.php"
    params = {
        "deviceToken": DEVICE_TOKEN,
        "mobileAuthentication": MOBILE_AUTH,
        "indicator": "1",
        "accountStatus": "0",
        "teamID": "2",
        "dateHelper": "6"
    }

    try:
        r = requests.get(url, params=params)
        r.raise_for_status()  # Raise an exception for non-2xx status codes
        data = r.json()
        if data['success'] is False: raise(ValueError("Mobile Authentication token has expired"))
        stats = {rep['name']: {'sales': rep['raw'], 'rev': float(rep['helper'].get('soldRevenue', 0))}
                 for rep in data['leaders']
                 if rep['name'] in reps}
    except Exception as e:
        logger.error(msg=f"Error updating stats: {e}")
        return stats  # Return empty stats in case of an error

    return stats

def main(reps: list, delay: int):
    stats = getStats(reps=reps)  # Get initial stats for comparison
    time.sleep(delay)
    while True:
        try:
            newStats = getStats(reps=reps)
        except Exception as e:
            logger.error(msg=f"Error retrieving stats: {e}")
            continue
        if newStats != stats:
            try:
                for rep in newStats:
                    if newStats[rep]['sales'] > stats[rep]['sales']:
                        alert(message=f"{rep} just got a sale, CV of ${newStats[rep]['rev'] - stats[rep]['rev']}",
                                logger=logger)
                        if (newStats[rep]['sales'] % 50) == 0:
                            alert(message=f"{rep} just hit {newStats[rep]['sales']} sales!", logger=logger)
                    elif newStats[rep]['sales'] < stats[rep]['sales']:
                        alert(message=f"{rep} just had a cancel",
                                logger=logger)
                stats = newStats
            except Exception as e:
                logger.error(msg=f"Error checking stats: {e}")
                stats = newStats

        time.sleep(delay)

main(reps=REPS, delay=10)
