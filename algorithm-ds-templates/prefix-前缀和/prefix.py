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

""" 
下面的7道题整理自灵神的列表, 都是用前缀和来处理枚举连续子数组的题目, 利用了哈希表来进行计数, 将复杂度从 O(n^2) 降到 O(n)
from [灵神](https://leetcode.cn/problems/number-of-wonderful-substrings/solution/qian-zhui-he-chang-jian-ji-qiao-by-endle-t57t/)

0560. 和为 K 的子数组 #medium
    给定一个数组, 问有多少个(连续)子数组的和为 k
0930. 和相同的二元子数组 #medium
    相较于 0560题, 数组中的元素均为 0/1
    因此有了 #滑动窗口 这一空间优化到 O(1) 的算法. 注意官答中 #双指针 的解法比较清晰
0974. 和可被 K 整除的子数组 #medium
1590. 使数组和能被 P 整除 #medium 但个人感觉 #hard #题型 有意思
    给定一个数字p, 对于一个数组, 可以移除一个连续子数组, 是的剩余的部分的和能否被p整除. 问最少移除的子数组长度.
    限制: 数组长度 1e5, p <= 1e9
    思路1: 等价问题为, 找到数组中子数组, 使其之和与整个数组对p同模.
    类似0974题, 不过现在要求最短数组, 因此用一个 #哈希表 记录最近的同模前缀和的位置即可

1371. 每个元音包含偶数次的最长子字符串 #medium
    相较于1915题, 变为: 给定一个字符串, 要求找到子串中, 元音字母aeiuo均为偶数次的最长子字符串 (的长度).
    思路: #状压 表示当前前缀, 然后 #哈希表 记录上一个出现的位置
    相较于前面的几道题都是计数, 这里用一个哈希表记录每一个pattern最开始出现的位置即可
1915. 最美子字符串的数目 #medium #题型 #前缀和
    定义「美子串」为: 字符串中, 字符的数量为奇数的字符最多出现一个. 现给定一个字符串, 求其所有的连续子串中「美子串」的数量.
    约束: 字符串长度 1e5, 字符只包含 a-j 10种.
    思路: 记录前缀和计数器; 观察满足条件 (i,j) 对其两个前缀和之间的关系?
1542. 找出最长的超赞子字符串 #hard
    定义「超赞」子串为, 重排列可以得到回文串. 现给定一个字符串, 要求得到连续子串中最长「超赞」子串的长度.
    限制: 所有字符均为数字, 也即0-9 十个
    思路1: 用一个 #哈希表 记录pattern出现的首次位置; 并枚举所有仅有一个字符出现奇数次的情况
    结合 1371和1915 中的思路


== 
1906. 查询差绝对值的最小值 #medium #题型
    定义查询为: 给定 [start, end], 返回这一子数组中元素的「差绝对值的最小值」 注意如果范围内所有元素都相同, 则返回-1 (也即不能为0). 现给定一个数组和一组查询, 返回所有查询的结果.
    限制: 数组长度 1e5, 查询数量 2e4; 数组中每个元素范围 [1,100]
    思路1: 用 #前缀和 记录当前前缀所包含的数字 cnt

 """
class Solution:
    """ 0560. 和为 K 的子数组 #medium
给定一个数组, 问有多少个(连续)子数组的和为 k
限制: 数组长度 2e4; 元素范围 [-1000, 1000]
思路0: #前缀和
    用一个 #哈希表 记录前缀和出现的个数, 遍历过程中, 累计 cnt[s-k] 即可.
"""
    def subarraySum(self, nums: List[int], k: int) -> int:
        cnt = Counter()
        cnt[0] = 1
        s = 0; ans = 0
        for num in nums:
            s += num
            ans += cnt[s-k]
            cnt[s] += 1
        return ans
    def subarraySum(self, nums: List[int], k: int) -> int:
        """ 官方题解给了 O(n^2) 的解法, 发现至少在Python中不能过 """
        acc = list(accumulate(nums, initial=0))
        n = len(nums)
        ans = 0
        for i in range(n):
            for j in range(i, n):
                if acc[j+1] - acc[i] == k:
                    ans += 1
        return ans
    
    """ 0930. 和相同的二元子数组 #medium
相较于 0560题, 数组中的元素均为 0/1
由于多了这一约束, 有空间复杂度为 O(1), 时间也是 O(n) 的解法: #滑动窗口
思路2: #滑动窗口
    注意边界情况: `nums = [0,0,0,0,0], goal = 0`
    思路: 对于每一个右指针 right, 维护满足条件的左指针区间 [left1, left2) 使得这一范围内的是合法的.
        也即要求: left1 是满足 `sum(nums[left1...right]) == goal` 的最左边的元素. left2 是满足 `sum(nums[left1...right]) < goal` 的最左边的元素.
    枚举所有的右边界, 更新两个指针后累计 left2-left1 即可
    [官答](https://leetcode.cn/problems/binary-subarrays-with-sum/solution/he-xiang-tong-de-er-yuan-zi-shu-zu-by-le-5caf/)
"""
    def numSubarraysWithSum(self, nums: List[int], goal: int) -> int:
        # if sum(nums) < goal: return 0
        ans = 0
        s1, s2 = 0, 0
        left1, left2 = 0, 0
        for right,num in enumerate(nums):
            s1 += num
            # nums[left1...right] 之和为 goal
            while s1 > goal:
                s1 -= nums[left1]
                left1 += 1
            s2 += num
            # left2 是第一个 nums[left2...right] 之和 <goal 的位置
            # left2 <= right 是为了避免 goal=0 可能发生越界
            while s2 >= goal and left2 <= right:
                s2 -= nums[left2]
                left2 += 1
            ans += left2-left1
        return ans
    
    
    """ 0974. 和可被 K 整除的子数组 #medium
相较于 0560题, 和为k换成了和为k的倍数.
下面的解法完全是 Copilot 补全的 Orz, 一字未改.
"""
    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        cnt = [0]*k
        cnt[0] = 1
        s = 0; ans = 0
        for num in nums:
            s += num
            ans += cnt[s%k]
            cnt[s%k] += 1
        return ans
    
    """ 1590. 使数组和能被 P 整除 #medium
给定一个数字p, 对于一个数组, 可以移除一个连续子数组, 是的剩余的部分的和能否被p整除. 问最少移除的子数组长度.
限制: 数组长度 1e5, p <= 1e9
思路1: 等价问题为, 找到数组中子数组, 使其之和与整个数组对p同模.
    类似0974题, 不过现在要求最短数组, 因此用一个 #哈希表 记录最近的同模前缀和的位置即可
"""
    def minSubarray(self, nums: List[int], p: int) -> int:
        target = sum(nums) % p
        # 边界1: 不需要移除 (注意如果在下面 `(s-target) % p in sum2idx` 检测之前 `sum2idx[s] = idx` 就不需要此特判)
        if target == 0: return 0
        sum2idx = {0: -1}
        # sum2idx = {}
        s = 0; ans = len(nums)
        for idx, num in enumerate(nums):
            s = (s+num) % p
            # sum2idx[s] = idx
            if (s-target) % p in sum2idx:
                ans = min(ans, idx-sum2idx[(s-target)%p])
            sum2idx[s] = idx
        # 边界2: 剩余不能为空 (返回-1)
        return ans if ans != len(nums) else -1
    
    """ 1915. 最美子字符串的数目 #medium #题型 #前缀和
定义「美子串」为: 字符串中, 字符的数量为奇数的字符最多出现一个. 现给定一个字符串, 求其所有的连续子串中「美子串」的数量.
约束: 字符串长度 1e5, 字符只包含 a-j 10种.
思路1: 枚举 #前缀和 #状压
    利用字符种类最多只有10个的限制, 可以用一个长度为10的二进制数表示这些数字的奇偶状态. 例如 aba 所对应 `...010` 表示b出现了奇数次
    对于当前枚举的位置j, 假设其前缀和为s[j], 若对于位置对 (i,j) 而言,
        若 `s[i]==s[j]`, 则说明 `word[i+1:j+1]` 这一子串中所有的字符都出现了偶数次.
        若 `s[i]^s[j]` 的结果仅包含一个非零位, 说明 `word[i+1:j+1]` 范围内有仅有一个字符出现了奇数次.
    因此, 我们在遍历字符串计算前缀和的过程中, 用一个计数器记录之前前缀和出现次数, 按照上面的规则累计即可.
    注意: 空字符串的前缀和定义为0
    复杂度: O(n)
    from [灵神](https://leetcode.cn/problems/number-of-wonderful-substrings/solution/qian-zhui-he-chang-jian-ji-qiao-by-endle-t57t/)
总结: 对于 (i,j) 对匹配计数的问题, 这里需要遍历的过程中直接进行累计计算, 而不是遍历完得到完整的cnt再处理. 这是两种不同的思路, 需要加强前一种方式的思维.
    
"""
    def wonderfulSubstrings(self, word: str) -> int:
        cnt = [0] * 2**10
        cnt[0] = 1  # 初始前缀和为 0，需将其计入出现次数
        ans = 0
        s = 0
        for ch in word:
            s ^= 1 << (ord(ch)-ord('a'))    # 更新前缀和
            ans += cnt[s]       # (i,j) 区间内的字符个数均为偶数
            for i in range(10): # 允许出现一个字符个数为奇数
                ans += cnt[s^(1<<i)]
            cnt[s] += 1     # 更新前缀和出现次数
        return ans
    
    """ 1371. 每个元音包含偶数次的最长子字符串 #medium
相较于1915题, 变为: 给定一个字符串, 要求找到子串中, 元音字母aeiuo均为偶数次的最长子字符串 (的长度).
思路: #状压 表示当前前缀, 然后 #哈希表 记录上一个出现的位置
    相较于前面的几道题都是计数, 这里用一个哈希表记录每一个pattern最开始出现的位置即可
"""
    def findTheLongestSubstring(self, ss: str) -> int:
        vowels = 'aeiou'
        def ch2int(ch):
            if ch not in vowels: return -1
            return vowels.index(ch)
        # fstIndx = [-1] * 2**5
        fstIdx = {}
        fstIdx[0] = -1
        s = 0; ans = 0
        for idx,ch in enumerate(ss):
            i = ch2int(ch)
            if i!=-1:
                s ^= 1<<i
            if s in fstIdx:
                ans = max(ans, idx-fstIdx[s])
            else:
                fstIdx[s] = idx
        return ans
    
    """ 1542. 找出最长的超赞子字符串 #hard
定义「超赞」子串为, 重排列可以得到回文串. 现给定一个字符串, 要求得到连续子串中最长「超赞」子串的长度.
限制: 所有字符均为数字, 也即0-9 十个
思路1: 用一个 #哈希表 记录pattern出现的首次位置; 并枚举所有仅有一个字符出现奇数次的情况
    类似1371题, 记录某一pattern出现的最早位置
    区别在于, 允许一个字符为奇数, 因此还在结合1915题中的思想, 对于编辑距离为1的pattern进行枚举
"""
    def longestAwesome(self, s: str) -> int:
        fstIdx = {}
        fstIdx[0] = -1
        mask = 0; ans = 0
        for idx, ch in enumerate(s):
            mask ^= 1<<(ord(ch)-ord('0'))
            if mask in fstIdx:
                ans = max(ans, idx-fstIdx[mask])
            else:
                fstIdx[mask] = idx
            # 枚举出现 odd 次数的数字
            for i in range(10):
                if mask^(1<<i) in fstIdx:
                    ans = max(ans, idx-fstIdx[mask^(1<<i)])
        return ans
    
    """ 1906. 查询差绝对值的最小值 #medium #题型
定义查询为: 给定 [start, end], 返回这一子数组中元素的「差绝对值的最小值」 注意如果范围内所有元素都相同, 则返回-1 (也即不能为0). 现给定一个数组和一组查询, 返回所有查询的结果.
限制: 数组长度 1e5, 查询数量 2e4; 数组中每个元素范围 [1,100]
思路1: #前缀和 
    注意, 这里元素的范围较小 (100) , 考虑用前缀和记录每一个前缀中所包含的元素数量
    这样, 对于任意的区间 (i,j) 都可以在O(100)的时间内查询出其中包含的元素数量. 对于每个查询计算即可.
    复杂度: (n+q)100
拓展: [这里](https://codeforces.com/problemset/problem/765/F) 将元素范围拓展到了 1e9, 只能采用离线方案了.
"""
    def minDifference(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n = len(nums)
        # 计算前缀和矩阵 numsMasks
        numsMasks = [None] * (n+1)
        mask = [0] * 101
        numsMasks[0] = mask[:]
        for i, num in enumerate(nums):
            mask[num] += 1
            numsMasks[i+1] = mask[:]
        # 计算每一个查询的结果
        ans = [101] * len(queries)
        def f(start, end):
            """ 计算最小差绝对值 """
            ans = 101; pre = None   # ans = inf
            for i in range(1, 101):
                if numsMasks[end][i] - numsMasks[start][i] > 0:
                    if pre is None:
                        pre = i
                        continue
                    ans = min(ans, i-pre)
                    pre = i
            return ans if ans!=101 else -1
        for i, (s,e) in enumerate(queries):
            ans[i] = f(s, e+1)
        return ans
    
sol = Solution()
result = [
    # sol.subarraySum(nums = [1,1,1], k = 2),
    # sol.numSubarraysWithSum(nums = [1,0,1,0,1], goal = 2),
    # sol.numSubarraysWithSum(nums = [0,0,0,0,0], goal = 0),
    # sol.findTheLongestSubstring(ss = "eleetminicoworoep"),
    # sol.findTheLongestSubstring("leetcodeisgreat"),
    # sol.longestAwesome(s = "3242415"),
    # sol.longestAwesome(s = "213123"),
    # sol.longestAwesome(s = "12345678"),
    sol.minSubarray(nums = [3,1,4,2], p = 6),
    sol.minSubarray(nums = [6,3,5,2], p = 9),
    sol.minSubarray(nums = [1,2,3], p = 7),
    sol.minSubarray(nums = [1000000000,1000000000,1000000000], p = 3),
]
for r in result:
    print(r)
