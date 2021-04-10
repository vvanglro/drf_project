# -*- coding: utf-8 -*-
# @Time    : 2021/3/18 14:40
# @Author  : wanghao
# @Email   : hz20126002@huize.com
# @File    : exception.py
# @Software: PyCharm

# 自定义异常处理
from rest_framework.views import exception_handler
from rest_framework.views import Response
from rest_framework import status


# 将仅针对由引发的异常生成的响应调用异常处理程序。它不会用于视图直接返回的任何响应
def custom_exception_handler(exc, context):
    # 先调用REST framework默认的异常处理方法获得标准错误响应对象
    response = exception_handler(exc, context)
    print(exc)    #错误原因   还可以做更详细的原因，通过判断exc信息类型
    print(type(exc))    #错误原因   还可以做更详细的原因，通过判断exc信息类型
    print(context)  #错误信息
    print('1234 = %s - %s - %s' % (context['view'], context['request'].method, exc))

    if response is None:

        return Response({
            'message': '服务器错误'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)

    else:
        # 这个循环是取第一个错误的提示用于渲染
        # for index, value in enumerate(response.data):
        #     if index == 0:
        #         key = value
        #         value = response.data[key]
        #
        #         if isinstance(value, str):
        #             message = value
        #         elif isinstance(value, list):
        #             # message = key + value[0]
        #             message = value[0]
        #         elif isinstance(value, dict):
        #             dict_values = value.values()
        #             if dict_values:
        #                 message = list(dict_values)[0]
        #             else:
        #                 message = ''

        # 将所有的错误返回
        message = {}
        for k, v  in response.data.items():

            if isinstance(v, str):
                message[k] = v
            elif isinstance(v, list):
                message[k] = v[0]
                # message = value[0]
            elif isinstance(v, dict):
                dict_values = v.values()
                if dict_values:
                    message[k] = list(dict_values)[0]
                else:
                    message = ''
        # if len(message) == 1:
        #     message = list(message.values())[0]

        # print('123 = %s - %s - %s' % (context['view'], context['request'].method, exc))
        return Response({
            'message': message,
        }, status=response.status_code, exception=True)

    return response
