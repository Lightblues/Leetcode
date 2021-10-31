"""
给定一个整数 n 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 有效的 括号组合。

输入：n = 3
输出：["((()))","(()())","(())()","()(())","()()()"]
"""

class Solution:
    # def generateParenthesis(self, n: int) -> List[str]:
    def generateParenthesis(self, n):
        result = []
        seq = []
        def gen(i,j):
            # 需要保证 i>=j 的循环条件
            # 结束条件
            if i==j==n:
                result.append(''.join(seq))
                return
            # 有三个可能，仅能添加 ( 或者 ) 或者 () 都可添加
            # 1. 仅能添加 )，条件只能是 ( 用完了
            if i==n:
                seq.append(')')
                gen(i, j+1)
            # 2. 仅能添加 (，条件只能是 () 数量相等
            elif i==j:
                seq.append('(')
                gen(i+1, j)
            # 3. () 均可
            else:
                seq.append('(')
                gen(i+1, j)
                seq.pop(-1)
                seq.append(')')
                gen(i, j+1)
            seq.pop(-1)
        gen(0, 0)
        return result

    # @lru_cache(None)
    def generateParenthesis2(self, n: int):
        if n == 0:
            return ['']
        ans = []
        for c in range(n):
            for left in self.generateParenthesis2(c):
                for right in self.generateParenthesis2(n - 1 - c):
                    ans.append('({}){}'.format(left, right))
        return ans



print(Solution().generateParenthesis(3))
print(Solution().generateParenthesis2(3))
