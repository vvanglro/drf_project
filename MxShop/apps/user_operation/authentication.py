# -*- coding: UTF-8 -*-
"""
@author:wanghao
@file:authentication.py
@time:2021/03/28
"""
from rest_framework import serializers
from rest_framework_simplejwt.authentication import JWTAuthentication


class MyJWTAuthentication(JWTAuthentication):
    '''
    验证headers中的Authorization
    继承 重写报错返回msg
    '''
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            raise serializers.ValidationError({'': '身份信息未提供'})

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            raise serializers.ValidationError({'': '身份信息格式错误'})

        try:
            validated_token = self.get_validated_token(raw_token)
        except Exception:
            raise serializers.ValidationError({'': '身份信息验证未通过'})

        return self.get_user(validated_token), validated_token
