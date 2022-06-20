# -*- coding: utf-8 -*-
"""
Created on Fri May  6 14:43:05 2022

@author: lucas
"""

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate

import statsmodels.api as sm
import statsmodels.formula.api as smf

from numpy import mean
from numpy import absolute
from numpy import sqrt
import pandas as pd



#df = pd.DataFrame({'y': [6, 8, 12, 14, 14, 15, 17, 22, 24, 23],
    #               'x1': [2, 5, 4, 3, 4, 6, 7, 5, 8, 9],
      #             'x2': [14, 12, 12, 13, 7, 8, 7, 4, 6, 5]})

df_k = pd.read_excel(
    r'C:\Users\lucas\OneDrive\Bureaublad\dataset-modelleren.xlsx',sheet_name= 'Sheet2')

combo = []

col = list(df_k.columns)

X = df_k[[col[1], col[2], col[3], col[4],col[5],col[6],col[7],col[8],col[9],
          col[10],col[11],col[12],col[13],col[14],col[15],col[16],col[17],
          col[18],col[19],col[21]]]
y = df_k['MODEL-TH|Modelleren theorie']



#define cross-validation method to use
cv = KFold(n_splits=5, random_state=1, shuffle=True)

#build multiple linear regression model
model = LinearRegression()


#use k-fold CV to evaluate model
scores = cross_val_score(model, X, y, scoring='neg_mean_absolute_error',
                         cv=cv, n_jobs=-1)

v = mean(absolute(scores))


print(v)
print(absolute(scores))


#cv_result = cross_validate(model, X,  y, scoring='neg_mean_absolute_error',
                        # cv=cv,  n_jobs=-1, return_estimator= True)







#print(min(combo)