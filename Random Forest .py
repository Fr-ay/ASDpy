#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 20:15:51 2021

@author: fredericayme

#Tester un modèle de forêt alétoire sur les données contenues dans le Dataframe en appliquant une reduction de dimension PCA pour réduire les featurees
"""

from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from imblearn.under_sampling import RandomUnderSampler,  ClusterCentroids
from imblearn.metrics import classification_report_imbalanced, geometric_mean_score
from sklearn.metrics import f1_score
from sklearn.svm import SVC
from sklearn import neighbors
from sklearn import datasets
from sklearn.model_selection import train_test_split


pca = PCA(n_components = 0.9)
pca.fit(data)
print("Nombre de composantes retenues :", pca.n_components_)


plt.figure()
plt.xlim(0,100)
plt.plot(pca.explained_variance_ratio_);

plt.figure()
plt.xlim(0,100)
plt.axhline(y = 0.9, color ='r', linestyle = '--')
plt.plot(pca.explained_variance_ratio_.cumsum());



X_test_pca=pca.transform(X_test)
X_test_pca.shape

from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.preprocessing import StandardScaler

X_train, X_test, y_train, y_test = train_test_split(data_pca,target,test_size = .2)


clf = RandomForestClassifier(n_jobs = -1,max_features='sqrt',n_estimators=1600)
# L'argument n_jobs vaut -1 par défaut. Il permet de forcer le processeur à utiliser toute sa puissance de calcul parallèle.
clf.fit(X_ru_pca, y_ru)
print(clf.score(X_ru_pca, y_ru))
clf.score(X_test_pca, y_test)

"""
from·sklearn.ensemble·import·RandomForestClassifierclf·=·RandomForestClassifier(n_jobs·=·-1,max_features='sqrt',n_estimators=1600)#·L'argument·n_jobs·vaut·-1·par·défaut.·Il·permet·de·forcer·le·processeur·à·utiliser·toute·sa·puissance·de·calcul·parallèle.clf.fit(X_ru_pca,·y_ru)print(clf.score(X_ru_pca,·y_ru))clf.score(X_test_pca,·y_test)

 1.0
0.8030009680542111
"""

Y_pred=clf.predict(X_test_pca)
print(classification_report_imbalanced(y_test, Y_pred))
pd.crosstab(y_test,Y_pred)

"""
                   pre       rec       spe        f1       geo       iba       sup

          0       0.94      0.82      0.74      0.87      0.78      0.61      5144
          1       0.45      0.74      0.82      0.56      0.78      0.60      1054

avg / total       0.86      0.80      0.75      0.82      0.78      0.60      6198

col_0	0	1
Target_ano		
0	4202	942
1	279	775
"""




