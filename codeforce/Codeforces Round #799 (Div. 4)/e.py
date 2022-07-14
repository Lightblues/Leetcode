""" E. Binary Deque
给定一个长n的数组, 可以从两端去掉数字, 问最少多少次可以是的数组和为s.
限制: n,s 2e5. 需要在线性时间求解
思路: 用一个 #哈希表 记录出现过的 #前缀和 然后遍历的时候检查是否出现过匹配元素.
"""

def f():
    n, s = map(int, input().split())
    nums = list(map(int, input().split()))
    acc2idx = {0: -1}
    acc = 0
    ans = float('inf')
    for i, num in enumerate(nums):
        acc += num
        if acc - s in acc2idx:
            ans = min(ans, n - (i - acc2idx[acc-s]))
        if acc not in acc2idx:
            acc2idx[acc] = i
    return -1 if ans == float('inf') else ans

for _ in range(int(input())):
    print(f())

