# -*- coding: utf-8 -*-
import urllib    
import urllib2  
import cookielib
import re
import os

cookie = cookielib.CookieJar()    
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))  
  
#自定义一个请求#  
req_get4 = urllib2.Request(    
    url = 'http://ids.hit.edu.cn/authserver/login?service=http%3A%2F%2Fjwts.hit.edu.cn%2FloginCAS'    
)  
  
#访问该链接#  
result = opener.open(req_get4)  
result = result.read()

#正则表达式提取四个项,用于登录
value = re.findall('"hidden" name=".*?" value="(.*?)"',result)

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
    url = 'http://ids.hit.edu.cn/authserver/login?service=http%3A%2F%2Fjwts.hit.edu.cn%2FloginCAS',
    data = postdata
)

result = opener.open(req_login)
print "login success"

'''
开始爬取教室信息
'''

#首先获取楼列表：楼编号|楼名
campus = {}
campus['firstcampus'] = '1'
campus['secondcampus'] = '2'
for x in campus:#对每个校区，x为校区名
    #发送id:校区号 到http://jwts.hit.edu.cn/kjscx/queryJxlListBySjid得到楼列表
    postdata=urllib.urlencode({
        'id': campus[x]
    })
    req_getbuildings = urllib2.Request(    
        url = 'http://jwts.hit.edu.cn/kjscx/queryJxlListBySjid',
        data = postdata
    )
    result = opener.open(req_getbuildings)
    result = result.read()
    item = re.findall('DM":"(.*?)".*?MC":"(.*?)"',result)#获得楼ID和楼名

    fp_result = open( x + "_buiding.txt", 'w')#创建校区的楼列表文件
    fp_result.write(campus[x] + '\n')#先写入校区ID
    for building in item:#对于每栋楼
        fp_result.write(building[0]+'|'+building[1]+'\n')#在楼列表文件中写入：楼编号|楼名
    fp_result.close()
print "楼列表创建完毕"

#然后获得每栋楼的教室列表：教室ID|教室名，最后爬取每个教室的时间表
path = os.getcwd()#获取当前文件夹路径
filelist = os.listdir(path)#获取path目录下的文件列表,即当前目录下的文件列表
for x in filelist:#对于每个文件
    filename = os.path.splitext(x)#分离文件名和后缀
    if filename[1] == '.txt': #以下只对txt文件操作，即对每个校区的楼列表文件操作，filename[0]为校区名
        campusName = filename[0] #campusName为校区名
        print campusName + " begin"
        if os.path.exists(campusName) == False: #创建校区文件夹储存楼内容
            os.mkdir(campusName)
        fp_building = open(x,'r')#打开楼列表文件
        campusID = fp_building.readline()[0:-1]#获得校区ID
        buildings = fp_building.readlines()#获取楼的ID、名字，一个楼为building中的一项
        fp_building.close()
        
        for building in buildings:#对于每栋楼
            building = building.split('|')
            buildingID = building[0]#获得楼ID
            buildingName = building[1][0:-1]#获得楼名
            print " "+ buildingID + "building"
            
            #发送id:楼号到http://jwts.hit.edu.cn/kjscx/queryJxcdListBySjid得到教室列表
            postdata=urllib.urlencode({    
                'id':buildingID
            })
            req_getrooms = urllib2.Request(    
                url = 'http://jwts.hit.edu.cn/kjscx/queryJxcdListBySjid',
                data = postdata
            )
            result = opener.open(req_getrooms)
            result = result.read()
            classrooms = re.findall('DM":"(.*?)","MC":"(.*?)"',result)#获得教室ID和教室名列表

            if os.path.exists(campusName+'/'+buildingID+'_room') == False: #创建楼文件夹储存教室
                os.mkdir(campusName+'/'+buildingID+'_room')

            fp_result = open(campusName + '/' + buildingID + "_room.txt", 'w')#创建教室列表文件
            fp_result.write(buildingName+'\n')#先写入楼名
            for classroom in classrooms:#对于每个教室
                roomID = classroom[0]
                roomName = classroom[1]
                fp_result.write(roomID+'|'+roomName+'\n')#在教室列表文件中写入教室ID|教室名
                
                fp_timetable = open(campusName+'/'+buildingID+"_room/"+roomID+".txt", 'w')#创建当前教室的文件，记录其时间表
                fp_timetable.write(roomName+'\n')#先写入教室名
                for j in range(1,19): #j为周数，从1-18周，爬取每周的时间表
                    #发送id:楼号到http://jwts.hit.edu.cn/kjscx/queryKjs得到教室空闲信息
                    postdata=urllib.urlencode({    
                        'pageXnxq':'2015-20161',
                        'pageZc1':str(j),
                        'pageZc2':str(j),
                        'pageXiaoqu':campusID,
                        'pageLhdm':buildingID,
                        'pageCddm':roomID
                    })
                    req_gettimetable = urllib2.Request(    
                        url = 'http://jwts.hit.edu.cn/kjscx/queryKjs',
                        data = postdata
                    )
                    result = opener.open(req_gettimetable)
                    result = result.read()
                    timetable = re.findall('div class=\'(.*?)\'',result)#获取空闲与否的列表
                    
                    for k in timetable:
                        if len(k)==0:
                            fp_timetable.write('0|')
                        else:
                            fp_timetable.write('1|')
                    fp_timetable.write('\n')
                fp_timetable.close()
                print "     " + roomID + "done"
            fp_result.close()
        print campusID + " done"
