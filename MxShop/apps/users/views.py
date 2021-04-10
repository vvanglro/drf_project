from random import choice
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import TokenObtainPairView
from MxShop.settings import APIKEY
from utils.yunpian import YunPian
from .serializers import MyTokenObtainPairSerializer,SmsSerializer,UserRegSerializer
from .models import VerifyCode

from django.contrib.auth import get_user_model
User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    '''
    继承自djangorestframework-simplejwt库的登录认证
    自定义序列化类
    '''

    serializer_class = MyTokenObtainPairSerializer



class SmsCodeViewset(CreateModelMixin,viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer


    def generate_code(self):
        '''
        生成四位数字的验证码
        :return:
        '''
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return ''.join(random_str)

    def create(self, request, *args, **kwargs):
        '''
            get_serializer 在这里获取的是上边的SmsSerializer
            raise_exception=True 表示如果is_valid里触发异常会被drf捕捉到，状态码drf设置为400.则不会继续往下执行代码
            短信接口发送成功在保存发送的验证码和手机号
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']

        yun_pian = YunPian(APIKEY)
        code = self.generate_code()
        sms_status= yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status['code'] != 0:
            return Response({
                'mobile':sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(msg_code=code,mobile=mobile)
            code_record.save()
            return Response({
                'mobile': mobile
            }, status=status.HTTP_201_CREATED)



class UserViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()

    '''
    注册返回token
    在视图类中导入from rest_framework_simplejwt.tokens import RefreshToken
    重写create方法，需要通过前边导入的RefreshToken来获取token返回给前端。
    '''
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        ret_dict = serializer.data
        # 给用户生成token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        # 将token添加到返回的data中
        ret_dict["token"] = access_token


        headers = self.get_success_headers(serializer.data)
        return Response(ret_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        '''
        源码里只是serializer.save() 没有返回
        上边的create要使用保存后的数据 所以这里加return回去
        :param serializer:
        :return:
        '''
        return serializer.save()