
from typing import List
import collections
import math
import bisect

class Solution271:
    def countPoints(self, rings: str) -> int:
        color2index = {
            "R": 0,
            "B": 1,
            "G": 2
        }
        records = [[False]*3 for _ in range(10)]
        while rings:
            color = rings[0]
            re = rings[1]
            records[int(re)][color2index[color]] = True
            rings = rings[2:]
        return sum([all(label) for label in records])

    """2104. 子数组范围和
给你一个整数数组 nums 。nums 中，子数组的 范围 是子数组中最大元素和最小元素的差值。 
返回 nums 中 所有 子数组范围的 和 。
子数组是数组中一个连续 非空 的元素序列。"""
    def subArrayRanges(self, nums: List[int]) -> int:
        n = len(nums)
        result = 0
        for i in range(n):
            nMin, nMax = nums[i], nums[i]
            for j in range(i+1, n):
                nMin = min(nMin, nums[j])
                nMax = max(nMax, nums[j])
                result += nMax - nMin
        return result

    """ 2105. 给植物浇水 II
模拟法即可 """
    def minimumRefill(self, plants: List[int], capacityA: int, capacityB: int) -> int:
        l, r = 0, len(plants)-1
        result = 0
        remainA, remainB = capacityA, capacityB
        while l < r:
            if remainA>=plants[l]:
                remainA -= plants[l]
            else:
                result += 1
                remainA = capacityA - plants[l]
            if remainB >= plants[r]:
                remainB -= plants[r]
            else:
                result += 1
                remainB = capacityB - plants[r]
            l += 1
            r -= 1
        if l==r:
            if max(remainA, remainB) < plants[l]:
                return result+1
        return result

    """ 2106. 摘水果
在一个无限的 x 坐标轴上, 分布一定的水果, 给定 startPos 和可以移动的步数 k, 计算可以拿到的最大数量 """
    def maxTotalFruits(self, fruits: List[List[int]], startPos: int, k: int) -> int:
        minL, maxL = fruits[0][0], fruits[-1][0]
        pos2index = lambda x: x-minL+1
        cumsum = [0] * (maxL - minL + 2)
        p = 1
        for pos, num in fruits:
            i = pos2index(pos)
            for j in range(p, i):
                cumsum[j] = cumsum[j-1]
            cumsum[i] = cumsum[i-1] + num
            p = i+1
        print(cumsum)

        def update(x, y):
            global result
            result = max(result, cumsum[pos2index(y)] - cumsum[pos2index(x)-1])
        
        global result
        result = 0

        if startPos > maxL:
            if startPos-k > maxL:
                return 0
            startPos = maxL
            k -= startPos-maxL
        if startPos < minL:
            if startPos+k < minL:
                return 0
            startPos = minL
            k -= minL-startPos

        update(max(minL, startPos-k), startPos)
        update(startPos, min(maxL, startPos+k))
        for i in range(1, k//2):
            s, e = max(startPos-i, minL), min(startPos+k-2*i, maxL)
            update(s, e)
            s, e = max(startPos-k+2*i, minL), min(startPos+i, maxL)
            update(s, e)
        return result

    def maxTotalFruits1(self, fruits: List[List[int]], startPos: int, k: int) -> int:
        cumsum = [0]
        pos = [float("-inf")]
        for p, num in fruits:
            pos.append(p)
            cumsum.append(num+cumsum[-1])
        result = 0
        # 遍历所有可能到达的区域
        for d1 in range(k+1):    # k+1
            d2 = max(k - 2*d1, 0)
            # 先向左
            l,r = startPos-d1, startPos+d2
            lindex,rindex = bisect.bisect_left(pos, l), bisect.bisect(pos, r)
            result = max(result, cumsum[rindex-1] - cumsum[lindex-1])
            # 先向右
            l,r = startPos-d2, startPos+d1
            lindex,rindex = bisect.bisect_left(pos, l), bisect.bisect(pos, r)
            result = max(result, cumsum[rindex-1] - cumsum[lindex-1])
        return result



sol = Solution271()
print(
    # sol.countPoints("B0B6G0R6R0R6G9"),
    # sol.subArrayRanges([1,2,3]),
    # sol.minimumRefill(plants = [1,2,4,4,5], capacityA = 6, capacityB = 5),

    # sol.maxTotalFruits1(fruits = [[2,8],[6,3],[8,6]], startPos = 5, k = 4),   # 9
    # sol.maxTotalFruits1(fruits = [[0,9],[4,1],[5,7],[6,2],[7,4],[10,9]], startPos = 5, k = 4),  # 14
    sol.maxTotalFruits1([[0,7],[7,4],[9,10],[12,6],[14,8],[16,5],[17,8],[19,4],[20,1],[21,3],[24,3],[25,3],[26,1],[28,10],[30,9],[31,6],[32,1],[37,5],[40,9]], 21, 30),
    sol.maxTotalFruits1([[200000,10000]], 0, 200000),   # 10000
    sol.maxTotalFruits1([[0,22],[1,15],[2,91],[3,50],[4,45],[5,61],[6,77],[7,86],[8,3],[10,71],[11,65],[12,37],[13,72],[14,77],[15,42],[17,43],[18,19],[20,33],[22,24],[24,45],[25,46],[26,10],[27,65],[28,49],[29,63],[30,75],[31,48],[32,72],[33,92],[34,88],[35,19],[36,69],[37,35],[38,80],[39,14],[40,87],[41,79],[42,47],[44,61],[45,94],[46,78],[47,43],[48,56],[50,50],[51,26],[52,99],[53,64],[54,99],[56,53],[57,19],[58,59],[59,23],[60,31],[61,36],[62,75],[63,11],[64,37],[65,86],[66,64],[67,62],[68,56],[69,87],[70,36],[71,22],[74,29],[75,17],[76,72],[77,78],[78,92],[79,64],[80,58],[81,94],[83,34],[84,56],[85,48],[86,70],[87,93],[88,83],[89,85],[90,78],[91,82],[92,98],[93,13],[94,53],[95,41],[96,42],[97,67],[98,87],[99,47]], 100, 94),
)


