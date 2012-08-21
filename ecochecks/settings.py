# Django settings for ecochecks project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
          # ('Your Name', 'your_email@domain.com'),
          )

#Before using you'll need to install Memcached and python-memcached
#Memcached is available  at http://danga.com/memcached/
#python-memcached is available atftp://ftp.tummy.com/pub/python-memcached/ which provides Python bindings to Memcached
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ecochecks_app',                      # Or path to database file if using sqlite3.
        'USER': 'ecochecks',                      # Not used with sqlite3.
        'PASSWORD': 'y4P9VL',                  # Not used with sqlite3.
        'HOST': 'mysql.ecochecks.org',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 2

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "static")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ks3=ynkg5pas8zqdw=+-1)xc$y=&+#=)8u8gruc2^t9=6zyq7)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    #     'django.template.loaders.eggs.Loader',
                    )

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
                 os.path.join(PROJECT_ROOT, "templates"),
                 )

INSTALLED_APPS = (
                  'django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.comments',
                  'django.contrib.sessions',
                  'django.contrib.sites',
                  'django.contrib.messages',
                  # Uncomment the next line to enable the admin:
                  'django.contrib.admin',
    'account',
    'hosts',
    'domains',
    'templatetags',
    'django.contrib.flatpages',
    'tinymce',
    'memcache_status',
    'contact',
    'tagging',
    'mptt',
    'zinnia',
    'django_bitly',
    'tweepy',
    'BeautifulSoup',
)

TEMPLATE_CONTEXT_PROCESSORS = (
                               'django.core.context_processors.auth',
                               'django.core.context_processors.i18n',
                               'django.core.context_processors.request',
                               'django.core.context_processors.media',
                               'zinnia.context_processors.media',
                               'zinnia.context_processors.version', # Optional
                               )



LOGIN_URL = '/account/login/'

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

#Email settings for sending email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@ecochecks.org'
EMAIL_HOST_PASSWORD = 'cin5gis8um2n'
EMAIL_USE_TLS = True

CONTACT_MAIL = 'contact@ecochecks.org'

API_KEY = '7a5762a966f3536df1a6b23a247afbc2'
USER_APP_KEY = 'a4409e7969ee33ce2798767f4798a82c-1245958316'

try:
    from local_settings import *
except ImportError:
    pass

