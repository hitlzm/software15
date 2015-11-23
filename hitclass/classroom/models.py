# -*- coding:utf-8 -*-
from django.db import models

class classroom(models.Model):
	campus = models.CharField(max_length = 1) #校区
	building = models.CharField(max_length = 2) #教学楼
	

