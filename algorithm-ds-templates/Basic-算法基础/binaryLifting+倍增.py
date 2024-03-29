from easonsi import utils
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

""" 倍增 法 Binary Lifting
[oi wiki](https://oi-wiki.org/basic/binary-lifting/)
1483. 树节点的第 K 个祖先 #hard
    给定一棵树, 要求快速查询节点的 k级祖先. 限制: k<=n 5e4; 查询 5e4
    思路1: #倍增 法 Binary Lifting

@2022 """
class Solution:
    """  """
    
    
    
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
