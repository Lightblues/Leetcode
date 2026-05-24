from typing import *
import math, collections, bisect
from math import inf
from itertools import accumulate
from bisect import bisect_left, bisect_right

"""
https://leetcode.cn/contest/weekly-contest-464
1. 简单模拟
2. 简单分析
3. 跳跃游戏 IX -- 限制跳跃条件下求每个位置可达最大值. 
    思路 1: 对于每个位置可达性的分析很巧妙 -- 最终转为 DP (状态转移)
        代码技巧: 1. accumulate 来计算 pre_max; 
    思路 2: 单调栈 -- 分析跳跃关系构成的可达性 (连通块)!
4. 可以被机器人摧毁的最大墙壁数目: 直线上给定一组 r 位置和对应的可射击距离 (r 相互遮挡), 每个只有一颗子弹, 子弹可以贯穿目标点但被下一个 r 阻挡, 问可以击中的目标最大数量
    DP, 最核心的寻找子问题! 从而构建转移方程
    细节: 在一组排序的位置上, 区间覆盖的点的数量, 二分查找, 通过 `bisect_left, bisect_right` 来确定边界!
Easonsi @2026 """


class Solution:
    """ 3658. 奇数和与偶数和的最大公约数 #3 
事实上, 答案就是 n 
https://leetcode.cn/problems/gcd-of-odd-and-even-sums/solutions/3762080/da-an-jiu-shi-npythonjavacgo-by-endlessc-u100/
    """
    def gcdOfOddEvenSums(self, n: int) -> int:
        sumOdd = (1 + 2*n-1) * n // 2
        sumEven = (2 + 2*n) * n // 2
        return math.gcd(sumOdd, sumEven)

    """ 3659. 数组元素分组 #4 
https://leetcode.cn/problems/partition-array-into-k-distinct-groups/solutions/3762099/jie-lun-ti-pythonjavacgo-by-endlesscheng-dfzw/
"""
    def partitionArray(self, nums: List[int], k: int) -> bool:
        return len(nums) % k == 0 and max(collections.Counter(nums).values()) <= len(nums) // k

    """ 3660. 跳跃游戏 IX #5
对于位置i, 可以选择 1. 往右 (j > i) 跳到更小 (nums[j] < nums[i]) 的位置; 2. 往左 (j < i) 跳到更大 (nums[j] > nums[i]) 的位置.
对于每个位置, 求可以跳到的最大值. 
观察:
    1. 右边更简单. 考虑 [6,8,5,9,7], 
        - index=n-1, 直接可跳到 max 位置
        - index=0 跳跃路径为 6->5->8->7->9
    2. 有些情况, e.g. [3,2,10,9], 对于 index=1, 无法"跨越"跳到后面去
        一般而言, 对于位置 i, 若 preMax[i] <= suffMin[i+1], 则无法往后跳 -- 只能取到 preMax[i]
        否则, 位置 i 可以通过 preMax -> suffMin 跳到 i+1 -- 转换子问题到 i+1
思路 1: DP
    基于上面的观察, 可得 DP 转移方程
    https://leetcode.cn/problems/jump-game-ix/solutions/3762167/jie-lun-ti-pythonjavacgo-by-endlesscheng-x2qu/
思路 2: 单调栈
    观察 "逆序对构成的连通块", 对于位置 i 的元素, 只要其小于左侧连通块的 max, 就可以将其合并! 连通块内的任意元素可达!
    回到上面 "无法跨越" 的情况是什么? 类似 [3,2,10,9] 的递增结构 -- 维护最大值!
    因此, 考虑 #单调栈 维护 (mx, l,r)
    https://leetcode.cn/problems/jump-game-ix/solutions/3961012/tiao-yue-you-xi-ix-by-leetcode-solution-mbzp/
    """
    def maxValue(self, nums: List[int]) -> List[int]:
        # 相对 "脏" 的写法
        n = len(nums)
        suf_min = nums[:]
        for i in range(n-2,-1,-1):
            suf_min[i] = min(suf_min[i+1], suf_min[i])
        pre_max = nums[:]
        for i in range(1,n):
            pre_max[i] = max(pre_max[i-1], pre_max[i])
        # 
        ans = [0] * n
        ans[-1] = pre_max[-1]
        for i in range(n-2,-1,-1):
            if pre_max[i] <= suf_min[i+1]:
                ans[i] = pre_max[i]
            else:
                ans[i] = ans[i+1]
        return ans

    def maxValue(self, nums: List[int]) -> List[int]:
        # by ling
        n = len(nums)
        pre_max = list(accumulate(nums, max))  # nums 的前缀最大值

        ans = [0] * n
        suf_min = inf
        for i in range(n - 1, -1, -1):
            ans[i] = pre_max[i] if pre_max[i] <= suf_min else ans[i + 1]
            suf_min = min(suf_min, nums[i])
        return ans

    def maxValue(self, nums: List[int]) -> List[int]:
        st = []
        for i,x in enumerate(nums):
            cl = cr = i
            cmx = x
            while st and st[-1][0] > x:  # NOTE: 严格大于的情况才能跳转!
                mx,l,_ = st.pop()
                cl = l
                cmx = max(cmx, mx)
            st.append((cmx, cl, cr))
        ans = [0] * len(nums)
        for x, l,r in st:
            for i in range(l, r+1):
                ans[i] = x
        return ans

    """ 3661. 可以被机器人摧毁的最大墙壁数目 #6 
无限长直线上有 robots, walls; 每个机器人 i 有一颗子弹, 射程 dist[i] (可选择向左向右), 可以摧毁所有墙, 但是会被中间的机器人拦下来. 问能摧毁的所有墙壁最大数.
限制: n 1e5; span 1e9
思路 1: DP
    对于 robots, walls 排序. 设 f(i,j) 表示前 i 个机器人向左/向右射击的最大收益
        j=-1, 子问题 
            f(i-1,-1) + 判断 [max(r[i-1]+1, r[i]-d[i]),r[i]] 范围内的 walls
            f(i-1,+1) + 判断 [max(r[i-1]+d[i-1], r[i]-d[i]),r[i]] 范围内的 walls
        j=+1, 子问题 max{ f(i-1,..) } + [robots[i], robots[i]+d[i]]
    NOTE: 上面的讨论还没有考虑 robots 遮挡边界的情况! 在实现中需要维护
    下面自己的实现中, 通过 left/right 数组来维护每个位置 i 的 robot 可以射击的边界, 简化 for 循环中的判断
下面 ling 的讲解更细致一些!
https://leetcode.cn/problems/maximum-walls-destroyed-by-robots/solutions/3762127/jiao-ni-yi-bu-bu-si-kao-dpcong-ji-yi-hua-dzd9/
    """
    def maxWalls(self, robots: List[int], distance: List[int], walls: List[int]) -> int:
        rs = [(r,d) for r,d in zip(robots, distance)]
        rs.sort()
        walls.sort()
        n = len(robots)
        # 计算每个位置子弹的边界
        left = [r-d for r,d in rs]
        for i in range(1, n):
            left[i] = max(left[i], rs[i-1][0]+1)
        right = [r+d for r,d in rs]
        for i in range(n-1):
            right[i] = min(right[i], rs[i+1][0]-1)
        
        def op(l:int, r:int) -> int:
            i = bisect_left(walls, l)
            j = bisect_right(walls, r)
            return j-i
        f1, f2 = 0, 0
        for i, (r,d) in enumerate(rs):
            nf2 = max(f1, f2) + op(r, right[i])
            nf1 = max(
                f1 + op(left[i], r),
                f2 + op(max(left[i], right[i-1]+1), r)
            )
            f1, f2 = nf1, nf2
        return max(f1, f2)


sol = Solution()
result = [
    # sol.maxValue(nums = [2,3,1]),
    # sol.maxValue([11,18,11]),
    sol.maxWalls(robots = [4], distance = [3], walls = [1,10]),
    sol.maxWalls(robots = [10,2], distance = [5,1], walls = [5,2,7]),
    sol.maxWalls(robots = [1,2], distance = [100,1], walls = [10]),
]
for r in result:
    print(r)
