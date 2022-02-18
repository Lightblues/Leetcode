A <- matrix(11:16, nrow = 3, ncol = 2)
print(A)
typeof(A)
class(A)
B <- matrix(c(1, -1, 1, 1), nrow = 2, ncol = 2, byrow = TRUE)
print(B)
nrow(A)
ncol(A)

dim(A)

############## 子矩阵 ################
A
A[1, ]
A[, 1]
A[c(1, 3), 1:2]

colnames(A) <- c("X", "Y")
rownames(A) <- c("a", "b", "c")
A

A[c("a", "c"), "Y"]

A[A[, 1] > 11, "Y", drop = FALSE]

# drop
A[, 1, drop = FALSE]

# 矩阵本质上是一个向量添加了`dim`属性， 实际保存还是保存成一个 **向量**
tmp <- A
tmp
dim(tmp) <- NULL
typeof(tmp)
class(tmp)
dim(tmp) <- c(3, 2)
tmp
class(tmp)

# 按照向量的方式来访问
A[1]
A[c(1, 3, 5)]

# 按照下标访问
ind <- matrix(c(1, 1, 2, 2, 3, 2), ncol = 2, byrow = TRUE)
ind
A[ind]

A[]
c(A)

################## cbind, rbind ##################
cbind(c(1, 2), c(3, 4), c(5, 6))
rbind(c(1, 2), c(3, 4), c(5, 6))

cbind(c(1, 2, 3))
rbind(c(1, 2, 3))

mA <- matrix(c(1, 2, 3, 4), nrow = 2, ncol = 2)
mB <- matrix(c(5, 6, 7, 8), nrow = 2, ncol = 2)
cbind(mA, mB)
mA

################### 矩阵运算 #####################
A
B
C2 <- A / 2
C2

C3 <- A %*% B
C3

c(1, 1) %*% B
B %*% c(1, 1)


# 内积
sum(c(1, 2), c(1, 2))
sum(c(1, 2) * c(1, 2))

# 外积
c(1, 2, 3) %o% c(1, -1)
# 等价
c(1, 2, 3) %*% t(c(1, -1))

##################### 逆矩阵与线性方程组求解 #####################
solve(B)
solve(B, c(1, 2))

####################### apply #######################
D <- matrix(c(6, 2, 3, 5, 4, 1), nrow = 3, ncol = 2)
D
apply(D, 2, sum)

# 若函数返回多个值, 则结果为一个向量
apply(D, 2, range)
# 注意返回的向量理解为列向量, 因此, 若 apply 按照行来计算, 应该转置
# apply(D, 1, range)
t(apply(D, 1, range))

#################### 多维数组 #####################
ara <- array(1:24, dim = c(2, 3, 4))
ara

# 子集
ara[, , 2]
ara[, 2, 2:3]