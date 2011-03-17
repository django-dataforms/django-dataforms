# Django settings for djangodbforms project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.split(PROJECT_DIR)[0]

INTERNAL_IPS = '127.0.0.1'

ADMINS = (
    #('Your Name', 'Your Email'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'			  # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'dataforms.db'			 # Or path to database file if using sqlite3.
DATABASE_USER = ''			   # Not used with sqlite3.
DATABASE_PASSWORD = ''		   # Not used with sqlite3.
DATABASE_HOST = ''			   # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''			   # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_DIR + '/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '6ibmo6b(9jlq%6_eq6t1ej05g8wpbpa7zu8$x0nm(4vkdzt=tf'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
#	  'django.template.loaders.eggs.load_template_source',
)

# Path for file uploads (don't forget trailing slash)
UPLOAD_PATH = 'uploads/'

#TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.debug',)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	PROJECT_DIR + '/templates/',
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.admin',
	'dataforms',
)

try: 
    INSTALLED_APPS += (
        'django_extensions',
        'reversion',
    )
except ImportError: pass
