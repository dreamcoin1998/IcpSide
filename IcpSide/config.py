# 项目各密码配置文件
# 放置于项目根目录下

### django APP秘钥
SECRET_KEY = '-qhsgt6r3a4lb1*181+hl141#o@7@am29wa8v$^@dgp(1e)=yj'

### 邮件发送配置
# 发件人授权码
EMAIL_HOST_PASSWORD = 'xfYC4mkT2QLPuBQv'

### Celery配置
# redis的地址
BROKER_URL = 'redis://134.175.218.240:6379/6'
#celery结果返回，可用于跟踪结果
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

class my_database():
    """
    我的数据库
    """
    host = '134.175.218.240'
    port = 3306
    name = 'icpside1'
    user = 'icpside1'
    password = 'IcpSidetest'


# 腾讯云对象存储

TENCENT_SECRET_ID = "AKIDCGPL5mIvTr472jIksmQr30iFXeYIIEKA"
TENCENT_SECRET_KEY = "kEYbWFk00mIfokRzHK6d083j9TXUDl37"
TENCENT_REGION = "ap-shenzhen-fsi"
TENCENT_SCHEME = "https"
TENCENT_BASE_URL = "https://icpside-1258554384.cos.ap-shenzhen-fsi.myqcloud.com/"

### 腾讯云短信配置
SecretId = 'AKIDpTrzrRknZ3GCOKzNUKtBCwOZS4PTFkyv'
SecretKey = 'h7JErDI5bqse9MIxLSJtBCySfbGekZ6N'
SmsSdkAppId = "1400542632"
SignName = "橡树黑卡"
TemplateId = "1024622"
