# coding=utf-8
# 文件的写入
# file = open('D:/file.txt', 'w')
# file.write('hello world!')

# 字符串练习
"""
s = 'dasda'
ss = "dasdasd"
sss = '''dasda
dasda
dasd
asd
asd'''
"""
'''
ssss = """sdasdasd
dasd"""

print(s)
print(ss)
print(sss)
print(ssss)
'''
import re

num = 1
string = '1'
num2 = int(string)
print(type(num))
print(num + num2)

words = 'word ' * 3
print(words)

word = 'a long long word'
num = 12
string = 'bang!'
total = string * (len(words) - num)
print(total)

word = 'zhe shi yi ge zi fu chuan jie qu'
newWord = word[0:3] + ' '+word[-2:]
print(newWord)

phone_number = '13300948732'
hiding_phone_number = phone_number.replace(phone_number[:7],'*'*7)
print(hiding_phone_number)
serch = '133'
num_a = '13340241324'
num_b = '19813325874'

print(serch + ' is at ' + str(num_a.find(serch) + 1 ) + ' to '+ str(num_a.find(serch) + len(serch)) + ' of num_a')


search_num = re.search(r'(.*)(\(\d{3}\)) (\d{3})(-.*)', '    (025) 154-   ', re.M | re.I)
print(search_num.group(3))