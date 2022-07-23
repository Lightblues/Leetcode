import random
import time
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



""" 
== 快速排序
0215. 数组中的第K个最大元素 #medium #题型 #star
    给定一个数组, 要求返回其中第k大的元素.
    思路1: 维护一个大小为k 的 最小 #堆
    思路2: #快速选择, 基于 #快速排序
"""
class Solution():
    """
    Merge sort
    """
    def mergeSort(self, arr):
        print("Splitting ", arr)
        if len(arr) > 1:
            mid = len(arr)//2
            lefthalf = arr[:mid]
            righthalf = arr[mid:]

            self.mergeSort(lefthalf)
            self.mergeSort(righthalf)

            i = 0
            j = 0
            k = 0
            while i < len(lefthalf) and j < len(righthalf):
                if lefthalf[i] < righthalf[j]:
                    arr[k] = lefthalf[i]
                    i = i+1
                else:
                    arr[k] = righthalf[j]
                    j = j+1
                k = k+1

            while i < len(lefthalf):
                arr[k] = lefthalf[i]
                i = i+1
                k = k+1

            while j < len(righthalf):
                arr[k] = righthalf[j]
                j = j+1
                k = k+1
            print("Merging ", arr)


    """
    Quick sort
    """
    def quickSort(self, arr: list):

        def quickHelper(arr: list, first: int, last: int):
            if first < last:
                splitpoint = partition(arr, first, last)
                quickHelper(arr, first, splitpoint - 1)
                quickHelper(arr, splitpoint + 1, last)

        # def partition(self, arr: list, first: int, last: int):
        #     pivot = arr[first]
        #     left = first + 1
        #     right = last
        #
        #     done = False
        #     while not done:
        #         while left <= right and arr[left] <= pivot:
        #             left = left + 1
        #         while arr[right] >= pivot and right >= left:
        #             right = right - 1
        #         if right < left:
        #             done = True
        #         else:
        #             temp = arr[left]
        #             arr[left] = arr[right]
        #             arr[right] = temp
        #     temp = arr[first]
        #     arr[first] = arr[right]
        #     arr[right] = temp
        #
        #     return right

        # 自己按照《算法导论》实现了一下
        def partition(arr: list, first: int, last: int):
            pivot = arr[last]       # 选定最后一个元素为 pivot
            le_pivot = first-1      # 指针，在遍历过程中满足 le_pivot 及其右侧的元素 <=pivot
            for i in range(first, last):
                if arr[i] <= pivot:
                    le_pivot += 1
                    arr[le_pivot], arr[i] = arr[i], arr[le_pivot]
            # 最后 pivot 和 le_pivot+1 位置进行交换
            arr[le_pivot+1], arr[last] = arr[last], arr[le_pivot+1]
            return le_pivot+1

        quickHelper(arr, 0, len(arr) - 1)


    """ 0215. 数组中的第K个最大元素 #medium #题型 #star
给定一个数组, 要求返回其中第k大的元素.
限制: 数组长度 1e5
思路1: 维护一个大小为k 的 最小 #堆
    复杂度: O(n logk)
思路2: #快速选择, 基于 #快速排序
    基本思路是, 每次选择一个pivot, 将数组元素按照相较pivot的大小关系分成两边.
    具体而言, 需要实现 `partition(arr, l,r)` 在 `arr[l...r]` 中随机选择一个pivot, 并返回其下标.
    复杂度: 平均复杂度 `O(n)`, 最坏情况下 `O(n^2)`. 为此, 在选择pivot的时候可以增加 random.
    具体见 [官答](https://leetcode.cn/problems/kth-largest-element-in-an-array/solution/shu-zu-zhong-de-di-kge-zui-da-yuan-su-by-leetcode-/)
"""
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # 推排序
        h = nums[:k]
        heapify(h)
        for num in nums[k:]:
            if num>h[0]:
                heappushpop(h, num)
        return h[0]
            
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # 快速选择
        random.seed(time.time())
        def partition(arr, l,r):
            # 选择 arr[r] 作为 pivot, 进行划分.
            x = arr[r]  # pivot
            i = l-1     # 记录最右边的 <=x 的位置
            for j in range(l, r):
                if arr[j]<=x:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            i += 1
            arr[i], arr[r] = arr[r], arr[i]
            return i
        def randomPartition(arr, l, r):
            # 在partition的基础上, 随机选择一个位置作为 pivot.
            idx = random.randint(l, r)
            arr[idx], arr[r] = arr[r], arr[idx]
            return partition(arr, l, r)
        
        def quickselect(arr, l, r, k):
            # 返回arr中第k大的元素
            # i = partition(arr, l, r)
            i = randomPartition(arr, l, r)
            if i==k:
                return arr[i]
            elif i<k:
                return quickselect(arr, i+1, r, k)
            else:
                return quickselect(arr, l, i-1, k)
        
        return quickselect(nums, 0, len(nums)-1, len(nums)-k)
    
    
    
    def testQuickSort(self):
        arr = [4, 5, 6, 3, 2, 1]
        print("before:", arr)
        self.quickSort(arr)
        print("after:", arr)


sol = Solution()
result = [
    # sol.findKthLargest([3,2,1,5,6,4], k = 2),
    sol.testQuickSort(),
    
]
for r in result:
    print(r)