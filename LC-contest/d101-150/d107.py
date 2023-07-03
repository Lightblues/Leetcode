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
https://leetcode-cn.com/contest/biweekly-contest-107
https://leetcode.cn/circle/discuss/6UIeEX/

进入了自己不太熟悉的领域... T2, T3 分别是3/4维的DP, 只能说还需要练习! (想转移的时候感觉这个维度就被吓住了). 
T4反倒是比较经典的题目了 (虽然自己一开始状态不好也没想到). 

Easonsi @2023 """
class Solution:
    """ 2744. 最大字符串配对数目 """
    def maximumNumberOfStringPairs(self, words: List[str]) -> int:
        n = len(words)
        used = [False] * n
        ans = 0
        for i,w in enumerate(words):
            if used[i]: continue
            for j in range(i+1, n):
                if used[j]: continue
                if w[::-1]==words[j]:
                    ans += 1
                    used[i] = used[j] = True
                    break
        return ans

    """ 2745. 构造最长的新字符串 #medium #题型, 有 (x,y,z) 个 AA/BB/AB 构成的最长不包含 AAA/BBB 的字符串 
限制: n 50
思路1: #DP
    定义 f(x,y,z, a) 表示上一个状态是 a, 剩余数量 (x,y,z) 的最大长度! (注意, 这里的接口定义决定了函数好不好写!)
    注意, 最后的答案是 max( f(x,y,z,0), f(x,y,z,1), f(x,y,z,2) ) 事实上这里的第三项可以省略~
思路2: #数学 
    注意到, 只有0/1状态的时候, 序列只能是 AABBAABB.. 的形式, 连接的数量为 min(x,y)*2 + x!=y
    引入状态2之后, AB只能在 BB/AB/AA 之间! 并且不影响0/1的约束! 总之, 不影响!
[灵神](https://leetcode.cn/problems/construct-the-longest-new-string/solution/liang-chong-fang-fa-o1-gong-shi-ji-yi-hu-7fdi/)
    """
    def longestString(self, x: int, y: int, z: int) -> int:
        @lru_cache(None)
        def f(x,y,z,a):
            # 剩余数量 (x,y,z) 并且上一个状态 0/1/2 的最大长度
            # if x<0 or y<0 or z<0: return -inf
            if a==0: return f(x,y-1,z,1) + 1 if y>0 else 0
            else:
                # 两种状态可以合并! 1/2 后面都能接0/2
                res2 = f(x,y,z-1,1) + 1 if z>0 else 0
                res0 = f(x-1,y,z,0) + 1 if x>0 else 0
            return max(res2, res0)
        return max( f(x,y,z,0), f(x,y,z,1), f(x,y,z,2) ) * 2
    def longestString(self, x: int, y: int, z: int) -> int:
        aa = min(x,y)*2 + (x!=y)
        return (aa+z) * 2


    """ 2746. 字符串连接删减字母 #medium #题型 顺序连接n个字符串 (可以选择哪个在前), 若两个字符串首尾字符一样就可以省掉一个长度. 问连接的最小长度
限制: n 1e3; 
思路1: #DP 还是比较绕的! 
    记 f(i,s,e) 表示前i个字符串, 首尾分别为 s,e 的(最小)长度
    则有转移 (两条) f(i+1,s,w[i+1][-1]) -> f(i,s,e) + len(w[i+1]) - (w[i+1][0]==e)
    注意这里得到的解不一定是最小的! 我们从最后转移到的结果中选择最大的即可!
    复杂度: O(n * 26^2) 直接看状态空间! 显然不会TLE
    反思: 为什么从前往后? 因为可转移的状态更少! 自己之前想着「从后往前」钻牛角尖了
        那么如何「从前往后」传递信息呢? naive的想法是直接在f函数中增加一个状态 (下面的 1.1), 但会MLE! 
        反过来想, 我们定义 f 返回的是「整个字符串的最小长度」! 我们中间返回的结果直接加到前面即可!
思路2: 能否有没有26^2 项的DP? 
    灵神给了一个巧妙的定义: f(i,j) 表示进行到 max(i,j) 位置时候, 分别以i,j个单词作为首尾的最小长度! 
        由于题目中是顺序连接的, 我们知道一定进行到了 max(i,j) 位置! 
    idx = max(i,j); f(i,j) = max{ f(i,idx+1)+xx, f(idx+1,j)+xx }
    复杂度: O(n^2) 看上去更慢了一点. 但这里的想法非常巧妙!!
见 [灵神](https://www.bilibili.com/video/BV1am4y1a7Zi/?spm_id_from=444.41.list.card_archive.click&vd_source=7fac3e19524199181e34d7728078f310)
    """
    def minimizeConcatenatedLength(self, words: List[str]) -> int:
        n = len(words)
        ans = inf
        # 1.1] MLE了! 因为这里的传入了没有必要的信息! cache不起作用
        @lru_cache(None)
        def f(i, s,e, now):
            nonlocal ans
            if i==n: 
                ans = min(ans, now)
                return now
            word = words[i]
            res1 = now + len(word) - (word[0]==e)
            f(i+1, s, word[-1], res1)
            res2 = now + len(word) - (word[-1]==s)
            f(i+1, word[0], e, res2)
            return min(res1, res2)
        w = words[0]
        f(1, w[0], w[-1], len(w))
        f.cache_clear()
        return ans
    def minimizeConcatenatedLength(self, words: List[str]) -> int:
        n = len(words)
        @lru_cache(None)
        def f(i, s,e):
            if i==n: 
                return 0
            word = words[i]
            res1 = f(i+1, s, word[-1]) + len(word) - (word[0]==e)
            res2 = f(i+1, word[0], e) + len(word) - (word[-1]==s)
            return min(res1, res2)
        # f.cache_clear()
        w = words[0]
        return f(1, w[0], w[-1]) + len(w)
    def minimizeConcatenatedLength(self, words: List[str]) -> int:
        # 思路2: O(n^2) 看上去更慢了一点. 但这里的想法非常巧妙!!
        n = len(words)
        @lru_cache(None)
        def f(i, j):
            idx = max(i,j) + 1
            if idx==n: return 0
            word = words[idx]
            res1 = f(i, idx) + len(word) - (word[0]==words[j][-1])
            res2 = f(idx, j) + len(word) - (word[-1]==words[i][0])
            return min(res1, res2)
        w = words[0]
        ans = f(0,0) + len(w)
        # 注意这里的状态空间较高, 需要手动 clear
        f.cache_clear()
        return ans

    """ 2747. 统计没有收到请求的服务器数目 #medium 给定n个服务器, 有一组 (sid, t) 收到请求的序列. 对于给定的q个查询, 返回在时间 [ti-k, ti] 范围内没有收到请求的数量
限制: n 1e5; time 1e5; q 1e5
思路1: #排序+#离线 对于logs和queries都进行排序, 然后滑窗 (双指针)
    看上去挺复杂的, 但实际上还是比较套路的
    """
    def countServers(self, n: int, logs: List[List[int]], x: int, queries: List[int]) -> List[int]:
        nq = len(queries); nl = len(logs)
        qs = sorted([(q,i) for i,q in enumerate(queries)])
        ans = [0] * nq
        logs.sort(key=lambda l:l[1])
        l = r = 0
        cnt = [0] * (n+1)       # 记录当前范围内服务器情况次数
        used = 0
        for q,i in qs:
            start,end = q-x, q
            while r<nl and logs[r][1]<=end:
                sid = logs[r][0]
                cnt[sid] += 1
                if cnt[sid]==1: used += 1
                r += 1
            while l<nl and logs[l][1]<start:
                sid = logs[l][0]
                cnt[sid] -= 1
                if cnt[sid]==0: used -= 1
                l += 1
            ans[i] = n - used
        return ans


    
sol = Solution()
result = [
    # sol.maximumNumberOfStringPairs(words = ["cd","ac","dc","ca","zz"]),
    # sol.longestString(x = 2, y = 5, z = 1),
    # sol.longestString(x = 3, y = 2, z = 2),

    # sol.minimizeConcatenatedLength(words = ["aa","ab","bc"]),
    # sol.minimizeConcatenatedLength(words = ["aaa","c","aba"]),
    # sol.minimizeConcatenatedLength(["a","ca"]),

    sol.countServers(n = 3, logs = [[1,3],[2,6],[1,5]], x = 5, queries = [10,11]),
    sol.countServers(n = 3, logs = [[2,4],[2,1],[1,2],[3,1]], x = 2, queries = [3,4]),
]
for r in result:
    print(r)
