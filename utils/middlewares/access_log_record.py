"""
访问日志记录中间件

Creator: Gao Junbin
Update: 2021-07-01
"""

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object
from access_log.models import AccessLog
from auth_user.models import User


class AccessLogRecord(MiddlewareMixin):

    def process_request(self, request):
        """
        获取并记录访问日志
        """
        # 获取Ip
        ip = request.META.get("REMOTE_ADDR")
        # 获取url
        url = request.path_info
        # 从cookie中获取user
        userid = request.COOKIES.get("userid")
        user_obj = None
        if userid:
            # 获取user对象
            user = User.objects.filter(pk=int(userid))
            # 如果能找到user，则保存user对象
            if user.count() == 1:
                user_obj = user[0]
        # 储存access_log
        access_log_obj = AccessLog()
        access_log_obj.ip = ip
        access_log_obj.url = url
        access_log_obj.user = user_obj
        access_log_obj.save()

    def process_response(self, request, response):
        return response
