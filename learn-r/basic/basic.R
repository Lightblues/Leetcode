getwd()

tax.tab <- read.csv("data/Rbook/taxsamp.csv",
                    # as.is=TRUE说明字符型列要原样读入而不是转换为因子(factor)
                    header=TRUE, as.is=TRUE)
print(head(tax.tab))
