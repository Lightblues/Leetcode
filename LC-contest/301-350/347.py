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
https://leetcode.cn/contest/weekly-contest-347
https://leetcode.cn/circle/discuss/5eR2p8/

虽然晚上了浑浑噩噩但意外地不错! 虚拟直接 36名! 不过代码非常不优雅orz
Easonsi @2023 """
class Solution:
    """ 2710. 移除字符串中的尾随零 """
    def removeTrailingZeros(self, num: str) -> str:
        return num.rstrip('0')
    
    """ 2711. 对角线上不同值的数量差 #模拟 很不优雅
[灵神](https://leetcode.cn/problems/difference-of-number-of-distinct-values-on-diagonals/solution/cong-o503-dao-o502-by-endlesscheng-5wp4/)
    """
    def differenceOfDistinctValues(self, grid: List[List[int]]) -> List[List[int]]:
        m,n = len(grid), len(grid[0])
        topLeft = [[0]*n for _ in range(m)]
        idx2set = defaultdict(set)
        for i in range(m):
            for j in range(n):
                idx = i-j
                topLeft[i][j] = len(idx2set[idx])
                idx2set[idx].add(grid[i][j])
        bottomRight = [[0]*n for _ in range(m)]
        idx2set = defaultdict(set)
        for i in range(m-1, -1, -1):
            for j in range(n-1, -1, -1):
                idx = i-j
                bottomRight[i][j] = len(idx2set[idx])
                idx2set[idx].add(grid[i][j])
        res = [[0]*n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                res[i][j] = abs(topLeft[i][j] - bottomRight[i][j])
        return res
    
    """ 2712. 使所有字符相等的最小成本 #medium 每次可以整体翻转左边/右边代价为反转的长度, 求得到全0/1的最小代价
思路1: 左右遍历
实际上可以只遍历一次 (启发)
[灵神](https://leetcode.cn/problems/minimum-cost-to-make-all-characters-equal/solution/yi-ci-bian-li-jian-ji-xie-fa-pythonjavac-aut0/)
    """
    def minimumCost(self, s: str) -> int:
        n = len(s)
        L = [0]*n
        acc = 0
        for i in range(1,n):
            if s[i]!=s[i-1]:
                acc += i
            L[i] = acc
        R = [0]*n
        acc = 0
        for i in range(n-2, -1, -1):
            if s[i]!=s[i+1]:
                acc += (n-1-i)
            R[i] = acc
        return min(L[i]+R[i] for i in range(n))
    
    """ 2713. 矩阵中严格递增的单元格数 #hard 每次可以移动到同行/列的严格大的格子, 问递增序列最大长度 
思路1: 排序, 代码太冗长了
    从小到大排序, 尝试得到每一个位置作为结尾的最大长度!
    如何得到? 记录每行/列的最大长度! 
    注意的是, 例如全1的grid, 需要注意严格递增的条件! 为此, 每行/列的记录值需要保留最大的两个值!
思路1.1: 同时处理相同数值的位置!
    对于相同的数字在同一个for中处理! 这样只需要记录比val小的元素的最大长度即可!
    见 [灵神](https://leetcode.cn/problems/maximum-strictly-increasing-cells-in-a-matrix/solution/dong-tai-gui-hua-you-hua-pythonjavacgo-b-axv0/)
    """
    def maxIncreasingCells(self, mat: List[List[int]]) -> int:
        m,n = len(mat), len(mat[0])
        s = []
        for i,j in product(range(m), range(n)):
            s.append((mat[i][j], i, j))
        s.sort()
        # 记录每行中, (val, maxLen) 对, 最多保留的数量为2
        # 注意到, 因为是排序后的, 若 vb>va, 则 maxb>maxa
        rowC = [[]for _ in range(m)]
        colC = [[]for _ in range(n)]
        ans = 1
        for v,i,j in s:
            # 求最大长度
            a = 1
            for ss in [rowC[i], colC[j]]:   # 统一处理行列
                if ss:
                    if ss[0][0]<v: a = max(a, ss[0][1]+1)
                    if ss[0][0]==v and len(ss)>1: a = max(a, ss[1][1]+1)
            ans = max(ans, a)
            # 
            for ss in [rowC[i], colC[j]]:
                if len(ss)==0:
                    ss.append([v, a])
                else:
                    if ss[0][0]==v:
                        ss[0][1] = max(ss[0][1], a)
                    else:
                        ss[:] = [[v, a], ss[0]]
        return ans



sol = Solution()
result = [
    # sol.differenceOfDistinctValues(grid = [[1,2,3],[3,1,5],[3,2,1]]),
    # sol.differenceOfDistinctValues([[1]]),
    # sol.minimumCost(s = "0011"),
    # sol.minimumCost(s = "010101"),
    sol.maxIncreasingCells(mat = [[3,1],[3,4]]),
    sol.maxIncreasingCells(mat = [[1,1],[1,1]]),
    sol.maxIncreasingCells(mat = [[3,1,6],[-9,5,7]]),
]
for r in result:
    print(r)
