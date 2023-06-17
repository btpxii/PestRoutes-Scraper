import requests
import time
import logging
from config import *

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s]: %(message)s',
)

def getStats():
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
    res = requests.get(url, params=params)
    res = res.json()
    for rep in res["leaders"]:
        stats[rep['name']] = {'sales': rep['raw'], 'rev': float(rep['helper']['soldRevenue'])}
    return stats

def main():
    # get initial stats for comparison
    stats = getStats()
    time.sleep(5)

    while True:
        newStats = getStats()
        if newStats != stats:
            for rep in newStats:
                if newStats[rep]['sales'] > stats[rep]['sales']:
                    logging.info(f"{rep} just got a sale, CV of ${newStats[rep]['rev'] - stats[rep]['rev']}")
                elif newStats[rep]['sales'] < stats[rep]['sales']:
                    logging.info(f"{rep} just had a cancel")
            stats = newStats
        time.sleep(5)

main()