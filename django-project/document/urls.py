from django.conf.urls import patterns, url
from References.urls import *

import views

urlpatterns = patterns('',
                       url(r'^$', views.list, name='list'),
                       url(r'^upload/$', views.upload_file, name='upload'),
                       url(r'^(?P<doc_id>\d+)/$', views.law_detail, name='law'),
)
