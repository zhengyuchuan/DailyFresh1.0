from goods.models import ProductSKU
from haystack import indexes


class ProductSKUIndex(indexes.SearchIndex, indexes.Indexable):
    """每个索引里面必须有且只能有一个字段为document = True，这代表django haystack
    和搜索引擎将使用此字段的内容作为索引进行检索(primaryfield)。
    注意，如果使用一个字段设置了document = True，则一般约定此字段名为text，这是在SearchIndex类里面一贯的命名，以防止后台混乱。
    haystack 提供了use_template=True在 text 字段中，这样就允许我们使用数据模板去建立搜索引擎索引的文件，
    说得通俗点就是索引里面需要存放一些什么东西"""
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return ProductSKU

    def index_queryset(self, using=None):
        # 确定在建立索引时有些记录被索引，这里我们简单地返回所有记录
        return self.get_model().objects.all()
