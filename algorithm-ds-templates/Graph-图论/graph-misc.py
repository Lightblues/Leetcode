from easonsi import utils
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
== #基环树 (pseudotree)
[灵神](https://leetcode-cn.com/problems/maximum-employees-to-be-invited-to-a-meeting/solution/nei-xiang-ji-huan-shu-tuo-bu-pai-xu-fen-c1i1b/)
5970. 参加会议的最多员工数 #hard #题型 #基环树 #hardhard
    每个人只有一个喜欢的人, 要求安排坐圆桌, 每个人左右之一要有他喜欢的人, 最大的可安排人数
    可知喜欢的人构成基环树; 除了求最长的圆, 要注意特殊情况: 当环的长度为2时, 其可以向两侧「伸展」树枝, 并且两侧的人都已满足条件, 因此可以将这些情况拼接起来.
6135. 图中的最长环 #hard
    给一张有向图, 每个节点至多有一条出边 (基环树). 找到图上出现的最长环.
    除了上面的拓扑排序剪枝, 还有一种简单的方式是利用 #时间戳 来记录当前尝试找环的起始状态
6134. 找到离给定两个节点最近的节点 #medium
    给一张有向图, 每个节点至多有一条出边 (基环树). 找到某一节点, 使得给定的两个节点node1, node2都能到达并且距离最短. 
    直接找出两个点可达的所有点的(最短)距离, 两者都可达的条件是两个距离值的最大值非inf; 因此, **对于所有的最大值取最小值即可**.





@2022 """
class Solution:
    """ 
5970. 参加会议的最多员工数 #hard #题型 #基环树 #hardhard
    每个人只有一个喜欢的人, 要求安排坐圆桌, 每个人左右要有他喜欢的人, 最大的可安排人数
    比较容易想到, 问题主要转化为求这样的有向图上的最大环,
        **特殊情况** 是两个互相喜欢的人, 他们相互满足了要求, 因此左右可以有一条「喜欢人的链」, 并且左右的人都是满足的; 因此, 这种大小为 2 的环一个桌上可以安排多个
        参见 [灵神](https://leetcode-cn.com/problems/maximum-employees-to-be-invited-to-a-meeting/solution/nei-xiang-ji-huan-shu-tuo-bu-pai-xu-fen-c1i1b/), 这种图叫做 内向 #基环树 (pseudotree)
    所以核心问题在于如何在 pseudotree 中找环, 比赛中的尝试没有想到如何「**剪枝**」超时了; 实际上, 可以通过一次 #拓扑排序 剪掉所有的分支 (最后留在图上的点的度数均为 1)
        具体实现上, 维护一个入度为 0 的队列, 对其喜欢的人的入度 -1, 如果减到了 0 则继续加入队列;
        这样, **拓扑排序后最终剩下的点都是成环的** (入度为 1).
"""
    def maximumInvitations(self, favorite: List[int]) -> int:
        # from 灵神, 更精简
        n = len(favorite)
        deg = [0] * n
        for u in favorite: deg[u]+= 1
        # 每条分支出发的最长路径. 注意环上的其他节点仍为初始值 -1
        max_depth = [0] * n
        q = collections.deque(i for i,degree in enumerate(deg) if degree ==0)
        # 拓扑排序, 并计算每个点的最大深度. 对于一条 (u->v)边而言, 由于是拓扑排序,u的深度一定先计算, 然后用来对v的深度更新 (注意指向v的可能有多条边)
        while q:
            u = q.popleft()
            max_depth[u] += 1
            v = favorite[u]
            max_depth[v] = max(max_depth[v], max_depth[u]) # 注意这里不需要 +1 !!! 因为深度更新是在 pop 的时候 +1 的
            deg[v] -= 1
            if deg[v]==0: q.append(v)
        max_ring_size, sum_chain_size = 0, 0
        for i,d in enumerate(deg):
            # 非环
            if d==0: continue
            # 遍历环
            deg[i] = 0 # 标记已访问
            ring_size = 1
            v = favorite[i]
            while v!=i:
                ring_size += 1
                deg[v] = 0
                v = favorite[v]
            # 1) 长2
            if ring_size==2:
                sum_chain_size += max_depth[i] + max_depth[favorite[v]] + 2   # 注意环上的点没有算上自己的深度!!!
            else:
                max_ring_size = max(max_ring_size, ring_size)
        return max(max_ring_size, sum_chain_size)

    """ 6135. 图中的最长环 #hard
给一张有向图, 每个节点至多有一条出边. 找到图上出现的最长环.
限制: 节点数量 1e5
思路2: 事实上是「5970. 参加会议的最多员工数」的一个子问题.
    上题用了拓扑排序将分枝都剪掉了. 除了这一做法, [灵神](https://leetcode.cn/problems/longest-cycle-in-a-graph/solution/nei-xiang-ji-huan-shu-zhao-huan-li-yong-pmqmr/) 介绍了利用 #时间戳 来解的思路
    用一个全局clock记录一次的遍历顺序. 每次从某点尝试找环的时候, 记录开始时间, 则在while循环中, 若 **找到一个节点是时间戳不小于开始时间**, 说明成环!
反思: 一开始也想歪了, 还乱用 SortedList
"""
    def longestCycle(self, edges: List[int]) -> int:
        # 思路2  #时间戳
        time = [0] * len(edges)
        clock = 1
        ans = -1
        for x,t in enumerate(time):
            # 还可以动态enumerate? 高级
            if t: continue
            startTime = clock
            while x>=0:
                if time[x]: # 重复访问节点了
                    if time[x]>=startTime:
                        # 找到环
                        ans = max(ans, clock-time[x])
                    break
                time[x] = clock
                clock += 1
                x = edges[x]
        return ans
    
    """ 6134. 找到离给定两个节点最近的节点 #medium
给一张有向图, 每个节点至多有一条出边. 找到某一节点, 使得给定的两个节点node1, node2都能到达并且距离最短. 
注意: 1) 若距离相等, 则返回较小的那个节点. 2) 可能成环
限制: 节点数量 1e5
思路2: 一种更为简单的方式是, 直接找出两个点可达的所有点的(最短)距离, 两者都可达的条件是两个距离值的最大值非inf; 因此, **对于所有的最大值取最小值即可**.
    from [灵神](https://leetcode.cn/problems/find-closest-node-to-given-two-nodes/solution/ji-suan-dao-mei-ge-dian-de-ju-chi-python-gr2u/)
"""
    def closestMeetingNode(self, edges: List[int], node1: int, node2: int) -> int:
        # 思路2
        n = len(edges)
        def f(v):
            # 计算v点到其他点的距离
            dis = [inf] * n
            d = 0
            while v!=-1 and dis[v]==inf:
                dis[v] = d
                d += 1
                v = edges[v]
            return dis
        dis1, dis2 = f(node1), f(node2)
        # ans = min(map(max, zip(dis1, dis2)))
        # return -1 if ans==inf else ans
        ans = -1; d = inf
        for i,d1,d2 in zip(range(n), dis1,dis2):
            if max(d1,d2) < d:
                ans = i; d = max(d1,d2)
        return ans

    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
