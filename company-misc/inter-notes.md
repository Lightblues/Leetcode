
## 数据结构

### 堆 heap

如何调整变成堆? 从中间的节点开始往上走到root, 每次调整使得该节点所定义的子树是满足堆的条件的! 
参见 [here](https://blog.csdn.net/xiaomucgwlmx/article/details/103522410) 的图.
也可以直接用Python包来模拟! 

```python
q = [7,11,23,32,16,9,12,45,27]
q = [-i for i in q]
heapq.heapify(q)
q = [-i for i in q]
print(q)
```

初始序列为 `1 8 6 2 5 4 7 3` 的一组数采用堆排序，当建堆(小根堆)完毕时，堆所对应的二叉树中序遍历序列为
[8 3 2 5 1 6 4 7]


### AVL树（平衡二叉树）

定义「失衡」为某一节点的左右子树高度差大于1, 为了保证树的平衡, AVL树的插入和删除操作都可能进行旋转操作.
旋转操作: 从失衡的点到新插入的点的路径上的三个点, 取中位数作为新的父节点, 进行「旋转」. 
具体参见下面的例子! 
[note](https://zhuanlan.zhihu.com/p/165939383)


## CNN

[paddle](https://paddlepedia.readthedocs.io/en/latest/tutorials/CNN/convolution_operator/index.html) 卷积算子

- 空洞卷积 (Dilated Convolutions) Atrous Convolution; 中文名也叫膨胀卷积或者扩张卷积
    - [note](https://zhuanlan.zhihu.com/p/113285797)
    - 空洞卷积可以增大感受野,但是可以不改变图像输出特征图的尺寸(分辨率,resolution)
- 分组卷积 (Group Convolution)
    - [paddle](https://paddlepedia.readthedocs.io/en/latest/tutorials/CNN/convolution_operator/Group_Convolution.html)
- 可分离卷积 (Separable Convolution)
    - [here](https://zhuanlan.zhihu.com/p/166736637)


## 聚类算法

聚类指标: 核心围绕是否有参考, 分为内部和外部指标. 
[here](https://zhuanlan.zhihu.com/p/260137686)

