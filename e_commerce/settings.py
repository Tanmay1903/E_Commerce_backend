import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR=os.path.join(BASE_DIR,'media')
STATIC_DIR=os.path.join(BASE_DIR,'static')


SECRET_KEY = '_!9q0$kh^(fwb4%dia(wcyc*%@&g!&(a^3p*whh4(d!8$=!6r2'

DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_mongoengine',
    'rest_framework.authentication',
    'django_mongoengine.mongo_auth',
    'django_mongoengine.mongo_admin',
    'django_mongoengine',
    'Users',
    'Product',
    'Review',
]

AUTH_USER_MODEL = ('mongo_auth.MongoUser')

MONGOENGINE_USER_DOCUMENT = 'Users.models.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'e_commerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'e_commerce.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'django_mongoengine.mongo_auth.backends.MongoEngineBackend',

)
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
REST_FRAMEWORK = {
        "DEFAULT_AUTHENTICATION_CLASSES" : (
            'rest_framework.authentication.SessionAuthentication',
        )
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MONGODB_DATABASES = {
    "default": {
        "name": "E_commerce",
        "host": "mongodb+srv://Tanmay1903:Tanmaymongodb@intern-9eye-at0b4.mongodb.net/E_commerce?retryWrites=true&w=majority",
        "password": "Tanmaymongodb",
        "username": "Tanmay1903",
        "tz_aware": True, # if you using timezones in django (USE_TZ = True)
    },
}
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    '/E_Commerce_backend/static/',
]
STATIC_ROOT = STATIC_DIR
MEDIA_ROOT=MEDIA_DIR
MEDIA_URL='/media/'
