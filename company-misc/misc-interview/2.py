""" 二叉树的非递归后序遍历

 """

class Node:
    def __init__(self) -> None:
        self.val = None
        self.left = None
        self.right = None

def dfs(node):
    if not node:
        return
    stack = []
    stack.append(node)
    while stack:
        node = stack.pop()
        print(node.val)
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
