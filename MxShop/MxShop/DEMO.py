# -*- coding: UTF-8 -*-
"""
@author:wanghao
@file:DEMO.py
@time:2021/04/04
"""


def to_find(var1, var2):
    index = []

    var1_len = len(var1)

    szm = var1[0]

    for k in range(len(var2)):
        if var2[k] == szm:
            # index.append(k)
            e = var1_len + k
            if var2[k:e] == var1:
                print("match found from {} to {}".format(k, e))
    # print(index)
    # for s in index:
    #     e = var1_len + s
    #     if var2[s:e] == var1:
    #         print("match found from {} to {}".format(s, e))


if __name__ == '__main__':
    var1 = 'to'

    var2 = 'This is a sample sentence to search for include help to search all occurrences'

    to_find(var1, var2)
