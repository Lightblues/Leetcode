
from itertools import accumulate
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

    """2104. 子数组范围和 #medium
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

    """ 2105. 给植物浇水 II #medium
#模拟 即可 """
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

    """ 2106. 摘水果 #hard #题型 #star
在一个无限的 x 坐标轴上, 分布一定的水果, 给定 startPos 和可以移动的步数 k, 计算可以拿到的最大数量
限制: 水果位置 2e5; 有水果的位置数量 n 2e5; 可以走的步数 k 2e5;
思路1: #双指针. 比较困难的那种.
    对于 [l,r] 区间, 可以在 O(1) 时间判断是否可以从 startPos在k步限制内到达.
    我们用 #滑动窗口 统计区间可达部分的水果数量.
        如何滑动? 遍历右端点, 根据条件移动左端点.
    为什么单向移动不会出现遗漏? 
        假设 l<r<startPos, 若 [l,startPos] 检查合法, 则在右端点从r右移到startPos的过程中, l并不会发生移动! 因此不会发生遗漏.
    复杂度: O(n)
思路0: 枚举可能的部分, #二分 搜索. 用到 #前缀和
    下面的实现中直接枚举 k次, 感觉复杂度较高...
    复杂度: O(k logn)
思路2: 更为「直观」的想法, 是分别尝试「先向右再向左」和「先向左再向右」, 但写了半天一堆错...
    参见 [灵神](https://leetcode.cn/problems/maximum-fruits-harvested-after-at-most-k-steps/solution/qian-zhui-he-er-fen-by-endlesscheng-jjn4/).

"""
    def maxTotalFruits(self, fruits: List[List[int]], startPos: int, k: int) -> int:
        cumsum = [0]
        pos = [float("-inf")]
        for p, num in fruits:
            pos.append(p)
            cumsum.append(num+cumsum[-1])
        result = 0
        # 遍历所有可能到达的区域: 可以先往一个方向前进 d1, 然后折往另一方向前进 d2
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


    def maxTotalFruits0(self, fruits: List[List[int]], startPos: int, k: int) -> int:
        fruits.append((float('inf'), 0))
        n = len(fruits)
        fs = [i[1] for i in fruits]
        acc = list(accumulate(fs, initial=0))
        def test(l,r):
            # 判断是否可以在k步内到达[l,r]
            l,r = fruits[l][0], fruits[r][0]
            l,r  = (startPos-r), (startPos-l)
            if l*r >= 0:
                return max(abs(l), abs(r)) <= k
            else:
                return 2*min(abs(l), abs(r)) + max(abs(l), abs(r)) <= k
        ans = 0
        l = 0
        # idx = bisect.bisect_left(fruits, startPos, key=lambda x:x[0])
        # for r in range(idx, n):
        for r in range(0, n):
            while l<=r and not test(l,r):
                l += 1
            # 区间是合法的!
            if l<=r:
                ans = max(ans, acc[r+1]-acc[l])
        return ans




sol = Solution271()
print(
    # sol.countPoints("B0B6G0R6R0R6G9"),
    # sol.subArrayRanges([1,2,3]),
    # sol.minimumRefill(plants = [1,2,4,4,5], capacityA = 6, capacityB = 5),

    sol.maxTotalFruits(fruits = [[2,8],[6,3],[8,6]], startPos = 5, k = 4),   # 9
    sol.maxTotalFruits(fruits = [[0,9],[4,1],[5,7],[6,2],[7,4],[10,9]], startPos = 5, k = 4),  # 14
    sol.maxTotalFruits([[0,7],[7,4],[9,10],[12,6],[14,8],[16,5],[17,8],[19,4],[20,1],[21,3],[24,3],[25,3],[26,1],[28,10],[30,9],[31,6],[32,1],[37,5],[40,9]], 21, 30),
    sol.maxTotalFruits([[200000,10000]], 0, 200000),   # 10000
    sol.maxTotalFruits([[0,10000]], 20000, 20000),   # 10000
)


