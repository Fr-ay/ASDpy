#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from os.path import isfile, join
import os
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageFilter
from pathlib import Path
from os import listdir
from joblib import dump, load

def CreateDataFrame(ArrayFolder):

    #Scenario- Using a non Deep learning approach
    #Create a dataframe for each equipment containing all the related files (the arrays), 1 array file = 1 line in the dataframe)

    #if not os.path.exists(DataframeFolder):
        #os.makedirs(DataframeFolder)

    Imfiles = [f for f in listdir(ArrayFolder)if isfile(join(ArrayFolder,f))]
    # wavfiles.remove('.DS_Store')

    list=[]

    i=0
    Target_Ano=0
    Machine=""
    ID=0
    file=""
    Arrays_f = np.empty([0, 40064])
    features=[]


    for f in Imfiles:

        print(i)
        if f[-4:] != '.txt':
            # ignore non .pngfiles
            continue

        Arrays = np.loadtxt(join(ArrayFolder,f),dtype=int,delimiter=",")
        Arrays = Arrays.reshape(1,-1)
        features.append(Arrays.tolist())

        #Ajout de l'array


        if f[0]=="a":
          Target_Ano=1
        else:
          Target_Ano=0

        Machine=machine
        ID=f[-15:-13]
        file=f[-12:-4]

        list.append([Machine,ID,file,Target_Ano])

        i += 1

    df_features=pd.DataFrame(features)
    df_features = pd.DataFrame(df_features[0].values.tolist())
    df_features_Conv=df_features.apply(pd.to_numeric, downcast='unsigned')
    df=pd.concat([pd.DataFrame(list,columns=['Machine','ID','file','Target_ano']),df_features_Conv],axis=1)


    return df

machines = ['fan', 'pump', 'slider', 'ToyCar', 'ToyConveyor', 'valve']
sets = ['train_png', 'test_png']
df=["df_fan_test","df_pump_test","df_slider_test","df_ToyCar_test","df_ToyConveyor_test","df_valve_test"]
i=0

for machine in machines:
    for s in sets:
      ArrayFolder='/content/drive/MyDrive/Projet Son/Data/'+machine+'/'+s+'/'
      #Creer le dataframe d'entrainement
      df[i]= CreateDataFrame(ArrayFolder)
      i += 1


df[0].to_csv('df_fan_train.csv', encoding='utf-8')
#!cp df_fan_train.csv "drive/MyDrive/Projet Son/"

df[1].to_csv('df_fan_test.csv', encoding='utf-8')
#!cp df_fan_test.csv "drive/MyDrive/Projet Son/"

df[2].to_csv('df_pump_train.csv', encoding='utf-8')
#!cp df_pump_train.csv "drive/MyDrive/Projet Son/"

df[3].to_csv('df_pump_test.csv', encoding='utf-8')
#!cp df_pump_test.csv "drive/MyDrive/Projet Son/"

df[4].to_csv('df_slider_train.csv', encoding='utf-8')
#!cp df_slider_train.csv "drive/MyDrive/Projet Son/"

df[5].to_csv('df_slider_test.csv', encoding='utf-8')
#!cp df_slider_test.csv "drive/MyDrive/Projet Son/"

df[6].to_csv('df_toycar_train.csv', encoding='utf-8')
#!cp df_toycar_train.csv "drive/MyDrive/Projet Son/"

df[7].to_csv('df_toycar_test.csv', encoding='utf-8')
#!cp df_toycar_test.csv "drive/MyDrive/Projet Son/"

df[8].to_csv('df_toyconveyor_train.csv', encoding='utf-8')
#!cp df_toyconveyor_train.csv "drive/MyDrive/Projet Son/"

df[9].to_csv('df_toyconveyor_test.csv', encoding='utf-8')
#!cp df_toyconveyor_test.csv "drive/MyDrive/Projet Son/"

df[10].to_csv('df_valve_train.csv', encoding='utf-8')
#!cp df_valve_train.csv "drive/MyDrive/Projet Son/"    

df[11].to_csv('df_valve_test.csv', encoding='utf-8')
#!cp df_valve_test.csv "drive/MyDrive/Projet Son/"  

df_valve=pd.concat((pd.read_csv('drive/MyDrive/Projet Son/df_valve_test.csv',header=0,index_col=0),pd.read_csv('drive/MyDrive/Projet Son/df_valve_train.csv',header=0,index_col=0)),axis=0)
df_fan=pd.concat((pd.read_csv('drive/MyDrive/Projet Son/df_fan_test.csv',header=0,index_col=0),pd.read_csv('drive/MyDrive/Projet Son/df_fan_train.csv',header=0,index_col=0)),axis=0)
df_pump=pd.concat((pd.read_csv('drive/MyDrive/Projet Son/df_pump_test.csv',header=0,index_col=0),pd.read_csv('drive/MyDrive/Projet Son/df_pump_train.csv',header=0,index_col=0)),axis=0)
df_slider=pd.concat((pd.read_csv('drive/MyDrive/Projet Son/df_slider_test.csv',header=0,index_col=0),pd.read_csv('drive/MyDrive/Projet Son/df_slider_train.csv',header=0,index_col=0)),axis=0)
df_toycar=pd.concat((pd.read_csv('drive/MyDrive/Projet Son/df_toycar_test.csv',header=0,index_col=0),pd.read_csv('drive/MyDrive/Projet Son/df_toycar_train.csv',header=0,index_col=0)),axis=0)
df_toyconveyor=pd.concat((pd.read_csv('drive/MyDrive/Projet Son/df_toyconveyor_test.csv',header=0,index_col=0),pd.read_csv('drive/MyDrive/Projet Son/df_toyconveyor_train.csv',header=0,index_col=0)),axis=0)

df_total=pd.concat((df_fan,df_pump,df_slider,df_toycar,df_toyconveyor,df_valve),axis=0)

target = df_total['Target_ano']
data = df_total.drop(['Machine','ID','file','Target_ano'],axis=1)