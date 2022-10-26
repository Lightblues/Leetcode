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

T4也太烦了, 官答也太长了... 

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

    """ 1307. 口算难题 #hard 给定一个字符串表达的加法式子. 每个字母对应一个数字, 没有前缀零. 问该表达式是否合法. 限制: 字符串数量 s 5; 每个字符串(数字)长度 l 7; 所有的字符的数量 n 10

[official](https://leetcode.cn/problems/verbal-arithmetic-puzzle/solution/suan-nan-ti-by-leetcode-solution/)

输入：words = ["SIX","SEVEN","SEVEN"], result = "TWENTY"
输出：true
解释：映射 'S'-> 6, 'I'->5, 'X'->0, 'E'->8, 'V'->7, 'N'->2, 'T'->1, 'W'->'3', 'Y'->4
所以 "SIX" + "SEVEN" + "SEVEN" = "TWENTY" ,  650 + 68782 + 68782 = 138214

来源：力扣（LeetCode）
链接：https://leetcode.cn/problems/verbal-arithmetic-puzzle
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
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

        return dfs(0, 0, len(result))



sol = Solution()
result = [
    # sol.canReach([3,0,2,1,2], 2),
    sol.isSolvable(["SEND","MORE"], "MONEY"),
    sol.isSolvable(["SIX","SEVEN","SEVEN"], "TWENTY"),
]
for r in result:
    print(r)
