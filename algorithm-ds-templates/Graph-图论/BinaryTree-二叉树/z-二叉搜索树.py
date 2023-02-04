from easonsi.util.leetcode import *
import random
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
https://www.bilibili.com/video/BV14G411P7C1/
讲了前序遍历、中序遍历和后序遍历三种方法。

0098. 验证二叉搜索树 https://leetcode.cn/problems/validate-binary-search-tree/solutions/2020306/qian-xu-zhong-xu-hou-xu-san-chong-fang-f-yxvh/
课后作业：
0230. 二叉搜索树中第K小的元素 https://leetcode.cn/problems/kth-smallest-element-in-a-bst/
0501. 二叉搜索树中的众数 https://leetcode.cn/problems/find-mode-in-binary-search-tree/
0530. 二叉搜索树的最小绝对差 https://leetcode.cn/problems/minimum-absolute-difference-in-bst/
0700. 二叉搜索树中的搜索 https://leetcode.cn/problems/search-in-a-binary-search-tree/

Easonsi @2023 """
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    """ 0098. 验证二叉搜索树 判断给定的二叉搜索树是否合法
思路1: #前序遍历 
    递归函数 `valid(root: TreeNode, l:int, r:int)` 传入合法的区间 [l, r]
思路2: #中序遍历
    利用性质: 二叉搜索树中序遍历是递增的
思路3: #后序遍历
    对于一个节点, 根据 val 和left子树最大值和right最大值的关系判断是否合法
    注意: 但一个节点不能只返回 最大/最小值, 而是两个值都要判断!!
[灵神](https://leetcode.cn/problems/validate-binary-search-tree/solution/qian-xu-zhong-xu-hou-xu-san-chong-fang-f-yxvh/)
"""
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # 思路1: #前序遍历
        def valid(root: TreeNode, l:int, r:int) -> bool:
            if root is None: return True
            x = root.val
            return l < x < r and valid(root.left, l, x) and valid(root.right, x, r)
        return valid(root, -inf, inf)
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # 思路2: #中序遍历
        def valid(root: TreeNode) -> bool:
            if root is None: return True
            if not valid(root.left): return False
            if root.val <= self.pre: return False
            self.pre = root.val
            return valid(root.right)
        self.pre = -inf
        return valid(root)
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        # 思路3: #后序遍历
        def f(node: TreeNode):
            if node is None: return (inf, -inf)     # 边界
            lmn,lmx = f(node.left)
            rmn,rmx = f(node.right)
            x = node.val
            if not lmx < x < rmn: return (-inf, inf)    # 标记区间不合法
            return (min(lmn, x), max(rmx, x))
        return f(root)[1] != inf
            
    """ 0230. 二叉搜索树中第K小的元素 #medium 得到二叉搜索树中的第K小的元素
思路1: #中序遍历 可以写成递归形式; 也可以用栈展开
    复杂度: O(n)
针对需要频繁修改/查询的, 如何优化?
思路2: 记录每个节点包含的子节点数目
    我们可以记录每个节点包含的子节点数目, 这样就可以在O(1)时间内知道左子树的节点数目
    在建立好索引之后, 每次查询的复杂度为 O(h)
思路3: 针对需要频繁修改的场景, 可以采用「平衡二叉搜索树（AVL树）」
    复杂度: 插入、删除、查询的复杂度均为 O(logn)
    关联: 「1382. 将二叉搜索树变平衡」
[官答](https://leetcode.cn/problems/kth-smallest-element-in-a-bst/solution/er-cha-sou-suo-shu-zhong-di-kxiao-de-yua-8o07/)
"""
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        # 思路1: #中序遍历. 神奇的 #yield 语法
        def f(node: TreeNode):
            if node is None: return
            yield from f(node.left)
            yield node.val
            yield from f(node.right)
        return list(f(root))[k-1]
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        # 用栈展开
        st = []
        while root or st:       # 注意这里的判断
            while root:
                st.append(root)
                root = root.left
            root = st.pop()
            k -= 1
            if k==0: return root.val
            root = root.right   # 注意要尝试遍历 right 
    def kthSmallest(self, root: TreeNode, k: int) -> int:
        class MyBst:
            def __init__(self, root: TreeNode):
                self.root = root
                # 统计以每个结点为根结点的子树的结点数，并存储在哈希表中
                self._node_num = {}
                self._count_node_num(root)
            def kth_smallest(self, k: int):
                """返回二叉搜索树中第k小的元素"""
                node = self.root
                while node:
                    left = self._get_node_num(node.left)
                    if left < k - 1:
                        node = node.right
                        k -= left + 1
                    elif left == k - 1:
                        return node.val
                    else:
                        node = node.left
            def _count_node_num(self, node) -> int:
                """统计以node为根结点的子树的结点数"""
                if not node:
                    return 0
                self._node_num[node] = 1 + self._count_node_num(node.left) + self._count_node_num(node.right)
                return self._node_num[node]
            def _get_node_num(self, node) -> int:
                """获取以node为根结点的子树的结点数"""
                return self._node_num[node] if node is not None else 0

        bst = MyBst(root)
        return bst.kth_smallest(k)
    def kthSmallest(self, root: TreeNode, k: int) -> int:
        # 
        def inorder(node):
            if node.left:
                inorder(node.left)
            inorder_lst.append(node.val)
            if node.right:
                inorder(node.right)
        # 中序遍历生成数值列表
        inorder_lst = []
        inorder(root)

        # 构造平衡二叉搜索树
        from AVL import AVL
        avl = AVL(inorder_lst)

        # # 模拟1000次插入和删除操作
        # random_nums = [random.randint(0, 10001) for _ in range(1000)]
        # for num in random_nums:
        #     avl.insert(num)
        # random.shuffle(random_nums)  # 列表乱序
        # for num in random_nums:
        #     avl.delete(num)
        
        return avl.kth_smallest(k)

    """ 0501. 二叉搜索树中的众数 #easy #题型 
思路1: 如何避免使用哈希表? (复杂度 O(n))
    可以在中序遍历的过程中, 利用二叉搜索树的递增特性!
    在定义一些辅助变量的基础上, 可以抽象出 update(x) 函数
思路2: 如何进一步优化为 O(1) 的空间? 可以利用 #Morris 中序遍历
"""
    def findMode(self, root: Optional[TreeNode]) -> List[int]:
        mx = 0; mxValues = []
        v = None; cnt = 0
        def update(x):
            nonlocal v,cnt,mx,mxValues
            if x != v: v = x; cnt = 1
            else: cnt += 1
            if cnt>mx: mx = cnt; mxValues = [v]
            elif cnt==mx: mxValues.append(v)
        # 
        st = []
        while root or st:
            while root:
                st.append(root)
                root = root.left
            root = st.pop()
            update(root.val)
            root = root.right
        return mxValues
    def findMode(self, root: Optional[TreeNode]) -> List[int]:
        mx = 0; mxValues = []
        v = None; cnt = 0
        def update(x):
            nonlocal v,cnt,mx,mxValues
            if x != v: v = x; cnt = 1
            else: cnt += 1
            if cnt>mx: mx = cnt; mxValues = [v]
            elif cnt==mx: mxValues.append(v)
        # Morris 中序遍历. cur 是当前节点 (一个节点最多访问两次)
        # 遍历过程中会对 [1,2,3,4,5] 形状的二叉树中的节点5新建right指针, 但最后会被取消
        cur, pre = root, None
        while cur:
            if not cur.left:
                update(cur.val)
                cur = cur.right
                continue
            p = cur.left    # p 是 cur 的前驱节点
            while p.right and p.right!=cur:     # 注意下面 p.right==cur 说明出现了新建的边!
                p = p.right
            # 注意, 左子树上的前驱节点应该是没有right指针的! 在下面else部分生成right指向cur, 并继续搜索左子树
            if p.right==cur:
                p.right = None  # 取消新建的边
                update(cur.val)
                cur = cur.right
            else:
                p.right = cur   # 新建边
                cur = cur.left
        return mxValues
    
    """ 0530. 二叉搜索树的最小绝对差 #easy """
    def getMinimumDifference(self, root: Optional[TreeNode]) -> int:
        pre = -inf
        mn = inf
        st = []
        while root or st:
            while root:
                st.append(root)
                root = root.left
            root = st.pop()
            mn = min(mn, root.val-pre)
            pre = root.val
            root = root.right
        return mn
    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
