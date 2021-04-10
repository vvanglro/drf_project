from collections import OrderedDict

from rest_framework import mixins, filters, permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework_simplejwt import authentication

from .filters import GoodsFilter
from .models import Goods, GoodsCategory
from .serializers import GoodsSerializer,CategorySerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


class GoodsPagination(PageNumberPagination):
    '''
    自定义分页
    '''
    page_size = 12  # 设置一页默认的数量 前端可根据需求传数量比如 http://127.0.0.1:8000/goods/?p=3&page_size=20
    page_size_query_param = 'page_size'  # 设置一页的数量
    page_query_param = 'page'  # 设置页码参数名
    max_page_size = 50  # 一页最大的数量

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('link', {
                'pre':self.get_previous_link(), 'next':self.get_next_link()
            }
             ),
            ('results', data),
            ('code',200)
        ]))


class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表页，分页，过滤，搜索，排序
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # permission_classes = [permissions.IsAuthenticated]  # 权限认证主要是这个
    # authentication_classes = (authentication.JWTAuthentication,)
    pagination_class = GoodsPagination  # 分页
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filter_class = GoodsFilter  # DjangoFilterBackend  过滤
    search_fields = ['name', 'goods_brief', 'goods_desc']  # filters.SearchFilter 搜索
    ordering_fields = ['sold_num', 'shop_price','add_time']  # filters.OrderingFilter 排序


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    list:
        商品分类列表数据
    '''
    queryset = GoodsCategory.objects.filter(category_type=1)
    # queryset = GoodsCategory.objects.all()
    serializer_class = CategorySerializer



class HotWordsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    热搜词
    '''
    pass