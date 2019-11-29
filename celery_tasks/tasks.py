# 使用celery
from celery import Celery
from DailyFresh import settings
from django.core.mail import send_mail
import os


# 设置环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DailyFresh.settings")
# 创建一个celery实例对象,并指定redis的ip和端口
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/0')
# 使用django的settings文件配置celery
app.config_from_object('django.conf:settings', namespace='Celery')
# Celery加载所有注册的应用
app.autodiscover_tasks()

# 定义任务函数
@app.task(bind=True)
def send_active_email(user_obj, token):
    # TODO 后续使用模板语言替换掉a标签中的href
    html_msg = """<h1>尊敬的用户您好，您已成功注册天天生鲜账户，请于24小时之内点击以下链接激活您的账户<h1><br><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>""" % (token, token)
    subject = '天天生鲜账户激活'
    received_list = [user_obj.email, ]
    send_mail(subject=subject, message='', html_message=html_msg, from_email=settings.EMAIL_HOST_USER,
              recipient_list=received_list)