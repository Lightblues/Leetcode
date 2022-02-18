
library(tidyverse)

# 7.10 练习
d.class <- read.csv("./data/Rbook/class.csv", header = TRUE, stringsAsFactors = FALSE)
# d.class <- read_csv("./data/Rbook/class.csv")
View(d.class)
name <- d.class$name
age <- d.class$age

age[c(3, 5, 7)]
age[age >= 15]
# 用变量name和age, 求出Mary与James的年龄。
age[match(c("Mary", "James"), name)]
# 求age中除Mary与James这两人之外的那些人的年龄值，保存到变量age1中。
age1 <- age[-c(match(c("Mary", "James"), name))]

# x 是 1:length(x) 的一个重排, 则 x 可以看成一种映射, 求逆映射
# 即, 如果x[i]=j, 则y[j]=i。
x <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
x <- sample(x) # shuffle
match(seq_along(x), x)
x