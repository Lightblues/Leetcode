from easonsi import utils
from easonsi.util.leetcode import *
""" 
技巧:
bisect 包提供了已有的二分查找模板, 那么需要手动在 [left, right] 这一区间内查找呢? 
    可以手动构造这一range, 然后在这一区间上查找即可 (使用 key 参数)
    例如, `bisect.bisect_left(list(range(int(1e5))), 1, key=check)` 查找最后第一个符合条件的元素的索引

"""

class Solution:

    """ 2064. 分配给商店的最多商品的最小值 #medium #二分
将一组商品分配给n家商店, 每家店只能有一种商品 (也可以没有商品). 要求一种最「平均」的分配方式, 也即这些店中的商品数量最大值达到最小.
限制: 商品种类 m = 1e5, 每一种的最大数量 a = 1e5
思路1: #二分查找 每次检查的复杂度为 m, 二分的范围最大为 a, 因此时间复杂度为 O(m*log(a)).
    左右边界: sum(quantities)/n), quantities[-1]+1
    注意二分的边界: 这里的题型是「满足条件的最小值」. 因此不满足时缩小左边界 `left = mid+1`, 最后返回 `left`.
说明: 出了手动写二分算法之外, [here](https://leetcode.cn/problems/minimized-maximum-of-products-distributed-to-any-store/solution/er-fen-da-an-by-endlesscheng-aape/)
    直接调用了 go 中的 `sort.Search` 函数, 简化了代码. 
    类似的, 在 Python 中可采用 `bisect.bisect_left`, 语法有所不同, 思路是一样的 (其实都是在一个range数组中二分查找).
"""
    def minimizedMaximum(self, n: int, quantities: List[int]) -> int:
        quantities.sort()
        left, right = math.ceil(sum(quantities)/n), quantities[-1]
        def check(a):
            remain = n
            for q in quantities:
                remain -= math.ceil(q/a)
                if remain < 0: return False
            return True
        while left < right:
            mid = (left+right)//2
            if not check(mid):
                left = mid+1
            else:
                right = mid
        return left

    def minimizedMaximum(self, n: int, quantities: List[int]) -> int:
        """ 参考 [here](https://leetcode.cn/problems/minimized-maximum-of-products-distributed-to-any-store/solution/er-fen-da-an-by-endlesscheng-aape/)
        相较于 go 中的 `sort.Search` 函数, 采用了 `bisect.bisect_left`, 语法有所不同, 思路是一样的. """
        def check(a):
            remain = n
            for q in quantities:
                remain -= math.ceil(q/a)
                if remain < 0: return False
            return True
        # 直接在 [1, 1e5] 这一区间内查找
        idx = bisect.bisect_left(list(1, range(int(1e5))), 1, key=check)
        return idx+1


sol = Solution()
result = [
    # sol.findPeakElement([1,2,3]),
    # sol.findMin(nums = [3,4,5,1,2]),
    sol.search(nums = [4,5,6,7,0,1,2], target = 0),
]
for r in result:
    print(r)