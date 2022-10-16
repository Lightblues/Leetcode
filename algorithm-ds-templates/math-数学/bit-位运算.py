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
位运算: https://oi-wiki.org/math/bit/
二进制集合操作 https://oi-wiki.org/math/binary-set/
@2022 """
class Solution:
    """  """
    
    
    
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)

def printBit(x: int):
    # 打印二进制
    return f"{x:b}"

def lowbit(x: int):
    # 获取最低位的 1
    return x & -x

def getSubsets(mask: int):
    # 降序遍历 mask 的非空子集. mask 二进制表示集合
    res = []
    s = mask
    while s:
        res.append(s)
        s = (s-1) & mask
    return res

x = 0b1010
print(f"x={x:b}, lowbit={lowbit(x):b}")
print(f"subsets: {getSubsets(x)}")