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
== 矩形系列
0084. 柱状图中最大的矩形 #hard #题型 给定一组数表示一系列柱子的高度, 求其中包含的最大矩形的面积
    单调栈, 得到每个柱子作为高的左右边界
0085. 最大矩形 #hard #题型 #interest 给定一个0/1矩阵, 问其中全1构成的最大矩形的面积.
    计算行前缀, 对于每一列转化为 0084
1504. 统计全 1 子矩形 #medium #题型 给定一个01矩阵, 统计其所有子矩阵中, 全1矩阵的数量.
    通过 (w,h) 的形式存储宽度递减矩阵, 并用一个acc变量记录所有矩阵总面积

Easonsi @2023 """
class Solution:
    """ 0084. 柱状图中最大的矩形 #hard #题型 给定一组数表示一系列柱子的高度, 求其中包含的最大矩形的面积. 限制: 数组长度 n 1e5
思路0: 分别从左、从右扫一遍, 用单调栈来得到以i作为高可以到达的边界
思路1: 实际上, 可以只用一个单调栈
    采用 #单调栈 来保留每一个柱子作为最大高度可以构成的矩形的底边长度.
    具体而言, 维护一个单调递增栈, 当栈顶元素被pop出来时, 说明 (stack[-2], i) 范围内的柱子都大于栈顶元素的高度, 可以构成面积 `stack[-1] * (i - stack[-2] - 1)` 的矩形.
    见 [官答](https://leetcode.cn/problems/largest-rectangle-in-histogram/solution/zhu-zhuang-tu-zhong-zui-da-de-ju-xing-by-leetcode-/)
"""
    def largestRectangleArea(self, heights: List[int]) -> int:
        # 思路1, from  Copilet.
        n = len(heights)
        stack = []  # 维护递增栈
        ans = 0
        for i in range(n):
            while stack and heights[i] < heights[stack[-1]]:
                # stack[-1] 可以在 (stack[-2], i) 范围内作为矩形高度
                h = heights[stack.pop()]
                w = i if not stack else i - stack[-1] - 1
                ans = max(ans, h*w)
            stack.append(i)
        while stack:
            h = heights[stack.pop()]
            w = n if not stack else n - stack[-1] - 1
            ans = max(ans, h*w)
        return ans


    """ 0085. 最大矩形 #hard #题型 #interest 给定一个0/1矩阵, 问其中全1构成的最大矩形的面积. 限制: 长宽 200 [图](https://leetcode.cn/problems/maximal-rectangle/)
提示: 先进行预处理, 对于每一个位置, 记录 **该行中以它结尾的连续1的长度** (0位置对应的数量就是0). 这样, 对于每一列, 就转换成 0084 题.
思路1: 按照上述思路将其转为 0084
    说明: 如何想到等价转换? 按照官答的思路, 我们枚举以 (i,j) 点作为右下角的所有矩阵, 这样判断的方式就可以通过上述预处理机制来实现. 从而得到等价转换.
    见 [官答](https://leetcode.cn/problems/maximal-rectangle/solution/zui-da-ju-xing-by-leetcode-solution-bjlu/)
"""
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        m,n = len(matrix), len(matrix[0])
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == '1':
                    matrix[i][j] = 1 if j==0 else matrix[i][j-1] + 1
                else:
                    matrix[i][j] = 0
        ans = 0
        for j in range(n):
            ans = max(self.largestRectangleArea([matrix[i][j] for i in range(m)]), ans)
        return ans
    
    """ 1504. 统计全 1 子矩形 #medium #题型 给定一个01矩阵, 统计其所有子矩阵中, 全1矩阵的数量. 限制: 长宽 n 150
思路1: #枚举 利用部分前缀和来加速.
    考虑以 (i,j) 为右下角的子矩阵数量. 
    注意到, 对于 (h,w) 的矩阵, 其每一行全1的长度至少要w个, 因此, 可以从第i行往上依次检查可以构成多宽的
    复杂度: O(nm^2)
思路2: #单调栈
    在思路1中, 向上可以构成的矩形宽度呈现递减趋势, 而我们需要每次进行递归吗?
    答案是没必要, 用单调栈进行优化. 结论: 这里存储的是单调信息是递减的矩形宽度, 但为了统计数量, 我们还需要高度信息, 因此单调栈存储的单元为 `(宽, 高)`.
    具体而言, 维护一个递增栈. 在考虑当前行时, 假如底边宽为 wi, 而栈顶的最大矩形为 (w,h), 若 w>wi, 则上面更宽的部分没有作用了, 直接弹出; 这部分和底边可以匹配的高度累计为 h+1.
    细节: 如何统计数量? **记录栈内矩形总面积**.
    复杂度: O(nm)
[官答](https://leetcode.cn/problems/count-submatrices-with-all-ones/solution/tong-ji-quan-1-zi-ju-xing-by-leetcode-solution/)
"""
    def numSubmat(self, mat: List[List[int]]) -> int:
        m,n = len(mat),len(mat[0])
        # 计算前缀长度
        for j in range(1,n):
            for i in range(m):
                if mat[i][j]:
                    mat[i][j] += mat[i][j-1]
        # 
        ans = 0
        for j in range(n):
            q = []
            acc = 0
            for i in range(m):
                h = 1
                w = mat[i][j]
                while q and q[-1][0] > w:
                    wOld, hOld = q.pop()
                    acc -= wOld * hOld
                    h += hOld
                q.append((w,h))
                acc += w * h
                ans += acc
        return ans

    
sol = Solution()
result = [
    # sol.largestRectangleArea([2,1,5,6,2,3]),
    # sol.largestRectangleArea([2,4]),
    # sol.maximalRectangle(matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]),
    sol.numSubmat(mat = [[1,0,1],[1,1,0],[1,1,0]]),
    sol.numSubmat([[0,1,1,0],[0,1,1,1],[1,1,1,0]]),
]
for r in result:
    print(r)
