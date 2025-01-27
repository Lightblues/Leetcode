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
https://leetcode.cn/contest/weekly-contest-423
https://leetcode.cn/circle/discuss/muNov6/

T2 的二分比较巧妙
T3 自己想到了DP, 不错子
T4 数位DP, 像一开始一样做了好久, 看到灵神解法之后恍然大悟! 需要背模板 (吗, in LLM era)
Easonsi @2024 """
class Solution:
    """ 3349. 检测相邻递增子数组 I 判断是否存在两个相邻的长度为k的子数组, 他们都是严格递增的 """
    def hasIncreasingSubarrays(self, nums: List[int], k: int) -> bool:
        if k==1: return len(nums) >= 2  # NOTE: boundary case
        acc = 1; flag = False
        for i in range(1, len(nums)):
            if nums[i] > nums[i-1]:
                acc += 1
                if acc >= 2*k: return True
                if acc >= k and flag: return True
            else:
                flag = acc >= k
                acc = 1
        return False
    
    """ 3350. 检测相邻递增子数组 II 找到最大的k 
思路1: #二分
    """
    def maxIncreasingSubarrays(self, nums: List[int]) -> int:
        l, r = 1, len(nums) // 2
        ans = 0
        while l <= r:
            mid = (l+r) // 2
            if self.hasIncreasingSubarrays(nums, mid):
                ans = mid; l = mid + 1
            else:
                r = mid - 1
        return ans
    
    """ 3351. 好子序列的元素之和 #hard 定义 "好子序列" 为, "子序列中任意 两个 连续元素的绝对差 恰好 为 1". 对于数组中所有的好子序列, 计算它们的元素和
限制: n 1e5; x 1e5
思路1: #模拟 #DP
    例子: 考虑 [1,2,1] 的case, 好子序列包括 [1], [2], [1], [1,2], [2,1], [1,2,1], 答案为 14. 
    核心: 从左到右考虑新增对于结果的影响. 
        定义 x2cnt[x] 表示以 x 结尾的好子序列的个数, x2acc[x] 表示以 x 结尾的好子序列的元素和. 
        对于一个新的元素x, 它可能和前面的 x-1, x+1 组成新的好子序列. 
            1. 更新 x2cnt[x] += x2cnt[x-1] + x2cnt[x+1]
            2. 更新 x2acc[x] += x2acc[x-1] + x2acc[x+1] + x2cnt[x-1] * x + x2cnt[x+1] * x
[ling](https://leetcode.cn/problems/sum-of-good-subsequences/solutions/2983496/te-shu-zi-xu-lie-dppythonjavacgo-by-endl-vv7e/)
    """
    def sumOfGoodSubsequences(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        ans = 0
        x2cnt, x2acc = defaultdict(int), defaultdict(int)
        for x in nums:
            cnt_x, acc_x = 1, x
            for y in [x-1, x+1]:
                cnt_x += x2cnt[y]
                acc_x += x2acc[y] + x2cnt[y] * x
            x2cnt[x] = (x2cnt[x] + cnt_x) % MOD
            x2acc[x] = (x2acc[x] + acc_x) % MOD
            ans = (ans + acc_x) % MOD
        return ans
            

    """ 3352. 统计小于 N 的 K 可约简整数 #hard #题型
定义: 一次 "操作" 为 "将 x 替换为其二进制表示中的置位数", 也即二进制表示中1的数量. "k-可约简" 整数, 是指最多经过 k 次操作后, 结果为 1 的整数. 
    例子: 6='110' -> 2='10' -> 1
给定一个二进制字符串s, 问小于 s 的 k-可约简整数有多少个. 
限制: s 800; k 1~5
思路1: 预处理 (线性DP) + 数位DP
    1. 预处理, 对于 1~800 的数, 我们可以简单地通过线性DP来得到结果! 
        因此, 问题转为, 对于在 1~800 范围内符合 "k-1 可约简" 的数字 x, 在 [1,s) 范围内有多少个位数恰好为 x 的数字. --> 数位DP!
    2. #数位DP
        定义 f(i, left1, is_limit) 表示考虑s左边i位, 在 [1, s) 范围内, 数字1的个数为left1的数量, 其中 is_limit 表示当前是否受到 <s 的限制. 
        转移: 
            1. 当前位置可取的数字 0~up: 若 is_limit=True, 则最多取 s[i]; 否则可以取全部数字 (0/1)
            2. is_limit 更新: 只有当 is_limit=True & 当前所取数字 d==up 时才为 True
            有 f(i, left1, is_limit) = sum{ f(i+1, left1-d, is_limit & (d==up)) for d in 0~up }
        边界: i==n 时, 当 left1==0 & is_limit=False 时, 返回 1; 否则返回 0
[ling](https://leetcode.cn/problems/count-k-reducible-numbers-less-than-n/solutions/2983541/xian-xing-dp-shu-wei-dppythonjavacgo-by-yw0dl/)
    """
    def countKReducibleNumbers(self, s: str, k: int) -> int:
        MOD = 10**9 + 7
        limit = 800
        # 1. preprocess: build the mapping from bits to steps below 800
        m = [inf] * (limit+1)
        m[1] = 0
        for i in range(2, limit+1):
            bits = i.bit_count()
            m[i] = m[bits] + 1
        # 2. digit DP
        n = len(s)
        @cache
        def f(i, left1, is_limit=True) -> int:
            if left1 > n-i: return 0   # NOTE: prune! or will TLE https://leetcode.cn/problems/count-k-reducible-numbers-less-than-n/submissions/590524774/
            if i==n:
                if left1==0 and not is_limit: return 1
                else: return 0
            up = int(s[i]) if is_limit else 1
            ans = 0
            for d in range(0, min(up, left1)+1):  # NOTE: min(up, left1) to avoid left1 < 0
                ans += f(i+1, left1-d, is_limit & (d==up))
            return ans % MOD

        ans = 0
        for x in range(1, limit+1):
            if m[x] < k:
                c = f(0, x)
                ans = (ans + c) % MOD
        f.cache_clear()
        return ans % MOD
    
    def countKReducibleNumbers(self, s: str, k: int) -> int:
        # from https://leetcode.cn/problems/count-k-reducible-numbers-less-than-n/solutions/2983541/xian-xing-dp-shu-wei-dppythonjavacgo-by-yw0dl/
        MOD = 1_000_000_007
        n = len(s)

        @cache
        def dfs(i: int, left1: int, is_limit: bool) -> int:
            if i == n:
                return 0 if is_limit or left1 else 1
            up = int(s[i]) if is_limit else 1
            res = 0
            for d in range(min(up, left1) + 1):
                res += dfs(i + 1, left1 - d, is_limit and d == up)
            return res % MOD

        ans = 0
        f = [0] * n
        for i in range(1, n):
            f[i] = f[i.bit_count()] + 1
            if f[i] <= k:
                # 计算有多少个二进制数恰好有 i 个 1
                ans += dfs(0, i, True)
        dfs.cache_clear()  # 防止爆内存
        return ans % MOD

    
sol = Solution()
result = [
    # sol.hasIncreasingSubarrays(nums = [2,5,7,8,9,2,3,4,3,1], k = 3),
    # sol.hasIncreasingSubarrays(nums = [1,2,3,4,4,4,4,5,6,7], k = 5),
    # sol.hasIncreasingSubarrays([19,5], 1),
    # sol.maxIncreasingSubarrays(nums = [2,5,7,8,9,2,3,4,3,1]),
    # sol.maxIncreasingSubarrays(nums = [1,2,3,4,4,4,4,5,6,7]),
    # sol.maxIncreasingSubarrays([19,5]),
    # sol.sumOfGoodSubsequences(nums = [1,2,1]),
    sol.countKReducibleNumbers( s = "111", k = 1),
    sol.countKReducibleNumbers( s = "1000", k = 2),
    sol.countKReducibleNumbers("10", 1),
]
for r in result:
    print(r)
