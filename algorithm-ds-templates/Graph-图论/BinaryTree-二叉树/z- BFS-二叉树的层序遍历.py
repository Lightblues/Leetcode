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

""" https://www.bilibili.com/video/BV1hG4y1277i/

0102. 二叉树的层序遍历 https://leetcode.cn/problems/binary-tree-level-order-traversal/solutions/2049807/bfs-wei-shi-yao-yao-yong-dui-lie-yi-ge-s-xlpz/
0103. 二叉树的锯齿形层序遍历 https://leetcode.cn/problems/binary-tree-zigzag-level-order-traversal/solutions/2049827/bfs-wei-shi-yao-yao-yong-dui-lie-yi-ge-s-xlv3/
0513. 找树左下角的值 https://leetcode.cn/problems/find-bottom-left-tree-value/solutions/2049776/bfs-wei-shi-yao-yao-yong-dui-lie-yi-ge-s-f34y/
课后作业: 都在 [二叉树递归] 中写过
0104. 二叉树的最大深度 https://leetcode.cn/problems/maximum-depth-of-binary-tree/
0111. 二叉树的最小深度 https://leetcode.cn/problems/minimum-depth-of-binary-tree/
0199. 二叉树的右视图 https://leetcode.cn/problems/binary-tree-right-side-view/

Easonsi @2023 """
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    """ 0102. 二叉树的层序遍历 #medium
思路1: 利用两个队列, 一个存储当前层的节点, 一个存储下一层的节点
思路2: 只用一个deque! 每一层 for _ in range(len(q)) 即可
"""
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None: return []
        ans = []
        cur = [root]
        while cur:
            nxt = []
            vals = []
            for node in cur:
                vals.append(node.val)
                if node.left:  nxt.append(node.left)
                if node.right: nxt.append(node.right)
            cur = nxt
            ans.append(vals)
        return ans
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if root is None: return []
        ans = []
        q = deque([root])
        while q:
            vals = []
            for _ in range(len(q)):
                node = q.popleft()
                vals.append(node.val)
                if node.left:  q.append(node.left)
                if node.right: q.append(node.right)
            ans.append(vals)
        return ans

    """ 0103. 二叉树的锯齿形层序遍历 #medium 相较于 0102, 偶数层从右往左返回 """
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        pass
    
    """ 0513. 找树左下角的值 #medium 找到二叉树最底层的最左节点 """
    def findBottomLeftValue(self, root: Optional[TreeNode]) -> int:
        q = deque([root])
        while q:
            node = q.popleft()
            if node.right: q.append(node.right)
            if node.left: q.append(node.left)
        return node.val
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
