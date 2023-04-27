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
https://leetcode.cn/tag/stack/problemset/

Easonsi @2023 """
class Solution:
    """ 227. 基本计算器 II #medium #题型
给你一个字符串表达式 s ，请你实现一个基本计算器来计算并返回它的值。
整数除法仅保留整数部分。
[official](https://leetcode.cn/problems/basic-calculator-ii/solution/ji-ben-ji-suan-qi-ii-by-leetcode-solutio-cm28/)
    """
    def calculate(self, s: str) -> int:
        stack = []
        preSign = '+'
        num = 0
        for c in s+'/':
            if c.isdigit():
                num = 10*num+int(c)
            elif c in '+-*/':
                if preSign == '+':
                    stack.append(num)
                elif preSign == '-':
                    stack.append(-num)
                elif preSign == '*':
                    stack.append(stack.pop()*num)
                else:
                    # 注意不能用 stack.pop()//num，因为在 python 中 -3//2 = -2，而按照题目要求应该是 -1
                    stack.append(int(stack.pop()/num))
                num = 0
                preSign = c

        return sum(stack)
    
    
    
    
    

    
sol = Solution()
result = [
    sol.calculate("14-3/2"), 
]
for r in result:
    print(r)
