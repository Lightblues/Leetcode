""" 对于一个数组的乘积, 求它所有的因子数量, 对结果取模
思路1: 就是统计不同的质因子数量
 """

from collections import Counter

n = int(input())
arr = list(map(int, input().strip().split()))

def getFactors(x):
    factors = []
    for i in range(2, int(x**0.5)+1):
        while x%i==0:
            factors.append(i)
            x//=i
    if x>1:
        factors.append(x)
    return factors

cnt = Counter()
for x in arr:
    # for factor in getFactors(x):
    #     cnt[factor] += 1
    cnt += Counter(getFactors(x))
MOD = 10**9+7
ans = 1
for v in cnt.values():
    ans = ans*(v+1)%MOD
print(ans)

