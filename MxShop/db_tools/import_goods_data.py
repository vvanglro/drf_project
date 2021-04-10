# -*- coding: utf-8 -*-
# @Time    : 2021/3/5 14:50
# @Author  : wanghao
# @File    : import_goods_data.py
# @Software: PyCharm
# 独立使用django的model
import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))  # 获取当前文件路径
sys.path.append(pwd + "../")  # 将当前文件路径加到python执行搜索路径
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MxShop.settings')

import django

django.setup()

# 需要放到django.setup()后才可以使用django的model
from goods.models import Goods, GoodsCategory, GoodsImage
from db_tools.data.product_data import row_data

for goods_detail in row_data:
    goods = Goods()
    goods.name = goods_detail['name']
    goods.market_price = float(int(goods_detail['market_price'].replace('￥', '').replace('元', '')))
    goods.shop_price = float(int(goods_detail['sale_price'].replace('￥', '').replace('元', '')))
    goods.goods_brief = goods_detail['desc'] if goods_detail['desc'] is not None else ''
    goods.goods_desc = goods_detail['goods_desc'] if goods_detail['goods_desc'] is not None else ''
    goods.goods_front_image = goods_detail['images'][0] if goods_detail['images'] else ''

    category_name = goods_detail['categorys'][-1]
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    goods.save()

    for goods_image in goods_detail['images']:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.goods = goods
        goods_image_instance.save()

