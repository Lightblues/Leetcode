from easonsi import utils
from easonsi.util.leetcode import *
""" 
https://leetcode.cn/contest/weekly-contest-285

@20220320 """
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


    """ 2211. 统计道路上的碰撞次数 #medium 一条公路上有 LRS表示汽车行驶的方向, S表示静止. 问会发生碰撞的车的数量
思路1: #模拟
思路1.1: 实际上, 用栈更加方便些
思路2: #思维 去掉左右两侧分别往左, 往右的, 其他移动的车必然会碰撞!
    from 灵神
"""
    def countCollisions(self, directions: str) -> int:
        # 思路1: #模拟 比较傻
        ans = 0
        last = 'L'
        nR = 0
        for d in directions:
            if d=='L':
                if last=='R':
                    ans += nR+1
                elif last=='S':
                    ans += 1
                    last = 'S'
                nR = 0
            elif d=='S':
                if last=='R':
                    ans += nR
                    nR = 0
                last = 'S'
            else:
                nR += 1
                last = 'R'
        return ans
    def countCollisions(self, directions: str) -> int:
        # 思路1.1: 实际上, 用栈更加方便些
        s = []
        ans = 0
        for d in directions:
            if d=='L':
                if not s: continue
                while s and s[-1]=='R':
                    s.pop(); ans += 1
                ans += 1
                s.append('S')
            elif d=='S':
                while s and s[-1]=='R':
                    s.pop(); ans += 1
                s.append('S')
            else:
                s.append('R')
        return ans
    def countCollisions(self, directions: str) -> int:
        # 思路2: #思维
        directions = directions.lstrip('L')  # 前缀向左的车不会发生碰撞
        directions = directions.rstrip('R')  # 后缀向右的车不会发生碰撞
        return len(directions) - directions.count('S')  # 剩下非停止的车必然会碰撞



    
    """ 6029. 射箭比赛中的最大得分
12个区域得分分别为 0...11; 如果 `ak >= bk` ，那么 Alice 得 `k` 分。如果 `ak < bk` ，则 Bob 得 `k` 分; 现在知道Alice的分布, 要求Bob得分最高的一种方式
DFS即可
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

    sol.countCollisions(directions = "RLRSLL"),
    sol.countCollisions("LLRR"),

    # sol.maximumBobPoints(numArrows = 9, aliceArrows = [1,1,0,1,0,0,2,1,0,1,2,0]),
    # sol.maximumBobPoints(numArrows = 3, aliceArrows = [0,0,1,0,0,0,0,0,0,0,0,2]),
]
for r in result:
    print(r)