####################### 函数调用 #######################
# 2. 中缀
`-`(5, 2)
5 - 2
# 也可以自定义
`%+%` <- function(x, y) paste0(x, y)
"xyz" %+% "123"
`%+%`("xzy", "123")

# 3. 替换形式
x <- 1:2
names(x) <- c("a", "b")
x

# 相当于前缀形式
x <- 1:2
`*tmp*` <- x
x <- `names<-`(x, c("a", "b"))
rm(`*tmp*`)
x

# 4. 特殊形式
x <- 1:5
x[1]
`[`(x, 1)

x[1] <- 999
x <- `[<-`(x, 1, 99999)
x

for (i in 1:3) print(i)
`for`(i, 1:3, print(i))

########################### 句法作用域 #########################
f0 <- function() {
    x <- -1
    f1 <- function() {
        x + 100
    }
    x <- 1000
    f1()
}
f0()
# 1100


solve.sqe <- function(x) {
    fd <- function(a, b, c) b^2 - 4 * a * c
    d <- fd(x[1], x[2], x[3])
    if (d >= 0) {
        return((-x[2] + c(1, -1) * sqrt(d)) / (2 * x[1]))
    } else {
        return(complex(real = -x[2], imag = c(1, -1) * sqrt(-d)) / (2 * x[1]))
    }
}
solve.sqe(c(1, -2, 1))
solve.sqe(c(1, -2, 2))

######################### 懒惰求值 #########################
f <- function(x, y = ifelse(x > 0, TRUE, FALSE)) {
    x <- -111
    if (y) x * 2 else x * 10
}
f(5)
# -1110

f <- function(x) {
    if (missing(x)) {
        x <- 1
    }
    x
}
f() # 1
f(2) # 2


############################### 辅助嵌套函数 ###############################
solve.sqe <- function(x) {
    fd <- function(a, b, c) b^2 - 4 * a * c
    d <- fd(x[1], x[2], x[3])
    if (d >= 0) {
        return((-x[2] + c(1, -1) * sqrt(d)) / (2 * x[1]))
    } else {
        return(complex(real = -x[2], imag = c(1, -1) * sqrt(-d)) / (2 * x[1]))
    }
}
solve.sqe(c(1, -2, 1))
solve.sqe(c(1, -2, 2))

########################### 泛函 ###########################
# purrr::map
library(tidyverse)
d.class <- readr::read_csv("./data/Rbook/class.csv")
typeof(d.class[["age"]])
library(purrr)
map(d.class, typeof) # map 结果总为 list
unlist(map(d.class, typeof))

map_chr(d.class, typeof)
map_lgl(d.class, is.numeric)


# ... 形参
map_dbl(d.class[, 3:5], mean, trim = 0.10) # trim 传递给 mean
# 其他的筛选列方式
dsub <- d.class[, map_lgl(d.class, is.numeric)]
map_dbl(dsub, mean, trim = 0.10)
dsub <- purrr::keep(d.class, is.numeric)
map_dbl(dsub, mean, trim = 0.10)

# strsplit 例子
s <- c(
    "10, 8, 7",
    "5, 2, 2",
    "3, 7, 8",
    "8, 8, 9"
)
strsplit(s[1], ",", fixed = TRUE)[[1]] %>%
    as.numeric() %>%
    sum()
tmpr <- strsplit(s, ",", fixed = TRUE)
tmpr
s %>%
    strsplit(",", fixed = TRUE) %>%
    map(as.numeric) %>%
    map_dbl(sum)
# 无名函数
map_dbl(
    strsplit(s, split = ",", fixed = TRUE),
    function(x) sum(as.numeric(x))
)
# 简化写法
# .
# .x, .y
# ..1, ..2, ..3
map_dbl(strsplit(s, split = ",", fixed = TRUE), ~ sum(as.numeric(.)))

## 提取元素
od <- list(
    list(
        101,
        name = "李明", age = 15,
        hobbies = c("绘画", "音乐")
    ),
    list(
        102,
        name = "张聪", age = 17,
        hobbies = c("足球"),
        birth = "2002-10-01"
    )
)
map_dbl(od, function(x) x[[1]])
map_dbl(od, ~ .[[1]])
# 简写: 输入标量
map_dbl(od, 1)
map_chr(od, "name")
# 列表, 表示嵌套提取
map_chr(od, list("hobbies", 1))
# default选项指定查找不到成员时的选项
map_chr(od, "birth", .default = NA)

## 分组
# split 分组处理
d.class %>%
    split(d.class[["sex"]]) %>%
    map(~ lm(weight ~ height, data = .)) %>%
    map(coef) %>%
    map_dbl(2) # 这是取向量第二个元素
d.class %>% split(d.class[["sex"]])
# 采用 group_by, 结合 nest
d.class %>%
    group_by(sex) %>%
    nest() %>%
    mutate(lmr = map(data, ~ lm(weight ~ height, data = .))) %>%
    mutate(coef = map_dbl(lmr, ~ summary(.)$coef[2])) %>%
    ungroup() %>%
    select(coef)

############### modify ###############
# 区分于 map 返回由函数所决定的类型, modify 返回和输入相同的类型
modify(d.class, ~ if (is.numeric(.x)) .x - median(.x) else .x)
# modify_if 仅修改满足条件的元素
modify_if(d.class, is.numeric, ~ .x - median(.x))

############### map2 ###############
# map2 可以接受两组参数, 对于 index 相同的元素进行操作
d1 <- tibble(
    x1 = c(106, 108, 103, 110),
    x2 = c(101, 112, 107, 105)
)
d2 <- tibble(
    x1 = c(104, 111, 112, 109),
    x2 = c(102, 114, 105, 107)
)
# 例如求和后计算增长率
map2_dbl(d1, d2, ~ (sum(.y) - sum(.x)) / sum(.x))
map2(d1, d2, ~ (.y - .x) / .x) # 返回 list
modify2(d1, d2, ~ (.y - .x) / .x) # 返回 tibble

############### walk ###############
# 对于不需要返回的, 可以用 walk
walk(d.class, ~ cat(typeof(.), "\n"))
# walk2
d.class %>%
    split(d.class[["sex"]]) %>%
    # split 根据性别分组, 得到的包括两个子df 的列表, 名字为 sex 列的元素 F和M
    walk2(paste0("calss-", names(.)), ~ {
        print(.y)
        print(.x)
    })
#   walk2(paste0("class-", names(.), ".csv"), ~ write.csv(.x, file=.y))

############### imap ###############
# 接受一张表, 处理函数的第二个参数 .y 为所输入表各个元素的 index: 有名字的是names, 没有的则是数字
iwalk(d.class, ~ cat(.y, ": ", typeof(.x), "\n"))
imap_chr(d.class, ~ paste0(.y, " ==> ", typeof(.x))) %>% unname()
# 没有 names 时
dl <- list(1:5, 101:103)
iwalk(dl, ~ cat("NO. ", .y, ": ", .x[[1]], "\n"))


############### pmap ###############
# 1. 输入 list
x <- list(101, name = "李明")
y <- list(102, name = "张聪")
z <- list(103, name = "王国")
pmap(list(x, y, z), c)
# 2. 输入数据框时, 是对每一行处理!
d <- tibble::tibble(
    x = 101:103,
    y = c("李明", "张聪", "王国")
)
pmap_chr(d, function(...) paste(..., sep = ":"))

# 使用 pmap 相较于 map 的区别在于, 由于打包成 list 可以有名字, 可以用名字来调用
# 例如要对于 x 数据, 根据不同裁剪比例计算 mean, 1. 若用 map 可以这么做
set.seed(11)
x <- rcauchy(1000)
trims <- c(0.05, 0.1, 0.2, 0.3, 0.4)
map_dbl(trims, ~ mean(x = x, trim = .))
# 2. 而采用 pmap 可以进行带名字的传递.
# 可以用pmap()的列表元素名自动对应到调用函数形参名的方法
pmap_dbl(list(trim = trims), mean, x = x) # trims 已经传入了!
# pmap_dbl(list(trim = trims), ~ mean(x, trim = trim)) # 注意 ~ 函数不能用命名形式, 报错 找不到对象'trim'
pmap_dbl(list(trim = trims), ~ mean(x, trim = .x)) # 这样可以
pmap_dbl(list(trim = trims), function(trim) mean(x, trim = trim)) # 而需要指定未命名函数的参数名字

test <- seq_along(trims)
pmap_chr(
    # 注意是 as.list 才能将向量转为列表! 而不是 list(trims)
    list(trim = as.list(trims), test = as.list(test)),
    function(test, trim) paste0("接收到: trim=", trim, "; test=", test)
)

# `invoke_map(.f, .x, ...)`
sim <- tribble(
    ~f,      ~params,
    "runif", list(min = -1, max = 1),
    "rnorm", list(sd = 5),
    "rpois", list(lambda = 10)
)
sim %>%
    mutate(sim = invoke_map(f, params, n = 10))


########################## reduce ##########################
reduce(1:4, `+`)
x <- list(
    c(2, 3, 1, 3, 1),
    c(1, 5, 3, 3, 2),
    c(5, 4, 2, 5, 3),
    c(1, 4, 3, 2, 5)
)
x[[1]] %>%
    intersect(x[[2]]) %>%
    intersect(x[[3]]) %>%
    intersect(x[[4]])
y <- x[[1]]
for (i in 2:4) y <- intersect(y, x[[i]])
y
reduce(x, intersect)

#### accumulate ####
cumsum(1:4)
accumulate(x, union)
accumulate(x, union) %>%
    map(~ sort(unique(.)))

############################## purrr包中使用示性函数的泛函 ##############################
some(d.class, is.factor)
detect(c(1, 5, 77, 105, 99, 123), ~ . >= 100)
detect_index(
    c(1, 5, 77, 105, 99, 123),
    ~ . >= 100
)
# 基本函数中的 which 可以返回所有 index
which(c(1, 5, 77, 105, 99, 123) >= 100)
d.class %>%
    keep(is.numeric) %>%
    map_dbl(~ sum(.^2))

modify_if(d.class, is.numeric, `/`, 100)


################################## 基本R的函数式编程支持 ##################################
# apply
# apply(X, MARGIN, FUN, ..., simplify = TRUE)
apply(d.class, 2, typeof)
# 返回列表
lapply(d.class, typeof)
# sapply 尝试将结果变为向量/矩阵
sapply(d.class, typeof)
# 第三个参数指定返回类型
vapply(d.class, typeof, "")

# Map
d <- data.frame(
    x = c(1, 7, 2),
    y = c(3, 5, 9)
)
Map(function(x) sum(x^2), d)
Map(max, d$x, d$y)
Map(max, d$x, d$y) |> unlist()
# 类似 sapply 简化 Map 结果
mapply(max, d$x, d$y)

# Reduce
set.seed(5)
x <- replicate(4, sample(
    1:5,
    size = 5, replace = TRUE
), simplify = FALSE)
x
Reduce(intersect, x)

# Filter
f <- function(x) x > 0 & x < 1
Filter(f, c(-0.5, 0.5, 0.8, 1))


################################ 函数工程 closure #################################
# 例子1: 执行次数计数
f.gen <- function() {
    runTimes <- 0

    function() {
        runTimes <<- runTimes + 1
        print(runTimes)
    }
}
f <- f.gen()
f()
f()

# 例子2: 记录函数前后两次调用的时间差
make_stop_watch <- function() {
    saved.time <- proc.time()[3]

    function() {
        t1 <- proc.time()[3]
        td <- t1 - saved.time
        # <<- 算子
        saved.time <<- t1

        cat("流逝时间（秒）：", td, "\n")
        invisible(td)
    }
}
ticker <- make_stop_watch()
ticker()
## 流逝时间（秒）： 0
for (i in 1:1000) sort(runif(10000))
ticker()
## 流逝时间（秒）： 1.53


# 懒惰求值的问题
make.pf <- function(power) {
    # 用force强制对于输入参数求值而不是懒惰求值
    force(power)

    function(x) x^power
}
p <- 2
square <- make.pf(p)
p <- 3
square(4)


# 函数算子例子
dot_every <- function(f, n) {
    i <- 0
    function(...) {
        i <<- i + 1
        if (i %% n == 0) cat(".")
        f(...)
    }
}
sim <- function(i) {
    x <- runif(1E6)
    invisible(sort(x))
}
walk(1:100, dot_every(sim, 10))


################################# 环境 ##################################
# rlang 包
e1 <- rlang::env(
    a = FALSE,
    b = "a",
    c = 2.3,
    d = 1:3
)

e1$e <- list(x = 1, y = "abcd")


# 函数环境
# 1. 一般的是全局环境, 没啥用
f1 <- function(x) 2 * x
rlang::fn_env(f1)
## <environment: R_GlobalEnv>
# 2. 闭包保留了函数环境
f1 <- function() {
    times <- 0
    f2 <- function() {
        times <<- times + 1
        cat("NO. ", times, "\n", sep = "")
    }
    print(rlang::fn_env(f2))
    f2
}
f2b <- f1()
## <environment: 0x00000201dc5096d8>
print(rlang::fn_env(f2b))
## <environment: 0x00000201dc5096d8>
f2b()
f2b()


# 调用栈
f1 <- function(x) {
    f2(x = 2)
}
f2 <- function(x) {
    f3(x = 3)
}
f3 <- function(x) {
    stop()
}
f1()
##  Error in f3(x = 3) :
## 4. stop()
## 3. f3(x = 3)
## 2. f2(x = 2)
## 1. f1()