# -*- coding: utf-8 -*-
"""
Created on Sat May  7 16:37:06 2022

@author: lucas
"""

import numpy as np
import pandas as pd
import scipy as stats
from scipy.stats import chi2
import matplotlib.pyplot as plt


df_m = pd.read_excel(
    r'C:\Users\lucas\OneDrive\Bureaublad\dataset-modelleren.xlsx',sheet_name= 'Sheet3')
#y = data["MODEL-TH|Modelleren theorie"]

def mahalanobis(x=None, data=None, cov=None):

    x_mu = x - np.mean(df_m)
    if not cov:
        cov = np.cov(df_m.values.T)
    inv_covmat = np.linalg.inv(cov)
    left = np.dot(x_mu, inv_covmat)
    mahal = np.dot(left, x_mu.T)
    return mahal.diagonal()


# create new column in dataframe that contains Mahalanobis distance for each row


df_m['mahalanobis'] = mahalanobis(x=df_m, data=df_m)


# calculate p-value for each mahalanobis distance
df_m['p'] = 1 - chi2.cdf(df_m['mahalanobis'], 3)

# display p-values for first five rows in dataframe
df_m.head()
p_val = df_m['p'].values
print(p_val)


row = 0
p_rows = []
for i in p_val:
    if i > 0.001:
        p_rows.append("No")
    else:
        p_rows.append('Yes')

df_m['outliars'] = p_rows


#df_m.to_excel(r'C:\Users\lucas\OneDrive\Bureaublad\dataset-modelleren.xlsx', sheet_name = 'modelleren results')