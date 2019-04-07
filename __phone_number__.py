# coding=utf-8
import requests, pymysql, re
from bs4 import BeautifulSoup


class PhoneNumberInfo(object):
    def __init__(self):
        self.state_id = 0
        self.prefix = ''
        self.usage = ''
        self.primary_city = ''
        self.carrier = ''
        self.introduced = ''
        self.area_code = ''


class SpiderNumber(object):
    def __init__(self):
        self.server = 'https://www.allareacodes.com'
        self.target = 'https://www.allareacodes.com/area-code-list.htm'
        self.headers = {'authority': 'www.allareacodes.com',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        # 存放州名
        self.state = []
        # 存放州id
        self.state_id = []
        # 存放区号
        self.area_code = []
        # 存放区号链接
        self.area_code_urls = []
        # 存放位置和时区
        self.location_time = []

    # 保存州信息
    def save_state_database(self, id, state):
        db = pymysql.connect('localhost', 'root', 'chenshuaide', 'phone_info')
        cursor = db.cursor()
        sql = "INSERT INTO phone_number_state(NID, STATE) \
                         VALUES (%s,'%s')" % (id, state)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print('插入数据库失败 id:%s  name:%s' % (id, state))
        db.close()

    # 获取所有州名 和区号链接
    def get_area_code_url(self):
        req = requests.get(url=self.target, headers=self.headers)
        html = req.text
        div_bf = BeautifulSoup(html)
        div = div_bf.find_all('div', class_='col-xs-12 col-md-6')
        # 获取表格
        table_bf = BeautifulSoup(str(div[0]))
        # 获取每一行
        trs = table_bf.find_all('tr')
        i = 0
        id = 0
        for line in trs[1:]:
            tr = BeautifulSoup(str(line))
            tds = tr.find_all('td')
            if len(tds) == 3:
                # 创建州id
                id = i
                state_content = BeautifulSoup(str(tds[0]))
                state_a = state_content.find_all('a')
                # 保存州名字
                self.state.append(state_a[0].string)
                # 保存州id
                self.state_id.append(id)
                # 保存到数据库中
                # self.save_state_database(id, state_a[0].string)
                # 获取区号
                area = BeautifulSoup(str(tds[1]))
                area_a = area.find_all('a')
                self.area_code.append(area_a[0].string)
                self.area_code_urls.append(self.server + area_a[0].get('href'))
                # 获取地区和时区
                self.location_time.append(str(tds[2]).replace('<td>', '').replace('</td>', '').replace('<br/>', ' '))
                # 更新下次的州id
                i += 1
            else:
                # 保存州id
                self.state_id.append(id)
                # 获取区号
                area = BeautifulSoup(str(tds[0]))
                area_a = area.find_all('a')
                self.area_code.append(area_a[0].string)
                self.area_code_urls.append(self.server + area_a[0].get('href'))
                # 获取地区和时区
                self.location_time.append(str(tds[1]).replace('<td>', '').replace('</td>', '').replace('<br/>', ' '))

    # 获取州下的号码信息
    def get_phone_info(self, target, state_id, area_code):
        req = requests.get(url=target, headers=self.headers)
        html = req.text
        bf = BeautifulSoup(html)
        group_items = bf.find_all('div', class_='list-group-item')
        # 声明一个集合 用来保存爬出来的电话信息
        phone_number_infos = []
        for item in group_items:
            phone_number_info = PhoneNumberInfo()
            # 保存州id
            phone_number_info.state_id = state_id
            item_bf = BeautifulSoup(str(item))
            num = item_bf.find('div', class_='col-xs-12 prefix-col1')
            # 匹配出电话号前缀 \d 数字
            search_num = re.search(r'(.*)(\(\d{3}\) \d{3})(-.*)', num.text, re.M | re.I)
            # 存入数据库 Prefix
            phone_number_info.prefix = search_num.group(2)
            # Usage 电话类型
            type = item_bf.find('div', class_='col-xs-12 prefix-col2')
            phone_number_info.usage = str(type.text).strip()
            # Primary City
            city = item_bf.find('div', class_='col-xs-12 prefix-col3')
            phone_number_info.primary_city = str(city.text).strip()
            # Carrier
            carr = item_bf.find('div', class_='col-xs-12 prefix-col4')
            phone_number_info.carrier = str(carr.text).strip().replace("'", "\\'")
            # Introduced 时间
            data = item_bf.find('div', class_='col-xs-12 prefix-col5')
            search_data = re.search(r'(.*)(\d{2}/\d{2}/\d{4})', str(data.text).strip(), re.M | re.I)
            if search_data:
                introduced = search_data.group(2)
            else:
                introduced = ''
            phone_number_info.introduced = introduced

            phone_number_info.area_code = area_code

            phone_number_infos.append(phone_number_info)

        return phone_number_infos

    # 保存到数据库中
    def save_database(self, phone_number_info):
        db = pymysql.connect('localhost', 'root', 'chenshuaide', 'phone_info')
        cursor = db.cursor()
        sql = "INSERT INTO phone_number_area(STATE_ID, \
               PREFIX, USEAGE, PRIMARY_CITY, CARRIER, INTRODUCED, AREA_CODE) \
               VALUES (%s,'%s', '%s',  '%s',  '%s',  '%s','%s')" % \
              (phone_number_info.state_id, phone_number_info.prefix, phone_number_info.usage,
               phone_number_info.primary_city, phone_number_info.carrier, phone_number_info.introduced,
               phone_number_info.area_code)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            print('插入数据库失败%s,  sql:%s' % (phone_number_info.prefix, sql))
        db.close()


if __name__ == '__main__':
    sn = SpiderNumber()
    sn.get_area_code_url()

    print('开始爬取数据\n')
    for i in range(len(sn.area_code_urls)):
        print('\n爬取第%s个，共%s个；当前进度：%2f' % (i, len(sn.area_code_urls), i / len(sn.area_code_urls)))
        # 区号
        print(sn.area_code[i])
        infos = sn.get_phone_info(sn.area_code_urls[i], sn.state_id[i], sn.area_code[i])
        if infos:
            for info in infos:
                sn.save_database(info)
    print('\n爬取结束')
