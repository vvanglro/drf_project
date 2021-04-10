# -*- coding: UTF-8 -*-
"""
@author:wanghao
@file:permissions.py
@time:2021/03/28
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    对象级权限仅允许对象的所有者对其进行编辑
    模型实例具有`user`属性。
    """

    def has_object_permission(self, request, view, obj):
        # 任何请求都允许读取权限，
        # 所以我们总是允许GET，HEAD或OPTIONS 请求.
        if request.method in permissions.SAFE_METHODS:
            return True

        # obj是模型
        # 验证当前登录的用户是否与 当前登录用户操作的模型数据中关联的用户相匹配
        return obj.user == request.user