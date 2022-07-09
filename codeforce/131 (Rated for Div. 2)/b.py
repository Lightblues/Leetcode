""" B. Permutation
对于1...n的排列p, 和一个数字d, 定义分数为所有满足 `p[i]*d = p[i+1]` 的下标数量之和. 现在给定数字n, 求使得分数最大的d和排列.
思路1: #贪心
    显然d取最小的2即可. 然后对于每各可选的数字取 d, d*2, d*2^2... 即可.
    为了避免遗漏, 可以用一个数组记录已经用过的数字, 然后遍历 1...n 输出即可.
"""
t = int(input())
# nums = list(range(1, 2*1e5+10))
for _ in range(t):
    n = int(input())
    used = [False] * (n+1)
    print(2)
    for i in range(1, n+1):
        # if used[i] or i>n: continue
        while i<=n and (not used[i]):
            print(i, end=" "); used[i] = True
            i *= 2
    print()