
""" 
题目: 0547, 0399
*   「力扣」第 547 题：[省份数量](https://leetcode-cn.com/problems/number-of-provinces)（中等）；
*   「力扣」第 684 题：[冗余连接](https://leetcode-cn.com/problems/redundant-connection)（中等）；
*   「力扣」第 1319 题：[连通网络的操作次数](https://leetcode-cn.com/problems/number-of-operations-to-make-network-connected)（中等）；
*   「力扣」第 1631 题：[最小体力消耗路径](https://leetcode-cn.com/problems/path-with-minimum-effort)（中等）；
*   「力扣」第 959 题：[由斜杠划分区域](https://leetcode-cn.com/problems/regions-cut-by-slashes)（中等）；
*   「力扣」第 1202 题：[交换字符串中的元素](https://leetcode-cn.com/problems/smallest-string-with-swaps)（中等）；
*   「力扣」第 947 题：[移除最多的同行或同列石头](https://leetcode-cn.com/problems/most-stones-removed-with-same-row-or-column)（中等）；
*   「力扣」第 721 题：[账户合并](https://leetcode-cn.com/problems/accounts-merge)（中等）；
*   「力扣」第 803 题：[打砖块](https://leetcode-cn.com/problems/bricks-falling-when-hit)（困难）；
*   「力扣」第 1579 题：[保证图可完全遍历](https://leetcode-cn.com/problems/remove-max-number-of-edges-to-keep-graph-fully-traversable)（困难）;
*   「力扣」第 778 题：[水位上升的泳池中游泳](https://leetcode-cn.com/problems/swim-in-rising-water)（困难）
"""

class UnionFind:
    # https://leetcode.cn/problems/number-of-provinces/solution/python-duo-tu-xiang-jie-bing-cha-ji-by-m-vjdr/
    def __init__(self):
        """
        记录每个节点的父节点
        """
        self.father = {}
    
    def find(self,x):
        """
        查找根节点
        路径压缩
        """
        root = x

        while self.father[root] != None:
            root = self.father[root]

        # 路径压缩
        while x != root:
            original_father = self.father[x]
            self.father[x] = root
            x = original_father
         
        return root
    
    def merge(self,x,y,val):
        """
        合并两个节点
        """
        root_x,root_y = self.find(x),self.find(y)
        
        if root_x != root_y:
            self.father[root_x] = root_y

    def is_connected(self,x,y):
        """
        判断两节点是否相连
        """
        return self.find(x) == self.find(y)
    
    def add(self,x):
        """
        添加新节点
        """
        if x not in self.father:
            self.father[x] = None

