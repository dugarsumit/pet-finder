"""
Django settings for petfinder project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!c@f(%twnxw=arck_p-26x6al6lla%xk9sc9m1ql&5l1np))ty'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

PORT = os.environ.get('PORT', None)

ALLOWED_HOSTS = ['dugarsumit.pythonanywhere.com','localhost','pet-finder-app2.herokuapp.com']

LOGIN_REDIRECT_URL = '/pets/all'

if PORT:
    ROOT_PROJ_DIR = '/app'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'd6bagneb2co9kb',
            'USER': 'lwtzifurghzrlw',
            'PASSWORD': '462ccdad37b2d354422cb67a39c4d0f31b8e29d41f41bf05f74777b2cffba548',
            'HOST': 'ec2-54-247-96-169.eu-west-1.compute.amazonaws.com',
            'PORT': '5432',
        }
    }
else:
    ROOT_PROJ_DIR = '/home/sumit/Documents/repo/pet-finder'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'mydb',
            'USER': 'myuser',
            'PASSWORD': 'warriorclan',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# ROOT_PROJ_DIR = '/home/dugarsumit/pet-finder'

PET_PROFILE_IMG_DIR = '/img/pet-profile'

UPLOAD_DIR = ROOT_PROJ_DIR + '/petfinder/static' + PET_PROFILE_IMG_DIR
# if not os.path.exists(UPLOAD_DIR):
#     os.makedirs(UPLOAD_DIR)


ALLOWED_EXTENSION = ['jpg', 'jpeg', 'png']

MAX_UPLOAD_SIZE = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_countries',
    'pets',
    'compressor',
    'easy_thumbnails',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'petfinder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'pets/templates'),
            os.path.join(BASE_DIR, 'petfinder/templates'),
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
            ],
        },
    },
]

WSGI_APPLICATION = 'petfinder.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'dugarsumit$default',
#         'USER': 'dugarsumit',
#         'PASSWORD': 'warriorclan',
#         'HOST': 'dugarsumit.mysql.pythonanywhere-services.com',
#         'PORT': '3306',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, '../static_root')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
