# Django settings for registration project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Darshan Desai', 'darshandesai17@gmail.com'),
)
DEFAULT_FROM_EMAIL = 'darshandesai17@gmail.com'
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'registration.db', # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New York'


#current year?



# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

INTERNAL_IPS = ('127.0.0.1',)

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    'C:/Users/Darshan/Desktop/registration/registrationApp/static/',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
FIXTURE_DIRS = (
   'registrationApp/static/fixtures/',
)
# Make this unique, and don't share it with anybody.
SECRET_KEY = '$l$(8%ln$#921yx1vj3j0hmmu&f-q4=b+w$3mou10^u7v&p82r'

# List of callables that know how to import templates from various sourcesself.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'registration.urls'

TEMPLATE_DIRS = (
    "C:/Users/Darshan/Desktop/registration/Templates"
    # Don't forget to use absolute paths, not relative paths.
)
LOGIN_REDIRECT_URL = '/registrationApp/login/'

LOGIN_URL = '/registrationApp/login/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'registrationApp',
    'debug_toolbar'
    # 'south'
    # 'django.contrib.admindocs',
)

#import logging
#logging.basicConfig(
 #   level = logging.DEBUG,
  #  format = '%(asctime)s %(levelname)s %(message)s',
  #  filename = 'registrationApp/myapp.log',
  #  filemode = 'w'
#)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'darshandesai17@gmail.com'
EMAIL_HOST_PASSWORD = 'kti316gu'
EMAIL_PORT = 587
LOGIN_REDIRECT_URL = '/registrationApp/search'
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)
#AUTHENTICATION_BACKENDS = (
# 'django_ldapbackend.LDAPBackend',
# 'django.contrib.auth.backends.ModelBackend',
#)

# Required
#AUTH_LDAP_SERVER = '127.0.0.1'                       # Hostname
#AUTH_LDAP_BASE_USER = "cn=admin,dc=example,dc=com"   # Administrative User's Username
#AUTH_LDAP_BASE_PASS = "password"                     # Administrative User's Password 
#AUTH_LDAP_BASE_DN = "dc=example,dc=com"              # Base DN (also accepts o=example.com format)
#AUTH_LDAP_FIELD_DOMAIN = "example.com"               # Domain from which users will take the domain for dummy e-mail generation (it keeps Django happy!)
#AUTH_LDAP_GROUP_NAME = "ldap_people"                 # Django group for LDAP users (helps us manage them for password changing, etc.)
#AUTH_LDAP_VERSION = 3                                # LDAP version
#AUTH_LDAP_OLDPW = False                              # Can the server take the old password? True/False

# Optional
#AUTH_LDAP_FIELD_USERAUTH = "uid"                     # The field from which the user authentication shall be done.
#AUTH_LDAP_FIELD_AUTHUNIT = "People"                  # The organisational unit in which your users shall be found.
#AUTH_LDAP_FIELD_USERNAME = "uid"                     # The field from which to draw the username (Default 'uid'). (Allows non-uid/non-dn custom fields to be used for login.)
#AUTH_LDAP_WITHDRAW_EMAIL = False                     # Should django try the directory for the user's email ('mail')? True/False.
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
