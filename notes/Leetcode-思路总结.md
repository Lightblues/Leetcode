## overall

- 通过所给数据的复杂性判断方案是否可行
- 有时候相较于更符合直觉的「优雅」解法, 可以通过更「暴力」的方式避免复杂判断
    - sample: 2086. 从房屋收集雨水需要的最少水桶数
    - 再如, 二分查找的时候用额外的变量记录符合条件的值, 而不必纠结是返回 l/l-1.
    - 如, 利用 for i in range(left, right) 避免数组越界的判断
- 方法论
    - 刷题量是必要的
    - 关于题解: 如果是成体系的内容, 可以学一套的路子. 例如我刷周赛跟着 [灵神](https://leetcode.cn/u/endlesscheng/)
    - 关于「重写」题目, 也是很有必要的

## Python 基本模块

见 `template`

### 默认环境函数

- `str, ord` 转换
- `pow(x,y, mod)`

### functools

cache

- 注意默认的 `lru_cache(maxsize=128)` 性能可能不高? 直接用可能会超时. Python 3.9 中引入的 `@cache = lru_cache(maxsize=None)` 也即不对于 cache size 进行限制性能会好一点.

### itertools

<https://docs.python.org/zh-cn/3/library/itertools.html>

- `product` 很好用
- `accumulate` 计算 cumsum (注意 `initial` 参数)
- `permutations(iterable, r=None)` 从一个长度为n的数组中得到所有长度为r的排列
- `chain` 来将二维列表转为一维: `list(itertools.chain(*list2d))`;
    - 也可以用 `list(itertools.chain.from_iterable(list2d))`

```py
list2d = [[1,2,3], [4,5,6], [7], [8,9]]
merged = [i for i in line for line in list2d]
merged = list(itertools.chain(*list2d))
merged = list(itertools.chain.from_iterable(list2d))
```


### sortedcontainers

- `SortedList` 插入、查询(`__getitem__`) 的时间复杂度约为 O(log(n))


## Python 语法

- 排序: <https://docs.python.org/zh-cn/3/howto/sorting.html>

### 性能上的说明

- 避免使用 deepcopy
    - 例如 2065 用了冗余的list复制没问题, 但用 deepcopy 会超时
- lru_cache() 需要设置limit大一点, 不然性能也很糟糕
    - Python3.9 新增的 cache 函数就是没有内存限制的语法糖
- 字典的union操作: 1. 原地add操作; 2. 将小集合合并到大集合 (重复add) 的速度更快.
- 奇巧淫技: numpy

### 定义 `__gt__`

例如, 在 heapq 或者 bisect 时, 需要判断元素大小, Python默认的大小比较不满足时可以自定义

```python
class MaxNode():
    # 最大堆的节点. 
    # 排序要求: 按照 score降序, name升序
    def __init__(self, score, name) -> None:
        super().__init__()
        self.score = score
        self.name = name
    def __lt__(self, other):
        # 注意 Python 中 heapq 只有最小堆, 因此需要取反: 分数越大, 优先级越高
        return (-self.score, self.name) < (-other.score, other.name)
class MinNode():
    def __init__(self, score, name) -> None:
        super().__init__()
        self.score = score
        self.name = name
    def __gt__(self, other):
        # 简单期间, 直接定义 __gt__ 即可
        return (-self.score, self.name) < (-other.score, other.name)

# 用例
max_node = MaxNode(10, "alice")
h = heapq.heapify(...)
heapq.heappush(h, max_node)
```


### slice 语法

要删(改) 数组中连续的一段元素, 可以采用切片语法, 效率较高. (当然, 无法在数量级上提升, 只是一个卡常数的小技巧)

参见 [here](https://leetcode.cn/problems/count-integers-in-intervals/solution/chun-er-fen-by-migeater-t5kh/),

### 集合 set

## 算法

### 位运算

- Python 3.10 新增了 `int.bit_count(a)` 函数统计 a 中非零位数量, 比 `bin(a).count('1')` 的效率高不少.

#### 遍历所有子集 (状态压缩)

对于一个 mask 所表示的集合, 遍历其所有非空子集可以采用下面的模板. 核心是 `subset = (subset - 1) & mask`

```py
subset = mask
while subset:
    ...
    subset = (subset - 1) & mask
```


### 二分查找

- 注意查找结果与所需值之间的关系.
    - 例如, 要「找到数组中出现的小于等于值v的元素」, 应该 `bisect.bisect_right - 1`
- 手工实现的时候
    - 由于 `mid = (r-l)>>1`, 因此如果需要修改 l时一定要更新为 `l  = mid+1`, 否则可能死循环
    - 技巧: 如果不确定结果是否为 `l` 或 `l-1`, 可以额外用一个 ans 来记录.


### 单调栈

参见 `stack.py`

- 注意
    - 空栈 pop 的错误; 语法: `while s and s[-1] >= nums[i]: s.pop()`
- 题型1: 得到指定条件的子序列
    - 限制子序列长度为 k: 1) 在push的时候判断时候超过限制; 2) pop时判断剩余的是否够, 即使 break;
    - 限制栈内元素数量 (比如要求ch的数量至少为repetition): 1) pop的时候检查剩余是否够; 2) 另外需要检查, 若栈内元素不足以放剩余的ch (repetition-countChInStack), 则需要push.
- 题型2: 枚举所有的连续子数组
    - 通过单调栈得到「数组中下一个比idx位置元素大/小的元素(位置)」
    - 注意若有相同的数值出现, 为了避免重复枚举, 可以对左右边界分别用 严格小于和小于等于来约束.


### 折半枚举

参见 `subset_half.py`

- 折半枚举 & 复杂度分析
    - 直接枚举所有子集的复杂度为 `O(2^n)`, 当 n=40 的时候数量级就到 12了
    - 折半枚举的思路是, 将数组等分成两部分, 这样每一半 n=20 数量级为 6.
    - 如何将两部分组合? 二分查找. 因此整体的复杂度为 `O(2^(n/2) * log(2^(n/2)))`
- 题型1: 枚举、划分数组
- 题型2: 简化DFS (类似双向搜索)

### 前缀和

itertools 包: `list(itertools.accumulate(arr, initial=0))`

- 注意 `[l,r]` 闭区间内的和可以通过前缀和计算: `arr[l:r] = cumsum[r+1] - cumsum[l]` 这里在左侧添加了一项 (cumsum长度为n+1), 这是为了处理闭区间.
    - 例如, 对于数组 [1,2,3], 通过 `itertools.accumulate(arr, initial=0))` 得到前缀和 [0,1,3,6], 则 `arr[0:2] = cumsum[3] - cumsum[0] = 6`
- 「前缀和的前缀和」
    - 例如6077题用到了, 注意这里和一般的前缀和没有区别, 也是 `s[l:r] = ss[r+1]-ss[l]` 这里是 ss 是 前缀和s的前缀和 (长度为 n+1). 只需要在推导的时候, 注意 s 的 l/r 是什么就好.


## 进阶算法

from [here](https://leetcode.cn/problems/count-of-range-sum/solution/xian-ren-zhi-lu-ru-he-xue-xi-ke-yi-jie-jue-ben-ti-/)

线段树

最基础的线段树支持这两种操作:

- 操作 1 「查询」: 给定一个范围 $[l e f t, r i g h t]$, 查询 $t[l e f t]$ 到 $t[r i g h t]$ 的和;
- 操作 2 「更新」: 给定一个元素 $x$, 将 $t[x]$ 增加 $\delta$ 。

两种操作的时间复杂度均为 $O(\log n)$ 。

树状数组

最基础的树状数组支持这两种操作:

- 操作 1 「查询」: 给定一个下标 right, 查询 $t[1]$ 到 $t[$ right $]$ 的和（即前缀和）;
- 操作 2 「更新」: 给定一个元素 $x$, 将 $t[x]$ 增加 $\delta$ 。

两种操作的时间复杂度均为 $O(\log n)$ 。

平衡树

平衡树实际上就是「平衡」的二叉搜索树, 它与线段树和树状数组不同, 并且它不需要借助离散化操作。支持的操作（在本题中会使用到的）主要有以下几种:

- 操作 1 「lower bound」：给定一个元素 $x$, 查询平衡树中最小的大于等于 $x$ 的元素;
- 操作 2 「upper bound」: 给定一个元素 $x$, 查询平衡树中最小的大于 $x$ 的元素;
- 操作 3 「rank」：给定一个元素 $x$ (它必须在平衡树中）, 求它是第几小的元素。当存在重复元素时, 会计入多次;
- 操作 4 「insert」：给定一个元素 $x$, 将它放入平衡树中。

所有操作的时间复杂度均为 $O(\log n)$ 。大部分语言自带的平衡树支持操作 1 和 2 和 4 但不支持操作 3 。

### 线段树

题目: 0715, 6066

- 尝试直接用数组存储 + 二分解决
- 注意采用Python列表的 slice 技巧进行修改, 否则 O(n) 的数组元素移动会超时

