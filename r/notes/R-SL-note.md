
## 杂项

```r
# 清除工作环境
cat("\014");rm(list=ls()) 

# 设置工作路径
setwd('/Users/zhaoyaying/Desktop/R/data_mining/hw3')

Sys.setlocale(category="LC_ALL",locale="Chinese")     # 设置语言

set.seed(1) # 设置随机数种子
```

## 快捷键

Rstudio 快捷键, [here](https://support.rstudio.com/hc/en-us/articles/200711853-Keyboard-Shortcuts-in-the-RStudio-IDE)

- 注释: command+shift+c, 修改为 cmd+Enter
- 赋值符号: (Insert Assignment Operator): Opt+-, 修改为 cmd+-
- 管道符号: (Insert Pipe Operator): Cmd+Shift+M, 修改为 Cmd+=
- 插入代码块: Cmd+Opt+I
- 执行代码块: Cmd+Shift+Enter

调整光标位置: 参见 `View` 中定义的各个快捷键

## 数据结构

### data.frame 数据框

根据要求构造df 作为模型的输入

```r
# 构造一条新的数据, 进行 lm 的预测
cnames = c("log_average_cost", "delivery_mode", "log_float_delivery_fee", "order_lead_time", "district", "保", "票", "manjian_discount", "other_activities", "open_time", "open18", "open23", "shop_type", "is_new", "is_premium")
new_shop = list(log(20), "蜂鸟专送", log(6), 45, "海淀区", T,F, 0.35, 5, 11, "1", "1", "快餐简餐", FALSE, FALSE)
test_data = as.data.frame(new_shop, col.names=cnames)
# test_data

predict.lm(model_bic, test_data)
```

### factor 因子

```r
# 可以对分类变量进行顺序调整
dat3$paifang <- factor(dat3$paifang, levels = c("国五", "国四", "国三", "国二", "国一"))    ## 调整排放标准顺序
summary(dat3$paifang)    ## 查看排放标准情况
```

### 哑变量

转换一组变量为单一因子变量

```r
for(i in 1:nrow(datFinal))    ## 处理哑变量
{
    if(datFinal[i, "SUV"] == 1)
    {
        datFinal[i, "车型"] <- "SUV"
    }
    else if(datFinal[i, "紧凑型车"] == 1)
    {
        datFinal[i, "车型"] <- "紧凑型车"
    }
    else if(datFinal[i, "中型车"] == 1)
    {
        datFinal[i, "车型"] <- "中型车"
    }
    else
    {
        datFinal[i, "车型"] <- "其他车型"
    }
}

datFinal$"车型" <- factor(datFinal$"车型", levels = c("其他车型", "SUV", "中型车", "紧凑型车"))    ## 调整车型顺序
```

## 基本统计

一些指标

```r
# 分位数
quantile(diamonds$price, c(.3, .5, .8))
```

## 基本数据操作

```r
# 删除特定的数据
dat0 <- read.csv("cars.csv", header = T, fileEncoding = "GB2312")    ## 读入数据
dim(dat0)    ## 12951行 19列
dat1 <- dat0[which(dat0$pailiang != -1 & dat0$paifang != -1), ]    ## 删除没有采集到排放和排量的数据
dim(dat1)    ## 12820行 19列
dat2 <- dat1[which(duplicated.data.frame(dat1) == F), ]    ## 删除重复冗余的数据
dat3 <- dat2[which(dat2$yuanjia != 0), ]    ## 删除原价为0的数据

# 选择特定列, 重命名列
dat <- read.xlsx("travel.xlsx", 1)                                                         # 原始数据
travel_dat <- dat[,c(1:8,12:13,15,17:23,25)]                                               # 筛选出需要用到的变量
colnames(travel_dat) <- c("Product", "TravelMethod", "Agency", "Star",
                          "Place", "Traffic", "Meal","FreeActivitie",
                          "Evaluate","Sale","Depart","SunPrice","MonPrice",
                          "Tuesprice","WedPrice","ThusPrice",
                          "Friprice","Satprice","Routine")  
travel_dat <- travel_dat[!startsWith(as.character(travel_dat$Product),"健康医疗"),]        # 去除数据中有健康医疗字样的样本
travel_dat <- travel_dat[which(travel_dat$Depart != "上海"&travel_dat$Depart != "北京"),]  # 去除从国内出发的


# 转换、统计
dat3$rvi <- dat3$baojia / dat3$yuanjia    ## 保值率 = 报价 / 原价 
dat3$log_rvi <- log(dat3$baojia / (dat3$yuanjia - dat3$baojia))    ## 对数保值比率 = log(报价 / (原价 - 报价))
```

### 排序: 利用 order

```r
head(dat3[order(dat3$log_rvi), ], n = 10)    ## 查看保值率最低的10个数据

attach(mtcars)
newdata <- mtcars[order(mpg, -cyl),]

# 按照 V1 降序排列
df1 <- df1[order(df1$V1, decreasing = TRUE),]
```

### 分位数 quantile

```r
# 找到其四分之三分位点，赋值给bar
bar = as.numeric(summary(zhihu$提问数)["3rd Qu."])
# 在zhihu中新建一列tiwen，初始值均设为“高问”
zhihu$tiwen = "高问"
# 将提问数小于四分之三分位点的设为“低问”
zhihu[which(zhihu$提问数 < bar), "tiwen"] = "低问"
```

### apply+函数 进行筛选

```r
# 利用周一到周日是否有报价计算每周出团日期，若当天有报价则视为出团，无报价则为未出团。提取出“仅工作日”，“仅周末”，“工作日和周末”三类出团情况并以“Date”变量存入数据集travel_dat（不属于上述任何一种情况的以缺失值存储），计算每一类出团日期的平均价格并展示

## 得到周一到周日的产品价格
price1 <- allPrice[!is.na(avgprice),] %>% apply(2, PriceToNum)   

## 仅工作日有团，周末无团
onlyweekday <- which(apply(price1, 1, function(y) (!all(is.na(y[2:6]))) & all(is.na(y[c(1,7)]))) ) 

## 仅周末有团，工作日无团
onlyweekend <- which(apply(price1, 1, function(y) all(is.na(y[2:6])) & !all(is.na(y[c(1,7)]))))

## 周末和周末都有团
allweek <- which(apply(price1, 1, function(y) !all(is.na(y[2:6])) & !all(is.na(y[c(1,7)]))))

## 得到产品的出团日期
travel_dat$Date <- rep(NA,dim(travel_dat)[1])
travel_dat$Date[onlyweekday] <- "仅工作日"
travel_dat$Date[onlyweekend] <- "仅周末"
travel_dat$Date[allweek] <- "工作日和周末"

## 不同出团日期的产品均价
travel_dat %>% group_by(Date) %>% summarise(mean = mean(Price))
```

### 划分连续为离散 cut

```r
# 根据p值划分为离散的显著性水平
cut(coef_district$p, breaks=c(0, .001, .01, .05, .1, 1), labels=c('***', '**', '*', '.', '_'))
```

### 分组统计: group_by + summarise

```r
# 从“Place”变量中提取出全部景点数和经典景点数，并分别以“AllPlace”和“ClassicPlace”变量存入数据集travel_dat，变量类型为数值型。
place <- travel_dat$Place %>% as.character()                                                  # 变成字符变量
travel_dat$AllPlace <- place %>% str_extract("[[:digit:]]+?(?=个景点)") %>% as.numeric()      # 得到所有景点个数
travel_dat$ClassicPlace <- place %>% str_extract("[[:digit:]]+?(?=个经典)") %>% as.numeric()  # 得到经典景点个数

# 将全部景点数按由少到多分成4组，分别为“9个及以下”，“10-16个”，“17-25个”，“25个以上”，以变量“AllPlacesGroup”变量保存在数据集travel_dat中，计算每一组内产品的平均价格并使用dplyr包的summarise()函数进行展示。
travel_dat$AllPlacesGroup <- cut(travel_dat$AllPlace, breaks = c(0, 9, 16, 25, 77))           # 按景点个数数量分组

travel_dat %>% group_by(AllPlacesGroup) %>% summarise(mean(Price, na.rm=T))                   # 每组价格均值
```

### jieba 分词, 词云

```r
library(jiebaRD)
library(jiebaR)         # 加载包

cutter <-  jiebaR::worker()  # 设置分词引擎
words.seg <-  jiebaR::segment(a$course.name, cutter) # 对文本进行分词处理
words.seg <- gsub("[0-9a-zA-Z]+?","",words.seg)  # 去除数字和英文
stopwords <- c('区','路','火锅','小区','分店','店')
words.seg <- filter_segment(words.seg, stopwords)  # 去除中文停止词
words.table = plyr::count(words.seg)
words.table <- words.table[sort(words.table$freq, decreasing = T),]

# 词云
library(wordcloud2)
wordcloud2(words.table)
```

### NER

任务需求是判断是否包含人名

```r
# 提示：箱线图显示，店名中包含人物词汇的火锅团购店的团购销量要显著高于店名中不包含人物词汇的。
library(Rwordseg) # 加载包

hot.pot$if.have.name = 0      # 定义变量
for (i in 1:dim(hot.pot)[1]){   # 若isNameRecognition设定变化前后分词情况有变化，则说明火锅店名字中含有人名
  segment.options(isNameRecognition=FALSE)
  words.seg1 = segmentCN(hot.pot[i,]$字段1)
  segment.options(isNameRecognition=TRUE)
  words.seg2 = segmentCN(hot.pot[i,]$字段1)
  if (length(words.seg1) != length(words.seg2))
    hot.pot[i,]$if.have.name = 1
}

boxplot(log.sales~if.have.name,data=hot.pot,varwidth=T,col=7,xlab='',ylab='对数（季均销量+1）',main='是否使用人名词汇对销量的影响',names=c('否','是')) # 箱线图
```

## 字符串处理

- [41 R语言的文本处理](https://www.math.pku.edu.cn/teachers/lidf/docs/Rbook/html/_Rbook/text.html)

gsub 提取数字

```r
# 提取周一到周日报价中的数值部分，计算一周报价的均值（若一周7天均无报价则缺失），并以新变量“Price”存入数据集travel_dat中，剔除平均价格缺失的样本
allPrice <- travel_dat[,12:18]                              # 取出周一到周日的数据
allPrice[allPrice==""] <- NA                                # 处理缺失值

PriceToNum <- function(price)                               # 自定义函数，提取价格的数值部分
{
  price <- gsub("\\D", "", as.character(price)) %>% 
    as.numeric()                                            # 去字符串中的价格部分
  return(price)
}

price <- allPrice %>% apply(2, PriceToNum)                  # 得到价格的数值部分

avgprice <- apply(price, 1, function(x) mean(x, na.rm = T)) # 平均价格
travel_dat$Price <- avgprice                                # 建立新变量价格
travel_dat <- travel_dat[!is.na(travel_dat$Price),]         # 去除缺失价格的观测
```

strsplit

```r
# 提取“Star”变量中的“*钻”字符来表示产品等级，当一个产品包含多个钻级时取最大钻级，并将产品钻级以新变量“Star2”存入数据集travel_dat中，变量类型为因子型
star <- strsplit( as.character(travel_dat$Star), "\\,")         # 按“,”分开等级

StarNum <- function(x)                                          # 自定义函数，提取产品等级
{
  if("暂无酒店信息" %in% x){
    return("无")
  }else{
    x <- x %>% strsplit("晚|钻")                                # 得到几晚几钻的信息
    x <- x %>% map(2) %>% unlist() %>% as.numeric() %>% 
      ceiling() %>% max(na.rm=T)                                # 用最大的钻级表示该产品的等级
    
    return(x)
  }
}

star1<- star  %>% lapply(StarNum) %>% unlist()                  # 得到产品等级
```

### stringr 包

- <https://stringr.tidyverse.org/>

```r
x <- c("why", "video", "cross", "extra", "deal", "authority")
str_length(x) 
#> [1] 3 5 5 5 4 9
str_c(x, collapse = ", ")
#> [1] "why, video, cross, extra, deal, authority"
str_sub(x, 1, 2)
#> [1] "wh" "vi" "cr" "ex" "de" "au"


# 正则表达式
# detect 检查是否存在匹配
str_detect(x, "[aeiou]")
#> [1] FALSE  TRUE  TRUE  TRUE  TRUE  TRUE

# count 计算匹配次数
str_count(x, "[aeiou]")
#> [1] 0 3 1 2 2 4

# subset 进行筛选
str_subset(x, "[aeiou]")
#> [1] "video"     "cross"     "extra"     "deal"      "authority"

# locate 给出匹配的位置 (第一次)
str_locate(x, "[aeiou]")
#>      start end
#> [1,]    NA  NA
#> [2,]     2   2
#> [3,]     3   3

# extract 抽取匹配内容
str_extract(x, "[aeiou]")
#> [1] NA  "i" "o" "e" "e" "a"

# match 抽取分组的匹配内容
# extract the characters on either side of the vowel
str_match(x, "(.)[aeiou](.)")
#>      [,1]  [,2] [,3]
#> [1,] NA    NA   NA  
#> [2,] "vid" "v"  "d" 

# replace 替换
str_replace(x, "[aeiou]", "?")
#> [1] "why"       "v?deo"     "cr?ss"     "?xtra"     "d?al"      "?uthority"

# split 进行切分
str_split(c("a,b", "c,d,e"), ",")
#> [[1]]
#> [1] "a" "b"
#> 
#> [[2]]
#> [1] "c" "d" "e"
```

#### str_extract 抽取

例子: 抽取数字 (正则)

```r
# 从“Place”变量中提取出全部景点数和经典景点数，并分别以“AllPlace”和“ClassicPlace”变量存入数据集travel_dat，变量类型为数值型。
place <- travel_dat$Place %>% as.character()                                                  # 变成字符变量
travel_dat$AllPlace <- place %>% str_extract("[[:digit:]]+?(?=个景点)") %>% as.numeric()      # 得到所有景点个数
travel_dat$ClassicPlace <- place %>% str_extract("[[:digit:]]+?(?=个经典)") %>% as.numeric()  # 得到经典景点个数

# 将全部景点数按由少到多分成4组，分别为“9个及以下”，“10-16个”，“17-25个”，“25个以上”，以变量“AllPlacesGroup”变量保存在数据集travel_dat中，计算每一组内产品的平均价格并使用dplyr包的summarise()函数进行展示。
travel_dat$AllPlacesGroup <- cut(travel_dat$AllPlace, breaks = c(0, 9, 16, 25, 77))           # 按景点个数数量分组

travel_dat %>% group_by(AllPlacesGroup) %>% summarise(mean(Price, na.rm=T))                   # 每组价格均值
```

### JiebaR 分词

下面展示了 jiebaR 载入自定义词典, 分词, 绘制词数分布图

```r
library(jiebaR)
# 初始化分词工具
seg <- worker(bylines = T)
# 读入自定义词典
new_words <- read.table('userdict.dat', header = F, stringsAsFactors = F)
# 将词典加入分词引擎
new_user_word(seg, new_words$V1)

# 分词, 注意分词结果是 list
catalog$name <- as.character(catalog$name)
cata_seg <- segment(catalog$name, seg)
# 提取出“生鲜”
food_and_drink_seg <- cata_seg[which(catalog$first == "生鲜")]
# 计算不同商品名称包含的词数
word_lengths <- sapply(food_and_drink_seg, length)
hist(word_lengths)
```

### 正则表达式 grepl

- \\\\:转义符
- ^:匹配输入字符串的开始位置
- $:匹配输入字符串的结束位置
- *:匹配前面的子表达式零次或多次
- +:匹配前面的子表示式一次或多次
- ?:匹配前面的子表达式零次或一次
- .:匹配除 `\n` 以外的任何单个字符
- x|y:匹配x或y
- \[xyz]:字符集和，匹配集合中所包含的任意字符
- \[^xyz]:负字符集合，匹配非集合中的任意字符
- \[a-z]:字符范围，匹配任意小写字母
- \[^a-z]:负值字符范围
- \[A-Z]:字符范围，匹配任意大写字母
- \[0-9]:字符范围，匹配任意数字
- `[\u4e00-\u9fa5]`:中文字符范围
- \\\\s:匹配任意空白字符，包括空格、制表符、换页符等等

```r
# 匹配包含某些关键词的字符串
s0 <- "have a nice day, 666"
grepl(".+nice.+", s0)
grepl(".+666.+", s0) # F

# 匹配全是英文字母组成的字符串
s1 <- "asfGYJKhkgdnabuqwKHg"
grepl("^([a-z]|[A-Z])+$", s1)

# 匹配全是数字组成的字符串
s2 <- "34241341"
grepl("^[0-9]+$", s2)

# 匹配中文
s3 <- "数据abc666挖掘"
grepl('^[\u4e00-\u9fa5]+[a-z|A-Z]+[0-9]+[\u4e00-\u9fa5]+$', s3)
```

## IO

```r
library(readxl)
catalogs <- readxl::read_excel("catalogs.xlsx")
head(catalogs)
```

## 模型

```r
glm.fit = glm(log.sales.code ~ .-quarterly.sales.volume-ID-字段1-字段2-price-price.code-评论数-log.sales,family='binomial',data=hot.pot)  # 逻辑回归
summary(glm.fit)
logit.aic <- step(glm.fit, k = 2, trace = 0, direction = "both")
summary(logit.aic)
```

### 分组 createFolds

```r
set.seed(1) # 设置随机数种子
library(caret) # 加载包，调用createFolds
folds = createFolds(y=as.matrix(hot.pot)[,23],k=10) # 随机分组，10折

p.rate <- as.numeric() # 记录正确率
for(i in 1:10){
  fold.test <- hot.pot[folds[[i]],] # 取folds[[i]]作为测试集
  fold.train <- hot.pot[-folds[[i]],] # 剩下的数据作为训练集
  glm.fit = glm(sales.code~.,family='binomial',data=fold.train) # 逻辑回归
  
  glm.probs = predict(glm.fit,fold.test,type='response') # 计算概率
  glm.pred = rep(F,dim(fold.test)[1])
  glm.pred[glm.probs>.5]=T # 模型预测结果
  
  prate = mean(glm.pred==fold.test$sales.code) # 正确率
  p.rate = append(p.rate,prate)
}
p.logistic = mean(p.rate) # 计算平均正确率
p.logistic
```

### 回归模型

#### 绘制回归系数的柱状图

对于一个回归模型, 绘制回归系数柱状图; (1) 按照系数大小排序; (2) 根据是否显著(p值)显示不同颜色

```r
# 1. 拿到回归系数, 构建 df
coef = summary(model_bic)$coefficients
coef_district = data.frame(coef[6:20,][,c(1,4)]) # 选择关注的回归系数
colnames(coef_district) = c('coef', 'p')
# 2. 按照系数大小排序
coef_district = coef_district[order(coef_district$coef),]
# 3. 判断显著性, 离散化
coef_district$sig = cut(coef_district$p, breaks=c(0, .001, .01, .05, .1, 1), labels=c('***', '**', '*', '.', '_'))
# 4. 设置颜色
par(family="PingFangSC-Regular")
library(RColorBrewer)
coul <- brewer.pal(5, "Set1")
coef_district$color = coul[coef_district$sig]
# 5. 绘制柱状图
mp = barplot(coef_district$coef, col=coef_district$color, main = "回归系数 ~ 行政区 柱状图", xlab="行政区", ylab="回归系数", 
             # legend.text=c('***', '**', '*', '.', '_'), args.legend=list(x="bottomright", fill=coul[1:5])
             )
legend("bottomright", legend=c('***', '**', '*', '.', '_'), fill=coul)
# 设置横坐标
lablist <- rownames(coef_district)
text(mp, par("usr")[3], labels = lablist, srt = 45, adj = c(1.1,1.1), xpd = TRUE, cex=0.6)
```

#### 指标

MSE, MAE

```r
MSE = mean(((preds$prediction)-log(preds$price))^2)
MAE = mean(abs((preds$prediction)-log(preds$price)))
cat('MSE:', MSE, "; MAE: ", MAE)
```

#### 模型选择

可以采用 `step`, 或者 `MASS::stepAIC`

```r
# Full model
mod <- lm(Price ~ ., data = wine)

# With AIC
modAIC <- MASS::stepAIC(mod, k = 2)
summary(modAIC)
# With BIC
modBIC <- MASS::stepAIC(mod, k = log(nrow(wine)))

# Add an irrelevant predictor to the wine dataset
set.seed(123456)
wineNoise <- wine
n <- nrow(wineNoise)
wineNoise$noisePredictor <- rnorm(n)

# Backward selection: removes predictors sequentially from the given model

# Starting from the model with all the predictors
modAll <- lm(formula = Price ~ ., data = wineNoise)
MASS::stepAIC(modAll, direction = "backward", k = log(n))
```

### 分类模型

#### 根据正负样本比例划分 (阈值)

```r
# 根据正负样本比例设置阈值
m = mean(as.integer(as.character(rtb$dc))) # 计算正负样本比例
pred.class = as.integer(glm.pred > quantile(glm.pred, 1-m))
table(rtb$dc, pred.class)
```

#### ROC 曲线 & AUC

好像可以直接 plot (包括了 AUC)

```r
glm.pred = predict(glm.fit2, data.test, type="response")
glm.roc = pROC::roc(rtb$dc, glm.pred)

plot(glm.roc, print.auc=TRUE, auc.polygon=TRUE, grid=c(0.1, 0.2),
     max.auc.polygon=TRUE, auc.polygon.col="skyblue",
     # print.thres=TRUE,
     main = "预测ROC曲线", xlim = c(1,0),
     xlab = "特异度",ylab = "敏感度"
     )
```

另一种方式

```r
library(pROC) # 加载包
library(ROCR)
par(mfrow = c(1, 2))

pre <- predict(glm.fit,type='response')  # 对总体回归结果计算AUC值、绘制ROC曲线
pred <- prediction(pre, hot.pot$log.sales.code)
# performance(pred,'auc')@y.values # 计算AUC值
perf <- performance(pred,'tpr','fpr')
plot(perf) # 绘制ROC曲线

pre <- predict(logit.aic, type='response')  # 对AIC的结果计算AUC值、绘制ROC曲线
pred <- prediction(pre,hot.pot$log.sales.code)
# performance(pred,'auc')@y.values # 计算AUC值
perf <- performance(pred,'tpr','fpr')
plot(perf) # 绘制ROC曲线
```

#### 逻辑回归 Logistic

```r
glm.fit = glm(sales.code~.,family='binomial',data=fold.train) # 逻辑回归

glm.probs = predict(glm.fit,fold.test,type='response') # 计算概率
glm.pred = rep(F,dim(fold.test)[1])
glm.pred[glm.probs>.5]=T # 模型预测结果
prate = mean(glm.pred==fold.test$sales.code) # 正确率
```

#### LDA

```r
library(MASS) # 加载包，调用lda

lda.fit = lda(sales.code~.,data=fold.train) # LDA

lda.pred = predict(lda.fit,fold.test)$class # 模型预测结果
prate=mean(lda.pred==fold.test$sales.code) # 正确率
```

#### 朴素贝叶斯 NaiveBayes

```r
# 需要因子类型变量, 可以这样写
hot.pot.nb=hot.pot
for(i in 1:dim(hot.pot.nb)[2]){
  hot.pot.nb[,i]=as.factor(t(hot.pot.nb[,i])) # 转变为factor类型
}

library(e1071) # 加载包，调用naiveBayes

# naiveBayes
nb.fit = naiveBayes(sales.code~.,data=fold.train)
nb.class = predict(nb.fit,fold.test) # 模型预测结果
prate=mean(nb.class==fold.test$sales.code) # 正确率
```

#### kNN

```r
library(class) # 加载包，调用knn

# 生成knn函数输入数据: train, test, cl
train.X = fold.train[,-23]
train.X = cbind(train.X$discount,train.X$time.duration,train.X$评分,train.X$online.intervel,train.X$HighFreq,train.X$log.price)
test.X = fold.test[,-23]
test.X = cbind(test.X$discount,test.X$time.duration,test.X$评分,test.X$online.intervel,test.X$HighFreq,test.X$log.price)
train.direction = t(as.vector(fold.train[,23])) # cl

knn.pred = knn(train.X,test.X,train.direction, k=1)
prate = mean(knn.pred==fold.test$sales.code) # 正确率
```

### PCA

```r
baseball_pca <- baseball_tbl %>%
  select(g,ab,r,h,X2b,X3b,hr,rbi,sb,cs,sh,sf) %>% 
  filter(g>=0,ab>=0,r>=0,h>=0,X2b>=0,X3b>=0,hr>=0,rbi>=0,sb>=0,cs>=0,sh>=0,sf>=0)
pca_model <- baseball_pca %>% 
  ml_pca()
pca_model
summary(pca_model)
```

#### PVE & CVE

就是统计各个变量对方差的贡献程度

```r
# PVE
plot(pca_model$explained_variance / sum(pca_model$explained_variance), 
     ylab="Prop. Variance Explained", 
     xlab="Principle Component")
lines(pca_model$explained_variance / sum(pca_model$explained_variance))

# CVE
plot(cumsum(pca_model$explained_variance)/sum(pca_model$explained_variance), 
     ylab="Cumulative Prop. Variance Explained",
     xlab="Principle Component")
lines(cumsum(pca_model$explained_variance)/sum(pca_model$explained_variance))
```

#### 比较PCA和理论值

```r
baseball_l <- collect(baseball_pca)
cov_baseball_pca <- cov.wt(baseball_l)$cov # 得到协方差矩阵
eigen_values = eigen(cov_baseball_pca)$value
eigen_values

# (1) 计算出来的特征值
print(cumsum(eigen_values)/sum(eigen_values))
# (2) PCA得到的结果
evs = pca_model$explained_variance %>% unname()
print(cumsum(evs)/sum(evs))
```

### 树模型：CART&Random Forest&Boosting


```r
# 随机森林
library(randomForest)
# 决策树
library(rpart)
library(rpart.plot)
# boosting 仅分类
library(adabag)
# boosting
library(gbm)

# 数据处理&模型评估
library(caret)
library(pROC)
```

