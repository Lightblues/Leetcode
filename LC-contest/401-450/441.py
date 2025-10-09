from typing import *
import collections

""" 
https://leetcode.cn/contest/weekly-contest-441
T2 循环数组, 注意写法
T3 0-1 背包, 注意问题的转换
T4 数位DP TODO:
Easonsi @2025 """
class Solution:
    """ 3487. 删除后的最大子数组元素和 删除部分元素, 使得剩余数组中, 子数组和最大 """
    def maxSum(self, nums: List[int]) -> int:
        # 注意边界情况
        s = set(nums)
        if max(s) < 0: return max(s)
        return sum(x for x in s if x>0)
    
    """ 3488. 距离最小相等元素查询 """
    def solveQueries(self, nums: List[int], queries: List[int]) -> List[int]:
        n = len(nums)
        d = collections.defaultdict(list)
        for i,x in enumerate(nums):
            d[x].append(i)
        dist = [-1] * n
        for v, idxs in d.items():
            if len(idxs) == 1: continue
            new = [idxs[0]+n-idxs[-1]] + [idxs[i+1]-idxs[i] for i in range(len(idxs)-1)] + [idxs[0]+n-idxs[-1]]
            val = [min(new[i], new[i+1]) for i in range(len(new)-1)]
            for i,v in zip(idxs, val):
                dist[i] = v
        return [dist[q] for q in queries]

    """ 3489. 零数组变换 IV #medium 给定一组查询 (l,r,val) 表示从 l...r 返回内选择下标集 -val, 问能够找到最小的k, 使得前k个操作后nums变为0数组
限制: n 10; V 1000; len(queries) 1000; val[i] 10
思路1: #0-1 背包
    由于选择的是下标记, 因此nums的每个数字要求是独立的! 答案就是所有的要求取max
    问题变为: 对于位置 i 的数字 x, 最少的前缀 k 个能覆盖的查询
        关联: 0416. 分割等和子集
    复杂度: O(nqU) 其中n为数组长度, q为查询次数, U 为max(nums)
思路2: 二分答案 + 多重背包 + 二进制优化
    -- 太复杂了...
ling: https://leetcode.cn/problems/zero-array-transformation-iv/solutions/3613907/0-1-bei-bao-pythonjavacgo-by-endlesschen-2y0l/
    """
    def minZeroArray(self, nums: List[int], queries: List[List[int]]) -> int:
        ans = 0
        for i,x in enumerate(nums):  # 遍历所有的, 取最大
            if x == 0: continue
            f = [True] + [False] * x  # 布尔数组
            for k, (l,r,v) in enumerate(queries):
                if l <= i <= r:
                    for j in range(x, v-1, -1):
                        f[j] = f[j] or f[j-v]
                if f[x]: 
                    ans = max(ans, k+1)
                    break
            else:
                return -1
        return ans

    """ 3490. 统计美丽整数的数目 #hard 问在 [l,r] 范围内, 满足 "数位之积能被之和整除" 的数字的数量
限制: n 1e9
思路: #数位DP
[ling](https://leetcode.cn/problems/count-beautiful-numbers/solutions/3613931/mo-ban-shu-wei-dp-v21pythonjavacgo-by-en-fdzz/)
    """
    def beautifulNumbers(self, l: int, r: int) -> int:
        pass

sol = Solution()
result = [
    # sol.solveQueries(nums = [1,3,1,4,1,3,2], queries = [0,3,5]),
    sol.minZeroArray(nums = [2,0,2], queries = [[0,2,1],[0,2,1],[1,1,3]]),
]
for r in result:
    print(r)
