""" 
给定 candidates 数组, 计算其中有多少组合可构成target. 可重复使用. 
思路1: DP
    f[i,x] 前i个数字可以构成x的组合数
    f[i,x] = sum{ f[i-1,x-j(arr[i])] for j in  }
"""

from functools import lru_cache


def getCounts(candidates, target):
    @lru_cache(None)
    def f(i,x):
        if x<0: return 0
        # if i==0: return int((x % candidates[0]) == 0)
        if i<0: return 0
        aa = candidates[i]
        ans = int((x % aa) == 0)
        while x>0:
            ans += f(i-1, x)
            x -= aa
        return ans
    return f(len(candidates)-1, target)

print(
    getCounts([2,3,6,7], 7),
    getCounts([2,3,5], 8),
    getCounts([2], 1),
)
