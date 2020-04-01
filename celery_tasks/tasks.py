from DailyFresh import settings
from django.core.mail import send_mail
from celery import Celery
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DailyFresh.settings")
# 使用redis作为broker
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/8')


# 定义任务函数,celery不能传User对象进去
@app.task
def send_active_email(user_email, token):
    html_msg = """<h1>尊敬的用户您好，您已成功注册天天生鲜账户，请于24小时之内点击以下链接激活您的账户<h1><br><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>""" % (token, token)
    subject = '天天生鲜账户激活'
    received_list = [user_email, ]
    send_mail(subject=subject, message='', html_message=html_msg, from_email=settings.EMAIL_HOST_USER,
              recipient_list=received_list)
