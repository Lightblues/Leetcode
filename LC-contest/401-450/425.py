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
https://leetcode.cn/contest/weekly-contest-425

TODO: T4
Easonsi @2024 """
class Solution:
    """ 3364. 最小正和子数组 #easy 在所有长度在 [l...r] 范围内的子数组中, 找到和大于0的, 最小和
限制: n 100; v +/- 1000
思路1: 滑动窗口. 
    复杂度 n*(r-l)
思路2: #前缀和 + #有序集合 #二分搜索
    可以枚举右端点, 滑动窗口可以维护在范围内的下标范围; 可以维护一个有序集合保存这些前缀和, 在其中二分搜索找到满足条件的. 
    复杂度: n * log(r-l)
ling https://leetcode.cn/problems/minimum-positive-sum-subarray/solutions/2998908/liang-chong-fang-fa-bao-li-mei-ju-qian-z-ndz5/
    """
    def minimumSumSubarray(self, nums: List[int], l: int, r: int) -> int:
        from sortedcontainers import SortedList
        acc = list(accumulate(nums, initial=0))
        sl = SortedList()
        ans = inf
        for j in range(l, len(nums)+1):
            sl.add(acc[j-l])
            idx = sl.bisect_left(acc[j])
            if idx:
                ans = min(ans, acc[j] - sl[idx-1])
            if j>=r:
                sl.remove(acc[j-r])
        return ans if ans!=inf else -1
    
    
    """ 3365. 重排子字符串以形成目标字符串 """
    def isPossibleToRearrange(self, s: str, t: str, k: int) -> bool:
        n = len(s)
        k = n // k
        cnt_s = Counter(s[i: i + k] for i in range(0, n, k))
        cnt_t = Counter(t[i: i + k] for i in range(0, n, k))
        return cnt_s == cnt_t

    """ 3366. 最小数组和 #medium 对于每个位置, 可以执行下面的两个操作 (每个位置的操作 1/2 最多都只能执行一次, 可以都做), 要求最小化数组和
操作1: x <- ceil(x/2), 最多进行 op1 次
操作2: x -= k, 要求 x>=k, 最多进行 op2 次
限制: n 100; x 1e5
思路1: DP
    记 f(i,j,k) 表示考虑前i位, 使用 (j,k) 次操作1/2 后的最小和. 
    转移: 
        f(i,j,k) = min(
            f(i-1,j,k) + nums[i], 
            f(i-1,j-1,k) + ceil(nums[i]/2), 
            f(i-1,j,k-1) + nums[i] - k,
            f(i-1,j-1,k-1) + min(...),
        )
    复杂度: n * op1 * op2
思路2: #贪心
    见 灵 https://leetcode.cn/problems/minimum-array-sum/solutions/2998867/jiao-ni-yi-bu-bu-si-kao-dpcong-ji-yi-hua-0pc5/
    """
    def minArraySum(self, nums: List[int], k: int, op1: int, op2: int) -> int:
        n = len(nums)
        @lru_cache(None)
        def f(i,j,kk):
            if j<0 or kk<0: return inf
            if i<0: return 0
            ans = min(
                f(i-1,j,kk) + nums[i], 
                f(i-1,j-1,kk) + ceil(nums[i]/2)
            )
            if nums[i]>=k:
                ans = min(ans, f(i-1,j,kk-1) + nums[i] - k)
                dd = ceil((nums[i] - k)/2)
                if ceil(nums[i]/2) >= k:
                    dd = min(ceil(nums[i]/2) - k, dd)
                ans = min(ans, f(i-1,j-1,kk-1) + dd)
            return ans
        return f(n-1, op1, op2)


    """ 3367. 移除边之后的权重最大和 #hard 需要从一个有权图中删去一组边, 使得 "任一节点连边数量不超过k", 求留下边权之和的最大值. 
限制: n 1e5
思路1: 树 #DP TODO: 
    """
    def maximizeSumOfWeights(self, edges: List[List[int]], k: int) -> int:
        pass

    
sol = Solution()
result = [
    # sol.minimumSumSubarray(nums = [3, -2, 1, 4], l = 2, r = 3),
    sol.minArraySum(nums = [2,8,3,19,3], k = 3, op1 = 1, op2 = 1),
    sol.minArraySum(nums = [2,4,3], k = 3, op1 = 2, op2 = 1),
    sol.minArraySum([9], 5,1,1),
]
for r in result:
    print(r)
