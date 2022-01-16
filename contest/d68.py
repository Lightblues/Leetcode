from typing import List
import collections
import math
import bisect

""" 
https://leetcode-cn.com/contest/biweekly-contest-68 """
class SolutionD68:
    """ 2114. 句子中的最多单词数 """
    def mostWordsFound(self, sentences: List[str]) -> int:
        words = [len(s.split(' ')) for s in sentences]
        return max(words)

    """ 2115. 从给定原材料中找到所有可以做出的菜 """
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        result = []
        def rec():
            changed = False
            for recipe, ingredient in zip(recipes, ingredients):
                if all(i in supplies for i in ingredient):
                    result.append(recipe)
                    supplies.append(recipe)
                    changed = True
                    recipes.remove(recipe)
                    ingredients.remove(ingredient)
            return changed
        while rec():
            continue
        return result

    """ 2116. 判断一个括号字符串是否有效 
给定一个在某些位上固定的字符串 (例如 `s = "))()))", locked = "010100"`), 判断能够通过修改其他自由位使其成为合法的括号序列

思路一: 
- 先尝试匹配 lock 部分的字符串, 记录未成功匹配的位置 (三种情况, 最后剩下 `((`, `))` or `))((`; 和 空白符号的位置;
- 利用 space 字符串来匹配剩下的左右括号 leftStack, rightStack
- 原本分了上面三种情况讨论, 实际上可以合并: 用 space 最前面的部分匹配右括号, 最后面的部分匹配左括号, `len(spaces)>=len(leftStack)+len(rightStack) and all([i>j for i,j in zip(spaces[-len(leftStack):], leftStack)]) and all([i<j for i,j in zip(spaces[:len(rightStack)], rightStack)])`

输入：s = "))()))", locked = "010100"
输出：true
解释：locked[1] == '1' 和 locked[3] == '1' ，所以我们无法改变 s[1] 或者 s[3] 。
我们可以将 s[0] 和 s[4] 变为 '(' ，不改变 s[2] 和 s[5] ，使 s 变为有效字符串。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/check-if-a-parentheses-string-can-be-valid
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。"""
    def canBeValid(self, s: str, locked: str) -> bool:
        n = len(s)
        if n%2 != 0:
            return False

        # leftCount = 0 # 目前的 ( 数量
        # leftSpace, rightSpace = 0,0 # 留给可以改变的位置

        """ 这里尝试匹配所有 lock 的左右括号, 记录未成功匹配的位置 (三种情况, 最后剩下 `((`, `))` or `))((` 和 空白符号的位置
        """
        spaces = []
        leftStack = collections.deque()
        rightStack = []
        for i,(ch,isLocked) in enumerate(zip(s,locked)):
            if isLocked=="1":
                if ch=='(':
                    leftStack.append(i)
                else:
                    if len(leftStack)>0:
                        leftStack.pop()
                    else:
                        rightStack.append(i)
            else:
                spaces.append(i)
        # if len(leftStack)==0:
        #     if len(rightStack)==0:
        #         return True
        #     else:
        #         # 剩下 )))
        #         if len(spaces)>=len(rightStack) and all([i<j for i,j in zip(spaces[:len(rightStack)], rightStack)]):
        #             return True
        #         return False
        # else:
        #     # (((
        #     if len(leftStack)==0:
        #         if len(spaces)>=len(leftStack) and all([i>j for i,j in zip(spaces[-len(leftStack):], leftStack)]):
        #             return True
        #         return False
        #     # )))(((
        #     else:
        #         if len(spaces)>=len(leftStack)+len(rightStack) and all([i>j for i,j in zip(spaces[-len(leftStack):], leftStack)]) and all([i<j for i,j in zip(spaces[:len(rightStack)], rightStack)]):
        #             return True
        #         return False

        if len(spaces)>=len(leftStack)+len(rightStack) and all([i>j for i,j in zip(spaces[-len(leftStack):], leftStack)]) and all([i<j for i,j in zip(spaces[:len(rightStack)], rightStack)]):
            return True
        return False

sol = SolutionD68()
result = [
    # sol.findAllRecipes(["bread","sandwich"], [["yeast","flour"],["bread","meat"]], ["yeast","flour","meat"])
    # sol.canBeValid(s = "))()))", locked = "010100"),
    sol.canBeValid(s = "((()(()()))()((()()))))()((()(()", locked="10111100100101001110100010001001")

]
for r in result:
    print(r)