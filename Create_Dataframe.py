#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 11:24:49 2021

@author: fredericayme
"""


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




def CreateDataFrame(ArrayFolder,DataframeFolder):

    if not os.path.exists(DataframeFolder):
        os.makedirs(DataframeFolder)

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
        Machine=machine
        ID=f[-15:-13]
        file=f[-12:-4]
        
        list.append([Machine,ID,file,Target_Ano,Arrays])
        
        i=i+1
    
    filename_t=DataframeFolder+'Df_t.csv'
    filename_f=DataframeFolder+'Df_f.csv'
    
    df_target=pd.DataFrame(list,columns=['Machine','ID','file','Target_ano','image'])
    df_features=pd.DataFrame(features)
    df_target.to_parquet(filename_t)
    df_features.to_parquet(filename_f)
    return df_target,df_features
 
           
  
        
#machines = ['fan', 'pump', 'slider', 'ToyCar', 'ToyConveyor', 'valve']
            
        
machines = ['fan']
sets = ['train_png_arrays']


for machine in machines:
    for s in sets:
       DataframeFolder='/Users/fredericayme/OneDrive/Documents/Projet -Indep/The Datascientest/Projet Son/Data/'+machine+'/'+s+'_df/'
       ArrayFolder='/Users/fredericayme/OneDrive/Documents/Projet -Indep/The Datascientest/Projet Son/Data/'+machine+'/'+s+'/'

    #Creer le dataframe d'entrainement
    df_target,df_features =  CreateDataFrame(ArrayFolder,DataframeFolder)









#ImportArraystoDF(ArrayFolder)
        
        # s.showMelSpectrogram()
        
        # plt.show()