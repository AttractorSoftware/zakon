from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       url(r'^$', views.list, name='list'),
                       url(r'^upload/$', views.upload_file, name='upload'),
                       url(r'^(?P<doc_id>\d+)/$', views.law_detail, name='law'),
                       url(r'^wrap_text/$', views.wrap_text_in_tag, name='wrap_text')
)
