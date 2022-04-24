from email.policy import default
from os import times
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
    """ 6041. 多个数组求交集
求给定的所有数组的交集. 思路: 直接调用 Python API 暴力解决
"""
    def intersection(self, nums: List[List[int]]) -> List[int]:
        result = set(nums[0])
        for i in nums[1:]:
            result = result.intersection(set(i))
        return sorted(list(result))

    def countLatticePoints(self, circles: List[List[int]]) -> int:
        """ 6042. 统计圆内格点数目
每个圆通过 (x,y,r) 所定义, 要求计算这些圆所覆盖的整数点数量. 思路: 暴力遍历
"""
        def inCircle(x, y, r):
            # 归到原点
            return x**2+y**2 <= r**2
        result = set()
        for x,y, r in circles:
            for i in range(-r, +r+1):
                for j in range(-r, +r+1):
                    if inCircle(i, j, r):
                        result.add((x+i, y+j))
        return len(result)
    
    def countRectangles(self, rectangles: List[List[int]], points: List[List[int]]) -> List[int]:
        """ 6043. 统计包含每个点的矩形数目
给定一组点所定义的矩形和一组点, 对于每个点, 要求判断包含该点的矩形的数量
重点是数量级分析: `1 <= rectangles.length, points.length <= 5 * 10^4` 因此无法暴力判断
注意这里的条件, (x,y) 中, `1 <= x <= 1^9; 1 <= y <= 100`, 因此, 构建 y2x, 分别排序即可.
此时, 对于每一个点, 从 `recY >= pY` 的最多 100 个序列中进行 bisect 即可.
"""
        y2x = collections.defaultdict(list)
        for x,y in rectangles:
            y2x[y].append(x)
        for y in y2x:
            y2x[y] = sorted(y2x[y])
        result = []
        ys = sorted(y2x.keys(), reverse=True)
        for px,py in points:
            c = 0
            for y in ys:
                if py>y: break
                c += len(y2x[y]) - bisect.bisect_left(y2x[y], px)
            result.append(c)
        return result
    
    def fullBloomFlowers(self, flowers: List[List[int]], persons: List[int]) -> List[int]:
        """ 6044. 花期内花的数目
每朵花 [start, end] 定义开花时期; 对于每一个在某时刻来的人, 返回此时开花数量.
思路: 排序累计, 二分.
转化为, 统计时间维度上, 不同区间内的花朵数量 (这样就可以二分查找了). 为此, 对于 start, end 两类节点统一排序, 然后记录各个变化的时间点即可
具体而言, 用 `timeSplits, flowerNums` 两个数组记录变化时刻和该区间内的花朵数量.
        """
        starts = [(f[0], "start") for f in flowers]
        ends = [(f[1]+1, "end") for f in flowers]
        flowerTimes = sorted(list(collections.Counter(starts + ends).items()))
        
        # 例如, [0, 2, 3, ...], [0, 1,...] 表示 0-1时刻有0朵花, 2-2时刻有1朵花, ...
        timeSplits, flowerNums = [0], [0]
        for (time, type), count in flowerTimes:
            if type == "start":
                if time != timeSplits[-1]:
                    timeSplits.append(time)
                    flowerNums.append(flowerNums[-1] + count)
                else:
                    flowerNums[-1] += count
            else:
                if time != timeSplits[-1]:
                    timeSplits.append(time)
                    flowerNums.append(flowerNums[-1] - count)
                else:
                    flowerNums[-1] -= count
        result = []
        for t in persons:
            idx = bisect.bisect_right(timeSplits, t) - 1
            result.append(flowerNums[idx])
        return result

sol = Solution()
result = [
    # sol.intersection(nums = [[3,1,2,4,5],[1,2,3,4],[3,4,5,6]]),
    # sol.countLatticePoints(circles = [[2,2,2],[3,4,1]]),
    
    sol.countRectangles(rectangles = [[1,1],[2,2],[3,3]], points = [[1,3],[1,1]]),
    sol.countRectangles(rectangles = [[1,2],[2,3],[2,5]], points = [[2,1],[1,4]]),
    
    # sol.fullBloomFlowers(flowers = [[1,6],[3,7],[9,12],[4,13]], persons = [2,3,7,11]),
    # sol.fullBloomFlowers(flowers = [[1,10],[3,3]], persons = [3,3,2]),
]
for r in result:
    print(r)