# -*- coding: utf-8 -*-
# @Time    : 2021/3/8 14:21
# @Author  : wanghao
# @File    : filters.py
# @Software: PyCharm

import django_filters
from django.db.models import Q
from django.http import JsonResponse

from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    '''
    商品的过滤类
    gte 大于等于
    lte 小于等于
    gt 大于
    lt 小于
    contains    模糊搜索
    icontains  加上i忽略大小写的模糊搜索
    iexact表示精确匹配, 并且忽略大小写
    exact表示精确匹配
    '''
    pricemin = django_filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    pricemax = django_filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')
    top_category = django_filters.NumberFilter(method='top_category_filter')

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    # @property
    # def qs(self):
    #     parent_qs = super(GoodsFilter, self).qs
    #     is_new_value = self.request.query_params.get('is_new')
    #     if is_new_value.capitalize() == 'True':
    #         return parent_qs
    #     elif is_new_value.capitalize() == 'False':
    #         return parent_qs.filter(is_new= False)
    #
    #     else:
    #         return parent_qs.filter(is_new=None)

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'name','is_new','is_hot']
