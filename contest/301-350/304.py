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
https://leetcode.cn/contest/weekly-contest-304
@2022 """
class Solution:
    """ 6132. 使数组中所有元素都等于零 """
    def minimumOperations(self, nums: List[int]) -> int:
        cnt = set(nums)
        return len(cnt) if 0 not in cnt else len(cnt)-1
    
    """ 6133. 分组的最大数量 """
    def maximumGroups(self, grades: List[int]) -> int:
        grades.sort()
        lmx = 0; amx = 0
        acc = 0; alen = 0
        ans = 0
        for i,a in enumerate(grades):
            acc += a; alen += 1
            if alen>lmx and acc>amx:
                amx, lmx = acc, alen
                acc = 0; alen = 0
                ans += 1
        return ans
            
    """ 6134. 找到离给定两个节点最近的节点 #medium
给一张有向图, 每个节点至多有一条出边. 找到某一节点, 使得给定的两个节点node1, node2都能到达并且距离最短. 
注意: 1) 若距离相等, 则返回较小的那个节点. 2) 可能成环
限制: 节点数量 1e5
提示: 由于每个节点最多只有一条出边, 因此 **从某一节点出发, 距离为x的特定节点无环节点只有一个**
思路1: 分别从两个点「同时」开始 #BFS, 判断是否发生重合
    根据提示, 用两个指针表示两节点 (不需要用queue了); 再用两个set记录分别经过的节点 (成环了则终止). 按照层级遍历, 若出现 `q1 in seen2 or q2 in seen1`, 则找到了.
    反思: 之前想简单了: **由于可能有环, 因此不能用一个set来记录两节点遍历的所有点**. 错误的例子 [1,0,-1] 图的情况.
思路2: 一种更为简单的方式是, 直接找出两个点可达的所有点的(最短)距离, 两者都可达的条件是两个距离值的最大值非inf; 因此, **对于所有的最大值取最小值即可**.
    from [灵神](https://leetcode.cn/problems/find-closest-node-to-given-two-nodes/solution/ji-suan-dao-mei-ge-dian-de-ju-chi-python-gr2u/)
"""
    def closestMeetingNode(self, edges: List[int], node1: int, node2: int) -> int:
        # 边界
        if node1==node2: return node1
        
        seen1 = set([node1]); seen2 = set([node2])
        q1 = node1; q2 =node2
        # 用 -1 表示某一节点出发的遍历结束.
        while True:
            # 终止条件
            if q1==q2==-1: break
            # 分别从两个节点出发遍历
            if q1 != -1 and edges[q1] not in seen1:
                q1 = edges[q1]
                if q1!=-1: seen1.add(q1)
            else: q1 = -1
            if q2 != -1 and edges[q2] not in seen2:
                q2 = edges[q2]
                if q2!=-1: seen2.add(q2)
            else: q2 = -1
            # p 记录是否达到目标
            p = []
            if q1 in seen2: p.append(q1)
            if q2 in seen1: p.append(q2)
            if p: return min(p)
        return -1

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


    """ 6135. 图中的最长环 #hard
给一张有向图, 每个节点至多有一条出边. 找到图上出现的最长环.
限制: 节点数量 1e5
思路1: 用一个ava集合记录当前可用的节点. 每次随机选一个出发尝试寻找环.
    DS: 由于出发节点可能不在环上, 因此需要一个path列表来记录遍历过程, 为了快速检查是否经过, 还需要一个pathseen字典. (找到的话, 答案为 `len(path) - path.index(ne)`)
    重复检查: 之前用ava来记录还可用的节点, 但在遍历的过程中如何进行重复判断?  这里需要注意成环点一定会被第二次访问, 因此 **重复检查需要放在环检测之后**!
思路2: 事实上是「5970. 参加会议的最多员工数」的一个子问题.
    上题用了拓扑排序将分枝都剪掉了. 除了这一做法, [灵神](https://leetcode.cn/problems/longest-cycle-in-a-graph/solution/nei-xiang-ji-huan-shu-zhao-huan-li-yong-pmqmr/) 介绍了利用 #时间戳 来解的思路
    用一个全局clock记录一次的遍历顺序. 每次从某点尝试找环的时候, 记录开始时间, 则在while循环中, 若 **找到一个节点是时间戳不小于开始时间**, 说明成环!
反思: 一开始也想歪了, 还乱用 SortedList
"""
    def longestCycle(self, edges: List[int]) -> int:
        # 思路1
        # 当前可用的节点
        ava = set([i for i,e in enumerate(edges) if e!=-1])
        ans = -1
        while ava:
            e = ava.pop()
            # 记录路径和是否出现过.
            path = [e]; pathseen = set([e])
            while edges[e] != -1: #  and edges[e] in ava
                ne = edges[e]
                # 找到环!
                if ne in pathseen:
                    idx = path.index(ne)
                    ans = max(ans, len(path)-idx)
                    break
                path.append(ne); pathseen.add(ne)
                e = ne
                # 重复检查!!! 需要放在环检测之后
                if e not in ava: break
                ava.discard(e)
        return ans
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
    
    
sol = Solution()
result = [
    # sol.minimumOperations(nums = [1,5,0,3,5]),
    # sol.minimumOperations([0]),
    # sol.maximumGroups(grades = [10,6,12,7,3,5]),
    # sol.maximumGroups([8,8]),
    sol.closestMeetingNode(edges = [2,2,3,-1], node1 = 0, node2 = 1),
    sol.closestMeetingNode(edges = [1,2,-1], node1 = 0, node2 = 2),
    sol.closestMeetingNode([5,-1,3,4,5,6,-1,-1,4,3], 0, 0),
    sol.closestMeetingNode([5,4,5,4,3,6,-1], 0, 1),
    sol.closestMeetingNode([4,3,0,5,3,-1], 4, 0),
    # sol.longestCycle(edges = [2,-1,3,1]),
    # sol.longestCycle(edges = [3,3,4,2,3]),
    # sol.longestCycle([3,4,0,2,-1,2]),
]
for r in result:
    print(r)
