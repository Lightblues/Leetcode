from typing import *
from collections import defaultdict
from heapq import nlargest
from bisect import bisect_right
from itertools import permutations

"""
https://leetcode.cn/contest/weekly-contest-462
1. 简单模拟
2. 排序排列
3. 最优激活顺序得到的最大总和 -- 阅读理解题😭
    其中 "选择最大的 l 个元素" 标准解是 快速选择 算法
4. 下一个特殊回文数 -- 给定一个 x, 要求构造比它大的特殊回文 (所有出现在其中 x 的出现次数为 x)
    方法是构造所有的合法回文数, 其中用到 枚举子集, 枚举全排列, 位数运算 等技巧, 综合应用题
Easonsi @2026 """


ODD_MASK = 0x155
D = 9  # 所有数字 (元素数)

special_numbers = []
for mask in range(1, 1 << D):  # 枚举所有非空集合
    t = mask & ODD_MASK
    if t & (t - 1):  # 至少有两个奇数
        continue

    # 构造排列 perm
    perm = []
    size = odd = 0
    for x in range(1, D + 1):
        if mask >> (x - 1) & 1:
            size += x
            perm.extend([x] * (x // 2))
            if x % 2:
                odd = x
    if size > 16:  # 回文串太长了
        continue

    # 枚举 perm 的所有排列 p，生成对应的回文数
    for p in permutations(perm):
        pal = 0
        for v in p:
            pal = pal * 10 + v
        v = pal
        if odd:
            pal = pal * 10 + odd
        # 反转 pal 的左半，拼在 pal 后面
        while v:
            v, d = divmod(v, 10)
            pal = pal * 10 + d
        special_numbers.append(pal)
special_numbers = sorted(set(special_numbers))


class Solution:
    """ 3643. 垂直翻转子矩阵 #3 """
    def reverseSubmatrix(self, grid: List[List[int]], x: int, y: int, k: int) -> List[List[int]]:
        l,r = x,x+k-1
        while l<r:
            for j in range(y,y+k):
                grid[l][j], grid[r][j] = grid[r][j], grid[l][j]
            l += 1
            r -= 1
        return grid

    """ 3644. 排序排列 #5 
给定一个排列, 给定 k, 只能对于 nums[i] AND nums[j] = k 的下标才能交换. 问能够将 nums 恢复递增的最大 k
限制: n 1e5. 若本来就有序, 返回 0
思路 1: 
    可知, 对于 0 是可以使得排列有序的 -- 因为, 借助 0 可以给任意 i,j 位置交换! 也即经过 (0,a), (0,b), (0,a) 操作后, 0 回到原点, ab 交换
    本题中, 对于不满足 i=nums[i] 的元素, 其一定需要和某元素交换 (AND = k) 来移动到对应位置.  -- 也即, 在一个交换组中, 元素两两 AND 的结果均为 k
        因此, 答案就是所有不满足 i=nums[i] 的元素 AND 的结果
        可以构造解法: 同样可以利用 k, 将任意两个元素交换位置!
    """
    def sortPermutation(self, nums: List[int]) -> int:
        ans = -1
        for i,x in enumerate(nums):
            if i!=x:
                ans &= x
        return ans if ans!=-1 else 0  # NOTE: 注意原本就有序的情况

    """ 3645. 最优激活顺序得到的最大总和 #5
给定一组点 (l, v), 一开始都是 non-active. 记当前激活元素数量为 c
    - 每次只能选择 l > c 的点激活;
    - 选后, 所有 l<=c 的点都回永远变为非激活 -- 包括哪些已经激活的和非激活的! (无法再次激活)
    要求过程中激活value的最大和
限制: 1e5
思路 1: 阅读理解题/脑筋急转弯
    根据题意, 若 limit=[2,2,2], 则选择两个 l=2 的节点之后, 所有 l=2 的节点都永久非激活. -- 因此选择最大的两个!
    若 limit=[2,3,3...], 加入 l=3 之后数量达到 2, 则开始激活的 l=2 节点也非激活了 -- 不影响 l=3 的那些!
    因此, 整体策略是从小到大选择 l; 每个 l group 中选择最大的 l 个元素
    复杂度: O(n logn); 使用快速选择可以做到 O(n)
https://leetcode.cn/problems/maximum-total-from-optimal-activation-order/solutions/3748516/yue-du-li-jie-ti-nao-jin-ji-zhuan-wan-py-kua4/
    """
    def maxTotal(self, value: List[int], limit: List[int]) -> int:
        groups = defaultdict(list)
        for l,v in zip(limit, value):
            groups[l].append(v)
        ans = 0
        for l,g in groups.items():
            ans += sum(nlargest(l, g))  # NOTE: nlargest 用法!
        return ans

    """ 3646. 下一个特殊回文数 #6
特殊数定义: 回文数, 且其中的任意数字 k 恰好出现 k 次. 
给定数字 n, 求严格 >n 的最小回文数
限制: n 1e15
方法 1: 枚举全排列
    构造所有的合法回文数, 二分查找即可
    - 一共有多少合法回文? 至多从 {1,3,5,7,9} 里选一个奇数; {2,4,6,8} 偶数自由选择 -- 共 2^4*6-1 = 95 个非空选择
    - 对于每种选择 (set), 枚举所有合法排列
    实现方面: 
        如何枚举所有可能出现的额数字集合 -- 二进制枚举 S={1,...9}
            如何判断出现了 >1 奇数? `t = mask & ODD_MASK`; 然后 t & (t-1) 则不满足!
        如何枚举所有排列? 借助 `itertools.permutations`
            "反转拼接" 大数字 -- 通过 枚举所有位来实现
    复杂度: 不考虑预处理, 二分 logN; 其中 N 只有 2k 左右
方法 2: 倒序贪心 + 0-1 背包 #optional
    类似 2048. 下一个更大的数值平衡数
https://leetcode.cn/problems/next-special-palindrome-number/solutions/3748548/bao-li-mei-ju-he-fa-pai-lie-by-endlessch-b5gw/
"""
    def specialPalindrome(self, n: int) -> int:
        i = bisect_right(special_numbers, n)
        return special_numbers[i]

sol = Solution()
result = [
    # sol.reverseSubmatrix(grid = [[3,4,2,3],[2,3,4,2]], x = 0, y = 2, k = 2),
    sol.sortPermutation(nums = [0,3,2,1]),
    # sol.maxTotal(value = [3,5,8], limit = [2,1,3]),
    # sol.maxTotal(value = [4,1,5,2], limit = [3,3,2,3]),
    # sol.maxTotal(value = [4,2,6], limit = [1,1,1]),
]
for r in result:
    print(r)
