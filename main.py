import requests
from dotenv import load_dotenv
import os

load_dotenv()


URL = 'https://api.telegram.org/bot{}/getUpdates'

def main():
    response = requests.get(URL.format(os.environ["TELEGRAM_BOT_API_KEY"]))
    updates = response.json()
    for message in updates['result']:
        if 'message' in message:
            mess = message['message']
            print(mess)

if __name__=="__main__":
    main()
