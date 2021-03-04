from bs4 import BeautifulSoup
import requests

Dict = {}

def single_page(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    a_tags = soup.find_all('a')

    megastring = ""
    for a_tag in a_tags:

        if a_tag['href'].find('?tag') != -1:
            megastring = megastring + a_tag['href'][17:] + '/'

        if a_tag['href'].find('submit')!=-1 and len(a_tag['href'])>18:
            #print(a_tag['href'][19:], megastring)
            Dict[a_tag['href'][19:]] = megastring
            megastring=""


def solved_problem_tags(url):
    Dict2 = {}
    req2 = requests.get(url)
    soup2 = BeautifulSoup(req2.text, 'html.parser')
    a_tags = soup2.find_all('a')

    for a_tag in a_tags:
        try:
            if a_tag['href'].find('/contest/') != -1 and a_tag['href'].find('submission') == -1 and a_tag['href'].find(
                    'standings') == -1:
                if a_tag['href'] in Dict2:
                    continue
                Dict2[a_tag['href']] = 1
                final_tag = a_tag['href'][9:].replace('problem/', '')
                #print(final_tag)
                if final_tag in Dict:
                    print(final_tag,Dict[final_tag])
        except:
            pass

def get_user_submission_last_page(url,username):
    r=requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a')
    value1=-1
    for link in links:
        try:
            if link['href'].find('/submissions/')!=-1 and link['href'].find('/page')!=-1:
                link1 = link['href'].replace('/submissions/','')
                link1 = link1.replace(username,'')
                link1 = link1.replace('/page/','')

                value = int(link1)
                value1 = max(value1,value)
        except:
            pass
    return value1


url = 'https://codeforces.com/problemset/page/'

print('Enter Username')
username=input()
user_url='https://codeforces.com/submissions/'
user_url1 = user_url + username + '/page/1'
user_url = user_url + username

#to get data from server
for i in range(1,69):
    single_page(url + str(i))
    print('getting data', (i / 68) * 100, '% completed')
    i = i+1

"""
#to check Main Dictionary for all entries
kar = input() 
while kar != 'x':
    kar = input()
    if kar in Dict:
        print(Dict[kar])
    else:
        print("NO")"""


#to get last page number
value = get_user_submission_last_page(user_url1, username)
print(value)

#to get user data

solved_problem_tags(user_url) #to get data of first page
user_url = user_url + '/page/'

for i in range(2, value+1):
    solved_problem_tags(user_url + str(i))
    print('getting user data', (i / value) * 100, '% completed')
    i = i+1
