""" 对于一个给定的n, 要求找到都 !=2 的正整数 (x,y), 使得下面的绝对值最接近 0
    |x!y - y - n|
问题转换: 要求 (x!-1)*y 尽量接近 n
注意到 factorial 的增长是非常快的, 所以直接暴力枚举x就好了
"""
import math
n = int(input())

mn = n
ans = [1,1] # 初始化
for x in range(3,100):  # 注意从3开始
    xx = math.factorial(x) - 1
    if xx > 1e10: break
    candidate = round(n/xx)
    # 找到最匹配的那个y
    if candidate==2:
        # 限制条件
        if abs(xx-n) < mn:
            mn = abs(xx-n)
            ans = [x,1]
        if abs(xx*3-n) < mn:
            mn = abs(xx*3-n)
            ans = [x,3]
    else:
        if abs(xx*candidate-n) < mn:
            mn = abs(xx*candidate-n)
            ans = [x,candidate]
print(' '.join(map(str,ans)))

