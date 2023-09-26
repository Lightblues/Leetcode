""" 给定一组数字, 问和构成60的方案数量 
"""
from collections import Counter
n = int(input())
arr = list(map(int, input().split()))
cnt = Counter()
ans = 0
for x in arr:
    ans += int(x==60)
    ans += cnt[60-x]
    for k,v in cnt.copy().items():
        cnt[k+x] += v
    cnt[x] += 1
print(ans)
