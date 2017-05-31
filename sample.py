import pandas as pd
import bs4
import urllib.request

link = 'https://www.practo.com/delhi/hospital/sir-ganga-ram-hospital-delhi-old-rajendra-nagar-1?page=1&ajax=true'
page_req = urllib.request.urlopen(link).read()
soup = bs4.BeautifulSoup(page_req, 'lxml')

for tag in soup.find_all('a', {'class':'link grey'}):
    print(tag.text)


# print()

