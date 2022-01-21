from typing import List
import collections
import math
import bisect
import heapq

""" 
https://leetcode-cn.com/contest/biweekly-contest-68 """
class SolutionD68:
    """ 2114. 句子中的最多单词数 """
    def mostWordsFound(self, sentences: List[str]) -> int:
        words = [len(s.split(' ')) for s in sentences]
        return max(words)

    """ 2115. 从给定原材料中找到所有可以做出的菜
你有 n 道不同菜的信息。给你一个字符串数组 recipes 和一个二维字符串数组 ingredients 。第 i 道菜的名字为 recipes[i] ，如果你有它 所有 的原材料 ingredients[i] ，那么你可以 做出 这道菜。一道菜的原材料可能是 另一道 菜，也就是说 ingredients[i] 可能包含 recipes 中另一个字符串。

输入：recipes = ["bread","sandwich"], ingredients = [["yeast","flour"],["bread","meat"]], supplies = ["yeast","flour","meat"]
输出：["bread","sandwich"]
解释：
我们可以做出 "bread" ，因为我们有原材料 "yeast" 和 "flour" 。
我们可以做出 "sandwich" ，因为我们有原材料 "meat" 且可以做出原材料 "bread" 。

思路一: 本题数据量比较小, 可以暴力遍历.
思路二: 依赖关系构成图, 可以用拓扑排序, see [here](https://leetcode-cn.com/problems/find-all-possible-recipes-from-given-supplies/solution/cong-gei-ding-yuan-cai-liao-zhong-zhao-d-d02i/)
 """
    def findAllRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        result = []
        def rec():
            changed = False
            """ 一开始直接 zip 然后调用了列表的 remove 方法, 没注意到: 两道菜所要求的成分可以是完全一样的! 
            修改成按照 index 遍历后过了 """
            for i in range(len(recipes)-1, -1, -1):
            # for recipe, ingredient in zip(recipes, ingredients):
                recipe, ingredient = recipes[i], ingredients[i]
                if all(i in supplies for i in ingredient):
                    result.append(recipe)
                    supplies.append(recipe)
                    changed = True
                    # recipes.remove(recipe)
                    # ingredients.remove(ingredient)
                    del recipes[i], ingredients[i]
            return changed
        while rec():
            continue
        return result
    
    def findAllRecipes2(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        n = len(recipes)
        depend = collections.defaultdict(list)  # 每个食材/菜 的依赖项, 反向图
        cnt = collections.Counter()     # 记录每道菜依赖的数量
        for i in range(n):
            for ing in ingredients[i]:
                depend[ing].append(recipes[i])
            cnt[recipes[i]] = len(ingredients[i])
        ans = list()
        q = collections.deque(supplies)
        while q:
            cur = q.popleft()
            if cur in depend:
                for rec in depend[cur]:
                    cnt[rec] -= 1 # 一道菜的依赖全部被满足
                    if cnt[rec] == 0:
                        ans.append(rec)
                        q.append(rec)
        return ans

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


    """ 2117. 一个区间内所有数乘积的缩写
给你两个正整数 left 和 right ，满足 left <= right 。请你计算 闭区间 [left, right] 中所有整数的 乘积 。
结果保留去掉最后 0 的前后五位数字.
比方说，12345678987600000 被表示为 "12345...89876e5" 。

输入：left = 371, right = 375
输出："7219856259e3"
解释：乘积为 7219856259000 。 """
    def abbreviateProduct(self, left: int, right: int) -> str:
        # 超时了
        # [思路详解+详细讨论一下精度问题](https://leetcode-cn.com/problems/abbreviating-the-product-of-a-range/solution/fen-bie-ji-suan-qian-5wei-he-hou-5wei-si-dc9x/)
        C, maxpre, mod, maxval = 0, 10**25, 10**10, 10**12
        val, pre, suf = 1,1,1
        for i in range(left, right+1):
            pre *= i
            suf *= i
            last = 0
            while pre > maxpre:
                last = pre % 10
                pre = pre // 10
            if last >= 5:       # 四舍五入
                pre += 1
            while suf % 10 == 0:
                suf //= 10
                C += 1
            # suf %= mod
            if val <= maxval:
                val *= i
                while val % 10 == 0:
                    val //= 10
        # val 记录非 0 项的数字长度
        if len(str(val)) <= 10:
            return str(val) + 'e' + str(C)
        else:
            p, s = str(pre), str(suf)
            return p[:5] + '...' +  s[-5:] + 'e' + str(C)

        if len(str(val)) <= 10:
            return str(val) + 'e' + str(C)
        else:
            p, s = str(pre), str(suf)
            while len(p) > 5:
                p = p[:-1]
            while len(s) > 5:
                s = s[1:]
            while len(s) < 5:
                s = '0' + s
            return p + '...' + s + 'e' + str(C)

sol = SolutionD68()
result = [
    # sol.findAllRecipes(["bread","sandwich"], [["yeast","flour"],["bread","meat"]], ["yeast","flour","meat"])
    # sol.findAllRecipes2(
    #     ["fe","nvvj","kps","ik","gd","gjpz","cff","ljb","ybxsh","vtu","htsn","jwwxz","znoem","h","mlg","ggd","bkinz","pzjna","pxum"],
    #     [["zqg"],["zqg"],["t"],["zqg"],["bkinz","ggd","ljb","ybxsh","nvvj","pzjna","cff"],["kps","nvvj","pxum","ik","cff","ybxsh","h"],["yyym"],["zqg"],["htsn","vtu"],["kfukc"],["zqg"],["zqg"],["a"],["zqg","gd","ybxsh","ggd","ljb"],["ybxsh","pxum","h","bkinz"],["zqg"],["zqg"],["mu"],["zqg"]],
    #     ["zqg"]
    # )
    # sol.canBeValid(s = "))()))", locked = "010100"),
    # sol.canBeValid(s = "((()(()()))()((()()))))()((()(()", locked="10111100100101001110100010001001")
    # sol.abbreviateProduct(left = 1, right = 4),
    # sol.abbreviateProduct(left = 371, right = 375)
    sol.abbreviateProduct(44, 9556)
]
for r in result:
    print(r)