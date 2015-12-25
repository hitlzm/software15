# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import Q
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from classroom.models import Classroom, Status, Week, ReserveInfo
import urllib, urllib2  
import cookielib
import re, time, string, datetime, random


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
		if len(message) % 4 == 0 and len(message) != 0:
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
		periodLst = [	"第1-2节 08:00--09:45",
						"第3-4节 10:00--11:45",
						"第5-6节 13:45--15:30",
						"第7-8节 15:45--17:30",
						"第9-10节 18:30--20:15",
						"第11-12节 20:30--22:15"]
		periodName = periodLst[period]

		return render_to_response('search.html',
			{'messageTeam':messageTeam, 'buildingName':buildingName, 'periodName':periodName, 'period':period})

	return render_to_response('search.html',)


# 校园导航
def navigation(request):
	return render_to_response('navigation.html', {'key':True})


# 登录认证
def login(request):
	key = False
	errors= []
	ID=None
	password=None
	if request.POST:
		ID = request.POST['ID']
		password= request.POST['password']
		
		###验证用户合法性
		cookie = cookielib.CookieJar()    
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))  
		  
		#获得四个项用于登录
		req_get4 = urllib2.Request(    
			url = 'https://ids.hit.edu.cn/authserver/login?service=https%3A%2F%2Fcms.hit.edu.cn%2Flogin%2Findex.php%3FauthCAS%3DCAS'    
		)    
		result = opener.open(req_get4)  
		value = re.findall('"hidden" name=".*?" value="(.*?)"',result.read())

		#登录需要POST的数据#  
		postdata=urllib.urlencode({    
			'username':ID,
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
			user = auth.authenticate(username=ID, password=password)
			if user is not None:
				if user.is_active:
					auth.login(request,user)
					return render_to_response('reserve.html',)
				else:
					key = True
					return render_to_response('login.html', {'user_password_false':key,})
			else:#合法用户，但数据库中没有，则加入用户
				user = User.objects.create_user(
					username=ID,   
					password=password
				)
				user = auth.authenticate(username=ID, password=password)
				if user.is_active:
					auth.login(request,user)
					return render_to_response('reserve.html',)
				else:
					key = True
					return render_to_response('login.html', {'user_password_false':key,})
		else:
			key = True
			return render_to_response('login.html', {'user_password_false':key,})

	return render_to_response('login.html',)


# 登出
def logout(request):
	auth.logout(request)
	return render_to_response('login.html', {'logout':True})


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
	if period == 0:
		message = Week.objects.filter(	classroom__campus__icontains = campus,
									classroom__building__icontains = building,
									classroom__floor__exact = floor,
									weeknum__exact = weeknum,
									week__icontains = week,							
									status__class12 = '0')
	elif period == 1:
		message = Week.objects.filter(	classroom__campus__icontains = campus,
									classroom__building__icontains = building,
									classroom__floor__exact = floor,
									weeknum__exact = weeknum,
									week__icontains = week,
									status__class34 = '0')

	elif period == 2:
		message = Week.objects.filter(	classroom__campus__icontains = campus,
									classroom__building__icontains = building,
									classroom__floor__exact = floor,
									weeknum__exact = weeknum,
									week__icontains = week,
									status__class56 = '0')
	elif period == 3:
		message = Week.objects.filter(	classroom__campus__icontains = campus,
									classroom__building__icontains = building,
									classroom__floor__exact = floor,
									weeknum__exact = weeknum,
									week__icontains = week,
									status__class78 = '0')
	elif period == 4:
		message = Week.objects.filter(	classroom__campus__icontains = campus,
									classroom__building__icontains = building,
									classroom__floor__exact = floor,
									weeknum__exact = weeknum,
									week__icontains = week,
									status__class910 = '0')
	elif period == 5:
		message = Week.objects.filter(	classroom__campus__icontains = campus,
									classroom__building__icontains = building,
									classroom__floor__exact = floor,
									weeknum__exact = weeknum,
									week__icontains = week,
									status__class1112 = '0')

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
	if len(message) % 4 == 0 and len(message) != 0:
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


# 教室预借
@login_required(login_url='/login/')
def reserveinfo(request):
	user = User.objects.filter(id__exact = request.user.id)[0]
	userinfo = []
	userinfo.append(user.username)
	reserveinfo = ReserveInfo.objects.filter(user__exact = user)
	if reserveinfo:
		userinfo.append(reserveinfo[0].name)
		userinfo.append(reserveinfo[0].phone)
		userinfo.append(reserveinfo[0].school)
	else:
		userinfo.append("")
		userinfo.append("")
		
	buildingLst = [	["1", "016", "正心", 10],
					["1", "025", "致知", 4],
					["1", "027", "诚意", 6],
					["1", "012", "机械", 4],
					["2", "033", "主楼", 9],
					["2", "032", "东配", 4],
					["2", "042", "西配", 3]]
	periodLst = ["第1-2节", "第3-4节", "第5-6节", "第7-8节", "第9-10节", "第11-12节"]
	weeknumLst = [	"第1周", "第2周", "第3周", "第4周", "第5周",
					"第6周", "第7周", "第8周", "第9周", "第10周",
					"第11周", "第12周", "第13周", "第14周", "第15周",
					"第16周", "第17周", "第18周", "第19周", "第20周"]
	weekLst = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

	if request.POST:
		reserve_building = request.POST['reserve_building']	# 教学楼
		reserve_room = request.POST['reserve_room']	# 教室
		reserve_weeknum = int(request.POST['reserve_weeknum']) # 教学周
		reserve_week = int(request.POST['reserve_week'])	# 星期
		reserve_period = int(request.POST['reserve_period']) # 节次

		classroomMessage = []
		for i in buildingLst:
			if i[1] == reserve_building:
				classroomMessage.append(i[2])
		classroomMessage.append(reserve_room)
		classroomMessage.append(weeknumLst[reserve_weeknum - 1])
		classroomMessage.append(weekLst[reserve_week - 1])
		periodName = periodLst[reserve_period]
		classroomMessage.append(periodName)

		return render_to_response('reserveinfo.html', {'classroomMessage':classroomMessage, 'username':user.username, 'userinfo':userinfo})

	return render_to_response('reserveinfo.html', {'username':user.username, 'userinfo':userinfo})


@login_required(login_url='/login/')
def reserveinfosave(request):
	buildingLst = [	["1", "016", "正心", 10],
					["1", "025", "致知", 4],
					["1", "027", "诚意", 6],
					["1", "012", "机械", 4],
					["2", "033", "主楼", 9],
					["2", "032", "东配", 4],
					["2", "042", "西配", 3]]
	periodLst = ["第1-2节", "第3-4节", "第5-6节", "第7-8节", "第9-10节", "第11-12节"]
	weeknumLst = [	"第1周", "第2周", "第3周", "第4周", "第5周",
					"第6周", "第7周", "第8周", "第9周", "第10周",
					"第11周", "第12周", "第13周", "第14周", "第15周",
					"第16周", "第17周", "第18周", "第19周", "第20周"]
	weekLst = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

	if request.POST:
		ID = request.POST['studentID']	# 学号
		name = request.POST['name']	# 姓名
		phone = request.POST['phone'] # 联系电话
		school = request.POST['school'] # 单位
		buildingname = request.POST['buildingname'] # 教学名
		room = request.POST['room']
		weeknumname = request.POST['weeknumname']
		weekname = request.POST['weekname']
		periodname = request.POST['periodname']
		description = request.POST['description']
		peopletnum = request.POST['peoplenum']
		media = request.POST['media']

		building = ""
		for i in buildingLst:
			if i[2] == buildingname:
				building = building + i[1]
		weeknum = ""
		for i in range(len(weeknumLst)):
			if weeknumLst[i] == weeknumname:
				weeknum = weeknum + str( i + 1)
		week = ""
		for i in range(len(weekLst)):
			if weekLst[i] == weekname:
				week = week + str(i + 1)
		period = ""
		for i in range(len(periodLst)):
			if periodLst[i] == periodname:
				period = period + str(i)

		user = User.objects.filter(id__exact = request.user.id)[0]
		reserveinfo = ReserveInfo(
			building = building,
			buildingname = buildingname,
			room = room,
			weeknum = weeknum,
			weeknumname = weeknumname,
			week = week,
			weekname = weekname,
			period = period,
			periodname = periodname,
			description = description,
			peoplenum = peopletnum,
			media = media,
			status = '1',
			phone = phone,
			school = school,
			name = name,
			user = user)
		reserveinfo.save()

		return render_to_response('reserve.html',)

	return render_to_response('reserve.html',)


@login_required(login_url='/login/')
def reserve(request):
	user = User.objects.filter(id__exact = request.user.id)[0]
	reserveinfo = ReserveInfo.objects.filter(user__exact = user)
	reserveInfoLst = []
	for i in reserveinfo:
		reserveInfoLst.append(i)
	for i in range(4):
		reserveInfoLst.append(ReserveInfo())

	return render_to_response('reserve.html',{'reserveInfoLst':reserveInfoLst, 'username':user.username})