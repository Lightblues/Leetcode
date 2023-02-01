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
[灵神](https://www.bilibili.com/video/BV1xG4y1F7nC/)

== 组合型
0077. 组合 #medium 返回 [1, n] 中选k的所有组合 限制: n 20
    思路: 相较于子集回溯, 组合需要限定搜索深度. 复杂度: 节点数量为 C(n,k), 每个叶子为 O(k), 因此总体复杂度为 O(C(n,k)*k)
0216. 组合总和 #medium 返回 [1, 9] 中选k的所有组合, 使得和为 n 限制: k 9; n 60
    关联 「0077. 组合」. 不同之处在于, 需要进行一定的剪枝/条件判断. 
0022. 括号生成 #medium 需要生成长度为 2n的括号序列, 找到所有合法的. 

Easonsi @2023 """
class Solution:
    """ 0077. 组合 #medium #回溯 返回 [1, n] 中选k的所有组合 限制: n 20
思路: 相较于子集回溯, 组合需要限定搜索深度. 复杂度: 节点数量为 C(n,k), 每个叶子为 O(k), 因此总体复杂度为 O(C(n,k)*k)
    1.1 枚举下一个数选哪个
    1.2 选或不选
"""
    def combine(self, n: int, k: int) -> List[List[int]]:
        # 方法一：枚举下一个数选哪个
        ans = []
        path = []
        def dfs(i: int) -> None:
            d = k - len(path)  # 还要选 d 个数
            if d == 0:
                ans.append(path.copy())
                return
            for j in range(i, d - 1, -1):
                path.append(j)
                dfs(j - 1)
                path.pop()
        dfs(n)
        return ans
    def combine(self, n: int, k: int) -> List[List[int]]:
        # 方法二：选或不选
        ans = []
        path = []
        def dfs(i: int) -> None:
            d = k - len(path)  # 还要选 d 个数
            if d == 0:
                ans.append(path.copy())
                return
            # 不选 i
            if i > d: dfs(i - 1)
            # 选 i
            path.append(i)
            dfs(i - 1)
            path.pop()
        dfs(n)
        return ans


    """ 0216. 组合总和 III #medium #回溯 返回 [1, 9] 中选k的所有组合, 使得和为 n 限制: k 9; n 60
关联 「0077. 组合」. 不同之处在于, 需要进行一定的剪枝/条件判断. 
下面给了两个基本的剪枝技巧. 
"""
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        # 方法一：枚举下一个数选哪个
        ans = []
        path = []
        def dfs(i: int, t: int) -> None:
            # 从元素i开始选择; 剩余和为t.
            # 在搜索过程中, 从后往前搜索, 只是方便起见
            d = k - len(path)  # 还要选 d 个数
            # 两点剪枝技巧: 1) 所选已经超过了n; 2) 取最大的d个数字仍无法达到n
            if t < 0 or t > (i * 2 - d + 1) * d // 2:  # 剪枝
                return
            if d == 0:  # 注意这个时候不需要判断了! 因为上面的剪枝已经保证了t==0
                ans.append(path.copy())
                return
            # 枚举下一个数选哪个
            for j in range(i, d - 1, -1):
                path.append(j)
                dfs(j - 1, t - j)
                path.pop()
        dfs(9, n)
        return ans
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        # 方法二：选或不选
        ans = []
        path = []
        def dfs(i: int, t: int) -> None:
            d = k - len(path)  # 还要选 d 个数
            if t < 0 or t > (i * 2 - d + 1) * d // 2:  # 剪枝
                return
            if d == 0:
                ans.append(path.copy())
                return
            # 不选 i
            if i > d: dfs(i - 1, t)
            # 选 i
            path.append(i)
            dfs(i - 1, t - i)
            path.pop()
        dfs(9, n)
        return ans

    """ 0022. 括号生成 #medium #回溯 需要生成长度为 2n的括号序列, 找到所有合法的. 
思路1: #回溯
    1.1 枚举选左括号还是右括号
    1.2 枚举下一个左括号的位置
"""
    def generateParenthesis(self, n: int) -> List[str]:
        # 方法一：枚举选左括号还是右括号
        m = n * 2
        ans = []
        path = [''] * m
        def dfs(i: int, open: int) -> None:
            # i 是当前要填的位置, open是左括号数量
            if i == m:
                ans.append(''.join(path))
                return
            if open < n:  # 可以填左括号
                path[i] = '('
                dfs(i + 1, open + 1)
            if i - open < open:  # 可以填右括号
                path[i] = ')'
                dfs(i + 1, open)
        dfs(0, 0)
        return ans
    def generateParenthesis(self, n: int) -> List[str]:
        # 方法二：枚举下一个左括号的位置
        ans = []
        path = []
        # balance = 左括号个数 - 右括号个数
        def dfs(i: int, balance: int) -> None:
            if len(path) == n:
                s = [')'] * (n * 2)
                for j in path:
                    s[j] = '('
                ans.append(''.join(s))
                return
            # 可以填 0 到 balance 个右括号
            for close in range(balance + 1):  # 填 close 个右括号
                path.append(i + close)  # 填 1 个左括号
                dfs(i + close + 1, balance - close + 1)
                path.pop()
        dfs(0, 0)
        return ans


sol = Solution()
result = [
    sol.combinationSum3(k = 3, n = 7),
    sol.combinationSum3(k = 3, n = 9),
]
for r in result:
    print(r)
