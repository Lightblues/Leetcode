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
https://www.bilibili.com/video/BV18M411z7bb/

0100. 相同的树 https://leetcode.cn/problems/same-tree/solutions/2015056/ru-he-ling-huo-yun-yong-di-gui-lai-kan-s-empk/
0101. 对称二叉树 https://leetcode.cn/problems/symmetric-tree/solutions/2015063/ru-he-ling-huo-yun-yong-di-gui-lai-kan-s-6dq5/
0110. 平衡二叉树 https://leetcode.cn/problems/balanced-binary-tree/solutions/2015068/ru-he-ling-huo-yun-yong-di-gui-lai-kan-s-c3wj/
0199. 二叉树的右视图 https://leetcode.cn/problems/binary-tree-right-side-view/solutions/2015061/ru-he-ling-huo-yun-yong-di-gui-lai-kan-s-r1nc/
课后作业：
0226. 翻转二叉树 https://leetcode.cn/problems/invert-binary-tree/
Easonsi @2023 """
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    """ 0100. 相同的树 #easy 判断两棵树是否相同 """
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if p is None or q is None: return p == q
        return p.val==q.val and self.isSameTree(p.left, q.left) and self.isSameTree(p.right,q.right)
    
    """ 0101. 对称二叉树 判断一棵二叉树是否是对称的 #easy 另见 [leetbook] """
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def isSymm(p,q):
            if p is None or q is None: return p==q
            return p.val==q.val and isSymm(p.left,q.right) and isSymm(p.right,q.left)
        return isSymm(root,root)
    
    """ 0110. 平衡二叉树. #easy 平衡二叉树定义: 「每个节点的左右子树高度差不超过1」 """
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def f(root):
            # 返回: 当前节点的高度, 若违反了则返回-1
            if not root: return 0
            l = f(root.left)
            r = f(root.right)
            # 判断是否平衡
            if l==-1 or r==-1 or abs(l-r)>1: return -1
            return max(l,r)+1
        return f(root)!=-1
    
    """ 0199. 二叉树的右视图 #medium 给定一棵树, 返回从右侧可以看到的节点列表. 
思路1: 先DFS右子树, 再用一个全局的变量记录当前的最大深度
[官答](https://leetcode.cn/problems/binary-tree-right-side-view/solution/er-cha-shu-de-you-shi-tu-by-leetcode-solution/)
 """
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        ans = []
        def dfs(root:TreeNode, d):
            if not root: return
            if d>=len(ans): ans.append(root.val)
            dfs(root.right,d+1)
            dfs(root.left,d+1)
        dfs(root,0)
        return ans
    
    """ 0226. 翻转二叉树 #easy #题型
思路1: 经典题目, 递归交换左右子树即可. 总结
[官答](https://leetcode.cn/problems/invert-binary-tree/solution/fan-zhuan-er-cha-shu-by-leetcode-solution/)
"""
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root: return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root
        
        
sol = Solution()
result = [
    
]
for r in result:
    print(r)
