
"""
Informer, Linformer 的区别
Attention 的实现
bias 对于多次曝光但是点击少的商品? 主要解决是「长尾问题」
"""

# auc:遍历正负样本对
"""
1、正的概率大于负的，auc加1
2、正的概率等于负的，auc加0.5
3、正的概率小于负的，auc加0
"""


def AUC(label, pre):
    pos = []
    neg = []
    auc = 0
    for index,l in enumerate(label):
        if l == 0:
            neg.append(index)
        else:
            pos.append(index)
    for i in pos:
        for j in neg:
            if pre[i] > pre[j]:
                auc += 1
            elif pre[i] == pre[j]:
                auc += 0.5
    return auc * 1.0 / (len(pos)*len(neg))

from collections import Counter
def AUC(label, pre):
    pos = []
    neg = []
    auc = 0
    for l,p in zip(label, pre):
        if l == 0:
            neg.append(p)
        else:
            pos.append(p)
    pos.sort()
    neg.sort()
    npos, npeg = len(pos), len(neg)
    cnt_neg = Counter(neg)
    idx = 0
    for i,x in enumerate(pos):
        while idx < npeg and neg[idx] < x:
            idx += 1
        auc += idx
        auc += cnt_neg[x] / 2
    return auc / (npos*npeg)

def AUC(label, pre):
    """ 使用桶排序进行优化
    对于 0~1 之间划分10000个区间
    """
    pos = []
    neg = []
    auc = 0
    for l,p in zip(label, pre):
        if l == 0:
            neg.append(p)
        else:
            pos.append(p)
    N = 1000
    slotsPos = [0] * N
    slotsNeg = [0] * N
    for p in pos:
        slotsPos[int(p*N)] += 1
    for n in neg:
        slotsNeg[int(n*N)] += 1
    for i in range(1, N):
        slotsNeg[i] += slotsNeg[i-1]
    auc = 0
    for i, x in enumerate(slotsPos):
        # auc += x * slotsNeg[i]
        if i>0:
            auc += x * slotsNeg[i-1]
            auc += x * (slotsNeg[i]-slotsNeg[i-1]) / 2
        else:
            auc += x * slotsNeg[i] / 2
    return auc * 1.0 / (len(pos)*len(neg))
    


if __name__ == '__main__':
    label = [1, 0, 0, 0, 1, 0, 1, 0]
    pre = [0.9, 0.8, 0.3, 0.1, 0.4, 0.9, 0.66, 0.7]
    print(AUC(label, pre))

    from sklearn import metrics
    auc = metrics.roc_auc_score(label, pre)
    print('sklearn',auc)
