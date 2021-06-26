'''
Author: dawnerstart
Function: 验证相关信息
Time: 2021-06-26
'''
from django.http import HttpResponse, JsonResponse, response
import json, simplejson, traceback, time, datetime, random
from .models import User, Verification_Code
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.serializers import serialize


def register(request):
    if request.POST:
        try:
            usernamepost = request.GET['username']
            passwordpost = request.GET['password']
            agepost = request.GET['age']
            emailpost = request.GET['email']
            phonepost = request.GET['phone']
            addresspost = request.GET['address']
            if(User.objects.filter(username = usernamepost) or User.objects.filter(email = emailpost)):
                print('注册失败')
                response = {'result':'False', 'status_code':'100'}
                return HttpResponse(json.dumps(response),  content_type = 'application/json')
            newuser = User(username = usernamepost, password = passwordpost, age = agepost, email = emailpost, phone = phonepost, address = addresspost)
            newuser.save()
            res = {'result':'True', 'status_code':'00'}
            return JsonResponse(data = res, safe = False)
            print(usernamepost, res)
        except:
            print('注册失败')
            response = {'result':'False', 'status_code':'100'}
            return HttpResponse(json.dumps(response),  content_type = 'application/json')

    '''
    请求验证码
    '''
def get_phone_verification_code(request):
    # 使用了POST方法
    if request.POST:
        phone_post = request.GET['phone']
        now=datetime.datetime.now()
        # 手机号已注册
        if(User.objects.filter(phone = phone_post)):
            result= {
                        "code": 4005,
                        "data": {
                                    
                                },
                        "msg": "手机号已注册"
                    }
        # 手机号获取验证码太过频繁
        elif(Verification_Code.objects.get(phone = phone_post)):
            result= {
                        "code": 4006,
                        "data": {
                                    
                                },
                        "msg": "手机号获取验证码太过频繁"
                    }
        # 可获取验证码
        else:
            try:
                x = str(random.randint(000000,999999))
                new_verification_code = Verification_Code(verification_type = 'phone', phoneOrEmail = phone_post, code = x)
                new_verification_code.save()
                # 调用手机验证码接口代码
                result= {
                        "code": 1,
                        "data": {
                                    
                                },
                        "msg": "手机验证码发送成功"
                    }
            except:
                # 手机号/邮箱验证码发送有问题
                result= {
                        "code": 4007,
                        "data": {
                                    
                                },
                        "msg": "手机号/邮箱验证码发送有问题"
                    }
    # 未使用POST方法
    else:
        result= {
                "code": 6000,
                "data": {
                            
                        },
                "msg": "歇会啊"
                }
    return JsonResponse(data=result,safe=False)
                


