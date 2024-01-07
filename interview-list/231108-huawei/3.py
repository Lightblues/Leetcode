""" 
给定一颗完全二叉树表示待运行任务. 需要从高层往下执行. 同层优先级相同. 
给定CPU运行时长, 在保证「利用率最高」的情况下最大完成的任务数量. 
限制: 节点数量 1e3; CPU 可运行时长 1e3
思路1: 转为背包DP
    问题转为, 给定arr, 求在MX限制下的最大和, 相同情况下要求数量最多. 
    例如: [4,5,6,9], MX=13 -> [9,4], out=2
    利用长度为 MX的DP数组, f[i] 表示和为i情况的最大数量. 对于一个新的数字x,
        f[i] = max(f[i], f[i-x]+1)
"""

def max_limit_count(arr, mx):
    if mx==0:
        return arr.count(0)
    # reverse sort?
    arr.sort(reverse=True)
    dp = [-1] * (mx+1)
    dp[0] = 0
    for x in arr:
        for i in range(mx, x-1, -1):
            dp[i] = max(dp[i], dp[i-x]+1)
    for i in range(len(dp)-1,-1,-1):
        if dp[i] != -1:
            return dp[i]
# print(max_limit_count([4,5,6,9], 13))
# print(max_limit_count([0,4,5,6,9,0], 13))
# print(max_limit_count([1], 0))

n = int(input())
arr = list(map(int, input().split()))
limit = int(input())
idx = 0; length = 1
ans = 0
while idx < n and limit >= 0:
    if sum(arr[idx:idx+length]) <= limit:
        ans += length
        limit -= sum(arr[idx:idx+length])
        idx += length
        length <<= 1
    else:
        ans += max_limit_count(arr[idx:idx+length], limit)
        break
print(ans)