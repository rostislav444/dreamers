import os
from pathlib import Path

from django.core.files.storage import default_storage
from dotenv import load_dotenv, dotenv_values

from .storage import S3Storage, CustomFileSystemStorage

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATICFILE_DIR = os.path.join(BASE_DIR, 'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

load_dotenv()
env = dotenv_values(".env")

# print(os.path.join(BASE_DIR, '.env'))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-zg@1y0y6nkmrhmeigva!jl@sxe)1=vsu96dt5h4(@6)ffel^60'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env['DEBUG']
PRODUCTION = env['PRODUCTION']
print('DEBUG', DEBUG)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.abstract.apps.AbstractConfig',
    'apps.product.apps.ProductConfig',
    'apps.order.apps.OrderConfig',
    'apps.category.apps.CategoryConfig',
    'apps.catalogue.apps.CatalogueConfig',
    'apps.attribute.apps.AttributeConfig',
    'apps.newpost.apps.NewpostConfig',
    'apps.core.apps.CoreConfig',
    'apps.material.apps.MaterialConfig',
    'rest_framework',
    'mptt',
    'corsheaders',
    'colorfield',
    'django_admin_inline_paginator',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env['DB_NAME'],
        'USER': env['DB_USER'],
        'PASSWORD': env['DB_PASSWORD'],
        'HOST': '0.0.0.0',
        'PORT': env.get('DB_PORT', 5432)
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    STATICFILE_DIR,
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://ecommerce-backend:8000"
]

AWS_BUCKET_URL = env['AWS_BUCKET_URL']
AWS_ACCESS_KEY_ID = env['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = env['AWS_SECRET_ACCESS_KEY']

FILE_STORAGE = CustomFileSystemStorage if DEBUG else S3Storage


STATIC_ROOT = os.path.join(BASE_DIR, 'static_root/')
MEDIA_URL = '/media/' if PRODUCTION else AWS_BUCKET_URL
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
