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

'''
注册
'''
def register(request):
    # 使用POST方法
    if request.POST:
        try:
            # 用手机号验证
            if(request.GET['type'] == 'phone'):
                username_post = request.GET['username']
                password_post = request.GET['password']
                phoneOrEmail_post = request.GET['phoneOrEmail']
                code_post = request.GET['code']
                # 手机号已存在或者验证码不正确
                if(User.objects.filter(phone = phoneOrEmail_post) or not Verification_Code.objects.filter(phoneOrEmail = phoneOrEmail_post, code = code_post)):
                    result={
                                "code": 6001,
                                "data": {
                                "userid": 1,
                                "username": "",
                                "email": "",
                                "phone": ""
                                },
                                "msg": "手机号已存在或者验证码不正确"
                            }
                    response=JsonResponse(data=result,safe=False)
                # 注册成功
                else:
                    new_user = User(username=username_post, password=password_post, phone=phoneOrEmail_post)
                    new_user.save()
                    userid=User.objects.filter(phone=phoneOrEmail_post).first().userid
                    result={
                                "code": 0,
                                "data": {
                                "userid": userid,
                                "username": username_post,
                                "email": "",
                                "phone": phoneOrEmail_post
                                },
                                "msg": "注册成功"
                            }
                    # 返回json和cookie，cookie需要在7天后到期
                    response=JsonResponse(data=result,safe=False)
                    response.set_cookie('userid', userid, expires = 60 * 60 * 24 * 7)
                    # 删除验证码
                    delete_verification_code = Verification_Code.objects.filter(phoneOrEmail = phoneOrEmail_post, code = code_post)
                    delete_verification_code.delete()
            # 用邮箱验证
            elif(request.GET['type'] == 'email'):
                username_post = request.GET['username']
                password_post = request.GET['password']
                phoneOrEmail_post = request.GET['phoneOrEmail']
                code_post = request.GET['code']
                # 手机号已存在或者验证码不正确
                if(User.objects.filter(email = phoneOrEmail_post) or not Verification_Code.objects.filter(phoneOrEmail = phoneOrEmail_post, code = code_post)):
                    result={
                                "code": 6001,
                                "data": {
                                "userid": 1,
                                "username": "",
                                "email": "",
                                "phone": ""
                                },
                                "msg": "邮箱已存在或者验证码不正确"
                            }
                    response=JsonResponse(data=result,safe=False)
                # 注册成功
                else:
                    new_user = User(username=username_post, password=password_post, email=phoneOrEmail_post)
                    new_user.save()
                    userid=User.objects.filter(email=phoneOrEmail_post).first().userid
                    result={
                                "code": 0,
                                "data": {
                                "userid": userid,
                                "username": username_post,
                                "email": phoneOrEmail_post,
                                "phone": ""
                                },
                                "msg": "注册成功"
                            }
                    # 返回json和cookie，cookie需要在7天后到期
                    response=JsonResponse(data=result,safe=False)
                    response.set_cookie('userid', userid, expires = 60 * 60 * 24 * 7)

            # 其他
            else:
                result={
                        "code": 5000,
                        "data": {
                        "userid": '',
                        "username": '',
                        "email": "",
                        "phone": ''
                        },
                        "msg": "后端错误"
                    }
                response=JsonResponse(data=result,safe=False)
        # 后端错误
        except:
            result={
                        "code": 5000,
                        "data": {
                        "userid": '',
                        "username": '',
                        "email": "",
                        "phone": ''
                        },
                        "msg": "后端错误"
                    }
            response=JsonResponse(data=result,safe=False)
    # 未使用POST方法
    else:
        result= {
                "code": 6000,
                "data": {
                            
                        },
                "msg": "歇会啊"
                }
        response=JsonResponse(data=result,safe=False)
    return response

'''
请求手机验证码
'''
def get_phone_verification_code(request):
    # 使用了POST方法
    if request.POST:
        phone_post = request.GET['phone']
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
                
'''
请求邮箱验证码
'''
def get_email_verification_code(request):
    # 使用了POST方法
    if request.POST:
        email_post = request.GET['email']
        # 手机号已注册
        if(User.objects.filter(email = email_post)):
            result= {
                        "code": 4005,
                        "data": {
                                    
                                },
                        "msg": "邮箱已注册"
                    }
        # 手机号获取验证码太过频繁
        elif(Verification_Code.objects.get(email = email_post)):
            result= {
                        "code": 4006,
                        "data": {
                                    
                                },
                        "msg": "邮箱获取验证码太过频繁"
                    }
        # 可获取验证码
        else:
            try:
                x = str(random.randint(000000,999999))
                new_verification_code = Verification_Code(verification_type = 'phone', phoneOrEmail = email_post, code = x)
                new_verification_code.save()
                # 调用手机验证码接口代码
                result= {
                        "code": 1,
                        "data": {
                                    
                                },
                        "msg": "邮箱验证码发送成功"
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

'''
手机号登录
'''
def login_phone(request):
    # POST方法
    if request.POST:
        # 尝试登陆
        try:
            phone_post=request.GET['phone']
            passwword_post=request.GET['password']
            # 若手机号和密码正确
            if(User.objects.filter(phone=phone_post, password=passwword_post)):
                login_userid=User.objects.filter(phone=phone_post, password=passwword_post).first().userid
                login_username=User.objects.filter(phone=phone_post, password=passwword_post).first().username
                login_email=User.objects.filter(phone=phone_post, password=passwword_post).first().email
                login_phone=User.objects.filter(phone=phone_post, password=passwword_post).first().phone
                login_verification=User.objects.filter(phone=phone_post, password=passwword_post).first().verification
                login_avatar=User.objects.filter(phone=phone_post, password=passwword_post).first().avatar
                result= {
                            "code": 0,
                            "data": {
                            "userid": login_userid,
                            "username": login_username,
                            "email": login_email,
                            "phone": login_phone,
                            "verification": login_verification,
                            "avatarUrl": login_avatar
                            },
                            "msg": "登陆成功"
                        }
                response=JsonResponse(data=result,safe=False)
                response.set_cookie('userid', login_userid, expires = 60 * 60 * 24 * 7)
            # 若手机号或密码不正确
            else:
                result= {
                            "code": 6002,
                            "data": {
                            "userid": '',
                            "username": "",
                            "email": "",
                            "phone": "",
                            "verification": '',
                            "avatarUrl": ""
                            },
                            "msg": "手机号或密码不正确"
                        }
                response=JsonResponse(data=result,safe=False)
        # 尝试登陆失败
        except:
            result= {
                "code": 6000,
                "data": {
                            
                        },
                "msg": "歇会啊"
                }
            response=JsonResponse(data=result,safe=False)
    # 未用POST
    else:
        result= {
                "code": 6000,
                "data": {
                            
                        },
                "msg": "歇会啊"
                }
        response=JsonResponse(data=result,safe=False)
    return response

'''
邮箱登录
'''
def login_email(request):
    # POST方法
    if request.POST:
        # 尝试登陆
        try:
            email_post=request.GET['email']
            passwword_post=request.GET['password']
            # 若手机号和密码正确
            if(User.objects.filter(email=email_post, password=passwword_post)):
                login_userid=User.objects.filter(email=email_post, password=passwword_post).first().userid
                login_username=User.objects.filter(email=email_post, password=passwword_post).first().username
                login_email=User.objects.filter(email=email_post, password=passwword_post).first().email
                login_phone=User.objects.filter(email=email_post, password=passwword_post).first().phone
                login_verification=User.objects.filter(email=email_post, password=passwword_post).first().verification
                login_avatar=User.objects.filter(email=email_post, password=passwword_post).first().avatar
                result= {
                            "code": 0,
                            "data": {
                            "userid": login_userid,
                            "username": login_username,
                            "email": login_email,
                            "phone": login_phone,
                            "verification": login_verification,
                            "avatarUrl": login_avatar
                            },
                            "msg": "登陆成功"
                        }
                response=JsonResponse(data=result,safe=False)
                response.set_cookie('userid', login_userid, expires = 60 * 60 * 24 * 7)
            # 若手机号或密码不正确
            else:
                result= {
                            "code": 6002,
                            "data": {
                            "userid": '',
                            "username": "",
                            "email": "",
                            "phone": "",
                            "verification": '',
                            "avatarUrl": ""
                            },
                            "msg": "邮箱或密码不正确"
                        }
                response=JsonResponse(data=result,safe=False)
        # 尝试登陆失败
        except:
            result= {
                "code": 6000,
                "data": {
                            
                        },
                "msg": "歇会啊"
                }
            response=JsonResponse(data=result,safe=False)
    # 未用POST
    else:
        result= {
                "code": 6000,
                "data": {
                            
                        },
                "msg": "歇会啊"
                }
        response=JsonResponse(data=result,safe=False)
    return response