"""
两个非空链表表示两个非负整数，逆序存储
将两数相加，返回一个形式相同的数字

输入：l1 = [2,4,3], l2 = [5,6,4]
输出：[7,0,8]
解释：342 + 465 = 807.
"""

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

def genNode(l):
    root = ListNode(val=l[0])
    pre = root
    for num in l[1:]:
        now = ListNode(val=num)
        pre.next = now
        pre = now
    return root

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        # 引入一个值为零的节点，没有 next
        zeroNote = ListNode(val=0, next=None)
        up, res = (l1.val+l2.val)//10, (l1.val+l2.val)%10
        result = ListNode(val=res)    # 先初始化
        pre = result
        while l1.next or l2.next or up:
            # 循环判断条件：（注意这里引入了一个 zeroNode 便于分析）当任意一个列表还有元素，或者有进位时继续
            l1 = l1.next if l1.next else zeroNote
            l2 = l2.next if l2.next else zeroNote
            up, res = (l1.val+l2.val+up)//10, (l1.val+l2.val+up)%10
            new = ListNode(val=res)
            pre.next = new
            pre = new
        return result

s = Solution()
l1 = [2,4,3]; l2 = [5,6,4]

l1, l2 = genNode(l1), genNode(l2)
r = s.addTwoNumbers(l1, l2)
r.printList()