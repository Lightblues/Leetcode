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
import operator
from operator import add, ne, sub, xor, mul, truediv, floordiv, mod, pow, neg, pos
import sys, os
# sys.setrecursionlimit(10000)
import re

# https://github.com/grantjenks/python-sortedcontainers
from sortedcontainers import SortedList, SortedSet, SortedDict
# help(SortedDict)
# import numpy as np
from fractions import Fraction
from decimal import Decimal

# from utils_leetcode import testClass
from structures import ListNode, TreeNode, LinkedList, list2linked, linked2list

""" 
https://leetcode.cn/contest/weekly-contest-267
https://leetcode-cn.com/contest/biweekly-contest-71
@2022 """
class Solution:
    """ 2073. 买票需要的时间
给定一个队列表示每个人要买的票的数量. 购票规则是, 每个人只能购买一张, 因此购买后只能回到队尾重新排队. 要求第k个人买到所需的所有票的时间

"""
    def timeRequiredToBuy(self, tickets: List[int], k: int) -> int:
        ans = 0
        while tickets[k]> 1:
            ans += sum(i>0 for i in tickets)
            tickets = [i-1 if i>0 else 0 for i in tickets]
        ans += sum(i>0 for i in tickets[:k+1])
        return ans
    def timeRequiredToBuy(self, tickets: List[int], k: int) -> int:
        # 更仔细分析一下, O(n)
        numK = tickets[k]
        result = 0
        for i in range(k):
            result += min(tickets[i], numK)
        for j in range(k+1, len(tickets)):
            result += min(tickets[j], numK-1)
        return result+numK

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
        """ 思路1: 非常繁琐的判断 """
        def reverse(head: ListNode, left, right):
            """ 翻转 head~right.prev 子序列, 其左右元素分别为 left, right """
            head_record = head
            # 翻转 head ~ right.prev
            prev = left
            curr = head
            # 注意, 是翻转 head ~ right.prev 这一子序列
            while curr!=right and curr:
                next = curr.next
                curr.next = prev
                prev, curr = curr, next
            # 将子序列拼接回原链表
            head_record.next = right
            left.next = prev
        
        # 哨兵节点
        node0 = ListNode(0, next=head)
        th = 0
        """ 
        这里的 prev, next 分别记录目标序列的前一个节点和下一个节点
        node 是当前检查的节点
        """
        node = node0.next
        next = node0.next
        prev = node0
        while node:
            counter = 1
            # 目标子序列之前的那个节点. 由于部分进行了翻转部分没有, 这里直接往后 th 个节点
            for i in range(th):
                prev = prev.next
            node = next
            # 向后遍历 th+1 个节点
            while node and counter <= th:
                node = node.next
                if node:
                    counter += 1
            # 记录子序列之后的那个节点
            next = node.next if node else None
            th += 1
            
            if counter%2 == 0:
                reverse(prev.next, prev, next)
        return node0.next

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
                # for j in range(length - 1):
                #     pre.next, cur.next.next, cur.next = cur.next, pre.next, cur.next.next
                # pre, cur = cur, cur.next
                #  version2: 笨拙实现.
                prevRecord = pre
                pre, cur = cur, cur.next
                for j in range(length-1):
                    next = cur.next
                    cur.next = pre
                    pre, cur = cur, next
                # 注意这里的pre!! 防止出现循环
                pre, prevRecord.next.next, prevRecord.next = prevRecord.next, cur, pre
                
        return head


    """ 2075. 解码斜向换位密码 #medium
定义一种加密方案: 给定一个固定行数 rows 的矩阵 (理解为「加密纸条」), 将originalText按照 主对角线、右上方的次对角线... 的规律进行填充. (填充保证右下角是填了的) 这样得到的encodedText是将这一矩阵一行一行拼接得到的序列.
思路1: #模拟 暴力求解
    直接叫 encodedText 展开为矩阵, 然后斜方向依次即可取回原字符串
    对于加密纸条中未填充的部分, 去除末尾的空格即可
"""
    def decodeCiphertext(self, encodedText: str, rows: int) -> str:
        """ 这是很早之前的代码, 想太多了!!! """
        if rows == 1:
            return encodedText
        cols = len(encodedText) // rows
        matrix = []
        for row in range(rows):
            matrix.append(encodedText[row*cols:(row+1)*cols])
        raw = ""
        # 这里的判断并不需要, 直接遍历到右上角即可
        if rows>cols:
            nDiag = 1
        else:
            nDiag= cols-rows + 1
            # 检查最后一个斜行是否有字母
            for i in range(rows-1):
                if matrix[i][nDiag+i] != " ":
                    nDiag += 1
                    break
        # 填入字母
        for i in range(nDiag):
            for j in range(rows):
                x, y = j, i+j
                if y>=cols:
                    break
                raw += matrix[x][y]
        return raw.rstrip()

    """ 2076. 处理含限制条件的好友请求 #hard #题型
有n个用户, 给定一组约束 restrictions, 每一个约束 (u,v) 表示两者不能联通; 对于一系列好友请求 requests, 判断他们能否建立关系(连边).
思路1: #并查集 的基础上利用 #哈希表 记录能否成为关系
    判断是否联通显然可以用并查集框架. 关键是如何判断是否违反了约束? 可以将所有的约束条件记录在根节点上
    因此, 对于每一个查询, 先找 (u,v) 的根节点, 基于 `cant[rootu][rootv]` (矩阵形式的哈希表) 的值判断是否违反了约束.
    若没有, 则请求成功. 然后合并集合 `father[rootu] = rootv` 并将 cant[rootu] 中所记录的约束条件都记录在节点 rootv 上.
    参见 [here](https://leetcode.cn/problems/process-restricted-friend-requests/solution/bing-cha-ji-by-endlesscheng-8ipg/)
"""
    def friendRequests(self, n: int, restrictions: List[List[int]], requests: List[List[int]]) -> List[bool]:
        """ [here](https://leetcode.cn/problems/process-restricted-friend-requests/solution/bing-cha-ji-by-endlesscheng-8ipg/) """
        # 并查集框架
        father = list(range(n))
        def find(u):
            path = []
            while father[u]!=u:
                u = father[u]
                path.append(u)
            for i in path: father[i] = u
            return u
        
        # 矩阵 cant[u][v] 记录 u 和 v 是否可以建立好友关系
        cant = [[False] * n for _ in range(n)]
        for u,v in restrictions:
            cant[u][v] = cant[v][u] = True
        
        ans = [False] * len(requests)
        for i,(u,v) in enumerate(requests):
            # 找到两者的root, 根据它们之间的关系判断是否可以建立关系
            rootu, rootv = find(u), find(v)
            if cant[rootu][rootv]: continue
            # 否则说明可以添加
            ans[i] = True
            if rootu==rootv:    # 已经在一个集合中
                continue
            else:
                """ 否则进行合并. 例如将rootu设为孩子, 将它的约束条件都添加到rootv上 """
                # 启发式合并：总是从小的集合合并到大的集合上
                if rootu>rootv: rootu, rootv = rootv, rootu 
                father[rootu] = rootv
                # 将rootu的约束条件都添加到rootv上
                for j, cannot in enumerate(cant[rootu]):
                    if cannot: cant[j][rootv] = cant[rootv][j] = True
        return ans
    
    
sol = Solution()
result = [
    # sol.timeRequiredToBuy(tickets = [2,3,2], k = 2),

    linked2list(sol.reverseEvenLengthGroups(head = list2linked(
        # [5,2,6,3,9,1,7,3,8,4]
        # [1,1,0,6]
        [1,1,0,6,5])
    )),

    # sol.decodeCiphertext("ch   ie   pr", rows = 3),
    # sol.decodeCiphertext("a  b  ", 3),
    # sol.decodeCiphertext("iveo    eed   l t    olc", 4),
    # sol.decodeCiphertext("iveo    eed   l te   olc", rows = 4)
    
    # sol.friendRequests(n = 3, restrictions = [[0,1]], requests = [[0,2],[2,1]]),
]
for r in result:
    print(r)
