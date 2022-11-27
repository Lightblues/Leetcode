from easonsi import utils
from easonsi.util.leetcode import *

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


""" 解析LC格式的树结构
关联: 0297. 二叉树的序列化与反序列化 #hard
参见 [LeetCode 序列化二叉树的格式](https://support.leetcode-cn.com/hc/kb/article/1567641/)
"""
def parseLCBinaryTree(data):
    """ 解析形如 '[1,2,3,null,null,4,5]' 这样的LC树结构 """
    if data == "[]": return None
    data = data[1:-1].split(",")
    n = len(data)
    root = TreeNode(int(data[0]))
    idx = 1
    q = deque([root])
    while q:
        node = q.popleft()
        if idx >= n: break
        lv = data[idx]; idx+=1
        if lv!='null':
            l = TreeNode(int(lv))
            node.left = l; q.append(l)
        if idx >= n: break
        rv = data[idx]; idx+=1
        if rv!='null':
            r = TreeNode(int(rv))
            node.right = r; q.append(r)
    return root

def printLCBinaryTree(root):
    """ 打印形如 '[1,2,3,null,null,4,5]' 这样的LC树结构 """
    if not root: return "[]"
    q = deque([root])
    res = []
    while q:
        node = q.popleft()
        if node:
            res.append(str(node.val))
            q.append(node.left)
            q.append(node.right)
        else:
            res.append("null")
    # 删除最后的可能多余的null
    while res[-1] == "null":
        res.pop()
    return f"[{','.join(res)}]"




def list2LinkedList(data):
    """ 根据 [5,2,13,3,8] 的列表构造链表 """
    if isinstance(data, str): data = eval(data)
    dummy = p = ListNode()
    for val in data:
        p.next = ListNode(val)
        p = p.next
    return dummy.next

def linkedList2List(head: ListNode):
    """ 根据链表构造列表 """
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res


root = parseLCBinaryTree('[1,2,3,null,null,4,5]')
print(printLCBinaryTree(root))
root = parseLCBinaryTree('[6,2,13,1,4,9,15,null,null,null,null,null,null,14]')
print(printLCBinaryTree(root))