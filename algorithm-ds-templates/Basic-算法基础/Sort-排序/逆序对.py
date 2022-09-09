from typing import List, Optional

""" 剑指 Offer 51. 数组中的逆序对
在数组中的两个数字，如果前面一个数字大于后面的数字，则这两个数字组成一个 #逆序对。输入一个数组，求出这个数组中的逆序对的总数。
思路1：#归并排序 
    注意归并排序是稳定的, 而 **逆序数** 等于一个 序列要变成升序排列所需要的相邻元素交换的最小次数. 
    因此直观理解, 在归并排序过程中, 统计交换次数即为逆序数.
思路2: 离散化树状数组
    采用离散化的方式缩减数字范围, 然后用 树状数组 计数
[官答](https://leetcode-cn.com/problems/shu-zu-zhong-de-ni-xu-dui-lcof/solution/shu-zu-zhong-de-ni-xu-dui-by-leetcode-solution/)
 """

class Solution:
    def reversePairs(self, nums: List[int]) -> int:
        # 注意在归并排序中需要用到的 tmp 数组, 空间复杂度 O(n), 时间 O(nlogn)
        n = len(nums)
        tmp = [0] * n
        return self.mergeSort(nums, tmp, 0, n-1)
    
    def mergeSort(self, nums, tmp, l,r):
        # 终止条件
        if l >= r:
            return 0
        mid = (l+r)//2
        # 分治
        cnt = self.mergeSort(nums, tmp, l, mid) + self.mergeSort(nums, tmp, mid+1, r)
        # 合并
        i, j, k = l, mid+1, l
        while i<=mid and j<=r:
            if nums[i] <= nums[j]:
                tmp[k] = nums[i]
                i += 1
                # (1) 官答案的理解: 考虑右侧的 j 的移动次数, 此时需要考虑最后可能剩余的 i, 因此在下面的 while i<=mid 要加上一行
                # cnt += (j - (mid + 1))
            else:
                tmp[k] = nums[j]
                j += 1
                # (2) 事实上可以直接看左侧的 i 的移动次数: 将i位置移动到mid+1
                # 计算逆序对 !!!
                cnt += mid+1 - i
            k += 1
        # 将剩余部分拷贝到 tmp 中
        while i<=mid:
            tmp[k] = nums[i]
            i += 1
            # (1) 官答案的理解
            # cnt += (j - (mid + 1))
            k += 1
        while j<=r:
            tmp[k] = nums[j]
            j += 1
            k += 1
        # 复制回来
        for i in range(l, r+1):
            nums[i] = tmp[i]
        return cnt

    """ 方法二：离散化树状数组
采用离散化的方式缩减数字范围, 然后用 树状数组 计数
 """
    def reversePairs(self, nums: List[int]) -> int:
        # 离散化
        sortedNums = sorted(set(nums))
        mapping = {num: i+1 for i, num in enumerate(sortedNums)}
        nums = [mapping[num] for num in nums]

        # 树状数组 计数
        res = 0
        bit = BIT(len(nums))
        for num in nums[::-1]:
            res += bit.query(num-1)
            bit.update(num, 1)
        return res

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
    sol.reversePairs([7,5,6,4]) # 5
]:
    print(res)