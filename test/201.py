""" https://www.nowcoder.com/exam/test/92590355/detail?pid=62105810
给定一个长n的01序列, AB分别依次取数字, 直到剩余k个; AB的目标分别是使得剩余数字最大/最小

思路1: 贪心
    简单分析, 可知A始终取最左侧的0; B是最左侧的1
    边界: A/B 取不到 0/1 了 --  简单答案取 [:k] 即可

5 3
10110
> 
110

"""

import sys
import math

n,k = map(int, sys.stdin.readline().split())
arr = list(sys.stdin.readline().strip())

a = math.ceil((n-k)/2)
b = n-k - a

res = []
for ch in arr:
    if ch == '0':
        if a > 0: a -= 1
        else: res.append(ch)
    else:
        if b > 0: b -= 1
        else: res.append(ch)

print(''.join(res[:k]))  # 边界情况: A/B 取不到 0/1 了
