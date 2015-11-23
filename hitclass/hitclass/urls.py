# -*- coding:utf-8 -*-
from django.conf.urls import *
from classroom.views import *
from django.contrib import admin
admin.autodiscover()
import settings


urlpatterns = patterns('',
	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', index),
	url(r'^index/$', index),
	url(r'^search/$', search),
	url(r'^search2/$', search2),
	url(r'^navigation/$', navigation),
	url(r'^login/$', login),
	url(r'^recommend/$', recommend),
)
