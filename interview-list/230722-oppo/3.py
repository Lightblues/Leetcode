""" 对于一个数组arr, 每次进行后缀删除, 删除第i个数字的概率为 a[i]/sum, 问期望删除的次数
限制:  n 100

思路1: #DP
    定义 f[i] 表示从开始删除到位置i的期望操作次数. 则有递推
        f[i] = 1 + sum{ prob[j] * f[j-1], j=0...i }
"""
# n = int(input())
# arr = list(map(int, input().split()))
# # from itertools import accumulate
# # acc = list(accumulate(arr, initial=0))
# from functools import lru_cache
# @lru_cache(None)
# def f(i):
#     if i==-1: return 0
#     s = sum(arr[:i+1])
#     ans = 1
#     for j in range(0,i+1):
#         ans += arr[j]/s * f(j-1)
#     return ans
# print(f(n-1))


from itertools import accumulate

n = int(input())
arr = list(map(int, input().split()))

acc = list(accumulate(arr, initial=0))
f = [0] * (n+1)
for i in range(n):
    s = acc[i+1]
    tmp = 1
    for j in range(0,i+1):
        tmp += arr[j]/s * f[j]
    f[i+1] = tmp
print(f[n])
    
