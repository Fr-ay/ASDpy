#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 15 15:15:55 2021

doc: 
preparation of data sets:
    generate charts about amount of data
    --- todo: ---
    generate metadata file
    generate spectograms in folders
"""

import pandas as pd
from os.path import isfile, join
import os
import seaborn as sns
import matplotlib.pyplot as plt

rootFolder = '/Users/fredericayme/OneDrive/Documents/Projet -Indep/The Datascientest/Projet Son/Data/'
# rootFolder = 'data/'

# list_datasets = ['fan', 'pump', 'ToyCar', 'slider', 'ToyConveyor', 'valve']  # folders in rootFolder
list_datasets = ['fan', 'pump', 'ToyCar'] # folders david


# list_datasets_train = ['fan', 'ToyCar', 'pump']  # folders in rootFolder
# list_datasets_train = ['fan'] # test
# list_datasets_validation = ['slider', 'valve'] # folders in rootFolder

def countInFolder():
    # count all files in folders
    list_folders= []
    list_stats= []

    for folder in list_datasets:
        # train_folder = './' + folder + '/train/'
        train_folder = rootFolder + folder + '/train/'
        
        print('f=', train_folder)

        wavFilesTrain = [f for f in os.listdir(train_folder) if isfile(join(train_folder, f))]
        if '.DS_Store' in wavFilesTrain: wavFilesTrain.remove('.DS_Store')
        list_folders.append(train_folder)
        list_stats.append(len(wavFilesTrain))
    

    df_train = pd.DataFrame(data = {'folder': list_folders, 'nb': list_stats})
    df_train.head()


def data_allFilesByType(typeFolder):
    # typeFolder : 'train' or 'test'
    list_files = []
    list_folders = []
    list_size = []
    list_type = []

    # get a df with all files and categories
    for folder in list_datasets:
        rel_folder =  folder + '/' + typeFolder
        full_folder = rootFolder + '/' + rel_folder + '/'
        print('full_folder=', full_folder)
        wavFilesTrain = [f for f in os.listdir(full_folder) if isfile(join(full_folder, f))]
        if '.DS_Store' in wavFilesTrain: wavFilesTrain.remove('.DS_Store')

        for f in wavFilesTrain:
            # f : filename (ex : normal_id_06_00000092.wav)
            list_files.append(f)

            # rel_folder : directory (ex : valve/test/)
            list_folders.append(rel_folder)

            # append file size in bytes
            list_size.append(os.path.getsize(full_folder + '/' + f))

            # append file type (normal/anomalous)
            list_type.append(f.split('_')[0])

    return(list_folders, list_files, list_size, list_type)


def data_allFiles():
    # for each filde in folders "train" & "test", get folder name, file name, file size
    list_folder1, list_files1, list_size1, list_type1 = data_allFilesByType('train')
    list_folder2, list_files2, list_size2, list_type2 = data_allFilesByType('test')

    list_folder1.extend(list_folder2)
    list_files1.extend(list_files2)    
    list_size1.extend(list_size2)
    list_type1.extend(list_type2)

    return ({'folder': list_folder1, 'file': list_files1, 'size': list_size1, 'type': list_type1})

countInFolder()

df = pd.DataFrame(data = data_allFiles()) # init df: list of all files in all folders
#ns.countplot(y="folder", data=df); # number of files in each folder
sns.countplot(data=df, y="folder", hue="type");

# sns.countplot(x="size", data=df_train); # compare sizes files
#df.boxplot(column= 'size', by='folder', figsize= (7,7)); # compare sizes files
plt.show()

#df_plot = df.groupby(['folder', 'type']).size().reset_index().pivot(columns='type', index='folder', values=0)
#df_plot.plot(kind='barh', stacked=True, color=['red', 'green'], figsize = (25,7))
#plt.show()

# create new columns
df['machine'] = df.apply(lambda x: x['folder'].split('/')[0], axis =1)
df['step'] = df.apply(lambda x: x['folder'].split('/')[1], axis =1)
df['data'] = df['step'] + ' ' + df['type']

# affichage de la répartion absolue des données pour chaque machine
print(df.head(10))
df_plot = df.groupby(['machine', 'data']).size().reset_index().pivot(columns='data', index='machine', values=0)
print(df_plot.head(10))
df_plot.plot(kind='barh', stacked=True,
             color=['orangered', 'lime', 'limegreen'], figsize = (25,7),
             title='Répartition absolue des données')
plt.show()

# affichage de la répartion relative des données pour chaque machine
df_plot_pc = pd.DataFrame()
samples = df_plot['test anomaly'] + df_plot['test normal'] + df_plot['train normal']
df_plot_pc['train normal'] = df_plot['train normal'] / samples
df_plot_pc['test normal'] = df_plot['test normal'] / samples
df_plot_pc['test anomaly'] = df_plot['test anomaly'] / samples
print(df_plot_pc.head(10))
df_plot_pc.plot(kind='barh', stacked=True,
                color=['limegreen', 'lime', 'orangered'], figsize = (25,7),
                title='Répartition relative des données')
plt.show()