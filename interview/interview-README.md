参见 list [interview](https://github.com/stars/Lightblues/lists/leetcode)

- ML-NLP: <https://github.com/NLP-LOVE/ML-NLP> 停更于2020 #todo



================
问题list

- [为什么回归问题不能用Dropout](https://zhuanlan.zhihu.com/p/561124500) NLP分类中可以采用Dropout. 但回归可能引入误差
    - 原因是, 虽然Dropout不会对均值产生影响, 但会影响方差, 经过非线性层之后发生变化.
    - 而Dropout由于在训练和测试过程中逻辑不一致, 导致训练和测试的输出分布差异.
