# -*- coding: utf-8 -*-
# @Time    : 2021/3/5 16:32
# @Author  : wanghao
# @File    : views_base.py
# @Software: PyCharm
import json


from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View
from goods.models import Goods

# 基于django自带的View
class GoodsListView(View):

    # def get(self,request):
    #     '''
    #     通过django的view实现商品列表页
    #     :param request:
    #     :return:
    #     '''
    #     json_list = []
    #     goods = Goods.objects.all()[:10]
    #     for good in goods:
    #         json_dict = {}
    #         json_dict['name'] = good.name
    #         json_dict['category'] = good.category.name
    #         json_dict['market_price'] = good.market_price
    #         json_list.append(json_dict)
    #
    #     return HttpResponse(json.dumps(json_list), content_type='application/json')

    # def get(self,request):
    #     '''
    #     通过django的model_to_dict序列化商品列表
    #     使用这种方法时datetime和imagefile类型的字段无法使用json.dumps序列化返回
    #     :param request:
    #     :return:
    #     '''
    #     from django.forms import model_to_dict
    #     json_list = []
    #     goods = Goods.objects.all()[:10]
    #     for good in goods:
    #         json_dict = model_to_dict(good)
    #         json_list.append(json_dict)
    #
    #     return HttpResponse(json.dumps(json_list), content_type='application/json')


    def get(self,request):
        '''
        通过django的serializers序列化商品列表
        使用这种方法时datetime和imagefile类型的字段正确返回
        :param request:
        :return:
        '''
        from django.core import serializers

        goods = Goods.objects.all()[:10]
        json_data = serializers.serialize('json',goods)
        return JsonResponse(json.loads(json_data), safe=False)
