# fundmanager
天天基金网，基金公司以及基金经理信息爬虫


## 使用方法


### 1. 安装依赖


1.1安装环境依赖软件docker，docker-compose，python

1.2克隆代码`https://github.com/JaysonAlbert/fundmanager.git`

1.3安装依赖库,在项目根目录运行`pip install -r requirements.txt`


### 2. 启动依赖服务


在项目根目录运行`docker-compose up`

### 3. 启动爬虫


在项目根目录运行`python main.py`

### 4. 生成爬虫请求到redis


在项目根目录运行`python feedurl.py`

### 5. 查看爬取的数据
5.1 使用Another Redis Desktop Manager查看Redis中的爬虫请求

5.2 使用compass查看Mongodb中爬虫爬取的数据。
