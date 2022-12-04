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
https://leetcode.cn/contest/weekly-contest-322


@2022 """
class Solution:
    """ 6253. 回环句 """
    def isCircularSentence(self, sentence: str) -> bool:
        words = sentence.split()
        if len(words)==1:
            return sentence[0]==sentence[-1]
        for i in range(len(words)-1):
            if words[i][-1] != words[i+1][0]:
                return False
            if words[-1][-1] != words[0][0]: return False
        return True
    
    """ 6254. 划分技能点相等的团队 """
    def dividePlayers(self, skill: List[int]) -> int:
        skill.sort()
        ans = 0
        n = len(skill)
        target = sum(skill) / (n//2)
        for i in range(n//2):
            if skill[i]+skill[n-1-i] != target:
                return -1
            ans += skill[i]*skill[n-1-i]
        return ans
    
    """ 6255. 两个城市间路径的最小分数 #medium 等价问题: 找到编号为1的节点所在的连通分量中, 权重最小的边
思路1: 从该节点出发DFS
"""
    def minScore(self, n: int, roads: List[List[int]]) -> int:
        # 构建图
        g = [[] for _ in range(n)]
        for u,v,w in roads:
            u,v = u-1,v-1
            g[u].append((v,w))
            g[v].append((u,w))
        # 通过 dfs, 找到 0 节点所在的连通分量中的最小边
        visited = [False]*n # 防止重复访问
        mn = inf
        def dfs(u):
            # DFS基本框架
            nonlocal mn
            for v,w in g[u]:
                mn = min(mn, w)
                if visited[v]: continue
                visited[v] = True
                dfs(v)  # 递归调用
        dfs(0)
        return mn

    """ 6256. 将节点分成尽可能多的组 #hard 对于一个图, 对于其中的节点分组, 要求每一条边所连接的两个点的组号都相差1. 求最多能分成多少组 (不能完成则返回 -1). 限制: n 500. 边的数量 1e4
思路0: 尝试计算节点之间的两两距离 (Floyd)
    考虑特殊情况: 1) 星状结构, 节点0连了其他所有点; 2) 环结构; 3) 链结构. 
    然后怎么进行搜索? 失败的想法: 节点0取坐标0, 然后依次对于距离为1的节点进行赋值, 同时考虑已赋值节点的距离约束.
    """
    def magnificentSets(self, n: int, edges: List[List[int]]) -> int:
        edges = [[i-1 for i in e] for e in edges]
        # Floyd
        d = [[inf] * n for _ in range(n)]
        for i in range(n):
            d[i][i] = 0
        for u, v in edges:
            d[u][v] = d[v][u] = 1
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    d[i][j] = min(d[i][j], d[i][k] + d[k][j])
        # 写不来的搜索...
        assign = [-1] * n
        q = []
        def f(u):
            locu = assign[u]
            toAssign = [i for i,dist in enumerate(d[u]) if dist==1 and assign[i]==-1]
            
sol = Solution()
result = [
    # sol.dividePlayers(skill = [3,2,5,1,3,4]),
    # sol.dividePlayers([3,4]),
    # sol.dividePlayers([1,1,2,3]),
    sol.minScore(n = 4, roads = [[1,2,9],[2,3,6],[2,4,5],[1,4,7]]),
    sol.minScore(n = 4, roads = [[1,2,2],[1,3,4],[3,4,7]]),
]
for r in result:
    print(r)
