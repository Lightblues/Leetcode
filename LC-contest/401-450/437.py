from typing import *
import string

""" 
https://leetcode.cn/contest/weekly-contest-437
Easonsi @2025 """

from collections import defaultdict

class Kosaraju:
    def __init__(self, graph):
        self.graph = graph
        self.n = len(graph)
        self.visited = set()
        self.order = []
        self.rev_graph = defaultdict(list)
        self.sccs = []
        
    def build_reverse_graph(self):
        """构建反图"""
        for u in self.graph:
            for v in self.graph[u]:
                self.rev_graph[v].append(u)
    
    def first_pass(self, u):
        """第一次DFS：记录后序遍历顺序"""
        self.visited.add(u)
        for v in self.graph.get(u, []):
            if v not in self.visited:
                self.first_pass(v)
        self.order.append(u)
    
    def second_pass(self, u, component):
        """第二次DFS：在反图上寻找SCC"""
        self.visited.add(u)
        component.append(u)
        for v in self.rev_graph.get(u, []):
            if v not in self.visited:
                self.second_pass(v, component)
    
    def find_sccs(self):
        """执行Kosaraju算法"""
        # 第一次DFS：记录完成顺序
        self.visited.clear()
        for node in range(self.n):
            if node not in self.visited:
                self.first_pass(node)
        
        # 构建反图
        self.build_reverse_graph()
        
        # 第二次DFS：按逆序在反图上寻找SCC
        self.visited.clear()
        while self.order:
            node = self.order.pop()
            if node not in self.visited:
                component = []
                self.second_pass(node, component)
                self.sccs.append(component)
        
        return self.sccs

class Solution:
    """ 3456. 找出长度为 K 的特殊子字符串 """
    def hasSpecialSubstring(self, s: str, k: int) -> bool:
        acc, pre = 0, ""
        for ch in s + " ":
            if ch != pre:
                if acc == k: return True
                acc, pre = 1, ch
            else:
                acc += 1
        return False
    
    """ 3457. 吃披萨 #medium 每次选4个数值 w<x<y<z, 在奇数/偶数天分别得到 z/y 的分数, 求最大和
思路1: #贪心
    假设有16个数值, 最大的6个为 a,b,c,d,e,f; 
        贪心策略: 选取 f,e 还有 c,a;
        不选择e: 选择 f,d, c,a 不会更优
    [ling](https://leetcode.cn/problems/eat-pizzas/solutions/3076629/tan-xin-pythonjavacgo-by-endlesscheng-fpjx/)
    """
    def maxWeight(self, pizzas: List[int]) -> int:
        pizzas.sort(reverse=True)
        n = len(pizzas) // 4
        n_odd, n_even = n-n//2, n//2
        ans = sum(pizzas[:n_odd])
        for i in range(n_odd+1, n_odd+1+2*n_even, 2):
            ans += pizzas[i]
        return ans
    
    """ 3458. 选择 K 个互不重叠的特殊子字符串 #medium 给定一个字符串, 问能否从中构造k个不重叠的, 特殊字符串.
特殊: 其中的任何字符不能出现在子串之外; 并且不能是整个字符串s. 限制: n 5e4; 0<=k<=26
思路1:
    考虑26个字母分别构成的 "特殊子串", 他们每个构成一个候选, 之间相互交叉的部分, 只能选取一个!
"""
    def maxSubstringLength(self, s: str, k: int) -> bool:
        if k==0: return True
        elif k==1: return len(set(s)) > 1
        g = defaultdict(list)
        for ch in string.ascii_letters:
            l,r = s.index(ch), s.rindex(ch)
            if l<r:
                for x in set(s[l+1:r]):
                    if x!=ch: g[x].append(ch)
        kosaraju = Kosaraju(g)
        sccs = kosaraju.find_sccs()
        # 
        remap = {}
        for i,scc in enumerate(sccs):
            for x in scc:
                remap[x] = i
        ng = defaultdict(set)
        for u,vs in g.items():
            for v in vs:
                ng[remap[u]].add(remap[v])
        out_degrees = [len(vs) for vs in ng.values()]
        return out_degrees >= k
        
sol = Solution()
result = [
    sol.maxWeight(pizzas = [1,2,3,4,5,6,7,8]),
]
for r in result:
    print(r)
