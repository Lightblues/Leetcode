对于五个样本点, 真实 11000, 预测概率 0.4 0.8 0.2 0.4 0.5, 求AUC

AUC, 即 Area under curve, 是ROC曲线 (receiver operating characteristic curve) 曲线下方的面积. 其横坐标是 FPR(false positive rate, 负样本有多少被误召回了), 纵坐标是 TPR(true positive rate, 也就是正样本召回率recall). 
除了画出曲线计算下方面积之外, 我们可以证明, 若定义「排序损失」l 为所有正负样本对中, 正样本得分更小的概率, 则 AUC = 1 - l.
本题中, 有 l = 1/(2*3) * (1 + .5) = 0.25. 因此, 有 AUC = 0.75. 

