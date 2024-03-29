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

""" 

== 变体
1585. 检查字符串是否可以通过排序子字符串得到另一个字符串 #hard #题型 #冒泡排序
    对于一个字符串, 每次可以对于某一子字符串进行排序操作. 问能否经过若干操作变为目标字符串.
    考虑逆向从t到s的变换: 对于当前考察的t的第一个字符x, 假设其在s中的位置为idx, 则要求s中剩余的比x小的字符的首位位置都应该比idx大, 这样才能顺利将s[idx]调换到首位.
@2022 """
class Solution:
    """  """
    
    
    
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
