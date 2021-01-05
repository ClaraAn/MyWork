import numpy as np
from collections import Counter

#设置类型对应字典
mydict={'1':'apple','2':'mandarin','3':'orange','4':'lemon'}

#打开数据文件并处理为数组形式
def data_dispose(str,len):                                #str:文件名 len:数据长度 wid:数据特征个数
    data_matrix=np.empty([len,6],dtype=float)             #生成训练数据的特征矩阵，每条数据有五个数据，分别为类别、宽、高、颜色
    with open(str, 'r') as f:                             #对txt文件逐行进行处理
        data=f.readlines()
        signnum = 0                                         #用于保存当前处理数据的行数
        for line in data:
             data_line = line.split()
             if signnum!=0:
                data_matrix[signnum-1,0]=signnum-1
                data_matrix[signnum-1,1]=data_line[0]       #提取水果类别
                data_matrix[signnum-1,2:]=data_line[3:]     #提取水果四个特征数值
             signnum=signnum+1
    return data_matrix

#定义求平方根函数
def sqrt_result(num):
    result=num**0.5
    return result

#求两数之差求平方函数
def two_num_square(a,b):
    result=np.square(a-b)
    return result

#计算两个点之间的距离
def two_point_distence(a,b):
    sum=0
    for i in range(4):
        r=two_num_square(a[i],b[i])
        # print("当前输入数据为"+str(a[i])+"与"+str(b[i]))
        # print(r)
        sum=sum+r
        # print(sum)
    result=sqrt_result(sum)
    return result

# 计算一个test点与测试集各点的距离
# 返回从小到大排序好的距离参数
# 第一位是距离，第二位是该点对应的主键
def one_test_to_all_train_point(testPoint):
    one_point_distance_array=np.empty([49,2],dtype=float)
    for i in range(49):                                              #循环
        # print("#######################################"+str(i))
        a=two_point_distence(train_matrix[i,2:],testPoint)   #计算两个点之间的距离
        # print(a)
        one_point_distance_array[i,0] = a                            #保存距离参数
        one_point_distance_array[i,1]=i                              #保存距离参数对应的数据点
    # print(one_point_distance_array)
    one_point_distance_array=one_point_distance_array.astype(np.uint8)
    # print(one_point_distance_array)
    sorted_data=sorted(one_point_distance_array,key=lambda x:x[0])
    # print("***************************************************")
    # print(sorted_data)
    return sorted_data

#主程序
train_matrix=data_dispose('fruit_data_with_colors_train.txt',50)   #获取训练集数据
test_matrix=data_dispose('fruit_data_with_colors_test.txt',11)     #获取测试集数据
# for j in range(10):
#     print("*********************************************************************")
#     for i in range(49):
#         print("#######################################")
#         print(train_matrix[i])
#         print(train_matrix[i,2:])
#         print(test_matrix[j,2:])
# print(one_test_to_all_train_point(test_matrix[1,2:]))

#使用KNN算法对单个点进行排序,获取可能性最大的点特征返回
#输入该点的位置及KNN算法的K值
def one_data_Prediction_type(point,k):
    k=9                                                           #设置KNN算法K值
    point_num=point[0].astype(np.uint8)
    ranking_num=one_test_to_all_train_point(point[2:])           #对单个点进行全部训练集数据距离计算
    ranking=np.empty([k],dtype=int)
    #获取测试点在所有训练点中的位置
    for i in range(k):                                                   #对前k个点进行遍历，获取前几名的type
        a=ranking_num[i]
        type_id=train_matrix[a[1],0].astype(np.uint8)
        type=train_matrix[type_id,1]
        ranking[i]=type
    classification=Counter(ranking).most_common(1)[0][0]
    result=[point_num,classification]
    return  result                        #返回当前可能性最大的预测种类及其序号

#判断单点预测正误,输入变量有测试点的编号和k值
def test_true_or_false(pointnum,k):
    #取出该点的预测值和序号
    flag = False
    result=one_data_Prediction_type(test_matrix[pointnum],k)
    if result[1] == test_matrix[pointnum,1].astype(np.uint8):
        flag = True
    returns=[result,flag]
    return returns
    # true_value=test_matrix[pointnum,]

# print(test_true_or_false(4,1))

#对多个点进行预测与正确性
k=5
test_point_num=10
test_point_result = np.empty([test_point_num,3]) #用于存放测试的结果
for i in range(test_point_num):
    a=test_true_or_false(i,k)
    print(a[0][0],a[0][1],a[1])
    test_point_result[i]=[a[0][0],a[0][1],a[1]]
    print("预测的点序列号为："+str(a[0][0]))
    print("预测的种类为："+str(mydict[str(a[0][1])]))
    if a[1]==True:
        print("预测结果正确")
    else:
        print("预测结果错误")

