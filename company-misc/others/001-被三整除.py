
"""
小Q得到一个神奇的数列: 1, 12, 123,...12345678910,1234567891011...。

并且小Q对于能否被3整除这个性质很感兴趣。

小Q现在希望你能帮他计算一下从数列的第l个到第r个(包含端点)有多少个数可以被3整除。


输入描述:
输入包括两个整数l和r(1 <= l <= r <= 1e9), 表示要求解的区间两端。

输出描述:
输出一个整数, 表示区间内能被3整除的数字个数。

输入例子1:
2 5

输出例子1:
3

例子说明1:
12, 123, 1234, 12345...
其中12, 123, 12345能被3整除。
"""

import sys

nums = sys.stdin.readline().split()
a, b = [int(n.strip()) for n in nums]
interval = b-a+1

n, m = interval//3, interval%3
count = n*2
if m==1:
    if not a%3 == 1:
        count += 1
elif m==2:
    if a%3 == 2:
        count += 2
    else:
        count += 1
print(count)
