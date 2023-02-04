from easonsi import utils
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
from 官方的 [二叉树](https://leetcode.cn/leetbook/read/data-structure-binary-tree/)
== 基本
二叉树的遍历: 前序, 中序, 后序; 层序;
    前序, 中序, 后序 分别可以写成递归和迭代的形式, 后者用到栈存储;
    层序遍历, 需要用到队列来记录同层的节点

递归逻辑
    「自顶向下」: 在每个递归层级，我们将首先访问节点来计算一些值，并在递归调用函数时将这些值传递到子节点
    「自底向上」: 在每个递归层次上，我们首先对所有子节点递归地调用函数，然后根据返回值和根节点本身的值得到答案
    几道例题: 求二叉树的最大深度; 判断二叉树是否对称; 二叉树上的路径总和是否有特定值. 除了较为方便的递归形式, 都可展开为迭代.


== 其他题目
从中序与后序遍历序列构造二叉树; 从前序与中序遍历序列构造二叉树
    利用了: 1) 前序/后序遍历的root节点的位置是固定的; 然后在中序的结果中找到分割点, 这样就知道了左/右子树的大小, 在前序/后序遍历中的对应位置就是该子树的遍历结果.
    递归函数签名: f(pl,pr, il,ir) -> TreeNode
填充每个节点的下一个右侧节点指针; 填充每个节点的下一个右侧节点指针 II
    给定一棵 (完美) 二叉树, 给每个节点设置next指针, 指向同层节点从左到右的下一个节点.
    限制: 进阶要求是, 使用常量级额外空间 (递归调用的栈空间不算).
    思路1:  采用 #BFS. 如何下一层中节点的pre是谁? 另外用一个链表来记录 下一层节点的next关系
236. 二叉树的最近公共祖先 给定二叉树上的两个节点, 找到它们的最短公共祖先
    思路1: 根据两个点的从跟节点出发的路径, 求交.
0297. 二叉树的序列化与反序列化 #题型 要求将一个二叉树序列化 (serialize) 和反序列化. 也即用无损的字符串表示二叉树. 限制: 节点数 1e4, 注意可能为 None
    思路: 采用任意的 BFS/DFS/前序 等遍历方式均可, 注意在解码的时候, 按照相同的顺序进行还原.

@2022 """
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Definition for a Node.
class Node:
    # next 指针指向同层节点的下一个元素
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

class Solution:
    """ 前序遍历 """
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        # 前序, 递归
        ans = []
        def f(root: TreeNode):
            if root is None: return
            ans.append(root.val)
            f(root.left)
            f(root.right)
        f(root)
        return ans
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        # 前序, 用stack展开为迭代
        ans = []
        stack = [root]
        while stack:
            p = stack.pop()
            if p is None: continue
            ans.append(p.val)
            stack.append(p.right)
            stack.append(p.left)
        return ans
    
    """ 中序遍历
    注意迭代形式需要用到栈记录历史路径, 并且终止条件是 `while p or stack` """
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        # 中序, 递归
        ans = []
        def f(root: TreeNode):
            if root is None: return
            f(root.left)
            ans.append(root.val)
            f(root.right)
        f(root)
        return ans
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        # 中序, 用stack记录待遍历右侧的节点. 参见 二叉搜索树中的 BSTIterator 类
        ans = []
        stack = []
        p = root    # p 指向当前节点
        # 注意: 终止条件由stack和p共同来决定.
        # 遍历过程中有可能 stack为空而p不为空; 反之也有可能.
        while p or stack:
            # 先尽量向左, 用stack记录遍历过的节点
            while p is not None:
                stack.append(p)
                p = p.left
            # 还有
            if stack:
                p = stack.pop()
                ans.append(p.val)
                p = p.right
        return ans

    """ 后序遍历 """
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        # 后序, 递归
        ans = []
        def f(root: TreeNode):
            if root is None: return
            f(root.left)
            f(root.right)
            ans.append(root.val)
        f(root)
        return ans
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        # 后序, 延续前序遍历的思路; 最后对于结果进行翻转
        ans = []
        stack = [root]
        while stack:
            p = stack.pop()
            if p is None: continue
            ans.append(p.val)
            stack.append(p.left)
            stack.append(p.right)
        return ans[::-1]
    
    """ 层序遍历 """
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        # 层序遍历, 使用queue
        if root is None: return []
        ans = []
        queue = [root]
        while queue:
            nqueue = []
            level = []
            for v in queue:
                level.append(v.val)
                if v.left: nqueue.append(v.left)
                if v.right: nqueue.append(v.right)
            queue = nqueue
            ans.append(level)
        return ans
    
    
    """ 0104. 二叉树的最大深度 给定一棵二叉树, 求其最大深度. """
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        # 终止条件
        if root is None: return 0
        # 递归逻辑
        return max(self.maxDepth(root.left)+1, self.maxDepth(root.right)+1)
    
    """ 0101. 对称二叉树 判断一棵二叉树是否是对称的 另见 [z-对称] """
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        # 递归写法
        def check(a:TreeNode, b:TreeNode) -> bool:
            # 检查两棵子树是否对称
            # 边界: None
            if a is None and b is None: return True
            if a is None or b is None: return False
            
            if a.val!=b.val: return False
            # 递归条件: 左右对称
            if not check(a.left, b.right): return False
            if not check(a.right, b.left): return False
            return True
        check(root.left, root.right)
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        # 循环写法, 利用一个 queue 进行记录匹配
        if root is None: return True
        # 直接用了 Copilot 的结果, 只用一个queue即可.
        queue = [root.left, root.right]
        while queue:
            nqueue = []
            for i in range(0, len(queue), 2):
                if queue[i] is None and queue[i+1] is None: continue
                if queue[i] is None or queue[i+1] is None: return False
                if queue[i].val!=queue[i+1].val: return False
                nqueue.append(queue[i].left); nqueue.append(queue[i+1].right)
                nqueue.append(queue[i].right); nqueue.append(queue[i+1].left)
            queue = nqueue
        return True
    
    """ 0112. 路径总和 给定一棵树, 判断是否有一条从根到叶子节点的路径使其和为target
思路1: 递归写法
思路2: 还可以展开为非递归, 例如用一个栈记录经过的节点, 在入栈时更新节点的val属性即可.
"""
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        # 递归写法
        def f(root: TreeNode, targetSum: int) -> bool:
            if root is None: return False
            # 检查是否为叶子节点
            if root.left is None and root.right is None:
                return targetSum==root.val
            return f(root.left, targetSum-root.val) or f(root.right, targetSum-root.val)
        return f(root, targetSum)
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        # 用一个栈记录经过的节点, 在入栈时更新节点的val属性
        if root is None: return False
        stack = [root]
        while stack:
            a = stack.pop()
            if a.left is None and a.right is None and a.val==targetSum: return True
            if a.left: a.left.val = a.val+a.left.val; stack.append(a.left)
            if a.right: a.right.val = a.val+a.right.val; stack.append(a.right)
        return False

    """ 0106. 从中序与后序遍历序列构造二叉树 
给定一棵二叉树的中序和后序遍历, 重构. 限制: 节点数 3000. 所有节点的值互不相同.
思路1: 利用后序和中序遍历的性质
    由于后序遍历的最后一个元素必然为root, 可以根据这样信息进行二分. 假设知道了中序遍历中左子树的部分, 则后序遍历对应长度的连续片段也可以找到.
    递归函数 `f(il,ir, pl,pr)` 匹配 `inorder[il...ir]` and `postorder[pl...pr]`, 返回构造出来的跟节点. 跟节点必然为 postorder[pr], 假设其在inorder出现的位置是idx.
    则inorder的前 len=idx-il 个节点对应的是左子树, postorder的前len个也对应左子树; 右子树是剩余部分.
"""
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        n = len(inorder)
        in2idx = dict(zip(inorder, range(n)))
        def f(il,ir, pl,pr):
            if il>ir: return None
            # 注意下面这条可以省略, 但上面这一条边界不能省!
            if il==ir: return TreeNode(inorder[il])
            root = TreeNode(postorder[pr])
            idx = in2idx[postorder[pr]]
            ll = idx-il
            root.left = f(il,idx-1, pl,pl+ll-1)
            root.right = f(idx+1,ir, pl+ll,pr-1)
            return root
        return f(0,n-1, 0,n-1)
    """ 0105. 从前序与中序遍历序列构造二叉树 题设类似上题. 
思路也类似, 利用「前序遍历的第一个正是跟节点」 """
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        n = len(preorder)
        in2idx = dict(zip(inorder, range(n)))
        def f(pl,pr, il,ir) -> TreeNode:
            if pl>pr: return None
            if pl==pr: return TreeNode(preorder[pl])
            root = TreeNode(preorder[pl])
            idx = in2idx[preorder[pl]]
            ll = idx-il
            root.left = f(pl+1,pl+ll, il,idx-1)
            root.right = f(pl+ll+1,pr, idx+1,ir)
            return root
        return f(0,n-1, 0,n-1)

    """ 0116. 填充每个节点的下一个右侧节点指针
给定一棵完美二叉树, 给每个节点设置next指针, 指向同层节点从左到右的下一个节点.
限制: 进阶要求是, 使用常量级额外空间 (递归调用的栈空间不算).
思路1: 递归实现. 需要利用到, 在当前节点进行递归的时候, a.next 指针已经是正确的了
思路2: 采用 #BFS. 但由于有了 next 指针, 所以不需要队列来记录同层信息了
"""
    def connect(self, root: 'Optional[Node]') -> 'Optional[Node]':
        # 思路1: 递归实现
        def f(a: Node):
            # 维护a下一层的next指针, 注意调用时 a.next 是正确的.
            if a is None: return
            if a.left is None: return
            # 维护下一层节点的next指针; 注意此时a 的next指针已经设置好了
            a.left.next = a.right
            a.right.next = a.next.left if a.next is not None else None
            # 递归调用
            f(a.left)
            f(a.right)  # 注意, 即使a.next is None, 也要调用f(a.right) !!!
        f(root)
        return root
    def connect(self, root: 'Optional[Node]') -> 'Optional[Node]':
        # 其实就是 BFS, 但由于有了 next 指针, 所以不需要队列来记录同层信息了
        # 下一题写得更清晰
        head = root
        while head:
            if head.left is None: break
            nxtHead = head.left
            cur = head      # 为了让变量名的含义更清晰
            while cur:
                cur.left.next = cur.right
                if cur.next:
                    cur.right.next = cur.next.left
                cur = cur.next
            head = nxtHead
        return root
    
    """ 0117. 填充每个节点的下一个右侧节点指针 II 相较于上一题, 不再是完美二叉树
思路1:  采用 #BFS. 如何下一层中节点的pre是谁? 另外用一个链表来记录 下一层节点的next关系
"""
    def connect(self, root: 'Node') -> 'Node':
        head = root
        while head:
            # 另外用一个链表来记录 下一层节点的next关系
            dummy = chain = Node(0)
            cur = head
            while cur:
                if cur.left:
                    chain.next = cur.left; chain = chain.next
                if cur.right:
                    chain.next = cur.right; chain = chain.next
                cur = cur.next
            head = dummy.next
        return root
    
    """ 0236. 二叉树的最近公共祖先 #medium #题型 给定二叉树上的两个节点, 找到它们的最短公共祖先
思路1: 得到每个节点的father, 直接得到路径!
    根据两个点的从跟节点出发的路径, 求交.
思路2: DFS返回 p/q 是否在该子树中
[灵神](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/solution/fen-lei-tao-lun-luan-ru-ma-yi-ge-shi-pin-2r95/)
"""


""" 0297. 二叉树的序列化与反序列化 #hard #题型 要求将一个二叉树序列化 (serialize) 和反序列化. 也即用无损的字符串表示二叉树. 限制: 节点数 1e4, 注意可能为 None
思路: 采用任意的 BFS/DFS/前序 等遍历方式均可, 注意在解码的时候, 按照相同的顺序进行还原.
[官答](https://leetcode.cn/problems/serialize-and-deserialize-binary-tree/solution/er-cha-shu-de-xu-lie-hua-yu-fan-xu-lie-hua-by-le-2/)
参见 [LeetCode 序列化二叉树的格式](https://support.leetcode-cn.com/hc/kb/article/1567641/) 其表示更简化一些. (本质上就是BFS)
"""
class Codec:
    def serialize(self, root):
        if root is None: return "#" # 边界
        # 采用BFS顺序 进行序列化和反序列化
        data = str(root.val) + ","
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for a in [node.left, node.right]:
                if a is None: data += "#,"
                else:
                    data += str(a.val) + ","
                    queue.append(a)
        return data[:-1]
    
    def deserialize(self, data):
        if data == "#": return None
        data = data.split(",")
        root = TreeNode(int(data[0]))
        idx = 1
        q = deque([root])
        while q:
            node = q.popleft()
            lv = data[idx]; idx+=1
            rv = data[idx]; idx+=1
            if lv!='#':
                l = TreeNode(int(lv))
                node.left = l; q.append(l)
            if rv!='#':
                r = TreeNode(int(rv))
                node.right = r; q.append(r)
        return root
            

sol = Solution()
data = "1,2,3,#,#,4,#,#,5,#,#"
codec = Codec()

result = [
    codec.serialize(codec.deserialize(data)),
]
for r in result:
    print(r)
