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


N = 105
is_prime = [True] * N
for i in range(2, N):
    if is_prime[i]:
        for j in range(i*i, N, i):
            is_prime[j] = False
primes = set(i for i in range(2, N) if is_prime[i])

""" 
https://leetcode.cn/contest/weekly-contest-393
https://leetcode.cn/circle/discuss/V0Tpx8/

比较难的一次! T3用到了容斥原理, T4的 #划分 DP 也计较混乱, 有时间刷刷题单hh
Easonsi @2023 """
class Solution:
    """ 3114. 替换字符可以得到的最晚时间 """
    def findLatestTime(self, s: str) -> str:
        s = list(s)
        if s[0] == '?':
            if s[1] in "01?":
                s[0] = '1'
            else:
                s[0] = '0'
        if s[1] == '?':
            if s[0] == '1':
                s[1] = '1'
            else:
                s[1] = '9'
        if s[3] == '?':
            s[3] = '5'
        if s[4] == '?':
            s[4] = '9'
        return "".join(s)
    
    """ 3115. 质数的最大距离 """
    def maximumPrimeDifference(self, nums: List[int]) -> int:
        first = -1
        ans = 0
        for i, x in enumerate(nums):
            if x in primes:
                if first == -1:
                    first = i
                ans = max(ans, i-first)
        return ans
    
    """ 3116. 单面值组合的第 K 小金额 #hard #题型 有一组不同面额的硬币, 每次只能选择一种硬币的任意数量, 问可以得到的所有金额中第 k 小的金额是多少
限制: n 15; coin 25; k 2e9
思路1: 二分答案+ #容斥原理
    #二分 是比较容易想到的, 问题是如何处理重复的情况? 
        例如, 2,3,5 来说, 元素30可能是有这三个硬币分别得到的!
        这时候就要用到容斥原理! 
            对于元素 2,3,5 他们分别对于30的贡献为 +1
            对于 lcm(2,3), lcm(2,5), lcm(3,5) 他们分别对于30的贡献为 -1
            对于 lcm(2,3,5) 他们对于30的贡献为 +1
        对于coins所构成的集合, 检查子集 (容斥原理). 这里的符号, 显然就是子集大小, 偶数的都是 -
    如何枚举子集? #二进制枚举
    复杂度: 二分的范围 log(2e9 * 25); 检查的复杂度 2^n * n
[ling](https://leetcode.cn/problems/kth-smallest-amount-with-single-denomination-combination/solutions/2739205/er-fen-da-an-rong-chi-yuan-li-pythonjava-v24i/)
关联: 
1201. 丑数 III
"""
    def findKthSmallest(self, coins: List[int], k: int) -> int:
        def check(x):
            # 检查 x 是否 >= kth 的元素
            acc = 0
            for i in range(1, 1<<n):
                lcm = 1
                cnt = 0
                for j in range(n):
                    if i & (1<<j):
                        # lcm = lcm // math.gcd(lcm, coins[j]) * coins[j]
                        lcm = math.lcm(lcm, coins[j])
                        cnt += 1
                acc += (x//lcm) * (1 if cnt%2 else -1)
            return acc >= k
        n = len(coins)

        mn = min(coins)
        l=mn; r=mn*k
        ans = 0     # 为什么这里ans一定可以取到? 因为二分的过程中找到的最小的满足「>= kth」的元素
        while l <= r:
            mid = (l+r)//2
            res = check(mid)
            if res: 
                ans = mid
                r = mid-1
            else: 
                l = mid+1
        return ans

    """ 3117. 划分数组得到最小的值之和 #hard 对于一个长n的数组划分为m段, 要求每段的 AND 结果是 andValid[i]. 对于每个划分, 分数为 sum{ seg_i[-1] }. 求最小的分数
限制: n 1e4; m 10; 
思路1: 
    记 f(i,j,a) 表示前i个数, 划分为j段, 最后一段的 AND 结果为a 的最小分数
    答案: f(n-1,m-1,v[m-1])
    状态转移: [见代码]
        若 a == v[j], 则 f(i,j,a) = min{ f(i+1,j+1,v[i+1])+nums[i], 当AND满足的时候 f(i+1,j,a)  }
        边界: 
            a < v[j] 时, 不可能满足!
    时间复杂度: O(n*m*log(U))
        这是因为, 对于一个固定的右端点 i, 其前缀AND的值只有 log(U) 种可能性! (AND 越来越小, 只能某一位变为 0)
[ling](https://leetcode.cn/problems/minimum-sum-of-values-by-dividing-array/solutions/2739258/ji-yi-hua-sou-suo-jian-ji-xie-fa-by-endl-728z/)
    避免了下面的边界讨论! 优雅! 
关联 [§6.3 约束划分个数]
410. 分割数组的最大值
1043. 分隔数组以得到最大和 1916
1745. 分割回文串 IV 1925
813. 最大平均值和的分组 1937
1278. 分割回文串 III 1979
1335. 工作计划的最低难度 2035
1473. 粉刷房子 III 2056
1478. 安排邮筒 2190
1959. K 次调整数组大小浪费的最小总空间 2310 *转换
2478. 完美分割的方案数 2344
3077. K 个不相交子数组的最大能量值 2557
2911. 得到 K 个半回文串的最少修改次数 2608
    """
    def minimumValueSum(self, nums: List[int], andValues: List[int]) -> int:
        n, m = len(nums), len(andValues)

        @lru_cache(None)
        def f(i,j,a):
            # 考虑边界
            if i==n-1:
                if j==m-1 and a==andValues[j]:
                    return nums[i]
                return inf
            if a < andValues[j]:        # prine
                return inf
            # 转移
            ans = inf
            if a == andValues[j]:
                if i<n-1 and j<m-1:     # 由于转移的下一个状态必然 i+1, 这里都进行特殊检查! 
                    ans = f(i+1,j+1,nums[i+1]) + nums[i]
                if i<n-1 and a&nums[i+1] == a:
                    ans = min(ans, f(i+1,j,a))
            else:
                if i<n-1:
                    ans = f(i+1,j,a&nums[i+1])
            return ans
        ans = f(0,0,nums[0])
        return ans if ans != inf else -1


sol = Solution()
result = [
    # sol.findLatestTime(s = "1?:?4"),
    # sol.findLatestTime(s = "0?:5?"),
    # sol.findLatestTime("??:1?"),
    # sol.findKthSmallest(coins = [3,6,9], k = 3),
    # sol.findKthSmallest(coins = [5,2], k = 7),
    # sol.minimumValueSum(nums = [1,4,3,3,2], andValues = [0,3,3,2]),
    # sol.minimumValueSum(nums = [2,3,5,7,7,7,5], andValues = [0,7,5]),
    # sol.minimumValueSum([1,2,3,4], [2]),
    sol.minimumValueSum([383,491,329], [363,329]),
]
for r in result:
    print(r)
