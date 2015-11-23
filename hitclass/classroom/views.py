# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db.models import Q
import time, string

import sys
reload(sys)
sys.setdefaultencoding('utf8')


def index(request):
	return render_to_response('index.html', {'key':True})


def search(request):
	return render_to_response('search.html', {'key':True})


def search2(request):
	return render_to_response('search2.html', {'key':True})


def navigation(request):
	return render_to_response('navigation.html', {'key':True})


def login(request):
	return render_to_response('login.html', {'key':True})


def	recommend(request):
	return render_to_response('recommend.html', {'key':True})