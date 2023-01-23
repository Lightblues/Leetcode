from easonsi import utils
from easonsi.util.leetcode import *
""" 
https://leetcode.cn/contest/weekly-contest-295


@2022 """
class Solution:
    """ 6078. 重排字符形成目标字符串 """
    def rearrangeCharacters(self, s: str, target: str) -> int:
        cntS = Counter(s)
        cntT = Counter(target)
        ans = len(s)
        for k,v in cntT.items():
            ans = min(ans, cntS[k]//v)
        return ans
    
    """ 6079. 价格减免 """
    def discountPrices(self, sentence: str, discount: int) -> str:
        ans = []
        for word in sentence.split():
            if not (word[0]=='$' and str.isdigit(word[1:])):
                ans.append(word)
                continue
            price = int(word[1:]) * (1-discount/100)
            ans.append(f"${price:.2f}")
        return " ".join(ans)
    
    """ 6080. 使数组按非递减顺序排列 #medium #题型
给定一个数组经过若干次删除操作将其变为非递减数组. 每次操作定义为: 删除满足 `nums[i - 1] > nums[i]` 的位置的元素 i. 问经过多少次操作后得到最终结果 (非递减).
尝试0: 一开始想到, 通过一次遍历可以得到最终保留的子序列. 这样只需要计算这些idx所分割的每一个连续序列中, 需要进行的操作次数即可. 
    然而, 对于如何计算按照的删除方式「删除序列中的每一个元素」, 还是没想出来. 一开始想记录每一个递增序列的长度, 但是还需要考虑到 [1,2,3,1,2,3] 中, 第二个3 这样的情况.
思路1: 单调栈
    [here](https://leetcode.cn/problems/steps-to-make-array-non-decreasing/solution/by-endlesscheng-s2yc/)
    对于每一个元素 i, (若会被删除), 其删除时间由什么决定? 由 `nums[i - 1] > nums[i]` 这一公式决定. 也即其左侧的第一个比它大的元素, 记为 j.
    如何记录 j 的删除时间? 可以通过一个(严格)单调递减栈来解决.
    具体而言, 栈内记录 `(num, delete_time)`, 后者为它被移除的时刻. 对于每一个元素, 移除所有满足 `stack[-1][0] <= num` 的栈顶元素 (注意是小于等于).
        相等的时候, 1) 若num被保留, 下面的 `if stack` 语句确保了其移除时间的记录为 0; 2) num被移除, 则其被移除的时刻同样取决于上一个值为 num的元素. 例如 [3,1,2,1,2] 中两个2的移除时刻分别为 2,3.
    若经过pop操作后栈空, 说明该元素会被保留到最后, 其 `delete_time` 为 0. 否则, 为出栈元素中  `delete_time` 最大值 +1. 也即, `if stack: maxt += 1`
    """
    def totalSteps(self, nums: List[int]) -> int:
        """ [here](https://leetcode.cn/problems/steps-to-make-array-non-decreasing/solution/by-endlesscheng-s2yc/)
        """
        # 栈内元素为 (num, maxt) 其中第二个数字是它被移除的时刻
        stack = []
        ans = 0
        for num in nums:
            maxt = 0    # 记录num左侧的元素的小于等于num的元素的最大移除时间
            # 注意这里是 <=. 相等的时候, 1) 若num被保留, 下面的 `if stack` 语句确保了其移除时间的记录为 0; 2) num被移除, 则其被移除的时刻同样取决于上一个值为 num的元素. 例如 [3,1,2,1,2] 中两个2的移除时刻分别为 2,3.
            while stack and stack[-1][0] <= num:
                maxt = max(maxt, stack.pop()[1])
            # 若栈为空, 说明是新的最大元素, 其被移除的时刻为 0; 否则, 该元素会被移除, 其被移除的时刻为 maxt+1.
            if stack: maxt += 1
            ans = max(ans, maxt)
            stack.append((num, maxt))
        return ans
    
    """ 2290. 到达角落需要移除障碍物的最小数目 #hard #题型 #BFS
从gird的左上走到右下, 要求最小代价. grid中的每个元素为0/1, 其中1表示有障碍物, 移除的代价为1.
思路: #BFS 其实是最短路径的变形问题
    实际上, 这里所有相连的空白位置都可以看作是(距离图上的)一个点, 每一个障碍物一个点; 这样, 可以构建我们常见的距离图, 并且可以用BFS来求解.
    具体实现上, 由于距离图上的一个节点对应了grid上的多个点, 因此可以用优先队列 (dist, (x, y)) 来规划BFS
思路2: 其实是 [01BFS]
"""
    def minimumObstacles(self, grid: List[List[int]]) -> int:
        m,n = len(grid), len(grid[0])
        checkValid = lambda i,j: 0<=i<m and 0<=j<n
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        
        visited = set([(0,0)])
        q = [(0, (0,0))]
        while q:
            dis, (i,j) = heapq.heappop(q)
            for di,dj in directions:
                ni,nj = i+di, j+dj
                if (ni,nj)==(m-1,n-1):
                    return dis
                if checkValid(ni,nj) and (ni,nj) not in visited:
                    if grid[ni][nj] == 0:
                        heapq.heappush(q, (dis, (ni,nj)))
                    elif grid[ni][nj] == 1:
                        heapq.heappush(q, (dis+1, (ni,nj)))
                    visited.add((ni,nj))
        return -1

sol = Solution()
result = [
    # sol.rearrangeCharacters(s = "abbaccaddaeea", target = "aaaaa"),
    # sol.discountPrices(sentence = "there are $1 $2 and 5$ candies in the shop", discount = 50),
    # sol.discountPrices(sentence = "1 2 $3 4 $5 $6 7 8$ $9 $10$", discount = 100),
    
    sol.totalSteps(nums = [5,3,4,4,7,3,6,11,8,5,11]),
    sol.totalSteps(nums = [4,5,7,7,13]),
    sol.totalSteps([10,1,2,3,4,5,6,1,2,3,6]),
    sol.totalSteps([1682, 63,124,147,897,1210,1585, 1744,1764,1945, 323,984,1886, 346,481,1059,1388,1483,1516,1842,1868,1877 ,504,1197,785,955,970,1848,1851, 398,907,995,1167,1214,1423,1452,1464,1474, 1311,1427,1757, 1992, 57,1625,1260,700,725]),
    
    # sol.minimumObstacles(grid = [[0,1,1],[1,1,0],[1,1,0]]),
    # sol.minimumObstacles(grid = [[0,1,0,0,0],[0,1,0,1,0],[0,0,0,1,0]]),
    
]
for r in result:
    print(r)
