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
from itertools import product, permutations, combinations, combinations_with_replacement, accumulate
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
# from structures import ListNode, TreeNode, linked2list, list2linked

""" 链表相关
技巧
    挺乱的, 没有硬性要求的话可以转为列表, 或者记录val之间的交换
    指针非常乱, 写代码前在纸上画一下.

2058. 找出临界点之间的最小和最大距离 #medium #链表
    给定一个链表, 定义关键点为局部(严格的)极小/极大值, 要求返回这些关键点之间距离的最小和最大值.


2074. 反转偶数长度组的节点 #medium #链表 #题型
    给定一个链表, 将其分割成 1,2,3... 长的子序列 (最后一个剩余的长度可以不符合). 对于这些子序列, 反转其中长度为偶数的.


0146. LRU 缓存 #medium #hard
"""

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def list2linked(l):
    """ 将 [1,3,2,4] 这样形式的列表转换为 ListNode 链表 """
    if not l: return None
    head = ListNode(l[0])
    cur = head
    for i in range(1, len(l)):
        cur.next = ListNode(l[i])
        cur = cur.next
    return head

def linked2list(head: ListNode):
    l = []
    while head:
        l.append(head.val)
        head = head.next
    return l



class Solution:
    """ 2058. 找出临界点之间的最小和最大距离 #medium #链表
给定一个链表, 定义关键点为局部(严格的)极小/极大值, 要求返回这些关键点之间距离的最小和最大值.
例如, head = [5,3,1,2,5,1,2] 这一链表的关键点位置在 2,4,5, 因此返回 [1,3]
思路1: 模拟遍历
    自己的思路是每次仅关注到当前遍历的节点, 因此需要记录上一个节点的值, 以及上一个节点与当前节点的大小比较.
    而 [answer](https://leetcode.cn/problems/find-the-minimum-and-maximum-number-of-nodes-between-critical-points/solution/zhao-chu-lin-jie-dian-zhi-jian-de-zui-xi-b08v/) 中, 
    使用 `cur.next.next.val` 来获取连续三个节点的值, 更为方便, 而不需要记录历史信息. 从代码上更为简洁.
"""
    def nodesBetweenCriticalPoints(self, head: Optional[ListNode]) -> List[int]:
        minDist = maxDist = -1
        first = last = -1
        pos = 0

        cur = head
        while cur.next.next:
            # 获取连续的三个节点的值
            x, y, z = cur.val, cur.next.val, cur.next.next.val
            # 如果 y 是临界点
            if y > max(x, z) or y < min(x, z):
                if last != -1:
                    # 用相邻临界点的距离更新最小值
                    minDist = (pos - last if minDist == -1 else min(minDist, pos - last))
                    # 用到第一个临界点的距离更新最大值
                    maxDist = max(maxDist, pos - first)
                if first == -1:
                    first = pos
                # 更新上一个临界点
                last = pos
            cur = cur.next
            pos += 1
        
        return [minDist, maxDist]


    """ 0206. 反转链表 #easy #题型
给定一个链表, 将其反转.
思路1: 迭代. 经典实现. 维护 pre,cur,next 三个指针会比较清晰.
思路2: 递归 实现
思路3: 能否再减少一个指针? 在 #双指针 思路中, 不移动 head 而在遍历过程中修改 head.next 所指向的节点.
    参见 2074
    from [here](https://leetcode.cn/problems/reverse-linked-list/solution/fan-zhuan-lian-biao-shuang-zhi-zhen-di-gui-yao-mo-/) 
[官答](https://leetcode.cn/problems/reverse-linked-list/solution/fan-zhuan-lian-biao-by-leetcode-solution-d1k2/)
"""
    def reverseList(self, head: ListNode) -> ListNode:
        # 思路3: 只有两个指针
        cur = head
        while head.next:
            # 一般写法
            # t = head.next.next
            # head.next.next, cur  = cur, head.next
            # head.next = t
            
            # 注意! 这样会出问题. 
            # 因为 LHS中, 先对于 head.next 进行了赋值, 这样 head.next.next 中的 head.next 就变了!!!
            # head.next, head.next.next, cur  = head.next.next, cur, head.next
            # 这样就没问题了
            head.next.next, head.next, cur  = cur, head.next.next, head.next
        return cur

    """ 2074. 反转偶数长度组的节点 #medium #链表 #题型
给定一个链表, 将其分割成 1,2,3... 长的子序列 (最后一个剩余的长度可以不符合). 对于这些子序列, 反转其中长度为偶数的.
思路1: 暴力模拟. 完全按照 #链表 的思路来写
    救命, 这题写了两个小时.
    思路是实现一个翻转 [i,j] 范围内节点的函数 (同时要求连上 i-1, j+1); 然后遍历
    然而如何判断最后剩余的长度是否为偶数呢? 自己的思路尝试用一次遍历用指针记录, 但是极为繁琐 (还不可行)
思路2: 针对第二个问题, 放弃了整合在一次遍历的想法. 而是通过两次遍历: 第一次判断剩余是否为偶数. 然后在确实下一个目标序列的奇偶性的前提下进行翻转
    总体来看, 只需要维护 pre, cur 两个指针即可. 1) 若当前长度 i 为奇数, 将两者都前进i步即可; 2) 若为偶数, 则需要实现「将从cur开始的i个节点进行翻转」, 见下代码.
    [官方](https://leetcode.cn/problems/reverse-nodes-in-even-length-groups/solution/fan-zhuan-ou-shu-chang-du-zu-de-jie-dian-owra/) 
    """
    def reverseEvenLengthGroups(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """ [官方](https://leetcode.cn/problems/reverse-nodes-in-even-length-groups/solution/fan-zhuan-ou-shu-chang-du-zu-de-jie-dian-owra/) 
        采用了两次遍历
        """
        i = 0
        cur, pre = head, None
        while cur:
            # i 是每一轮的目标序列长度
            i += 1
            
            # 第一次遍历, 检查剩余链表长度是否够满 i 个
            it = cur
            length = 0
            while length < i and it:
                length += 1
                it = it.next
            
            # 第二次遍历, 根据是否需要翻转:
            # 若序列长度为奇数, 直接将 pre, cur 移动到下一个序列
            if length & 1:
                for j in range(length):
                    pre, cur = cur, cur.next
            # 若序列长度为偶数, 需要翻转
            else:
                # version1: 官方的神奇代码
                for j in range(length - 1):
                    pre.next, cur.next.next, cur.next = cur.next, pre.next, cur.next.next
                pre, cur = cur, cur.next
                
                #  version2: 笨拙实现.
                # prevRecord = pre
                # pre, cur = cur, cur.next
                # for j in range(length-1):
                #     next = cur.next
                #     cur.next = pre
                #     pre, cur = cur, next
                # # 注意这里的pre!! 防止出现循环
                # pre, prevRecord.next.next, prevRecord.next = prevRecord.next, cur, pre
                
        return head



sol = Solution()
result = [
    linked2list(sol.reverseList(list2linked([1,2,3,4,5]))),
    
    # linked2list(sol.reverseEvenLengthGroups(head = list2linked(
    #     # [5,2,6,3,9,1,7,3,8,4]
    #     # [1,1,0,6]
    #     [1,1,0,6,5])
    # )),

]
for r in result:
    print(r)
