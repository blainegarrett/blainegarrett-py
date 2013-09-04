'''
Application Settings and default overrides
'''
import os.path

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
INSTALLED_APPS = ('merkabah', 'home')

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)


###############################
# Installed Plugins
###############################
INSTALLED_PLUGINS = ()

###############################
# Installation Properties
###############################
MERKABAH_ADMIN_URL = 'madmin/'
MERKABAH_PATH = 'merkabah/' # Used for template loaders, etc

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
