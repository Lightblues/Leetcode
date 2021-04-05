"""
给定一个字符串数组words，找到length(word[i]) * length(word[j])的最大值，并且这两个单词不含有公共字母。你可以认为每个单词只包含小写字母。如果不存在这样的两个单词，返回 0。

输入: ["abcw","baz","foo","bar","xtfn","abcdef"]
输出: 16
解释: 这两个单词为 "abcw", "xtfn"。

输入: ["a","ab","abc","d","cd","bcd","abcd"]
输出: 4
解释: 这两个单词为 "ab", "cd"。

输入: ["a","aa","aaa","aaaa"]
输出: 0
解释: 不存在这样的两个单词。

"""
from typing import List

class Solution:
    """
    方法一：优化的方法 noCommonLetters：位操作+预计算
    还是基于两两组合，选出最大值的框架，用了位运算来加速比较是否有交集。
    """
    def maxProduct(self, words: List[str]) -> int:
        char2num = lambda c: ord(c) - ord('a')

        def str2bitmask(s):
            s = set(s)
            bitmask = 0
            for c in s:
                bitmask |= 1<<char2num(c)
            return bitmask

        words_mask = [str2bitmask(s) for s in words]

        max_len = 0
        n = len(words)
        for i in range(n):
            for j in range(i+1, n):
                if words_mask[i] & words_mask[j] == 0:
                    max_len = max(max_len, len(words[i])*len(words[j]))

        return max_len

    """
    方法二：优化比较次数：位操作+预计算+HashMap
    """
    def maxProduct2(self, words: List[str]) -> int:
        char2num = lambda c: ord(c) - ord('a')

        def str2bitmask(s):
            s = set(s)
            bitmask = 0
            for c in s:
                bitmask |= 1<<char2num(c)
            return bitmask

        from collections import defaultdict
        hashmap = defaultdict(int)
        for w in words:
            mask = str2bitmask(w)
            hashmap[mask] = max(hashmap[mask], len(w))

        max_len = 0
        for x in hashmap:
            for y in hashmap:
                if x&y==0:
                    max_len = max(max_len, hashmap[x]*hashmap[y])
        return max_len


words = ["abcw","baz","foo","bar","xtfn","abcdef"]
print(Solution().maxProduct(words))