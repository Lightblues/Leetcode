
总结一下二分搜索的基本代码.

### 基本情况: 返回在一个数组中要插入元素的index

仔细记录bisect库的代码: `bisect(arr, x, l,r)`

- mid计算: `mid = (l+r)//2`
- 搜索边界: `[l,r)` 因此假设要搜索 [1,10], 则需要初始化 r=11
- 更新条件: `l = mid+1`, `r=mid`
- 返回: `l`

注意: 1) 这里mid的计算方式决定了当 r=l+1 时, mid=l, 因此一定要用 l = mid+1 的更新条件才能保证不会出现死循环. 2) 而l的更新方式决定了l无法更新到初始化的r, 因此函数搜索范围为 `[l,r)`.

重点来看判断条件:

- 右插入: (等价于, 找到满足 `arr[index] <= x 的index + 1`), 判断条件 `arr[mid] <= x` 时更新 l
- 左插入: (等价于, 找到满足 `arr[index] < x 的index + 1`), 判断条件 `arr[mid] < x` 时更新 l

```python
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
```

### 条件归并

重点是, 应该 **很多变体是如何转化到这一基本模板**.

- 要查找最后一个满足条件的位置. 等价于, `bisect_right - 1`; 不限于数组的情况, 对于在 `[l, r)` 范围内搜索的问题都可以建模为 `bisect(l, r)`, 在其中调用 test 函数判断条件是否成立, 比如要找「满足一定条件的最大值」, 也等价于 `bisect_right - 1`.
- 要查找第一个符合条件的位置, 等价于 bisect_left.

```python
def get_last(arr, x):
    # 返回最后一个满足条件, 即 arr[index] <= x 的index
    return bisect_right(arr, x) - 1

def get_first(arr, x):
    # 返回第一个满足条件, 即 arr[index] >= x 的index
    return bisect_left(arr, x)
```

注意, 这里的「找到最后一个相等元素的位置」, 其实等价于「查询满足 >target 插入位置 - 1」, 完全可以套用 `bisect_right` 模版, 并且上面的形式比这里更通用. 此外, 这里多了一些判断条件, 对于test成本较高的就不适用.

```go
func searchLastEqualElement(nums []int, target int) int {
    l, r := 0, len(nums)-1
    for l<=r{
        mid := l+(r-l)>>1
        if nums[mid]>target{
            r = mid-1
        } else if nums[mid] < target{
            l = mid +1
        } else {
            // 加入test复杂度较高, 这里比较浪费?
            if mid==len(nums)-1 || (nums[mid+1]!=target) {
                return mid
            }
            l = mid+1
        }
    }
    return -1
}
```
