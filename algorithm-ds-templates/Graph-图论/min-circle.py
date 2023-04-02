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
https://oi-wiki.org/graph/min-circle/
【朝夕的ACM笔记】 [图论-最小环](https://zhuanlan.zhihu.com/p/342293693)

6330. 图中的最短环 #hard
Easonsi @2023 """
class Solution:
    """  """
    
    
    
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
