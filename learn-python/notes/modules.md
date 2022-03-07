
## functools

- `lru_cache`
    - LRU（Least Recently Used，最近最少使用）是很常见的一个，也是 Python 中提供的缓存置换策略
    - see [Python 中 lru_cache 的使用和实现](https://zhuanlan.zhihu.com/p/348370957)

```python
import functools
# 注意 lru_cache 后的一对括号，证明这是带参数的装饰器
@functools.lru_cache()
def factorial(n):
    print(f"计算 {n} 的阶乘")
    return 1 if n <= 1 else n * factorial(n - 1)

# 手动实现 cache
def wrapper(f):
    cache = {}
    def inner(*args, **kwargs):
        if args not in cache:
            cache[args] = f(*args, **kwargs)
        return cache[args]
        # return f(*args, **kwargs)
    return inner
f = wrapper(f)
```
