from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views.generic import View
from user.models import User, UserAddress
from goods.models import ProductCategory
import re
from itsdangerous import TimedJSONWebSignatureSerializer
from DailyFresh import settings
from celery_tasks.tasks import send_active_email
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django_redis import get_redis_connection


# 使用类视图
class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        user = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        agreement = request.POST.get('allow')
        if not all([user, password, email, agreement]):
            return render(request, 'register.html', {'error_msg': '输入不能为空'})
        if User.objects.filter(username=user):
            return render(request, 'register.html', {'error_msg': '用户名已存在'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'error_msg': '请输入正确的邮箱格式'})
        user_obj = User.objects.create_user(username=user, email=email, password=password)
        user_obj.is_active = False
        user_obj.save()
        # 生成具有过期时间的签名
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
        token = serializer.dumps({'verify': user_obj.id})
        token = token.decode('utf-8')
        user_email = user_obj.email
        # 使用celery任务函数,celery默认接收json格式的数据
        send_active_email.delay(user_email, token)
        return redirect(reverse('user:login'))


class Login(View):
    def get(self, request):
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            checked = ''
            username = ''
        return render(request, 'user/login.html', {'username': username, 'checked': checked})

    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        if not all([username, password]):
            return render(request, 'user/login.html', {'error_msg': '用户名或密码不能为空'})
        user_obj = authenticate(username=username, password=password)
        if not user_obj:
            return render(request, 'user/login.html', {'error_msg': '用户名或密码错误'})
        if not user_obj.is_active:
            return render(request, 'user/login.html', {'error_msg': '用户名未激活'})
        login(request, user=user_obj)
        response_url = request.GET.get('next', reverse('user:index'))
        remember = request.POST.get('remember')
        response = redirect(response_url)
        if remember == 'on':
            response.set_cookie('username', username, max_age=7*24*3600)
        else:
            response.delete_cookie('username')
        return response


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


def index(request):
    page_name = 1
    category_obj = ProductCategory.objects.all()
    return render(request, 'index.html', {'types': category_obj, 'page_name': page_name})


def logout_view(request):
    logout(request)
    return redirect(reverse('user:index'))


@login_required
def user_center(request):
    info = 1
    user = request.user
    address_obj = UserAddress.objects.get_default_addr(user=user)
    return render(request, 'user_center_info.html', {'info': info, 'address': address_obj})


class Useraddress(View):
    def get(self, request):
        site = 1
        user = request.user
        address_obj = UserAddress.objects.get_default_addr(user=user)

        return render(request, 'user_address.html', {'site': site, 'address': address_obj})

    def post(self, request):
        recipient = request.POST.get('recipient')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        if not all([recipient, address, phone]):
            error_msg = '不能为空！'
            return render(request, 'user_address.html', {'error_msg': error_msg})
        if not re.match(r'^(1[3-9])\d{9}$', phone):
            error_msg = '手机号格式错误！'
            return render(request, 'user_address.html', {'error_msg': error_msg})
        user = request.user
        address_obj = UserAddress.objects.get_default_addr(user=user)
        if address_obj:
            is_default = False
        else:
            is_default = True
        UserAddress.objects.create(user=user,
                                   recipient=recipient,
                                   address=address,
                                   contact_num=phone,
                                   is_default=is_default)
        return render(request, 'user_address.html', {'address': address_obj})


@login_required
def user_order(request):
    order = 1
    return render(request, 'user_order.html', {'order': order})