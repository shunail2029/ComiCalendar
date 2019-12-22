import json
import os.path
import requests

def get_access_token():
    token = ''
    creds = None
    if os.path.exists('linecredentials.json'):
        with open('linecredentials.json', 'r') as f:
            creds = json.load(f)

    if not creds:
        print('failed to load linecredentials.json')
        return ''

    API_URL = 'https://api.line.me/v2/oauth/accessToken'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant_type': 'client_credentials',
        'client_id': creds["channel_id"],
        'client_secret': creds["channel_secret"]
    }

    r = requests.post(url=API_URL, data=payload, headers=headers)
    if r.status_code == 200:
        print('got line access token')
        token = r.json()["access_token"]
    else:
        print('failed to get line access token')
    return token

def send_broadcast(access_token, message):
    if not access_token:
        print('cannot send message without access token')
        return

    API_URL = 'https://api.line.me/v2/bot/message/broadcast'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }
    payload = {
        'messages': [
            {
                'type': 'text',
                'text': message
            }
        ]
    }

    r = requests.post(url=API_URL, data=json.dumps(payload), headers=headers)
    if r.status_code == 200:
        print('sent message')
    else:
        print('failed to send message')

if __name__ == "__main__":
    token = get_access_token()
    send_broadcast(token, 'Hello!!')