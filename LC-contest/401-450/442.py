from typing import *
import heapq

""" 
https://leetcode.cn/contest/weekly-contest-442

Easonsi @2025 """
class Solution:
    """ 3492. 船上可以装载的最大集装箱数量 """
    def maxContainers(self, n: int, w: int, maxWeight: int) -> int:
        return min(n**2, maxWeight//w)

    """ 3493. 属性图 """
    def numberOfComponents(self, properties: List[List[int]], k: int) -> int:
        n = len(properties)
        g = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i+1,n):
                if len(set(properties[i]) & set(properties[j])) >= k:
                    g[i].append(j)
                    g[j].append(i)
        # 
        vis = [False]*n
        def dfs(u):
            vis[u] = True
            for v in g[u]:
                if not vis[v]:
                    dfs(v)
        ans = 0
        for i in range(n):
            if not vis[i]:
                ans += 1
                dfs(i)
        return ans
    

    """ 3494. 酿造药水需要的最少总时间 #medium 有n个巫师能力值为skill[i], 给定 """
    def minTime(self, skill: List[int], mana: List[int]) -> int:

sol = Solution()
result = [
    sol.numberOfComponents(properties = [[1,2],[1,1],[3,4],[4,5],[5,6],[7,7]], k = 1),
]
for r in result:
    print(r)
