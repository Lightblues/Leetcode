from easonsi import utils
from easonsi.util.leetcode import *
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
        
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
https://leetcode.cn/contest/weekly-contest-199
@2022 """
class Solution:

    """ 1528. 重新排列字符串 """
    def restoreString(self, s: str, indices: List[int]) -> str:
        n = len(s)
        ans = ['a'] * n
        for i,idx in enumerate(indices):
            ans[idx] = s[i]
        return ''.join(ans)
    """ 1529. 最少的后缀翻转次数 """
    def minFlips(self, target: str) -> int:
        target.lstrip('0')
        last = '0'; ans = 0
        for ch in target:
            if ch!=last:
                ans += 1
            last = ch
        return ans
    


    """ 1530. 好叶子节点对的数量 #medium #边界 #题型
给定一棵二叉树, 问所有叶子结点对中, 距离小于等于一定阈值的组有多少个. 限制: 节点数量 2^10, 距离限制 100
思路1: 采用 #DFS, 对与每一个节点, 匹配左右孩子分别包含的叶子节点的深度.
    注意: 特殊情况是, 如何判断当前传入的节点是叶子?
"""
    def countPairs(self, root: TreeNode, distance: int) -> int:
        if distance==1: return 0
        ans = 0
        def f(root:TreeNode):
            # 返回: 深度在 0...distance 之间的点的数量 (针对root的父亲节点)
            nonlocal ans
            ret = [0] * distance
            # 边界1: 传入的root为空
            if root is None: return ret
            # 边界2: 传入的root为叶子结点
            if root.left is None and root.right is None:
                ret[1] += 1; return ret
            ld = f(root.left); rd = f(root.right)
            # 匹配左右子树
            for i in range(1, distance):
                for j in range(1, distance-i+1):
                    ans += ld[i]*rd[j]
            # 计算root下的叶子数量.
            res = [0] * distance
            for i,ci in enumerate(ld[:-1]):
                res[i+1] += ci
            for j,cj in enumerate(rd[:-1]):
                res[j+1] += cj
            # print(root.val, res)
            return res
        f(root)
        return ans


    """ 1531. 压缩字符串 II #hard #DP #题型 较为复杂, 主要是代码细节较多.
「行程长度编码」是对于字符串中连续(超过一次)出现的字符进行压缩表示; 现给定一个字符串以及可以删去的字符数量, 要求删去若干字符之后, 行程长度编码最小. 限制: 字符串长度 100
提示: 注意, 我们对于连续的字符进行压缩表示, 对于一组 `(ck,dk)`, 我们的表示代价与数量dk的关系是: `cost = 1/2/3/4` 其中dk分别取 `[1], [2...9], [10...99], [100]`.
思路1: #DP #细节
    记 `f(i,j)` 为前i个字符删去j个后的最小压缩长度.
    转移: #分类 考虑. 1) i删去, 则有 `f(i,j) = f(i-1,j-1)`; 2) 保留i, 此时我们考虑最后的那一组 `(ci,di)`, 它们是哪些坐标中的字符串呢?
        假设删除后保留di个相同字符 ci, 直觉可知我们保留i往前最近的di个该字符即可. 具体证明见官答. 假设从i开始往左的第di个相同字符的位置是idxi, 则需要删除 i-idxi+1-ci 个字符
        因此, 有转移 `f(i,j) = min{ cost(ci,di) + f(idxi-1, j-(i-idxi+1-ci)) }`
[官答](https://leetcode.cn/problems/string-compression-ii/solution/ya-suo-zi-fu-chuan-ii-by-leetcode-solution/)
"""
    def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
        n = len(s)
        @lru_cache(None)
        def cost(cnt):
            if cnt==0: return 0
            elif cnt==1: return 1
            elif cnt<10: return 2
            elif cnt<100: return 3
            return 4
        # 记 `f(i,j)` 为前i个字符删去j个后的最小压缩长度
        # 1. 外层哨兵: 空字符串, 结果为0; 2. 内层, 删除的范围本来就是 0...k
        f = [[inf] * (k+1) for _ in range(n+1)]
        f[0] = [0] * (k+1)
        for i in range(1, n+1):     # 和字符串idx有一个差值
            for j in range(0, k+1):
                # 1) 删除第i个字符
                if j>=1:
                    f[i][j] = f[i-1][j-1]
                # 2) cnt, cntD 分别记录 s[i-1] 出现的数量和需要少出的数量.
                chi = s[i-1]
                cnt = 0; cntD = 0
                for idx in range(i-1, -1, -1):
                    if s[idx]==chi:
                        cnt += 1
                        # 剩余 s[0...idx-1], 用掉了cntD个删除操作, 因此 f[idx][j-cntD]
                        f[i][j] = min(f[i][j], cost(cnt) + f[idx][j-cntD])
                    else:
                        cntD += 1
                        if cntD > j: break
        return f[n][k]
        
sol = Solution()
result = [
    # sol.minFlips(target = "10111"),
    # sol.minFlips("000"),
    sol.getLengthOfOptimalCompression(s = "aaaaaaaaaaa", k = 0),
    sol.getLengthOfOptimalCompression(s = "aaabcccd", k = 2),
    sol.getLengthOfOptimalCompression(s = "aabbaa", k = 2),
]
for r in result:
    print(r)
