# -*- coding: utf-8 -*-
import os
import re

im = 0

fp_final = open("shaped data.data",'w')
path = os.getcwd()#获取当前文件夹路径
filelist = os.listdir(path)#获取path目录下的文件列表,即当前目录下的文件列表
for x in filelist:#对于每个文件
    filename = os.path.splitext(x)#分离文件名和后缀
    if filename[1] == '.txt': #以下只对txt文件操作，即对每个校区的楼列表文件操作，filename[0]为校区名
        campusName = filename[0] #campusName为校区名
        fp_building = open(x,'r')#打开楼列表文件
        campusID = fp_building.readline()[0:-1]#获得校区ID
        buildings = fp_building.readlines()#获取楼的ID、名字，一个楼为building中的一项
        fp_building.close()

        for building in buildings:#对于每栋楼
            building = building.split('|')
            buildingID = building[0]#获得楼ID
            buildingName = building[1][0:-1]#获得楼名

            fp_result = open(campusName + '/' + buildingID + "_room.txt", 'r')#打开教室列表文件
            fp_result.readline()#读楼名
            classrooms = fp_result.readlines()
            for classroom in classrooms:#对于每个教室
                classroom = classroom.split('|')
                roomID = classroom[0]#获得教室ID
                temp = re.findall('\w+',classroom[1][0:-1])
                if temp:#纯中文的教室名不要
                    roomName = temp[0]#获得教室名，只截取英文字母和数字
                    fp_timetable = open(campusName+'/'+buildingID+"_room/"+roomID+".txt", 'r')#打开教室时间表
                    fp_timetable.readline()#读出教室名
                    timetable = fp_timetable.readlines()
                    fp_final.write(campusID+'|'+buildingID+'|'+roomName+'|'+roomID+'\n')
                    for i in timetable:#有的教室在教务处上信息有错误，存在另一个空表，在此删去
                        if len(i) == 169:#错误的情况
                            fp_final.write(i[0:84] + '\n')
                        else:
                            fp_final.write(i)
fp_final.close()
