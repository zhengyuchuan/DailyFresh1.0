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
from django.conf.urls import url
from apps.user import views


urlpatterns = [
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^active/(?P<token>.*)$', views.Active.as_view(), name='active'),
    url(r'^index$', views.index, name='index'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^user_center$', views.UserCenter.as_view(), name='user_center'),
    url(r'^user_address$', views.Useraddress.as_view(), name='user_address'),
    url(r'^user_order/(\d)$', views.UserOrder.as_view(), name='user_order'),
    url(r'^order_verify$', views.UserOrderVerify.as_view(), name='order_verify'),
    url(r'^order_commit$', views.UserOrderCommit.as_view(), name='order_commit'),
    url(r'^order_pay$', views.UserOrderPay.as_view(), name='order_pay'),
    url(r'^order_pay_check$', views.OrderPayCheck.as_view(), name='order_pay_check')
]


