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
[滑动窗口和双指针](https://leetcode.cn/leetbook/detail/sliding-window-and-two-pointers/) #star 就是题量太大了.

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
0995. K 连续位的最小翻转次数 #hard #题型 #star 给定一个01数组, 每次可以对长度为k的子数组进行翻转. 问最少需要多少次可以得到全1的数组? 限制: 1e5
    提示: 由于每一位都要变为1, 因此翻转的顺序不重要. 也即, 我们从左到右遍历, 尽可能保证左边部分符合条件即可.
    思路1: #差分数组 来记录翻转的区间.
0727. 最小窗口子序列 #hard #题型 #star 给定字符串s,t, 要求找到s中最小的子串, 使得t是该子串的子序列. 限制 s的长度 n 2e4 t的长度 k 100
    思路3: #滑动窗口 #star. 我们从每一个位置出发, 尝试正向匹配t, 若在位置right匹配成功了, 则反向再匹配一次, 得到最小的窗口.


== 类型3: 计数问题
0340. 至多包含 K 个不同字符的最长子串 #medium #题型 给定一个字符串, 要求找到拥有最多k个不同字符的子串的最大长度
    关联: 「159. 至多包含两个不同字符的最长子串」 #medium
0795. 区间子数组个数 #medium 求数组中, 最大元素在 [l,r] 范围内的子数组数量
    思路2: #分解. 考虑子问题「最大元素小于等于x的子数组数量」
0992. K 个不同整数的子数组 #hard #题型
    对于一个数字, 给定数字k, 统计所有子数组中, 「刚好包含k个不同数字」的子数组数量. 限制: 2e4
    思路1: #滑动窗口. 维护「两个窗口」, 从而实现区间的计数.
    思路2: 问题 #转化 为「求最多包含k个不同数字的子数组数量」, 再减去「最多包含k-1个不同数字的子数组数量」
0713. 乘积小于 K 的子数组 #medium
0904. 水果成篮 #medium 
1358. 包含所有三种字符的子字符串数目 #medium 
0467. 环绕字符串中唯一的子字符串 #medium #题型 #star
    「环绕字符串」是指 zabc, a 这种形式的, 给定一个字符串, 问其中有多少个「唯一的环绕子字符串」. 限制: n 1e5
    提示: 关键是如何去重? 一种思路是, 统计以ch结尾的环绕子串的最大长度.
    思路1: #DP 以 `dp[ch]` 表示在前i个字符中, 以ch结尾的最长环绕字符串.
0719. 找出第 K 小的数对距离 #hard #题型 #二分
    给定一个数组, 每个数对构成「绝对差值」. 问第k小的差值. 限制: 长度 n 1e4. 数字大小 C 1e6.  
    见 [二分] 这里要得到所有的差值复杂度过高, 显然需要二分. 
    那么为什么会想到 #滑动窗口? 对于排序的数组, 进行计数的一个通用方法就是双指针.

== 类型4: 使用数据结构维护窗口性质
0239. 滑动窗口最大值 #hard #题型 对长n的数组进行宽k的滑窗, 问过程中每一个位置中窗口最大值. 限制: n 1e5, k 1e5
    思路1: 采用 #优先队列 记录当前状态下的最大值. 并通过时间戳来防止超长. 复杂度 O(n logk)
    思路2: #单调队列
0480. 滑动窗口中位数 #hard #题型 #hardhard 对长n的数组进行宽k的滑窗, 问过程中每一个位置中窗口中位数. 限制: n 1e5, k 1e5
    关联: 「0295. 数据流的中位数」
    思路1: 双 #优先队列 + #延迟删除
    类似 0295. 数据流的中位数, 也是用两个「平衡」的优先队列, 来维护较小和较大的一半数据. 但下面的 #细节 非常多.
0220. 存在重复元素 III #medium #题型
    给定一个数组, 要求判断是否有一个下标对 (i,j), 满足间距 <=k, 两者的值相差 <=t. 限制: 数组长度 2e4
0683. K 个关闭的灯泡 #hard #题型  有 n 个顺序排列的灯泡按照一定次序打开, 问哪一天恰好有 k 个连续的关闭灯泡, 两侧为打开的灯泡.
    思路1: 暴力用 #有序集合 O(n logn)
    思路2: #滑动窗口 + 维护最小值.
1438. 绝对差不超过限制的最长连续子数组 #medium #题型 找最长的子数组, 其中的任意两元素绝对差不超过limit 限制: 1e5
    思路1: #有序集合 暴力 复杂度 O(n logn)
    思路2: 本质上就是维护 #滑动窗口 范围内的最大值和最小值! 因此可以用 #单调队列 分别维护递增和递减的序列. 复杂度 O(n)
    关联: 0239. 滑动窗口最大值


== 链表中双指针技巧 见 [链表]
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
    
    """ 0995. K 连续位的最小翻转次数 #hard #题型 #star 给定一个01数组, 每次可以对长度为k的子数组进行翻转. 问最少需要多少次可以得到全1的数组? 限制: 1e5
提示: 由于每一位都要变为1, 因此翻转的顺序不重要. 也即, 我们从左到右遍历, 尽可能保证左边部分符合条件即可.
思路1: #差分数组 来记录翻转的区间.
    从左往右遍历, 我们需要统计「每一位被翻转的次数」. 但每次翻转的是一个区间, 所以关键是如何记录每次翻转k的范围? 答案是用差分数组
    复杂度: O(n)
思路2: #滑动窗口 , 简化了空间开销
    上面的空间开销是 O(n), 能否优化到 O(1)? 实际上, 我们在遍历过程中维护acc, 只需要记录翻转区间的结束位置即可.
    一个小技巧是, 对于翻转开始位 +x 来标记翻转, 当遍历idx位时, 若 nums[idx-k] >=k 说明翻转区间结束.
[official](https://leetcode.cn/problems/minimum-number-of-k-consecutive-bit-flips/solution/k-lian-xu-wei-de-zui-xiao-fan-zhuan-ci-s-bikk/)
"""
    def minKBitFlips(self, nums: List[int], k: int) -> int:
        # 思路1: #差分数组 来记录翻转的区间.
        n = len(nums)
        diff = [0] * (n+1)      # 差分数组
        acc = 0 # 当前遍历位的翻转次数
        cnt = 0 # 累计翻转次数
        for i in range(n-k+1):
            acc += diff[i]
            if (nums[i]+acc) & 1 == 0:
                acc += 1; diff[i+k] -= 1 # diff[i] += 1; 
                cnt += 1
        # 检查是否可行
        for i in range(n-k+1,n):
            acc += diff[i]
            if (nums[i]+acc) & 1 == 0: return -1
        return cnt
    def minKBitFlips(self, nums: List[int], k: int) -> int:
        # 思路2: #滑动窗口 , 简化了空间开销
        n = len(nums)
        acc = cnt = 0
        # 统一了上面的两次for
        for i in range(n):
            # 检查是否翻转区间结束. 也可以 nums[i-k]-=2 对于原数组复原
            if i >= k and nums[i-k] >= 2: acc -= 1
            if (nums[i]+acc) & 1 == 0:
                if i+k > n: return -1
                acc += 1; nums[i] += 2
                cnt += 1
        return cnt

    """ 0727. 最小窗口子序列 #hard #题型 #star 给定字符串s,t, 要求找到s中最小的子串, 使得t是该子串的子序列. 限制 s的长度 n 2e4 t的长度 k 100
思路1: #DP (前缀递推)
思路3: #滑动窗口 #star. 我们从每一个位置出发, 尝试正向匹配t, 若在位置right匹配成功了, 则反向再匹配一次, 得到最小的窗口.
    复杂度: 虽然看上去有「浪费」, 但注意这里复杂度仍然是 `O(n * k)`! 实际测试下来反而是最优的!
    see [here](https://leetcode.cn/problems/minimum-window-subsequence/solution/itcharge-727-zui-xiao-chuang-kou-zi-xu-l-v3az/)
 """
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

    """ 1100. 长度为 K 的无重复字符子串 #medium """
    def numKLenSubstrNoRepeats(self, s: str, k: int) -> int:
        cnt = Counter(s[:k])
        ans = len(cnt)==k
        for i in range(k,len(s)):
            cnt[s[i]] += 1
            cnt[s[i-k]] -= 1
            if cnt[s[i-k]]==0: del cnt[s[i-k]]
            if len(cnt)==k: ans += 1
        return int(ans)
    """ 1151. 最少交换次数来组合所有的 1 #medium """
    def minSwaps(self, data: List[int]) -> int:
        c = sum(data)
        cnt = sum(data[:c])
        mx = cnt
        for i in range(c, len(data)):
            cnt += data[i]-data[i-c]
            mx = max(mx, cnt)
        return c - mx
    """ 1176. 健身计划评估 #easy """
    def dietPlanPerformance(self, calories: List[int], k: int, lower: int, upper: int) -> int:
        s = sum(calories[:k])
        ans = 0
        calories.append(0)
        for i in range(k, len(calories)):
            if s>upper: ans +=1
            elif s<lower: ans -=1
            s += calories[i]-calories[i-k]
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
    
    """ 0992. K 个不同整数的子数组 #hard #题型
对于一个数字, 给定数字k, 统计所有子数组中, 「刚好包含k个不同数字」的子数组数量. 限制: 2e4
思路1: #滑动窗口. 维护「两个窗口」, 从而实现区间的计数.
    对于同样的右边界r, 满足条件的左边界形成一个区间 [l1,l2], 因此需要用两个指针维护这个区间. 计数.
思路2: 问题 #转化 为「求最多包含k个不同数字的子数组数量」, 再减去「最多包含k-1个不同数字的子数组数量」
"""
    def subarraysWithKDistinct(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = 0
        cnt1,cnt2 = Counter(),Counter()
        # 注意两个指针的定义. l1 是符合条件的左边界, l2是第一个不符合条件的边界.
        l1 = l2 = 0
        for r in range(n):
            cnt1[nums[r]] += 1
            cnt2[nums[r]] += 1
            while len(cnt2)>=k:
                cnt2[nums[l2]] -= 1
                if cnt2[nums[l2]]==0: del cnt2[nums[l2]]
                l2 += 1
            while len(cnt1)>k:
                cnt1[nums[l1]] -= 1
                if cnt1[nums[l1]]==0: del cnt1[nums[l1]]
                l1 += 1
            # 加if判断初始情况.
            if len(cnt1)==k: ans += l2-l1
        return ans
    
    """ 0713. 乘积小于 K 的子数组 #medium """
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        mul = 1
        l = 0
        ans = 0
        for r,num in enumerate(nums):
            mul *= num
            while l<=r and mul>= k:
                mul //= nums[l]
                l += 1
            ans += r-l+1
        return ans
    """ 0904. 水果成篮 #medium """
    def totalFruit(self, fruits: List[int]) -> int:
        mx = 0
        cnt = Counter()
        l = 0
        for r,f in enumerate(fruits):
            cnt[f] += 1
            while len(cnt) > 2:
                cnt[fruits[l]]-=1
                if cnt[fruits[l]]==0: del cnt[fruits[l]]
                l+=1
            mx = max(mx, r-l+1)
        return mx
    """ 1358. 包含所有三种字符的子字符串数目 #medium """
    def numberOfSubstrings(self, s: str) -> int:
        ans = 0; n = len(s)
        cnt = Counter()
        l = 0
        for r,ch in enumerate(s):
            cnt[s[r]] += 1
            while len(cnt)==3 and all(i>0 for i in cnt.values()):
                cnt[s[l]]-=1; l+=1
            ans += l
        return ans
    
    """ 0467. 环绕字符串中唯一的子字符串 #medium #题型 #star
「环绕字符串」是指 zabc, a 这种形式的, 给定一个字符串, 问其中有多少个「唯一的环绕子字符串」. 限制: n 1e5
提示: 关键是如何去重? 一种思路是, 统计以ch结尾的环绕子串的最大长度.
思路1: #DP 以 `dp[ch]` 表示在前i个字符中, 以ch结尾的最长环绕字符串.
    在遍历过程中, 维护当前符合条件的环绕串长度. 
    e.g. 此前的环绕串长k, 对于第i的字符ch 满足 s[i-1]邻接s[i], 则更新 `dp[ch] = max{ dp[ch], k+1 }`
    [官答](https://leetcode.cn/problems/unique-substrings-in-wraparound-string/solution/huan-rao-zi-fu-chuan-zhong-wei-yi-de-zi-ndvea/)
为何是 #滑动窗口? 是一个比较特殊的变体. 参见 [here总结](https://leetcode.cn/problems/unique-substrings-in-wraparound-string/solution/xi-fa-dai-ni-xue-suan-fa-yi-ci-gao-ding-qian-zhui-/)
"""
    def findSubstringInWraproundString(self, p: str) -> int:
        # 思路1: #DP 以 `dp[ch]` 表示在前i个字符中, 以ch结尾的最长环绕字符串.
        dp = defaultdict(int)
        k = 0
        for i,ch in enumerate(p):
            # if i>0 and (ch=='a' and p[i-1]=='z' or ord(ch)-ord(p[i-1])==1):
            # 技巧: 可以用%来简化逻辑.
            if i>0 and (ord(ch)-ord(p[i-1])) % 26 == 1:
                k += 1
            else: k = 1
            dp[ch] = max(dp[ch], k)
        return sum(dp.values())
    
    """ 0719. 找出第 K 小的数对距离 #hard #题型 #二分
给定一个数组, 每个数对构成「绝对差值」. 问第k小的差值. 限制: 长度 n 1e4. 数字大小 C 1e6.  
见 [二分] 这里要得到所有的差值复杂度过高, 显然需要二分. 
那么为什么会想到 #滑动窗口? 对于排序的数组, 进行计数的一个通用方法就是双指针.
"""


    """ ==================================== 类型 4 使用数据结构维护窗口性质 ==================================== """
    """ 0239. 滑动窗口最大值 #hard #题型 对长n的数组进行宽k的滑窗, 问过程中每一个位置中窗口最大值. 限制: n 1e5, k 1e5
思路1: 采用 #优先队列 记录当前状态下的最大值. 并通过时间戳来防止超长. 复杂度 O(n logk)
思路2: #单调队列
    优化思想: 假如滑窗内有 i<j 并且 nums[i]<=nums[j], 那么 nums[i] 一定不会是滑窗的最大值.
    因此, 在遍历过程中, 维护「在窗口内的并且单调递减的队列」, 那么队首元素就是当前窗口的最大值.
    注意, 这个DS要实现尾部添加和头部/尾部删除, 并且要维护单调性, 因此是「单调队列」.
    复杂度: O(n)
思路3: 对于nums按照长度k进行分组, 讨论. #拓展
    类似 #稀疏表（Sparse Table）
[官答](https://leetcode.cn/problems/sliding-window-maximum/solution/hua-dong-chuang-kou-zui-da-zhi-by-leetco-ki6m/)
"""
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # 思路1: 采用 #优先队列 记录当前状态下的最大值. 并通过时间戳来防止超长. 复杂度 O(n logk)
        q = [(-num,i) for i,num in enumerate(nums[:k-1])]
        heapify(q)
        ans = []
        for i in range(k-1, len(nums)):
            heappush(q, (-nums[i], i))
            while q[0][1] <= i-k: heappop(q)
            ans.append(-q[0][0])
        return ans
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # 思路2: #单调队列
        q = deque()
        for i in range(k-1): # 先填满窗口的前k-1个元素
            while q and nums[q[-1] ]<= nums[i]: q.pop()
            q.append(i)
        ans = []
        for i in range(k-1, len(nums)):
            while q and nums[q[-1]] <= nums[i]: q.pop()
            q.append(i)
            # 由于i始终会append, 因此不会 空.
            while q[0] <= i-k: q.popleft()
            ans.append(nums[q[0]])
        return ans
    
    """ 0480. 滑动窗口中位数 #hard #题型 #hardhard 对长n的数组进行宽k的滑窗, 问过程中每一个位置中窗口中位数. 限制: n 1e5, k 1e5
关联: 「0295. 数据流的中位数」
思路1: 双 #优先队列 + #延迟删除
    类似 0295. 数据流的中位数, 也是用两个「平衡」的优先队列, 来维护较小和较大的一半数据. 但下面的 #细节 非常多.
    我们直接用数据结构的思想来考虑, 对于要实现的 `DualHeap` 需要哪些操作?
        插入操作 `insert`, 类似 0295. 插入后需要维护平衡.
        维护平衡 `makeBalance`. 当某一个堆的长度超了, 将一个「有效数据」转移到另一个堆中.
        最重要的是删除操作 `erase`. 堆的一个问题是无法删除非堆顶元素. 
            因此我们需要 #延迟删除 的机制. 用一个 `delayed` 记录待删除的元素.
            何时删除? 由于我们关心的仅仅是堆顶元素 (需要保证其有效性). 因此只有当堆顶元素被弹出, 才需要触发删除操作.
        这里的 erase,makeBalance 都涉及删除操作, 因此可以用一个 `prune` 函数复用, 作用是「不断地弹出 heap 的堆顶无效元素」
        细节: 因为堆中可能保存了延迟删除的数据, 需要用两个计数器来记录当前堆中的有效数据量.
[official](https://leetcode.cn/problems/sliding-window-median/solution/hua-dong-chuang-kou-zhong-wei-shu-by-lee-7ai6/)
"""
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        # 仔细看下面的 DualHeap 实现!!!
        dh = DualHeap(k)
        for num in nums[:k]:
            dh.insert(num)
        
        ans = [dh.getMedian()]
        for i in range(k, len(nums)):
            dh.insert(nums[i])
            dh.erase(nums[i - k])
            ans.append(dh.getMedian())
        
        return ans
    
    
    """ 0220. 存在重复元素 III #medium #题型
给定一个数组, 要求判断是否有一个下标对 (i,j), 满足间距 <=k, 两者的值相差 <=t. 限制: 数组长度 2e4
思路1: 维护长度为 k+1 的 #滑动窗口. 每次需要插入删除元素, 并且需要得到插入元素临近的两个元素大小. 可以用 #有序列表, 复杂度 `O(n logk)`
"""
    
    
    """ 0683. K 个关闭的灯泡 #hard #题型  有 n 个顺序排列的灯泡按照一定次序打开, 问哪一天恰好有 k 个连续的关闭灯泡, 两侧为打开的灯泡.
限制: n 2e4
思路1: 暴力用 #有序集合 O(n logn)
思路2: #滑动窗口 + 维护最小值.
    上面是是以「开灯的时间顺序」视角; 还可以根据「每个灯的打开时间」来看.
    注意到, 条件等价于, r=l+k+1, 并且 [l+1...l+k] 这k个灯的打开时间都比两者晚!
    因此, 可以维护一个长k+1 的滑窗. 在遍历过程中记录滑窗内的最小值 (于边界比较)
        具体而言, 滑窗的跳转逻辑可以进行简化: 每次检查 [l+1...l+k] 区间的元素即可. 更新l到第一个不满足的位置.
    复杂度: 每个位置最多被访问两次, 因此 O(n)
    图示见 [here](https://leetcode.cn/problems/k-empty-slots/solution/k-ge-kong-hua-pen-by-beney-2-22uh/)
"""
    def kEmptySlots(self, bulbs: List[int], k: int) -> int:
        from sortedcontainers import SortedList
        sl = SortedList()
        for i,b in enumerate(bulbs):
            idx = sl.bisect_right(b)
            if idx>0 and b - sl[idx-1] == k+1: return i+1
            if idx<len(sl) and sl[idx] - b == k+1: return i+1
            sl.add(b)
        return -1
    def kEmptySlots(self, bulbs, k):
        # 思路2: #滑动窗口 + 维护最小值.
        # 得到每个位置的灯的点亮时间.
        days = [0] * len(bulbs)
        for day, position in enumerate(bulbs, 1):
            days[position - 1] = day

        ans = float('inf')
        left, right = 0, k+1
        while right < len(days):
            # 检查当前范围是否满足条件
            for i in range(left + 1, right):
                if days[i] < days[left] or days[i] < days[right]:
                    left, right = i, i+k+1
                    break
            # 满足条件. 注意到可以直接右移k个单位! 因为中间部分显然不满足条件.
            else:
                ans = min(ans, max(days[left], days[right]))
                left, right = right, right+k+1

        return ans if ans < float('inf') else -1

    """ 1438. 绝对差不超过限制的最长连续子数组 #medium #题型 找最长的子数组, 其中的任意两元素绝对差不超过limit 限制: 1e5
思路1: #有序集合 暴力 复杂度 O(n logn)
思路2: 本质上就是维护 #滑动窗口 范围内的最大值和最小值! 因此可以用 #单调队列 分别维护递增和递减的序列. 复杂度 O(n)
    关联: 0239. 滑动窗口最大值
    回顾: 为什么可以单调性? 例如要求最大值, 若 i<j 有 nums[i]<nums[j], 则 nums[i] 一定不会是滑窗最大值, 维护递减序列即可.
[official](https://leetcode.cn/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/solution/jue-dui-chai-bu-chao-guo-xian-zhi-de-zui-5bki/)
"""
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        # 思路1: #有序集合 暴力 复杂度 O(n logn)
        s = SortedList()
        n = len(nums)
        left = right = ret = 0
        while right < n:
            s.add(nums[right])
            while s[-1] - s[0] > limit:
                s.remove(nums[left])
                left += 1
            ret = max(ret, right - left + 1)
            right += 1
        return ret
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        n = len(nums)
        # 单调队列
        queMax, queMin = deque(), deque()
        left = right = ret = 0

        while right < n:
            # 维护两个队列的单调性
            # 不同于 0239题中的实现, 这里由于实现不太一样, 只能是 < 而不能 <=! 其实用上面的思路更清晰.
            while queMax and queMax[-1] < nums[right]:
                queMax.pop()
            while queMin and queMin[-1] > nums[right]:
                queMin.pop()
            queMax.append(nums[right])
            queMin.append(nums[right])
            # 检查是否满足条件
            while queMax and queMin and queMax[0] - queMin[0] > limit:
                if nums[left] == queMin[0]:
                    queMin.popleft()
                if nums[left] == queMax[0]:
                    queMax.popleft()
                left += 1
            
            ret = max(ret, right - left + 1)
            right += 1
        
        return ret

    
    
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


class DualHeap:
    def __init__(self, k: int):
        # 大根堆，维护较小的一半元素，注意 python 没有大根堆，需要将所有元素取相反数并使用小根堆
        self.small = list()
        # 小根堆，维护较大的一半元素
        self.large = list()
        # 哈希表，记录「延迟删除」的元素，key 为元素，value 为需要删除的次数
        self.delayed = collections.Counter()

        self.k = k
        # small 和 large 当前包含的元素个数，需要扣除被「延迟删除」的元素
        self.smallSize = 0
        self.largeSize = 0


    # 不断地弹出 heap 的堆顶元素，并且更新哈希表
    def prune(self, heap: List[int]):
        while heap:
            num = heap[0]
            if heap is self.small:
                num = -num
            if num in self.delayed:
                self.delayed[num] -= 1
                if self.delayed[num] == 0:
                    self.delayed.pop(num)
                heapq.heappop(heap)
            else:
                break
    
    # 调整 small 和 large 中的元素个数，使得二者的元素个数满足要求
    def makeBalance(self):
        if self.smallSize > self.largeSize + 1:
            # small 比 large 元素多 2 个
            heapq.heappush(self.large, -self.small[0])
            heapq.heappop(self.small)
            self.smallSize -= 1
            self.largeSize += 1
            # small 堆顶元素被移除，需要进行 prune
            self.prune(self.small)
        elif self.smallSize < self.largeSize:
            # large 比 small 元素多 1 个
            heapq.heappush(self.small, -self.large[0])
            heapq.heappop(self.large)
            self.smallSize += 1
            self.largeSize -= 1
            # large 堆顶元素被移除，需要进行 prune
            self.prune(self.large)

    def insert(self, num: int):
        if not self.small or num <= -self.small[0]:
            heapq.heappush(self.small, -num)
            self.smallSize += 1
        else:
            heapq.heappush(self.large, num)
            self.largeSize += 1
        self.makeBalance()

    def erase(self, num: int):
        self.delayed[num] += 1
        if num <= -self.small[0]:
            self.smallSize -= 1
            if num == -self.small[0]:
                self.prune(self.small)
        else:
            self.largeSize -= 1
            if num == self.large[0]:
                self.prune(self.large)
        self.makeBalance()

    def getMedian(self) -> float:
        return float(-self.small[0]) if self.k % 2 == 1 else (-self.small[0] + self.large[0]) / 2



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
    # sol.numSubarrayBoundedMax(nums = [2,1,4,3], left = 2, right = 3),
    # sol.numSubarrayBoundedMax(nums = [2,9,2,5,6], left = 2, right = 8),
    # sol.subarraysWithKDistinct(nums = [1,2,1,2,3], k = 2),
    # sol.subarraysWithKDistinct(nums = [1,2,1,3,4], k = 3),
    # sol.findSubstringInWraproundString('zab'),
    # sol.maxSlidingWindow(nums = [1,3,-1,-3,5,3,6,7], k = 3),
    # sol.kEmptySlots(bulbs = [1,3,2], k = 1),
    # sol.kEmptySlots(bulbs = [1,2,3], k = 1),
    # sol.minKBitFlips(nums = [0,1,0], k = 1),
    # sol.minKBitFlips(nums = [0,0,0,1,0,1,1,0], k = 3),
    sol.minWindow(S = "abcdebdde", T = "bde"),
]
for r in result:
    print(r)
