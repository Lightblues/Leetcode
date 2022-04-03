from typing import List, Optional
import collections
import math
import bisect
import heapq
from functools import lru_cache
# import sys
# sys.setrecursionlimit(10000)

from structures import ListNode, TreeNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@220403 """
class Solution:
    """ 6055. 转化时间需要的最少操作数 """
    def convertTime(self, current: str, correct: str) -> int:
        minutes0, minutes1 = 0, 0
        hours, minutes = map(int, current.split(":"))
        minutes0 = 60*hours + minutes
        hours, minutes = map(int, correct.split(":"))
        minutes1 = 60*hours + minutes
        minutes_delta = abs(minutes1 - minutes0)
        res = 0
        for diff in [60, 15, 5, 1]:
            a, b = divmod(minutes_delta, diff)
            res += a
            minutes_delta = b
        return res
        
    def findWinners(self, matches: List[List[int]]) -> List[List[int]]:
        """ 5235. 找出输掉零场或一场比赛的玩家 """
        no_loss = set()
        one_loss = set()
        more_loss = set()
        for winner, losser in matches:
            if winner not in one_loss and winner not in more_loss:
                no_loss.add(winner)
            if losser in no_loss:
                one_loss.add(losser)
                no_loss.remove(losser)
            elif losser in one_loss:
                more_loss.add(losser)
                one_loss.remove(losser)
            elif losser not in more_loss:
                one_loss.add(losser)
        return sorted(no_loss), sorted(one_loss)
    
    def maximumCandies(self, candies: List[int], k: int) -> int:
        """ 5219. 每个小孩最多能分到多少糖果
给一组糖果, candies[i] 表示第i堆糖果有多少, 将其分给k个人, 糖果只能划分不能合并; 求最大.
思路: 二分搜索
"""
        if sum(candies) < k:
            return 0
        candies.sort(reverse=True)
        def test(m):
            acc = 0
            for candy in candies:
                acc += candy//m
                if acc >= k:
                    return True
                if candy < m:
                    break
            return False
        # 注意在下面的更新中 left指针无法到达 right的初始值!
        l, r = 1, sum(candies)//k+1
        while l < r:
            m = (l+r)//2
            if test(m):
                l = m+1
            else:
                r = m
        # 对于二分搜索, 讨巧的方案其实可以最后再检查一遍, 简化思考
        # if test(l):
        #     return l
        # else:
        #     return l-1
        return l-1

    def test4(self):
        """ 5302. 加密解密字符串 `难` https://leetcode-cn.com/problems/encrypt-and-decrypt-strings/
题目好长 Orz, 总而言之就是给一个 {key:value} 的映射, 将一个字符映射到长度为2的一个字符串, key不重复但是允许values重复. 然后 key->value 是加密, value->key 解密.
并且有约束, **所有允许的原字符串仅包含在一个 len<=100 的dictionary中**. (反向思维!)
要求是设计一个数据结构, 支持加解密操作, 最多调用200次.
复杂度分析: keys, values 的长度 <=26, 给出的待解密的字符串长度 <=200; 最多调用200次.

显然, 复杂度在解密环节, 若一个value对应了太多keys的时候搜索空间太高.
但这里给定了所有可能的原字符串, 显然要钻的空子就是预计算所有可能的加密结果.

输入：
["Encrypter", "encrypt", "decrypt"]
[[['a', 'b', 'c', 'd'], ["ei", "zf", "ei", "am"], ["abcd", "acbd", "adbc", "badc", "dacb", "cadb", "cbda", "abad"]], ["abcd"], ["eizfeiam"]]
输出：
[null, "eizfeiam", 2]

解释：
Encrypter encrypter = new Encrypter([['a', 'b', 'c', 'd'], ["ei", "zf", "ei", "am"], ["abcd", "acbd", "adbc", "badc", "dacb", "cadb", "cbda", "abad"]);
encrypter.encrypt("abcd"); // 返回 "eizfeiam"。 
                           // 'a' 映射为 "ei"，'b' 映射为 "zf"，'c' 映射为 "ei"，'d' 映射为 "am"。
encrypter.decrypt("eizfeiam"); // return 2. 
                              // "ei" 可以映射为 'a' 或 'c'，"zf" 映射为 'b'，"am" 映射为 'd'。 
                              // 因此，解密后可以得到的字符串是 "abad"，"cbad"，"abcd" 和 "cbcd"。 
                              // 其中 2 个字符串，"abad" 和 "abcd"，在 dictionary 中出现，所以答案是 2 。
"""
        global s
        s = s.split("\n")
        steps = eval(s[0])
        paras = eval(s[1])
        en = Encrypter(*paras[0])
        print(en.encrypt(paras[1][0]))
        print(en.decrypt(paras[2][0]))

class Encrypter0:
    """ 正常的思路, 因为解密的一对多问题, 这样暴力解法超时!
容易想到的改进是 DFS+Trie, 参见 [here](https://leetcode-cn.com/problems/encrypt-and-decrypt-strings/solution/by-class_-8pci/)

"""
    def __init__(self, keys: List[str], values: List[str], dictionary: List[str]):
        self.dictonary = set(dictionary)
        self.key2value = {key: value for key, value in zip(keys, values)}
        self.value2keys = {value: set() for value in values}
        for key, value in self.key2value.items():
            self.value2keys[value].add(key)

    def encrypt(self, word1: str) -> str:
        # assert word1 in self.dictonary
        res = ""
        for ch in word1:
            res += self.key2value[ch]
        return res

    def decrypt(self, word2: str) -> int:
        origin_chars = []
        for i in range(0, len(word2), 2):
            if word2[i:i+2] not in self.value2keys:
                return 0
            origin_chars.append(self.value2keys[word2[i:i+2]])
        def get_origin(chars_list):
            results = set()
            def dfs(i, s=""):
                if i >= len(chars_list):
                    results.add(s)
                    return
                for ch in chars_list[i]:
                    dfs(i+1, s+ch)
                return results
            return dfs(0)
        possible_origins = get_origin(origin_chars)
        return len([o for o in possible_origins if o in self.dictonary])

class Encrypter:
    """ 但这题题目就很特殊, 约束了合法的加密字符一定出现在 dictionary中.

思路2: 反向思维
因此可以反过来: 统计所有可能的加密结果, 然后解密的时候根据这一结果返回即可.
from [here](https://leetcode-cn.com/problems/encrypt-and-decrypt-strings/solution/by-endlesscheng-sm8h/)
"""
    def __init__(self, keys: List[str], values: List[str], dictionary: List[str]):
        self.map = dict(zip(keys, values))
        self.cnt = collections.Counter(self.encrypt(s) for s in dictionary)

    def encrypt(self, word1: str) -> str:
        res = ""
        for ch in word1:
            if ch not in self.map:
                return ""
            res += self.map[ch]
        return res

    def decrypt(self, word2: str) -> int:
        return self.cnt[word2]


s0 = """["Encrypter","encrypt","decrypt"]
[[["a","b","c","d"],["ei","zf","ei","am"],["abcd","acbd","adbc","badc","dacb","cadb","cbda","abad"]],["abcd"],["eizfeiam"]]
"""
s= """["Encrypter","encrypt","decrypt"]
[[["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"],["ei","zf","ei","am","gb","zz","zz","ac","qa","mn","aa","is","aa","op","pq","qr","rs","st","tu","uv","aa","sz","bb","aa","ac","aa"],["abcd","acbd","adbc","badc","dacb","cadb","cbda","abad"]],["abce"],["eizfeiam"]]
"""

sol = Solution()
result = [
    # sol.convertTime(current = "02:30", correct = "04:35"),
    
    # sol.findWinners(matches = [[1,3],[2,3],[3,6],[5,6],[5,7],[4,5],[4,8],[4,9],[10,4],[10,9]]),
    
    sol.maximumCandies(candies = [5,8,6], k = 3),
    sol.maximumCandies(candies = [2,5], k = 11),
    sol.maximumCandies([4,7,5], 4),
    sol.maximumCandies([5,8,6], 3),
    
    # sol.test4()
]
for r in result:
    print(r)