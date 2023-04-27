
相关资源

- Rstudio 的 Cheatsheet <https://github.com/rstudio/cheatsheets>

## 笔记/小结

- 关于R语言中的数据类型
    - 函数: `typeof, class, attributes`
    - 属性
        - 用 `attr` 函数 定义属性 (例如一些meta信息)
        - `names, dim, class`

### 常见的数据类型

- 向量
    - 一般(原子类型)类型为向量, 基本数据类型包括 logical, integer, double, character, complex, raw 等
    - 向量也可定义 names, 通过 `a["5"]` 的形式访问, `names` 查看. 注意对于向量 `[[]]` 和 `[]` 是一样的
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

### purrr 包中的泛函 (基本R中 apply 等函数)

- 共同语法
    - 无名函数以及简化写法, 采用 `~ 表达式` 的格式, 参数为 `.`, `.x, .y`, `..1, ..2, ..3` 这样的形式
    - 提取列表中各个元素的语法: 例如 `map_dbl(df, 1)` 或 `map_chr(df, list("hobbies", 1))`, 第二个参数为标量时提取相应位置的元素, 为列表时进行嵌套提取
- map `map(.x, .f, ...)` 将函数.f作用于一组数据上, 注意返回的是列表, `map_lgl, map_int, map_dbl, map_chr` 指定了函数的返回类型, 从而将输出化简为向量
    - walk 默认输出原本的变量 .x
    - modify 语法和 map 一致, 不过返回的类型和输入 .x 一致; 另外有 `modify_if(.x, .p, .f, ...` 等根据 .p 条件对于 .x 进行筛选修改
- map2 `map2(.x, .y, .f, ...)` 拓展到对于 .x, .y 两个列表根据相同的index进行操作, 函数可以使用 .x, .y 参数
- imap `imap(.x, .f, ...)` 形式上和 map 一样, .f 函数中可以使用 .y 就是每个元素所对应的index (名字或者数字)
- pmap 主要作用其实是参数传递. `pmap(.l, .f, ...)` 中第一个列表.l定义了列表形式的一组命名参数, 然后和函数.f的参数名之间进行匹配. 在定义函数的时候注意其参数名字和传入列表的名字匹配.
    - 相关的是 invoke 函数类, `invoke(.f, .x = list(NULL), ...)` 将 .x 作为参数 (list) 传给 .f, 而 `invoke_map(.f, .x, ...)` 将.x中定义参数列表传递给 .f(一个或者一列表函数)
- reduce `reduce(.x, .f, ..., .init, .dir = c("forward", "backward"))`
    - `reduce2(.x, .y, .f, ..., .init)` 将 .y 作为参数传递给执行函数, 注意 .init 不指定参数长度应比 .x 长度小一 (等于.f执行次数)
    - accumulate 相较于 reduce, 保留了每一步的结果 (类似 cumsum)
- 使用示性函数(返回逻辑向量)的泛函
    - some, every, none, 语法为 `every(.x, .p, ...)` 根据预测函数.p 的结果做逻辑运算
    - detect, detect_index, 检索直到第一个元素满足条件
    - 根据条件筛选, keep, discard
    - modify_if, map_if 等语法

其实在基本 R语言中已经有功能类似的函数

- apply `apply(X, MARGIN, FUN, ..., simplify = TRUE)` 对于 array 的第 MARGIN 个维度进行操作
- lapply
    - `lapply(X, FUN, ...)` 对于 X 的每个元素作用, 返回一个列表
    - sapply `sapply(X, FUN, ..., simplify = TRUE, USE.NAMES = TRUE)` 对于结果尝试简化, 但可能是 vector, matrix, array, list
    - vapply 第三个参数 FUN.VALUE 指定返回类型 (简化)
    - 注意 replicate 是sapply的一个封装, 用于重复执行一些命令 `replicate(n, expr, simplify = "array")`
- Map `Map(f, ...)` 对于 ... 构成的list的每一个元素进行操作, 结果为列表. 例如 `Map(max, d$x, d$y)` 可以计算d的每一行最大值
    - mapply 可以理解为对 Map 结果进行了简化 `mapply(FUN, ..., MoreArgs = NULL, SIMPLIFY = TRUE, USE.NAMES = TRUE)`; 当然官方文档指出 mapply 为 sapply 的多变量版本
- Reduce `Reduce(f, x, init, right = FALSE, accumulate = FALSE)` 类似 purrr 中的 reduce, accumulate
- Filter `Filter(f, x)`
- Find `Find(f, x, right = FALSE, nomatch = NULL)`
- Position `Position(f, x, right = FALSE, nomatch = NA_integer_)` 分别类似 purrr 中的 detect, detect_index

### 函数

- 函数包括三部分: 参数表、函数体、环境, 分别通过 `formals, body, environments` 得到
- 函数调用, `do.call()`
- 复合调用, `|>`, `magrittr::%>%`
- 递归调用, Recall
- 向量化 `Vectorize`
- 函数调用有四种方式: 1. 前缀 `fsub(5, 2)`; 2. 中缀 `` `+` ``; 3. 替换, `` `[<-` ``; 4. 特殊, 例如基本的 `[, [[, {}, (), if, for`
- 参数
    - 懒惰求值
    - `missing` 判断用户是否没有提供对应的实参
- 程序调试
    - `browser()`
    - `debug(f)` 对函数`f`开启跟踪运行
    - 设置出错开启调试: `options(error=recover)`
    - stop()、warning()、message()
    - `stopifnot` 判断条件, 类似Python中的 assert
    - 出错处理: `tryCatch()`
- 函数式编程介绍
    - 可以输入函数作为自变量的函数叫 **泛函**(functionals)
    - 返回函数的函数叫 **函数工厂**, 返回的 **闭包**(closer) 包括了当时的环境
    - 输入为函数, 输出对于该函数进行修改后返回的叫 **函数算子**(function operators), 例如 Vectorize 函数
- 闭包
    - 闭包包含了生产它的函数工厂的运行环境
    - `<<-` 赋值
- 环境
    - `rlang` 包中的一些函数
    - 一般编程不会直接设计对于环境的操作, 但是在下面场景中会用到
        - 扩展包的环境和搜索路径
            - 拓展包为全局环境的父环境
        - 函数环境
            - 自定义函数包括形参表、函数体和定义时绑定的环境三个部分
        - 命名空间
            - 包有依赖关系, 载入拓展包可能产生覆盖的问题, 为了避免该问题, R拓展包与两个环境相关: 1. 拓展包的环境, 实际上是用户得到的; 2. **命名空间环境**, 上层包括imports环境, 定义清楚了包依赖.
        - 运行环境
            - 函数在调用执行时自动生成一个运行环境， 其父环境为函数定义时的环境
            - 闭包就是保存了其函数工厂的运行环境
- 调用栈
    - 调用栈由若干个分层的框架(frames)组成, 求值上下文(evaluation context)
    - 框架包括: 1. 一个表示调用函数的表达式 `expr`; 2. 环境; 3. 父框架;
    - `traceback()`; `lobstr::cst()`
    - R采用 **句法作用域**， 即由定义决定变量作用域， 有少数语言如 Lisp 采用 **动态作用域**(dynamic scoping)， 即在调用栈上查找变量值。

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
