from typing import List
import collections
import math
import bisect
import heapq


""" 
https://leetcode-cn.com/contest/biweekly-contest-68 """
class SolutionD68:
    """ 2176. 统计数组中相等且可以被整除的数对 """
    def countPairs(self, nums: List[int], k: int) -> int:
        num2index = collections.defaultdict(list)
        for i, num in enumerate(nums):
            num2index[num].append(i)
        res = 0
        for indexs in num2index.values():
            for i in range(len(indexs)):
                for j in range(i+1, len(indexs)):
                    if (indexs[j] * indexs[i]) % k == 0:
                        res += 1
        return res

    """ 2177. 找到和为给定整数的三个连续整数 """
    def sumOfThree(self, num: int) -> List[int]:
        if num%3!= 0:
            return []
        d = num//3
        return [d-1,d,d+1]

    """ 2178. 拆分成最多数目的偶整数之和 """
    def maximumEvenSplit(self, finalSum: int) -> List[int]:
        if finalSum%2 != 0:
            return []
        res = []
        i = 2
        while finalSum >= i:
            res.append(i)
            finalSum -= i
            i += 2
        res[-1] += finalSum
        return res

    """ 2179. 统计数组中好三元组数目
整数数组 `nums1` 和 `nums2` ，两者都是 `[0, 1, ..., n - 1]` 的 **排列** 。
要求找满足条件的三元组数量, 条件: (x,t,z) 出现在两数组中的次序是一致的.

输入：nums1 = [2,0,1,3], nums2 = [0,1,2,3]
输出：1
解释：
总共有 4 个三元组 (x,y,z) 满足 pos1x < pos1y < pos1z ，分别是 (2,0,1) ，(2,0,3) ，(2,1,3) 和 (0,1,3) 。
这些三元组中，只有 (0,1,3) 满足 pos2x < pos2y < pos2z 。所以只有 1 个好三元组。

将nums1中数字在num2中的index依次写出来, 记为 numMap, 则结果就是该数组中递增的三元组的个数

笔记: 这里的核心问题在于: 实现一个数据结构, 可以 1. 查询其中比 query 小的数量; 2. 插入某一个数值的数量. 
该问题可以建模为 「树状数组/线段树」, 参见 [here](https://oi-wiki.org/ds/fenwick/)

另见 [here](https://leetcode-cn.com/problems/count-good-triplets-in-an-array/solution/deng-jie-zhuan-huan-shu-zhuang-shu-zu-by-xmyd/)
 """
    def goodTriplets0(self, nums1: List[int], nums2: List[int]) -> int:
        # 任务转为, 在 numMap 找到递增的三元组
        n2iNum2 = {num:i for i, num in enumerate(nums2)}
        numMap = [n2iNum2[num] for num in nums1]
        res = 0
        """ 超时了 """
        # # 记录长度为 1 的子序列中, 结尾的数字, 排好序
        # last1 = []
        # last2 = []
        # for num in numMap:
        #     # 有多少比 num 小的数字在前面
        #     idx1 = bisect.bisect_left(last1, num)
        #     idx2 = bisect.bisect_left(last2, num)
        #     res += idx2
        #     last1.insert(idx1, num)
        #     for _ in range(idx1):
        #         last2.insert(idx2, num)

        """ 笑死, 暴力用 numpy; 用数组+for会超时 """
        import numpy as np
        last1 = [] # 遍历数组过程中, 记录出现过的数字 (长度为1的子序列), 为了统计数量, 排好序
        last2 = np.zeros([len(nums2),], dtype=int) # 记录出现比nums小的数字的数量
        for num in numMap:
            idx1 = bisect.bisect_left(last1, num) # 以num结尾的长度2子序列的个数
            res += last2[num]
            last1.insert(idx1, num)
            last2[num:] += idx1
        return int(res) # 返回 int
    
    def goodTriplets(self, nums1: List[int], nums2: List[int]) -> int:
        class BIT:
            def __init__(self, n):
                self.n = n
                self.tree = [0] * (n + 1)
            def update(self, i, val):
                while i <= self.n:
                    self.tree[i] += val
                    i += i & -i
            def query(self, i):
                res = 0
                while i > 0:
                    res += self.tree[i]
                    i -= i & -i
                return res
        # 转换nums2的元素到nums1数组中的index, 然后问题等价于求nums中递增三元组的数量
        mapping = {num:i+1 for i, num in enumerate(nums1)} # 注意index从1开始!
        nums = [mapping[num] for num in nums2]
        # 采用两个BIT 树状数组计算
        n = len(nums)
        bit1 = BIT(n)
        bit2 = BIT(n)
        low = [0] * n # low 记录左侧比 nums[i] 小的数字的个数
        high = [0] * n # high 记录右侧比 nums[i] 小的数字的个数, 从右往左计算
        for i in range(n):
            # i, j 分别从左右遍历
            j = n-1-i
            n1, n2 = nums[i], nums[j]
            low[i] = bit1.query(n1-1)
            high[j] = i - bit2.query(n2-1)
            bit1.update(n1, 1)
            bit2.update(n2, 1)
        return sum(low[i]*high[i] for i in range(n))



sol = SolutionD68()
result = [
    # sol.countPairs(nums = [1,2,3,4], k = 1),
    # sol.countPairs(nums = [3,1,2,2,2,1,3], k = 2),
    # sol.sumOfThree(num = 33),
    # sol.maximumEvenSplit(finalSum = 12),
    # sol.maximumEvenSplit(finalSum = 28),

    sol.goodTriplets(nums1 = [2,0,1,3], nums2 = [0,1,2,3]),
    sol.goodTriplets(nums1 = [4,0,1,3,2], nums2 = [4,1,0,2,3]),
    # 1, 4
]
for r in result:
    print(r)
    # print(type(r))