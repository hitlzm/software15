# -*- coding: utf-8 -*-
import urllib    
import urllib2  
import cookielib
import re

cookie = cookielib.CookieJar()    
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))  
  
#自定义一个请求#  
req_get4 = urllib2.Request(    
    url = 'https://ids.hit.edu.cn/authserver/login?service=https%3A%2F%2Fcms.hit.edu.cn%2Flogin%2Findex.php%3FauthCAS%3DCAS'    
)  
  
#访问该链接#  
result = opener.open(req_get4)  

#正则表达式提取四个项,用于登录
value = re.findall('"hidden" name=".*?" value="(.*?)"',result.read())

studentID = raw_input("输入学号：")
password = raw_input("输入密码：")

#登录需要POST的数据#  
postdata=urllib.urlencode({    
    'username':studentID,
    'password':password,
    'lt':value[0],
    'execution':value[1],
    '_eventId':value[2],
    'rmShown':value[3]
})

req_login = urllib2.Request(    
    url = 'https://ids.hit.edu.cn/authserver/login?service=https%3A%2F%2Fcms.hit.edu.cn%2Flogin%2Findex.php%3FauthCAS%3DCAS',
    data = postdata
)

result = opener.open(req_login)

if (result.read().find("logout")) != -1:
    print "login success"
else:
    print "failed"

