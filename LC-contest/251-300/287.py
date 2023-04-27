from easonsi import utils
from easonsi.util.leetcode import *
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

""" 2227. 加密解密字符串 #hard 给一个 {key:value} 的映射, 将一个字符映射到长度为2的一个字符串, key不重复但是允许values重复. 然后 key->value 是加密, value->key 解密.
    有约束, **所有允许的原字符串仅包含在一个 len<=100 的dictionary中**. 
    要求是设计一个数据结构, 支持加解密操作, 最多调用200次.
    复杂度: keys, values 的长度 <=26, 给出的待解密的字符串长度 <=200; 最多调用200次.
思路0: 暴力模拟 #TLE
    复杂度在解密环节, 若一个value对应了太多keys的时候搜索空间太高.
    容易想到的改进是 DFS+Trie, 参见 [here](https://leetcode-cn.com/problems/encrypt-and-decrypt-strings/solution/by-class_-8pci/)
思路1: #逆向 #思维
    这里给定了所有可能的原字符串, 可以预计算所有可能的加密结果!
    [灵神](https://leetcode.cn/problems/encrypt-and-decrypt-strings/solution/by-endlesscheng-sm8h/)
"""
class Encrypter:
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

sol = Solution()
result = [
    # sol.convertTime(current = "02:30", correct = "04:35"),
    
    # sol.findWinners(matches = [[1,3],[2,3],[3,6],[5,6],[5,7],[4,5],[4,8],[4,9],[10,4],[10,9]]),
    
    sol.maximumCandies(candies = [5,8,6], k = 3),
    sol.maximumCandies(candies = [2,5], k = 11),
    sol.maximumCandies([4,7,5], 4),
    sol.maximumCandies([5,8,6], 3),
]
for r in result:
    print(r)