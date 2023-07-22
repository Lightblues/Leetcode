from easonsi import utils
from easonsi.util.leetcode import *
""" 链表相关
技巧
    挺乱的, 没有硬性要求的话可以转为列表, 或者记录val之间的交换
    指针非常乱, 写代码前在纸上画一下.

2058. 找出临界点之间的最小和最大距离 #medium #链表
    给定一个链表, 定义关键点为局部(严格的)极小/极大值, 要求返回这些关键点之间距离的最小和最大值.


2074. 反转偶数长度组的节点 #medium #链表 #题型
    给定一个链表, 将其分割成 1,2,3... 长的子序列 (最后一个剩余的长度可以不符合). 对于这些子序列, 反转其中长度为偶数的.


0146. LRU 缓存 #medium #hard
"""

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def printList(self):
        res = [self.val]
        now = self
        while now.next:
            now = now.next
            res.append(now.val)
        print(res)

def list2linked(l):
    """ 将 [1,3,2,4] 这样形式的列表转换为 ListNode 链表 """
    if not l: return None
    head = ListNode(l[0])
    cur = head
    for i in range(1, len(l)):
        cur.next = ListNode(l[i])
        cur = cur.next
    return head

def linked2list(head: ListNode):
    l = []
    while head:
        l.append(head.val)
        head = head.next
    return l



class Solution:
    """ 2058. 找出临界点之间的最小和最大距离 #medium #链表
给定一个链表, 定义关键点为局部(严格的)极小/极大值, 要求返回这些关键点之间距离的最小和最大值.
例如, head = [5,3,1,2,5,1,2] 这一链表的关键点位置在 2,4,5, 因此返回 [1,3]
思路1: 模拟遍历
    自己的思路是每次仅关注到当前遍历的节点, 因此需要记录上一个节点的值, 以及上一个节点与当前节点的大小比较.
    而 [answer](https://leetcode.cn/problems/find-the-minimum-and-maximum-number-of-nodes-between-critical-points/solution/zhao-chu-lin-jie-dian-zhi-jian-de-zui-xi-b08v/) 中, 
    使用 `cur.next.next.val` 来获取连续三个节点的值, 更为方便, 而不需要记录历史信息. 从代码上更为简洁.
"""
    def nodesBetweenCriticalPoints(self, head: Optional[ListNode]) -> List[int]:
        minDist = maxDist = -1
        first = last = -1
        pos = 0

        cur = head
        while cur.next.next:
            # 获取连续的三个节点的值
            x, y, z = cur.val, cur.next.val, cur.next.next.val
            # 如果 y 是临界点
            if y > max(x, z) or y < min(x, z):
                if last != -1:
                    # 用相邻临界点的距离更新最小值
                    minDist = (pos - last if minDist == -1 else min(minDist, pos - last))
                    # 用到第一个临界点的距离更新最大值
                    maxDist = max(maxDist, pos - first)
                if first == -1:
                    first = pos
                # 更新上一个临界点
                last = pos
            cur = cur.next
            pos += 1
        
        return [minDist, maxDist]


    """ 0206. 反转链表 #easy #题型 给定一个链表, 将其反转. [z-reverse]
思路1: 迭代. 经典实现. 维护 pre,cur,next 三个指针会比较清晰.
思路2: 递归 实现
思路3: 能否再减少一个指针? 在 #双指针 思路中, 不移动 head 而在遍历过程中修改 head.next 所指向的节点.
    参见 2074
    from [here](https://leetcode.cn/problems/reverse-linked-list/solution/fan-zhuan-lian-biao-shuang-zhi-zhen-di-gui-yao-mo-/) 
[官答](https://leetcode.cn/problems/reverse-linked-list/solution/fan-zhuan-lian-biao-by-leetcode-solution-d1k2/)
"""
    def reverseList(self, head: ListNode) -> ListNode:
        # 思路3: 只有两个指针
        cur = head
        while head.next:
            # 一般写法
            # t = head.next.next
            # head.next.next, cur  = cur, head.next
            # head.next = t
            
            # 注意! 这样会出问题. 
            # 因为 LHS中, 先对于 head.next 进行了赋值, 这样 head.next.next 中的 head.next 就变了!!!
            # head.next, head.next.next, cur  = head.next.next, cur, head.next
            # 这样就没问题了
            head.next.next, head.next, cur  = cur, head.next.next, head.next
        return cur

    """ 2074. 反转偶数长度组的节点 #medium #链表 #题型
给定一个链表, 将其分割成 1,2,3... 长的子序列 (最后一个剩余的长度可以不符合). 对于这些子序列, 反转其中长度为偶数的.
思路1: 暴力模拟. 完全按照 #链表 的思路来写
    救命, 这题写了两个小时.
    思路是实现一个翻转 [i,j] 范围内节点的函数 (同时要求连上 i-1, j+1); 然后遍历
    然而如何判断最后剩余的长度是否为偶数呢? 自己的思路尝试用一次遍历用指针记录, 但是极为繁琐 (还不可行)
思路2: 针对第二个问题, 放弃了整合在一次遍历的想法. 而是通过两次遍历: 第一次判断剩余是否为偶数. 然后在确实下一个目标序列的奇偶性的前提下进行翻转
    总体来看, 只需要维护 pre, cur 两个指针即可. 1) 若当前长度 i 为奇数, 将两者都前进i步即可; 2) 若为偶数, 则需要实现「将从cur开始的i个节点进行翻转」, 见下代码.
    [官方](https://leetcode.cn/problems/reverse-nodes-in-even-length-groups/solution/fan-zhuan-ou-shu-chang-du-zu-de-jie-dian-owra/) 
    """
    def reverseEvenLengthGroups(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """ [官方](https://leetcode.cn/problems/reverse-nodes-in-even-length-groups/solution/fan-zhuan-ou-shu-chang-du-zu-de-jie-dian-owra/) 
        采用了两次遍历
        """
        i = 0
        cur, pre = head, None
        while cur:
            # i 是每一轮的目标序列长度
            i += 1
            
            # 第一次遍历, 检查剩余链表长度是否够满 i 个
            it = cur
            length = 0
            while length < i and it:
                length += 1
                it = it.next
            
            # 第二次遍历, 根据是否需要翻转:
            # 若序列长度为奇数, 直接将 pre, cur 移动到下一个序列
            if length & 1:
                for j in range(length):
                    pre, cur = cur, cur.next
            # 若序列长度为偶数, 需要翻转
            else:
                # version1: 官方的神奇代码
                for j in range(length - 1):
                    pre.next, cur.next.next, cur.next = cur.next, pre.next, cur.next.next
                pre, cur = cur, cur.next
                
                #  version2: 笨拙实现.
                # prevRecord = pre
                # pre, cur = cur, cur.next
                # for j in range(length-1):
                #     next = cur.next
                #     cur.next = pre
                #     pre, cur = cur, next
                # # 注意这里的pre!! 防止出现循环
                # pre, prevRecord.next.next, prevRecord.next = prevRecord.next, cur, pre
                
        return head


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

sol = Solution()
result = [
    linked2list(sol.reverseList(list2linked([1,2,3,4,5]))),
    
    # linked2list(sol.reverseEvenLengthGroups(head = list2linked(
    #     # [5,2,6,3,9,1,7,3,8,4]
    #     # [1,1,0,6]
    #     [1,1,0,6,5])
    # )),

]
for r in result:
    print(r)
