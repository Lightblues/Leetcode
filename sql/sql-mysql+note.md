
参见 [mysql-note]. 这里记录刷题过程中的总结.

TODO

- 自定义变量: <https://www.jianshu.com/p/357a02fb2d64>

常见语法

- round(3.423, 2)
- 聚合操作: sum, max, count, avg 等
- `order by desc/asec`
- 合并: `union`
- `IF(*, a,b)` 语法
    - `IFNULL(*, *)` 防止为空 (例如加了 OFFSET)
- `CASE * WHEN * THEN * ELSE * END` 语法
- 连接: JOIN; 或者是两张表直接笛卡尔积.
    - `ON(* AND *)`
- 窗口函数 `row_number, rank, dense_rank, ntile`, 
    - 需要配合 `over()`, 该函数的参数一般有 `partition by, order by`.
- 数量限制: 配合order得到order (当然可以直接用窗口函数)
    - `LIMIT a OFFSET b` 等价于 `LIMIT b,a`

mysql 语句的执行顺序:

```sh
from -> on -> join -> where -> group by -> 聚集函数 -> having -> select ->distinct -> union -> order by -> limit
```

