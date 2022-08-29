import random
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

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


""" 
[哈希表](https://leetcode.cn/leetbook/detail/hash-table/)
== 基本实现
支持操作: 增、删、改、查询
冲突解决方法

== 基本应用
=== 1. 哈希集合: 查重
0136. 只出现一次的数字 #easy 一个数字中, 除了一个数字出现一次外, 其他数字都出现两次. 找到那个特殊值.
0202. 快乐数 #easy
    检查一个数字重复某一操作是否会出现循环. 因此可以用set来记录出现的数字.
=== 2. 哈希映射
1) 提供额外的信息. 通过哈希映射建立密钥与信息之间的映射关系。
0001. 两数之和 #easy 找到数组中两个值之和为target的下标组合
    可以用dict记录下标信息
0205. 同构字符串 #easy #题型
    两个字符串同构的条件是, 字符之间存在一一映射关系. 注意不能是一对多. 判断两字符串是否同构.
    思路1: 由于要判断是否符合一一映射, 需要记录 `s2t, t2s` 两个方向的map.
0599. 两个列表的最小索引总和 #easy #题型
    两个人各有一个顺序的喜欢的餐厅列表. 在他们都喜欢的餐厅中, 找到「索引和」最小的餐厅 (若有相同值的都输出). 这里的索引和即排名之和.

2) 按键聚合. 分类聚合.
0359. 日志速率限制器 #easy #现实 对于顺序发过来的日志打印请求, 只有在上一个相同消息的时间在10s之前才能打印. 
    思路1: 用哈希表来记录上一次打印某个消息的时间

== 如何设计键? 上面的key都是比较显然的, 但有些时候的key不是那么直观.
本质上, 就是如何对于特定的DS来计算其hash值.
键的设计就是如何进行分类. 参见 [一些总结](https://leetcode.cn/leetbook/read/hash-table/xxavl2/)
    顺序不重要, 则进行排序; 关注偏移量, 则将偏移量作为key; 
    如何表达子树? 利用树的「序列化」
    矩阵: 行列索引, 对角线索引...
0049. 字母异位词分组 #medium 「字母异位词」是指构成的字符相同只是顺序不同的字符串. 将字母异位词分组返回.
0249. 移位字符串分组 #medium #题型 
    类似0049, 不过这里两个字符串在同一组的要求是, 每个字符进行一定移位之后有对应关系, 例如 aac 与 bbd
0652. 寻找重复的子树 #medium #题型
    在二叉树中, 找到所有子树结构出现重复的节点. 两颗子树「相同」也即具有相同的结构和值. 对于重复的结构只需要返回其中一个节点即可.
    转换: 也即, 要求子树的hash表示.

== 应用题
0003. 无重复字符的最长子串 #medium #题型
    思路1: 双指针, 并用set记录当前段落出现的字符.
0170. 两数之和 III - 数据结构设计 #easy 类似 0001. 两数之和 不过需要多次添加数据和查询
0347. 前 K 个高频元素 #medium #题型
0288. 单词的唯一缩写 #medium 
    单词的缩写定义为 `i18n` 的形式. 初始化时, 给定一组单词. 对于每个查询的单词 word, 记其所写为 h, 若满足 1) 字典中没有缩写相同的单词; 2) 字典中所有缩写为 h 的词均为 word. 则返回 true, 否则返回 false.
    思路1: 记录哈希表的形式记录唯一性.
0380. O(1) 时间插入、删除和获取随机元素 #medium #题型
    要求实现一个DS (类似set), 能够在 常数时间内完成 插入, 删除, 以及从当前所有元素中随机得到一个元素
    注意: 要求随机获得元素, 但是哈希表的底层结构 (无法顺序idx) 决定了其不能随机索引. (pop操作不是随机的!!)
    思路1: 利用一个数组动态存储元素, 再用一个哈希表记录每个值所在的位置.

"""
class Solution:
    """ 0136. 只出现一次的数字 #easy 一个数字中, 除了一个数字出现一次外, 其他数字都出现两次. 找到那个特殊值.
思路1: 用一个哈希表存储出现过的值
思路2: 进阶要求是使用 O(1) 的空间. 可以用到 xor 的性质!
"""
    def singleNumber(self, nums: List[int]) -> int:
        s = set()
        for a in nums:
            if a in s: s.remove(a)
            else: s.add(a)
        return s.pop()
    def singleNumber(self, nums: List[int]) -> int:
        return reduce(xor, nums)
    """ 0349. 两个数组的交集 """
    def intersection(self, nums1: List[int], nums2: List[int]) -> List[int]:
        return list(set(nums1).intersection(set(nums2)))
    """ 0202. 快乐数 #easy
检查一个数字重复某一操作是否会出现循环. 因此可以用set来记录出现的数字.
"""
    def isHappy(self, n: int) -> bool:
        def f(x):
            ans = 0
            while x>0:
                x,a = divmod(x,10)
                ans += a*a
            return ans
        s = set(); s.add(n)
        while n!=1:
            n = f(n)
            if n in s: return False
            else: s.add(n)
        return True
    
    """ 0001. 两数之和 #easy 找到数组中两个值之和为target的下标组合
可以用dict记录下标信息
"""
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        v2idx = {}
        for i,a in enumerate(nums):
            if target-a in v2idx: return [i,v2idx[target-a]]
            else: v2idx[a] = i
    """ 0205. 同构字符串 #easy #题型
两个字符串同构的条件是, 字符之间存在一一映射关系. 注意不能是一对多. 判断两字符串是否同构.
思路1: 由于要判断是否符合一一映射, 需要记录 `s2t, t2s` 两个方向的map.
"""
    def isIsomorphic(self, s: str, t: str) -> bool:
        s2t,t2s = {}, {}
        for a,b in zip(s,t):
            if a in s2t and b!=s2t[a] or b in t2s and a!=t2s[b]: return False
            else: s2t[a] = b; t2s[b] = a
        return True
    """ 0599. 两个列表的最小索引总和 #easy #题型
两个人各有一个顺序的喜欢的餐厅列表. 在他们都喜欢的餐厅中, 找到「索引和」最小的餐厅 (若有相同值的都输出). 这里的索引和即排名之和.
"""
    def findRestaurant(self, list1: List[str], list2: List[str]) -> List[str]:
        r2idx = dict(zip(list1, range(len(list1))))
        mn = inf; ans = []
        for i,r in enumerate(list2):
            if r not in r2idx or r2idx[r]+i>mn: continue
            elif r2idx[r]+i==mn: ans.append(r)
            else: mn=r2idx[r]+i; ans=[r]
        return ans






    """ 0387. 字符串中的第一个唯一字符 #easy 找到字符串中只出现一次的字符中, idx的最小值. """
    def firstUniqChar(self, s: str) -> int:
        ch2idx = {}
        for i,c in enumerate(s):
            if c not in ch2idx: ch2idx[c] = i
            else: ch2idx[c] = -1
        ans = inf
        for k,v in ch2idx.items():
            if v==-1: continue
            else: ans = min(ans, v)
        return ans if ans!=inf else -1
    
    """ 0350. 两个数组的交集 II #easy 类似 0349. 两个数组的交集, 不过数组中的元素可以重复. 要求返回相交的元素的个数.
思路1: 首先对于nums1的元素个数进行统计. 然后遍历nums2
"""
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        c1,c2 = Counter(nums1),Counter(nums2)
        ans = []
        for k,v in c2.items():
            if k in c1: ans += [k]*min(v, c1[k])
        return ans
    """ 0219. 存在重复元素 II #easy 对于给定的数组, 判断是否存在 值相同并且距离小于k的下标组. """
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        d = {}
        for i,a in enumerate(nums):
            if a in d and i-d[a]<=k: return True
            else: d[a] = i
        return False
    
    
    """ 0049. 字母异位词分组 #medium 「字母异位词」是指构成的字符相同只是顺序不同的字符串. 将字母异位词分组返回. """
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        results = defaultdict(list)
        for s in strs:
            results[''.join(sorted(s))].append(s)
        return list(results.values())
    """ 0249. 移位字符串分组 #medium #题型 
    类似0049, 不过这里两个字符串在同一组的要求是, 每个字符进行一定移位之后有对应关系, 例如 aac 与 bbd """
    def groupStrings(self, strings: List[str]) -> List[List[str]]:
        # hash 1: 将第一个字符变为 a
        def ch2idx(ch): return ord(ch)-ord('a')
        def idx2ch(idx): return str(ord('a') + idx)
        def h(s):
            offset = ch2idx(s[0])
            return "".join(idx2ch((ch2idx(c)-offset) % 26) for c in s)
        # hash 2: 字符串之间可以移位得到必然是每一位距离差对应一致的时候
        def h(string):
            return tuple(((ord(string[i]) - ord(string[i-1])) % 26) for i in range(1 , len(string))) if len(string) > 1 else 0

        ans = defaultdict(list)
        for s in strings: ans[h(s)].append(s)
        return list(ans.values())
    """ 0652. 寻找重复的子树 #medium #题型
在二叉树中, 找到所有子树结构出现重复的节点. 两颗子树「相同」也即具有相同的结构和值. 对于重复的结构只需要返回其中一个节点即可.
转换: 也即, 要求子树的hash表示.
 """
    def findDuplicateSubtrees(self, root: Optional[TreeNode]) -> List[Optional[TreeNode]]:
        # 思路1: 分离求子树 hash 的方法. 带来复杂度的提升
        def h(node):
            if not node: return "#"
            return str(node.val)+" "+h(node.left)+" "+h(node.right)
        ans = []
        def dfs(node):
            if not node: return
            hs = h(node)
            seen[hs] += 1
            if seen[hs]==2: ans.append(node)
            dfs(node.left)
            dfs(node.right)
        seen = Counter()
        dfs(root)
        return ans
    def findDuplicateSubtrees(self, root: Optional[TreeNode]) -> List[Optional[TreeNode]]:
        cnt = Counter(); ans = []
        def dfs(node: TreeNode):
            # 返回该子树的 hash表示.
            if not node: return "#"
            hs = str(node.val) + " " + dfs(node.left) + " " + dfs(node.right)
            cnt[hs] += 1
            if cnt[hs]==2: ans.append(node)
            return hs
        dfs(root)
        return ans
    
    
    
    """ 0003. 无重复字符的最长子串 #medium #题型
思路1: 双指针, 并用set记录当前段落出现的字符. """
    def lengthOfLongestSubstring(self, s: str) -> int:
        st = set()
        l = -1      # 左指针.
        ans = 0
        for r,ch in enumerate(s):
            while ch in st:
                l += 1; st.remove(s[l])
            ans = max(ans, r-l)
            st.add(ch)
        return ans
    
    """ 0454. 四数相加 II #medium
给四个数组, 要求统计 (i,j,k,l) 下标组对应元素之和为 0 的组对数量. 限制: 每个数组长度 n 200
思路1: 先统计两个数组的数字可以构成的和 (以及计数). 然后匹配. 类似二分?
"""
    def fourSumCount(self, nums1: List[int], nums2: List[int], nums3: List[int], nums4: List[int]) -> int:
        def f(nums1, nums2):
            return Counter(a+b for a in nums1 for b in nums2)
        c1,c2 = f(nums1, nums2), f(nums3, nums4)
        ans = 0
        for k in c1: ans += c1[k] * c2[-k]
        return ans
    
    """ 0347. 前 K 个高频元素 #medium #题型
给定一个数组, 返回其中出现频次前k高的元素. 题目保证了答案唯一. 要求复杂度小于 O(n logn)
思路1: 对于计数的结果, 要求得到 「 #topK」, 经典可以用 #堆 解决
    复杂度: O(n logk)
思路2: 对于「topK」问题, 另一个经典解法是 #快排.
    注意这里只需要得到前k大的元素而不需要完整排序, 因此每次期望减半, 复杂度 O(n)
"""
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        cnt = Counter(nums)
        h = []  # (cnt, num)
        for a,c in cnt.items():
            if len(h)==k:
                if h[0][0] < c: heappushpop(h, (c,a))
                else: continue
            else: heappush(h, (c,a))
        return [a for c,a in h]
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # 思路2: 快排. 注意这里指需要得到前k大的元素而不需要完整排序, 因此每次期望减半, 复杂度 O(n)
        def swep(i,j): cnt[i],cnt[j] = cnt[j],cnt[i]
        def qsort(l,r,k):
            # 对于 [l...r] 区间, 保证前k个元素是最大的.
            if l>=r: return
            # 引入随机
            picked = random.randint(l,r)
            # 选择最后一个作为pivot
            swep(r,picked)
            pivot = cnt[r][0]
            idx = l     # [l...idx) > pivot. idx 是下一个要被填入的位置.
            for i in range(l,r):
                if cnt[i][0]>pivot:
                    swep(i,idx)
                    idx += 1
            swep(idx,r)
            # [l...idx] 位置是最大的 idx-l+1 个元素.
            # k = idx-l+1 / idx-l 都不用再递归了.
            if idx-l>k: qsort(l,idx-1,k)
            elif idx-l+1<k: qsort(idx+1,r,k-(idx-l+1))
        cnt = Counter(nums)
        cnt = [(c,a) for a,c in cnt.items()]
        qsort(0, len(cnt)-1, k)
        return [a for c,a in cnt[:k]]
    
    
    
    
    
    
    
    
    
""" 705. 设计哈希集合 #easy
要求支持 增删和查询操作. 限制: key [0...1e6]
思路1: 直接用一个 1e6 的数组存. 复杂度: 空间复杂度较高 O(n)
思路2: 采用 #链地址法 用一个链表来存储每一个桶中的冲突的key
    复杂度: 假设hash值是均匀分布的, 则对于n个键b个桶, 时间复杂度为 O(n/b).
细节: 在删除操作中, 由于我们采用的是list的方式存储, pop的时间复杂度为O(n). 如何优化? 一种方式是将要删除的元素替换为最后一个元素; 第二种方式是用链表来实现.
补充: 解决冲突的常见策略. 1) 链地址法; 2) 开放地址法 (找下一个空的位置); 3) 再哈希法 (换一个hash函数)

"""
class MyHashSet:
    def __init__(self):
        self.c = [False] * (10**6+2)
    def add(self, key: int) -> None:
        self.c[key] = True
    def remove(self, key: int) -> None:
        self.c[key] = False
    def contains(self, key: int) -> bool:
        return self.c[key]
class MyHashSet:
    # 思路2: 采用 #链地址法 用一个链表来存储每一个桶中的冲突的key
    def __init__(self) -> None:
        self.base = 769
        self.d = [[] for _ in range(self.base)]
    def fhash(self, key): 
        return key % self.base
    def add(self, key: int) -> None:
        h = self.fhash(key)
        if key not in self.d[h]:
            self.d[h].append(key)
    def remove(self, key: int) -> None:
        h = self.fhash(key)
        if key in self.d[h]:
            self.d[h].remove(key)
    def contains(self, key: int) -> bool:
        return key in self.d[self.fhash(key)]
""" 0706. 设计哈希映射 #easy #题型 相较于 0705题, 由于还要存储value, 多了很多的细节. """
class MyHashMap:
    def __init__(self) -> None:
        self.base = 769
        self.d = [[] for _ in range(self.base)]
    def fhash(self, key): 
        return key % self.base
    def put(self, key: int, value: int) -> None:
        h = self.fhash(key)
        for i,(k,v) in enumerate(self.d[h]):
            if k == key:
                self.d[h][i] = (key,value)
                return
        else:
            self.d[h].append((key,value))
    def remove(self, key: int) -> None:
        h = self.fhash(key)
        for i,(k,v) in enumerate(self.d[h]):
            if k == key: 
                self.d[h].pop(i); break
    def get(self, key: int) -> int:
        for k, v in self.d[self.fhash(key)]:
            if k == key:
                return v
        return -1


""" 0359. 日志速率限制器 #easy #现实 对于顺序发过来的日志打印请求, 只有在上一个相同消息的时间在10s之前才能打印. 
思路1: 用哈希表来记录上一次打印某个消息的时间 """
class Logger:
    def __init__(self):
        self.d = {}
    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        if message in self.d and timestamp<self.d[message]+10:
            return False
        self.d[message]=timestamp
        return True
""" 0170. 两数之和 III - 数据结构设计 #easy 类似 0001. 两数之和 不过需要多次添加数据和查询 """
class TwoSum:
    def __init__(self):
        self.d = Counter()
    def add(self, number: int) -> None:
        self.d[number] += 1
    def find(self, value: int) -> bool:
        for a in self.d:
            if value-a != a and value-a in self.d: return True
            if value-a==a and self.d[a] > 1: return True
        return False

""" 0288. 单词的唯一缩写 #medium 
单词的缩写定义为 `i18n` 的形式. 初始化时, 给定一组单词. 对于每个查询的单词 word, 记其所写为 h, 若满足 1) 字典中没有缩写相同的单词; 2) 字典中所有缩写为 h 的词均为 word. 则返回 true, 否则返回 false.
思路1: 记录哈希表的形式记录唯一性.
"""
class ValidWordAbbr:
    def hash(self, s):
        # 转为 i18n 形式
        if len(s)<=2: return s
        return s[0] + str(len(s)-2) + s[-1]
    def __init__(self, dictionary: List[str]):
        self.d = {}
        for s in dictionary:
            h = self.hash(s)
            if h not in self.d: self.d[h] = s
            elif self.d[h] != s: self.d[h] = None
    def isUnique(self, word: str) -> bool:
        h = self.hash(word)
        if h not in self.d or self.d[h]==word: return True
        return False

""" 0380. O(1) 时间插入、删除和获取随机元素 #medium #题型
要求实现一个DS (类似set), 能够在 常数时间内完成 插入, 删除, 以及从当前所有元素中随机得到一个元素
注意: 要求随机获得元素, 但是哈希表的底层结构 (无法顺序idx) 决定了其不能随机索引. (pop操作不是随机的!!)
思路1: 利用一个数组动态存储元素, 再用一个哈希表记录每个值所在的位置.
    如何删除? 将末尾元素补到被删除元素所在idx.
"""
class RandomizedSet:
    def __init__(self):
        self.arr = []
        self.val2idx = {}
    def insert(self, val: int) -> bool:
        if val in self.val2idx: return False
        else: 
            self.val2idx[val] = len(self.arr); self.arr.append(val)
            return True
    def remove(self, val: int) -> bool:
        if val not in self.val2idx: return False
        else:
            idx = self.val2idx[val]
            x = self.arr[-1]        # 注意, 不能直接pop, 因为idx可能在最后一个
            self.arr[idx] = x
            self.arr.pop()
            self.val2idx[x] = idx
            self.val2idx.pop(val); 
            return True
    def getRandom(self) -> int:
        return random.choice(self.arr)


sol = Solution()
result = [
#     testClass("""["MyHashMap", "put", "put", "get", "get", "put", "get", "remove", "get"]
# [[], [1, 1], [2, 2], [1], [3], [2, 1], [2], [2], [2]]"""),
    # sol.groupStrings(["abc", "bcd", "acef", "xyz", "az", "ba", "a", "z"]),
    # sol.lengthOfLongestSubstring(s = "pwwkew"),
    # sol.topKFrequent(nums = [1,1,1,2,2,3], k = 2),
#     testClass("""["RandomizedSet", "insert", "remove", "insert", "getRandom", "remove", "insert", "getRandom"]
# [[], [1], [2], [2], [], [1], [2], []]"""),
    testClass("""["RandomizedSet","insert","insert","remove","insert","remove","getRandom"]
[[],[0],[1],[0],[2],[1],[]]"""),
    # sol.topKFrequent([3,0,1,0], 1),
]
for r in result:
    print(r)