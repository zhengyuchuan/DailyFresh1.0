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
# from django.conf.urls import url
from django.urls import re_path, path
from apps.user import views


urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    re_path('active/(?P<token>.*)/', views.Active.as_view(), name='active'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('user_center/', views.UserCenter.as_view(), name='user_center'),
    path('user_address/', views.Useraddress.as_view(), name='user_address'),
    re_path('user_order/(\d*)/', views.UserOrder.as_view(), name='user_order'),
    path('order_verify/', views.UserOrderVerify.as_view(), name='order_verify'),
    path('order_commit/', views.UserOrderCommit.as_view(), name='order_commit'),
    path('order_pay/', views.UserOrderPay.as_view(), name='order_pay'),
    path('order_pay_check/', views.OrderPayCheck.as_view(), name='order_pay_check'),
    path('order_direct_purchase/', views.UserDirectPurchase.as_view(), name='order_direct_purchase')
]


