from __future__ import absolute_import

import datetime
from configparser import ConfigParser
from time import sleep
import json
import requests
from celery import shared_task
from django.core.mail import send_mail
import random
from IcpSide import settings
from IcpSide.celery import app
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20210111 import sms_client, models
from IcpSide.config import SecretId, SecretKey, SmsSdkAppId, SignName, TemplateId


def random_str(random_length=8):
    """
    随机验证码
    :param random_length:
    :return:
    """
    string = ""
    chars = "0123456789"
    length = len(chars) - 1
    for i in range(random_length):
        string += chars[random.randint(0, length)]
    # print(string)
    return string


@app.task()
def send_code_email(email, code=None):
    """
    登录注册等邮件发送
    密码重置和修改邮箱都需要验证验证码
    :param email:
    :param username:
    :param token:
    :param send_type:
    :param code: 验证码
    :return:
    """
    email_title = '注册用户验证信息'
    email_body = "\n".join(['欢迎注册，您的验证码为：\n', code, "\n该验证码5分钟内有效"])
    print('========发送邮件中')
    send_stutas = send_mail(email_title, email_body, settings.EMAIL_HOST_USER, [email])
    print(send_stutas)
    if send_stutas:
        print('========发送成功')
        pass


@app.task()
def send_code_phone(PhoneNumber: list, TemplateParamSet: list):
    try:
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "sms.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = sms_client.SmsClient(cred, "ap-guangzhou", clientProfile)

        req = models.SendSmsRequest()
        params = {
            "PhoneNumberSet": PhoneNumber,
            "SmsSdkAppId": SmsSdkAppId,
            "SignName": SignName,
            "TemplateId": TemplateId,
            "TemplateParamSet": TemplateParamSet
        }
        req.from_json_string(json.dumps(params))

        resp = client.SendSms(req)
        print(resp.to_json_string())

    except TencentCloudSDKException as err:
        print(err)

