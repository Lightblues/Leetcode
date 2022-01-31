

from typing import List
import collections
import random
import heapq


""" @220116
https://leetcode-cn.com/contest/weekly-contest-278
 """
class Solution278:
    """ 5994. 查找给定哈希值的子串
定义一个字符串的哈希值 hash(s, p, m) = (val(s[0]) * p0 + val(s[1]) * p1 + ... + val(s[k-1]) * pk-1) mod m
给你一个字符串 s 和整数 power，modulo，k 和 hashValue 。请你返回 s 中 第一个 长度为 k 的 子串 sub ，满足 hash(sub, power, modulo) == hashValue 。

输入：s = "leetcode", power = 7, modulo = 20, k = 2, hashValue = 0
输出："ee"
解释："ee" 的哈希值为 hash("ee", 7, 20) = (5 * 1 + 5 * 7) mod 20 = 40 mod 20 = 0 。
"ee" 是长度为 2 的第一个哈希值为 0 的子串，所以我们返回 "ee" 。 """
    # 理解错题目了, 子川的 base 是从 0 重新开始的
    def subStrHash0(self, s: str, power: int, modulo: int, k: int, hashValue: int) -> str:
        sInt = [ord(i) - ord('a')+1 for i in s]
        hash = 0
        powerNow = 1
        for i in range(k):
            hash = (hash + powerNow*sInt[i]) % modulo
            powerNow = (powerNow*power) % modulo
        powerBefore = 1
        if hash == hashValue:
            return s[:k]
        print(hash, end=" ")
        for i in range(k, len(sInt)):
            if hash == hashValue:
                return s[i-k:i]
            hash -= powerBefore*sInt[i-k]
            hash += powerNow*sInt[i]
            hash = hash % modulo
            powerBefore = (powerBefore*power) % modulo
            powerNow = (powerNow*power) % modulo
            print(hash, end=" ")
        return ""

    # 暴力遍历, 超时了
    def subStrHash2(self, s: str, power: int, modulo: int, k: int, hashValue: int) -> str:
        sInt = [ord(i) - ord('a')+1 for i in s]
        powers = []
        it = 1
        for _ in range(k):
            powers.append(it)
            it = it*power % modulo
        for i in range(0, len(s)-k+1):
            hash = sum(i*j for i,j in zip(powers, sInt[i:i+k])) % modulo
            print(hash, end=' ')
            if hash == hashValue:
                return s[i:i+k]

    """ from https://leetcode-cn.com/problems/find-substring-with-given-hash-value/solution/pythongo-hua-dong-chuang-kou-by-himymben-2udq/
    滑动平均, O(n)
    给出的哈希计算函数是一个等比求和数列，两者可以通过减去首元素，除以power再加上新元素的power的k-1次方计算。
    但是 **除法不满足取余的恒等性**。因此需要倒序，减去当前的值，乘以power再加上新元素的值。(乘法满足取余恒等)
 """
    def subStrHash(self, s: str, power: int, modulo: int, k: int, hashValue: int) -> str:
        t = pow(power, k - 1, modulo) # pow 还可以指定 mod !
        val = ans = 0
        for i in range(k):
            val = (val + (ord(s[len(s) - 1 -i]) - ord('a') + 1) * pow(power, k - 1 - i, modulo) % modulo) % modulo
        if val == hashValue:
            ans = len(s) - k
        for i in range(len(s) - 1, k - 1, -1):
            val = (val - (ord(s[i]) - ord('a') + 1) * t % modulo) % modulo
            val = val * power  % modulo
            val = (val + ord(s[i - k]) - ord('a') + 1) % modulo 
            if val == hashValue:
                ans = i - k
        return s[ans:ans+k]


sol = Solution278()
res = [
    # sol.subStrHash(s = "leetcode", power = 7, modulo = 20, k = 2, hashValue = 0),
    # sol.subStrHash(s = "fbxzaad", power = 31, modulo = 100, k = 3, hashValue = 32),
    # sol.subStrHash("xxterzixjqrghqyeketqeynekvqhc",15,94,4,16),
    sol.subStrHash2("xmmhdakfursinye", 96,45,15,21),
]
for r in res:
    print(r)