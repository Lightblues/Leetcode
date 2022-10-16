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
https://leetcode-cn.com/contest/biweekly-contest-90

T1 好复杂Orz, 写了个好蠢的方法; T2也有一定的难度, 用到前缀和; T4感觉是个图论, 但用了半小时猜了出来. 这次的难度还挺大. 
排名 79 https://leetcode.cn/contest/biweekly-contest-89/ranking/

@2022 """
class Solution:
    """ 6208. 有效时间的数目 #easy #题型 给定一个 "?5:?0" 这种形式的时间, 问有多少种可能的时间.
思路1: 暴力遍历所有的 00:00 ~ 23:59, 尝试匹配.
"""
    def countTime(self, time: str) -> int:
        # digits = [-1] * 4
        # if time[0] != '?': digits[0] = int(time[0])
        # if time[1] != '?': digits[1] = int(time[1])
        # if time[3] != '?': digits[2] = int(time[3])
        # if time[4] != '?': digits[3] = int(time[4])
        def f(pattern, ttime):
            for p,t in zip(pattern, ttime):
                if p in "?:": continue
                elif p!=t: return False
            return True
        cnt = 0
        for h in range(24):
            for m in range(60):
                t = f'{h:02d}:{m:02d}'
                # if re.match(time, t):
                if f(time, t):
                    cnt += 1
        return cnt
    
    """ 6209. 二的幂数组中查询范围内的乘积 #medium #题型 对于一个数字, 分解成2的倍数的唯一形式 例如 15 分解成 powers = [1,2,4,8]. 
然后要求计算一些查询, 统计 powers[l,r] 的乘积. 限制: 查询数量 n 1e5. 取模
思路1: 本质上就是求出二进制表达. 统计在哪些位上有1. 
    注意到累乘的值可能比较大, 需要用 mod. 
"""
    def productQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        nstr = bin(n)[2:]
        idxs = []
        for i,c in enumerate(nstr[::-1]):
            if c == '1': idxs.append(i)
        acc = list(accumulate(idxs, initial=0))
        ans = []
        mod = 10**9 + 7
        for l,r in queries:
            p = acc[r+1] - acc[l]
            ans.append(pow(2, p, mod))
        return ans
    
    """ 6210. 最小化数组中的最大值 #medium 对于一个数组, 每次可以将第i位的值-1, 转移到第i-1位上. 问经过操作后, 数组最大值最小可以是多少.
思路1: #贪心 即可 
    注意贪心的正确性: 对于历史的较大值, 由于我们是顺序计算的, 不会被遗漏. 
"""
    def minimizeArrayValue(self, nums: List[int]) -> int:
        acc = 0
        ans = 0
        for i,a in enumerate(nums):
            acc += a
            ans = max(ans , math.ceil(acc/(i+1)))
        return ans
    
    
    """ 6211. 创建价值相同的连通块 #hard 每个节点有一个值, 构成树结构. 问最多能够删除多少边, 使得每个联通块的值之和相同.
限制: n 2e4; 值 50. 
思路1: 猜出来的. 统计每个节点子树和.
    对于每颗子树统计和. 观察, 猜规律: 假如能够分割成每个块和值为 x, 则子树和中x的倍数的数量一定要多于 sum//x. 
    因此, 统计每棵子树和. 计数. 然后从小到大枚举x, 检查是否满足条件.
    复杂度: 计算子树和 O(n); 枚举数量 nV 每次最多 n, 因此 O(n^2 * V)? 但一般不会这么差.
"""
    def componentValue(self, nums: List[int], edges: List[List[int]]) -> int:
        n = len(nums)
        g = [[] for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        # 计算每个节点的子树和
        vals = [0] * n
        def dfs(node, p):
            acc = nums[node]
            for v in g[node]:
                if v==p: continue
                acc += dfs(v, node)
            vals[node] = acc
            return acc
        dfs(0, -1)
        # 统计子树和的频率
        cnt = Counter(vals)
        # 验证每一个可能成立的 联通块和. 从小到大验证 (快的数量一次减少)
        s = sum(nums)
        poss = [i for i in range(1, s+1) if s%i==0]
        for a in poss:
            if sum(cnt[v] for v in range(a, s+1, a)) >= s//a:
                return s//a - 1 # 可以减去的数量 = 联通块数量 - 1
    
sol = Solution()
result = [
    # sol.countTime("?5:00"),
    # sol.countTime("0?:0?"),
    # sol.countTime(time = "??:??"),
    # sol.productQueries(n = 15, queries = [[0,1],[2,2],[0,3]]),
    # sol.productQueries(n = 2, queries = [[0,0]]),
    # sol.minimizeArrayValue(nums = [3,7,1,6]),
    # sol.minimizeArrayValue([10,1]),
    sol.componentValue(nums = [6,2,2,2,6], edges = [[0,1],[1,2],[1,3],[3,4]] ),
    sol.componentValue(nums = [2], edges = []),
]
for r in result:
    print(r)
