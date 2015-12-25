# -*- coding: utf-8 -*-
import urllib    
import urllib2  
import cookielib
import re
import os
from PIL import Image

cookie = cookielib.CookieJar()    
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))  

#验证码
urllib.urlretrieve('http://jwts.hit.edu.cn/captchaImage?id=7464','code.jpeg')
fp = open("code.jpeg",'rb')
image = Image.open(fp)
image.show()
fp.close()
validatecode = raw_input("输入验证码:")
path = os.getcwd()
os.remove(path + '\code.jpeg')

#登录需要POST的数据#  
postdata=urllib.urlencode({
    'usercode':'1133710314',
    'password':'peng53678',
    'code':validatecode
})
#自定义一个请求#  
req_login = urllib2.Request(    
    url = 'http://jwts.hit.edu.cn/loginLdap',
    data = postdata
)
#访问该链接#  
result = opener.open(req_login)
result = result.read()

