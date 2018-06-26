"""
Django settings for btsbroke project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import environ

env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="9+z7)*&@q-7s$&dilq95^ue7=###2b9b3tkh9y7vnfs!evr99e")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "rest_framework",
    "tweetdb.apps.TweetDBConfig",
    "btsanalysis.apps.BTSAnalysisConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "btsbroke.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "btsbroke.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {"default": env.db(default="sqlite:///" + os.path.join(BASE_DIR, "db.sqlite3"))}

# Cache

CACHES = {"default": env.cache(default="locmemcache://")}
SESSION_ENGINE = env("SESSION_ENGINE", default="django.contrib.sessions.backends.db")

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "th"

TIME_ZONE = "Asia/Bangkok"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "WARNING", "handlers": ["gunicorn"]},
    "formatters": {"verbose": {"format": "%(levelname)s %(asctime)s %(name)s %(message)s"}},
    "handlers": {"gunicorn": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "verbose"}},
    "loggers": {
        "django": {"handlers": ["gunicorn"], "level": env("DJANGO_LOG_LEVEL", default="INFO" if DEBUG else "WARNING")},
        "gunicorn.errors": {"level": "ERROR", "handlers": ["gunicorn"], "propagate": True},
        "django.security.DisallowedHost": {"level": "ERROR", "handlers": ["gunicorn"], "propagate": False},
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

SWAGGER_SETTINGS = {"USE_SESSION_AUTH": False}

TWITTER_CONSUMER_KEY = env("TWITTER_CONSUMER_KEY", default="")
TWITTER_CONSUMER_SECRET = env("TWITTER_CONSUMER_SECRET", default="")
TWITTER_ACCESS_TOKEN = env("TWITTER_ACCESS_TOKEN", default="")
TWITTER_ACCESS_TOKEN_SECRET = env("TWITTER_ACCESS_TOKEN_SECRET", default="")
