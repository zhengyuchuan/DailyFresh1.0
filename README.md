### 基于Django3.0实现的生鲜商城项目

> **引言**：此项目原是黑马的天天生鲜项目，本人仅用于个人学习，不作他用。此项目是一个B2C模式的生鲜产品商城项目，使用的是最新的**Django3.0.4**web框架，主要模块有：**用户登录注册模块**、**商品模块**、**购物车模块**、**订单模块**。主要用到的技术有**whoosh搜索引擎**、**celery异步任务队列**、**nginx**、**FastDFS分布式文件系统**等。

&nbsp;

---

#### 1.python依赖包

> ```shell
> pip install -r requirements.txt
> ```

&nbsp;

#### 2.第三方SDK支持

> - 支付宝沙箱：这里使用的是支付宝的沙箱环境，仅用于测试。使用之前，需要先使用**openSSL**工具生成密钥对，将自己生成的公钥填入支付宝沙箱中的应用公钥。然后将生成的私钥和支付宝的公钥，放到[app_private_key](https://github.com/zhengyuchuan/iHome1.0/blob/master/ihome/api_1/Alipay_keys/app_private_key.pem)与[alipay_public_key](https://github.com/zhengyuchuan/iHome1.0/blob/master/ihome/api_1/Alipay_keys/alipay_public_key.pem)两个文件中。

&nbsp;

#### 3.服务支持

> - openSSL：生成RSA密钥对，用于支付宝沙箱环境
> - FastDFS：用于存储商品图片。安装说明请看：[nginx+fastdfs安装]()
> - Nginx：结合FastDFS，可实现http访问图片功能。后续还可以实现动静分离及负载均衡。
> - jieba：中文分词技术，用于替换whoosh搜索引擎自带分词器。替换过程请看：[使用jieba分词]()
> - MySQL：提供数据库支持。
> - Redis：提供缓存支持。

&nbsp;

#### 4.setting.py配置

> ```python
> # 数据库配置
> DATABASES = {
>     'default': {
>         'ENGINE': 'django.db.backends.mysql',
>         'NAME': 'dailyfresh',
>         'HOST': '127.0.0.1',
>         'PORT': 3306,
>         'USER': 'mysql用户名',
>         'PASSWORD': 'mysql密码'
>     }
> }
> 
> # 配置Redis作为缓存
> CACHES = {
>     'default': {
>         'BACKEND': 'django_redis.cache.RedisCache',
>         'LOCATION': 'redis://ip地址:6379/9',
>         "OPTIONS": {
>             "CLIENT_CLASS": "django_redis.client.DefaultClient",
>         },
>     },
> }
> 
> # 邮件服务器配置
> EMAIL_HOST = 'smtp.163.com'  # 如果是 qq 改成 smtp.qq.com
> EMAIL_PORT = 465
> EMAIL_HOST_USER = ''  # 在这里填入您的163邮箱账号
> EMAIL_HOST_PASSWORD = ''  # 请在这里填上您自己邮箱的授权码
> DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
> EMAIL_USE_SSL = True
> # 收件人看到的发件人，尖括号中的必须与上面的user一致
> EMAIL_FROM = '天天生鲜<156********@163.com>'
> 
> # 配置celery
> # celery结果返回，可用于跟踪结果
> CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
> ```
>
> 



#### 5.项目启动

> ```shell
> # nginx、fastdfs启动方式在安装说明内，确保已启动
> # 确保redis、mysql已启动，并在mysql内建立dailyfresh数据库
> create database dailyfresh charset=utf8;
> 
> # 开启celery
> cd /Users/zhengyuchuan/PycharmProjects/DailyFresh
> celery -A  celery_tasks worker -l info
> # 生成迁移文件（数据库内容可在django后台管理页面导入，可使用/static/products目录内商品图片）
> python manage.py makemigrations
> # 建立表结构
> python manage.py migrate
> # 启动项目
> python manage.py runserver
> ```
>
> 



---

#### 参考链接

- [Django3.0.4文档](https://docs.djangoproject.com/zh-hans/3.0/)
- [Django-redis文档](https://django-redis-chs.readthedocs.io/zh_CN/latest/)
- [nginx&&FastDFS实现分布式文件服务器](https://mp.weixin.qq.com/s/6ctV0RMj9_vKswm6dZCVYQ)

