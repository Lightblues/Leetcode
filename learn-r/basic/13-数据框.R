d <- data.frame(
    name = c("李明", "张聪", "王建"),
    age = c(30, 35, 28),
    height = c(180, 162, 175),
    stringsAsFactors = FALSE
)
print(d)
typeof(d) # list
class(d) # data.frame
attributes(d)
d$name
View(d)
str(d)


names(d)
colnames(d) # 相等
rownames(d) # 默认为 1,2,3

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

################# 行名 #################
# tibble 中不使用了 —— 可以认为行名是特殊的一列 (主键) —— join
# 1. 一个例子, 行名作为索引
# 指定行名
dm <- data.frame(
    "年级" = 1:6,
    "出游" = c(0, 2, 2, 2, 2, 1),
    "疫苗" = c(TRUE, FALSE, FALSE, FALSE, TRUE, FALSE)
)
rownames(dm) <- dm[["年级"]]
dm[["年级"]] <- NULL
# 利用行名索引
ind <- c(2, 1, 1, 3)
# 这样列名不太好 dm[as.character(ind), ]
xx <- dm[as.character(ind), ]
rownames(xx) <- NULL
xx

# 2. 可以将 列名 作为单独的一列, 这里用 match 进行替代 !!
dm <- data.frame(
    "年级" = 1:6,
    "出游" = c(0, 2, 2, 2, 2, 1),
    "疫苗" = c(T, F, F, F, T, F)
)
ind <- match(c(2, 1, 1, 3), dm[["年级"]])
ind
## [1] 2 1 1 3
dm[ind, ]

################# tibble #################
library(tibble)
library(readr)

d.class <- read_csv("./data/Rbook/class.csv")
View(d.class)
class(d.class) # `spec_tbl_df`, `tbl_df`, `tbl`, `data.frame`

d.bp <- tibble(
    "序号" = c(1, 5, 6, 9, 10, 15),
    `收缩压` = c(145, 110, "未测", 150, "拒绝", 115)
)
d.bp
# 需要用 ~ 符号指定列名?
# `` 符号包裹可以避免非法变量名
tribble(
    ~序号, ~`收缩压`,
    1, 145,
    5, 110,
    6, NA,
    9, 150,
    10, NA,
    15, 115
)
dd <- readr::read_csv("序号,收缩压
1,145
5,110
6,NA
9,150
10,NA
15,115
")

########### 列表类型的列 ###########
ll <- tibble(
    x = 1:3,
    y = list(1, 1:2, 1:3)
)
ll$y[[2]]
ll$y[2] # 注意这种语法仍然返回一个列表

#################### 练习 ####################
d.class <- read_csv("./data/Rbook/class.csv")
View(d.class)
d.class["sex"] <- as.factor(d.class[["sex"]]) # 注意 ['class'] 得到的是 tibble 类型!

d.class[d.class$age >= 15, ]
d.class[d.class$age >= 15 & d.class$sex == "F", c("name", "age")]
d.class[["age"]]