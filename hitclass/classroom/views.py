# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import Q
import time, string, datetime, random
from classroom.models import Classroom, Status, Week

import sys
reload(sys)
sys.setdefaultencoding('utf8')


# 主页
def index(request):
	return render_to_response('index.html', {'key':True})

# 教室查询
def search(request):
	buildingLst = [["016", "正心"], ["025", "致知"], ["027", "诚意"], ["012", "机械"], 
					["033", "主楼"], ["032", "东配楼"], ["042", "西配楼"]]

	message = Week()
	if request.POST:
		campus = request.POST['campus']	# 校区
		building = request.POST['building'] # 教学楼
		floor = request.POST['floor'] # 楼层
		weeknum = request.POST['weeknum'] # 教学周
		week = request.POST['week']	# 星期
		period = int(request.POST['period']) # 节次

		message = Week.objects.filter(	classroom__campus__icontains = campus,
										classroom__building__icontains = building,
										classroom__floor__exact = floor,
										weeknum__exact = weeknum,
										week__icontains = week)
		
		# 处理节次问题
		for everyweek in message:
			if period == 1:
				everyweek.status.class12 = everyweek.status.class34
			elif period == 2:
				everyweek.status.class12 = everyweek.status.class56
			elif period == 3:
				everyweek.status.class12 = everyweek.status.class78
			elif period == 4:
				everyweek.status.class12 = everyweek.status.class910
			elif period == 5:
				everyweek.status.class12 = everyweek.status.class1112

		# 搜索结果处理
		messageLst = []
		for i in range(len(message)):
			messageLst.append(message[i])
		for j in range(4):
			messageLst.append(Week())
	
		key = len(message) / 4 + 1
		if len(message) % 4 == 0:
			key = len(message) / 4
		
		messageTeam = []
		for i in range(0, key * 4, 4):
			everyLst = []
			for j in range(4):
				everyLst.append(messageLst[i + j])
			messageTeam.append(everyLst)

		# 教学楼名
		buildingName = ""
		for i in buildingLst:
			if i[0] == building:
				buildingName = i[1]
		
		# 节次
		periodLst = ["第1-2节", "第3-4节", "第5-6节", "第7-8节", "第9-10节", "第11-12节"]
		periodName = periodLst[period]

		return render_to_response('search.html', 
			{'messageTeam':messageTeam, 'buildingName':buildingName, 'periodName':periodName, 'period':period})

	return render_to_response('search.html',)

# 校园导航
def navigation(request):
	return render_to_response('navigation.html', {'key':True})

# 登录认证
def login(request):
	return render_to_response('login.html', {'key':True})

# 教室推荐
def	recommend(request):
	buildingLst = [	["1", "016", "正心", 10],
					["1", "025", "致知", 4],
					["1", "027", "诚意", 6],
					["1", "012", "机械", 4],
					["2", "033", "主楼", 9],
					["2", "032", "东配楼", 4],
					["2", "042", "西配楼", 3]]

	randLst = [0, 1, 0, 2, 0, 3, 0, 1, 4, 0, 1, 5, 6, 0, 2, 1, 2, 2] #加权随机序列
	randNum = random.randint(0, len(randLst) - 1)
	key = randLst[randNum]
	
	campus = buildingLst[key][0]	# 随机校区
	building = buildingLst[key][1]	# 随机教学楼
	floor = random.randint(1, buildingLst[key][3] + 1) # 随机楼层
	week = 1

	# 获取当前星期
	weekday = [	['星期一', '1'],
				['星期二', '2'],
				['星期三', '3'],
				['星期四', '4'],
				['星期五', '5'],
				['星期六', '6']]
	todayweekday = datetime.datetime.now().weekday()
	if todayweekday > 0:
	    week = weekday[datetime.datetime.now().weekday()][1]
	else:
	    week = '7'

	# 获取当前教学周
	startdate ={'2015-3':[9,14]}	# -1是春季学期，-2是夏季学期，-3是秋季学期
	today = datetime.datetime.now()
	month = today.month
	year = today.year
	if month > 8:
	    term = str(year) + '-3'
	elif month < 2:
	    term = str(year-1) + '-3'
	elif month > 6:
	    term = str(year) + '-2'
	else:
	    term = str(term) + '-1'
	d1 = datetime.datetime(year,month,today.day)
	d2 = datetime.datetime(string.atoi(term[0:4]),startdate[term][0],startdate[term][1])
	weeknum = (d1 - d2).days / 7 + 1

	# 获取当前时间
	currentTime = time.strftime("%H:%M", time.localtime(time.time()))
	hour = int(currentTime[:2])
	minutes = int(currentTime[3:])
	period = 0
	if (hour <= 9) or (hour == 9 and minutes <= 45):
		period = 0	#第1-2节
	elif (hour == 9 and minutes > 45) or (hour == 10) or (hour == 11 and minutes <= 45):
		period = 1	#第3-4节
	elif (hour == 11 and minutes > 45) or (12 <= hour <= 14) or (hour == 15 and minutes <= 30):
		period = 2	#第5-6节
	elif (hour == 15 and minutes > 30) or (hour == 16) or (hour == 17 and minutes <= 30):
		period = 3	#第7-8节
	elif (hour == 17 and minutes > 30) or (18 <= hour <= 19) or (hour == 20 and minutes <= 15):
		period = 4	#第9-10节
	else:
		period = 5	#第11-12节

	periodLst = ["第1-2节", "第3-4节", "第5-6节", "第7-8节", "第9-10节", "第11-12节"]
	periodName = periodLst[period]


	# 按照生成的随机信息去数据查询
	message = Week()
	message = Week.objects.filter(	classroom__campus__icontains = campus,
									classroom__building__icontains = building,
									classroom__floor__exact = floor,
									weeknum__exact = weeknum,
									week__icontains = week)

	# 处理节次问题
	for everyweek in message:
		if period == 1:
			everyweek.status.class12 = everyweek.status.class34
		elif period == 2:
			everyweek.status.class12 = everyweek.status.class56
		elif period == 3:
			everyweek.status.class12 = everyweek.status.class78
		elif period == 4:
			everyweek.status.class12 = everyweek.status.class910
		elif period == 5:
			everyweek.status.class12 = everyweek.status.class1112

	# 搜索结果处理
	messageLst = []
	for i in range(len(message)):
		messageLst.append(message[i])
	for j in range(4):
		messageLst.append(Week())

	key = len(message) / 4 + 1
	if len(message) % 4 == 0:
		key = len(message) / 4
	
	messageTeam = []
	for i in range(0, key * 4, 4):
		everyLst = []
		for j in range(4):
			everyLst.append(messageLst[i + j])
		messageTeam.append(everyLst)

	# 教学楼名
	buildingName = ""
	for i in buildingLst:
		if i[1] == building:
			buildingName = i[2]

	return render_to_response('recommend.html', 
		{'messageTeam':messageTeam, 'buildingName':buildingName, 'periodName':periodName, 'period':period})