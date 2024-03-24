
- 参见 [[mysql-note]]. 这里记录刷题过程中的总结.
- 一些基本原理的理解见 [[mysql-digging]] 概念深入理解: 记录看过的一些原理性文章
- 另外的资源: Data whale [Wonderful-sql](https://github.com/datawhalechina/wonderful-sql)

TODO

- 自定义变量: <https://www.jianshu.com/p/357a02fb2d64>

常见语法

- round(3.423, 2)
- 聚合操作: sum, max, count, avg 等
- `order by desc/asc`
- 合并: `union`
    - UNION 和 UNION ALL 的区别在于, 前者会进行去重 (因此也更慢)
- `IF(*, a,b)` 语法
    - `IFNULL(*, *)` 防止为空 (例如加了 OFFSET)
- `CASE * WHEN * THEN * ELSE * END` 语法
- 连接: JOIN; 或者是两张表直接笛卡尔积.
    - `ON(* AND *)`
    - 配合 WHERE
    - 若 LEFT JOIN 是一对多关系, 那么, 也会使得行数增加
- 窗口函数 `row_number, rank, dense_rank, ntile`, 
    - 需要配合 `over()`, 该函数的参数一般有 `partition by, order by`.
- 数量限制: 配合order得到order (当然可以直接用窗口函数)
    - `LIMIT a OFFSET b` 等价于 `LIMIT b,a`

mysql 语句的执行顺序:

```sh
from -> on -> join -> where -> group by -> 聚集函数 -> having -> select ->distinct -> union -> order by -> limit
```

## 基本用法

见 [[mysql-note#MySQL 基础命令]]

## 窗口函数

[doc](https://dev.mysql.com/doc/refman/8.0/en/window-functions.html); 见 [通俗易懂的学会：SQL窗口函数](https://zhuanlan.zhihu.com/p/92654574)

```sql
-- 窗口函数语法
<window function> OVER (
    [PARTITION BY <partition column(s)>]
    [ORDER BY <order column(s)>]
    [<window frame clause>]
)
<窗口函数> over (partition by <用于分组的列名>
                order by <用于排序的列名>)
```
