## overall

- 通过所给数据的复杂性判断方案是否可行
- 有时候相较于更符合直觉的「优雅」解法, 可以通过更「暴力」的方式避免复杂判断
    - sample: 2086. 从房屋收集雨水需要的最少水桶数
    - 再如, 二分查找的时候用额外的变量记录符合条件的值, 而不必纠结是返回 l/l-1.
    - 如, 利用 for i in range(left, right) 避免数组越界的判断

## 技巧: base模块

### functools

cache

- 注意默认的 `lru_cache(maxsize=128)` 性能可能不高? 直接用可能会超时. Python 3.9 中引入的 `@cache = lru_cache(maxsize=None)` 也即不对于 cache size 进行限制性能会好一点.

### itertools

- `product` 很好用

### sortedcontainers

- `SortedList` 插入、查询(`__getitem__`) 的时间复杂度约为 O(log(n))


## Python 语法

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

要删(改) 数组中连续的一段元素, 可以采用切片语法, 效率较高.

参见 [here](https://leetcode.cn/problems/count-integers-in-intervals/solution/chun-er-fen-by-migeater-t5kh/),

## 算法

### 二分查找

- 注意查找结果与所需值之间的关系.
    - 例如, 要「找到数组中出现的小于等于值v的元素」, 应该 `bisect.bisect_right - 1`
- 手工实现的时候
    - 由于 `mid = (r-l)>>1`, 因此如果需要修改 l时一定要更新为 `l  = mid+1`, 否则可能死循环
    - 技巧: 如果不确定结果是否为 `l` 或 `l-1`, 可以额外用一个 ans 来记录.

### 线段树

题目: 0715, 6066

- 尝试直接用数组存储+二分解决
- 注意采用Python列表的 slice 技巧进行修改, 否则 O(n) 的数组元素移动会超时
