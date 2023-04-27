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
https://leetcode.cn/contest/weekly-contest-170

T2 用到前缀异或和, 有点巧妙; T3 读题的时候不太仔细; T4的等价问题转化非常有趣! 

@2022 """
class Solution:
    """ 1309. 解码字母到整数映射 #easy 顺序逆序遍历都可以 """
    def freqAlphabets(self, s: str) -> str:
        ret = []
        chars = string.ascii_lowercase
        idx = len(s)-1
        while idx>=0:
            if s[idx]=='#': 
                ret.append(chars[int(s[idx-2:idx])-1])
                idx -= 3
            else:
                ret.append(chars[int(s[idx])-1])
                idx -= 1
        return ''.join(ret[::-1])
    
    """ 1310. 子数组异或查询 #medium #题型 给定一个数组, 对于每个查询 [s,e] 返回区间数组中的元素异或和.
思路1: 采用 #前缀 #异或
    利用异或的性质 `x^x = 0`, 可以用前缀来处理区间查询问题
[官答](https://leetcode.cn/problems/xor-queries-of-a-subarray/solution/zi-shu-zu-yi-huo-cha-xun-by-leetcode-solution/)
"""
    def xorQueries(self, arr: List[int], queries: List[List[int]]) -> List[int]:
        # 前缀异或和
        pre_xor = [0]
        for a in arr:
            pre_xor.append(pre_xor[-1]^a)
        return [pre_xor[q[1]+1]^pre_xor[q[0]] for q in queries]
    
    """ 1311. 获取你好友已观看的视频 #medium
注意这里 level k 的定义: 所有和source的最短距离为k的节点. 
"""
    def watchedVideosByFriends(self, watchedVideos: List[List[str]], friends: List[List[int]], id: int, level: int) -> List[str]:
        n = len(friends)
        used = [False] * n
        q = collections.deque([id])
        used[id] = True
        for _ in range(level):
            span = len(q)
            for i in range(span):
                u = q.popleft()
                for v in friends[u]:
                    if not used[v]:
                        q.append(v)
                        used[v] = True
        
        freq = collections.Counter()
        for _ in range(len(q)):
            u = q.pop()
            for watched in watchedVideos[u]:
                freq[watched] += 1

        videos = list(freq.items())
        videos.sort(key=lambda x: (x[1], x[0]))

        ans = [video[0] for video in videos]
        return ans


    """ 1312. 让字符串成为回文串的最少插入次数 #hard 对于一个字符串, 可以在其中插入字符, 问变为回文串所需的最少操作次数. 限制: n 500
提示: 注意, 问题等价于, 求「字符串中最长回文子序列」
    考察结果字符串中, 哪些部分需要新增? 我们将新增的那些字符的回文对应部分删去, 则「剩下的字符是原字符串的子序列, 并且回文」!
    因此, 本题答案为 n - 最长回文子序列长度
思路1: 基本 #DP 用来求最长回文子序列. 
    记 `f[i,j]` 表示子串中的最长回文长度. 
    递归: 1) 若 s[i]==s[j], 则 `f[i,j] = f[i+1,j-1]+2`; 2) 否则为 `min{ f[i,j-1], f[i+1,j] }`
    简单起见, 可以写成记忆化搜索; 当然要写成正常DP形式更快, 但要注意遍历顺序. 
关联: 0516. 最长回文子序列
[官答](https://leetcode.cn/problems/minimum-insertion-steps-to-make-a-string-palindrome/solution/rang-zi-fu-chuan-cheng-wei-hui-wen-chuan-de-zui--2/)
"""
    def minInsertions(self, s: str) -> int:
        # 思路1 写成记忆化搜索
        n = len(s)
        # 求最长回文子序列
        @lru_cache(None)
        def f(i,j):
            if i>j: return 0
            if i==j: return 1
            if s[i]==s[j]: return f(i+1,j-1)+2
            else: return max(f(i+1,j), f(i,j-1))
        return n-f(0,n-1)

    def minInsertions(self, s: str) -> int:
        # 思路1, 正常DP, 速度更快. 
        n = len(s)
        dp = [[0] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            dp[i][i] = 1
            for j in range(i + 1, n):
                if s[i] == s[j]:
                    dp[i][j] = dp[i + 1][j - 1] + 2
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
        return n - dp[0][n - 1]



sol = Solution()
result = [
    # sol.freqAlphabets(s = "10#11#12"),
    # sol.freqAlphabets("1326#"),
    sol.minInsertions(s = "mbadm"),
    sol.minInsertions("zzazz")
]
for r in result:
    print(r)
