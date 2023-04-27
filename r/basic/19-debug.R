# 假设这是一开始错误的函数
# v1
f <- function(x) {
    # 使用 browser() 进入调试
    browser()
    for (i in 1:n) {
        s <- s + x[i]
    }
}
# v2 修复了变量不存在, 还有对于零长向量输入的 robust 问题
f <- function(x) {
    # 进入调试
    browser()
    s <- 0
    # 当x为零长向量时, 实际上循环了 i=1, 0, 最后返回 numeric(0)
    for (i in 1:length(x)) {
        s <- s + x[i]
    }
    s
}
# v3
f <- function(x) {
    # 关闭调试
    # browser()
    s <- 0
    # 当x为零长向量时, 实际上循环了 i=1, 0, 最后返回 numeric(0)
    for (i in seq_along(x)) {
        s <- s + x[i]
    }
    s
}
# print(f(1:5))
f(numeric(0))