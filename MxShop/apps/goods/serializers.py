# -*- coding: utf-8 -*-
# @Time    : 2021/3/5 17:50
# @Author  : wanghao
# @File    : serializers.py
# @Software: PyCharm

from rest_framework import serializers
from goods.models import Goods, GoodsCategory, GoodsImage


class CategorySerializer3(serializers.ModelSerializer):
    '''
    商品类别序列化
    '''
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    '''
    商品类别序列化
    '''
    sub_cat = CategorySerializer3(many=True)  # 将二级类别下关联的三级类别序列化嵌套进来
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    '''
    商品类别序列化
    '''
    sub_cat = CategorySerializer2(many=True)  # 将一级类别下关联的二级类别序列化嵌套进来
    class Meta:
        model = GoodsCategory
        fields = "__all__"



class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    '''
    商品的序列化
    '''
    # 将商品关联的类别序列化返回
    category = CategorySerializer()
    # Goods模型里没有images这个字段 但是GoodsImage模型里外键是Goods模型 外键字段goods有设置related_name='images' 所以这里可以这样使用
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"