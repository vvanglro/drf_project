from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class UserProfile(AbstractUser):
    '''
    用户
    继承的django自带的用户模型 所以需要去settings中设置来覆盖django默认的表  在settings中添加AUTH_USER_MODEL = 'users.UserProfile'
    '''
    # 用户注册时用的是mobile,没提供name之类的信息,所以可以为null
    # 注意null针对数据库,blank针对表单
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name='姓名')
    birthday = models.DateField(null=True, blank=True, verbose_name='出生年月')
    # 这里如果设置成不允许为null,那么在用户注册的Serializer里因为用了ModelSerializer,就要求mobile是必填的
    mobile = models.CharField(null=True, blank=True, max_length=11, verbose_name='电话')
    gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', '女')), default='female',
                              verbose_name='性别')
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name='邮箱')

    class Meta:
        verbose_name = '用户'  # 给你的模型类起一个更可读的名字
        verbose_name_plural = verbose_name  # 这个选项是指定，模型的复数形式是什么  若未提供该选项, Django 会使用 verbose_name + “s”.

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.username  # 父类AbstractUser原本的属性


class VerifyCode(models.Model):
    '''
    短信验证码,由手机号关联,回填验证码进行验证。可以保存在redis中
    '''
    msg_code = models.CharField(max_length=10, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='电话')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.msg_code
