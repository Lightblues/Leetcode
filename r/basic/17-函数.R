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

# 递归调用, 用 Recall
fib1 <- function(n) {
    if (n == 0) {
        return(0)
    } else if (n == 1) {
        return(1)
    } else if (n >= 2) {
        return(Recall(n - 1) + Recall(n - 2))
    }
}
for (i in 0:10) cat("i =", i, " x[i] =", fib1(i), "\n")


##### 向量化 #####
g <- function(x) {
    if (abs(x) <= 1) {
        y <- x^2
    } else {
        y <- 1
    }
    return(y)
}
gv <- Vectorize(g)
gv(c(-2, -0.5, 0, 0.5, 1, 1.5))

# 三个语句都用到了无名函数
vapply(iris[, 1:4], function(x) max(x) - min(x), 0.0)
# 最后一个参数 FUN.VALUE 指定函数返回类型
d <- scale(Filter(is.numeric, iris))
integrate(function(x) sin(x)^2, 0, pi)