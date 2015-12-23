# -*- coding: utf-8 -*-
import re
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hitclass.settings")
from django.core.management import execute_from_command_line
from classroom.models import Classroom, Week, Status

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
    floor = cul_level(buildingID,roomname)
    
    if buildingID =='016' or buildingID == '025' or buildingID == '002' or\
       buildingID == '027' or buildingID == '033' or buildingID == '032' or buildingID == '042':
        if len(roomname) <= 10:
            c = Classroom.objects.filter(roomid__exact = roomID)
            if c:#若存在则更新并使用该对象
                c.update(campus = campusID, building = buildingID,\
                         floor = floor, room = roomname)
                c = c[0]
                c.save()
            else:#若不存在则插入一个项
                c = Classroom(campus = campusID,building = buildingID,floor = floor,\
                              room = roomname,roomid = roomID)
                c.save()
            print c.roomid
            #更新week表
            if time[0]:
                for j in range(1,19):#周数
                    time[j-1] = time[j-1].split('|')
                    for k in range(1,8):#星期几
                        p = (k-1)*6#基址
                        weekid = str(j)+str(k)+c.roomid
                        w = Week.objects.filter(weekid__exact = weekid)
                        if w:#若存在则使用该对象,更新status表
                            w = w[0]
                            s = w.status
                            s.class12 = time[j-1][p]
                            s.class34 = time[j-1][p+1]
                            s.class56 = time[j-1][p+2]
                            s.class78 = time[j-1][p+3]
                            s.class910 = time[j-1][p+4]
                            s.class1112 = time[j-1][p+5]
                            s.save()
                        else:#若不存在则插入一个status项，再插入一个week项
                            s = Status(class12 = time[j-1][p],class34 = time[j-1][p+1],class56 = time[j-1][p+2],\
                                       class78 = time[j-1][p+3],class910 = time[j-1][p+4],class1112 = time[j-1][p+5])
                            s.save()
                            w = Week(weeknum = str(j),week = str(k),status = s,classroom = c,weekid = weekid)
                            w.save()
    room = fp_data.readline()[0:-1]
    time = []
    for i in range(18):
        time.append(fp_data.readline()[0:-1])
fp_data.close()
