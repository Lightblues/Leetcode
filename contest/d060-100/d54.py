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
https://leetcode.cn/contest/weekly-contest-261
https://leetcode-cn.com/contest/biweekly-contest-54
@2022 """
class Solution:
    """ 1893. 检查是否区域内所有整数都被覆盖 #easy #题型
给定一组闭区间 ranges, 然后再给一个区间 [left, right], 要求判断这一区间的数字是否被ranges中至少一个区间覆盖.
思路1: #排序 之后依次判断
    复杂度: 假设区间数量为 n, 则复杂度 O(nlogn)
思路2: #差分数组
    注意本题中的数字范围有限再 [1,50] 之间; 因此, 如何记录ranges中的区间? 可以对于 [l,r] 之前的数字都计数+1; 然后检查查询区间 [left, right] 是否都大于零即可
    简化复杂度的方式为, 利用 #差分数组 记录这些ranges, 然后累加一边即可得到每一个数字的被覆盖次数. 这样复杂度为 O(n+l) 其中l为维护的数字大小 (这里为 50)
    [官答](https://leetcode.cn/problems/check-if-all-the-integers-in-a-range-are-covered/solution/jian-cha-shi-fou-qu-yu-nei-suo-you-zheng-5hib/)
"""
    def isCovered(self, ranges: List[List[int]], left: int, right: int) -> bool:
        ranges.sort()
        # if ranges[0][0] > left: return False
        # next 记录下一个没有被覆盖的数字; 若有部分区间被覆盖, 则更新为右端点+1
        next = left
        for l,r in ranges:
            # 终止条件1: 假若下一个区间的l无法覆盖next, 则失败
            if l > next: return False
            if r >= next: next = r+1
            # 终止条件2: next > right 说明整个区间都已被覆盖
            if next > right: return True
        return False
    
    """ 1894. 找到需要补充粉笔的学生编号 """
    def chalkReplacer(self, chalk: List[int], k: int) -> int:
        acc = list(accumulate(chalk))
        idx = bisect_right(acc, k%acc[-1])
        return idx
    
    """ 1895. 最大的幻方 #medium #前缀和
要求在一个矩阵中找到「幻方」, 也即行和、列和、两条对角线元素和都相同的正方形.
思路1: 记录四个方向上的 #前缀和 即可.
    需要注意的是, 一般用 (m+1, n+1) 大小的矩阵距离前缀和, 第一行第一列为哨兵. 在这里, 行列和主对角线是可以这么做的, 但是对于副对角线 (右上-左下), 需要设置哨兵为第一行和最后一列, 这样造成idx会有一点区别.
"""
    def largestMagicSquare(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        sum1 = [[0] * (n+1) for _ in range(m+1)]
        sum2 = [[0] * (n+1) for _ in range(m+1)]
        sum3 = [[0] * (n+1) for _ in range(m+1)]
        sum4 = [[0] * (n+1) for _ in range(m+1)]
        for i in range(m):
            for j in range(n):
                sum1[i+1][j+1] = sum1[i+1][j] + grid[i][j]      # 行
                sum2[i+1][j+1] = sum2[i][j+1] + grid[i][j]      # 列
                sum3[i+1][j+1] = sum3[i][j] + grid[i][j]        # 左上-右下
                # 注意, 这一方向的前缀和由于需要从后往前, 因此哨兵放在了右边!!!
                sum4[i+1][j] = sum4[i][j+1] + grid[i][j]    # 右上-左下
        def test(i,j, k):
            # test the rectangle with left-top corner at (i,j) and size k
            i,j = i+1, j+1
            s = sum1[i][j+k-1] - sum1[i][j-1]
            for ii in range(k):
                if sum1[i+ii][j+k-1] - sum1[i+ii][j-1] != s: return False
                if sum2[i+k-1][j+ii] - sum2[i-1][j+ii] != s: return False
            if sum3[i+k-1][j+k-1] - sum3[i-1][j-1] != s: return False
            if sum4[i+k-1][j-1] - sum4[i-1][j+k-1] != s: return False
            return True
        for k in range(min(m,n), 0, -1):
            for i in range(m-k+1):
                for j in range(n-k+1):
                    if test(i,j, k): return k
        
    
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

sol = Solution()
result = [
    # sol.isCovered(ranges = [[1,2],[3,4],[5,6]], left = 2, right = 5),
    # sol.isCovered(ranges = [[1,10],[10,20]], left = 21, right = 21),
    # sol.chalkReplacer(chalk = [5,1,5], k = 22),
    # sol.chalkReplacer(chalk = [3,4,1,2], k = 25),
    # sol.largestMagicSquare(grid = [[7,1,4,5,6],[2,5,1,6,4],[1,5,4,3,2],[1,2,7,3,4]]),
    # sol.largestMagicSquare(grid = [[5,1,3,1],[9,3,3,1],[1,3,3,8]]),
    
    sol.minOperationsToFlip(expression = "(0&0)&(0&0&0)"),
    sol.minOperationsToFlip(expression = "(0|(1|0&1))"),
]
for r in result:
    print(r)
