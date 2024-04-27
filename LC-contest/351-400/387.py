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
https://leetcode.cn/contest/weekly-contest-387
对于Python比较简单的一场
Easonsi @2023 """
class Solution:
    """ 3069. 将元素分配到两个数组中 I """
    
    """ 3070. 元素和小于等于 k 的子矩阵的数目 """
    def countSubmatrices(self, grid: List[List[int]], k: int) -> int:
        m,n = len(grid),len(grid[0])
        ans = 0
        acc = [0] * n
        for i,row in enumerate(grid):
            acc_row = 0
            for j,x in enumerate(row):
                acc_row += x
                acc[j] = acc[j] + acc_row
                if acc[j] <= k: ans += 1
        return ans
    
    """ 3071. 在矩阵上写出字母 Y 所需的最少操作次数 """
    def minimumOperationsToWriteY(self, grid: List[List[int]]) -> int:
        cnt = Counter(itertools.chain(*grid))
        cnt_y = Counter()
        n = len(grid)
        c = n // 2
        for i in range(c):
            cnt_y[grid[i][i]] += 1
            cnt_y[grid[i][n-i-1]] += 1
        for i in range(c,n):
            cnt_y[grid[i][c]] += 1
        cnt_others = cnt - cnt_y
        ans = n**2
        for y in [0,1,2]:
            for o in [0,1,2]:
                if o==y: continue
                candidate = sum(cnt_y.values()) - cnt_y[y] + sum(cnt_others.values()) - cnt_others[o]
                ans = min(ans, candidate)
        return ans
    
    """ 3072. 将元素分配到两个数组中 II 对于一个数组, 先按照下面的规则分为 arr1, arr2 然后拼接输出
初始化 arr1, arr2 = [nums[0]], [nums[1], 然后对于 i=2...n-1, 根据 greaterCount(arr1, nums[i]) > greaterCount(arr2, nums[i]) 的大小关系, 加到更大的数组上, 相等的话加到元素数量较少的数组中
限制: n 1e5
思路0: 暴力用 SortedList 来模拟
思路1: 离散化 + #树状数组
    离散化之后, 需要有一个「统计比x小的数字出现的次数」 —— 可以用 树状数组!
    注意, 除了用两个树状数组, 还可以简化到一个
见 [ling](https://leetcode.cn/problems/distribute-elements-into-two-arrays-ii/solutions/2664646/chi-san-hua-shu-zhuang-shu-zu-pythonjava-3bb2/)

307. 区域和检索 - 数组可修改 *模板题
315. 计算右侧小于当前元素的个数 *逆序对
2426. 满足不等式的数对数目 2030
493. 翻转对
327. 区间和的个数
    """
    def resultArray(self, nums: List[int]) -> List[int]:
        from sortedcontainers import SortedList
        arr1, arr2 = [nums[0]], [nums[1]]
        sarr1, sarr2 = SortedList(arr1), SortedList(arr2)
        for i in range(2, len(nums)):
            x = nums[i]
            c1 = len(arr1) - sarr1.bisect_right(x)
            c2 = len(arr2) - sarr2.bisect_right(x)
            if c1 > c2 or (c1==c2 and len(arr1)<=len(arr2)): 
                arr1.append(x)
                sarr1.add(x)
            else: 
                arr2.append(x)
                sarr2.add(x)
        return arr1 + arr2
    
sol = Solution()
result = [
    # sol.countSubmatrices(grid = [[7,2,9],[1,5,0],[2,6,6]], k = 20),
    # sol.minimumOperationsToWriteY(grid = [[0,1,0,1,0],[2,1,0,1,2],[2,2,2,0,1],[2,2,2,2,2],[2,1,2,2,2]]),
    sol.resultArray(nums = [5,14,3,1,2]),
]
for r in result:
    print(r)
