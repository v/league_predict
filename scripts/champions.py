from bs4 import BeautifulSoup
import requests

r = requests.get('http://www.lolking.net/champions/')

soup = BeautifulSoup(r.text)

table = soup.find('table', 'champion-list')
trs = table.find_all("tr")

for tr in trs:
    data = []
    tds = tr.find_all('td')
    for td in tds:
        data.append(td.text.strip())
    print ','.join(['"%s"' % (item) for item in data])
