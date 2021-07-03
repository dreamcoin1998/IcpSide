"""
Author: dawnerstart
Function: 验证相关信息
Time: 2021-06-26
"""
import json

from django.contrib.auth.hashers import make_password, check_password
from IcpSide.settings import EXPIRE_TIME
from auth_user.models import Yonghu, VerificationCode
from utils.response import Response
import datetime
from .tasks import random_str, send_code_email, send_code_phone
from utils.image_io.image_io import upload_image
from image.models import ImagePath
from utils.jwt_auth.authentication import jwt_payload_handler, JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_encode_handler


def verify_phone_email_code(phone_or_email, code_post, username_post, password, introduction, type='phone'):
    if type == "phone":
        yonghu_count = Yonghu.objects.filter(phone=phone_or_email).count()
    else:
        yonghu_count = Yonghu.objects.filter(email=phone_or_email).count()
    # 不为0，手机号存在
    if yonghu_count:
        return Response.PhoneOrEmailOccupied(), False
    verify_filter = VerificationCode.objects.filter(phoneOrEmail=phone_or_email, code=code_post)
    print(verify_filter)
    # 等于0，不存在验证码
    if verify_filter.count() == 0:
        return Response.CodeErrorResponse(), False
    # 是否在5分钟之内
    if not code_validated(verify_filter.first(), 5):
        return Response.CodeOverTimeResponse(), False
    if type == "phone":
        new_user = Yonghu(username=username_post, password=password, phone=phone_or_email, introduction=introduction)
    else:
        new_user = Yonghu(username=username_post, password=password, email=phone_or_email, introduction=introduction)
    return new_user, True


def format_user_data(user_obj=None):
    data = {
        "data": user_obj.userid,
        "username": user_obj.username,
        "email": user_obj.email,
        "phone": user_obj.phone,
        "introduction": user_obj.introduction,
        "avatar": user_obj.avatar_url
    }
    return data


def register(request):
    """
    注册
    """
    # 使用POST方法
    if request.method == "POST":
        # 提取前端数据
        image_stream = request.FILES.get('file')
        username_post = request.POST.get('username')
        password_post = request.POST.get('password')
        phone_or_email = request.POST.get('phoneOrEmail')
        code_post = request.POST.get("code")
        introduction = request.POST.get("introduction")
        # 密码长度小于8
        if len(password_post) < 8:
            return Response.PasswordLengthResponse()
        password = make_password(password_post)
        # 用手机号验证
        if request.POST.get("type") == 'phone':
            new_user, verification_status = verify_phone_email_code(phone_or_email, code_post, username_post,
                                                                    password, introduction)
            if not verification_status:
                return new_user
        # 用邮箱验证
        elif request.POST.get("type") == 'email':
            new_user, verification_status = verify_phone_email_code(phone_or_email, code_post, username_post,
                                                                    password, introduction, type="email")
            if not verification_status:
                return new_user
        else:
            return Response.ClientErrorResponse()
        new_user.save()
        return_url = upload_image(image_stream)
        if return_url:
            image_path = ImagePath()
            image_path.url = return_url
            image_path.content_object = new_user
            image_path.save()
        else:
            return Response.BackendErrorResponse()
        data = format_user_data(user_obj=new_user)
        # 使用token验证
        payload = jwt_payload_handler(new_user)
        token = jwt_encode_handler(payload)
        response = Response.Response(data=data, token=token)
        # response.set_cookie('userid', new_user.userid, expires=EXPIRE_TIME)
        return response


def code_validated(verify_obj, minutes: int):
    """
    验证码时间验证 是否在1分钟内
    """
    update_time_timestamp = datetime.datetime.timestamp(verify_obj.update_time)
    now = datetime.datetime.now()  # 当前时间
    now_timestamp = datetime.datetime.timestamp(now)
    if now_timestamp - update_time_timestamp < 60 * minutes:
        return True
    return False


def get_phone_verification_code(request):
    """
    请求手机验证码
    """
    # 使用了POST方法
    if request.method == "POST":
        data = request.body.decode('utf-8')
        data = json.loads(data)
        phone_post = data.get("phone")
        verify_filter = VerificationCode.objects.filter(phoneOrEmail=phone_post)
        if verify_filter:
            # 判断时间是否在5分钟内
            verify_obj = verify_filter.first()
            if code_validated(verify_obj, 1):
                return Response.GetCodeTooOftenResponse()
        else:
            verify_obj = VerificationCode()
        random_code = random_str(random_length=6)
        verify_obj.code = random_code
        verify_obj.verification_type = "phone"
        verify_obj.phoneOrEmail = phone_post
        verify_obj.save()
        # 手机验证码发送
        send_code_phone.delay(phone_post, random_code)
        return Response.Response()
    return Response.ClientErrorResponse()


def get_email_verification_code(request):
    """
    请求邮箱验证码
    """
    # 使用了POST方法
    if request.method == "POST":
        data = request.body.decode('utf-8')
        data = json.loads(data)
        email_post = data.get("email")
        # 手机号获取验证码太过频繁
        if VerificationCode.objects.filter(phoneOrEmail=email_post):
            # 判断时间是否在5分钟内
            verify_obj = VerificationCode.objects.filter(phoneOrEmail=email_post).first()
            if code_validated(verify_obj, 1):
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
    return Response.BackendErrorResponse()


def login_phone(request):
    """
    手机号登录
    """
    # POST方法
    if request.method == "POST":
        # 尝试登陆
        data = request.body.decode('utf-8')
        data = json.loads(data)
        phone_post = data.get("phone")
        password_post = data.get("password")
        yonghu_filter = Yonghu.objects.filter(phone=phone_post)
        # 若手机号和密码正确
        if yonghu_filter and check_password(password_post, yonghu_filter.first().password):
            user_obj = yonghu_filter.first()
            result = format_user_data(user_obj)
            # 使用token验证
            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            response = Response.Response(data=result, token=token)
            return response
        # 若手机号或密码不正确
        else:
            return Response.PhoneOrEmailErrorResponse()
    return Response.ClientErrorResponse()


def login_email(request):
    """
    邮箱登录
    """
    # POST方法
    if request.method == "POST":
        # 尝试登陆
        data = request.body.decode('utf-8')
        data = json.loads(data)
        email_post = data.get("email")
        password_post = data.get("password")
        yonghu_filter = Yonghu.objects.filter(email=email_post)
        # 若手机号和密码正确
        if yonghu_filter and check_password(password_post, yonghu_filter.first().password) :
            user_obj = yonghu_filter.first()
            result = format_user_data(user_obj)
            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            response = Response.Response(data=result, token=token)
            return response
        # 若手机号或密码不正确
        else:
            return Response.PhoneOrEmailErrorResponse()
    return Response.ClientErrorResponse()


def change_passswd_pnone(request):
    """
    找回密码-phone
    """
    # 使用了POST方法
    if request.method == "POST":
        data = request.body.decode('utf-8')
        data = json.loads(data)
        phone_post = data.get("phone")
        password_post = data.get("password")
        code_post = data.get("code")
        # 验证码正确
        if VerificationCode.objects.filter(phoneOrEmail=phone_post, code=code_post):
            user_obj = Yonghu.objects.filter(phone=phone_post).first()
            user_obj.password = make_password(password_post)
            user_obj.save()
            result = format_user_data(user_obj=user_obj)
            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            response = Response.Response(data=result, token=token)
            return response
        # 验证码不正确
        else:
            return Response.CodeErrorResponse()
    return Response.ClientErrorResponse()


def change_passswd_email(request):
    """
    找回密码-email
    """
    # 使用了POST方法
    if request.method == "POST":
        data = request.body.decode('utf-8')
        data = json.loads(data)
        email_post = data.get("email")
        password_post = data.get("password")
        code_post = data.get("code")
        # 验证码正确
        if VerificationCode.objects.filter(phoneOrEmail=email_post, code=code_post):
            user_obj = Yonghu.objects.filter(email=email_post).first()
            user_obj.password = make_password(password_post)
            user_obj.save()
            result = format_user_data(user_obj=user_obj)
            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            response = Response.Response(data=result, token=token)
            response.set_cookie('userid', user_obj.userid, expires=EXPIRE_TIME)
            return response
        # 验证码不正确
        else:
            return Response.CodeErrorResponse()
    return Response.ClientErrorResponse()


def change_phone(request):
    """
    修改手机-phone
    """
    user_obj = JSONWebTokenAuthentication().authenticate(request)
    # 未登录
    if user_obj is None:
        return Response.NotLoginResponse()
    phone_post = request.GET.get("phone")
    code_post = request.GET.get("code")
    password = request.GET.get("password")
    # 密码正确
    if not check_password(password, user_obj.password):
        return Response.PhoneOrEmailErrorResponse()
    # 验证码正确
    if VerificationCode.objects.filter(phoneOrEmail=phone_post, code=code_post, verification_type="phone"):
        try:
            user_obj.phone = phone_post
            user_obj.save()
            result = format_user_data(user_obj)
            return Response.Response(data=result)
        except:
            return Response.BackendErrorResponse()
    # 验证码不正确
    else:
        result = Response.ClientErrorResponse()
        return result


def change_email(request):
    """
    修改邮箱-email
    """
    # 获取前端传来的消息
    user_obj = JSONWebTokenAuthentication().authenticate(request)
    # 未登录
    if user_obj is None:
        return Response.NotLoginResponse()
    email_post = request.GET.get("email")
    code_post = request.GET.get("code")
    password = request.GET.get("password")
    # 密码正确
    if not check_password(password, user_obj.password):
        return Response.PhoneOrEmailErrorResponse()
    # 验证码正确
    verify_filter = VerificationCode.objects.filter(phoneOrEmail=email_post, code=code_post, verification_type="email")
    if verify_filter:
        # 验证码过期
        if not code_validated(verify_filter.filter(), 5):
            return Response.CodeOverTimeResponse()
        try:
            user_obj.email = email_post
            user_obj.save()
            result = format_user_data(user_obj)
            return Response.Response(data=result)
        except:
            return Response.BackendErrorResponse()
    # 验证码不正确
    else:
        result = Response.ClientErrorResponse()
        return result
