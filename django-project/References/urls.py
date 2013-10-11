from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
                       url(r'^wrap_text/$', views.wrap_text_in_tag, name='wrap_text')
)
