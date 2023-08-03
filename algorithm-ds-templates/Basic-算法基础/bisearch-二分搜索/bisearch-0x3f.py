from easonsi import utils
from easonsi.util.leetcode import *
""" 
== 二分查找总结
0034. 在排序数组中查找元素的第一个和最后一个位置 #medium #题型 对于一个非递减数组, 找到数字x出现的范围; 若不存在返回 [-1,-1]
    思路1: (数组中存在x的情况下) 范围为 [lower_bound(x), lower_bound(x+1)-1]
0162. 寻找峰值 #medium 数组相邻元素不等, 假设左右边界的值都是 -inf, 找到任一峰值元素的下标
    思路1: 注意两个部分的划分方式!!! 
    划分方式为, 「peak左侧」 和 「peak位置或右侧」. 因此, 最后一个元素一定是符合条件的
    因此开区间范围为 (-1, n-1); 闭区间范围为 [0, n-2]; 左闭右开区间范围为 [0, n-1)
    https://leetcode.cn/problems/find-peak-element/
0153. 寻找旋转排序数组中的最小值 #medium 原本有序的数组经过了旋转, 问最小值
    思路1: 和最后一个元素比较, 注意划分的范围!!
    https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array/
0033. 搜索旋转排序数组 #medium #题型 相较于「0153. 寻找旋转排序数组中的最小值」, 旋转数组中元素各不相同, 搜索元素target出现的位置
    思路1: 先找到旋转点, 然后再二分查找
    思路2: 只用一次二分. 直接与目标值进行比较! 利用「红蓝染色」, 写一个 is_blue(i) 返回True时: target在位置i或者左侧
    https://leetcode.cn/problems/search-in-rotated-sorted-array/

灵神 [Video1](https://www.bilibili.com/video/BV1AP41137w7/)

"""


""" lower_bound 模版, from https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/solutions/1980196/er-fen-cha-zhao-zong-shi-xie-bu-dui-yi-g-t9l9/
注意:
    函数目标: lower_bound 返回最小的满足 nums[i] >= target 的 i
    循环不变量: 注意三种写法中的注释, 判断条件都是 `nums[mid] < target`, 相应地需要维护的不变量要满足 <, >= 的条件 (具体是取 left,left-1 根据区间的写法决定)
不同的写法: (时刻注意区间表示的是搜索的范围!)
    闭区间: [l,r] 范围内都是不确定的. 因此更新方式是 l = mid + 1, r = mid - 1
    左闭右开区间: [l,r) 其中r是确定满足的. 因此更新方式是 l = mid + 1, r = mid
    开区间: (l,r) 其中l是确定不满足的, r是确定满足的. 因此更新方式是 l = mid, r = mid
"""
# lower_bound 返回最小的满足 nums[i] >= target 的 i
# 如果数组为空，或者所有数都 < target，则返回 len(nums)
# 要求 nums 是非递减的，即 nums[i] <= nums[i + 1]

# 闭区间写法
def lower_bound(nums: List[int], target: int) -> int:
    left, right = 0, len(nums) - 1  # 闭区间 [left, right]
    while left <= right:  # 区间不为空
        # 循环不变量：
        # nums[left-1] < target
        # nums[right+1] >= target
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1  # 范围缩小到 [mid+1, right]
        else:
            right = mid - 1  # 范围缩小到 [left, mid-1]
    return left  # 或者 right+1

# 左闭右开区间写法
def lower_bound2(nums: List[int], target: int) -> int:
    left = 0
    right = len(nums)  # 左闭右开区间 [left, right)
    while left < right:  # 区间不为空
        # 循环不变量：
        # nums[left-1] < target
        # nums[right] >= target
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1  # 范围缩小到 [mid+1, right)
        else:
            right = mid  # 范围缩小到 [left, mid)
    return left  # 或者 right

# 开区间写法
def lower_bound3(nums: List[int], target: int) -> int:
    left, right = -1, len(nums)  # 开区间 (left, right)
    while left + 1 < right:  # 区间不为空
        mid = (left + right) // 2
        # 循环不变量：
        # nums[left] < target
        # nums[right] >= target
        if nums[mid] < target:
            left = mid  # 范围缩小到 (mid, right)
        else:
            right = mid  # 范围缩小到 (left, mid)
    return right  # 或者 left+1






class Solution:
    """ 0034. 在排序数组中查找元素的第一个和最后一个位置 #medium #题型 对于一个非递减数组, 找到数字x出现的范围; 若不存在返回 [-1,-1]
思路1: (数组中存在x的情况下) 范围为 [lower_bound(x), lower_bound(x+1)-1]
"""
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        def lower_bound(arr,x):
            l,r = 0,len(arr)-1
            while l<=r:
                mid = (l+r)//2
                if arr[mid]<x:
                    l = mid+1
                else:
                    r = mid-1
            return l
        start = lower_bound(nums, target)  # 选择其中一种写法即可
        if start == len(nums) or nums[start] != target:
            return [-1, -1]
        # 如果 start 存在，那么 end 必定存在
        end = lower_bound(nums, target + 1) - 1
        return [start, end]

    """ 0162. 寻找峰值 #medium 数组相邻元素不等, 假设左右边界的值都是 -inf, 找到任一峰值元素的下标
思路1: 注意两个部分的划分方式!!!
    划分方式为, 「peak左侧」 和 「peak位置或右侧」. 因此, 最后一个元素一定是符合条件的
    因此开区间范围为 (-1, n-1); 闭区间范围为 [0, n-2]; 左闭右开区间范围为 [0, n-1)
"""
    def findPeakElement(self, nums: List[int]) -> int:
        left, right = -1, len(nums) - 1  # 开区间 (-1, n-1)
        while left + 1 < right:  # 开区间不为空
            mid = (left + right) // 2
            if nums[mid] > nums[mid + 1]:  # 蓝色
                right = mid
            else:  # 红色
                left = mid
        return right
    def findPeakElement(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1  # 左闭右开区间 [0, n-1)
        while left < right:  # 区间不为空
            mid = (left + right) // 2
            if nums[mid] > nums[mid + 1]:  # 蓝色
                right = mid
            else:  # 红色
                left = mid+1
        return right


    """ 0153. 寻找旋转排序数组中的最小值 #medium 原本有序的数组经过了旋转, 问最小值
思路1: 和最后一个元素比较, 注意划分的范围!!
    注意到, 从左往左顺着最后一个元素往下, 可以找到最小值. 因此, 二分的时候可以与它比较来搜索范围
    记最后一个数为x, 划分方式为: <=x 和 >x
"""
    def findMin(self, nums: List[int]) -> int:
        # 记最后一个数为x, 划分方式为: 在x左侧 和 x右侧
        x = nums[-1]
        l,r = -1,len(nums)-1    # 开区间 (-1, n-1)
        while l+1<r:
            mid = (l+r)//2
            if nums[mid]<=x: r = mid
            else: l = mid
        return nums[r]

    """ 0033. 搜索旋转排序数组 #medium #题型 相较于「0153. 寻找旋转排序数组中的最小值」, 旋转数组中元素各不相同, 搜索元素target出现的位置
思路1: 先找到旋转点, 然后再二分查找
    这样, 需要两次二分. 
思路2: 只用一次二分. 直接与目标值进行比较
    利用「红蓝染色」, 写一个 is_blue(i) 返回True时: target在位置i或者左侧. 两种情况
        1] nums[i]>nums[-1] 时, i左侧是上升节点, 需要 target>nums[-1] 且 target<=nums[i]
        2] nums[i]<nums[-1] 时, i右侧是上升阶段, 需要 target>nums[-1] 或 target<=nums[i]
    [官答](https://leetcode.cn/problems/search-in-rotated-sorted-array/solution/sou-suo-xuan-zhuan-pai-xu-shu-zu-by-leetcode-solut/)
见 [灵神](https://leetcode.cn/problems/search-in-rotated-sorted-array/solution/by-endlesscheng-auuh/)
"""
    def search(self, nums: List[int], target: int) -> int:
        """ 思路1: 先找到旋转点, 然后再二分查找 """
        # 先找到旋转点
        x = nums[-1]
        l,r = 0,len(nums)-2     # 闭区间 [0, n-2]
        while l<=r:
            mid = (l+r)//2
            if nums[mid]<=x: r = mid-1
            else: l = mid+1
        idxmn = r+1
        # 定位二分的范围
        if target>x: l,r = 0,idxmn-1
        else: l,r = idxmn,len(nums)-1
        # 二分搜索. 区间 [l,r]
        while l<=r:
            mid = (l+r)//2
            if nums[mid]<target: l = mid+1
            else: r = mid-1
        if l<len(nums) and nums[l]==target: return l
        else: return -1
    def search(self, nums: List[int], target: int) -> int:
        def is_blue(i):
            # 返回True时: target在位置i或者左侧
            if nums[i]>nums[-1]: 
                # [0:i] 上升
                return target>nums[-1] and target<=nums[i]
            else:
                # [i:n-1] 上升
                return target>nums[-1] or target<=nums[i]
        l,r = 0,len(nums)-1 # [0,n-1]
        while l<=r:
            mid = (l+r)//2
            if is_blue(mid): r = mid-1
            else: l = mid+1
        if l<len(nums) and nums[l]==target: return l
        else: return -1

    """ 0081. 搜索旋转排序数组 II #medium 但实际上 #hard 数组在某一位置发生了旋转, 元素可能重复, 找到目标
关联「0033. 搜索旋转排序数组」旋转数组中元素各不相同
提示: 相较于0033, 核心是需要避免 nums[l]==nums[mid]==nums[r] 的情况
思路1: 当出现这种情况的时候, 无法判断哪边是有序的, 因此只能 l++, r-- 缩小范围
    见 [官答](https://leetcode.cn/problems/search-in-rotated-sorted-array-ii/solution/sou-suo-xuan-zhuan-pai-xu-shu-zu-ii-by-l-0nmp/)
思路2: 提前将这种情况避免掉: 可以通过pop掉nums最后==nums[0]的那些数字
复杂度: 最坏情况 O(n)
    """
    def search(self, nums: List[int], target: int) -> bool:
        if not nums: return False
        # 避免 nums[l]==nums[mid]==nums[r] 的情况
        while len(nums)>1 and nums[0] == nums[-1]:
            nums.pop()
        base = nums[0]

        left, right = 0, len(nums)-1
        while left <= right:
            mid = (left + right)//2
            if nums[mid] == target:
                return True
            if nums[mid] >= base:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        return False



sol = Solution()
result = [
    # sol.findPeakElement([1,2,3]),
    # sol.findMin(nums = [3,4,5,1,2]),
    
    # sol.search(nums = [4,5,6,7,0,1,2], target = 0),
    sol.search([4,5,1,2,3], 3),
]
for r in result:
    print(r)
