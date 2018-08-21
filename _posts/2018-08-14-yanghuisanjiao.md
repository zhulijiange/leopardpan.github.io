---
layout: post
title: '杨辉三角形'
description: python程序
tag: 博客
---
## 打印杨辉三角形(只打印6层)

### 源码
    def get_next_line(L):
        '''此函数将用一层的列表L 计算下一层然后返回
           L = [1, 3, 3, 1], 则返回 [1, 4, 6, 4, 1]
        '''
        line = [1]  # 最左侧的1
        # 计算中间的数字
        for i in range(len(L) - 1):  # i绑定L的索引
            line.append(L[i] + L[i + 1])
        # 在最后放入一个1
        line.append(1)
        return line


    def get_yh_list(n):
        L = []
        line = [1]  # 当前是第一行
        for _ in range(n):
            L.append(line)  # 当前行放入
            # 再算出下一行
            line = get_next_line(line)
        return L


    def list_to_string(L):
        '''此函数任意给定一个列表,将其转换为字符串
        如: L = [1, 3, 3, 1], 则返回'1 3 3 1'
        '''
        L2 = [str(x) for x in L]  # L2 = ['1', '3', '3', '1']
        return ' '.join(L2)


    L = get_yh_list(6)

    # 得到最下面一行占几个字符的宽度:
    max_char = len(list_to_string(L[-1]))

    # 居中显示
    for line_list in L:
        s = list_to_string(line_list)
        print(s.center(max_char))
