from easonsi import utils
from easonsi.util.leetcode import *
from functools import cache

""" 
w[i]: 第i个物品的体积
v[i]: 第i个物品的价值
返回: 不超过capacity的前提下, 能够获得的最大价值
"""
def zero_one_knapsack(capacity, w, v):
    n = len(w)
    @cache
    def dfs(i,c):
        if i<0: return 0
        if c<w[i]: return dfs(i-1,c)
        return max(dfs(i-1,c), dfs(i-1,c-w[i])+v[i])
    return dfs(n-1, capacity)