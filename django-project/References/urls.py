from django.conf.urls import patterns, url

from views import  AddReferenceView

urlpatterns = patterns('',
                       url(r'^wrap_text/$', AddReferenceView.as_view(), name='wrap_text')
)
