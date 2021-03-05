from bs4 import BeautifulSoup
import requests

problem_count = {}
problems = {}

url = 'https://codeforces.com/problemset/page/'
user_url = 'https://codeforces.com/submissions/'


def load_server_problems():
    f = open("server_data.txt", "r")
    for data in f:
        problem_tag = ''
        tags = ''
        flag = 1
        for c in data:
            if c == '-' and flag == 1:
                flag = 0
            if flag == 1:
                problem_tag = problem_tag + c
            if flag == 0:
                tags = tags + c
        problems[problem_tag] = tags[1:]


def solved_problem_tags(url):
    dict2 = {}
    count_attempted_problems = 0

    req2 = requests.get(url)
    soup2 = BeautifulSoup(req2.text, 'html.parser')
    a_tags = soup2.find_all('a')

    for a_tag in a_tags:
        try:
            if a_tag['href'].find('/contest/') != -1 and a_tag['href'].find('submission') == -1 and a_tag['href'].find(
                    'standings') == -1:
                if a_tag['href'] in dict2:
                    continue
                dict2[a_tag['href']] = 1
                final_tag = a_tag['href'][9:].replace('problem/', '')
                # print(final_tag)
                if final_tag in problems:
                    count_attempted_problems = count_attempted_problems + 1

                    single_tag = ''
                    for ch in problems[final_tag]:
                        if ch == '/':
                            if single_tag in problem_count:
                                problem_count[single_tag] += 1
                            else:
                                problem_count[single_tag] = 1
                            single_tag = ''
                        else:
                            single_tag = single_tag + ch

        except:
            pass
    return count_attempted_problems


def get_user_submission_last_page(url, username):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a')
    value1 = -1
    for link in links:
        try:
            if link['href'].find('/submissions/') != -1 and link['href'].find('/page') != -1:
                link1 = link['href'].replace('/submissions/', '')
                link1 = link1.replace(username, '')
                link1 = link1.replace('/page/', '')

                value = int(link1)
                value1 = max(value1, value)
        except:
            pass
    return value1


# main
load_server_problems()
print('Enter Username')
username = input()
user_url1 = user_url + username + '/page/1'
user_url = user_url + username


# to get last page number
value = get_user_submission_last_page(user_url1, username)

# to get user data
count_attempted_problems = solved_problem_tags(user_url)  # to get data of first page
user_url = user_url + '/page/'
print('getting user data ->', "{0:.2f}".format(abs(1 / value) * 100), '% completed')

for i in range(2, value + 1):
    count_attempted_problems = count_attempted_problems + solved_problem_tags(user_url + str(i))
    print('getting user data ->', "{0:.2f}".format((i / value) * 100), '% completed')
    i = i + 1

print('\nTotal attempted problems: ', count_attempted_problems)
print('')

# to print count
for problem_type in problem_count:
    print(problem_type, '->', problem_count[problem_type])
