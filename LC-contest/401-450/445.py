from typing import *
import heapq
import math
from collections import Counter

""" 
https://leetcode.cn/contest/weekly-contest-445

Easonsi @2025 """
class Solution:
    """ 3516. 找到最近的人 """
    def findClosest(self, x: int, y: int, z: int) -> int:
        a = abs(x-z)
        b = abs(y-z)
        if a < b: return 1
        elif a > b: return 2
        else: return 0

    """ 3517. 最小回文排列 I """
    def smallestPalindrome(self, s: str) -> str:
        cnt = Counter(s)
        center = ""
        pre = ""
        for ch in sorted(cnt.keys()):
            c = cnt[ch]
            c1, c2 = divmod(c, 2)
            pre += ch * c1
            if c2 == 1:
                center = ch
        return pre + center + pre[::-1]
    
    """ 3518. 最小回文排列 II #hard 对于一个字符串的所有回文排列, 返回第k小的那一个
限制: n 1e4
思路1: 试填法 + 组合数学
    等价问题, 对于一组字符 S (有重复), 找到其第k大的排列.
    在每个位置, 尝试填入 ch=a,b,... 对于每个数字, 计算填入后其他字符 S\{ch} 的排列数目 p;
        若 p < k, 则说明第k大的排列不以 ch 开头, 则 k -= p, 继续尝试下一个字符;
        否则, 确定当前位置的字符, 继续下一个位置.
    如何计算排列数, 对于字符串计数器 cnt, 假设各字符出现个数为 c1, c2, ... 对于长sz的字符串, 排列数量为 C(cz, c1) * C(cz-c1, c2) * ...
    复杂度: O(n S (S+logk)), 其中 S=26 为字符集大小. 这里的 O(S+logk) 是计算组合数perm的复杂度, 注意这里是加法, 因为内层循环至多乘以 logk 个大于1的数!
关联: 1850. 邻位交换的最小次数, 是求给定序列的后第k个排列! 
    官方题解类似 "暴力" 复杂度为 O(n(k+n))
    [here](https://leetcode.cn/problems/minimum-adjacent-swaps-to-reach-the-kth-smallest-number/solutions/1/0msfei-bao-li-onlogn-shi-tian-fa-ji-suan-s3ku/)
    给出了 O(nS + n logn) 的做法, 结合了本题中组合数据 & Fenwick Tree 技巧
"""
    def smallestPalindrome(self, s: str, k: int) -> str:
        n = len(s)
        m = n // 2
        cnt = [0] * 26  # 统计token按顺序数量
        for ch in s[:m]:
            cnt[ord(ch) - ord('a')] += 1
        
        # 计算cnt中的字符构成sz长度的排列数量 (sum(cnt) == sz)
        def perm(sz: int) -> int:
            res = 1
            for c in cnt:
                if c == 0: continue
                res = res * math.comb(sz, c)
                sz -= c
                if res >= k: return k  # 提前剪枝
            return res
        
        if perm(m) < k:
            return ""  # 不足k个排列
        
        s_left = [""] * m
        for i in range(m):
            for j in range(26):
                if cnt[j] == 0:
                    continue
                cnt[j] -= 1  # 尝试使用j
                p = perm(m - i - 1)
                if p >= k:
                    s_left[i] = chr(j + ord('a'))
                    break
                k -= p
                cnt[j] += 1  # 恢复
        s_left = "".join(s_left)
        center = "" if n % 2 == 0 else s[m]
        return s_left + center + s_left[::-1]

    """ 3519. 统计逐位非递减的整数 #hard 对于十进制的范围 [l,r], 统计其中以b进制表示时 "逐位非递减" 的整数个数.
限制: len(l) 100; b [2,10]. 结果取mod
思路1: #数位DP
    定义 dfs(i, pre, limitLow, limitHigh) 表示构造i为及其之后数位的合法方案数
    状态转移: 枚举第i位填 d = [max(lo, pre), hi]
"""
    def countNumbers(self, l: str, r: str, b: int) -> int:
        MOD = 10**9 + 7

sol = Solution()
result = [
    sol.smallestPalindrome(s = "abba", k = 2),
]
for r in result:
    print(r)
