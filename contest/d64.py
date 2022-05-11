from typing import List, Optional, Generator, Tuple, Literal
import collections
import math
import bisect
import heapq
import functools, itertools
# from functools import lru_cache
# import sys, os
# sys.setrecursionlimit(10000)
# from utils_leetcode import testClass
from structures import ListNode, TreeNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-64
@20220223 补 """
class Solution:
    """ 2053. 数组中第 K 个独一无二的字符串 """
    def kthDistinct(self, arr: List[str], k: int) -> str:
        c = collections.Counter(arr)
        # strOrder = list(set(arr)) # 注意set是无序的!!
        strOrder = []
        for s in arr:
            if s not in strOrder: strOrder.append(s)
        cum = 0
        for s in strOrder:
            cum += c[s]==1
            if cum==k: return s
        return ""
    
    """ 2054. 两个最好的不重叠活动
有一组活动 (start, end, value), 可以选择其中一个/两个不重叠的活动, 要求value最大化.
要求: 两个活动不重叠, 也即 end1 < start2
复杂度: 活动数量 1e5, 起止时间 1e9

思路1: #统一排序
将活动的s/e时间统一进行排序, 排序元素为 (time, type, value), 这里的time是活动的起止时间, type是0/1, 0表示s, 1表示e, value是活动的value.
维护 bestEnd 为截止到当前时间已经结束的单个事件的最大value. 这样在遍历排好序的数组的过程中: 1) type=0, 更新 `ans = max(ans, bestEnd+value)`; 2) 否则更新 `bestEnd = max(bestEnd, value)`
注意, 这里有效的排序是 time和type. 题目要求两活动不重叠, 因此将 start排在end 之前 —— 这样如果有s/e时间相同, 会先更新 ans, 此时用的是上一时刻的 bestEnd.
[官方解答](https://leetcode.cn/problems/two-best-non-overlapping-events/solution/liang-ge-zui-hao-de-bu-zhong-die-huo-don-urq5/) 很优雅

思路2: 排序 + #最小堆
更为直观的思路: 先对于start进行排序. 在遍历的过程中, 如何得到早于该时刻的所有事件的最大value? 显然可以用一个最小堆来维护.
具体而言, 堆的元素为 `(end, value)`. 遍历过程中同样维护 bestEnd: 对于当前事件的 start, 从堆出取出所有 end_i < start 来更新 bestEnd.
参见 [here](https://leetcode.cn/problems/two-best-non-overlapping-events/solution/yong-you-xian-dui-lie-wei-hu-ling-yi-ge-8ld3x/)
"""
    def maxTwoEvents_0(self, events: List[List[int]]) -> int:
        l = []
        for s,e,v in events:
            l.append((s,0,v))
            l.append((e,1,v))
        l.sort()
        bestEnd = 0
        ans = 0
        for time, type, value in l:
            if type==0: # 由于 start 排在前面, 如有重复 s/e 此时 bestEnd 还是上一时刻的.
                ans = max(ans, bestEnd+value)
            else:
                bestEnd = max(bestEnd, value)
        return ans
    
    def maxTwoEvents(self, events: List[List[int]]) -> int:
        # 思路2: 排序 + #最小堆
        events.sort()
        # 存储 (end, value) 的heap
        h = []
        bestEnd = 0
        ans = 0
        for s,e,v in events:
            while h and h[0][0]<s:
                bestEnd = max(bestEnd, heapq.heappop(h)[1])
            ans = max(ans, bestEnd+v)
            heapq.heappush(h, (e,v))
        return ans
    
    """ 2055. 蜡烛之间的盘子
一个数组包括两种元素 (蜡烛、盘子). 给一个查询 [l,r], 要求返回在该子序列中, 被蜡烛包围的盘子数量.
思路: 二分搜索. 先抽取提取所有蜡烛的idx, 然后在这个数组中进行二分. 注意边界判断.
"""
    def platesBetweenCandles(self, s: str, queries: List[List[int]]) -> List[int]:
        n = len(s)
        candles = [i for i, c in enumerate(s) if c=="|"]
        ans = []
        for l,r in queries:
            lidx = bisect.bisect_left(candles, l)
            ridx = bisect.bisect_left(candles, r)
            # 注意 idx 可能为 len(candles), 要避免访问越界
            if ridx>len(candles)-1 or candles[ridx]>r: ridx -= 1
            if lidx >= ridx: ans.append(0)
            else: ans.append(candles[ridx]-candles[lidx]-(ridx-lidx))
        return ans
    
    """ 2056. 棋盘上有效移动组合的数目
大小为 8*8 的棋盘上有三种类型的的棋子 车, 象, 后 (rook, bishop, queen), 分别可以按照横竖、斜, 以及两者的组合这些方向移动.
每个棋子可以在指定的方向上移动 k步, 然后停在该点. 若一个棋子先到达某点, 另一个棋子也需要经过该点, 则冲突.
已知棋盘上最多有四个棋子 (最多只有一个后), 要求返回最终所有棋子的组合中有效移动的组合的数目.

思路: #模拟. 先根据棋子类型计算出其所有可能的 (direction, step) 组合, 然后模拟移动 (也即判断该组合是否合法).
见 [here](https://leetcode.cn/problems/number-of-valid-move-combinations-on-chessboard/solution/python-producthan-shu-de-yong-fa-by-9813-p0cp/)
总结: 可以充分利用 Python 的相关函数检查代码, 例如这里用了两次 product 来 生成棋子的走法, 和生成所有棋子的走法组合.
    
[这里](https://leetcode.cn/problems/number-of-valid-move-combinations-on-chessboard/solution/go-mo-ni-by-endlesscheng-kjpt/) 还用了 DFS 的思路, 但复杂度上应该差不多

输入：pieces = ["queen","bishop"], positions = [[5,7],[3,4]]
输出：281
解释：总共有 12 * 24 = 288 种移动组合。
但是，有一些不有效的移动组合：
- 如果后停在 (6, 7) ，它会阻挡象到达 (6, 7) 或者 (7, 8) 。
- 如果后停在 (5, 6) ，它会阻挡象到达 (5, 6) ，(6, 7) 或者 (7, 8) 。
- 如果象停在 (5, 2) ，它会阻挡后到达 (5, 2) 或者 (5, 1) 。
在 288 个移动组合当中，281 个是有效的。


来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/number-of-valid-move-combinations-on-chessboard
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
    def countCombinations(self, pieces: List[str], positions: List[List[int]]) -> int:
        """ 解法1, 利用了 Python的 product 函数 """
        # https://leetcode.cn/problems/number-of-valid-move-combinations-on-chessboard/solution/python-producthan-shu-de-yong-fa-by-9813-p0cp/
        DIRS = {
            "rook": ((0, 1), (0, -1), (1, 0), (-1, 0)),
            "bishop": ((1, 1), (1, -1), (-1, 1), (-1, -1)),
            "queen": ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)),
        }
        # 用于 typing
        Role = Literal["rook", "bishop", "queen"]
        State = Tuple[int, int, int, int, int]
        def getNextState(role: Role, curX: int, curY: int) -> Generator[State, None, None]:
            """每一个状态用起点，方向，距离表示"""
            yield curX, curY, 0, 0, 0
            for dist, (dx, dy) in itertools.product(range(1, 8), DIRS[role]):
                if 1 <= curX + dx * dist <= 8 and 1 <= curY + dy * dist <= 8:
                    yield curX, curY, dx, dy, dist

        def checkAllStates(allStates: Tuple[State]) -> bool:
            """所有棋子同时移动，检查是否有冲突"""
            maxT = max([s[4] for s in allStates])
            for dist1 in range(1, maxT+1):
            # for dist1 in range(8):
                visited = set()
                for x, y, dx, dy, dist2 in allStates:
                    curDist = min(dist1, dist2)
                    if (x + dx * curDist, y + dy * curDist) in visited:
                        return False
                    visited.add((x + dx * curDist, y + dy * curDist))
            return True

        return sum(
            checkAllStates(allStates)
            for allStates in itertools.product(
                *(getNextState(role, x, y) for role, (x, y) in zip(pieces, positions))
            )
        )


sol = Solution()
result = [
    # sol.kthDistinct(["d","b","c","b","c","a"], 2),   
    
    sol.maxTwoEvents([[1,3,2],[4,5,2],[2,4,3]]),
    sol.maxTwoEvents(events = [[1,3,2],[4,5,2],[2,4,3]]),
    sol.maxTwoEvents(events = [[1,3,2],[4,5,2],[1,5,5]]),
    
    
    # sol.platesBetweenCandles(s = "**|**|***|", queries = [[2,5],[5,9], [9,9]]),
    # sol.platesBetweenCandles(s = "***|**|*****|**||**|*", queries = [[1,17],[4,5],[14,17],[5,11],[15,16]]),
    
    # sol.countCombinations(pieces = ["queen","bishop"], positions = [[5,7],[3,4]]),
]
for r in result:
    print(r)
