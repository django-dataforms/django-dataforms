from django.conf.urls.defaults import *
from django.conf import settings
from views import form, form_collection

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', form),
	(r'^wizard/$', form_collection),
	(r'^admin/(.*)', admin.site.root),
)

# This is for development only. Use apache rewrites in production. 
if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	)