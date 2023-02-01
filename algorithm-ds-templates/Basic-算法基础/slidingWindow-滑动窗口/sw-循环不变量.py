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
== 循环不变量
基本思想: 在循环过程中维护变量满足某一性质.
0026. 删除有序数组中的重复项 #easy
    「原地」修改已经排好序的数组, 使其不重复.
0027. 移除元素 #easy 原地移除数组中等于某val的元素
0283. 移动零 #easy 原地操作, 将0都放在数组最后, 保持其他元素相对位置
0674. 最长连续递增序列 #easy 找到数组中最长的严格递增序列
0080. 删除有序数组中的重复项 II #medium 将次数超过两次的多余数字删去

[应用] 类似快排的两道题
0075. 颜色分类 #medium #题型
    有3种颜色, 要求「原地」修改使得数组变为有序的状态.
0215. 数组中的第K个最大元素 #medium #题型 另见 [quick sort]
    思路1: 采用类似 #快排 的思路, 每次选择 pivot 对于 [l,r] 区间进行分割. 也类似 #二分


Easonsi @2023 """
class Solution:
    """ ================================== 循环不变量 ================================ """
    """ 0026. 删除有序数组中的重复项 #easy
「原地」修改已经排好序的数组, 使其不重复.
思路1: 用一个指针指向下一个要放的位置.
"""
    def removeDuplicates(self, nums: List[int]) -> int:
        i = 0; pre = None
        for j,num in enumerate(nums):
            if num != pre:
                nums[i] = num
                i += 1
            pre = num
        return i
    """ 0027. 移除元素 #easy 原地移除数组中等于某val的元素 """
    """ 0283. 移动零 #easy 原地操作, 将0都放在数组最后, 保持其他元素相对位置 """
    def moveZeroes(self, nums: List[int]) -> None:
        n = len(nums)
        i = 0
        for j,num in enumerate(nums):
            if num != 0:
                nums[i] = num
                i += 1
        for j in range(i,n):
            nums[j] = 0
        

    """ 0674. 最长连续递增序列 #easy 找到数组中最长的严格递增序列 """
    def findLengthOfLCIS(self, nums: List[int]) -> int:
        start = 0; pre=inf; ans = 0
        for i,num in enumerate(nums+[-inf]):
            if num <= pre:
                ans = max(ans, i-start)
                start = i
            pre = num
        return ans
    """ 0080. 删除有序数组中的重复项 II #medium 将次数超过两次的多余数字删去 """
    def removeDuplicates(self, nums: List[int]) -> int:
        pre,cnt = None,0
        i = 0
        for num in nums:
            if num == pre:
                cnt += 1
            else:
                pre = num
                cnt = 1
            if cnt <= 2:
                nums[i] = num
                i += 1
        return i

    """ 0075. 颜色分类 #medium #题型
有3种颜色, 要求「原地」修改使得数组变为有序的状态.
进阶要求: 时间 O(n)
思路1: 定义「循环不变量」
    定义 [0...i] 范围内数字为0; [i+1...j] 为 1; [k...n-1] 为 2, 而 [j+1...k-1] 为未知.
    终止条件: 遍历的idx遇到k.
    注意: 实际上保障了 j=idx-1. 因此这里的j没有必要维护!
[这里](https://leetcode.cn/leetbook/read/sliding-window-and-two-pointers/rl7myd/) 对于 #循环不变量 讲的很好.
[官答](https://leetcode.cn/problems/sort-colors/solution/yan-se-fen-lei-by-leetcode-solution/)
"""
    def sortColors(self, nums: List[int]) -> None:
        i=-1; k=len(nums)
        idx = 0
        while idx<k:
            num = nums[idx]
            if num==0:
                i += 1
                # 1) 若直接赋值, 注意边界!
                # nums[i] = 0
                # if i!=idx:
                #     nums[idx] = 1
                # 2) 采用交换可以简化逻辑
                nums[i],nums[idx] = nums[idx],nums[i]
                idx += 1
            elif num==1:
                idx += 1
            else:
                k-=1
                nums[k], nums[idx] = nums[idx],nums[k]
        # for test
        return nums

    """ 0215. 数组中的第K个最大元素 #medium #题型 
另见 [quick sort]
思路1: 采用类似 #快排 的思路, 每次选择 pivot 对于 [l,r] 区间进行分割. 也类似 #二分
    注意: 采用随机化策略选 pivot.
从 #循环不变量 的角度, 另见 [here](https://leetcode.cn/leetbook/read/sliding-window-and-two-pointers/rli5s3/)
"""
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # by copilot
        import random
        def partition(l,r):
            # 对于 [l,r] 区间, 随机选点作为pivot, 返回最后pivot所在位置
            # 1) 随机化 pivot
            idx = random.randint(l,r)
            nums[l],nums[idx] = nums[idx],nums[l]
            pivot = nums[l]
            # 2) 分割
            i = l+1
            for j in range(l+1,r+1):
                if nums[j] > pivot:
                    nums[i],nums[j] = nums[j],nums[i]
                    i += 1
            nums[l],nums[i-1] = nums[i-1],nums[l]
            return i-1
        # 3) 递归. 类似二分
        l,r = 0,len(nums)-1
        while l<=r:
            idx = partition(l,r)
            if idx == k-1:
                return nums[idx]
            elif idx > k-1:
                r = idx-1
            else:
                l = idx+1
        return -1
        
    
    
    
    
    
    

    
sol = Solution()
result = [
    # sol.minWindow(s = "ADOBECODEBANC", t = "ABC"),
    # sol.minWindow(s = "a", t = "a"),
    # sol.minWindow(s = "a", t = "aa"),
    # sol.findLengthOfLCIS([2,2,2]),
    # sol.findLengthOfLCIS([1,3,5,4,7]),
    # sol.sortColors(nums = [2,0,2,1,1,0]),
]
for r in result:
    print(r)
