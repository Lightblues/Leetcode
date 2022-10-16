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
https://leetcode.cn/contest/weekly-contest-173

对于 copilot的「抄袭」能力又有了新的认识: 仅仅写了下面的「1332. 删除回文子序列」这些文字, 直接补全到了「1335. 工作计划的最低难度 #hard #题型」. 三道题目直接AK! (当然 T4也是写了个函数签名就AC了)
不仅仅是代码上的「借鉴」, 连代码 (注释) 的格式都和我的习惯完全一致 (#easy, #medium 的tag也是自动加上去的)...
对于这种经典问题, 感觉自己的工作就是代码审核...

本期的题目水准挺高! T1 审题不够仔细; T3居然考了 Floyd; T4 直接给补完了没啥思考量, 如果真要做的话估计也要想一想. 

@2022 """
class Solution:
    """ 1332. 删除回文子序列 #easy 序列仅由 ab两种元素构成. 每次删除一个「回文子序列」, 问最快的删除次数. 注意审题: 是子序列!
    """
    def removePalindromeSub(self, s: str) -> int:
        if not s: return 0
        return 1 if s == s[::-1] else 2

    """ 1333. 餐厅过滤器 #medium 每家餐厅 (id, rating, veganFriendly, price, distance) 给出. 根据一定的规则过滤, 然后按照 rating 降序, id 升序排序输出.
    """
    def filterRestaurants(self, restaurants: List[List[int]], veganFriendly: int, maxPrice: int, maxDistance: int) -> List[int]:
        ans = []
        for r in restaurants:
            if r[2] >= veganFriendly and r[3] <= maxPrice and r[4] <= maxDistance:
                ans.append(r)
        ans.sort(key=lambda x: (x[1], x[0]), reverse=True)
        return [r[0] for r in ans]

    """ 1334. 阈值距离内邻居最少的城市 #medium 一张带权图表示城市之间的距离. 在maxDist距离限制内计算每个城市的邻居数量, 返回邻居数量最小的城市. 限制: n 100.
思路1: 先用 #Floyd 算法计算任意两点之间的距离. 然后遍历每个城市, 计算距离小于等于 maxDist 的城市数量. 时间复杂度 O(n^3).
思路2: 当然, 也可以对于每个节点用 #Dijkstra
参见 [这里](https://leetcode.cn/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/solution/zui-duan-lu-jing-mo-ban-da-ji-he-cban-fl-gs7u/) 的性能测试.
wiki [Floyd](https://zh.wikipedia.org/zh-cn/Floyd-Warshall%E7%AE%97%E6%B3%95)
    """
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        # Floyd
        INF = 1e9
        d = [[INF] * n for _ in range(n)]
        for i in range(n):
            d[i][i] = 0
        for u, v, w in edges:
            d[u][v] = d[v][u] = w
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    d[i][j] = min(d[i][j], d[i][k] + d[k][j])
        # print(d)
        ans = -1
        minCnt = n
        for i in range(n):
            cnt = 0
            for j in range(n):
                if d[i][j] <= distanceThreshold:
                    cnt += 1
            if cnt <= minCnt:
                ans = i
                minCnt = cnt
        return ans

    """ 1335. 工作计划的最低难度 #hard #题型 分割数组成 d个子数组, 要求 sum{ max(subarr) } 最小. 限制: n 300. d 10.
思路1: #DP
    记 `f[i,j]` 表示分割好的前i个子数组覆盖 arr[:j] 的情况下的最小难度
    递推: f[i,j] = min{ f[i-1,k] + max(arr[k:j]) } for k in range(j)
    复杂度: 状态 nd, 转移 n, 因此时间复杂度 O(n^2 d)
思路2: 实际上, 上述 DP 可以用 #单调栈 优化. 时间复杂度 O(n d)
    见 [here](https://leetcode.cn/problems/minimum-difficulty-of-a-job-schedule/solution/ond-dong-tai-gui-hua-dan-diao-zhan-you-hua-by-arse/)
"""
    def minDifficulty(self, jobDifficulty: List[int], d: int) -> int:
        n = len(jobDifficulty)
        if n < d: return -1
        dp = [[1e9] * n for _ in range(d)]
        # 初始化
        dp[0][0] = jobDifficulty[0]
        for i in range(1, n):
            dp[0][i] = max(dp[0][i-1], jobDifficulty[i])
        for i in range(1, d):
            for j in range(i, n):
                # 任意子数组都需要非空
                for k in range(i-1, j):
                    dp[i][j] = min(dp[i][j], dp[i-1][k] + max(jobDifficulty[k+1:j+1]))
        return dp[-1][-1]
    
    
    
    
    

    
sol = Solution()
result = [
    sol.minDifficulty(jobDifficulty = [6,5,4,3,2,1], d = 2),
]
for r in result:
    print(r)
