

from typing import List
import collections
import random
import heapq


""" @220116
https://leetcode-cn.com/contest/weekly-contest-278
 """
class Solution278:
    """ 2154. 将找到的值乘以 2
在数组中找一个数字, 若出现, 则进一步将该数字 *2, 继续找; 直到要寻找的数字不在数组中 """
    def findFinalValue(self, nums: List[int], original: int) -> int:
        if original in nums:
            return self.findFinalValue(nums, original*2)
        return original
    
    """ 2155. 分组得分最高的所有下标 
nums 可以按下标 i（ 0 <= i <= n ）拆分成两个数组（可能为空）, 定义其得分为 左半部分 0 的个数 + 右半部分 1 的个数。
返回是的得分最大的所有拆分的下标

输入：nums = [0,0,1,0]
输出：[2,4]
解释：按下标分组
- 0 ：numsleft 为 [] 。numsright 为 [0,0,1,0] 。得分为 0 + 1 = 1 。
- 1 ：numsleft 为 [0] 。numsright 为 [0,1,0] 。得分为 1 + 1 = 2 。
- 2 ：numsleft 为 [0,0] 。numsright 为 [1,0] 。得分为 2 + 1 = 3 。
- 3 ：numsleft 为 [0,0,1] 。numsright 为 [0] 。得分为 2 + 0 = 2 。
- 4 ：numsleft 为 [0,0,1,0] 。numsright 为 [] 。得分为 3 + 0 = 3 。
下标 2 和 4 都可以得到最高的分组得分 3 。
注意，答案 [4,2] 也被视为正确答案。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/all-divisions-with-the-highest-score-of-a-binary-array
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。"""
    def maxScoreIndices(self, nums: List[int]) -> List[int]:
        count0, count1 = 0, 0
        sum0, sum1 = [0], [0]
        for num in nums:
            if num==0:
                count0 += 1
            elif num==1:
                count1 += 1
            sum0.append(count0)
            sum1.append(count1)
        sum1 = [sum1[-1]-i for i in sum1]
        scores = [a+b for a,b in zip(sum0, sum1)]
        maxS = max(scores)
        result = []
        for i,s in enumerate(scores):
            if s == maxS:
                result.append(i)
        return result

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


    """ 2157. 字符串分组
每个字符串包括了一组不相同的字符 (比如 cde), 定义两个字符串「相连」: 其一可以通过 添加/删除/替换(替换成相同字符也可, 即包括相同字符集合的两字符串相连) 一个字符得到另一个字符串。
定义组: 如果一个字符串与该组中的任一字符串相连，则这个字符串属于该组。
给一组字符串, 计算有多少个不同的组, 以及最大组包括的字符串数量。

输入：words = ["a","b","ab","cde"]
输出：[2,3]
解释：
- words[0] 可以得到 words[1] （将 'a' 替换为 'b'）和 words[2] （添加 'b'）。所以 words[0] 与 words[1] 和 words[2] 关联。
- words[1] 可以得到 words[0] （将 'b' 替换为 'a'）和 words[2] （添加 'a'）。所以 words[1] 与 words[0] 和 words[2] 关联。
- words[2] 可以得到 words[0] （删去 'b'）和 words[1] （删去 'a'）。所以 words[2] 与 words[0] 和 words[1] 关联。
- words[3] 与 words 中其他字符串都不关联。
所以，words 可以分成 2 个组 ["a","b","ab"] 和 ["cde"] 。最大的组大小为 3 。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/groups-of-strings
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。


方法一：状态压缩 + 广度优先搜索
from [here](https://leetcode-cn.com/problems/groups-of-strings/solution/zi-fu-chuan-fen-zu-by-leetcode-solution-a8dr/) """
    def groupStrings(self, words: List[str]) -> List[int]:
        # 使用哈希映射统计每一个二进制表示出现的次数
        wordmasks = collections.Counter()
        for word in words:
            mask = 0
            for ch in word:
                mask |= (1 << (ord(ch) - ord("a")))
            wordmasks[mask] += 1
        
        # 辅助函数，用来得到 mask 的所有可能的相邻节点
        def get_adjacent(mask: int) -> List[int]:
            adj = list()
            # 将一个 0 变成 1，或将一个 1 变成 0
            for i in range(26):
                adj.append(mask ^ (1 << i))
            # 将一个 0 变成 1，且将一个 1 变成 0
            for i in range(26):
                if mask & (1 << i):
                    for j in range(26):
                        if not (mask & (1 << j)):
                            adj.append(mask ^ (1 << i) ^ (1 << j))
            return adj
        
        used = set()
        best = cnt = 0
        for mask, occ in wordmasks.items():
            if mask in used:
                continue
            
            # 从一个未搜索过的节点开始进行广度优先搜索，并求出对应连通分量的大小
            q = collections.deque([mask])
            used.add(mask)
            # total 记录联通分量的大小
            total = occ

            while q:
                u = q.popleft()
                for v in get_adjacent(u):
                    if v in wordmasks and v not in used:
                        q.append(v)
                        used.add(v)
                        total += wordmasks[v]
            
            best = max(best, total)
            cnt += 1
            
        return [cnt, best]


sol = Solution278()
res = [
    # sol.subStrHash(s = "leetcode", power = 7, modulo = 20, k = 2, hashValue = 0),
    # sol.subStrHash(s = "fbxzaad", power = 31, modulo = 100, k = 3, hashValue = 32),
    # sol.subStrHash("xxterzixjqrghqyeketqeynekvqhc",15,94,4,16),
    sol.subStrHash2("xmmhdakfursinye", 96,45,15,21),
]
for r in res:
    print(r)