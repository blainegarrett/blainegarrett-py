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
DEBUG=False
TEMPLATE_DIRS += ( os.path.join(PROJECT_DIR, "templates"),)
INSTALLED_APPS = ('merkabah')

###############################
# Installed Plugins
###############################
INSTALLED_PLUGINS = ('blogs')

###############################
# Installation Properties
###############################
MERKABAH_ADMIN_URL = 'madmin/'

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