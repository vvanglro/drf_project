# -*- coding: UTF-8 -*-
"""
@author:wanghao
@file:serializers.py
@time:2021/03/27
"""
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import UserFav
from goods.models import Goods


class CurrentUser():
    # https://blog.csdn.net/qq_40999403/article/details/81069598
    def set_context(self,serializer_field):
        user_info = serializer_field.context['request'].user
        # print(user_info)
        # print(type(user_info))
        if type(user_info) == AnonymousUser:
            raise serializers.ValidationError({'':"用户信息错误"})
        else:
            self.user = user_info

    def __call__(self):
        return self.user

    def __repr__(self):
        return '%s()' % self.__class__.__name__

class UserFavSerializer(serializers.ModelSerializer):

    # 获取当前用户
    user = serializers.HiddenField(
        default=CurrentUser() #自己重写了
    )

    # 验证用户收藏表中关联的Goods id是否存在
    goods = serializers.PrimaryKeyRelatedField(
        queryset=Goods.objects.all(), required=True,
        error_messages={
            'required': '该字段为必填项',
            'does_not_exist': '请输入正确的id',
            'incorrect_type': '请输入正确的id',
        },
    )

    class Meta:
        model = UserFav
        # 2种方法  也可以在模型里加 unique_together= ("user","goods",)
        # 联合索引 如果保存数据时 有相同的数据 则数据库会报错
        # 比如 user=1 goods=1 表中已存在 再保存user=1 goods=1时会报错
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields = ('user','goods'),
                message='您已收藏',
            )
        ]

        fields = ('user','goods','id')