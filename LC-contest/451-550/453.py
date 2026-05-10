from typing import *
from collections import deque
import collections
import math

"""
https://leetcode.cn/contest/weekly-contest-453
Easonsi @2026 """


class Solution:
    """ 3576. 数组元素相等转换. #medium
对于原本只有 1, -1 元素的数组, 每次操作将 i,i+1 相邻元素翻转; 问在 k 步内能够使所有元素相等
思路 1: 两种情况：都变成 1 或者都变成 -1
    参见: 贪心题单的「§1.4 从最左/最右开始贪心」
    复杂度: O(n)
https://leetcode.cn/problems/transform-array-to-all-equal-elements/solutions/3695707/liang-chong-qing-kuang-du-bian-cheng-1-h-pcpj/
PS: 观察 1, 当 1/-1 的数量都为奇数是, 无法完成
    观察 2: 否则, 不考虑k 的条件下, 一定可以完成! 但同样要看奇偶性!
    """
    def canMakeEqual(self, nums: List[int], k: int) -> bool:
        n = len(nums)
        n1 = nums.count(1)
        if n1 & 1 and (n-n1) & 1: return False
        def test(nums: list[int], flag: int) -> bool:
            cnt = k
            pre = 1
            for i,x in enumerate(nums):
                if pre * x != flag:
                    if i == len(nums) - 1: return False  # NOTE: 需要验证可以完成!
                    cnt -= 1
                    pre = -1
                    if cnt < 0: return False
                else: pre = 1
            return True
        return test(nums, 1) or test(nums, -1)

    """ 3577. 统计计算机解锁顺序排列数 #medium
有 n 个机器复杂度分别为 complexity[i], 初始只有 0 号解锁. 解锁规则, i<j 且 complexity[i]<complexity[j] 的条件下, 可用 i 解锁 j. 问总有多少中解锁顺序 (排列)
限制: n 1e5. 结果求模
思路 1: #脑筋急转弯
    实际上, 只有当 c[0] < c[1:n] 时, 才能被全部解锁.
    因此, 在可解锁状态下, 后面的排列是任意的! 因此答案就是 (n-1)!
    复杂度: O(n)
    """
    def countPermutations(self, complexity: List[int]) -> int:
        MOD = 10**9+7
        for i in range(1, len(complexity)):
            if complexity[i] <= complexity[0]: return 0
        # return math.factorial
        ans = 1
        for i in range(2, len(complexity)):
            ans = ans*i % MOD
        return ans

    """ 3578. 统计极差最大为 K 的分割方式数 #medium
给定一个数组, 要求将其分割为若干子数组, 每个子数组的数字差值 <=k, 问可分割方案数.
限制: n5e4; v 1e9; 对结果求 mod
思路 1: 划分型 DP + #单调队列 优化
    观察 [9,4,1,3,7]; k=4 的情况
    注意到, 从左往右考虑新增元素的影响, 记前 i 个元素可构成的方案数为 f[i], 则对于对于 nums[j] = x, f[j] = sum(f[l]), 其中 l 的范围满足构成数组的极差 <=k
    因此, 需要考虑 #滑动窗口 内的 min, max -- 可以通过两个单调队列来实现!
    NOTE: 考虑边界情况, 应该设置 f[0] = 1, #哨兵
    复杂度: O(n)
https://leetcode.cn/problems/count-partitions-with-max-min-difference-at-most-k/solutions/3695716/hua-fen-xing-dp-dan-diao-dui-lie-you-hua-9rtj/
    """
    def countPartitions(self, nums: List[int], k: int) -> int:
        MOD = 10**9+7
        f = [0] * (len(nums)+1)
        f[0] = 1  # 哨兵
        min_q, max_q = deque(), deque()  # 记录区域内 index
        sum_f = 0  # 窗口内 f[i] 之和
        left = 0  # 窗口边界
        for i,x in enumerate(nums):
            # in
            sum_f += f[i]  # NOTE: 增加当前元素!
            while max_q and x>nums[max_q[-1]]: max_q.pop()
            max_q.append(i)
            while min_q and x<nums[min_q[-1]]: min_q.pop()
            min_q.append(i)
            # out
            while nums[max_q[0]] - nums[min_q[0]] > k:
                sum_f -= f[left]
                left += 1
                if max_q[0] < left: max_q.popleft()
                if min_q[0] < left: min_q.popleft()
            f[i+1] = sum_f % MOD
        return f[len(nums)]

    """ 3579. 字符串转换需要的最小操作数 #hard
给定两个字符串, 可以将 word1 分成若干串, 执行 1. 替换一个字符; 2. 两个字符交换; 2. 翻转 操作. 问最少操作得到 word2
限制: n 100;
思路 1: 划分型 DP + 贪心 + 中心扩展法
    整体思路, 考虑 f[i+1] 为 0...j 部分的最小操作, 则有 f[i+1] = min{ f[j] + op(j,i), 0<=j<=i}
    下面考虑 最小操作次数 op(j,i)?
        先考虑只用前两个操作, 采用贪心策略 -- 因为翻转操作省一次操作!
            假设 (p,q) 坐标满足翻转, 则有 s[p]=t[q], s[q]=t[p]. -- 不妨直接统计 (sp, tp) 的数量!
            用一个 cnt 来记录, 对于 (sp, tp):
            1. sp=tp, 无需操作;
            2. cnt[tp][sp] = 0, 将 op+1; cnt[sp][tp]+=1
            3. cnt[tp][sp] > 0, 说明之前的操作可以替换为翻转; cnt[tp][sp]==1
        因为仅能执行一次翻转操作, 再考虑翻转重新算一次即可!
    复杂度: O(n^3)
优化: 对于不翻转的情况可以增量计算 cnt; 而对于翻转的情况, 可以考虑 #中心扩展法 #optional TODO
    复杂度: O(n^2)
https://leetcode.cn/problems/minimum-steps-to-convert-string-with-operations/solutions/3695734/hua-fen-xing-dp-tan-xin-pythonjavacgo-by-17kb/
    """
    def minOperations(self, word1: str, word2: str) -> int:
        n = len(word1)
        f = [0] * (n+1)
        for i in range(n):
            res = math.inf
            # NOTE: 对于不翻转的情况, 可以增量计算
            cnt = collections.defaultdict(int)  # 统计后缀区域内的 (sp, tp) 数量
            op = 0
            for j in range(i,-1,-1):  # 逆序枚举 j
                # 不反转
                # -- 和 rev 情况一样
                # cnt = collections.defaultdict(int)
                # op = 0
                # for p in range(j, i+1):
                #     x,y = word1[p], word2[p]
                #     if x==y: continue
                #     if cnt[(y,x)] > 0: cnt[(y,x)] -= 1
                #     else:
                #         cnt[(x,y)] += 1
                #         op += 1
                x,y = word1[j], word2[j]
                if x != y:
                    if cnt[(y,x)] > 0: cnt[(y,x)] -= 1
                    else:
                        cnt[(x,y)] += 1
                        op += 1
                # 反转
                rev_cnt = collections.defaultdict(int)
                rev_op = 1
                for p in range(j, i+1):
                    x,y = word1[p], word2[i+j-p]
                    if x==y: continue
                    if rev_cnt[(y,x)] > 0: rev_cnt[(y,x)] -= 1
                    else:
                        rev_cnt[(x,y)] += 1
                        rev_op += 1
                res = min(res, f[j]+min(op, rev_op))
            f[i+1] = res
        return f[n]


sol = Solution()
result = [
    # sol.canMakeEqual(nums = [1,-1,1,-1,1], k = 3),
    # sol.canMakeEqual(nums = [-1,-1,-1,1,1,1], k = 5),
    # sol.canMakeEqual([1,-1,-1,-1,-1,1,1,1,-1], 3),
    # sol.countPermutations(complexity = [1,2,3]),
    # sol.countPermutations(complexity = [3,3,3,4,4,4]),
    # sol.countPartitions(nums = [9,4,1,3,7], k = 4),
    sol.minOperations(word1 = "abcdf", word2 = "dacbe"),
    sol.minOperations(word1 = "abceded", word2 = "baecfef"),
]
for r in result:
    print(r)