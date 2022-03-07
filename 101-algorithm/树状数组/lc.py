from typing import List, Optional

class Solution:
    """ 315. 计算右侧小于当前元素的个数
给你一个整数数组 `nums` ，按要求返回一个新数组 `counts` 。数组 `counts` 有该性质： `counts[i]` 的值是  `nums[i]` 右侧小于 `nums[i]` 的元素的数量。

输入：nums = [5,2,6,1]
输出：[2,1,1,0] 
解释：
5 的右侧有 2 个更小的元素 (2 和 1)
2 的右侧仅有 1 个更小的元素 (1)
6 的右侧有 1 个更小的元素 (1)
1 的右侧有 0 个更小的元素

思路一: 离散化树状数组
from [here](https://leetcode-cn.com/problems/count-of-smaller-numbers-after-self/solution/ji-suan-you-ce-xiao-yu-dang-qian-yuan-su-de-ge-s-7/)

方法二：归并排序
略
 """
    def countSmaller(self, nums: List[int]) -> List[int]:
        sortedNums = sorted(set(nums))
        mapped = {n: i+1 for i, n in enumerate(sortedNums)}
        nums = [mapped[n] for n in nums]
        n = len(nums)
        ans = [0] * n
        bit = BIT(n)
        for i in range(n-1, -1, -1):
            bit.update(nums[i], 1)
            ans[i] = bit.query(nums[i]-1)
        return ans

class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n+1)
    @staticmethod
    def lowbit(x):
        return x & (-x)
    def update(self, i, delta):
        while i <= self.n:
            self.tree[i] += delta
            i += self.lowbit(i)
    def query(self, i):
        res = 0
        while i > 0:
            res += self.tree[i]
            i -= self.lowbit(i)
        return res

sol = Solution()
for res in [
    sol.countSmaller(nums = [5,2,6,1]),
]:
    print(res)