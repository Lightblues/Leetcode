from itertools import accumulate
from typing import *
import heapq
from math import inf

""" 
https://leetcode.cn/contest/biweekly-contest-147
Easonsi @2025 

- T2 的懒删除, 意识到工程优化需要考虑边界! 两个数据存储需要同步删除
- T3 DP 的优化的递归计算有意思
- T4 前后缀分解代码实现很重要! ling 的代码真的优雅
"""

""" 3408. 设计任务管理器
思路1: #懒删除
[ling](https://leetcode.cn/problems/design-task-manager/solutions/3039132/lan-shan-chu-dui-pythonjavacgo-by-endles-q5vb/) 的思路更清楚! 
"""
class TaskManager:
    def __init__(self, tasks: List[List[int]]):
        self.h = []
        self.tid2info = {}
        for uid, tid, p in tasks:
            self.tid2info[tid] = (uid, p)
            heapq.heappush(self.h, (-p, -tid, uid))  # 优先级, 任务ID, 用户ID

    def add(self, userId: int, taskId: int, priority: int) -> None:
        heapq.heappush(self.h, (-priority, -taskId, userId))
        self.tid2info[taskId] = (userId, priority)

    def edit(self, taskId: int, newPriority: int) -> None:
        uid, p = self.tid2info[taskId]
        heapq.heappush(self.h, (-newPriority, -taskId, uid))
        self.tid2info[taskId] = (uid, newPriority)

    def rmv(self, taskId: int) -> None:
        self.tid2info.pop(taskId)

    def execTop(self) -> int:
        while self.h:
            p, tid, uid = heapq.heappop(self.h)
            if -tid not in self.tid2info: continue
            if self.tid2info[-tid][1] != -p or self.tid2info[-tid][0] != uid: continue
            self.tid2info.pop(-tid)  # NOTE: 不然会有错!! 考虑 corner case
            return uid
        return -1


class Solution:
    """ 3407. 子字符串匹配模式
[ling](https://leetcode.cn/problems/substring-matching-pattern/solutions/3038944/ku-han-shu-jian-ji-xie-fa-pythonjavacgo-sukdf/) 拓展到多个 * 
    """
    def hasMatch(self, s: str, p: str) -> bool:
        l,r = p.split("*")
        if not l or not r:
            if not l and not r: return True
            return (l or r) in s
        l_index = s.find(l)
        if l_index == -1: return False
        r_index = s.rfind(r)
        if r_index == -1: return False
        return l_index+len(l) <= r_index

    """ 3409. 最长相邻绝对差递减子序列 #medium 找出最长子序列, 要求相邻数字的绝对差递减 (可以相等)
限制: n 1e4; 数字范围 D 300
思路1: #DP + 优化
    考虑 f(i,j) 表示以 nums[i] 结尾, 且差值为 j 的最长子序列长度
      这样的话, 已有 O(nD) 个状态; 状态转移: 需要考虑倒数第二个数字 nums[i]+/-j 并枚举倒数第二第三的差值 j,j+1... 整体复杂度至少 O(nD^2) -- #TLE!
    优化: 不妨考虑 f(i,j) 表示以 nums[i] 结尾, 且最后两数差值 *至少* 为 j 的最长子序列长度; -- 这样, 利用转移方程之间的关系:
      - 最后两数只差 > j: 有 f(i,j) = f(i+1,j)
      - 最后两数只差 == j: 有 f(i,j) = max{ f(last[nums[i]-j], j), f(last[nums[i]+j], j) } + 1
      - 单独作为第一个数字, 有 f(i,j) = 1
    最终转移方程为3中情况取 max
    复杂度: O(nD)
[ling](https://leetcode.cn/problems/longest-subsequence-with-decreasing-adjacent-difference/solutions/3038930/zhuang-tai-she-ji-you-hua-pythonjavacgo-qy2bu/)
     """
    def longestSubsequence(self, nums: List[int]) -> int:
        n = len(nums); mx = max(nums)
        last = [-1]*(mx+1)
        f = [[0]*(mx+2) for _ in range(n)]  # 因为转移的时候要用到 f(i+1,j)
        for i,x in enumerate(nums):
            for j in range(mx, -1, -1):  # 从大到小枚举 j
                f[i][j] = max(f[i][j+1], 1)
                if x-j>=0 and last[x-j]>=0:
                    f[i][j] = max(f[i][j], f[last[x-j]][j]+1)
                if x+j<=mx and last[x+j]>=0:
                    f[i][j] = max(f[i][j], f[last[x+j]][j]+1)
            last[x] = i
        return max(map(max, f))
    

    """ 3410. 删除所有值为某个元素后的最大子数组和 #hard *最多* 删除数组中所有值为x的元素, 求最大子数组和
限制: n 1e5; 数字范围 1e6
思路1: #线段树
思路2: #前后缀分解
    易知, 被删除的一个是负数!
    假设被删除的是 x = nums[i], 考虑 pre[i], suf[i] 分别表示删除所有x后, i位置前缀/后缀的最大子数组和. 考虑pre[i]
        假设前面一个x出现的位置是j
        1. 若 pre[i] 包含位置j, 则 pre[i] = pre[j] + sum(nums[j+1:i-1]) = pre[j] + s[i] - s[j+1], 其中s是前缀和
        2. 若不包含位置j, 又因为x一定是负数, 所以 pre[i] = "以i-1结尾的子数组和" f[i-1]
        因此, pre[i] = max(pre[j] + s[i] - s[j+1], f[i-1])
    同理, suf[i] = max(suf[j] + s[j] - s[i+1], f'[i+1]) 其中j为下一个x出现的位置
    最终答案
        - 不删除, 即原本的 "最大子数组和"
        - 删除: max(pre[i] + suf[i], pre[i], suf[i]) -- 因为pre/suf可能是负数
[ling](https://leetcode.cn/problems/maximize-subarray-sum-after-removing-all-occurrences-of-one-element/solutions/3039428/liang-chong-fang-fa-xian-duan-shu-qian-h-961z/)
"""
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        s = list(accumulate(nums, initial=0))
        pre_f = [0]*n; pre = 0
        pre_j = [-1]*n; idx = {}
        for i,x in enumerate(nums):
            pre_f[i] = max(pre, 0) + x
            pre = max(pre+x, x)
            if x in idx: pre_j[i] = idx[x]
            idx[x] = i
        suf_f = [0]*n; pre = 0
        suf_j = [n]*n; idx = {}
        for i in range(n-1, -1, -1):
            x = nums[i]
            suf_f[i] = max(pre, 0) + x
            pre = max(pre+x, x)
            if x in idx: suf_j[i] = idx[x]
            idx[x] = i
        # 
        pre = [-inf] * n
        for i,x in enumerate(nums):
            if i>0: pre[i] = pre_f[i-1]
            if (j := pre_j[i]) >= 0:
                pre[i] = max(pre[i], pre[j] + s[i] - s[j+1])
        suf = [-inf] * n
        for i in range(n-1, -1, -1):
            if i<n-1: suf[i] = suf_f[i+1]
            if (j := suf_j[i]) < n:
                suf[i] = max(suf[i], suf[j] + s[j] - s[i+1])
        ans = max(pre_f)
        for i,x in enumerate(nums):
            ans = max(ans, pre[i] + suf[i], pre[i], suf[i])
        return ans



sol = Solution()
result = [
    # sol.hasMatch(s = "leetcode", p = "ee*e"),
    # sol.hasMatch(s = "luck", p = "u*"),

    # sol.longestSubsequence(nums = [10,20,10,19,10,20]),

    sol.maxSubarraySum(nums = [-3,2,-2,-1,3,-2,3]),
    sol.maxSubarraySum([1,2,3,4]),
]
for r in result:
    print(r)