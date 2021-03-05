import requests
from bs4 import BeautifulSoup

f = open("server_data.txt", "w")
f.write("")
f.close()
f = open("server_data.txt", "a")

def get_max_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    a_tags = soup.find_all('a')
    value1 = -1

    for a_tag in a_tags:

        if a_tag['href'].find('/problemset/page/') != -1:
            value = a_tag['href'][17:]
            value = int(value)
            value1 = max(value,value1)
    return value1

def single_page(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    a_tags = soup.find_all('a')

    megastring = ""
    for a_tag in a_tags:

        if a_tag['href'].find('?tag') != -1:
            megastring = megastring + a_tag['href'][17:] + '/'

        if a_tag['href'].find('submit')!=-1 and len(a_tag['href'])>18:
            megastring = megastring.replace('+', ' ')
            f.write(a_tag['href'][19:])
            f.write("-")
            f.write(megastring)
            f.write("\n")
            megastring=""

url = 'https://codeforces.com/problemset/page/'
url_problemset = 'https://codeforces.com/problemset'

upperlimit = get_max_page(url_problemset)

for i in range(1,upperlimit+1):
    single_page(url + str(i))
    print('getting data', "{0:.2f}".format((i / 68) * 100), '% completed')
    i = i+1

f.close()
