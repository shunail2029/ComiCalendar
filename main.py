import datetime
import re
import requests
from bs4 import BeautifulSoup

import mygoogle

def main():
    # build service of google calender
    service = mygoogle.build_service()

    # get event list
    events = mygoogle.get_event_list(service)

    today = str(datetime.date.year).zfill(4) + '-' + str(datetime.date.month).zfill(2) + '-' + str(datetime.date.day).zfill(2)
    message = ''

    for event in events:
        event_date = event['start'].get('date')
        event_title = event['summary']
        event_description = event['description']
        comic_title = event_description.split('\n')[1]

        # skip cirus+
        if event_title == 'citrus+':
            continue

        # get html from url in description
        url = event_description.split('\n')[2]
        r = requests.get(url)
        if not r:
            print('failed to get info from ' + url)

        # parse html
        soup = BeautifulSoup(r.text, 'html.parser')

        # find date in html
        is_vague = False
        text = soup.find(class_='text-success')
        if not text:
            text = soup.find(class_='text-warning')
            if not text:
                text = soup.find(class_='iteminfo lead')
                if not text:
                    print('cannot any info of ' + comic_title + '.')
                else:
                    text = text.get_text()
                    if '未定' in text:
                        print('release date of ' + comic_title + ' is undeclared.')
                    else:
                        print('??? about ' + comic_title)
                continue
            else:
                is_vague = True
        text = text.get_text()
        s = re.split('[年月日]', text)
        release_date = s[0] + '-' + s[1] + '-' + s[2]

        if event_date != release_date:
            print(1)


if __name__ == '__main__':
    main()
