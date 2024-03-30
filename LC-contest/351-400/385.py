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
https://leetcode.cn/contest/weekly-contest-385
https://leetcode.cn/circle/discuss/ZnbNSt/

T2想复杂了; T3 没想到不用质数筛会更快; T4 #字典树 题很有意思!

Easonsi @2023 """

# 利用筛法求质数
N = int(1e7)
is_prime = [True] * N
is_prime[0] = is_prime[1] = False
for i in range(2, N):
    if is_prime[i]:
        for j in range(i * i, N, i):        # NOTE: 从 i^2 开始
            is_prime[j] = False

class Tire:
    __slots__ = ('children', 'cnt')
    def __init__(self) -> None:
        self.children = {}
        self.cnt = 0

class Solution:
    """ 3042. 统计前后缀下标对 I """
    def countPrefixSuffixPairs(self, words: List[str]) -> int:
        n = len(words)
        ans = 0
        for i in range(n):
            for j in range(i+1,n):
                x,y = words[i], words[j]
                if y.startswith(x) and y.endswith(x):
                    ans += 1
        return ans

    """ 3043. 最长公共前缀的长度 给定两组数字, 问两者的的交叉中, 最长的前缀长度
思路0: #Tire 树, 下面的解法, 复杂了
思路1: 直接用一个set来记录前缀情况! 可以用str或者直接用int处理 (直接记录最大值即可, 因为数字越大对应的字符串越长!)
    见 [ling](https://leetcode.cn/problems/find-the-length-of-the-longest-common-prefix/solutions/2644176/liang-chong-xie-fa-yong-zi-fu-chuan-bu-y-qwh8/)
    """
    def longestCommonPrefix(self, arr1: List[int], arr2: List[int]) -> int:
        class Tree:
            def __init__(self, val) -> None:
                self.val = val
                self.children = {}
        def add_number(root, num):
            for x in str(num):
                if x not in root.children:
                    root.children[x] = Tree(x)
                root = root.children[x]
        def query_number(root, num):
            ans = 0
            for x in str(num):
                if x in root.children:
                    root = root.children[x]
                    ans += 1
                else:
                    break
            return ans
        root = Tree('')
        for num in arr1:
            add_number(root, num)
        return max(query_number(root, num) for num in arr2)
    
    """ 3044. 出现频率最高的质数 #medium """
    def mostFrequentPrime(self, mat: List[List[int]]) -> int:
        directions = [(0,1), (1,0), (0,-1), (-1,0)] + [(-1,-1), (-1,1), (1,-1), (1,1)]
        m,n = len(mat), len(mat[0])
        cnt = Counter()
        for i, row in enumerate(mat):
            for j, x in enumerate(row):
                for ds,dy in directions:
                    nx = x
                    ni,nj = i,j
                    while 0<=ni+ds<m and 0<=nj+dy<n:
                        nx = 10*nx + mat[ni+ds][nj+dy]
                        ni,nj = ni+ds, nj+dy
                        # 在路径上检测是否是质数
                        if is_prime[nx]:
                            cnt[nx] += 1
        vals = list(cnt.items())
        vals.sort(key=lambda x: (-x[1], -x[0]))
        return vals[0][0] if vals else -1
    
    """ 3045. 统计前后缀下标对 II #medium 给定一组字符串, 问有多少组 (i<j) 使得 words[i] 同时是 words[j] 的前缀和后缀
限制: n 1e5; 字符串总长度 5e5
思路1: #字典树 + #Z函数
    由于 z[i] 的定义是后缀 t[i:] 与 t 的最长公共前缀的长度，所以只要 z[i]=n-i，那么 t[i:] 和与其等长的 t 的前缀是相等的。
思路2: 直接用 #字典树 用pair来记录前后缀!
    如何判断s是t的前后缀? (s[0],s[-1]), (s[1],s[-2]), (s[2],s[-3]) ... 这样的序列需要是t对应序列的前缀!!!
[ling](https://leetcode.cn/problems/count-prefix-and-suffix-pairs-ii/solutions/2644160/z-han-shu-zi-dian-shu-pythonjavacgo-by-e-5c2v/)
    """
    def countPrefixSuffixPairs(self, words: List[str]) -> int:
        # TLE!!!
        pres = Counter()
        ans = 0
        for word in words:
            # NOTE: 暴力枚举会超时! 例如对于 word = 'a'*100000 的复杂度为 O(n^2)
            # for i in range(len(word)):
            #     p = word[:i+1]
            #     if word.endswith(p):
            #         ans += pres[p]
            z = self.calc_z(word)
            nn = len(z)
            for i in range(nn):
                if z[-i-1] == i+1:  # t[-1-i:] == t[:i+1]
                    # NOTE: 这里一定要用字典树orz! 因为对于 word = 'a'*100000 它的所有前缀都是前后缀, 取字符串的复杂度也得是 O(n^2)
                    ans += pres[word[:i+1]]
            pres[word] += 1
        return ans

    def countPrefixSuffixPairs(self, words: List[str]) -> int:
        # 思路1: #字典树 + #Z函数
        ans = 0
        root = Tire()
        for word in words:
            z = self.calc_z(word)
            cur = root
            for i,c in enumerate(word):
                if c not in cur.children:
                    cur.children[c] = Tire()
                cur = cur.children[c]
                if z[-i-1] == i+1:  # t[-1-i:] == t[:i+1]
                    ans += cur.cnt
            cur.cnt += 1        # 记录这个单词!!
        return ans

    def countPrefixSuffixPairs(self, words: List[str]) -> int:
        # 思路2: 直接用 #字典树 用pair来记录前后缀!
        root = Tire()
        ans = 0
        for word in words:
            cur = root
            for p in zip(word, word[::-1]):
                if p not in cur.children:
                    cur.children[p] = Tire()
                cur = cur.children[p]
                ans += cur.cnt
            cur.cnt += 1
        return ans


    def calc_z(self, s: str) -> List[int]:
        n = len(s)
        z = [0] * n
        l, r = 0, 0
        for i in range(1, n):
            if i <= r:
                z[i] = min(z[i - l], r - i + 1)
            while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                l, r = i, i + z[i]
                z[i] += 1
        z[0] = n
        return z


sol = Solution()
result = [
    # sol.longestCommonPrefix(arr1 = [1,10,100], arr2 = [1000]),
    # sol.mostFrequentPrime(mat = [[1,1],[9,9],[1,1]]),
    # sol.mostFrequentPrime(mat = [[7]]),

    sol.countPrefixSuffixPairs(words = ["a","aba","ababa","aa"]),
    sol.countPrefixSuffixPairs(words = ["pa","papa","ma","mama"]),
    sol.countPrefixSuffixPairs(["abab", "ab"])
]
for r in result:
    print(r)
