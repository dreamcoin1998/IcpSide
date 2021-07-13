"""
Author: dawnerstart
Function: 验证相关信息
Time: 2021-06-26
"""
import json

from django.contrib.auth.hashers import make_password
from IcpSide.settings import EXPIRE_TIME
from auth_user.models import Yonghu, VerificationCode, Sensitives
from utils.response import Response
import datetime
from .tasks import random_str, send_code_email, send_code_phone



def register(request):
    """
    注册
    """
    # 使用POST方法
    if request.method == 'POST':
        try:
            # 提取前端数据
            data = request.body.decode('utf-8')
            data = json.loads(data)
            username_post = data.get('username')
            password_post = data.get('password')
            phone_or_email = data.get('phoneOrEmail')
            code_post = request.body.get("code")
            # 密码长度小于8
            if len(password_post) < 8:
                return Response.PasswordLengthResponse()
            password = make_password(password_post)
            # 用手机号验证
            if data.get("type") == 'phone':
                # 手机号已存在或者验证码不正确
                if Yonghu.objects.filter(phone=phone_or_email) \
                        or not VerificationCode.objects.filter(phoneOrEmail=phone_or_email, code=code_post):
                    return Response.PhoneOrEmailOccupied()
                new_user = Yonghu(username=username_post, password=password, phone=phone_or_email)
            # 用邮箱验证
            elif data.get("type") == 'email':
                # 邮箱已存在或者验证码不正确
                if (Yonghu.objects.filter(email=phone_or_email) or not VerificationCode.objects.filter(
                        phoneOrEmail=phone_or_email, code=code_post)):
                    return Response.PhoneOrEmailOccupied()
                new_user = Yonghu(username=username_post, password=password, email=phone_or_email)
            else:
                return Response.ClientErrorResponse()
            new_user.save()
            user_obj = Yonghu.objects.filter(phone=phone_or_email).first()
            data = {
                "data": user_obj.userid,
                "username": user_obj.username,
                "email": user_obj.email,
                "phone": user_obj.phone,
                "introduction": user_obj.introduction,
                "avatar": user_obj.avatar.url
            }
            # 返回json和cookie，cookie需要在90年后到期
            response = Response.Response(data=data)
            response.set_cookie('userid', user_obj.userid, expires=EXPIRE_TIME)
            return response
        # 后端错误
        except Exception as e:
            # TODO: 写日志
            return Response.BackendErrorResponse()


def code_validated(verify_obj):
    """
    验证码时间验证 是否在1分钟内
    """
    update_time_timestamp = datetime.datetime.timestamp(verify_obj.update_time)
    now = datetime.datetime.now()  # 当前时间
    now_timestamp = datetime.datetime.timestamp(now)
    if now_timestamp - update_time_timestamp < 60:
        return True
    return False


def get_phone_verification_code(request):
    """
    请求手机验证码
    """
    # 使用了POST方法
    data = request.body.decode('utf-8')
    data = json.loads(data)
    if request.method == 'POST':
        phone_post = data.get("phone")
        # 手机号已注册
        if Yonghu.objects.filter(phone=phone_post):
            return Response.PhoneOrEmailOccupied()
        # 手机号获取验证码太过频繁
        elif VerificationCode.objects.filter(phoneOrEmail=phone_post):
            # 判断时间是否在5分钟内
            verify_obj = VerificationCode.objects.filter(phoneOrEmail=phone_post).first()
            if code_validated(verify_obj):
                return Response.GetCodeTooOftenResponse()
        else:
            verify_obj = VerificationCode()
        random_code = random_str(random_length=6)
        verify_obj.code = random_code
        verify_obj.verification_type = "phone"
        verify_obj.phoneOrEmail = phone_post
        verify_obj.save()
        # 手机验证码发送
        phone_post = '+86' + phone_post
        phone_number = []
        phone_number.append(phone_post)
        template_param_set = []
        template_param_set.append(random_code)
        send_code_phone.delay(phone_number, template_param_set)
        return Response.Response()


def get_email_verification_code(request):
    """
    请求邮箱验证码
    """
    # 使用了POST方法
    data = request.body.decode('utf-8')
    data = json.loads(data)
    if request.method == 'POST':
        email_post = data.get("email")
        # 手机号已注册
        if Yonghu.objects.filter(email=email_post):
            return Response.PhoneOrEmailOccupied()
        # 手机号获取验证码太过频繁
        elif VerificationCode.objects.filter(email=email_post):
            # 判断时间是否在5分钟内
            verify_obj = VerificationCode.objects.filter(phoneOrEmail=email_post).first()
            if code_validated(verify_obj):
                return Response.GetCodeTooOftenResponse()
        # 可获取验证码
        else:
            verify_obj = VerificationCode()
        random_code = random_str(random_length=6)
        verify_obj.code = random_code
        verify_obj.verification_type = "email"
        verify_obj.phoneOrEmail = email_post
        verify_obj.save()
        # 发送邮箱验证码
        send_code_email.delay(email_post, code=random_code)
        return Response.Response()


def login_phone(request):
    """
    手机号登录
    """
    # POST方法
    if request.method == 'POST':
        # 尝试登陆
        try:
            data = request.body.decode('utf-8')
            data = json.loads(data)
            phone_post = data.get("phone")
            password_post = data.get("password")
            password = make_password(password_post)
            # 若手机号和密码正确
            if Yonghu.objects.filter(phone=phone_post, password=password):
                user_obj = Yonghu.objects.filter(phone=phone_post, password=password).first()
                result = {
                    "data": user_obj.userid,
                    "username": user_obj.username,
                    "email": user_obj.email,
                    "phone": user_obj.phone,
                    "introduction": user_obj.introduction,
                    "avatar": user_obj.avatar.url
                }
                response = Response.Response(data=result)
                response.set_cookie('userid', user_obj.userid, expires=EXPIRE_TIME)
                return response
            # 若手机号或密码不正确
            else:
                return Response.PhoneOrEmailErrorResponse()
        # 尝试登陆失败
        except:
            return Response.BackendErrorResponse()


def login_email(request):
    """
    邮箱登录
    """
    # POST方法
    if request.method == 'POST':
        # 尝试登陆
        try:
            data = request.body.decode('utf-8')
            data = json.loads(data)
            email_post = data.get("email")
            password_post = data.get("password")
            password = make_password(password_post)
            # 若手机号和密码正确
            if Yonghu.objects.filter(email=email_post, password=password):
                user_obj = Yonghu.objects.filter(email=email_post, password=password).first()
                result = {
                    "data": user_obj.userid,
                    "username": user_obj.username,
                    "email": user_obj.email,
                    "phone": user_obj.phone,
                    "introduction": user_obj.introduction,
                    "avatar": user_obj.avatar.url
                }
                response = Response.Response(data=result)
                response.set_cookie('userid', user_obj.userid, expires=EXPIRE_TIME)
                return response
            # 若手机号或密码不正确
            else:
                return Response.PhoneOrEmailErrorResponse()
        # 尝试登陆失败
        except:
            return Response.BackendErrorResponse()


def change_passswd_pnone(request):
    """
    找回密码-phone
    """
    # 使用了POST方法
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data = json.loads(data)
        phone_post = data.get("phone")
        password_post = data.get("password")
        code_post = data.get("code")
        # 验证码正确
        if VerificationCode.objects.filter(phoneOrEmail=phone_post, code=code_post):
            try:
                user_obj = Yonghu.objects.filter(phone=phone_post).first()
                user_obj.password = make_password(password_post)
                user_obj.save()
                result = {
                    "data": user_obj.userid,
                    "username": user_obj.username,
                    "email": user_obj.email,
                    "phone": user_obj.phone,
                    "introduction": user_obj.introduction,
                    "avatar": user_obj.avatar.url
                }
                response = Response.Response(data=result)
                response.set_cookie('userid', user_obj.userid, expires=EXPIRE_TIME)
                return response
            except:
                return Response.BackendErrorResponse()
        # 验证码不正确
        else:
            return Response.ClientErrorResponse()


def change_passswd_email(request):
    """
    找回密码-email
    """
    # 使用了POST方法
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data = json.loads(data)
        email_post = data.get("email")
        password_post = data.get("password")
        code_post = data.get("code")
        # 验证码正确
        if VerificationCode.objects.filter(phoneOrEmail=email_post, code=code_post):
            try:
                user_obj = Yonghu.objects.filter(email=email_post).first()
                user_obj.password = make_password(password_post)
                user_obj.save()
                result = {
                    "data": user_obj.userid,
                    "username": user_obj.username,
                    "email": user_obj.email,
                    "phone": user_obj.phone,
                    "introduction": user_obj.introduction,
                    "avatar": user_obj.avatar.url
                }
                response = Response.Response(data=result)
                response.set_cookie('userid', user_obj.userid, expires=EXPIRE_TIME)
                return response
            except:
                return Response.BackendErrorResponse()
        # 验证码不正确
        else:
            return Response.ClientErrorResponse()


def change_phone(request):
    """
    修改手机-phone
    """
    # 获取前端传来的消息
    try:
        userid_post = request.COOKIES.GET.get("userid")
        phone_post = request.GET.get("phone")
        code_post = request.GET.get("code")
        # 验证码正确
        if VerificationCode.objects.filter(phoneOrEmail=phone_post, code=code_post):
            try:
                user_obj = Yonghu.objects.filter(userid=userid_post).first()
                user_obj.phone = phone_post
                user_obj.save()
                result = {
                    "data": user_obj.userid,
                    "username": user_obj.username,
                    "email": user_obj.email,
                    "phone": user_obj.phone,
                    "introduction": user_obj.introduction,
                    "avatar": user_obj.avatar.url
                }
                return Response.Response(data=result)
            except:
                return Response.BackendErrorResponse()
        # 验证码不正确
        else:
            result = Response.ClientErrorResponse()
            return result
    # 错误
    except:
        return Response.BackendErrorResponse()


def change_email(request):
    """
    修改邮箱-email
    """
    # 获取前端传来的消息
    try:
        userid_post = request.COOKIES.GET['userid']
        email_post = request.GET['email']
        code_post = request.GET['code']
        # 验证码正确
        if VerificationCode.objects.filter(phoneOrEmail=email_post, code=code_post):
            try:
                user_obj = Yonghu.objects.filter(userid=userid_post).first()
                user_obj.email = email_post
                user_obj.save()
                result = {
                    "data": user_obj.userid,
                    "username": user_obj.username,
                    "email": user_obj.email,
                    "phone": user_obj.phone,
                    "introduction": user_obj.introduction,
                    "avatar": user_obj.avatar.url
                }
                return Response.Response(data=result)
            except:
                return Response.BackendErrorResponse()
        # 验证码不正确
        else:
            result = Response.ClientErrorResponse()
            return result
        # 错误
    except:
        return Response.BackendErrorResponse()


def update_info(request):
    """
    修改用户信息
    """
    # 使用了POST方法
    if request.method == 'POST':
        try:
            userid = request.COOKIES.GET.get('userid')
            # 用户不存在
            if not  userid or not Yonghu.objects.filter(userid = userid):
                return Response.NotLoginResponse()
            # 提取前端数据
            data = request.body.decode('utf-8')
            data = json.loads(data)
            username = data.get('username')
            introduction = data.get('introduction')
            avatar = data.get('avatar')
            # 更新信息
            yonghu_obj = Yonghu.objects.filter(userid = userid).first()
            yonghu_obj.username = username
            yonghu_obj.introduction = introduction
            yonghu_obj.avatar = avatar
            yonghu_obj.save()
            return  Response.Response()
        # 后端错误
        except Exception as e:
            result = Response.BackendErrorResponse()
            return result
