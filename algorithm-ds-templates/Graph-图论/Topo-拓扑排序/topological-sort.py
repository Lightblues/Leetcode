from easonsi import utils
from easonsi.util.leetcode import * 

""" 拓扑排序
https://oi-wiki.org/graph/topo/


0207. 课程表 #medium 一组课程有依赖关系, 问是否能完成
    思路1: 基本的 #拓扑排序 模版题
0210. 课程表 II #medium 相较于上一题需要返回拓扑排序的顺序
2050. 并行课程 III #hard #题型
    课程之间存在DAG依赖关系, 每个课程修习需要一定的月份, 前序依赖满足的情况下, 不同课程可以同时修习. 求完成所有可能的最小时间.
    在遍历的过程中记录每个节点的timeLimit, 这样, 遍历每一条边的时候, 可以更新 `timeLimit[v]` 为 max(timeLimit[v], timeLimie[u]+time[v])`
2392. 给定条件下构造矩阵 #hard #题型
    给定一个k, 要求构造 k*k 的矩阵, 填充 1~k 共k个数字, 其他位置填0. 要求满足行/列约束. 约束的形式是, 给定一组 (i,j), 要求数字i所在行应该在j所在行的上面. 限制: k 400, 约束数量 n 1e4
    思路1: 实际上就是一个 #拓扑排序. 分解行列的约束
    
1857. 有向图中最大颜色值 #hard
    给定一张图 (可认定为是 DAG), 每个节点有一个颜色. 对于每一条路径, 定义其值为相同颜色数量的最大值. 要求计算图上路径分数的最大值.
    如何记录分数? 对于每一个节点记录「以该节点结束的路径中, 各个颜色的最大值」, 根据上一个节点进行状态转移.


5970. 参加会议的最多员工数 #hard #题型 #基环树 #hardhard [基环树]
    每个人只有一个喜欢的人, 要求安排坐圆桌, 每个人左右要有他喜欢的人, 最大的可安排人数
"""
class Solution:
    """ 0207. 课程表 #medium 一组课程有依赖关系, 问是否能完成
思路1: 基本的 #拓扑排序 模版题
     """
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        inD = [0] * numCourses
        outG = [set() for _ in range(numCourses)]
        for i,pre in prerequisites:
            inD[i] += 1
            outG[pre].add(i)
        q = [i for i,d in enumerate(inD) if d==0]
        cnt = len(q)
        while q:
            u = q.pop()
            for v in outG[u]:
                inD[v] -= 1
                if inD[v] == 0:
                    q.append(v)
                    cnt += 1
        return cnt == numCourses

    """ 0210. 课程表 II #medium 相较于上一题需要返回拓扑排序的顺序 """
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        inD = [0] * numCourses
        outG = [set() for _ in range(numCourses)]
        for i,pre in prerequisites:
            inD[i] += 1
            outG[pre].add(i)
        q = [i for i,d in enumerate(inD) if d==0]
        cnt = len(q)
        ans = []
        while q:
            u = q.pop()
            ans.append(u)
            for v in outG[u]:
                inD[v] -= 1
                if inD[v] == 0:
                    q.append(v)
                    cnt += 1
        return ans if cnt == numCourses else []

    """ 2050. 并行课程 III #hard #题型
课程之间存在DAG依赖关系, 每个课程修习需要一定的月份, 前序依赖满足的情况下, 不同课程可以同时修习. 求完成所有可能的最小时间.
复杂度: 节点/边数量 5e4, 
思路1: #拓扑排序 在遍历的过程中记录每个节点的timeLimit, 这样, 遍历每一条边的时候, 可以更新 `timeLimit[v]` 为 max(timeLimit[v], timeLimie[u]+time[v])`
"""
    def minimumTime(self, n: int, relations: List[List[int]], time: List[int]) -> int:
        degrees = [0] * n   # in degree
        timeLimit  = time[:]
        g = [[] for _ in range(n)]
        for u, v in relations:
            g[u-1].append(v-1)
            degrees[v-1] += 1
        
        q = collections.deque([i for i,d in enumerate(degrees) if d==0])
        while q:
            u = q.popleft()
            t = timeLimit[u]
            for v in g[u]:
                degrees[v] -= 1
                timeLimit[v] = max(timeLimit[v], t+time[v])
                if degrees[v] == 0:
                    q.append(v)
        return max(timeLimit)
    

    """ 2392. 给定条件下构造矩阵 #hard #题型
给定一个k, 要求构造 k*k 的矩阵, 填充 1~k 共k个数字, 其他位置填0. 要求满足行/列约束. 约束的形式是, 给定一组 (i,j), 要求数字i所在行应该在j所在行的上面. 限制: k 400, 约束数量 n 1e4
思路0: 一开始看到约束条件想到 #CSP 问题, 但一想约束满足问题的搜索复杂度似乎不够? 没想清楚
思路1: 实际上就是一个 #拓扑排序. 
    分解行/列的约束条件, 每一个可以通过拓扑排序求解
"""
    def buildMatrix(self, k: int, rowConditions: List[List[int]], colConditions: List[List[int]]) -> List[List[int]]:
        def f(conditions):
            # 拓扑排序
            # 构图
            nout = [0] * k
            nins = [[] for _ in range(k)]
            for u,v in conditions:
                u,v = u-1,v-1
                nout[u] += 1
                nins[v].append(u)
            # 拓扑排序
            zero = deque([i for i in range(k) if nout[i]==0])
            ans = list(zero)
            while zero:
                v = zero.popleft()
                for u in nins[v]:
                    nout[u] -= 1
                    if nout[u]==0:
                        zero.append(u)
                        ans.append(u)
            if len(ans)!=k: return []
            return [i+1 for i in ans[::-1]]
        rows, cols = f(rowConditions), f(colConditions)
        if not rows or not cols: return []
        # 综合行列约束
        ans = [[0] * k for _ in range(k)]
        n2row = {rows[i]:i for i in range(k)}
        n2col = {cols[i]:i for i in range(k)}
        for i in range(1, k+1):
            ans[n2row[i]][n2col[i]] = i
        return ans

    """ 1857. 有向图中最大颜色值 #hard #题型 #DAG #拓扑排序 #DP
给定一张图 (可认定为是 DAG), 每个节点有一个颜色. 对于每一条路径, 定义其值为相同颜色数量的最大值. 要求计算图上路径的最大值.
若图上出现环, 则返回 -1.
思路1: #拓扑排序
    状态转移: 如何记录路径上的(最大)节点数量? 对于每个节点, 用一个数组记录以该节点终止的所有路径上, 各个颜色的最大值.
    更新公式: 对于 (u,v) 边, 其每一个颜色的更新值为 `colorNode[u][color] + (color==colors[v])` 也即上一个邻居点的值, 加上是否为v的颜色.
    如何判断是否有环? 拓扑排序是否遍历了所有节点
链接：https://leetcode.cn/problems/largest-color-value-in-a-directed-graph
"""
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        # 边界: 边数为 0
        if len(edges)==0: return 1
        
        # 将字母形式的颜色转为数字
        colors = [ord(c) - ord('a') for c in colors]
        # 节点数量
        n = len(colors)
        degrees = [0] * n # 入度
        colorNode = [[0] * 26 for _ in range(n)]   # 对于每个节点, 用一个数组记录以该节点终止的所有路径上, 各个颜色的最大值
        g = [[] for _ in range(n)]
        for u,v in edges:
            degrees[v] += 1
            g[u].append(v)
            
        ans = 0
        q = collections.deque([i for i,d in enumerate(degrees) if d==0])
        # visited 记录访问过的节点数量, 若其 != 总的节点数, 说明图上有环!
        visited = len(q)
        for i in q:
            colorNode[i][colors[i]] += 1
        while q:
            u = q.popleft()
            for v in g[u]:
                degrees[v] -= 1
                for i in range(26):
                    if i==colors[v]:
                        colorNode[v][i] = max(colorNode[u][i]+1, colorNode[v][i])
                        ans = max(ans,colorNode[v][i])
                    else:
                        colorNode[v][i] = max(colorNode[u][i], colorNode[v][i])
                if degrees[v] == 0:
                    q.append(v)
                    visited += 1
        if visited!=n: return -1
        return ans
    


sol = Solution()
result = [
    # sol.largestPathValue(colors = "abaca", edges = [[0,1],[0,2],[2,3],[3,4]]),
    # sol.largestPathValue(colors = "a", edges = [[0,0]]),
    sol.canFinish(numCourses = 2, prerequisites = [[1,0]]),
    sol.canFinish(numCourses = 2, prerequisites = [[1,0],[0,1]]),
]
for r in result:
    print(r)
