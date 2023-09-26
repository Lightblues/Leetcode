""" TODO: 复杂度不够
定义数组的权重为, 任意两个数的异或之和. 
所有 连续子数组 的权值和是多少. 答案取模. 
限制: n 1e5
思路0: 暴力, O(n^2)
    考虑 i,j 两个位置的元素, 它们会被计算多少次异或值? 
    此时, 子数组一定包含 [i...j] 这个区间, 再遍历所有, 一共计数 (i+1)*(n-j) 次
"""
n = int(input())
arr = list(map(int, input().split()))
mod = 10**9+7

def brust(arr):
    n = len(arr)
    ans = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            ans += (arr[i]^arr[j]) * (i+1) * (n-j)
            ans %= mod
    return ans
print(brust(arr))