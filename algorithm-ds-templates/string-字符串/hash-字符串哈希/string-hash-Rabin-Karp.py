from easonsi.util.leetcode import *
import random

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
https://oi-wiki.org/string/hash/

Easonsi @2023 """
class Solution:
    """ 0187. 重复的DNA序列 #medium 对于 ACGT组成的核苷酸序列, 找出所有长度为10的重复序列 (至少出现两次) 限制: n 1e5 
见 [bit]
"""
    def findRepeatedDnaSequences(self, s: str) -> List[str]:
        L, n = 10, len(s)
        if n<=L: return []

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

    """ 1044. 最长重复子串 #hard 对于一个字符串, 找到重复子串中, 最长的那些. 限制: n 3e4
思路1: #二分+字符串哈希
    答案的范围为 [1, n-1], 二分查找答案, 检查是否有重复子串
    时间复杂度 O(n logn)
    问题: Rabin-Karp 编码之后, 由于字符串长度很长, 需要做取模处理, 这样会产生冲突!!
        因此: 采用 #双哈希, 两个进制, 两个模, 两个编码都相同的时候才认为子串重复
[官答](https://leetcode.cn/problems/longest-duplicate-substring/solution/zui-chang-zhong-fu-zi-chuan-by-leetcode-0i9rd/)
"""
    def longestDupSubstring(self, s: str) -> str:
        # 生成两个进制
        a1, a2 = random.randint(26, 100), random.randint(26, 100)
        # 生成两个模
        mod1, mod2 = random.randint(10**9+7, 2**31-1), random.randint(10**9+7, 2**31-1)
        n = len(s)
        # 先对所有字符进行编码
        arr = [ord(c)-ord('a') for c in s]
        # 二分查找的范围是[1, n-1]
        l, r = 1, n-1
        length, start = 0, -1
        while l <= r:
            m = l + (r - l + 1) // 2
            idx = self.check(arr, m, a1, a2, mod1, mod2)
            # 有重复子串，移动左边界
            if idx != -1:
                l = m + 1
                length = m
                start = idx
            # 无重复子串，移动右边界
            else:
                r = m - 1
        return s[start:start+length] if start != -1 else ""

    def check(self, arr, m, a1, a2, mod1, mod2):
        """ 检查串arr中是否有长度为m的重复子串, 用两个 base 和 mod 进行编码 """
        n = len(arr)
        aL1, aL2 = pow(a1, m, mod1), pow(a2, m, mod2)
        h1, h2 = 0, 0
        for i in range(m):
            h1 = (h1 * a1 + arr[i]) % mod1
            h2 = (h2 * a2 + arr[i]) % mod2
        # 存储一个编码组合是否出现过
        seen = {(h1, h2)}
        for start in range(1, n - m + 1):
            h1 = (h1 * a1 - arr[start - 1] * aL1 + arr[start + m - 1]) % mod1
            h2 = (h2 * a2 - arr[start - 1] * aL2 + arr[start + m - 1]) % mod2
            # 如果重复，则返回重复串的起点
            if (h1, h2) in seen:
                return start
            seen.add((h1, h2))
        # 没有重复，则返回-1
        return -1

    """ 1392. 最长快乐前缀 #hard #KMP 给定一个字符串s, 要求最长的, 既是s的前缀也是后缀的子串. """
    def longestPrefix(self, s: str) -> str:
        # 思路2: #Rabin-Karp 字符串编码
        n = len(s)
        prefix, suffix = 0, 0
        base, mod, mul = 31, 1000000007, 1
        happy = 0
        for i in range(1, n):
            prefix = (prefix * base + (ord(s[i - 1]) - 97)) % mod
            suffix = (suffix + (ord(s[n - i]) - 97) * mul) % mod
            if prefix == suffix:
                happy = i
            mul = mul * base % mod
        return s[:happy]
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
