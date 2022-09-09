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
@2022 """
class Solution:
    """ 0719. 找出第 K 小的数对距离 #hard #题型 #二分
给定一个数组, 每个数对构成「绝对差值」. 问第k小的差值. 限制: 长度 n 1e4. 数字大小 C 1e6.  
思路0: #二分. 一个比较蠢的实现
    考虑问题「对于给定的d问差值小于d的数对有多少」, 可以通过排序+bisct解决. 每次检查的复杂度为 `O(n log(n))`.
    搜索空间为 [0,C]. 因此可以用二分来查找, 总体复杂度 `O(log(C) * n log(n))`.
    注意: 本题二分的特殊性在于, 搜索的值可能无法取到! 可以通过检查函数返回一个flag来标记数组中是否存在该差值.
"""
    def smallestDistancePair(self, nums: List[int], k: int) -> int:
        # 思路0: #二分. 一个比较蠢的实现
        nums.sort(); n = len(nums)
        def f(d):
            # 统计nums中差值 <d 的组数
            # 返回: (cnt, flag) 后者标记是否存在该差值
            cnt = 0; flag = False
            for i,a in enumerate(nums):
                lmt = bisect_left(nums, a+d, i)
                cnt += lmt - i - 1
                if lmt<n and nums[lmt]==a+d: flag=True
            return cnt,flag
        # 二分
        l,r = 0,max(nums) - min(nums)
        ans = 0
        while l<=r:
            m = (l+r)>>1
            cnt,flag = f(m)
            if cnt<k:
                l = m+1
                # 只有存在时才更新
                if flag: ans = m
            else: r = m-1
        return ans

    """ 0407. 接雨水 II #hard #题型
相较于 「0042. 接雨水」 变成了二维形式. 限制: 矩阵 m,n 200
思路1: 向内传播「约束高度」, 采用 #最小堆.
    每个位置的水位受什么决定? 四周三个柱子的(水位)高度的最小值. 
        因此直觉是: **根据已经确定的较小值来更新周围位置**. —— 「约束传播」
    本题中, 矩形四边上肯定无法蓄水, 将约束条件向内传递即可.
        如何确定更新的顺序? 向内传播「约束高度」, 每次取约束高度最小的位置更新.
        为什么最小值? 因为最小值的蓄满水之后可能变高, 需要更新传递给周围的位置.
    具体而言, **维护一个 #最小堆 记录当前边界上的约束高度**.
    复杂度: O(mn log(m+n))
思路2: 上面的思路理解为一个一个「加水」, 另一种思路是「漏水」. 初始时假设水位是最高的柱子高度. 然后从四周开始漏水, 将新的高度约束向内传递.
    具体而言, 可以用一个 #队列 来记录更新过的水位, 然后用起来更新周围的位置.
    复杂度: 由于采用的是队列, 更新某一位置的高度, 可能需要传播到整个矩阵, 因此复杂度 `O(m^2 n^2)`.
[官答](https://leetcode.cn/problems/trapping-rain-water-ii/solution/jie-yu-shui-ii-by-leetcode-solution-vlj3/)
"""
    def trapRainWater(self, heightMap: List[List[int]]) -> int:
        m,n = len(heightMap), len(heightMap[0])
        # 边界
        if m<3 or n<3: return 0
        ans = 0
        visited = [[0] * n for _ in range(m)]
        q = []
        # (h, i,j) 蓄水高度(约束), 位置
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        def check(x,y): return 0<=x<m and 0<=y<n
        # 初始化边界
        for x in range(m):
            for y in range(n):
                if x==0 or x==m-1 or y==0 or y==n-1:
                    visited[x][y] = 1
                    for dx,dy in directions:
                        nx,ny = x+dx, y+dy
                        if not check(nx,ny) or visited[nx][ny]: continue
                        # 约束传播
                        nHeight = max(heightMap[nx][ny], heightMap[x][y])
                        heappush(q, (nHeight, nx,ny))
        # 
        while q:
            nh,x,y = heappop(q)
            # 避免重复访问!
            if visited[x][y]: continue
            visited[x][y] = 1       # 标记访问
            # 可蓄水高度 > 柱子, 更新 ans
            if nh > heightMap[x][y]: ans += nh - heightMap[x][y]
            # 直接传播的约束
            h = max(nh, heightMap[x][y])
            for dx,dy in directions:
                nx,ny = x+dx, y+dy
                if not check(nx,ny) or visited[nx][ny]: continue
                # 约束传播
                nHeight = max(heightMap[nx][ny], h)
                heappush(q, (nHeight, nx,ny))
        return ans
    
    """ 1095. 山脉数组中查找目标值 #hard 
给定一个「山脉数组」, 元素严格递增递减. 在其中查找 =target 的元素 idx. 
限制: 本题是一个 #交互题, 对于 n 1e4, 要求 100次调用内解决.
思路1: 模拟搜索的过程, #细节比较多
思路2: 官答分解成两步, 先用二分找到peak点, 然后在两个有序数组中 #二分 找目标值. 更清楚
    [official](https://leetcode.cn/problems/find-in-mountain-array/solution/shan-mai-shu-zu-zhong-cha-zhao-mu-biao-zhi-by-leet/)
"""
    def findInMountainArray(self, target: int, mountain_arr: 'MountainArray') -> int:
        def find(l,r):
            if l > r: return -1
            m = (l+r) // 2
            vm = mountain_arr.get(m)
            if vm==target:
                # 注意不能直接返回! 因为可能mid可能是等高的靠右的那个. 
                v = find(l,m-1)
                if v!=-1: return v
                return m
            if m==0: return find(l+1,r)
            vml = mountain_arr.get(m-1)
            # if vml==target: return m-1
            if vm > vml:
                if target > vm: return find(m+1,r)
                else:
                    v = find(l,m-1)
                    if v!=-1: return v
                    else: return find(m+1,r)
            else:
                if target > vm: return find(l,m-1)
                else:
                    v = find(l,m-1)
                    if v!=-1: return v
                    else: return find(m+1,r)
        return find(0, mountain_arr.length()-1)

    """ 0727. 最小窗口子序列 #hard #题型 #star 给定字符串s,t, 要求找到s中最小的子串, 使得t是该子串的子序列. 限制 s的长度 n 2e4 t的长度 k 100
思路1: #DP (前缀递推)
    记 `f(i,j)` 为 s[:i] 中, 包含了 t[:j] 的子序列的最右start位置. 例如, 对于 aabc.., 中的位置c, 要找到最小的包含ab的子序列, 则最晚的start位置为1.
    转移: 每次转移时, 尽量用「最小长度/最右start的序列」. 因此有 `f(i,j) = max{f(0...i-1, j-1)} and 位置i匹配第j个目标 or f(i, 0...j)`
        其中第一项表示匹配前 j-1 个字符并且当前i位置匹配第j个字符, 第二项表示 [:j-1] 进行完成了匹配.
        具体的转移有较多 #细节. 并且可以转为一维.
    复杂度: `O(n * k)`
    在官答中, `f(i,j)` 的定义为, s[i]=t[j] 并且 s[:i-1] 可以匹配 t[:j-1] 的最右start位置. 思路更简洁.
思路2: 从每个位置开始 #模拟 匹配s 的过程, 利用 next 数组来加速.
    具体而言, 需要预处理得到 `next[i][ch]` 表示「从位置i开始, 下一个字符为ch的位置」.
    这样, 我们从idx开始匹配target, 可以在 O(k) 内得到结果. 因此总复杂度 O(n * k)
思路3: #滑动窗口 #star. 我们从每一个位置出发, 尝试正向匹配t, 若在位置right匹配成功了, 则反向再匹配一次, 得到最小的窗口.
    复杂度: 虽然看上去有「浪费」, 但注意这里复杂度仍然是 `O(n * k)`! 实际测试下来反而是最优的!
    see [here](https://leetcode.cn/problems/minimum-window-subsequence/solution/itcharge-727-zui-xiao-chuang-kou-zi-xu-l-v3az/)
[官答](https://leetcode.cn/problems/minimum-window-subsequence/solution/zui-xiao-chuang-kou-zi-xu-lie-by-leetcode/)
"""
    def minWindow(self, S: str, T: str) -> str:
        # 思路1: #DP (前缀递推)
        m,n = len(S), len(T)
        # f(i,j): S[:i] 中, 包含了 T[:j] 的子序列的最右start位置
        f = [[-1]*n for _ in range(m)]
        # 边界: 仅匹配第一个字符. 应该可以通过哨兵来优化.
        last = -1   # 最近一个符合的位置.
        for i,ch in enumerate(S):
            if ch == T[0]: last = i
            f[i][0] = last
        # 匹配剩余字符.
        for j in range(n):
            last = -1   # 最近一个符合的位置.
            for i in range(m):
                if i>0 and f[i-1][j-1] != -1 and T[j]==S[i]: f[i][j] = f[i-1][j-1]
                if f[i][j] != -1: last = f[i][j]
                if last != -1: f[i][j] = last
        # 找到最小窗口
        ans = ""; mn = m+1
        for i in range(m):
            if f[i][n-1] != -1 and i-f[i][n-1]+1 < mn:
                mn = i-f[i][n-1]+1
                ans = S[f[i][n-1]:i+1]
        return ans
    def minWindow(self, S, T):
        # 思路1: #DP (前缀递推) 官方实现
        cur = [i if x == T[0] else None for i, x in enumerate(S)]
        # At time j when considering T[:j+1],
        # the smallest window [s, e] where S[e] == T[j]
        # is represented by cur[e] = s.
        for j in range(1, len(T)):
            last = None
            new = [None] * len(S)
            # Now we would like to calculate the candidate windows
            # "new" for T[:j+1].  'last' is the last window seen.
            for i, u in enumerate(S):
                if last is not None and u == T[j]: new[i] = last
                if cur[i] is not None: last = cur[i]
            cur = new

        # Looking at the window data cur, choose the smallest length window [s, e].
        ans = 0, len(S)
        for e, s in enumerate(cur):
            if s is None: continue
            if s >= 0 and e - s < ans[1] - ans[0]:
                ans = s, e
        return S[ans[0]: ans[1]+1] if ans[1] < len(S) else ""
    def minWindow(self, S, T):
        # 思路2: 从每个位置开始 #模拟 匹配s 的过程, 利用 next 数组来加速.
        N = len(S)
        # `next[i][ch]` 表示「从位置i开始, 下一个字符为ch的位置」.
        next = [None] * N
        last = [-1] * 26
        for i in range(N-1, -1, -1):
            last[ord(S[i]) - ord('a')] = i
            next[i] = tuple(last)
        # 从target的角度进行匹配, 相较于从source的角度, 可以起到一定的「剪枝」效果? 
        windows = [[i, i] for i, c in enumerate(S) if c == T[0]]
        for j in range(1, len(T)):
            letter_index = ord(T[j]) - ord('a')
            windows = [[root, next[i+1][letter_index]]
                       for root, i in windows
                       if 0 <= i < N-1 and next[i+1][letter_index] >= 0]
        if not windows: return ""
        i, j = min(windows, key = lambda x: x[1]-x[0])
        return S[i: j+1]
    
    def minWindow(self, s1: str, s2: str) -> str:
        # 思路3: #滑动窗口 #star. 我们从每一个位置出发, 尝试正向匹配t, 若在位置right匹配成功了, 则反向再匹配一次, 得到最小的窗口.
        i, j = 0, 0     # j: 待匹配的s2的位置
        min_len = float('inf')
        left, right = 0, 0
        while i < len(s1):
            if s1[i] == s2[j]:
                j += 1
            # 完成了匹配
            if j == len(s2):
                right = i
                # 反向匹配, 从而找到最小的子数组.
                j -= 1
                while j >= 0:
                    if s1[i] == s2[j]:
                        j -= 1
                    i -= 1
                i += 1
                if right - i + 1 < min_len:
                    left = i
                    min_len = right - left + 1
                j = 0
            i += 1
        return "" if min_len == float('inf') else s1[left: left + min_len]


    """ 0010. 正则表达式匹配 #hard #题型 #star 实现可以有 `.*` 两个符号规则的正则表达式. 规则: `.` 匹配任意单个字符; `*` 匹配零个或多个前面的那一个元素
思路1: #DP 记 `f(i,j)` 表示 `s[:i]` 和 `p[:j]` 是否匹配.
    然后 #分类: 1) p[j] 为一般字符, 只有当 `s[i]==p[j]` 且 `f(i-1,j-1)` 成立时, 才匹配. 2) 若为 `.`, 忽略 `s[i]==p[j]` 这一条件.
        3) 若为 `*`, 再次根据 `p[i-1]` 的情况分类: 若为一般字符, 向前搜索 s[i,i-1...] 是否为 p[i-1], 若遇到 `f(x, j-2)` 成立, 则匹配; 若为 `.` 则匹配条件放宽.
    细节: 注意 #空字符串 的情况, 引入哨兵.
参见 [官答](https://leetcode.cn/problems/regular-expression-matching/solution/zheng-ze-biao-da-shi-pi-pei-by-leetcode-solution/), 更为简洁.
"""
    def isMatch(self, s: str, p: str) -> bool:
        m,n = len(s), len(p)
        f = [[False] * (n+1) for _ in range(m+1)]
        f[0][0] = True
        for i in range(m+1):
            for j in range(1, n+1):
                if p[j-1]=='.': f[i][j] = f[i-1][j-1] if i>0 else False
                elif p[j-1]=='*':
                    # 2) 重点是 `*` 的匹配
                    if p[j-2]=='.': f[i][j] = any(f[k][j-2] for k in range(i+1))
                    else:
                        # 匹配所有和 ch = p[j-2] 相同的字符.
                        ch = p[j-2]; idx = i
                        while idx>0:
                            if f[idx][j-2]: f[i][j] = True; break
                            if s[idx-1]!=ch: break
                            else: idx -= 1
                        # 最后的边界: 匹配到空字符串.
                        else: f[i][j] = f[0][j-2]
                else: f[i][j] = f[i-1][j-1] if (i>0 and s[i-1]==p[j-1]) else False
        return f[m][n]
    def isMatch(self, s: str, p: str) -> bool:
        # from 官答, 更为简洁.
        m, n = len(s), len(p)
        def match(i, j):
            # 辅助函数，判断 s[i-1] 是否等于 p[j-1]。成立条件：1. p[j-1] == '.'则可匹配任意非空字符；2. 或者 s[i-1]=p[j-1]
            # 考虑边界条件：i>=0, j>=1
            if i == 0:
                # 加上这一行的目的在于：例如 "" 无法被 "." 匹配，但不加的话因为 p[j-1] == '.' 而返回 True
                return False
            if p[j-1] == '.':
                return True
            return s[i-1] == p[j-1]

        f = [[False] * (n+1) for _ in range(m+1)]
        f[0][0] = True
        for i in range(m+1):
            # 注意 0 长度的 s 是可能和如 'a*' 的 p 匹配的，因此要从开始循环
            for j in range(1, n+1):
                # 而 0 长度 p 只能和 0 长 s 匹配
                if p[j-1] != '*':
                    if match(i, j):
                        f[i][j] |= f[i-1][j-1]
                    # else:
                    #     f[i][j] = False
                else:
                    # if match(i, j-1):
                    #     f[i][j] |= f[i][j-2] | f[i-1][j]
                    # else:
                    #     f[i][j] |= f[i][j-2]
                    f[i][j] |= f[i][j - 2]
                    if match(i, j - 1):
                        f[i][j] |= f[i-1][j]
        return f[m][n]
    
    """ 0044. 通配符匹配 #hard #题型 #star. 检查p是否可以完全匹配s. 符号: `?` 匹配任意单个字符, `*` 匹配任意字符串 (包括空)
e.g.: s = "adceb", p='*a*b' 是匹配的
思路1: #DP. 注意对于空字符的匹配, #细节.
    记 `f(i,j)` 表示 `s[:i]` 和 `p[:j]` 是否匹配.
    #分类 讨论: 1) 若 p[j] 为一般字符, 只有当 `s[i]==p[j]` 且 `f(i-1,j-1)` 成立时, 才匹配. 2) 若为 `?`, 忽略 `s[i]==p[j]` 这一条件.
        3) 若为 `*`, 只需要 `p[:j-1]` 能与之前的任意前缀匹配即可, 也即 `f(i,j) = any( f(0...i,j-1))` 
    复杂度: O(mn)
思路2: #贪心. 基本思想是, 本题中特殊字符只有 `*` 可以匹配任意子串.
    因此, 可以基于 * 对于 p进行分割, 剩余部分 `u_i` 是一定要匹配到的. 
    具体而言, 我们可以将 p 表示为 `*, u_1, *, u_2, *, .... u_i, *` 的形式 (首尾的非 * 可以预处理先匹配掉).
    如何对于这些子表达式进行匹配? 基本思路是, 我们在 s中尝试找到 `u_1` (记录匹配位置 `sRecord, pRecord`), 并接着继续找 `u_2` 若失败, 则回到记录位置重新开始找 `u_1`,....
    具体见代码.
本题与「0010. 正则表达式匹配」非常类似，但相比较而言，本题稍微容易一些。因为在本题中，模式 p 中的任意一个字符都是独立的，即不会和前后的字符互相关联，形成一个新的匹配模式。因此，本题的状态转移方程需要考虑的情况会少一些。
[官方](https://leetcode-cn.com/problems/wildcard-matching/solution/tong-pei-fu-pi-pei-by-leetcode-solution/)
"""
    def isMatch1(self, s: str, p: str) -> bool:
        # 思路1: #DP. 注意对于空字符的匹配, #细节.
        m,n = len(s), len(p)
        # 由于需要匹配空字符, 所以至少 s维度 需要引入哨兵.
        f = [[False] * (n+1) for _ in range(m+1)]
        f[0][0] = True
        for i in range(m+1): # 注意从空字符开始匹配.
            for j in range(1,n+1):
                if p[j-1]=='?': f[i][j] = f[i-1][j-1] if i>0 else False
                elif p[j-1]=='*': f[i][j] = any(f[k][j-1] for k in range(i+1))
                else: f[i][j] = (s[i-1]==p[j-1] and f[i-1][j-1]) if i>0 else False
        return f[-1][-1]
    def isMatch1(self, s: str, p: str) -> bool:
        # 思路2: #贪心. #hardhard
        def allStars(st: str, left: int, right: int) -> bool:
            return all(st[i] == '*' for i in range(left, right))
        
        def charMatch(u: str, v: str) -> bool:
            return u == v or v == '?'

        sRight, pRight = len(s), len(p)
        # 1) 匹配掉尾部, 直到 p[pRight - 1] == '*'
        while sRight > 0 and pRight > 0 and p[pRight - 1] != '*':
            if charMatch(s[sRight - 1], p[pRight - 1]):
                sRight -= 1
                pRight -= 1
            else:
                return False
        # 边界
        if pRight == 0:
            return sRight == 0
        # 2) 经过处理后 p 以 * 结尾 ( `*, u_1, *, u_2, *, .... u_i, *` 的形式), 将其与 s 进行匹配.
        sIndex, pIndex = 0, 0       # 用 sIndex 和 pIndex 表示当前遍历到 s 和 p 的位置
        sRecord, pRecord = -1, -1   # 此时我们正在 s 中寻找某个 u_i (被 * 分割的段), 其在 s 和 p 中的起始位置为 sRecord 和 pRecord
        while sIndex < sRight and pIndex < pRight:
            if p[pIndex] == '*':
                # 如果遇到星号，说明找到了 u_i，开始寻找 u_i+1
                pIndex += 1
                sRecord, pRecord = sIndex, pIndex
            elif charMatch(s[sIndex], p[pIndex]):
                # 如果两个字符可以匹配，就继续寻找 u_i 的下一个字符
                sIndex += 1
                pIndex += 1
            elif sRecord != -1 and sRecord + 1 < sRight:
                # 如果两个字符不匹配，那么需要重新寻找 u_i 枚举下一个 s 中的起始位置
                sRecord += 1
                sIndex, pIndex = sRecord, pRecord
            else:
                # 如果不匹配并且下一个起始位置不存在，那么匹配失败
                return False
        # 3) 将s匹配完毕之后, p剩余的部分只能是全 *
        return allStars(p, pIndex, pRight)


""" 0295. 数据流的中位数 #hard 实现一个数据结构, 可以加入数据, 并计算当前数据 #中位数.
思路1: 维护两个「平衡的」 #优先队列. 一个最大堆, 一个最小堆.
    我们分别用 mn,mx 最大堆最小堆维护 最小的一半和较大的一半数据, 并保持 size(mn) = size(mx) or size(mx)+1
    查询: 根据两个堆的大小关系返回
    插入: 根据与堆顶元素的大小关系插入, 再维护平衡性. 复杂度 O(logn)
思路2: 可以用 #有序集合 SortedList 维护数据, 并用 #双指针 记录中位数位置
进阶1: 若数据范围在 [0,100], 可以用 「计数排序统计每一类数的数量，并使用双指针维护中位数」
进阶2: 若 99% 的整数都在 0 到 100 范围内. 则可以直接用数组保存超过该范围的数字 (因为大概率没用), 若小概率中位数在这范围内的话, 暴力搜索即可.
[official](https://leetcode.cn/problems/find-median-from-data-stream/solution/shu-ju-liu-de-zhong-wei-shu-by-leetcode-ktkst/)
"""
class MedianFinder:
    def __init__(self):
        self.mn = []
        self.mx = []

    def addNum(self, num: int) -> None:
        if self.mn and num < -self.mn[0]:
            heappush(self.mn, -num)
            if len(self.mn) > len(self.mx)+1:
                heappush(self.mx, -heappop(self.mn))
        else:
            heappush(self.mx, num)
            if len(self.mx) > len(self.mn):
                heappush(self.mn, -heappop(self.mx))

    def findMedian(self) -> float:
        if len(self.mn)==len(self.mx): return (-self.mn[0]+self.mx[0])/2
        else: return -self.mn[0]




    
sol = Solution()
result = [
    # sol.smallestDistancePair([1,3,1], 1),
    # sol.smallestDistancePair(nums = [1,1,1], k = 2),
    # sol.smallestDistancePair(nums = [1,6,1], k = 3),
    # sol.smallestDistancePair([9,10,7,10,6,1,5,4,9,8], 18),
    # sol.trapRainWater(heightMap = [[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]]),
    # sol.trapRainWater(heightMap = [[3,3,3,3,3],[3,2,2,2,3],[3,2,1,2,3],[3,2,2,2,3],[3,3,3,3,3]]),
#     testClass("""["MedianFinder","addNum","findMedian","addNum","findMedian","addNum","findMedian","addNum","findMedian","addNum","findMedian","addNum","findMedian","addNum","findMedian","addNum","findMedian","addNum","findMedian","addNum","findMedian","addNum","findMedian"]
# [[],[6],[],[10],[],[2],[],[6],[],[5],[],[0],[],[6],[],[3],[],[1],[],[0],[],[0],[]]""")
    # sol.minWindow(S = "abcdebdde", T = "bde"),
    # sol.isMatch1(s = "aa", p='a'),
    # sol.isMatch1(s = "aa", p='*'),
    # sol.isMatch1(s = "adceb", p='*a*b'),
    # sol.isMatch1("", '***'),
    
    sol.isMatch(s = "aa", p = "a"),
    sol.isMatch(s = "ab", p = ".*"),
    sol.isMatch(s = '', p = '.'),     #边界
    sol.isMatch(s = "aaaab", p = "a*ab"),   #懒惰匹配
    sol.isMatch("ipp", "ip*"),
    sol.isMatch("mississippi", "mis*is*ip*.")
]
for r in result:
    print(r)
