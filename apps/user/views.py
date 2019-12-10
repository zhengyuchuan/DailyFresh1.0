from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views.generic import View
from user.models import User, UserAddress
from goods.models import ProductCategory,ProductBanner,PromotionPc, TypeShow, ProductSKU
from order.models import OrderInfo, OrderProduct
import re
from itsdangerous import TimedJSONWebSignatureSerializer
from DailyFresh import settings
from celery_tasks.tasks import send_active_email
from django.contrib.auth import authenticate, login, logout
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin
from django.http import JsonResponse
from datetime import datetime
from django.db import transaction


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
    banner_obj = ProductBanner.objects.all()
    promotion_obj = PromotionPc.objects.all()
    # 动态增加属性，以便区分商品类型
    for p in category_obj:
        word_show = TypeShow.objects.filter(product_type=p, display_type=0)
        pic_show = TypeShow.objects.filter(product_type=p, display_type=1)
        p.word_show = word_show
        p.pic_show = pic_show
    # 获取用户购物车内商品数量
    user = request.user
    cart_count = 0
    if user.is_authenticated:
        con = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        cart_count = con.hlen(cart_key)
    return render(request, 'index.html', {'types': category_obj,
                                          'page_name': page_name,
                                          'banners': banner_obj,
                                          'promotion': promotion_obj,
                                          'count': cart_count})


def logout_view(request):
    logout(request)
    return redirect(reverse('user:index'))


class UserCenter(LoginRequiredMixin, View):
    def get(self, request):
        info = 1
        user = request.user
        address_obj = UserAddress.objects.get_default_addr(user=user)
        # 创建StrictRedis对象
        con = get_redis_connection('default')
        history_key = 'history_%d' % user.id
        # 获取最新5条记录
        sku_id = con.lrange(history_key, 0, 4)
        product_list = []
        for i in sku_id:
            product = ProductSKU.objects.get(id=i)
            product_list.append(product)
        # 获取购物车商品类的数量
        cart_key = 'cart_%d' % user.id
        cart_count = con.hlen(cart_key)
        return render(request, 'user_center_info.html', {'info': info,
                                                         'address': address_obj,
                                                         'product_list': product_list,
                                                         'count': cart_count})


class Useraddress(LoginRequiredMixin, View):
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


class UserOrder(LoginRequiredMixin, View):
    def get(self, request):
        order = 1
        return render(request, 'user_order.html', {'order': order})

    def post(self, request):
        """TODO 订单页面渲染"""
        order = 1
        return render(request, 'user_order.html', {'order': order})


class UserOrderVerify(LoginRequiredMixin, View):
    def get(self, request):
        pass

    def post(self, request):
        sku_ids = request.POST.getlist('sku_id')
        user = request.user
        con = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        skus = []
        total_count = 0
        total_amount = 0
        for sku_id in sku_ids:
            sku = ProductSKU.objects.get(id=sku_id)
            count = con.hget(cart_key, sku_id)
            amount = sku.price*int(count)
            sku.count = count
            sku.amount = amount
            skus.append(sku)
            total_count += int(count)
            total_amount += amount
        transport_price = 10
        total_price = total_amount + transport_price
        addrs = UserAddress.objects.filter(user=user)
        sku_str = ",".join(sku_ids)
        return render(request, 'order.html', {'skus': skus,
                                              'total_count': total_count,
                                              'total_amount': total_amount,
                                              'transport_price': transport_price,
                                              'total_price': total_price,
                                              'addrs': addrs,
                                              'sku_str': sku_str})


class UserOrderCommit(View):
    """订单创建发起ajax请求"""
    @transaction.atomic
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return redirect(reverse('user:login'))
        addr_id = request.POST.get('addr_id')  # 地址id
        pay_id = request.POST.get('pay_id')  # 支付方式
        sku_str = request.POST.get('sku_str')  # 所有购买的sku商品的id
        if pay_id not in OrderInfo.PAY_METHOD_DIC.keys():
            return JsonResponse({'res': 0, 'error_msg': '非法的下单方式'})
        try:
            addr_obj = UserAddress.objects.get(id=addr_id)
        except:
            return JsonResponse({'res': 1, 'error_msg': '地址不存在'})
        # 组织订单id
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        # 运费写死
        transport_price = 10
        # 先=0，后面更改
        total_count = 0
        total_price = 0
        # 设置事务保存点
        save_id = transaction.savepoint()
        # 向订单信息表中添加记录
        order = OrderInfo.objects.create(order_id=order_id,
                                         user=user,
                                         addr=addr_obj,
                                         pay_method=pay_id,
                                         transit_price=transport_price,
                                         product_count=total_count,
                                         product_price=total_price)
        sku_ids = sku_str.split(",")
        con = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id

        for sku_id in sku_ids:
            try:
                sku = ProductSKU.objects.get(id=sku_id)
            except:
                # 事务回滚
                transaction.savepoint_rollback(save_id)
                return JsonResponse({'res': 2, 'error_msg': '商品不存在'})
            # 判断商品库存
            count = con.hget(cart_key, sku_id)
            inventory = sku.inventory
            if int(count) > inventory:
                # 事务回滚
                transaction.savepoint_rollback(save_id)
                error_msg = '%s下单量大于库存' % sku.name
                return JsonResponse({'res': 3, 'error_msg': error_msg})
            # 向订单商品sku表添加记录
            OrderProduct.objects.create(order_info=order,
                                        product=sku,
                                        count=count,
                                        price=sku.price)

            # 更新商品的库存和销量
            sku.inventory -= int(count)
            sku.sales += int(count )
            sku.save()
            # 总数量与总价格更改
            amount = sku.price*int(count)
            total_count += int(count)
            total_price += amount
        # 更改后写入订单信息表，并保存
        order.product_count = total_count
        order.product_price = total_price
        order.save()
        # 提交事务
        transaction.savepoint_commit(save_id)
        # 下单后购物车删除对应商品
        con.hdel(cart_key, *sku_ids)
        return JsonResponse({'res': 4, 'error_msg': '订单创建成功'})