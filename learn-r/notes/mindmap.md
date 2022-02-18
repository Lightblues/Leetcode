## 笔记/小结

- 关于R语言中的数据类型
  - 函数: `typeof, class, attributes`
  - 属性
    - 用 `attr` 函数 定义属性 (例如一些meta信息)
    - `names, dim, class`

常见的数据类型

- 向量
  - 一般(原子类型)类型为向量, 基本数据类型包括 logical, integer, double, character, complex, raw 等
  - 向量也可定义 names, 通过 `a["5"]` 的形式访问, `names` 查看
- 列表 list
  - 可以存放不同类型的一组数据; 可以指定名字也可以没有名字
  - 对于 names, 通过 `l[["5"]]` 的形式访问, 注意用 `[]` 得到的仍为大小为 1 的 list
- 数组 array & 矩阵 matrix
  - 给一个基本的向量添加 dim 属性即变为数组, dim的长度决定了数组维度
  - 当数据维度为 2 时即为矩阵
    - `nrow, ncol, dim, colnames, rownames`, 注意 names 属性和向量时候一样
    - 矩阵运算: `%*%, sum(A*B), %o%`
    - `solve` 
    - `cbind, rbind`
  - 矩阵子集访问
    - 注意, **因为矩阵本质上还是向量**, 因此引用方式仍为 `[]` 而没有 `[[]]` 的列表方式.
    - 相较于一般向量的子集使用方式有 1. `[,]` 语法对于行列进行筛选; 2. 输入一个列数等于数组维度的矩阵对于单个元素进行索引.
- 数据框 data.frame & tibble::tibble
  - 本质上是列表, 要求每一列的长度相同
  - 数据框内容访问
    - 注意, **由于数据框本质上是列表**, 因此当索引内容为标量时 `[]` 和 `[[]]` 和 list 一样, 例如 `d[1]` 返回第一列df 而 `d[[1]]` 返回第一列作为向量
    - 相较于矩阵, 除了向量和列表的区别, 1. 一样用 `[,]` 的索引形式; 2. 增加了 `$name` 的形式
  - 对于df而言, 1. 列名 colnames就是names; 2. 原生R中可以定义 rownames 但不推荐可以直接作为数据的一列 (主键然后用 dplry::inner+join 使用);
  - **tibble**
    - dplyr 包中 filter, select, arrange, mutate 等函数

## base

- 查看数据
    - head
    - `str` 数据格式, `summary` 得到统计值
    - dim 查看维度 (df大小); nrow
- 文件读取
    - read.csv(file=, stringsAsFactors=TRUE)
- 文件写入
    - sink(file)

其他

- unique()

## stats

- t.test(x,y)
- aov(formula, data) 进行方差分析 Analysis of Variance (ANOVA)
- PCA
    - `procomp(x, scale.=TRUE)` 设置 scale 进行归一化

## 画图

- plot(x,y, main,sub, xlab, ylab, col,pch, cex, lwd)
- boxplot(formula, data)
- abline(reg, lty, lwd)

