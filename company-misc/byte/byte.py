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

""" 字节 电商NLP面试 @230202

Easonsi @2023 """
class Solution:
    """ 给定两个数组 x,y, 判断是否存在 i<j 满足 x[i]*log(y[j]) - y[j]*log(x[i]) > 0
思路1: 预处理+DP
    等式转化为 log(xi)/xi < log(yj)/yj. 因此可以对两数组预处理. 等价于找到 i<j 满足 x[i]<y[j]
    为了找到下标对, 可以反向遍历数组, 维护 y[i+1:] 的最大值
    复杂度: O(n+m)
"""
    def find(self, x,y):
        # 对数组进行预处理
        def f(x, default):
            # 计算 f(x) = log(x) / x. 需要注意 log操作的合法性
            if x>0: return log(x) / x
            return default
        x = [f(i,inf) for i in x]
        y = [f(i,-inf) for i in y]
        # print(x,y)
        #反向遍历数组 DP
        n,m = len(x), len(y)
        max_y = -inf
        if m>n: max_y = max(y[n:])
        for i in range(min(n,m)-1,-1,-1):
            if x[i] < max_y: return True
            max_y = max(max_y, y[i])
        return False
    
    
    
    
    
sol = Solution()
result = [
    # sol.find([-5,2,3,3,3], [-1,3,1,5]),
]
for r in result:
    print(r)
