from typing import List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
    def toList(self):
        # 按照题目要求的形式输出? 虽然也不知道题目输出是按照什么遍历的
        def printNode(node: TreeNode, numList: list =[]) -> list:
            if node == None:
                numList.append(None)
            else:
                numList.append(node.val)
                if node.left:
                    printNode(node.left, numList=numList)
                    printNode(node.right, numList=numList)
            return numList
        return printNode(self)


class Solution:
    def generateTrees(self, n: int) -> List[TreeNode]:
        return self.generateBSTree(1, n)
    def generateBSTree(self, start: int, end: int) -> List[TreeNode]:
        res = []
        if start > end:
            return [None]
        for i in range(start, end+1):
            left = self.generateBSTree(start, i-1)
            right = self.generateBSTree(i+1, end)
            for l in left:
                for r in right:
                    root = TreeNode(i, l, r)
                    res.append(root)
        return res

tree = Solution().generateTrees(3)
print(len(tree))
for t in tree:
    l = t.toList()
    print(l)
