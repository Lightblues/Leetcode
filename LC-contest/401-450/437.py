from typing import *
import string
import math

""" 
https://leetcode.cn/contest/weekly-contest-437
T2 贪心策略
T3 暴力想法, 卡在一个点居然要用 SCC 来计算 (DeepSeek 辅助很棒); 正常的转为 "无重叠区间" 区间的范式很精彩
T4 是一个考验功底的复杂 DP
Easonsi @2025 """

from collections import defaultdict

class Kosaraju:
    # by @DeepSeek
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
思路1: #转化 为有向图, 然后 #Kosaraju 压缩强连通分量 #SCC
    考虑26个字母分别构成的 "特殊子串", 他们每个构成一个候选, 之间相互交叉的部分, 只能选取一个!
    注意到, 在 a..b..a 这样的结构中, a 对于 b 有约束条件. -- 因此, 考虑构建 a->b 的边
        遍历所有字符, 找到它们之间的边关系
    问题转化为: 是否存在k个组, 它们的出度为0
        注意是 r-> {a,b,c}, a<->b 的结构中, {c}, {a,b} 满足条件!
        形式化的, 就是 #强连通分量 压缩之后的图上, 出度为0的节点数量
        为此, 可以用 Kosaraju 计算强连通分量, 然后重构图
    复杂度: O(n + Sigma), 其中 Sigma 为字符类别数
    [wiki](https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm)
思路2: 有向图建模+合并区间+ #无重叠区间
    和上面一样, 还是建图; 然后从每个节点(字符)触发DFS, 获取其对应的区间. -- 需要去掉覆盖整个区间的那些 (对应整个字符串)
    问题转化为: 这些区间中能否找到 k 个不重叠的? 见 "0435. 无重叠区间"
[ling](https://leetcode.cn/problems/select-k-disjoint-special-substrings/solutions/3077261/you-xiang-tu-jian-mo-he-bing-qu-jian-bu-sw1lb/)
"""
    def maxSubstringLength(self, s: str, k: int) -> bool:
        if k==0: return True
        ch_set = set(s)
        ch_map = dict(zip(ch_set, range(len(ch_set))))
        g = {i: [] for i in range(len(ch_set))}
        for ch in string.ascii_letters:
            if ch not in s: continue
            l,r = s.index(ch), s.rindex(ch)
            if l<r:
                for x in set(s[l+1:r]):
                    if x!=ch: g[ch_map[ch]].append(ch_map[x])
        # Kosaraju
        kosaraju = Kosaraju(g)
        sccs = kosaraju.find_sccs()
        # 重构压缩有向图
        if len(sccs)==1: return False  # 不允许整个字符串
        remap = {}
        for i,scc in enumerate(sccs):
            for x in scc:
                remap[x] = i
        ng = [set() for _ in range(len(sccs))]
        for u,vs in g.items():
            for v in vs:
                ui, vi = remap[u], remap[v]
                if ui!=vi: ng[ui].add(vi)
        out_degrees = [len(vs) for vs in ng]
        return out_degrees.count(0) >= k

    def maxSubstringLength(self, s: str, k: int) -> bool:
        # 思路2
        # build graph
        if k==0: return True
        ch_set = set(s)
        ch_map = dict(zip(ch_set, range(len(ch_set))))
        ch_interval = [(-1,-1)]*len(ch_set)
        g = {i: [] for i in range(len(ch_set))}
        for ch in string.ascii_letters:
            if ch not in s: continue
            l,r = s.index(ch), s.rindex(ch)
            ch_interval[ch_map[ch]] = (l,r)
            if l<r:
                for x in set(s[l+1:r]):
                    if x!=ch: g[ch_map[ch]].append(ch_map[x])
        # DFS
        def dfs(x: int) -> tuple[int, int]:
            nonlocal l,r,vis
            vis.add(x)
            l,r = min(l, ch_interval[x][0]), max(r, ch_interval[x][1])
            for y in g[x]:
                if y not in vis:
                    dfs(y)

        intervals = []
        for i in g:
            vis = set()
            l,r = math.inf, 0
            dfs(i)
            if not (l==0 and r==len(s)-1):
                intervals.append((l,r))
        return len(intervals) - self.eraseOverlapIntervals(intervals) >= k


    """ 0435. 无重叠区间 #medium 给定一组区间, 问至少去掉多少个可以使得其他的不重叠.
思路1: #反向思考 #排序 右端点
    考虑反问题: 问最多能保留多少个区间?
     """
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key=lambda x: x[1])
        ans = 0
        pre = -math.inf
        for l,r in intervals:
            if l >= pre:
                ans, pre = ans+1, r
        return len(intervals) - ans

    """ 3459. 最长 V 形对角线段的长度 #hard 在一个0/1/2的矩形中, 从 1 的位置按照对角线方向 (4个) 出发, 然后经过 0,2,0,2,... 的循环, 最多可以经过一次"顺时针转90度", 问最长的长度
限制: n,m 500
思路1: #DP
 """
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        pass #TODO: 

sol = Solution()
result = [
    # sol.maxWeight(pizzas = [1,2,3,4,5,6,7,8]),
    # sol.maxSubstringLength(s = "abcdbaefab", k = 2),
    # sol.maxSubstringLength(s = "cdefdc", k = 3),
    # sol.maxSubstringLength("alulu", 1),
    # sol.eraseOverlapIntervals(intervals = [[1,2],[2,3],[3,4],[1,3]]),
    # sol.maxSubstringLength("bcikby", 5)
]
for r in result:
    print(r)
