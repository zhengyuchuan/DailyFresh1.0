# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-28 01:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('image', models.ImageField(upload_to='banner', verbose_name='轮播图片')),
                ('index', models.SmallIntegerField(default=0, verbose_name='轮播索引')),
            ],
            options={
                'verbose_name': '首页轮播商品',
                'verbose_name_plural': '首页轮播商品',
                'db_table': 'product_banner',
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('category_name', models.CharField(max_length=20, verbose_name='分类名称')),
                ('logo', models.CharField(max_length=10, verbose_name='标识')),
                ('image', models.ImageField(upload_to='category', verbose_name='商品类型图片')),
            ],
            options={
                'verbose_name': '商品分类',
                'verbose_name_plural': '商品分类',
                'db_table': 'product_category',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('image', models.ImageField(upload_to='products', verbose_name='商品图片路径')),
            ],
            options={
                'verbose_name': '商品图片',
                'verbose_name_plural': '商品图片',
                'db_table': 'product_image',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=20, verbose_name='商品SPU名称')),
                ('detail', tinymce.models.HTMLField(blank=True, verbose_name='商品详情')),
            ],
            options={
                'verbose_name': '商品SPU',
                'verbose_name_plural': '商品SPU',
                'db_table': 'products',
            },
        ),
        migrations.CreateModel(
            name='ProductSKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=50, verbose_name='商品名称')),
                ('desc', models.CharField(max_length=100, verbose_name='商品简介')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('unite', models.CharField(max_length=20, verbose_name='单位')),
                ('image', models.ImageField(upload_to='products', verbose_name='商品图片')),
                ('inventory', models.IntegerField(default=1, verbose_name='库存')),
                ('sales', models.IntegerField(default=0, verbose_name='销量')),
                ('status', models.SmallIntegerField(choices=[(0, '下线'), (1, '上线')], default=1, verbose_name='商品状态')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Products', verbose_name='商品SPU')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.ProductCategory', verbose_name='所属分类')),
            ],
            options={
                'verbose_name': '商品',
                'verbose_name_plural': '商品',
                'db_table': 'product_sku',
            },
        ),
        migrations.CreateModel(
            name='PromotionPc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=20, verbose_name='活动名称')),
                ('image', models.ImageField(upload_to='banner', verbose_name='活动图片')),
                ('url', models.URLField(verbose_name='互动连接')),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
            ],
            options={
                'verbose_name': '促销活动',
                'verbose_name_plural': '促销活动',
                'db_table': 'promotion',
            },
        ),
        migrations.CreateModel(
            name='TypeShow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('display_type', models.SmallIntegerField(choices=[(0, '文字'), (1, '图片')], default=1, verbose_name='展示类型')),
                ('index', models.SmallIntegerField(default=0, verbose_name='展示顺序')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.ProductSKU', verbose_name='商品SKU')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.ProductCategory', verbose_name='商品种类')),
            ],
            options={
                'verbose_name': '分类商品展示',
                'verbose_name_plural': '分类商品展示',
                'db_table': 'product_show',
            },
        ),
        migrations.AddField(
            model_name='productimage',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.ProductSKU', verbose_name='商品'),
        ),
        migrations.AddField(
            model_name='productbanner',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.ProductSKU', verbose_name='商品'),
        ),
    ]
