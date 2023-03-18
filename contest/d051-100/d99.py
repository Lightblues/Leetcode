from easonsi.util.leetcode import *

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
https://leetcode-cn.com/contest/biweekly-contest-99
Easonsi @2023 """
class Solution:
    """ 6312. 最小和分割 """
    def splitNum(self, num: int) -> int:
        ints = [int(i) for i in str(num)]
        ans = 0
        ints.sort(reverse=True)
        for i,x in enumerate(ints):
            ans += x * 10 ** (i//2)
        return ans
    
    """ 6311. 统计染色格子数 找规律/公式 """
    def coloredCells(self, n: int) -> int:
        if n==1: return 1
        return 1 + 4*n*(n-1)//2

    """ 6313. 统计将重叠区间合并成组的方案数 #medium 基本的合并交叉区间 变形 """
    def countWays(self, ranges: List[List[int]]) -> int:
        ranges.sort()
        num = 0
        last = -1
        for l,r in ranges:
            if l>last:
                num += 1
                last=r
            else:
                last = max(last, r)
        MOD = 10**9 + 7
        return pow(2, num, MOD)

    """ 6314. 统计可能的树根数目 #hard 有一个n节点的树, 但只知道edges (也即根节点不确定). 
然后B进行了一些猜测 (u,v) 是父子关系, B只说这些猜测中至少有k个是对的. 问有多少个节点可能是根节点? 限制: n 1e5; 猜测数量 1e5
思路1: DFS
    参考示例中的图, 发现讲根u的孩子v翻转为root, 发生父子关系变化的只有 (u,v) 边!
    因此, 先任意选择一个节点作为root, 统计猜对的数量cnt. 
    然后, #DFS 遍历所有节点, 在搜索过程中记录动态的「作为根节点时的猜对数量」, 进行转移
    复杂度: O(n)
"""
    def rootCount(self, edges: List[List[int]], guesses: List[List[int]], k: int) -> int:
        # 先建图
        n = len(edges)+1
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v); g[v].append(u)
        # 转为树结构. 设置root=0
        t = [set() for _ in range(n)]
        q = deque([0]); visited = set([0])
        while q:
            u = q.popleft()
            for v in g[u]:
                if v not in visited:
                    t[u].add(v)
                    q.append(v)
                    visited.add(v)
        # 初始化. 统计以0作为root下的猜对的数量. 
        guess = Counter(tuple(g) for g in guesses)
        cnt = 0
        for (u,v),c in guess.items():
            if v in t[u]:
                cnt += c
        # DFS
        ans = int(cnt>=k)
        def dfs(u, cnt):
            nonlocal ans
            for v in t[u]:
                ncnt = cnt - guess[(u,v)] + guess[(v,u)]
                if ncnt>=k:
                    ans += 1
                dfs(v, ncnt)
        dfs(0, cnt)
        return ans


sol = Solution()
result = [
    # sol.splitNum(num = 4325),
    # sol.splitNum(num = 687),
    # sol.coloredCells(1),
    # sol.coloredCells(2),
    # sol.coloredCells(3),
    # sol.countWays(ranges = [[1,3],[10,20],[2,5],[4,8]]),
    # sol.countWays(ranges = [[6,10],[5,15]]),
    sol.rootCount(edges = [[0,1],[1,2],[1,3],[4,2]], guesses = [[1,3],[0,1],[1,0],[2,4]], k = 3),
    sol.rootCount(edges = [[0,1],[1,2],[2,3],[3,4]], guesses = [[1,0],[3,4],[2,1],[3,2]], k = 1),
]
for r in result:
    print(r)
