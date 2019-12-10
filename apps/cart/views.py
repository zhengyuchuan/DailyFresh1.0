from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.http import JsonResponse
from goods.models import ProductSKU
from django_redis import get_redis_connection
from utils.mixin import LoginRequiredMixin


class CartInfo(LoginRequiredMixin, View):
    """显示购物车页面"""
    def get(self, request):
        user = request.user
        con = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        cart_dict = con.hgetall(cart_key)
        skus = []
        total_count = 0
        total_amount = 0
        for sku_id, count in cart_dict.items():
            sku = ProductSKU.objects.get(id=sku_id)
            amount = sku.price*int(count)
            sku.amount = amount
            sku.count = count
            skus.append(sku)
            total_count += int(count)
            total_amount += amount
        # 计算购物车显示的商品类的数量
        cart_count = con.hlen(cart_key)
        return render(request, 'cart.html', {'count': cart_count,
                                             'total_count': total_count,
                                             'total_amount': total_amount,
                                             'skus': skus,
                                             })


class CartADDView(View):
    """商品详情页面，列表页，点击添加至购物车，会提交至这里"""
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'error_msg': '请先登录'})
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'error_msg': '数据不完整'})
        try:
            count = int(count)
        except:
            return JsonResponse({'res': 2, 'error_msg': '商品数目出错'})
        try:
            sku = ProductSKU.objects.get(id=sku_id)
        except ProductSKU.DoesNotExist:
            return JsonResponse({'res': 3, 'error_msg': '商品不存在'})
        # 添加至购物车
        con = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        cart_count = con.hget(cart_key, sku_id)  # 如果不存在，则返回None
        if cart_count:
            count += int(cart_count)
        con.hset(cart_key, sku_id, count)
        # 计算购物车中条目数
        total_count = con.hlen(cart_key)
        return JsonResponse({'res': 4, 'error_msg': '商品添加成功', 'total_count': total_count})


class CartUpdateView(View):
    """购物车页面，商品的添加减少与手动输入"""
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'error_msg': '请先登录'})
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        if not all([sku_id, count]):
            return JsonResponse({'res': 1, 'error_msg': '数据不完整'})
        try:
            count = int(count)
        except:
            return JsonResponse({'res': 2, 'error_msg': '商品数目出错'})
        try:
            sku = ProductSKU.objects.get(id=sku_id)
        except ProductSKU.DoesNotExist:
            return JsonResponse({'res': 3, 'error_msg': '商品不存在'})
        # 添加至购物车
        con = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        con.hset(cart_key, sku_id, count)
        # 计算购物车中条目数
        total_count = con.hlen(cart_key)
        category_count = 0
        value_list = con.hvals(cart_key)
        for value in value_list:
            category_count += int(value)
        return JsonResponse({'res': 4,
                             'error_msg': '商品添加成功',
                             'count': total_count,
                             'total_count': category_count})


class CartDeleteView(View):
    """购物车页面，购物车商品的删除"""
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'error_msg': '请先登录'})
        sku_id = request.POST.get('sku_id')
        try:
            sku = ProductSKU.objects.get(id=sku_id)
        except ProductSKU.DoesNotExist:
            return JsonResponse({'res': 1, 'error_msg': '商品不存在'})
        con = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        con.hdel(cart_key, sku_id)
        category_count = 0
        value_list = con.hvals(cart_key)
        for value in value_list:
            category_count += int(value)
        return JsonResponse({'res': 2,
                             'count': category_count,
                             'error_msg': '商品删除成功'})