from easonsi import utils
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
https://leetcode.cn/contest/weekly-contest-196
T2有噱头, 需要想到转化情况; T3和T4 都是非常经典的题型, 需要较高的思维量.


@2022 """
class Solution:
    """ 1502. 判断能否形成等差数列 """
    def numSubmat(self, mat: List[List[int]]) -> int:
        n, m = len(mat), len(mat[0])
        
        row = [[0] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if j == 0:
                    row[i][j] = mat[i][j]
                else:
                    row[i][j] = 0 if mat[i][j] == 0 else row[i][j - 1] + 1
    """ 1503. 所有蚂蚁掉下来前的最后一刻 #medium #脑筋急转弯
有一根长n的木板, 上面有一组蚂蚁, 向左或向右移动, 到两侧会掉下木板, 左右相遇则调转方向. 问经过多少时间所有蚂蚁都掉下来? 限制: 数量 n 1e4
提示: 两蚂蚁相遇, 虽然改变了方向, 但因为速度是一样的, 所以可以理解为相遇了没有任何影响.
"""
    def getLastMoment(self, n: int, left: List[int], right: List[int]) -> int:
        left.append(0); right.append(n)
        return max(
            max(left), n-min(right)
        )
    
    """ 1504. 统计全 1 子矩形 #medium #题型 #star
给定一个01矩阵, 统计其所有子矩阵中, 全1矩阵的数量. 限制: 长宽 n 150
思路1: #枚举 利用部分前缀和来加速.
    考虑以 (i,j) 为右下角的子矩阵数量. 若直接枚举左上角, 则复杂度过高.
    注意到, 对于 (h,w) 的矩阵, 其每一行全1的长度至少要w个, 因此, 可以从第i行往上依次检查可以构成多宽的
    复杂度: O(nm^2)
思路2: #单调栈
    在思路1中, 向上可以构成的矩形宽度呈现递减趋势, 而我们需要每次进行递归吗?
    答案是没必要, 用单调栈进行优化. 结论: 这里存储的是单调信息是递减的矩形宽度, 但为了统计数量, 我们还需要高度信息, 因此单调栈存储的单元为 `(宽, 高)`.
    具体而言, 维护一个递增栈. 在考虑当前行时, 假如底边宽为 wi, 而栈顶的最大矩形为 (w,h), 若 w>wi, 则上面更宽的部分没有作用了, 直接弹出; 这部分和底边可以匹配的高度累计为 h+1.
    细节: 如何统计数量? **记录栈内矩形总面积**.
[官答](https://leetcode.cn/problems/count-submatrices-with-all-ones/solution/tong-ji-quan-1-zi-ju-xing-by-leetcode-solution/)
"""
    def numSubmat(self, mat: List[List[int]]) -> int:
        # 思路1, 枚举
        n, m = len(mat), len(mat[0])
        # row[i][j] 第i行中, 以第j结尾的连续1向量的长度.
        row = [[0] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if j == 0:
                    row[i][j] = mat[i][j]
                else:
                    row[i][j] = 0 if mat[i][j] == 0 else row[i][j - 1] + 1
        
        ans = 0
        for i in range(n):
            for j in range(m):
                # 从下往上统计高为 k-j 的矩阵的数量.
                col = row[i][j]
                for k in range(i, -1, -1):
                    col = min(col, row[k][j])
                    if col == 0:        # 无法构成矩阵了
                        break
                    ans += col
        return ans
    def numSubmat(self, mat: List[List[int]]) -> int:
        # 思路2: #单调栈
        n, m = len(mat), len(mat[0])
        # row[i][j] 第i行中, 以第j结尾的连续1向量的长度.
        row = [[0] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                if j == 0:
                    row[i][j] = mat[i][j]
                else:
                    row[i][j] = 0 if mat[i][j] == 0 else row[i][j - 1] + 1
        ans = 0
        for j in range(m):
            stack = []      # 单调栈
            totalS = 0      # 栈内矩形总面积
            for i in range(n):
                hi = 1; wi = row[i][j]
                totalS += wi
                # if wi==0: 
                #     stack = []
                #     continue
                while stack and stack[-1][0] >= wi:
                    w,h = stack.pop()
                    hi += h
                    totalS -= (w-wi) * h
                ans += totalS
                stack.append((wi, hi))
        return ans
    
    """ 1505. 最多 K 次交换相邻数位后得到的最小整数 #hard #题型 #star
给定一个字符串形式的整数, 每次可以交换两个相邻位, 问k步操作之内最多可以得到最小的数字. 限制: 数字长度 3e5
提示: 从高到低选择最小的数字, 可以贪心选择最近的还没被用到的数字
思路1: #贪心 #树状数字
    按照提示的方式贪心选择第1,2,...位, 每次从k次操作范围内选择最近的最小数字, 将其移动到最前面. (注意, 这样的操作次数是最优的)
    问题是, 经过前置操作后, 原本的位置发生了变化, 如何计算新的位置? 假设结果数字前i的位用到的数字在原本字符串中的位置是 [a1,a2,...ai], 而此次选择前置的数字的原本位置是idx, 它在经过之前操作后的位置在 `newidx = idx + sum(ai>idx)` 也即在idx之后前置的元素对于其位置发生了影响; 它需要被移动到 i+1 位, 消耗操作 `newidx - (i+1)` 次.
        需要的操作: **单点修改, 区间查询**, 可以通过 #树状数组 来实现.
    如何快速找到最近的最小数字? 我们对于0..9的位置进行索引, 用掉就pop, 每次从0到9查询是否还有剩余.
具体见 [官答](https://leetcode.cn/problems/minimum-possible-integer-after-at-most-k-adjacent-swaps-on-digits/solution/zui-duo-k-ci-jiao-huan-xiang-lin-shu-wei-hou-de-da/)
"""
    def minInteger(self, num: str, k: int) -> str:
        n = len(num)
        pos = [list() for _ in range(10)]
        for i in range(n - 1, -1, -1):
            pos[ord(num[i]) - ord('0')].append(i + 1)
        
        ans = ""
        bit = BIT(n)
        for i in range(1, n + 1):
            for j in range(10):
                if pos[j]:
                    # 当前检查元素的原本位置为 pos[j][-1], 检查其后有多少数字已经用掉了 (该元素现在的位置变成了 pos[j][-1]+behind)
                    behind = bit.queryRange(pos[j][-1] + 1, n)
                    dist = pos[j][-1] + behind - i
                    if dist <= k:
                        bit.update(pos[j][-1])  # 标记原本在 pos[j][-1] 位置的元素被用了
                        pos[j].pop()
                        ans += str(j)
                        k -= dist
                        break
        return ans

class BIT:
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)
    
    @staticmethod
    def lowbit(x: int) -> int:
        return x & (-x)
    
    def update(self, x: int):
        # 对于x位置 +1
        while x <= self.n:
            self.tree[x] += 1
            x += BIT.lowbit(x)
    
    def query(self, x: int) -> int:
        # 查询 1...x 的区间和
        ans = 0
        while x > 0:
            ans += self.tree[x]
            x -= BIT.lowbit(x)
        return ans

    def queryRange(self, x: int, y: int) -> int:
        # 查询 [x...y] 范围内的和
        return self.query(y) - self.query(x - 1)


    

    
sol = Solution()
result = [
    sol.numSubmat(mat = [[1,0,1],[1,1,0],[1,1,0]]),
    sol.numSubmat([[0,1,1,0],[0,1,1,1],[1,1,1,0]]),
]
for r in result:
    print(r)
