# coding=utf-8

import requests, pymysql, re
from bs4 import BeautifulSoup


class Loc(object):
    def __init__(self):
        self.loc = ''
        self.des = ''
        self.general_code = ''


def get_wiki_page():
    target = 'https://en.wikipedia.org/wiki/Library_of_Congress_Classification'
    headers = {
        'authority': 'en.wikipedia.org',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'cookie': 'mwPhp7Seed=1b2; PHP_ENGINE=php7; WMF-Last-Access-Global=17-Oct-2019; GeoIP=US:::37.75:-97.82:v4; WMF-Last-Access=17-Oct-2019',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    req = requests.get(url=target, headers=headers)
    # 得到网页结果
    html = req.text
    return html


def parse_general_code(html):
    general_map = {}
    bf = BeautifulSoup(html, features="html.parser")
    tables = bf.find_all('table', class_='wikitable')
    rows = tables[0].find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        if len(tds) < 2:
            continue
        general_map[tds[0].string] = tds[1].find_all('a')[0].string
        print("code : %s" % tds[0].string)
        print("des : %s" % tds[1].find_all('a')[0].string)
    return general_map


def parse_loc_code(html):
    loc_list = []
    bf = BeautifulSoup(html, features="html.parser")
    uls = bf.find_all('ul')
    for ul in uls:
        lis = ul.find_all('li', class_='')
        if len(lis) == 0:
            continue
        for li in lis:
            subclass = re.match(r'^Subclass ([A-Z]{2,}) +– (.+)', li.text)
            if subclass:
                loc = Loc()
                loc.loc = subclass.group(1)
                loc.des = subclass.group(2)
                loc.general_code = subclass.group(1)[0:1]
                print('loc : %s' % loc.loc)
                print('des : %s' % loc.des)
                print('general_code : %s' % loc.general_code)
                loc_list.append(loc)
    return loc_list


def save_general(cursor, code, des):
    sql = "INSERT INTO general_loc_code " \
          "(general_code, des) " \
          "VALUES ('%s', '%s')" % \
          (code, des)
    cursor.execute(sql)


def save_loc(cursor, loc):
    sql = "INSERT INTO loc_code " \
          "(loc, des, general_of) " \
          "VALUES ('%s', '%s', '%s')" % \
          (loc.loc, loc.des, loc.general_code)
    cursor.execute(sql)


def save2db(general_map, loc_list):
    db = pymysql.connect('localhost', 'root', '', 'book')
    cursor = db.cursor()
    for code in general_map:
        save_general(cursor, code, general_map[code])
    for loc in loc_list:
        save_loc(cursor, loc)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print('插入数据库失败%s' % e)
    db.close()


if __name__ == "__main__":
    html = get_wiki_page()
    general_map = parse_general_code(html)
    loc_list = parse_loc_code(html)
    save2db(general_map, loc_list)
