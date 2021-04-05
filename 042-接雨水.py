"""
给定 n 个非负整数表示每个宽度为 1 的柱子的高度图，计算按此排列的柱子，下雨之后能接多少雨水。

输入：height = [0,1,0,2,1,0,1,3,2,1,2,1]
输出：6
解释：上面是由数组 [0,1,0,2,1,0,1,3,2,1,2,1] 表示的高度图，在这种情况下，可以接 6 个单位的雨水（蓝色部分表示雨水）。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/trapping-rain-water
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from typing import List

class Solution:
    """
    考虑暴力计算每一点（宽度为 1）可能积水量 —— 取决于其左右两侧的最大高度中较低的一个。因此，暴力法可以依次遍历数组的每一个元素计算其积水量。
    可以简化搜索左右最大高度的方式：分别左右搜索一次，记录到两个数组中
    【动态规划】
    """
    def trap1(self, height: List[int]) -> int:
        n = len(height)
        max_from_left = [0 for _ in range(n)]
        max_from_right = [0 for _ in range(n)]
        highest = 0
        for i in range(n):
            if height[i] > highest:
                highest = height[i]
            max_from_left[i] = highest
        highest = 0
        for i in range(n-1, -1, -1):
            if height[i] > highest:
                highest = height[i]
            max_from_right[i] = highest
        waters = [min(max_from_right[i], max_from_left[i])-height[i] for i in range(n)]
        return sum(waters)

    """
    【递减栈】
    从左向右搜索的过程中，我们要记录的其实是那些较高的柱子（的位置）。
    若遇到了一些低洼部分，直接填平（累积到结果中）。
    这里就用到了「递减栈」：记录了从左向右「向下的一个个台阶」的形状，若右侧出现了某个更高的柱子，可以将这些台阶按照一个个矩形的方式填充。
    
    这里需要注意的是栈的修改情况：注意到，遍历的每一个点都是会入栈的 —— 无论是较低的或者是最高的柱子。
    若遇到等高的柱子怎么办？也是直接入栈，这个矩形面积的计算有关；
    如何计算矩形面积？我们入栈的递减的柱子序号，若当前遍历的柱高 h>stack[-1]，说明可以积水
    （1）pop 出左侧节点，从而得到的左侧节点的高度 left_height 
    （2）宽度计算为 i-stack[-1]-1 
    （3）而最大的高度为 min(h, height[stack[-1]]) - left_height 
    当遇到等高情况是，右侧的柱子 h>stack[-1] 始终满足，因此虽然第一次根据上式计算的面积为 0，但不影响最终结果。
    """
    def trap2(self, height: List[int]) -> int:
        stack = []
        n = len(height)
        result = 0
        for i in range(n):
            h = height[i]
            while stack and h > height[stack[-1]]:
                left_height = height[stack.pop()]
                if not stack:
                    break
                result += (min(h, height[stack[-1]]) - left_height) * (i-stack[-1]-1)
            stack.append(i)     # 入栈
        return result

    """
    双指针
    与之前 011 很类似，自己有想过这个方向，轻易居然放弃了，不该。
    思路就是左右双指针，每次移动其中较小的一个；同时记录左侧和右侧的最高值 
    """
    def trap3(self, height: List[int]) -> int:

        result = 0
        left, right = 0, len(height)-1
        left_max, right_max = 0, 0
        while left<right:
            if height[left] < height[right]:
                nex = left+1
                if height[nex] > left_max:
                    left_max = height[nex]
                else:
                    # 注意，若移动的是左指针，这说明此时 left_max < right_max !
                    # 因为左右两个 max 指针是递增的，left_max < right_max满足时，left 始终指向这个最大值，直至左侧出现更高的柱子
                    result += left_max - height[nex]
                left = nex
            else:
                nex = right-1
                if height[nex] > right_max:
                    right_max = height[nex]
                else:
                    result += right_max - height[nex]
                right = nex
        return result



# height = [0,1,0,2,1,0,1,3,2,1,2,1]
height = [4,2,0,3,2,5]
# height = [4,2,3]
print(Solution().trap3(height))
