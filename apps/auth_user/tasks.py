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


def random_str(random_length=8):
    """
    随机验证码
    :param random_length:
    :return:
    """
    string = ""
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
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
def send_code_phone(phone: str, code=None):
    print('========发送邮件中')
    resp = requests.post("http://sms-api.luosimao.com/v1/send.json",
                         auth=("api", "3646f0434444618610f6476b1a984c9a"),
                         data={
                             "mobile": phone,
                             "message": f"欢迎注册，您的验证码为:{code}，该验证码5分钟内有效【铁壳测试】"
                         },
                         verify=False
                         )
    error = resp.json().get("error")
    if error == 0:
        print('========发送成功')

