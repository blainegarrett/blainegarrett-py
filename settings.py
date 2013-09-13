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
TEMPLATE_DIRS += (os.path.join(PROJECT_DIR, "templates"), )
INSTALLED_APPS = ('merkabah', 'plugins.blog', 'home') # Note: Plugins need to appear first here

APPEND_SLASH = True

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
)


###############################
# Installed Plugins
###############################
INSTALLED_PLUGINS = ('blog')

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
o1 = {'title' :'Blog', 'icon' : 'icon-book', 'link' : '/plugin/blog', 'sub_items': []}
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
