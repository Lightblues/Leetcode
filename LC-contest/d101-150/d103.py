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
https://leetcode-cn.com/contest/biweekly-contest-103
https://leetcode.cn/circle/discuss/KAtdoc/
Easonsi @2023 """
class Solution:
    """ 2656. K 个元素的最大和 """
    def maximizeSum(self, nums: List[int], k: int) -> int:
        m = max(nums)
        ans = 0
        for i in range(m,m+k):
            ans += i
        return ans
    
    """ 2657. 找到两个数组的前缀公共数组 """
    def findThePrefixCommonArray(self, A: List[int], B: List[int]) -> List[int]:
        s1,s2 = set(),set()
        ans = []
        acc = 0
        for a,b in zip(A,B):
            # if a==b or a in s2 or b in s1: acc+=1
            acc += (a==b) + (a in s2) + (b in s1)
            ans.append(acc)
            s1.add(a)
            s2.add(b)
        return ans
    
    """ 2658. 网格图中鱼的最大数目 """
    def findMaxFish(self, grid: List[List[int]]) -> int:
        n,m = len(grid),len(grid[0])
        def dfs(i,j):
            if i<0 or i>=n or j<0 or j>=m or grid[i][j]==0: return 0
            # if grid[i][j] == 0: return 0
            score = grid[i][j] 
            grid[i][j] = 0
            score += dfs(i-1,j) + dfs(i+1,j) + dfs(i,j-1) + dfs(i,j+1)
            return score
        ans = 0
        for i in range(n):
            for j in range(m):
                ans = max(ans, dfs(i,j))
        return ans

    """ 2659. 将数组清空 #hard 对于所有元素不同的数组(理解成排列), 两个操作: 1] 若第一个元素是最小值, 则删除; 2] 否则将其移到最后. 问清空数组所需的次数.
限制: n 1e5
思路0: 加上index排序
    例如, 对于 5 2 4 1 3, 
        第一个删除掉的1需要循环掉 5 2 4 这些前缀; 
        2在1的前面, 需要循环掉 3 5 两个;
        3在2后面, 需要循环掉 4 一个;
        4在3后面, 需要循环掉 5 一个;
        5在4后面, 只剩下它一个元素了不需要第二个操作.
    总结: 对于排序后的元素遍历, 若当前x在x-1的后面, 则需要循环掉 [idx(x-1), idx(x)] 中间剩余的元素(更大的); 若在前面, 则需要循环掉这个区间外剩余的元素
    如何记录区间内元素是否被用掉? 想到利用 #树状数组, 有点复杂就没写, 见 灵神
思路1: 考虑更多的性质! 
    什么时候增加移动的步数? 只考虑「绕圈」的那些数字! 见灵神
[灵神](https://leetcode.cn/problems/make-array-empty/solution/shu-zhuang-shu-zu-mo-ni-pythonjavacgo-by-ygvb/)
    """
    def countOperationsToEmptyArray(self, nums: List[int]) -> int:
        ans = n = len(nums)  # 先把 n 计入答案
        t = BIT(n + 1)  # 下标从 1 开始
        pre = 1  # 上一个最小值的位置，初始为 1
        for k, i in enumerate(sorted(range(n), key=lambda i: nums[i])):
            i += 1  # 下标从 1 开始
            if i >= pre:  # 从 pre 移动到 i，跳过已经删除的数
                ans += i - pre - t.query(pre, i)
            else:  # 从 pre 移动到 n，再从 1 移动到 i，跳过已经删除的数
                ans += i - pre + n - k + t.query(i, pre - 1)
            t.inc(i)  # 删除 i
            pre = i
        return ans

    def countOperationsToEmptyArray(self, nums: List[int]) -> int:
        ans = n = len(nums)
        id = sorted(range(n), key=lambda x: nums[x])
        for k, (pre, i) in enumerate(itertools.pairwise(id), 1):
            if i < pre:  # 必须多走一整圈
                ans += n - k  # 减去前面删除的元素个数
        return ans


# 树状数组模板
class BIT:
    def __init__(self, n):
        self.tree = [0] * n
        # lowbit: i & -i

    # 将下标 i 上的数加一
    def inc(self, i: int) -> None:
        while i < len(self.tree):
            self.tree[i] += 1
            i += i & -i

    # 返回闭区间 [1, i] 的元素和
    def sum(self, i: int) -> int:
        res = 0
        while i > 0:
            res += self.tree[i]
            i &= i - 1
            # 等价于 i -= i&-i 
        return res

    # 返回闭区间 [left, right] 的元素和
    def query(self, left: int, right: int) -> int:
        return self.sum(right) - self.sum(left - 1)



sol = Solution()
result = [
    sol.findMaxFish(grid = [[0,2,1,0],[4,0,0,3],[1,0,0,4],[0,3,2,0]]),
]
for r in result:
    print(r)
