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
https://leetcode.cn/contest/weekly-contest-366
讨论: https://leetcode.cn/circle/discuss/OSToh6/


Easonsi @2023 """
class Solution:
    """ 2894. 分类求和并作差 求 [1...n] 中的数字, 无法被m整除的数字之和 - 可以整除的
 """
    def differenceOfSums(self, n: int, m: int) -> int:
        ans = 0
        for i in range(1,n+1):
            if i%m: ans += i
            else: ans -= i
        return ans
    
    """ 2895. 最小处理时间 #medium 有n个处理器 (从某一时刻开始空闲), 每个处理器4核并发, 要求最优分配 4n个任务, 计算所有任务都完成的最短时间
限制: 3e4
思路1: 用最小栈, 但直接两个排序即可!
 """
    def minProcessingTime(self, processorTime: List[int], tasks: List[int]) -> int:
        tasks.sort(reverse=True)
        processes = [[i,4] for i in processorTime]
        heapq.heapify(processes)
        ans = 0
        for t in tasks:
            ts, r = heapq.heappop(processes)
            ans = max(ans, ts+t)
            r -= 1
            if r: heapq.heappush(processes, [ts, r])
        return ans
    
    """ 2896. 执行操作使两个字符串相等 #medium, 但实际上 #hard 的DP 给定两个长度相等的0/1字符串 s1,s2. 对于 s1 定义两个操作: 1] 翻转相邻两个位置, 代价为 1; 2] 翻转任意 i,j 两个位置, 代价 x. 
问使得 s1 == s2 的最小代价. 限制: n,x 500
思路1: #DP 
    考虑DP, 对于前i个位置来说, 将其和s2变得相同之后, 还有两个剩余: 经过操作1需要反转下一个, 经过操作2剩余一次任意反转机会.
    因此, 定义DP `f(i,r,isFlip)` 对于前i个位置满足后, 剩余条件 r,isFlip 的最小代价
        实际上, 考虑贪心, 这里的 r 和 isFlip 一样, 只会出现 [0,1] 更多的情况不考虑~
        递归目标: f(n,0,False)
        递归方程:
            [1] 若 isFlip==False, 则对于第i位置 needFlip = s1[i]!=s2[i]; 否则相反
            [2] 若需要反转, 考虑两种方法
                操作1, 转移到 f(i+1,r,True) + 1
                操作2, 转移到 f(i+1,0,False) if r==1 else f(i+1,1,False) + x
    复杂度: O(n^2)
见 [灵神](https://leetcode.cn/problems/apply-operations-to-make-two-strings-equal/solutions/2472122/ji-yi-hua-sou-suo-by-endlesscheng-64vq/)
但实际上也可以迁移到思路2
思路2: 一个更加神奇的 #DP, 见题解 [小羊]
    更直觉一些: 我们只需要考虑 s1,s2 不同的那些位置即可! 我们记这些位置分别在 idxs 中
        显然, len(idxs) 为奇数时, 无法满足!
    考虑「解决前i个元素的最小代价」. 
        1] 采用操作1, 代价为 idxs[i]-idxs[i-1]
        2] 采用操作2, 代价为 x. 注意只需要在偶数位置上计算 [神奇的是, 在奇数位置上计算也可以!]
    复杂度: O(n)
 """
    def minOperations(self, s1: str, s2: str, x: int) -> int:
        n = len(s1)
        from functools import lru_cache
        @lru_cache(None)
        def dfs(i,r,isFlip):
            """ 
            返回: 答案
            """
            ans = inf
            if i==n:
                return 0 if r==0 and isFlip==False else float('inf')
            isMatch = s1[i]==s2[i] if isFlip==False else s1[i]!=s2[i]
            if isMatch:
                ans = min(ans, dfs(i+1, r, False))
            else:
                # op 1
                ans = min(ans, dfs(i+1, r, True)+1)
                # op 2
                if r>0:     # 实际上这里的 r in [0, 1]
                    ans = min(ans, dfs(i+1, r-1, False))
                else:
                    ans = min(ans, dfs(i+1, 1, False)+x)
            return ans
        a = dfs(0,0,False)
        return a if a!=inf else -1

    def minOperations(self, s1: str, s2: str, x: int) -> int:
        n = len(s1)
        idxs = [i for i in range(n) if s1[i]!=s2[i]]
        nn = len(idxs)
        # NOTE: 注意合法判断
        if len(idxs)%2==1: return -1
        dp = [0] * (nn+1)
        for i in range(nn):
            # op 1
            if i%2==1: dp[i+1] = dp[i] + x
            # if i%2==0: dp[i+1] = dp[i] + x
            else: dp[i+1] = dp[i]
            # op 2
            if i > 0:
                dp[i+1] = min(dp[i+1], dp[i-1]+idxs[i]-idxs[i-1])
        return dp[nn]
        
    """ 2897. 对数组执行操作使平方和最大 #hard 有一组数字, 可以进行以下操作任意次: 选择元素x,y, 替换为 AND, OR 之后的结果. 
最后, 要求选择其中的k个数字, 使得平方和最大. 
限制: n 1e5; 取模. 
思路1: 把 1 都聚在一起 #贪心
    注意, x,y --> x AND y, x OR y 之后发生了什么? 对于相同01的位, 不变; 对于不同0/1的位, 1都「转移」到了AND的结果上!
        因此, 因为变换之后, 1/0 的总数不变!
    第二点, 假设原本为 x>y, 经过变换为y中的一些位a转移到了x上, 那么 (x+a)^2 + (y-a)^2 - x^2 - y^2 = 2ax - 2ay + 2a^2 > 0
        因此, 应该尽量将1位集中在一个大数字上面
    总结: 用一个counter记录每个位上的出现次数. 用这些 #贪心 构成最大的k个数字

见 [灵神](https://leetcode.cn/problems/apply-operations-on-array-to-maximize-sum-of-squares/solutions/2472120/ba-1-du-ju-zai-yi-qi-pythonjavacgo-by-en-rzng/)
    """
    def maxSum(self, nums: List[int], k: int) -> int:
        # 数字范围 1e9
        LIMIT = 32
        cnt = [0] * LIMIT
        for x in nums:
            for i in range(LIMIT):
                if x & (1 << i):
                    cnt[i] += 1
        # 
        mod = 10**9 + 7
        ans = 0
        for i in range(k):
            tmp = 0
            for j in range(LIMIT):
                if cnt[j]:
                    tmp += 1 << j
                    cnt[j] -= 1
            ans = (ans + tmp * tmp) % mod
        return ans
        
sol = Solution()
result = [
    # sol.differenceOfSums(n = 10, m = 3),
    # sol.minProcessingTime(processorTime = [10,20], tasks = [2,3,1,2,5,8,4,3]),
    # sol.minProcessingTime(processorTime = [8,10], tasks = [2,2,3,1,8,7,4,5]),
    
    sol.minOperations(s1 = "1100011000", s2 = "0101001010", x = 2),
    sol.minOperations(s1 = "10110", s2 = "00011", x = 4),
    
    # sol.maxSum(nums = [2,6,5,8], k = 2),
    # sol.maxSum(nums = [4,5,4,7], k = 3),
]
for r in result:
    print(r)
