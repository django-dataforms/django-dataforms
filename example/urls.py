from django.conf import settings
from django.conf.urls.defaults import *
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('views',
	url(r'^$', 'index', name="index"),
	url(r'^collection/$', 'form_collection', name="form_collection"),
	url(r'^upload/$', 'upload', name="upload"),
	(r'^admin/', include(admin.site.urls)),
)

# Serve Static and Media on development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()