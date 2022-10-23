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
https://leetcode.cn/contest/weekly-contest-169



@2022 """

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    """ 1304. 和为零的 N 个不同整数 """
    
    """ 1305. 两棵二叉搜索树中的所有元素 """
    def getAllElements(self, root1: TreeNode, root2: TreeNode) -> List[int]:
        vals = []
        
        def dfs(node: TreeNode):
            if not node: return
            dfs(node.left)
            vals.append(node.val)
            dfs(node.right)
        dfs(root1)
        dfs(root2)
        return sorted(vals)
    
    """ 1306. 跳跃游戏 III #medium 从一个位置出发, 判断能否到达任意一个值为0的格子. """
    def canReach(self, arr: List[int], start: int) -> bool:
        n = len(arr)
        # @lru_cache(None)
        visited = [False] * n
        def f(idx):
            if visited[idx]: return False
            visited[idx] = True
            d = arr[idx]
            if d==0: return True
            if idx-d>=0 and f(idx-d): return True
            if idx+d<n and f(idx+d): return True
            return False
        return f(start)

    """ 1307. 口算难题 #hard

[official](https://leetcode.cn/problems/verbal-arithmetic-puzzle/solution/suan-nan-ti-by-leetcode-solution/)
"""
    def isSolvable(self, words: List[str], result: str) -> bool:
        used, carry = [False] * 10, [0] * 10
        lead_zero, rep = dict(), dict()

        for word in words:
            if len(word) > len(result):
                return False
            for ch in word:
                rep[ch] = -1
                lead_zero[ch] = max(lead_zero.get(ch, 0), 0)
            if len(word) > 1:
                lead_zero[word[0]] = 1
        for ch in result:
            rep[ch] = -1
            lead_zero[ch] = max(lead_zero.get(ch, 0), 0)
        if len(result) > 1:
            lead_zero[result[0]] = 1
        
        def dfs(pos, iden, length):
            """ 
            pos: 数位位置
            iden: words中的位置
            """
            if pos == length:
                # 搜索边界
                return carry[pos] == 0
            elif iden < len(words):
                # 搜索等式左边
                sz = len(words[iden])
                if sz < pos or rep[words[iden][sz - pos - 1]] != -1:
                    # 搜索下一个位置
                    return dfs(pos, iden + 1, length)
                else:
                    # 尝试映射到一个数字
                    ch = words[iden][sz - pos - 1]
                    for i in range(lead_zero[ch], 10):
                        if not used[i]:
                            used[i], rep[ch] = True, i
                            check = dfs(pos, iden + 1, length)
                            used[i], rep[ch] = False, -1
                            if check:
                                return True
                    return False
            else:
                # 搜索等式右边
                left = carry[pos] + sum(rep[word[len(word) - pos - 1]] for word in words if len(word) > pos)
                carry[pos + 1], left = left // 10, left % 10
                ch = result[len(result) - pos - 1]
                if rep[ch] == left:
                    return dfs(pos + 1, 0, length)
                elif rep[ch] == -1 and not used[left] and not (lead_zero[ch] == 1 and left == 0):
                    used[left], rep[ch] = True, left
                    check = dfs(pos + 1, 0, length)
                    used[left], rep[ch] = False, -1
                    return check
                else:
                    return False

        length = len(result)
        return dfs(0, 0, len(result))



sol = Solution()
result = [
    sol.canReach([3,0,2,1,2], 2),
]
for r in result:
    print(r)
