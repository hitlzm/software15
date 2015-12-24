# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Classroom(models.Model):
	campus = models.CharField(max_length = 1) #校区编号
	building = models.CharField(max_length = 3) #教学楼编号
	floor = models.CharField(max_length = 2) #楼层
	room = models.CharField(max_length = 10) #教室名
	roomid = models.CharField(max_length = 4, primary_key = True) #教室id

	def __unicode__(self):
		return self.campus + '-' + self.building + '-' + self.floor + '-' + self.room


class Status(models.Model):
	class12 = models.CharField(max_length = 1)
	class34 = models.CharField(max_length = 1)
	class56 = models.CharField(max_length = 1)
	class78 = models.CharField(max_length = 1)
	class910 = models.CharField(max_length = 1)
	class1112 = models.CharField(max_length = 1)

	def __unicode__(self):
		return self.class12 + self.class34 + self.class56 + self.class78 + self.class910 + self.class1112


class Week(models.Model):
	weeknum = models.CharField(max_length = 2) #周次
	week = models.CharField(max_length = 1) #星期
	weekid = models.CharField(max_length = 7, primary_key = True) #ID，内容是'周次'+'星期'+'教室id'
	status = models.OneToOneField(Status)
	classroom = models.ForeignKey(Classroom)

	def __unicode__(self):
		return self.classroom.campus + '-' + self.classroom.building + '-' + self.classroom.floor + '-' + self.classroom.room + '-' + self.weeknum


class ReserveInfo(models.Model):
	building = models.CharField(max_length = 3) #教学楼编号
	buildingname = models.CharField(max_length = 15) #教学楼名
	room = models.CharField(max_length = 10) #教室名
	weeknum = models.CharField(max_length = 2) #周次
	week = models.CharField(max_length = 1) #星期
	weekname = models.CharField(max_length = 10) #星期一；星期二；
	period = models.CharField(max_length = 1) #节次
	periodname = models.CharField(max_length = 15) #节次
	description = models.CharField(max_length = 1000) #描述
	peoplenum = models.CharField(max_length = 3) #人数
	media =  models.CharField(max_length = 1) #是否使用媒体设备
	status = models.CharField(max_length = 1) #审核状态
	phone = models.CharField(max_length = 11) #联系人电话
	school = models.CharField(max_length = 30) #联系人单位
	user = models. ForeignKey(User)