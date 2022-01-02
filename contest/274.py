from typing import List
import collections
import random
# collections.deque

class Solution274:
    def checkString(self, s: str) -> bool:
        hasB = False
        for char in s:
            if char == 'a' and hasB:
                return False
            elif char == 'b':
                hasB = True
        return True

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

    def asteroidsDestroyed(self, mass: int, asteroids: List[int]) -> bool:
        asteroids.sort()
        for ast in asteroids:
            if mass < ast:
                return False
            mass += ast
        return True

    """ 5970. 参加会议的最多员工数
一个公司准备组织一场会议，邀请名单上有 n 位员工。公司准备了一张 圆形 的桌子，可以坐下 任意数目 的员工。
员工编号为 0 到 n - 1 。每位员工都有一位 喜欢 的员工，每位员工 当且仅当 他被安排在喜欢员工的旁边，他才会参加会议。每位员工喜欢的员工 不会 是他自己。
给你一个下标从 0 开始的整数数组 favorite ，其中 favorite[i] 表示第 i 位员工喜欢的员工。请你返回参加会议的 最多员工数目 。
 """
    # 这里超时了, 主要是 findCircle 复杂度不确定, 例如对一个 拖着很多长链的环而言, 失败的概率太高了
    def maximumInvitations(self, favorite: List[int]) -> int:
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

    def maximumInvitations2(self, favorite: List[int]) -> int:
        n = len(favorite)
        graph = [[] for _ in range(n)]  # 喜欢 i 的员工列表
        degrees = [0] * n
        #  建图
        for u,v in enumerate(favorite):
            graph[v].append(u)
            degrees[v] += 1
        # 拓扑排序，剪掉图 g 上的所有树枝
        # 这题的关键点在这里 !!!
        q = collections.deque(i for i,degree in enumerate(degrees) if degree ==0)
        while q:
            u = q.popleft()
            v = favorite[u]
            degrees[v] -= 1
            if degrees[v]==0:
                q.append(v)
        # 寻找图 g 上的基环
        possibleNodes = set([i for i,degree in enumerate(degrees) if degree>0])
        rings = []
        def findCircle(x):
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
            if graph[x]:
                results = []
                for lover in graph[x]:
                    results.append(dfsFindLoveChain(lover, chainLen+1))
                return max(results)
            return chainLen
        # 
        circles2 = []
        results = []
        for c in rings:
            if len(c)>2:
                results.append(len(c))
            else:
                circles2.append(list(c))
        cumsum2 = 0
        for p1,p2 in circles2:
            graph[p1].remove(p2)
            graph[p2].remove(p1)
            len1 = dfsFindLoveChain(p1)
            len2 = dfsFindLoveChain(p2)
            cumsum2 += len1 + len2 + 2
        results.append(cumsum2)
        return max(results)


sol = Solution274()

print(
    # sol.maximumInvitations(favorite = [3,0,1,4,1]),
    # sol.maximumInvitations(favorite = [1,2,0]),
    # sol.maximumInvitations(favorite = [2,2,1,2])
    sol.maximumInvitations2([1,0,0,2,1,4,7,8,9,6,7,10,8]),  # 6
    sol.maximumInvitations2([1,0,3,2,5,6,7,4,9,8,11,10,11,12,10]),  # 11
    sol.maximumInvitations2([7,0,7,13,11,6,8,5,9,8,9,14,15,7,11,6]) # 11
)