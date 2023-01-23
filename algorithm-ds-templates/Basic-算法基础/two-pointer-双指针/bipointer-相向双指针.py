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


    
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
