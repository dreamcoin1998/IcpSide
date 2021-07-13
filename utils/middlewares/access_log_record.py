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
from auth_user.models import Yonghu
from utils.jwt_auth.authentication import JSONWebTokenAuthentication


class AccessLogRecord(MiddlewareMixin):

    def process_request(self, request):
        """
        获取并记录访问日志
        """
        # 获取Ip
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        # try:
        #     request_ip = request.META['REMOTE_ADDR']
        # except KeyError:
        #     pass

        # try:
        #     # 反向代理后存储的IP
        #     user_ip = request.META['HTTP_X_FORWARDED_FOR']
        # except KeyError:
            # 局域网请求
            user_ip = None
        # 获取url
        url = request.path_info
        # 从cookie中获取user
        user_obj = JSONWebTokenAuthentication().authenticate(request)
        # 储存access_log
        access_log_obj = AccessLog()
        access_log_obj.ip = ip
        access_log_obj.url = url
        access_log_obj.user = user_obj if user_obj else None
        access_log_obj.save()

    def process_response(self, request, response):
        return response
