typeof(1:3) # integer
typeof(c(1, 2, 3)) # double
typeof(c(TRUE, NA, FALSE)) # logical
typeof("Abc") # character
typeof(factor(c("a", "b", "c"))) # integer

c(-1, 0, 1) / 0
## [1] -Inf  NaN  Inf
is.na(c(-1, 0, 1) / 0)
## [1] FALSE  TRUE FALSE

# 类型转换
as.numeric(c(FALSE, TRUE))
## [1] 0 1
as.character(sqrt(1:4))
## [1] "1"                "1.4142135623731"  "1.73205080756888" "2"

# 类型升档
c(FALSE, 1L, 2.5, "3.6")
## [1] "FALSE" "1"     "2.5"   "3.6"


is.infinite(3L)


typeof(list("a", 1L, 1.5))
## [1] "list"
tmp <- c(1, c(2, 3, c(4, 5)))
typeof(tmp)

# NULL
typeof(NULL)
c() # NULL

####################### 属性 #######################
x <- table(c(1, 2, 1, 3, 2, 1))
print(x)
typeof(x) # integer
x
# attributes
attributes(x) # dim, dimnames, class 三个属性
class(x)
dimnames((x))

# attr
x <- c(1, 3, 5)
attr(x, "theta") <- c(0, 1)
print(x)

# names
x <- 1:5
y <- x^2
lmr <- lm(y ~ x)
print(names(lmr)) # "coefficients"  "residuals"
attributes(lmr)
lmr$coefficients

# dim
x <- 1:4
dim(x) <- c(2, 2)
x
attributes(x)

##################### 8.4 类属 ######################
typeof(factor(c("F", "M", "M", "F")))
## [1] "integer"
mode(factor(c("F", "M", "M", "F")))
## [1] "numeric"
storage.mode(factor(c("F", "M", "M", "F")))
## [1] "integer"
class(factor(c("F", "M", "M", "F")))
## [1] "factor"
class(as.numeric(factor(c("F", "M", "M", "F"))))
## [1] "numeric"

#################### str #####################
s <- 101:200
attr(s, "author") <- "李小明"
attr(s, "date") <- "2016-09-12"
s
str(s)