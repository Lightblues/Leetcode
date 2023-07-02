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
https://leetcode-cn.com/contest/biweekly-contest-106
https://leetcode.cn/circle/discuss/9UKZwR/

T4需要进行猜想简化, 有点意思

Easonsi @2023 """
class Solution:
    """ 2729. 判断一个数是否迷人 """
    def isFascinating(self, n: int) -> bool:
        s = str(n) + str(2*n) + str(3*n)
        if len(s)==9 and len(set(s))==9 and '0' not in s: return True
        return False
    
    """ 2730. 找到最长的半重复子字符串 #双指针
 """
    def longestSemiRepetitiveSubstring(self, s: str) -> int:
        if len(s)<=2: return len(s)
        n = len(s)
        cnt = 0; ans = 0;
        l = 0
        for r in range(1,n):
            if s[r]==s[r-1]:
                cnt += 1
                while cnt>1:
                    if s[l]==s[l+1]: cnt -= 1
                    l += 1
            ans = max(ans, r-l+1)
        return ans
    
    """ 2731. 移动机器人 #medium """
    def sumDistance(self, nums: List[int], s: str, d: int) -> int:
        mod = 10**9+7
        fi = []
        for x,dir in zip(nums, s):
            if dir=='L': fi.append(x-d)
            else: fi.append(x+d)
        fi.sort()
        ans = 0; acc=0
        for i in range(1, len(fi)):
            acc = (acc + (fi[i]-fi[i-1]) * i) % mod
            ans = (ans+acc) % mod
        return ans
    
    """ 2732. 找到矩阵中的好子集 #hard 对于一个m*n 的0/1矩阵, 选取其行集合s (大小为k), 使得这些行构成的矩阵中, 列和都满足 <=k//2
要求找到一个子集s. 限制: m 1e4; n 5
思路0: 最多考虑两行!
    考虑若有一个解选了3行, 说明每一列中最多只有一行为1其他都是0; 这样, 可以得到一个大小为2行的解!
    这样的话, 问题简化为两种情况!
    进一步, 对于 (i,j) 组合的问题? 注意到这里限制 n<=5, 所以可以不考虑重复行, 枚举所有的列组合!
分析见 [灵神](https://leetcode.cn/problems/find-a-good-subset-of-the-matrix/solution/xiang-xi-fen-xi-wei-shi-yao-zhi-duo-kao-mbl6a/)
     """
    def goodSubsetofBinaryMatrix(self, grid: List[List[int]]) -> List[int]:
        m,n = len(grid), len(grid[0])
        v2idx = dict()
        for i,row in enumerate(grid):
            v = 0
            for j in range(n):
                v = v*2 + row[j]
            if v==0: return [i]
            if v not in v2idx: v2idx[v] = i
        for v1,idx1 in v2idx.items():
            for v2,idx2 in v2idx.items():
                if idx1!=idx2 and v1&v2==0: return [idx1,idx2]
        return []






    
sol = Solution()
result = [
    # sol.longestSemiRepetitiveSubstring("52233"),
    # sol.longestSemiRepetitiveSubstring("1111"),
    # sol.sumDistance(nums = [-2,0,2], s = "RLL", d = 3),
    # sol.sumDistance(nums = [1,0], s = "RL", d = 2),
    sol.goodSubsetofBinaryMatrix(grid = [[0,1,1,0],[0,0,0,1],[1,1,1,1]]),
    sol.goodSubsetofBinaryMatrix([[0]]),
    sol.goodSubsetofBinaryMatrix(grid = [[1,1,1],[1,1,1]]),
]
for r in result:
    print(r)
