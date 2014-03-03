"""
.. module:: settings
   :synopsis: Application settings for your application. This imports merkabah base settings and
        lets you override here for your application. Also you can create a settingslocal
        file for deployment settings.

.. moduleauthor:: Blaine Garrett <blaine@blainegarrett.com>

"""
import os.path
TEMPLATE_DIRS = []

try:
    from merkabah import settings as merkabah_settings
except ImportError:
    merkabah_settings = None

if merkabah_settings:
    for setting in dir(merkabah_settings):
        globals()[setting.upper()] = getattr(merkabah_settings, setting)

PROJECT_DIR = os.path.dirname(__file__) # this is not Django setting.
DEBUG = False
TEMPLATE_DIRS += (os.path.join(PROJECT_DIR, 'templates'), )
INSTALLED_APPS = ('merkabah', 'plugins.blog', 'home') # Note: Plugins need to appear first here

DEFAULT_GS_BUCKET_NAME = 'blaine-garrett'

APPEND_SLASH = True

MIDDLEWARE_CLASSES = (
    'gaesessions.DjangoSessionMiddleware', # located in merkabah.lib - MUST BE FIRST
    'django.middleware.common.CommonMiddleware',
    'merkabah.core.auth.middleware.AuthenticationMiddleware',

    #'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
)

###############################
# Session and Auth Settings
###############################
# Note if the AUTHENTICATION_BACKENDS are not defined, it might try to use default django ones
#    wich result in the confusing error: ImproperlyConfigured: You haven't set the database ENGINE setting yet.
COOKIE_KEY = '12345678901234x678901234567x901234567890' #os.urandom(64)
AUTHENTICATION_BACKENDS = (
    'merkabah.core.auth.services.local_password.backends.LocalPasswordAuthenticationBackend',
)


###############################
# Installed Plugins
###############################
INSTALLED_PLUGINS = ('artwork', 'blog')
PLUGIN_PATH = 'plugins'
plugin_settings = {}

###############################
# Installation Properties
###############################
MERKABAH_ADMIN_URL = 'madmin/'
MERKABAH_PATH = 'merkabah/' # Used for template loaders, etc

###############################
# Admin Structure
###############################
#TODO: Make this DS driven?
o0 = {'title' :'Dashboard', 'icon' : 'icon-home', 'link' : '/', 'sub_items': []}
o1 = {'title' :'Blog', 'icon' : 'icon-book', 'link' : '/plugin/blog/',
    'sub_items': [
        {'title' :'Dashboard', 'icon' : 'icon-dashboard', 'link' : '/plugin/blog/'}, 
        {'title' :'Posts', 'icon' : 'icon-book', 'link' : '/plugin/blog/posts/'}, 
        {'title' :'Categories', 'icon' : 'icon-book', 'link' : '/plugin/blog/categories/'}, 
        {'title' :'Images', 'icon' : 'icon-book', 'link' : '/plugin/blog/images/'},
    ]}
ADMIN_PRIMARY_MENU = [o0, o1]

###############################
# Local Development Overrides
###############################
# Import local settings
try:
    import settingslocal
except ImportError:
    settingslocal = None

if settingslocal:
    for setting in dir(settingslocal):
        globals()[setting.upper()] = getattr(settingslocal, setting)
