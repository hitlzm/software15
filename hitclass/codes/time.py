# -*- coding: utf-8 -*-
import datetime
import string
#打印当前周几
weekday = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
todayweekday = datetime.datetime.now().weekday()
if todayweekday > 0:
    print weekday[datetime.datetime.now().weekday()]
else:
    print '星期日'


#打印当前处于的周数
startdate ={'2015-3':[9,14]}#-1是春季学期，-2是夏季学期，-3是秋季学期
today = datetime.datetime.now()
month = today.month
year = today.year
if month>8:
    term = str(year) + '-3'
elif month<2:
    term = str(year-1) + '-3'
elif month>6:
    term = str(year) + '-2'
else:
    term = str(term) + '-1'
d1 = datetime.datetime(year,month,today.day)
d2 = datetime.datetime(string.atoi(term[0:4]),startdate[term][0],startdate[term][1])
print (d1 - d2).days/7+1
