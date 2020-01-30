import datetime
import re
import requests
from bs4 import BeautifulSoup

from mypackage import *

def update_calendar(event, context):
    # build service of google calendar
    service = mygoogle.build_service()

    # get event list
    events = mygoogle.get_event_list(service)

    now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
    today = str(now.year).zfill(4) + '-' + str(now.month).zfill(2) + '-' + str(now.day).zfill(2)
    message = ''
    remained_events = ''
    updated_events = ''
    new_events = ''
    failed_events = ''

    for event in events:
        event_date = event['start'].get('date')
        event_title = event['summary']
        event_description = event['description']
        comic_title = event_description.split('\n')[1]
        event_id = event['id']

        event_is_vague = False
        event_is_undeclared = False
        if event_title[0] == '?':
            if event_title[1] == '?':
                event_is_undeclared = True
            else:
                event_is_vague = True

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
        release_date = ''
        release_is_vague = False
        release_is_undeclared = False
        text = soup.find(class_='text-success')
        if not text:
            text = soup.find(class_='text-warning')
            if not text:
                text = soup.find(class_='iteminfo lead')
                if not text:
                    print('cannot get any info of ' + comic_title + '.')
                    failed_events += 'cannot get any info of ' + comic_title + '\n'
                    continue
                else:
                    text = text.get_text()
                    if '未定' in text:
                        release_date = str(now.year + 1).zfill(4) + '-' + str(12) + '-' + str(31)
                        release_is_undeclared = True
                    else:
                        print('??? about ' + comic_title)
                        failed_events += '??? about ' + comic_title + '\n'
                        continue
            else:
                release_is_vague = True
        if not release_is_undeclared:
            text = text.get_text()
            s = re.split('[年月日]', text)
            release_date = s[0] + '-' + s[1] + '-' + s[2]

        # check comic name is same as one in web site
        text = soup.find(class_='iteminfo lead')
        text = text.get_text()
        if comic_title not in text:
            print(comic_title + ' is different name from one in web site')
            failed_events += comic_title + ' is different name from one in web site\n'

        # set prefix '?' to title
        if release_is_vague:
            event_title = '?' + event_title.strip('?')
        elif release_is_undeclared:
            event_title = '??' + event_title.strip('?')
        else:
            event_title = event_title.strip('?')

        # check update of release date
        if event_date != release_date:
            if event_date <= today:
                remained_events += event_date + ' ' + event_title.strip('?') + '\n'
                if len([lis for lis in events if event_title.strip('?') == lis['summary'].strip('?')]) == 1:
                    new_event = mygoogle.make_event_body(event_title, release_date, event_description)
                    res = mygoogle.insert_event(service, new_event)
                    if res:
                        print('inserted ' + event_title)
                        new_events += release_date + ' ' + event_title + '\n'
                    else:
                        print('failed to insert ' + event_title)
                        failed_events += 'failed to insert ' + event_title + '\n'
            else:
                new_event = mygoogle.make_event_body(event_title, release_date, event_description)
                res = mygoogle.update_event(service, event_id, new_event)
                if res:
                    print('updated ' + event_title)
                    updated_events += event_date + ' -> ' + release_date + ' ' + event_title + '\n'
                else:
                    print('failed to insert ' + event_title)
                    failed_events += 'failed to update ' + event_title + '\n'
        elif event_is_vague != release_is_vague or event_is_undeclared != release_is_undeclared:
            new_event = mygoogle.make_event_body(event_title, release_date, event_description)
            res = mygoogle.update_event(service, event_id, new_event)
            if res:
                print('updated ' + event_title)
                updated_events += event_date + ' -> ' + release_date + ' ' + event_title + '\n'
            else:
                print('failed to update ' + event_title)
                failed_events += 'failed to update ' + event_title + '\n'

    if remained_events:
        message += '-- まだ買ってないんですか??? --\n' + remained_events
    if updated_events:
        message += '-- updated events --\n' + updated_events
    if new_events:
        message += '-- new events --\n' + new_events
    if failed_events:
        message += '-- failure information --\n' + failed_events.strip('\n')
    if not message:
        message = '【定期】今日も順調ですね！！'

    myline.send_message(message.strip('\n'))

if __name__ == "__main__":
    update_calendar()
