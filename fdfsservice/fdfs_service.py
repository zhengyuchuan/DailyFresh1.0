from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client


class FastDFSStorage(Storage):
    def __init__(self):
        print("chushihua")
    # 必须返回一个file对象
    def _open(self, name):
        pass

    # 如果给定的名称引用的文件已经存在于存储系统中返回True，如果名称是适用于一个新的文件返回False。
    def exists(self, name):
        return False

    # 应该返回保存的文件名的实际名称（通常是name 传入的名称，但是如果存储需要更改文件名，则返回新名称）
    def _save(self, name, content):
        # 创建client对象
        client = Fdfs_client('./fdfsservice/client.conf')
        # 上传至fastdfs系统中
        up_load_result = client.upload_appender_by_buffer(content.read())
        # return dict {
        #     'Group name'      : group_name,
        #     'Remote file_id'  : remote_file_id,
        #     'Status'          : 'Upload successed.',
        #     'Local file name' : '',
        #     'Uploaded size'   : upload_size,
        #     'Storage IP'      : storage_ip
        # } if success else None
        if up_load_result.get('Status') != 'Upload successed.':
            raise Exception('上传文件失败')
        file_name = up_load_result.get('Remote file_id')
        return file_name

    def url(self, name):
        return 