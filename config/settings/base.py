import os
import sys
from pathlib import Path

from django.utils.translation import gettext_noop as _

# Get key env values from the virtual environment.
def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable.".format(var_name)
        raise Exception(error_msg)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Subdirectory for app bundles.
APP_DIR = "django-async"
sys.path.append(os.path.join(BASE_DIR, APP_DIR))

APPS_ROOT = BASE_DIR / APP_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['127.0.0.1','localhost']

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'core.apps.CoreConfig',
    'users.apps.UserConfig',
    'django_telegram.apps.DjangoTelegramConfig',
    'bot_misc.apps.BotMiscConfig',
    'group_admin.apps.GroupAdminConfig',
    'group_points.apps.GroupPointsConfig',
    'group_notes.apps.GroupNotesConfig',
    'test_bot.apps.TestBotConfig',
    'project_app.apps.ProjectAppConfig'
]

THIRD_PARTY_APPS = []

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

AUTH_USER_MODEL = 'users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
EN = "en"
ES = "es"
LANGUAGE_CODE = EN
LANGUAGES = [
    (EN, _("English")),
    (ES, _("Spanish")),
]
LANGUAGES_DICT = dict(LANGUAGES)
LOCALE_PATHS = (
    APPS_ROOT / "project_app" / "locale",
)

TIME_ZONE = 'UTC'
USE_I18N = True
# USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / APP_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging
LOGGING = {
    'version': 1,
    # Version of logging
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # Handlers
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'nublado-debug.log',
        },
        'console': {
            'level': 'INFO',
            # 'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    # Loggers
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'django-debug': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

MON, TUE, WED, THU, FRI, SAT, SUN = range(7)
WEEKDAYS = [
    _("Monday"), _("Tuesday"), _("Wednesday"), _("Thursday"),
    _("Friday"), _("Saturday"), _("Sunday")
]
WEEKDAYS_ABBR = [
    _("Mon."), _("Tue."), _("Wed."), _("Thu."),
    _("Fri."), _("Sat."), _("Sun.")
]

# Telegram bot stuff
BOT_MODE_WEBHOOK = "webhook"
BOT_MODE_POLLING = "polling"

# Command line arg to run this bot
TEST_BOT = "testbot"
TEST_BOT_TOKEN = get_env_variable('TEST_BOT_TOKEN')
TEST_GROUP_ID = int(get_env_variable('TEST_GROUP_ID'))
TEST_REPO_ID = int(get_env_variable('TEST_REPO_ID'))
TEST_GROUP_OWNER_ID = int(get_env_variable('TEST_GROUP_OWNER_ID'))
TEST_SUDO_LIST = [
    TEST_GROUP_OWNER_ID, 
]

DJANGO_TELEGRAM = {
    'mode': BOT_MODE_WEBHOOK,
    'webhook_port': int(os.environ.get('PORT', 5000)),
    'webhook_site' : "https://djangoasync.onrender.com",
	'webhook_path' : "bot/webhook",
    'set_webhook_path': "bot/setwebhook",
    'bots': {
        TEST_BOT_TOKEN: {
            'token': TEST_BOT_TOKEN,
            'group_id': TEST_GROUP_ID,
            'repo_id': TEST_REPO_ID,
            'sudo_list': TEST_SUDO_LIST
        },
    },
    'testing': {
        'api_id': get_env_variable('TG_API_KEY'),
        'api_hash': get_env_variable('TG_API_HASH'),
        'api_session_str': get_env_variable('TG_API_SESSION_STR')
    }
}

BOT_CLI = {
    TEST_BOT: DJANGO_TELEGRAM['bots'][TEST_BOT_TOKEN]
}
