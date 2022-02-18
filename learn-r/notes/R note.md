
- 李东风 [R语言教程](https://www.math.pku.edu.cn/teachers/lidf/docs/Rbook/html/_Rbook/index.html)

### 2-R语言入门运行样例

- 数学函数
    - sqrt, exp, log10
    - 取整 round(1.1234, 2), floor, ceiling
    - sin, cos, tan, asin, acos, atan
    - pi
    - 分布函数
        - 标准正态分布 `dnorm(1.98)` 分布密度函数, `pnorm()` (累积)分布函数, `qnorm` 分位数函数
        - `qt(1-0.05/2, 10)`
- 函数
    - 管道 `exp(1.0) |> log()`
- 输出
    - print()
    - cat("sin(pi/2)=", sin(pi/2), "\n")
    - sink() 函数作运行记录
        - 在R命令行中运行过的命令会被保存在运行的工作文件夹中的一个名为.Rhistory的文件中。 用`sink()`函数打开一个文本文件开始记录文本型输出结果。 结束记录时用空的`sink()`即可关闭文件不再记录。 如
        - 例如 sink("tmpres01.txt", split=TRUE), 最后再调用 sink() 停止记录
        - `sink()`用作输出记录主要是在测试运行中使用， 正常的输出应该使用`cat()`函数、`write.table()`、`write.csv()`等函数。
- 向量计算与变量赋值
    - R语言以向量为最小单位。用`<-`赋值。
    - `x1 <- 1:10`
    - `marks <- c(3, 5, 10, 5, 6)`
    - R的许多函数都可以用向量作为自变量， 结果是自变量的每个元素各自的函数值
- 绘图示例
    - `demo("graphics")`
    - `demo("image")`
    - 函数曲线: `curve(x^2, -2, 2)` (x 是传入的函数默认要求的参数)
    - 参考线 `abline(h=0)`
    - 条形图 `barplot(c("男生"=10, "女生"=7),)`
    - 散点图 `plot(1:10, sqrt(1:10))`
- 统计汇总
    - table 计数
        - 交叉计数 table(tax.tab[["征收方式"]], tax.tab[["申报渠道"]])
    - summary 数值变量
    - mean, sd,
        - `sd(c(1,2,NA), na.rm=TRUE)`
- 运行源程序文件
    - `source("fn.r", encoding="UTF-8")` 可以运行对应文件中的代码
- 工作目录
    - `getwd()`
    - `setwd("d:/work")`

### 7-向量下标和子集

- 正整数, 负整数下标
- 空下标和零下标
    - `x[0]`是一种少见的做法， 结果返回类型相同、长度为零的向量， 如 `numeric(0)`。 相当于空集。
    - 当0与正整数下标一起使用时会被忽略
- 下标越界: 返回 NA
- 逻辑下标
    - 注意逻辑判断的时候的 NA
    - `x[!is.na(x) & x > 2]` 去除 NA
- which, which.min, which.max
    - 例如 `which(x>5)` 等价于 `seq(along=x)[x > 5]`
    - 用`which.min()`、`which.max`求最小值的下标和最大值的下标， 不唯一时只取第一个
- 元素名
    - 变量的元素名为字符串, 可以通过 names 访问和赋值
    - `ages <- c("李明"=30, "张聪"=25, "刘颖"=28)`, 或者通过 `names` 函数去的名字然后赋值 `names(ages) <- c("李明", "张聪", "刘颖")` (原地操作), 或者直接用 `setNames` 设置.
    - 用元素名作为下标 `ages[c("李明", "刘颖")]`
    - 用`unname(x)`返回去掉了元素名的`x`的副本， 用`names(x) <- NULL`可以去掉`x`的元素名 (原地操作)。
    - R允许仅给部分元素命名， 这时其它元素名字为空字符串。 不同元素的元素名一般应该是不同的， 否则在使用元素作为下标时会发生误读， 但是R语法允许存在重名。
- 用R向量下标作映射
    - 例如, 定义映射 `sex_color <- c("男"="blue", "女"="red")`
    - 可以使用 `unmane(sex_color[c("男", "男", "女", "女", "男")])` 得到对应的颜色向量
- 集合运算
    - unique
    - %in%
    - match(x,y) 对于 x 中的每个元素, 在 y 中查找, 返回第一个找到的下标, 不存在的话返回 NA
        - `match(c(2,5,0), c(1,5,2,5))`
    - intersect(x,y), union, setdiff, setequal
        - 结果都会去重, 例如 `setequal(c(1,5,2), c(2,5,1,5))` 返回 TRUE

```r
x <- c(1, 4, 6.25)
x[c(1,3)] <- c(11, 13); x
x[c(1,3,1)]
# 负下标表示去除
x[-c(1,3)]

# 空下标 [] 表示取所有元素
x <- c(1,4,6.25)
x[] <- 999
x
## [1] 999 999 999
#

# 下标越界
x <- c(1,4,6.25)
x[5] # NA, 不报错
x
x[5] = 9
x # 长度变为 5

# 逻辑下标
x[x > 3]
# 注意缺失值
x <- c(1, 4, 6.25, NA)
x[x > 2]
## [1] 4.00 6.25   NA
x[!is.na(x) & x > 2]
## [1] 4.00 6.25

# which
x <- c(3, 4, 3, 5, 7, 5, 9)
which(x > 5)
## [1] 5 7
seq(along=x)[x > 5]

# which.min
which.min(x)
## [1] 1
```

```r
# 元素名
ages <- c("李明"=30, "张聪"=25, "刘颖"=28)
# or
ages <- c(30, 25, 28)
names(ages) <- c("李明", "张聪", "刘颖")
# or
ages <- setNames(c(30, 25, 28), c("李明", "张聪", "刘颖"))
# 可以用元素名作为下标
ages[c("李明", "刘颖")]

sex <- c("李明"="男", "张聪"="男", "刘颖"="女")
```

```r
# 集合运算
unique(c(1, 5, 2, 5))

c(5,6) %in% c(1,5,2)
## [1]  TRUE FALSE

match(c(2,5,0), c(1,5,2,5))
## [1]  3  2 NA
```

### 8-R 数据类型的性质

- R中数据的最基本的类型包括 logical, integer, double, character, complex, raw, 其它数据类型都是由基本类型组合或转变得到的。 character类型就是字符串类型， raw类型是直接使用其二进制内容的类型。 为了判断某个向量`x`保存的基本类型， 可以用`is.xxx()`类函数， 如`is.integer(x)`, `is.double(x)`, `is.numeric(x)`, `is.logical(x)`, `is.character(x)`, `is.complex(x)`, `is.raw(x)`。 其中`is.numeric(x)`对integer和double内容都返回真值。
    - 注意因子的结果是`integer`而不是因子。
    - 在R语言中数值一般看作double, 如果需要明确表明某些数值是整数， 可以在数值后面附加字母L, 例如 `c(1L, 4L)`
    - 整数型的缺失值是`NA`， 而double型的特殊值除了`NA`外， 还包括`Inf`, `-Inf`和`NaN`， 其中`NaN`也算是缺失值, `Inf`和`-Inf`不算是缺失值。
    - is.finite(), is.infinite, is.na, is.nan. `is.na()`判断是否`NA`或`NaN`； `is.nan()`判断是否`NaN`
    - 严格说来， `NA`表示逻辑型缺失值， 但是当作其它类型缺失值时一般能自动识别。 `NA_integer_`是整数型缺失值， `NA_real_`是double型缺失值， `NA_character_`是字符型缺失值。
- 向量类型
    - integer类型、double类型、logical类型、character类型、还有complex类型和raw类型称为 **原子类型**(atomic types)， 原子类型的向量中元素都是同一基本类型的。 比如， double型向量的元素都是double或者缺失值。
        - 原子类型的各个元素除了基本类型相同， 还不包含任何嵌套结构
        - `c(1, c(2, 3, c(4, 5)))` 会被展开
    - 除了 原子类型的向量， 在R语言的定义中， 向量还包括后面要讲到的 **列表**（list）， 列表的元素不需要属于相同的基本类型， 而且列表的元素可以不是单一基本类型元素。 用`typeof()`函数可以返回向量的类型， 列表返回结果为`"list"`
        - 例如 `typeof(list("a", 1L, 1.5))`
- R有一个特殊的`NULL`类型， 这个类型只有唯一的一个`NULL`值， 表示不存在。 `NULL`长度为0， 不能有任何属性值。 用`is.null()`函数判断某个变量是否取`NULL`。
    - `NULL`值可以用来表示类型未知的零长度向量， 如`c()`没有自变量时返回值就是`NULL`； 也经常用作函数缺省值， 在函数内用`is.null()`判断其缺省后再用一定的计算逻辑得到真正的缺省情况下的数值。
    - 要把NULL与NA区分开来， NA是有类型的（integer、double、logical、character等), NA表示存在但是未知。 数据库管理系统中的NULL值相当于R中的NA值。
- 类型转换
    - 可以用`as.xxx()`类的函数在不同类型之间进行强制转换
    - 在用`c()`函数合并若干元素时， 如果元素基本类型不同， 将统一转换成最复杂的一个，复杂程度从简单到复杂依次为： `logical<integer<double<character`。 这种做法称为类型升档
- 属性
    - 除了`NULL`以外， R的变量都可以看成是 **对象**， 都可以有属性。 在R语言中， 属性是把变量看成对象后， 除了其存储内容（如元素）之外的其它附加信息， 如维数、类属等。 R对象一般都有 `length`和`mode` 两个属性 (mode 是为了兼容 S 语言)。
    - names, dim, class
    - attributes 函数
        - 对象`x`的所有属性可以用`attributes()`读取
    - attr 函数
        - 可以用`attr(x, "属性名")`的格式读取或定义`x`的属性
        - 例如, 对于一个原子类型 `x=c(1,2)`, 可以定义属性 `attr(x, "theta") <- c(0, 1)`
        - 这样的属性常常成为“元数据”(meta data)， 比如， 用来保存数据的说明、模拟数据的真实模型参数，等等。
    - `names` 属性
        - 有元素名的向量、列表、数据框等都有 `names` 属性， 许多R函数的输出本质上也是列表， 所以也有`names`属性。 用`names(x)`的格式读取或设定。
        - 例如, 对于 lm 模型而言, `names(lm(...))` 包括 "coefficients"  "residuals" 等, 可以通过 `$` 符号获取
    - `dim` 属性
        - `dim`属性的存在表明对象是矩阵或一维、多维数组
        - 修改`dim`属性就将向量转换成矩阵（数组）， 或修改了矩阵的性质， 元素按列次序重排填入新的矩阵。
            - 例如 `x <- 1:4` 默认的 dim 应该是 4, 注意若指定 `dim(x)=c(1,4)` 则将其改为矩阵
        - R允许`dim`仅有一个元素， 这对应于一维向量， 与普通的没有`dim`属性的向量有区别。 另外要注意， 取矩阵子集时如果结果仅有一列或一行， 除非用了`drop=FALSE`选项， 结果不再有`dim`属性， 退化成了普通向量。
- 类属
    - R具有一定的面向对象语言特征， 其数据类型有一个 `class` 属性， 函数`class()`可以返回变量类型的类属
    - class属性是特殊的。 如果一个对象具有class属性， 某些所谓“通用函数(generic functions)”会针对这样的对象进行专门的操作， 比如， `print()`函数在显示向量和回归结果时采用完全不同的格式。 这在其它程序设计语言中称为“重载”(overloading)。
    - class属性用来支持R的S3风格的类， 常用的有factor, 日期，日期时间， 数据框，tibble。 R还有S4、R6等风格的类。
- `str()` 函数
    - 用`print()`函数可以显示对象内容。 如果内容很多， 显示行数可能也很多。 用`str()`函数可以显示对象的类型和主要结构及典型内容

```r
typeof(1:3) # integer
typeof(c(1, 2, 3)) # double
typeof(c(TRUE, NA, FALSE)) # logical
typeof("Abc") # character
typeof(factor(c("a", "b", "c"))) # integer

c(-1, 0, 1)/0
## [1] -Inf  NaN  Inf
is.na(c(-1, 0, 1)/0)
## [1] FALSE  TRUE FALSE
```

```r
# 类属
typeof(factor(c('F', 'M', 'M', 'F')))
## [1] "integer"
mode(factor(c('F', 'M', 'M', 'F')))
## [1] "numeric"
storage.mode(factor(c('F', 'M', 'M', 'F')))
## [1] "integer"
class(factor(c('F', 'M', 'M', 'F')))
## [1] "factor"
class(as.numeric(factor(c('F', 'M', 'M', 'F'))))
## [1] "numeric"
```

### 11-列表类型

- list
    - R中列表(list)类型来保存不同类型的数据。 一个主要目的是提供R分析结果输出包装： 输出一个变量， 这个变量包括回归系数、预测值、残差、检验结果等等一系列不能放到规则形状数据结构中的内容。 实际上，数据框也是列表的一种， 但是数据框要求各列等长， 而列表不要求。
    - `rec <- list(name = "李明", age = 30, scores = c(85, 76, 90))`
    - is.list(), typeof
- 列表元素访问
    - 列表的一个元素也可以称为列表的一个“变量”， 单个列表元素必须用两重方括号格式访问
        - 可以序号, 也可以用name访问, `rec[[3]], rec[["age"]]`
    - 列表的单个元素也可以用 `$` 格式访问 (**names**)
    - 如果使用单重方括号对列表取子集， 结果还是列表而不是列表元素, 例如 `rec[3]` 得到仅有 scores 的一个列表
    - 列表一般都应该有元素名， 元素名可以看成是 **变量名**， 列表中的每个元素看成一个变量。 用`names()`函数查看和修改元素名。
    - 编辑列表元素: `rec[["身高"]] <- 178`
    - 删除: 把某个列表元素赋值为 `NULL` 就删掉这个元素
        - 在`list()`函数中允许定义元素为`NULL`，这样的元素是存在的, 例如 `li <- list(a = 120, b = "F", c = NULL)`
        - 而若要赋值为 NULL, 需要 `li["b"] <- list(NULL)` 也即定义一个子列表
- 列表类型转换
    - as.list, unlist
- 返回列表的函数示例 strsplit()
    - `strsplit()`输入一个字符型向量并指定一个分隔符， 返回一个项数与字符型向量元素个数相同的列表， 列表每项对应于字符型向量中一个元素的拆分结果。
    - 例如, 对于分割后等长的字符串 `x <- c("10, 8, 7", "5, 2, 2", "3, 7, 8", "8, 8, 7")`, 将其分割 `res <- strsplit(x, ",")`
    - 可以用 sapply 转为矩阵 `sapply(res, as.numeric)`

```r
# list
rec <- list(name = "李明", age = 30, scores = c(85, 76, 90))
rec
typeof(rec)
attributes(rec)
names(rec)
rec$name

# name
names(rec)
## [1] "name"   "age"    "scores"
names(rec)[names(rec) == "scores"] <- "三科分数"
names(rec)
## [1] "name"     "age"      "三科分数"
rec[["三科分数"]]
## [1] 85 76 90
```

### 13-R矩阵和数组

- R 矩阵
    - 矩阵用matrix函数定义，实际存储成一个向量，根据保存的行数和列数对应到矩阵的元素， 存储次序为按列存储。
    - `matrix()`函数把矩阵元素以一个向量的形式输入， 用`nrow`和`ncol`规定行数和列数，向量元素填入矩阵的缺省次序是按列填入， 用`byrow=TRUE`选项可以转换成按行填入。
    - `matrix(c(1, -1, 1, 1), nrow = 2, ncol = 2, byrow = TRUE)`
    - nrow, ncol
    - dim
    - colnames, rownames
    - 另外, `t()` 可以将向量转为行向量 (也即默认向量为按列的), `t(t(c(1,2)))` 转为列向量
- 矩阵子集
    - 用`A[1,]`取出A的第一行，变成一个普通向量。 用`A[,1]`取出A的第一列，变成一个普通向量。 用`A[c(1,3),1:2]`取出指定行、列对应的子矩阵
        - 命名了行列的也可以用名字 `A[c("a", "c"), "Y"]`
    - 注意在对矩阵取子集时， 如果取出的子集仅有一行或仅有一列， 结果就不再是矩阵而是变成了R向量， R向量既不是行向量也不是列向量。 如果想避免这样的规则起作用， 需要在方括号下标中加选项 `drop=FALSE`
        - 例如 `A[,1,drop=FALSE]`
    - 矩阵本质上是一个向量添加了`dim`属性， 实际保存还是保存成一个 **向量**， 其中元素的保存次序是按列填入
        - 若将 dim 属性删去, `dim(tmp) <- NULL`, 则直接变成了一般的向量; 也可通过指定 dim 将向量变为矩阵
        - 所以， 也可以向对一个向量取子集那样， 仅用一个正整数向量的矩阵取子集。例如 `A[1], A[c(1, 3, 5)]`
    - 也可以根据两列指标来访问
        - 例如定义指标矩阵 `ind <- matrix(c(1,1, 2,2, 3,2), ncol=2, byrow=TRUE)`, 也通过 `A[ind]` 访问指定的三个位置
    - **总结**: `[]` 内可以是: 1. 数字或向量, 则按照基本的向量形式访问 (记得矩阵仅仅是制定了 dim 的向量!!); 2. 加了 `,` 根据行列访问子矩阵, 注意若不加 drop 时近选择一行/列会转为向量; 3. 两列的矩阵, 则根据每一行的位置访问矩阵内的单个元素
    - 用`c(A)`或`A[]`返回矩阵`A`的所有元素。 如果要修改矩阵`A`的所有元素， 可以对`A[]`赋值。
    - diag 函数: 对矩阵`A`，`diag(A)`访问`A`的主对角线元素组成的向量。 另外，若`x`为正整数值标量，`diag(x)`返回`x`阶单位阵； 若`x`为长度大于1的向量， `diag(x)`返回以`x`的元素为主对角线元素的对角矩阵。
- cbind, rbind
    - 若`x`是向量，`cbind(x)`把`x`变成列向量， 即列数为1的矩阵， `rbind(x)`把`x`变成行向量。
    - 若`x1`, `x2`, `x3`是等长的向量， `cbind(x1, x2, x3)`把它们看成列向量并在一起组成一个矩阵。 `cbind()`的自变量可以同时包含向量与矩阵，向量的长度必须与矩阵行数相等。
    - `cbind()`的自变量中也允许有标量， 这时此标量被重复使用. 例如 `cbind(1, c(1,-1,10))`
    - 总结: 1. 传入向量, 则 cbind 和 rbind 分别将其是为列向量和行向量, 另一个维度设置为 1; 2. 传入多个向量, 将这些向量看作列向量和行向量拼接; 3. 传入矩阵也类似
- 矩阵运算
    - 四则运算
    - 矩阵乘法: 用`%*%`表示矩阵乘法而不是用`*`表示， 注意矩阵乘法要求左边的矩阵的列数等于右边的矩阵的行数
    - 向量和矩阵相乘: 矩阵与向量进行乘法运算时， 向量按需要解释成列向量或行向量。 当向量左乘矩阵时，看成行向量； 当向量右乘矩阵时，看成列向量.
        - 注意矩阵乘法总是给出矩阵结果， 即使此矩阵已经退化为行向量、列向量甚至于退化为标量也是一样。 如果需要，可以用`c()`函数把一个矩阵转换成按列拉直的向量。
    - 内积
        - 向量内积用 `sum(x*y)` 计算
        - 两矩阵, $A^TB$ 是广义的内积， 也称为叉积(crossprod), 注意结果为矩阵 (A的每列和B的每列做内积), 在R中用 `crossprod(A, B)` 计算. 但由于结果总为矩阵, 因此向量内积还是用 `sum(x*y)` 计算
    - 外积
        - 记为`%o%`, 结果为矩阵
            - 例如 `c(1, 2, 3) %o% c(1, -1)`, 等价于 `c(1, 2, 3) %*% t(c(1, -1))`
        - 这种运算还可以推广到`x`的每一元素与`y`的每一元素进行其它的某种运算， 而不限于乘积运算，可以用`outer(x,y,f)`完成， 其中`f`是某种运算，或者接受两个自变量的函数。
- 逆矩阵与线性方程组求解
    - `solve(A)`
    - `solve(A, b)`
- apply() 函数
    - `apply(A, 2, FUN)` 把矩阵`A`的每一列分别输入到函数FUN中， 得到对应于每一列的结果
    - `apply(A, 1, FUN)`把矩阵`A`的每一行分别输入到函数FUN中， 得到与每一行对应的结果
    - 如果函数FUN返回多个结果
        - 则`apply(A, 2, FUN)`结果为矩阵， 矩阵的每一列是输入矩阵相应列输入到FUN的结果， 结果列数等于`A`的列数
        - 若要使得按照行计算, 返回一个行数和 A 相同的矩阵, 则应该用`t(apply(A, 1, FUN))`的形式 (注意, 将返回的向量理解为列向量!)
- 多维数组
    - 矩阵是多维数组(array)的特例。
    - 实际上， 给一个向量添加一个 `dim` 属性就可以把它变成多维数组。
    - 定义
        - `数组名 <- array(数组元素, dim=c(第一下标个数, 第二下标个数, ..., 第s下标个数))`
        - 其中数组元素的填入次序是第一下标变化最快， 第二下标次之， 最后一个下标是变化最慢的。 这种次序称为 **FORTRAN次序**
    - 取子集
        - 多维数组在取子集时如果某一维下标是标量， 则结果维数会减少， 可以在方括号内用`drop=FALSE`选项避免这样的规则发生作用。
        - 例如, 对于三维数组 `ara <- array(1:24, dim = c(2, 3, 4))`, 子集 `ara[,2,2:3]` 得到的是一个 (2,2) 矩阵
        - 和矩阵一样, s 维数组可以通过一个 s维矩阵来提取, 每一行对应了每一个元素的坐标

### 13-数据框

- 统计分析中最常见的原始数据形式是类似于数据库表或Excel数据表的形式。 这样形式的数据在R中叫做数据框(data.frame)。 数据框类似于一个矩阵，有 n 个横行、p 个纵列， 但各列允许有不同类型：数值型向量、因子、字符型向量、日期时间向量。 同一列的数据类型相同。 在R中数据框是一个特殊的列表， 其每个列表元素都是一个长度相同的向量。 事实上，数据框还允许一个元素是一个矩阵， 但这样会使得某些读入数据框的函数发生错误。
    - `d <- data.frame( name=c("李明", "张聪", "王建"), age=c(30, 35, 28))`
    - `data.frame()`函数会将字符型列转换成因子， 加选项`stringsAsFactors=FALSE`可以避免这样的转换
- 方法
    - `nrow(d)`求`d`的行数， `ncol(d)`或`length(d)`求`d`的列数。 数据框每列叫做一个变量， 每列都有名字，称为列名或变量名， 可以用`names()`函数和`colnames()`函数访问。
    - 用`as.data.frame(x)`可以把`x`转换成数据框。 如果`x`是一个向量， 转换结果是以`x`为唯一一列的数据框。 如果`x`是一个列表并且列表元素都是长度相同的向量， 转换结果中每个列表变成数据框的一列。 如果`x`是一个矩阵，转换结果把矩阵的每列变成数据框的一列。
- 数据框是一个随着R语言前身S语言继承下来的概念， 现在已经有一些不足之处， tibble包提供了tibble类， 这是数据框的一个改进版本。
- 数据框内容访问
    - 单个元素 `d[2,3]`
    - 访问列, **返回向量**, 可以按照序号或列名 `d[[2]]`
        - 也可以用类似矩阵的形式 `d[,2]`; 然而在 tibble 中返回的还是数据框, 因此推荐 `[[]]` 的形式引用列
    - 访问行, 由于数据格式不同, 仍为 df. 方式为 `[1,]`
    - 复合行列索引, 例如 `d[1:2, c("age", "height")]`
    - 注意, 例如 `d[1:2, "age"]` 将缩减为向量, 可以指定 drop 强制保留为 df
    - 条件索引 `d[d[,"age"]>=30,]`
    - 对数据框变量名按照字符串与集合进行操作可以实现复杂的列子集筛选， 但是建议使用[26](https://www.math.pku.edu.cn/teachers/lidf/docs/Rbook/html/_Rbook/summary-manip.html#summary-manip)中所述的借助于tidyverse库的做法。
    - **总结**: 1. 相较于矩阵, 数据框的 `[...]` 中指定一个参数或向量, 是选取列 (例如 `d[1]` 返回第一列作为 df), 而矩阵则是对于底层的向量; 2. `[..., ...]` 指定两个参数, 分别对行列索引, 此时是一样的 (也可以留空, 不能少 `,`); 3. 注意矩阵没有 `[[]]` 和 `$` 语法, 这是选取某一列 (返回向量).
- 行名
    - 数据框每一行可以有行名， 这在原始的S语言和传统的R语言中是重要的技术， 但是在改进类型tibble中则取消了行名， 需要用行名实现的功能一般改用`left_join()`函数实现。 建议新的R程序不要再利用数据框的行名功能。
    - 对于代替数据框的tibble类型， 如果要实现行名的功能， 可以将行名作为单独的一列， 然后用dplyr包的`inner_join()`、`left_join()`、`full_join()`等函数横向合并数据集。
- 数据框与矩阵的区别
    - 数据框不能作为矩阵参加矩阵运算。 需要时，可以用`as.matrix()`函数转换数据框或数据框的子集为矩阵。
- **tibble** 类型
    - tibble类型是一种改进的数据框。 readr包的`read_csv()`函数是`read.csv()`函数的一个改进版本， 它将CSV文件读入为tibble类型
    - tibble类型的类属依次为`spec_tbl_df`, `tbl_df`, `tbl`, `data.frame`
- 生成
    - 用`as_tibble()`可以将一个数据框转换为tibble, dplyr包提供了`filter()`、`select()`、`arrange()`、`mutate()` 等函数用来对tibble选取行子集、列子集，排序、修改或定义新变量，等等。
    - 可以用`tibble()`函数生成小的tibble, 语法同 df.
        - 在调用`tibble()`函数时， 定义在后面的列可以调用前面的列的值。
- 区别于 df
    - tibble与数据框的一大区别是在显示时不自动显示所有内容， 这样可以避免显示很大的数据框将命令行的所有显示都充满。 没有显示的列的列名会罗列在显示下方， 显示时每列的类型同时显示，也会显示tibble的行列数。 可以在`print()`用`n=`和`width=`选项指定要显示的行数和列数。
    - tibble在生成或输入时不自动将字符型列转换为因子。 (区分 read.csv )
    - 列子集
        - 用`d[,ind]`这样的单重的方括号取列子集时， 即使仅取一列， 从tibble取出的一列结果仍是tibble而不是向量， 为了提取一列为向量应使用双方括号格式或`$`格式。
    - 行名:
        - tibble不支持行名(rownames)， 有行名的数据框用`as_tibble()`转换为tibble时， 可以用`rownames="变量名"`选项将行名转换成tibble的一列， 该列的变量名由选项值确定。 原来用行名完成的功能， 可以改用dplyr包的`left_join()`等函数， 这些函数进行数据框的横向连接。
- tibble在定义时不需要列名为合法变量名， 但是这样的变量名在作为变量名使用时需要用反单撇号包裹。
- 列表类型的列
    - `tibble(x = 1:3, y = list(1, 1:2, 1:3))`

```r
d <- data.frame(
    name = c("李明", "张聪", "王建"),
    age = c(30, 35, 28),
    height = c(180, 162, 175),
    stringsAsFactors = FALSE
)

############## 访问数据 ##############
# 单个元素
d[2, 3]
d[1, "name"] # 取第一行的 name 列

# 列
# 访问第二列, 结果为向量
# 注意 matrix 没有下面两种访问方式
d[[2]]
d[["age"]]
d$age
d[, 2] # 注意在 tibble 中返回的还是 tibble

# 行, 注意返回的还是 df
x <- d[2, ]
x
class(x)
is.data.frame(x)

# 同时取行和列
d[1:2, "age"]
d[1:2, "age", drop = FALSE]
d[1:2, c("age", "height")]
d[d[, "age"] >= 30, ]
```

### 14-工作空间和变量赋值

- 用`ls()`命令可以查看工作空间中的内容
- 可以用`rm()`函数删除工作空间中的变量
- `browser()` 沙盒
    - 在这样的browser命令行中随意定义变量， 定义的变量不会保存到工作空间中。 用“Q”命令可以退出这个沙盘环境， 接连回车也可以退出
- 变量名
    - R的变量名要求由字母、数字、下划线、小数点组成， 开头不能是数字、下划线、小数点， 中间不能使用空格、减号、井号等特殊符号， 变量名不能与`if`、`NA`等保留字相同。
    - 有时为了与其它软件系统兼容， 需要使用不符合规则的变量名， 这只要将变量名两边用反向单撇号 `` ` `` 保护
- 变量赋值与绑定
    - 在R中赋值 `<-` 本质上是把一个存储的对象与一个变量名 “**绑定**”(bind) 在一起
    - 并不是像C++、JAVA等语言那样， `x`代表某个存储位置， “`x <- c(1,2,3)`”代表将1到3这些值存储到`x`所指向的存储位置。 实际上，`<-`右边的`c(1,2,3)`是一个表达式， 其结果为一个R对象(object)， 而`x`只是一个变量名， 并没有固定的类型、固定的存储位置， 赋值的结果是将`x`绑定到值为`(1,2,3)`的R对象上。 R对象有值，但不必有对应的变量名； 变量名必须经过绑定才有对应的值和存储位置。
    - 同一个R对象可以被两个或多个变量名绑定。
    - 对于基本的数据类型如数值型向量， 两个指向相同对象的变量当一个变量被修改时自动制作副本。
    - `tracemem(x)` 可以显示变量名x绑定的地址并在其被制作副本时显示地址变化。
- 垃圾回收
    - 在当前的R语言中， 一个对象的引用（如绑定的变量名）个数， 只区分0个、1个或多个这三种情况。 在没有引用时， R的垃圾收集器会定期自动清除这些对象。 `rm(x)`只是删除绑定， 并不会马上清除`x`绑定的对象。
    - 垃圾收集器是在R程序要求分配新的对象空间时自动运行的， R函数`gc()`可以要求马上运行垃圾收集器， 并返回当前程序用到的存储量； lobstr包的`mem_used()`函数则报告当前会话内存字节数。
- 其他类型的复制
    - 如果`x`是一个有5个元素的列表， 则`y <- x`使得`y`和`x`指向同一个列表对象。 但是， 列表对象的每个元素实际上也相当于一个绑定， 每个元素指向一个元素值对象。 所以如果修改`y`：`y[[3]] <- 0`， 这时列表`y`首先被制作了副本， 但是每个元素指向的元素值对象不变， 仍与`x`的各个元素指向的对象相同； 然后， `y[[3]]`指向的元素值进行了重新绑定， 不再指向`x[[3]]`， 而是指向新的保存了值`0`的对象， 但`y`的其它元素指向的对象仍与`x`公用。 列表的这种复制方法称为浅拷贝， 表格对象及各个元素绑定被复制， 但各个元素指向（保存）的对象不变。 这种做法节省空间也节省运行时间。 在R的3.1.0之前则用的深拷贝方法， 即复制列表时连各个元素保存的值也制作副本。
    - 如果`x`是一个数据框， 这类似于一个列表， 每个变量相当于一个列表元素， 数据框的每一列实际绑定到一个对象上。 如果`y <- x`， 则修改`y`的某一列会对`y`进行浅拷贝， 然后仅该列被制作了副本并被修改， 其它未修改的列仍与`x`共用值对象。
        - 但是如果修改数据框`y`的一行， 因为这涉及到所有列， 所以整个数据框的所有列都会制作副本。
    - 对于字符型向量， 实际上R程序的所有字符型常量都会建立一个全局字符串池， 这样有许多重复值时可以节省空间。
- 对象大小
    - 用lobstr包的`obj_size()`函数可以求变量的存储大小， 如`obj_size(x)`， 也可以求若干个变量的总大小， 如`obj_size(x,y)`。 因为各种绑定到同一对象的可能性， 所以变量的存储大小可能会比想象要少， 比如， 共用若干列的两个数据框， 字符型向量， 等等。 基本R软件的`object.size()`则不去检查是否有共享对象， 所以对列表等变量的存储大小估计可能会偏高。
- **总结**: 在R语言中, 1. 对象以赋值的形式绑定在变量名上; 2. 通过 `y <- x` 的形式将不同变量绑定到同一(基本)对象/向量, 仅当 y 对于该对象的某一部分进行修改的时候, R内部才会复制该向量, 修改, 然后绑定给 y; 3. 对于更复杂的如 列表/数据框 对象, 按照列存储, 每一列都是基本对象/向量; 引用同一对象的两个变量名, 当 y 修改其中一列时, R只会复制修改被改动的那一列, 其他列仍然指向原本的基本对象 (**浅拷贝**); 若修改行则需要重新复制整个 列表/数据框; 4. 对于函数, 传入的是引用值, 若在函数内部不对于传入值进行修改, 则不会增加内存消耗; 若进行了修改则需要重新复制修改.

```r
# 变量赋值与绑定
x <- c(1, 2, 3)
cat(tracemem(x), "\n") # <0x7f8e14874d88>
y <- x # 这时y和x绑定到同一R对象
cat(tracemem(y), "\n") # <0x7f8e14874d88>
y[3] <- 0 # 这时y制作了副本
# tracemem[0x7f8e2dd52608 -> 0x7f8e14901ca8]:

tracemem(x) # <0x7f8e14874d88>
tracemem(y) # <0x7f8e14832cc8>

# 对于变量重新赋值不会对对象进行复制
y <- c(1, 2)

untracemem(x); untracemem(y)
rm(x, y)
```

### 17-函数

- 函数的自变量是只读的， 函数中定义的局部变量只在函数运行时起作用， 不会与外部或其它函数中同名变量混杂
- 函数返回一个对象作为输出， 如果需要返回多个变量， **可以用列表进行包装**
- 定义
    - `函数名 <- function(形式参数表) 函数体`
    - 函数体是一个表达式或复合表达式（复合语句）， 以复合表达式中最后一个表达式为返回值， 也可以用`return(x)`返回`x`的值。 如果函数需要返回多个结果， 可以打包在一个列表（list）中返回。 形式参数表相当于函数自变量，可以是空的， 形式参数可以有缺省值， R的函数在调用时都可以用“形式参数名=实际参数”的格式输入自变量值。
    - `f <- function(x) 1/sqrt(1 + x^2)`
    - 简写语法: `\(x)`
        - 上面等价于 `f <- \(x) 1/sqrt(1 + x^2)`
- 向量化
    - R函数有一个向量化的好处， 在上述函数调用时，如果形式参数`x`的实参是一个向量， 则结果也是向量，结果元素为实参向量中对应元素的变换值
- 一个自定义R函数由三个部分组成：
    - 函数体`body()`，即要函数定义内部要执行的代码；
    - `formals()`，即函数的形式参数表以及可能存在的缺省值，这是一个列表对象；
    - `environment()`，是函数定义时所处的环境， 这会影响到参数表中缺省值与函数体中非局部变量的的查找。
- 函数调用
    - 在调用函数时， 如果以“形参名=实参值”的格式输入参数， 则“形参名”与定义时的形参名完全匹配时最优先采用； 如果“形参名”是定义时的形参名的前一部分子串， 即部分匹配， 这时调用表中如果没有其它部分匹配， 也可以输入到对应的完整形参名的参数中； 按位置匹配是最后才进行的。 有缺省值的形参在调用时可省略。
    - 形参部分匹配不太严谨, 设置 `options(warnPartialMatchArgs = TRUE)`
    - 如果调用函数的形参、实参对应关系保存在列表中， 可以用函数`do.call()`来表示函数调用
        - 例如 `do.call(fsub, list(3, y=1))` 等价于 `fsub(3, y=1)`
- 复合调用
    - R在4.1.0版本以后定义了一个管道运算符“`|>`”， 在magrittr包中也定义了类似的运算符“`%>%`”， 可以使得这种复合调用按照正常的执行次序来写
- 递归调用
    - R中在递归调用时， 最好用 `Recall` 代表调用自身， 这样保证函数即使被改名（在R中函数是一个对象， 改名后仍然有效）递归调用仍指向原来定义。
- 向量化
    - 有些函数 (比如用到了 if) 仅能作用于标量, 若要修改为针对向量的, 可以 1. 手动在函数内部实现 for 循环; 2. 函数`Vectorize`可以将这样的操作自动化
    - 例如 函数 g 是针对标量的, 则 `gv <- Vectorize(g)` 将函数改造为适合向量输入
    - 还可以使用`purrr::map()`或基本R的`lapply()`等泛函实现对各个元素的函数变换。
- 无名函数
    - R允许使用没有函数名的函数对象, `lapply`类的函数经常使用无名的函数对象作为输入
- 变量作用域
- 全局变量和工作空间
    - 在所有函数外面（如R命令行）定义的变量是全局变量。 在命令行定义的所有变量都保存在工作空间 （workspace）， 也称为全局环境中。
        - 在RStudio的Environment窗格可以看到“Global Environment”的内容， 分为数据框(Data)、其它变量(Values)和函数(Functions)三类。
    - 在命令行可以用`ls()`查看工作空间内容。 `ls()`中加上`pattern`选项可以指定只显示符合一定命名模式的变量
        - 例如 `ls(pattern="^tmp[.]")` 显示所有以`tmp.`开头的变量
    - 用`object.size()`函数查看变量占用存储大小， 单位为字节。
    - `rm()`中还可以用`list`参数指定一个要删除的变量名表
        - 例如 `rm(list=ls(pattern="^tmp[.]"))`
    - 用`save()`函数保存工作空间中选择的某些变量； 用`load()`函数载入保存在文件中的变量
        - `save(my.large.data, file="my-large-data.RData")`
    - 实际上，R的工作空间是R的变量搜索路径中的一层， 大体相当于全局变量空间。 R的已启用的软件包中的变量以及用命令引入的变量也在这个搜索路径中。 用 `search()`返回当前的 **搜索路径**。

```r
fsub <- function(x, y = 0) {
    cat("x=", x, " y=", y, "\n")
    x - y
}
attributes(fsub)
class(fsub)
typeof(fsub)

body(fsub)
formals(fsub)
formalArgs(fsub)
environment(fsub)

# 函数调用
fsub(3, y = 1)
do.call(fsub, list(3, y = 1))

# 三个语句都用到了无名函数
vapply(iris[, 1:4], function(x) max(x) - min(x), 0.0)
# 最后一个参数 FUN.VALUE 指定函数返回类型
d <- scale(Filter(is.numeric, iris))
integrate(function(x) sin(x)^2, 0, pi)
```

### 19-函数进阶

from [here](https://www.math.pku.edu.cn/teachers/lidf/docs/Rbook/html/_Rbook/p-advfunc.html)

- 函数调用的各种形式
- 泛函
    - 许多函数需要用函数作为参数，称这样的函数为**泛函**(functionals)。 典型的泛函是`lapply`类函数。 这样的函数具有很好的通用性， 因为需要进行的操作可以输入一个函数来规定， 用输入的函数规定要进行什么样的操作。

### 26-数据整理

from [here](https://www.math.pku.edu.cn/teachers/lidf/docs/Rbook/html/_Rbook/summary-manip.html)

- dplyr包和tidyr包定义了一系列“动词”， 可以用比较自然的方式进行数据整理。 较复杂的分组操作还可以利用purrr包的`map`类函数。
- 为了使用这些功能，可以载入`tidyverse`包， 则magrittr包，readr包，dplyr包和tidyr包都会被自动载入

- `filter()`选择行子集
    - `filter()` 按条件选出符合条件的行组成的子集
- `slice(.data, ...)` 用来选择指定序号的行子集
    - 正的序号表示保留，负的序号表示排除
- sample_n 对观测随机抽样
    - size, replace, weight
- distinct() 去除重复行
    - distinct(d.class, sex, age) 注意不是写成字符串, 而是直接写变量名， 这是dplyr和tidyr包的特点
- `drop_na()` 去除指定的变量有缺失值的行
    - 基本stats包的`complete.cases`函数返回是否无缺失值的逻辑向量， `na.omit`函数则返回无缺失值的观测的子集。
- select() 选择列子集
    - d.class |> select(name:age, weight, -height) |> head()
    - `:` 表示列范围, 也可以用 `3:5` 的形式;  `-` 扣除, `,` 多选
    - `select()`有若干个配套函数可以按名字的模式选择变量列, `one_of(c('name', 'sex')), starts_wth("sex"), ends_with, contains(), matches("^[[:alpha:]]+[[:digit:]]+$"), num_range("x", 1:3 )`
    - see <https://tidyselect.r-lib.org/reference/language.html>
    - R函数subset也能对数据框选取列子集和行子集。
- pull() 取出单个变量为向量
    - `head(d.class, 3) |> pull(name)` 注意选择的列名不是字符串
    - 如果要取出的变量名保存在一个字符型变量`varname`中， 可以用`pull(.data, !!sym(varname))`这种格式； 如果`varname`是函数的自变量， 可以用`pull(.data, {{ varname }})`这种格式
    - 也可以select一列之后再用 pull
        - `varname ="name"; d.class |> select(one_of(varname)) |> pull()`
    - 基于基本R， 也可以用`d.class[["name"]]`这种格式取出一列为普通变量， 如果`varname`保存了变量名， 可以用`d.class[[varname]]`这种格式
    - 不能用`d.class[,"name"]`这种方法， 对于tibble类型， 其结果仍是一个子数据框； 用`d.class["name"]`这种格式， 结果也是一个子数据框。
- arrange()排序
    - `arrange(d.class, sex, desc(age))`
    - desc() 包裹想要降序排列的变量
    - 排序时不论升序还是降序， 所有的缺失值都自动排到末尾。
    - R函数`order()`可以用来给出数据框的排序次序， 然后以其输出为数据框行下标， 可以将数据框排序
- rename() 修改变量名
    - `dplyr::rename(d.class, h=height, w=weight)`
- mutate()计算新变量
    - `mutate(d.class, rwh=weight/height, sexc=ifelse(sex=="F", "女", "男"))`
    - 用`mutate()`计算新变量时如果计算比较复杂， 也可以用多个语句组成复合语句
        - `secx={x=rep("男", length(sex)); x[sex=="F"]="女"; x}`
- tranmute()生成新变量的数据框
    - 函数`transmute()`用法与`mutate()`类似， 但是仅保留新定义的变量， 不保留原来的所有变量
    - 给数据框中某个变量赋值为NULL可以修改数据框， 从数据框中删去该变量。
- 用管道连接多次操作
    - 如果管道传递的变量在下一层调用中不是第一自变量， 可以用`.`代表， 这种用法需要使用magrittr的`%>%`管道而不是标准的`|>`管道
    - `d.class %>% lm(weight~height, data=.) %>% coef()` 如果管道输入的变量不是下一个函数的第一个变量, 采用 `.`, 不是标准的 `|>` 管道
- expand_grid()函数
    - 在进行有多个因素的试验设计时， 往往需要生成多个因素完全搭配并重复的表格。 tidyr包的函数`expand_grid()`可以生成这样的重复模式。 基本R的`expand.grid()`功能类似。 基本R的gl函数提供了更简单的功能。
    - `tidyr::expand_grid(group=1:3, subgroup=1:2, obs=1:2)` 生成 12 行的观测(行)
- 宽表转换为长表
    - 实际数据中经常需要将数据框进行长宽格式的转换。 以典型的纵向数据为例， 每个受试者有次随访的记录值， 如果每个受试者的所有随访记录值存放在一个观测中， 就称为宽表， 如果每个受试者的随访记录值存放在多个观测的一列中， 另外增加一列表示记录时间， 就称为长表。
    - tidyr的`pivot_longer()`可以将宽表转换成长表， `pivot_wider()`可以将长表转换成宽表。 基本R的`reshape()`函数也可以进行长宽格式的转换。 reshape2包也提供了较丰富的长宽表转换功能。 建议优先使用tidyr包的功能。
    - pivot_longer
        - tidyr的pivot_longer()函数可以将横向的多次观测堆叠在一列中。
        - `dwide1 |> pivot_longer(`1`:`4`, names_to="time", values_to="response", values_drop_na=TRUE)` 将原表格中的名字为 1-4 的列转化为长表中新的一列 time, 表格值转化为 response 列
        - 有时要合并的列名中带有数值， 需要将这些数值部分提取出来， 这时可以用`names_prefix`指定要去掉的非数值前缀， 用`names_transform`指定将列名转换为值时结果的类型， `names_transform`是一个列表， 实现列表元素名到转换函数的映射
    - 相关需求:
        - 从列名中提取数字, 例如 `time1, time2, time3` 转化为 time 列, 值转化为新的一列
        - 从列名中提取多个分类变量值, 例如 `F_1, F_2, M_1, M_2` 列名表示男女赞成和反对, 需要从中提取 gender, direction 两列, 值转化为新的一列
        - 一行中有多个属性的多次观测的情形, 例如 `x1,x2,x3, y1,y2,y3` 分别记录了 x和y 两个指标不同时间的值, 需要转化为 x,y,time 三列, 此时值会转化到 xy 两列中
- 长表转换为宽表
    - 需求
        - 将多个混在一起的变量拆开, 例如 variable 一列中包括 x,y 两个指标, 转化为 x,y 两列, 原本的 value 列变为相应的值
        - 将交叉类别合并到一个观测, 例如有 set, type 两列, 分别包括 (F,M), (Benign, Malignant) 等值, 转化为 F_Benign 等列, 原本的 value 列变为相应的值
- seperate(), extract() 拆分数据列
    - separate
        - `d.sep |> separate(`succ/total`, into=c("succ", "total"), sep="/", convert=TRUE)`
        - 其中`into`指定拆分后新变量名， `sep`指定分隔符， `convert=TRUE`要求自动将分割后的值转换为适当的类型。 `sep`还可以指定取子串的字符位置， 按位置拆分各个子串。
    - extract
        - 函数`extract()`可以按照某种正则表达式表示的模式从指定列拆分出对应于正则表达式中捕获组的一列或多列内容
        - 例如, 对于数据 dexp 的 design 列, 若其为 AB, BB, AA BA 这样的形式, 要将其拆分为两个变量, 可以用 `extract(dexp, design, into=c("fac1", "fac2"), regex="(.)(.)")`
- unite(),  合并数据列
    - `d.sep |> separate(`succ/total`, into=c("succ", "total"), sep="/", convert=TRUE) |> unite(ratio, succ, total, sep=":")`
    - `unite()`的第一个参数是要修改的数据框， 这里用管道`|>`传递进来， 第二个参数是合并后的变量名（`ratio`变量）， 其它参数是要合并的变量名，`sep`指定分隔符。
    - 实际上用`mutate()`、`paste()`或者`sprintf()`也能完成合并。
- 数据框纵向合并
    - 矩阵或数据框要纵向合并，使用`rbind`函数即可。 dplyr包的`bind_rows()`函数也可以对两个或多个数据框纵向合并。 要求变量集合是相同的，变量次序可以不同。
- 横向合并
    - 为了将两个行数相同的数据框按行号对齐合并， 可以用基本R的`cbind()`函数或者dplyr包的`bind_cols()`函数。
    - `inner_join(d1.class, d2.class, by=c("name"="name"))`
    - `left_join()`按照`by`变量指定的关键列匹配观测， 左数据集所有观测不论匹配与否全部保留， 右数据集仅使用与左数据集能匹配的观测。 不指定`by`变量时， 使用左、右数据集的共同列作为关键列。 如果左右数据集关键列变量名不同， 可以用`by=c("左名"="右名")`的格式。
    - 类似地， `right_join()`保留右数据集的所有观测， 而仅保留左数据集中能匹配的观测。 `full_join()`保留所有观测。 `inner_join()`仅保留能匹配的观测。
- 利用第二个数据集筛选
    - `left_join()`将右表中与左表匹配的观测的额外的列添加到左表中。 如果希望按照右表筛选左表的观测， 可以用`semi_join()`， 函数`anti_join()`则是要求保留与右表不匹配的观测。
- 数据集的集合操作
    - R的`intersect()`，`union()`, `setdiff()`本来是以向量作为集合进行集合操作。 dplyr包也提供了这些函数， 但是将两个tibble的各行作为元素进行集合操作。
- 标准化
    - 设x是各列都为数值的列表(包括数据框和tibble)或数值型矩阵， 用`scale(x)`可以把每一列都标准化， 即每一列都减去该列的平均值，然后除以该列的样本标准差。 用`scale(x, center=TRUE, scale=FALSE)`仅中心化而不标准化。
    - 比如缩放到 0-1 之间 `d.class %>% select(height, weight) %>% scale(center=apply(., 2, min), scale=apply(., 2, max)-apply(., 2, min))`
        - 上面的要求也可以自定义一个函数, 最后调用 scale 来实现

### 27-数据汇总

from [here](https://www.math.pku.edu.cn/teachers/lidf/docs/Rbook/html/_Rbook/summary-summ.html)

- 用 dplyr 做数据汇总
    - `summarise(d.cancer, nobs=n(), n=sum(!is.na(age)), meam.age=mean(age, na.rm=TRUE), sd.age=sd(age, na.rm=TRUE))`
    - summarise 中常用的汇总函数
        - 位置度量：`mean()`, `median()`。
        - 分散程度（变异性）度量：`sd()`, `IQR()`, `mad()`。
        - 分位数：`min()`, `max()`, `quantile()`。
        - 按下标查询，如`first(x)`取出`x[1]`， `last(x)`取出`x`的最后一个元素， `nth(x,2)`取出`x[2]`。 可以提供一个缺省值以防某个下标位置不存在。
        - 计数：`n()`给出某个组的观测数， `sum(!is.na(x))`统计`x`的非缺失值个数， `n_distinct(x)`统计`x`的不同值个数(缺失值也算一个值)。 `count(x)`给出`x`的每个不同值的个数（类似于`table()`函数）。
- 多个变量的统计
    - `summarise_at(d.cancer, c("v0", "v1"), list(avg=~mean(.), std=~sd(.)), na.rm=TRUE)`
        - 第二个参数设置要统计的列, 也可以用 `5:6` 的形式指定
        - 选项`na.rm`将作为`...`格式的参数传递给统计函数`mean`和`sd`
        - 第三个参数可以为
            - 一个函数, 如 `mean`
            - 一个如`~ f(.)`这样的自定义无名函数，其中`.`表示自变量
            - 函数或者自定义无名函数的列表
        - 结果统计量自动命名为“`变量名_统计量名`”的格式。
    - `summarise_if(d.cancer, is.numeric, mean, na.rm=TRUE)`
        - 其中的`is_numeric`用来筛选需要进行统计的变量子集， 可以替换成其它的示性函数（对每列返回一个逻辑值的函数）
- 用dplyr作数据分组汇总: group_by
    - 数据汇总问题更常见的是作分组汇总。 dplyr包的`group_by()`函数对数据框（或tibble）分组， 随后的`summarise()`将按照分组汇总。
        - `d.cancer %>% group_by(sex) %>% summarise(count=n(), mean.age=mean(age, na.rm=TRUE))`
        - 为了查询数值型变量取值满足某种条件的个数和比例， 可以将该条件用`sum()`和`mean()`函数统计
            - `d.cancer %>% group_by(sex) |> summarise(nold=sum(age>=60, na.rm=TRUE), pold=nold/n())`
    - `group_by()`分组后除了可以分组汇总， 还可以分组筛选
        - `d.cancer |> group_by(sex) |> filter(rank(desc(v0)) <= 2) |> arrange(sex, desc(v0))` 分别筛选出男女中 v0 最大的两项
    - 在分组后也可以根据每组的统计量用`mutate()`定义新变量
        - `d.cancer |> group_by(sex) |> mutate(v0s=v0/max(v0), v1s=v1/sum(v1))` 定义 v0s, v1s 为归一化之后的结果
- 交叉分类的汇总
    - 用`group_by()`交叉分组汇总后的结果不是普通的tibble， 总是带有外层分组信息， 最内层的分组信息不再有效。 不注意这种规定在后续的使用中可能会产生问题， 为此， 可以用`ungroup()`函数取消分组。
        - 例如对于 `g1.cancer <- d.cancer |> group_by(sex, type) |> summarise(freq=n())` 这一分组结果, 包括 sex, type, freq 三列
        - 若直接 `g1.cancer |> summarise(ntotal=sum(freq))`, 会得到 sex, ntotal 两列的分组结果.
        - 采用 `g1.cancer |> ungroup() |> summarise(ntotal=sum(freq))` 取消分组, 得到单一的统计结果
- tibble中的列表列
    - `nest`和`unnest`
        - dplyr包的`group_by`与`summarise`、`summarise_at`等函数配合， 可以对数据框分组计算各种概括统计量。
            - 但是，如果分组以后希望进行更复杂的统计分析， 比如分组回归建模， `summarise`就不够用了。 这时， 可以用基本R的`split`函数将数据框按某个分类变量拆分为子数据框的列表， 然后用purrr包的map类函数分类建模， 最终将各个模型的结果合并为一个数据框。
        - 上面的办法虽然可行， 但是管理不够方便。 tidyr包（属于tidyverse系列，载入tidyverse时会自动载入）提供了`nest`和`unnest`函数， 可以将子数据框保存在tibble中， 可以将保存在tibble中的子数据框合并为一个大数据框。 实际上， **tibble允许存在数据类型是列表(list)的列**， 子数据框就是以列表数据类型保存在tibble的一列中的。
    - unnest
        - 除了 nest 返回的结果, 也可以直接生成列表类型的列， 符合条件时可以用`unnest()`合并为大数据框
        - 例如, 先定义一个 tibble `d1 = tibble(id=1:2, df=vector("list", 2))`, 分别对于两行 df 赋值(注意类型需要是list) `d1[["df"]][1] = list(tibble(x=1, y=2))`, `d1[["df"]][2] = list(tibble(x=11:12, y=21:22))`, 两个 list 内保存的 tibble 行数不同(分别是 1, 2). 然后可以用 unnest 展开 df 列, `d1 |> unnest(df)` 得到 id, x,y 三列, 一共展开成三行.
    - group_by 配合 nest
        - 例如 `n1.cancer <- d.cancer |> group_by(type) |> nest()` 利用 nest 将分组结果划分为两张表 (列表, 值保存的是数据框). 列名分别为 type, data
        - 可以用purrr包的`map()`等函数对每个子数据框进行处理， 结果可以用`mutate`保存为新的列表类型的列， 如果结果是数值型标量也可以保存为普通的数据框列。
        - 例如 `model.cancer = n1.cancer |> mutate(lmr = map(data, fmodel))` 对于 data 列中的每张表调用 fmodel 函数 (例如简单定义线性回归  `fmodel = function(subdf) lm(v1~v0, data=subdf)`), 保存为 lmr 列
        - 现在 lmr列保存的是一个线性回归的结果, 可以提取出其中的单个数值 `model.cancer |> mutate(r.squared=map_dbl(lmr, frsqr)) |> select(-data)`, 这里的 frsqr 可以定义为 `frsqr = function(lm) { summary(lm)$r.squared }`
        - 要返回多个值, 保存在一个 tibble 中; 为了使得这些值展开保存在同一行, 可以用`unnest`将每个组提取的回归结果转换为普通的数据框列
            - 例如 `model.cancer |> mutate(outlist=map(lmr, fextract)) |> unnest(outlist)`, 其中 `fextract = function(df.lm) { x1 = coef(df.lm); tibble(intercept=x1[1], v0=x1[2], r.squared=summary(df.lm)$r.squared) }` 函数提取lm模型的相关属性. 这里通过 unxest 函数将 outlist 列展开为 intercept, v0, r.squared 列
        - 返回的还可以不止一列! 例如, 定义 `fcoefmat <- function(mod){ as_tibble(summary(mod)$coefficients, rownames="term") }` 取得lm模型的回归系数信息, 这里的 tibble 大小为 (2,5); 同样可以 `model.cancer %>% mutate(outlist=map(lmr, fcoefmat)) %>% unnest(outlist)` 进行展开, 这样的话原本的一行变为两行
            - broom扩展包提供了tidy函数， 可以将统计模型的输出转换为数据框, (替代上面自己实现的 fcoefmat), 直接写成 `model.cancer |> mutate(outlist=map(lmr, broom::tidy)) |> unnest(outlist)`
        - 也可以将一个 df 展开, 实际上对于 nest 对象 n1.cancer 可以直接 `n1.cancer |> unnest(data)` 将 data 展开为原本的数据表
        - 例如, `model.cancer |> mutate(v1hat=map(lmr, ~fitted(.))) |> unnest(c(data, v1hat))` 对于数据进行 fit 得到 v1hat, 然后展开 data, v1hat 两列
    - summarise统计量用列表表示
        - 例如, 要统计 v0, v1 两列的最大最小值, 定义 summarise 中统计量为 value=list(c(range(v0), range(v1)))), 然后 `d.cancer |> group_by(type) |> summarise(stat=list(vnames), value=list(c(range(v0), range(v1)))) |> unnest(c(stat, value))`
        - 其中的统计量名字为 `vnames = expand_grid(var = c("v0", "v1"), stat = c("min", "max")) |> pmap_chr(paste, sep="_")`
- 基本R的汇总功能
    - summary()函数
        - summary, 可以获得每个连续型变量的基本统计量， 和每个离散取值变量的频率
        - str, head
        - 用 boxplot 看分布, 例如 `boxplot(d.cancer[,c("v0", "v1")], main="肿瘤体积")`
    - 连续型变量概括函数
        - mean, std, var, sum, prod, min, max
        - 加 `na.rm=TRUE` 选项可以仅对非缺失值计算
        - `sort(x)` 返回排序后的结果。 `rev(x)`把`x`所有元素次序颠倒后返回。 `quantile(x, c(0.05, 0.95))` 可以求`x`的样本分位数。 `rank(x)` 对`x`求秩得分（即名次，但从最小到最大排列）。
    - 分类变量概括
        - 分类变量一般输入为因子。 对因子或其它向量`x`， `table(x)` 返回 `x`的每个不同值的频率（出现次数）， 结果为一个类（class）为table的一维数组。 每个元素有对应的元素名，为`x`的各水平值。
        - table
            - `res2 <- with(d.cancer, table(sex, type));` 返回的是一个 table. 对于table 可以用下面的函数处理
            - prop.table(res) 转为频率表, 第二个参数指定按照哪一个 dim 求频率
            - as.data.frame()
            - addmargins 行列求和
            - margin.table(res2, 2) 对于行/列 (dim) 求和
            - barplot(res2, legend=TRUE, beside=TRUE) 箱图
        - dplyr包的 `count()` 功能与 `table()` 类似。
    - 数据框概括
        - 用`colMeans()`对数据框或矩阵的每列计算均值， 用`colSums()`对数据框或矩阵的每列计算总和。 用`rowMeans()`和`rowSums()`对矩阵的每行计算均值或总和。
        - 数据框与矩阵有区别， 某些适用于矩阵的计算对数据框不适用， 例如矩阵乘法。 用`as.matrix()`把数据框的数值子集转换成矩阵。
        - 对矩阵，用`apply(x, 1, FUN)`对矩阵x的每一行使用函数FUN计算结果， 用`apply(x, 2, FUN)`对矩阵x的每一列使用函数FUN计算结果。
        - 如果`apply(x,1,FUN)`中的FUN对每个行变量得到多个 m 结果， 结果将是一个矩阵，行数为 m，列数等于nrow(x)。 如果`apply(x,2,FUN)`中的FUN对每个列变量得到多个 m 结果， 结果将是一个矩阵，行数为 m，列数等于ncol(x)。
        - `apply(as.matrix(iris[,1:4]), 2, function(x) c(n=sum(!is.na(x)), mean=mean(x, na.rm=TRUE), sd=sd(x, na.rm=TRUE)))`
- 用基本R作分类汇总
    - 用`tapply()`函数进行分组概括. `tapply(X, INDEX, FUN)`, 其中`X`是一个向量， `INDEX`是一个分类变量， `FUN`是概括统计函数
        - `with(d.cancer, tapply(v0, sex, mean))` 利用 sex 分组, 计算 v0 列的平均值
    - 用 `aggregate()` 分组概括数据框
        - `aggregate`函数对输入的数据框用指定的分组变量（或交叉分组） 分组进行概括统计。
        - `aggregate()`第一个参数是数据框， 第二个参数是列表，列表元素是用来分组或交叉分组的变量， 第三个参数是概括用的函数， 概括用的函数的选项可以在后面给出
        - 例如 `aggregate(d.cancer[, c("age", "v0", "v1")], list(sex=d.cancer[["sex"]]), mean, na.rm=TRUE)` 根据 sex 分组, 计算 age, v0, v1 三列的平均值
        - 交叉分组后概括 `with(d.cancer, aggregate(cbind(v0, v1), list(sex=sex, type=type), mean, na.rm=TRUE))` 对于 sex, type 三个因子进行分组, 计算平均估值
    - 用 `split()` 函数分组后概括
        - split函数可以把数据框的各行按照一个或几个分组变量分为子集的列表， 然后可以用`sapply()`或`vapply()`对每组进行概括。
        - 例如, `sp = split(d.cancer[,c("v0", "v1")], d.cancer[["sex"]])` 分组, 然后 `sapply(sp, colMeans)`
            - 返回矩阵，行为变量v0, v1，列为不同性别， 值为相应的变量在各性别组的平均值。 当`sapply()`对列表每项的操作返回一个向量时， 总是列表每项的输出保存为结果的一列。 `colMeans`函数计算分组后数据框子集每列的平均值。
- 用plyr包进行分类概括
    - plyr包已经被dplyr、purrr包代替，不再继续开发新版本。 这部分内容仅作为备忘， 读者可以跳过。

## Learn-r 教程

!!! warning
    暂弃

- from <https://jcoliver.github.io/learn-r/>
- repo <https://github.com/jcoliver/learn-r>

### first plot

查看数据

- `head` shows us the first 6 rows in a data frame.
- `str` (structure) provides some information about the data stored in the data frame.
- `summary` provides even more information about the data, including some summary statistics for numerical data.

```r
# 读取数据, 绘制每个年份的 Life expectancy ~ GDP per capita 散点图, 保存到 pdf 中
# Read in data
all_gapminder <- read.csv(file = "data/gapminder-FiveYearData.csv",
                          stringsAsFactors = TRUE)

# Make new vector of Log GDP
all_gapminder$Log10GDP <- log10(all_gapminder$gdpPercap)

# Store values to use for some plotting parameters
symbol <- 18
sym_size <- 1.2
continents <- levels(all_gapminder$continent)
continent_colors <- c("red", "orange", "forestgreen", "darkblue", "violet")

# Create new vector for colors
all_gapminder$colors <- NA
# Loop over continents and assign colors
for (i in 1:length(continents)) {
  all_gapminder$colors[all_gapminder$continent == continents[i]] <- continent_colors[i]
}

# Find the unique values in the all_gapminder$year vector
years <- unique(all_gapminder$year)

# Now loop over each of the different years to create the PDFs.
for (curr_year in years) {
  # Subset data
  gapminder_one_year <- all_gapminder[all_gapminder$year == curr_year, ]
  
  # Open PDF device
  filename <- paste0("output/Life_exp_", curr_year, "_graph.pdf")
  pdf(file = filename, useDingbats = FALSE)
  # Create main plot
  plot(x = gapminder_one_year$Log10GDP, 
       y = gapminder_one_year$lifeExp, 
       main = "Life expectancy v. GDP", 
       sub = curr_year, 
       xlab = "Log(GDP Per capita)", 
       ylab = "Life expectancy (years)",
       col = gapminder_one_year$colors,
       pch = symbol,
       cex = sym_size,
       lwd = 1.5)
  
  # Add a legend
  legend("topleft", 
         legend = continents, 
         col = continent_colors,
         pch = symbol)
  
  # Add a regression line
  lifeExp_lm <- lm(gapminder_one_year$lifeExp ~ gapminder_one_year$Log10GDP)
  abline(reg = lifeExp_lm, lty = 2, lwd = 2)
  
  # Close PDF device
  dev.off()
}
```

#### 设置透明度: rgb, col2rgb

下面利用 `col2rgb, rgb` 函数自定义颜色透明度.

```r
# Investigating colors 将颜色转为 RGB 值
col2rgb(continent_colors)

# 转为 hax 颜色
rgb(1,1,0, .5)
rgb(red=255,green=255,blue=0, alpha=100, maxColorValue = 255)
# "#FFFF0064"
```

```r
continent_colors <- c("red", "orange", "forestgreen", "darkblue", "violet")
# Convert colors to RGB, so we can add an alpha (transparency) value
continent_rgb <- col2rgb(continent_colors)
continent_colors <- NULL
opacity <- 150
# Loop over each column (i.e. color) in continent_rgb and extract Red, Green, and Blue values
for (color_column in 1:ncol(continent_rgb)) {
  new_color <- rgb(red = continent_rgb['red', color_column],
                   green = continent_rgb['green', color_column], 
                   blue = continent_rgb['blue', color_column],
                   alpha = opacity,
                   maxColorValue = 255)
  continent_colors[color_column] <- new_color
}

# Create new vector for colors
gapminder$colors <- NA
# loop over continents and assign colors
for (i in 1:length(continents)) {
  gapminder$colors[gapminder$continent == continents[i]] <- continent_colors[i]
}

# Create main plot
plot(x = gapminder$Log10GDP, 
     y = gapminder$lifeExp, 
     main = "Life expectancy v. GDP", 
     xlab = "Log(GDP Per capita)", 
     ylab = "Life expectancy (years)",
     col = gapminder$colors,
     bg = gapminder$colors, 
     pch = symbol,
     cex = sym_size, 
     lwd = 1.5)
```

### stats with R

#### Student’s t

```r
# Subset data
setosa <- iris[iris$Species == "setosa", ]
versicolor <- iris[iris$Species == "versicolor", ]

# Run t-test
setosa.v.versicolor <- t.test(x = setosa$Petal.Length, y = versicolor$Petal.Length)

# Save results to file
sink(file = "output/petal-length-setosa-versicolor-t-test.txt")
setosa.v.versicolor
sink()
```

结果包括

- Test statistic, degrees of freedom, and p-value
- The confidence interval for the difference in means between the two data sets
- The means of each data set

```js
## 
##  Welch Two Sample t-test
## 
## data:  setosa$Petal.Length and versicolor$Petal.Length
## t = -39.493, df = 62.14, p-value < 2.2e-16
## alternative hypothesis: true difference in means is not equal to 0
## 95 percent confidence interval:
##  -2.939618 -2.656382
## sample estimates:
## mean of x mean of y 
##     1.462     4.260
```

#### Analysis of Variance (ANOVA)

注意用 summary 查看 aov 返回的对象 (和 lm 一样)

```r
# Run ANOVA on petal length
petal.length.aov <- aov(formula = Petal.Length ~ Species, data = iris)

# Save results to file
sink(file = "output/petal-length-anova.txt")
summary(object = petal.length.aov)
sink()
```

The species do have significantly different petal lengths (P < 0.001). If one wanted to run a post hoc test to assess how the species are different, a Tukey test comparing means would likely be the most appropriate option.

<https://www.r-bloggers.com/2013/06/anova-and-tukeys-test-on-r/>

```js
##              Df Sum Sq Mean Sq F value Pr(>F)    
## Species       2  437.1  218.55    1180 <2e-16 ***
## Residuals   147   27.2    0.19                   
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```

#### Linear regression

```r
# Read data from comma-separated values file
orig.gapminder <- read.csv(file = "data/gapminder-FiveYearData.csv",
                           stringsAsFactors = TRUE)

# Subset 2007 data
gapminder <- orig.gapminder[orig.gapminder$year == 2007, ]

# Plot to look at data
plot(x = gapminder$gdpPercap, y = gapminder$lifeExp)

# Create log-transformed GDP
gapminder$logGDP <- log10(gapminder$gdpPercap)

# Plot new variable
plot(x = gapminder$logGDP, 
     y = gapminder$lifeExp, 
     xlab = "log10(GDP)", 
     ylab = "Life Expectancy")

# Run linear model
lifeExp.v.gdp <- lm(formula = lifeExp ~ logGDP, data = gapminder)

# Save results to file
sink(file = "output/lifeExp-gdp-regression.txt")
summary(lifeExp.v.gdp)
sink()
```

回归结果

- Pr(>|t|) 小, 说明显著
- 16.585, which means that for every 10-fold increase in per capita GDP (remember we log10\-transformed GDP), life expectancy increases by almost 17 years. 系数说明, 人均GDP每增加10倍, 预期寿命增加约16.5

```js
## 
## Call:
## lm(formula = lifeExp ~ logGDP, data = gapminder)
## 
## Residuals:
##     Min      1Q  Median      3Q     Max 
## -25.947  -2.661   1.215   4.469  13.115 
## 
## Coefficients:
##             Estimate Std. Error t value Pr(>|t|)    
## (Intercept)    4.950      3.858   1.283    0.202    
## logGDP        16.585      1.019  16.283   <2e-16 ***
## ---
## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
## 
## Residual standard error: 7.122 on 140 degrees of freedom
## Multiple R-squared:  0.6544, Adjusted R-squared:  0.652 
## F-statistic: 265.2 on 1 and 140 DF,  p-value: < 2.2e-16
```

### multivariate analyses

#### PCA

### ggplot
