# -*- coding: utf-8 -*-
import MySQLdb
import re

conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='zheng53678',
        db ='timetable',
        )
cur = conn.cursor()

ins_room = "insert into Classroom values(%s,%s,%s,%s,%s)"
ins_week = "insert into Week values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
find_room = "select * from Classroom where classroomID = %s"
find_time = "select * from Week where weeknum = %s and week = %s and classroomID = %s and class12 = %s and class34 = %s and class56 = %s and class78 = %s and class910 = %s and class112 = %s"

'''
Classroom:
create table Classroom(campus varchar(1),building varchar(3),floor varchar(2),room varchar(10),classroomID varchar(4) primary key)

Week:
create table Week(weeknum varchar(2),week varchar(1),classroomID varchar(4),class12 varchar(1),class34 varchar(1),class56 varchar(1),class78 varchar(1),class910 varchar(1),class112 varchar(1),foreign key(classroomID) references Classroom(ClassroomID))
'''

'''
016正心 025致知 002主楼 027诚意楼
033主楼 032东配 042西配

正心 数字4位前两位 3位前一位 2位前一位 无数字未知 D121负一楼
致知 数字2位前一位
主楼 数字3位前一位
诚意 数字3位前一位 2位前一位

东配 数字3位前一位 2位前一位 物实验室未知
主楼 数字3位前一位 2位前一位 B909-1 B909-2 9
西配 数字3位前一位 2位前一位
'''
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
            if cur.execute(find_room,room[3]) == 0:
                cur.execute(ins_room,(campusID,buildingID,floor,roomname,roomID))
                    #更新week表
            if time[0]:
                for j in range(1,19):#周数
                    time[j-1] = time[j-1].split('|')
                    for k in range(1,8):#星期几
                        p = (k-1)*6#基址 
                        if cur.execute(find_time,(str(j),str(k),roomID,time[j-1][p],time[j-1][p+1],time[j-1][p+2],time[j-1][p+3],time[j-1][p+4],time[j-1][p+5])) == 0:
                            cur.execute(ins_week,(str(j),str(k),roomID,time[j-1][p],time[j-1][p+1],time[j-1][p+2],time[j-1][p+3],time[j-1][p+4],time[j-1][p+5]))
            conn.commit()

    room = fp_data.readline()[0:-1]
    time = []
    for i in range(18):
        time.append(fp_data.readline()[0:-1])
        
fp_data.close()
cur.close()
