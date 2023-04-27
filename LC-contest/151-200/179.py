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
https://leetcode.cn/contest/weekly-contest-179

手速场. 不过T4的边界需要仔细考虑.

@2022 """
class Solution:
    """ 1374. 生成每种字符都是奇数个的字符串 """
    
    """ 1375. 二进制字符串前缀一致的次数 """
    def numTimesAllBlue(self, flips: List[int]) -> int:
        ret = 0
        mx = 0
        for i,f in enumerate(flips):
            mx = max(mx, f)
            if mx == i+1:
                ret += 1
        return ret
    
    """ 1376. 通知所有员工所需的时间 #medium 基本 DFS """
    def numOfMinutes(self, n: int, headID: int, manager: List[int], informTime: List[int]) -> int:
        g = [[] for _ in range(n)]
        root = -1
        for i,m in enumerate(manager):
            if m==-1: root = i; continue
            g[m].append(i)
        def dfs(r, t=0):
            if not g[r]: return t
            t += informTime[r]
            ret = t
            for c in g[r]:
                ret = max(ret, dfs(c, t))
            return ret
        return dfs(root)
    
    """ 1377. T 秒后青蛙的位置 #hard 有n个节点构成一棵无向树, 青蛙从节点1开始跳, 问经过t秒后停留在节点target上的概率
跳跃的逻辑: 不能跳到历史节点, 在其他邻居节点中等概率, 到达叶子节点后不能再跳. 限制: n 100; t 50
思路1: #DFS. 从根节点开始遍历, 累计概率.
    细节: 注意「停留在点target的条件」: 1) 刚好t步跳到该节点, 2) 或者t步之前到达叶子节点target.
"""
    def frogPosition(self, n: int, edges: List[List[int]], t: int, target: int) -> float:
        g = [[] for _ in range(n+1)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        vis = [False]*(n+1)
        def dfs(node, depth, revp):
            # 从根节点出发, 遍历当前深度为 depth的节点. revp为当前节点的概率 (为了避免浮点数取反)
            vis[node] = True
            # 终止
            if depth > t: return 0
            # 遇到了target: 需要检查, 若有其他可跳的节点, 需要进行判断
            if node==target:
                if depth==t: return revp
                # 否则, 只有在叶子节点才能停留
                nchild = len([c for c in g[node] if not vis[c]])
                return revp if nchild==0 else 0
            # 继续遍历
            nchild = len([c for c in g[node] if not vis[c]])
            for child in g[node]:
                if vis[child]: continue
                ret = dfs(child, depth+1, revp*nchild)
                if ret>0: return ret
            return 0
        ret = dfs(1, 0, 1)
        return 1/ret if ret else 0
    
sol = Solution()
result = [
    # sol.numTimesAllBlue([3,2,4,1,5]),
    sol.frogPosition(n = 7, edges = [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], t = 1, target = 7),
    sol.frogPosition(n = 7, edges = [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], t = 2, target = 4),
    sol.frogPosition(7, [[1,2],[1,3],[1,7],[2,4],[2,6],[3,5]], 20,6),
    sol.frogPosition(8, [[2,1],[3,2],[4,1],[5,1],[6,4],[7,1],[8,7]], 7,7),
]
for r in result:
    print(r)
