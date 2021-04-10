"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.views import static

import xadmin
from MxShop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from goods.views import GoodsListViewSet, CategoryViewSet
from users.views import MyTokenObtainPairView, SmsCodeViewset, UserViewset
from user_operation.views import UserFavViewset

router = DefaultRouter()

# 配置goods的url
router.register(r'goods', GoodsListViewSet, basename='goods')

# 配置category的url
router.register(r'categorys', CategoryViewSet, basename='categorys')

# 配置发送短信的url
router.register(r'code', SmsCodeViewset, basename='codes')
# 注册用户
router.register(r'users', UserViewset, basename='users')
# 收藏
router.register(r'userfavs', UserFavViewset, basename='userfavs')

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # drf页面的登录接口
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # 图片url
    path('media/<path:path>', serve, {"document_root": MEDIA_ROOT}),
    # 静态资源路由地址
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

    # 配置xadmin中商品详情的富文本url 配置了才可以上传图片
    path('ueditor/', include('DjangoUeditor.urls')),
    # 商品列表页
    path('', include(router.urls)),

    # drf的接口文档生成页面
    path('docs/', include_docs_urls(title='慕学生鲜')),

    # drf 自带的token认证模式
    path('api-token-auth/', views.obtain_auth_token),

    # djangorestframework-simplejwt库的认证接口
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 继承自djangorestframework-simplejwt库TokenObtainPairView类的登录
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pairs'),

    # 刷新JWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 验证token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
