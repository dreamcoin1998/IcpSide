# 开发环境搭建

```shell
# 创建虚拟环境
virtualenv venv
# 根目录下
pip install -r requirements.txt
```

# 运行
**打开第一个终端**

```shell
python manage.py runserver
```
输出django后台日志和错误信息

**打开第二个终端**
```shell
Celery -A IcpSide worker -l info -P eventlet
```
输出任务队列任务执行状态
