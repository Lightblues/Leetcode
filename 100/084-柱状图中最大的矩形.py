"""
给定 n 个非负整数，用来表示柱状图中各个柱子的高度。每个柱子彼此相邻，且宽度为 1 。
求在该柱状图中，能够勾勒出来的矩形的最大面积。

输入: [2,1,5,6,2,3]
输出: 10
"""
from typing import  List
class Solution:
    """
    暴力求解：每次向两边扩散
    """
    def largestRectangleArea(self, heights: List[int]) -> int:
        res = 0
        n = len(heights)
        for i in range(n):
            baseHeight = heights[i]
            left = i
            while left>0 and heights[left-1]>=baseHeight:
                left -= 1
            right = i
            while right<n-1 and heights[right+1]>=baseHeight:
                right += 1
            res = max(res, baseHeight*(right-left+1))
        return res

    """
    方法一：单调栈
    """

    def largestRectangleArea2(self, heights: List[int]) -> int:
        n = len(heights)
        res = 0
        stack = []
        for i in range(n):
            if not stack or heights[i] > heights[stack[-1]]:
                stack.append(i)
            elif heights[i] < heights[stack[-1]]:
                while stack and heights[stack[-1]] > heights[i]:
                    h = heights[stack[-1]]
                    res = max(res, h * (i - stack[-1]))
                    stack.pop()
                if not stack or (stack and heights[stack[-1]] == heights[i]):
                    stack.append(i)
        while stack:
            res = max(res, heights[stack[-1]] * (n-stack[-1]))
            stack.pop()
        return res


    # 官答
    def largestRectangleArea3(self, heights: List[int]) -> int:
        n = len(heights)
        left, right = [0] * n, [n] * n

        mono_stack = list()
        for i in range(n):
            while mono_stack and heights[mono_stack[-1]] >= heights[i]:
                right[mono_stack[-1]] = i
                mono_stack.pop()
            left[i] = mono_stack[-1] if mono_stack else -1
            mono_stack.append(i)

        ans = max((right[i] - left[i] - 1) * heights[i] for i in range(n)) if n > 0 else 0
        return ans



    def largestRectangleArea_(self, heights):
        # 找stack中 左面第一个比cur（栈外）大的---单调递 增 栈（栈尾）---在栈中（L,R）（，第一个比R小的，L第一个比L大的,）--处理中间的山峰peak
        # 找stack中 左面第一个比cur（栈外）小的---单调递 减 栈（栈尾）---在栈中（L,R）（，第一个比R大的，L第一个比L小的,）--处理中间的山谷valley
        # 找当前最大的，单调递 减 队列（队首）
        # 找当前最小的，单调递 增 队列（队首）
        heights = [0] + heights + [0]
        # 前面加0，为了确保至少有2个数递增   后面加0为了防止 1 2 3 4 5不计算
        n = len(heights)
        res = 0
        monoinc_stk = []
        for i in range(n):
            while monoinc_stk and heights[monoinc_stk[-1]] > heights[i]:
                window_L_height_min_height = heights[monoinc_stk.pop(-1)]  # 当前窗口的最左端的高度，也是当前窗口的公共高度
                window_L = monoinc_stk[-1] + 1  # 因为与左面第一个比自己小的之间，可能还有山峰，只能这么求
                window_R = i - 1  # 当前窗口的右端点
                cur_area = (window_R - window_L + 1) * window_L_height_min_height
                res = max(res, cur_area)
            monoinc_stk.append(i)
        return res

# heights = [2,1,5,6,2,3]
# heights = [2,4]
heights = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,]
print(Solution().largestRectangleArea2(heights))

