from __future__ import print_function
from numpy import *
# �����ѧ�����numpy�������ģ��operator
import operator
from os import listdir
from collections import Counter


def createDataSet():
    """
    �������ݼ��ͱ�ǩ
     ���÷�ʽ
     import kNN
     group, labels = kNN.createDataSet()
    """
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classify0(inX, dataSet, labels, k):
    """
    inx[1,2,3]
    DS=[[1,2,3],[1,2,0]]
    inX: ���ڷ������������
    dataSet: �����ѵ��������
    labels: ��ǩ����
    k: ѡ������ھӵ���Ŀ
    ע�⣺labelsԪ����Ŀ��dataSet������ͬ������ʹ��ŷʽ���빫ʽ.
    Ԥ���������ڷ������������������
    kNN.classify0([0,0], group, labels, 3)
    """

    # -----------ʵ�� classify0() �����ĵ�һ�ַ�ʽ----------------------------------------------------------------------------------------------------------------------------
    # 1. �������
    dataSetSize = dataSet.shape[0]
    # tile���ɺ�ѵ��������Ӧ�ľ��󣬲���ѵ���������
    """
    tile: ��-3��ʾ���Ƶ������� ��-1��2��ʾ��inx���ظ��Ĵ���
    In [8]: tile(inx, (3, 1))
    Out[8]:
    array([[1, 2, 3],
        [1, 2, 3],
        [1, 2, 3]])
    In [9]: tile(inx, (3, 2))
    Out[9]:
    array([[1, 2, 3, 1, 2, 3],
        [1, 2, 3, 1, 2, 3],
        [1, 2, 3, 1, 2, 3]])
    """
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    """
    ŷ�Ͼ��룺 �㵽��֮��ľ���
       ��һ�У� ͬһ���� �� dataSet�ĵ�һ����ľ��롣
       �ڶ��У� ͬһ���� �� dataSet�ĵڶ�����ľ��롣
       ...
       ��N�У� ͬһ���� �� dataSet�ĵ�N����ľ��롣
    [[1,2,3],[1,2,3]]-[[1,2,3],[1,2,0]]
    (A1-A2)^2+(B1-B2)^2+(c1-c2)^2
    """
    # ȡƽ��
    sqDiffMat = diffMat ** 2
    # �������ÿһ�����
    sqDistances = sqDiffMat.sum(axis=1)
    # ����
    distances = sqDistances ** 0.5
    # ���ݾ��������С��������򣬷��ض�Ӧ������λ��
    # argsort() �ǽ�x�е�Ԫ�ش�С�������У���ȡ���Ӧ��index����������Ȼ�������y��
    # ���磺y=array([3,0,2,1,4,5]) ��x[3]=-1��С������y[0]=3;x[5]=9�������y[5]=5��
    # print 'distances=', distances
    sortedDistIndicies = distances.argsort()
    # print 'distances.argsort()=', sortedDistIndicies

    # 2. ѡ�������С��k����
    classCount = {}
    for i in range(k):
        # �ҵ�������������
        voteIlabel = labels[sortedDistIndicies[i]]
        # ���ֵ��н������ͼ�һ
        # �ֵ��get����
        # �磺list.get(k,d) ���� get�൱��һ��if...else...���,����k���ֵ��У��ֵ佫����list[k];�������k�����ֵ����򷵻ز���d,���K���ֵ����򷵻�k��Ӧ��valueֵ
        # l = {5:2,3:4}
        # print l.get(3,0)���ص�ֵ��4��
        # Print l.get��1,0������ֵ��0��
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    # 3. ���򲢷��س��������Ǹ�����
    # �ֵ�� items() ���������б��ؿɱ�����(����ֵ)Ԫ�����顣
    # ���磺dict = {'Name': 'Zara', 'Age': 7}   print "Value : %s" %  dict.items()   Value : [('Age', 7), ('Name', 'Zara')]
    # sorted �еĵ�2������ key=operator.itemgetter(1) �����������˼���ȱȽϵڼ���Ԫ��
    # ���磺a=[('b',2),('a',1),('c',0)]  b=sorted(a,key=operator.itemgetter(1)) >>>b=[('c',0),('a',1),('b',2)] ���Կ��������ǰ��պ�ߵ�0,1,2��������ģ�������a,b,c
    # b=sorted(a,key=operator.itemgetter(0)) >>>b=[('a',1),('b',2),('c',0)] ��αȽϵ���ǰ�ߵ�a,b,c������0,1,2
    # b=sorted(a,key=opertator.itemgetter(1,0)) >>>b=[('c',0),('a',1),('b',2)] ������ȱȽϵ�2��Ԫ�أ�Ȼ��Ե�һ��Ԫ�ؽ��������γɶ༶����
    # sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    # return sortedClassCount[0][0]
    # 3.����max����ֱ�ӷ����ֵ���value����key
    maxClassCount = max(classCount, key=classCount.get)
    return maxClassCount
    
    # ------------------------------------------------------------------------------------------------------------------------------------------
    # ʵ�� classify0() �����ĵڶ��ַ�ʽ

    # """
    # 1. �������
    
    # ŷ�Ͼ��룺 �㵽��֮��ľ���
    #    ��һ�У� ͬһ���� �� dataSet�ĵ�һ����ľ��롣
    #    �ڶ��У� ͬһ���� �� dataSet�ĵڶ�����ľ��롣
    #    ...
    #    ��N�У� ͬһ���� �� dataSet�ĵ�N����ľ��롣

    # [[1,2,3],[1,2,3]]-[[1,2,3],[1,2,0]]
    # (A1-A2)^2+(B1-B2)^2+(c1-c2)^2
    
    # inx - dataset ʹ����numpy broadcasting���� https://docs.scipy.org/doc/numpy-1.13.0/user/basics.broadcasting.html
    # np.sum() ������ʹ�ü� https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.sum.html
    # """
	#   dist = np.sum((inx - dataset)**2, axis=1)**0.5
    
    # """
    # 2. k������ı�ǩ
    
    # �Ծ�������ʹ��numpy�е�argsort������ �� https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.sort.html#numpy.sort
    # �������ص������������ȡǰk������ʹ��[0 : k]
    # ����k����ǩ�����б�k_labels��
    # """
    # k_labels = [labels[index] for index in dist.argsort()[0 : k]]
	# """
    # 3. ���ִ������ı�ǩ��Ϊ�������
    
    # ʹ��collections.Counter����ͳ�Ƹ�����ǩ�ĳ��ִ�����most_common���س��ִ������ı�ǩtuple������[('lable1', 2)]�����[0][0]����ȡ����ǩֵ
	# """
    # label = Counter(k_labels).most_common(1)[0][0]
    # return label

    # ------------------------------------------------------------------------------------------------------------------------------------------


def test1():
    """
    ��һ��������ʾ
    """
    group, labels = createDataSet()
    print(str(group))
    print(str(labels))
    print(classify0([0.1, 0.1], group, labels, 3))


# ----------------------------------------------------------------------------------------
def file2matrix(filename):
    """
    ����ѵ������
    :param filename: �����ļ�·��
    :return: ���ݾ���returnMat�Ͷ�Ӧ�����classLabelVector
    """
    fr = open(filename)
    # ����ļ��е������е�����
    numberOfLines = len(fr.readlines())
    # ���ɶ�Ӧ�Ŀվ���
    # ���磺zeros(2��3)��������һ�� 2*3�ľ��󣬸���λ����ȫ�� 0 
    returnMat = zeros((numberOfLines, 3))  # prepare matrix to return
    classLabelVector = []  # prepare labels return
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        # str.strip([chars]) --�����Ƴ��ַ���ͷβָ�����ַ����ɵ����ַ���
        line = line.strip()
        # �� '\t' �и��ַ���
        listFromLine = line.split('\t')
        # ÿ�е���������
        returnMat[index, :] = listFromLine[0:3]
        # ÿ�е�������ݣ����� label ��ǩ����
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    # �������ݾ���returnMat�Ͷ�Ӧ�����classLabelVector
    return returnMat, classLabelVector


def autoNorm(dataSet):
    """
    ��һ������ֵ����������֮��������ͬ���µ�Ӱ��
    :param dataSet: ���ݼ�
    :return: ��һ��������ݼ�normDataSet,ranges��minVals����Сֵ�뷶Χ����û���õ�
    ��һ����ʽ��
        Y = (X-Xmin)/(Xmax-Xmin)
        ���е� min �� max �ֱ������ݼ��е���С����ֵ���������ֵ���ú��������Զ�����������ֵת��Ϊ0��1�����䡣
    """
    # ����ÿ�����Ե����ֵ����Сֵ����Χ
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    # ����
    ranges = maxVals - minVals
    # -------��һ��ʵ�ַ�ʽ---start-------------------------
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    # ��������Сֵ֮����ɵľ���
    normDataSet = dataSet - tile(minVals, (m, 1))
    # ����Сֵ֮����Է�Χ��ɾ���
    normDataSet = normDataSet / tile(ranges, (m, 1))  # element wise divide
    # -------��һ��ʵ�ַ�ʽ---end---------------------------------------------
    
    # # -------�ڶ���ʵ�ַ�ʽ---start---------------------------------------
    # norm_dataset = (dataset - minvalue) / ranges
    # # -------�ڶ���ʵ�ַ�ʽ---end---------------------------------------------
    return normDataSet, ranges, minVals


def datingClassTest():
    """
    ��Լ����վ�Ĳ��Է���
    :return: ������
    """
    # ���ò������ݵĵ�һ��������ѵ�����ݼ�����=1-hoRatio��
    hoRatio = 0.1  # ���Է�Χ,һ���ֲ���һ������Ϊ����
    # ���ļ��м�������
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')  # load data setfrom file
    # ��һ������
    normMat, ranges, minVals = autoNorm(datingDataMat)
    # m ��ʾ���ݵ�������������ĵ�һά
    m = normMat.shape[0]
    # ���ò��Ե����������� numTestVecs:m��ʾѵ������������
    numTestVecs = int(m * hoRatio)
    print('numTestVecs=', numTestVecs)
    errorCount = 0.0
    for i in range(numTestVecs):
        # �����ݲ���
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
        print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i]))
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print("the total error rate is: %f" % (errorCount / float(numTestVecs)))
    print(errorCount)


def img2vector(filename):
    """
    ��ͼ������ת��Ϊ����
    :param filename: ͼƬ�ļ� ��Ϊ���ǵ��������ݵ�ͼƬ��ʽ�� 32 * 32��
    :return: һά����
    �ú�����ͼ��ת��Ϊ�������ú������� 1 * 1024 ��NumPy���飬Ȼ��򿪸������ļ���
    ѭ�������ļ���ǰ32�У�����ÿ�е�ͷ32���ַ�ֵ�洢��NumPy�����У���󷵻����顣
    """
    returnVect = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32 * i + j] = int(lineStr[j])
    return returnVect


def handwritingClassTest():
    # 1. ��������
    hwLabels = []
    trainingFileList = listdir('trainingDigits')  # load the training set
    m = len(trainingFileList)
    trainingMat = zeros((m, 1024))
    # hwLabels�洢0��9��Ӧ��indexλ�ã� trainingMat��ŵ�ÿ��λ�ö�Ӧ��ͼƬ����
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]  # take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        # �� 32*32�ľ���->1*1024�ľ���
        trainingMat[i, :] = img2vector('trainingDigits/%s' % fileNameStr)

    # 2. �����������
    testFileList = listdir('testDigits')  # iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]  # take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr))
        if (classifierResult != classNumStr): errorCount += 1.0
    print("\nthe total number of errors is: %d" % errorCount)
    print("\nthe total error rate is: %f" % (errorCount / float(mTest)))


#test1()
#datingClassTest()
handwritingClassTest()