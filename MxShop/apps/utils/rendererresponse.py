# -*- coding: utf-8 -*-
# @Time    : 2021/3/18 14:41
# @Author  : wanghao
# @Email   : hz20126002@huize.com
# @File    : rendererresponse.py
# @Software: PyCharm
'''
自定义返回处理
'''

# 导入控制返回的JSON格式的类
from rest_framework.renderers import JSONRenderer


class customrenderer(JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            # print(renderer_context)
            # print(renderer_context["response"].status_code)

            # 响应的信息，成功和错误的都是这个
            # 成功和异常响应的信息，异常信息在前面自定义异常处理中已经处理为{'message': 'error'}这种格式
            # print(data)

            if isinstance(data, dict):
                msg = data.pop('message', 'success')
                code = data.pop('code', renderer_context["response"].status_code)
            else:
                msg = 'success'
                code = renderer_context["response"].status_code

            # # 重新构建返回的JSON字典
            # for key in data:
            #     # 判断是否有自定义的异常的字段
            #     if key == 'message':
            #         msg = data[key]
            #         data = ''
            #         code = 0
            if not data:
                data=''

            ret = {
                'msg': msg,
                'code': code,
                'data': data,
            }
            # 返回JSON数据
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)