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
https://leetcode.cn/contest/weekly-contest-224
这次的难度好高! 猫和老鼠只有22个人[做出来](https://leetcode.cn/contest/weekly-contest-224/ranking/). T3也很有意思, 关联两道相关题.

@2022 """
class Solution:
    """ 1725. 可以形成最大正方形的矩形数目 """
    def countGoodRectangles(self, rectangles: List[List[int]]) -> int:
        rs = [min(a) for a in rectangles]
        return Counter(rs)[max(rs)]
    
    """ 1726. 同积元组 """
    def tupleSameProduct(self, nums: List[int]) -> int:
        n = len(nums)
        cnt = Counter()
        for i in range(n):
            for j in range(i+1,n):
                cnt[nums[i]*nums[j]] += 1
        ans = 0
        for _,v in cnt.items():
            ans += v*(v-1)//2
        return ans * 8
    
    """ 1727. 重新排列后的最大子矩阵 #medium #题型
有一个0/1矩阵, 可以对于列进行重排列. 问可能得到的全为1的最大矩阵的大小. 见[图](https://leetcode.cn/problems/largest-submatrix-with-rearrangements/)
限制: 矩阵面积 1e5
提示: 这里每一列不变, 可以参考0085进行预处理: 对于某列的i位置, 计算「以其结尾的连续1的长度」.
思路1: #预处理 之后, 排序统计
    相较于0085, 这里可以对列进行重排列. 因此, 对于每一个行指标i, 我们可以对预处理的结果进行排序. 自然得到最大的合法矩阵.
关联: 0085. 最大矩形 #hard
"""
    def largestSubmatrix(self, matrix: List[List[int]]) -> int:
        m,n = len(matrix), len(matrix[0])
        # 计算 m[i,j] 为底其往上有多少连续1. 
        for i in range(1, m):
            for j in range(n):
                if matrix[i][j] == 1:
                    matrix[i][j] = matrix[i-1][j] + 1
        ans = 0
        # 枚举列重排之后可能达到的最大矩形. 
        for i in range(m):
            heights = sorted(matrix[i], reverse=True)
            for i,h in enumerate(heights):
                ans = max(ans, h*(i+1))
        return ans
    
    """ 1728. 猫和老鼠 II 见博弈论 """
    
    
sol = Solution()
result = [

    sol.largestSubmatrix(matrix = [[0,0,1],[1,1,1],[1,0,1]]),
]
for r in result:
    print(r)
