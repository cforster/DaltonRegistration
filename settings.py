import ldap

# Django settings for registration project.

DEBUG = False
TEMPLATE_DEBUG = False
ADMINS = (
     ('Darshan Desai', 'darshandesai17@gmail.com'),
)
DEFAULT_FROM_EMAIL = 'DaltonCourseReg@gmail.com'
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'registration2012-2013', # Or path to database file if using sqlite3.
        'USER': 'darshan',                      # Not used with sqlite3.
        'PASSWORD': 'kti316gu',                  # Not used with sqlite3.
        'HOST': 'compsci.dalton.org',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
        
    }
}
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
STATIC_ROOT = '/home/ddesai/registration/site_media/'
#STATIC_ROOT = 'C:/Users/Darshan/Desktop/registration/site_media/'


# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'http://compsci.dalton.org/registrationApp/site_media/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX ='/media/'

# Additional locations of static files
STATICFILES_DIRS = (
    '',
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
SESSION_COOKIE_AGE = 1209600
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    "/home/ddesai/registration/Templates/"
    #"C:/Users/Darshan/Desktop/registration/Templates"
    # Don't forget to use absolute paths, not relative paths.
)

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'registrationApp',
    # 'django.contrib.admindocs',
)


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'DaltonCourseReg@gmail.com'
EMAIL_HOST_PASSWORD = 'kti316daltonu'
EMAIL_PORT = 587

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)


AUTHENTICATION_BACKENDS = (
    'registrationApp.customBackend.customBackend',
    'django.contrib.auth.backends.ModelBackend',
)
