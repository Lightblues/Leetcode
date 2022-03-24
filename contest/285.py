from typing import List, Optional
import collections
import math
import bisect
import heapq
from functools import lru_cache
# import sys
# sys.setrecursionlimit(10000)

from structures import ListNode, TreeNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220223 补 """
class Solution:
    """ 6027. 统计数组中峰和谷的数量
首尾的不算, 相同数字算一个峰/谷
例如 [2,4,1,1,6,5] 就有三个

遍历, 模拟
 """
    def countHillValley(self, nums: List[int]) -> int:
        res = 0
        direction = None
        for i in range(1, len(nums)):
            if nums[i] == nums[i-1]:
                continue
            dir = 1 if nums[i] > nums[i-1] else -1
            if direction is None:
                direction = dir
            else:
                if dir != direction:
                    direction = dir
                    res += 1
        return res

    """ 6028. 统计道路上的碰撞次数 
给定一个字符串表示车辆方向. 
`'L'`、`'R'` 或 `'S'` 分别表示第 `i` 辆车是向 **左** 、向 **右** 或者 **停留** 在当前位置。每辆车移动时 **速度相同** 。
相向碰撞 2分, 一个静止的1分; 碰撞后都静止; 求最后的分数。

模拟. 注意一些边界讨论.
"""
    def countCollisions(self, directions: str) -> int:
        res = 0
        leftLimit = False # 边界
        last = None # 上一辆车的状态
        numRight = 0 # 记录存在的向右车, 在碰到S或L时累计
        for d in directions:
            if d == "L":
                if last == "R":
                    res += numRight+1
                    leftLimit = True
                    last = "S"
                    numRight = 0
                elif leftLimit:
                    res += 1
                    last = "S"
            elif d=="S":
                leftLimit = True
                last = "S"
                if numRight>0:
                    res += numRight
                    numRight = 0
            else:
                numRight += 1
                last = 'R'
        return res

    """ 6029. 射箭比赛中的最大得分
12个区域得分分别为 0...11
如果 `ak >= bk` ，那么 Alice 得 `k` 分。如果 `ak < bk` ，则 Bob 得 `k` 分
现在知道Alice的分布, 要求Bob得分最高的一种方式

DBS即可
     """
    def maximumBobPoints(self, numArrows: int, aliceArrows: List[int]) -> List[int]:
        maxScore = 0
        n = len(aliceArrows)
        bobArrows = [0] * n
        res = None
        def dfs(idx, remainArrows, score):
            nonlocal maxScore, res
            if idx == n or remainArrows==0:
                if score > maxScore:
                    maxScore = score
                    res = bobArrows[:]
                    if remainArrows>0:
                        res[0] += remainArrows
                return
            if remainArrows > aliceArrows[idx]:
                bobArrows[idx] = aliceArrows[idx]+1
                dfs(idx+1, remainArrows-aliceArrows[idx]-1, score+idx)
                bobArrows[idx] = 0
            dfs(idx+1, remainArrows, score)
        dfs(0, numArrows, 0)
        print(maxScore)
        return res

    """ 6030. 由单个字符重复的最长子字符串
给定一个字符串和一组查询, 要求返回一个数组, 每一个元素为, 经过下面的操作后, 字符串中留下的重复字符串子串的最大长度.
第 `i` 个查询会将 `s` 中位于下标 `queryIndices[i]` 的字符更新为 `queryCharacters[i]` 。

输入：s = "babacc", queryCharacters = "bcb", queryIndices = [1,3,3]
输出：[3,3,4]
解释：
- 第 1 次查询更新后 s = "bbbacc" 。由单个字符重复组成的最长子字符串是 "bbb" ，长度为 3 。
- 第 2 次查询更新后 s = "bbbccc" 。由单个字符重复组成的最长子字符串是 "bbb" 或 "ccc"，长度为 3 。
- 第 3 次查询更新后 s = "bbbbcc" 。由单个字符重复组成的最长子字符串是 "bbbb" ，长度为 4 。
因此，返回 [3,3,4] 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/longest-substring-of-one-repeating-character
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

TODO: 看题解吧
 """
    def longestRepeating(self, s: str, queryCharacters: str, queryIndices: List[int]) -> List[int]:
        len2line = collections.defaultdict(set)
        lastCh = None
        lastLen = 0
        for idx,ch in enumerate(s+'#'):
            if lastCh is None:
                lastCh = ch
                continue
            if ch==lastCh:
                lastLen += 1
            else:
                len2line[lastLen].add(idx-lastLen)
                lastCh = ch
                lastLen = 1
        res = []
        for idx, ch in zip(queryIndices, queryCharacters):
            pass

sol = Solution()
result = [
    # sol.countHillValley(nums = [2,4,1,1,6,5]),
    # sol.countHillValley([1,2,3]),

    # sol.countCollisions(directions = "RLRSLL"),
    # sol.countCollisions("LLRR"),

    # sol.maximumBobPoints(numArrows = 9, aliceArrows = [1,1,0,1,0,0,2,1,0,1,2,0]),
    # sol.maximumBobPoints(numArrows = 3, aliceArrows = [0,0,1,0,0,0,0,0,0,0,0,2]),
]
for r in result:
    print(r)