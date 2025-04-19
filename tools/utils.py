import requests
from dotenv import load_dotenv
import os

load_dotenv()


URL = 'https://api.telegram.org/bot{}/getUpdates'

def get_telegram_messages(last_message_id = 0):
    messages = []
    params = {
        'offset': last_message_id + 1,
        'timeout': 60  
    }

    response = requests.get(URL.format(os.environ["TELEGRAM_BOT_API_KEY"]), params=params)
    updates = response.json()
    for message in updates['result']:
        if 'message' in message:
            messages.append(message)
    return messages

if __name__=="__main__":
    main()
