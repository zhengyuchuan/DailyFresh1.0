from django.contrib import admin
from goods.models import ProductCategory, ProductBanner, PromotionPc, ProductSKU, Products, TypeShow

# Register your models here.
admin.site.register([ProductCategory, ProductBanner, PromotionPc, Products, ProductSKU, TypeShow])