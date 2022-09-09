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
[排序](https://leetcode.cn/leetbook/detail/sort-algorithms/) #star ⭐️

======= O(n^2)
下面三种排序方法的 [总结与比较](https://leetcode.cn/leetbook/read/sort-algorithms/oz4nzd/)
== 冒泡排序
稳定排序
剑指 Offer 45. 把数组排成最小的数 #medium #题型
    给定一组数组, 重新排列形成最小的数字. 可以有前置零.
    思路1: 显然是一个 #排序问题. 关键是如何定义排序规则?
0283. 移动零 #easy 原地操作, 将0都放在数组最后, 保持其他元素相对位置
== 选择排序
选择排序的思想是：双重循环遍历数组，每经过一轮比较，找到最小元素的下标，将其交换至首位。
相较于冒泡排序的区别: 
    细节: 冒泡排序在比较过程中就不断交换；而选择排序增加了一个变量保存最小值 / 最大值的下标，遍历完成后才交换，减少了交换次数。
    核心: 冒泡排序法是稳定的，选择排序法是不稳定的。
== 插入排序
特性: 稳定排序
0147. 对链表进行插入排序 #medium #题型 主要考察一些 #细节

======= O(n logn)
下面的几个排序算法的 [总结](https://leetcode.cn/leetbook/read/sort-algorithms/oz1mgh/)
如何超越 `O(n^2)`? 通过「逆序对」的思路, 可知前面的算法都 **必须通过比较和交换相邻元素来消除逆序对**, 因此复杂度不可能超过 O(n^2).
    参见 [希尔排序]
总结: **归并排序、堆排序的复杂度可以稳定为 O(n logn)**, 而其他算法的复杂度都是平均意义下较优. 
    下面的几种算法中, 只有 归并排序 是 #稳定 的.
== 希尔排序
「希尔排序本质上是插入排序的优化，先对间隔较大的元素进行插入排序，完成宏观调控，然后逐步缩小间隔，最后一轮一定是间隔为 1 的排序，
    也就是插入排序。间隔在希尔排序中被称为「增量」，增量序列不同，希尔排序的效率也不同。」
特性: 不稳定.
#增量序列 的选择: 「增量元素不互质，则小增量可能根本不起作用」
    `Hibbard` 增量序列: 2^k-1, 也即 1,3,7,15...
    `Knuth` 增量序列: d{k+1} = 3 * d{k} + 1, 也即 1,4,13,40...
    `Sedgewick` 增量序列
复杂度: 不好分析, 介于 O(n)和 O(n^2) 之间.
== 堆排序
特性: 不稳定.
用堆来实现排序的基本思路: **先完成 `buildMaxHeap`. 然后每次将堆顶元素与堆尾元素交换, 并将堆的大小减 1, 重复这个过程直到堆的大小为 1**.
    如何 `buildMaxHeap`? 从最后一个非叶子节点开始, 依次向前遍历, 对每个节点执行「下沉」操作. 也即调用 `maxHeapify`
    如何 `maxHeapify(i)`? 对于第i的位置, 若不满足堆性质, 不断下沉.
剑指 Offer 40. 最小的k个数 #easy 找到数组中最小的k个元素. 利用 #最大堆 维护最小的k个元素.
== 快速排序
[解析](https://leetcode.cn/leetbook/read/sort-algorithms/eul7hm/)
特性: 不稳定
基数选择: 随机化
分区算法: 放在最前最后; 双指针方法
0169. 多数元素 #easy
    思路2: 若存在「多数元素」, 则排序后, 中间的元素一定为「多数元素」.
== 归并排序
[解析](https://leetcode.cn/leetbook/read/sort-algorithms/euivj1/)
复杂度: 时间 稳定 O(n logn). 空间: 总归是需要额外的 O(n) 空间, O(1) 是不存在的 (实际上就变成了冒泡排序), 参见 解析.
特点: 稳定排序
面试题 10.01. 合并排序的数组 #easy
剑指 Offer 51. 数组中的逆序对 #hard #题型 #star
    在数组中的两个数字，如果前面一个数字大于后面的数字，则这两个数字组成一个 #逆序对。输入一个数组，求出这个数组中的逆序对的总数。


======= O(n)
如何超越 `O(n logn)` 的排序算法? 参见 [计数排序解析](https://leetcode.cn/leetbook/read/sort-algorithms/ozyo63/)
    之前从逆序对的角度, 对于基于相邻元素比较的算法得到了下界 O(n^2), 这里通过 #决策树 来得到「基于比较的排序算法的下界 `O(n logn)`」.
    对于一个长n的数组, 其所有的排列有 O(n!) 中可能. 我们可以将「基于比较的排序算法」看成是决策树上的路径, 从根节点到叶子结点代表了完全对顺序无知到得到排序结果.
    这样, 对于一个高 h 的二叉树, 其叶子结点数量 l需要满足 `n! <= l <= 2^h`. 因此有 `h >= log(n!)`
    根据斯特林（`Stirling`）近似公式, `lg(n!) = O(n logn)`. 
因此, 有《算法导论》定理 8.1：**在最坏情况下，任何比较排序算法都需要做 `O(nlogn)` 次比较**
== 计数排序
特性: 稳定.
[介绍](https://leetcode.cn/leetbook/read/sort-algorithms/ozyo63/)
基本思路: 「先对于出现的数字进行计数; 然后通过计数的结果, 计算出每个元素在排序完成后的位置, 然后将元素赋值到对应位置。」
细节: 我们得到了每个数字的数量, 并通过 #前缀和 得到前置数量. 那么具体如何得到「序列中第 r 个 x 元素的idx」?
    除了顺序遍历, 记录x元素出现的数量. 一种更方便的做法是, 「倒序遍历」, 这样前缀和记录的就是当前x元素最后一个元素应该放的位置, 更简洁.
复杂度:  `O(n+d)`, 其中 d 是数据范围 (因此限制了使用场景)
1122. 数组的相对排序 #easy 但是很有意思 #interest 限制: 数组长度 1e3; 元素范围 [0,1000]
    给定两个数组 arr1, arr2. arr2中的元素互不相同且都出现在arr1中. 要求对于arr1排序: 按照arr2的顺序排, 不在arr2中的元素再按照大小排列在最后.
    思路1: #计数排序 由于本体的元素大小范围较小, 可以采用计数排序.
== 基数排序 Radix sort
[介绍](https://leetcode.cn/leetbook/read/sort-algorithms/raydw2/)
两种不同的方式: 
    「最高位优先法」，简称 `MSD (Most significant digital)`，思路是从最高位开始，依次对基数进行排序
    「最低位优先法」，简称 `LSD (Least significant digital)`。思路是从最低位开始，依次对基数进行排序。使用 LSD 必须保证对基数进行排序的过程是稳定的。
    比较: 从人的直觉角度来理解, MSD 比较容易理解, 但实际上需要一些额外的空间. 而「最低位优先法」中, 每一轮遍历都是直接用所有的数字, 「更符合计算机的操作习惯」
基本思路: 从最低位开始 (作为排序指标), 每一轮对所有数字进行排序, 依次直到最高位. 
    注意到其中会调用「排序算法」, 需要是稳定的. 可以用 #计数排序.
细节: 如何获得基数? 假设要取的某位在十进制下表示是dev, 则可以 `radix = value / dev % 10` 得到.
    如何处理负数? 一种思路是全加一个偏移量, 更为 #优雅 的思路是, 对于负数的取模结果取负数, 例如 -2%5 = -2. (JAVA取模的规范, 但Python不是)
    这样, 可能的 #基数 就有 [-9...9] 共19个, 根据这个进行排序即可.
复杂度: 时间: `O(d(n+r))`, 空间: O(n+r) (和计数排序一样). 这里的d是「最长数字的位数」; r表示「基数可能的取值范围大小」.
    因此, 问到「基数排序算法和快速排序算法哪个更快？」, 答案是无法比较.
0164. 最大间距 #hard #题型 #star 要求得到数组排序之后的相邻元素「最大差值」. 要求: #线性时间, 线性空间.
    限制: n 1e5; 数字范围 [0, 1e9]
    思路1: 根据数字范围不能使用 计数排序. 而本题的数据范围适合使用 #基数排序.
0561. 数组拆分 #easy 将2n的数组分成大小为2的n个, 求 sum{min(pair)} 的最大值.
    提示: 等价于, 排序后两两作为一组.
    思路2: 强行 #基数排序. 注意需要对负数进行调整
== 桶排序
[介绍](https://leetcode.cn/leetbook/read/sort-algorithms/phtz1j/)
基本思想: 将 [mn,mx] 区间分成 n 个相同大小的子区间, 在每个桶中进行排序.
基于假设: 「所有输入数据都服从均匀分布，也就是说输入数据应该尽可能地均匀分布在每个桶中」
0164. 最大间距 #hard #题型 #star 要求得到数组排序之后的相邻元素「最大差值」. 要求: #线性时间, 线性空间.
    假设长n的数组中数据范围 [mn,mx], 可知「最大差值」至少为 (mx-mn)/(n-1).
    因此, 我们可以取 `d <= (mx-mn)/(n-1)`. 这样, 我们可以保证「最大差值不出现在同一桶中」. 这样, **每个桶中仅需要记录最大最小值即可**.



===== 拓展
关于 [Java 源码解析](https://leetcode.cn/leetbook/read/sort-algorithms/phkv6h/)
=== 其他奇怪的排序: 图一乐
- 猴子排序. 取名于「打字的猴子」概念, 也即随机乱序, 检查是否有序. 复杂度 `O(n n!)`
- 睡眠排序. 遍历数组，为每个数字开启一个线程。这个数字有多大，这个线程就睡眠多少秒。待线程睡醒后，输出此数字。利用「小的数字所在的线程会先于大的数字所在的线程醒来」这个特性完成排序。


@2022 """
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    """ ========================== 冒泡排序 =========================  """
    """ 剑指 Offer 45. 把数组排成最小的数 #medium #题型
给定一组数组, 重新排列形成最小的数字. 可以有前置零.
思路1: 显然是一个 #排序问题. 关键是如何定义排序规则?
    提示: 对于 x,y 两个数字/字符串, 直接比较 x+y, y+x (拼接)的大小即可.
    技巧: 在Python中, 定义 comp(x,y) 返回两个数字的大小关系定义, 然后可以通过 `functools.cmp_to_key(comp)` 进行包装, 从而作为 key 传入sort函数.
[here](https://leetcode.cn/problems/ba-shu-zu-pai-cheng-zui-xiao-de-shu-lcof/solution/mian-shi-ti-45-ba-shu-zu-pai-cheng-zui-xiao-de-s-4/)
"""
    def minNumber(self, nums: List[int]) -> str:
        def comp(x:str, y:str):
            # 定义比较函数
            return 1 if x+y > y+x else -1
        nums = [str(i) for i in nums]
        nums.sort(key=functools.cmp_to_key(comp))
        return ''.join(nums)
    
    """ 0283. 移动零 #easy 原地操作, 将0都放在数组最后, 保持其他元素相对位置 """
    
    """ ========================== 选择排序 =========================  """
    """ 0215. 数组中的第K个最大元素 #medium #题型 另见 [quick sort]
思路1: 采用类似 #快排 的思路, 每次选择 pivot 对于 [l,r] 区间进行分割. 也类似 #二分
"""

    """ 0912. 排序数组 #medium 实际上用选择排序过不了... 1e5 """
    def sortArray(self, nums: List[int]) -> List[int]:
        n = len(nums)
        for i in range(n-1,-1,-1):
            idx = 0
            for j in range(i+1):
                if nums[j]>nums[idx]:
                    idx = j
            nums[idx],nums[i] = nums[i],nums[idx]
        return nums
    
    
    """ ========================== 插入排序 =========================  """
    """ 0147. 对链表进行插入排序 #medium #题型 主要考察一些 #细节 """
    def insertionSortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        h = now = ListNode()
        hh = ListNode(0, head)
        while hh.next:
            pre, mn = hh, hh.next.val
            p = hh.next
            while p.next:
                if p.next.val < mn:
                    pre, mn = p, p.next.val
                p = p.next
            now.next = pre.next; now = now.next
            pre.next = pre.next.next
            now.next = None
        return h.next
    
    
    """ ========================== 希尔排序 =========================  """
    """ 0506. 相对名次 #easy 给定一系列运动员的得分, 得到他们的名次. 题目确保了每个人的得分都不一样. 
任何排序算法都可以, 这里强行 #希尔排序.
"""
    def findRelativeRanks(self, score: List[int]) -> List[str]:
        # 希尔排序, 从小到大, 增量序列选择 //2.原地操作.
        n = len(score)
        s2idx = {s:i for i,s in enumerate(score)}
        def shellSort(nums):
            n = len(nums)
            # 增量序列 的选择: //2
            gap = n//2
            while gap:
                for i in range(gap,n):
                    # 冒泡排序的思路, 对于 i=gap...n 找到合适的位置.
                    j = i
                    while j>=gap and nums[j-gap]>nums[j]:
                        nums[j-gap], nums[j] = nums[j], nums[j-gap]
                        j -= gap
                gap //= 2
        # 强行用 shellSort, 任何排序都可以
        shellSort(score)
        ans = [None] * n
        # 注意不能 -1,-2,-3 直接索引, 因为score的长度可能不够.
        for i in range(-1, -n-1,-1):
            srank = str(-i)
            if i==-1: srank = "Gold Medal"
            elif i==-2: srank = "Silver Medal"
            elif i==-3: srank = "Bronze Medal"
            ans[s2idx[score[i]]] = srank
        return ans
    """ ========================== 堆排序 =========================  """
    """ 0215. 数组中的第K个最大元素 #medium #题型 #star [另见 sliding Window 的循环不变量部分] 给定一个数组, 要求返回其中第k大的元素.
限制: 数组长度 1e5
思路1: 维护一个大小为k 的 最小 #堆 复杂度: O(n logk) 
"""

    """ 剑指 Offer 40. 最小的k个数 #easy 找到数组中最小的k个元素. 利用 #最大堆 维护最小的k个元素. """
    def getLeastNumbers(self, arr: List[int], k: int) -> List[int]:
        if k==0: return []  # 恶心的边界.
        h = [-i for i in arr[:k]]
        heapify(h)
        for i in range(k, len(arr)):
            if arr[i] < -h[0]:
                heappushpop(h, -arr[i])
        return [-i for i in h]
    
    """ ========================== 快速排序 =========================  """
    """ 0169. 多数元素 #easy
思路2: 若存在「多数元素」, 则排序后, 中间的元素一定为「多数元素」.
"""
    
    """ ========================== 归并排序 =========================  """
    """ 面试题 10.01. 合并排序的数组 #easy """
    def merge(self, A: List[int], m: int, B: List[int], n: int) -> None:
        i, j = m-1, n-1
        while i>=0 and j>=0:
            if A[i]>B[j]:
                A[i+j+1] = A[i]
                i -= 1
            else:
                A[i+j+1] = B[j]
                j -= 1
        while j>=0:
            A[j] = B[j]
            j -= 1
        # return A
    """ 剑指 Offer 51. 数组中的逆序对 #hard #题型 #star
在数组中的两个数字，如果前面一个数字大于后面的数字，则这两个数字组成一个 #逆序对。输入一个数组，求出这个数组中的逆序对的总数。
思路1：#归并排序 
    注意归并排序是稳定的, 而 **逆序数** 等于一个 序列要变成升序排列所需要的相邻元素交换的最小次数. 
    因此直观理解, 在归并排序过程中, 统计交换次数即为逆序数. """
    
    
    """ ========================== 计数排序 =========================  """
    """ 1122. 数组的相对排序 #easy 但是很有意思 #interest 限制: 数组长度 1e3; 元素范围 [0,1000]
给定两个数组 arr1, arr2. arr2中的元素互不相同且都出现在arr1中. 要求对于arr1排序: 按照arr2的顺序排, 不在arr2中的元素再按照大小排列在最后.
思路1: #计数排序 由于本题的元素大小范围较小, 可以采用计数排序.
    具体而言, 计数后, 先对于出现在arr2中的元素, 按照arr2的顺序输出, 再顺序输出剩余的元素.
"""
    def relativeSortArray(self, arr1: List[int], arr2: List[int]) -> List[int]:
        mx = max(arr1)
        cnt = [0] * (mx+1)
        for a in arr1: cnt[a] += 1
        ans = [0] * len(arr1); idx = 0
        # arr2 顺序
        for a in arr2:
            for i in range(cnt[a]):
                ans[idx] = a; idx += 1
            cnt[a] = 0
        # 其他元素
        for a in range(mx+1):
            for i in range(cnt[a]):
                ans[idx] = a; idx += 1
        return ans
    
    """ ========================== 基数排序 =========================  """
    """ 0164. 最大间距 #hard #题型 #star 要求得到数组排序之后的相邻元素「最大差值」. 要求: #线性时间, 线性空间.
限制: n 1e5; 数字范围 [0, 1e9]
思路1: 根据数字范围不能使用 计数排序. 而本题的数据范围适合使用 #基数排序.
    具体而言, 为了实现基数排序, 对于从低到高位进行排序, 内部采用 计数排序 (稳定). 参见代码.
思路2: #桶排序. 见下面 「桶排序」
    假设长n的数组中数据范围 [mn,mx], 可知「最大差值」至少为 (mx-mn)/(n-1).
    因此, 我们可以取 `d <= (mx-mn)/(n-1)`. 这样, 我们可以保证「最大差值不出现在同一桶中」. 这样, **每个桶中仅需要记录最大最小值即可**.
[official](https://leetcode.cn/problems/maximum-gap/solution/zui-da-jian-ju-by-leetcode-solution/)
"""
    def maximumGap(self, nums: List[int]) -> int:
        # 思路1: 而本题的数据范围适合使用 #基数排序.
        def radixSort(nums):
            # 基数排序 的基本实现.
            radixCnt = [0] * 10
            aux = [0] * len(nums)
            mx = max(nums)
            exp = 1     # 从低到高位排序.
            while mx//exp:
                # 对于 radix计数
                for num in nums: radixCnt[num//exp%10] += 1
                # 统计 前缀和
                radixCnt = list(accumulate(radixCnt))
                # 利用前缀和计算应该填入的idx; 注意需要从后往前!!!
                for i in range(len(nums)-1, -1, -1):
                    radix = nums[i]//exp%10
                    radixCnt[radix] -=1; aux[radixCnt[radix]] = nums[i]
                # 清空 cnt; 复制回 nums
                radixCnt = [0]*10
                for i, num in enumerate(aux): nums[i] = num
                exp *= 10
        if len(nums)<2: return 0    # 边界
        # 基数排序
        radixSort(nums)
        # 输出题目要求.
        ans = 0
        for i in range(1, len(nums)):
            ans = max(ans, nums[i]-nums[i-1])
        return ans
    
    
    """ 0561. 数组拆分 #easy 将2n的数组分成大小为2的n个, 求 sum{min(pair)} 的最大值.
提示: 等价于, 排序后两两作为一组.
思路2: 强行 #基数排序. 注意需要对负数进行调整, 参见 [here](https://leetcode.cn/leetbook/read/sort-algorithms/raf5pg/).
"""
    def arrayPairSum(self, nums: List[int]) -> int:
        nums.sort()
        return sum(nums[::2])
    """ ========================== 桶排序 =========================  """
    """ 0908. 最小差值 I #easy 对于数组中的每一个元素, 可以加上 [-k,k] 范围的数字, 要求操作后 mx-mn 最小.
说明: 寻找最大值和最小值的步骤与桶排序的第一步是相同的
"""
    def smallestRangeI(self, nums: List[int], k: int) -> int:
        mx,mn = max(nums),min(nums)
        return max(0, mx-mn-2*k)
    
    """ 0164. 最大间距 #hard #题型 #star 要求得到数组排序之后的相邻元素「最大差值」. 要求: #线性时间, 线性空间. """
    def maximumGap(self, nums: List[int]) -> int:
        # 思路2: #桶排序.
        if len(nums)<2: return 0
        # 确定桶的大小
        mx = max(nums); mn = min(nums)
        d = max(1, (mx-mn)//(len(nums)-1))
        bucketCnt = (mx-mn)//d + 1  # 桶的数量.
        # 每个桶记录其中元素的 (min, max), -1 表示为空
        buckects = [[-1,-1] for _ in range(bucketCnt)]
        for num in nums:
            idx = (num-mn)//d
            if buckects[idx][0]==-1: buckects[idx] = [num, num]
            else:
                buckects[idx][0] = min(buckects[idx][0], num)
                buckects[idx][1] = max(buckects[idx][1], num)
        # 遍历每个桶得到答案
        pre = -1; ans = 0
        for i in range(bucketCnt):
            if buckects[i][0]==-1: continue
            if pre!=-1: ans = max(ans, buckects[i][0]-pre)
            pre = buckects[i][1]
        return ans
    
    
sol = Solution()
result = [
    # sol.minNumber([10,2]),
    # sol.sortArray(nums = [5,2,3,1]),
    # sol.findRelativeRanks(score = [5,4,3,2,1]),
    # sol.getLeastNumbers([3,2,1], 2),
    # sol.relativeSortArray(arr1 = [2,3,1,3,2,4,6,7,9,2,19], arr2 = [2,1,4,3,9,6]),
    sol.maximumGap(nums = [3,6,9,1]),
    sol.maximumGap([10]),
]
for r in result:
    print(r)
