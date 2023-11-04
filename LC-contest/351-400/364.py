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
https://leetcode.cn/contest/weekly-contest-364
https://leetcode.cn/circle/discuss/WhhMVw/

T2T3 居然是相同的题目😂 T4的想法自以为还不错!

Easonsi @2023 """
class Solution:
    """ 2864. 最大二进制奇数 """
    def maximumOddBinaryNumber(self, s: str) -> str:
        s = sorted(list(s), reverse=True)
        s = s[1:] + ['1']
        return ''.join(s)

    """ 2865. 美丽塔 I #medium 给定每个位置的最大高度 maxHeights, 要求构建一个数组, 在满足最大高度的约束下, 同时是「山状 数组」. 求最大高度和
限制: n 1e3
    """
    def maximumSumOfHeights(self, maxHeights: List[int]) -> int:
        n = len(maxHeights)
        ans = 0
        for i in range(n):
            tmp = acc = maxHeights[i]
            for j in range(i-1,-1,-1):
                tmp = min(tmp, maxHeights[j])
                acc += tmp
            tmp = maxHeights[i]
            for j in range(i+1,n):
                tmp = min(tmp, maxHeights[j])
                acc += tmp
            ans = max(ans, acc)
        return ans
    
    """ 2866. 美丽塔 II #medium 
限制 n 1e5
思路1: #单调栈
    计算左右「最大和」
    例如对于 [5,3,4,1,1], 从右往左, 最大和分别可以取到 1; 1+1=2; 1+1+4=6; 1+1+3+3=8; 1+1+3+3+5=13
    如何进行「历史状态」的记录和更新? 可以用 #单调栈
    """
    def maximumSumOfHeights(self, maxHeights: List[int]) -> int:
        n = len(maxHeights)
        def getLeftMax(arr):
            leftMax = [0]*n
            ss = 0
            st = []
            for i,x in enumerate(arr):
                cnt = 1
                while st and st[-1][0]>=x:
                    pv,c = st.pop()
                    ss -= pv*c
                    cnt += c
                st.append((x,cnt))
                ss += x*cnt
                leftMax[i] = ss
            return leftMax
        leftMax = getLeftMax(maxHeights)
        rightMax = getLeftMax(maxHeights[::-1])[::-1]
        ans = 0
        for l,r,x in zip(leftMax, rightMax, maxHeights):
            ans = max(ans, l+r-x)
        return ans
    
    """ 2867. 统计树中的合法路径数目 #hard 给定一棵树, 计算所有的路径数量, 其节点序号只包含一个质数
限制: n 1e5
思路1: 对于一个质数节点, 包含其的「合法路径」数量, 取决于它所连接的非质数节点子树!
    """
    def countPaths(self, n: int, edges: List[List[int]]) -> int:
        # get primes from [1...n]
        isPrime = [True]*(n+1)
        isPrime[0] = isPrime[1] = False
        for i in range(2, n+1):
            if isPrime[i]:
                for j in range(i*i, n+1, i):
                    isPrime[j] = False
        # build the graph
        g = [[] for _ in range(n+1)]
        for u,v in edges:
            g[u].append(v)
            g[v].append(u)
        # bfs
        ans = 0
        prime2cnt = [0]*(n+1)
        visited = [False]*(n+1)
        def bfs(u):
            if isPrime[u] or visited[u]: return
            nonlocal ans
            primes = []
            q = deque([u])
            num_noprime = 0
            while q:
                u = q.popleft()
                num_noprime += 1
                visited[u] = True
                for v in g[u]:
                    if visited[v]: continue
                    if isPrime[v]:
                        primes.append(v)
                    else:
                        q.append(v)
            for p in primes:
                ans += (prime2cnt[p]+1) * num_noprime
                prime2cnt[p] += num_noprime
        for i in range(1, n+1):
            bfs(i)
        return ans
    
sol = Solution()
result = [
    # sol.maximumOddBinaryNumber(s = "0101"),
    sol.maximumSumOfHeights(maxHeights = [5,3,4,1,1]),
    
    # sol.countPaths(n = 5, edges = [[1,2],[1,3],[2,4],[2,5]]),
    # sol.countPaths(n = 6, edges = [[1,2],[1,3],[2,4],[3,5],[3,6]]),
    # sol.countPaths(9, [[7,4],[3,4],[5,4],[1,5],[6,4],[9,5],[8,7],[2,8]])
]
for r in result:
    print(r)
