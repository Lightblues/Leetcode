from mimetypes import init
from re import A
import typing
from typing import List, Optional, Tuple
import copy
from copy import deepcopy, copy
import collections
from collections import deque, defaultdict, Counter, OrderedDict, namedtuple
import math
from math import sqrt, ceil, floor, log, log2, log10, exp, sin, cos, tan, asin, acos, atan, atan2, hypot, erf, erfc, inf, nan
import bisect
import heapq
from heapq import heappush, heappop, heapify, heappushpop
import functools
from functools import lru_cache, cache, reduce, partial
# cache for Python 3.9, equivalent to @lru_cache(maxsize=None)
import itertools
from itertools import accumulate, product, permutations, combinations, combinations_with_replacement
import string
from string import ascii_lowercase, ascii_uppercase
# s = ""
# s.isdigit, s.islower, s.isnumeric
import sys, os
# sys.setrecursionlimit(10000)

# https://github.com/grantjenks/python-sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode

""" 单调栈题型
=== 得到指定条件的子序列
0316. 去除重复字母 #medium #题型 #单调栈 #stack
    要求得到一个字符串的子串, 1) 由原本字符串中的所有元素组成; 2) 所有字符不重复; 3) 字典序最小.
2030. 含特定字母的最小子序列 #单调栈 #hard #题型
    给定一个字符串s要求找到一个长度为k的子序列 (不要求连续), 使得: 1) 其中包含至少 repetition 个特定字符 letter; 2) 子序列字典序最小.


=== 枚举子数组
0496. 下一个更大元素 I #easy #题型 #单调栈 
    要求 O(n) 时间内计算数组中每个元素的下一个更大元素
0503. 下一个更大元素 II #medium
    相较于 0496, 这里是一个「循环数组」, 也即需要考虑一个环中, 比当前元素更大的下一个元素值.
    思路: 仅需要「循环遍历」两次即可
0907. 子数组的最小值之和 #medium #题型 #单调栈
    求所有子数组的最小值的和
1856. 子数组最小乘积的最大值 #medium 
    定义一个子数组的score: 为 **数组元素和 * 最小元素**. 现给定一个数组, 要求返回最大的score.
    思路1: #单调栈 #前缀和 类似 0907 寻找左右边界; 子数组和可以通过前缀和求得.
    代码: 可以将寻找左右边界合并到一个单调栈上, 但注意一个是开一个是比区间.
2104. 子数组范围和 #medium
    定义子数组的score为 **最大最小元素的差值**. 要求返回一个数组中所有子数组score和.
6077. 巫师的总力量和 #hard #单调栈 #前缀和
    对一个子数组, 定义score为 **最小元素 * 子数组元素和**, 现给定一个数组求所有子数组的score之和.

6080. 使数组按非递减顺序排列 #medium #题型
    给定一个数组经过若干次删除操作将其变为非递减数组. 每次操作定义为: 删除满足 `nums[i - 1] > nums[i]` 的位置的元素 i. 问经过多少次操作后得到最终结果 (非递减).
    利用单调栈维护「该元素被删除的时刻」

@2022 """
class Solution:
    """ 0316. 去除重复字母 #medium #题型 #单调栈 #stack
要求得到一个字符串的子串, 1) 由原本字符串中的所有元素组成; 2) 所有字符不重复; 3) 字典序最小.
思路: 单调栈
    去除限制条件, 我们如何得到一个尽可能小的字符串? 基本思路是 **维护一个单调栈**, 当遇到一个新的字符时, 如果栈顶元素小于当前字符, 则递归弹出栈顶元素, 然后再把这个字符入栈; 否则直接把当前字符压入栈 (注意当前字符总会入栈).
    这里要求 1) 保留原字符串中的所有元素, 因此用一个 counter 记录剩余的数量, 当剩余数量为0时, 我们不能将该元素弹出栈; 3) 字符不重复, 因此在入栈的时候判断该字符是否已经在栈内.
[here](https://leetcode.cn/problems/remove-duplicate-letters/solution/qu-chu-zhong-fu-zi-mu-by-leetcode-soluti-vuso/)
"""
    def removeDuplicateLetters(self, s: str) -> str:
        stack = []
        # counter 记录字母剩余的数量
        counter = collections.Counter(s)
        for ch in s:
            counter[ch] -= 1
            # 字符已经用过了, 去重
            if ch in stack: continue
            while stack and ch < stack[-1]:
                # 注意这里是 while, 例如 "bcabc" 需要将栈中的 bc 都弹出.
                # 剩余字符还有, 可以弹出
                if counter[stack[-1]] > 0: stack.pop()
                else: break
            # ch 在 ch < stack[-1] 与否两种情况下都会入栈
            stack.append(ch)
        return "".join(stack)


    """ 2030. 含特定字母的最小子序列 #单调栈 #hard #题型
给定一个字符串s要求找到一个长度为k的子序列 (不要求连续), 使得: 1) 其中包含至少 repetition 个特定字符 letter; 2) 子序列字典序最小.
关联: 0316. 去除重复字母; 另有基本题型「求长为 k 的字典序最小子序列」
本题的限制包括 1) 子序列长度为 k; 2) 子序列中包含至少 repetition 个特定字符 letter.
思路: 单调栈, 注意判断这些限制条件!
单调栈相关问题思路: 
- 注意空栈 pop 的错误;
- 限制子序列长度为 k: 1) 在push的时候判断时候超过限制; 2) pop时判断剩余的是否够, 即使 break;
- 限制栈内元素数量 (比如要求ch的数量至少为repetition): 1) pop的时候检查剩余是否够; 2) 另外需要检查, 若栈内元素不足以放剩余的ch (repetition-countInStack), 则需要push.
"""
    def smallestSubsequence(self, s: str, k: int, letter: str, repetition: int) -> str:
        countLetter = collections.Counter(s)[letter]
        stack = []
        n = len(s)
        # 允许从栈中弹出的 letter 数量
        # possPop = counter[letter] - repetition
        # 
        cInStack = 0 # 当前栈中的字符 letter 数量
        cPop = 0     # 弹出的 letter数量
        for i, ch in enumerate(s):
            """ 单调栈的 pop 条件: 递归弹出比当前判断元素大的栈顶元素 """
            # 注意防止 stack 空
            while stack and ch < stack[-1]:
                # 条件1: 长度k的约束不允许弹出
                if len(stack) + (n-i) <= k:
                    break
                if stack[-1]==letter:
                    # 条件2: 不允许弹出 letter 了
                    if countLetter - cPop - 1 < repetition:
                        break
                    cPop += 1
                    cInStack -= 1
                    stack.pop()
                else:
                    stack.pop()
            # 条件2: 剩余空间不足以放剩下的 letter
            # while k - len(stack) < repetition-cInStack: 
            #     c = stack.pop()
            #     # cInStack -= c==letter
            # 每次压入栈一个元素的时候检查即可, 不需要用到while
            if k-len(stack) < repetition-cInStack:
                stack.pop()
            # 条件1: 长度k约束. 当前栈已经超过 k 了, 不在压入栈
            if len(stack) >= k:
                cPop += ch==letter
                continue
            stack.append(ch)
            if ch==letter:
                cInStack += 1
        return "".join(stack)














    """ 0496. 下一个更大元素 I #easy #题型 #单调栈
有一个数组 nums2, 满足所有元素都不同. 在给一组查询 nums1, 其每一个元素都是 nums2 中的元素, 要求返回每一次查询的数字之后的 (下一个) 更大元素的值.
思路1: #单调栈. 
    也即, 需要建立一个index, 记为 nextGreater[i] 表示在nums2的第i位置的元素的下一个更大元素 (位置或者值).
    为建立这里index, 可以从后往前遍历, 构建单调递减栈 (从栈底到栈顶).
[here](https://leetcode.cn/problems/next-greater-element-i/solution/xia-yi-ge-geng-da-yuan-su-i-by-leetcode-bfcoj/)

输入：nums1 = [4,1,2], nums2 = [1,3,4,2].
输出：[-1,3,-1]
解释：nums1 中每个值的下一个更大元素如下所述：
- 4 ，用加粗斜体标识，nums2 = [1,3,4,2]。不存在下一个更大元素，所以答案是 -1 。
- 1 ，用加粗斜体标识，nums2 = [1,3,4,2]。下一个更大元素是 3 。
- 2 ，用加粗斜体标识，nums2 = [1,3,4,2]。不存在下一个更大元素，所以答案是 -1 。

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/next-greater-element-i
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        # 单调栈
        s = []
        # 实际上, 由于仅需要下一个更大元素 (而不是 idx), 因此这里 直接用 num 作为栈元素即可而不需要 (num, idx) 作为元素
        # for num in nums2[::-1]:
        nextGreater = [None] * len(nums2)
        for i in range(len(nums2)-1, -1, -1):
            num = nums2[i]
            while s and s[-1][0] < num:
                s.pop()
            if not s:
                nextGreater[i] = -1
            else:
                # nextGreater[i] = s[-1][1]
                nextGreater[i] = s[-1][0]
            s.append((num, i))
        num2idx = {num: i for i, num in enumerate(nums2)}
        return [nextGreater[num2idx[num]] for num in nums1]
    
    """ 0503. 下一个更大元素 II #medium
相较于 0496, 这里是一个「循环数组」, 也即需要考虑一个环中, 比当前元素更大的下一个元素值.
例子: [1,2,1] 的结果应该是 [2, -1, 2]
思路1: 还是用 #单调栈, 不过需要循环两次
"""
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        n = len(nums)
        s = []
        ans = [-1] * n
        for i,a in enumerate(nums+nums):
            while s and s[-1][0]<a: # 要找的是严格大的元素
                v, idx = s.pop()
                ans[idx%n] = a
            s.append((a,i))
        return ans
    
    """ 0907. 子数组的最小值之和 #medium #题型 #单调栈
对于一个数组的所有(连续)子数组定义一个分数: 为这一子数组中的最小元素的值. 要求返回该数组所有子数组的分数之和.
思路1: #单调栈 记录每一个元素作为最小值的(左右)边界.
    考虑一个元素可以作为哪些子数组的最小值? [-100, 2,3,0,1, -100] 为例, 中间0作为子数组最小值的情况被两侧比0小的元素所确定.
    因此, 可以记录每一个元素的左右边界 (左右比该元素小的下一个位置), 经典的单调栈问题.
    注意, 需要考虑重复数值的问题, 例如 [1,3,1,2] 中, 可以将第一个1负责 [1,3,1,2] 这里范围, 而第二个1负责 [3,1,2] 范围. 也即, 右侧边界是严格小, 左侧边界是小于等于.
    具体计算最小值所出现的子数组数量, 假设idx位置元素的左右边界分别为l,r, 则有 `(idx-l) * (r-idx)` 个子数组. 例如 [1,2,0,1] 中的0作为子数组最小值的情况就有 3*2=6 种.
    因此答案就是 sum(arr[idx] * (idx-l) * (r-idx)) 对于每一个idx遍历求和.
思路2: #DP #单调栈
    相较于上面考虑每一个元素在哪些部分作为最小值, 这里考虑从左到右, 每一个增加的元素所增加的子数组. 对于增加的第j个元素, 遍历所有 [i,j] 区间, 这些区间的最小值有什么规律?
    例如, 对于数组 `A = [1,7,5,2,4,3,9]` 考虑元素 9 (j=6) 所新增的子数组, 这些数组的最小值分别为 `B = [1,2,2,2,3,3,9]`.
    有什么规律? 递增! 可以用递增栈的形式存储 (val, count) 元素, 例如 `(1,1), (2,3), (3,2)`. 每次更新时时, 尝试压入 (arr[j], 1).
    为了得到栈内信息 (数组B的和), 可以维护一个变量 `dot = sum(val*count)`.
[here](https://leetcode.cn/problems/sum-of-subarray-minimums/solution/zi-shu-zu-de-zui-xiao-zhi-zhi-he-by-leetcode/)
"""
    def sumSubarrayMins(self, arr: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(arr)
        # 记录下一个比 idx 小 (严格小) 的元素的 idx
        right = [n] * n
        s = []
        for i in range(n-1, -1, -1):
            while s and s[-1][0] >= arr[i]:
                s.pop()
            right[i] = s[-1][1] if s else n
            s.append((arr[i], i))
        # 记录上一个比 idx 小 (小于等于) 的元素的 idx
        left = [-1] * n
        s = []
        for i in range(n):
            while s and s[-1][0] > arr[i]:
                s.pop()
            left[i] = s[-1][1] if s else -1
            s.append((arr[i], i))
        
        ans = 0
        for i in range(n):
            # 注意, 这个元素所在的子数组数量为 (idx-l) * (r-idx)
            ans += (arr[i] * (i - left[i]) * (right[i] - i)) % MOD
            ans %= MOD
        return ans

    def sumSubarrayMins(self, arr: List[int]) -> int:
    # https://leetcode.cn/problems/sum-of-subarray-minimums/solution/zi-shu-zu-de-zui-xiao-zhi-zhi-he-by-leetcode/
        MOD = 10**9 + 7
        n = len(arr)
        
        stack = []
        ans = dot = 0
        for i,num in enumerate(arr):
            count = 1
            while stack and num < stack[-1][0]:
                v, c = stack.pop()
                dot -= v*c
                count += c
            stack.append((num, count))
            dot += num*count
            dot %= MOD
            ans += dot
        return ans % MOD


    """ 1856. 子数组最小乘积的最大值 #medium 
定义一个子数组的score: 为数组元素和 * 最小元素. 现给定一个数组, 要求返回最大的score.
思路1: #单调栈 #前缀和 类似 0907 寻找左右边界; 子数组和可以通过前缀和求得.
    通过单调栈来计算每一个元素作为最小值的左右边界
思路2: 在代码层面, 除了用两次单调栈来得到所有边界, 实际上只需要一个单调栈即可同时求出
    具体来说, 若在遍历位置i的过程中, 假如遵循的是 `nums[s[-1]] >= nums[i]`, 则对于每一个栈顶元素来说, 其下一个更小元素为位置i; 而对于while循环后将i入栈, 则此时的栈顶元素 j 是左侧第一个满足大于等于 nums[i] 的元素.
    注意, 这里求的 right是严格小于 nums[i] 的元素位置, 而left则是小于等于 nums[i] 的元素位置. 但 **这不影响结果, 因为左右边界中总有一个得到了最长的数组**.
关联: 「6077. 巫师的总力量和」

输入：nums = [1,2,3,2]
输出：14
解释：最小乘积的最大值由子数组 [2,3,2] （最小值是 2）得到。
2 * (2+3+2) = 2 * 7 = 14 。

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/maximum-subarray-min-product
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
    def maxSumMinProduct(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        # 记录下一个比 idx 小 (严格小) 的元素的 idx
        right = [n] * n
        s = []
        for i in range(n-1, -1, -1):
            while s and s[-1][0] >= nums[i]:
                s.pop()
            right[i] = s[-1][1] if s else n
            s.append((nums[i], i))
        # 记录上一个比 idx 小 (严格小) 的元素的 idx
        left = [-1] * n
        s = []
        for i in range(n):
            while s and s[-1][0] >= nums[i]:
                s.pop()
            left[i] = s[-1][1] if s else -1
            s.append((nums[i], i))
        
        cumsum = list(itertools.accumulate(nums, initial=0))
        ans = 0
        for a,l,r in zip(nums, left, right):
            ans = max(ans, a * (cumsum[r] - cumsum[l+1]))
        return ans%MOD
    
    def maxSumMinProduct(self, nums: List[int]) -> int:
        n = len(nums)
        left = [0]*n; right = [n-1]*n
        s = []
        for i, num in enumerate(nums):
            # 注意下面的 right, left 都不包含边界点
            while s and nums[s[-1]] >= num:
                j = s.pop()
                right[j] = i-1   # nums[j] < nums[j+1,...,i-1]
            if s:
                left[i] = s[-1] + 1  # nums[i] >= nums[s[-1]+1,...,i-1]
            s.append(i)
        acc = list(accumulate(nums, initial=0))
        return max(v * (acc[r+1]-acc[l]) for v,l,r in zip(nums, left, right)) % (10**9 + 7)
    
    """ 2104. 子数组范围和 #medium
定义子数组的score为 **最大最小元素的差值**. 要求返回一个数组中所有子数组score和.
本题为中等的原因是复杂度 `nums.length <= 1000` 因此可以暴力求解, 进阶的要求是 O(n) 的实现.
思路1: #单调栈 记录每一个元素作为最大/最小值的次数 (计算左右边界).
    整体的分数为 `sum(max(i:j) - min(i:j)) = sum(max(i:j)) - sum(min(i:j))` 这里的最大最小是针对子数组 arr[i:j] 的.
    因此, 可以将原问题, 分解为求每一个元素作为最大/最小的次数, 求和相减即可.
    如何计算idx位置的元素在多少子数组中为最小元素? 类似0907, 维护左右两个边界即可. 注意出现的子数组数量是 `(idx-l) * (r-idx)` 乘法交互.
    see [here](https://leetcode.cn/problems/sum-of-subarray-ranges/solution/zi-shu-zu-fan-wei-he-by-leetcode-solutio-lamr/)


输入：nums = [1,2,3]
输出：4
解释：nums 的 6 个子数组如下所示：
[1]，范围 = 最大 - 最小 = 1 - 1 = 0 
[2]，范围 = 2 - 2 = 0
[3]，范围 = 3 - 3 = 0
[1,2]，范围 = 2 - 1 = 1
[2,3]，范围 = 3 - 2 = 1
[1,2,3]，范围 = 3 - 1 = 2
所有范围的和是 0 + 0 + 0 + 1 + 1 + 2 = 4

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/sum-of-subarray-ranges
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
    
"""
    def subArrayRanges(self, nums: List[int]) -> int:
        def tmp(nums):
            n = len(nums)
            # 记录下一个比 idx 小 (严格小) 的元素的 idx
            right = [n] * n
            s = []
            for i in range(n-1, -1, -1):
                while s and s[-1][0] >= nums[i]:
                    s.pop()
                right[i] = s[-1][1] if s else n
                s.append((nums[i], i))
            # 记录上一个比 idx 小 (小于等于) 的元素的 idx
            left = [-1] * n
            s = []
            for i in range(n):
                while s and s[-1][0] > nums[i]:
                    s.pop()
                left[i] = s[-1][1] if s else -1
                s.append((nums[i], i))
                
            # cumsum = list(itertools.accumulate(nums, initial=0))
            ans = 0
            for idx, (val,l,r) in enumerate(zip(nums, left, right)):
                # 注意, 这个元素所在的子数组数量为 (idx-l) * (r-idx)
                ans += val * (r - idx)*(idx - l)
            return ans
            
        return  -tmp([-x for x in nums]) - tmp(nums)

    """ 6077. 巫师的总力量和 #hard #单调栈
对一个子数组, 定义score为 **最小元素 * 子数组元素和**, 现给定一个数组求所有子数组的score之和.
    结合了 0907 和 1856
    复杂度: 长度 1e5, 每个元素 1e9
思路1: #单调栈 #前缀和
    考虑「一个元素在哪些子数组作为最小值」? 类似 0907, 利用单调栈求左右的边界.
    这些子数组的和如何计算? 参见下面的公式分析, 通过「前缀和的前缀和」.
    另外注意 cumsum的使用: 为了得到 arr[l:r] 的和, 可以使用 cumsum[r+1] - cumsum[l]
        例如, 对于数组 [1,2,3], 通过 `itertools.accumulate(arr, initial=0))` 得到前缀和 [0,1,3,6], 则 arr[0:2] = cumsum[3] - cumsum[0] = 6
总结: 利用数学公式进行严谨的推导 (和思维方式).
from [here](https://leetcode.cn/problems/sum-of-total-strength-of-wizards/solution/dan-diao-zhan-qian-zhui-he-de-qian-zhui-d9nki/)

设子数组右端点为 $r$, 左端点为 $l$, 当前枚举的元素下标为 $i$, 那么有 $l \leq i \leq r$ 。 设 strength 数组的前缀和为 $s$, 在范围 $[L, R]$ 内的所有子数组的元素和的和为
$$
\begin{aligned}
& \sum_{r=i+1}^{R+1} \sum_{l=L}^{i} s[r]-s[l] \\
=& \sum_{r=i+1}^{R+1}\left((i-L+1) \cdot s[r]-\sum_{l=L}^{i} s[l]\right) \\
=&(i-L+1) \cdot \sum_{r=i+1}^{R+1} s[r]-(R-i+1) \cdot \sum_{l=L}^{i} s[l]
\end{aligned}
$$
因此我们还需要计算出前缀和 $s$ 的前缀和 $s s$, 上式即为
$$
(i-L+1) \cdot(s s[R+2]-s s[i+1])-(R-i+1) \cdot(s s[i+1]-s s[L])
$$
累加所有贡献即为答案。
"""
    def totalStrength(self, strength: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(strength)
        
        # 求左右边界, 注意这里的边界都是开区间
        right  = [n] * n
        stack = []
        for i in range(n-1, -1, -1):
            while stack and stack[-1][0] >= strength[i]:
                stack.pop()
            right[i] = stack[-1][1] if stack else n
            stack.append((strength[i], i))
        left = [-1] * n
        stack = []
        for i in range(n):
            while stack and stack[-1][0] > strength[i]:
                stack.pop()
            left[i] = stack[-1][1] if stack else -1
            stack.append((strength[i], i))
        
        # len(s) == n+1; len(ss) == n+2
        s = list(itertools.accumulate(strength, initial=0))
        ss = list(itertools.accumulate(s, initial=0))
        ans = 0
        for idx, (val,l,r) in enumerate(zip(strength, left, right)):
            l,r = l+1, r-1
            ans += val * ((idx-l+1)*(ss[r+2] - ss[idx+1]) -  (r-idx+1)*(ss[idx+1] - ss[l]))
        return ans % MOD



    """ 6080. 使数组按非递减顺序排列 #medium #题型
给定一个数组经过若干次删除操作将其变为非递减数组. 每次操作定义为: 删除满足 `nums[i - 1] > nums[i]` 的位置的元素 i. 问经过多少次操作后得到最终结果 (非递减).
尝试0: 一开始想到, 通过一次遍历可以得到最终保留的子序列. 这样只需要计算这些idx所分割的每一个连续序列中, 需要进行的操作次数即可. 
    然而, 对于如何计算按照的删除方式「删除序列中的每一个元素」, 还是没想出来. 一开始想记录每一个递增序列的长度, 但是还需要考虑到 [1,2,3,1,2,3] 中, 第二个3 这样的情况.
思路1: 单调栈
    [here](https://leetcode.cn/problems/steps-to-make-array-non-decreasing/solution/by-endlesscheng-s2yc/)
    对于每一个元素 i, (若会被删除), 其删除时间由什么决定? 由 `nums[i - 1] > nums[i]` 这一公式决定. 也即其左侧的第一个比它大的元素, 记为 j.
    如何记录 j 的删除时间? 可以通过一个(严格)单调递减栈来解决.
    具体而言, 栈内记录 `(num, delete_time)`, 后者为它被移除的时刻. 对于每一个元素, 移除所有满足 `stack[-1][0] <= num` 的栈顶元素 (注意是小于等于).
        相等的时候, 1) 若num被保留, 下面的 `if stack` 语句确保了其移除时间的记录为 0; 2) num被移除, 则其被移除的时刻同样取决于上一个值为 num的元素. 例如 [3,1,2,1,2] 中两个2的移除时刻分别为 2,3.
    若经过pop操作后栈空, 说明该元素会被保留到最后, 其 `delete_time` 为 0. 否则, 为出栈元素中  `delete_time` 最大值 +1. 也即, `if stack: maxt += 1`
    """
    def totalSteps(self, nums: List[int]) -> int:
        """ [here](https://leetcode.cn/problems/steps-to-make-array-non-decreasing/solution/by-endlesscheng-s2yc/)
        """
        # 栈内元素为 (num, maxt) 其中第二个数字是它被移除的时刻
        stack = []
        ans = 0
        for num in nums:
            maxt = 0    # 记录num左侧的元素的小于等于num的元素的最大移除时间
            # 注意这里是 <=. 相等的时候, 1) 若num被保留, 下面的 `if stack` 语句确保了其移除时间的记录为 0; 2) num被移除, 则其被移除的时刻同样取决于上一个值为 num的元素. 例如 [3,1,2,1,2] 中两个2的移除时刻分别为 2,3.
            while stack and stack[-1][0] <= num:
                maxt = max(maxt, stack.pop()[1])
            # 若栈为空, 说明是新的最大元素, 其被移除的时刻为 0; 否则, 该元素会被移除, 其被移除的时刻为 maxt+1.
            if stack: maxt += 1
            ans = max(ans, maxt)
            stack.append((num, maxt))
        return ans

sol = Solution()
result = [
    # sol.nextGreaterElement(nums1 = [4,1,2], nums2 = [1,3,4,2]),
    # sol.nextGreaterElements(nums = [1,2,1]),
    # sol.nextGreaterElements(nums = [1,2,3,4,3]),
    
    # sol.sumSubarrayMins(arr = [3,1,2,4]),
    # sol.sumSubarrayMins(arr = [11,81,94,43,3]),
    
    sol.maxSumMinProduct(nums = [1,2,3,2]),
    sol.maxSumMinProduct(nums = [2,3,3,1,2]),
    
    # sol.subArrayRanges(nums = [1,2,3]),
    # sol.subArrayRanges(nums = [1,3,3]),
    # sol.subArrayRanges(nums = [4,-2,-3,4,1]),
    
    # sol.totalStrength(strength = [1,3,1,2]),
    # sol.totalStrength(strength = [5,4,6]),
]
for r in result:
    print(r)
