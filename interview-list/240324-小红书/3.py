""" 
初始有一个数组, 每次操作可以使得 ai+1, 但是对于某个i的两次操作至少间隔为2, 问ai变为数组中最大数字的时候, 数组和最小值
限制: n 1e5; ai 1e9
思路1:
    假设最大/小元素为 mx, mn; 原本数组和为 s
    对于非最小元素 x, 需要的操作次数为 2*(mx-x) -1, 因为间隔把没必要的操作施加到最小元素上即可
    对于唯一的最小元素 mn, 将其他数组从小到大排序, 则「注水」产生的空间是可以拓展的次数, 假设注水面积为 sq
        若 mx-mn <= sq+1, 则需要的操作次数为 2*(mx-mn) -1
        否则, 先经过 2*sq +1 将「水位填平」, 然后, 每 2*(n-1) 次, 
            mx, mn = mx+1, mn+(n-1)
            因此, 需要满足 mx+q <= mn+q(n-1), 得到 q >= (mx-mn)/n-2

3
3 1 4
# 9
# 15
# 8
2
1 3
# -1
# 0
"""
from math import ceil
n = int(input())
arr = list(map(int, input().split()))
mx, mn = max(arr), min(arr)
s = sum(arr)
ans = [2*(mx-x)-1 if x!=mx else 0 for x in arr]
if arr.count(mn)==1 and n>1:
    idx = arr.index(mn)
    sq = n*mx - s - (mx-mn)
    if (mx-mn) <= sq+1:
        ans[idx] = 2*(mx-mn) -1
    else:
        if n==2:
            ans[idx] = -1 - s
        else:
            ans_ = 2*sq + 1
            mn += sq + 1
            q = ceil((mx-mn)/(n-2)) - 1
            ans_ += 2*q*(n-1)
            mx += q
            mn += q*(n-1)
            # 
            ans_ += 2*(mx+1-mn)
            ans[idx] = ans_
ans = [x+s for x in ans]
for x in ans:
    print(x)
