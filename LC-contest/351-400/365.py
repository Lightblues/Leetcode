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
https://leetcode.cn/contest/weekly-contest-365
https://leetcode.cn/circle/discuss/9idUqp/
状态不错, 半小时左右模拟做了出来~

Easonsi @2023 """
class Solution:
    """ 2874. 有序三元组中的最大值 II #medium 对下表组 i<j<k, 求 (a[i]-a[j]) * a[k] 的最大值 
限制: n 1e5
思路1: 前缀最大差值, 后缀最大
    """
    def maximumTripletValue(self, nums: List[int]) -> int:
        n = len(nums)
        pre = [0]*n
        mxi=nums[0]; mxdiff=0
        for j in range(1,n):
            mxdiff = max(mxdiff, mxi - nums[j])
            mxi = max(mxi, nums[j])
            pre[j] = mxdiff
        post = [0]*n
        mx=0
        for k in range(n-1,0,-1):
            mx = max(mx, nums[k])
            post[k-1] = mx
        ans = max(i*j for i,j in zip(pre,post))
        return max(ans, 0)
    
    """ 2875. 无限数组的最短子数组 #medium 无限循环数组中, 和为target的最短子数组长度 """
    def minSizeSubarray(self, nums: List[int], target: int) -> int:
        n = len(nums)
        s = sum(nums)
        a,t = divmod(target, s)
        # 在 nums+nums 中找和为t的最短长度
        i = 0
        acc = 0
        mn = inf
        nums = nums + nums
        for j,x in enumerate(nums):
            acc += x
            while acc > t:
                acc -= nums[i]
                i += 1
            if acc == t:
                mn = min(mn, j-i+1)
        return mn+n*a if mn!=inf else -1
    
    """ 2876. 有向图访问计数 #hard n个节点, 每个节点一条出边. 对于每个节点, 求其可以访问的所有节点的数量
限制: n 1e5
思路1: 注意, 图的结构, 对于一个联通分支来说, 只能是一个环, 加上连入环的一些分支构成!
    尝试从每个节点开始 DFS, 防止重复. 
    如何得到「支链」的深度和环的大小? 可以用一个 #栈 + #哈希表 来记录! 
思路2: 形式上来说, 结构叫做 #内向基环树 
    见 [灵神](https://leetcode.cn/problems/count-visited-nodes-in-a-directed-graph/solutions/2464852/nei-xiang-ji-huan-shu-pythonjavacgo-by-e-zrzh/)
相关
*   [2127\. 参加会议的最多员工数](https://leetcode.cn/problems/maximum-employees-to-be-invited-to-a-meeting/)
*   [2359\. 找到离给定两个节点最近的节点](https://leetcode.cn/problems/find-closest-node-to-given-two-nodes/)
*   [2360\. 图中的最长环](https://leetcode.cn/problems/longest-cycle-in-a-graph/)
*   [2836\. 在传球游戏中最大化函数值](https://leetcode.cn/problems/maximize-value-of-function-in-a-ball-passing-game)
    """
    def countVisitedNodes(self, edges: List[int]) -> List[int]:
        n = len(edges)
        ans = [-1] * n
        def dfs(u):
            if ans[u] != -1: return ans[u]
            st = []
            vis = set()
            while u not in vis and ans[u] == -1:
                st.append(u)
                vis.add(u)
                u = edges[u]
            if ans[u] != -1:    # 从支链到了环
                a = ans[u]
                while st:
                    x = st.pop()
                    a += 1
                    ans[x] = a
            else:               # 找到了一个环
                sz = 0
                tmp = []
                while st:
                    x = st.pop()
                    tmp.append(x)
                    sz += 1
                    if x==u: break
                for x in tmp:
                    ans[x] = sz
                while st:
                    x = st.pop()
                    sz += 1
                    ans[x] = sz
        for i in range(n):
            dfs(i)
        return ans
    
sol = Solution()
result = [
    # sol.maximumTripletValue(nums = [12,6,1,2,7]),
    # sol.maximumTripletValue([1,2,3]),
    # sol.minSizeSubarray(nums = [1,2,3], target = 5),
    # sol.minSizeSubarray(nums = [2,4,6,8], target = 3),
    sol.countVisitedNodes(edges = [1,2,0,0]),
    sol.countVisitedNodes(edges = [1,2,3,4,0]),
    sol.countVisitedNodes(edges = [1,0,3,4,2]),
]
for r in result:
    print(r)
