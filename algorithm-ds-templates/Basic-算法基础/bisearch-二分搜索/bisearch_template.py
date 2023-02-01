from easonsi import utils
from easonsi.util.leetcode import *

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




""" 二分模板 bisect
- bisect_right 摘自bisect包; 注意在 Python3.9中, 新增了一个 key 参数支持传入函数比较, 可以实现更为通用的二分查找.
- get_last, get_first 得到符合条件的第一/最后一个元素, 直接调包
- get_last_man 在相等时手动向前/后检查了一个, 代码更为简单.
"""

def bisect_right(a, x, lo=0, hi=None):
    """在一个有序数组a中插入数字x的位置, 若数组中已有x则插入到最右边.
    The return value i is such that all e in a[:i] have e <= x, and all e in
    a[i:] have e > x.  So if x already appears in the list, a.insert(x) will
    insert just after the rightmost x already there.
    """
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if x < a[mid]: hi = mid
        else: lo = mid+1
    return lo

def bisect_left(a, x, lo=0, hi=None):
    """区别在于, 出现相同元素时, 插入到最左边.
    The return value i is such that all e in a[:i] have e < x, and all e in
    a[i:] have e >= x.  So if x already appears in the list, a.insert(x) will
    insert just before the leftmost x already there.
    """
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid] < x: lo = mid+1
        else: hi = mid
    return lo

def get_last(arr, x):
    # 返回最后一个满足条件, 即 arr[index] <= x 的index
    return bisect_right(arr, x) - 1

def get_first(arr, x):
    # 返回第一个满足条件, 即 arr[index] >= x 的index
    return bisect_left(arr, x)

arr = [1,2,2,2,3]
res = [
    bisect_left(arr, 2),
    bisect_right(arr, 2),
    get_last(arr, 2),
    get_first(arr, 2),
]
for r in res: print(r)
