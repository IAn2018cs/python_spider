# coding=utf-8
import requests, sys
from bs4 import BeautifulSoup



class downloader(object):
    def __init__(self):
        self.server = 'http://www.biqukan.com'
        self.target = 'http://www.biqukan.com/1_1094/'
        # 存放章名
        self.names = []
        # 存放章节链接
        self.urls = []
        # 章节数
        self.nums = 0

    def get_download_url(self):
        req = requests.get(url=self.target)
        html = req.text
        div_bf = BeautifulSoup(html)
        div = div_bf.find_all('div', class_='listmain')
        a_bf = BeautifulSoup(str(div[0]))
        a = a_bf.find_all('a')
        self.nums = len(a[15:])
        for each in a[15:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))

    def get_content(self, target):
        req = requests.get(url=target)
        html = req.text
        bf = BeautifulSoup(html)
        texts = bf.find_all('div', class_='showtxt')
        if texts:
            texts = texts[0].text.replace('\xa0' * 8, '\n\n')
        else:
            texts = ''
        return texts

    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


if __name__ == '__main__':
    '''
    target = 'http://www.biqukan.com/1_1094/'
    service = 'http://www.biqukan.com'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'host': 'www.biqukan.com',
        'Pragma': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    req = requests.get(url=target, headers=headers, allow_redirects=True)
    # 得到网页结果
    html = req.text
    # 解析出来
    bf = BeautifulSoup(html)
    div = bf.find_all('div', class_='listmain')
    listmain = BeautifulSoup(str(div[0]))
    a = listmain.find_all('a')
    for each in a:
        print(each.string, service + each.get('href'))
    '''

    dl = downloader()
    dl.get_download_url()
    print('《一年永恒》开始下载：')
    for i in range(dl.nums):
        #print(dl.get_content(dl.urls[i]))
        dl.writer(dl.names[i], '一年永恒.txt', dl.get_content(dl.urls[i]))
        sys.stdout.write(" 已下载：%.3f%%" % float(i/dl.nums) + '\r')
        sys.stdout.flush()
    print('《一年永恒》下载完成')