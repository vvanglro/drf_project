from rest_framework import mixins, status
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user_operation.authentication import MyJWTAuthentication
from .serializers import UserFavSerializer
from .models import UserFav
from utils.permissions import IsOwnerOrReadOnly


class UserFavViewset(viewsets.GenericViewSet,mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    '''
    用户收藏
    create:
        创建-用户收藏
    Destroy：
        删除-用户收藏
    List：
        获取-用户收藏列表
    '''

    # queryset = UserFav.objects.all()
    serializer_class = UserFavSerializer

    # IsOwnerOrReadOnly重写的权限 在删除和获取时会验证当前登录用户是否和操作的数据相匹配 也就是说验证当前登录用户是不是删除自己的数据和获取自己的数据
    # IsAuthenticated drf自带的权限 验证是否有登录
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    # 登录验证
    authentication_classes = (MyJWTAuthentication,)

    # url后面跟的就不是pk(主键id)了  而是goods_id
    lookup_field = 'goods_id'

    def get_queryset(self):
        # 获取当前登录用户的收藏
        return UserFav.objects.filter(user=self.request.user)


    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception:
            raise serializers.ValidationError({'': '未找到'})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)