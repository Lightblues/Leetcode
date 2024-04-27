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
https://leetcode.cn/contest/weekly-contest-392
难度不大. T4 要求遍历子图的所有边, 体型比较少见
Easonsi @2023 """
class Solution:
    """ 3105. 最长的严格递增或递减子数组 """
    def longestMonotonicSubarray(self, nums: List[int]) -> int:
        ans = 1
        pre=inf; acc=1
        preN=-inf; accN=1
        for i,x in enumerate(nums):
            if x>pre:
                acc += 1
                ans = max(ans, acc)
            else:
                acc = 1
            pre = x
            if x<preN: 
                accN += 1
                ans = max(ans, accN)
            else:
                accN = 1
            preN = x
        return ans
    
    """ 3106. 满足距离约束且字典序最小的字符串 """
    def getSmallestString(self, s: str, k: int) -> str:
        def dist(a,b):
            d = abs(ord(b) - ord(a))
            return min(d, 26-d)
        ans = []
        for i,ch in enumerate(s):
            d = dist('a', ch)
            if d <= k:
                ans.append('a')
                k -= d
            else:
                ch = chr(ord(ch) - k)
                ans.append(ch)
                break
        return ''.join(ans) + s[i+1:]
    
    """ 3107. 使数组中位数等于 K 的最少操作数 """
    def minOperationsToMakeMedianK(self, nums: List[int], k: int) -> int:
        nums.sort()
        n = len(nums)
        idx = n//2
        acc = 0
        if nums[idx] < k:
            for i in range(idx, n):
                if nums[i] >= k: break
                acc += k - nums[i]
        elif nums[idx] > k:
            for i in range(idx, -1, -1):
                if nums[i] <= k: break
                acc += nums[i] - k
        return acc
    
    """ 3108. 带权图里旅途的最小代价 #hard 给定一个带权图, 一条路径的代价是边权AND. 对于一组查询 (s,t), 计算两个点路径代价的最小值. 
NOTE: 一个边/点可以经过很多次, 例如 s->t->1->t
思路1: BFS, 注意要检索所有的边!
[ling](https://leetcode.cn/problems/minimum-cost-walk-in-weighted-graph/solutions/2727290/xian-xing-zuo-fa-dfspythonjavacgo-by-end-i0gg/)
    DFS / 并查集
    """
    def minimumCost(self, n: int, edges: List[List[int]], query: List[List[int]]) -> List[int]:
        g = [[] for _ in range(n)]
        for u,v,w in edges:
            g[u].append((v,w))
            g[v].append((u,w))
        def dfs(u):
            """ 从u出发, 访问子图中所有边AND最小值 """
            if len(g[u])==0:
                return set([u]), 0
            vis = set()
            q = deque([u])
            # AND = (1<<20) - 1  # 11111...1
            AND= -1             # NOTE: 设置为-1 就是 0xFFFFFFFF
            while q:
                u = q.popleft()
                vis.add(u)
                for v,w in g[u]:
                    AND &= w
                    if v not in vis:
                        q.append(v)
            return vis, AND
        m = {}
        group_cnt = 0
        for u in range(n):
            if u in m: continue
            vis, AND = dfs(u)
            for v in vis:
                m[v] = (group_cnt, AND)
            group_cnt += 1
        
        ans = []
        for u,v in query:
            if m[u][0] != m[v][0]:
                ans.append(-1)
            else:
                ans.append(m[u][1])
        return ans


sol = Solution()
result = [
    # sol.longestMonotonicSubarray(nums = [1,4,3,3,2]),
    # sol.longestMonotonicSubarray([3,2,1]),
    # sol.getSmallestString(s = "zbbz", k = 3),
    # sol.getSmallestString(s = "xaxcd", k = 4),
    # sol.minOperationsToMakeMedianK(nums = [2,5,6,8,5], k = 4),
    # sol.minOperationsToMakeMedianK(nums = [2,5,6,8,5], k = 7),
    sol.minimumCost(n = 5, edges = [[0,1,7],[1,3,7],[1,2,1]], query = [[0,3],[3,4]]),
]
for r in result:
    print(r)
