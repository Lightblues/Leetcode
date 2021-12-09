from typing import List
from collections import defaultdict, deque
import heapq
import random

class Solution:

    """ 332. 重新安排行程 机票行程重排列, 要求首尾相连, 欧拉通路
所有这些机票都属于一个从 JFK（肯尼迪国际机场）出发的先生，所以该行程必须从 JFK 开始。如果存在多种有效的行程，请你按字典排序返回最小的行程组合。"""
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        edges = defaultdict(list)
        for s,d in tickets:
            edges[s].append(d)
        for k in edges.keys():
            edges[k].sort()
        result = []
        # Hierholzer 算法 求解欧拉通路
        def dfs(u):
            while edges[u]:
                v = edges[u].pop(0)     # 尽量去排序较小的机场
                dfs(v)
                result.append(v)
        dfs('JFK')
        return ['JFK'] + result[::-1]
    # from https://leetcode-cn.com/problems/reconstruct-itinerary/solution/zhong-xin-an-pai-xing-cheng-by-leetcode-solution/
    # 思路一致, 这里用了 heapq
    def findItinerary2(self, tickets: List[List[str]]) -> List[str]:
        def dfs(curr: str):
            while vec[curr]:
                tmp = heapq.heappop(vec[curr])
                dfs(tmp)
                stack.append(curr)
        vec = defaultdict(list)
        for depart, arrive in tickets:
            vec[depart].append(arrive)
        for key in vec:
            heapq.heapify(vec[key])     # 利用最小堆保存数据
        stack = list()
        dfs('JFK')
        return stack[::-1]

    """ 753. 破解保险箱
密码是 n 位数, 密码的每一位是 k 位序列 0, 1, ..., k-1 中的一个 。
返回一个最短字符串, 其子字符串包括所有可能的密码. 
关键在于将其转化为一个规范的欧拉通路问题: see [here](https://leetcode-cn.com/problems/cracking-the-safe/solution/po-jie-bao-xian-xiang-by-leetcode-solution/) 官方解答有点fancy

简言之, 要求的是 n 长序列, 都可将其看成 n-1长序列加上 0~k-1 的数字. 因此, 可以构建一个图, 节点为所有的 n-1长序列, 其第i个出边就是在最后加上数字i并去除第一位数字, 跳到相应的节点上. 
例如, 节点u的第v的出边就跳转到数值为 u*k % (k**(n-1)) + v 的节点上. 
可知, 这样构造的图, 每个节点都有 k条出边和入边, 共可代表 $k^{n-1} * k$ 个不同的数字, 正好对应了所有可能的密码.
显然, 这张图是欧拉图, 可基于一个欧拉回路对应一个题目所要求的字符串. 
 """
    def crackSafe(self, n: int, k: int) -> str:
        edges = defaultdict(list)
        for i in range(k**(n-1)):
            edges[i] = list(range(k))
        result = []
        def dfs(u):
            while edges[u]:
                v = edges[u].pop()
                dfs(u*k % (k**(n-1)) + v)
                result.append(str(v))
        dfs(0)
        result = result[::-1]
        return "0"*(n-1) + ''.join(result)

sol = Solution()
results = [
    sol.findAllPeople(4, [[3,1,3],[1,2,2],[0,3,3]], 3),
    sol.findAllPeople2(6, [[1,2,5],[2,3,8],[1,5,10]], 1),
    sol.findAllPeople2(4, [[3,1,3],[1,2,2],[0,3,3]], 3),
    
    # sol.findItinerary([["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]),
    # sol.findItinerary2([["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]])

    # sol.crackSafe(1,2),
    # sol.crackSafe(2,2)
]
for r in results:
    print(r)

