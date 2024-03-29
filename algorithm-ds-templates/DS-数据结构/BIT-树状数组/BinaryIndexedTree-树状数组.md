树状数组或二叉索引树（Binary Indexed Tree），又以其发明者命名为 Fenwick 树。其初衷是解决数据压缩里的累积频率的计算问题，现多用于高效计算数列的前缀和、区间和。

[树状数组](https://oi-wiki.org/ds/fenwick/) 参见 [here](https://blog.csdn.net/Yaokai_AssultMaster/article/details/79492190), 图很直观.

- 对于不需要修改的数组而言, 要求区间和可以用前缀和, 查询 O(1)
- 对于要修改的, 可以用树状数组, 更新和查询均为 O(log(n)), 从一个数组构建需要 O(n)


辅助函数: 得到数字的最低非零位

```python
def lowbit(x):
    """x 的二进制表示中，最低位的 1 的位置。
例如, 000100100, 返回 100
    """
    return x & -x
```

## 树状数组

- 简言之, 希望 0100 能够存储数组中 0001-0100 四个位置之和 (从1开始计数), 1010能够存储 1001, 1010 两个位置数字之和
    - 从而, 希望得到数组前 1010之和时, 能够进行分解 `sum[1010] = l[1010] + l[1000]`
    - 要更新数组 1010位置的数字 (+某一数值), 则需要更新 1010, 1100 即每次加上最低1位 (这里假设 10000 超过了数组长度)

因此, 1. 求前缀和, 每次减去数字最低的数字1位, 累计; 2. 对某一个idx的数字更新, 每次加上最低数字1位, 直到数组最大长度.

```python
# 简化实现版本
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n+1)
    @staticmethod
    def lowbit(x):
        return x & (-x)
    def update(self, i, delta):
        while i <= self.n:
            self.tree[i] += delta
            i += self.lowbit(i)
    def query(self, i):
        res = 0
        while i > 0:
            res += self.tree[i]
            i -= self.lowbit(i)
        return res

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
```

## 案例: 计算逆序对

- 剑指 Offer 51. 数组中的逆序对
- 0315. 计算右侧小于当前元素的个数
