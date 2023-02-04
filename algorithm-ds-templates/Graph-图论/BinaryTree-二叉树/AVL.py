class AVL:
    """平衡二叉搜索树（AVL树）：允许重复值
    https://leetcode.cn/problems/kth-smallest-element-in-a-bst/solution/er-cha-sou-suo-shu-zhong-di-kxiao-de-yua-8o07/
    """

    class Node:
        """平衡二叉搜索树结点"""
        __slots__ = ("val", "parent", "left", "right", "size", "height")

        def __init__(self, val, parent=None, left=None, right=None):
            self.val = val
            self.parent = parent
            self.left = left
            self.right = right
            self.height = 0  # 结点高度：以node为根节点的子树的高度（高度定义：叶结点的高度是0）
            self.size = 1  # 结点元素数：以node为根节点的子树的节点总数

    def __init__(self, vals):
        self.root = self._build(vals, 0, len(vals) - 1, None) if vals else None

    def _build(self, vals, l, r, parent):
        """根据vals[l:r]构造平衡二叉搜索树 -> 返回根结点"""
        m = (l + r) // 2
        node = self.Node(vals[m], parent=parent)
        if l <= m - 1:
            node.left = self._build(vals, l, m - 1, parent=node)
        if m + 1 <= r:
            node.right = self._build(vals, m + 1, r, parent=node)
        self._recompute(node)
        return node

    def kth_smallest(self, k: int) -> int:
        """返回二叉搜索树中第k小的元素"""
        node = self.root
        while node:
            left = self._get_size(node.left)
            if left < k - 1:
                node = node.right
                k -= left + 1
            elif left == k - 1:
                return node.val
            else:
                node = node.left

    def insert(self, v):
        """插入值为v的新结点"""
        if self.root is None:
            self.root = self.Node(v)
        else:
            # 计算新结点的添加位置
            node = self._subtree_search(self.root, v)
            is_add_left = (v <= node.val)  # 是否将新结点添加到node的左子结点
            if node.val == v:  # 如果值为v的结点已存在
                if node.left:  # 值为v的结点存在左子结点，则添加到其左子树的最右侧
                    node = self._subtree_last(node.left)
                    is_add_left = False
                else:  # 值为v的结点不存在左子结点，则添加到其左子结点
                    is_add_left = True

            # 添加新结点
            leaf = self.Node(v, parent=node)
            if is_add_left:
                node.left = leaf
            else:
                node.right = leaf

            self._rebalance(leaf)

    def delete(self, v) -> bool:
        """删除值为v的结点 -> 返回是否成功删除结点"""
        if self.root is None:
            return False

        node = self._subtree_search(self.root, v)
        if node.val != v:  # 没有找到需要删除的结点
            return False

        # 处理当前结点既有左子树也有右子树的情况
        # 若左子树比右子树高度低，则将当前结点替换为右子树最左侧的结点，并移除右子树最左侧的结点
        # 若右子树比左子树高度低，则将当前结点替换为左子树最右侧的结点，并移除左子树最右侧的结点
        if node.left and node.right:
            if node.left.height <= node.right.height:
                replacement = self._subtree_first(node.right)
            else:
                replacement = self._subtree_last(node.left)
            node.val = replacement.val
            node = replacement

        parent = node.parent
        self._delete(node)
        self._rebalance(parent)
        return True

    def _delete(self, node):
        """删除结点p并用它的子结点代替它，结点p至多只能有1个子结点"""
        if node.left and node.right:
            raise ValueError('node has two children')
        child = node.left if node.left else node.right
        if child is not None:
            child.parent = node.parent
        if node is self.root:
            self.root = child
        else:
            parent = node.parent
            if node is parent.left:
                parent.left = child
            else:
                parent.right = child
        node.parent = node

    def _subtree_search(self, node, v):
        """在以node为根结点的子树中搜索值为v的结点，如果没有值为v的结点，则返回值为v的结点应该在的位置的父结点"""
        if node.val < v and node.right is not None:
            return self._subtree_search(node.right, v)
        elif node.val > v and node.left is not None:
            return self._subtree_search(node.left, v)
        else:
            return node

    def _recompute(self, node):
        """重新计算node结点的高度和元素数"""
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        node.size = 1 + self._get_size(node.left) + self._get_size(node.right)

    def _rebalance(self, node):
        """从node结点开始（含node结点）逐个向上重新平衡二叉树，并更新结点高度和元素数"""
        while node is not None:
            old_height, old_size = node.height, node.size
            if not self._is_balanced(node):
                node = self._restructure(self._tall_grandchild(node))
                self._recompute(node.left)
                self._recompute(node.right)
            self._recompute(node)
            if node.height == old_height and node.size == old_size:
                node = None  # 如果结点高度和元素数都没有变化则不需要再继续向上调整
            else:
                node = node.parent

    def _is_balanced(self, node):
        """判断node结点是否平衡"""
        return abs(self._get_height(node.left) - self._get_height(node.right)) <= 1

    def _tall_child(self, node):
        """获取node结点更高的子树"""
        if self._get_height(node.left) > self._get_height(node.right):
            return node.left
        else:
            return node.right

    def _tall_grandchild(self, node):
        """获取node结点更高的子树中的更高的子树"""
        child = self._tall_child(node)
        return self._tall_child(child)

    @staticmethod
    def _relink(parent, child, is_left):
        """重新连接父结点和子结点（子结点允许为空）"""
        if is_left:
            parent.left = child
        else:
            parent.right = child
        if child is not None:
            child.parent = parent

    def _rotate(self, node):
        """旋转操作"""
        parent = node.parent
        grandparent = parent.parent
        if grandparent is None:
            self.root = node
            node.parent = None
        else:
            self._relink(grandparent, node, parent == grandparent.left)

        if node == parent.left:
            self._relink(parent, node.right, True)
            self._relink(node, parent, False)
        else:
            self._relink(parent, node.left, False)
            self._relink(node, parent, True)

    def _restructure(self, node):
        """trinode操作"""
        parent = node.parent
        grandparent = parent.parent

        if (node == parent.right) == (parent == grandparent.right):  # 处理需要一次旋转的情况
            self._rotate(parent)
            return parent
        else:  # 处理需要两次旋转的情况：第1次旋转后即成为需要一次旋转的情况
            self._rotate(node)
            self._rotate(node)
            return node

    @staticmethod
    def _subtree_first(node):
        """返回以node为根结点的子树的第1个元素"""
        while node.left is not None:
            node = node.left
        return node

    @staticmethod
    def _subtree_last(node):
        """返回以node为根结点的子树的最后1个元素"""
        while node.right is not None:
            node = node.right
        return node

    @staticmethod
    def _get_height(node) -> int:
        """获取以node为根结点的子树的高度"""
        return node.height if node is not None else 0

    @staticmethod
    def _get_size(node) -> int:
        """获取以node为根结点的子树的结点数"""
        return node.size if node is not None else 0

