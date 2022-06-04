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
from operator import add, sub, xor, mul, truediv, floordiv, mod, pow, neg, pos
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
# from structures import ListNode, TreeNode, linked2list, list2linked

""" 


0208. 实现 Trie (前缀树) #medium #题型 #Trie
    请你实现 Trie 类

0421. 数组中两个数的最大异或值 #medium
    给定一组数字, 要求返回这组数字中, 两个数字的最大异或值.
    思路: 从高到低位检查最大可能的异或值
1707. 与数组中元素的最大异或值 #hard
    有一组固定的数字 nums. 然后给定一组查询 queries, 对于每个查询 (x,m) 要求返回x与nums中不大于m的元素的最大异或值.
    用Trie存储数组信息; 离线和在线查询两种思路
1938. 查询最大基因差 #hard #trie #DFS
    给定一组树结构的「基因」, 每一个节点都是数字 (从 0到 n-1). 定义基因之前的差是两个数字的异或值. 然后给定一组查询 (node, val) 要求从树上的node节点及其祖先节点中国呢, 找到与val异或最大值.
    离线的思路; 需要对字典树实现「删除」操作

1948. 删除系统中的重复文件夹 #hard
    背景很有意思: 对于一棵目录树, 若两个节点所包含的目录结构(文件夹名字)相同, 则认为它们是重复的. 给定一棵目录树, 要求检测删除所有重复节点.
    主体是对于树节点的序列化表达. 用 Trie 来处理从根目录到叶子节点的路径.

"""

class TrieBit:
    """ 二分的前缀树. left, right 分别存储该位为 0/1
    从高位到低位保存值信息. 由于数字对应的序列的(最大)长度是固定的, 因此不需要 isleaf 标记 """
    def __init__(self) -> None:
        self.left = None
        self.right = None


class Trie:
    """ 0208. 实现 Trie (前缀树) #medium #题型 #Trie
请你实现 Trie 类
    Trie() 初始化前缀树对象。
    void insert(String word) 向前缀树中插入字符串 word 。
    boolean search(String word) 如果字符串 word 在前缀树中，返回 true（即，在检索之前已经插入）；否则，返回 false 。
    boolean startsWith(String prefix) 如果之前已经插入的字符串 word 的前缀之一为 prefix ，返回 true ；否则，返回 false 。
思路: 前缀树基本写法. 每个节点存储: 1) 子节点的哈希表; 2) 是否为单词结尾标记
    复杂度: 初始化为 O(1)，其余操作为 O(|S|)，其中 |S| 是每次插入或查询的字符串的长度
[官方](https://leetcode.cn/problems/implement-trie-prefix-tree/solution/shi-xian-trie-qian-zhui-shu-by-leetcode-ti500/)

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/implement-trie-prefix-tree
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
    def __init__(self):
        self.children = [None] * 26
        self.isleaf = False

    def insert(self, word: str) -> None:
        # 注意, node 初始化为 self
        node = self
        for ch in word:
            ch = ord(ch) - ord('a')
            if not node.children[ch]:
                node.children[ch] = Trie()
            node = node.children[ch]
        # 标记为单词结尾
        node.isleaf = True

    def searchPrefix(self, prefix: str) -> "Trie":
        """ 抽象下面两个需求/函数: 给一个prefix, 不管是否为leaf, 若有该prefix的话返回节点, 否则返回None """
        node = self
        for ch in prefix:
            ch = ord(ch) - ord('a')
            if not node.children[ch]:
                return None
            node = node.children[ch]
        return node

    def search(self, word: str) -> bool:
        """ 检索是否包含该词 """
        node = self.searchPrefix(word)
        return node is not None and node.isleaf

    def startsWith(self, prefix: str) -> bool:
        """ 只需要检索前缀即可 """
        node = self.searchPrefix(prefix)
        return node is not None


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)





class Solution:
    
    def testClass(self, inputs):
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res
    
    """ 0421. 数组中两个数的最大异或值 #medium
给定一组数字, 要求返回这组数字中, 两个数字的最大异或值.
约束: nums.length 1e4, 数组元素 nums[i] <= 2^31 - 1
思路1: #trie 
    因为数字大小有范围, 因此可以用前缀树来存储所包含的数字.
    取最大值是希望高位有效. 因此, 应该从高位开始构建前缀树.
    因此, 遍历列表, 对于每个数字 num: 1) 与之前的值查询, 尽量使得xor最大 (从高位开始取相反 bit); 2) 插入 num 到前缀树中.
    [官方](https://leetcode.cn/problems/maximum-xor-of-two-numbers-in-an-array/solution/shu-zu-zhong-liang-ge-shu-de-zui-da-yi-h-n9m9/)
思路2: #哈希表
    思路是类似的: 每次尽量使得高位有效. 只不过 Trie的思路是每次加一个数字进来查询, 而是每次都是所有的 nums.
    递推公式: 假如最高的 k位可以异或为 cur, 则最高 k+1 位可能构成 curr<<1 或者 (curr<<1)+1. 也即第 k+1位能否构成1.
    每次检查这一位即可. 为此, 可以用一个 #哈希表 `prefixed` 来所有 nums 的前 k+1位, 然后进行检查:
        当前待检查的目标值为 `x=(curr<<1)+1`, 利用 `a^b=x` 等价于 `a^x=b` 的性质, 可以 O(m) 复杂度检查是否存在二元组构成目标前缀, 其中 m为哈希表长度.
    参见官方, 下面搬运的实现异常简洁, 很 Pythonic.
"""
    def findMaximumXOR(self, nums: List[int]) -> int:
        class TrieBit:
            """ 二分的前缀树. left, right 分别存储该位为 0/1
            从高位到低位保存值信息. 由于数字对应的序列的(最大)长度是固定的, 因此不需要 isleaf 标记 """
            def __init__(self) -> None:
                self.left = None
                self.right = None
        MAXBIT = 31
        
        def add(root, num):
            node = root
            for i in range(MAXBIT-1, -1, -1):
                # 从高位构建字典树!
                bit = (num >> i) & 1        # 注意 >> 运算的优先级较低
                if bit == 0:
                    # left 存储 0
                    if not node.left:
                        node.left = TrieBit()
                    node = node.left
                else:
                    if not node.right:
                        node.right = TrieBit()
                    node = node.right
        def query(root, num):
            
            node = root
            x = 0   # 存储最大异或值. 初始化为 0, 由于是从高位到低位的遍历, 在每次更新是 <<1 进行更新
            for k in range(MAXBIT-1, -1, -1):
                bit = (num >> k) & 1
                if bit == 0:
                    # a_i 的第 k 个二进制位为 0，应当往表示 1 的子节点 right 走
                    if node.right:
                        node = node.right
                        x = (x<<1) + 1
                    else:   # 否则一定存在 left
                        node = node.left
                        x <<= 1
                else:
                    if node.left:
                        node = node.left
                        x = (x<<1) + 1
                    else:
                        node = node.right
                        x <<= 1
            return x
        
        x = 0
        root = TrieBit()
        add(root, nums[0])
        for num in nums[1:]:
            x = max(query(root, num), x)
            add(root, num)
        return x

    def findMaximumXOR(self, nums: List[int]) -> int:
        """ 利用哈希集合存储按位前缀 """
        L = len(bin(max(nums)))-2
        max_xor = 0
        for i in range(L)[::-1]:
            max_xor <<= 1
            # max_xor 保存在前 i 个 bin 可能的最大与结果，则 max_xor <<= 1 是肯定取得到的
            # 接下来判断更新后的末位是否也可取 1，即 curr_xor = max_xor | 1 能否满足
            # 也即，在 prefixed 中是否存在 x,y 满足 x^y=curr_xor
            # 转化成 any(curr_xor^p in prefixed for p in prefixed) 这句代码判断是否满足
            curr_xor = max_xor | 1  # 将目前最后一位置设为 1. 递推过程中, 可能构成的最大结果
            prefixed = {num>>i for num in nums}
            max_xor |= any(curr_xor^p in prefixed for p in prefixed)
        return max_xor
    
    """ 1707. 与数组中元素的最大异或值 #hard
有一组固定的数字 nums. 然后给定一组查询 queries, 对于每个查询 (x,m) 要求返回x与nums中不大于m的元素的最大异或值.
约束: 数组和查询长度 1e5, 数组元素 1e9 (2^30)
参见「0421. 数组中两个数的最大异或值」
    一开始的时候, 直接沿用 0421 的思路, TrieBit 非常简介, 用了naive的方式DFS检索.
    [官方](https://leetcode.cn/problems/maximum-xor-with-an-element-from-array/solution/yu-shu-zu-zhong-yuan-su-de-zui-da-yi-huo-7erc/)
    这里的思路有意思: 区分所给的查询是 在线/离线查询. **若为离线的, 可以进行排序** 然后在检索!
思路1: #离线询问 + 字典树
    在 0421中已经实现了基于字典树的最大异或, 差别仅在于约束m.
    利用这里给的查询是静态的这一特点, 可以对于 nums, queries 排序, 维护双指针, 对于每次查询仅将小于m的数字插入字典树.
思路2: #在线询问 + 字典树
    对于在线查询而言, 如何满足约束该路径对应的数字不大于m? 自己之前的思路是从高到低位进行比较, 到需要标记为, 因此采用了DFS, 超时.
    官答中, 相较于之前基本的 TrieBit 结构, 每个节点上存储了 `min_val` 属性, 也即该节点下的最小元素. 这样按照 0421 题中搜索思路即可.
    
"""
    def maximizeXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        """ naive 实现, 超时了!!!
        因为是因为query里用了DFS?"""
        MAXBIT = 30
        def add(root, num):
            """ 将 num 插入到 root 树中 """
            for x in range(MAXBIT)[::-1]:
                bit = (num >> x) & 1
                if bit==1:
                    if not root.right:
                        root.right = TrieBit()
                    root = root.right
                else:
                    if not root.left:
                        root.left = TrieBit()
                    root = root.left
            root.val = num
        # 就用上一题的仅有左右子树的字典树
        root = TrieBit()
        for num in nums:
            add(root, num)
        
        def query(root, x, m):
            """ 检查root树中, 不大于m的元素与x的最大异或值
            思路: 在遍历到树上的每个点的时候, 看是否满足小于等于m"""
            x = [(x>>i)&1 for i in range(MAXBIT)][::-1]
            m = [(m>>i)&1 for i in range(MAXBIT)][::-1]
            def dfs(node, i, maxXor, fSmall=False) -> int:
                """ flag `fSmall` 标记在遍历过程中, 是否已有一位已比m的某一位小. """
                if i==len(x):
                    return maxXor
                # 只能往右的情况
                if not fSmall and m[i]==0:
                    if not node.left: return -1
                    b = (maxXor<<1) + (x[i]==1)
                    return dfs(node.left, i+1, b, fSmall=fSmall)
                # 两边都可
                maxs = []
                if node.left:
                    a = False if fSmall==False and m[i]==0 else True
                    b = (maxXor<<1) + (x[i]==1)
                    max1 = dfs(node.left, i+1, b, fSmall=a)
                    maxs.append(max1)
                if node.right:
                    b = (maxXor<<1) + (x[i]==0)
                    max2 = dfs(node.right, i+1, b, fSmall=fSmall)
                    maxs.append(max2)
                return max(maxs)
            return dfs(root, 0, 0)
        ans = []
        for x,m in queries:
            ans.append(query(root, x, m))
        return ans
    
    def maximizeXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        """思路2, 在线算法. [官方](https://leetcode.cn/problems/maximum-xor-with-an-element-from-array/solution/yu-shu-zu-zhong-yuan-su-de-zui-da-yi-huo-7erc/) """
        MAXBIT = 30
        
        class TrieBitv2:
            """ 相较于上面的数据结构, 每个节点多维护了 min_val 属性  """
            def __init__(self) -> None:
                self.left = None
                self.right = None
                self.min_val = math.inf
        
            def insert(self, val):
                node = self
                node.min_val = min(node.min_val, val)
                for x in range(MAXBIT-1, -1, -1):
                    bit = (val>>x) & 1
                    if bit==1:
                        if not node.right:
                            node.right = TrieBitv2()
                        node = node.right
                    else:
                        if not node.left:
                            node.left = TrieBitv2()
                        node = node.left
                    node.min_val = min(node.min_val, val)
                    
            def query(self, x, m):
                """ 查询字典树中, 不大于m的元素中, 与x的最大异或值 """
                node = self
                if node.min_val > m: return -1
                ans = 0
                for k in range(MAXBIT-1, -1, -1):
                    bit = (x>>k) & 1
                # 下面是官方的思路, 后面的是自己写的
                #     check = False
                #     if bit==0:
                #         if node.right and node.right.min_val <= m:
                #             node = node.right
                #             check = True
                #         else:
                #             node = node.left
                #     else:
                #         if node.left and node.left.min_val <= m:
                #             node = node.left
                #             check = True
                #         else:
                #             node = node.right
                #     if check:
                #         ans |= (1<<k)
                # return ans
            
                    reversebit = 1-bit
                    n = node.right if reversebit==1 else node.left
                    if n and n.min_val <= m:
                        node = n
                        continue
                    n = node.right if bit==1 else node.left
                    if n and n.min_val <= m:
                        node = n
                        continue
                    return -1
                return node.min_val ^ x
            
        root = TrieBitv2()
        for num in nums:
            root.insert(num)
        ans = []
        for x,m in queries:
            ans.append(root.query(x, m))
        return ans

    def maximizeXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        """ 思路1, 离线查询 """
        class Trie:
            # 这里定义的树结构和方法和 0421 一致
            L = 30
            def __init__(self):
                self.left = None
                self.right = None

            def insert(self, val: int):
                node = self
                for i in range(Trie.L, -1, -1):
                    bit = (val >> i) & 1
                    if bit == 0:
                        if not node.left:
                            node.left = Trie()
                        node = node.left
                    else:
                        if not node.right:
                            node.right = Trie()
                        node = node.right
            
            def getMaxXor(self, val: int) -> int:
                ans, node = 0, self
                for i in range(Trie.L, -1, -1):
                    bit = (val >> i) & 1
                    check = False
                    if bit == 0:
                        if node.right:
                            node = node.right
                            check = True
                        else:
                            node = node.left
                    else:
                        if node.left:
                            node = node.left
                            check = True
                        else:
                            node = node.right
                    if check:
                        ans |= 1 << i
                return ans

        n, q = len(nums), len(queries)
        # 先排序! 然后双指针插入、查询
        nums.sort()
        queries = sorted([(x, m, i) for i, (x, m) in enumerate(queries)], key=lambda query: query[1])
        
        ans = [0] * q
        t = Trie()
        idx = 0
        for x, m, qid in queries:
            while idx < n and nums[idx] <= m:
                t.insert(nums[idx])
                idx += 1
            if idx == 0:
                # 字典树为空
                ans[qid] = -1
            else:
                ans[qid] = t.getMaxXor(x)
        
        return ans



    """ 1938. 查询最大基因差 #hard #trie #DFS
给定一组树结构的「基因」, 每一个节点都是数字 (从 0到 n-1). 定义基因之前的差是两个数字的异或值. 然后给定一组查询 (node, val) 要求从树上的node节点及其祖先节点中国呢, 找到与val异或最大值.
限制: 节点数量 1e5, 查询次数 3e4 (可能是做过的最复杂的题之一?)
思路1: #离线算法 + #字典树
    首先, 这里的查询是离线的. 然后需要获取祖先节点 (路径), 那么可以对于查询归类 (排序), 然后 **在DFS过程中就天然记录了这条路径**!
    这样, 在对基因树DFS的过程中, 对于每个节点 (如果出现在了查询中) 需要得到 「val与当前路径上的节点的最大异或值」.
    我们可以用一个字典树来记录这些值, 与之前两道题区别在于, 这里DFS过程中, 我们需要能够「删除」字典树上的节点.
    如何删除? (感觉也应用在正常的字符序列形式的字典树上), 只需要记录每个节点(包括叶子节点和中间节点) 所包含的路径 (前缀) 数量即可. 在删除操作中, 对于该条路径上的所有节点count-1.
    注意: 这里有基因树和字典树两个树结构, 实现的时候注意区分.
    [here](https://leetcode.cn/problems/maximum-genetic-difference-query/solution/cha-xun-zui-da-ji-yin-chai-by-leetcode-s-sybl/)

输入：parents = [-1,0,1,1], queries = [[0,2],[3,2],[2,5]]
输出：[2,3,7]
解释：查询数组处理如下：
- [0,2]：最大基因差的对应节点为 0 ，基因差为 2 XOR 0 = 2 。
- [3,2]：最大基因差的对应节点为 1 ，基因差为 2 XOR 1 = 3 。
- [2,5]：最大基因差的对应节点为 2 ，基因差为 5 XOR 2 = 7 。

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/maximum-genetic-difference-query
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

"""
    def maxGeneticDifference(self, parents: List[int], queries: List[List[int]]) -> List[int]:
        LIMIT = 20
        class Trie():
            def __init__(self) -> None:
                self.right = None
                self.left = None
                self.count = 0
            def add(self, val: int):
                node = self
                for i in range(LIMIT-1, -1, -1):
                    bit = (val>>i) & 1
                    if bit==1:
                        if not node.right:
                            node.right = Trie()
                        node = node.right
                    else:
                        if not node.left:
                            node.left = Trie()
                        node = node.left
                    # 在路径 (除了根节点) 的每一个节点 count+1 —— 在查询的时候也是这样做的
                    node.count += 1
            def remove(self, val: int):
                node = self
                # for i in range(LIMIT-1, 0, -1):
                #     bit = (val>>i) & 1
                #     if bit==1:
                #         if not node.right: return
                #         node = node.right
                #     else:
                #         if not node.left: return
                #         node = node.left
                # bit = val & 1
                # if bit==1: node.right = None
                # else: node.left = None
                for i in range(LIMIT-1, -1, -1):
                    bit = (val>>i) & 1
                    node = node.right if bit==1 else node.left
                    node.count -= 1
            def query(self, val: int) -> int:
                """ 查询当前树中与val的最大异或值 """
                node = self
                x = 0
                for i in range(LIMIT-1, -1, -1):
                    bit = (val>>i) & 1
                    # reverseBit = 1-bit
                    # a = node.right if reverseBit==1 else node.left
                    # if a:
                    #     node = a
                    #     x = (x<<1) + 1
                    # else:
                    #     node = node.right if reverseBit==0 else node.left
                    #     x = x<<1
                    
                    if bit==1:
                        if node.left and node.left.count>0:
                            node = node.left
                            x = (x<<1) + 1
                        else:
                            node = node.right
                            x = x<<1
                    else:
                        if node.right and node.right.count>0:
                            node = node.right
                            x = (x<<1) + 1
                        else:
                            node = node.left
                            x = x<<1
                return x
        # 构造基因树
        root = None
        childs = [[] for _ in range(len(parents))]
        for i,parent in enumerate(parents):
            if parent==-1:
                root = i
                continue
            childs[parent].append(i)
        # 对于查询排序
        node2queries = defaultdict(list)
        for i,(node, val) in enumerate(queries):
            node2queries[node].append((i, val))
        
        rootTrie = Trie()
        results = []
        def dfs(root):
            rootTrie.add(root)
            if root in node2queries:
                for (i,val) in node2queries[root]:
                    results.append((i, rootTrie.query(val)))
            for child in childs[root]:
                dfs(child)
            rootTrie.remove(root)
        dfs(root)
        return [i[1] for i in sorted(results)]
        

    """ 1948. 删除系统中的重复文件夹 #hard
背景很有意思: 对于一棵目录树, 若两个节点所包含的目录结构(文件夹名字)相同, 则认为它们是重复的. 给定一棵目录树, 要求检测删除所有重复节点.
约束: 目录树的节点数量 2e4, 路径最大深度 500, 文件夹名称不超过 10个字符.
思路1: #字典树 + #括号表示法 + 哈希表
    如何检测两棵子树结构相同? 对于树结构序列化为字符串, 判断两个字符串是否相同. (采用后续遍历DFS)
    如何保证子节点之间的顺序? 利用Trie存储子节点, 对于key排序.
    如何删除重复节点? 用一个哈希表存储节点表示到节点的映射, 将 1:n 映射的节点删除.
    [官答](https://leetcode.cn/problems/delete-duplicate-folders-in-system/solution/shan-chu-xi-tong-zhong-de-zhong-fu-wen-j-ic32/)
    复杂度: 见答案中的分析.

"""
    def deleteDuplicateFolder(self, paths: List[List[str]]) -> List[List[str]]:
        class Trie:
            def __init__(self, name) -> None:
                self.name = name
                self.children = {}  # name to node
                self.duplicated = False
        root = Trie("/")
        for path in paths:
            node = root
            for d in path:
                if d not in node.children:
                    node.children[d] = Trie(d)
                node = node.children[d]
        # 存储节点的序列化表示到节点的映射
        parse2node = defaultdict(list)
        def dfs(node: Trie) -> str:
            """ 后续遍历得到节点包含的子树的表示 """
            if len(node.children)==0:
                return ""
            # s = node.name
            s = ""
            for child in sorted(node.children):
                child = node.children[child]
                p = dfs(child)
                s += child.name + "("+p+")"
            parse2node[s].append(node)
            return s
        dfs(root)
        # 通过标记的方式删除重复节点
        for p, nodes in parse2node.items():
            if len(nodes)>1:
                for n in nodes:
                    n.duplicated = True
        # DFS遍历所有保留的节点, 返回结果
        res = []
        path = []
        def dfsOut(node: Trie):
            for childName, childNode in node.children.items():
                if childNode.duplicated: continue
                path.append(childName)
                # 对于每一个非duplicated目录都需要输出
                res.append(path[:])
                dfsOut(childNode)
                path.pop()
        dfsOut(root)
        return res

sol = Solution()
result = [
#     sol.testClass("""["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
# [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]"""),
    
    # sol.findMaximumXOR(nums = [3,10,5,25,2,8]),
    # sol.findMaximumXOR(nums = [0]),
    
    # sol.maximizeXor(nums = [0,1,2,3,4], queries = [[1,3],[5,6]]),
    # sol.maximizeXor(nums = [5,2,4,6,6,3], queries = [[12,4],[8,1],[6,3]]),
    
    sol.maxGeneticDifference(parents = [-1,0,1,1], queries = [[0,2],[3,2],[2,5]]),
    sol.maxGeneticDifference(parents = [3,7,-1,2,0,7,0,2], queries = [[4,6],[1,15],[0,5]]), # [6,14,7]
    sol.maxGeneticDifference([3,3,3,-1,3], [[2,6],[2,1],[1,9],[2,3],[3,6]])
]
for r in result:
    print(r)
