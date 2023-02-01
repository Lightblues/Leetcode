from easonsi.util.leetcode import *

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
重新整理一下 [[分类.md]]
@2022 """
class Solution:
    """ 0072. 编辑距离 #hard 可以进行 插入、删除、替换操作, 问两个字符串的编辑距离. 限制: 两单词长度 500
思路1: #DP 记 dp[i,j]
    若 ij元素不同: min{ dp[i-1, j-1]+1, dp[i, j-1]+1, dp[i-1, j]+1 }
    否则: min{ dp[i, j-1]+1, dp[i-1, j]+1, dp[i-1, j-1] }
"""
    def minDistance(self, word1: str, word2: str) -> int:
        m,n = len(word1),len(word2)
        f = [[0]*(n+1) for _ in range(m+1)]
        for i in range(m): f[i+1][0] = i+1
        for j in range(n): f[0][j+1] = j+1
        # 
        for i,a in enumerate(word1):
            for j,b in enumerate(word2):
                if a!=b: mn = min(f[i][j],f[i][j+1],f[i+1][j])+1
                else: mn = min(f[i][j],f[i][j+1]+1,f[i+1][j]+1)
                f[i+1][j+1] = mn
        return f[-1][-1]
    
    
    
    
    

    
sol = Solution()
result = [
    sol.minDistance(word1 = "horse", word2 = "ros"),
    sol.minDistance("intention", "execution"),
]
for r in result:
    print(r)
