""" 给定一个序列的长度n，接下来n个数，表示一个序列，要求输出这个序列的中位数和平均数，中位数和平均数都要四舍五入到整数
限制: 数量 n 2e5; 数值 1e5
等价于求「流数据中的中位数」 原题[剑指 Offer 41. 数据流中的中位数](https://leetcode.cn/problems/shu-ju-liu-zhong-de-zhong-wei-shu-lcof/)
思路0: Python直接作弊 #有序数组
思路1: 正经的做法, 可以维护一个最大堆和最小堆分别存前后一半
    注意数组长度的维护
 """

from sortedcontainers import SortedList

n = int(input())
arr = list(map(int, input().split()))

means = [0] * n
medians = [0] * n

# 注意自带的 round 不是四舍五入!
def round_5(x):
    return int(x + 0.5)

s = 0
sl = SortedList()
for i,x in enumerate(arr):
    s += x
    means[i] = round_5(s / (i+1))
    sl.add(x)
    if (i+1) % 2:
        medians[i] = round_5(sl[(i+1)//2])
    else:
        medians[i] = round_5((sl[i//2] + sl[i//2+1]) / 2)

print(" ".join(map(str, means)))
print(" ".join(map(str, medians)))