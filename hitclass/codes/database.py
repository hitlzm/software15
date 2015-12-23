# -*- coding: utf-8 -*-
import MySQLdb
import re
from classroom.models import Classroom, Week

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def cul_level(buildingID,roomname):
    purenumber = re.findall('\d+',roomname)
    if purenumber:
        purenumber = purenumber[0]
        if len(purenumber) == 2 or len(purenumber) == 3:
            return purenumber[0]
        elif len(purenumber) == 4:
            return purenumber[0] + purenumber[1]
        else:
            return -1
    else:
        return -1

fp_data = open("shaped data.data",'r')
room = fp_data.readline()[0:-1]
time = []
for i in range(18):
    time.append(fp_data.readline()[0:-1])
while room:
    #formalize room
    room = room.split('|')
    campusID = room[0]
    buildingID = room[1]
    roomname = room[2]
    roomID = room[3]
    floor = cul_level(buildingID,roomID)
    
    if buildingID =='016' or buildingID == '025' or buildingID == '002' or buildingID == '027' or buildingID == '033' or buildingID == '032' or buildingID == '042':
        if len(roomname) <= 10:
            if len(Classroom.objects.filter(roomid__icontains = roomID)) == 0:
                p = Classroom(campus = campusID,building = buildingID,floor = floor,room = roomname,roomid = roomID)
                p.save()
            #更新week表
            if time[0]:
                for j in range(1,19):#周数
                    time[j-1] = time[j-1].split('|')
                    for k in range(1,8):#星期几
                        p = (k-1)*6#基址
                        if len(Week.objects.filter(weeknum__icontains = str(j),week__icontains = str(k),classroom__roomid__icontains =roomID)) == 0:
                            s = Status(class12 = time[j-1][p],class34 = time[j-1][p+1],class56 = time[j-1][p+2],class78 = time[j-1][p+3],class910 = time[j-1][p+4],class1112 = time[j-1][p+5])
                            s.save()
                            r = Week(weeknum = str(j),week = str(k),status = s,classroom = p)
                            r.save()
    room = fp_data.readline()[0:-1]
    time = []
    for i in range(18):
        time.append(fp_data.readline()[0:-1])
        
fp_data.close()
cur.close()
