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
https://leetcode.cn/contest/weekly-contest-418
https://leetcode.cn/circle/discuss/DezDBG/

难炸了的一次周赛... 
T1 学会了新的语法;
T2 需要仔细阅读题目. 
T3 也是需要审题, 同时代码比较冗长学会精简. 
T4 最大公约数的性质, 复杂度基于调和级数的性质! 

Easonsi @2023 """
class Solution:
    """ 3309. 连接二进制表示可形成的最大数值 #medium 二进制的方式连接数字, 要求得到的结果最大
[ling](https://leetcode.cn/problems/maximum-possible-number-by-binary-concatenation/solutions/2940489/fei-bao-li-zuo-fa-onlogn-pai-xu-pythonja-540j/)
标准的做法应该是定义两个数字之间的大小关系! 需要用到 functools.cmp_to_key 来实现. 
""" 
    def maxGoodNumber(self, nums: List[int]) -> int:
        # 因为数据太小的暴力做法
        nums = [bin(i)[2:] for i in nums]
        res = []
        for order in itertools.permutations(nums):
            res.append(int("".join(order), 2))
        return max(res)
    def maxGoodNumber(self, nums: list[int]) -> int:
        """ from ling """
        def cmp(a: int, b: int) -> int:
            # 如果其二进制表示（字符串）满足 a+b>b+a，那么 a 排在 b 的左边，否则 b 排在 a 的左边。
            len_a = a.bit_length()
            len_b = b.bit_length()
            return (b << len_a | a) - (a << len_b | b)
        nums.sort(key=functools.cmp_to_key(cmp))

        ans = 0
        for x in nums:
            ans = ans << x.bit_length() | x
        return ans

    
    """ 3310. 移除可疑的方法 #medium 有一组API调用关系 (a,b) 表示b调用了a. 对于给定的bug节点k, 它和它调用的节点都suspicious
对于一组可以方法, 若有其他方法掉用了其中一个节点, 则都不能被删除! 
思路1: 先 DFS找到所有的可疑方法, 然后检查其他节点和这组节点之间是否有连边! 
[ling](https://leetcode.cn/problems/remove-methods-from-project/solutions/2940460/liang-ci-dfspythonjavacgo-by-endlesschen-cjat/)
    """
    def remainingMethods(self, n: int, k: int, invocations: List[List[int]]) -> List[int]:
        g = [[] for _ in range(n)]
        for u,v in invocations:
            g[u].append(v)
        vis = set([k])
        q = deque([k])
        while q:
            u = q.popleft()
            for v in g[u]:
                if v in vis: continue
                vis.add(v)
                q.append(v)
        # 
        for u,v in invocations:
            if (u not in vis) and (v in vis):
                return list(range(n))
        return list(set(range(n)) - vis)
        
    """ 3311. 构造符合图结构的二维矩阵 #hard 给定一张包含N个节点的图. 构造一个m*n=N的矩阵填入节点, 要求矩阵相邻位置的两个节点都连了边. 
限制: E 1e5, u_i < v_i. 注意没有多余的边!
思路1: (假设是宽矩阵) 根据行数 1, 2, >=3 分类讨论
[ling](https://leetcode.cn/problems/construct-2d-grid-matching-graph-layout/solutions/2940537/fen-lei-tao-lun-zhu-xing-gou-zao-by-endl-v3x0/)
"""
    def constructGridLayout(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        g = [[] for _ in range(n)]
        degrees = [0 for _ in range(n)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
            degrees[u] += 1
            degrees[v] += 1
        # 
        degreeIdx = [[] for i in range(4)]
        for i,ds in enumerate(degrees):
            degreeIdx[ds].append(i)
        # condition 1
        if len(degreeIdx[0]) > 0:
            ans = [0] * n
            ans[0] = degreeIdx[0][0]
            vis = set([ans[0]])
        ...
    
    """ 3312. 查询排序后的最大公约数 #hard 对于一个数组, 首先得到所有 (i,j) pair 的最大公约数, 升序排列得到 gcdPairs, 然后对于q个查询返回 gcdPairs[q[i]]
限制: n 1e5; q 1e5
思路1: 统计gcd为 1,2,3,... 的数量, 对于每个查询二分! 
    如何计算gcd为 x 的数对数量? 假设数组中x的倍数有c个, 那么两两组合有 c*(c-1)/2 对. 
        需要排除掉所有gcd=x倍数的情况! 也即 gcdPairs[x] = c*(c-1)/2 - gcdPairs[2x] - gcdPairs[3x] - ...
    因此, 需要从 mx 开始倒序枚举. 
    复杂度多少? 这里枚举的过程, 根据调和级数可知复杂度为 O(U logU)
[ling](https://leetcode.cn/problems/sorted-gcd-pair-queries/solutions/2940415/mei-ju-rong-chi-qian-zhui-he-er-fen-pyth-ujis/)
"""
    def gcdValues(self, nums: List[int], queries: List[int]) -> List[int]:
        ...


sol = Solution()
result = [
    # sol.maxGoodNumber(nums = [1,2,3]),
    # sol.maxGoodNumber(nums = [2,8,16]),
    sol.remainingMethods(n = 5, k = 0, invocations = [[1,2],[0,2],[0,1],[3,4]]),
    sol.remainingMethods( n = 4, k = 1, invocations = [[1,2],[0,1],[3,2]]),
    sol.remainingMethods(3,2, [[1,0],[2,0]]),
]
for r in result:
    print(r)
