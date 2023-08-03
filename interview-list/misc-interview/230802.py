""" 
定义操作A为合并相邻的重复元素, 分数为所得到的数组长度. 需要将一个长度为n的数组切分为k块, 问可得的最大分数之和. 
限制: n 1e5
思路1: #贪心 注意到, 一个切分操作最多增加整体分数值1
    因此, 记整体的分数为a, 统计最多容许进行切分的个数即可

8 3
1 1 1 2 2 3 3 1
# 6
1 4
1 1 1 1 1 1 1 1
# 3
"""

n,k = map(int, input().split())
arr = list(map(int, input().split()))

a = b = 0
pre = -1
for x in arr:
    if x!=pre:
        a += 1
    else:
        b += 1
    pre = x

print(a + min(b, k-1))