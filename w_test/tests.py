import urllib.request
from bs4 import BeautifulSoup

url = "https://old.reddit.com/top/"
request = urllib.request.Request(url)
html = urllib.request.urlopen(request).read()

soup = BeautifulSoup(html, 'html.parser')
main_table = soup.find("div", attrs={'id': 'siteTable'})
links = main_table.find_all("a", class_="title")

extracted_records = []
for link in links:
    title = link.text
    url = link['href']
    record = {
        'title': title,
        'url': url
    }
    extracted_records.append(record)
print(extracted_records)
