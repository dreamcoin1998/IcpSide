import json
from django.http.response import JsonResponse
from utils.response import Response
from .models import ProductType, ProductInfo
from auth_user.models import Yonghu
from datetime import datetime
from django.core.paginator import Paginator


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
        },
        "images": product_obj.images
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
            if not userid_post or not Yonghu.objects.filter(userid=userid_post):
                return Response.NotLoginResponse()
            # 提取前端数据
            data = request.body.decode('utf-8')
            data = json.loads(data)
            product_name_post = data.get('product_name')
            product_detail_post = data.get('product_detail')
            price_post = data.get('price')
            inventory_post = data.get('inventory')
            product_type_id_post = data.get('product_type_id')
            # 产品type存在
            if ProductType.objects.filter(product_type_id=product_type_id_post):
                product_type_obj = ProductType.objects.filter(product_type_id=product_type_id_post).first()
                user_obj = Yonghu.objects.filter(userid=userid_post).first()
                new_product = ProductInfo(product_name=product_name_post,
                                          product_detail=product_detail_post,
                                          price=price_post,
                                          inventory=inventory_post,
                                          product_type_id=product_type_obj,
                                          userid=user_obj)
                new_product.save()
                # 返回结果
                result = creat_result(new_product)
                return Response.Response(data=result)
            else:
                return Response.ProductTypeErrorResponse()
        # 后端错误
        except Exception as e:
            # TODO: 写日志
            return Response.BackendErrorResponse()


def update(request):
    """
    发布产品信息接口
    """
    # 使用POST方法
    if request.POST:
        try:
            userid_post = request.COOKIES.GET.get('userid')
            # 用户id不存在
            if not userid_post or not Yonghu.objects.filter(userid=userid_post):
                return Response.NotLoginResponse()
            # 提取前端数据
            data = request.body.decode('utf-8')
            data = json.loads(data)
            product_id = data.get('id')
            product_name = data.get('userid')
            product_detail = data.get('product_detail')
            price = data.get('price')
            inventory = data.get('inventory')
            product_type_id = data.get('product_type_id')
            # 产品存在
            if ProductInfo.objects.filter(id=product_id):
                # 筛选产品
                product_obj = ProductInfo.objects.filter(id=product_id).first()
                # 筛选产品类型
                product_type_obj = ProductType.objects.filter(product_type_id=product_type_id).first()
                product_obj.product_name = product_name
                product_obj.product_detail = product_detail
                product_obj.price = price
                product_obj.inventory = inventory
                # product_type：外键
                product_obj.product_type = product_type_obj
                product_obj.save()
                # 返回结果
                result = creat_result(product_obj)
                return Response.Response(data=result)
            # userid不存在或产品id不存在
            else:
                result = Response.ClientErrorResponse()
                return result
                # 后端错误
        except Exception as e:
            result = Response.BackendErrorResponse()
            return result


def get_product_info(request, product_id):
    """
    获取产品信息-GET方法
    """
    # 若使用GET方法
    if request.method == 'GET':
        # 获取传来的信息
        try:
            # 从数据库查询产品信息
            product_info_obj = ProductInfo.objects.filter(id=product_id).first()
            # 返回结果
            result = creat_result(product_info_obj)
            return Response.Response(data=result)
        # 获取传来的信息不成功，后端错误
        except:
            result = Response.BackendErrorResponse()
            return result


def product_types(request):
    """
    产品类型列表-GET
    """
    # 若使用GET方法
    if request.method == 'GET':
        # 返回信息
        try:
            # 从数据库查询产品类型信息
            product_type_objs = ProductType.objects.all()
            data = []
            for product_type_obj in product_type_objs:
                product_type_id = product_type_obj.product_type_id
                type_name = product_type_obj.type_name
                type = {
                    "id": product_type_id,
                    "type_name": type_name
                }
                data.append(type)
            return Response.Response(data=data)
        # 后端错误
        except:
            result = Response.BackendErrorResponse()
            return result


def my_products(request):
    """
    获取用户发布的产品列表-GET
    """
    # 若使用GET方法
    if request.method == 'GET':
        # 返回信息
        try:
            userid_post = request.COOKIES.GET.get('userid')
            # 用户id不存在
            if not userid_post or not Yonghu.objects.filter(userid=userid_post):
                return Response.NotLoginResponse()
            # 从数据库查询产品类型信息
            the_products = ProductInfo.objects.filter(userid=userid_post)
            count = int(request.GET.get('count', default='10'))
            page = int(request.GET.get('page', default='1'))
            paginator = Paginator(the_products, count)
            page_objs = paginator.get_page(page)
            data = [creat_result(page_obj) for page_obj in page_objs]
            return Response.Response(data=data)
        # 后端错误
        except:
            result = Response.BackendErrorResponse()
            return result


def products_type(request):
    """
    根据类型id获取该类型的产品列表-GET
    """
    # 若使用GET方法且存在userid、产品类型id
    if request.method == 'GET':
        # 返回信息
        try:
            # 从数据库查询产品类型信息
            product_type_id = request.GET.get('id')
            # 若类型id不存在
            if not ProductType.objects.filter(product_type_id = product_type_id):
                return Response.ProductTypeErrorResponse()
            count = int(request.GET.get('count', default='10'))
            page = int(request.GET.get('page', default='1'))
            # 筛选该类型下的产品
            the_products = ProductInfo.objects.filter(product_type_id = product_type_id)
            # 对筛选出来的产品the_products进行分页，每页为count个
            paginator = Paginator(the_products, count)
            # 获取总的页数
            page_objs = paginator.get_page(page)
            # 返回结果
            data = [creat_result(page_obj) for page_obj in page_objs]
            return Response.Response(data=data)
        # 后端错误
        except:
            result = Response.BackendErrorResponse()
            return result


def recommond(request):
    """
    推荐产品接口-GET
    """
    pass


def get_all_products(request):
    """
    获取所有产品-GET
    """
    # 若使用GET方法且存在userid
    if request.method == 'GET':
        # 返回信息
        try:
            # 从数据库查询产品类型信息
            the_products = ProductInfo.objects.all()
            total = the_products.count()
            count = int(request.GET.get('count', default='10'))
            page = int(request.GET.get('page', default='1'))
            # 对筛选出来的产品the_products进行分页，每页为count个
            paginator = Paginator(the_products, count)
            # 获取总的页数
            page_objs = paginator.get_page(page)
            total_page = paginator.page_range[-1]
            # 返回结果
            data = [creat_result(page_obj) for page_obj in page_objs]
            return Response.Response(data=data, total=total, total_page=total_page, page=page)
        # 后端错误
        except:
            return Response.BackendErrorResponse()


def search_products(request):
    """
    搜索产品-GET
    """
    # 若使用GET方法且存在userid
    if request.method == 'GET':
        # 返回信息
        try:
            # 从数据库查询产品类型信息
            product_name = request.GET.get('product_name', default='1')
            count = int(request.GET.get('count', default='10'))
            page = int(request.GET.get('page', default='1'))
            the_products = ProductInfo.objects.filter(product_name = product_name)
            # 对筛选出来的产品the_products进行分页，每页为count个
            paginator = Paginator(the_products, count)
            # 获取总的页数
            page_objs = paginator.get_page(page)
            # 返回结果
            data = [creat_result(page_obj) for page_obj in page_objs]
            return Response.Response(data=data)
        # 后端错误
        except:
            return Response.BackendErrorResponse()
