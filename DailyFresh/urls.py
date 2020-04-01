"""DailyFresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# django1.11：from django.conf.urls import url, include
from django.urls import include, path
from django.contrib import admin

# www.fresh.com/goods/?id=123,匹配时不匹配GET请求参数
# 命名空间namespace可以实现不同app使用相同url，命名空间提供了区分这些URL的方法
# 使用时 user：index
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('user/', include(('user.urls','user'), namespace='user')),
    path('cart/', include(('cart.urls', 'cart'),namespace='cart')),
    # 使用haystack搜索框架
    path('search/', include('haystack.urls')),
    path('', include(('goods.urls', 'goods'), namespace='goods')),
]

