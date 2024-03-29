# !/usr/bin/env python3
"""
自定义响应类

Creator: Gao Junbin
Update Time: 2021/06/21
"""

from django.http import JsonResponse
from IcpSide import settings


class Response(JsonResponse):

    code = 0
    msg = "Ok"

    def __init__(self, data=None, total=None, total_page=None, page=None, token=None, **kwargs):
        """
        @param data 这里的data是响应数据{code: 0, data: [], msg: ""}的data
        @param total 结果总数
        @param total_page 总页数
        @param page 第几页
        """
        params = {
            "code": self.code,
            "data": data if data is not None else {},  # 未传data默认为{}
            "msg": self.msg,
        }
        if total or total_page or page:
            params.update({
                "total": total,
                "totalPage": total_page,
                "page": page
            })
        # 携带token，增加headers
        if token:
            token_prefix = settings.JWT_AUTH.get("JWT_AUTH_HEADER_PREFIX")
            kwargs.update({
                "headers": {
                    "Access-Control-Expose-Headers": "Authorization",
                    "Authorization": token_prefix + " " + token,
                }
            })
        super(Response, self).__init__(params, **kwargs)


class FailedResponse(Response):

    code = 1
    msg = "失败"


class ClientErrorResponse(Response):

    code = 4000
    msg = "客户端错误"


class PasswordLengthResponse(Response):

    code = 4001
    msg = "密码长度不及8位"


class HttpMethodErrorResponse(Response):

    code = 4002
    msg = "HTTP请求方法错误"


class NotLoginResponse(Response):

    code = 4003
    msg = "用户未登录"


class CodeErrorResponse(Response):

    code = 4004
    msg = "验证码错误"


class PhoneOrEmailOccupied(Response):

    code = 4005
    msg = "手机号/邮箱已被注册"


class GetCodeTooOftenResponse(Response):

    code = 4006
    msg = "手机号/邮箱获取验证码太过频繁"


class PhoneOrEmailErrorResponse(Response):

    code = 4007
    msg = "手机号/密码不正确"


class ProductTypeErrorResponse(Response):

    code = 4008
    msg = "产品类型不存在"


class CodeOverTimeResponse(Response):

    code = 4008
    msg = "验证码过期"


class BackendErrorResponse(Response):

    code = 5000
    msg = "服务端错误"


class DataBaseErrorResponse(Response):

    code = 5001
    msg = "数据库错误"


class UsernameErrorResponse(Response):

    code = 4010
    msg = "用户名包含敏感词"


class IntroductionErrorResponse(Response):

    code = 4011
    msg = "您的介绍包含敏感词"


class ProductnameErrorResponse(Response):

    code = 4012
    msg = "产品名称包含敏感词"


class ProductinfoErrorResponse(Response):

    code = 4013
    msg = "产品介绍包含敏感词"
