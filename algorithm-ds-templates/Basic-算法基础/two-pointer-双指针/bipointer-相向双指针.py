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
灵神 [相向双指针](https://www.bilibili.com/video/BV1bP411c7oJ/)
== 相向双指针
下面是灵神的代码
    0167. 两数之和 II - 输入有序数组 #medium
    0015. 三数之和 #medium
作业
    0016. 最接近的三数之和 https://leetcode.cn/problems/3sum-closest/
    0018. 四数之和 https://leetcode.cn/problems/4sum/
    0611. 有效三角形的个数 https://leetcode.com/problems/valid-triangle-number/

0011. 盛最多水的容器 #medium #题型 从一组柱子中选两个, 构成的容积最大.
    采用 #双指针. 每次向内移动较短边.
0042. 接雨水 #hard #题型 给定一组柱子, 求下雨之后能接多少水.

== 此前滑动窗口的题
== 双指针：相向交替移动的两个变量
0011. 盛最多水的容器 #medium #题型 从一组柱子中选两个, 构成的容积最大.
    思路1: 采用 #双指针. 每次向内移动较短边.
0167. 两数之和 II - 输入有序数组 #medium 给定一有序数组, 判断其中两个数字之和是否可以达到目标
    思路1: #双指针 根据当前值和目标的大小进行移动. 正确性: 相当于缩减了搜索空间.
0015. 三数之和 #medium #题型 给定一个数组, 找到所有「不重复的」三个数之和为0的组合. 限制: 数组长度 3000
    思路1: 排序后, 转化为「两数之和」.
0016. 最接近的三数之和 #medium #题型 给定一个数组, 找到三个数之和最接近目标值. 限制: 数组长度 1000.
0018. 四数之和 #medium 给定一个数组, 找到所有「不重复」的四个数字之和为目标的组合. 限制: 数组长度 200
    类似 0015, 不过外面套两层循环. 内部还是 #双指针.
0125. 验证回文串 #easy 忽略非数字字母字符, 判断是否回文.
0658. 找到 K 个最接近的元素 #medium 给定一个有序数组, 返回其中最接近x的k个数字 (距离相同取idx较小的).
    思路1: 双指针收缩, 直到长度为k.
0259. 较小的三数之和 #medium 给定一个数组, 计算 i,j,k 之和 <target 的三元组数量
0360. 有序转化数组 #medium 给定一数组, 对 其中每一个元素计算 f(x) = ax^2+bx+c, 对于结果排序
    进阶要求是在 O(n) 时间内完成.
0977. 有序数组的平方 #easy 给定一个有序数组, 返回平方后的有序数组.
0844. 比较含退格的字符串 #medium 给定两个字符串, 定义 # 为特殊字符表示退格, 判断两字符串是否相等.
    进阶要求: 空间 O(1)
0845. 数组中的最长山脉 #medium 定义「山脉」为上升下降的序列, 返回数组中最长的山脉长度.
    思路1: 遍历右端, 通过 #flag 标记当前是否满足条件 (并记录左端点). 但要考虑的 #细节 比较多. 其实也就是下面的 #双指针, 官答更清楚
0881. 救生艇 #medium 
0925. 长按键入 #easy
1099. 小于 K 的两数之和 #easy
1229. 安排会议日程 #medium 给定两组区间表示两人的空闲时间, 找到重叠最早的至少为 duration 的时间段.



Easonsi @2023 """
class Solution:
    """ 0167. 两数之和 II - 输入有序数组 #medium 给定一有序数组, 判断其中两个数字之和是否可以达到目标
思路1: #相向双指针 根据当前值和目标的大小进行移动. 
    正确性: 利用到了数组的有序性.
"""
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1
        while True:  # left < right
            s = numbers[left] + numbers[right]
            if s == target:
                return [left + 1, right + 1]
            if s > target:
                right -= 1
            else:
                left += 1
    """ 0015. 三数之和 #medium #题型 给定一个数组, 找到所有「不重复的」三个数之和为0的组合. 限制: 数组长度 3000
思路1: 排序后, 转化为「两数之和」. 复杂度 O(n^2)
    细节: 注意这里需要去重!!!
"""
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        ans = []
        n = len(nums)
        for i in range(n - 2):
            x = nums[i]
            if i > 0 and x == nums[i - 1]:  # 跳过重复数字
                continue
            # 优化: 考虑边界的情况
            if x + nums[i + 1] + nums[i + 2] > 0:  # 优化一
                break
            if x + nums[-2] + nums[-1] < 0:  # 优化二
                continue
            j = i + 1
            k = n - 1
            while j < k:
                s = x + nums[j] + nums[k]
                if s > 0:
                    k -= 1
                elif s < 0:
                    j += 1
                else:
                    ans.append([x, nums[j], nums[k]])
                    j += 1
                    while j < k and nums[j] == nums[j - 1]:  # 跳过重复数字
                        j += 1
                    k -= 1
                    while k > j and nums[k] == nums[k + 1]:  # 跳过重复数字; 当然这里的 J,k 只需要跳过一边即可
                        k -= 1
        return ans




    """ 0011. 盛最多水的容器 #medium #题型 从一组柱子中选两个, 构成的容积最大.
思路1: 采用 #双指针. 每次向内移动较短边.
    正确性? **假设 l 是较短边, 它已经构成了可能组成的容积的最大值**. 因为底边减小而高不可能增加.
"""
    def maxArea(self, height: List[int]) -> int:
        l,r = 0,len(height)-1
        mx = 0
        while l<r:
            mx = max(mx, (r-l)*min(height[l],height[r]))
            if height[l] < height[r]: l+=1
            else: r-=1
        return mx
    
    """ 0042. 接雨水 #hard #题型 给定一组柱子, 求下雨之后能接多少水. 限制: n 2e4
思路1: 双指针. 维护左右的最大值, 每次更新 **最大值较小**的那一侧.
    正确性: 维护两个递增结构. 较低的一侧限制了最多接水高度
思路2: 分别左右遍历计算前缀、后缀最大值; 取两者较小就是每个位置可以蓄水的高度!
"""
    def trap(self, height: List[int]) -> int:
        l,r = 0,len(height)-1
        lmax,rmax = height[l],height[r]
        ans = 0
        while l<r:
            if lmax<rmax:
                l+=1
                if height[l]<lmax: ans += lmax-height[l]
                else: lmax = height[l]
            else:
                r-=1
                if height[r]<rmax: ans += rmax-height[r]
                else: rmax = height[r]
        return ans
    def trap(self, height: List[int]) -> int:
        n = len(height)
        ava = [0]*n
        mx = 0
        for i in range(n):
            mx = max(mx,height[i])
            ava[i] = mx
        mx = 0
        for j in range(n-1,-1,-1):
            mx = max(mx,height[j])
            ava[j] = min(ava[j],mx)
        ans = 0
        for a,h in zip(ava,height):
            ans += a-h
        return ans
    

    
sol = Solution()
result = [
    sol.trap(height = [0,1,0,2,1,0,1,3,2,1,2,1]),
    sol.trap(height = [4,2,0,3,2,5]),
]
for r in result:
    print(r)
