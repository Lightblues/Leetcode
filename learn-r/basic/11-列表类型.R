
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

# 赋值为 NULL 就是删除; 但是在 list 函数中是可以定义 NULL 变量的
li <- list(a = 120, b = "F", c = NULL)
li
li$c <- NULL
li

##################### 列表类型转换 #####################
li1 <- as.list(1:3)
li1
# 这样生成的列表有三项, 都是没有名字的. 仅能通过下面的 [[1]] 来访问
li1[["1"]] # NULL
li1[[1]] # 1
unlist(li1)
li2 <- list(x = 1, y = c(2, 3))
li2
unlist(li2)

######################### strsplit  #####################
x <- c("10, 8, 7", "5, 2, 2", "3, 7, 8", "8, 8, 7")
res <- strsplit(x, ",")
res

sapply(res, as.numeric) # 转为矩阵
t(sapply(res, as.numeric)) # 可以转置了