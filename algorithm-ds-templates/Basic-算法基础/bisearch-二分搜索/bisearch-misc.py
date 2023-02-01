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
https://leetcode.cn/contest/weekly-contest-bisearch-misc
https://leetcode-cn.com/contest/biweekly-contest-81
Easonsi @2023 """
class Solution:
    """ 0074. 搜索二维矩阵 #medium 矩阵按照一行一行具有递增性质, 在其中进行搜索
思路1: 就是在 MN 的有序数组上进行 #二分
"""
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        def listIndex2matrixIndes(i):
            quotient, remainder = divmod(i, n)
            return quotient, remainder
        left, right = 0, m*n-1
        while left <= right:
            mid = (left+right)//2
            i,j = listIndex2matrixIndes(mid)
            if matrix[i][j] == target:
                return True
            elif matrix[i][j] < target:
                left = mid+1
            else:
                right = mid-1
        return False
    
    
    
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
