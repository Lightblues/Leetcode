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
https://leetcode-cn.com/contest/biweekly-contest-114
https://leetcode.cn/circle/discuss/slLdgm/

难度较低. T3 有意思. 
Easonsi @2023 """
class Solution:
    """ 2869. 收集元素的最少操作次数 """
    def minOperations(self, nums: List[int], k: int) -> int:
        vis = set()
        for i in range(len(nums)):
            x = nums[-i-1]
            if x<=k and x not in vis:
                vis.add(x)
                if len(vis)==k: return i+1
    
    """ 2870. 使数组为空的最少操作次数 """
    def minOperations(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        ccnt = Counter(cnt.values())
        res = 0
        for c,multi in ccnt.items():
            if c==1: return -1
            res += ceil(c/3) * multi
        return res
    
    """ 2871. 将数组分割成最多数目的子数组 #medium 考察对于 AND 操作的理解 (结果越来越小) """
    def maxSubarrays(self, nums: List[int]) -> int:
        tgt = reduce(operator.and_, nums)
        # WA 的一个点: 若和不为0, 无法分割!!!
        if tgt!=0: return 1
        res = 0
        tmp = None
        for x in nums:
            tmp = x if tmp is None else tmp & x
            if tmp==tgt:
                res += 1
                tmp = None
        return res
    
    """ 2872. 可以被 K 整除连通块的最大数目 #hard 要求分割一棵树得到的联通快, 每个联通块的和都是K的倍数
限制: n 3e4
思路1: 比较简单的树上 DP
"""
    def maxKDivisibleComponents(self, n: int, edges: List[List[int]], values: List[int], k: int) -> int:
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        
        cnt = 0
        def dfs(u,fa) -> int:
            nonlocal cnt
            acc = values[u]
            for v in g[u]:
                if v==fa: continue
                acc += dfs(v,u)
            if acc%k==0:
                cnt += 1
                return 0
            else:
                return acc
        dfs(0,-1)
        return cnt
    
sol = Solution()
result = [
    # sol.minOperations(nums = [3,1,5,4,2], k = 5),

    # sol.minOperations(nums = [2,3,3,2,2,4,2,3,4]),

    sol.maxSubarrays(nums = [1,0,2,0,1,2]),
    sol.maxSubarrays([22,21,29,22]),
    
    # sol.maxKDivisibleComponents(n = 5, edges = [[0,2],[1,2],[1,3],[2,4]], values = [1,8,1,4,4], k = 6),
    # sol.maxKDivisibleComponents(n = 7, edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]], values = [3,0,6,1,5,2,1], k = 3),
]
for r in result:
    print(r)
