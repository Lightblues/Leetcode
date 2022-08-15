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
import sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode, linked2list, list2linked

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 数位 DP
灵神的 [题目列表和模版](https://leetcode.cn/problems/count-special-integers/solution/shu-wei-dp-mo-ban-by-endlesscheng-xtgx/). 另外参见 [1397的官答](https://leetcode.cn/problems/find-all-good-strings/solution/zhao-dao-suo-you-hao-zi-fu-chuan-by-leetcode-solut/)
对应 [视频讲解](https://www.bilibili.com/video/BV1rS4y1s721)

== 灵神提供的板子
6151. 统计特殊整数 #hard #模板 之后写 #数位 DP 可以直接copy #star
    给定上限n, 要求从 1...n 的数字中, 没有相同元素的数字. 限制: 2e9
    通用的递归函数形式 `f(idx: int, mask: int, isLimit: bool, isNum: bool)`. idx是当前枚举的位; mask记录了历史的约束条件(状压); isLimit记录前缀是否和最大值相同(限制数字大小); isNum记录当前位之前是否已有数字填充(防止首位出现0). 注意这类通用递归的函数的返回类型也要根据题目来灵活变化.
    注意: 需要配合记忆化搜索, 否则会超时
    关联: 1012
1012. 至少有 1 位重复的数字 #hard 上一题的相反问题.
    修改了灵神上面的板子, 加了一个 isDone 参数判断是否已经有重复.

0233. 数字 1 的个数 #hard
    相同题: 面试题 17.06. 2出现的次数
    给定一个整数 n，计算所有小于等于 n 的非负整数中数字 1 出现的个数。
    相较于 1012题, 1) 由于这里对于数字没有限制, 只需要isLimit来判断最大值即可; 2) 需要对于符号计数, 因此返回值除了合法数字个数, 还要返回子问题中包含的符号个数.
1067. 范围内的数字计数 #hard
    相较于 0233. 数字 1 的个数, 这里要求范围 [low,high] 内的数字中, 数字d出现的次数.
    思路1: 类似「利用前缀和求区间和」, 直接调用 `countDigit(n, high) - countDigit(n, low-1)` 即可

0600. 不含连续1的非负整数 #hard
    给定一个整数n, 要求在0...n中, 其二进制表示不包含连续1的数字的数量.
    思路1: 直接套板子, 每一位分别尝试填入0/1, isLimit判断极值
0902. 最大为 N 的数字组合 #hard
    给定一组字符集 (例如 135), 要求用这些字符构成的 <=n 的数字数量.
    思路1: 灵神的视频里板子的应用题. 递归函数 `dfs(idx: int, isNum: bool, isLimit: bool)`


== others
1397. 找到所有好字符串 #hard #KMP #hardhard
    给定两个长度均为n的字符串 s1<s2, 要求字典序在两者之间的, 不包含 evil 为子字符串 的所有合法字符串数量.
    限制: 字符串长度 500
    提示: #KMP 这里的整体设置和前面的题目, 包括1012题很像. 难点在于, 如何传递当前匹配evil的长度? 答案是借鉴 KMP 算法
    思路1: 基本框架还是 #数位 DP, 需要结合 #前缀函数. 重点应该去看前缀函数的计算和KMP算法中的失败转移过程.


@2022 """
class Solution:
    """ 6151. 统计特殊整数 #hard
给定上限n, 要求从 1...n 的数字中, 没有相同元素的数字. 限制: 2e9
思路2: 通用的 #数位 DP #板子
    写成了规范的递归函数形式 `f(i: int, mask: int, isLimit: bool, isNum: bool)`.
        这里的i是当前位, mask表示约束条件;
        isLimit 表示当前位是否受到约束. 例如本题中, 一般情况下可以取所有非冲突位, 而当前缀和n相同时, 只能取更小值;
        isNum 表示 当前位之前是否已有了非零数字, 否则首位不能填0.
    见 [灵神](https://leetcode.cn/problems/count-special-integers/solution/shu-wei-dp-mo-ban-by-endlesscheng-xtgx/)
关联: 1012. 至少有 1 位重复的数字 #hard 完全一致的题目
"""
    def countSpecialNumbers(self, n: int) -> int:
        # 思路2: 通用的 #数位 DP
        s = str(n)
        @lru_cache(None)
        def f(i: int, mask: int, is_limit: bool, is_num: bool) -> int:
            # isLimit 表示当前是否受到了 n 的约束。若为真，则第 i 位填入的数字至多为 s[i]，否则可以是 9。
            # isNum 表示 i 前面的位数是否填了数字。若为假，则或者要填入的数字至少为 1 (或当前位可以跳过)；若为真，则要填入的数字可以从 0 开始。
            if i == len(s):
                return int(is_num)
            
            res = 0
            # 1) 首位留空, 注意这里递归调用的 is_num=False
            if not is_num:  # 可以跳过当前数位
                res = f(i + 1, mask, False, False)
            # 2) 填数字, is_num 决定了是否为首位, 注意递归调用 is_num=True
            up = int(s[i]) if is_limit else 9   # 注意「isLimit 表示当前是否受到了 n 的约束」, 因此递归的参数是 is_limit and d == up
            for d in range(0 if is_num else 1, up + 1):  # 枚举要填入的数字 d
                if mask >> d & 1 == 0:  # d 不在 mask 中
                    res += f(i + 1, mask | (1 << d), is_limit and d == up, True)
            return res
        return f(0, 0, True, False)
    
    """ 1012. 至少有 1 位重复的数字 #hard 同上题, 答案是 n-countSpecialNumbers(n).
重写了灵神上面的板子, 加了一个 isDone 参数判断是否已经有重复.
"""
    def numDupDigitsAtMostN(self, n: int) -> int:
        # isLimit 表示前缀是否和n相同: 若是则当前最多填到n[idx]; 否则可以填到9
        # isNum 表示前面是否已经填了: 若是则没有首位约束了; 否则当前位不能填0
        # isDone 表示是否已经符合要求
        s = list(map(int, str(n)))
        @lru_cache(None)
        def f(idx: int, mask: int, isNum: bool, isLimit: bool, isDone: bool) -> int:
            # 返回从idx开始填, 前面用掉mask的情况下, 可以填的数字个数
            if idx == len(s):
                return 1 if isDone else 0
            ans = 0
            if not isNum:
                ans = f(idx + 1, mask, False, False, False) # 因为跳过了这一位, 所以 isLimit=False
            up = s[idx] if isLimit else 9
            for d in range(0 if isNum else 1, up + 1):
                if ((mask >> d) & 1) == 1:   # 出现重复
                    ans += f(idx + 1, mask, True, isLimit and d == up, True)
                else:
                    ans += f(idx + 1, mask | (1 << d), True, isLimit and d == up, isDone)
            return ans
        return f(0,0,False,True,False)

    """ 0233. 数字 1 的个数 #hard
给定一个整数 n，计算所有小于等于 n 的非负整数中数字 1 出现的个数。
相同题: 面试题 17.06. 2出现的次数
思路1: 板子. 
    相较于 1012题, 1) 由于这里对于数字没有限制, 只需要isLimit来判断最大值即可; 2) 需要对于符号计数, 因此返回值除了合法数字个数, 还要返回子问题中包含的符号个数.
[官答](https://leetcode.cn/problems/number-of-digit-one/solution/shu-zi-1-de-ge-shu-by-leetcode-solution-zopq/)
"""
    def countDigitOne(self, n: int) -> int:
        s = list(map(int, str(n)))
        @lru_cache(None)
        def f(idx: int, isLimit: bool) -> int:
            # return: <合法数字的数量, 数字1的数量>
            # 这里只需要 idx, isLimit 参数.
            if idx==len(s): return 1, 0     # 由于数字构造没有限制, 因此第一个永远返回 1
            cnt, cnt1 = 0, 0
            up = s[idx] if isLimit else 9
            for i in range(up+1):
                nnum, n1 = f(idx+1, True if isLimit and i==s[idx] else False)
                cnt += nnum
                cnt1 += n1
                if i==1: cnt1 += nnum
            return cnt, cnt1
        return f(0,True)[1]
    
    """ 0902. 最大为 N 的数字组合 #hard
给定一组字符集 (例如 135), 要求用这些字符构成的 <=n 的数字数量.
思路1: 灵神的视频里板子的应用题. 递归函数 `dfs(idx: int, isNum: bool, isLimit: bool)`
"""
    def atMostNGivenDigitSet(self, digits: List[str], n: int) -> int:
        # digits = list(map(int, digits))
        n = str(n)
        @lru_cache(None)
        def dfs(idx: int, isNum: bool, isLimit: bool):
            if idx==len(n): return int(isNum)
            ans = 0
            if not isNum:
                ans = dfs(idx+1, False, False)
            up = n[idx] if isLimit else digits[-1]
            for d in digits:
                if d>up: break
                ans += dfs(idx+1, True, isLimit and d==up)
            return ans
        return dfs(0,False,True)
    
    
    
    """ 0600. 不含连续1的非负整数 #hard
给定一个整数n, 要求在0...n中, 其二进制表示不包含连续1的数字的数量.
思路1: 直接套板子, 每一位分别尝试填入0/1, isLimit判断极值
"""
    def findIntegers(self, n: int) -> int:
        num = list(map(int, bin(n)[2:]))
        @lru_cache(None)
        def dfs(idx:int, isNum: bool, before1: bool, isLimit: bool) -> int:
            # 这里的before1记录上一位是否为1, 可以理解为板子里的 mask
            # 由于不需要判断重复位, 首位0的情况不会产生冲突或重复, 因此这里的 isNum参数可以省略.
            if idx == len(num): return 1 # int(isNum)
            ans = 0
            # fill 0
            ans += dfs(idx+1, isNum, False, isLimit and num[idx]==0)
            if not before1 and not (isLimit and num[idx]==0):
                ans += dfs(idx+1, True, True, isLimit and num[idx]==1)
            return ans
        return dfs(0,False,False,True)
            


    """ 1067. 范围内的数字计数 #hard
相较于 0233. 数字 1 的个数, 这里要求范围 [low,high] 内的数字中, 数字d出现的次数.
限制: 计数对象0-9; 1<=low<=high<=10^9
思路1: 类似「利用前缀和求区间和」, 直接调用 `countDigit(n, high) - countDigit(n, low-1)` 即可

会员题, see https://cloud.tencent.com/developer/article/1787932
"""
    def digitsCount(self, d:int, low:int, high: int) -> int:
        def countDigit(n: int, d: int) -> int:
            n = list(map(int, str(n)))
            def dfs(idx:int, isLimit:bool, isNum:int) -> Tuple[int,int]:
                # return [#合法数字, #数字d]
                if idx == len(n): return int(isNum), 0
                cnt, cntd = 0, 0
                if not isNum:
                    cnt, cntd = dfs(idx+1, False, False)
                up = n[idx] if isLimit else 9
                for i in range(0 if isNum else 1, up+1):
                    c, cd = dfs(idx+1, isLimit and i==n[idx], True)
                    # cnt+= c; cntd+=cd
                    cntd += cd
                    if i==d: cntd += c
                    cnt += c
                return cnt, cntd
            return dfs(0,True,False)[1]
        
        return countDigit(high, d) - countDigit(low-1, d)




    """ 1397. 找到所有好字符串 #hard #KMP #hardhard
给定两个长度均为n的字符串 s1<s2, 要求字典序在两者之间的, 不包含 evil 为子字符串 的所有合法字符串数量.
限制: 字符串长度 500
提示: #KMP 这里的整体设置和前面的题目, 包括1012题很像. 难点在于, 如何传递当前匹配evil的长度? 答案是借鉴 KMP 算法
思路1: 基本框架还是 #数位 DP, 需要结合 #前缀函数. 重点应该去看 **前缀函数的计算和KMP算法中的失败转移过程**.
    先计算evil字符串的 [前缀函数](https://oi-wiki.org/string/kmp/), 方便匹配失败之后的转移.
    核心的递归函数 `dfs(idx:int, pidx:int, isLimit:bool)`, 和上面的题目类似, pidx对应模板中的mask, 记录此时应该匹配的evil前缀位置.
[官答](https://leetcode.cn/problems/find-all-good-strings/solution/zhao-dao-suo-you-hao-zi-fu-chuan-by-leetcode-solut/)
"""
    def findGoodStrings(self, n: int, s1: str, s2: str, evil: str) -> int:
        def prefix_function(s):
            # 计算前缀函数, from https://oi-wiki.org/string/kmp/
            n = len(s)
            pi = [0] * n
            for i in range(1, n):
                j = pi[i - 1]
                while j > 0 and s[i] != s[j]:
                    j = pi[j - 1]
                if s[i] == s[j]:
                    j += 1
                pi[i] = j
            return pi
        prefix = prefix_function(evil)
        mod = 100**9+7
        def f(s):
            # 计算长度为n的小于等于s的字符串中, 不含evil子串的数量
            nchars = 26
            @lru_cache(None)
            def dfs(idx:int, pidx:int, isLimit:bool) -> int:
                # 核心. pidx类似板子中的mask, 记录此时应该匹配的evil前缀位置.
                if idx==n: return 1
                ans = 0
                up = ord(s[idx])-ord('a') if isLimit else nchars-1
                for ii,ch in enumerate(string.ascii_lowercase[:up+1]):
                    ppidx = pidx
                    while ppidx and ch!=evil[ppidx]:
                        ppidx = prefix[ppidx-1]
                    if ch==evil[ppidx]:
                        ppidx += 1
                    if ppidx==len(evil): continue
                    ans += dfs(idx+1, ppidx, isLimit and ii==up)
                    ans %= mod
                return ans
            return dfs(0,0,True)
                    
        return (f(s2) - f(s1) + (evil not in s1)) % mod


sol = Solution()
result = [
    # sol.countDigitOne(13),
    # sol.countDigitOne(1),
    # sol.numDupDigitsAtMostN(20),
    # sol.numDupDigitsAtMostN(100),
    # sol.atMostNGivenDigitSet(digits = ["1","3","5","7"], n = 100),
    # sol.atMostNGivenDigitSet(digits = ["1","4","9"], n = 1000000000),
    # sol.findIntegers(5),
    # sol.findIntegers(2),
    # sol.digitsCount(d = 1, low = 1, high = 13),
    # sol.digitsCount(d = 3, low = 100, high = 250),
    # sol.digitsCount(0, 1, 10),
    sol.findGoodStrings(n = 2, s1 = "aa", s2 = "da", evil = "b"),
    sol.findGoodStrings(n = 8, s1 = "leetcode", s2 = "leetgoes", evil = "leet"),
    sol.findGoodStrings(n = 2, s1 = "ax", s2 = "az", evil = "x"),
]
for r in result:
    print(r)
