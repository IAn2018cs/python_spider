# coding=utf-8
import requests,flask,json
from bs4 import BeautifulSoup


class SpamInfo(object):
    def __init__(self):
        self.is_mark = False
        self.mark_info = ''
        self.mark_topone = ''
        self.danger_levels = ''


class SpiderNumber(object):
    def __init__(self):
        self.target = 'https://directory.youmail.com/directory/phone/'
        self.headers = {'authority': 'directory.youmail.com',
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    # 判断是否是骚扰电话
    def get_phone_harassment(self, number):
        spam_info = SpamInfo()
        flag = False
        req = requests.get(url=self.target + number, headers=self.headers)
        bf = BeautifulSoup(req.text)
        # 查询该号码的危险等级
        result_item = bf.find('span', class_='safety-rating-text pull-right')
        if result_item:
            spam_info.danger_levels = result_item.text
            flag = True

        # 获取当前电话标记信息
        info = bf.find('h2', class_='phone-display-name')
        if info:
            spam_info.mark_info = info.text

        # 获取标记列表
        list = bf.find('div', class_='caller-name-chart-legend')
        if list:
            flag = True
            spam_info.mark_topone = str(list.text).strip().split('\n')[0]

        spam_info.is_mark = flag

        return spam_info


# if __name__ == '__main__':
#     sn = SpiderNumber()
#     info = sn.get_phone_harassment('8009556600')
#     print('是否标记：', info.is_mark)
#     print('标记信息：' + info.mark_info)
#     print('危险等级：' + info.danger_levels)
#     print('标记最多：' + info.mark_topone)



server = flask.Flask(__name__)
@server.route('/callblocker',methods=['get','post'])
def callblocker():
    number = flask.request.values.get('number')
    if number:
        sn = SpiderNumber()
        info = sn.get_phone_harassment(number)
        return json.dumps(info.__dict__)
    else:
        return json.dumps({'msg':'error'}, ensure_ascii=False)
server.run(port=7777,debug=False,host='0.0.0.0')