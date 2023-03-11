from easonsi.util.leetcode import *
from functools import cache


def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
LIS: Longest increasing subsequence (最长递增子序列) 
最长公共子序列 LCS

Easonsi @2023 """
class Solution:
    """ 1143. 最长公共子序列 #medium #DP #题型 求 最长 公共子序列 的长度 LCS
最简单的写法: 1] 用cache/memo 写一个搜索函数; 2] 处理边界条件; 3] 写出核心的转移方程
     """
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m,n = len(text1),len(text2)
        @cache
        def f(i,j):
            # 处理边界
            if i<0 or j<0: return 0
            # 核心的转移方程
            if text1[i]==text2[j]: return f(i-1,j-1)+1
            return max(f(i-1,j),f(i,j-1))
        return f(m-1,n-1)
    
    
    
    
    

    
sol = Solution()
result = [
    sol.longestCommonSubsequence(text1 = "abcde", text2 = "ace" ),
    sol.longestCommonSubsequence(text1 = "abc", text2 = "abc"),
]
for r in result:
    print(r)
