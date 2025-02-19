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
https://leetcode.cn/contest/weekly-contest-427

T4 排序构造! 
Easonsi @2024 """
class Solution:
    """ 3379. 转换数组 """
    def constructTransformedArray(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [0] * n
        for i,x in enumerate(nums):
            res[i] = nums[(i+x)%n]
        return res
    
    """ 3380. 用点构造面积最大的矩形 I """
    
    """ 3381. 长度可被 K 整除的子数组的最大元素和 #medium 计算一个数组中, 满足长度为k的倍数的子数组的最大和. 
限制: n 2e5
思路1: 前缀和 + 维护同组最小值
    对于 i, i+k, i+2k, ... 在计算子数组最大和的时候, 显然我们只关心左边最小的那个!
    NOTE: left_min 应该初始化为什么? inf!
    from ling https://leetcode.cn/problems/maximum-subarray-sum-with-length-divisible-by-k/solutions/3013897/qian-zhui-he-mei-ju-you-wei-hu-zuo-pytho-0t8p/
     """
    def maxSubarraySum(self, nums: List[int], k: int) -> int:
        acc = list(accumulate(nums, initial=0))
        left_min = [inf] * k
        ans = -inf
        for i in range(len(acc)):
            if i >= k:  # NOTE the first k prefix should also be considered to init left_min!
                ans = max(ans, acc[i] - left_min[i%k])
            left_min[i%k] = min(left_min[i%k], acc[i])
        return ans
    
    """ 3382. 用点构造面积最大的矩形 II #hard 给定平面上一组点, 求最大面积的矩形, 要求边界和内部不包含其他点
限制: n 2e5
思路1: #排序, 维护历史最右的边界! 
    如何检查 (x1,y1) 和 (x2,y2) 构成的矩形之间没有其他点? -- 可以统计 "x<=x1 并且y在 [y1,y2] 的点的数量", 以及 "x<=x2 并且y在 [y1,y2] 的点的数量", 如果正好差2就是! (注意四个角的点都要取到)
    可以对于 (x,y) 两个坐标排序, 然后遍历pairwise (注意到合法的右边一定是相同的x, y1<y2 是相邻的两个点!)
    ling https://leetcode.cn/problems/maximum-area-rectangle-with-point-constraints-ii/solutions/3013907/chi-xian-xun-wen-chi-san-hua-shu-zhuang-gd604/
    """
    def maxRectangleArea(self, xCoord: List[int], yCoord: List[int]) -> int:
        from sortedcontainers import SortedList
        from itertools import pairwise
        points = sorted(zip(xCoord, yCoord)) # sort by x, then y
        pair_to_right = {} # {range: (x,v)}, where range is (y1, y2) pair, x is the previous right bound, v is the number of points
        sl = SortedList([points[0][1]])
        ans = -1
        for p1, p2 in pairwise(points):
            sl.add(p2[1])   # add the new y first
            if p1[0] != p2[0]: continue

            range_ = (p1[1], p2[1])
            x = p1[0]
            val = sl.bisect_right(p2[1]) - sl.bisect_left(p1[1])
            if range_ in pair_to_right and val == pair_to_right[range_][1]+2:
                ans = max(ans, (p2[1]-p1[1]) * (x-pair_to_right[range_][0]))
            pair_to_right[range_] = (x, val) # update the right bound
        return ans


sol = Solution()
result = [
    # sol.constructTransformedArray(nums = [3,-2,1,1]),
    sol.maxSubarraySum(nums = [-1,-2,-3,-4,-5], k = 4),
    sol.maxSubarraySum( nums = [-5,1,2,-3,4], k = 2),
    sol.maxSubarraySum([-10,-1], 1),
    sol.maxSubarraySum([9,-11,15], 2),
    # sol.maxRectangleArea(xCoord = [1,1,3,3], yCoord = [1,3,1,3]),
    # sol.maxRectangleArea(xCoord = [1,1,3,3,1,3], yCoord = [1,3,1,3,2,2]),
]
for r in result:
    print(r)
