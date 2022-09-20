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
https://leetcode.cn/contest/cnunionpay2022

前三题都比较基础, T4题目很复杂 (但主体部分的实现, 和数据量要求不难), 最后居然因为精度问题没有AC, 应该长记性了!
@2022 """

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
class Solution:
    """ 银联-1. 重构链表 """
    def reContruct(self, head: Optional[ListNode]) -> Optional[ListNode]:
        d = p = ListNode(0)
        while head:
            if head.val % 2 != 0:
                d.next = head
                d = d.next
            head = head.next
        d.next = None
        return p.next
    
    """ 银联-2. 勘探补给 #二分 查找 """
    def explorationSupply(self, station: List[int], pos: List[int]) -> List[int]:
        n = len(station)
        ans = []
        for p in pos:
            idx = bisect_left(station, p)
            if idx==0: ans.append(0)
            elif idx==n: ans.append(idx-1)
            else:
                if station[idx]-p < p-station[idx-1]:
                    ans.append(idx)
                else: ans.append(idx-1)
        return ans
    
    """ 银联-3. 风能发电 #模拟 """
    def stored_energy(self, storeLimit: int, power: List[int], supply: List[List[int]]) -> int:
        stores = 0
        supply.sort()
        supply = deque(supply)
        ll,lr = 0,0
        for t,p in enumerate(power):
            if supply and t>=supply[0][0]:
                limit = supply.popleft()
                ll,lr = limit[1],limit[2]
            if p<ll: stores -= ll-p; stores = max(0, stores)
            elif p>lr: stores += p-lr; stores = min(stores, storeLimit)
        return stores
        
""" 银联-4. 设计自动售货机 #hard 要求实现一个自动售货机, 题目描述好复杂...
https://leetcode.cn/contest/cnunionpay2022/problems/NyZD2B/
题意: 需要设计一个自动售货机. 可以 addItem, 商品居然 (上架时间, 保质期, 价格, 数量); sell(time, customer, item, number) 的逻辑是, 选择所购买商品中, 优先选择价格最低、距离过期最近的商品.
并且需要记录用户的成功购买次数, 从而计算折扣.
优化: 下面的代码中, 由于需要检查过期时间, 所以每一次sell的复杂度还是 O(n). 如何优化到 O(n logn)?
    参见灵神的 [代码](https://leetcode.cn/circle/discuss/7c1ifr/). 用到 #懒删除堆, 可以实现「在维护一个堆的同时，修改另一个堆中的元素」.
    关键在于, 令两个堆中维护的对象是同一个. 参见 [视频](https://www.bilibili.com/video/BV1fP4y1d7Mn).
"""
class VendingMachine:
    def __init__(self):
        self.customers = defaultdict(int)
        # 物品排序: 按照 (price, remainDaies) 的双重优先级排序. 由于剩余过期时间不好记录, 可以用 -过期日期 代替
        self.items = defaultdict(list)

    def addItem(self, time: int, number: int, item: str, price: int, duration: int) -> None:
        itemInfo = (price, -(time+duration), number)
        heappush(self.items[item], itemInfo)

    def sell(self, time: int, customer: str, item: str, number: int) -> int:
        if item not in self.items or not self.items[item]: return -1
        items = self.items[item]
        # 商品是否足够.
        if sum([i[2] for i in items if -i[1]>=time]) < number: return -1
        acc = 0
        # xs... 因为这里用了分数, 浮点误差导致没有 AC. 解决方案是直接用整数, 最后转分数.
        discount = max(100 - self.customers[customer], 70) # / 100
        while items and number > 0:
            price, endTime, count = heappop(items)
            if -endTime < time: continue
            c = min(number, count)
            acc += ceil(price * c * discount)
            number -= c
            if count > c:
                heappush(items, (price, endTime, count-c))
        # 记录用户消费次数, 从而计算折扣
        self.customers[customer] += 1
        return ceil(acc / 100)

    
sol = Solution()
result = [
    testClass("""["VendingMachine","addItem","sell","sell","sell","sell"]
[[],[0,3,"Apple",10,10],[1,"Tom","Apple",1],[2,"Tom","Apple",3],[3,"Mary","Banana",2],[11,"Jim","Apple",1]]"""),
    testClass("""["VendingMachine","addItem","addItem","sell","addItem","sell","sell","sell","addItem","sell","sell"]
[[],[0,1,"Apple",4,3],[1,3,"Apple",4,2],[2,"Mary","Apple",2],[2,1,"Banana",2,5],[4,"Jim","Banana",2],[4,"Mary","Banana",1],[4,"Mary","Apple",1],[6,200,"Apple",2,5],[6,"Jim","Apple",100],[7,"Mary","Apple",100]]"""),
    testClass("""["VendingMachine","addItem","sell","addItem","sell","sell","sell","sell","sell","addItem","sell","sell","sell","sell","sell","sell","sell","sell","addItem","sell","addItem","sell","sell","sell","sell","addItem","sell","sell","sell"]
[[],[1,444,"Costs",14,233],[35,"Nidia","Costs",136],[64,382,"Costs",33,6],[66,"Jessica","Costs",23],[74,"Jessica","Cell",434],[75,"Jessica","Costs",42],[105,"Jessica","Costs",150],[106,"Jessica","Costs",78],[110,334,"Costs",450,12],[119,"Jessica","Costs",233],[124,"Jessica","Costs",1],[141,"Nidia","Costs",1],[168,"Jessica","Costs",1],[170,"Jessica","Costs",1],[276,"Nidia","Costs",1],[283,"Nidia","Costs",1],[289,"Nidia","Costs",1],[300,472,"Lunches",174,24],[305,"Nidia","Lunches",380],[391,215,"Lunches",233,6],[396,"Nidia","Costs",1],[402,"Jessica","Costs",1],[403,"Jessica","Costs",1],[416,"Nidia","Lunches",1],[424,4,"Cell",105,7],[439,"Jessica","Lunches",1],[445,"Jessica","Lunches",1],[461,"Nidia","Costs",1]]"""),
    # sol.explorationSupply(station = [2,7,8,10], pos = [4,9]),
    # sol.explorationSupply(station = [2,5,8,14,17], pos = [1,14,11,2]),
    # sol.stored_energy(storeLimit = 6, power = [6,5,2,1,0], supply = [[0,1,2],[2,3,3]]),
    # sol.stored_energy(storeLimit = 10, power = [1,3,4,3,6], supply = [[0,2,3]])
]
for r in result:
    print(r)
