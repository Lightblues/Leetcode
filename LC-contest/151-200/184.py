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
https://leetcode.cn/contest/weekly-contest-184

T2 的查询很有意思, 利用树状数组的题解是很优雅的想法. T4是基本的状压DP.

@2022 """
class Solution:
    """ 1409. 查询带键的排列 #medium #题型 一开始有一个 1...m 的数组, 然后给 q个查询, 每次将第 idx个元素抽到最前面. 问这q次查询中, 每次取到的元素. 限制: 1000
思路1: 暴力 #模拟 复杂度 O(n^2)
思路2: #树状数组
    注意树状数组的作用就是「单点修改」和「区间查询」
    如何记录「将某一位置的数字向前置顶」的操作? 假设原数组长 n, 操作数 q. 我们先开辟一个长 n+q 的数组, 将原数组放在最后, 
        然后每次将需要置顶的元素调出来放在最前面的空位处. 
    这样, 有一些位置是留空的, 我们可以用 0/1 表征.
    需要DS支持什么操作? 要找到数组中的第i的元素, 等价于数组前缀和为 i的元素. 这样, 可以用树状数组来记录
[official](https://leetcode.cn/problems/queries-on-a-permutation-with-key/solution/cha-xun-dai-jian-de-pai-lie-by-leetcode-solution/)
"""
    def processQueries(self, queries: List[int], m: int) -> List[int]:
        # 思路1: 暴力 #模拟 复杂度 O(n^2)
        p = list(range(1, m+1))
        ret = []
        for q in queries:
            idx = p.index(q)
            ret.append(idx)
            p = [p[idx]] + p[:idx] + p[idx+1:]
        return ret
    
    """ 1410. HTML 实体解析器 #medium 需要将原字符串中的HTML转义字符替换回来. 相关字符如下. """
    def entityParser(self, text: str) -> str:
        m = zip(
            # 注意将 &amp; = & 放在最后替换, 避免产生重复替换. 例如 `&amp;gt` 若发生两题替换则变为 >
            "&quot; &apos; &gt; &lt; &frasl; &amp;".split(),
            "\" ' > < / &".split()
        )
        for u,v in m:
            text = text.replace(u, v)
        return text
    
    """ 1411. 给 N x 3 网格图涂色的方案数 #hard 需要给一个 N x 3 的网格图涂色, 每个格子有三种颜色, 且相邻格子不能有相同的颜色. 求有多少种涂色方案. 
限制: n 5000; 对答案取模.
思路1: #状压 #DP. 对于每一行的涂色状态, 可以通过三进制的一个数表示. (共 3^3 = 27种状态)
    注意, 每一行的限制仅与上一临近行有关.
    记 `dp[i, mask]` 表示第 i行的涂色状态为 mask 的方案数. 显然有转移方程 `dp[i, mask] = sum{ dp[i-1, m] }`, 这里的m要求和mask不冲突.
    复杂度: 所有的mask数量为 27. 因此整体复杂度为 O(27 n)
思路2: 将mask分成两类, 直接递推更新.
    实际上, 不同的涂色方案可以分为两种: 123 形式和 121 形式. 我们用两个变量记录遍历的每一行其可能出现的次数, 可以得到更新公式.
见 [official](https://leetcode.cn/problems/number-of-ways-to-paint-n-3-grid/solution/gei-n-x-3-wang-ge-tu-tu-se-de-fang-an-shu-by-leetc/)
"""
    def numOfWays(self, n: int) -> int:
        MOD = 10**9 + 7 
        MX = 3**3
        def checkLine(mask):
            a,b,c = mask//9,mask//3%3,mask%3
            if a==b or b==c: return False
            return True
        def check(mask1, mask2):
            a1,b1,c1 = mask1//9, mask1//3%3, mask1%3
            if a1==b1 or b1==c1: return False
            a2,b2,c2 = mask2//9, mask2//3%3, mask2%3
            if a2==b2 or b2==c2: return False
            if a1==a2 or b1==b2 or c1==c2: return False
            return True
        f = [1 if checkLine(mask) else 0 for mask in range(MX)]
        for i in range(1, n):
            g = [0] * MX
            for mask1 in range(MX):
                for mask2 in range(MX):
                    if check(mask1, mask2):
                        g[mask1] += f[mask2]
                g[mask1] %= MOD
            f = g
        return sum(f) % MOD
    def numOfWays(self, n: int) -> int:
        # 思路2: 将mask分成两类, 直接递推更新.
        mod = 10**9 + 7
        fi0, fi1 = 6, 6
        for i in range(2, n + 1):
            fi0, fi1 = (2 * fi0 + 2 * fi1) % mod, (2 * fi0 + 3 * fi1) % mod
        return (fi0 + fi1) % mod

    
sol = Solution()
result = [
    sol.numOfWays(3),
    sol.numOfWays(5000),
]
for r in result:
    print(r)
