from typing import List
import collections
import random
# collections.deque

class Solution274:
    """ 2124. 检查是否所有 A 都在 B 之前 """
    def checkString(self, s: str) -> bool:
        hasB = False
        for char in s:
            if char == 'a' and hasB:
                return False
            elif char == 'b':
                hasB = True
        return True

    """ 2125. 银行中的激光束数量
 """
    def numberOfBeams(self, bank: List[str]) -> int:
        result = 0
        last1 = 0
        for line in bank:
            num1 = line.count('1')
            if num1 != 0:
                if last1 != 0:
                    result += last1*num1
                last1 = num1
        return result

    """ 2126. 摧毁小行星 """
    def asteroidsDestroyed(self, mass: int, asteroids: List[int]) -> bool:
        asteroids.sort()
        for ast in asteroids:
            if mass < ast:
                return False
            mass += ast
        return True

    """ 
- 5970. 参加会议的最多员工数 #hard #题型 #基环树 #hardhard
    - 每个人只有一个喜欢的人, 要求安排坐圆桌, 每个人左右要有他喜欢的人, 最大的可安排人数
    - 比较容易想到, 问题主要转化为求这样的有向图上的最大环,
        - **特殊情况** 是两个互相喜欢的人, 他们相互满足了要求, 因此左右可以有一条「喜欢人的链」, 并且左右的人都是满足的; 因此, 这种大小为 2 的环一个桌上可以安排多个
        - 参见 [灵神](https://leetcode-cn.com/problems/maximum-employees-to-be-invited-to-a-meeting/solution/nei-xiang-ji-huan-shu-tuo-bu-pai-xu-fen-c1i1b/), 这种图叫做 内向 #基环树 (pseudotree)
    - 所以核心问题在于如何在 pseudotree 中找环, 比赛中的尝试没有想到如何「**剪枝**」超时了; 实际上, 可以通过一次 #拓扑排序 剪掉所有的分支 (最后留在图上的点的度数均为 1)
        - 具体实现上, 维护一个入度为 0 的队列, 对其喜欢的人的入度 -1, 如果减到了 0 则继续加入队列;
        - 这样, **拓扑排序后最终剩下的点都是成环的** (入度为 1).
 """
    def maximumInvitations(self, favorite: List[int]) -> int:
        """ 很早自己写的版本, 完全没考虑复杂度, 显然会超时!
         """
        # revG
        beLoved = collections.defaultdict(list)
        for i, love in enumerate(favorite):
            beLoved[love].append(i)
        
        possibleStart = set([k for k,v in beLoved.items() if len(v)>0])
        def findCircle(start):
            nodes = set([start])
            now = favorite[start]
            while now!=start:
                if now in nodes:
                    return None
                nodes.add(now)
                now = favorite[now]
            # now == start, find circle
            return nodes
        circles = []
        while possibleStart:
            s = random.choice(tuple(possibleStart))
            rr = findCircle(s)
            if rr != None:
                circles.append(rr)
                possibleStart -= rr
            else:
                possibleStart.remove(s)
        # result = max(len(c) for c in circles)
        # if result>2:
        #     return result
        # for pair in circles:
        #     p1,p2 = list(pair)
        #     if len(beLoved[p1])>1 or len(beLoved[p2])>1:
        #         return 3
        # return 2

        def dfsFindLoveChain(x, chainLen=0):
            if beLoved[x]:
                results = []
                for lover in beLoved[x]:
                    results.append(dfsFindLoveChain(lover, chainLen+1))
                return max(results)
            return chainLen
        # result = []
        # for c in circles:
        #     if len(c)>2:
        #         result.append(len(c))
        #     else:
        #         p1,p2 = list(c)
        #         beLoved[p1].remove(p2)
        #         beLoved[p2].remove(p1)
        #         len1 = dfsFindLoveChain(p1)
        #         len2 = dfsFindLoveChain(p2)
        #         result.append(len1+len2+2)

        # 比较特殊的
        circles2 = []
        results = []
        for c in circles:
            if len(c)>2:
                results.append(len(c))
            else:
                circles2.append(list(c))
        cumsum2 = 0
        for p1,p2 in circles2:
            beLoved[p1].remove(p2)
            beLoved[p2].remove(p1)
            len1 = dfsFindLoveChain(p1)
            len2 = dfsFindLoveChain(p2)
            cumsum2 += len1 + len2 + 2
        results.append(cumsum2)
        return max(results)

    def maximumInvitations(self, favorite: List[int]) -> int:
        # 参考了 [灵神](https://leetcode-cn.com/problems/maximum-employees-to-be-invited-to-a-meeting/solution/nei-xiang-ji-huan-shu-tuo-bu-pai-xu-fen-c1i1b/)
        n = len(favorite)
        revG = [[] for _ in range(n)]   # 喜欢 i 的员工列表
        inDegree = [0] * n               # 入度
        #  建图
        for u,v in enumerate(favorite):
            revG[v].append(u)
            inDegree[v] += 1
        # 拓扑排序，剪掉图 g 上的所有树枝
        q = collections.deque(i for i,degree in enumerate(inDegree) if degree ==0)
        while q:
            u = q.popleft()
            v = favorite[u]
            inDegree[v] -= 1
            if inDegree[v]==0:
                q.append(v)
        # 寻找图 g 上的基环
        possibleNodes = set([i for i,degree in enumerate(inDegree) if degree>0])
        rings = []
        def findCircle(x) -> set:
            nodes = set([x])
            now = favorite[x]
            while now != x:
                if now in nodes:
                    return None
                nodes.add(now)
                now = favorite[now]
            return nodes
        while possibleNodes:
            start = random.choice(tuple(possibleNodes))
            cc = findCircle(start)
            if cc:
                possibleNodes -= cc
                rings.append(cc)
        # 通过反图 rg 寻找树枝上最深的链
        def dfsFindLoveChain(x, chainLen=0):
            if revG[x]:
                results = []
                for lover in revG[x]:
                    results.append(dfsFindLoveChain(lover, chainLen+1))
                return max(results)
            return chainLen
        # 
        circles2 = []       # 大小为2的环
        results = []
        for c in rings:
            if len(c)>2:
                results.append(len(c))
            else:
                circles2.append(list(c))
        cumsum2 = 0
        for p1,p2 in circles2:
            revG[p1].remove(p2)
            revG[p2].remove(p1)
            len1 = dfsFindLoveChain(p1)
            len2 = dfsFindLoveChain(p2)
            cumsum2 += len1 + len2 + 2
        results.append(cumsum2)
        return max(results)

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


sol = Solution274()

print(
    # sol.maximumInvitations(favorite = [3,0,1,4,1]),
    # sol.maximumInvitations(favorite = [1,2,0]),
    sol.maximumInvitations(favorite = [2,2,1,2]),
    sol.maximumInvitations([1,0,0,2,1,4,7,8,9,6,7,10,8]),  # 6
    sol.maximumInvitations([1,0,3,2,5,6,7,4,9,8,11,10,11,12,10]),  # 11
    sol.maximumInvitations([7,0,7,13,11,6,8,5,9,8,9,14,15,7,11,6]) # 11
)