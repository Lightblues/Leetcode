import typing
from typing import List, Optional, Tuple
import copy
from copy import deepcopy, copy
import collections
from collections import deque, defaultdict, Counter, OrderedDict, namedtuple
import math
from math import sqrt, ceil, floor, log, log2, log10, exp, sin, cos, tan, asin, acos, atan, atan2, hypot, erf, erfc, inf, nan
import bisect
from bisect import bisect_right, bisect_left
import heapq
from heapq import heappush, heappop, heapify, heappushpop
import functools
from functools import lru_cache, reduce, partial # cache
# cache = partial(lru_cache, maxsize=None)
# cache for Python 3.9, equivalent to @lru_cache(maxsize=None)
import itertools
from itertools import product, permutations, combinations, combinations_with_replacement, accumulate
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import operator
from operator import add, sub, xor, mul, truediv, floordiv, mod, neg, pos # 注意 pow 与默认环境下的 pow(x,y, MOD) 签名冲突
import sys, os
# sys.setrecursionlimit(10000)
import re

# https://github.com/grantjenks/python-sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode, linked2list, list2linked

""" 
0224. 基本计算器 #hard #题型
    要求实现一个解析 +/- 的计算器. 输入字符串形如 ` 2-1 + 22 `, `(1+(4+5+2)-3)+(6+8)`, 也即需要处理空格和括号的情况, 不存在单元的 +/- 符号.
    思路2: 用两个栈分别记录数字和符号(与括号); 按照运算符的优先级出栈
0227. 基本计算器 II / 面试题 16.26. 计算器 #medium
    相较于 0224, 多了乘除算子, 但不需要考虑括号.
    其实也是用栈记录中间结果. 不过这里只有两种优先级, 可以不用栈.
    
1896. 反转表达式值的最少操作次数 #hard #双栈 #语法分析
    给定一个形如 `"1&(0|1)"` 的布尔表达式, 问最少通过多少操作使其的值发生改变, 例如将这个例子的值变为0, 可以将|操作变为&, 或者将其中一个1变为0.
    允许的操作是: 翻转 0/1, 或者翻转&/|
    思路1: 使用 #双栈 记录 操作符和运算元. 运算元记录将节点变为 0/1 所需的最小操作数. 利用 &| 节点的性质得到递推公式.

 """
class Solution:

    
    
    """ 0224. 基本计算器 #hard #题型
要求实现一个解析 +/- 的计算器. 输入字符串形如 ` 2-1 + 22 `, `(1+(4+5+2)-3)+(6+8)`, 也即需要处理空格和括号的情况, 不存在单元的 +/- 符号.
思路1: 将括号表达式展开, 用栈记录符号状态
    [官答](https://leetcode.cn/problems/basic-calculator/solution/ji-ben-ji-suan-qi-by-leetcode-solution-jvir/)
    由于括号表达式只有加减法, 因此考虑将其展开, 只需要计算每一个元素前的符号即可.
    如何处理括号? 可以用 #栈 来记录括号前的符号; 这样, 对于括号内的每一个数字的符号, 只需要 `opStack[-1] * op` 即可, 这里的op是当前 +/- 符号
    技巧: 除了括号以及加减符号固定为1 之外, 数字的长度不确定, 因此相较于用 for训练解析表达式, 用while循环更加方便, 只需要在处理数字的时候内层进行遍历来搜索完整的数字即可.
思路2: 用两个栈分别记录数字和符号(与括号)
    用两个栈分别保存历史的运算符和运算单元. 顺序遍历, 1) 出现运算符, 则将栈内比该运算符更高或相同级别的运算符使用掉; 2) 将做括号也加入运算符栈, 这样出现右括号的时候, 将第一个匹配到的左括号之前的运算符使用掉.
    see [here](https://leetcode.cn/problems/basic-calculator/solution/shuang-zhan-jie-jue-tong-yong-biao-da-sh-olym/)
"""
    def calculate(self, s: str) -> int:
        opStack = [1]
        op = 1
        ans = 0
        idx = 0
        # 采用while循环而不是for, 这样处理数字的时候更方便
        while idx < len(s):
            if s[idx] == ' ': idx += 1
            elif s[idx] == '(':
                opStack.append(op)  # add current op to stack
                idx += 1
            elif s[idx] == ')':
                op = opStack.pop()  # pop the last op, 并且将当前的符号设置为该括号之前的状态
                idx += 1
            elif s[idx] == '+':
                op = opStack[-1]
                idx += 1
            elif s[idx] == '-':
                op = -opStack[-1]
                idx += 1
        else:
            # 处理数字
                num = 0
                while idx < len(s) and s[idx].isdigit():
                    num = num * 10 + int(s[idx])
                    idx += 1
                ans += num * op
        return ans

    def calculate(self, s: str) -> int:
        # 运算符号优先级
        hashmap = {
            '-': 1,
            '+': 1,
            '*': 2,
            '/': 2,
            '%': 2,
            '^': 3,
        }

        # 存放所有数字
        nums = deque([0])  # 为了防止第一个数为负数，先往nums加个0
        # 存放所有的操作
        ops = deque([])


        def calc(nums, ops):
            if not nums or len(nums) < 2 or not ops:
                return
            b, a = nums.pop(), nums.pop()
            op = ops.pop()
            ans = 0
            if op == '+':
                ans = a + b
            elif op == '-':
                ans = a - b
            elif op == '*':
                ans = a * b
            elif op == '/':
                ans = a // b
            elif op == '^':
                ans = int(pow(a, b))
            elif op == '%':
                ans = a % b
            nums.append(ans)

        n = len(s)
        i = 0
        while i < n:
            c = s[i]
            if c == ' ':
                i += 1
                continue
            # 1. 处理括号
            if c == '(':
                ops.append(c)
            elif c == ')':
                while ops:
                    if ops[-1] != '(':
                        calc(nums, ops)
                    else:
                        ops.pop()
                        break
            else:
                # 2. 处理数字, 入栈 nums
                if c.isdigit():
                    u = 0
                    while i < n and s[i].isdigit():
                        u = u * 10 + int(s[i])
                    nums.append(u)
                    i = i - 1   # 在最后统一移动 i += 1
                else:
                    # 3. 处理运算符 和括号
                    # 考虑处理首位的 +/- 符号
                    # if i > 0 and s[i - 1] in '(+-':
                    #     nums.append(0)
                    while ops and ops[-1] != '(':
                        # 当遇到一个运算符的时候, 将栈内此前的更高等级的运算符用掉
                        prev = ops[-1]
                        if hashmap[prev] >= hashmap[c]:
                            calc(nums, ops)
                        else:
                            break
                    ops.append(c)
            i += 1

        while ops and ops[-1] != '(':
            calc(nums, ops)
        return nums[-1]

    """ 0227. 基本计算器 II / 面试题 16.26. 计算器 #medium
相较于 0224, 多了乘除算子, 但不需要考虑括号.
思路0: 用一个curr数字来记录乘除的结果, 只有当出现加减的时候才累加到ans中.
    由于没有括号, 这里没有采用栈, 直接遍历.
    如何处理乘除法的优先级? 用curr记录当前数字/乘除结果, 只有遇到加减的时候才累加到ans中. (这样为了处理最后一个数字, 可以在最后加一个哨兵符号 `+`)
思路1: 用 #栈 来保存中间计算结果
    上面很倔强没有用什么DS, 造成了变量上的复杂: 因为实际上需要记录二元运算符的两个运算元, 还有因为优先级而需要记录的符号.
    这里用栈记录的优势在哪里呢? 我们可以用栈来记录所有的累加元素; 这样, 遇到乘法的时候, 栈顶就是天然的第一个计算元.
    在下面的代码中, 除了栈结构之外, 仅需要记录当前数字num和之前的运算符preOp: 1) 遇到加减法, 直接将第二个运算元num入栈; 2) 遇到乘除法, 对栈顶元素和num进行乘除运算, 并将结果入栈.
    见 [官答](https://leetcode.cn/problems/basic-calculator-ii/solution/ji-ben-ji-suan-qi-ii-by-leetcode-solutio-cm28/)
note: 注意Python中整除运算是向下取整的, 例如 `-5//3 == -2`. 为了实现题目中「优先乘除」的要求, 除了加括号保障运算元都是正数之外, 下面用了 `int` 实现向零取整.
"""
    def calculateB(self, s: str) -> int:
        # 思路0
        ans = 0
        curr = None # 当前数字 (包括乘除操作之后的结果)
        idx = 0
        flag = 1    # 记录正负号
        mul = None  # 记录乘除法的符号
        s += '+'
        while idx < len(s):
            if s[idx] == ' ':
                idx += 1
                continue
            if s[idx] in '+-':
                ans += flag * curr
                flag = 1 if s[idx] == '+' else -1
                mul = None
                idx += 1
            elif s[idx] in '*/':
                mul = s[idx]
                idx += 1
            else:
                num = 0
                while idx < len(s) and s[idx].isdigit():
                    num = num * 10 + int(s[idx])
                    idx += 1
                # curr 记录当前的数字情况, 方便进行加减法以及乘除法
                if mul == "*":
                    curr *= num
                elif mul == '/':
                    curr //= num
                else:
                    curr = num
        return ans

    def calculateB(self, s: str) -> int:
        # 思路1: 用栈来保存
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
                    # 注意, Python中整除运算是向下取整的!! 下面用int来实现向零取整.
                    # 例如: -5//3 == -2, int(-5/3) == -1
                    stack.append(int(stack.pop()/num))
                num = 0
                preSign = c

        return sum(stack)



    """ 1896. 反转表达式值的最少操作次数 #hard #双栈 #语法分析
- 关联: 0224. 基本计算器
给定一个形如 `"1&(0|1)"` 的布尔表达式, 问最少通过多少操作使其的值发生改变, 例如将这个例子的值变为0, 可以将|操作变为&, 或者将其中一个1变为0.
允许的操作是: 翻转 0/1, 或者翻转&/|
限制: 表达式长度 1e5
思路1: 使用 #双栈 记录 操作符和运算元. 运算元记录将节点变为 0/1 所需的最小操作数. 利用 &| 节点的性质得到递推公式.
    参考 0224, 为了处理操作和括号语句, 采用双栈来分别存储数字和运算符.
        不同之处在于, 这里不是求表达式的值, 而是问最少操作次数. 为此, 将运算元记录变为 `(x,y)` 表示将该节点变为 0/1 分别所需的最小操作数.
        如何确保 **相同级别的操作符顺序执行**? 这里的策略是遇到布尔值就尝试用掉前面的操作符, 直到遇上左括号.
    显然, 遇到叶子节点, 即布尔值的时候, 记录分别为 (1,0) 和 (0,1)
    关键在于, 遇到一个操作符的时候如何更新?
        例如, 当前为 &节点, 假设两子节点返回的分别为 (x1,y1) (x2,y2)
        在不改变节点为| 的情况下, 要求其值为 0/1, 所需的最少操作数分别为 `min{x1+x2, x1+y2, x2+y1}` (实际上就是 `min{x1, x2}`, 这里应该是为了和or节点保持一致), `x2+y2`, 记为 `x_and, y_and`
        然而, 另一种将表达式值变为 1 的方式是将操作符变为 or, 然后只需要 `y_or` 个操作即可.
        综上, 节点记录的更新公式为 `(min(x_and, x_or + 1), min(y_and, y_or + 1))`
    [官答](https://leetcode.cn/problems/minimum-cost-to-change-the-final-value-of-expression/solution/fan-zhuan-biao-da-shi-zhi-de-zui-shao-ca-s9ln/)
思路2: 
    符合自己一开始的想法: 如果已有了输入字符串对应语法树, 求解是比较简单的 (不一定需要上面的策略). 但问题还是如何构建语法树?
    下面还是用 #双栈 分别存储数字和运算符, 然后定义节点构建二叉树结构.
    还是那个问题, 如何保证 **相同级别的操作符顺序执行**? 可以给操作符定义优先级 (例如 `dict(zip('(&|', (0, 1, 1)))`), 当遇到某一操作符的时候, 将更高或相同优先级的运算符全部用掉. 这一思路比上面的更为通用.
    [here](https://leetcode.cn/problems/minimum-cost-to-change-the-final-value-of-expression/solution/zhong-zhui-biao-da-shi-gou-zao-er-cha-bi-gman/)
"""
    def minOperationsToFlip(self, expression: str) -> int:
        """ https://leetcode.cn/problems/minimum-cost-to-change-the-final-value-of-expression/solution/fan-zhuan-biao-da-shi-zhi-de-zui-shao-ca-s9ln/
        用两个栈来保存运算符, 以及中间结果. 注意, stack_num 中的元素 (x,y) 分别为将该子树的表达式值变为 0/1 所需的最小操作数 """
        # 数字栈
        stack_num = list()
        # 符号栈
        stack_op = list()

        def op_and(x1: int, y1: int, x2: int, y2: int):
            # 不改变 & 节点符号, 使得该节点值为 0/1 的最少操作数
            # 例如, `y1 + y2` 表示通过令左右子树的值都为 1, 来使得结果为 1
            return min(x1 + x2, x1 + y2, y1 + x2), y1 + y2
        def op_or(x1: int, y1: int, x2: int, y2: int):
            return x1 + x2, min(x1 + y2, y1 + x2, y1 + y2)
        
        # 尝试将数字栈顶的两个二元组和符号栈顶的运算符进行运算
        def calc():
            if len(stack_num) >= 2 and stack_op[-1] in ["|", "&"]:
                x1, y1 = stack_num.pop()
                x2, y2 = stack_num.pop()
                # 不改变节点符号 (& |) 的情况下的最小操作数
                x_and, y_and = op_and(x1, y1, x2, y2)
                x_or, y_or = op_or(x1, y1, x2, y2)
                # 注意还需要考虑改变节点符号. 例如下面求将一个 & 节点变为0的操作数为 `min(x_and, x_or + 1)`, 其中 `x_and` 是通过修改子节点使得左右孩子均为1, 而 `x_or + 1` 表示将节点变为 | 节点, 然后让子节点符合需求.
                if (op := stack_op.pop()) == "&":
                    stack_num.append((min(x_and, x_or + 1), min(y_and, y_or + 1)))
                else:
                    stack_num.append((min(x_or, x_and + 1), min(y_or, y_and + 1)))

        for ch in expression:
            if ch in ["(", "|", "&"]:
                stack_op.append(ch)
            # 为了保证相同级别的运算符顺序执行, 会将符号栈中的非左括号的运算符全部运算掉
            elif ch == "0":
                stack_num.append((0, 1))
                calc()
            elif ch == "1":
                stack_num.append((1, 0))
                calc()
            else:
                assert ch == ")"
                # 此时符号栈栈顶一定是左括号
                stack_op.pop()
                calc()
        # 注意我们没有求原本表达式的值; 但由于「动态规划中的状态转移一定是最优的」, 因此我们最终得到的 (x,y) 中一定有一个值为0, 对应着原本的表达式值.
        return max(stack_num[0])

    def minOperationsToFlip(self, expression: str) -> int:
        """ https://leetcode.cn/problems/minimum-cost-to-change-the-final-value-of-expression/solution/zhong-zhui-biao-da-shi-gou-zao-er-cha-bi-gman/
        也只利用双栈来解析表达式, 只是定义了节点和dfs函数, 理解上更为清晰? """
        class MyNode:
            def __init__(self, val='0', left: Optional['MyNode'] = None, right: Optional['MyNode'] = None):
                self.val = val
                self.left = left
                self.right = right

        def dfs(root: Optional['MyNode']) -> Tuple[int, int]:
            """返回(变为0的最小操作次数,变为1的最小操作次数)"""
            if not root:
                return int(1e20), int(1e20)
            if root.val.isdigit():
                return int(root.val == '1'), int(root.val == '0')

            left0, left1 = dfs(root.left)
            right0, right1 = dfs(root.right)
            res0, res1 = int(1e20), int(1e20)

            if root.val == '&':
                res0 = min(res0, left0 + right0, left0 + right1, left1 + right0)
                res1 = min(res1, left1 + right1, left0 + right1 + 1, left1 + right0 + 1)
            else:
                res0 = min(res0, left0 + right0, left0 + right1 + 1, left1 + right0 + 1)
                res1 = min(res1, left1 + right1, left0 + right1, left1 + right0)

            return res0, res1


        weight = dict(zip('(&|', (0, 1, 1)))    # 定义不同符号的优先级
        numStack, optStack = [], []
        expression += ')'       # 加一个哨兵
        for char in expression:
            if char == '(':
                optStack.append(char)
            elif char.isdigit():
                numStack.append(MyNode(char))
            elif char in '&|':
                # 遇到运算符, 将更高或相同优先级的运算符全部用掉
                while optStack and weight[optStack[-1]] >= weight[char]:
                    node2, node1 = numStack.pop(), numStack.pop()
                    numStack.append(MyNode(optStack.pop(), node1, node2))
                optStack.append(char)
            elif char == ')':
                # 遇到左括号
                while optStack and optStack[-1] != '(':
                    ndoe2, node1 = numStack.pop(), numStack.pop()
                    numStack.append(MyNode(optStack.pop(), node1, ndoe2))
                if optStack:
                    optStack.pop()

        root = numStack[0]
        return max(dfs(root))

    
    
    
    
    
    
    def testClass(self, inputs):
        # 用于测试 LeetCode 的类输入
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res
    
sol = Solution()
result = [
    # sol.calculate(s = "1 + 1"),
    # sol.calculate(s = "(1+(4+5+2)-3)+(6+8)"),
    
    # sol.calculateB("3+2*2"),
    # sol.calculateB(" 3/2 "),
    # sol.calculateB(" 3+5 / 2 "),
]
for r in result:
    print(r)
