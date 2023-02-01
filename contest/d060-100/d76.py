from easonsi import utils
from easonsi.util.leetcode import *
""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220428 补 """
class Solution:
    """ 2239. 找到最接近 0 的数字 """
    def findClosestNumber(self, nums: List[int]) -> int:
        res = None
        minDist = float('inf')
        for num in nums:
            if abs(num) < minDist:
                minDist = abs(num)
                res = num
            elif abs(num) == minDist:
                res = max(res, num)
        return res

    """ 2240. 买钢笔和铅笔的方案数 """
    def waysToBuyPensPencils(self, total: int, cost1: int, cost2: int) -> int:
        result = 0
        for i in range(total//cost1 + 1):
            result += (total - i*cost1)//cost2 + 1
        return result
    
    """ 2242. 节点序列的最大得分 #hard 给一张带节点权重的无向图, 求长度为4的节点序列的最大得分. 序列之间需要连接, 四个节点不得重复.
复杂度: 节点和边均为 5e4
思路1: 遍历中间两个节点 (边)
    关键看这里的序列长度为4, 因此可以考虑 **遍历中间的两个节点** (边)
进一步降低复杂度: 从边 uv 的两个节点出发, 各拓展出一个节点 a,b; 为了使得分数和最大, 则搜索的 ab 节点权重必然是最大/次大的; 因此, 仅需要对每个节点维护最大的三个邻居即可 (还要考虑 uv 边可能最最大邻居)
在简化了搜索空间的基础上, 可以用 `itertools.product(neighbors(u), neighbors(v))` 直接遍历所有可能的节点对, 而不需要 uv 的邻居进行排序比较等复杂的判断.
参见 [灵神](https://leetcode-cn.com/problems/maximum-score-of-a-node-sequence/solution/by-endlesscheng-dt8h/)
    """
    def maximumScore(self, scores: List[int], edges: List[List[int]]) -> int:
        neighbor_scores = [[] for _ in range(len(scores))]
        for u,v in edges:
            neighbor_scores[u].append((scores[v], v))
            neighbor_scores[v].append((scores[u], u))
        for i in range(len(neighbor_scores)):
            # neighbor_scores[i].sort(reverse=True)[:3]
            neighbor_scores[i] = heapq.nlargest(3, neighbor_scores[i])
        
        ans = -1
        for u,v in edges:
            for (score_a, a), (score_b, b) in itertools.product(neighbor_scores[u], neighbor_scores[v]):
                """ 注意连续的不等比较! Python 只会比较相邻的两个元素
                这里需要满足的条件: 从u节点开始搜索的 a!=v,b, 同理 b!=u,a
                因此, 需要写成连续不等式 u != b != a != v. 下面注释这样写是错的! """
                # if a != u != v != b:
                if u != b != a != v:
                    ans = max(ans, score_a + score_b + scores[u] + scores[v])
        return ans

sol = Solution()
result = [
    # sol.findClosestNumber(nums = [2,-1,1]),
    # sol.waysToBuyPensPencils(total = 20, cost1 = 10, cost2 = 5),
    
    # sol.maximumScore(scores = [5,2,9,8,4], edges = [[0,1],[1,2],[2,3],[0,2],[1,3],[2,4]]),
]
for r in result:
    print(r)


""" 2241. 设计一个 ATM 机器 `medium`
难度不大. 需要写一个类. 通过这题希望写一个函数进行本地调试.
"""
class ATM:
    def __init__(self):
        self.values = [20, 50, 100, 200, 500]
        self.counts = [0] * 5

    def deposit(self, banknotesCount: List[int]) -> None:
        for i,num in enumerate(banknotesCount):
            self.counts[i] += num

    def withdraw(self, amount: int) -> List[int]:
        reversedCount = []
        for v, count in zip(reversed(self.values), reversed(self.counts)):
            a = min(count, amount // v)
            reversedCount.append(a)
            amount -= a * v
        if amount != 0:
            return [-1]
        counts = list(reversed(reversedCount))
        for i,c in enumerate(counts):
            self.counts[i] -= c
        return counts

inputs = """["ATM", "deposit", "withdraw", "deposit", "withdraw", "withdraw"]
[[], [[0,0,1,2,1]], [600], [[0,1,0,1,1]], [600], [550]]"""
methods, args = [eval(l) for l in inputs.split('\n')]
atm = ATM()
for method, arg in list(zip(methods, args))[1:]:
    print(getattr(atm, method)(*arg))
