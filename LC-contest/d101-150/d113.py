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
https://leetcode-cn.com/contest/biweekly-contest-113
https://leetcode.cn/circle/discuss/9iS9Gy/

T3和T4想到了就不难. 挺长时间没打手有点生疏orz

Easonsi @2023 """
class Solution:
    """ 2855. 使数组成为递增数组的最少右移次数 #easy 判断能否通过整体右移, 得到整体递增数组 """
    def minimumRightShifts(self, nums: List[int]) -> int:
        n = len(nums)
        flag = False; idx = -1
        pre = -inf
        for i,x in enumerate(nums):
            if x<pre:
                if flag: return -1
                flag = True
                idx = i
            pre = x
        if not flag: return 0
        # 注意 [2,1,4] 的情况, 无法顺起来!
        if nums[-1] > nums[0]: return -1
        return n-idx
    
    """ 2856. 删除数对后的最小数组长度 #medium 不同的数字两两配对, 问最后剩下多少 """
    def minLengthAfterRemovals(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        mx = max(cnt.values())
        n = len(nums)
        if mx > n-mx: return mx-(n-mx)
        return 1 if n%2 else 0
    
    """ 2857. 统计距离为 k 的点对 #medium #题型 给定一组 (x,y), 找到 (x1 XOR x2) + (y1 XOR y2) == k 的点的数量
限制: n 5e4; k 100
思路1: #散列表 字典
    注意! 对于k的分解 k=a+b, 对于给定的 x2,x1 其所需要匹配的 x1,y1 就固定了!
关联: 「两数之和」
    """
    def countPairs(self, coordinates: List[List[int]], k: int) -> int:
        cnt = Counter()
        ans = 0
        for x,y in coordinates:
            for a in range(k+1):
                b = k-a
                ans += cnt[(x^a,y^b)]
            cnt[(x,y)] += 1
        return ans
    
    """ 2858. 可以到达每一个节点的最少边反转次数 #hard #题型 对于一个树结构的, 但是有向图. 对于每个节点, 从它出发, 问需要翻转多少条边可以遍历所有节点.
限制: n 1e5
反思: 尝试用一次BFS/DFS来完成, 但实际上信息无法完成传递 (每个节点都需要全局信息得到答案的!)
思路1: #换根 DP
    两次DFS, 第一次得到节点0的次数. 然后再进行一次, 临近的节点可以转移!
    """
    def minEdgeReversals(self, n: int, edges: List[List[int]]) -> List[int]:
        # 构建有向图
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append((v,0))
            g[v].append((u,1))
        
        # def bfs(u, fa, nflip, ntot):
        #     for v,type in g[u]:
        #         if v == fa: continue
        #         if type==0: pass
        
        def dfs(u,fa):
            c = 0
            for v,type in g[u]:
                if v == fa: continue
                if type==1: c += 1
                c += dfs(v,u)
            return c
        
        cost = [-1] * n
        cost[0] = dfs(0,-1)
        
        def dp(u,fa):
            for v,type in g[u]:
                if v == fa: continue
                if type==1: cost[v] = cost[u]-1
                else: cost[v] = cost[u]+1
                dp(v,u)
        dp(0,-1)
        return cost

    
sol = Solution()
result = [
    # sol.minimumRightShifts(nums = [3,4,5,1,2]),
    # sol.minimumRightShifts(nums = [2,1,4]),
    # sol.countPairs(coordinates = [[1,2],[4,2],[1,3],[5,2]], k = 5),
    sol.minEdgeReversals(n = 4, edges = [[2,0],[2,1],[1,3]]),
]
for r in result:
    print(r)
