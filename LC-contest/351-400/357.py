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
https://leetcode.cn/contest/weekly-contest-357
https://leetcode.cn/circle/discuss/chtVBq/
Easonsi @2023 """
class Solution:
    """ 2810. 故障键盘 #easy 遇到每一个字符i, 会将前面的字符串翻转, 问最后的字符串 
思路0: 模拟 复杂度 O(n^2)
思路1: #双端队列 复杂度 O(n)
"""
    def finalString(self, s: str) -> str:
        ans = ""
        for i,x in enumerate(s):
            if x=='i':
                ans = ans[::-1]
            else: ans += x
        return ans
    
    
    """ 2811. 判断是否能拆分数组 #medium 对于一个长n的数组 和一个目标值m, 每次可以进行拆分操作, 要求满足 1] 或者长度为1, 2] 或者只和>=m, 问能够拆分成n个子数组 (也就是都拆开)
限制; n 100; m 200
思路1: #贪心
    注意, 若要分割成n部分, 那最后完成分割的一定是一个和 >=m 的长度为2的数组! 

=== 下面没有理解题目
思路0: #DP, 好像不太行
    记 f[i] 表示前i个元素可以划分的最大数量, 则有递推: 
        最后一个单独加进去 f[i-1]+1, 注意要求 f[i-1] > 0
        找到最右边的j, 满足 sum{arr[j:i]}>=m, 则 f[i] = f[j-1]+1
思路1: #贪心 最后一定剩下一个大于m的子数组.
    问题等价于, 找到最短的 >=m 的子数组
"""
    def canSplitArray(self, nums: List[int], m: int) -> bool:
        if len(nums)<=2: return True
        l = 0
        acc = 0
        mn = inf
        for r,x in enumerate(nums):
            acc += x
            while acc>=m:
                acc -= nums[l]
                mn = min(mn, r-l+1)
                l += 1
        return mn <= 2
        
    """ 2812. 找出最安全路径 #medium 矩阵中存在若干小偷的格点,要求从左上到右下的路径中, 最远离的小偷距离 (安全系数定义为曼哈顿距离) 
限制: n 400
思路1: 先用多源BFS计算每个点的「安全系数」, 然后左右队列求路径
    """
    def maximumSafenessFactor(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        q = deque()
        for i,row in enumerate(grid):
            for j,x in enumerate(row):
                if x==1: q.append((i,j,1))  # 直接用1以上的数字标记距离 (bias=1) 这样就不用另外开visit了
        while q:
            i,j,d = q.popleft()
            for di,dj in [(0,1),(0,-1),(1,0),(-1,0)]:
                ni,nj = i+di,j+dj
                if 0<=ni<m and 0<=nj<n and grid[ni][nj]==0:
                    grid[ni][nj] = d+1
                    q.append((ni,nj,d+1))
        ans = grid[0][0]
        # q = deque([(0,0,ans)])
        q = [(-ans,0,0)]
        grid[0][0] = -1
        while q:
            d,i,j = heappop(q)
            ans = min(ans, -d)
            if i==m-1 and j==n-1: 
                return ans-1
            for di,dj in [(0,1),(0,-1),(1,0),(-1,0)]:
                ni,nj = i+di,j+dj
                if 0<=ni<m and 0<=nj<n and grid[ni][nj]>0:
                    nd = grid[ni][nj]
                    heappush(q, (-nd,ni,nj))
                    grid[ni][nj] = -1
    
    """ 2813. 子序列最大优雅度 #hard 有一组物品 (profit, category) , 对于一个长k的子序列, 定义其分数为 total_profit + distinct_categories^2 求最大值
限制: n 1e5
思路1: #贪心反悔 #贪心 先贪心选择最大的k个数字, 对于后面的数字, 若类别不同的话, 用其替换已选中数值最小的重复类的物品
    为此, 对于重复类别的物品可以用一个 #栈 来记录其 profit
见 [灵神](https://leetcode.cn/problems/maximum-elegance-of-a-k-length-subsequence/solutions/2375128/fan-hui-tan-xin-pythonjavacgo-by-endless-v2w1/)
    """
    def findMaximumElegance(self, items: List[List[int]], k: int) -> int:
        items.sort(key=lambda x: -x[0])
        total_profit = 0
        used_categories = set()
        st = []
        for p,c in items[:k]:
            total_profit += p
            if c not in used_categories:
                used_categories.add(c)
            else:
                st.append(p)
        ans = total_profit + len(used_categories)**2
        for p,c in items[k:]:
            if c not in used_categories:
                if not st: break        # 注意边界!
                total_profit += p - st.pop()
                used_categories.add(c)
                ans = max(ans, total_profit + len(used_categories)**2)
        return ans
        
sol = Solution()
result = [
    # sol.canSplitArray(nums = [2, 2, 1], m = 4),
    # sol.maximumSafenessFactor(grid = [[0,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,0]]),
    
    sol.findMaximumElegance(items = [[3,2],[5,1],[10,1]], k = 2),
    sol.findMaximumElegance(items = [[3,1],[3,1],[2,2],[5,3]], k = 3),
]
for r in result:
    print(r)
