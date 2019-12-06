from django.shortcuts import render, redirect, reverse
from goods.models import ProductCategory, ProductSKU
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def goods(request):
    return render(request, 'index.html')


def goods_list(request, product_category_id, page_number):
    # 查询出当前请求的商品类
    try:
        category_obj = ProductCategory.objects.get(id=product_category_id)
    except ProductCategory.DoesNotExist:
        return redirect(reverse('goods:index'))
    sort = request.GET.get('sort')
    # 获取当前页的查询的内容
    if sort == 'price':
        object_list = ProductSKU.objects.filter(type=category_obj).order_by('price')
    elif sort == 'sales':
        object_list = ProductSKU.objects.filter(type=category_obj).order_by('-sales')
    else:
        sort = 'default'
        object_list = ProductSKU.objects.filter(type=category_obj).order_by('-id')
    paginator = Paginator(object_list, 1)
    try:
        current_page = int(page_number)
    except:
        current_page = 1
    if current_page > paginator.num_pages:
        current_page = 1
    # 查询出当前类下的商品sku，然后给当前类动态增加属性，以便区分商品类
    paginator.object_list = paginator.page(current_page)
    # 返回分页之后的总页数
    num_page = paginator.page_range
    # todo：页码控制
    # 如果页数小于等于5页，则显示所有页码
    # 如果页数大于5页，当前页在前三页，显示前5页
    # 如果页数大于5页，当前页在后三页，显示后5页
    # 如果页数大于5页，当前页在前三页与后三页之间，显示当前页+前两页+后两页
    if len(num_page) > 5:
        if current_page <= 3:
            num_page = range(1, 6)
        elif current_page >= len(num_page)-3:
            num_page = range(len(num_page)-4, len(num_page)+1)
        else:
            num_page = range(current_page-2, current_page+2)

    paginator.number = current_page
    new_product = ProductSKU.objects.filter(type=category_obj).order_by('-create_time')[:2]
    return render(request, 'list.html', {'page': paginator,
                                         'sort': sort,
                                         'show_nums': num_page,
                                         'new_product': new_product,
                                         'category_obj': category_obj,
                                         })


def detail(request, detail_id):
    product_sku = ProductSKU.objects.get(id=detail_id)
    return render(request, 'detail.html', {'product': product_sku})
