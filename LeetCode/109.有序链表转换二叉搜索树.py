#
# @lc app=leetcode.cn id=109 lang=python3
#
# [109] 有序链表转换二叉搜索树
#

# @lc code=start
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    """ 0109. 有序链表转换二叉搜索树 #medium 给定一个单向有序链表, 将其转化为高度平衡的二叉搜索树.
限制: n 2e4
思路1: #分治 O(nlogn)
    显然, 我们可以将中位数作为root; 然后左右两边的链表分别递归构建左右子树.
    因此, 对于 [left,right), 我们需要找到其中点. 可以利用 #快慢指针 来找到
        具体而言, 可以实现函数 findMedium(left, right)
    时间复杂度: 考虑到分治特点, 每一层累计的复杂度为 O(n). 深度为分治高度, 因此整体 O(nlogn)
思路2: #分治 + 中序遍历优化 O(n)
    考虑简单的: 「对于一个列表, 如何转为搜索树?」
        我们可以将中间位置作为root, 然后左右两边的列表分别递归构建左右子树.
    如何对于链表呢? 只能顺序移动获取val!
        此时, 我们可以类似DFS地考虑 [0,4] -> 2, [0,1] -> 1, [0] 选择中间节点, 缩减左边的区间; 处理当前head; 再处理右边区间
    复杂度: 只需要过一次链表 (中序遍历)
[官答](https://leetcode.cn/problems/convert-sorted-list-to-binary-search-tree/solution/you-xu-lian-biao-zhuan-huan-er-cha-sou-suo-shu-1-3/)
"""
    def sortedListToBST(self, head: Optional[ListNode]) -> Optional[TreeNode]:
        # 思路1: #分治 O(nlogn)
        def findMedium(left, right):
            # 找到 [left,right) 区间的中点
            slow = fast = left
            while fast!=right and fast.next!=right:
                slow = slow.next
                fast = fast.next.next
            return slow
        def build(left,right):
            # 构建这一范围内的搜索树
            if left==right: return None
            mid = findMedium(left, right)
            root = TreeNode(mid.val)
            root.left = build(left, mid)
            root.right = build(mid.next, right)
            return root
        return build(head, None)
    def sortedListToBST(self, head: Optional[ListNode]) -> Optional[TreeNode]:
        # 思路2: #分治 + 中序遍历优化 O(n)
        def getLen(head):
            res = 0
            while head: res+= 1; head = head.next
            return res
        l = getLen(head)
        def build(left, right):
            # [left, right] 闭区间
            if left>right: return None  # 边界条件
            # mid = (left+right)//2       # 选择中点作为根节点, 下面也可以
            mid = (left+right+1)//2 
            root = TreeNode()   # 此时并不知道 mid 节点的值
            root.left = build(left, mid-1)
            nonlocal head
            root.val = head.val
            head = head.next    # 递归过程中, head 会不断向后移动
            root.right = build(mid+1, right)
            return root         # 函数返回的时候, head 指向 left+1
        return build(0, l-1)
    def sortedListToBST(self, head):
        # 思路1.1 直接修改链表指针的方式! 
        if not head:
            return 
        if not head.next:
            return TreeNode(head.val)
        # here we get the middle point,
        # even case, like '1234', slow points to '2',
        # '3' is root, '12' belongs to left, '4' is right
        # odd case, like '12345', slow points to '2', '12'
        # belongs to left, '3' is root, '45' belongs to right
        slow, fast = head, head.next.next
        while fast and fast.next:
            fast = fast.next.next
            slow = slow.next
        # tmp points to root
        tmp = slow.next
        # cut down the left child
        slow.next = None
        root = TreeNode(tmp.val)
        root.left = self.sortedListToBST(head)
        root.right = self.sortedListToBST(tmp.next)
        return root
# @lc code=end

