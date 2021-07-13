import json
from django.http.response import JsonResponse

from image.models import ImagePath
from utils.image_io.image_io import upload_image
from utils.response import Response
from .models import ProductType, ProductInfo
from auth_user.models import Yonghu
from django.db import transaction
from django.core.paginator import Paginator
from auth_user.views import format_user_data
from utils.jwt_auth.authentication import JSONWebTokenAuthentication
from utils.detect.detect_sensitives import detect_sensitives
import random


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
        "user_info": format_user_data(product_obj.user),
        "images": product_obj.images
    }
    return result


def create(request):
    """
    发布产品信息接口
    """
    # 使用POST方法
    if request.method == "POST":
        user_obj = JSONWebTokenAuthentication().authenticate(request)
        if user_obj is None:
            return Response.NotLoginResponse()
        # 提取前端数据
        image_stream = request.FILES.get("file")
        product_name_post = request.POST.get('product_name')
        product_name = detect_sensitives(product_name_post)
        product_detail_post = request.POST.get('product_detail')
        product_detail = detect_sensitives(product_detail_post)
        price_post = request.POST.get('price')
        inventory_post = request.POST.get('inventory')
        product_type_id_post = request.POST.get('product_type_id')
        print(request)
        product_type_filter = ProductType.objects.filter(product_type_id=product_type_id_post)
        # 产品名错误
        if product_name == product_name_post:
            return  Response.ProductnameErrorResponse()
        # 产品详情错误
        if product_detail == product_detail_post:
            return Response.ProductinfoErrorResponse()
        # 产品type存在
        if product_type_filter:
            product_type_obj = product_type_filter.first()
            with transaction.atomic():
                sid = transaction.savepoint()
                new_product = ProductInfo(product_name=product_name_post,
                                          product_detail=product_detail_post,
                                          price=price_post,
                                          inventory=inventory_post,
                                          product_type=product_type_obj,
                                          user=user_obj)
                new_product.save()
                return_url = upload_image(image_stream)
                if return_url:
                    image_path = ImagePath()
                    image_path.url = return_url
                    image_path.content_object = new_product
                    image_path.save()
                    transaction.savepoint_commit(sid)
                else:
                    transaction.savepoint_rollback(sid)
                    return Response.BackendErrorResponse()
            # 返回结果
            result = creat_result(new_product)
            return Response.Response(data=result)
        else:
            return Response.ProductTypeErrorResponse()
    return Response.BackendErrorResponse()


def update(request):
    """
    发布产品信息接口
    """
    # 使用POST方法
    if request.method == 'POST':
        try:
            userid_post = request.COOKIES.GET.get('userid')
            # 用户id不存在
            if not userid_post or not Yonghu.objects.filter(userid=userid_post):
                return Response.NotLoginResponse()
            # 提取前端数据
            data = request.body.decode('utf-8')
            data = json.loads(data)
            product_id = data.get('id')
            product_name_post = request.POST.get('product_name')
            product_name = detect_sensitives(product_name_post)
            product_detail_post = request.POST.get('product_detail')
            product_detail = detect_sensitives(product_detail_post)
            price = data.get('price')
            inventory = data.get('inventory')
            product_type_id = data.get('product_type_id')
            # 产品名错误
            if product_name == product_name_post:
                return Response.ProductnameErrorResponse()
            # 产品详情错误
            if product_detail == product_detail_post:
                return Response.ProductinfoErrorResponse()
            # 产品存在
            if ProductInfo.objects.filter(id=product_id):
                # 筛选产品
                product_obj = ProductInfo.objects.filter(id=product_id).first()
                # 筛选产品类型
                product_type_obj = ProductType.objects.filter(product_type_id=product_type_id).first()
                product_obj.product_name = product_name_post
                product_obj.product_detail = product_detail_post
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
    return Response.BackendErrorResponse()


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
        user_obj = JSONWebTokenAuthentication().authenticate(request)
        if user_obj is None:
            return Response.NotLoginResponse()
        # 从数据库查询产品类型信息
        the_products = ProductInfo.objects.filter(user=user_obj).order_by("-update_time")
        count = int(request.GET.get('count', default='10'))
        page = int(request.GET.get('page', default='1'))
        paginator = Paginator(the_products, count)
        total_page = paginator.page_range[-1]
        page_objs = paginator.get_page(page)
        data = [creat_result(page_obj) for page_obj in page_objs]
        return Response.Response(data=data, total=the_products.count(), total_page=total_page, page=page)
        # 后端错误
    result = Response.BackendErrorResponse()
    return result


def products_type(request):
    """
    根据类型id获取该类型的产品列表-GET
    """
    # 若使用GET方法且存在userid、产品类型id
    if request.method == 'GET':
        # 返回信息
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
        total_page = paginator.page_range[-1]
        # 获取总的页数
        page_objs = paginator.get_page(page)
        # 返回结果
        data = [creat_result(page_obj) for page_obj in page_objs]
        return Response.Response(data=data, total=the_products.count(), total_page=total_page, page=page)
    result = Response.BackendErrorResponse()
    return result


def recommond(request):
    """
    推荐产品接口-GET
    """
    products_all = ProductInfo.objects.all()
    products_len = products_all.count()
    if products_len < 9:
        data = [creat_result(page_obj) for page_obj in products_all]
    else:
        randints = random.sample(range(0, products_len), 10)
        page_objs = []
        for i in randints:
            page_objs.append(products_all[i])
            data = [creat_result(page_obj) for page_obj in page_objs]
    return Response.Response(data=data)


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
        # 从数据库查询产品类型信息
        product_name = request.GET.get('product_name', default='1')
        count = int(request.GET.get('count', default='10'))
        page = int(request.GET.get('page', default='1'))
        # 搜索包含product_name字段的产品
        the_products = ProductInfo.objects.filter(product_name__icontains=product_name)
        # 对筛选出来的产品the_products进行分页，每页为count个
        paginator = Paginator(the_products, count)
        # 获取总的页数
        page_objs = paginator.get_page(page)
        total_page = paginator.page_range[-1]
        # 返回结果
        data = [creat_result(page_obj) for page_obj in page_objs]
        return Response.Response(data=data, total=the_products.count(), total_page=total_page, page=page)
    return Response.BackendErrorResponse()
