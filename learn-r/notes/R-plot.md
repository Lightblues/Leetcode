
### 基本绘图样式

设置子图等

```r
# 规范流程
opar <- par(no.readonly = TRUE)    ## 保存绘图原格式
par(mfrow = c(1, 2), font.main = 2, font.axis = 2, font.lab = 2, lwd = 2)    ## 设置绘图格式

# ... 绘图

par(opar)    ## 格式复位

# macOS 下中文
par(family="PingFangSC-Regular")
```

#### legend

```r
# 两种方式: 可以在 barplot中设置, 更规范的应该是另外设置 legend
mp = barplot(coef_district$coef, col=coef_district$color, main = "回归系数 ~ 行政区 柱状图", xlab="行政区", ylab="回归系数", 
             # legend.text=c('***', '**', '*', '.', '_'), args.legend=list(x="bottomright", fill=coul[1:5])
             )
legend("bottomright", legend=c('***', '**', '*', '.', '_'), fill=coul)
```

#### 中文问题

参见 [mac中RStudio中文正常显示问题汇总](https://blog.csdn.net/CrispyCici/article/details/102482593)

```r
# 安装字体
library(showtext)  # 安装此包前需要在mac中按照XQuartz，https://www.xquartz.org
showtext_auto() 
font_add("PingFangSC-Regular",regular = "/System/Library/Fonts/PingFang.ttc") # 第一个参数是根据字体随便取个名字，regular参数是相应字体在电脑中的文件

# (1) 一般作图含中文
par(family="PingFangSC-Regular")
plot(...)

# (2) ggplot
ggplot(data, aes(x= ,y= )) + #用法示例
  geom_histogram() +
  geom_text(..., family="PingFangSC-Regular") +
  ggtitle("xxx") + 
  theme(text=element_text(family='PingFangSC-Regular')) 
```

### 对于变量排序

### 转为 factor

```r
# 按照中位数对于领域进行排序
# 先计算不同 type 分组之后, 各个组中的 topic_ordcnt 中位数; 然后排序, 转为 factor
median.order <- topic.districs %>% group_by(type) %>% summarise(ordcnt_median=median(topic_ordcnt))
median.order <- median.order[order(median.order$ordcnt_median, decreasing = TRUE),]
topic.districs$type <- factor(topic.districs$type, levels = median.order$type) # 转为 factor
ggplot(topic.districs) + 
  geom_boxplot(aes(type, log(topic_ordcnt+1)), fill="gray", varwidth=TRUE) +
  labs(x="领域", y = "对数约见人数") +
  theme_bw()
```

#### reorder 函数

参见 [Ordering boxplots in base R](https://r-graph-gallery.com/9-ordered-boxplot.html)

```r
new_order <- with(data, reorder(district0, log_recent_order_num, median))
boxplot(log_recent_order_num ~ new_order, data=data, main = "对数月销量 ~ 行政区划 箱线图", xlab = "行政区划", ylab = "月销量", col = "#FF9933")
```

## R 基本绘图类型

### 分布图 hist

```r
opar <- par(no.readonly = TRUE)    ## 保存绘图原格式
par(mfrow = c(1, 2), font.main = 2, font.axis = 2, font.lab = 2, lwd = 2)    ## 设置绘图格式

hist(dat3$rvi, freq = T, main = "汽车保值率直方图", col = "#7F7FFF", xlab = "保值率", ylab = "频数", xlim = c(0, 1), ylim = c(0, 1500), breaks = seq(0, 1, 0.05))    ## 保值率 直方图

hist(dat3$log_rvi, freq = T, main = "汽车对数保值比率直方图", col = "#7F7FFF", xlab = "对数保值比率", ylab = "频数", xlim = c(-3, 3), ylim = c(0, 2000), breaks = seq(-5, 5, 0.25))    ## 对数保值比率 直方图

par(opar)    ## 格式复位
```

### 柱状图 barplot

```r
mp = barplot(coef_district$coef, col=coef_district$color, main = "回归系数 ~ 行政区 柱状图", xlab="行政区", ylab="回归系数", 
             # legend.text=c('***', '**', '*', '.', '_'), args.legend=list(x="bottomright", fill=coul[1:5])
             )
# 设置 legend
legend("bottomright", legend=c('***', '**', '*', '.', '_'), fill=coul)
# 设置横坐标
lablist <- rownames(coef_district)
text(mp, par("usr")[3], labels = lablist, srt = 45, adj = c(1.1,1.1), xpd = TRUE, cex=0.6)
```

### 箱线图

```r
par(font.main = 2, font.axis = 2, font.lab = 2, lwd = 2, pch = 1)    ## 设置绘图格式

boxplot(dat3$log_rvi ~ dat3$nationalState, main = "对数保值比率关于排放标准的箱线图", xlab = "排放标准", ylab = "对数保值比率", col = "#FF9933")    ## 对数保值比率 - 排放标准 箱线图

par(opar)    ## 格式复位
```

### 散点图

```r
plot(datFinal$licheng, datFinal$ratio, main = "汽车对数保值比率对里程的散点图", xlab = "里程", ylab = "对数保值比率", font.main = 2, font.lab = 2, font.axis = 2, lwd = 2, pch = 16, cex = 0.6)    ## 保值比率对里程的散点图
```

### Spline 图

分组的比例图

```r
rtb$isp = factor(rtb$isp,                         # 更名
                   levels = c(0,1,2,3), 
                   labels = c("未知","中国移动","中国联通","中国电信"))
table(rtb$isp)
# 输入的应该是二维表. 如下面横轴是 isp也即手机运营商, 纵轴是dc, 有两个标签也即 点击/未点击
table(rtb$isp, rtb$dc) %>% 
  spineplot(main="手机运营商",
            col=c("gray","gold"),
            yaxlabels = c("未点击","点击"))
```

## ggplot

- <https://ggplot2.tidyverse.org/index.html>

### 分组绘图: facet_wrap

```r
ggplot(diamonds, aes(x=price)) +
  geom_histogram(bins=50) + 
  facet_wrap(~cut) + 
  theme_minimal() +
  ggtitle("Diamond Prices Distribution ~ Cut") 
```

### 设置 theme

可以自行设置 theme 的配置, 然后之后绘图的时候引用

```r
## 设置绘图主题
# ggplot() + theme_bw()
# ggplot() + plot_theme_pie
# ggplot() + plot_theme

# plot_theme <- theme(xxxxxxxxxxx)

# 饼图绘制主题
theme(panel.background = element_rect(fill = rgb(255, 255, 255, maxColorValue = 255)),
      plot.background = element_rect(rgb(255, 255, 255, maxColorValue = 255)),
      axis.text = element_text(color = rgb(236, 241, 249, maxColorValue = 255)),
      panel.grid.major = element_line(color = rgb(236, 241, 249, maxColorValue = 255)),
      panel.grid.minor = element_line(color = rgb(236, 241, 249, maxColorValue = 255)),
      plot.title = element_text(family = "Hei", face = "bold", size = 14),
      legend.title = element_text(family = "Hei", face = "bold",size = 12),
      legend.text = element_text(family = "Hei",size = 11)) -> plot_theme_pie # 饼图绘制主题
## 设置绘图主题
theme(panel.background = element_rect(fill = rgb(255, 255, 255, maxColorValue = 255)),
      plot.background = element_rect(rgb(255, 255, 255, maxColorValue = 255)),
      axis.text = element_text(size = 12,family = "Hei"),
      axis.text.x = element_text(size = 12, family = "Hei", face = "bold") ,
      axis.text.y = element_text(size = 12, family = "Hei", face = "bold") ,
      axis.ticks = element_line(color = rgb(236, 241, 249, maxColorValue = 255)),
      axis.title = element_text(size = 13, family = "Hei"),
      panel.grid.major = element_line(size = 1),
      panel.grid.minor = element_line(color = rgb(236, 241, 249, maxColorValue = 255)),
      plot.title = element_text(family = "Hei", face = "bold", size = 14),
      legend.title = element_text(family = "Hei", face = "bold",size = 12),
      legend.text = element_text(family = "Hei",size = 11)) -> plot_theme   # 其他图形绘制主题
```

使用 theme

```r
ggplot(descriptive) +
  geom_bar(aes(x = factor("1"), fill = factor(offertype)), position = "fill", width = 1) +
  # position参数，有stack、fill、dodge
  scale_fill_manual("申请结果", values = c("grey", "gold", "skyblue")) +
  coord_polar(theta = "y") +
  labs(x = "", y = "", title = "\n录取类型") +
  plot_theme_pie
```

### geom_bar

- <https://ggplot2.tidyverse.org/reference/geom_bar.html>

#### 高度根据计算好的值绘制: 设置stat

```r
# 柱子的高度设置为 count列
ggplot(user.industry.cnt) +
    geom_bar(aes(x=user_industry_name, y=count), fill = "gray", stat = 'identity') +
    labs(y = "频数", x = "用户所在行业") +
    coord_flip() +
```

### geom_point

例子: 画出 kmeans 聚类结果

```r
# 这里用的是 sparkR 训练模型
kmean.model4 = km_data$training %>%
  ml_kmeans(features=c("V1", "V2"), k=4, seed = 116)
pred4 = ml_predict(kmean.model4, km_data$training) %>%
  collect()

# plot cluster membership
pred4 %>%
  ggplot(aes(V1, V2)) +
  geom_point(aes(V1, V2, col = factor(prediction + 1)),
             size = 2, alpha = 0.5) + 
  # 聚类中心
  geom_point(data = kmean.model4$centers, aes(V1, V2),
             col = scales::muted(c("red", "green", "blue", "yellow")), 
             pch = 'x', size = 12) +
  # 类标签
  scale_color_discrete(name = "Predicted Cluster",
                       labels = paste("Cluster", 1:4)) +
  labs(
    x = "V1",
    y = "V2",
    title = "K-Means Clustering with K=4",
  )
```

### geom_boxplot

```r
ggplot(diamonds, aes(factor(color), price, fill=color)) + 
  geom_boxplot() +
  ggtitle("Boxplot Price ~ Color") 

# 绘制价格的对数对产品等级的分组箱线图，并按每一等级的平均价格由低到高进行排列
travel_dat$Star2 <- as.factor(star1)                            # 变成因子变量并保存至travel_dat中
travel_dat$Star2 <- factor(travel_dat$Star2,                    # 按照均价重新排序水平
                      levels = levels(travel_dat$Star2)[c(1,5,2,3,4)], 
                      labels = c("2钻","无信息","3钻","4钻","5钻"))
ggplot(travel_dat, aes_string(x="Star2", y="Price")) +          # 箱线图
  geom_boxplot(varwidth=T, color = adjustcolor("#8CE52E"), fill = adjustcolor("#8CE52E", alpha.f = 0.4)) +
  scale_y_log10(breaks=c(2e3,1e4,8e4),                          # 对价格取对数
    labels=c("2千", "1万", "8万")) +
  ylab("产品价格（对数变换）") +
  xlab("") + 
  theme(panel.background = element_rect(fill = "transparent"),  # 背景透明
        panel.grid.major = element_blank(),                     # 去掉背景网格
        panel.grid.minor = element_blank(),
        axis.ticks = element_blank())                           # 去掉坐标轴
```

#### 同一数据多变量分组的boxplot

- 参见 [here](https://guangchuangyu.github.io/cn/2017/10/boxplot-multiple-group/)

例如, 想要对于 BMI, stage, age, gender 分别绘制箱线图, 放进一张图中.

```r
d <- data.frame(riskScore = abs(rnorm(100)), BMI = sample(1:2, 100, replace=T), stage = sample(1:2, 100, replace=T), age = sample(1:2, 100, replace=T), gender = sample(1:2, 100, replace=T))
head(d)

##     riskScore BMI stage age gender
## 1 0.008282743   1     2   1      1
## 2 0.499375414   1     1   2      1
```

为此, 需要对于数据进行转换, 将这些列都作为一个新的 type变量 (短表转为长表).

```r
convert <- function(d) {
    lapply(2:ncol(d), function(i) {
        d2 <- d[, c(1,i)]
        d2$type = colnames(d2)[2]
        colnames(d2) = c("riskScore", "category", "type")
        return(d2)
    }) %>% do.call('rbind', .)
}
dd <- convert(d)
head(dd)
##     riskScore category type
## 1 0.008282743        1  BMI
## 2 0.499375414        1  BMI
```

然后画图

```r
ggplot(dd, aes(type, riskScore, fill=factor(category))) + geom_boxplot()

# 分面
ggplot(dd, aes(type, riskScore, group=factor(category), fill=type)) +
    geom_boxplot() + facet_grid(.~type, scales = "free_x")
```

另外介绍了不采用 ggplot 的手动写函数的方式

```r
myboxplot <- function(x, data, col = NULL, xlab, pvalue="auto") {
    boxplot(x, data, axes = FALSE, col = col)
    axis(1, at = 1:2, labels =FALSE)
    text(1:2, y=par()$usr[3]-0.08*(par()$usr[4]-par()$usr[3]),
         srt=60, xpd=T, adj=1, labels = xlab)
    if (pvalue == "auto") {
        pvalue <- round(t.test(x, data=data)$p.value, 3)
    }

    if (!is.null(pvalue)) {
        plab <- paste("p =", pvalue)
        text(1.5, y = par()$usr[4]*1.05, xpd=T, label=plab, col=col)
    }
}

layout(t(1:4))
par(oma=c(2, 4, 4, 0), mar=c(5,2,1,1), cex=1)

myboxplot(riskScore~age, data=d, col='red', xlab=c("age < 60", "age > 60"))
axis(2, las=1)
myboxplot(riskScore~gender, data=d, col='green', xlab=c("Male", "Female"))
myboxplot(riskScore~stage, data=d, col='blue', xlab=c("pStage 1-2", "pStage 1-2"))
myboxplot(riskScore~BMI, data=d, col='cyan', xlab=c("BMI < 24", "BMI > 24"))
```

### geom_histogram

```r
ggplot(travel_dat, aes(x = Price)) + 
  geom_histogram(fill = adjustcolor("#FDE255")) +           # 直方图
  scale_x_log10(                                            # log变换
    breaks=c(1e3,1e4,1e5),                   
    labels=c("1千", "1万", "10万")) +                       # 改变坐标轴数值名称
  xlab("产品价格（对数变换）") + ylab("频数") +             # x轴y轴的label
  theme_classic()
```

## ggpubr

- <https://rpkgs.datanovia.com/ggpubr/>
- [ggplot2一页多图排版的简便方法](https://www.jianshu.com/p/c154ca35530b)
    - 除了下面的, 还介绍了 注释、对其绘图区、更改图形的行列跨度、通用图例、具有边际密度图的散点图、混排表格，文字和图形、在ggplot图中插入图形元素、多页图形的排版、使用ggarrange()的嵌套布局
- [ggpubr：快速绘制用于发表的图形](https://blog.chipcui.top/archives/ggpubr-publication-ready-plots)

下面加载数据, 绘制了 箱线图、点图、条形图 (分组) 和散点图 (加回归线)

```r
# ToothGrowth
data("ToothGrowth")
head(ToothGrowth)

# mtcars 
data("mtcars")
mtcars$name <- rownames(mtcars)
mtcars$cyl <- as.factor(mtcars$cyl)
head(mtcars[, c("name", "wt", "mpg", "cyl")])
```

```r
# Box plot (bp)
bxp <- ggboxplot(ToothGrowth, x = "dose", y = "len",
                 color = "dose", palette = "jco")
bxp
# Dot plot (dp)
dp <- ggdotplot(ToothGrowth, x = "dose", y = "len",
                 color = "dose", palette = "jco", binwidth = 1)
dp

# Bar plot (bp)
bp <- ggbarplot(mtcars, x = "name", y = "mpg",
          fill = "cyl",               # 根据cyl类型填充颜色
          color = "white",            # 将条形边框颜色设为白色
          palette = "jco",            # jco 调色板
          sort.val = "asc",           # 按升序排序
          sort.by.groups = TRUE,      # 分组排序
          x.text.angle = 90           # 垂直旋转x轴文本
          )
bp + font("x.text", size = 8)
# Scatter plots (sp)
sp <- ggscatter(mtcars, x = "wt", y = "mpg",
                add = "reg.line",               # 添加回归线
                conf.int = TRUE,                # 添加置信区间
                color = "cyl", palette = "jco", # 根据cyl填充颜色
                shape = "cyl"                   # 根据cyl类型设置点形状
                )+
  stat_cor(aes(color = cyl), label.x = 3)       # 添加相关系数
sp
```

### 利用 ggarrange 进行排版

```r
ggarrange(bxp, dp, bp + rremove("x.text"), 
          labels = c("A", "B", "C"),
          ncol = 2, nrow = 2)
```

也可以使用 cowplot::plot_grid, gridExtra::grid.arrange 来完成

```r
library("cowplot")
plot_grid(bxp, dp, bp + rremove("x.text"), 
          labels = c("A", "B", "C"),
          ncol = 2, nrow = 2)

library("gridExtra")
grid.arrange(bxp, dp, bp + rremove("x.text"), 
             ncol = 2, nrow = 2)
```
