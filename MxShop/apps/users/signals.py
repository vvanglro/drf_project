# -*- coding: utf-8 -*-
# @Time    : 2021/3/22 14:28
# @Author  : wanghao
# @Email   : hz20126002@huize.com
# @File    : signals.py
# @Software: PyCharm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

'''
https://docs.djangoproject.com/zh-hans/3.0/ref/signals/#module-django.db.models.signals
django的模型信号量
下面代码是在创建新用户完成时，截获signals，把保存的明文密码修改为密文
'''
# 第二种方法：保存时将明文密码加密
# sender的参数是模型 接收哪个模型的
# 在传过来的时候 created参数来区别是否是新建 新建时是True
@receiver(post_save,sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:
        '''
        instance这里返回的是user对象
        '''
        password= instance.password
        instance.set_password(password)
        instance.save()
