"""
421-数组中两个数的最大异或值

给定一个非空数组，数组中元素为 a0, a1, a2, … , an-1，其中 0 ≤ ai < 231。
找到 ai 和aj最大的异或 (XOR) 运算结果，其中0 ≤ i,j < n。
你能在O(n)的时间解决这个问题吗？


输入: [3, 10, 5, 25, 2, 8]
输出: 28
解释: 最大的结果是 5 ^ 25 = 28.
"""
from typing import List
class Solution:
    # 方法一：利用哈希集合存储按位前缀
    def findMaximumXOR(self, nums: List[int]) -> int:
        L = len(bin(max(nums)))-2
        max_xor = 0
        for i in range(L)[::-1]:
            max_xor <<= 1
            # max_xor 保存在前 i 个 bin 可能的最大与结果，则 max_xor <<= 1 是肯定取得到的
            # 接下来判断更新后的末位是否也可取 1，即 curr_xor = max_xor | 1 能否满足
            # 也即，在 prefixed 中是否存在 x,y 满足 x^y=curr_xor
            # 转化成 any(curr_xor^p in prefixed for p in prefixed) 这句代码判断是否满足
            curr_xor = max_xor | 1  # 将目前最后一位置设为 1. 递推过程中, 可能构成的最大结果
            prefixed = {num>>i for num in nums}
            max_xor |= any(curr_xor^p in prefixed for p in prefixed)
        return max_xor

    # 方法二：逐位字典树
    def findMaximumXOR2(self, nums: List[int]) -> int:
        L = len(bin(max(nums))) - 2
        nums = [[(x>>i)&1 for i in range(L)][::-1] for x in nums]

        # 构建字典树
        # trie = {}
        # for num in nums:
        #     node = trie
        #     for bit in num:
        #         if not bit in node:
        #             node[bit] = {}
        #         node = node[bit]

        max_xor = 0
        trie = {}
        for num in nums:
            node = trie
            xor_node = trie
            curr_xor = 0
            for bit in num:
                # 将新的数字插入字典树
                if not bit in node:
                    node[bit] = {}
                node = node[bit]

                # 试图查找当前位的相反位
                toggled_bit = 1-bit
                if toggled_bit in xor_node:
                    curr_xor = (curr_xor<<1) | 1
                    xor_node = xor_node[toggled_bit]
                else:
                    curr_xor = curr_xor<<1
                    xor_node = xor_node[bit]
            max_xor = max(max_xor, curr_xor)
        return max_xor

    def findMaximumXOR_naive(self, nums: List[int]) -> int:
        max_xor = 0
        for i, n1 in enumerate(nums):
            for n2 in nums[i+1:]:
                max_xor = max(max_xor, n1^n2)
        return max_xor

""" 
# 三种方法的测试时间
16777215 0.12825298309326172
16777215 0.3856987953186035
16777215 10.352491855621338 """

# from time import time
# t0 = time()
# print(Solution().findMaximumXOR(nums), time()-t0)
# t0 = time()
# print(Solution().findMaximumXOR2(nums), time()-t0)
# t0 = time()
# print(Solution().findMaximumXOR_naive(nums), time()-t0)