"""
Django settings for DailyFresh project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 不需要再每次都写apps.
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&i1oj6ywa^q4s=vi*tf!xh7_zg01v9(zbnd!mt*%6#2iun)333'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 主机域名，debug模式下可以为空
ALLOWED_HOSTS = []


# Application definition
# 注册的app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # 将session存储在数据库中，具体配置看CACHE项
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',  # 富文本编辑器注册
    'haystack',  # 全文检索框架
    'cart',
    'goods',
    'order',
    'user',
]

# 中间件是有顺序的，一层包一层
MIDDLEWARE = [
    # 安全中间件，比如防止xss攻击，将http重定向到https等
    'django.middleware.security.SecurityMiddleware',
    # 使用session功能。
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 完美主义者必备，主要是对URL的重写，比如访问是/goods/12会被修饰为标准的/goods/12/
    'django.middleware.common.CommonMiddleware',
    # 通过向POST表单添加隐藏的表单字段并检查请求的正确值来增强对跨站点请求伪造的保护
    'django.middleware.csrf.CsrfViewMiddleware',
    # 验证中间件。将user代表当前登录用户的属性添加到每个传入HttpRequest对象中
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 消息中间件，启动基于cookie和session的消息支持
    'django.contrib.messages.middleware.MessageMiddleware',
    # 启动简单的点击劫持保护
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 根urls位置
ROOT_URLCONF = 'DailyFresh.urls'

# 配置模板
TEMPLATES = [
    {
        # 使用DjangoTemplates模板引擎
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 定义模板目录
        'DIRS': [os.path.join(BASE_DIR, 'apps/../templates')],
        # 是否在已安装的app中查找模板
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

WSGI_APPLICATION = 'DailyFresh.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dailyfresh',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'mysql用户名',
        'PASSWORD': 'mysql密码'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# 指定django认证系统使用的模型类
AUTH_USER_MODEL = 'user.User'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'apps/../static')
]

# 富文本编辑器配置
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'width': 500,
    'height': 400
}

# 配置Redis作为缓存
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://ip地址:6379/9',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}


# 邮件服务器配置
EMAIL_HOST = 'smtp.163.com'  # 如果是 qq 改成 smtp.qq.com
EMAIL_PORT = 465
EMAIL_HOST_USER = ''  # 在这里填入您的163邮箱账号
EMAIL_HOST_PASSWORD = ''  # 请在这里填上您自己邮箱的授权码
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_SSL = True
# 收件人看到的发件人，尖括号中的必须与上面的user一致
EMAIL_FROM = '天天生鲜<15698208195@163.com>'


# 配置celery
# celery结果返回，可用于跟踪结果
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
# celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# celery时区设置，使用TIME_ZONE
CELERY_TIMEZONE = TIME_ZONE

# 配置login_url，即登录url地址。没有登录访问用户中心时，会跳转至此地址。
LOGIN_URL = '/user/login/'

# 修改默认上传文件类
DEFAULT_FILE_STORAGE = 'fdfsservice.fdfs_service.FastDFSStorage'


# 全文搜索框架配置
HAYSTACK_CONNECTIONS = {
    'default': {
        # 使用whoosh引擎
        # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        # 使用jieba分词
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        # 索引文件路径
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}

# 当添加删除修改数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'