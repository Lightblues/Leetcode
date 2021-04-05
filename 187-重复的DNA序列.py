"""
所有 DNA 都由一系列缩写为 'A'，'C'，'G' 和 'T' 的核苷酸组成，例如："ACGAATTCCG"。在研究 DNA 时，识别 DNA 中的重复序列有时会对研究非常有帮助。
编写一个函数来找出所有目标子串，目标子串的长度为 10，且在 DNA 字符串 s 中出现次数超过一次。


输入：s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
输出：["AAAAACCCCC","CCCCCAAAAA"]

输入：s = "AAAAAAAAAAAAA"
输出：["AAAAAAAAAA"]

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/repeated-dna-sequences
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
from typing import List
class Solution:
    def findRepeatedDnaSequences(self, s: str) -> List[str]:
        L, n = 10, len(s)
        seen, output = set(), set()
        for start in range(n-L+1):
            tmp = s[start: start+L]
            if tmp in seen:
                output.add(tmp)
            seen.add(tmp)
        return list(output)


    def findRepeatedDnaSequences2(self, s: str) -> List[str]:
        L, n = 10, len(s)
        if n<=L:
            return []

        # rolling hash parameters: base a
        a = 4
        aL = pow(a, L)

        to_int = {'A': 0, 'C':1, 'G':2, 'T':3}
        nums = [to_int.get(c) for c in s]

        h = 0
        seen, output = set(), set()
        for start in range(n-L+1):
            if start != 0:
                # compute hash of the current sequence in O(1) time
                h = h*a - nums[start-1]*aL + nums[start+L-1]
            else:
                # compute hash of the first sequence in O(L) time
                for i in range(L):
                    h = h*a + nums[i]
            if h in seen:
                output.add(s[start: start+L-1])
            seen.add(h)
        return list(output)


    def findRepeatedDnaSequences3(self, s: str) -> List[str]:
        L, n = 10, len(s)
        if n <= L:
            return []

        # convert string to the array of 2-bits integers:
        # 00_2, 01_2, 10_2 or 11_2
        to_int = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
        nums = [to_int.get(s[i]) for i in range(n)]

        bitmask = 0
        seen, output = set(), set()
        # iterate over all sequences of length L
        for start in range(n - L + 1):
            # compute bitmask of the sequence in O(1) time
            if start != 0:
                # left shift to free the last 2 bit
                bitmask <<= 2
                # add a new 2-bits number in the last two bits
                bitmask |= nums[start + L - 1]
                # unset first two bits: 2L-bit and (2L + 1)-bit
                bitmask &= ~(3 << 2 * L)
            # compute bitmask of the first sequence in O(L) time
            else:
                for i in range(L):
                    bitmask <<= 2
                    bitmask |= nums[i]
            if bitmask in seen:
                output.add(s[start:start + L])
            seen.add(bitmask)
        return list(output)

    def findRepeatedDnaSequences3_me(self, s: str) -> List[str]:
        L, n = 10, len(s)
        if n<=L:
            return []

        char2bit = {'A':0, 'C':1, 'G':2, 'T':3}
        bits = [char2bit[c] for c in s]

        bitmask = 0
        seen = set()
        output = set()      # 注意 output 也需要用 set()，因为可能出现重复很多次的
        for i in range(L):
            bitmask <<= 2
            bitmask |= bits[i]
        seen.add(bitmask)
        for i in range(1, n-L+1):
            # 对于长度为 L 的字符串来说，转化成的 bit 串长为 2L，为了覆盖掉最左侧的两个 bit（保留最后 2(L-1)bits）
            # 可知 (1<<2*(L-1))-1 最后的 2*(L-1) 位为 1
            bitmask &= (1<<2*(L-1))-1
            bitmask <<= 2
            bitmask |= bits[i+L-1]
            if bitmask in seen:
                output.add(s[i:i+L])
            else:
                seen.add(bitmask)
        return list(output)


# s = "AAAAAAAAAAA"
s = "GAGAGAGAGAGA"
# s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
print(Solution().findRepeatedDnaSequences3(s))