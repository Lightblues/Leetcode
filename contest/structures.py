from copy import deepcopy
from operator import ne

################# 定义 ##############################

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 二叉树
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

################# 链表 ##############################

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

def printLinked(head):
    """ 打印链表 """
    while head:
        print(head.val, end=' ')
        head = head.next
    print()
    
def reverse(head):
    """ 链表反转
    返回新的 head"""
    if not head: return None
    prev, cur = None, head
    while cur:
        next = cur.next
        cur.next = prev
        prev, cur = cur, next
    return prev

def reverseList2(head: ListNode) -> ListNode:
    """ 思路2: 双指针 """
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
    
def reverseInter(pre, cur, length):
    """ 反转链表的中, 从 cur 出发的长度为 length 的子链表 (并且要求与左右连起来, 或者说, 避免出现环) 
    注意是原地操作 """
    # version1: 官方的神奇代码
    # 在 length - 1 次遍历过程中, 不改变 pre, cur 指针, 而是利用 pre.next, cur.next 指向实际修改的元素
    for j in range(length - 1):
        # 每次修改 cur.next 节点的 next 指针
        # pre.next, cur.next 指向的元素每次都右移一格
        pre.next, cur.next.next, cur.next = cur.next, pre.next, cur.next.next
    pre, cur = cur, cur.next
    return

    #  version2: 笨拙实现.
    prevRecord = pre
    pre, cur = cur, cur.next
    for j in range(length-1):
        next = cur.next
        cur.next = pre
        pre, cur = cur, next
    # 注意这里的pre!! 防止出现循环
    pre, prevRecord.next.next, prevRecord.next = prevRecord.next, cur, pre



class LinkedList:
    """ 写一个类? 没必要 """
    def __init__(self, l=None):
        """ 用 [1,2,3] 初始化链表 """
        self.head = None
        if isinstance(l, list):
            head = ListNode()
            node = head
            for i in l:
                node.next = ListNode(i)
                node = node.next
            self.head = head.next
        elif isinstance(l, ListNode):
            self.head = l
    def __str__(self):
        """ 转为字符串 """
        cur = self.head
        res = []
        while cur:
            res.append(str(cur.val))
            cur = cur.next
        return "->".join(res)

if __name__=="__main__":
    res = []
    # 原始列表
    head = list2linked([1,2,3,4,5])
    res.append(head)
    # 翻转 (注意是原地操作)
    head = list2linked([1,2,3,4,5])
    # res.append(reverse(head))
    res.append(reverseList2(head))
    # 翻转从第2个元素开始的长度为2的子链表 
    head = list2linked([1,2,3,4,5])
    reverseInter(head, head.next, 2),
    res.append(
        head
    )

    for r in res:
        print(linked2list(r))