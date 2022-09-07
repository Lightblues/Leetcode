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
[滑动窗口和双指针](https://leetcode.cn/leetbook/detail/sliding-window-and-two-pointers/)

== 循环不变量
基本思想: 在循环过程中维护变量满足某一性质.
0026. 删除有序数组中的重复项 #easy
    「原地」修改已经排好序的数组, 使其不重复.
0027. 移除元素 #easy 原地移除数组中等于某val的元素
0283. 移动零 #easy 原地操作, 将0都放在数组最后, 保持其他元素相对位置
0674. 最长连续递增序列 #easy 找到数组中最长的严格递增序列
0080. 删除有序数组中的重复项 II #medium 将次数超过两次的多余数字删去

[应用] 类似快排的两道题
0075. 颜色分类 #medium #题型
    有3种颜色, 要求「原地」修改使得数组变为有序的状态.
0215. 数组中的第K个最大元素 #medium #题型 另见 [quick sort]
    思路1: 采用类似 #快排 的思路, 每次选择 pivot 对于 [l,r] 区间进行分割. 也类似 #二分


== 类型1: 同向交替移动的两个变量
固定长度的滑动窗口
0643. 子数组最大平均数 I #easy
1052. 爱生气的书店老板 #medium

== 类型2: 不定长度的滑动窗口
0076. 最小覆盖子串 #hard #题型
    给定字符串s和t, 要求s中长度最小的包含t中所有元素的子串. 限制: 长度 1e5
2062. 统计字符串中的元音子字符串 #easy #题型
    要求统计连续子序列的数量. 条件为: 1) 所有元素为元音字符 2) 包含所有aeiou五个元素.
    思路1: #双指针. 在满足条件的情况下尽量移动左边界.

== 类型3: 计数问题
0340. 至多包含 K 个不同字符的最长子串 #medium #题型 给定一个字符串, 要求找到拥有最多k个不同字符的子串的最大长度
    关联: 「159. 至多包含两个不同字符的最长子串」 #medium
0795. 区间子数组个数 #medium 求数组中, 最大元素在 [l,r] 范围内的子数组数量
    思路2: #分解. 考虑子问题「最大元素小于等于x的子数组数量」



== 链表中双指针技巧
0141. 环形链表 #easy #题型 判断链表是否有环
    思路1: #快慢指针
0142. 环形链表 II #题型 #medium
    相较于 0141, 需要返回进入环的第一个节点.
    **让slow继续从相遇点走, 同时在起点放置一个速度也为1的指针, 他们恰好会在入环点相遇**.
0019. 删除链表的倒数第 N 个结点 #medium #题型
    思路1: 让第一个指针先走n步. 然后两个指针一起走.
0160. 相交链表 #easy #题型
    给定两个节点, 判断他们是否会相交 (Y字型), 若相交返回相交的那个节点. 保证了无环. 进阶限制: 时间 O(m+n), 空间 O(1)
0876. 链表的中间结点 #easy 若长度为偶数, 则返回靠右的那个


== 双指针：相向交替移动的两个变量
0011. 盛最多水的容器 #medium #题型 从一组柱子中选两个, 构成的容积最大.
    思路1: 采用 #双指针. 每次向内移动较短边.
0167. 两数之和 II - 输入有序数组 #medium 给定一有序数组, 判断其中两个数字之和是否可以达到目标
    思路1: #双指针 根据当前值和目标的大小进行移动. 正确性: 相当于缩减了搜索空间.
0015. 三数之和 #medium #题型 给定一个数组, 找到所有「不重复的」三个数之和为0的组合. 限制: 数组长度 3000
    思路1: 排序后, 转化为「两数之和」.
0016. 最接近的三数之和 #medium #题型 给定一个数组, 找到三个数之和最接近目标值. 限制: 数组长度 1000.
0018. 四数之和 #medium 给定一个数组, 找到所有「不重复」的四个数字之和为目标的组合. 限制: 数组长度 200
    类似 0015, 不过外面套两层循环. 内部还是 #双指针.
0125. 验证回文串 #easy 忽略非数字字母字符, 判断是否回文.
0658. 找到 K 个最接近的元素 #medium 给定一个有序数组, 返回其中最接近x的k个数字 (距离相同取idx较小的).
    思路1: 双指针收缩, 直到长度为k.
0259. 较小的三数之和 #medium 给定一个数组, 计算 i,j,k 之和 <target 的三元组数量
0360. 有序转化数组 #medium 给定一数组, 对 其中每一个元素计算 f(x) = ax^2+bx+c, 对于结果排序
    进阶要求是在 O(n) 时间内完成.
0977. 有序数组的平方 #easy 给定一个有序数组, 返回平方后的有序数组.
0844. 比较含退格的字符串 #medium 给定两个字符串, 定义 # 为特殊字符表示退格, 判断两字符串是否相等.
    进阶要求: 空间 O(1)
0845. 数组中的最长山脉 #medium 定义「山脉」为上升下降的序列, 返回数组中最长的山脉长度.
    思路1: 遍历右端, 通过 #flag 标记当前是否满足条件 (并记录左端点). 但要考虑的 #细节 比较多. 其实也就是下面的 #双指针, 官答更清楚
0881. 救生艇 #medium 
0925. 长按键入 #easy
1099. 小于 K 的两数之和 #easy
1229. 安排会议日程 #medium 给定两组区间表示两人的空闲时间, 找到重叠最早的至少为 duration 的时间段.


"""
class Solution:
    
    """ ================================== 循环不变量 ================================ """
    """ 0026. 删除有序数组中的重复项 #easy
「原地」修改已经排好序的数组, 使其不重复.
思路1: 用一个指针指向下一个要放的位置.
"""
    def removeDuplicates(self, nums: List[int]) -> int:
        i = 0; pre = None
        for j,num in enumerate(nums):
            if num != pre:
                nums[i] = num
                i += 1
            pre = num
        return i
    """ 0027. 移除元素 #easy 原地移除数组中等于某val的元素 """
    """ 0283. 移动零 #easy 原地操作, 将0都放在数组最后, 保持其他元素相对位置 """
    def moveZeroes(self, nums: List[int]) -> None:
        n = len(nums)
        i = 0
        for j,num in enumerate(nums):
            if num != 0:
                nums[i] = num
                i += 1
        for j in range(i,n):
            nums[j] = 0
        

    """ 0674. 最长连续递增序列 #easy 找到数组中最长的严格递增序列 """
    def findLengthOfLCIS(self, nums: List[int]) -> int:
        start = 0; pre=inf; ans = 0
        for i,num in enumerate(nums+[-inf]):
            if num <= pre:
                ans = max(ans, i-start)
                start = i
            pre = num
        return ans
    """ 0080. 删除有序数组中的重复项 II #medium 将次数超过两次的多余数字删去 """
    def removeDuplicates(self, nums: List[int]) -> int:
        pre,cnt = None,0
        i = 0
        for num in nums:
            if num == pre:
                cnt += 1
            else:
                pre = num
                cnt = 1
            if cnt <= 2:
                nums[i] = num
                i += 1
        return i

    """ 0075. 颜色分类 #medium #题型
有3种颜色, 要求「原地」修改使得数组变为有序的状态.
进阶要求: 时间 O(n)
思路1: 定义「循环不变量」
    定义 [0...i] 范围内数字为0; [i+1...j] 为 1; [k...n-1] 为 2, 而 [j+1...k-1] 为未知.
    终止条件: 遍历的idx遇到k.
    注意: 实际上保障了 j=idx-1. 因此这里的j没有必要维护!
[这里](https://leetcode.cn/leetbook/read/sliding-window-and-two-pointers/rl7myd/) 对于 #循环不变量 讲的很好.
[官答](https://leetcode.cn/problems/sort-colors/solution/yan-se-fen-lei-by-leetcode-solution/)
"""
    def sortColors(self, nums: List[int]) -> None:
        i=-1; k=len(nums)
        idx = 0
        while idx<k:
            num = nums[idx]
            if num==0:
                i += 1
                # 1) 若直接赋值, 注意边界!
                # nums[i] = 0
                # if i!=idx:
                #     nums[idx] = 1
                # 2) 采用交换可以简化逻辑
                nums[i],nums[idx] = nums[idx],nums[i]
                idx += 1
            elif num==1:
                idx += 1
            else:
                k-=1
                nums[k], nums[idx] = nums[idx],nums[k]
        # for test
        return nums

    """ 0215. 数组中的第K个最大元素 #medium #题型 另见 [quick sort]
思路1: 采用类似 #快排 的思路, 每次选择 pivot 对于 [l,r] 区间进行分割. 也类似 #二分
    注意: 采用随机化策略选 pivot.
从 #循环不变量 的角度, 另见 [here](https://leetcode.cn/leetbook/read/sliding-window-and-two-pointers/rli5s3/)

"""
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # by copilot
        import random
        def partition(l,r):
            # 对于 [l,r] 区间, 随机选点作为pivot, 返回最后pivot所在位置
            # 1) 随机化 pivot
            idx = random.randint(l,r)
            nums[l],nums[idx] = nums[idx],nums[l]
            pivot = nums[l]
            # 2) 分割
            i = l+1
            for j in range(l+1,r+1):
                if nums[j] > pivot:
                    nums[i],nums[j] = nums[j],nums[i]
                    i += 1
            nums[l],nums[i-1] = nums[i-1],nums[l]
            return i-1
        # 3) 递归. 类似二分
        l,r = 0,len(nums)-1
        while l<=r:
            idx = partition(l,r)
            if idx == k-1:
                return nums[idx]
            elif idx > k-1:
                r = idx-1
            else:
                l = idx+1
        return -1
        
    """ ==================================== 类型 1 ==================================== """
    """ 0643. 子数组最大平均数 I #easy """
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        mx = s = sum(nums[:k])
        for i in range(k,len(nums)):
            s += nums[i]-nums[i-k]
            mx = max(mx,s)
        return mx/k
    
    """ 1052. 爱生气的书店老板 #medium """
    def maxSatisfied(self, customers: List[int], grumpy: List[int], minutes: int) -> int:
        n = len(customers)
        base = sum([customers[i] for i in range(n) if grumpy[i]==0])
        # 滑动窗口
        s = sum([customers[i] for i in range(minutes) if grumpy[i]==1])
        mx = s
        for i in range(minutes,n):
            s += customers[i]*grumpy[i] - customers[i-minutes]*grumpy[i-minutes]
            mx = max(mx,s)
        return base + mx



    """ ==================================== 类型 2 ==================================== """
    """ 0076. 最小覆盖子串 #hard #题型
给定字符串s和t, 要求s中长度最小的包含t中所有元素的子串. 限制: 长度 1e5
思路1: 滑动窗口仅需要检查当前窗口是否符合要求即可. 可以用一个 Counter 来记录
"""
    def minWindow(self, s: str, t: str) -> str:
        tgt = Counter(t)
        cnt = Counter()
        def check():
            return all(cnt[i]>=tgt[i] for i in tgt)
        n = len(s)
        # 滑动窗口直接 for r in range(n): 即可!!!
        l = 0
        ansLen = inf; ansL = 0
        for r in range(n):
            cnt[s[r]] += 1
            while check():
                if r-l+1 < ansLen:
                    ansLen = r-l+1; ansL = l
                cnt[s[l]] -= 1
                l += 1
        return s[ansL:ansL+ansLen] if ansLen!=inf else ""
    
    """ 0424. 替换后的最长重复字符 #medium 
对于一个字符串, 最多可以修改字符k次. 问经过这些操作后最长的连续相同字符长度. 限制: k<n 1e5.
思路1: 滑动窗口. 用一个 Counter 来记录当前窗口内的字符频率.
    如何判断所需的最少修改次数? 由于字符数量有限, 直接用最大值计算即可.
"""
    def characterReplacement(self, s: str, k: int) -> int:
        cnt = Counter()
        # mx = 0
        l = 0
        for r,ch in enumerate(s):
            cnt[ch] += 1
            # 技巧: 这里不用 while 循环. 因为我们之前已经长 r-l+1 的满足条件的区间了. 若不满足的话, 直接平移相同长度的区间即可.
            if r-l+1 - max(cnt.values()) > k:
                cnt[s[l]] -= 1
                l += 1
            # mx = max(mx, r-l+1)
        return r-l+1
    
    """ 2062. 统计字符串中的元音子字符串 #easy #题型
要求统计连续子序列的数量. 条件为: 1) 所有元素为元音字符 2) 包含所有aeiou五个元素.
思路1: #双指针. 在满足条件的情况下尽量移动左边界.
    技巧: #re 抽取所有仅由元音组成的子串, 对于每一个符合要求的子串, 双指针遍历.
    具体而言, 存储左右指针内包含的元音数量. 遍历有指针的过程中, 维护左指针使得「左右指针包含的包含所有元音的最短序列」, 这样, 以右指针结尾的包含左右元音的子串数量为 left+1.
"""
    def countVowelSubstrings(self, word: str) -> int:
        vowelSubs = re.findall(r'[aeiou]+', word)
        ans = 0
        ch2idx = {ch:i for i,ch in enumerate("aeiou")}
        for sub in vowelSubs:
            left = 0
            count = [0] * 5
            for ch in sub:
                count[ch2idx[ch]] += 1
                # 尽量移动左边界.
                while count[ch2idx[sub[left]]]>1:
                    count[ch2idx[sub[left]]] -= 1
                    left += 1
                if all(c>0 for c in count):
                    ans += left+1
        return ans
    


    """ ==================================== 类型 3 计数问题 ==================================== """
    """ 0340. 至多包含 K 个不同字符的最长子串 #medium #题型 给定一个字符串, 要求找到拥有最多k个不同字符的子串的最大长度
关联: 「159. 至多包含两个不同字符的最长子串」 #medium
"""
    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        cnt = Counter()
        l = 0
        ans = 0
        for r,ch in enumerate(s):
            cnt[ch] += 1
            while len(cnt)>k:
                cnt[s[l]] -= 1
                if cnt[s[l]]==0:
                    del cnt[s[l]]
                l += 1
            ans = max(ans, r-l+1)
        return ans
    
    """ 0795. 区间子数组个数 #medium 求数组中, 最大元素在 [l,r] 范围内的子数组数量
思路1: 显然, 子数组被超过 r 的元素分割. 如何求被分割区间中的数量?
    假设最大值要求2, 观察 [1,2,1,2,1] 有多少满足条件的子数组? 以l为左端点的数组分别有 4,4,2,2,0 个
    也即, 取决于 [l,r] 范围内的元素位置.
思路2: #分解. 考虑子问题「最大元素小于等于x的子数组数量」
"""
    def numSubarrayBoundedMax(self, nums: List[int], left: int, right: int) -> int:
        sidx = -1
        idxs = []
        ans = 0
        # 注意加 #哨兵
        for i,num in enumerate(nums + [right+1]):
            if num <= right:
                if sidx==-1: sidx = i
                if num >= left: idxs.append(i)
            # 分割
            else:
                for idx in idxs:
                    ans += (i-idx) * (idx-sidx+1)
                    sidx = idx+1
                # 重制
                sidx = -1; idxs = []
        return ans
    
    
    
    
    """ ==================================== 双指针：相向交替移动的两个变量 ==================================== """
    """ 0011. 盛最多水的容器 #medium #题型 从一组柱子中选两个, 构成的容积最大.
思路1: 采用 #双指针. 每次向内移动较短边.
    正确性? **假设 l 是较短边, 它已经构成了可能组成的容积的最大值**. 因为底边减小而高不可能增加.
"""
    def maxArea(self, height: List[int]) -> int:
        l,r = 0,len(height)-1
        mx = 0
        while l<r:
            mx = max(mx, (r-l)*min(height[l],height[r]))
            if height[l] < height[r]: l+=1
            else: r-=1
        return mx
    
    """ 0167. 两数之和 II - 输入有序数组 #medium 给定一有序数组, 判断其中两个数字之和是否可以达到目标
思路1: #双指针 根据当前值和目标的大小进行移动. 正确性: 相当于缩减了搜索空间.
"""
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        l,r = 0,len(numbers)-1
        while l<r:
            s = numbers[l] + numbers[r]
            if s == target: return [l+1,r+1]
            elif s < target: l+=1
            else: r-=1
    
    """ 0015. 三数之和 #medium #题型 给定一个数组, 找到所有「不重复的」三个数之和为0的组合. 限制: 数组长度 3000
思路1: 排序后, 转化为「两数之和」.
    最一般的思路是什么? 三种循环.
    先固定一个值, 问题等价「找到和为 -a 的两数」, 显然可以 #双指针.
    如何避免重复? 判断是否和上个值相同.
"""
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        ans = []
        n = len(nums)
        for i in range(n):
            if i>0 and nums[i]==nums[i-1]: continue # 避免重复
            a = nums[i]
            l,r = i+1,n-1
            while l<r:
                s = nums[l]+nums[r]
                if s == -a:
                    ans.append([a,nums[l],nums[r]])
                    l+=1
                    # 避免重复
                    while l<r and nums[l]==nums[l-1]: l+=1
                elif s < -a: l+=1
                else: r-=1
        return ans
    
    """ 0016. 最接近的三数之和 #medium #题型 给定一个数组, 找到三个数之和最接近目标值. 限制: 数组长度 1000. """
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()
        n = len(nums)
        ans = inf
        for i in range(n):
            if i>0 and nums[i]==nums[i-1]: continue # 避免重复
            l,r = i+1,n-1
            while l<r:
                s = nums[l] + nums[r]
                if abs(target-s-nums[i]) < abs(target-ans):
                    ans = s + nums[i]
                if s < target-nums[i]: l+=1
                else: r -= 1
        return ans
    
    """ 0018. 四数之和 #medium 给定一个数组, 找到所有「不重复」的四个数字之和为目标的组合. 限制: 数组长度 200
类似 0015, 不过外面套两层循环. 内部还是 #双指针.
"""
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        n = len(nums)
        ans = []
        for i in range(n):
            if i>0 and nums[i]==nums[i-1]: continue # 避免重复
            for j in range(i+1,n):
                if j>i+1 and nums[j]==nums[j-1]: continue # 这里也要去重
                # 
                l,r = j+1,n-1
                while l<r:
                    s = nums[l]+nums[r]+nums[i]+nums[j]
                    if s==target:
                        ans.append([nums[i],nums[j],nums[l],nums[r]])
                        l+=1
                        while l<r and nums[l]==nums[l-1]: l+=1
                    elif s>target: r-=1
                    else: l+=1
        return ans
                    
    
    
    """ 0125. 验证回文串 #easy 忽略非数字字母字符, 判断是否回文. """
    def isPalindrome(self, s: str) -> bool:
        l,r = 0,len(s)-1
        while l<r:
            # while l<r and not s[l].isalnum(): l+=1
            # while l<r and not s[r].isalnum(): r-=1
            if not s[l].isalnum(): l+=1; continue
            if not s[r].isalnum(): r-=1; continue
            if s[l].lower() != s[r].lower(): return False
            l,r = l+1,r-1
        return True
    
    """ 0042. 接雨水 #hard #题型 给定一组柱子, 求下雨之后能接多少水. 限制: n 2e4
思路1: 双指针. 维护左右的最大值, 每次更新 **最大值较小**的那一侧.
"""
    def trap(self, height: List[int]) -> int:
        l,r = 0,len(height)-1
        lmax,rmax = height[l],height[r]
        ans = 0
        while l<r:
            if lmax<rmax:
                l+=1
                if height[l]<lmax: ans += lmax-height[l]
                else: lmax = height[l]
            else:
                r-=1
                if height[r]<rmax: ans += rmax-height[r]
                else: rmax = height[r]
        return ans


    """ 0658. 找到 K 个最接近的元素 #medium 给定一个有序数组, 返回其中最接近x的k个数字 (距离相同取idx较小的).
思路1: 双指针收缩, 直到长度为k.
"""
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        l,r = 0,len(arr)-1
        while r-l+1>k:
            # 相同时, l优先.
            if abs(arr[l]-x) > abs(arr[r]-x): l+=1
            else: r-=1
        return arr[l:r+1]


    """ 0259. 较小的三数之和 #medium 给定一个数组, 计算 i,j,k 之和 <target 的三元组数量"""
    def threeSumSmaller(self, nums: List[int], target: int) -> int:
        nums.sort()
        n = len(nums)
        ans = 0
        for i in range(n):
            l,r = i+1,n-1
            while l<r:
                s = nums[i]+nums[l]+nums[r]
                if s < target:
                    ans += r-l
                    l+=1
                else: r-=1
        return ans  

    """ 0360. 有序转化数组 #medium 给定一数组, 对 其中每一个元素计算 f(x) = ax^2+bx+c, 对于结果排序
进阶要求是在 O(n) 时间内完成.
思路1: 根据二次函数的性质, 函数值大小与距离轴 -b/2a 的距离相关. 因此可以用双指针收缩. 注意边界 a=0 时退化.
"""
    def sortTransformedArray(self, nums: List[int], a: int, b: int, c: int) -> List[int]:
        def f(x):
            return a*x**2+b*x+c
        n = len(nums)
        ans = []
        if a==0:
            for i in range(n):
                ans.append(f(nums[i]))
            if b<0: ans.reverse()
            return ans
        # a!=0
        mid = -b/(2*a)
        l,r = 0,n-1
        while l<=r:
            if abs(nums[l]-mid) < abs(nums[r]-mid):
                ans.append(f(nums[r]))
                r-=1
            else:
                ans.append(f(nums[l]))
                l+=1
        if a>0: ans.reverse()
        return ans
    """ 0977. 有序数组的平方 #easy 给定一个有序数组, 返回平方后的有序数组. """
    def sortedSquares(self, nums: List[int]) -> List[int]:
        l,r = 0,len(nums)-1
        ans = []
        while l<=r:
            if abs(nums[l]) > abs(nums[r]): ans.append(nums[l]**2);l += 1
            else: ans.append(nums[r]**2); r -= 1
        return ans[::-1]


    """ 0844. 比较含退格的字符串 #medium 给定两个字符串, 定义 # 为特殊字符表示退格, 判断两字符串是否相等.
进阶要求: 空间 O(1)
思路1: 考虑「退格」的性质, 从后往前 #逆序 模拟; 双指针.
[official](https://leetcode.cn/problems/backspace-string-compare/solution/bi-jiao-han-tui-ge-de-zi-fu-chuan-by-leetcode-solu/)
"""
    def backspaceCompare(self, s: str, t: str) -> bool:
        i,j = len(s)-1,len(t)-1
        cnts, cntt = 0,0
        while i>=0 or j>=0:
            if i>=0 and s[i]=='#': i-=1; cnts+=1; continue
            if j>=0 and t[j]=='#': j-=1; cntt+=1; continue
            if i>=0 and cnts>0: i-=1; cnts-=1; continue
            if j>=0 and cntt>0: j-=1; cntt-=1; continue
            if i<0 or j<0: return False
            if s[i]!=t[j]: return False
            i,j = i-1,j-1
        return True


    """ 0845. 数组中的最长山脉 #medium 定义「山脉」为上升下降的序列, 返回数组中最长的山脉长度.
思路1: 遍历右端, 通过 #flag 标记当前是否满足条件 (并记录左端点). 但要考虑的 #细节 比较多. 其实也就是下面的 #双指针, 官答更清楚
思路2: 官答的双指针思路更清楚 [official](https://leetcode.cn/problems/longest-mountain-in-array/solution/shu-zu-zhong-de-zui-chang-shan-mai-by-leetcode-sol/)
关联: 「1095. 山脉数组中查找目标值」
"""
    def longestMountain(self, arr: List[int]) -> int:
        flag = False  # 遇到下降点时, 是否可以构成山脉 (需要之前有过上升)
        isInc = False # 前一点是否上升
        start = None  # 当前山脉的起点 
        ans = 0
        for i in range(1, len(arr)):
            if arr[i] > arr[i-1]:
                if not isInc:
                    isInc = True; start = i-1
                    flag = True
            elif arr[i] < arr[i-1]:
                isInc = False
                if flag: ans = max(ans, i-start+1)
            else: flag = False; isInc = False
        return ans

    """ 0881. 救生艇 #medium  """
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        people.sort()
        l,r = 0,len(people)-1
        ans = 0
        while l<=r:
            if people[l]+people[r]<=limit: l+=1
            r-=1
            ans+=1
        return ans
    
    """ 0925. 长按键入 #easy """
    def isLongPressedName(self, name: str, typed: str) -> bool:
        m,n = len(name),len(typed)
        i,j = 0,0
        while i<m and j<n:
            if name[i]==typed[j]: i+=1; j+=1
            elif j>0 and typed[j]==typed[j-1]: j+=1
            else: return False
        if i<m: return False
        for k in range(j,n):
            if typed[k]!=typed[k-1]: return False
        return True
    
    """ 1099. 小于 K 的两数之和 #easy 复杂度 O(n logn) """
    def twoSumLessThanK(self, nums: List[int], k: int) -> int:
        nums.sort()
        r = len(nums)-1
        ans = -1
        for l,num in enumerate(nums):
            while r>=0 and num + nums[r] >= k: r-=1
            if r<=l: break
            ans = max(ans, num+nums[r])
        return ans
    
    """ 1229. 安排会议日程 #medium 给定两组区间表示两人的空闲时间, 找到重叠最早的至少为 duration 的时间段. """
    def minAvailableDuration(self, slots1: List[List[int]], slots2: List[List[int]], duration: int) -> List[int]:
        slots1.sort(); slots2.sort()
        m,n = len(slots1),len(slots2)
        i,j = 0,0
        while i<m and j<n:
            if slots1[i][0]>slots2[j][1]: j+=1
            elif slots1[i][1]<slots2[j][0]: i+=1
            else:
                start = max(slots1[i][0], slots2[j][0])
                end = min(slots1[i][1], slots2[j][1])
                if end-start>=duration: return [start, start+duration]
                if slots1[i][1]<slots2[j][1]: i+=1
                else: j+=1
        return []
    
sol = Solution()
result = [
    # sol.minWindow(s = "ADOBECODEBANC", t = "ABC"),
    # sol.minWindow(s = "a", t = "a"),
    # sol.minWindow(s = "a", t = "aa"),
    # sol.findLengthOfLCIS([2,2,2]),
    # sol.findLengthOfLCIS([1,3,5,4,7]),
    # sol.sortColors(nums = [2,0,2,1,1,0]),
    # sol.maxSatisfied(customers = [1,0,1,2,1,1,7,5], grumpy = [0,1,0,1,0,1,0,1], minutes = 3),
    # sol.characterReplacement(s = "ABAB", k = 2),
    # sol.threeSum(nums = [-1,0,1,2,-1,-1,-4])
    # sol.threeSumClosest(nums = [-1,2,1,-4], target = 1)
    # sol.fourSum([2,2,2,2], 8)
    # sol.isPalindrome("A man, a plan, a canal: Panama"),
    # sol.backspaceCompare(s = "ab#c", t = "ad#c"),
    # sol.backspaceCompare(s = "ab##", t = "c#d#")
    # sol.longestMountain(arr = [2,1,4,7,3,2,5]),
    # sol.longestMountain([2,2,2])
    # sol.twoSumLessThanK([34,23,1,24,75,33,54,8], 60),
    sol.numSubarrayBoundedMax(nums = [2,1,4,3], left = 2, right = 3),
    sol.numSubarrayBoundedMax(nums = [2,9,2,5,6], left = 2, right = 8),
]
for r in result:
    print(r)
