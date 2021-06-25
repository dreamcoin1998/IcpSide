'''
Author: dawnerstart
Function: 验证相关信息
Time: 2021-06-26
'''
from django.http import HttpResponse, JsonResponse, response
import json, simplejson, traceback
from .models import User
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
