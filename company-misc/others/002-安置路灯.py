"""
时间限制：C/C++ 1秒，其他语言2秒

空间限制：C/C++ 32M，其他语言64M

小Q正在给一条长度为n的道路设计路灯安置方案。

为了让问题更简单,小Q把道路视为n个方格,需要照亮的地方用'.'表示, 不需要照亮的障碍物格子用'X'表示。

小Q现在要在道路上设置一些路灯, 对于安置在pos位置的路灯, 这盏路灯可以照亮pos - 1, pos, pos + 1这三个位置。

小Q希望能安置尽量少的路灯照亮所有'.'区域, 希望你能帮他计算一下最少需要多少盏路灯。


输入描述:
输入的第一行包含一个正整数t(1 <= t <= 1000), 表示测试用例数
接下来每两行一个测试数据, 第一行一个正整数n(1 <= n <= 1000),表示道路的长度。
第二行一个字符串s表示道路的构造,只包含'.'和'X'。

输出描述:
对于每个测试用例, 输出一个正整数表示最少需要多少盏路灯。

输入例子1:
2
3
.X.
11
...XX....XX

输出例子1:
1
3
"""

import sys
# import re
# import math

def roadlights():
    _n = int(sys.stdin.readline().strip())
    road = sys.stdin.readline()
    # toBeLighted = re.split('X+', road)
    # num_lights = 0
    # for segment in toBeLighted:
    #     num_lights += math.ceil(len(segment)/3) # 前后为空字符串也无所谓
    # print(num_lights)
    num_lights = 0
    i = 0
    while i< _n:
        char = road[i]
        if char == '.':
            num_lights += 1
            i += 3
        elif char == 'X':
            i += 1
    print(num_lights)


n = int(sys.stdin.readline().strip())
for _ in range(n):
    roadlights()

