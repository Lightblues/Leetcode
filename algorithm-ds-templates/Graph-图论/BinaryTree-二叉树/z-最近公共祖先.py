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

""" https://www.bilibili.com/video/BV1W44y1Z7AR/
0236. 二叉树的最近公共祖先 https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/solutions/2023872/fen-lei-tao-lun-luan-ru-ma-yi-ge-shi-pin-2r95/
0235. 二叉搜索树的最近公共祖先 https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-search-tree/solutions/2023873/zui-jin-gong-gong-zu-xian-yi-ge-shi-pin-8h2zc/
Easonsi @2023 """
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    """ 0236. 二叉树的最近公共祖先 #medium #题型 给定二叉树上的两个节点, 找到它们的最短公共祖先
思路1: 得到每个节点的father, 直接得到路径!
    根据两个点的从跟节点出发的路径, 求交.
思路2: DFS返回 p/q 是否在该子树中
[灵神](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/solution/fen-lei-tao-lun-luan-ru-ma-yi-ge-shi-pin-2r95/)
"""
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # 思路1: 根据两个点的从跟节点出发的路径, 求交.
        fa = {root: None}
        def dfs(a: TreeNode):
            if a.left: fa[a.left] = a; dfs(a.left)
            if a.right: fa[a.right] = a; dfs(a.right)
        dfs(root)
        pathP = set()
        while p:
            pathP.add(p); p = fa[p]
        while q not in pathP:
            q = fa[q]
        return q
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # 返回: 若 p/q 在当前节点下, 则返回该节点; 若都不在, 则返回 None
        if root in (None, p, q):    # 若当前节点正是 p/q, 该节点就是 LCA
            return root
        # 递归在左右孩子中找
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:  # p/q 分别出现在左右
            return root
        return left if left else right
    
    """ 0235. 二叉搜索树的最近公共祖先 #easy 相较于一般的二叉树, 利用其有序的性质简单了很多 """
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        a,b = sorted([p.val, q.val])
        def f(root: TreeNode, a,b):
            if a<=root.val<=b: return root
            elif root.val<a: return f(root.right,a,b)
            else: return f(root.left, a,b)
        return f(root, a,b)
    
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
