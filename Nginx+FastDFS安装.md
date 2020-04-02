### 安装环境

> **Centos**
>
> 环境依赖：
>
> ```shell
> yum -y install gcc
> yum install -y pcre pcre-devel
> yum install -y zlib zlib-devel
> yum install -y openssl openssl-devel
> # 没有make的需要安装一下make
> yum install -y make
> ```

&nbsp;

### 安装配置流程

> 1.创建fastdfs目录：
>
> ```shell
> mkdir -p /fastdfs/tracker
> mkdir -p /fastdfs/storage
> mkdir -p /fastdfs/logs
> ```
>
> &nbsp;
>
> 1.下载安装libfastcomman（基础环境）
>
> ```shell
> wget https://github.com/happyfish100/libfastcommon/archive/V1.0.7.tar.gz
> tar -zxvf V1.0.7.tar.gz
> cd libfastcommon-1.0.7
> ./make.sh && ./make.sh install
> # 复制文件，解决FastDFS中lib配置文件路径问题。
> cp /usr/lib64/libfastcommon.so /usr/local/lib/libfastcommon.so
> cp /usr/lib64/libfastcommon.so /usr/lib/libfastcommon.so
> ```
>
> &nbsp;
>
> 2.下载安装FastDFS。安装完成后，默认配置文件目录为： `/etc/fdfs/`，默认命令放在 `/usr/bin/`中，以 `fdfs_`开头。
>
> ```shell
> wget https://github.com/happyfish100/fastdfs/archive/V5.05.tar.gz
> tar -zxvf V5.05.tar.gz
> cd fastdfs-5.05/
> ./make.sh && ./make.sh install
> ```
>
> &nbsp;
>
> 3.配置tracker
>
> ```shell
> # 将配置文件复制到/etc/fdfs目录下
> cd .../fastdfs-5.05/conf
> cp * /etc/fdfs/
> sudo vim tracker.conf
> ```
>
> &emsp;&emsp;&emsp;修改bath_path，配置如下：
>
> ```nginx
> base_path=/fastdfs/tracker
> ```
>
> &emsp;&emsp;&emsp;启动tracker：
>
> ```shell
> fdfs_trackerd /etc/fdfs/tracker.conf start
> ```
>
> &nbsp;
>
> 4.配置storage
>
> ```shell
> vim storage.conf
> ```
>
> &emsp;&emsp;&emsp;修改配置项，配置如下：
>
> ```nginx
> #日志目录
> base_path=/fastdfs/storage   
> #存储目录
> store_path0=/fastdfs/storage     
> #tracker节点
> tracker_server=192.168.1.4:22122
> ```
>
> &emsp;&emsp;&emsp;启动storage：
>
> ```shell
> fdfs_storaged /etc/fdfs/storage.conf start
> ```
>
> &nbsp;
>
> 5.配置client
>
> ```shell
> vim client.conf
> ```
>
> &emsp;&emsp;&emsp;配置项如下：
>
> ```shell
> #tracker节点
> tracker_server=192.168.1.4:22122
> #日志路径
> base_path=/fastdfs/logs  
> ```
>
> &nbsp;
>
> 6.安装nginx与fastdfs-nginx-module。不建议使用yum或apt直接安装nginx，因为安装fastdfs-nginx-module模块时，还需要再次编译，很麻烦。
>
> ```shell
> # 下载fastdfs-nginx-module模块
> cd /fastdfs
> wget https://github.com/happyfish100/fastdfs-nginx-module/archive/5e5f3566bbfa57418b5506aaefbe107a42c9fcb1.zip
> unzip 5e5f3566bbfa57418b5506aaefbe107a42c9fcb1.zip
> mv fastdfs-nginx-module-5e5f3566bbfa57418b5506aaefbe107a42c9fcb1 fastdfs-nginx-module
> # 下载nginx
> wget http://nginx.org/download/nginx-1.12.1.tar.gz
> tar -zxvf nginx-1.12.1.tar.gz
> # 安装nginx与fsatdfs-nginx-module
> cd nginx-1.12.1
> ./configure --prefix=/opt/nginx --sbin-path=/usr/bin/nginx --add-module=/fastdfs/fastdfs-nginx-module/src
> make
> make install
> ```
>
> &nbsp;
>
> 7.配置mod_fastdfs.conf文件
>
> ```shell
> cd /fastdfs/fastdfs-nginx-module/src
> cp mod_fastdfs.conf /etc/fdfs/
> vim /etc/fdfs/mod_fastdfs.conf
> ```
>
> &emsp;&emsp;&emsp;配置项如下：
>
> ```nginx
> connect_timeout=10 # 客户端访问文件连接超时时长（单位：秒）
> base_path=/fastdfs/tmp # 存储日志路径
> tracker_server=192.168.1.4:22122 # tracker服务IP和端口
> url_have_group_name=true # 访问链接前缀加上组名
> group_name=group1 # 和storage的groupname一一对应
> store_path0=/fastdfs/storage # 文件存储路径
> ```
>
> &nbsp;
>
> 8.配置nginx
>
> ```shell
> cd /opt/nginx/conf/
> vim nginx.conf
> ```
>
> &emsp;&emsp;&emsp;配置项如下，即访问以**group1**起始的资源时交给fastdfs-nginx-module处理：
>
> ```nginx
> # 监听域名中带有group0 到 group9 的，交给fastdfs-nginx-module模块处理
> location ~/group([0-9])/ {
> ngx_fastdfs_module;
> }
> ```
>
> &emsp;&emsp;&emsp;启动nginx：
>
> ```shell
> nginx
> ```
>
> 

&nbsp;

### 测试

> 1.上传图片
>
> ```shell
> fdfs_upload_file /etc/fdfs/client.conf ~/Desktop/test.png
> ```
>
> &emsp;&emsp;&emsp;此时会返回给我们一串字符串。
>
> ![](https://i.loli.net/2020/03/31/yD4eIRhkgSfKT12.png)
>
> 2.访问测试，浏览器输入:
>
> ```
> 192.168.1.4/group1/M00/00/00/wKgBBF6Cu4GATwTvABy5G9p0iEE119.png
> ```
>
> ![](https://i.loli.net/2020/03/31/Ci1JLFd2ny9PUbM.png)
>
> &emsp;&emsp;访问成功！

