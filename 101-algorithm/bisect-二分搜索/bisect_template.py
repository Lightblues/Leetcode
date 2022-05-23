""" 二分模板
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

def get_last_man(arr, x):
    """ 相较于最上面的两个模板, 更为好理解, 因为这里对于相等情况的判断条件直接写了 """
    l, r = 0, len(arr)-1
    while l<=r:
        mid = (l+r)//2
        if arr[mid] > x:
            r = mid-1
        elif arr[mid] < x:
            l = mid+1
        else:
            # 在相等的时候手动判断
            if mid==len(arr)-1 or arr[mid+1] > x:
                return mid
            l = mid+1
    return -1

arr = [1,2,2,2,3]
res = [
    bisect_left(arr, 2),
    bisect_right(arr, 2),
    get_last(arr, 2),
    get_first(arr, 2),
    get_last_man(arr, 2),
]
for r in res: print(r)
