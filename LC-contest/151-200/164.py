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
https://leetcode.cn/contest/weekly-contest-164

T2 当时想多了; T3的复杂度不好分析, 没想到直接暴力就可以~ T4是基本的DP


@2022 """
class Solution:
    """ 1266. 访问所有点的最小时间 """
    
    """ 1267. 统计参与通信的服务器 #medium 
思路1: 对于 row, col 的计数, 然后对于每一个服务器判断是否可以通信.
"""
    def countServers(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        count_m, count_n = [0] * m, [0] * n
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    count_m[i] += 1
                    count_n[j] += 1
        ans = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1 and (count_m[i] > 1 or count_n[j] > 1):
                    ans += 1
        return ans

    """ 1268. 搜索推荐系统 #medium 有一组产品名, 对于一个查询 searchWord, 需要对于 s[:1], s[:2]... 每次找到前三个匹配的产品名. (字典序) 
限制: n 1e3; 所有产品名的字符总数 2e4; searchWord 长度 1e3. 
思路1: 排序之后 #二分 查找
    复杂度分析见官答
思路2: #字典树
    如何记录「字典树记录中, 当前前缀的三个最小字符串」? 可以用一个额外的结构存储到每个节点. 理论的时间复杂度会更优一些. 
[官答](https://leetcode.cn/problems/search-suggestions-system/solution/suo-tui-jian-xi-tong-by-leetcode-solution/)
"""
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        products.sort()
        ans = []
        for i in range(1, len(searchWord) + 1):
            # ans.append([p for p in products if p.startswith(searchWord[:i])][:3])
            idx = bisect_left(products, searchWord[:i])
            ans.append([p for p in products[idx:idx+3] if p.startswith(searchWord[:i])])
        return ans
    
    """ 1269. 停在原地的方案数 #hard 有一个长 arrLen 的数组, 一开始在索引0, 每次可以左/右移动一格/不动. 问 steps 步骤之后仍然在索引0 的可能数量. 
限制: steps 600. 对答案 #取模. 
思路1: #DP. 记 `f[s][i]` 表示经过s步骤之后停留在位置i的操作数. 则有 `f[s+1][i] = sum( f[s][i-1...i+1] )`. 
    复杂度: O(steps * arrLen). 
"""
    def numWays(self, steps: int, arrLen: int) -> int:
        # 边界: 数组长度为1, 没有移动
        if arrLen==1: return 1
        mod = 10 ** 9 + 7
        # 例如, step=2, 则可以移动的对应数组长度应该是 2
        mx = min(ceil(steps/2)+1, arrLen)
        f = [[0]*mx for _ in range(steps+1)]
        f[0][0] = 1
        for step in range(1, steps+1):
            # 左右两个边界
            f[step][0] = (f[step-1][0] + f[step-1][1]) % mod
            for i in range(1, mx-1):
                f[step][i] = (f[step-1][i-1] + f[step-1][i] + f[step-1][i+1]) % mod
            f[step][mx-1] = (f[step-1][mx-2] + f[step-1][mx-1]) % mod
        return f[steps][0]

    
sol = Solution()
result = [
    # sol.suggestedProducts(products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"),
    sol.numWays(steps = 3, arrLen = 2),
    sol.numWays(steps = 4, arrLen = 2),
    sol.numWays(2,4), # 2
]
for r in result:
    print(r)
