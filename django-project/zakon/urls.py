from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import settings
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zakon.views.home', name='home'),
    # url(r'^zakon/', include('zakon.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^$', ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('document.urls', namespace='document')),
	url(r'', include('References.urls', namespace='references')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
