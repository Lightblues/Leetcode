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
https://leetcode.cn/contest/weekly-contest-369
https://leetcode.cn/circle/discuss/ItEVoI/

T3, T4 有意思的. 

Easonsi @2023 """
class Solution:
    """ 2917. 找出数组中的 K-or 值 """
    def findKOr(self, nums: List[int], k: int) -> int:
        cnt = [0] * 32
        for num in nums:
            for i in range(32):
                if num & (1<<i):
                    cnt[i] += 1
        ans = 0
        for i,c in enumerate(cnt):
            if c>=k: ans += 1<<i
        return ans
    
    """ 2918. 数组的最小相等和 """
    def minSum(self, nums1: List[int], nums2: List[int]) -> int:
        s1,s2 = sum(nums1),sum(nums2)
        c1,c2 = nums1.count(0),nums2.count(0)
        if s1>s2:
            s1,s2 = s2,s1
            c1,c2 = c2,c1
        if c1==0:
            if s2==s1:
                return s1 if c2==0 else -1
            else: return -1
        else:
            if c2==0:
                return s2 if c1 <= s2-s1 else -1
            else:
                return max(s1+c1,s2+c2)
    
    """ 2919. 使数组变美的最小增量运算数 #medium 每次选择数组元素+1, 最后要求任意长度为3的子数组的最大值至少为k, 问最少步数
限制: n 1e5
思路1: DP 
    记 f[i] 表示前i个元素满足条件的, 并且最后位置的元素 >=k 的最小操作. 
    """
    def minIncrementOperations(self, nums: List[int], k: int) -> int:
        n = len(nums)
        dp = [0]*n
        for i in range(3):
            dp[i] = max(0,k-nums[i])
        for i in range(3,n):
            a = max(0,k-nums[i])
            dp[i] = a + min(dp[i-3:i])
        return min(dp[-3:])
    
    
    """ 2920. 收集所有金币可获得的最大积分 #hard #题型 在一个树上, 每个节点有x金币. 只能从祖先出发收集所有金币. 
收集规则: [1] 获取/失去 coins[i]-k 个金币; [2] 获取 coins[i]//2 个金币, 并且子节点的所有金币均 //2
限制: n 1e5; 数字 1e4
思路: 层数限制的 #DP 
    记 f[i,x] 表示节点i所代表的子树, 经过x次右移操作之后的最大分数.
        sum{ f[c,x] } + (coin[i]>>c)-k
        sum{ f[c,x+1] } + coin[i]//2
    注意到, 这样的时间复杂度为 O(n^2). 但是, 根据数据范围, 可知x数量最多到 14次就一定为0了!
    答案: f[0,0]
[灵神](https://leetcode.cn/problems/maximum-points-after-collecting-coins-from-all-nodes/solutions/2503152/shu-xing-dp-ji-yi-hua-sou-suo-by-endless-phzx/)
    """
    def maximumPoints(self, edges: List[List[int]], coins: List[int], k: int) -> int:
        n = len(edges) + 1
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        # get tree
        tree = [[] for _ in range(n)]
        def dfs(u,pa):
            for v in g[u]:
                if v != pa:
                    tree[u].append(v)
                    dfs(v,u)
        dfs(0,-1)
        
        from functools import lru_cache
        @lru_cache(None)
        def f(i,x):
            s1 = sum(f(c,x) for c in tree[i]) + (coins[i]>>x)-k
            # 折半情况下，新节点前的总折半次数，大于 14 和等于 14 等价
            nx = min(x+1,14)
            s2 = sum(f(c,nx) for c in tree[i]) + (coins[i]>>nx)
            return max(s1,s2)
        f.cache_clear()
        return f(0,0)
        
    
sol = Solution()
result = [
    # sol.findKOr(nums = [7,12,9,8,9,15], k = 4),
    # sol.minSum(nums1 = [3,2,0,1,0], nums2 = [6,5,0]),
    # sol.minSum(nums1 = [2,0,2,0], nums2 = [1,4]),
    # sol.minSum([0,16,28,12,10,15,25,24,6,0,0],[20,15,19,5,6,29,25,8,12]),
    # sol.minIncrementOperations(nums = [2,3,0,0,2], k = 4),
    # sol.minIncrementOperations(nums = [0,1,3,3], k = 5),
    # sol.minIncrementOperations(nums = [1,1,2], k = 1),
    sol.maximumPoints(edges = [[0,1],[1,2],[2,3]], coins = [10,10,3,3], k = 5),
    sol.maximumPoints(edges = [[0,1],[0,2]], coins = [8,4,4], k = 0),
]
for r in result:
    print(r)
