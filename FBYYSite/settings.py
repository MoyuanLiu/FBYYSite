"""
Django settings for FBYYSite project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q-g3f3^+c-@!e2u8#k6bnbk$!&=5=ha*z#mct-7*=bk&iy^2yh'

# SECURITY WARNING: don't run with debug turned on in production!
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
    'SiteLogin',
    'UserManage',
    'DataManage',
    'PermissionManage'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'FBYYSite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/')],
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

WSGI_APPLICATION = 'FBYYSite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fbyydb',
		'USER': 'root',
		'PASSWORD':'FBYYroot',
		'HOST':'fbyydata',
		'PORT':'3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# log settings
# 日志的文字日志级别,由低到高分别为：DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL
# 日志的数字日志级别,由低到高分别为: 10 -> 20 -> 30 -> 40 -> 50
# formatters: 指定输出的格式，被handler使用
# handlers：实际上来处理日志记录的地方。指定输出到控制台还是文件中还是其他..，以及输出的方式。被logger引用
# loggers： 指定django中的每个模块使用哪个handlers。以及日志输出的级别
# filters: 是在信息从logger传递到handler的过程中实施一些过滤行为,没有默认情况: 任何达到log level的日志信息都会被处理
# 注意：日志的输出级别是由loggers中的每个模块中level选项定义。如果没有配置，那么默认为warning级别



LOGGING = {
 'version': 1,
 'disable_existing_loggers': True,
 'formatters': {#日志格式
 'standard': {
  'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
 },
 'filters': {#过滤器
 'require_debug_false': {
  '()': 'django.utils.log.RequireDebugFalse',
  }
 },
 'handlers': {#处理器
 'debug': {#记录到日志文件(需要创建对应的目录，否则会出错)
  'level':'INFO',
  'class':'logging.handlers.RotatingFileHandler',
  'filename': os.path.join(BASE_DIR, "LogFile",'debug.log'),#日志输出文件
  'maxBytes':1024*1024*5,#文件大小
  'backupCount': 5,#备份份数
  'formatter':'standard',#使用哪种formatters日志格式
 },
 'console':{#输出到控制台
  'level': 'INFO',
  'class': 'logging.StreamHandler',
  'formatter': 'standard',
 },
 },
 'loggers': {#logging管理器
 'django': {
  'handlers': ['console','debug'],
  'level': 'DEBUG',
  'propagate': False
 },
 'django.request': {
  'handlers': ['debug'],
  'level': 'INFO',
  'propagate': True,
 },
 }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '384848522@qq.com'
EMAIL_HOST_PASSWORD = 'semovtfxjwyebgig'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DEFAULT_CHARSET = 'UTF-8'
