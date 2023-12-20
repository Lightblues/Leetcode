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
https://leetcode.cn/contest/weekly-contest-372
Easonsi @2023 """
class Solution:
    """ 2937. 使三个字符串相等 """
    def findMinimumOperations(self, s1: str, s2: str, s3: str) -> int:
        i = 0
        mn = min(len(s1), len(s2), len(s3))
        while i<mn and s1[i]==s2[i]==s3[i]:
            i += 1
        if i==0: return -1
        return len(s1)+len(s2)+len(s3) - 3*i
    
    """ 2938. 区分黑球与白球 """
    def minimumSteps(self, s: str) -> int:
        cnt = 0
        ans = 0
        for i,x in enumerate(s):
            if x=='0':
                ans += i-cnt
                cnt += 1
        return ans
    
    """ 2939. 最大异或乘积 #medium #位运算
利用到了结论: 根据二次函数的知识我们知道，当 p + q 为定值时，为了让 p * q 最大，需要让 abs(p - q) 最小
    """
    def maximumXorProduct(self, a: int, b: int, n: int) -> int:
        mod = 10**9+7
        mask = (1<<50)-1 - ((1<<n)-1)
        aa, bb = a&mask, b&mask
        for i in range(n-1,-1,-1):
            da, db = a&(1<<i), b&(1<<i)
            if da != db:
                if aa > bb: bb |= 1<<i
                else: aa |= 1<<i
            else:
                aa |= 1<<i
                bb |= 1<<i
        return (aa*bb)%mod
    
    """ 2940. 找到 Alice 和 Bob 可以相遇的建筑 #hard 
给定一个数组, 对于每次查询 (i,j) 数组, 找到最小的满足条件的 idx > i or j, 同时 h[idx] > h[i] or h[j]
限制: n 5e4; q 5e4; arr[i] 1e9
思路1: #离线 处理 见下
    显然, 困难的场景就是 i<j 同时 h[i]>h[j] 的情况, 需要在j右侧找到更大的数字!
    我可以先对查询按照j进行排序! 然后, 我们在遍历右边界的时候, 可以记录还没有处理到的查询 (h[i],i)
        每次遇到新的 j,h[j], 我们可以对于此前的满足 h[i]<h[j] 的 i, 更新答案! 
思路2: 在线做法 + 线段树二分
    构建一棵维护区间 最大值 mx 的线段树
    上面的困难问题等价于, 给定 h[i],j 要在 [j+1,n-1] 范围内找到最左边的 mx > h[i]
[灵神](https://leetcode.cn/problems/find-building-where-alice-and-bob-can-meet/solutions/2533058/chi-xian-zui-xiao-dui-pythonjavacgo-by-e-9ewj/)
关联: 2286. 以组为单位订音乐会的门票 强制要求在线
    """
    def leftmostBuildingQueries(self, heights: List[int], queries: List[List[int]]) -> List[int]:
        # 思路1: #离线 处理
        n = len(heights)
        ans = [-1] * len(queries)
        queries_left = [[] for _ in range(n)]
        for idx,(i,j) in enumerate(queries):
            if i > j:
                i,j = j,i
            if i==j or heights[i] < heights[j]:
                ans[idx] = j
            else:
                queries_left[j].append((heights[i],idx))
        # 
        h = []
        for j, qs in enumerate(queries_left):
            while h and h[0][0] < heights[j]:
                _,idx = heapq.heappop(h)
                ans[idx] = j
            for q in qs:
                heapq.heappush(h, q)
        return ans

    def leftmostBuildingQueries(self, heights: List[int], queries: List[List[int]]) -> List[int]:
        """ https://leetcode.cn/problems/find-building-where-alice-and-bob-can-meet/solutions/2533058/chi-xian-zui-xiao-dui-pythonjavacgo-by-e-9ewj/ """



sol = Solution()
result = [
    # sol.findMinimumOperations('a','a','a'),
    # sol.minimumSteps(s = "100"),
    # sol.maximumXorProduct(a = 12, b = 5, n = 4),
    sol.leftmostBuildingQueries(heights = [6,4,8,5,2,7], queries = [[0,1],[0,3],[2,4],[3,4],[2,2]]),
    sol.leftmostBuildingQueries(heights = [5,3,8,2,6,1,4,6], queries = [[0,7],[3,5],[5,2],[3,0],[1,6]]),

]
for r in result:
    print(r)
