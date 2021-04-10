# -*- coding: utf-8 -*-
# @Time    : 2021/3/18 15:07
# @Author  : wanghao
# @Email   : hz20126002@huize.com
# @File    : serializers.py
# @Software: PyCharm
import re
from datetime import datetime, timedelta

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import VerifyCode

from MxShop.settings import REGRX_MOBILE

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    '''
    继承自djangorestframework-simplejwt库的登录认证序列化 并重写validate(返回的响应)
    token验证
    若使用drf默认登录认证，不能使用自定义表的用户信息，只可以用默认User表用户登录，通过python manage.py createsuperuser创建
    验证自定义用户模型https://blog.csdn.net/tlju_xiao_ma/article/details/114182293
    '''

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username  # 这个是你的自定义返回的
        data['user_id'] = self.user.id  # 这个是你的自定义返回的

        return data


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """

        # 手机号是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        # re.match
        # 从指定字符串的开始位置进行匹配。开始位置匹配成功则继续匹配，否则输出None。
        # 该方法的结果是返回一个正则匹配对象，通过两个方法获取相关内容：
        # 通过 group() 来获取内容
        # 通过 span() 来获取范围：匹配到字符的开始和结束的索引位置
        if not re.match(REGRX_MOBILE, mobile):
            raise serializers.ValidationError({'': "手机号码非法"})

        # 验证码发送频率
        '''
            第一次50分请求的
            one_mintes_ago = 49分
            add_time = 50
            第二次50.30
            one_mintes_ago = 49.30
            add_time = 50
            50 > 49.30
        '''
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)  # 获取一分钟以前的时间
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            # 如果添加时间大于一分钟以前的时间，则在这一分钟内已经发过短信，不允许再次发送
            raise serializers.ValidationError({'': "距离上一次发送未超过60s"})

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    '''
    用户
    '''
    # required=True 表示必填字段
    # write_only 将其设置True为确保在更新或创建实例时可以使用该字段，但在序列化表示时不包括该字段。 默认为 False
    code = serializers.CharField(label="验证码",required=True, write_only=True, max_length=4, min_length=4,
                                 error_messages={
                                     # 设置每种错误的错误提示
                                     'blank': '请输入验证码',  # 这是针对提交了该字段但是值是空的情况
                                     "required": "请输入验证码",  # 这是针对没提交该字段的提示
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误",
                                 },
                                 help_text='验证码')
    # allow_blank=False表示不能为空
    username = serializers.CharField(label="用户名",required=True, allow_blank=False,
                                     # UniqueValidator验证username字段唯一性
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='用户已经存在')]
                                     )

    # style={'input_type': 'password'} 在drf接口页面输入密码时不显示明文
    # label 也是在drf接口页面验证的参数名为密码 就不是显示的password了
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'}, label="密码",
    )

    # 第一种方法：保存时将明文密码加密
    def create(self, validated_data):
        # 重写create方法
        # 继承了serializer里的create方法
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        # 用户模型继承自django的AbstractUser模型 用AbstractUser模型的set_password
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_code(self, code):
        '''
            1.验证验证码是否存在
            2.验证码是否过期
            3.验证码是否正确
        '''
        # 在ModelSerializer前端传递过来的值都会放在initial_data里
        # self.initial_data 这里是获取前端传过来的参数 这里手机号前端是用username为key  order_by("-add_time")排序最新的
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by("-add_time")
        if verify_records:
            last_records = verify_records[0]
            five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)  # 获取五分钟以前的时间
            '''
            5分钟的有效期
            50分发的验证码
            52分来提交的
            52-5 = 47分
            47分小于50分
            '''
            if five_mintes_ago > last_records.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_records.msg_code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate_username(self, username):
        # 验证手机号码是否合法
        # re.match
        # 从指定字符串的开始位置进行匹配。开始位置匹配成功则继续匹配，否则输出None。
        # 该方法的结果是返回一个正则匹配对象，通过两个方法获取相关内容：
        # 通过 group() 来获取内容
        # 通过 span() 来获取范围：匹配到字符的开始和结束的索引位置
        if not re.match(REGRX_MOBILE, username):
            raise serializers.ValidationError({'': "手机号码非法"})
        return username

    def validate(self, attrs):
        '''
        validate是用于验证所有的字段
        attrs是所有字段验证后返回的data
        '''
        # 因为mobile值就是username的值, 所以我们把username的值赋值给mobile
        attrs["mobile"] = attrs['username']
        del attrs['code']  # code在UserProfile表中未定义 所以这里要删除掉
        return attrs

    class Meta:
        model = User
        # username必填, 因为UserProfile继承了AbstractUser
        # 模型类写了必填, 你序列化的字段写了这个字段的话, 那么前端必须传这个字段的数据
        # 这里因为用户模型是继承django的 所以username是必填字段
        fields = ("username", "code", "mobile","password")
