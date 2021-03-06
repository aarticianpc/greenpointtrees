"""
Django settings for superbook project.
For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import os
#canhhs added this
OSCAR_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from oscar import OSCAR_MAIN_TEMPLATE_DIR
from oscar import get_core_apps
from oscar.defaults import *


# Build paths inside the project like this: BASE_DIR / "directory"
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIRS = [str(BASE_DIR / 'templates'), ]
STATICFILES_DIRS = [str(BASE_DIR / 'statics/'), ]
# STATICFILES_DIRS = []
# print 'canhkaka', STATICFILES_DIRS
# Use 12factor inspired environment variables or from a file
import environ
env = environ.Env()
# Ideally move env file should be outside the git repo
# i.e. BASE_DIR.parent.parent
env_file = BASE_DIR.parent / 'local.env'
if env_file.is_file():
    environ.Env.read_env(str(env_file))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Turn off debug while imported by Celery with a workaround
# See http://stackoverflow.com/a/4806384
import sys
if "celery" in sys.argv[0]:
    DEBUG = False

# Application definition

INSTALLED_APPS = [
    'django_admin_bootstrapped',
    'crispy_forms',
    #canhhs
    'django.contrib.sites', 
    'django.contrib.flatpages',
    'compressor',
    'widget_tweaks',
    'paypal',
    #end canhhs
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]+ get_core_apps()

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #canhhs added
    'oscar.apps.basket.middleware.BasketMiddleware', 
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #end canhhs
    
)


AUTHENTICATION_BACKENDS = (
    'oscar.apps.customer.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}


ROOT_URLCONF = 'superbook.urls'



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(OSCAR_BASE_DIR, 'templates'),
            OSCAR_MAIN_TEMPLATE_DIR
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'oscar.apps.search.context_processors.search_form',
                'oscar.apps.promotions.context_processors.promotions',
                'oscar.apps.checkout.context_processors.checkout',
                'oscar.apps.customer.notifications.context_processors.notifications',
                'oscar.core.context_processors.metadata',
            ],
        },
    },
]

WSGI_APPLICATION = 'superbook.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in
    # os.environ
    'default': env.db(),
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/uploads/'
#canhhs
PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'uploads')

# Crispy Form Theme - Bootstrap 3
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# For Bootstrap 3, change error alert to 'danger'
from django.contrib import messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# Django Debug Toolbar
if DEBUG:
    INSTALLED_APPS += (
       # 'debug_toolbar.apps.DebugToolbarConfig',
       )

FIXTURE_DIRS = '/fixtures'


# PAYPAL_API_USERNAME = 'canhhs91_api1.gmail.com'
# PAYPAL_API_PASSWORD = 'QS8S7PCTVJPRJVRB'
# PAYPAL_API_SIGNATURE = 'ArC72r3j1fs1tcJLuAukRJqngnhVA4uWJKg3LbYxGXZE2Kz25txF.myF'

#canhhs
# PAYPAL_API_USERNAME = 'canhhs91-facilitator_api1.gmail.com'
# PAYPAL_API_PASSWORD = 'DPCFFE3J4QRESJNF'
# PAYPAL_API_SIGNATURE = 'AFcWxV21C7fd0v3bYYYRCpSSRl31Ag7zVA2tWWA96x4iGnEEEr7cNvvI'
PAYPAL_API_USERNAME = 'greenpointtrees_api1.gmail.com'
PAYPAL_API_PASSWORD = 'VDNU6UHWPNY9WTS3'
PAYPAL_API_SIGNATURE = 'AXEjJsnGKyuWuxuPt4rCEoDJRjKhACThadgdiwX-CcojBwYe.UjG80At'
# PAYPAL_API_USERNAME = 'canhhs91_api1.gmail.com'
# PAYPAL_API_PASSWORD = 'QS8S7PCTVJPRJVRB'
# PAYPAL_API_SIGNATURE = 'ArC72r3j1fs1tcJLuAukRJqngnhVA4uWJKg3LbYxGXZE2Kz25txF.myF'
PAYPAL_CALLBACK_HTTPS=True
PAYPAL_SOLUTION_TYPE='Sole'  #does not need create paypal acc
PAYPAL_LANDING_PAGE = 'Billing'
PAYPAL_BRAND_NAME = 'Green Point Trees'
PAYPAL_SANDBOX_MODE=False
PAYPAL_CURRENCY='USD'
PAYPAL_LOCALE= 'US'
# PAYPAL_HEADER_IMG = 'http://www.greenpointtrees.nyc/static/site/img/home-banner.jpg'

THUMBNAIL_FORMAT='PNG'