## overall

- 通过所给数据的复杂性判断方案是否可行

## 技巧: base模块

### functools

cache

- 注意默认的 `lru_cache(maxsize=128)` 性能可能不高? 直接用可能会超时. Python 3.9 中引入的 `@cache = lru_cache(maxsize=None)` 也即不对于 cache size 进行限制性能会好一点.

### itertools

- `product` 很好用


## 算法

### 二分查找

- 注意查找结果与所需值之间的关系.
    - 例如, 要「找到数组中出现的小于等于值v的元素」, 应该 `bisect.bisect_right - 1`
- 手工实现的时候
    - 由于 `mid = (r-l)>>1`, 因此如果需要修改 l时一定要更新为 `l  = mid+1`, 否则可能死循环
    - 技巧: 如果不确定结果是否为 `l` 或 `l-1`, 可以额外用一个 ans 来记录.
