import json
from django.http.response import JsonResponse
from utils.response import Response
from .models import ProductType, ProductInfo
from auth_user.models import Yonghu
from datetime import datetime


def creat_result(product_obj):
    result = {
        "id": product_obj.id,
        "product_name": product_obj.product_name,
        "product_detail": product_obj.product_detail,
        "product_type": {
            "product_type_id": product_obj.product_type.product_type_id,
            "type_name": product_obj.product_type.type_name
        },
        "create_time": product_obj.create_time,
        "update_time": product_obj.update_time,
        "price": product_obj.price,
        "inventory": product_obj.inventory,
        "user_info": {
            "userid": product_obj.user.userid,
            "username": product_obj.user.username,
            "email": product_obj.user.email,
            "phone": product_obj.user.phone,
            "verification": product_obj.user.verification
        }
    }
    return result


def create(request):
    """
    发布产品信息接口
    """
    # 使用POST方法
    if request.POST:
        try:
            userid_post = request.COOKIES.GET.get('userid')
            if not userid_post or not Yonghu.objects.filter(userid = userid_post):
                return Response.NotLoginResponse()
            data = request.body.decode('utf-8')
            data = json.loads(data)
            product_name_post = data.get('product_name')
            product_detail_post = data.get('product_detail')
            price_post = data.get('price')
            inventory_post = data.get('inventory')
            product_type_id_post = data.get('product_type_id')
            # 产品type存在
            if ProductType.objects.filter(product_type_id = product_type_id_post):
                product_type_obj = ProductType.objects.filter(product_type_id = product_type_id_post).first()
                user_obj = Yonghu.objects.filter(userid=userid_post).first()
                new_product  = ProductInfo(product_name = product_name_post,
                                           product_detail = product_detail_post,
                                           price = price_post,
                                           inventory = inventory_post,
                                           product_type_id = product_type_obj,
                                           userid = user_obj)
                new_product.save()
                result = creat_result(new_product)
                return Response.Response(data=result)
            else:
                return Response.ProductTypeErrorResponse()
        # 后端错误
        except:
            result = Response.BackendErrorResponse()
            return result

'''
发布产品信息接口
'''
def update(request):
    # 使用POST方法
    if request.POST and request.COOKIES.GET['userid']:
        try:
            userid_post = request.COOKIES.GET['userid']
            product_id_post = request.GET['id']
            product_name_post = request.GET['product_name']
            product_detail_post = request.GET['product_detail']
            price_post = request.GET['price']
            inventory_post = request.GET['inventory']
            product_type_id_post = request.GET['product_type_id']
            # userid存在且产品id存在
            if Yonghu.objects.filter(userid = userid_post) and ProductInfo.objects.filter(id = product_id_post):
                try:
                    update_product = ProductInfo.objects.filter(id = product_id_post).first()
                    update_product.product_name = product_name_post
                    update_product.product_detail = product_detail_post
                    update_product.price = price_post
                    update_product.inventory = inventory_post
                    update_product.product_type_id = product_type_id_post
                    update_product.save()
                    type_name = ProductType.objects.get(product_type_id = product_type_id_post).type_name
                    new_product  = ProductInfo(product_name = product_name_post, product_detail = product_detail_post, price = price_post, inventory = inventory_post, product_type_id = product_type_id_post, userid = userid_post)
                    new_product.save()

                    username = Yonghu.objects.get(userid = userid_post).username
                    email = Yonghu.objects.get(userid = userid_post).email
                    phone = Yonghu.objects.get(userid = userid_post).phone

                    create_time = update_product.update_product
                    result = {
                                "code": 0,
                                "data": {
                                    "id": product_id_post,
                                    "product_name": product_name_post,
                                    "product_detail": product_detail_post,
                                    "product_type": {
                                    "id": product_type_id_post,
                                    "type_name": type_name
                                    },
                                    "create_time": create_time,
                                    "update_time": datetime.now(),
                                    "price": price_post,
                                    "inventory": inventory_post,
                                    "user_info": {
                                        "userid": userid_post,
                                        "username": username,
                                        "email": email,
                                        "phone": phone,
                                    "verification": 'false'
                                    }
                                },
                                "msg": "ok"
                            }
                    return JsonResponse(data = result, safe = False)

                except:
                    result = Response.ClientErrorResponse()
                    return result
            # userid不存在或产品id不存在
            else:
                result = Response.ClientErrorResponse()
                return result   
        # 后端错误
        except:
            result = Response.BackendErrorResponse()
            return result
    # 未使用POST方法
    else:
        result = Response.HttpMethodErrorResponse()
        return result

'''
获取产品信息-GET方法
'''
def get_product_info(request, product_id):
    # 若使用GET方法
    if request.method == 'GET':
        # 获取传来的信息
        try:
            # 从数据库查询产品信息
            the_product_info = ProductInfo.objects.get(id = product_id)
            product_name = the_product_info.product_name
            product_type_id = the_product_info.product_type_id
            product_detail = the_product_info.product_detail
            create_time = the_product_info.create_time
            update_time = the_product_info.update_time
            userid = the_product_info.userid
            price = the_product_info.price
            inventory = the_product_info.inventory
            # 产品类型信息
            user_info = Yonghu.objects.get(userid = userid)
            username = user_info.username
            email = user_info.email
            phone = user_info.phone
            # 产品所属user信息

            # 构造result
            result = {
                        "code": 0,
                        "data": {
                        "id": product_id,
                        "product_name": product_name,
                        "product_detail": product_detail,
                        "product_type": {
                            "id": ,
                            "type_name": ""
                        },
                        "create_time": create_time,
                        "update_time": update_time,
                        "price": price,
                        "inventory": inventory,
                        "user_info": {
                            "userid": userid,
                            "username": username,
                            "email": email,
                            "phone": phone,
                            "verification": 'false'
                        },
                        "images": ["https://xxx.xxx.com"]               # 待改进
                        },
                        "msg": "ok"
            }
            return JsonResponse(data = result, safe = False)


        # 获取传来的信息不成功，后端错误
        except:
            result = Response.BackendErrorResponse()
            return result
    # 不使用GET方法
    else:
        result = Response.HttpMethodErrorResponse()
        return result

'''
产品类型列表-GET
'''
def product_types(request):
    # 若使用GET方法
    if request.method == 'GET':
        # 返回信息
        try:
            # 从数据库查询产品类型信息
            the_product_type = ProductType.objects.all()
            data = []
            for i in the_product_type:
                product_type_id = i.product_type_id
                type_name = i.type_name
                type = {
                    "id": product_type_id,
                    "type_name": type_name
                }
                data.append(type)
            result = {
                    "code": 0,
                    "data": data,
                    "msg": "产品类型列表已成功查询"
                    }
            return JsonResponse(data = result, safe = False)
        # 后端错误
        except:
            result = Response.BackendErrorResponse()
            return result
    # 不使用GET方法
    else:
        result = Response.HttpMethodErrorResponse()
        return result

'''
获取用户发布的产品列表-GET
'''
def my_products(request):
    # 若使用GET方法且存在userid
    if request.method == 'GET' and request.COOKIES.GET['userid']:
        # 返回信息
        try:
            data = []
            userid_post = request.COOKIES.GET['userid']
            # 从数据库查询产品类型信息
            the_products = ProductInfo.objects.filter(userid = userid_post)
            count_products = len(the_products)
            count = int(request.GET.get('count', default = '10'))
            page = int(request.GET.get('page', default = '1'))
            n1 = count * (page - 1) + 1
            n2 = count * (page)
            # 从数据库得到用户信息
            the_user = Yonghu.objects.get(userid = userid_post)
            username = the_user.username
            email = the_user.email
            phone = the_user.phone
            if (count_products < n1):
                result = Response.HttpMethodErrorResponse()
                return result
            elif (n1 <= count_products <= n2):
                for i in range(n1-1, count_products):
                    product = the_products[i]
                    product_name = product.product_name
                    product_detail = product.product_detail
                    product_type = product.product_type
                    product_id = product.id
                    product_type_id = product.product_type_id
                    create_time = product.create_time
                    update_time = product.update_time
                    price = product.price
                    inventory = product.inventory

                    the_type= ProductType.objects.get(product_type_id = product_type_id)
                    type_name = the_type.type_name

                    total = count_products - n1 + 1
                    totalPage = int(count_products / count + 1)

                    the_data = {
                        "id": product_id,
                        "product_name": product_name,
                        "product_detail": product_detail,
                        "product_type": {
                        "id": product_type_id,
                        "type_name": type_name
                        },
                        "create_time": create_time,
                        "update_time": update_time,
                        "price": price,
                        "inventory": inventory,
                        "user_info": {
                            "userid": userid_post,
                            "username": username,
                            "email": email,
                            "phone": phone,
                        "verification": 'false'
                        },
                        "images": ["https://xxx.xxx.com"]                                       # 待改进
                    }
                    data.append(the_data)
                result = {
                    "code": 0,
                    "data": data,
                    total: total,
                    "totalPage": totalPage,
                    "page": page,
                    "msg": "ok"
                }

                return JsonResponse(data = result, safe = False)
            else:
                for i in range(n1-1, n2):
                    product = the_products[i]
                    product_name = product.product_name
                    product_detail = product.product_detail
                    product_type = product.product_type
                    product_id = product.id
                    product_type_id = product.product_type_id
                    create_time = product.create_time
                    update_time = product.update_time
                    price = product.price
                    inventory = product.inventory

                    the_type= ProductType.objects.get(product_type_id = product_type_id)
                    type_name = the_type.type_name

                    total = count_products - n1 + 1
                    totalPage = int(count_products / count + 1)

                    the_data = {
                        "id": product_id,
                        "product_name": product_name,
                        "product_detail": product_detail,
                        "product_type": {
                        "id": product_type_id,
                        "type_name": type_name
                        },
                        "create_time": create_time,
                        "update_time": update_time,
                        "price": price,
                        "inventory": inventory,
                        "user_info": {
                            "userid": userid_post,
                            "username": username,
                            "email": email,
                            "phone": phone,
                        "verification": 'false'
                        },
                        "images": ["https://xxx.xxx.com"]                                       # 待改进
                    }
                    data.append(the_data)
                result = {
                    "code": 0,
                    "data": data,
                    total: total,
                    "totalPage": totalPage,
                    "page": page,
                    "msg": "ok"
                }

                return JsonResponse(data = result, safe = False)
            
        # 后端错误
        except:
            result = Response.BackendErrorResponse()
            return result
    # 不使用GET方法
    else:
        result = Response.HttpMethodErrorResponse()
        return result

'''
根据类型id获取该类型得产品列表-GET
'''
def products_type(request):
    # 若使用GET方法且存在userid、产品类型id
    if request.method == 'GET' and request.COOKIES.GET['userid'] and request.GET.get('id'):
        # 返回信息
        try:
            data = []
            userid_post = request.COOKIES.GET['userid']
            # 从数据库查询产品类型信息
            product_type_id_post = request.GET.get('id', default = '1')
            count = int(request.GET.get('count', default = '10'))
            page = int(request.GET.get('page', default = '1'))
            # 若没有该类型产品
            if ProductInfo.objects.filter(product_type_id = product_type_id_post) == None:
                result = Response.HttpMethodErrorResponse()
                return result

            the_products = ProductInfo.objects.filter(product_type_id = product_type_id_post)
            count_products = len(the_products)
            
            n1 = count * (page - 1) + 1
            n2 = count * (page)
            # 从数据库得到用户信息
            the_user = Yonghu.objects.get(userid = userid_post)
            username = the_user.username
            email = the_user.email
            phone = the_user.phone
            if (count_products < n1):
                result = Response.HttpMethodErrorResponse()
                return result
            elif (n1 <= count_products <= n2):
                for i in range(n1-1, count_products):
                    product = the_products[i]
                    product_name = product.product_name
                    product_detail = product.product_detail
                    product_type = product.product_type
                    product_id = product.id
                    product_type_id = product.product_type_id
                    create_time = product.create_time
                    update_time = product.update_time
                    price = product.price
                    inventory = product.inventory

                    the_type= ProductType.objects.get(product_type_id = product_type_id)
                    type_name = the_type.type_name

                    total = count_products - n1 + 1
                    totalPage = int(count_products / count + 1)
                    the_data = {
                        "id": product_id,
                        "product_name": product_name,
                        "product_detail": product_detail,
                        "product_type": {
                        "id": product_type_id,
                        "type_name": type_name
                        },
                        "create_time": create_time,
                        "update_time": update_time,
                        "price": price,
                        "inventory": inventory,
                        "user_info": {
                            "userid": userid_post,
                            "username": username,
                            "email": email,
                            "phone": phone,
                        "verification": 'false'
                        },
                        "images": ["https://xxx.xxx.com"]                                       # 待改进
                    }
                    data.append(the_data)
                result = {
                    "code": 0,
                    "data": data,
                    total: total,
                    "totalPage": totalPage,
                    "page": page,
                    "msg": "ok"
                }

                return JsonResponse(data = result, safe = False)
            else:
                for i in range(n1-1, n2):
                    product = the_products[i]
                    product_name = product.product_name
                    product_detail = product.product_detail
                    product_type = product.product_type
                    product_id = product.id
                    product_type_id = product.product_type_id
                    create_time = product.create_time
                    update_time = product.update_time
                    price = product.price
                    inventory = product.inventory

                    the_type= ProductType.objects.get(product_type_id = product_type_id)
                    type_name = the_type.type_name

                    total = count_products - n1 + 1
                    totalPage = int(count_products / count + 1)

                    the_data = {
                        "id": product_id,
                        "product_name": product_name,
                        "product_detail": product_detail,
                        "product_type": {
                        "id": product_type_id,
                        "type_name": type_name
                        },
                        "create_time": create_time,
                        "update_time": update_time,
                        "price": price,
                        "inventory": inventory,
                        "user_info": {
                            "userid": userid_post,
                            "username": username,
                            "email": email,
                            "phone": phone,
                        "verification": 'false'
                        },
                        "images": ["https://xxx.xxx.com"]                                       # 待改进
                    }
                    data.append(the_data)
                result = {
                    "code": 0,
                    "data": data,
                    total: total,
                    "totalPage": totalPage,
                    "page": page,
                    "msg": "ok"
                }

                return JsonResponse(data = result, safe = False)
            
        # 后端错误
        except:
            result = Response.BackendErrorResponse()
            return result
    # 不使用GET方法
    else:
        result = Response.HttpMethodErrorResponse()
        return result

'''
推荐产品接口-GET
'''
def recommond(request):
    # 若使用GET方法且存在userid
    if request.method == 'GET' and request.COOKIES.GET['userid']:
        # 返回信息
        try:
            data = []
            userid_post = request.COOKIES.GET['userid']
            # 从数据库查询产品类型信息
            product_type_id_post = request.GET.get('id', default = '1')
            count = int(request.GET.get('count', default = '10'))
            page = int(request.GET.get('page', default = '1'))

            the_products = ProductInfo.objects.all()
            count_products = len(the_products)
            
            n1 = count * (page - 1) + 1
            n2 = count * (page)
            # 从数据库得到用户信息
            the_user = Yonghu.objects.get(userid = userid_post)
            username = the_user.username
            email = the_user.email
            phone = the_user.phone
            if (count_products < n1):
                result = Response.HttpMethodErrorResponse()
                return result
            elif (n1 <= count_products <= n2):
                for i in range(n1-1, count_products):
                    product = the_products[i]
                    product_name = product.product_name
                    product_detail = product.product_detail
                    product_type = product.product_type
                    product_id = product.id
                    product_type_id = product.product_type_id
                    create_time = product.create_time
                    update_time = product.update_time
                    price = product.price
                    inventory = product.inventory

                    the_type= ProductType.objects.get(product_type_id = product_type_id)
                    type_name = the_type.type_name

                    total = count_products - n1 + 1
                    totalPage = int(count_products / count + 1)
                    the_data = {
                        "id": product_id,
                        "product_name": product_name,
                        "product_detail": product_detail,
                        "product_type": {
                        "id": product_type_id,
                        "type_name": type_name
                        },
                        "create_time": create_time,
                        "update_time": update_time,
                        "price": price,
                        "inventory": inventory,
                        "user_info": {
                            "userid": userid_post,
                            "username": username,
                            "email": email,
                            "phone": phone,
                        "verification": 'false'
                        },
                        "images": ["https://xxx.xxx.com"]                                       # 待改进
                    }
                    data.append(the_data)
                result = {
                    "code": 0,
                    "data": data,
                    total: total,
                    "totalPage": totalPage,
                    "page": page,
                    "msg": "ok"
                }

                return JsonResponse(data = result, safe = False)
            else:
                for i in range(n1-1, n2):
                    product = the_products[i]
                    product_name = product.product_name
                    product_detail = product.product_detail
                    product_type = product.product_type
                    product_id = product.id
                    product_type_id = product.product_type_id
                    create_time = product.create_time
                    update_time = product.update_time
                    price = product.price
                    inventory = product.inventory

                    the_type= ProductType.objects.get(product_type_id = product_type_id)
                    type_name = the_type.type_name

                    total = count_products - n1 + 1
                    totalPage = int(count_products / count + 1)

                    the_data = {
                        "id": product_id,
                        "product_name": product_name,
                        "product_detail": product_detail,
                        "product_type": {
                        "id": product_type_id,
                        "type_name": type_name
                        },
                        "create_time": create_time,
                        "update_time": update_time,
                        "price": price,
                        "inventory": inventory,
                        "user_info": {
                            "userid": userid_post,
                            "username": username,
                            "email": email,
                            "phone": phone,
                        "verification": 'false'
                        },
                        "images": ["https://xxx.xxx.com"]                                       # 待改进
                    }
                    data.append(the_data)
                result = {
                    "code": 0,
                    "data": data,
                    total: total,
                    "totalPage": totalPage,
                    "page": page,
                    "msg": "ok"
                }

                return JsonResponse(data = result, safe = False)
            
        # 后端错误
        except:
            result = Response.BackendErrorResponse()
            return result
    # 不使用GET方法
    else:
        result = Response.HttpMethodErrorResponse()
        return result

'''
获取所有产品-GET
'''
def get_all_products(request):
    # 若使用GET方法且存在userid
    if request.method == 'GET' and request.COOKIES.GET['userid']:
        # 返回信息
        try:
            data = []
            userid_post = request.COOKIES.GET['userid']
            # 从数据库查询产品类型信息
            product_name_post = request.GET.get('product_name', default = '1')
            count = int(request.GET.get('count', default = '10'))
            page = int(request.GET.get('page', default = '1'))

            the_products = ProductInfo.objects.filter(product_name = product_name_post)
            count_products = len(the_products)
            
            n1 = count * (page - 1) + 1
            n2 = count * (page)
            # 从数据库得到用户信息
            the_user = Yonghu.objects.get(userid = userid_post)
            username = the_user.username
            email = the_user.email
            phone = the_user.phone
            if (count_products < n1):
                result = Response.HttpMethodErrorResponse()
                return result
            elif (n1 <= count_products <= n2):
                for i in range(n1-1, count_products):
                    product = the_products[i]
                    product_name = product.product_name
                    product_detail = product.product_detail
                    product_type = product.product_type
                    product_id = product.id
                    product_type_id = product.product_type_id
                    create_time = product.create_time
                    update_time = product.update_time
                    price = product.price
                    inventory = product.inventory

                    the_type= ProductType.objects.get(product_type_id = product_type_id)
                    type_name = the_type.type_name

                    total = count_products - n1 + 1
                    totalPage = int(count_products / count + 1)
                    the_data = {
                        "id": product_id,
                        "product_name": product_name,
                        "product_detail": product_detail,
                        "product_type": {
                        "id": product_type_id,
                        "type_name": type_name
                        },
                        "create_time": create_time,
                        "update_time": update_time,
                        "price": price,
                        "inventory": inventory,
                        "user_info": {
                            "userid": userid_post,
                            "username": username,
                            "email": email,
                            "phone": phone,
                        "verification": 'false'
                        },
                        "images": ["https://xxx.xxx.com"]                                       # 待改进
                    }
                    data.append(the_data)
                result = {
                    "code": 0,
                    "data": data,
                    total: total,
                    "totalPage": totalPage,
                    "page": page,
                    "msg": "ok"
                }

                return JsonResponse(data = result, safe = False)
            else:
                for i in range(n1-1, n2):
                    product = the_products[i]
                    product_name = product.product_name
                    product_detail = product.product_detail
                    product_type = product.product_type
                    product_id = product.id
                    product_type_id = product.product_type_id
                    create_time = product.create_time
                    update_time = product.update_time
                    price = product.price
                    inventory = product.inventory

                    the_type= ProductType.objects.get(product_type_id = product_type_id)
                    type_name = the_type.type_name

                    total = count_products - n1 + 1
                    totalPage = int(count_products / count + 1)

                    the_data = {
                        "id": product_id,
                        "product_name": product_name,
                        "product_detail": product_detail,
                        "product_type": {
                        "id": product_type_id,
                        "type_name": type_name
                        },
                        "create_time": create_time,
                        "update_time": update_time,
                        "price": price,
                        "inventory": inventory,
                        "user_info": {
                            "userid": userid_post,
                            "username": username,
                            "email": email,
                            "phone": phone,
                        "verification": 'false'
                        },
                        "images": ["https://xxx.xxx.com"]                                       # 待改进
                    }
                    data.append(the_data)
                result = {
                    "code": 0,
                    "data": data,
                    total: total,
                    "totalPage": totalPage,
                    "page": page,
                    "msg": "ok"
                }

                return JsonResponse(data = result, safe = False)
            
        # 后端错误
        except:
            result = Response.BackendErrorResponse()
            return result
    # 不使用GET方法
    else:
        result = Response.HttpMethodErrorResponse()
        return result

'''
获取所有产品-GET
'''
def search_products(request):
    # 若使用GET方法且存在userid
    if request.method == 'GET' and request.COOKIES.GET['userid']:
        # 返回信息
        try:
            data = []
            userid_post = request.COOKIES.GET['userid']
            # 从数据库查询产品类型信息
            product_type_id_post = request.GET.get('id', default = '1')
            count = int(request.GET.get('count', default = '10'))
            page = int(request.GET.get('page', default = '1'))

            the_products = ProductInfo.objects.all()
            count_products = len(the_products)
            
            n1 = count * (page - 1) + 1
            n2 = count * (page)
            # 从数据库得到用户信息
            the_user = Yonghu.objects.get(userid = userid_post)
            username = the_user.username
            email = the_user.email
            phone = the_user.phone
            if (count_products < n1):
                result = Response.HttpMethodErrorResponse()
                return result
            elif (n1 <= count_products <= n2):
                for i in range(n1-1, count_products):
                    product = the_products[i]
                    product_name = product.product_name
                    product_detail = product.product_detail
                    product_type = product.product_type
                    product_id = product.id
                    product_type_id = product.product_type_id
                    create_time = product.create_time
                    update_time = product.update_time
                    price = product.price
                    inventory = product.inventory

                    the_type= ProductType.objects.get(product_type_id = product_type_id)
                    type_name = the_type.type_name

                    total = count_products - n1 + 1
                    totalPage = int(count_products / count + 1)
                    the_data = {
                        "id": product_id,
                        "product_name": product_name,
                        "product_detail": product_detail,
                        "product_type": {
                        "id": product_type_id,
                        "type_name": type_name
                        },
                        "create_time": create_time,
                        "update_time": update_time,
                        "price": price,
                        "inventory": inventory,
                        "user_info": {
                            "userid": userid_post,
                            "username": username,
                            "email": email,
                            "phone": phone,
                        "verification": 'false'
                        },
                        "images": ["https://xxx.xxx.com"]                                       # 待改进
                    }
                    data.append(the_data)
                result = {
                    "code": 0,
                    "data": data,
                    total: total,
                    "totalPage": totalPage,
                    "page": page,
                    "msg": "ok"
                }

                return JsonResponse(data = result, safe = False)
            else:
                for i in range(n1-1, n2):
                    product = the_products[i]
                    product_name = product.product_name
                    product_detail = product.product_detail
                    product_type = product.product_type
                    product_id = product.id
                    product_type_id = product.product_type_id
                    create_time = product.create_time
                    update_time = product.update_time
                    price = product.price
                    inventory = product.inventory

                    the_type= ProductType.objects.get(product_type_id = product_type_id)
                    type_name = the_type.type_name

                    total = count_products - n1 + 1
                    totalPage = int(count_products / count + 1)

                    the_data = {
                        "id": product_id,
                        "product_name": product_name,
                        "product_detail": product_detail,
                        "product_type": {
                        "id": product_type_id,
                        "type_name": type_name
                        },
                        "create_time": create_time,
                        "update_time": update_time,
                        "price": price,
                        "inventory": inventory,
                        "user_info": {
                            "userid": userid_post,
                            "username": username,
                            "email": email,
                            "phone": phone,
                        "verification": 'false'
                        },
                        "images": ["https://xxx.xxx.com"]                                       # 待改进
                    }
                    data.append(the_data)
                result = {
                    "code": 0,
                    "data": data,
                    total: total,
                    "totalPage": totalPage,
                    "page": page,
                    "msg": "ok"
                }

                return JsonResponse(data = result, safe = False)
            
        # 后端错误
        except:
            result = Response.BackendErrorResponse()
            return result
    # 不使用GET方法
    else:
        result = Response.HttpMethodErrorResponse()
        return result