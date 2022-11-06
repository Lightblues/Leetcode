from easonsi.util.leetcode import *

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
https://leetcode.cn/contest/weekly-contest-152
T3 没看清题意是「重排」. T4 也是阅读理解有问题... 整体的质量很高~

@2022 """
class Solution:
    """ 1175. 质数排列 """
    def numPrimeArrangements(self, n: int) -> int:
        def getPrimes(n):
            ps = [2]
            for x in range(3, n+1, 2):
                for p in ps:
                    if x % p == 0:
                        break
                else:
                    ps.append(x)
            return ps
        primes = getPrimes(n)
        p = len(primes)
        mod = 10**9 + 7
        return math.factorial(p) * math.factorial(n-p) % mod
    
    """ 1176. 健身计划评估 #easy """
    
    """ 1177. 构建回文串检测 #medium #题型 对于字符串, 需要返回 q个检查, 每次检查 (l,r) 范围的子串元素在 **修改k个字符的限制下** 能否 **通过重排** 构成回文串 限制: n, q 1e5
思路1: 利用 #位运算 记录每个字符的奇偶性. 
    对于可 #重排 的情况是否 #回文? 判断字符数量的 #奇偶性 即可!
    提示: 利用 #二进制 #压缩表示. 
    可以利用 #前缀和 快速得到区间元素的奇偶性. 
    具体而言, 假设一组数字中, 出现奇数的个数有 x个, 则当 x//2 <= k 时是可以的. 例如 abc 只需要修改一次. 
"""
    def canMakePaliQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        mask = 0
        acc = [0]
        for x in s:
            mask ^= 1 << (ord(x) - ord('a'))
            acc.append(mask)
        ans = []
        for l,r,k in queries:
            m = acc[r+1] ^ acc[l]
            ans.append(m.bit_count()//2 <= k)
        return ans
    
    """ 1178. 猜字谜 #hard 一个word可以作为puzzle所匹配的条件是, word中所有字符都在puzzle中出现过, 并且包含其第一个字符. 现在给定一组 words 和 puzzles, 对于每个puzzle判断其可以作为多少word的谜面. 
限制: words数量 n 1e5; 每个词的长度 4...50; puzzle数量 m 1e4, 每个词的长度都是7 都是7个不同的字符. 
提示, 可以用二进制表示puzzle中所包含的7个字符, 再加上首位字符即可表示该谜面. (mask, firstCh)
思路1: 二进制 #状态压缩 的基础上, 进行 #子集枚举
    用什么来存储word的信息? 重要的只有其中所包含的字符, 直接二进制表示, 用一个cnt = {mask: freq} 存储即可.
    如何得到每个puzzle可能匹配的word? 其首字母一定到, 其他的六个字母 #子集枚举 即可. 
    复杂度分析: 对于所有的puzzle, 需要进行 2^6 级别的子集枚举. 
说明: 如何进行子集枚举? 1) 一种方式是对于 0~2^6 选出子集; 2) 也可以先得到6个字符的mask, 然后用 subset = (subset - 1) & mask 的方式筛选. 
见 [官答](https://leetcode.cn/problems/number-of-valid-words-for-each-puzzle/solution/cai-zi-mi-by-leetcode-solution-345u/)
"""
    def findNumOfValidWords(self, words: List[str], puzzles: List[str]) -> List[int]:
        # 记录所有的谜面 (word) 信息: 计数
        cnt = Counter()
        for word in words:
            mask = 0
            for ch in word:
                mask |= 1 << (ord(ch) - ord('a'))
            cnt[mask] += 1
        # 得到所有的 6个字符的组合 (子集)
        combs = []
        for m in range(2**6):
            i = 0
            idxs = []
            while m:
                if m & 1: idxs.append(i)
                m>>=1; i+=1
            combs.append(idxs)
        # 对于每个puzzle, 进行子集枚举
        ans = []
        for puzzle in puzzles:
            acc = 0
            # 注意这里的 mask, chars 计算方式!
            mask = 1 << (ord(puzzle[0]) - ord('a'))
            chars = [1<<(ord(c)-ord('a')) for c in puzzle[1:]]
            for comb in combs:
                m = reduce(operator.or_, [mask] + [chars[i] for i in comb])
                acc += cnt[m]
            ans.append(acc)
        return ans
    
sol = Solution()
result = [
    # sol.numPrimeArrangements(100),
    # sol.findNumOfValidWords(words = ["aaaa","asas","able","ability","actt","actor","access"], puzzles = ["aboveyz","abrodyz","abslute","absoryz","actresz","gaswxyz"]),
    sol.canMakePaliQueries(s = "abcda", queries = [[3,3,0],[1,2,0],[0,3,1],[0,3,2],[0,4,1]]),
]
for r in result:
    print(r)
