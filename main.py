import datetime

import mygoogleauth
import myweb

def main():
    # build service of google calender
    service = mygoogleauth.build_service()

    # get comic sales list
    # sales_list = myweb.get_sales_list()

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='3goiblvs1uhkoghhbmt9t8miug@group.calendar.google.com',
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'], event['description'].split('\n')[1])

if __name__ == '__main__':
    main()
