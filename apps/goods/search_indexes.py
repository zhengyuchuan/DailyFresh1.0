from goods.models import ProductSKU
from haystack import indexes

# 定义索引类
# 指定某个类的某个数据建立索引
# 格式：索引类名+Index
class ProductSKUIndex(indexes.SearchIndex, indexes.Indexable):
    """每个索引里面必须有且只能有一个字段为document = True，这代表django haystack
    和搜索引擎将使用此字段的内容作为索引进行检索(primaryfield)。
    注意，如果使用一个字段设置了document = True，则一般约定此字段名为text，这是在SearchIndex类里面一贯的命名，以防止后台混乱。
    haystack 提供了use_template=True在 text 字段中，这样就允许我们使用数据模板去建立搜索引擎索引的文件，
    说得通俗点就是索引里面需要存放一些什么东西"""
    # use_template指定将说明放在一个文件中，需要去templates文件夹内建立文件夹search/indexes/goods/productsku_text.txt
    # 前两项固定。应用叫goods，所以第三项为goods，第四项为模型类名小写
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return ProductSKU

    # 建立索引的数据
    def index_queryset(self, using=None):
        # 确定在建立索引时有些记录被索引，这里我们简单地返回所有记录
        return self.get_model().objects.all()


# python manage.py rebuild_index 建立索引
