"""
给定 n 个正整数，第 i 个正整数表示坐标为 i 的地方有高度为 a_i 的柱子；找出两个点（柱子），使其构成的容器（盛水，所以是矩形）容积最大

输入：[1,8,6,2,5,4,8,3,7]
输出：49
解释：图中垂直线代表输入数组 [1,8,6,2,5,4,8,3,7]。在此情况下，容器能够容纳水（表示为蓝色部分）的最大值为 49。

输入：height = [1,1]
输出：1

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/container-with-most-water
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""

class Solution:
    # def maxArea(self, height: List[int]) -> int:
    def maxArea(self, height):
        # # 原本想对于每一根建立一个 partner，保存与其组队的距离最远的柱子；问题在于这样做需要维护两个方向上的；
        # # 似乎还不如真正两两组合的暴力求解
        # num = len(height)
        # partner = list(range(num))  # 保存第 i 根柱子所对应的最远（宽度最大）的 partner 的 index
        # for i in range(1, num):
        #     for j in range(i):
        #         if height[i] >= height[j]:
        #             partner[j] = i
        # volume = [height[i] * (partner[i]-i) for i in range(num)]
        # result = max(volume)
        #
        # partner2 = list(range(num))
        # for i in range(num-2, -1, -1):
        #     for j in range(num-1, i, -1):
        #         if height[i] >= height[j]:
        #             partner2[j] = i
        # volume = [height[i] * (i - partner2[i]) for i in range(num)]
        # result = max(volume + [result])
        # return result

        # 暴力
        # result = 0
        # num = len(height)
        # for i in range(num):
        #     for j in range(i+1, num):
        #         result = max(result, (j-i)*min(height[i], height[j]))
        # return result

        # 注意到，从两侧开始搜索，对于 right, left 对应的柱子中较小的那一根来说，它们组成矩形的面积就是其可能的最大面积
        result = 0
        left, right = 0, len(height)-1
        while left != right:
            result = max(result, min(height[left], height[right]) * (right-left))
            if height[right] < height[left]:
                right -= 1
            else:
                left += 1
        return result

# height = [1,8,6,2,5,4,8,3,7]
height = [2,3,4,5,18,17,6]
sol = Solution()
print(sol.maxArea(height))