# -*- coding: utf-8 -*-
# @Time    : 2021/3/18 15:09
# @Author  : wanghao
# @Email   : hz20126002@huize.com
# @File    : authentication.py
# @Software: PyCharm

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CustomBackend(ModelBackend):
    '''
    自定义用户验证
    需要在settings文件中配置
    # 自定义的用户登录效验
    AUTHENTICATION_BACKENDS = (
        'users.authentication.CustomBackend',
    )
    '''

    def authenticate(self, request, username=None, password=None, **kwargs):

            try:
                user = User.objects.get(Q(username=username) | Q(mobile=username))
            except Exception:
                raise serializers.ValidationError({'': '账号不存在'})

            if user.check_password(password):
                return user
            else:
                # 如果不想密码登录也可以验证码在这里写
                # 这里做验证码的操作
                raise serializers.ValidationError({'': '账号或密码错误'})


