from django.db import models


class BaseModel(models.Model):
    # 第一次保存当前时间，后面的时间可以手动赋值
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 字段保存时，自动保存当前时间。verbose_name控制admin界面的显示
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta():
        # 说明是一个抽象基类
        abstract = True
