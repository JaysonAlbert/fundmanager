# fundmanager
天天基金网，基金公司以及基金经理信息爬虫


## 使用方法


### 1. 安装依赖


1.1安装环境依赖软件docker，docker-compose，python

1.2克隆代码`https://github.com/JaysonAlbert/fundmanager.git`,并在项目根目录运行`pip install -r requirements.txt`安装依赖库


### 2. 启动依赖服务


在项目根目录运行`docker-compose up`

### 3. 启动爬虫


在项目根目录运行`python main.py`

### 4. 生成爬虫请求到redis


在项目根目录运行`python feedurl.py`
