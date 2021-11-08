#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 16:57:32 2021

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




def convertImageInArray(imageFolder, ArrayFolder):

    if not os.path.exists(ArrayFolder):
        os.makedirs(ArrayFolder)
    
    Imfiles = [f for f in listdir(imageFolder) if isfile(join(imageFolder, f))]
        # wavfiles.remove('.DS_Store')
    for f in Imfiles:
        if f[-4:] != '.png':
            # ignore non .pngfiles
            continue

        img= Image.open(imageFolder+f)
        if img.size != (313,128):
            img= img.resize((313,128))
        img_array= np.array(img)
        filename=ArrayFolder+f[:-4]+'.txt'
        np.savetxt(filename,img_array.astype(int), fmt='%i', delimiter=",")
            
        
machines = ['fan', 'pump', 'slider', 'ToyCar', 'ToyConveyor', 'valve']
sets = ['train_png', 'test_png']

for machine in machines:
    for s in sets:
        imageFolder='/Users/fredericayme/OneDrive/Documents/Projet -Indep/The Datascientest/Projet Son/Data/'+machine+'/'+s+'/'
        ArrayFolder='/Users/fredericayme/OneDrive/Documents/Projet -Indep/The Datascientest/Projet Son/Data/'+machine+'/'+s+'_arrays'+'/'
        convertImageInArray(imageFolder,ArrayFolder)
        
        # s.showMelSpectrogram()
        
        # plt.show()

