# !/usr/bin/env python3
"""
自定义响应类

Creator: Gao Junbin
Update Time: 2021/06/21
"""

from django.http import JsonResponse


class Response(JsonResponse):

    code = 0
    msg = "Ok"

    def __init__(self, data=None, total=None, total_page=None, page=None, **kwargs):
        """
        @param data 这里的data是响应数据{code: 0, data: [], msg: ""}的data
        @param total 结果总数
        @param total_page 总页数
        @param page 第几页
        """
        params = {
            "code": self.code,
            "data": data if data else {},  # 未传data默认为{}
            "msg": self.msg,
        }
        if total or total_page or page:
            params.update({
                "total": total,
                "totalPage": total_page,
                "page": page
            })
        super(Response, self).__init__(params, **kwargs)


class FailedResponse(Response):

    code = 1
    msg = "失败"


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


class BackendErrorResponse(Response):

    code = 5000
    msg = "服务端错误"


class DataBaseErrorResponse(Response):

    code = 5001
    msg = "数据库错误"

