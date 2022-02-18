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

untracemem(x)
untracemem(y)
rm(x, y)