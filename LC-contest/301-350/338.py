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
https://leetcode.cn/contest/weekly-contest-338
https://www.bilibili.com/video/BV11o4y1p7Ci/

这次的有点难! T2就考了prime+二分, T3是前缀和+二分; T4好难orz
Easonsi @2023 """
class Solution:
    """ 6354. K 件物品的最大和
 """
    def kItemsWithMaximumSum(self, numOnes: int, numZeros: int, numNegOnes: int, k: int) -> int:
        ans = min(numOnes, k)
        k -= min(numOnes, k)
        k -= min(numZeros, k)
        ans -= k
        return ans
    
    """ 6355. 质数减法运算 #medium #质数 对于数组中的任意数字可以减去1个质数, 问能否得到严格递增的数组? 限制: n 1e3; 数字范围 1e3
思路0: 看错题目了, 一个数字只能做一次操作!
    注意到, 质数之和可以构成任意 >2 的整数! 
思路1: #筛质数 + #二分查找
    注意到, 每个位置都只能减去一个质数! 
关联: 「2523. 范围内最接近的两个质数」
见 [灵神](https://leetcode.cn/problems/prime-subtraction-operation/solution/jian-ji-xie-fa-shai-zhi-shu-er-fen-cha-z-wj7i/)
     """
    def primeSubOperation(self, nums: List[int]) -> bool:
        # 思路0: 看错题目了
        mn = 2 if nums[0]==2 else 1
        for x in nums[1:]:
            if x<=mn+1: return False
            mn += 1
        return True
    def primeSubOperation(self, nums: List[int]) -> bool:
        # 筛质数
        primes = [0]    # 哨兵，避免二分越界
        MX = max(nums)+1 # 1000
        is_prime = [True]*(MX)
        for i in range(2, MX):
            if is_prime[i]:
                primes.append(i)
                for j in range(i*i, MX, i):
                    is_prime[j] = False
        # 
        pre = 0
        for x in nums:
            if x<=pre: return False
            idx = bisect.bisect_left(primes, x-pre)
            pre = x - primes[idx-1]
        return True

    """ 6357. 使数组元素全部相等的最少操作次数 #medium
每个操作 +/-1, 问对于每次查询x, 变成x所需的操作次数. 限制: n, q 1e5
思路1: 排序之后 #前缀和
    对于每个查询q, 每次可以根据阶梯来统计需要增减的面积
见 [灵神](https://leetcode.cn/problems/minimum-operations-to-make-all-array-elements-equal/solution/yi-tu-miao-dong-pai-xu-qian-zhui-he-er-f-nf55/)
      """
    def minOperations(self, nums: List[int], queries: List[int]) -> List[int]:
        n = len(nums)
        nums.sort()
        acc = list(accumulate(nums, initial=0)) # , initial=0
        ans = []
        for q in queries:
            aa = 0
            idx = bisect.bisect_left(nums, q)
            # 不管找不找得到, 都可以到idx前面的位置; 由于acc不需要进行idx-1
            aa += q*(idx) - acc[idx]
            aa += acc[-1]-acc[idx] - q*(n-idx)
            ans.append(aa)
        return ans

    """ 6356. 收集树中金币 #hard
给定一个树结构, 部分节点有金币. 要求选择从一个节点开始出发并返回原始位置. 每次可以 1] 移动到相邻节点, 代价+1; 2] 收集临近距离在2以内节点的金币. 问最少代价?
限制: n 3e4
思路1: #拓扑排序
    首先, 没有金币的节点没有作用; 进一步的, 删掉之后的中间节点页没有作用! 可以利用拓扑排序的思想! 
    其次, 由于距离为2的金币没有意义, 因此可以进一步删减掉距离叶子节点为2的节点! 
        如何找到? 在拓扑排序的时候记录 深度/时间戳! 
    最后, 剩余节点都要走到! 对于一棵树, 要经过这些点, 还要回到原来的点, 发现每条边都要经过两次! 
[灵神](https://leetcode.cn/problems/collect-coins-in-a-tree/solution/tuo-bu-pai-xu-ji-lu-ru-dui-shi-jian-pyth-6uli/)
       """
    def collectTheCoins(self, coins: List[int], edges: List[List[int]]) -> int:
        n = len(coins)
        g = [[] for _ in range(n)]
        deg = [0] * n
        for u, v in edges:
            g[u].append(v)
            g[v].append(u)
            deg[u] += 1
            deg[v] += 1
        # 拓扑排序
        q = deque([])
        for i,(c,d) in enumerate(zip(coins, deg)):
            if d==1 and c==0: q.append(i)
        while q:
            u = q.popleft()
            for v in g[u]:
                deg[v] -= 1
                if deg[v]==1 and coins[v]==0: q.append(v)
        # 再次拓扑排序
        # 或者也可以用两轮for! 不需要queue, 见视频
        for i, (d, c) in enumerate(zip(deg, coins)):
            if d == 1 and c:  # 有金币叶子
                q.append(i)
        if len(q) <= 1:  # 至多一个有金币的叶子，直接收集
            return 0
        time = [0] * n
        while q:
            x = q.popleft()
            for y in g[x]:
                deg[y] -= 1
                if deg[y] == 1:
                    time[y] = time[x] + 1  # 记录入队时间
                    q.append(y)
        # 统计答案
        return sum(time[x] >= 2 and time[y] >= 2 for x, y in edges) * 2


sol = Solution()
result = [
    # sol.minOperations(nums = [3,1,6,8], queries = [1,5]),
    # sol.minOperations(nums = [2,9,6,3], queries = [10]),
    # sol.primeSubOperation(nums = [4,9,6,10]),
    # sol.primeSubOperation(nums = [5,8,3]),
    sol.collectTheCoins(coins = [1,0,0,0,0,1], edges = [[0,1],[1,2],[2,3],[3,4],[4,5]]),
]
for r in result:
    print(r)
