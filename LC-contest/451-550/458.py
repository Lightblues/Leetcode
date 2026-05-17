from typing import *
from functools import cache
from collections import Counter

"""
https://leetcode.cn/contest/weekly-contest-458
1. 模拟
2. 又是 联通分量, 通过并查集来维护
3. 字符串处理, 求最终得到的第 k 位, 通过 逆向思维 + 分类讨论, 注意边界情况 #details
4. 图中的最长回文路径
    类型属于 "§9.2 排列型 ② 相邻相关" -- 考虑 f(x,y, S)
    考虑题目情况的优化方案!
Easonsi @2026 """


class Solution:
    """ 3612. 用特殊操作处理字符串 I """
    def processStr(self, s: str) -> str:
        res = []
        for ch in s:
            if ch == "*":
                if res: res.pop()
            elif ch == "#":
                res += res[:]
            elif ch == "%":
                res = res[::-1]
            else: res.append(ch)
        return "".join(res)

    """ 3613. 最小化连通分量的最大成本
给定一个带权图, 可以任意移除边, 最多剩余 k 个 CC; CC 的 "成本" 为边权最大值; 要求 min{ max(cost) }
限制: n 5e4
思路 1: 反向加边, 直到构成 k 个 CC; 通过并查集来维护
    """
    def minCost(self, n: int, edges: List[List[int]], k: int) -> int:
        fa = list(range(n))
        cc = n
        def find(x:int) -> int:
            root = x
            while fa[root] != root: root = fa[root]
            while fa[x] != x:
                x, fa[x] = fa[x], root
            return root
        def merge(x: int, y: int) -> int:
            fx,fy = find(x),find(y)
            nonlocal cc
            if fx != fy:
                fa[fx] = fy
                cc -= 1
            return cc
        edges.sort(key=lambda x: x[-1])
        if n <= k: return 0  # NOTE: 边界
        for x,y,w in edges:
            c = merge(x,y)
            if c <= k: return w
        # return edges[-1][-1]
    
    """ 3614. 用特殊操作处理字符串 II #hard #6
给定一个字符串做处理: 1. * 删除最后; 2. # 复制; 3. % 反转. 返回最终得到的字符串的第 k 个字符 (从 0 开始), 超出范围则返回 `.`
限制: n 1e5
思路 1: #逆向思维 + 分类
    - 首先, 正向考虑每一步得到的字符串长度 size[i]
    - 然后反向考虑: 对于位置 i, s[i] = c
        - c 是字母
            - size[i] == k+1: 即为答案
            - 否则, 递归 i-1
        - c == "*": 无影响, 递归 i-1
        - c == "#": 设 m = size[i] / 2
            - 若 m > k: 无影响
            - m <= k: 递归 k-m 位置
        - c == "%": 递归 size[i]-1-k 位置
    复杂度: O(n)
https://leetcode.cn/problems/process-string-with-special-operations-ii/solutions/3722462/ni-xiang-si-wei-pythonjavacgo-by-endless-26al/
    """
    def processStr(self, s: str, k: int) -> str:
        n = len(s)
        size = [0] * n
        sz = 0
        for i, ch in enumerate(s):
            if ch == "*": sz = sz-1 if sz>0 else 0
            elif ch=="#": sz *= 2
            elif ch=="%": pass
            else: sz += 1
            size[i] = sz
        if k>=sz: return "."
        for i in range(n-1,-1,-1):
            c = s[i]
            sz = size[i]
            if c == "#":
                if sz//2 <= k:  # NOTE: 前半的范围为 [0,sz//2-1], 因此这里需要 <=
                    k -= sz//2
            elif c=="%":
                k = sz-1-k
            elif c != "*" and sz==k+1:
                return c
        # return "."

    """ 3615. 图中的最长回文路径 #hard #6
给定一个无向图, 节点有字符. 求不经过相同点的回文路径的最大长度.
限制: n 14
尝试 1: 从一个节点出发, dfs 记录 "半条路径" 所经过的所有节点 & 字母顺序; 若出现字母顺序同&节点都不一样的情况则构成回文
    问题: 1. 需要枚举所有的 dfs 情况, 连通图复杂度 O(n!); 2. 相同字母顺序的情况可能很多, 判断"节点不相交"复杂度较高
思路 1: 中心扩展法 + 状压 DP + 优化
    记 f(x,y,S) 表示从 x,y 作为中心拓展, 包含节点 S 情况下的最长匹配路径 (不包含 x/y); 则: 
    - 遍历 x, y 的邻居 u,v, 不在 S 中, 若 label[u]==label[v] & u!=v, 可向外拓展
    - f(x,y,S) = max{ f(u,v,S+{u,v}) + 2 for (u,v) }
    复杂度: 考虑 DP 状态数为 n^2*2^n, 状态转移 (完全图) n^2; 因此 DP 复杂度 O(n^4 2^n)
    优化:
        1. (x,y) 的顺序不影响, 因此可以默认 x<=y -- 优化后才能过, 9.4s
        2. 可以计算理论最大值: 所有偶数的都放进去; 奇数的最多加一个 -- 8.3s
        3. 特判完全图 -- 可以取得 theoretical_max -- 0.7s
https://leetcode.cn/problems/longest-palindromic-path-in-graph/solutions/3722469/zhong-xin-kuo-zhan-fa-zhuang-ya-dp-by-en-ai9s/
    """
    def maxLen(self, n: int, edges: List[List[int]], label: str) -> int:
        # def max(x:int,y:int): 
        max = lambda a,b: b if b>a else a

        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        @cache
        def f(x:int, y:int, vis:int) -> int:
            # 从 x/y 出发的最大回文长度, 不考虑 x/y
            res = 0
            for u in g[x]:
                if vis>>u & 1: continue
                for v in g[y]:
                    if vis>>v & 1 or u==v or label[u]!=label[v]: continue
                    # 优化 1. (x,y)
                    if v>u:
                        v,u = u,v
                    res = max(res, f(u, v, vis | 1<<u | 1<<v) + 2)
            return res
        # 
        ans = 0
        for x in range(n):
            ans = max(ans, f(x,x,1<<x) + 1)
        for x,y in edges:
            if label[x]==label[y]:
                ans = max(ans, f(x,y,1<<x|1<<y) + 2)
        return ans

    def maxLen(self, n: int, edges: List[List[int]], label: str) -> int:
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        # 优化 2. 可以计算理论最大值
        num_odds = sum(c%2 for c in Counter(label).values())
        theoretical_max = n - max(num_odds - 1, 0)  # 最多选一个奇数
        # 优化 3. 特判完全图
        if len(edges) == n*(n-1)//2: return theoretical_max

        @cache
        def f(x:int, y:int, vis:int) -> int:
            # 从 x/y 出发的最大回文长度, 不考虑 x/y
            res = 0
            for u in g[x]:
                if vis>>u & 1: continue
                for v in g[y]:
                    if vis>>v & 1 or u==v or label[u]!=label[v]: continue
                    # 优化 1. (x,y)
                    if v>u:
                        v,u = u,v
                    res = max(res, f(u, v, vis | 1<<u | 1<<v) + 2)
            return res
        # 
        ans = 0
        for x in range(n):
            ans = max(ans, f(x,x,1<<x) + 1)
        for x,y in edges:
            if label[x]==label[y]:
                ans = max(ans, f(x,y,1<<x|1<<y) + 2)
                if ans == theoretical_max: return ans  # 提前结束
        return ans

sol = Solution()
result = [
    # sol.processStr(s = "a#b%*"),
    # sol.minCost(n = 5, edges = [[0,1,4],[1,2,3],[1,3,2],[3,4,6]], k = 2),
    # sol.processStr(s = "a#b%*", k = 1),
    # sol.processStr(s = "cd%#*#", k = 3),
    # sol.processStr(s = "z*#", k = 0),
    sol.maxLen(n = 3, edges = [[0,1],[1,2]], label = "aba"),
    sol.maxLen(n = 3, edges = [[0,1],[0,2]], label = "abc"),
]
for r in result:
    print(r)