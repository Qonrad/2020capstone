from scipy.io import loadmat
import os
import pandas as pd
import numpy as np
#/Users/Conrad/Box/Conrad Leonik Capstone/data/connectivity/connectivity_matrices/resultsROI_Subject002_Condition001.mat
path = '../../data/connectivity/connectivity_matrices'
scores = pd.read_csv("./out.tsv", sep="\t")
conn_key = pd.read_csv("../../data/connectivity/conn_key")
files = []
#fixing subject IDs in conn_key
for idx, row in conn_key.iterrows():
    conn_key.loc[idx, 'ID'] = "A000" + str(conn_key.loc[idx, 'ID'])
#getting the subset of subjects with scores (only ones that also have connectivity matrices)
scores = pd.merge(scores, conn_key, how='right', on='ID')
print(scores)
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if 'resultsROI' in file:
            files.append(os.path.join(r, file))
X = np.array([np.zeros(164 * 167)]) #quite possibly unnecessarily complicated, unsure how to do this
#it absolutely must be checked that the scores match up properly with the correct connectivity matrix
for i in range(len(files)):
    #print(files[i])
    #print(scores.ID.values[i])
    connectome = loadmat(files[i])
    #quite possibly unnecessarily complicated, unsure how to do this
    longarray = np.array([np.array(connectome['Z'].reshape(164 * 167).tolist())])
    #print(longarray)
    #print(X)
    X = np.concatenate((X, longarray), axis=0)
    #print(longarray)
X = X[1:]
y = scores.skourascore_down.values
#print(X.shape)
#print(y.shape)
