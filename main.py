import requests
from bs4 import BeautifulSoup
import re
import csv

url = 'https://store.steampowered.com/search/?filter=topsellers&page='
max_pages = 1
games_data = []

file = open('export_data2.csv', 'w', newline='')
writer = csv.writer(file)
headers = ['Name', 'Price', 'Reviews', 'Popularity', 'Developer', 'Genres', 'Critics score', 'OS', 'Processor',
           'Memory', 'Graphics', 'DirectX',
           'Network', 'Storage']
writer.writerow(headers)


def get_sys_req(regex):
    try:
        variable = re.findall(regex, sys_req)[0]
    except IndexError:
        variable = None
    return variable


for page in range(1, max_pages + 1):
    r = requests.get(url + str(page))
    soup = BeautifulSoup(r.content, 'html.parser')
    games = soup.select(".search_result_row, .ds_collapse_flag, .app_impression_tracked")

    for game in games:
        name = game.find('span', {'class': 'title'}).text
        price = int(re.findall(r'(\d*).*', game.find("div", {"class": "search_price"}).text.strip())[0] or 0)
        game_url = game.get("href")
        r2 = requests.get(game_url)
        soup2 = BeautifulSoup(r2.content, 'html.parser')
        try:
            reviews = re.match(r'(.*)', soup2.find('div', {'class': 'summary column'}).text.strip()).group(0)
        except:
            reviews = None
        try:
            popularity = int(''.join(re.findall(r'.*%\D*(\S*)\s.*', soup2.find('span', {
                'class': 'nonresponsive_hidden responsive_reviewdesc'}).text.strip())[0].split(',')))
        except (IndexError, AttributeError):
            popularity = None

        try:
            developer = soup2.find('div', {'id': 'developers_list'}).text.strip()
        except AttributeError:
            developer = None

        try:
            genres = soup2.find('span', {'data-panel': '{"flow-children":"row"}'}).text
        except AttributeError:
            genres = None

        try:
            critics_score = int(
                re.findall(r'(\d*).*', soup2.find('div', {'id': 'game_area_metascore'}).text.strip())[0])
        except:
            critics_score = None

        sys_req = str(soup2.find('div', {'class': 'game_area_sys_req sysreq_content active'}))

        try:
            os1 = (re.findall(r'.*OS:<\/strong>([^<]*).*', sys_req)[0]).replace('/', ' Windows')
            os1 = os1.replace('®', '')
            os1 = os1.replace(' ', '')
            os = re.findall(r'(7|8|8.1|10|Vista|XP)', os1)
            for a in range(len(os)):
                os[a] = 'Windows ' + os[a]
        except IndexError:
            os = None
        try:
            proc = re.findall(r'.*Processor:<\/strong>([^<]*).*', sys_req)[0]
            proc = proc.replace('/', ',')
            proc = proc.replace('®', '')
            proc = proc.replace('™', '')
            proc = proc.replace('|', '')
            proc = proc.lower()
            proc = proc.replace('intel core ', 'intel ')
            # print(proc)
            proc = re.findall(
                r'(intel( \w?\d\d\d\d?)?( atom \S*)?( aubrey isle)?( celeron \S*)?(( 2)? ((duo)|(extreme)|(quad)|(solo ulv)) \S*)?( i\S*)?(( mobile)? pentium \S*( \S*)?)?( xeon \S*)?).*(amd(( mobile)? athlon( 64)?( ii)?( x\d)?( dual core)?( xp)?(-m)? \S*)?( epyc \S*)?( opteron( x2)?)?( phenom( ii)?( x\d)?)?( pro)?( ryzen( \d)?( \w*)?)?( sempron)?( turion( x2)?( \d\d)?)?( \w\S*)?)',
                proc)
            # print(proc)
            proc = proc[0][0] + ", " + proc[0][17]
            # print(proc)
            # proc = re.findall(r'(intel i\d(-\d\d\d\d)?)', proc)[0][0] + re.findall(r'(amd (fx-\d\d\d\d)?phenom( x\d)?( \d\d\d\d)?)', proc)[0][0]
        except IndexError:
            proc = None

        try:
            proc = re.sub(r'\sor\s.*', '', proc)
        except TypeError:
            proc = None

        try:
            graphics = re.findall(r'.*Graphics:<\/strong>([^<]*).*', sys_req)[0]
            graphics = graphics.replace('/', ',')
        except IndexError:
            graphics = None

        try:
            graphics = re.sub(r'\sor\s.*', '', graphics)
        except TypeError:
            graphics = None

        memory = get_sys_req(r'.*Memory:<\/strong>([^<]*).*')

        file = open('export_data2.csv', 'a', newline='', encoding='utf-8')
        writer = csv.writer(file)
        headers = (
            [name, price, reviews, popularity, developer, genres, critics_score, os, proc, memory,
             # getsysreq(r'.*Processor:<\/strong>([^<]*).*'),
             # re.sub(r'\sor\s.*', '', getsysreq(r'.*Processor:<\/strong>([^<]*).*')),
             # getsysreq(r'.*Memory:<\/strong>([^<]*).*'),
             # getsysreq(r'.*Graphics:<\/strong>([^<]*).*'),
             graphics,
             get_sys_req(r'.*DirectX:<\/strong>([^<]*).*'),
             get_sys_req(r'.*Network:<\/strong>([^<]*).*'),
             get_sys_req(r'.*Storage:<\/strong>([^<]*).*')])
        writer.writerow(headers)
        file.close()
