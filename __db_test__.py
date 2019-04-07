# coding=utf-8
import pymysql

# db = pymysql.connect('localhost', 'root', 'chenshuaide', 'test')
# cursor = db.cursor()
# cursor.execute('select VERSION()')
# data = cursor.fetchone()
# print('database version : %s' % data)
# db.close()

db = pymysql.connect('localhost', 'root', 'chenshuaide', 'phone_info')
cursor = db.cursor()
sql = "INSERT INTO phone_number(STATE_ID, \
               PREFIX, USEAGE, PRIMARY_CITY, CARRIER, INTRODUCED) \
               VALUES (%s,'%s', '%s',  '%s',  '%s',  '%s')" % \
      (0, '012', 'dsds',
       'sdsds', 'sdsdsd', '2015/545')
try:
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()
    print('插入数据库失败')
db.close()
