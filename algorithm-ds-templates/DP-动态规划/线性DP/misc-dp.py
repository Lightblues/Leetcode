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
Easonsi @2023 """
from functools import cache
class Solution:
    """ 0221. 最大正方形 #medium 0/1矩阵中最大的全1正方形面积. 限制: n 300
思路1: #DP
    f[i,j] 表示以 (i,j) 为右下角的最大正方形边长
    递推: min(f(i-1,j),f(i,j-1),f(i-1,j-1))+1
     """
    def maximalSquare(self, matrix: List[List[str]]) -> int:
        m,n = len(matrix),len(matrix[0])
        @cache
        def f(i,j):
            if i<0 or j<0 or matrix[i][j]=='0': return 0
            return min(f(i-1,j),f(i,j-1),f(i-1,j-1))+1
        return max(f(i,j) for i in range(m) for j in range(n))**2
    
    
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
