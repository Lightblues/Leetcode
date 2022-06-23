from cmath import pi
from typing import List
import collections
import math
import bisect
import heapq

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220223 补 """
class SolutionD68:
    """ 2160. 拆分数位后四位数字的最小和 """
    def minimumSum(self, num: int) -> int:
        ints = [int(i) for i in str(num)]
        ints.sort()
        return sum(ints[:2])*10 + sum(ints[2:])

    """ 2161. 根据给定数字划分数组 """
    def pivotArray(self, nums: List[int], pivot: int) -> List[int]:
        left, right = [], []
        for num in nums:
            if num < pivot:
                left.append(num)
            if num > pivot:
                right.append(num)
        return left + [pivot]*(len(nums)-len(left)-len(right)) + right


    """ 2162. 设置时间的最少代价
- 设置四位的时间, 前后两位分别表示分钟和秒钟, 例如 `8090` 表示 80*60+90 秒
- 给定 startAt ，moveCost ，pushCost 和 targetSeconds 分别表示初始的手指位置, 移动和按按钮的代价, 以及目标的秒数, 要求返回最小的代价. **前置0可以不输入**
- 思路: 模拟
    - 注意到, 犹豫两位数字可以大于59, 因此同样的秒数可能有多种表示. 除了 1. 基本的 `minutes, seconds = targetSeconds//60 , targetSeconds%60`, 还有可能 2. 是 `minutes-1, seconds+60` (`seconds+60<100`), 计算两者较小的代价.
    - 用函数 `getCost(minutes, seconds)` 模拟该方案的代价.
    - 需要注意边界: 1. 当 `targetSeconds<60` 时 第二种方案非法; 2. 当 `targetSeconds>=60000` 时, 第一种方案非法. 因此可以在 getCost 函数中增加判断: `minutes>99 or seconds>99 or minutes<0 or seconds<0` 时返回 Inf, 更简单.
 """
    def minCostSetTime(self, startAt: int, moveCost: int, pushCost: int, targetSeconds: int) -> int:
        def getCost(minutes, seconds):
            if minutes==seconds==0:
                return 0
            if minutes>99 or seconds>99 or minutes<0 or seconds<0:
                return float('inf')
            chars = []
            if minutes > 0:
                chars += list(str(minutes))
                if seconds<10:
                    chars += ['0', str(seconds)]
                else:
                    chars += list(str(seconds))
            else:
                chars += list(str(seconds))
            result = 0
            lastChar = str(startAt)
            for char in chars:
                if char != lastChar:
                    result += moveCost + pushCost
                    lastChar = char
                else:
                    result += pushCost
            return result
        result = float('inf')
        minutes, seconds = targetSeconds//60 , targetSeconds%60
        result = getCost(minutes, seconds)
        if seconds+60<100 and minutes>0:
            result = min(getCost(minutes-1, seconds+60), result)
        return result

    """ 2163. 删除元素后和的最小差值
给一个长度为 3n 的数组 nums, 要求删除其中 n个数字, 使得删除后, 数组前n个数字之和 - 后n个数字之和最小.

输入：nums = [3,1,2]
输出：-1
解释：nums 有 3 个元素，所以 n = 1 。
所以我们需要从 nums 中删除 1 个元素，并将剩下的元素分成两部分。
- 如果我们删除 nums[0] = 3 ，数组变为 [1,2] 。两部分和的差值为 1 - 2 = -1 。
- 如果我们删除 nums[1] = 1 ，数组变为 [3,2] 。两部分和的差值为 3 - 2 = 1 。
- 如果我们删除 nums[2] = 2 ，数组变为 [3,1] 。两部分和的差值为 3 - 1 = 2 。
两部分和的最小差值为 min(-1,1,2) = -1 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/minimum-difference-in-sums-after-removal-of-elements
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

目标: 前n个数字之和最小, 后n个数字之和最大.
可知, 最后剩余的两组数字, 其原始的分割点一定在 [n, 2n] 之间. 因此, 可以 遍历遍历每一个分割点, 分别计算前后的最小和最大和, 然后求最小值.
为此, 可以分别建立一个最大堆和最小堆, 遍历 [n, 2n] 个数字 (pushpop), 记录每一个分割点的的值. 需要注意的是, 后半部分应该逆序, 注意代码.
 """
    def minimumDifference(self, nums: List[int]) -> int:
        n = len(nums) // 3
        part1, part2, part3 = nums[:n], nums[n:2*n], nums[2*n:]
        # 前n个数字之和最小, 因此建立最大堆
        part1 = [-i for i in part1]
        heapq.heapify(part1)
        sum1 = sum(part1)
        part1_min = [sum1]
        for num in part2:
            # 这里的判断也可以去掉: 因为 pushpop 是先 push后pop
            if num < -part1[0]:
                out = heapq.heappushpop(part1, -num)
                sum1 = sum1-out-num
            part1_min.append(sum1)
        part1_min = [-i for i in part1_min]
        # 后n个数字之和最大
        heapq.heapify(part3)
        sum3 = sum(part3)
        part3_max = [sum3]
        for num in part2[::-1]:
            out = heapq.heappushpop(part3, num)
            sum3 = sum3-out+num
            part3_max.append(sum3)
        part3_max = part3_max[::-1]
        
        # 找最小差值
        result = [i-j for i, j in zip(part1_min, part3_max)]
        return min(result)


sol = SolutionD68()
result = [
    # sol.minimumSum(num = 2932),
    # sol.minCostSetTime(startAt = 0, moveCost = 1, pushCost = 2, targetSeconds = 76),
    # sol.minCostSetTime(0, 6578, 6577, 17),
    # sol.minCostSetTime(1, 9403, 9402, 6008),
    # sol.minimumDifference(nums = [3,1,2]),
    sol.minimumDifference([16,46,43,41,42,14,36,49,50,28,38,25,17,5,18,11,14,21,23,39,23]),
]
for r in result:
    print(r)