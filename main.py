import schedule
import time
from tools.utils import get_telegram_messages


LAST_UPDATE_ID_RECEIVED = 0

def find_me_jobs():
    global LAST_UPDATE_ID_RECEIVED
    messages = get_telegram_messages(LAST_UPDATE_ID_RECEIVED)
    print(messages)
    for message in messages:
        message_obj = message['message']
        LAST_UPDATE_ID_RECEIVED = message['update_id']
        print(LAST_UPDATE_ID_RECEIVED)

schedule.every(5).seconds.do(find_me_jobs)


if __name__=="__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)

