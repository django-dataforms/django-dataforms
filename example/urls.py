from django.conf.urls.defaults import *
from django.conf import settings
from views import form, form_collection

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
	(r'^form/', form),
	(r'^wizard/$', form_collection),
	
    # (r'^djangodbforms/', include('djangodbforms.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

# This is for development only.	 Use apache rewrites in production. 
if settings.DEBUG:
	urlpatterns += patterns('',
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)