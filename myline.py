import os
import requests

LINE_ACCESS_TOKEN = os.environ['LINE_ACCESS_TOKEN']

def send_message(message):
    API_URL = 'https://notify-api.line.me/api/notify'
    headers = {
        'Authorization': 'Bearer ' + LINE_ACCESS_TOKEN
    }
    payload = {
        'message': '\n' + message
    }

    r = requests.post(url=API_URL, headers=headers, params=payload)
    if r.status_code == 200:
        print('sent message')
    else:
        print('failed to send message')
