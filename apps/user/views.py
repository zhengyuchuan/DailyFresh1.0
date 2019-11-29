from django.shortcuts import render,HttpResponse,redirect,reverse
from django.views.generic import View
from user.models import User
import re
from itsdangerous import TimedJSONWebSignatureSerializer
from DailyFresh import settings
from celery_tasks.tasks import send_active_email


# 使用类视图
class Register(View):
    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):
        user = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        agreement = request.POST.get('allow')
        if not all([user, password, email, agreement]):
            return render(request, 'user/register.html', {'error_msg': '输入不能为空'})
        if User.objects.filter(username=user):
            return render(request, 'user/register.html', {'error_msg': '用户名已存在'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'user/register.html', {'error_msg': '请输入正确的邮箱格式'})
        user_obj = User.objects.create_user(username=user, email=email, password=password)
        user_obj.is_active = False
        user_obj.save()
        # 生成具有过期时间的签名
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
        token = serializer.dumps({'verify': user_obj.id})
        token = token.decode('utf-8')
        # 使用celery任务函数
        send_active_email.delay(user_obj, token)
        return render(request, 'user/login.html')


def login(request):
    return render(request, 'user/login.html')


class Active(View):
    def get(self, request, token):
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['verify']
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse("激活链接已过期")