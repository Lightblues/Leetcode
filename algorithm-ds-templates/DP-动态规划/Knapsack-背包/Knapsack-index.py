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
多维背包
[01 字符构成最多的字符串](https://leetcode-cn.com/problems/ones-and-zeroes/)：多维费用的 0-1 背包最大值，两个背包大小：0和1的数量
[盈利计划](https://leetcode-cn.com/problems/profitable-schemes/)：多维费用的 0-1 背包最大值

分组背包: 
1155. 掷骰子的N种方法 每一组是一个骰子，每个骰子只能拿一个体积为1到6的物品


Easonsi @2023 """
class Solution:
    """  """
    
    
    
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
