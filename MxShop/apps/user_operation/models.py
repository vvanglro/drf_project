from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

from goods.models import Goods

User = get_user_model()


# Create your models here.

class UserFav(models.Model):
    '''
    用户收藏
    '''
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='用户')
    goods = models.ForeignKey(Goods, on_delete=models.SET_NULL,null=True, blank=True, verbose_name='商品')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        # 2种方法  也可以在序列化里加validators = [
        #             UniqueTogetherValidator(
        #                 queryset=UserFav.objects.all(),
        #                 fields = ('user','goods'),
        #                 message='已经收藏'
        #             )
        #         ]
        # 联合索引 如果保存数据时 有相同的数据 则数据库会报错
        # 比如 user=1 goods=1 表中已存在 再保存user=1 goods=1时会报错
        # unique_together= ("user","goods",)

    def __str__(self):
        if self.user.name:
            return self.user.name
        else:
            return self.user.username  # 父类AbstractUser原本的属性


class UserLeavingMessage(models.Model):
    '''
    用户留言
    '''
    MESSAGE_CHOICES = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (5, "求购"),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, blank=True, verbose_name='用户')
    message_type = models.IntegerField(default=1, choices=MESSAGE_CHOICES, verbose_name='留言类型',
                                       help_text='留言类型：1(留言),2(投诉),3(询问),4(售后),5(求购)')
    subject = models.CharField(max_length=100, default='', verbose_name='主题')
    message = models.TextField(default='', verbose_name='留言内容', help_text='留言内容')
    file = models.FileField(verbose_name='上传的文件', help_text='上传的文件')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject


class UserAddress(models.Model):
    '''
    用户收货地址
    '''
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, blank=True, verbose_name='用户')
    district = models.CharField(max_length=100, default='', verbose_name='区域')
    address = models.CharField(max_length=100, default='', verbose_name='详细地址')
    signer_name = models.CharField(max_length=100, default='', verbose_name='签收人')
    signer_mobile = models.CharField(max_length=11, default='', verbose_name='电话')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address