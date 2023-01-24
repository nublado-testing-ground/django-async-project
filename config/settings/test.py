from .base import *

TESTING = True
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ["DATABASE_NAME"],
        "USER": os.environ["DATABASE_USER"],
        "PASSWORD": os.environ["DATABASE_PWD"],
        "HOST": "localhost",
        "PORT": "",
        "TEST": {
            "NAME": os.environ["TEST_DATABASE_NAME"],
        }
    }
}

DJANGO_TELEGRAM['mode'] = BOT_MODE_POLLING
