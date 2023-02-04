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

""" https://www.bilibili.com/video/BV1UD4y1Y769/

0104. 二叉树的最大深度 https://leetcode.cn/problems/maximum-depth-of-binary-tree/solutions/2010612/kan-wan-zhe-ge-shi-pin-rang-ni-dui-di-gu-44uz/
课后作业：
0111. 二叉树的最小深度 https://leetcode.cn/problems/minimum-depth-of-binary-tree/
0129. 求根节点到叶节点数字之和 https://leetcode.cn/problems/sum-root-to-leaf-numbers/
0257. 二叉树的所有路径 https://leetcode.cn/problems/binary-tree-paths/

Easonsi @2023 """
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    """ 0104. 二叉树的最大深度 #easy #题型
思路1: 不用全局变量
思路2: 全局变量 (写DFS函数)
[灵神](https://leetcode.cn/problems/maximum-depth-of-binary-tree/solution/kan-wan-zhe-ge-shi-pin-rang-ni-dui-di-gu-44uz/)
"""
    
    """ 0111. 二叉树的最小深度 #easy 从根节点到任一叶子节点的最小距离 """
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if not root: return 0
        d = inf 
        for node in [root.left, root.right]:
            if node is not None: d = min(d, self.minDepth(node)+1)
        return d if d!=inf else 1   # 注意跟节点判断
    
    """ 0129. 求根节点到叶节点数字之和 #medium 每一条路径表示从高位到低位的数字, 求所有路径表示数字之和
思路1: 递归DFS
    为了方便数字的计算, 在DFS的过程中需要传入上层的数字
[官答](https://leetcode.cn/problems/sum-root-to-leaf-numbers/solution/qiu-gen-dao-xie-zi-jie-dian-shu-zi-zhi-he-by-leetc/)
"""
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        def dfs(root,pre):
            if not root: return 0
            if root.left is None and root.right is None: return root.val + pre*10
            s = 0
            for c in [root.left, root.right]:
                s += dfs(c, pre*10+root.val)
            return s
        return dfs(root,0)
    
    """ 0257. 二叉树的所有路径 #easy 以字符形式范围二叉树上所有到叶子的路径 """
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        path = []
        ans = []
        def dfs(root:TreeNode):
            # leaf
            if root.left is None and root.right is None: 
                ans.append('->'.join(path+[str(root.val)]))
                return
            path.append(str(root.val))
            if root.left: dfs(root.left)
            if root.right: dfs(root.right)
            path.pop()
        dfs(root)
        return ans




sol = Solution()
result = [
    
]
for r in result:
    print(r)
