""" 
在长度k的限制下, 找到数组中的最大子数组和. 限制: n 2e5
思路0: 不知道为什么 #WA 了
    没有长度限制的情况下, dp[i] 表示以i结尾的最大值, 则有 dp[i] = arr[i] + max(0, dp[i-1])
    加了长度限制, 问题是处理 [2,2,-3,...] 的情况, 若第一个2不能选, 则应该缩减到-3后面!
    为此, 对于每一个负数, 构建其「前缀覆盖段」, 
        具体而言, 可以用一个back数组, 标记到该位置时, 是否应该缩减
思路1: #前缀和 + #单调队列
[带长度限制的最大子数组和](https://chengzhaoxi.xyz/f1d4b382.html)
[最大子数组和的三种解法](https://chengzhaoxi.xyz/8501.html)
"""

def getMaxProfit(arr, k):
    # WA!
    n = len(arr)
    back = [False] * n
    acc = 0
    for i in range(n-1,-1,-1):
        acc += arr[i]
        if acc < 0: back[i] = True
        acc = min(0, acc)
    # 
    mx = 0
    acc = 0
    l = 0
    for i,x in enumerate(arr):
        if acc<0:
            acc = x
            l = i
            mx = max(mx, acc)
        else:
            acc += x
            if i-l+1>k:
                acc -= arr[l]
                l += 1
                while l<i and back[l]: 
                    acc -= arr[l]
                    l += 1
            mx = max(mx, acc)
    return mx

from collections import deque
def getMaxProfit(arr,k):
    n = len(arr)
    sums = [0] * (n + 1)    # 前缀和
    deq = deque([0])
    ans = 0
    for i in range(n):
        v = arr[i]
        sums[i + 1] = sums[i] + v
        mx = sums[deq[0]]
        ans = max(ans, sums[i + 1] - mx)
        while len(deq) > 0 and sums[deq[-1]] >= sums[i + 1]:
            deq.pop()
        deq.append(i + 1)
        if i - (deq[0] - 1) + 1 > k:
            deq.popleft()
    return ans

# 15
# 8
for ans in (
    getMaxProfit([-3,4,3,-2,2,5], 4),   # 8
    getMaxProfit([4,3,-2,9,-4,2,7], 6),   # 15
    getMaxProfit([3,2,2,-4,1,-2,3,7], 5),
    getMaxProfit([2,3,-2,-2,4,5], 5),
    getMaxProfit([-2,-2], 5),
    getMaxProfit([2,5,-7,8,-6,4,1,-9], 5),  # 8
):
    print(ans)