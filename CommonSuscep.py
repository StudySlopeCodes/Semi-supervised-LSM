# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import GradientBoostingClassifier
import xgboost
from xgboost import XGBClassifier
from sklearn import svm


from sklearn.model_selection import *
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, confusion_matrix, recall_score
from sklearn.metrics import precision_score, f1_score, roc_auc_score, classification_report
import matplotlib.pyplot as plt
import warnings



# 数据构造
AllData = pd.read_excel(r'D:\software\arcgis\可解释机器学习\可解释机器学习基本数据\InputInter.xlsx')
lenData = 6000
FeatureData = AllData.iloc[0:lenData, 2:8].values
LabelData = AllData.iloc[0:lenData, 8:9].values

#构建训练集和测试集
NumTrain = 20
AllRocDT = []
AllRocRF = []
AllRocBP = []
AllRocSVM = []

Trainx, Testx, Trainy, Testy = train_test_split(FeatureData, LabelData, test_size = 0.2, random_state=None)

##-----构建预测模型-----##
#--DT
ClassifierDT =DecisionTreeClassifier()
DT = ClassifierDT.fit(Trainx, Trainy)
DTResult = DT.predict_proba(Testx)[:,1]
DTClass = DT.predict(Testx)

#--RF
ClassifierRF = RandomForestClassifier()
RF = ClassifierRF.fit(Trainx, Trainy)
RFResult = RF.predict_proba(Testx)[:, 1]
RFClass = RF.predict(Testx)

#--BP
ClassifierBP = MLPClassifier(hidden_layer_sizes= [5, 5], activation= 'relu', solver= 'adam', learning_rate_init = 0.001, max_iter = 8000)
BP = ClassifierBP.fit(Trainx, Trainy)
BPResult = BP.predict_proba(Testx)[:,1]
BPClass = BP.predict(Testx)

#--SVC
ClassiferSvc = svm.SVC(C=10,kernel='rbf',gamma=2,decision_function_shape='ovr', probability= True)
SVC = ClassiferSvc.fit(Trainx, Trainy)
SVCResult = SVC.predict_proba(Testx)[:,1]
SVCClass = SVC.predict(Testx)

#--GBM模型
ClassiferGBM = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0,max_depth=1, random_state=1)
GBM = ClassiferGBM.fit(Trainx, Trainy)
GBMResult = GBM.predict_proba(Testx)[:,1]
GBMClass = GBM.predict(Testx)

#--XGBoost sklearn
ClassifierXGB= XGBClassifier(n_estimators = 20, learning_rate = 0.01, max_depth = 5)
XGB = ClassifierXGB.fit(Trainx, Trainy)
XGBResult = XGB.predict_proba(Testx)[:,1]
XGBClass = XGB.predict(Testx)



##----模型精度评价----##
# 计算Accur
AccuDT = accuracy_score(Testy, DTClass)
AccuRF = accuracy_score(Testy, RFClass)
AccuBP = accuracy_score(Testy, BPClass)
AccuSVC = accuracy_score(Testy, SVCClass)
AccuGBM = accuracy_score(Testy, GBMClass)
AccuXGB = accuracy_score(Testy, XGBClass)
Accuracy = [AccuDT, AccuRF, AccuBP, AccuSVC, AccuGBM, AccuXGB]

# 计算ROC
RocAucDT = roc_auc_score(Testy, DTResult)
RocAucRF = roc_auc_score(Testy, RFResult)
RocAucBP = roc_auc_score(Testy, BPResult)
RocAucSVC = roc_auc_score(Testy, SVCResult)
RocAucGBM = roc_auc_score(Testy, GBMResult)
RocAucXGB = roc_auc_score(Testy, XGBResult)
RocAuc = [RocAucDT, RocAucRF, RocAucBP, RocAucSVC, RocAucGBM, RocAucXGB]

# 计算F1_Score
F1ScorDT = f1_score(Testy, DTClass)
F1ScorRF = f1_score(Testy, RFClass)
F1ScorBP = f1_score(Testy, BPClass)
F1ScorSVC = f1_score(Testy, SVCClass)
F1ScorEBM = f1_score(Testy, EBMClass)
F1ScorGBM = f1_score(Testy, GBMClass)
F1ScorXGB = f1_score(Testy, XGBClass)

F1Score = [F1ScorDT, F1ScorRF, F1ScorBP, F1ScorSVC, F1ScorGBM, F1ScorXGB]

# 计算kappa
def kappaCal(matrix):
    n = np.sum(matrix)
    sum_po = 0
    sum_pe = 0
    for i in range(len(matrix[0])):
        sum_po += matrix[i][i]
        row = np.sum(matrix[i, :])
        col = np.sum(matrix[i, :])
        sum_pe += row * col
    po = sum_po / n
    pe = sum_pe / (n * n)
    return (po - pe) / (1 - pe)

matrixDT = confusion_matrix(Testy, DTClass)
KappaDT = kappaCal(matrixDT)
matrixRF = confusion_matrix(Testy, RFClass)
KappaRF = kappaCal(matrixRF)
matrixBP = confusion_matrix(Testy, BPClass)
KappaBP = kappaCal(matrixBP)
matrixSVC = confusion_matrix(Testy, SVCClass)
KappaSVC = kappaCal(matrixSVC)
matrixGBM = confusion_matrix(Testy, GBMClass)
KappaGBM = kappaCal(matrixGBM)
matrixXGB = confusion_matrix(Testy, XGBClass)
KappaXGB= kappaCal(matrixXGB)

Kappa = [KappaDT, KappaRF, KappaBP, KappaSVC, KappaEBM, KappaGBM, KappaXGB]


##----读取研究区所有栅格数据----##
StudyData = pd.read_csv(r'D:\software\arcgis\可解释机器学习\可解释机器学习基本数据\StudyPoint.txt')
ObjectId = StudyData.iloc[:, 0:1]
FeatureData = StudyData.fillna(value = 0).iloc[:,1:7]

# 计算研究区敏感性
DTSuscep = pd.DataFrame(DT.predict_proba(FeatureData)[:,1])
RFSuscep = pd.DataFrame(RF.predict_proba(FeatureData)[:,1])
BPSuscep = pd.DataFrame(BP.predict_proba(FeatureData)[:,1])
SVCSuscep = pd.DataFrame(SVC.predict_proba(FeatureData)[:,1])
GBMSuscep = pd.DataFrame(GBM.predict_proba(FeatureData)[:,1])
XGBSuscep = pd.DataFrame(XGB.predict(xgboost.DMatrix(FeatureData[:, 1])))


# 输出研究区敏感性
TurkeySuscep = pd.concat([ObjectId, DTSuscep, RFSuscep, BPSuscep, SVCSuscep, GBMSuscep, XGBSuscep],axis = 1)
TurkeySuscep.to_csv(r'C:\Users\ZhiYong\Desktop\WenchuanSuscep.txt', index = True)



