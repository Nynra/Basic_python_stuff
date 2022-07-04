# -*- coding: utf-8 -*-
"""
Created on Sat May  7 10:54:30 2022

@author: lucas
"""


import pandas as pd # for data manipulation
import numpy as np # for data manipulation


from sklearn.model_selection import train_test_split # for splitting the data into train and test samples
from sklearn.metrics import classification_report # for model evaluation metrics
from sklearn.preprocessing import MinMaxScaler # for feature scaling
from sklearn.preprocessing import OrdinalEncoder # to encode categorical variables
from sklearn.neighbors import KNeighborsClassifier # for KNN classification
from sklearn.neighbors import KNeighborsRegressor # for KNN regression

import matplotlib.pyplot as plt # for data visualization
import plotly.express as px # for data visualization


df = pd.read_excel(
    r'C:\Users\lucas\OneDrive\Bureaublad\dataset-modelleren.xlsx',sheet_name= 'modelleren')




df['mod band'] = pd.qcut(df['MODEL-TH|Modelleren theorie'], 3, labels=['bottom 33', 'middle 33', 'top 33'])

"""
# Create a 3D scatter plot
fig = px.scatter_3d(df, x=df['BSTAT-THI Beschrijvende Statistiek'], y=df['KVERD-TH|Kansverdelingen theorie'], z=df['MODEL-TH|Modelleren theorie'],
                    color=df['mod band'],
                   )

# Update chart looks
fig.update_layout(#title_text="Scatter 3D Plot",
                  showlegend=True,
                  legend=dict(orientation="h", yanchor="top", y=1, xanchor="center", x=0.5),
                  scene_camera=dict(up=dict(x=0, y=0, z=1),
                                        center=dict(x=0, y=0, z=-0.2),
                                        eye=dict(x=-1.5, y=1.5, z=0.5)),
                                        margin=dict(l=0, r=0, b=0, t=0),
                  scene = dict(xaxis=dict(backgroundcolor='white',
                                          color='black',
                                          gridcolor='#f0f0f0',
                                          title_font=dict(size=10),
                                          tickfont=dict(size=10),
                                          dtick=0.01,
                                         ),
                               yaxis=dict(backgroundcolor='white',
                                          color='black',
                                          gridcolor='#f0f0f0',
                                          title_font=dict(size=10),
                                          tickfont=dict(size=10),
                                          dtick=0.01,
                                          ),
                               zaxis=dict(backgroundcolor='lightgrey',
                                          color='black',
                                          gridcolor='#f0f0f0',
                                          title_font=dict(size=10),
                                          tickfont=dict(size=10),
                                          dtick=5
                                         )))

# Update marker size
fig.update_traces(marker=dict(size=2))

fig.show()
"""




#---------- Step 1 - Preprocess data
# Do Min-Max scaling
scaler = MinMaxScaler()
df['BSTAT-THI Beschrijvende Statistiek scl']=scaler.fit_transform(df[['BSTAT-THI Beschrijvende Statistiek']])
df['KVERD-TH|Kansverdelingen theorie scl']=scaler.fit_transform(df[['KVERD-TH|Kansverdelingen theorie']])
df['MODEL-TH|Modelleren theorie scl']=scaler.fit_transform(df[['MODEL-TH|Modelleren theorie']])

# Encode Price Band for usage as target in the classification model
enc=OrdinalEncoder() # select encoding method
df['mod band enc']=enc.fit_transform(df[['mod band']]) # encode categorical values


#---------- Step 2 - Create training and testing samples (note, we have two sets of targets (yC and yR))
# Split into train and test dataframes
df_train, df_test = train_test_split(df, test_size=0.2, random_state=42)

# Independent variables (features)
X_train=df_train[['BSTAT-THI Beschrijvende Statistiek scl', 'KVERD-TH|Kansverdelingen theorie scl', 'MODEL-TH|Modelleren theorie scl']]
X_test=df_test[['BSTAT-THI Beschrijvende Statistiek scl', 'KVERD-TH|Kansverdelingen theorie scl', 'MODEL-TH|Modelleren theorie scl']]


# Target for regression model
yR_train=df_train['MODEL-TH|Modelleren theorie'].ravel()
yR_test=df_test['MODEL-TH|Modelleren theorie'].ravel()


#---------- Step 3b - Set model parameters - Regression
modelR = KNeighborsRegressor(n_neighbors=7, #default=5
                             weights='distance', #{‘uniform’, ‘distance’} or callable, default='uniform'
                             algorithm='auto', #{‘auto’, ‘ball_tree’, ‘kd_tree’, ‘brute’}, default=’auto’
                             #leaf_size=30, #default=30, Leaf size passed to BallTree or KDTree.
                             #p=2, #default=2, Power parameter for the Minkowski metric.
                             #metric='minkowski', #default=’minkowski’, with p=2 is equivalent to the standard Euclidean metric.
                             metric_params=None, #dict, default=None, Additional keyword arguments for the metric function.
                             n_jobs=-1 #default=None, The number of parallel jobs to run for neighbors search, -1 means using all processors
                            )


#---------- Step 4 - Fit the two models
reg = modelR.fit(X_train, yR_train)


#---------- Step 5 - Predict class labels / target values
# Predict on training data
pred_values_tr = modelR.predict(X_train)

# Predict on a test data
pred_values_te = modelR.predict(X_test)


# Basic info about the model
print("")
print('****************** KNN Regression ******************')
print('Effective Metric: ', reg.effective_metric_)
print('Effective Metric Params: ', reg.effective_metric_params_)
print('No. of Samples Fit: ', reg.n_samples_fit_)
print("")
scoreR_te = modelR.score(X_test, yR_test)
print('Test Accuracy Score: ', scoreR_te)
scoreR_tr = modelR.score(X_train, yR_train)
print('Training Accuracy Score: ', scoreR_tr)

print('---------------------------------------------------------')