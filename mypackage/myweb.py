import datetime
import re
import requests
from bs4 import BeautifulSoup

current_month_url = 'https://honto.jp/netstore/calender/old.html'
next_month_url = 'https://honto.jp/netstore/calender.html'

# change date format from mm月dd日 to yyyy-mm-dd


def change_date_format(date):
    s = re.split('[月日]', date)
    month = s[0]
    day = s[1]

    now = datetime.datetime.utcnow()
    year = now.year

    if month == '1' and now.month == 12:
        year += 1

    return str(year) + '-' + month.zfill(2) + '-' + day.zfill(2)


def get_sales_list():
    sales_list = []

    for i in range(2):
        url = current_month_url if i == 0 else next_month_url

        # get html
        r = requests.get(url)
        if not r:
            return []

        # parse html
        soup = BeautifulSoup(r.text, 'html.parser')

        # get sales information from tables in html
        book_list = soup.find_all('tr')
        for book in book_list:
            info = book.find_all('td')
            if not info:
                continue
            sales_list.append([change_date_format(
                info[0].get_text()),
                info[1].get_text().replace('\u3000', ' ')])

    return sales_list
