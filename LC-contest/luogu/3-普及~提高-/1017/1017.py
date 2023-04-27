""" P1017 [NOIP2000 提高组] 进制转换 #进制 #math
相较于一般情况下的正数base进制, 这里给定一个数字n, 要求转为 -R 进制
限制: -R的范围 [-20, -2], 所给数字绝对值范围 37336
see: [Negative base](https://en.wikipedia.org/wiki/Negative_base#Calculation)
观察: 例如以 -2 为base, 则不同因子的大小分别为 1, -2, 4, -8,...
    注意到, 只用第一项可以构成1, 用前两项可以新构成-1...-2, 用前三项可以新构成2...5, 前四项可以新构成-3...-10
        可以表示的范围为 [0,1]长2, [-2,1]长4, [-2,5]长8, [-10,5]长16, ...
    每多用一个因子, 可以在正数/负数上多一些表示空间. 并且正好长度n的数字可以表示 `base^n` 个数字
    比较正数base, 可表示的范围长度是一样的, 不过只能在正数范围内增长.
思路1: 有标准的流程
    对于待转换的数字n, 我们每次找到满足 `n/base = n'...r`, 其中保证余数r为最小正数. 重复直到商n'为0. 这样, 所得的余数反向排列就是需要的-R进制表示.
    为什么要求余数为正? 因为我们最近的数字表示都是用的正数.
    算法的正确性: 直观理解, 每次除base的过程中, 商的正负号每次都发生变化; 并且每间隔两次的绝对值都在减小, 正好落在上述观察的区间之内.
总结: 从直观上理解了负base的基本操作, 对于转换算法没有进行证明.
"""
import math
n, base = map(int, input().split())
nn = n
ans = []
while n:
    # if n<0:
    #     a = math.ceil(n/base)
    #     ans.append(n - a*base)
    #     n = a
    # else:
    #     a = math.ceil(n/base)
    #     ans.append(n - a*base)
    #     n = a
    a = math.ceil(n/base)
    ans.append(n - a*base)
    n = a
baseLabels = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
label = "".join(baseLabels[i] for i in ans[::-1])
print(f"{nn}={label}(base{base})")