""" 
24秋招第二场
https://www.nowcoder.com/exam/test/79025466/detail?pid=52007812
T6. 小美的数组构造
给定一个数组a, 要求构造数组b, 使得sum(b)==sum(a) 并且对应位置的元素各不相等
限制: sum 500, n 100 对于结果取模
思路1: #DP
    定义 f[i,s] 表示前i个元素符合条件, 并且和为s的方案数量. 
    转移: f[i,s] = sum{ f[i-1,s-k] | k=1...s-i 并且!=a[i] }
"""
mod = 10**9+7
