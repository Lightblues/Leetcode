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
0237. 删除链表中的节点 https://leetcode.cn/problems/delete-node-in-a-linked-list/solutions/2004056/ru-he-shan-chu-jie-dian-liu-fen-zhong-ga-x3kn/
0019. 删除链表的倒数第 N 个结点 https://leetcode.cn/problems/remove-nth-node-from-end-of-list/solutions/2004057/ru-he-shan-chu-jie-dian-liu-fen-zhong-ga-xpfs/
0083. 删除排序链表中的重复元素 https://leetcode.cn/problems/remove-duplicates-from-sorted-list/solutions/2004062/ru-he-qu-zhong-yi-ge-shi-pin-jiang-tou-p-98g7/
0082. 删除排序链表中的重复元素 II https://leetcode.cn/problems/remove-duplicates-from-sorted-list-ii/solutions/2004067/ru-he-qu-zhong-yi-ge-shi-pin-jiang-tou-p-2ddn/
课后作业：
0203. 移除链表元素 https://leetcode.cn/problems/remove-linked-list-elements/

Easonsi @2023 """

# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
class Solution:
    """ 0237. 删除链表中的节点 #medium 只给定需要删除节点的指针, 如何删除? 题目保证了该节点不是尾节点
思路1: 转换思路, 将下一个节点的val赋值给当前节点, 然后删除下一个节点
"""
    def deleteNode(self, node):
        node.val = node.next.val
        node.next = node.next.next
    
    """ 0019. 删除链表的倒数第 N 个结点 #medium #题型
思路1: 让第一个指针先走n步. 然后两个指针一起走.
    优化: 一个技巧是, 在头上采用 #dummy 节点. 这样就不会发生越界了!
思路0: 官答中还提出了 1) 计算链表长度; 2) 使用栈 的方法.
[官答](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/solution/shan-chu-lian-biao-de-dao-shu-di-nge-jie-dian-b-61/)
 """
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        # 倒数N个可能是head, 所以用dummy
        dummy = ListNode(next=head)
        right = dummy
        for _ in range(n): right = right.next
        left = dummy    # right = left+n 
        while right.next:
            left = left.next
            right = right.next
        left.next = left.next.next
        return dummy.next
    
    """ 0083. 删除排序链表中的重复元素 #easy 链表已排序, 删除链表中的重复元素
思路1: 左右指针
思路2: 只用cur指针, 通过不断「删除下一个节点」来实现
"""
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 思路1: 左右指针
        if not head: return head    # 边界
        left = head; right = head.next
        while right:
            if left.val!=right.val:
                left.next = right
                left = right
            right = right.next
        left.next = None    # 注意去掉最后的部分
        return head
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 思路2: 只用cur指针, 通过不断「删除下一个节点」来实现
        if head is None: return None        # 没有dummy, 要考虑边界
        cur = head
        while cur.next:
            if cur.val==cur.next.val:   # 删除cur的下一个节点
                cur.next = cur.next.next
            else:
                cur = cur.next
        return head
    """ 0082. 删除排序链表中的重复元素 II #medium 相较于 0083, 对于出现过的重复的元素, 删除全部. 例如 [1,2,2,3] -> [1,3]
思路1: 检查cur后面的两个元素, 1] 若相等, 则删除所有带这个val的元素; 2] 否则, 移动cur到下一个节点
 """
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(next=head) # 因为头可能要删掉
        cur = dummy
        # 下面的代码比较 0083 思路2
        while cur.next and cur.next.next:
            if cur.next.val==cur.next.next.val:
                val = cur.next.val
                # 不断删除值为 val 的节点!
                while cur.next and cur.next.val==val:   # 注意这里考虑 cur.next 可能为空的情况
                    cur.next = cur.next.next
            else:
                cur = cur.next
        return dummy.next
    
    
    """ 0203. 移除链表元素 #easy """
    def removeElements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        dummy = ListNode(next=head)
        cur = dummy
        while cur.next:
            if cur.next.val==val:
                cur.next = cur.next.next
            else:
                cur = cur.next
        return dummy.next
    
    
    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
