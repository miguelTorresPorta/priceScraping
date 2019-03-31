#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 23:39:04 2019

@author: migueltorresporta
"""
import pandas as pd                              # tables and data manipulations
import numpy as np

df = pd.read_csv('pisosDF.csv')





# Drop the columns that are not going to be used
dataset = df.drop(['distance',
                   'detailedType',
                   'externalReference',
                   'has360',
                   'has3DTour',
                   'hasPlan',
                   'hasVideo',
                   'numPhotos',
                   'operation',
                   'propertyCode',
                   'showAddress',
                   'suggestedTexts',
                   'thumbnail',
                   'hasLift',
                   'url'], axis=1)


dataset['district'].unique()
dataset['status'].unique()
dataset['province'].unique()
dataset['district'].unique()

dataset.dtypes

def changetogood(string):
    if type(string) != str:
        return "good"
    else:
        return string
    
dataset['status'] = dataset['status'].apply(changetogood)    

def changefloor(floor):
    if type(floor) != str:
        return 0
    if floor == "bj":
        return -1
    else:
        return int(floor)

dataset['floor'] = dataset['floor'].apply(changefloor) 




# Encoding categorical data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn import preprocessing

dataset['status'] = le.fit_transform(dataset['status'])


le = preprocessing.LabelEncoder()

labelencoder_X_1 = LabelEncoder()
dataset['label'] = le.fit_transform(df.label.values)



X[:, 1] = labelencoder_X_1.fit_transform(X[:, 1])
labelencoder_X_2 = LabelEncoder()
X[:, 2] = labelencoder_X_2.fit_transform(X[:, 2])
onehotencoder = OneHotEncoder(categorical_features = [1])
X = onehotencoder.fit_transform(X).toarray()
X = X[:, 1:]
