
""" 增加了用一个数组来初始化, 复杂度 O(n)
用一个数组来初始化树状数组, 这里 idx 从 1 开始
add(self, idx, delta): 在 idx 处添加 delta
getPrefixSum(self, idx): 返回到 idx 的前缀和
getRangeSum(self, l, r): 返回 [l, r] 的和
 """
def lowbit(x): return x & -x
class BinaryIndexedTree:
    def __init__(self, l) -> None:
        # 根据数组 l 进行初始化

        # 这种初始化需要 O(nlogn)
        # self.l = [0] * (len(l) + 1)
        # for i in range(len(l)):
        #     self.add(i+1, l[i])
        
        # 这样复杂度 O(n) [实际上就是简化了重复的累加操作]
        self.l = [0] * (len(l) + 1)
        for i in range(len(l)):
            self.l[i+1] = l[i]
        for i in range(1, len(l)+1):
            j = i + lowbit(i)
            if j <= len(l):
                self.l[j] = self.l[j] + self.l[i]
        
        # 这种初始化需要 O(nlogn)
        self.l = [0] * (len(l) + 1)
        for i in range(len(l)):
            self.add(i+1, l[i])

    def add(self, idx, delta):
        # 对于 idx 位置的元素 +delta
        # idx += 1
        while idx < len(self.l):
            self.l[idx] += delta
            idx += lowbit(idx)
    
    def getPrefixSum(self, idx):
        # 计算 0...idx 的和
        # idx += 1
        ret = 0
        while idx > 0:
            ret += self.l[idx]
            idx -= lowbit(idx)
        return ret

    def getRangeSum(self, l, r):
        return self.getPrefixSum(r) - self.getPrefixSum(l-1)


def loj130():
    """ https://loj.ac/p/130 130. 树状数组 1 ：单点修改，区间查询
    第一行两个数 n,q 表示数组大小和查询次数
    第二行为数组初始化
    下面 q 行为查询, (1) 1 i x：给定 i 和 x, 将 i 位置的元素 +x; (2) 2 l r：求区间 [l,r] 的和
    注意这里 1 <= l,r <= n, 即从 1 开始计数

    Input:
    3 2
    1 2 3
    1 2 0
    2 1 3

    output:
    6
    """
    n,q = map(int, input().split())
    t = BinaryIndexedTree(list(map(int, input().split())))
    for i in range(q):
        cmd,x,y = map(int, input().split())
        if cmd == 1:
            t.add(x, y)
        else:
            print(t.getRangeSum(x, y))