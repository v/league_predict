"""
This file builds free_week.csv which contains the champions for each free week.
"""
from bs4 import BeautifulSoup
from dateutil.parser import parse
import requests

def remove_refs(name):
    parts = name.split('[')
    return parts[0]

with open('free_week.csv', 'w') as csv:
    with open('free_week_urls', 'r') as urls:
        for url in urls.readlines():

            r = requests.get(url.strip())
            soup = BeautifulSoup(r.text)

            weeks = soup.find_all('table', cellspacing="5")
            for week in weeks:
                tds = week.find_all('td')

                for td in tds:
                    tables = td.find_all('table')
                    if tables:
                        table_one = tables[0]
                        table_two = tables[1]

                        week_date = table_one.find("th").text.strip()
                        week_date = remove_refs(week_date)
                        week_date_obj = parse(week_date)
                        csv.write("%s" % (week_date_obj.strftime("%Y-%m-%d")))

                        chars = table_two.find_all('span', 'character_icon')
                        for char in chars:
                            csv.write(',"%s"' % (char.span.text))
                        csv.write("\n")
