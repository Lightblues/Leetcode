""" 给定一组数字, 对于 1] 相同数字; 2] 数字之和为M的倍数 的两个数字, 可以构成一对. 问最多构成的数量. 
限制: n 2e5
思路0: 根据对m的mod来分组. 注意到优先对于数字之和匹配! 例如对于 4 2 2 5 6 12 3 可以构成3组
    对于两个取模分别为 i,j 满足 i+j=m 的数字, 假设 cnt[i] > cnt[j], 则可以构成 cnt[j] 对. 然后cnt[i]中剩余的相同数字可以另外构成!
    
"""

import sys
from collections import Counter, defaultdict

def getPairs(cnt):
    acc = 0
    for c in cnt.values():
        acc += c//2
    return acc
def getPairs(cnt):
    return sum(c//2 for c in cnt.values())

def maxMatch(arr: list[int], m: int):
    # NOTE: 注意这样会 #TLE 应该是因为 defaultdict 的原因
    mod2cnt = defaultdict(Counter)
    mod2sum = defaultdict(int)
    for x in arr:
        mod2cnt[x%m][x] += 1
        mod2sum[x%m] += 1
    ans = 0
    used = set()
    for x,cnt in mod2cnt.items():
        if m-x in used: continue
        used.add(x); used.add(m-x)
        if x==0:
            ans += sum(cnt.values()) // 2
            continue
        if m-x not in mod2cnt: 
            ans += getPairs(cnt)
            continue
        
        cnt2 = mod2cnt[m-x]
        acc1, acc2 = mod2sum[x], mod2sum[m-x]
        mx, mn = sorted(acc1, acc2)
        ans += mn + min(
            getPairs(cnt if acc1>acc2 else cnt2), (mx-mn) // 2
        )
    return ans


import sys
from collections import Counter
def maxMatch(arr: list[int], m: int):
    """ 转为list可以避免TLE """
    cnt = Counter(arr)
    mod2cnt = [0] * m
    mod2pairs = [0] * m
    for x,c in cnt.items():
        mod2cnt[x%m] += c
        mod2pairs[x%m] += c//2
    ans = mod2cnt[0] // 2
    if m%2==0:
        ans += mod2cnt[m//2] // 2
    for i in range(1, (m+1)//2):
        mn,mx = sorted([mod2cnt[i], mod2cnt[m-i]])
        _pairs = mod2pairs[
            i if mod2cnt[i]>mod2cnt[m-i] else m-i
        ]
        ans += mn + min(_pairs, (mx-mn)//2)
    return ans

n = int(sys.stdin.readline())
for _ in range(n):
    _, m = map(int, sys.stdin.readline().split())
    arr = list(map(int, sys.stdin.readline().split()))
    print(maxMatch(arr, m))
