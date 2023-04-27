from easonsi.util.leetcode import *

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode, linked2list, list2linked

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
https://leetcode.cn/contest/weekly-contest-311

T3非常有意思, 当时用了暴力思路不太行! T4写了个 Tire 居然还记得.

@2022 """
    
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    """ 2413. 最小偶倍数 """
    
    """ 2414. 最长的字母序连续子字符串的长度 """
    def longestContinuousSubstring(self, s: str) -> int:
        s = list(ord(c)-ord('a') for c in s+"0")
        ans = 0
        idx = 0
        for i,ch in enumerate(s):
            if i>0 and ch!=s[i-1]+1:
                ans = max(ans, i-idx)
                idx = i
            ans = max(ans, i-idx)
        return ans
    
    """ 2415. 反转二叉树的奇数层 #medium #题型 给定一颗完全二叉树, 要求翻转其第 1,3,5... 层. 限制: 节点数量 2^14
思路1: #暴力 求解, 记录每一层的节点序列.
    空间复杂度: O(n) 这里的n是每层的最大节点数.
思路2: #BFS 记录每一层的节点序列. 然后交换每一层的节点元素值. (而非节点顺序!!)
思路3: #DFS. 同时递归左右子树
    递归函数: `dfs(node1, node2, is_odd_level)` 利用一个bool来记录当前层是否为奇数层. 
    如何「对称」? 分别递归两个节点的 left, right. 想法精巧!
    关联: 「0101. 对称二叉树」(给定二叉树, 判断是否对称)
见 [灵神](https://leetcode.cn/problems/reverse-odd-levels-of-binary-tree/solutions/1831556/zhi-jie-jiao-huan-zhi-by-endlesscheng-o8ze/)
"""
    def reverseOddLevels(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        s = [root]
        flip = True
        while s[0]:
            nxt = list(itertools.chain(*[[t.left, t.right] for t in s]))
            # print(list(t.val for t in s))
            # print([t.val for t in nxt])
            if flip:
                n = len(s)
                for i,node in enumerate(s):
                    node.left = nxt[2*n-1-i*2]
                    node.right = nxt[2*n-1-i*2-1]
            else:
                n = len(s)
                for i in range(n):
                    s[n-1-i].left = nxt[i*2]
                    s[n-1-i].right = nxt[i*2+1]
            flip = False if flip else True
            s = nxt
        return root
    def reverseOddLevels(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # 思路2: #BFS 记录每一层的节点序列. 然后交换每一层的节点元素值. (而非节点顺序!!)
        q, level = [root], 0
        while q[0].left:
            q = list(itertools.chain.from_iterable((node.left, node.right) for node in q))
            if level == 0:
                for i in range(len(q) // 2):
                    x, y = q[i], q[len(q) - 1 - i]
                    x.val, y.val = y.val, x.val
            level ^= 1
        return root
    def reverseOddLevels(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # 思路3: #DFS. 同时递归左右子树
        def dfs(node1: Optional[TreeNode], node2: Optional[TreeNode], is_odd_level: bool) -> None:
            if node1 is None: return
            if is_odd_level: node1.val, node2.val = node2.val, node1.val
            dfs(node1.left, node2.right, not is_odd_level)
            dfs(node1.right, node2.left, not is_odd_level)
        dfs(root.left, root.right, True)
        return root

    
    """ 2416. 字符串的前缀分数和 #hard 简单考察 #Trie 字典树
给定一组字符串. 每个查询字符串的分数是, 其作为其他词的前缀的次数. 对于数组中所有字符串, 求其所有前缀的分数之和. 限制: n 1e3; 字符串长度 L 1e3
https://leetcode.cn/problems/sum-of-prefix-scores-of-strings/
思路1: #字典树. 利用字典树记录前缀出现的次数.
    对于每个字符串, 依次累计其路径上的节点的cnt值. (作为前缀)
"""
    def sumPrefixScores(self, words: List[str]) -> List[int]:
        class Node():
            def __init__(self, ch) -> None:
                self.ch = ch
                self.cnt = 0    # 当前前缀出现的次数.
                self.childs = defaultdict(Node)
        root = Node(" ")
        def add(word: str, root: Node):
            # 加word
            for ch in word:
                if ch not in root.childs: root.childs[ch] = Node(ch)
                root = root.childs[ch]
                root.cnt += 1
        def cnt(word: str, root: Node):
            # 查询题目要求
            ans = 0
            for ch in word:
                root = root.childs[ch]
                ans += root.cnt
            return ans
        for word in words: add(word, root)
        ans = []
        for word in words: ans.append(cnt(word, root))
        return ans

    
sol = Solution()
result = [
    # sol.longestContinuousSubstring("abacaba"),
    # sol.longestContinuousSubstring("abcde"),
    # sol.longestContinuousSubstring("a"),
    sol.sumPrefixScores(["abc","ab","bc","b"]),
    sol.sumPrefixScores(["abcd"])
]
for r in result:
    print(r)
