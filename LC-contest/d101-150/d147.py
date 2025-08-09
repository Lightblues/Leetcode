from typing import *
import heapq

""" 
https://leetcode.cn/contest/biweekly-contest-147
Easonsi @2025 """

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
     """
    def longestSubsequence(self, nums: List[int]) -> int:

sol = Solution()
result = [
    # sol.hasMatch(s = "leetcode", p = "ee*e"),
    # sol.hasMatch(s = "luck", p = "u*"),
    testClass(zip(["TaskManager", "add", "edit", "execTop", "rmv", "add", "execTop"], [[[[1, 101, 10], [2, 102, 20], [3, 103, 15]]], [4, 104, 5], [102, 8], [], [101], [5, 105, 15], []]))
]
for r in result:
    print(r)