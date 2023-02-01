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
0876. 链表的中间结点 https://leetcode.cn/problems/middle-of-the-linked-list/solutions/1999265/mei-xiang-ming-bai-yi-ge-shi-pin-jiang-t-wzwm/
0141. 环形链表 https://leetcode.cn/problems/linked-list-cycle/solutions/1999269/mei-xiang-ming-bai-yi-ge-shi-pin-jiang-t-c4sw/
0142. 环形链表 II https://leetcode.cn/problems/linked-list-cycle-ii/solutions/1999271/mei-xiang-ming-bai-yi-ge-shi-pin-jiang-t-nvsq/
0143. 重排链表 https://leetcode.cn/problems/reorder-list/solutions/1999276/mei-xiang-ming-bai-yi-ge-shi-pin-jiang-t-u66q/
课后作业：
0234. 回文链表 https://leetcode.cn/problems/palindrome-linked-list/
Easonsi @2023 """
class ListNode:
    def __init__(self, x) -> None:
        self.val = x
        self.next = None
class Solution:
    """ 0876. 链表的中间结点 #easy 若长度为偶数, 则返回靠右的那个 """
    def middleNode(self, head: ListNode) -> ListNode:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow # 注意长度为偶数情况下的模拟
    
    """ 0141. 环形链表 #easy #题型 判断链表是否有环
思路0: 用哈希表记录
思路1: #快慢指针
    复杂度: O(n) 因为最多绕两圈.
"""
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if fast==slow: return True
        return False
    """ 0142. 环形链表 II #题型 #medium 相较于 0141, 需要返回进入环的第一个节点.
思路0: 用哈希表记录出现过的节点.
思路1: #快慢指针 复杂度 O(n)
    slow, fast 同时从起点走. 假设进入环的第一个点的距离是 a, 入环点和相遇点将环分割成长 b,c 两部分.
    假设fast在环上走了n圈, 则有 `a + (b+c)n + b = 2 * (a+b)`. 注意, 这里用到了结论「slow在环上 走不满一圈就会被 fast追到」
    于是有 `a-c = (b+c)(n-1) `. 
        因此, **让slow继续从相遇点走, 同时在起点放置一个速度也为1的指针, 他们恰好会在入环点相遇**.
    复杂度: O(n). 因为相遇时间是 O(n)
见图示 [official](https://leetcode.cn/problems/linked-list-cycle-ii/solution/huan-xing-lian-biao-ii-by-leetcode-solution/)
"""
    def detectCycle(self, head: ListNode) -> ListNode:
        # 思路1: #快慢指针
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if fast is slow:
                p = head
                while p is not slow:
                    slow = slow.next
                    p = p.next
                return p
        return None
    
    """ 0143. 重排链表 #medium 对于一个长n的链表, 重排为 1,n, 2,n-1, ...的形式
思路1: 找到中间节点, 反转后半部分, 然后合并两条链表.
    注意, 反转之后, 链表结构为 1->2->3<-4<-5 (其中3节点next为空) 或者 1->2->3<-4 的形式
    在奇数情况下, 合并的时候可能出现 head1=head2 的情况, 要注意避免死循环!!
[灵神](https://leetcode.cn/problems/reorder-list/solution/mei-xiang-ming-bai-yi-ge-shi-pin-jiang-t-u66q/)
 """
    def reorderList(self, head: Optional[ListNode]) -> None:
        # 0876. 链表的中间结点
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        # 0206. 反转链表
        pre,cur = None,slow
        while cur:
            nxt = cur.next
            cur.next = pre
            pre,cur = cur,nxt
        head2 = pre
        # 合并两条链表
        # 注意这里的边界条件!! 要避免 head, head2 同时指向最中间的元素, 导致死循环
        while head2.next:       # 判断: 
            nxt,nxt2 = head.next,head2.next
            head.next = head2
            head2.next = nxt
            head,head2 = nxt,nxt2
        # 原地修改, 不需要return
    
    """ 0234. 回文链表 #easy 判断链表是否回文
[官答](https://leetcode.cn/problems/reorder-list/solution/mei-xiang-ming-bai-yi-ge-shi-pin-jiang-t-u66q/)
"""
    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
