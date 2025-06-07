from typing import *
# from easonsi.util.leetcode import *

# def testClass(inputs):
#     # 用于测试 LeetCode 的类输入
#     s_res = [None] # 第一个初始化类, 一般没有返回
#     methods, args = [eval(l) for l in inputs.split('\n')]
#     class_name = eval(methods[0])(*args[0])
#     for method_name, arg in list(zip(methods, args))[1:]:
#         r = (getattr(class_name, method_name)(*arg))
#         s_res.append(r)
#     return s_res

""" @2025-06-07
https://leetcode.cn/contest/biweekly-contest-140
#remark 两道前后缀分解题目, 非常有难度!
T3: 要求为子序列, 基本前缀匹配的计算; "几乎等于" 的要求需要转化!
T4: 要求为子数组, 设计到 Z 数组的计算!

Easonsi @2025 """
class Solution:
    """ 3302. 字典序最小的合法序列 #medium 找到一个最小的递增的index序列, 让 word1 的子序列 "几乎等于" word2, 这里的 "几乎等于" 是指最多只相差一个字符
限制: n 3e5
思路1: #前后缀分解
    关联: [2565. 最少得分子序列] 也是找子序列
    预处理: 先计算后缀 suf[i] 表示 words1[i:] 可以匹配 word2 的最长后缀的左下标
    关键是如何 "字典序最小"? 枚举前缀位置i, 同时记录word2的匹配位置j:
        若 word1[i] == word2[j], 直接使用;
        若 不等, 且 suf[i+1] <= j+1, 说明一定要修改了 -- 最小字典序
        注意! 为了避免仅修改一次, 需要用一个flag来标记是否修改过 
[ling](https://leetcode.cn/problems/find-the-lexicographically-smallest-valid-sequence/solutions/2934051/qian-hou-zhui-fen-jie-zi-xu-lie-pi-pei-t-le8d/)
#remark: 下面的两种 for 循环中, 前者考虑复杂的条件判断 (early stop), 后者直接尝试往后匹配, 复杂度一样的情况下更为精简!
"""
    def validSequence(self, word1: str, word2: str) -> List[int]:
        m,n = len(word1), len(word2)
        
        suf = [0] * (m+1)  # init as 0 for break
        j = n-1
        for i in range(m-1,-1,-1):
            if word1[i] == word2[j]:
                j -= 1
            if j == -1: break
            suf[i] = j+1
        
        ans = []  # record the answer
        j = 0
        changed = False
        # 思路1: 复杂判断, 逻辑比较乱
        # for i, c in enumerate(word1):
        #     if c == word2[j]:
        #         j += 1
        #         ans.append(i)
        #     else:
        #         if changed and suf[i] > j: return []  # early stop
        #         elif not changed and suf[i+1] <= j+1:
        #             changed = True
        #             j += 1
        #             ans.append(i)
        #     if j == n: return ans
        # return []
        
        # 思路2: 尽量往后匹配, 不考虑 early stop!
        for i,c in enumerate(word1):
            if c==word2[j] or (not changed and suf[i+1] <= j+1):
                if c!=word2[j]: changed = True
                j += 1
                ans.append(i)
                if j == n: return ans
        return []
    
    """ 3303. 第一个几乎相等子字符串的下标 #hard 相较于上一题, 要求为子字符串
限制: n 1e5
思路1: #前后缀分解 + #Z数组
    子序列变为子数组, 差异在哪里? 需要考虑连续字符串的性质了!
    考虑两个问题:
        对于 s[i...], 能匹配 pattern多长的前缀?
        对于 s[...j], 能匹配 pattern多长的后缀?
    这样我们就能进行判断了, 例如 s=abcdefg, pattern=bcdffg (m=6)
        s[1...] 可以匹配前缀长度 3;
        s[...6] 可以匹配后缀长度 2;
        说明长m的子字符串 s[1...6] 可以匹配 3+2 = 6-1, 满足要求!
    对于这两个问题, 可以用 Z 数组预处理!
        对于 pattern+s, 计算 Z 数组 preZ, 则 s[i...] 可以匹配 pattern 的最大长度为 preZ[i+m]
        对于 pattern[::-1]+s[::-1], 计算 Z 数组并反转得到 sufZ, 则 s[...j] 可以匹配 pattern 的最大长度为 sufZ[j]
    回到原问题, 从左到右遍历字符串 [i...i+m-1]
        若 preZ[i+m] + sufZ[i+m-1] >= m-1, 则满足要求 "几乎相等"
        PS: 也可以直接 for i in m...n, 则条件化简为:
            preZ[i] + sufZ[i-1] >= m-1 

[ling](https://leetcode.cn/problems/find-the-occurrence-of-first-almost-equal-substring/solutions/2934098/qian-hou-zhui-fen-jie-z-shu-zu-pythonjav-0est/)
"""
    def calc_z(self, s: str) -> List[int]:
        # 计算 Z 数组, from ling
        n = len(s)
        z = [0] * n
        box_l = box_r = 0  # z-box 左右边界
        for i in range(1, n):
            if i <= box_r:
                z[i] = min(z[i - box_l], box_r - i + 1)  # 改成手动 if 可以加快速度
            while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                box_l, box_r = i, i + z[i]
                z[i] += 1
        return z

    def minStartingIndex(self, s: str, pattern: str) -> int:
        preZ = self.calc_z(pattern + s)
        sufZ = self.calc_z(pattern[::-1] + s[::-1])[::-1]
        m = len(pattern)
        for i in range(m, len(s)+1):
            if preZ[i] + sufZ[i-1] >= m-1:
                return i-m
        return -1

sol = Solution()
result = [
    # sol.validSequence(word1 = "vbcca", word2 = "abc"),
    # sol.validSequence(word1 = "bacdc", word2 = "abc"),
    # sol.validSequence("cbbccc", "bb"),
    sol.minStartingIndex(s = "abcdefg", pattern = "bcdffg"),
    sol.minStartingIndex(s = "ababbababa", pattern = "bacaba"),
]
for r in result:
    print(r)
