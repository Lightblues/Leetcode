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
https://leetcode-cn.com/contest/biweekly-contest-125
Easonsi @2023 """
class Solution:
    """ 3065. 超过阈值的最少操作数 I """
    def minOperations(self, nums: List[int], k: int) -> int:
        return sum(i<k for i in nums)
    
    """ 3066. 超过阈值的最少操作数 II 每次操作, 删除数字中最小的两个元素 x,y, 并将 min(x,y)*2 + max(x,y) 加入. 问操作多少次之后, 所有元素 >=k
    """
    def minOperations(self, nums: List[int], k: int) -> int:
        heapify(nums)
        ans = 0
        while nums[0] < k:
            x,y = heappop(nums), heappop(nums)
            heappush(nums, 2*x+y)
            ans += 1
        return ans
    
    """ 3067. 在带权树网络中统计可连接服务器对数目 给定一棵带权树, 对于节点i, 另外两个节点a,b经过i是可连接的定义是, (1) a<b; (2) a->i->b 没有公共边, 并且两段路径长度都是 signalSpeed 的整数倍.
求每个点作为中间点可连接的数量. 限制: n 1e3; w 1e6
思路1: 从每个节点出发, DFS统计路径长度分布
    最后的答案是什么? 对于root节点, 看从他的每个分支出发, 路径%signalSpeed == 0 的子路径有多少, 匹配! 
    复杂度: O(n * n)
    NOTE: 下面第一种方法TLE, 因为 f -> 一个大小为 W 的cnt, 复杂度直接变为 O(n * nW)
        优化: f -> int
[ling](https://leetcode.cn/problems/count-pairs-of-connectable-servers-in-a-weighted-tree-network/solutions/2664330/mei-ju-gen-dfs-cheng-fa-yuan-li-pythonja-ivw5/)
    """
    def countPairsOfConnectableServers(self, edges: List[List[int]], signalSpeed: int) -> List[int]:
        # TLE
        n = len(edges) + 1
        g = [[] for _ in range(n)]
        for u,v,w in edges:
            g[u].append((v,w))
            g[v].append((u,w))
        # 
        # def f(u, fa):
        #     cnt = Counter()
        #     for v,w in g[u]:
        #         if v==fa: continue
        #         for x,c in f(v, u).items():
        #             cnt[w+x] += c
        #     cnt[0] += 1
        #     return cnt
        # def get_pairas(u):
        #     ans = 0
        #     cntMulti = 0
        #     for v,w in g[u]:
        #         nc = sum(c for x,c in f(v, u).items() if (x+w) % signalSpeed == 0)
        #         ans += nc * cntMulti
        #         cntMulti += nc
        #     return ans
        def f(u, fa) -> List[int]:
            cnt = [0] * signalSpeed
            for v,w in g[u]:
                if v==fa: continue
                for x,c in enumerate(f(v,u)):
                    cnt[(w+x) % signalSpeed] += c
            cnt[0] += 1
            return cnt
        def get_pairas(u):
            ans = 0
            cntMulti = 0
            for v,w in g[u]:
                nc = f(v,u)[(signalSpeed-w) % signalSpeed]
                ans += nc * cntMulti
                cntMulti += nc
            return ans
        return [get_pairas(i) for i in range(n)]

    def countPairsOfConnectableServers(self, edges: List[List[int]], signalSpeed: int) -> List[int]:
        n = len(edges) + 1
        g = [[] for _ in range(n)]
        for u,v,w in edges:
            g[u].append((v,w))
            g[v].append((u,w))
    
        def dfs(u, fa, pw) -> List[int]:
            # 统计前缀和为 pw 情况下, 构成路径 %signalSpeed==0 的数量
            cnt = 0 if pw%signalSpeed else 1
            for v,w in g[u]:
                if v==fa: continue
                cnt += dfs(v, u, w+pw)
            return cnt
        def get_pairas(u):
            ans = 0
            cntMulti = 0
            for v,w in g[u]:
                nc = dfs(v,u,w)
                ans += nc * cntMulti
                cntMulti += nc
            return ans
        return [get_pairas(i) for i in range(n)]
    
    
    """ 3068. 最大节点价值之和 #hard  给定一棵树, 节点上面有分数. 每次操作: 选择一条边, 两个节点的分数都 XOR=k, 问任意操作之后最大分数和. 
限制: n 2e4; v 149
思路1: 直接 #树形 #DP
    分析比较复杂, 参见 ling
见 [ling](https://leetcode.cn/problems/find-the-maximum-sum-of-node-values/solutions/2664309/liang-chong-fang-fa-shu-xing-dp-xian-xin-lh6b/)
思路2: 转化 + #DP
    1. 注意到, 对于 x->...->y 假如我们对于每条边进行操作, 等价于 "只对于x,y进行XOR操作"! 
    2. 进一步, 显然, 最终被异或的个数是偶数! 
    -> 问题等价于, 从n个数中选择偶数个进行异或, 得到的最大值
    然后呢? 一种想法是记录每个节点经过异或之后的增量 (#贪心), 不过下面的实现好像有问题
    另一种思路是DP, 考虑 dp0[i], dp1[i] 表示遍历到i元素时, 有 偶数/奇数 个元素经过异或之后的最大和, 则有下面的递推关系. 
    """
    def maximumValueSum(self, nums: List[int], k: int, edges: List[List[int]]) -> int:
        # add = [(x ^ k) - x for x in nums if x!=k] # ensure != 0
        # add.sort()
        # idx = bisect_left(add, 0)
        # if 0 < idx < len(add) and add[idx] > abs(add[idx-1]):
        #     add = add[idx-1:]
        # else: add = add[idx:]
        # return sum(nums) + sum(add if len(add)%2==0 else add[:-1])
        
        # https://leetcode.cn/problems/find-the-maximum-sum-of-node-values/solutions/2664197/xiao-yang-xiao-en-jia-shu-zhen-dp-on-de-ddxag/
        dp0, dp1 = 0, -inf # 分别记录有 偶数/奇数 个元素经过异或之后的最大和
        for num in nums:
            dp0, dp1 = max(dp0 + num, dp1 + (num ^ k)), max(dp0 + (num ^ k), dp1 + num)
        return dp0


sol = Solution()
result = [
    # sol.minOperations(nums = [2,11,10,1,3], k = 10),
    # sol.countPairsOfConnectableServers(edges = [[0,1,1],[1,2,5],[2,3,13],[3,4,9],[4,5,2]], signalSpeed = 1),
    # sol.countPairsOfConnectableServers(edges = [[0,6,3],[6,5,3],[0,3,1],[3,2,7],[3,1,6],[3,4,2]], signalSpeed = 3),
    sol.maximumValueSum(nums = [1,2,1], k = 3, edges = [[0,1],[0,2]]),
    sol.maximumValueSum(nums = [2,3], k = 7, edges = [[0,1]]),
    sol.maximumValueSum([24,78,1,97,44], 6, [])
]
for r in result:
    print(r)
