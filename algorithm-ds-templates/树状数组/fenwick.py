""" 
[树状数组](https://oi-wiki.org/ds/fenwick/) 参见 [here](https://blog.csdn.net/Yaokai_AssultMaster/article/details/79492190)
图参见上面的链接. 简言之, 希望 0100 能够存储数组中 0001-0100 四个位置之和 (从1开始计数), 1010能够存储 1001, 1010 两个位置数字之和
从而, 希望得到数组前 1010之和时, 能够进行分解 sum[1010] = l[1010] + l[1000]
要更新数组 1010位置的数字 (+某一数值), 则需要更新 1010, 1100 即每次加上最低1位 (这里假设 10000 超过了数组长度)

因此, 1. 求前缀和, 每次减去数字最低的数字1位, 累计; 2. 对某一个idx的数字更新, 每次加上最低数字1位, 直到数组最大长度.
"""

def lowbit(x):
    """
    x 的二进制表示中，最低位的 1 的位置。
    lowbit(0b10110000) == 0b00010000
             ~~~^~~~~
    lowbit(0b11100100) == 0b00000100
             ~~~~~^~~
    """
    return x & -x

""" 用一个数组来初始化树状数组, 这里 idx 从 1 开始
add(self, idx, delta): 在 idx 处添加 delta
getPrefixSum(self, idx): 返回到 idx 的前缀和
getRangeSum(self, l, r): 返回 [l, r] 的和
 """
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

""" https://loj.ac/p/130 #130. 树状数组 1 ：单点修改，区间查询

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